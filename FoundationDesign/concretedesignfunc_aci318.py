"""
ACI 318M-25 Concrete Design Functions Module

This module contains functions for concrete design calculations according to 
ACI 318M-25 Building Code Requirements for Structural Concrete (Metric).

Key sections implemented:
- Section 5.3: Load combinations and strength reduction factors
- Section 7: Flexural design requirements  
- Section 22: Shear and torsion design
- Section 22.6: Two-way shear (punching shear)
- Section 7.6: Minimum and maximum reinforcement
- Section 20.5: Concrete cover requirements
"""

import math
import numpy as np


def aci_load_factors():
    """
    ACI 318M-25 Section 5.3.1 - Required strength U
    
    Returns
    -------
    dict
        Load factors for different load combinations
    """
    return {
        "dead_load_factor": 1.2,
        "live_load_factor": 1.6, 
        "wind_load_factor": 1.0,
        "earthquake_load_factor": 1.0,
        "dead_load_factor_min": 0.9,  # When dead load counteracts other loads
        "roof_live_load_factor": 0.5,
        "snow_load_factor": 0.5,
    }


def aci_strength_reduction_factors():
    """
    ACI 318M-25 Section 5.4.2 - Strength reduction factors φ
    
    Returns
    -------
    dict
        Strength reduction factors for different failure modes
    """
    return {
        "flexure": 0.90,                    # Tension-controlled sections
        "compression_tied": 0.65,           # Compression-controlled, tied
        "compression_spiral": 0.75,         # Compression-controlled, spiral
        "shear_torsion": 0.75,             # Shear and torsion
        "bearing_concrete": 0.65,           # Bearing on concrete
        "strut_tie": 0.75,                 # Strut-and-tie models
    }


def whitney_stress_block_factor(fc_prime):
    """
    ACI 318M-25 Section 7.2.2.1 - Whitney stress block factor β₁
    
    Parameters
    ----------
    fc_prime : float
        Specified compressive strength of concrete in MPa
        
    Returns
    -------
    float
        Whitney stress block factor β₁
    """
    if fc_prime <= 28:
        beta1 = 0.85
    elif fc_prime <= 55:
        beta1 = 0.85 - 0.05 * (fc_prime - 28) / 7
    else:
        beta1 = 0.65
    
    return max(beta1, 0.65)


def flexural_design_aci318(Mu, b, d, fc_prime, fy, phi=0.9):
    """
    ACI 318M-25 Section 7 - Flexural design using Whitney stress block
    
    Parameters
    ----------
    Mu : float
        Ultimate moment in N·mm
    b : float
        Width of compression face in mm
    d : float  
        Distance from extreme compression fiber to centroid of tension reinforcement in mm
    fc_prime : float
        Specified compressive strength of concrete in MPa
    fy : float
        Specified yield strength of reinforcement in MPa
    phi : float, default 0.9
        Strength reduction factor for flexure
        
    Returns
    -------
    dict
        Design results including required steel area and design checks
    """
    beta1 = whitney_stress_block_factor(fc_prime)
    
    # Design moment
    Mn_required = Mu / phi
    
    # Material properties conversion (MPa to N/mm²)
    fc = fc_prime 
    
    # Calculate required reinforcement ratio
    # Assuming singly reinforced section first
    Rn = Mn_required / (b * d**2)  # N/mm²
    
    # Maximum steel ratio for tension-controlled section
    # εₜ = 0.005 (tension-controlled limit)
    c_max = d / (1 + 0.005 * 200000 / (0.003 * 200000))  # Assume Es = 200,000 MPa
    rho_max = 0.85 * beta1 * fc / fy * c_max / d
    
    # Calculate required steel ratio
    # From quadratic: ρ = (0.85*fc/fy) * [1 - √(1 - 2*Rn/(0.85*fc))]
    sqrt_term = 1 - 2 * Rn / (0.85 * fc)
    
    if sqrt_term < 0:
        return {
            "status": "FAIL - Compression reinforcement required",
            "area_of_steel": None,
            "rho_required": None,
            "compression_steel_required": True
        }
    
    rho_required = (0.85 * fc / fy) * (1 - math.sqrt(sqrt_term))
    
    # Check if section is tension-controlled
    if rho_required > rho_max:
        return {
            "status": "FAIL - Exceeds maximum reinforcement ratio",
            "area_of_steel": None,
            "rho_required": rho_required,
            "rho_max": rho_max,
            "compression_steel_required": True
        }
    
    # Calculate required steel area
    As_required = rho_required * b * d
    
    return {
        "status": "PASS",
        "area_of_steel": round(As_required, 0),
        "rho_required": rho_required,
        "rho_max": rho_max,
        "Mn_provided": None,  # Could calculate actual capacity
        "compression_steel_required": False
    }


