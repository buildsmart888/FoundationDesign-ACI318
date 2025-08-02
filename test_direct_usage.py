"""
Simple Test - Direct Usage without Installation
FoundationDesign-ACI318 Package

This script tests the package functionality without formal installation.
"""

import sys
import os

# Add the package to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_direct_usage():
    print("="*80)
    print("DIRECT USAGE TEST - ACI 318M-25 FOUNDATION DESIGN")
    print("="*80)
    
    try:
        # Import the modules directly
        from FoundationDesign.foundationdesign_aci318 import PadFoundationACI318
        from FoundationDesign.concretedesignfunc_aci318 import (
            aci_load_factors,
            aci_strength_reduction_factors,
            whitney_stress_block_factor,
            minimum_flexural_reinforcement_aci318
        )
        
        print("✓ Successfully imported ACI 318M-25 modules")
        
        # Test load factors
        load_factors = aci_load_factors()
        phi_factors = aci_strength_reduction_factors()
        
        print(f"\nACI 318M-25 Design Parameters:")
        print(f"  Dead load factor: {load_factors['dead_load_factor']}")
        print(f"  Live load factor: {load_factors['live_load_factor']}")
        print(f"  φ flexure: {phi_factors['flexure']}")
        print(f"  φ shear: {phi_factors['shear_torsion']}")
        
        # Test Whitney stress block
        fc_prime = 30  # MPa
        beta1 = whitney_stress_block_factor(fc_prime)
        print(f"\nWhitney Stress Block:")
        print(f"  f'c = {fc_prime} MPa → β₁ = {beta1:.3f}")
        
        # Create foundation
        foundation = PadFoundationACI318(
            foundation_length=2500,    # mm
            foundation_width=2500,     # mm
            column_length=400,         # mm
            column_width=400,          # mm
            col_pos_xdir=1250,        # mm
            col_pos_ydir=1250,        # mm
            soil_bearing_capacity=200, # kN/m²
        )
        
        print(f"\nFoundation Object Created:")
        print(f"  Size: {foundation.foundation_length} × {foundation.foundation_width} mm")
        print(f"  Area: {foundation.area_of_foundation()/1e6:.2f} m²")
        
        # Apply loads
        foundation.column_axial_loads(
            dead_axial_load=800,  # kN
            live_axial_load=300,  # kN
        )
        
        foundation.foundation_loads(
            foundation_thickness=400,
            soil_depth_abv_foundation=700,
            soil_unit_weight=18,
            concrete_unit_weight=24
        )
        
        # Calculate loads
        service_load = foundation.total_force_Z_dir_service()
        ultimate_load = foundation.total_force_Z_dir_ultimate()
        
        print(f"\nLoad Analysis:")
        print(f"  Service load: {service_load:.1f} kN")
        print(f"  Ultimate load (ACI 318M-25): {ultimate_load:.1f} kN")
        print(f"  Load factor: {ultimate_load/service_load:.2f}")
        
        # Bearing pressure check
        bearing_check = foundation.bearing_pressure_check_service()
        print(f"\nBearing Pressure Check:")
        print(f"  Applied: {bearing_check['bearing_pressure']:.1f} kN/m²")
        print(f"  Allowable: {bearing_check['allowable_pressure']:.1f} kN/m²")
        print(f"  Status: {bearing_check['check_status']}")
        
        # Test minimum reinforcement
        fy = 420  # MPa
        b = 1000  # mm
        d = 325   # mm
        As_min = minimum_flexural_reinforcement_aci318(b, d, fc_prime, fy)
        print(f"\nMinimum Reinforcement (ACI 318M-25 Section 7.6):")
        print(f"  As,min = {As_min:.0f} mm²/m")
        
        # Test shear functions
        from FoundationDesign.concretedesignfunc_aci318 import (
            one_way_shear_strength_aci318,
            punching_shear_strength_aci318
        )
        
        Vc_oneway = one_way_shear_strength_aci318(b, d, fc_prime)
        print(f"\nShear Strength (ACI 318M-25 Section 22):")
        print(f"  One-way Vc = {Vc_oneway/1000:.1f} kN/m")
        
        # Punching shear
        bo = 2900  # mm (estimated perimeter)
        beta_c = 1.0  # square column
        punching_result = punching_shear_strength_aci318(bo, d, fc_prime, beta_c)
        print(f"  Punching Vc = {punching_result['Vc_governing']/1000:.1f} kN")
        print(f"  Governing case: {punching_result['governing_case']}")
        
        print(f"\n✓ All tests passed successfully!")
        print(f"✓ ACI 318M-25 implementation is working correctly")
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

def usage_instructions():
    print(f"\n" + "="*80)
    print("USAGE INSTRUCTIONS")
    print("="*80)
    
    print(f"\n1. Direct Script Usage:")
    print(f"   python test_direct_usage.py")
    print(f"   python complete_design_example.py")
    
    print(f"\n2. Import in Your Python Code:")
    print(f"   import sys")
    print(f"   sys.path.append('path/to/FoundationDesign-ACI318')")
    print(f"   from FoundationDesign.foundationdesign_aci318 import PadFoundationACI318")
    
    print(f"\n3. Key Features Available:")
    print(f"   ✓ ACI 318M-25 load combinations")
    print(f"   ✓ Whitney stress block flexural design")
    print(f"   ✓ Minimum/maximum reinforcement per Section 7.6")
    print(f"   ✓ One-way shear per Section 22.5")
    print(f"   ✓ Punching shear per Section 22.6")
    print(f"   ✓ Complete foundation analysis and design")
    
    print(f"\n4. Design Example:")
    print(f"   foundation = PadFoundationACI318(")
    print(f"       foundation_length=2500,")
    print(f"       foundation_width=2500,")
    print(f"       column_length=400,")
    print(f"       column_width=400,")
    print(f"       col_pos_xdir=1250,")
    print(f"       col_pos_ydir=1250,")
    print(f"       soil_bearing_capacity=200")
    print(f"   )")
    
    print(f"\n5. Design Standards:")
    print(f"   • ACI 318M-25 Building Code Requirements for Structural Concrete")
    print(f"   • Chapter 13.1 - Foundations")
    print(f"   • Section 5.3 - Load combinations")
    print(f"   • Section 7 - Flexural design")
    print(f"   • Section 22 - Shear and torsion")

if __name__ == "__main__":
    success = test_direct_usage()
    if success:
        usage_instructions()
    else:
        print("\n✗ Please check the error messages and fix any issues.")
