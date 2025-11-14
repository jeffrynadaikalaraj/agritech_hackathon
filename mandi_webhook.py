"""
e-NAM Mandi Webhook Integration
Triggered when farmer's crop is sold on e-NAM
Auto-initiates loan repayment and disbursement
"""
import logging
from typing import Dict

logger = logging.getLogger(__name__)

# Mock mandi prices by district and commodity
MANDI_PRICES = {
    'Madurai': {'Rice': 3200, 'Sugarcane': 280, 'Maize': 1850},
    'Coimbatore': {'Maize': 1850, 'Groundnut': 4200, 'Cotton': 5600},
    'Tiruchirappalli': {'Groundnut': 4200, 'Rice': 3200, 'Sugarcane': 280},
    'Chennai': {'Rice': 3100, 'Sugarcane': 285},
    'Salem': {'Cotton': 5500, 'Groundnut': 4150}
}

def get_mandi_prices(district: str) -> Dict:
    """
    Get current mandi prices for a district
    
    Args:
        district: District name
    
    Returns:
        Dict with commodity prices
    """
    
    prices = MANDI_PRICES.get(district, {})
    
    return {
        "district": district,
        "prices": prices,
        "source": "e-NAM",
        "timestamp": "2025-01-13"
    }

def process_mandi_sale(
    farmer_mobile: str,
    commodity: str,
    quantity: float,
    sale_amount: float,
    mandi_id: str
) -> Dict:
    """
    Process a mandi sale - triggered by e-NAM webhook
    
    Auto-deduct EMI and disburse remaining credit
    
    Args:
        farmer_mobile: Farmer's phone number
        commodity: Crop sold (Rice, Sugarcane, etc.)
        quantity: Quantity in quintals
        sale_amount: Total sale amount in INR
        mandi_id: e-NAM transaction ID
    
    Returns:
        Dict with repayment and disbursement status
    """
    
    try:
        logger.info(f"Mandi sale received: {farmer_mobile} sold {quantity}q of {commodity} for ₹{sale_amount}")
        
        # --- STEP 1: DEDUCT EMI ---
        # EMI amount (assuming ₹8000 loan with 12 months = ₹667/month)
        emi_amount = 667
        
        if sale_amount >= emi_amount:
            # Deduct EMI automatically
            remaining_amount = sale_amount - emi_amount
            
            response = {
                "status": "SUCCESS",
                "farmer_mobile": farmer_mobile,
                "mandi_transaction_id": mandi_id,
                "commodity": commodity,
                "quantity": quantity,
                "sale_amount": sale_amount,
                "emi_deducted": emi_amount,
                "farmer_receives": remaining_amount,
                "message": f"✅ EMI of ₹{emi_amount} auto-deducted from sale of {commodity}. Remaining ₹{remaining_amount:.0f} transferred to your account.",
                "whatsapp_message": f"""✅ *Mandi Sale Processed*

Commodity: {commodity}
Quantity: {quantity}q
Sale Amount: ₹{sale_amount:,.0f}

🧮 Breakdown:
• EMI Deducted: -₹{emi_amount}
• You Receive: ₹{remaining_amount:,.0f}

Thanks for using AgriFlow! 🌾"""
            }
        else:
            # Not enough to cover EMI
            response = {
                "status": "PARTIAL",
                "farmer_mobile": farmer_mobile,
                "mandi_transaction_id": mandi_id,
                "sale_amount": sale_amount,
                "emi_required": emi_amount,
                "shortfall": emi_amount - sale_amount,
                "message": f"⚠ Sale amount (₹{sale_amount}) is less than EMI (₹{emi_amount}). Shortfall of ₹{emi_amount - sale_amount:.0f} will be adjusted next sale.",
                "whatsapp_message": f"""⚠️ *Mandi Sale - Partial EMI Payment*

Sale Amount: ₹{sale_amount:,.0f}
EMI Due: ₹{emi_amount}

Shortfall: ₹{emi_amount - sale_amount:.0f}

This will be adjusted in your next sale. 🌾"""
            }
        
        logger.info(f"Mandi processing complete: {response['status']}")
        
        return response
    
    except Exception as e:
        logger.error(f"Mandi webhook error: {e}")
        return {
            "status": "ERROR",
            "error": str(e),
            "message": "Error processing mandi sale"
        }

def get_mandi_sale_history(farmer_mobile: str) -> Dict:
    """Get mandi sale history for a farmer (from database in production)"""
    
    # Mock data - would query database in production
    mock_history = [
        {
            "date": "2025-01-10",
            "commodity": "Rice",
            "quantity": 5.0,
            "sale_amount": 16000,
            "emi_deducted": 667,
            "farmer_received": 15333
        },
        {
            "date": "2024-12-15",
            "commodity": "Groundnut",
            "quantity": 3.0,
            "sale_amount": 12600,
            "emi_deducted": 667,
            "farmer_received": 11933
        }
    ]
    
    return {
        "farmer_mobile": farmer_mobile,
        "total_sales": len(mock_history),
        "sales": mock_history
    }
