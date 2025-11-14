"""
AgriFlow FastAPI Server
Main entry point with WhatsApp webhook, mandi webhook, and API endpoints
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AgriFlow API",
    description="Agricultural Credit Platform with WhatsApp Integration",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import modules
from .whatsapp import handle_message, format_whatsapp_response
from .mandi_webhook import process_mandi_sale, get_mandi_prices

# --- ENDPOINTS ---

@app.get("/")
async def root():
    """Root endpoint - API status"""
    return {
        "message": "🌾 AgriFlow Running!",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "whatsapp": "POST /webhook/whatsapp",
            "mandi": "POST /webhook/mandi",
            "mandi_prices": "GET /mandi-prices/{district}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AgriFlow"}

# --- WHATSAPP WEBHOOK ---

@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    """
    Twilio WhatsApp webhook endpoint
    Receives incoming messages and sends bot responses
    
    Expected form data:
    - From: WhatsApp sender number (whatsapp:+919876543210)
    - Body: Message text
    """
    
    try:
        form_data = await request.form()
        
        # Extract message details
        from_number = form_data.get("From", "").replace("whatsapp:", "")
        message_body = form_data.get("Body", "").strip()
        
        logger.info(f"WhatsApp from {from_number}: {message_body}")
        
        # Process message through bot
        response_text, response_type = handle_message(message_body, from_number)
        
        # Format as TwiML XML
        twiml = format_whatsapp_response(response_text)
        
        return Response(content=twiml, media_type="application/xml")
    
    except Exception as e:
        logger.error(f"WhatsApp webhook error: {e}")
        error_twiml = format_whatsapp_response(
            "❌ *Error Processing Message*\n\nPlease try again or contact support."
        )
        return Response(content=error_twiml, media_type="application/xml")

# --- MANDI WEBHOOK ---

@app.post("/webhook/mandi")
async def mandi_webhook(request: Request):
    """
    e-NAM Mandi sale webhook endpoint
    Triggered when farmer's crop is sold on e-NAM
    
    Expected JSON:
    {
        "farmer_mobile": "9876543210",
        "commodity": "Rice",
        "quantity": 5.0,
        "sale_amount": 16000,
        "mandi_id": "ENAM-TN-2025-001"
    }
    """
    
    try:
        data = await request.json()
        
        # Validate required fields
        required = ["farmer_mobile", "commodity", "quantity", "sale_amount", "mandi_id"]
        if not all(field in data for field in required):
            return {"error": "Missing required fields", "required": required}
        
        # Process mandi sale
        result = process_mandi_sale(
            farmer_mobile=data["farmer_mobile"],
            commodity=data["commodity"],
            quantity=data["quantity"],
            sale_amount=data["sale_amount"],
            mandi_id=data["mandi_id"]
        )
        
        logger.info(f"Mandi processed: {result['status']}")
        
        return result
    
    except Exception as e:
        logger.error(f"Mandi webhook error: {e}")
        return {"status": "error", "error": str(e)}

# --- MANDI PRICES ---

@app.get("/mandi-prices/{district}")
async def get_mandi_prices_endpoint(district: str):
    """
    Get current mandi prices for a district
    
    Args:
        district: District name (e.g., Madurai, Coimbatore)
    
    Returns:
        Dict with commodity prices
    """
    
    return get_mandi_prices(district)

# --- API ENDPOINTS ---

@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "status": "ok",
        "message": "API is responding",
        "timestamp": "2025-01-13"
    }

# --- ERROR HANDLERS ---

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return {
        "error": "Internal Server Error",
        "message": str(exc)
    }

# --- STARTUP/SHUTDOWN ---

@app.on_event("startup")
async def startup_event():
    """Called when server starts"""
    logger.info("🌾 AgriFlow server starting...")
    logger.info("WhatsApp webhook ready at: /webhook/whatsapp")
    logger.info("Mandi webhook ready at: /webhook/mandi")

@app.on_event("shutdown")
async def shutdown_event():
    """Called when server shuts down"""
    logger.info("🌾 AgriFlow server shutting down...")

# --- RUN SERVER ---

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )
