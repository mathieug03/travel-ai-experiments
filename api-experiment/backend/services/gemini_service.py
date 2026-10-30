from __future__ import annotations

from google import genai
from google.genai import types

from backend.config import get_settings
from backend.models.intent import TravelIntent

SYSTEM_PROMPT = """\
Tu es Travel AI, un assistant de voyage spécialisé dans le voyage bas-carbone en Europe.
Tu aides les utilisateurs à planifier des voyages en privilégiant le train quand c'est pertinent.
Tu as accès à des outils pour chercher des transports, calculer le carbone, et construire des itinéraires.
Tu es honnête : si l'avion est significativement plus pratique, tu le dis, mais tu montres toujours la comparaison carbone.
Tu es enthousiaste sur le voyage en train sans être moralisateur.
Réponds dans la langue de l'utilisateur.
"""

# Tool declarations for Gemini function calling
TOOL_DECLARATIONS = types.Tool(
    function_declarations=[
        types.FunctionDeclaration(
            name="parse_travel_intent",
            description="Parse le message de l'utilisateur en un objet TravelIntent structuré. "
            "Appelle cet outil quand l'utilisateur exprime une envie de voyage.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "origin": types.Schema(
                        type=types.Type.STRING,
                        description="Ville ou code IATA de départ",
                    ),
                    "destination": types.Schema(
                        type=types.Type.STRING,
                        description="Ville ou code IATA de destination",
                    ),
                    "departure_date": types.Schema(
                        type=types.Type.STRING,
                        description="Date de départ au format YYYY-MM-DD",
                    ),
                    "return_date": types.Schema(
                        type=types.Type.STRING,
                        description="Date de retour au format YYYY-MM-DD",
                    ),
                    "duration_days": types.Schema(
                        type=types.Type.INTEGER,
                        description="Nombre de jours du voyage",
                    ),
                    "flexibility": types.Schema(
                        type=types.Type.STRING,
                        description="Flexibilité sur les dates: exact, flexible_few_days, flexible_week, anytime",
                    ),
                    "travelers": types.Schema(
                        type=types.Type.INTEGER,
                        description="Nombre de voyageurs",
                    ),
                    "budget": types.Schema(
                        type=types.Type.STRING,
                        description="Niveau de budget: pas cher, modéré, pas de limite",
                    ),
                    "preferences": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                        description="Préférences: train_only, no_fly, direct, overnight",
                    ),
                    "purpose": types.Schema(
                        type=types.Type.STRING,
                        description="But du voyage: city break, road trip, nature, etc.",
                    ),
                },
            ),
        ),
        types.FunctionDeclaration(
            name="search_transport",
            description="Cherche les options de transport (train + avion) pour un trajet donné",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "origin": types.Schema(
                        type=types.Type.STRING,
                        description="Ville de départ",
                    ),
                    "destination": types.Schema(
                        type=types.Type.STRING,
                        description="Ville d'arrivée",
                    ),
                    "date": types.Schema(
                        type=types.Type.STRING,
                        description="Date au format YYYY-MM-DD",
                    ),
                    "mode": types.Schema(
                        type=types.Type.STRING,
                        description="Mode de transport: train, flight, all",
                    ),
                },
                required=["origin", "destination", "date"],
            ),
        ),
        types.FunctionDeclaration(
            name="get_carbon_comparison",
            description="Compare les émissions CO₂ train vs avion pour une route",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "origin": types.Schema(
                        type=types.Type.STRING,
                        description="Ville de départ",
                    ),
                    "destination": types.Schema(
                        type=types.Type.STRING,
                        description="Ville d'arrivée",
                    ),
                },
                required=["origin", "destination"],
            ),
        ),
        types.FunctionDeclaration(
            name="generate_itinerary",
            description="Génère un itinéraire jour par jour avec hébergement et activités",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "destination_city": types.Schema(
                        type=types.Type.STRING,
                        description="Ville de destination principale",
                    ),
                    "duration_days": types.Schema(
                        type=types.Type.INTEGER,
                        description="Nombre de jours",
                    ),
                    "budget_level": types.Schema(
                        type=types.Type.STRING,
                        description="Niveau de budget",
                    ),
                    "interests": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING),
                        description="Centres d'intérêt du voyageur",
                    ),
                },
                required=["destination_city", "duration_days"],
            ),
        ),
    ]
)


class GeminiService:
    def __init__(self):
        settings = get_settings()
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    async def chat(
        self,
        message: str,
        conversation_history: list[types.Content] | None = None,
    ) -> types.GenerateContentResponse:
        """Send a message to Gemini with tool use enabled.

        Returns the raw response — the caller (chat router) is responsible
        for executing tool calls and looping back with results.
        """
        contents: list[types.Content] = []

        if conversation_history:
            contents.extend(conversation_history)

        contents.append(types.Content(role="user", parts=[types.Part.from_text(text=message)]))

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[TOOL_DECLARATIONS],
                temperature=0.7,
            ),
        )

        return response

    def parse_intent_from_tool_call(self, args: dict) -> TravelIntent:
        """Convert a parse_travel_intent tool call's arguments to a TravelIntent."""
        return TravelIntent(
            origin=args.get("origin"),
            destination=args.get("destination"),
            departure_date=args.get("departure_date"),
            return_date=args.get("return_date"),
            duration_days=args.get("duration_days"),
            flexibility=args.get("flexibility", "exact"),
            travelers=args.get("travelers", 1),
            budget=args.get("budget"),
            preferences=args.get("preferences", []),
            purpose=args.get("purpose"),
            raw_query="",
        )
