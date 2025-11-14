"""
NDVI (Normalized Difference Vegetation Index) calculation
Determines crop health from satellite data
Returns: 0-1 scale (0.78 = healthy crop)
"""
import logging

logger = logging.getLogger(__name__)

# Mock NDVI values by district
NDVI_BY_DISTRICT = {
    'Madurai': 0.78,
    'Chennai': 0.65,
    'Coimbatore': 0.82,
    'Tiruchirappalli': 0.70,
    'Salem': 0.75,
    'Erode': 0.73,
    'Kancheepuram': 0.68,
    'Villupuram': 0.72
}

def get_ndvi(district: str) -> float:
    """
    Get NDVI (crop health) score for a district
    In production, this would fetch from Sentinel Hub API
    
    Args:
        district: District name
    
    Returns:
        NDVI score (0-1, where 0.78 = healthy crop)
    """
    
    # Return mock value or default to 0.70
    ndvi = NDVI_BY_DISTRICT.get(district, 0.70)
    logger.debug(f"NDVI for {district}: {ndvi}")
    return ndvi

def get_crop_health_status(ndvi: float) -> str:
    """
    Convert NDVI score to health status
    
    Args:
        ndvi: NDVI score (0-1)
    
    Returns:
        Health status string
    """
    
    if ndvi >= 0.75:
        return "Excellent"
    elif ndvi >= 0.65:
        return "Good"
    elif ndvi >= 0.50:
        return "Fair"
    else:
        return "Poor"