def minimum_flexural_reinforcement_aci318(b, d, fc_prime, fy):
    """
    ACI 318M-25 Section 7.6.1 - Minimum flexural reinforcement
    
    Parameters
    ----------
    b : float
        Width of tension face in mm
    d : float
        Distance to tension reinforcement in mm  
    fc_prime : float
        Specified compressive strength of concrete in MPa
    fy : float
        Specified yield strength of reinforcement in MPa
        
    Returns
    -------
    float
        Minimum area of flexural reinforcement in mm²
    """
    # ACI 318M-25 Section 7.6.1.1
    As_min1 = 1.4 * b * d / fy  # Basic requirement
    
    # ACI 318M-25 Section 7.6.1.2
    As_min2 = math.sqrt(fc_prime) * b * d / (4 * fy)  # Alternative requirement
    
    As_min = max(As_min1, As_min2)
    
    return round(As_min, 0)


def maximum_flexural_reinforcement_aci318(b, d, fc_prime, fy):
    """
    ACI 318M-25 Section 7.6.2 - Maximum flexural reinforcement
    For tension-controlled sections (εₜ ≥ 0.005)
    
    Parameters
    ----------
    b : float
        Width in mm
    d : float  
        Effective depth in mm
    fc_prime : float
        Specified compressive strength of concrete in MPa
    fy : float
        Specified yield strength of reinforcement in MPa
        
    Returns
    -------
    float
        Maximum area of flexural reinforcement in mm²
    """
    beta1 = whitney_stress_block_factor(fc_prime)
    Es = 200000  # MPa, modulus of elasticity of steel
    
    # For tension-controlled sections, εₜ = 0.005
    epsilon_t = 0.005
    epsilon_cu = 0.003  # Ultimate concrete strain
    
    # Neutral axis depth for tension-controlled limit
    c = d * epsilon_cu / (epsilon_cu + epsilon_t)
    
    # Maximum reinforcement ratio
    rho_max = 0.85 * beta1 * fc_prime / fy * c / d
    
    As_max = rho_max * b * d
    
    return round(As_max, 0)


def one_way_shear_strength_aci318(b, d, fc_prime, lambda_factor=1.0):
    """
    ACI 318M-25 Section 22.5 - One-way shear strength of concrete
    
    Parameters
    ----------
    b : float
        Width of member in mm
    d : float
        Distance from extreme compression fiber to centroid of tension reinforcement in mm
    fc_prime : float
        Specified compressive strength of concrete in MPa
    lambda_factor : float, default 1.0
        Modification factor for lightweight concrete
        
    Returns
    -------
    float
        Nominal shear strength provided by concrete Vc in N
    """
    # ACI 318M-25 Section 22.5.5.1 - Simplified method
    Vc = 0.17 * lambda_factor * math.sqrt(fc_prime) * b * d
    
    return round(Vc, 0)


