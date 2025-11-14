# 🌾 AgriFlow - Agricultural Credit Platform

An AI-powered platform connecting Tamil Nadu farmers with digital credit using satellite data, soil health, and mandi prices.

## 📋 Features

- **Farmer Registration**: WhatsApp-based onboarding
- **Digital Credit Score (DCS)**: ML model using satellite NDVI, soil health, PM-KISAN status
- **Automated Payouts**: UPI disbursement via RazorpayX
- **Mandi Integration**: Auto-trigger credit on e-NAM sales
- **WhatsApp Bot**: 24/7 farmer support via Twilio
- **Satellite Data**: Real-time NDVI from Sentinel-2

## 🏗️ Architecture

```
agriflow/
├── backend/           # FastAPI + ML services
│   ├── main.py        # API entry point
│   ├── database.py    # SQLAlchemy ORM
│   ├── agri_stack.py  # Farmer data aggregation
│   ├── ndvi.py        # Satellite health scores
│   ├── risk_model.py  # Credit assessment ML
│   ├── whatsapp.py    # Twilio chatbot
│   ├── mandi_webhook.py  # e-NAM integration
│   └── payout.py      # RazorpayX payments
├── data/
│   ├── raw/           # Downloaded datasets
│   └── processed/     # Cleaned data
├── db/
│   └── schema.sql     # PostgreSQL schema
└── demo/              # Marketing assets
```

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- PostgreSQL (optional, SQLite for dev)
- Twilio account (WhatsApp)
- Sentinel Hub credentials
- RazorpayX account

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourrepo/agriflow.git
cd agriflow

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your API credentials

# 5. Initialize database
python -c "from backend.database import init_db; init_db()"

# 6. Download sample datasets
python data/raw/download_datasets.py

# 7. Run API server
python -m uvicorn backend.main:app --reload
```

Visit: `http://localhost:8000/docs` for API documentation

## 🔗 API Endpoints

### Farmers
- `POST /api/farmers/register` - Register farmer
- `GET /api/farmers/{farmer_id}` - Get farmer profile
- `GET /api/farmers/{farmer_id}/mandi-sales` - Get sales history

### Credit Assessment
- `POST /api/assess` - Calculate DCS score
- `GET /api/assess/{farmer_id}` - Get assessment results

### Payments
- `POST /api/payout/disburse` - Disburse credit to UPI
- `GET /api/payout/history/{farmer_id}` - Get payout history

### Webhooks
- `POST /webhook/whatsapp` - Twilio WhatsApp webhook
- `POST /webhook/mandi-sale` - e-NAM sale trigger

## 📊 Data Sources

| Source | Type | Coverage |
|--------|------|----------|
| PM-KISAN | Subsidy Database | Tamil Nadu |
| Soil Health Card | Soil NPK | Tamil Nadu |
| e-NAM | Mandi Prices | All India |
| Sentinel-2 | NDVI Satellite | Real-time |
| IMD Weather | Rainfall/Temp | Tamil Nadu |

## 💡 Credit Decision Flow

```
Farmer Registration
       ↓
Collect Data (Land, Soil, NDVI)
       ↓
ML Risk Assessment (DCS Score)
       ↓
Determine Credit Amount
       ↓
Auto-Payout on Mandi Sale
```

## 🤖 ML Model: DCS Score

Weighted factors:
- Land Size (15%)
- PM-KISAN Status (15%)
- Soil Health (25%)
- NDVI (25%)
- Payment History (20%)

**Score 0-100:**
- 70+: LOW risk → 2.5x multiplier
- 50-70: MEDIUM risk → 1.5x multiplier
- <50: HIGH risk → 0.5x multiplier

## 🔐 Security

- `.env` for secrets (not in git)
- CORS enabled for frontend
- API authentication ready (JWT optional)
- HTTPS recommended for production

## 📱 WhatsApp Bot Commands

```
REGISTER - Start farmer onboarding
ASSESS   - Get credit assessment
MANDI    - Check mandi prices
WEATHER  - Get weather forecast
HELP     - Show menu
```

## 🗄️ Database

### Development
Uses SQLite (`agriflow.db`) by default

### Production
Switch to PostgreSQL:
```bash
# .env
DATABASE_URL=postgresql://user:password@localhost/agriflow

# Create tables
psql -U user -d agriflow < db/schema.sql
```

## 📈 Deployment

### Docker
```bash
docker build -t agriflow .
docker run -p 8000:8000 agriflow
```

### Cloud (AWS/GCP/Azure)
Use `main.py` with:
- Gunicorn for production WSGI
- CloudSQL for database
- Cloud Run/App Engine for serverless

## 📝 Example Usage

### Register Farmer
```bash
curl -X POST http://localhost:8000/api/farmers/register \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": "TN-MAD-001",
    "name": "Raj Kumar",
    "phone": "919876543210",
    "district": "Madurai",
    "land_size_ha": 2.5
  }'
```

### Get Credit Assessment
```bash
curl http://localhost:8000/api/assess/TN-MAD-001
```

### Disburse Credit
```bash
curl -X POST http://localhost:8000/api/payout/disburse \
  -H "Content-Type: application/json" \
  -d '{
    "farmer_id": "TN-MAD-001",
    "upi_id": "raj@upi",
    "amount": 25000
  }'
```

## 🤝 Contributing

```bash
git checkout -b feature/new-feature
git commit -m "Add new feature"
git push origin feature/new-feature
```

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- Sentinel Hub for satellite imagery
- Twilio for WhatsApp integration
- RazorpayX for payment infrastructure
- Government of Tamil Nadu for data sources

---

**Questions?** Open an issue or contact: support@agriflow.dev
