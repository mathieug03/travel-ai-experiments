# Travel AI experiments

**Archived / abandoned research prototypes for a future travel-planning platform.**

Experiments in travel API integration, structured AI output, and approximate transport/carbon comparisons.

## Two separate approaches

| Folder | Experiment | Implemented scope |
| --- | --- | --- |
| `web-experiment/` | February 2026, Next.js / TypeScript / Mistral | Trip form, itinerary rendering, server-side generation request, and mock fallback |
| `api-experiment/` | April 2026, Python / FastAPI / Gemini / Duffel | Structured travel intent, flight/stay search integration, chat tool calls, and approximate carbon comparison |

The two directories are separate experiments. Neither implements a complete booking or payment workflow.

## Inspect or run

### Web experiment

```bash
cd web-experiment
npm ci
npm run dev
```

Open `http://localhost:3000`. Without configuration, activities, prices, and the sustainability score are **mock data**. To use the Mistral integration, copy `.env.example` to `.env.local` and supply your own key and agent ID. Provider API changes may require updates.

### API experiment

Use Python 3.11+. From `api-experiment/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

API schema: `http://127.0.0.1:8000/docs`. `/health` and `/api/carbon/compare` work without provider credentials. Chat and inventory integrations require your own provider access.

`demo.ipynb` and `backend/test_services.py` are manual integration checks that can make remote requests. For offline checks of carbon estimates and flight-response parsing, run:

```bash
python -m unittest discover -s tests -v
```

## What this explored

- Keeping provider integrations behind service classes and representing transport options with typed models.
- Converting flight-offer responses into durations, stops, and prices, leaving non-EUR prices unknown rather than inventing a conversion.
- Separating a language model's suggested itinerary from data returned by inventory providers.
- Comparing transport modes using a transparent, simple emissions estimate.

## Limits

Carbon estimates use geodesic city-to-city distance and static factors. Train/stay availability and pricing coverage are incomplete. These prototypes are intended for local use and lack production authentication and rate limiting.

Built by Mathieu Gautier.
