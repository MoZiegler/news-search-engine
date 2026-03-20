# Frontend Implementation Plan

## Goal
Build a React frontend with TypeScript and separate CSS files, backed by FastAPI GET endpoints only in v1.

## Locked Decisions
- Framework: React
- Rendering: SSR/Hybrid (Next.js App Router)
- API style in v1: GET endpoints only
- CSV export: generated on frontend from GET JSON response
- Styling: CSS in separate files (CSS Modules per component + global styles)

## Why SSR/Hybrid For This Project
- Better SEO for search result pages because the first HTML is server-rendered.
- Faster perceived load for first page view (content arrives in HTML, not only after client JS fetch).
- Keep rich interactivity for search/filter/export through client components.
- Lower initial JS is possible when non-interactive UI stays server-rendered.

## Target Architecture

### Backend (FastAPI adapter over existing Python modules)
Reuse existing logic in:
- main.py
- src/news_api.py
- src/summarizer.py
- src/entity_extractor.py
- src/i18n.py
- src/csv_handler.py (column mapping reference only)

Proposed v1 endpoints (GET-only):
- GET /health
- GET /api/search?query=<string>&language=<en|de>&limit=<int>
- GET /api/summary?query=<string>&language=<en|de>&limit=<int>
- GET /api/entities?query=<string>&language=<en|de>&limit=<int>
- GET /api/translations/<language>

Notes:
- Summary/entities can be derived from current query results server-side.
- Keep CORS enabled for local frontend origin.
- Keep API key only in backend.

### Frontend (Next.js + TypeScript)
Suggested structure:

```
frontend/
  app/
    page.tsx
    search/
      page.tsx
    layout.tsx
  components/
    search/
      SearchForm.tsx
      SearchForm.module.css
    articles/
      ArticleList.tsx
      ArticleList.module.css
      ArticleCard.tsx
      ArticleCard.module.css
    summary/
      SummaryPanel.tsx
      SummaryPanel.module.css
    entities/
      EntitiesPanel.tsx
      EntitiesPanel.module.css
    export/
      ExportCsvButton.tsx
      ExportCsvButton.module.css
  lib/
    api/
      client.ts
      types.ts
      search.ts
      summary.ts
      entities.ts
      translations.ts
    csv/
      toCsv.ts
  styles/
    globals.css
    variables.css
```

## Server vs Client Component Map

Use server components by default, add client components only where browser interactivity is required.

| Area | Component | Render Mode | Why | JS Impact |
|---|---|---|---|---|
| App shell | app/layout.tsx | Server | Static frame, metadata, SEO basics | Almost none |
| Home intro | app/page.tsx | Server | Marketing/intro content, indexable | None after HTML |
| Search results route | app/search/page.tsx | Server (initial) + hydrate children | SEO and first paint for initial query | Lower initial JS |
| Search form | SearchForm.tsx | Client | Input handling, submit, validation UX | Required |
| Article list wrapper | ArticleList.tsx | Server when static initial list, Client when dynamic filters/sort | Server for first render, client if live filtering | Medium |
| Article card | ArticleCard.tsx | Server preferred | Mostly presentational | Very low |
| Summary panel | SummaryPanel.tsx | Client | Triggering refetch/loading/error states | Required |
| Entities panel | EntitiesPanel.tsx | Client | Interactive chips/sorting/toggles | Required |
| Export button | ExportCsvButton.tsx | Client | Blob/download API is browser-only | Required |
| Language switch | Language control | Client | Immediate UI switch interactions | Required |

Rule of thumb:
- If a component needs useState/useEffect/onClick/browser APIs, make it Client.
- Otherwise keep it Server.

## Does SSR/Hybrid Mean Less JS?
Usually yes for initial load, but not always less total JS over a full session.

- Less initial JS: non-interactive UI can stay server-rendered and avoid hydration costs.
- Same or more JS in interactive zones: search form, dynamic panels, export still need client JS.
- Net effect here: likely smaller first payload than SPA, with similar interactive JS once user starts using tools.

## SPA vs SSR/Hybrid (Pros and Cons)

### SPA (React + Vite)
Pros:
- Simpler mental model and deployment (static hosting is easy).
- Fast client-side navigation after first bundle load.
- Great DX for purely app-like experiences.

Cons:
- Weak first-load SEO unless pre-rendering is added separately.
- Slower first meaningful content on low-end devices/networks (needs JS boot + fetch).
- Usually larger initial JS shipped.

### SSR/Hybrid (React + Next.js)
Pros:
- Better SEO out of the box for indexable routes.
- Faster first contentful render for initial page view.
- Can reduce initial JS if server components are used well.
- Flexible mix of server-rendered and interactive areas.

Cons:
- More architectural complexity (server/client split).
- More moving parts for deployment and caching strategy.
- Need discipline to avoid turning everything into client components.

## Design Pattern Used

This plan follows a hybrid of several established patterns:

- Layered Architecture:
  Separate layers for UI, API client, FastAPI adapter, and domain services.

- Adapter Pattern (backend):
  FastAPI routes are a thin adapter over existing Python modules, translating HTTP requests into service calls.

- Feature-Based Frontend Structure:
  UI code is organized by feature areas (search, articles, summary, entities, export) for better scalability.

- SSR/Hybrid Component Boundary Pattern:
  Server components by default, client components only for interactive behavior.

- API-First Contract Pattern:
  Endpoint contracts and response types are defined early to reduce integration churn.

In short, the implementation is layered and adapter-based, with feature-oriented frontend modules and clear server/client boundaries for SSR/Hybrid rendering.

## Implementation Phases

### Phase 1: API Contract Freeze
1. Define exact request params and response types for all GET endpoints.
2. Match article field names to current CSV mapping and tests.
3. Define error payload format and status code conventions.

### Phase 2: FastAPI Adapter
1. Create app entrypoint and dependency wiring.
2. Implement GET routes listed above.
3. Add CORS config for local frontend origin.
4. Add basic API tests for success, invalid params, and empty result.

### Phase 3: Frontend SSR/Hybrid Setup
1. Scaffold Next.js TypeScript app in frontend/.
2. Implement route-level server rendering for app/search/page.tsx.
3. Add client components for interactive features.
4. Add typed API client under lib/api.
5. Add CSV generator utility under lib/csv/toCsv.ts.

### Phase 4: Styling and UX
1. Add global styles and CSS variables.
2. Keep component styles in CSS Modules.
3. Add loading/empty/error states for each panel.
4. Validate desktop and mobile layouts.

### Phase 5: Verification and Docs
1. Run backend tests and add endpoint coverage.
2. Add frontend tests for CSV escaping and API parsing.
3. Validate full flow: search, summary, entities, CSV download.
4. Update README with run commands and architecture notes.

## Risks and Mitigations
- Model warm-up latency for summary/entities: show loading skeletons and clear status text.
- GET-only derived endpoints may recompute often: add short-lived cache where safe.
- Query-string size limits: keep query params compact and avoid large payloads in URL.
- CORS misconfiguration: define explicit allowed origins in dev/prod envs.

## Recommendation
For your goals (SEO + load-time perception + React + TypeScript), SSR/Hybrid is the better fit than SPA.
Use server components by default, then selectively add client components only for interactive UI areas.