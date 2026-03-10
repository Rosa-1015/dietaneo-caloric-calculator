# Frontend Integration Guide - Dietaneo API

*Quick reference for integrating the Dietaneo caloric calculator API*

---

## Quick Start

### Run Backend Locally

**With Docker** (recommended):
```bash
docker compose up --build
# API available at http://localhost:8001
```

**Manual setup**:
```bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.api:app --reload --port 8001
```

### Interactive Documentation

Visit: **http://localhost:8001/docs** (Swagger UI)

You can test all endpoints directly in the browser.

Alternative: **http://localhost:8001/redoc** (ReDoc format)

---

## API Endpoints Reference

### 1. Health Check

```
GET /
```

**Response**: `{ "message": "Dietaneo API is running" }`

---

### 2. Calculate Daily Calories (Main Endpoint)

```
POST /calculate
```

**Request Body**:
```json
{
  "sexo": "H",
  "peso": 80,
  "altura": 180,
  "edad": 35,
  "nivel_actividad": 3
}
```

**Request Fields**:

| Field | Type | Description | Valid Values |
|-------|------|-------------|---------------|
| `sexo` | string | Gender | "H" (male) or "M" (female) |
| `peso` | number/string | Weight in kg | Positive number (e.g., 80, "80.5", "80,5") |
| `altura` | number/string | Height in cm | Positive number (e.g., 180) |
| `edad` | number/string | Age in years | ≥ 18 |
| `nivel_actividad` | number/string | Activity level 1-5 | 1=Sedentary, 2=Light, 3=Moderate, 4=Heavy, 5=Very Heavy |

**Successful Response (200 OK)**:
```json
{
  "status": "success",
  "sexo": "H",
  "peso": 80,
  "altura": 180,
  "edad": 35,
  "nivel_actividad": 3,
  "calorias_en_reposo": 1715.0,
  "peso_utilizado_kg": 80,
  "kcal_actividad": 100,
  "total_calorias_diarias": 2756.25,
  "factor_actividad": 1.55,
  "reduccion_edad": 0,
  "suplementacion_requerida": false,
  "aviso_suplementacion": "",
  "aviso_legal": "Legal disclaimer text...",
  "recomendacion": "Professional recommendation text..."
}
```

**Response Fields**:
- `status` - "success" or "error"
- `total_calorias_diarias` - **Main result**: Daily calorie needs
- `calorias_en_reposo` - Calories burned at rest (BMR)
- `peso_utilizado_kg` - Adjusted weight (lower if BMI ≥ 30)
- `kcal_actividad` - Calories from activity
- `factor_actividad` - Activity level multiplier
- `reduccion_edad` - Caloric reduction based on age
- `suplementacion_requerida` - Boolean: needs micronutrient supplementation
- `aviso_suplementacion` - Supplementation warning message
- `aviso_legal` - Legal disclaimer
- `recomendacion` - Professional recommendation

---

## Error Handling

### Validation Error (422 Unprocessable Entity)

Missing required field:
```json
{
  "detail": [
    {
      "loc": ["body", "sexo"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Business Logic Error (200 with error status)

Invalid data:
```json
{
  "status": "error",
  "message": "Gender must be 'H' (Male) or 'M' (Female)"
}
```

**Common error messages**:
- "Gender must be 'H' (Male) or 'M' (Female)"
- "This calculator is for adults only (18+)"
- "Activity level must be between 1-5"
- "Weight must be a positive number"

---

## Implementation Notes

### CORS Configuration

Backend accepts requests from all origins:
```
Access-Control-Allow-Origin: *
```

### Input Flexibility

API accepts flexible input formats:
- Weight: `80`, `80.5`, `"80"`, `"80,5"` (comma decimals)
- Height: `180`, `"180"`, `180.2`
- Age: `35`, `"35"`
- Activity: `3`, `"3"`

### Response Format

All responses are JSON. Always check `status` field:
- `"success"` - Use the calculated data
- `"error"` - Display error message to user

### Supplementation Warning

When `suplementacion_requerida: true`:
- Calories are very low (< 1800 kcal)
- Weight was adjusted (obesity correction)
- Show user the warning message before suggesting the diet

---

## Testing

### Option 1: Interactive Documentation (Recommended)
1. Run backend locally
2. Go to http://localhost:8001/docs
3. Click `/calculate` endpoint
4. Click "Try it out"
5. Fill example data
6. Click "Execute"

### Option 2: cURL Command

```bash
curl -X POST "http://localhost:8001/calculate" \
  -H "Content-Type: application/json" \
  -d '{
    "sexo": "H",
    "peso": 80,
    "altura": 180,
    "edad": 35,
    "nivel_actividad": 3
  }'
```

### Option 3: Postman/Insomnia

- Method: `POST`
- URL: `http://localhost:8001/calculate`
- Body (JSON):
```json
{
  "sexo": "H",
  "peso": 80,
  "altura": 180,
  "edad": 35,
  "nivel_actividad": 3
}
```

---

## Common Issues

### Error: Cannot Connect to Server
- Is backend running? Check http://localhost:8001/
- Check port (default 8001)
- Check firewall

### Error: "Module not found" or 500 Server Error
- Backend issue, not frontend
- Check backend logs

### CORS Error in Browser Console
- In production: configure backend to allow your domain
- In development: should work (all origins allowed)

---

## Deployment

### Production Server

Replace `http://localhost:8001` with your production API URL:
```
https://your-api-domain.com
```

### Environment Configuration

Store API URL in environment variables:
```
REACT_APP_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
VUE_APP_API_URL=https://api.yourdomain.com
```

---

## Resources

- **Interactive API Docs**: http://localhost:8001/docs
- **Backend Architecture**: See [CLAUDE.md](../CLAUDE.md)
- **Testing Guide**: See [TESTING.md](./TESTING.md)
- **CI/CD Setup**: See [GITHUB_ACTIONS.md](./GITHUB_ACTIONS.md)

---

**For detailed integration examples (code samples, frameworks, error handling), ask the backend team for the extended guide.**
