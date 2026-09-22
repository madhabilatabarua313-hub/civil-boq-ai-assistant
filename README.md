# 🏗️ Civil BOQ AI

A clean Streamlit starter for:

- Civil quantity takeoff
- BOQ generation
- Location-wise market rates
- Persistent project data
- AI assistant with Claude
- Public user reviews
- CSV export

## 1. Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

The local prototype stores data in `civil_boq.db`, so refreshes do not erase saved projects.

## 2. Claude API

Create `.streamlit/secrets.toml` locally:

```toml
ANTHROPIC_API_KEY = "your-key"
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"
```

For Streamlit Community Cloud, put the same values in the app's Secrets settings.

## 3. Important production note

For a public multi-user deployment, do NOT rely on the local SQLite file as the permanent shared database. Use a hosted PostgreSQL/Supabase database and authentication. Keep the database connection string/API credentials in Streamlit Secrets, never in GitHub.

## 4. Architecture

```text
Streamlit UI
    ↓
Project / Quantity / BOQ / Rates / Reviews
    ↓
Persistent database
    ↓
Deterministic calculation engine
    ↓
Claude AI assistant
```

AI is an assistant; the numerical calculation engine should remain deterministic and auditable.

## 5. Next upgrades

- Supabase/PostgreSQL persistence
- User authentication
- PDF report generation
- Excel `.xlsx` export
- BOQ revision snapshots
- Rate locking/snapshots
- Supplier quotation upload
- Admin review moderation
- AI BOQ checker
- Drawing/PDF quantity extraction
- Revit/BIM integration
