"""
Test script to exercise all backend services step by step.

Usage:
    # From project root, with .env configured:
    python -m backend.test_services

    # Run a specific test:
    python -m backend.test_services carbon
    python -m backend.test_services duffel
    python -m backend.test_services gemini
    python -m backend.test_services chat
    python -m backend.test_services all
"""

import asyncio
import json
import sys
from datetime import date, timedelta

# ──────────────────────────────────────────────
# 1. Carbon Service (offline, no API key needed)
# ──────────────────────────────────────────────

def test_carbon():
    print("\n" + "=" * 60)
    print("TEST: Carbon Service")
    print("=" * 60)

    from backend.services.carbon_service import (
        get_distance_km,
        calculate_co2,
        co2_equivalence,
        compare_carbon,
    )

    # Distance calculation
    routes = [
        ("Paris", "Barcelona"),
        ("Paris", "Rome"),
        ("London", "Amsterdam"),
        ("Berlin", "Prague"),
    ]

    print("\n--- Distances ---")
    for origin, dest in routes:
        dist = get_distance_km(origin, dest)
        print(f"  {origin} → {dest}: {dist:.0f} km")

    # CO2 calculation
    print("\n--- CO2 par mode (Paris → Barcelona, ~830 km) ---")
    dist = get_distance_km("Paris", "Barcelona")
    for mode in ("train", "flight", "bus"):
        co2 = calculate_co2(mode, dist)
        print(f"  {mode:>8}: {co2:,} gCO2 ({co2/1000:.1f} kg)")

    # Equivalence
    print("\n--- Équivalences ---")
    print(f"  10 kg CO2: {co2_equivalence(10_000)}")
    print(f"  120 kg CO2: {co2_equivalence(120_000)}")

    # Full comparison
    print("\n--- Comparaison complète ---")
    for origin, dest in routes:
        result = compare_carbon(origin, dest)
        if result:
            print(f"\n  {origin} → {dest} ({result['distance_km']} km):")
            print(f"    Train: {result['train_co2_grams']:,} g ({result['train_co2_grams']/1000:.1f} kg)")
            print(f"    Avion: {result['flight_co2_grams']:,} g ({result['flight_co2_grams']/1000:.1f} kg)")
            print(f"    Économie: {result['savings_pct']}% ({result['savings_grams']/1000:.1f} kg)")

    # Unknown city
    print("\n--- Ville inconnue ---")
    result = compare_carbon("Paris", "Tombouctou")
    print(f"  Paris → Tombouctou: {result}")

    print("\n✓ Carbon service OK")


# ──────────────────────────────────────────────
# 2. Duffel Service (requires DUFFEL_ACCESS_TOKEN)
# ──────────────────────────────────────────────

async def test_duffel():
    print("\n" + "=" * 60)
    print("TEST: Duffel Service (flights via REST API)")
    print("=" * 60)

    from backend.config import get_settings
    settings = get_settings()

    if not settings.duffel_access_token:
        print("  ⚠ DUFFEL_ACCESS_TOKEN not set — skipping")
        return

    from backend.services.duffel_service import DuffelService
    duffel = DuffelService()

    # Search flights Paris → Barcelona, 2 weeks from now
    dep_date = date.today() + timedelta(days=14)
    print(f"\n--- Recherche vols: CDG → BCN, {dep_date} ---")

    try:
        flights = await duffel.search_flights(
            origin="CDG",
            destination="BCN",
            departure_date=dep_date,
            passengers=1,
        )
        print(f"  {len(flights)} offre(s) trouvée(s)")
        for flight in flights[:5]:
            print(
                f"  {flight.provider:20} | "
                f"{flight.departure.strftime('%H:%M')}→{flight.arrival.strftime('%H:%M')} | "
                f"{flight.duration_minutes}min | "
                f"{'€'+str(flight.price_eur) if flight.price_eur else 'N/A':>8} | "
                f"{flight.transfers} escale(s)"
            )

        print(f"\n✓ Duffel flights OK ({len(flights)} results)")
    except Exception as e:
        print(f"  ✗ Erreur: {e}")

    # Search stays in Barcelona
    print(f"\n--- Recherche hébergements: Barcelona, {dep_date} → {dep_date + timedelta(days=3)} ---")

    try:
        stays = await duffel.search_stays(
            city="Barcelona",
            check_in=dep_date,
            check_out=dep_date + timedelta(days=3),
            guests=1,
        )
        print(f"  {len(stays)} hébergement(s) trouvé(s)")
        for stay in stays[:5]:
            price = f"€{stay['price_eur']}" if stay.get("price_eur") else "N/A"
            print(f"  {stay['name'][:40]:40} | {price:>8} | ★{stay.get('rating', '?')}")

        print(f"\n✓ Duffel stays OK ({len(stays)} results)")
    except Exception as e:
        print(f"  ✗ Erreur stays: {e}")


# ──────────────────────────────────────────────
# 3. Gemini Service (requires GEMINI_API_KEY)
# ──────────────────────────────────────────────

