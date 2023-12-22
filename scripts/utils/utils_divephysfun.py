"""
depth: z
volume: V
pressure: p
"""
import numpy as np

# By default this assumes we use a seawater regime
DEFAULT_REGIME = 'seawater'

def get_z_conversion_factor(regime: str = DEFAULT_REGIME) -> float:
    """
    Get the conversion factor based on the given regime.
    
    Parameters:
        regime (str): Default regime for which the conversion factor is required.
        
    Returns:
        float: Conversion factor based on the regime.
        
    Raises:
        ValueError: If an unsupported regime is provided.
    """
    if regime == 'seawater':
        return 10
    elif regime == 'freshwater':
        return 10.2
    else:
        raise ValueError(f"Unsupported regime: {regime}")

# Conversion factor from bars to meters of seawater or freshwater
CONVERSION_FACTOR = get_z_conversion_factor()

def get_p_from_z(depth: float) -> float:
    """
    Calculate pressure in bars from depth in meters of seawater.
    
    Parameters:
        depth (float): Depth in meters of seawater.
        
    Returns:
        float: Pressure in bars.
        
    Raises:
        ValueError: If depth is not a positive number.
    """
    if np.any(depth) < 0:
        raise ValueError("Depth should be a positive number.")
    
    return depth/CONVERSION_FACTOR + 1

def get_z_from_p(pressure: float) -> float:
    """
    Calculate depth in meters of seawater from pressure in bars.
    
    Parameters:
        pressure (float): Pressure in bars.
        
    Returns:
        float: Depth in meters of seawater.
        
    Raises:
        ValueError: If pressure is not greater than 1 bar.
    """
    if np.any(pressure) < 1:
        raise ValueError("Pressure should be greater than 1 bar.")
    
    return (pressure - 1) * CONVERSION_FACTOR
