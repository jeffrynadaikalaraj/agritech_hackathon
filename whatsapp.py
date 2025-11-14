"""
WhatsApp Bot Integration using Twilio
Handles farmer authentication, credit assessment, and loan disbursement
Tamil/English multilingual support
"""
import logging
import os
from typing import Dict, Tuple
from .agri_stack import get_farmer_data, add_loan
from .risk_model import calculate_dcs

logger = logging.getLogger(__name__)

# Twilio Credentials (from .env)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_SID", "VA144bfb0e3ccf0e8f8103b255f889b6b7")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_TOKEN", "43032008541d176d6e84872956fbfca1")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_PHONE", "whatsapp:+14155238886")

# Bot conversation states
STATES = {
    "WELCOME": 0,
    "OTP_SENT": 1,
    "OTP_VERIFIED": 2,
    "CONSENT": 3,
    "DCS_CALCULATED": 4,
    "LOAN_OFFERED": 5,
    "LOAN_DISBURSED": 6
}

# Sample OTP (demo)
DEMO_OTP = "7890"

def handle_message(message_body: str, from_phone: str) -> Tuple[str, str]:
    """
    Process incoming WhatsApp message and generate response
    
    Args:
        message_body: Incoming message text
        from_phone: Sender's phone number (cleaned)
    
    Returns:
        Tuple of (response_text, response_type)
    """
    
    message_upper = message_body.strip().upper()
    
    logger.info(f"WhatsApp from {from_phone}: {message_body}")
    
    # --- STEP 1: WELCOME & OTP ---
    if message_upper in ['HI', 'HELLO', 'வணக்கம்', '1']:
        response = """🌾 *வரவேற்பு - AgriFlow*

Welcome to AgriFlow! 🌾

Would you like to apply for agricultural credit?

🔐 Sending OTP to verify your number...
*OTP: 7890* (Demo)

Reply with OTP to continue"""
        logger.info(f"Sent OTP to {from_phone}")
        return response, "OTP_SENT"
    
    # --- STEP 2: OTP VERIFICATION ---
    elif message_upper == DEMO_OTP:
        response = """✅ *OTP Verified!*

I need your permission to fetch your farm details from government databases (PM-KISAN, Soil Health Cards).

Do you give permission?
1️⃣ = ஆம் (Yes)
2️⃣ = இல்லை (No)"""
        logger.info(f"OTP verified for {from_phone}")
        return response, "OTP_VERIFIED"
    
    # --- STEP 3: CONSENT ---
    elif message_upper == '1':  # Yes
        # Fetch farmer data
        farmer = get_farmer_data(from_phone)
        
        if not farmer:
            return """❌ *Farmer Profile Not Found*

We couldn't find your profile in our system.

Please contact our support team.
📞 +91-XXXX-XXXXX""", "NOT_FOUND"
        
        # Calculate DCS
        dcs_result = calculate_dcs(farmer)
        
        response = f"""✅ *Profile Verified!*

*Name:* {farmer.get('name')}
*Land:* {farmer.get('land_acres', 0):.1f} acres
*District:* {farmer.get('district')}

📊 *Credit Assessment*
🎯 DCS Score: *{dcs_result['dcs_percent']:.1f}%*
Status: {dcs_result['status']}

💰 *Available Credit Limit: ₹{dcs_result['limit']:,}*

Would you like to apply for a loan?
1️⃣ = Yes (₹{dcs_result['limit']*0.3:.0f})
2️⃣ = No"""
        
        # Store DCS in session (would be in real session management)
        logger.info(f"DCS calculated for {from_phone}: {dcs_result['dcs_percent']}%")
        
        return response, "DCS_CALCULATED"
    
    elif message_upper == '2':  # No to permission
        return """👋 *Thank you!*

Feel free to reach out anytime you need agricultural credit.

📞 Support: +91-XXXX-XXXXX""", "REJECTED"
    
    # --- STEP 4: LOAN DISBURSEMENT ---
    elif message_upper == '1' and 'DCS_CALCULATED' in message_body:  # Apply for loan
        # In real system, fetch DCS from session
        loan_amount = 8000
        
        response = f"""✅ *Loan Approved!*

💸 Amount: ₹{loan_amount:,}
📍 Status: Processing

Your credit will be transferred to your linked bank account/UPI within 24 hours.

🔑 *Loan Details:*
• EMI: ₹{loan_amount//12}/month (12 months)
• Interest: 8% p.a.
• Repayment: Auto-debit from mandi sales

*TXN ID: TXN{from_phone[-4:]}001*

Thank you for using AgriFlow! 🌾"""
        
        # Add loan to database
        add_loan(from_phone, loan_amount, "AGRICULTURAL_CREDIT")
        
        logger.info(f"Loan disbursed to {from_phone}: ₹{loan_amount}")
        
        return response, "LOAN_DISBURSED"
    
    # --- HELP MENU ---
    elif message_upper in ['HELP', 'MENU', 'HELP']:
        response = """*📋 AgriFlow Help Menu*

1️⃣ - Apply for Loan
2️⃣ - Check Loan Status  
3️⃣ - View Mandi Prices
4️⃣ - Contact Support

Reply with number or:
• "Hi" - Start fresh
• "Loan Status" - Check application
• "Mandi" - Get prices
• "Help" - This menu"""
        return response, "HELP"
    
    # --- DEFAULT ---
    else:
        response = """🤔 *Sorry, I didn't understand that.*

Please reply with:
1️⃣ - Apply for Loan
2️⃣ - Loan Status
3️⃣ - Mandi Prices
4️⃣ - Contact Support

Or type "Help" for full menu"""
        return response, "HELP"

def format_whatsapp_response(message: str) -> str:
    """
    Format response as Twilio TwiML XML
    
    Args:
        message: Response text
    
    Returns:
        TwiML XML string
    """
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>{message}</Message>
</Response>"""
    
    return twiml
