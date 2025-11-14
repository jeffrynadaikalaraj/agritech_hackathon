"""
Farmer data aggregation from SQLite
Integrates: PM-KISAN, Soil Health, Land Records, e-NAM
"""
import sqlite3
import pandas as pd
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# SQLite connection
DB_PATH = 'data/agriflow.db'

def get_farmer_data(mobile: str) -> Optional[Dict]:
    """
    Fetch farmer data from SQLite database using fuzzy mobile match
    
    Args:
        mobile: Farmer's mobile number (last 4 digits used for fuzzy match)
    
    Returns:
        Dict with farmer profile or None if not found
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Fuzzy match on last 4 digits of mobile
        last_4 = mobile[-4:]
        cursor.execute("SELECT * FROM farmers WHERE mobile LIKE ?", (f'%{last_4}%',))
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            logger.warning(f"Farmer not found for mobile: {mobile}")
            return None
        
        farmer = dict(result)
        return {
            "name": farmer.get("name"),
            "mobile": farmer.get("mobile"),
            "land_acres": farmer.get("land_acres"),
            "district": farmer.get("district"),
            "soil_ph": farmer.get("soil_ph"),
            "ndvi": farmer.get("ndvi"),
            "dcs_score": farmer.get("dcs_score")
        }
    
    except Exception as e:
        logger.error(f"Error fetching farmer data: {e}")
        return None

def get_farmer_loans(mobile: str) -> list:
    """Get loan history for farmer"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        last_4 = mobile[-4:]
        cursor.execute("""
            SELECT * FROM loans 
            WHERE farmer_mobile LIKE ? 
            ORDER BY created_at DESC
        """, (f'%{last_4}%',))
        
        results = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in results]
    
    except Exception as e:
        logger.error(f"Error fetching loans: {e}")
        return []

def add_loan(mobile: str, amount: float, purpose: str) -> bool:
    """Add new loan record"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO loans (farmer_mobile, amount, purpose, status)
            VALUES (?, ?, ?, ?)
        """, (mobile, amount, purpose, 'ACTIVE'))
        
        conn.commit()
        conn.close()
        logger.info(f"Loan added for {mobile}: ₹{amount}")
        return True
    
    except Exception as e:
        logger.error(f"Error adding loan: {e}")
        return False

def update_farmer_dcs(mobile: str, dcs_score: float) -> bool:
    """Update DCS score for farmer"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        last_4 = mobile[-4:]
        cursor.execute("""
            UPDATE farmers 
            SET dcs_score = ? 
            WHERE mobile LIKE ?
        """, (dcs_score, f'%{last_4}%'))
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        logger.error(f"Error updating DCS: {e}")
        return False