async def test_gemini():
    print("\n" + "=" * 60)
    print("TEST: Gemini Service (function calling)")
    print("=" * 60)

    from backend.config import get_settings
    settings = get_settings()

    if not settings.gemini_api_key:
        print("  ⚠ GEMINI_API_KEY not set — skipping")
        return

    from backend.services.gemini_service import GeminiService
    gemini = GeminiService()

    # Test 1: Simple greeting (no tool call expected)
    print("\n--- Test 1: Greeting (pas de tool call attendu) ---")
    try:
        response = await gemini.chat("Salut ! C'est quoi Travel AI ?")
        text = response.text or ""
        has_tool_calls = any(
            part.function_call
            for part in (response.candidates[0].content.parts if response.candidates else [])
        )
        print(f"  Tool calls: {has_tool_calls}")
        print(f"  Réponse: {text[:200]}...")
        print("  ✓ Greeting OK")
    except Exception as e:
        print(f"  ✗ Erreur: {e}")

    # Test 2: Travel intent (should trigger parse_travel_intent)
    print("\n--- Test 2: Intent parsing (tool call attendu) ---")
    try:
        response = await gemini.chat(
            "Je veux aller de Paris à Barcelone début mai, 5 jours, pas trop cher"
        )

        tool_calls_found = []
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if part.function_call:
                    fn = part.function_call
                    tool_calls_found.append({
                        "name": fn.name,
                        "args": dict(fn.args) if fn.args else {},
                    })

        if tool_calls_found:
            print(f"  {len(tool_calls_found)} tool call(s):")
            for tc in tool_calls_found:
                print(f"    → {tc['name']}")
                print(f"      args: {json.dumps(tc['args'], ensure_ascii=False, indent=8)}")

                # If it's parse_travel_intent, convert to TravelIntent
                if tc["name"] == "parse_travel_intent":
                    intent = gemini.parse_intent_from_tool_call(tc["args"])
                    print(f"      → TravelIntent: {intent.model_dump_json(indent=8)}")
        else:
            print(f"  Pas de tool call (texte direct): {(response.text or '')[:200]}")

        print("  ✓ Intent parsing OK")
    except Exception as e:
        print(f"  ✗ Erreur: {e}")


# ──────────────────────────────────────────────
# 4. Full chat flow (Gemini + Carbon + Duffel)
# ──────────────────────────────────────────────

async def test_chat_flow():
    print("\n" + "=" * 60)
    print("TEST: Full chat flow (FastAPI endpoint simulation)")
    print("=" * 60)

    from backend.config import get_settings
    settings = get_settings()

    if not settings.gemini_api_key:
        print("  ⚠ GEMINI_API_KEY not set — skipping")
        return

    from backend.services.gemini_service import GeminiService
    from backend.services.duffel_service import DuffelService
    from backend.routers.chat import _handle_tool_calls

    gemini = GeminiService()
    duffel = DuffelService()

    message = "Je veux aller de Paris à Rome la semaine prochaine, 4 jours"
    print(f"\n--- Message: \"{message}\" ---")

    try:
        # Step 1: Send to Gemini
        print("\n  [1] Envoi à Gemini...")
        response = await gemini.chat(message)

        # Step 2: Handle tool calls (execute tools + send results back)
        print("  [2] Traitement des tool calls...")
        text, intent, tool_calls = await _handle_tool_calls(message, response, gemini, duffel)

        # Step 3: Display results
        print("\n  [3] Résultats:")
        if intent:
            print(f"      Intent: {intent.origin} → {intent.destination}")
            print(f"      Dates: {intent.departure_date} ({intent.duration_days}j)")
            print(f"      Budget: {intent.budget}")

        if tool_calls:
            print(f"      Tools appelés: {[tc['tool'] for tc in tool_calls]}")

            for tc in tool_calls:
                if tc["tool"] == "get_carbon_comparison" and tc.get("result"):
                    r = tc["result"]
                    print(f"      Carbone: train {r.get('train_co2_grams', '?')}g vs avion {r.get('flight_co2_grams', '?')}g")

        print(f"\n      Réponse finale:")
        for line in text.split("\n")[:15]:
            print(f"        {line}")
        if text.count("\n") > 15:
            print(f"        ... ({text.count(chr(10)) - 15} lignes de plus)")

        print("\n  ✓ Full chat flow OK")
    except Exception as e:
        print(f"  ✗ Erreur: {e}")
        import traceback
        traceback.print_exc()


# ──────────────────────────────────────────────
# 5. Affiliate links
# ──────────────────────────────────────────────

def test_affiliate():
    print("\n" + "=" * 60)
    print("TEST: Affiliate URLs")
    print("=" * 60)

    from backend.services.affiliate import (
        trainline_url,
        booking_com_url,
        get_your_guide_url,
    )

    print(f"  Trainline:     {trainline_url('Paris', 'Barcelona', '2026-05-01')}")
    print(f"  Booking.com:   {booking_com_url('Barcelona', '2026-05-01', '2026-05-05')}")
    print(f"  GetYourGuide:  {get_your_guide_url('Barcelona')}")
    print("\n✓ Affiliate URLs OK")


# ──────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────

async def main():
    # Load .env
    from dotenv import load_dotenv
    load_dotenv()

    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    tests = {
        "carbon": lambda: test_carbon(),
        "affiliate": lambda: test_affiliate(),
        "duffel": lambda: asyncio.ensure_future(test_duffel()),
        "gemini": lambda: asyncio.ensure_future(test_gemini()),
        "chat": lambda: asyncio.ensure_future(test_chat_flow()),
    }

    if target == "all":
        # Sync tests first
        test_carbon()
        test_affiliate()
        # Async tests
        await test_duffel()
        await test_gemini()
        await test_chat_flow()
    elif target in tests:
        result = tests[target]()
        if asyncio.isfuture(result) or asyncio.iscoroutine(result):
            await result
    else:
        print(f"Unknown test: {target}")
        print(f"Available: {', '.join(tests.keys())}, all")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("DONE")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
