# PreSurg.AI - ML Simulation API

AI-powered biomechanical simulation for pre-surgical planning.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Test
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "surgeryType": "osteotomy",
    "location": "mandible",
    "force": 50,
    "angle": 45
  }'
```

## API Docs

Visit: http://localhost:8000/docs