def punching_shear_strength_aci318(bo, d, fc_prime, beta_c, alpha_s=40, lambda_factor=1.0):
    """
    ACI 318M-25 Section 22.6 - Two-way shear (punching shear) strength
    
    Parameters
    ----------
    bo : float
        Perimeter of critical section in mm
    d : float
        Distance from extreme compression fiber to centroid of tension reinforcement in mm
    fc_prime : float
        Specified compressive strength of concrete in MPa
    beta_c : float
        Ratio of long side to short side of concentrated load or reaction area
    alpha_s : float, default 40
        Location parameter (40 for interior columns, 30 for edge, 20 for corner)
    lambda_factor : float, default 1.0
        Modification factor for lightweight concrete
        
    Returns
    -------
    dict
        Punching shear design results
    """
    # ACI 318M-25 Section 22.6.5.2 - Three governing equations
    
    # Equation (a) - Column aspect ratio effect
    Vc1 = (2 + 4/beta_c) * lambda_factor * math.sqrt(fc_prime) * bo * d / 6
    
    # Equation (b) - Column location effect  
    Vc2 = (alpha_s * d / bo + 2) * lambda_factor * math.sqrt(fc_prime) * bo * d / 6
    
    # Equation (c) - Maximum strength
    Vc3 = 4 * lambda_factor * math.sqrt(fc_prime) * bo * d / 6
    
    # Governing strength is minimum of the three
    Vc = min(Vc1, Vc2, Vc3)
    
    return {
        "Vc_governing": round(Vc, 0),
        "Vc_aspect_ratio": round(Vc1, 0),
        "Vc_location": round(Vc2, 0), 
        "Vc_maximum": round(Vc3, 0),
        "governing_case": "aspect_ratio" if Vc == Vc1 else ("location" if Vc == Vc2 else "maximum")
    }


def critical_section_punching_aci318(column_length, column_width, d):
    """
    ACI 318M-25 Section 22.6.4.1 - Critical section for punching shear
    Located at d/2 from face of column
    
    Parameters
    ----------
    column_length : float
        Column dimension parallel to x-axis in mm
    column_width : float  
        Column dimension parallel to y-axis in mm
    d : float
        Effective depth in mm
        
    Returns
    -------
    dict
        Critical section properties
    """
    # Critical section dimensions
    b1 = column_length + d  # Length of critical section
    b2 = column_width + d   # Width of critical section
    
    # Perimeter of critical section
    bo = 2 * (b1 + b2)
    
    # Area enclosed by critical section
    Ao = b1 * b2
    
    return {
        "critical_length": b1,
        "critical_width": b2, 
        "perimeter": bo,
        "area": Ao,
        "distance_from_face": d/2
    }


def concrete_cover_aci318(exposure_condition="normal", member_type="foundation"):
    """
    ACI 318M-25 Section 20.5 - Concrete cover requirements
    
    Parameters
    ----------
    exposure_condition : str
        Exposure condition: "normal", "severe", "marine"
    member_type : str
        Type of member: "foundation", "beam", "column", "slab"
        
    Returns
    -------
    float
        Minimum concrete cover in mm
    """
    cover_requirements = {
        "foundation": {
            "normal": 75,    # Cast against earth
            "severe": 100,   # Severe exposure
            "marine": 100    # Marine environment
        },
        "beam": {
            "normal": 40,
            "severe": 50, 
            "marine": 65
        },
        "column": {
            "normal": 40,
            "severe": 50,
            "marine": 65  
        },
        "slab": {
            "normal": 20,
            "severe": 30,
            "marine": 40
        }
    }
    
    return cover_requirements.get(member_type, {}).get(exposure_condition, 75)


def development_length_tension_aci318(db, fy, fc_prime, cover=75, spacing=150):
    """
    ACI 318M-25 Section 12.2 - Development length for deformed bars in tension
    
    Parameters
    ----------
    db : float
        Nominal diameter of bar in mm
    fy : float
        Specified yield strength of reinforcement in MPa
    fc_prime : float
        Specified compressive strength of concrete in MPa
    cover : float, default 75
        Concrete cover in mm
    spacing : float, default 150  
        Clear spacing between bars in mm
        
    Returns
    -------
    float
        Required development length in mm
    """
    # Base development length
    ld_base = (fy * db) / (2.1 * math.sqrt(fc_prime))
    
    # Modification factors
    # Clear spacing and cover
    c = min(cover, spacing/2)  # Controlling dimension
    if (c + db/2) >= 3*db:
        alpha = 1.0
    else:
        alpha = 1.3
    
    # Top bar factor (assume not top bar for foundations)
    beta = 1.0
    
    # Coating factor (assume uncoated)  
    gamma = 1.0
    
    # Size factor
    if db <= 20:
        lambda_factor = 1.0
    else:
        lambda_factor = 1.3
    
    # Required development length
    ld = ld_base * alpha * beta * gamma * lambda_factor
    
    # Minimum length
    ld_min = max(300, 12 * db)
    
    return max(ld, ld_min)


