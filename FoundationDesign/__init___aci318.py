"""
FoundationDesign-ACI318 Package

A Python module for structural analysis and design of different foundation types 
in accordance with ACI 318M-25 Chapter 13.1 Foundations.

This package provides:
- Isolated pad foundation design per ACI 318M-25
- Combined footing foundation design per ACI 318M-25
- Load combinations per ACI 318M-25 Section 5.3
- Flexural design per ACI 318M-25 Section 7
- Shear design per ACI 318M-25 Section 22
- Punching shear design per ACI 318M-25 Section 22.6

Classes
-------
PadFoundationACI318 : Main foundation analysis class
padFoundationDesignACI318 : Foundation design function

Functions  
---------
Concrete design functions per ACI 318M-25:
- flexural_design_aci318
- minimum_flexural_reinforcement_aci318
- maximum_flexural_reinforcement_aci318
- one_way_shear_strength_aci318
- punching_shear_strength_aci318
- critical_section_punching_aci318
- aci_load_factors
- aci_strength_reduction_factors
- whitney_stress_block_factor
- concrete_cover_aci318
- development_length_tension_aci318

Data validation functions:
- assert_input_limit
- assert_number
- assert_strictly_positive_number
- assert_maximum_input_limit
- assert_input_range

Usage
-----
>>> from FoundationDesign import PadFoundationACI318, padFoundationDesignACI318
>>> 
>>> # Create foundation object
>>> fdn = PadFoundationACI318(
...     foundation_length=2500,      # mm
...     foundation_width=2500,       # mm  
...     column_length=400,           # mm
...     column_width=400,            # mm
...     col_pos_xdir=1250,          # mm
...     col_pos_ydir=1250,          # mm
...     soil_bearing_capacity=200,   # kN/m²
... )
>>>
>>> # Apply loads
>>> fdn.column_axial_loads(
...     dead_axial_load=800,         # kN
...     live_axial_load=300,         # kN
... )
>>>
>>> # Design foundation
>>> design = padFoundationDesignACI318(
...     fdn_analysis=fdn,
...     concrete_grade=30,           # f'c = 30 MPa
...     steel_grade=420,             # fy = 420 MPa
...     foundation_thickness=400,    # mm
... )
>>>
>>> print(design["design_summary"]["foundation_adequate"])
"""

# Import main classes and functions for ACI 318M-25 design
from FoundationDesign.foundationdesign_aci318 import (
    PadFoundationACI318, 
    padFoundationDesignACI318
)

# Import ACI 318M-25 concrete design functions
from FoundationDesign.concretedesignfunc_aci318 import (
    flexural_design_aci318,
    minimum_flexural_reinforcement_aci318,
    maximum_flexural_reinforcement_aci318,
    one_way_shear_strength_aci318,
    punching_shear_strength_aci318,
    critical_section_punching_aci318,
    aci_load_factors,
    aci_strength_reduction_factors,
    whitney_stress_block_factor,
    concrete_cover_aci318,
    development_length_tension_aci318,
    reinforcement_bar_spacing_aci318,
    aci318_load_combination_factors,
)

# Import data validation functions
from FoundationDesign.datavalidation import (
    assert_input_limit,
    assert_number,
    assert_strictly_positive_number,
    assert_maximum_input_limit,
    assert_input_range,
)

# Import combined footing design (if available)
try:
    from FoundationDesign.combinedfootingdesign_aci318 import (
        CombinedFootingAnalysisACI318,
        CombinedFootingDesignACI318,
    )
except ImportError:
    # Combined footing not yet implemented for ACI 318M-25
    pass

# Package metadata
__version__ = "0.2.0"
__author__ = "Kunle Yusuf"
__email__ = "kunleyusuf858@gmail.com"
__description__ = "Foundation design per ACI 318M-25 Chapter 13.1"
__license__ = "GPL-3.0"
__url__ = "https://github.com/buildsmart888/FoundationDesign-ACI318"

# Design code information
DESIGN_CODE = "ACI 318M-25"
DESIGN_STANDARD = "Building Code Requirements for Structural Concrete (Metric)"
APPLICABLE_CHAPTERS = [
    "Chapter 5: Load combinations and strength reduction factors",
    "Chapter 7: Flexural design",
    "Chapter 13.1: Foundations", 
    "Chapter 20: Concrete cover and spacing",
    "Chapter 22: Shear and torsion"
]

