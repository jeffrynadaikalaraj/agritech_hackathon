AGRIFLOW QUICK START GUIDE
==========================

🚀 SERVER STATUS: RUNNING at http://localhost:8000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ VERIFY SERVER IS RUNNING
   
   Option A - Open browser:
   → http://localhost:8000/
   Expected: {"message": "🌾 AgriFlow Running!"}
   
   Option B - Use curl:
   → curl http://localhost:8000/
   
   Option C - Check API docs:
   → http://localhost:8000/docs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ RUN TEST SUITE

   Command:
   python test_api.py
   
   This tests:
   ✅ Health check
   ✅ Root endpoint
   ✅ Mandi prices
   ✅ Mandi webhook (simulated crop sale)
   ✅ API test endpoint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

3️⃣ TEST MANDI WEBHOOK (e-NAM Crop Sale Trigger)

   curl -X POST http://localhost:8000/webhook/mandi \
     -H "Content-Type: application/json" \
     -d '{
       "farmer_mobile": "9176543210",
       "commodity": "Rice",
       "quantity": 5.0,
       "sale_amount": 16000,
       "mandi_id": "ENAM-TEST-001"
     }'
   
   Expected response:
   {
     "status": "SUCCESS",
     "emi_deducted": 667,
     "farmer_receives": 15333,
     "whatsapp_message": "✅ EMI auto-deducted..."
   }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

4️⃣ GET MANDI PRICES FOR DISTRICT

   curl http://localhost:8000/mandi-prices/Madurai
   
   Returns commodity prices:
   {
     "district": "Madurai",
     "prices": {
       "Rice": 3200,
       "Sugarcane": 280,
       "Maize": 1850
     }
   }
   
   Available districts:
   - Madurai
   - Chennai
   - Coimbatore
   - Tiruchirappalli
   - Salem

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5️⃣ SETUP TWILIO FOR WHATSAPP (NEXT STEP)

   A. Create Twilio account (free):
      → twilio.com/whatsapp
   
   B. Get credentials:
      - TWILIO_SID (Account SID)
      - TWILIO_TOKEN (Auth Token)
      - TWILIO_PHONE (WhatsApp number)
   
   C. Add to .env:
      TWILIO_SID=your_sid
      TWILIO_TOKEN=your_token
      TWILIO_PHONE=whatsapp:+14155238886
   
   D. Expose server with ngrok:
      → Download from ngrok.com
      → ./ngrok http 8000
      → Copy public URL
   
   E. Set webhook in Twilio console:
      → Messaging > Webhook URL
      → https://YOUR_NGROK_URL/webhook/whatsapp
   
   F. Test WhatsApp bot:
      Send "Hi" to Twilio WhatsApp number
      Bot should reply with OTP

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

6️⃣ DATABASE STATUS

   SQLite DB: data/agriflow.db ✅
   
   Tables:
   - farmers (5 records loaded)
   - loans (empty, populated on disbursement)
   
   Test data:
   Mobile: 9176543210 (Raj Kumar, Madurai)
   Land: 6.2 acres
   DCS Score: 89.4% (APPROVED)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

7️⃣ ARCHITECTURE FLOW

   WhatsApp Message
        ↓
   Twilio Webhook
        ↓
   /webhook/whatsapp endpoint
        ↓
   whatsapp.py (Bot Logic)
        ↓
   agri_stack.py (Fetch farmer)
        ↓
   risk_model.py (Calculate DCS)
        ↓
   Response + Database Log
        ↓
   Twilio sends WhatsApp reply

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

8️⃣ TROUBLESHOOTING

   ❌ "Port 8000 already in use"
   → Kill process: netstat -ano | findstr :8000
   → taskkill /PID <PID> /F
   → Restart uvicorn
   
   ❌ "ModuleNotFoundError: dotenv"
   → pip install python-dotenv
   
   ❌ "Database not found"
   → Run: python db_init.py
   
   ❌ "Whatsapp webhook error"
   → Check .env for TWILIO credentials
   → Verify ngrok URL in Twilio console
   → Test with curl first

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ ALL SYSTEMS READY FOR HACKATHON/DEMO!

Next: Connect Twilio + Test WhatsApp Bot
