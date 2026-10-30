# Travel AI experiments

**Archived / abandoned research prototypes for a future travel-planning platform.**

These experiments explored travel API integration, structured AI output, and rough transport/carbon comparisons. They never became a complete booking product. They are preserved as development work, with their limitations visible.

## Two separate approaches

| Folder | Experiment | Implemented scope |
| --- | --- | --- |
| `web-experiment/` | February 2026, Next.js / TypeScript / Mistral | Trip form, itinerary rendering, server-side generation request, and mock fallback |
| `api-experiment/` | April 2026, Python / FastAPI / Gemini / Duffel | Structured travel intent, flight/stay search integration, chat tool calls, and approximate carbon comparison |

The two directories are **not wired together**. The intended platform would have needed reliable inventory, validated prices, a coherent itinerary flow, and booking/payment handling. None of that is claimed complete here. This repository contains no purchase/payment endpoint.

## Inspect or run

### Web experiment

```bash
cd web-experiment
npm ci
npm run dev
```

Open `http://localhost:3000`. Without configuration, generation returns fixed example content: activities, prices, and the sustainability score are **mock data**, not researched recommendations. To try the historical Mistral integration, copy `.env.example` to `.env.local` and supply your own key and agent ID. Remote API compatibility is not guaranteed.

### API experiment

Python 3.11+ was the intended environment. From `api-experiment/`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

API schema: `http://127.0.0.1:8000/docs`. `/health` and `/api/carbon/compare` can be used without paid provider credentials. Chat and inventory integrations need your own configured provider access. No live API calls were made to prepare this archive.

`demo.ipynb` and `backend/test_services.py` are **manual integration explorations**, not a passing offline test suite. Running them can make remote requests. Notebook outputs have been removed. `tests/test_offline.py` checks local carbon behavior and flight-response parsing with a mocked HTTP client.

## What this explored

- Keeping provider integrations behind service classes and representing transport options with typed models.
- Converting flight-offer responses into durations, stops, and prices, leaving non-EUR prices unknown rather than inventing a conversion.
- Separating a language model's suggested itinerary from data returned by inventory providers.
- Comparing transport modes using a transparent, simple emissions estimate.

## Limits

Carbon figures use geodesic city-to-city distance and static factors, not measured route-specific emissions. Train/stay availability and pricing coverage are incomplete. A configuration field or dependency does not mean a database, Redis cache, or deployment was implemented. This is an archived local prototype without production authentication or rate limiting.

Built by Mathieu Gautier. This clean archive combines two historical experiments without publishing old environment files, credentials, cached responses, worktrees, or notebook output. Provider names refer to integrations and do not imply affiliation. Dependencies retain their own licenses.

Archive maintenance: the web experiment's ESLint version/configuration was aligned with its existing Next.js version, and JSX quotation marks were escaped so its production build can be checked. The application flow is unchanged.