# Load factors per ACI 318M-25 Section 5.3.1
DEFAULT_LOAD_FACTORS = {
    "dead": 1.2,
    "live": 1.6,
    "wind": 1.0,
    "earthquake": 1.0,
    "dead_minimum": 0.9,
}

# Strength reduction factors per ACI 318M-25 Section 5.4.2
DEFAULT_PHI_FACTORS = {
    "flexure": 0.90,
    "shear": 0.75,
    "compression_tied": 0.65,
    "compression_spiral": 0.75,
    "bearing": 0.65,
}

# Material property limits per ACI 318M-25
MATERIAL_LIMITS = {
    "fc_prime_min": 17,      # MPa - minimum concrete strength
    "fc_prime_max": 83,      # MPa - maximum concrete strength
    "fy_min": 280,           # MPa - minimum steel yield strength
    "fy_max": 550,           # MPa - maximum steel yield strength
}

# Concrete cover requirements per ACI 318M-25 Section 20.5.1.3 (mm)
CONCRETE_COVER = {
    "foundations_cast_against_earth": 75,
    "foundations_formed_against_earth": 50,
    "beams_columns_severe_exposure": 50,
    "beams_columns_normal_exposure": 40,
    "slabs_severe_exposure": 30,
    "slabs_normal_exposure": 20,
}

def get_design_info():
    """
    Get information about the design standard and implementation.
    
    Returns
    -------
    dict
        Design code information and implementation details
    """
    return {
        "design_code": DESIGN_CODE,
        "design_standard": DESIGN_STANDARD,
        "version": __version__,
        "applicable_chapters": APPLICABLE_CHAPTERS,
        "default_load_factors": DEFAULT_LOAD_FACTORS,
        "default_phi_factors": DEFAULT_PHI_FACTORS,
        "material_limits": MATERIAL_LIMITS,
        "concrete_cover_requirements": CONCRETE_COVER,
        "package_info": {
            "author": __author__,
            "email": __email__,
            "license": __license__,
            "url": __url__,
            "description": __description__
        }
    }

def validate_material_properties(fc_prime, fy):
    """
    Validate material properties against ACI 318M-25 limits.
    
    Parameters
    ----------
    fc_prime : float
        Specified compressive strength of concrete in MPa
    fy : float
        Specified yield strength of reinforcement in MPa
        
    Returns
    -------
    dict
        Validation results
    """
    errors = []
    warnings = []
    
    # Check concrete strength
    if fc_prime < MATERIAL_LIMITS["fc_prime_min"]:
        errors.append(f"Concrete strength {fc_prime} MPa is below minimum {MATERIAL_LIMITS['fc_prime_min']} MPa")
    elif fc_prime > MATERIAL_LIMITS["fc_prime_max"]:
        warnings.append(f"Concrete strength {fc_prime} MPa exceeds typical range")
    
    # Check steel yield strength
    if fy < MATERIAL_LIMITS["fy_min"]:
        errors.append(f"Steel yield strength {fy} MPa is below minimum {MATERIAL_LIMITS['fy_min']} MPa")
    elif fy > MATERIAL_LIMITS["fy_max"]:
        warnings.append(f"Steel yield strength {fy} MPa exceeds typical range")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }

# Expose main classes and functions at package level
__all__ = [
    # Main classes
    'PadFoundationACI318',
    'padFoundationDesignACI318',
    
    # Concrete design functions
    'flexural_design_aci318',
    'minimum_flexural_reinforcement_aci318', 
    'maximum_flexural_reinforcement_aci318',
    'one_way_shear_strength_aci318',
    'punching_shear_strength_aci318',
    'critical_section_punching_aci318',
    'aci_load_factors',
    'aci_strength_reduction_factors',
    'whitney_stress_block_factor',
    'concrete_cover_aci318',
    'development_length_tension_aci318',
    'reinforcement_bar_spacing_aci318',
    'aci318_load_combination_factors',
    
    # Data validation
    'assert_input_limit',
    'assert_number', 
    'assert_strictly_positive_number',
    'assert_maximum_input_limit',
    'assert_input_range',
    
    # Utility functions
    'get_design_info',
    'validate_material_properties',
    
    # Constants
    'DESIGN_CODE',
    'DEFAULT_LOAD_FACTORS',
    'DEFAULT_PHI_FACTORS',
    'MATERIAL_LIMITS',
    'CONCRETE_COVER',
]
