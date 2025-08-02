"""
Complete Foundation Design Example - ACI 318M-25
================================================

This script demonstrates a complete pad foundation design 
according to ACI 318M-25 Chapter 13.1 Foundations.

Problem:
- Design a square pad foundation for an interior column
- Column loads: Dead = 800 kN, Live = 300 kN  
- Column size: 400mm × 400mm
- Materials: f'c = 30 MPa, fy = 420 MPa
- Soil bearing capacity: 200 kN/m²
"""

import sys
import os
import math

# Add the FoundationDesign package to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from FoundationDesign.foundationdesign_aci318 import (
    PadFoundationACI318,
    padFoundationDesignACI318
)

def main():
    print("="*80)
    print("COMPLETE PAD FOUNDATION DESIGN - ACI 318M-25")
    print("="*80)
    
    # Design parameters
    dead_load = 800      # kN
    live_load = 300      # kN
    column_length = 400  # mm
    column_width = 400   # mm
    fc_prime = 30        # MPa
    fy = 420            # MPa
    allowable_bearing = 200  # kN/m²
    foundation_thickness = 400  # mm
    
    print(f"\nDesign Parameters:")
    print(f"  Column loads: Dead = {dead_load} kN, Live = {live_load} kN")
    print(f"  Column size: {column_length} × {column_width} mm")
    print(f"  Materials: f'c = {fc_prime} MPa, fy = {fy} MPa") 
    print(f"  Allowable bearing: {allowable_bearing} kN/m²")
    print(f"  Foundation thickness: {foundation_thickness} mm")
    
    # Step 1: Size foundation
    print(f"\nStep 1: Foundation Sizing")
    total_service_load = dead_load + live_load
    
    # Estimate foundation size (iterative process)
    foundation_size = 2500  # mm initial guess
    
    # Create foundation object
    foundation = PadFoundationACI318(
        foundation_length=foundation_size,
        foundation_width=foundation_size,
        column_length=column_length,
        column_width=column_width,
        col_pos_xdir=foundation_size/2,  # centered
        col_pos_ydir=foundation_size/2,  # centered
        soil_bearing_capacity=allowable_bearing,
    )
    
    print(f"  Foundation size: {foundation_size} × {foundation_size} mm")
    print(f"  Foundation area: {foundation.area_of_foundation()/1e6:.2f} m²")
    
    # Step 2: Apply loads
    print(f"\nStep 2: Load Application")
    foundation.column_axial_loads(
        dead_axial_load=dead_load,
        live_axial_load=live_load,
        wind_axial_load=0
    )
    
    foundation.foundation_loads(
        foundation_thickness=foundation_thickness,
        soil_depth_abv_foundation=700,  # mm
        soil_unit_weight=18,           # kN/m³
        concrete_unit_weight=24        # kN/m³
    )
    
    service_load = foundation.total_force_Z_dir_service()
    ultimate_load = foundation.total_force_Z_dir_ultimate()
    
    print(f"  Service load: {service_load:.1f} kN")
    print(f"  Ultimate load (ACI 318M-25): {ultimate_load:.1f} kN")
    print(f"  Load factor: {ultimate_load/service_load:.2f}")
    
    # Step 3: Bearing pressure check
    print(f"\nStep 3: Bearing Pressure Check")
    bearing_check = foundation.bearing_pressure_check_service()
    
    print(f"  Applied pressure: {bearing_check['bearing_pressure']:.1f} kN/m²")
    print(f"  Allowable pressure: {bearing_check['allowable_pressure']:.1f} kN/m²")
    print(f"  Utilization: {bearing_check['utilization_ratio']:.3f}")
    print(f"  Status: {bearing_check['check_status']}")
    
    if bearing_check['check_status'] != 'PASS':
        print(f"  ⚠️  Foundation size needs to be increased!")
        return
    
    # Step 4: Complete design
    print(f"\nStep 4: Complete Foundation Design")
    
    try:
        design_results = padFoundationDesignACI318(
            fdn_analysis=foundation,
            concrete_grade=fc_prime,
            steel_grade=fy,
            foundation_thickness=foundation_thickness,
            soil_depth_abv_foundation=700,
            steel_cover=75,  # mm per ACI 318M-25 Section 20.5.1.3
            bar_dia_x=16,   # mm
            bar_dia_y=16,   # mm
        )
        
        print(f"  ✓ Design completed successfully")
        
    except Exception as e:
        print(f"  ✗ Design error: {e}")
        return
    
    # Step 5: Display results
    print(f"\n" + "="*80)
    print(f"DESIGN RESULTS - ACI 318M-25")
    print(f"="*80)
    
    # Foundation geometry
    geometry = design_results['foundation_geometry']
    print(f"\nFoundation Geometry:")
    print(f"  Length: {geometry['length']} mm")
    print(f"  Width: {geometry['width']} mm") 
    print(f"  Thickness: {geometry['thickness']} mm")
    print(f"  Area: {geometry['area']/1e6:.2f} m²")
    
    # Materials
    materials = design_results['material_properties']
    print(f"\nMaterial Properties:")
    print(f"  f'c: {materials['fc_prime']} MPa")
    print(f"  fy: {materials['fy']} MPa")
    print(f"  Cover: {materials['cover']} mm (ACI 318M-25 Section 20.5.1.3)")
    
    # Load summary
    loads = design_results['loads']
    print(f"\nLoad Summary:")
    print(f"  Service load: {loads['service_load']:.1f} kN")
    print(f"  Ultimate load: {loads['ultimate_load']:.1f} kN")
    print(f"  Load combinations per ACI 318M-25 Section 5.3.1")
    
    # Bearing pressure
    bearing = design_results['bearing_pressure']
    print(f"\nBearing Pressure Check:")
    print(f"  Applied: {bearing['bearing_pressure']:.1f} kN/m²")
    print(f"  Allowable: {bearing['allowable_pressure']:.1f} kN/m²")
    print(f"  Status: {bearing['check_status']}")
    
    # Flexural design
    flexural = design_results['flexural_design']
    print(f"\nFlexural Design (ACI 318M-25 Section 7):")
    
    print(f"  X-Direction:")
    print(f"    Required As: {flexural['x_direction']['required_As']:.0f} mm²/m")
    print(f"    Minimum As:  {flexural['x_direction']['minimum_As']:.0f} mm²/m")
    print(f"    Status: {flexural['x_direction']['status']}")
    
    print(f"  Y-Direction:")
    print(f"    Required As: {flexural['y_direction']['required_As']:.0f} mm²/m")
    print(f"    Minimum As:  {flexural['y_direction']['minimum_As']:.0f} mm²/m")
    print(f"    Status: {flexural['y_direction']['status']}")
    
    # Reinforcement provision
    print(f"\nReinforcement Provision:")
    As_x = max(flexural['x_direction']['required_As'], flexural['x_direction']['minimum_As'])
    As_y = max(flexural['y_direction']['required_As'], flexural['y_direction']['minimum_As'])
    
    # Calculate bar spacing for 16mm bars
    bar_area_16 = math.pi * (16/2)**2  # mm²
    spacing_x = min(250, int(1000 * bar_area_16 / As_x / 25) * 25)  # round to 25mm
    spacing_y = min(250, int(1000 * bar_area_16 / As_y / 25) * 25)  # round to 25mm
    
    As_provided_x = 1000 * bar_area_16 / spacing_x
    As_provided_y = 1000 * bar_area_16 / spacing_y
    
    print(f"  Bottom reinforcement X: 16mm @ {spacing_x}mm c/c")
    print(f"    As provided: {As_provided_x:.0f} mm²/m")
    print(f"  Bottom reinforcement Y: 16mm @ {spacing_y}mm c/c") 
    print(f"    As provided: {As_provided_y:.0f} mm²/m")
    
    # Shear design
    shear = design_results['shear_design']
    print(f"\nShear Design (ACI 318M-25 Section 22):")
    
    # Punching shear
    punching = shear['punching_shear']
    print(f"  Punching Shear (Section 22.6):")
    print(f"    Applied force: {punching['punching_force']/1000:.1f} kN")
    print(f"    Design strength: {punching['design_strength']/1000:.1f} kN")
    print(f"    Demand/Capacity: {punching['demand_capacity_ratio']:.3f}")
    print(f"    Status: {punching['check_status']}")
    print(f"    Critical section: {punching['critical_section']['distance_from_face']:.0f}mm from column face")
    
    # One-way shear
    shear_x = shear['one_way_x']
    shear_y = shear['one_way_y']
    print(f"  One-way Shear (Section 22.5):")
    print(f"    X-direction: {shear_x['demand_capacity_ratio']:.3f} - {shear_x['check_status']}")
    print(f"    Y-direction: {shear_y['demand_capacity_ratio']:.3f} - {shear_y['check_status']}")
    
    # Overall design adequacy
    summary = design_results['design_summary']
    print(f"\n" + "="*80)
    print(f"DESIGN SUMMARY")
    print(f"="*80)
    
    print(f"\nFoundation Adequacy: {'✓ PASS' if summary['foundation_adequate'] else '✗ FAIL'}")
    
    if summary['foundation_adequate']:
        print(f"\n✓ All design checks satisfy ACI 318M-25 requirements")
        print(f"\nFinal Design Specification:")
        print(f"  Foundation: {foundation_size}mm × {foundation_size}mm × {foundation_thickness}mm")
        print(f"  Concrete: f'c = {fc_prime} MPa")
        print(f"  Steel: fy = {fy} MPa")
        print(f"  Bottom reinforcement:")
        print(f"    X-direction: 16mm @ {spacing_x}mm c/c")
        print(f"    Y-direction: 16mm @ {spacing_y}mm c/c")
        print(f"  Cover: {materials['cover']}mm to reinforcement")
        
        print(f"\nDesign Code Compliance:")
        print(f"  ✓ ACI 318M-25 Chapter 13.1 - Foundations")
        print(f"  ✓ Section 5.3 - Load combinations")  
        print(f"  ✓ Section 7 - Flexural design")
        print(f"  ✓ Section 22 - Shear and torsion")
        print(f"  ✓ Section 20.5 - Concrete cover")
        
    else:
        print(f"\n✗ Foundation design does not meet ACI 318M-25 requirements")
        print(f"Please review design parameters and increase foundation size or thickness")
    
    print(f"\nDesign completed per ACI 318M-25 Building Code Requirements for Structural Concrete")

if __name__ == "__main__":
    main()
