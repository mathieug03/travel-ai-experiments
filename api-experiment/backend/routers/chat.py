from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from google.genai import types

from backend.models.intent import TravelIntent
from backend.services.gemini_service import GeminiService
from backend.services.carbon_service import compare_carbon
from backend.services.duffel_service import DuffelService

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    intent: TravelIntent | None = None


class ChatResponse(BaseModel):
    response: str
    intent: TravelIntent | None = None
    tool_calls: list[dict] | None = None


def get_gemini() -> GeminiService:
    return GeminiService()


def get_duffel() -> DuffelService:
    return DuffelService()


async def _handle_tool_calls(
    user_message: str,
    response: types.GenerateContentResponse,
    gemini: GeminiService,
    duffel: DuffelService,
) -> tuple[str, TravelIntent | None, list[dict]]:
    """Process tool calls from Gemini, execute them, and return final text."""
    intent: TravelIntent | None = None
    tool_results: list[dict] = []

    # Check if the response has function calls
    if not response.candidates or not response.candidates[0].content.parts:
        return response.text or "", None, []

    has_function_calls = False
    for part in response.candidates[0].content.parts:
        if part.function_call:
            has_function_calls = True
            fn = part.function_call
            name = fn.name
            args = dict(fn.args) if fn.args else {}

            if name == "parse_travel_intent":
                intent = gemini.parse_intent_from_tool_call(args)
                tool_results.append(
                    {"tool": name, "result": intent.model_dump(mode="json")}
                )

            elif name == "get_carbon_comparison":
                result = compare_carbon(
                    args.get("origin", ""),
                    args.get("destination", ""),
                )
                tool_results.append({"tool": name, "result": result})

            elif name == "search_transport":
                tool_results.append(
                    {
                        "tool": name,
                        "result": {"status": "search_initiated", "args": args},
                    }
                )

            elif name == "generate_itinerary":
                tool_results.append(
                    {
                        "tool": name,
                        "result": {"status": "itinerary_requested", "args": args},
                    }
                )

    if not has_function_calls:
        return response.text or "", None, []

    # Send results back to Gemini with full conversation context:
    # user message → model function call → function responses
    function_response_parts = []
    for tr in tool_results:
        function_response_parts.append(
            types.Part.from_function_response(
                name=tr["tool"],
                response=tr["result"] or {"status": "no_data"},
            )
        )

    from backend.services.gemini_service import SYSTEM_PROMPT

    followup_contents = [
        types.Content(role="user", parts=[types.Part.from_text(text=user_message)]),
        response.candidates[0].content,  # model's function call turn
        types.Content(role="user", parts=function_response_parts),
    ]

    followup = gemini.client.models.generate_content(
        model=gemini.model,
        contents=followup_contents,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
        ),
    )
    text = followup.text or ""

    return text, intent, tool_results


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    gemini: GeminiService = Depends(get_gemini),
    duffel: DuffelService = Depends(get_duffel),
):
    """Main chat endpoint — sends message to Gemini with tool use."""
    response = await gemini.chat(request.message)
    text, intent, tool_calls = await _handle_tool_calls(
        request.message, response, gemini, duffel
    )

    return ChatResponse(
        response=text,
        intent=intent,
        tool_calls=tool_calls if tool_calls else None,
    )
