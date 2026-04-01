# AI-Powered Trading Psychology Trainer

Hackathon-ready full-stack starter focused on trading behavior and AI feedback.

## Tech Stack

- Frontend: React + Vite
- Backend: FastAPI
- Database: MongoDB
- AI: OpenAI API

## Project Structure

```text
frontend/
  src/
    components/
    pages/
    services/
    state/
    styles/
backend/
  routes/
  services/
  models/
  database/
  utils/
  data/
```

## Setup

### 1. Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

### 3. Environment Variables

Create `backend/.env`:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB=trading_psychology
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
PRICE_DATA_PATH=backend/data/sample_prices.csv
```

Create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## API Endpoints

- `GET /scenario/init`
- `POST /scenario/next-day`
- `POST /trade`
- `POST /analyze-behavior`
- `POST /ai-feedback`
- `GET /portfolio`
- `GET /trade-history`

## MongoDB Collections

- `users`: player profile, XP, preferences
- `trades`: executed buy/sell records
- `behavior_logs`: detected rule-based behavior events
- `feedback_logs`: AI feedback history
- `portfolio_state`: current simulated holdings and cash

## Notes

- MongoDB usage is optional during early hacking; the app returns mock-safe defaults if the database is unavailable.
- `backend/data/sample_prices.csv` is a starter dataset for scenario progression.
- The frontend includes minimal pages and state so you can plug in charts and AI UI quickly.
