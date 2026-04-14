# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Spendly — a personal expense tracker web app built with Flask and SQLite, targeting Indian users (Rupee currency). The project is structured as a step-by-step build: frontend templates are complete, backend/database implementation is in progress.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run dev server (port 5001, debug mode)
python app.py

# Run tests
pytest
```

## Architecture

- **app.py** — Single-file Flask app with all routes. Implemented routes serve Jinja2 templates; placeholder routes return text strings indicating which step they belong to.
- **database/db.py** — Stub for SQLite connection factory (`get_db`), schema creation (`init_db`), and seed data (`seed_db`). Not yet wired into the app.
- **templates/** — Jinja2 templates using block inheritance from `base.html`. Base provides sticky navbar, footer, and static asset loading.
- **static/css/style.css** — Custom design system using CSS custom properties (`--ink`, `--accent`, `--accent-2`, `--danger`, `--paper`). Responsive breakpoints at 900px and 600px.
- **static/js/main.js** — Placeholder; landing page modal logic is inline in `landing.html`.

## Design Conventions

- Fonts: DM Serif Display (headings), DM Sans (body) via Google Fonts
- Colors: dark green accent (`#1a472a`), orange-brown secondary (`#c17f24`), off-white paper (`#f7f6f3`)
- Max content width: 1200px; auth forms: 440px
- No JS framework — vanilla JS only, no build step
