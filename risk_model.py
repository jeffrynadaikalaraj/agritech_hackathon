"""
Risk Assessment Model - Calculate Digital Credit Score (DCS)
DCS = 0.3 * land_score + 0.3 * ndvi + 0.2 * weather_risk + 0.2 * group_risk
Returns: DCS (0-1) and credit limit in INR
"""
import logging
from .ndvi import get_ndvi, get_crop_health_status

logger = logging.getLogger(__name__)

def calculate_dcs(farmer_data: dict) -> dict:
    """
    Calculate Digital Credit Score (DCS) for a farmer
    
    Args:
        farmer_data: Dict with farmer profile from agri_stack
        {
            "name": str,
            "land_acres": float,
            "district": str,
            "soil_ph": float,
            "ndvi": float,
            "mobile": str
        }
    
    Returns:
        Dict with DCS score and recommended credit limit
        {
            "dcs": float (0-1),
            "dcs_percent": float (0-100),
            "limit": float (INR),
            "status": str
        }
    """
    
    try:
        # Extract farmer data
        land_acres = farmer_data.get("land_acres", 2.5)
        district = farmer_data.get("district", "Unknown")
        soil_ph = farmer_data.get("soil_ph", 7.0)
        
        # 1. Land Score (0-1): More land = higher score
        # Max at 5 acres, cap at 1.0
        land_score = min(land_acres / 5.0, 1.0)
        
        # 2. NDVI Score (0-1): Crop health from satellite
        ndvi = get_ndvi(district)
        
        # 3. Weather Risk (0-1): Default to 0.9 (low risk)
        # In production: check rainfall, temp, etc.
        weather_risk = 0.9
        
        # 4. Group Risk (0-1): Default to 0.9 (low risk)
        # In production: check group lending history
        group_risk = 0.9
        
        # Calculate DCS (0-1)
        dcs = (
            0.3 * land_score +
            0.3 * ndvi +
            0.2 * weather_risk +
            0.2 * group_risk
        )
        
        # Convert to percentage
        dcs_percent = dcs * 100
        
        # Calculate credit limit based on DCS
        # Base: 15,000 INR + variable up to 50,000
        base_limit = 15000
        variable_limit = int(dcs * 50000)
        credit_limit = base_limit + variable_limit
        
        # Determine status
        if dcs >= 0.7:
            status = "APPROVED"
        elif dcs >= 0.5:
            status = "UNDER_REVIEW"
        else:
            status = "REJECTED"
        
        logger.info(f"DCS calculated for {farmer_data.get('name')}: {dcs_percent:.1f}% (₹{credit_limit})")
        
        return {
            "dcs": round(dcs, 3),
            "dcs_percent": round(dcs_percent, 1),
            "limit": credit_limit,
            "status": status,
            "details": {
                "land_score": round(land_score, 2),
                "ndvi": round(ndvi, 2),
                "ndvi_status": get_crop_health_status(ndvi),
                "weather_risk": weather_risk,
                "group_risk": group_risk,
                "soil_ph": soil_ph
            }
        }
    
    except Exception as e:
        logger.error(f"DCS calculation error: {e}")
        return {
            "dcs": 0.5,
            "dcs_percent": 50.0,
            "limit": 25000,
            "status": "ERROR",
            "error": str(e)
        }
