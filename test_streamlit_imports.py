"""
Test script for Foundation Design ACI 318M-25 functions
"""

import sys
import os

# Add the FoundationDesign package to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Test imports
try:
    from FoundationDesign.foundationdesign_aci318 import (
        PadFoundationACI318,
        padFoundationDesignACI318
    )
    from FoundationDesign.concretedesignfunc_aci318 import (
        aci_load_factors,
        aci_strength_reduction_factors,
        whitney_stress_block_factor,
        validate_material_properties,
        get_design_info
    )
    print("✅ All imports successful!")
    
    # Test functions
    print("\n📋 Testing functions:")
    
    # Test load factors
    load_factors = aci_load_factors()
    print(f"  Dead load factor: {load_factors['dead_load_factor']}")
    
    # Test phi factors
    phi_factors = aci_strength_reduction_factors()
    print(f"  φ flexure: {phi_factors['flexure']}")
    
    # Test material validation
    validation = validate_material_properties(30, 420)
    print(f"  Material validation: {'PASS' if validation['valid'] else 'FAIL'}")
    
    # Test design info
    design_info = get_design_info()
    print(f"  Design code: {design_info['design_code']}")
    
    print("\n🎉 All tests completed successfully!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