def reinforcement_bar_spacing_aci318(bar_diameter, aggregate_size=20):
    """
    ACI 318M-25 Section 6.3 - Spacing limits for reinforcement
    
    Parameters
    ----------
    bar_diameter : float
        Nominal diameter of reinforcing bar in mm
    aggregate_size : float, default 20
        Maximum aggregate size in mm
        
    Returns
    -------
    dict
        Minimum and maximum spacing requirements in mm
    """
    # Minimum clear spacing
    min_clear = max(
        25,                    # Absolute minimum
        bar_diameter,          # One bar diameter
        (4/3) * aggregate_size # 4/3 times max aggregate size
    )
    
    # Maximum spacing for crack control (foundations)
    max_spacing = min(300, 3 * 400)  # Assume 400mm slab thickness
    
    return {
        "minimum_clear_spacing": min_clear,
        "maximum_spacing": max_spacing,
        "recommended_spacing": min(200, max_spacing)
    }


def aci318_load_combination_factors():
    """
    ACI 318M-25 Section 5.3.1 - Load combination factors for strength design
    
    Returns
    -------
    dict
        Load combination factors for different limit states
    """
    return {
        "strength_design": {
            # Basic combinations
            "combination_1": {"D": 1.2, "L": 1.6, "S": 0.5},
            "combination_2": {"D": 1.2, "L": 1.0, "W": 1.0, "S": 0.5},
            "combination_3": {"D": 1.2, "L": 1.0, "E": 1.0, "S": 0.5},
            "combination_4": {"D": 0.9, "W": 1.0},
            "combination_5": {"D": 0.9, "E": 1.0},
        },
        "service_loads": {
            # No factors for service loads
            "all_factors": 1.0
        }
    }


def validate_material_properties(fc_prime, fy):
    """
    Validate material properties according to ACI 318M-25 requirements
    
    Parameters
    ----------
    fc_prime : float
        Specified compressive strength of concrete (MPa)
    fy : float
        Specified yield strength of reinforcement (MPa)
    
    Returns
    -------
    dict
        Validation results with status, errors, and warnings
    """
    validation_result = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # ACI 318M-25 Section 19.2.1 - Concrete strength limits
    if fc_prime < 17:
        validation_result["valid"] = False
        validation_result["errors"].append(
            f"f'c = {fc_prime} MPa is below minimum 17 MPa (ACI 318M-25 Section 19.2.1)"
        )
    elif fc_prime > 83:
        validation_result["valid"] = False
        validation_result["errors"].append(
            f"f'c = {fc_prime} MPa exceeds maximum 83 MPa (ACI 318M-25 Section 19.2.1)"
        )
    
    # ACI 318M-25 Section 20.2.1 - Steel yield strength limits
    if fy < 280:
        validation_result["valid"] = False
        validation_result["errors"].append(
            f"fy = {fy} MPa is below minimum 280 MPa (ACI 318M-25 Section 20.2.1)"
        )
    elif fy > 550:
        validation_result["valid"] = False
        validation_result["errors"].append(
            f"fy = {fy} MPa exceeds maximum 550 MPa (ACI 318M-25 Section 20.2.1)"
        )
    
    # Warnings for commonly used values
    if fc_prime < 21:
        validation_result["warnings"].append(
            f"f'c = {fc_prime} MPa is quite low for structural concrete"
        )
    
    if fy > 420 and fc_prime < 28:
        validation_result["warnings"].append(
            "High strength steel with low strength concrete may not be economical"
        )
    
    return validation_result


def get_design_info():
    """
    Get design code information and default parameters
    
    Returns
    -------
    dict
        Design code information and parameters
    """
    return {
        "design_code": "ACI 318M-25",
        "design_standard": "Building Code Requirements for Structural Concrete (Metric)",
        "version": "2025 Edition",
        "applicable_chapters": [
            "Chapter 13.1 - Foundations",
            "Section 5.3 - Load combinations",
            "Section 5.4 - Strength reduction factors",
            "Section 7 - Flexural design",
            "Section 22 - Shear and torsion",
            "Section 20.5 - Concrete cover"
        ],
        "default_load_factors": aci_load_factors(),
        "default_phi_factors": aci_strength_reduction_factors()
    }
