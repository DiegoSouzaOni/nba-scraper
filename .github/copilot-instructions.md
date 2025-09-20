# Copilot Instructions for NBA Scraper

## Project Overview
- **Purpose:** Scrape, analyze, and visualize NBA data for betting and performance analysis.
- **Language:** Python
- **Architecture:** Modular, with clear separation between data fetching (clients), business logic (services), data models, and output/export utilities.
- **Data Sources:** Official NBA API (via custom clients/endpoints).
- **Outputs:** CSV and HTML reports in `outputs/`.

## Key Components
- `main.py`: Entry point for running analyses and generating reports.
- `clients/`: Handles API requests to NBA endpoints. Example: `nba_api_client.py`, `player_endpoint.py`.
- `endpoints/`: Defines endpoint logic and parameterization for API calls.
- `services/`: Core business logic for games, players, analysis, and reporting. Example: `game_service.py`, `analysis_service.py`.
- `models/`: Data models for players, teams, and games.
- `database/`: SQLite database management (see `nba_data.db`, `db_manager.py`).
- `utils/`: Helpers for formatting, exporting, logging, and scraping.
- `outputs/`: Generated reports (CSV/HTML) and logs.

## Developer Workflows
- **Install dependencies:** `pip install -r requirements/requirements.txt`
- **Run analysis:** `python main.py`
- **View results:** Open files in `outputs/` (CSV/HTML)
- **Database:** Uses SQLite (`nba_data.db`) for persistent storage.
- **Logging:** See logs in `outputs/logs/nba_scraper.log`.

## Project Conventions
- **Service Pattern:** Business logic is encapsulated in `services/` modules. Each service focuses on a single domain (e.g., player, game, analysis).
- **API Client Pattern:** All external NBA API calls go through `clients/` and `endpoints/` for maintainability.
- **Data Flow:**
  1. Fetch data via `clients/` and `endpoints/`.
  2. Process/analyze in `services/`.
  3. Export results via `utils/exporter.py` to `outputs/`.
- **Configuration:** Global constants in `utils/globals.py`.
- **Extensibility:** Add new endpoints/services by following the existing modular structure.

## Examples
- To add a new player analysis, create a service in `services/`, update `main.py` to use it, and export results via `utils/exporter.py`.
- To fetch new data, add an endpoint in `endpoints/`, implement a client in `clients/`, and integrate with services.

## Integration Points
- **NBA API:** All data fetched via custom clients/endpoints.
- **Database:** Persistent storage in SQLite, managed by `database/db_manager.py`.
- **Output:** Reports and logs in `outputs/`.

## Tips for AI Agents
- Reuse service and client patterns for new features.
- Follow naming conventions and directory structure.
- Reference `README.md` for high-level usage and workflow.
- Log important actions to `outputs/logs/nba_scraper.log`.

---
_Last updated: 2025-09-20_
