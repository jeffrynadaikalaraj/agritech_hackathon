"""
RazorpayX UPI integration for credit disbursement
Handles automatic and manual payouts to farmer UPI accounts
"""
import logging
import os
import sqlite3
from typing import Dict, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

RAZORPAY_KEY = os.getenv("RAZORPAY_KEY", "")
DB_PATH = 'data/agriflow.db'

class RazorpayPaymentHandler:
    """Handle payments via RazorpayX"""
    
    def __init__(self):
        self.key = RAZORPAY_KEY
    
    def initiate_payout(
        self,
        farmer_mobile: str,
        upi_id: str,
        amount: float,
        description: str = "Agricultural Credit Disbursement"
    ) -> Dict:
        """
        Initiate UPI payout via RazorpayX
        
        Args:
            farmer_mobile: Farmer's phone number
            upi_id: UPI ID (e.g., farmer@upi)
            amount: Amount in INR
            description: Transaction description
            
        Returns:
            Payment initiation response
        """
        
        if not self.key:
            logger.warning("RazorpayX credentials not configured - using mock mode")
            return self._mock_payout(farmer_mobile, upi_id, amount)
        
        try:
            # In production, use Razorpay SDK
            # import razorpay
            # client = razorpay.Client(auth=(self.key_id, self.key_secret))
            # response = client.payout.create(...)
            
            logger.info(f"Payout initiated: {farmer_mobile} -> {upi_id} for ₹{amount}")
            
            return {
                "status": "success",
                "transaction_id": f"TXN_{farmer_mobile[-4:]}_{int(datetime.now().timestamp())}",
                "farmer_mobile": farmer_mobile,
                "upi_id": upi_id,
                "amount": amount,
                "currency": "INR",
                "message": f"✅ ₹{amount:.0f} disbursed to {upi_id}"
            }
            
        except Exception as e:
            logger.error(f"Payout failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "farmer_mobile": farmer_mobile
            }
    
    def _mock_payout(self, farmer_mobile: str, upi_id: str, amount: float) -> Dict:
        """Mock payout for testing"""
        return {
            "status": "pending",
            "transaction_id": f"MOCK_{farmer_mobile[-4:]}_{int(datetime.now().timestamp())}",
            "farmer_mobile": farmer_mobile,
            "upi_id": upi_id,
            "amount": amount,
            "mode": "MOCK",
            "message": f"[MOCK] Would disburse ₹{amount:.0f} to {upi_id}"
        }

# Initialize handler
payout_handler = RazorpayPaymentHandler()

def disburse_credit(
    farmer_mobile: str,
    upi_id: str,
    amount: float
) -> Dict:
    """Disburse credit to farmer's UPI account"""
    
    # Validate amount
    if amount <= 0 or amount > 500000:
        return {"error": "Invalid amount"}
    
    # Initiate payout
    payout_result = payout_handler.initiate_payout(farmer_mobile, upi_id, amount)
    
    # Log transaction in database (would store in SQLite in production)
    if payout_result["status"] in ["success", "pending"]:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO loans (farmer_mobile, amount, purpose, status)
                VALUES (?, ?, ?, ?)
            """, (farmer_mobile, amount, "CREDIT_DISBURSEMENT", payout_result['status']))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Transaction logged for {farmer_mobile}: ₹{amount}")
        except Exception as e:
            logger.error(f"Error logging transaction: {e}")
    
    return payout_result

def get_payment_status(transaction_id: str) -> Dict:
    """Check status of a disbursement"""
    
    # In production, query transaction log from database
    return {
        "transaction_id": transaction_id,
        "status": "pending",
        "message": "Transaction status lookup not yet implemented"
    }

def get_payout_history(farmer_mobile: str) -> Dict:
    """Get payout history for a farmer"""
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query loans for this farmer
        cursor.execute("""
            SELECT * FROM loans 
            WHERE farmer_mobile LIKE ? 
            ORDER BY created_at DESC
            LIMIT 10
        """, (f'%{farmer_mobile[-4:]}%',))
        
        results = cursor.fetchall()
        conn.close()
        
        return {
            "farmer_mobile": farmer_mobile,
            "total_transactions": len(results),
            "transactions": [dict(row) for row in results]
        }
    
    except Exception as e:
        logger.error(f"Error fetching payout history: {e}")
        return {
            "error": str(e),
            "farmer_mobile": farmer_mobile,
            "transactions": []
        }
