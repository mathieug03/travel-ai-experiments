import { NextResponse } from "next/server";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const { destination, duration, context, vibe, earthFirst } = body;

    const MISTRAL_API_KEY = process.env.MISTRAL_API_KEY;
    const MISTRAL_AGENT_ID = process.env.MISTRAL_AGENT_ID;

    if (!MISTRAL_API_KEY || !MISTRAL_AGENT_ID) {
      return NextResponse.json(getMockItinerary(destination, duration, earthFirst));
    }

    const prompt = `Plan a ${duration}-day ${context} trip to ${destination}. Vibe: ${vibe}. Earth-First: ${earthFirst}.`;

    const response = await fetch("https://api.mistral.ai/v1/conversations", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${MISTRAL_API_KEY}`
      },
      body: JSON.stringify({
        agent_id: MISTRAL_AGENT_ID,
        inputs: [{ role: "user", content: prompt }]
      })
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Mistral API Error: ${response.status} - ${errorText}`);
    }

    const data = await response.json();
    
    // Extract the message output from the outputs array
    const messageOutput = data.outputs?.find((o: any) => o.type === "message.output");
    const rawContent = messageOutput?.content;

    if (!rawContent) {
      console.error("Mistral Response Missing Content:", data);
      throw new Error("Could not extract content from Mistral response");
    }

    // Robust JSON extraction
    const cleanedJson = rawContent.replace(/```json/g, "").replace(/```/g, "").trim();
    let result = JSON.parse(cleanedJson);
    
    // NORMALIZATION: If the AI wrapped the result in a "trip" object, flatten it.
    if (result.trip) {
      result = {
        ...result.trip,
        // Ensure days vs totalDays consistency if needed
        days: result.trip.days || result.trip.itinerary
      };
    }
    
    return NextResponse.json(result);

  } catch (error) {
    console.error("Failed to generate itinerary:", error);
    return NextResponse.json({ error: "Failed to generate itinerary" }, { status: 500 });
  }
}

function getMockItinerary(destination: string, duration: number, earthFirst: boolean) {
  const days = Array.from({ length: Number(duration) }).map((_, i) => ({
    dayNumber: i + 1,
    theme: "Exploration & Discovery",
    transport: { type: "Electric Shuttle", cost: "$15", details: "Eco-friendly local transport" },
    activities: [
      { 
        time: "10:00 AM", 
        name: "Hidden Garden Walk", 
        description: "A serene walk through local flora and fauna, showcasing the natural beauty of the region.", 
        sentiment: "Loved by locals for its tranquility and scenic views." 
      }
    ],
    dining: { 
      name: "The Green Table", 
      description: "Organic farm-to-table dining experience with a focus on seasonal and local ingredients.", 
      sentiment: "Viral for its zero-waste menu and incredible flavor profile." 
    }
  }));

  return {
    destination: destination,
    totalDays: Number(duration),
    sustainabilityScore: earthFirst ? 92 : 45,
    days: days
  };
}
