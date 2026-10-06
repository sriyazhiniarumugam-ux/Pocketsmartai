# PocketSmart AI

PocketSmart AI is a GenAI-powered budget and recommendation assistant.

The application supports:

- Home Interior Planning
- Party Budget Planning
- Jewelry Recommendations
- Optional Jewelry Outfit Image Analysis
- Gemini AI
- User Registration
- User Login
- JWT Authentication
- Recommendation History
- SQLite Database
- Responsive Frontend

---

# Project Architecture

```text
Browser
    |
    v
Jinja2 HTML
CSS
JavaScript
    |
    v
FastAPI
    |
    +------ Authentication
    |
    +------ Home Planner
    |
    +------ Party Planner
    |
    +------ Jewelry Planner
    |
    +------ History
    |
    v
Gemini AI
    |
    v
Recommendation Engine
    |
    v
SQLite Database