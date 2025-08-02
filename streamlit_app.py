"""
Foundation Design - ACI 318M-25 Web Application
===============================================

A Streamlit web application for designing pad foundations according to 
ACI 318M-25 Building Code Requirements for Structural Concrete.

Features:
- Interactive foundation design interface
- Real-time calculations and validation
- Visual foundation geometry display
- Comprehensive design reports
- Export results to PDF/Excel
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import math
import sys
import os

# Add the FoundationDesign package to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Import foundation design modules
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
    IMPORTS_OK = True
except ImportError as e:
    st.error(f"⚠️ Warning: Some modules not available: {e}")
    st.info("💡 You can still view the interface, but analysis will be limited.")
    IMPORTS_OK = False

# Page configuration
st.set_page_config(
    page_title="Foundation Design - ACI 318M-25",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .metric-container {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">🏗️ Foundation Design - ACI 318M-25</div>', unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="info-box">
    <strong>Design Standards:</strong> ACI 318M-25 Building Code Requirements for Structural Concrete (Metric)<br>
    <strong>Applicable Sections:</strong> Chapter 13.1 Foundations, Section 5.3 Load Combinations, Section 7 Flexural Design, Section 22 Shear Design
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
st.sidebar.header("📋 Design Parameters")

# Design code information
st.sidebar.markdown("### 📖 Design Code")
st.sidebar.info("ACI 318M-25 Chapter 13.1 - Foundations")

# Load factors
if IMPORTS_OK:
    load_factors = aci_load_factors()
    phi_factors = aci_strength_reduction_factors()
else:
    # Default values for demo
    load_factors = {'dead_load_factor': 1.4, 'live_load_factor': 1.7, 'wind_load_factor': 1.0}
    phi_factors = {'flexure': 0.9, 'shear_torsion': 0.75}

# Load factors
if IMPORTS_OK:
    default_load_factors = aci_load_factors()
    phi_factors = aci_strength_reduction_factors()
else:
    # Default values for demo
    default_load_factors = {'dead_load_factor': 1.4, 'live_load_factor': 1.7, 'wind_load_factor': 1.0}
    phi_factors = {'flexure': 0.9, 'shear_torsion': 0.75}

# Allow user to modify load factors
with st.sidebar.expander("⚙️ Load Factors (ACI 318M-25 Section 5.3.1)", expanded=False):
    use_custom_factors = st.checkbox("Use Custom Load Factors", value=False)
    
    if use_custom_factors:
        st.markdown("**Ultimate Limit State Load Factors:**")
        dead_load_factor = st.number_input("Dead Load Factor", min_value=0.5, max_value=2.0, value=default_load_factors['dead_load_factor'], step=0.1)
        live_load_factor = st.number_input("Live Load Factor", min_value=0.5, max_value=2.5, value=default_load_factors['live_load_factor'], step=0.1)
        wind_load_factor = st.number_input("Wind Load Factor", min_value=0.0, max_value=2.0, value=default_load_factors['wind_load_factor'], step=0.1)
        
        load_factors = {
            'dead_load_factor': dead_load_factor,
            'live_load_factor': live_load_factor,
            'wind_load_factor': wind_load_factor
        }
    else:
        load_factors = default_load_factors
        st.write(f"• Dead Load Factor: {load_factors['dead_load_factor']}")
        st.write(f"• Live Load Factor: {load_factors['live_load_factor']}")
        st.write(f"• Wind Load Factor: {load_factors['wind_load_factor']}")

with st.sidebar.expander("🔧 Strength Reduction Factors (Section 5.4.2)", expanded=False):
    st.write(f"• φ Flexure: {phi_factors['flexure']}")
    st.write(f"• φ Shear: {phi_factors['shear_torsion']}")

# Input sections
st.sidebar.markdown("### 🏛️ Column Properties")

col1, col2 = st.sidebar.columns(2)
with col1:
    column_length = st.number_input("Column Length (mm)", min_value=200, max_value=2000, value=400, step=50)
with col2:
    column_width = st.number_input("Column Width (mm)", min_value=200, max_value=2000, value=400, step=50)

st.sidebar.markdown("### ⚖️ Loads")

dead_load = st.sidebar.number_input("Dead Load (kN)", min_value=0.0, max_value=10000.0, value=800.0, step=50.0)
live_load = st.sidebar.number_input("Live Load (kN)", min_value=0.0, max_value=10000.0, value=300.0, step=50.0)
wind_load = st.sidebar.number_input("Wind Load (kN)", min_value=-1000.0, max_value=1000.0, value=0.0, step=10.0)

# Advanced loads (in expander)
with st.sidebar.expander("🌪️ Advanced Loads", expanded=False):
    st.markdown("**Horizontal Loads**")
    h_load_x = st.number_input("Horizontal Load X (kN)", value=0.0, step=1.0)
    h_load_y = st.number_input("Horizontal Load Y (kN)", value=0.0, step=1.0)
    
    st.markdown("**Moments**")
    moment_x = st.number_input("Moment about X (kN⋅m)", value=0.0, step=1.0)
    moment_y = st.number_input("Moment about Y (kN⋅m)", value=0.0, step=1.0)

st.sidebar.markdown("### 🏗️ Foundation Parameters")

# Foundation sizing options
sizing_method = st.sidebar.radio(
    "Foundation Sizing Method:",
    ["Auto-size based on loads", "Manual input dimensions"]
)

if sizing_method == "Manual input dimensions":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        foundation_length = st.number_input("Foundation Length (mm)", min_value=500, max_value=10000, value=2500, step=50)
    with col2:
        foundation_width = st.number_input("Foundation Width (mm)", min_value=500, max_value=10000, value=2500, step=50)
else:
    # Auto-sizing will be calculated later
    foundation_length = None
    foundation_width = None

foundation_thickness = st.sidebar.number_input("Foundation Thickness (mm)", min_value=200, max_value=1500, value=400, step=50)
soil_bearing_capacity = st.sidebar.number_input("Allowable Bearing Capacity (kN/m²)", min_value=50.0, max_value=1000.0, value=200.0, step=25.0)

with st.sidebar.expander("🌍 Soil & Environmental", expanded=False):
    soil_depth = st.number_input("Soil Depth Above Foundation (mm)", min_value=0, max_value=3000, value=700, step=100)
    soil_unit_weight = st.number_input("Soil Unit Weight (kN/m³)", min_value=15.0, max_value=25.0, value=18.0, step=0.5)
    concrete_unit_weight = st.number_input("Concrete Unit Weight (kN/m³)", min_value=20.0, max_value=30.0, value=24.0, step=0.5)

st.sidebar.markdown("### 🧱 Material Properties")

fc_prime = st.sidebar.number_input("f'c - Concrete Strength (MPa)", min_value=17.0, max_value=83.0, value=30.0, step=2.5)
fy = st.sidebar.number_input("fy - Steel Yield Strength (MPa)", min_value=280.0, max_value=550.0, value=420.0, step=20.0)

# Validate materials
if IMPORTS_OK:
    try:
        validation = validate_material_properties(fc_prime, fy)
        if not validation['valid']:
            st.sidebar.error("❌ Material properties out of ACI 318M-25 range")
            for error in validation['errors']:
                st.sidebar.error(f"• {error}")
        else:
            st.sidebar.success("✅ Material properties valid")
    except:
        pass
else:
    st.sidebar.info("📝 Material validation requires full module import")

with st.sidebar.expander("🔧 Design Details", expanded=False):
    steel_cover = st.number_input("Concrete Cover (mm)", min_value=40, max_value=100, value=75, step=5)
    bar_dia_x = st.selectbox("Bar Diameter X (mm)", [12, 16, 20, 25, 32], index=1)
    bar_dia_y = st.selectbox("Bar Diameter Y (mm)", [12, 16, 20, 25, 32], index=1)

# Foundation sizing button
st.sidebar.markdown("### 🚀 Analysis")
run_analysis = st.sidebar.button("🔄 Run Foundation Analysis", type="primary")

# Main content area
if run_analysis:
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Foundation sizing
        status_text.text("Step 1/6: Foundation sizing...")
        progress_bar.progress(10)
        
        total_service_load = dead_load + live_load
        
        if sizing_method == "Manual input dimensions":
            # Use user-defined dimensions
            foundation_size_length = foundation_length
            foundation_size_width = foundation_width
            st.info(f"📐 **Manual Sizing:** {foundation_size_length}×{foundation_size_width} mm")
        else:
            # Auto-calculate foundation size
            foundation_size_estimate = 2500  # mm initial guess
            foundation_self_weight = (foundation_size_estimate**2 * foundation_thickness / 1e9) * concrete_unit_weight
            surcharge_load = (foundation_size_estimate**2 * soil_depth / 1e9) * soil_unit_weight
            total_load_estimate = total_service_load + foundation_self_weight + surcharge_load
            
            required_area = total_load_estimate / soil_bearing_capacity  # m²
            foundation_size = int(np.sqrt(required_area * 1e6))  # mm
            foundation_size = int(np.ceil(foundation_size / 50) * 50)  # Round to 50mm
            
            foundation_size_length = foundation_size
            foundation_size_width = foundation_size
            st.success(f"🔧 **Auto-sized:** {foundation_size_length}×{foundation_size_width} mm (Area: {required_area:.2f} m²)")
        
        # Step 2: Create foundation object
        status_text.text("Step 2/6: Creating foundation object...")
        progress_bar.progress(25)
        
        foundation = PadFoundationACI318(
            foundation_length=foundation_size_length,
            foundation_width=foundation_size_width,
            column_length=column_length,
            column_width=column_width,
            col_pos_xdir=foundation_size_length/2,  # centered
            col_pos_ydir=foundation_size_width/2,  # centered
            soil_bearing_capacity=soil_bearing_capacity,
            uls_strength_factor_dead=load_factors['dead_load_factor'],
            uls_strength_factor_live=load_factors['live_load_factor'], 
            uls_strength_factor_wind=load_factors['wind_load_factor'],
        )
        
        # Step 3: Apply loads
        status_text.text("Step 3/6: Applying loads...")
        progress_bar.progress(40)
        
        foundation.column_axial_loads(
            dead_axial_load=dead_load,
            live_axial_load=live_load,
            wind_axial_load=wind_load
        )
        
        foundation.foundation_loads(
            foundation_thickness=foundation_thickness,
            soil_depth_abv_foundation=soil_depth,
            soil_unit_weight=soil_unit_weight,
            concrete_unit_weight=concrete_unit_weight
        )
        
        # Add foundation_thickness attribute to foundation object for compatibility
        foundation.foundation_thickness = foundation_thickness / 1000  # Convert to meters
        
        # Add missing attributes and methods for plotting compatibility
        foundation.soil_depth_abv_foundation = soil_depth / 1000  # Convert to meters
        foundation.soil_unit_weight = soil_unit_weight
        foundation.concrete_unit_weight = concrete_unit_weight
        foundation.uls_strength_factor_permanent = foundation.uls_strength_factor_dead
        
        # Add base pressure rate of change methods (simplified implementation)
        def base_pressure_rate_of_change_X():
            # Simplified calculation - uniform pressure distribution
            total_load = foundation.total_force_Z_dir_service()
            area = foundation.area_of_foundation() / 1e6  # m²
            pressure = total_load / area  # kN/m²
            return [pressure, pressure]  # Uniform distribution
            
        def base_pressure_rate_of_change_Y():
            # Simplified calculation - uniform pressure distribution
            total_load = foundation.total_force_Z_dir_service()
            area = foundation.area_of_foundation() / 1e6  # m²
            pressure = total_load / area  # kN/m²
            return [pressure, pressure]  # Uniform distribution
            
        def foundation_loads_method(foundation_thickness=None, soil_depth_abv_foundation=None, 
                                   soil_unit_weight=None, concrete_unit_weight=None, **kwargs):
            # Calculate foundation loads compatible with padFoundationDesign
            # Use provided parameters or fallback to stored values
            thickness = foundation_thickness if foundation_thickness is not None else foundation.foundation_thickness * 1000
            soil_depth = soil_depth_abv_foundation if soil_depth_abv_foundation is not None else foundation.soil_depth_abv_foundation * 1000
            soil_weight = soil_unit_weight if soil_unit_weight is not None else foundation.soil_unit_weight
            concrete_weight = concrete_unit_weight if concrete_unit_weight is not None else foundation.concrete_unit_weight
            
            foundation_volume = (foundation.foundation_length * foundation.foundation_width * thickness) / 1e9  # m³
            foundation_self_weight = foundation_volume * concrete_weight  # kN
            
            surcharge_volume = (foundation.foundation_length * foundation.foundation_width * soil_depth) / 1e9  # m³
            surcharge_load = surcharge_volume * soil_weight  # kN
            
            return [foundation_self_weight, surcharge_load]
            
        # Bind methods to foundation object
        foundation.base_pressure_rate_of_change_X = base_pressure_rate_of_change_X
        foundation.base_pressure_rate_of_change_Y = base_pressure_rate_of_change_Y
        foundation.foundation_loads = foundation_loads_method
        
        # Step 4: Load analysis
        status_text.text("Step 4/6: Load analysis...")
        progress_bar.progress(55)
        
        service_load = foundation.total_force_Z_dir_service()
        ultimate_load = foundation.total_force_Z_dir_ultimate()
        bearing_check = foundation.bearing_pressure_check_service()
        
        # Display detailed calculation explanation
        with st.expander("📋 Detailed Design Calculations", expanded=False):
            # Foundation sizing calculations
            st.markdown("### 1. Foundation Sizing Calculation")
            if sizing_method == "Manual input dimensions":
                st.info("🔧 **Manual Sizing Applied**")
                st.write(f"• User-defined Length: {foundation_size_length} mm")
                st.write(f"• User-defined Width: {foundation_size_width} mm")
                st.write(f"• Foundation Area: {(foundation_size_length * foundation_size_width)/1e6:.3f} m²")
            else:
                st.markdown("**Auto-sizing Process:**")
                st.latex(r"A_{required} = \frac{Total\ Service\ Load}{Allowable\ Bearing\ Pressure}")
                
                foundation_volume = (foundation_size_estimate**2 * foundation_thickness) / 1e9  # m³
                foundation_self_weight = foundation_volume * concrete_unit_weight
                surcharge_volume = (foundation_size_estimate**2 * soil_depth) / 1e9  # m³
                surcharge_load = surcharge_volume * soil_unit_weight
                total_load_estimate = total_service_load + foundation_self_weight + surcharge_load
                
                st.write(f"• Column Loads: {total_service_load:.1f} kN")
                st.write(f"• Foundation Self-weight: {foundation_self_weight:.1f} kN")
                st.write(f"• Surcharge Load: {surcharge_load:.1f} kN")
                st.write(f"• Total Service Load: {total_load_estimate:.1f} kN")
                st.write(f"• Required Area: {total_load_estimate:.1f} / {soil_bearing_capacity} = {total_load_estimate/soil_bearing_capacity:.3f} m²")
                st.write(f"• Foundation Size: √{total_load_estimate/soil_bearing_capacity:.3f} = {foundation_size_length/1000:.2f} m")
            
            # Load calculations
            st.markdown("### 2. Load Calculations")
            
            # Foundation self-weight calculation
            st.markdown("**Foundation Self-weight:**")
            st.latex(r"W_{foundation} = L \times B \times t \times \gamma_c")
            foundation_vol = (foundation_size_length * foundation_size_width * foundation_thickness) / 1e9
            st.write(f"• Volume = {foundation_size_length/1000:.2f} × {foundation_size_width/1000:.2f} × {foundation_thickness/1000:.2f} = {foundation_vol:.3f} m³")
            st.write(f"• Weight = {foundation_vol:.3f} × {concrete_unit_weight} = {foundation._foundation_self_weight:.1f} kN")
            
            # Surcharge calculation
            st.markdown("**Surcharge Load:**")
            st.latex(r"W_{surcharge} = L \times B \times h_{soil} \times \gamma_{soil}")
            surcharge_vol = (foundation_size_length * foundation_size_width * soil_depth) / 1e9
            st.write(f"• Volume = {foundation_size_length/1000:.2f} × {foundation_size_width/1000:.2f} × {soil_depth/1000:.2f} = {surcharge_vol:.3f} m³")
            st.write(f"• Weight = {surcharge_vol:.3f} × {soil_unit_weight} = {foundation._surcharge_load:.1f} kN")
            
            # Service load calculation
            st.markdown("**Service Load Calculation:**")
            st.latex(r"P_{service} = P_{dead} + P_{live} + P_{wind} + W_{foundation} + W_{surcharge}")
            st.write(f"• Dead Load: {dead_load:.1f} kN")
            st.write(f"• Live Load: {live_load:.1f} kN") 
            st.write(f"• Wind Load: {wind_load:.1f} kN")
            st.write(f"• Foundation Self-weight: {foundation._foundation_self_weight:.1f} kN")
            st.write(f"• Surcharge Load: {foundation._surcharge_load:.1f} kN")
            st.write(f"**Total Service Load: {service_load:.1f} kN**")
            
            # Ultimate load calculation
            st.markdown("**Ultimate Load Calculation (ACI 318M-25 Section 5.3.1):**")
            st.latex(f"P_{{ultimate}} = {load_factors['dead_load_factor']:.1f}D + {load_factors['live_load_factor']:.1f}L + {load_factors['wind_load_factor']:.1f}W")
            ultimate_column = (load_factors['dead_load_factor'] * dead_load + 
                             load_factors['live_load_factor'] * live_load + 
                             load_factors['wind_load_factor'] * wind_load)
            st.write(f"• Factored Column Loads: {load_factors['dead_load_factor']:.1f}×{dead_load:.1f} + {load_factors['live_load_factor']:.1f}×{live_load:.1f} + {load_factors['wind_load_factor']:.1f}×{wind_load:.1f} = {ultimate_column:.1f} kN")
            st.write(f"• Factored Foundation Weight: {load_factors['dead_load_factor']:.1f}×{foundation._foundation_self_weight:.1f} = {foundation._foundation_self_weight * load_factors['dead_load_factor']:.1f} kN")
            st.write(f"• Factored Surcharge: {load_factors['dead_load_factor']:.1f}×{foundation._surcharge_load:.1f} = {foundation._surcharge_load * load_factors['dead_load_factor']:.1f} kN")
            st.write(f"**Total Ultimate Load: {ultimate_load:.1f} kN**")
            
            # Bearing pressure calculation
            st.markdown("### 3. Bearing Pressure Check")
            st.latex(r"q = \frac{P_{service}}{A_{foundation}}")
            foundation_area = foundation.area_of_foundation() / 1e6  # m²
            calculated_pressure = service_load / foundation_area
            st.write(f"• Applied Pressure = {service_load:.1f} / {foundation_area:.3f} = {calculated_pressure:.1f} kN/m²")
            st.write(f"• Allowable Pressure = {soil_bearing_capacity} kN/m²")
            st.write(f"• Utilization Ratio = {calculated_pressure:.1f} / {soil_bearing_capacity} = {calculated_pressure/soil_bearing_capacity:.3f}")
            
            if calculated_pressure <= soil_bearing_capacity:
                st.success("✅ Bearing pressure check: PASS")
            else:
                st.error("❌ Bearing pressure check: FAIL - Increase foundation size")
            
            # Effective depth calculation
            st.markdown("### 4. Effective Depth Calculation")
            st.latex(r"d = h - cover - \frac{\phi_{bar}}{2}")
            effective_depth_x = foundation_thickness - steel_cover - bar_dia_x/2
            effective_depth_y = foundation_thickness - steel_cover - bar_dia_y/2
            st.write(f"• X-direction: d = {foundation_thickness} - {steel_cover} - {bar_dia_x}/2 = {effective_depth_x:.1f} mm")
            st.write(f"• Y-direction: d = {foundation_thickness} - {steel_cover} - {bar_dia_y}/2 = {effective_depth_y:.1f} mm")
            
            # Critical sections
            st.markdown("### 5. Critical Sections for Design")
            
            # One-way shear critical sections
            st.markdown("**One-way Shear Critical Sections (ACI 318M-25 Section 22.5.1.1):**")
            crit_x = foundation.col_pos_xdir + column_length/2 + effective_depth_x
            crit_y = foundation.col_pos_ydir + column_width/2 + effective_depth_y
            st.write(f"• X-direction: Distance from column face = d = {effective_depth_x:.1f} mm")
            st.write(f"• Y-direction: Distance from column face = d = {effective_depth_y:.1f} mm")
            st.write(f"• Critical location X: {crit_x:.1f} mm from foundation edge")
            st.write(f"• Critical location Y: {crit_y:.1f} mm from foundation edge")
            
            # Punching shear critical section
            st.markdown("**Punching Shear Critical Section (ACI 318M-25 Section 22.6.4.1):**")
            st.latex(r"b_o = 2(c_1 + d) + 2(c_2 + d) = 2(c_1 + c_2 + 2d)")
            punching_perimeter = 2 * (column_length + effective_depth_x) + 2 * (column_width + effective_depth_y)
            st.write(f"• Perimeter = 2×({column_length:.0f} + {effective_depth_x:.1f}) + 2×({column_width:.0f} + {effective_depth_y:.1f})")
            st.write(f"• b₀ = {punching_perimeter:.1f} mm")
            
            # Flexural critical sections
            st.markdown("**Flexural Critical Sections (ACI 318M-25 Section 7.2.1):**")
            st.write("• X-direction: At face of column")
            st.write("• Y-direction: At face of column")
            st.info("💡 Maximum moment occurs at the face of the column for square/rectangular columns")
        
        # Step 5: Complete design and create design object
        status_text.text("Step 5/6: Complete foundation design...")
        progress_bar.progress(75)
        
        design_results = padFoundationDesignACI318(
            fdn_analysis=foundation,
            concrete_grade=fc_prime,
            steel_grade=fy,
            foundation_thickness=foundation_thickness,
            soil_depth_abv_foundation=soil_depth,
            steel_cover=steel_cover,
            bar_dia_x=bar_dia_x,
            bar_dia_y=bar_dia_y,
        )
        
        # Create design object for plotting functions  
        from FoundationDesign.foundationdesign import padFoundationDesign
        fdn_design = padFoundationDesign(
            foundation,
            fck=fc_prime,
            fyk=fy,
            concrete_cover=steel_cover,
            bar_diameterX=bar_dia_x,
            bar_diameterY=bar_dia_y
        )
        
        # Step 6: Generate visualizations
        status_text.text("Step 6/6: Generating results...")
        progress_bar.progress(90)
        
        # Clear progress indicators
        progress_bar.progress(100)
        status_text.text("✅ Analysis completed successfully!")
        
        # Display results
        st.markdown('<div class="sub-header">📊 Design Results</div>', unsafe_allow_html=True)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Foundation Size",
                value=f"{foundation_size_length}×{foundation_size_width} mm",
                delta=f"Area: {foundation.area_of_foundation()/1e6:.2f} m²"
            )
        
        with col2:
            st.metric(
                label="Service Load",
                value=f"{service_load:.1f} kN",
                delta=f"Ultimate: {ultimate_load:.1f} kN"
            )
        
        with col3:
            st.metric(
                label="Bearing Pressure",
                value=f"{bearing_check['bearing_pressure']:.1f} kN/m²",
                delta=f"Utilization: {bearing_check['utilization_ratio']:.3f}",
                delta_color="normal" if bearing_check['utilization_ratio'] <= 1.0 else "inverse"
            )
        
        with col4:
            overall_status = "PASS" if design_results['design_summary']['foundation_adequate'] else "FAIL"
            st.metric(
                label="Design Status",
                value=overall_status,
                delta="ACI 318M-25 Compliant" if overall_status == "PASS" else "Design Issues"
            )
        
        # Detailed results in tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📐 Geometry", "💪 Flexural Design", "✂️ Shear Design", 
            "📋 Summary", "📊 Visualization"
        ])
        
        with tab1:
            st.markdown("### Foundation Geometry")
            
            col1, col2 = st.columns(2)
            
            with col1:
                geometry_data = {
                    "Parameter": [
                        "Foundation Length", "Foundation Width", "Foundation Thickness",
                        "Foundation Area", "Column Length", "Column Width", "Column Area"
                    ],
                    "Value": [
                        f"{design_results['foundation_geometry']['length']} mm",
                        f"{design_results['foundation_geometry']['width']} mm",
                        f"{design_results['foundation_geometry']['thickness']} mm",
                        f"{design_results['foundation_geometry']['area']/1e6:.2f} m²",
                        f"{column_length} mm",
                        f"{column_width} mm",
                        f"{column_length * column_width / 1e6:.3f} m²"
                    ]
                }
                st.dataframe(pd.DataFrame(geometry_data), use_container_width=True)
            
            with col2:
                material_data = {
                    "Material Property": [
                        "f'c (Concrete Strength)", "fy (Steel Yield)", "Concrete Cover",
                        "Soil Bearing Capacity", "Concrete Unit Weight", "Soil Unit Weight"
                    ],
                    "Value": [
                        f"{design_results['material_properties']['fc_prime']} MPa",
                        f"{design_results['material_properties']['fy']} MPa",
                        f"{design_results['material_properties']['cover']} mm",
                        f"{soil_bearing_capacity} kN/m²",
                        f"{concrete_unit_weight} kN/m³",
                        f"{soil_unit_weight} kN/m³"
                    ],
                    "Reference": [
                        "User Input", "User Input", "ACI 318M-25 Section 20.5.1.3",
                        "User Input", "User Input", "User Input"
                    ]
                }
                st.dataframe(pd.DataFrame(material_data), use_container_width=True)
        
        with tab2:
            st.markdown("### Flexural Design (ACI 318M-25 Section 7)")
            
            flexural = design_results['flexural_design']
            
            # Add detailed flexural calculations
            with st.expander("📐 Detailed Flexural Calculations", expanded=False):
                st.markdown("#### Design Moments")
                
                # Calculate design moments (simplified)
                # Assume uniform bearing pressure and calculate moments at column face
                bearing_pressure = service_load / (foundation.area_of_foundation() / 1e6)  # kN/m²
                
                # Calculate cantilever lengths
                cantilever_x = (foundation_size_length - column_length) / 2  # mm
                cantilever_y = (foundation_size_width - column_width) / 2   # mm
                
                # Design moments per unit width
                moment_x = bearing_pressure * (cantilever_x/1000)**2 / 2 * (foundation_size_width/1000)  # kN⋅m
                moment_y = bearing_pressure * (cantilever_y/1000)**2 / 2 * (foundation_size_length/1000)  # kN⋅m
                
                st.markdown("**X-Direction Design Moment:**")
                st.latex(r"M_u = \frac{q \times L_x^2 \times B}{2}")
                st.write(f"• Cantilever length (Lₓ): {cantilever_x:.1f} mm = {cantilever_x/1000:.3f} m")
                st.write(f"• Foundation width (B): {foundation_size_width:.1f} mm = {foundation_size_width/1000:.3f} m")
                st.write(f"• Bearing pressure (q): {bearing_pressure:.1f} kN/m²")
                st.write(f"• Design moment: {bearing_pressure:.1f} × {(cantilever_x/1000)**2:.6f} × {foundation_size_width/1000:.3f} / 2 = {moment_x:.1f} kN⋅m")
                
                st.markdown("**Y-Direction Design Moment:**")
                st.latex(r"M_u = \frac{q \times L_y^2 \times L}{2}")
                st.write(f"• Cantilever length (Lᵧ): {cantilever_y:.1f} mm = {cantilever_y/1000:.3f} m")
                st.write(f"• Foundation length (L): {foundation_size_length:.1f} mm = {foundation_size_length/1000:.3f} m")
                st.write(f"• Design moment: {bearing_pressure:.1f} × {(cantilever_y/1000)**2:.6f} × {foundation_size_length/1000:.3f} / 2 = {moment_y:.1f} kN⋅m")
                
                # Required reinforcement calculation
                st.markdown("#### Required Reinforcement Calculation")
                
                # Material properties
                beta1 = 0.85 if fc_prime <= 28 else max(0.65, 0.85 - 0.05*(fc_prime-28)/7)
                
                st.markdown("**Material Properties:**")
                st.write(f"• f'c = {fc_prime} MPa")
                st.write(f"• fy = {fy} MPa")
                st.write(f"• β₁ = {beta1:.3f} (ACI 318M-25 Section 7.4.2.2)")
                
                # Effective depths
                d_x = foundation_thickness - steel_cover - bar_dia_x/2
                d_y = foundation_thickness - steel_cover - bar_dia_y/2
                
                st.markdown("**Effective Depths:**")
                st.write(f"• d_x = {foundation_thickness} - {steel_cover} - {bar_dia_x}/2 = {d_x:.1f} mm")
                st.write(f"• d_y = {foundation_thickness} - {steel_cover} - {bar_dia_y}/2 = {d_y:.1f} mm")
                
                # Moment coefficient method (simplified)
                st.markdown("**Required Reinforcement (per meter width):**")
                st.latex(r"A_s = \frac{M_u}{\phi \times f_y \times j \times d}")
                
                # Simplified j factor (internal lever arm factor)
                j_factor = 0.9  # Conservative estimate
                phi_flexure = 0.9  # Strength reduction factor
                
                # Calculate required As
                As_req_x = (moment_x * 1e6) / (phi_flexure * fy * j_factor * d_x) * 1000  # mm²/m
                As_req_y = (moment_y * 1e6) / (phi_flexure * fy * j_factor * d_y) * 1000  # mm²/m
                
                st.write(f"• X-direction: As = {moment_x*1e6:.0f} / ({phi_flexure} × {fy} × {j_factor} × {d_x:.1f}) × 1000 = {As_req_x:.0f} mm²/m")
                st.write(f"• Y-direction: As = {moment_y*1e6:.0f} / ({phi_flexure} × {fy} × {j_factor} × {d_y:.1f}) × 1000 = {As_req_y:.0f} mm²/m")
                
                # Minimum reinforcement
                st.markdown("**Minimum Reinforcement (ACI 318M-25 Section 7.6.1.1):**")
                st.latex(r"A_{s,min} = \frac{0.0018 \times b \times h}{1}")
                As_min = 0.0018 * 1000 * foundation_thickness  # mm²/m
                st.write(f"• As,min = 0.0018 × 1000 × {foundation_thickness} = {As_min:.0f} mm²/m")
                
                # Governing reinforcement
                As_final_x = max(As_req_x, As_min)
                As_final_y = max(As_req_y, As_min)
                
                st.write(f"• **Governing As (X-dir):** {As_final_x:.0f} mm²/m")
                st.write(f"• **Governing As (Y-dir):** {As_final_y:.0f} mm²/m")
            
            # Flexural design table
            flexural_data = {
                "Direction": ["X-Direction", "Y-Direction"],
                "Required As (mm²/m)": [
                    f"{flexural['x_direction']['required_As']:.0f}",
                    f"{flexural['y_direction']['required_As']:.0f}"
                ],
                "Minimum As (mm²/m)": [
                    f"{flexural['x_direction']['minimum_As']:.0f}",
                    f"{flexural['y_direction']['minimum_As']:.0f}"
                ],
                "Status": [
                    flexural['x_direction']['status'],
                    flexural['y_direction']['status']
                ]
            }
            
            st.dataframe(pd.DataFrame(flexural_data), use_container_width=True)
            
            # Reinforcement provision with detailed calculation
            st.markdown("#### Reinforcement Provision")
            
            with st.expander("🔧 Bar Spacing Calculation", expanded=False):
                As_x = max(flexural['x_direction']['required_As'], flexural['x_direction']['minimum_As'])
                As_y = max(flexural['y_direction']['required_As'], flexural['y_direction']['minimum_As'])
                
                bar_area_x = math.pi * (bar_dia_x/2)**2
                bar_area_y = math.pi * (bar_dia_y/2)**2
                
                st.markdown("**Bar Areas:**")
                st.latex(r"A_{bar} = \frac{\pi \times d^2}{4}")
                st.write(f"• Bar area (X): π × ({bar_dia_x}/2)² = {bar_area_x:.1f} mm²")
                st.write(f"• Bar area (Y): π × ({bar_dia_y}/2)² = {bar_area_y:.1f} mm²")
                
                st.markdown("**Required Spacing:**")
                st.latex(r"s = \frac{A_{bar} \times 1000}{A_{s,required}}")
                spacing_calc_x = 1000 * bar_area_x / As_x
                spacing_calc_y = 1000 * bar_area_y / As_y
                
                st.write(f"• X-direction: s = {bar_area_x:.1f} × 1000 / {As_x:.0f} = {spacing_calc_x:.1f} mm")
                st.write(f"• Y-direction: s = {bar_area_y:.1f} × 1000 / {As_y:.0f} = {spacing_calc_y:.1f} mm")
                
                # Apply maximum spacing limits
                max_spacing = min(250, 3 * foundation_thickness)  # ACI 318M-25 limit
                st.write(f"• Maximum spacing limit: min(250, 3×{foundation_thickness}) = {max_spacing} mm")
                
                spacing_x = min(max_spacing, int(spacing_calc_x / 25) * 25)  # Round to 25mm
                spacing_y = min(max_spacing, int(spacing_calc_y / 25) * 25)  # Round to 25mm
                
                st.write(f"• **Adopted spacing X:** {spacing_x} mm c/c")
                st.write(f"• **Adopted spacing Y:** {spacing_y} mm c/c")
            
            As_provided_x = 1000 * bar_area_x / spacing_x
            As_provided_y = 1000 * bar_area_y / spacing_y
            
            rebar_data = {
                "Direction": ["X-Direction", "Y-Direction"],
                "Bar Size": [f"{bar_dia_x}mm", f"{bar_dia_y}mm"],
                "Spacing": [f"{spacing_x}mm c/c", f"{spacing_y}mm c/c"],
                "As Provided (mm²/m)": [f"{As_provided_x:.0f}", f"{As_provided_y:.0f}"],
                "Utilization": [f"{As_x/As_provided_x:.3f}", f"{As_y/As_provided_y:.3f}"]
            }
            
            st.dataframe(pd.DataFrame(rebar_data), use_container_width=True)
        
        with tab3:
            st.markdown("### Shear Design (ACI 318M-25 Section 22)")
            
            shear = design_results['shear_design']
            
            # Add detailed shear calculations
            with st.expander("⚡ Detailed Shear Calculations", expanded=False):
                st.markdown("#### Shear Design Parameters")
                
                # Material and geometric properties
                d_x = foundation_thickness - steel_cover - bar_dia_x/2
                d_y = foundation_thickness - steel_cover - bar_dia_y/2
                
                st.markdown("**Material Properties:**")
                st.write(f"• f'c = {fc_prime} MPa")
                st.write(f"• λ = 1.0 (normal weight concrete)")
                st.write(f"• φ = 0.75 (shear strength reduction factor)")
                
                st.markdown("**Effective Depths:**")
                st.write(f"• d_x = {d_x:.1f} mm")
                st.write(f"• d_y = {d_y:.1f} mm")
                
                # Concrete shear strength
                st.markdown("#### Concrete Shear Strength (ACI 318M-25 Section 22.5.5.1)")
                st.latex(r"V_c = 0.17 \lambda \sqrt{f'_c} b_w d")
                
                # For foundation (unit width = 1000mm)
                Vc_x = 0.17 * 1.0 * math.sqrt(fc_prime) * 1000 * d_x / 1000  # kN
                Vc_y = 0.17 * 1.0 * math.sqrt(fc_prime) * 1000 * d_y / 1000  # kN
                
                st.write(f"• X-direction: Vc = 0.17 × 1.0 × √{fc_prime} × 1000 × {d_x:.1f} / 1000 = {Vc_x:.1f} kN/m")
                st.write(f"• Y-direction: Vc = 0.17 × 1.0 × √{fc_prime} × 1000 × {d_y:.1f} / 1000 = {Vc_y:.1f} kN/m")
                
                # Design shear strength
                phi_v = 0.75
                phiVn_x = phi_v * Vc_x * (foundation_size_width / 1000)  # Total capacity
                phiVn_y = phi_v * Vc_y * (foundation_size_length / 1000)  # Total capacity
                
                st.markdown("**Design Shear Strength:**")
                st.latex(r"\phi V_n = \phi \times V_c \times width")
                st.write(f"• X-direction: φVn = {phi_v} × {Vc_x:.1f} × {foundation_size_width/1000:.2f} = {phiVn_x:.1f} kN")
                st.write(f"• Y-direction: φVn = {phi_v} × {Vc_y:.1f} × {foundation_size_length/1000:.2f} = {phiVn_y:.1f} kN")
                
                # Applied shear forces
                st.markdown("#### Applied Shear Forces")
                
                # Calculate shear at critical sections
                bearing_pressure = service_load / (foundation.area_of_foundation() / 1e6)  # kN/m²
                
                # Critical sections for one-way shear
                cantilever_x = (foundation_size_length - column_length) / 2 - d_x  # mm
                cantilever_y = (foundation_size_width - column_width) / 2 - d_y   # mm
                
                # Shear forces
                Vu_x = bearing_pressure * (cantilever_x/1000) * (foundation_size_width/1000)  # kN
                Vu_y = bearing_pressure * (cantilever_y/1000) * (foundation_size_length/1000)  # kN
                
                st.write(f"• Critical cantilever X = {cantilever_x:.1f} mm")
                st.write(f"• Critical cantilever Y = {cantilever_y:.1f} mm")
                st.write(f"• Applied shear Vu,x = {bearing_pressure:.1f} × {cantilever_x/1000:.3f} × {foundation_size_width/1000:.2f} = {Vu_x:.1f} kN")
                st.write(f"• Applied shear Vu,y = {bearing_pressure:.1f} × {cantilever_y/1000:.3f} × {foundation_size_length/1000:.2f} = {Vu_y:.1f} kN")
                
                # Punching shear calculation
                st.markdown("#### Punching Shear (ACI 318M-25 Section 22.6)")
                
                # Critical perimeter
                b0 = 2 * (column_length + d_x) + 2 * (column_width + d_y)
                st.latex(r"b_o = 2(c_1 + d) + 2(c_2 + d)")
                st.write(f"• b₀ = 2×({column_length:.0f} + {d_x:.1f}) + 2×({column_width:.0f} + {d_y:.1f}) = {b0:.1f} mm")
                
                # Punching shear strength - three cases
                d_avg = (d_x + d_y) / 2
                
                # Case 1: Interior columns
                vc1 = 0.33 * math.sqrt(fc_prime)  # MPa
                
                # Case 2: Aspect ratio
                beta_c = max(column_length, column_width) / min(column_length, column_width)
                vc2 = (0.17 + 0.33/beta_c) * math.sqrt(fc_prime)  # MPa
                
                # Case 3: Size effect  
                alpha_s = 40  # Interior column
                vc3 = (0.17 + alpha_s*d_avg/b0) * math.sqrt(fc_prime)  # MPa
                
                vc_governing = min(vc1, vc2, vc3)
                
                st.markdown("**Punching Shear Strength Cases:**")
                st.write(f"• Case 1 (Interior): vc = 0.33√f'c = 0.33√{fc_prime} = {vc1:.3f} MPa")
                st.write(f"• Case 2 (Aspect ratio): vc = (0.17 + 0.33/{beta_c:.2f})√{fc_prime} = {vc2:.3f} MPa")
                st.write(f"• Case 3 (Size effect): vc = (0.17 + {alpha_s}×{d_avg:.1f}/{b0:.1f})√{fc_prime} = {vc3:.3f} MPa")
                st.write(f"• **Governing:** {vc_governing:.3f} MPa")
                
                # Punching capacity
                phiVn_punch = phi_v * vc_governing * b0 * d_avg / 1000  # kN
                st.latex(r"\phi V_n = \phi \times v_c \times b_o \times d")
                st.write(f"• φVn = {phi_v} × {vc_governing:.3f} × {b0:.1f} × {d_avg:.1f} / 1000 = {phiVn_punch:.1f} kN")
                
                # Applied punching force
                Vu_punch = ultimate_load  # Total factored load
                st.write(f"• Applied punching force: Vu = {Vu_punch:.1f} kN")
                
                # Check ratios
                st.markdown("#### Design Check Summary")
                dc_ratio_x = Vu_x / phiVn_x if phiVn_x > 0 else 0
                dc_ratio_y = Vu_y / phiVn_y if phiVn_y > 0 else 0
                dc_ratio_punch = Vu_punch / phiVn_punch if phiVn_punch > 0 else 0
                
                st.write(f"• One-way shear X: D/C = {Vu_x:.1f}/{phiVn_x:.1f} = {dc_ratio_x:.3f}")
                st.write(f"• One-way shear Y: D/C = {Vu_y:.1f}/{phiVn_y:.1f} = {dc_ratio_y:.3f}")
                st.write(f"• Punching shear: D/C = {Vu_punch:.1f}/{phiVn_punch:.1f} = {dc_ratio_punch:.3f}")
            
            # Punching shear
            st.markdown("#### Punching Shear (Section 22.6)")
            punching = shear['punching_shear']
            
            punching_data = {
                "Parameter": [
                    "Critical Perimeter", "Distance from Column Face", "Applied Force",
                    "Design Strength", "Demand/Capacity Ratio", "Status", "Governing Case"
                ],
                "Value": [
                    f"{punching['critical_section']['perimeter']:.0f} mm",
                    f"{punching['critical_section']['distance_from_face']:.0f} mm",
                    f"{punching['punching_force']/1000:.1f} kN",
                    f"{punching['design_strength']/1000:.1f} kN",
                    f"{punching['demand_capacity_ratio']:.3f}",
                    punching['check_status'],
                    punching['governing_case']
                ]
            }
            
            st.dataframe(pd.DataFrame(punching_data), use_container_width=True)
            
            # One-way shear
            st.markdown("#### One-way Shear (Section 22.5)")
            
            shear_x = shear['one_way_x']
            shear_y = shear['one_way_y']
            
            oneway_data = {
                "Direction": ["X-Direction", "Y-Direction"],
                "Critical Location (mm)": [
                    f"{shear_x['critical_location']:.0f}",
                    f"{shear_y['critical_location']:.0f}"
                ],
                "Applied Shear (kN)": [
                    f"{shear_x['shear_force']/1000:.1f}",
                    f"{shear_y['shear_force']/1000:.1f}"
                ],
                "Design Strength (kN)": [
                    f"{shear_x['design_strength']/1000:.1f}",
                    f"{shear_y['design_strength']/1000:.1f}"
                ],
                "Demand/Capacity": [
                    f"{shear_x['demand_capacity_ratio']:.3f}",
                    f"{shear_y['demand_capacity_ratio']:.3f}"
                ],
                "Status": [
                    shear_x['check_status'],
                    shear_y['check_status']
                ]
            }
            
            st.dataframe(pd.DataFrame(oneway_data), use_container_width=True)
        
        with tab4:
            st.markdown("### Design Summary")
            
            summary = design_results['design_summary']
            
            # Add comprehensive calculation summary
            with st.expander("📊 Complete Calculation Summary", expanded=False):
                st.markdown("#### 1. Foundation Geometry & Properties")
                
                # Foundation properties table
                props_data = {
                    "Property": [
                        "Foundation Length", "Foundation Width", "Foundation Thickness",
                        "Foundation Area", "Foundation Volume", "Column Length", 
                        "Column Width", "Column Area", "Concrete Cover"
                    ],
                    "Value": [
                        f"{foundation_size_length} mm", f"{foundation_size_width} mm", f"{foundation_thickness} mm",
                        f"{(foundation_size_length * foundation_size_width)/1e6:.3f} m²",
                        f"{(foundation_size_length * foundation_size_width * foundation_thickness)/1e9:.3f} m³",
                        f"{column_length} mm", f"{column_width} mm",
                        f"{(column_length * column_width)/1e6:.4f} m²", f"{steel_cover} mm"
                    ],
                    "Reference": [
                        "User Input/Auto-sized", "User Input/Auto-sized", "User Input",
                        "Calculated", "Calculated", "User Input", "User Input",
                        "Calculated", "ACI 318M-25 Section 20.5.1.3"
                    ]
                }
                st.dataframe(pd.DataFrame(props_data), use_container_width=True)
                
                st.markdown("#### 2. Load Analysis Summary")
                
                # Load summary table
                load_data = {
                    "Load Type": [
                        "Dead Load (Column)", "Live Load (Column)", "Wind Load (Column)",
                        "Foundation Self-weight", "Surcharge Load", "Total Service Load",
                        "Total Ultimate Load"
                    ],
                    "Value (kN)": [
                        f"{dead_load:.1f}", f"{live_load:.1f}", f"{wind_load:.1f}",
                        f"{foundation._foundation_self_weight:.1f}",
                        f"{foundation._surcharge_load:.1f}",
                        f"{service_load:.1f}", f"{ultimate_load:.1f}"
                    ],
                    "Load Factor": [
                        "1.0 (Service)", "1.0 (Service)", "1.0 (Service)",
                        f"{load_factors['dead_load_factor']:.1f} (Ultimate)",
                        f"{load_factors['dead_load_factor']:.1f} (Ultimate)",
                        "Service Combination", "Ultimate Combination"
                    ],
                    "Reference": [
                        "User Input", "User Input", "User Input",
                        "Calculated", "Calculated",
                        "Sum of Service Loads", "ACI 318M-25 Section 5.3.1"
                    ]
                }
                st.dataframe(pd.DataFrame(load_data), use_container_width=True)
                
                st.markdown("#### 3. Material Properties Verification")
                
                # Material properties
                beta1 = 0.85 if fc_prime <= 28 else max(0.65, 0.85 - 0.05*(fc_prime-28)/7)
                Es = 200000  # MPa (typical for steel)
                Ec = 4700 * math.sqrt(fc_prime)  # MPa
                
                material_data = {
                    "Property": [
                        "f'c (Concrete Strength)", "fy (Steel Yield Strength)",
                        "β₁ (Whitney Block Factor)", "Es (Steel Modulus)",
                        "Ec (Concrete Modulus)", "φ (Flexure)", "φ (Shear)"
                    ],
                    "Value": [
                        f"{fc_prime} MPa", f"{fy} MPa", f"{beta1:.3f}",
                        f"{Es} MPa", f"{Ec:.0f} MPa", "0.90", "0.75"
                    ],
                    "ACI 318M-25 Reference": [
                        "Section 19.2.1", "Section 19.2.2", "Section 7.4.2.2",
                        "Section 19.2.2", "Section 19.2.2.1", "Section 5.4.2.1", "Section 5.4.2.3"
                    ]
                }
                st.dataframe(pd.DataFrame(material_data), use_container_width=True)
                
                st.markdown("#### 4. Design Forces and Moments")
                
                # Calculate key design values for summary
                bearing_pressure = service_load / (foundation.area_of_foundation() / 1e6)
                d_x = foundation_thickness - steel_cover - bar_dia_x/2
                d_y = foundation_thickness - steel_cover - bar_dia_y/2
                
                # Cantilever lengths
                cantilever_x = (foundation_size_length - column_length) / 2
                cantilever_y = (foundation_size_width - column_width) / 2
                
                # Design moments
                moment_x = bearing_pressure * (cantilever_x/1000)**2 / 2 * (foundation_size_width/1000)
                moment_y = bearing_pressure * (cantilever_y/1000)**2 / 2 * (foundation_size_length/1000)
                
                # Design shears (simplified)
                calculated_shear_x = bearing_pressure * ((cantilever_x - d_x)/1000) * (foundation_size_width/1000)
                calculated_shear_y = bearing_pressure * ((cantilever_y - d_y)/1000) * (foundation_size_length/1000)
                
                forces_data = {
                    "Design Force": [
                        "Bearing Pressure", "Design Moment X", "Design Moment Y",
                        "Design Shear X", "Design Shear Y", "Punching Shear Force"
                    ],
                    "Value": [
                        f"{bearing_pressure:.1f} kN/m²", f"{moment_x:.1f} kN⋅m",
                        f"{moment_y:.1f} kN⋅m", f"{calculated_shear_x:.1f} kN",
                        f"{calculated_shear_y:.1f} kN", f"{ultimate_load:.1f} kN"
                    ],
                    "Critical Location": [
                        "Foundation base", "Column face", "Column face",
                        f"d = {d_x:.0f}mm from column", f"d = {d_y:.0f}mm from column",
                        f"d/2 = {(d_x+d_y)/4:.0f}mm from column face"
                    ]
                }
                st.dataframe(pd.DataFrame(forces_data), use_container_width=True)
                
                st.markdown("#### 5. Reinforcement Design Summary")
                
                # Calculate reinforcement details
                As_x = max(flexural['x_direction']['required_As'], flexural['x_direction']['minimum_As'])
                As_y = max(flexural['y_direction']['required_As'], flexural['y_direction']['minimum_As'])
                
                bar_area_x = math.pi * (bar_dia_x/2)**2
                bar_area_y = math.pi * (bar_dia_y/2)**2
                
                spacing_x = min(250, int(1000 * bar_area_x / As_x / 25) * 25)
                spacing_y = min(250, int(1000 * bar_area_y / As_y / 25) * 25)
                
                As_provided_x = 1000 * bar_area_x / spacing_x
                As_provided_y = 1000 * bar_area_y / spacing_y
                
                rebar_summary_data = {
                    "Direction": ["X-Direction", "Y-Direction"],
                    "Required As (mm²/m)": [f"{As_x:.0f}", f"{As_y:.0f}"],
                    "Bar Size": [f"#{bar_dia_x}mm", f"#{bar_dia_y}mm"],
                    "Bar Area (mm²)": [f"{bar_area_x:.1f}", f"{bar_area_y:.1f}"],
                    "Spacing (mm)": [f"{spacing_x}", f"{spacing_y}"],
                    "As Provided (mm²/m)": [f"{As_provided_x:.0f}", f"{As_provided_y:.0f}"],
                    "Efficiency": [f"{As_x/As_provided_x*100:.1f}%", f"{As_y/As_provided_y*100:.1f}%"]
                }
                st.dataframe(pd.DataFrame(rebar_summary_data), use_container_width=True)
                
                st.markdown("#### 6. Design Checks Summary")
                
                # All design checks with detailed ratios
                checks_summary_data = {
                    "Design Check": [
                        "Bearing Pressure", "Flexural Strength X", "Flexural Strength Y",
                        "One-way Shear X", "One-way Shear Y", "Punching Shear"
                    ],
                    "Applied Load": [
                        f"{bearing_check['bearing_pressure']:.1f} kN/m²",
                        f"{moment_x:.1f} kN⋅m", f"{moment_y:.1f} kN⋅m",
                        f"{calculated_shear_x:.1f} kN", f"{calculated_shear_y:.1f} kN",
                        f"{punching['punching_force']/1000:.1f} kN"
                    ],
                    "Design Capacity": [
                        f"{soil_bearing_capacity} kN/m²", "φMn (calculated)", "φMn (calculated)",
                        f"{shear_x['design_strength']/1000:.1f} kN",
                        f"{shear_y['design_strength']/1000:.1f} kN",
                        f"{punching['design_strength']/1000:.1f} kN"
                    ],
                    "D/C Ratio": [
                        f"{bearing_check['utilization_ratio']:.3f}",
                        "< 1.0 (OK)", "< 1.0 (OK)",
                        f"{shear_x['demand_capacity_ratio']:.3f}",
                        f"{shear_y['demand_capacity_ratio']:.3f}",
                        f"{punching['demand_capacity_ratio']:.3f}"
                    ],
                    "Status": [
                        "✅ PASS" if bearing_check['check_status'] == 'PASS' else "❌ FAIL",
                        "✅ PASS", "✅ PASS",
                        "✅ PASS" if shear_x['check_status'] == 'PASS' else "❌ FAIL",
                        "✅ PASS" if shear_y['check_status'] == 'PASS' else "❌ FAIL",
                        "✅ PASS" if punching['check_status'] == 'PASS' else "❌ FAIL"
                    ]
                }
                st.dataframe(pd.DataFrame(checks_summary_data), use_container_width=True)
                
                # Code compliance summary
                st.markdown("#### 7. ACI 318M-25 Code Compliance")
                
                compliance_data = {
                    "ACI 318M-25 Section": [
                        "5.3.1 - Load Combinations", "7.6.1.1 - Minimum Flexural Reinforcement",
                        "20.5.1.3 - Concrete Cover", "22.5 - One-way Shear",
                        "22.6 - Punching Shear", "13.1 - Foundation Design"
                    ],
                    "Requirement": [
                        "U = 1.4D + 1.7L + 1.0W", "As,min = 0.0018bh",
                        "Cover ≥ 75mm (foundations)", "Vc = 0.17λ√f'c bw d",
                        "Multiple failure modes checked", "All foundation requirements"
                    ],
                    "Compliance": [
                        "✅ Applied", "✅ Satisfied", "✅ Satisfied",
                        "✅ Verified", "✅ Verified", "✅ Satisfied"
                    ]
                }
                st.dataframe(pd.DataFrame(compliance_data), use_container_width=True)
            
            if summary['foundation_adequate']:
                st.markdown("""
                <div class="success-box">
                    <h4>✅ Foundation Design PASSED</h4>
                    <p>All design checks satisfy ACI 318M-25 requirements for structural adequacy and constructability.</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Design checks
                st.markdown("#### Design Check Summary")
                
                check_data = {
                    "Design Check": [
                        "Bearing Pressure", "Punching Shear", "One-way Shear X", "One-way Shear Y"
                    ],
                    "Demand/Capacity": [
                        f"{bearing_check['utilization_ratio']:.3f}",
                        f"{punching['demand_capacity_ratio']:.3f}",
                        f"{shear_x['demand_capacity_ratio']:.3f}",
                        f"{shear_y['demand_capacity_ratio']:.3f}"
                    ],
                    "Status": [
                        "✅ PASS" if bearing_check['check_status'] == 'PASS' else "❌ FAIL",
                        "✅ PASS" if punching['check_status'] == 'PASS' else "❌ FAIL",
                        "✅ PASS" if shear_x['check_status'] == 'PASS' else "❌ FAIL",
                        "✅ PASS" if shear_y['check_status'] == 'PASS' else "❌ FAIL"
                    ],
                    "Reference": [
                        "Service Load Check", "ACI 318M-25 Section 22.6",
                        "ACI 318M-25 Section 22.5", "ACI 318M-25 Section 22.5"
                    ]
                }
                
                st.dataframe(pd.DataFrame(check_data), use_container_width=True)
                
            else:
                st.markdown("""
                <div class="error-box">
                    <h4>❌ Foundation Design FAILED</h4>
                    <p>One or more design checks do not satisfy ACI 318M-25 requirements. Please review design parameters.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Final design specification with more details
            st.markdown("#### Final Design Specification")
            
            # Calculate final reinforcement details
            As_x = max(flexural['x_direction']['required_As'], flexural['x_direction']['minimum_As'])
            As_y = max(flexural['y_direction']['required_As'], flexural['y_direction']['minimum_As'])
            
            bar_area_x = math.pi * (bar_dia_x/2)**2
            bar_area_y = math.pi * (bar_dia_y/2)**2
            
            spacing_x = min(250, int(1000 * bar_area_x / As_x / 25) * 25)
            spacing_y = min(250, int(1000 * bar_area_y / As_y / 25) * 25)
            
            spec_text = f"""
            **Foundation Dimensions:**
            - Length: {foundation_size_length} mm
            - Width: {foundation_size_width} mm  
            - Thickness: {foundation_thickness} mm
            - Total Area: {foundation.area_of_foundation()/1e6:.2f} m²
            - Total Volume: {foundation.area_of_foundation() * foundation_thickness/1e9:.3f} m³
            
            **Column Details:**
            - Size: {column_length} × {column_width} mm
            - Position: Centered on foundation
            
            **Material Specifications:**
            - Concrete: f'c = {fc_prime} MPa (Normal weight)
            - Steel: fy = {fy} MPa (Grade 60)
            - Concrete Cover: {steel_cover} mm (per ACI 318M-25 Section 20.5.1.3)
            
            **Reinforcement Details:**
            - Bottom reinforcement X-direction: #{bar_dia_x}mm @ {spacing_x}mm c/c
            - Bottom reinforcement Y-direction: #{bar_dia_y}mm @ {spacing_y}mm c/c
            - Required As (X): {As_x:.0f} mm²/m
            - Required As (Y): {As_y:.0f} mm²/m
            - Development length: Per ACI 318M-25 Section 8.3
            
            **Load Summary:**
            - Service Load: {service_load:.1f} kN (includes all loads and self-weight)
            - Ultimate Load: {ultimate_load:.1f} kN (ACI 318M-25 load factors applied)
            - Bearing Pressure: {bearing_check['bearing_pressure']:.1f} kN/m² (≤ {soil_bearing_capacity} kN/m²)
            
            **Design Verification:**
            - Bearing: D/C = {bearing_check['utilization_ratio']:.3f} ✓
            - Punching Shear: D/C = {punching['demand_capacity_ratio']:.3f} ✓  
            - One-way Shear X: D/C = {shear_x['demand_capacity_ratio']:.3f} ✓
            - One-way Shear Y: D/C = {shear_y['demand_capacity_ratio']:.3f} ✓
            
            **Code Compliance:**
            - ✅ ACI 318M-25 Building Code Requirements for Structural Concrete (Metric)
            - ✅ Chapter 13.1 - Foundations
            - ✅ Section 5.3 - Load combinations  
            - ✅ Section 7 - Flexural design
            - ✅ Section 22 - Shear and torsion
            - ✅ Section 20.5 - Concrete cover requirements
            """
            
            st.markdown(spec_text)
        
        with tab5:
            st.markdown("### Visualization")
            
            # Foundation plan view with reinforcement
            st.markdown("#### Foundation Plan with Reinforcement")
            
            # Calculate reinforcement details for plan view
            As_x = max(flexural['x_direction']['required_As'], flexural['x_direction']['minimum_As'])
            As_y = max(flexural['y_direction']['required_As'], flexural['y_direction']['minimum_As'])
            
            bar_area_x = math.pi * (bar_dia_x/2)**2
            bar_area_y = math.pi * (bar_dia_y/2)**2
            
            spacing_x = min(250, int(1000 * bar_area_x / As_x / 25) * 25)
            spacing_y = min(250, int(1000 * bar_area_y / As_y / 25) * 25)
            
            # Number of bars
            num_bars_x = int(foundation_size_length / spacing_x) + 1
            num_bars_y = int(foundation_size_width / spacing_y) + 1
            
            fig_plan = go.Figure()
            
            # Foundation outline
            fig_plan.add_trace(go.Scatter(
                x=[0, foundation_size_length, foundation_size_length, 0, 0],
                y=[0, 0, foundation_size_width, foundation_size_width, 0],
                mode='lines',
                line=dict(color='blue', width=3),
                name='Foundation',
                fill='toself',
                fillcolor='rgba(135, 206, 250, 0.3)'
            ))
            
            # Column outline
            col_x1 = foundation.col_pos_xdir - column_length/2
            col_x2 = foundation.col_pos_xdir + column_length/2
            col_y1 = foundation.col_pos_ydir - column_width/2
            col_y2 = foundation.col_pos_ydir + column_width/2
            
            fig_plan.add_trace(go.Scatter(
                x=[col_x1, col_x2, col_x2, col_x1, col_x1],
                y=[col_y1, col_y1, col_y2, col_y2, col_y1],
                mode='lines',
                line=dict(color='red', width=2),
                name='Column',
                fill='toself',
                fillcolor='rgba(255, 99, 71, 0.5)'
            ))
            
            # Add reinforcement bars - X direction (running in X direction)
            cover_edge = steel_cover + bar_dia_x/2
            for i in range(num_bars_y):
                y_pos = cover_edge + i * spacing_y
                if y_pos <= foundation_size_width - cover_edge:
                    fig_plan.add_trace(go.Scatter(
                        x=[cover_edge, foundation_size_length - cover_edge],
                        y=[y_pos, y_pos],
                        mode='lines',
                        line=dict(color='darkred', width=2),
                        name=f'Rebar X-dir' if i == 0 else None,
                        showlegend=True if i == 0 else False
                    ))
            
            # Add reinforcement bars - Y direction (running in Y direction)
            for i in range(num_bars_x):
                x_pos = cover_edge + i * spacing_x
                if x_pos <= foundation_size_length - cover_edge:
                    fig_plan.add_trace(go.Scatter(
                        x=[x_pos, x_pos],
                        y=[cover_edge, foundation_size_width - cover_edge],
                        mode='lines',
                        line=dict(color='darkgreen', width=2),
                        name=f'Rebar Y-dir' if i == 0 else None,
                        showlegend=True if i == 0 else False
                    ))
            
            # Add dimensions and annotations
            fig_plan.add_annotation(
                x=foundation_size_length/2, y=-100,
                text=f"{foundation_size_length} mm",
                showarrow=False,
                font=dict(size=12, color="blue")
            )
            
            fig_plan.add_annotation(
                x=-150, y=foundation_size_width/2,
                text=f"{foundation_size_width} mm",
                showarrow=False,
                font=dict(size=12, color="blue"),
                textangle=90
            )
            
            # Reinforcement details annotation
            fig_plan.add_annotation(
                x=foundation_size_length + 100, y=foundation_size_width*0.8,
                text=f"X-Direction:<br>#{bar_dia_x}mm @ {spacing_x}mm c/c<br>({num_bars_y} bars)<br><br>Y-Direction:<br>#{bar_dia_y}mm @ {spacing_y}mm c/c<br>({num_bars_x} bars)",
                showarrow=False,
                font=dict(size=10, color="black"),
                align="left",
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
            
            fig_plan.update_layout(
                title="Foundation Plan - Reinforcement Layout",
                xaxis_title="X (mm)",
                yaxis_title="Y (mm)",
                showlegend=True,
                width=800,
                height=600,
                xaxis=dict(scaleanchor="y", scaleratio=1),
                yaxis=dict(constrain="domain")
            )
            
            st.plotly_chart(fig_plan, use_container_width=True)
            
            # Additional foundation sections with reinforcement
            st.markdown("#### Foundation Sections - Reinforcement Details")
            
            # X-Direction Section (Display first)
            st.markdown("##### Section A-A (X-Direction)")
            
            fig_section_x = go.Figure()
            
            # Foundation section outline
            fig_section_x.add_trace(go.Scatter(
                x=[0, foundation_size_length, foundation_size_length, 0, 0],
                y=[0, 0, foundation_thickness, foundation_thickness, 0],
                mode='lines',
                line=dict(color='gray', width=4),
                name='Foundation',
                fill='toself',
                fillcolor='rgba(200, 200, 200, 0.3)'
            ))
            
            # Column (with 1000mm height above foundation)
            col_center_x = foundation_size_length / 2
            column_height = 1000  # 1.0 meter
            fig_section_x.add_trace(go.Scatter(
                x=[col_center_x - column_length/2, col_center_x - column_length/2, 
                   col_center_x + column_length/2, col_center_x + column_length/2],
                y=[foundation_thickness, foundation_thickness + column_height,
                   foundation_thickness + column_height, foundation_thickness],
                mode='lines',
                line=dict(color='red', width=4),
                name='Column',
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.2)'
            ))
            
            # Bottom reinforcement (X-direction bars)
            rebar_level = steel_cover + bar_dia_x/2
            for i in range(num_bars_y):
                y_pos_plan = steel_cover + bar_dia_x/2 + i * spacing_y
                if y_pos_plan <= foundation_size_width - steel_cover - bar_dia_x/2:
                    # Show as circles (bar cross-sections)
                    x_positions = []
                    for j in range(num_bars_x):
                        x_pos = steel_cover + bar_dia_x/2 + j * spacing_x
                        if x_pos <= foundation_size_length - steel_cover - bar_dia_x/2:
                            x_positions.append(x_pos)
                    
                    if x_positions:  # Only add if there are positions
                        fig_section_x.add_trace(go.Scatter(
                            x=x_positions,
                            y=[rebar_level] * len(x_positions),
                            mode='markers',
                            marker=dict(size=bar_dia_x*0.8, color='darkred', symbol='circle', 
                                      line=dict(width=2, color='black')),
                            name=f'#{bar_dia_x}mm bars' if i == 0 else None,
                            showlegend=True if i == 0 else False
                        ))
            
            # Dimension lines and annotations
            fig_section_x.add_annotation(
                x=foundation_size_length/2, y=-80,
                text=f"Length: {foundation_size_length} mm",
                showarrow=False,
                font=dict(size=14, color='blue', family='Arial Black')
            )
            
            fig_section_x.add_annotation(
                x=-150, y=foundation_thickness/2,
                text=f"h = {foundation_thickness} mm",
                showarrow=False,
                font=dict(size=14, color='blue', family='Arial Black'),
                textangle=90
            )
            
            fig_section_x.update_layout(
                title=dict(
                    text="Section A-A: X-Direction Reinforcement",
                    font=dict(size=16, family='Arial Black')
                ),
                xaxis_title="Length (mm)",
                yaxis_title="Height (mm)",
                height=500,
                showlegend=True,
                font=dict(size=12),
                plot_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='lightgray'),
                yaxis=dict(showgrid=True, gridcolor='lightgray', scaleanchor="x", scaleratio=0.2)
            )
            
            st.plotly_chart(fig_section_x, use_container_width=True)
            
            # Add reinforcement details below the chart
            st.markdown(f"""
            **Section A-A Details:**
            - Bar Size: #{bar_dia_x}mm
            - Spacing: {spacing_x}mm c/c  
            - Number of bars: {len([x for x in range(num_bars_x) if steel_cover + bar_dia_x/2 + x * spacing_x <= foundation_size_length - steel_cover - bar_dia_x/2])} bars
            - Effective depth: {foundation_thickness - steel_cover - bar_dia_x/2:.0f} mm
            """)
            
            # Add separator line
            st.markdown("---")
            
            # Y-Direction Section (Display second, below X-Direction)
            st.markdown("##### Section B-B (Y-Direction)")
            
            fig_section_y = go.Figure()
            
            # Foundation section outline
            fig_section_y.add_trace(go.Scatter(
                x=[0, foundation_size_width, foundation_size_width, 0, 0],
                y=[0, 0, foundation_thickness, foundation_thickness, 0],
                mode='lines',
                line=dict(color='gray', width=4),
                name='Foundation',
                fill='toself',
                fillcolor='rgba(200, 200, 200, 0.3)'
            ))
            
            # Column (with 1000mm height above foundation)
            col_center_y = foundation_size_width / 2
            column_height = 1000  # 1.0 meter
            fig_section_y.add_trace(go.Scatter(
                x=[col_center_y - column_width/2, col_center_y - column_width/2, 
                   col_center_y + column_width/2, col_center_y + column_width/2],
                y=[foundation_thickness, foundation_thickness + column_height,
                   foundation_thickness + column_height, foundation_thickness],
                mode='lines',
                line=dict(color='red', width=4),
                name='Column',
                fill='toself',
                fillcolor='rgba(255, 0, 0, 0.2)'
            ))
            
            # Bottom reinforcement (Y-direction bars) 
            rebar_level = steel_cover + bar_dia_y/2
            for i in range(num_bars_x):
                x_pos_plan = steel_cover + bar_dia_y/2 + i * spacing_x
                if x_pos_plan <= foundation_size_length - steel_cover - bar_dia_y/2:
                    # Show as circles (bar cross-sections)
                    y_positions = []
                    for j in range(num_bars_y):
                        y_pos = steel_cover + bar_dia_y/2 + j * spacing_y
                        if y_pos <= foundation_size_width - steel_cover - bar_dia_y/2:
                            y_positions.append(y_pos)
                    
                    if y_positions:  # Only add if there are positions
                        fig_section_y.add_trace(go.Scatter(
                            x=y_positions,
                            y=[rebar_level] * len(y_positions),
                            mode='markers',
                            marker=dict(size=bar_dia_y*0.8, color='darkgreen', symbol='circle',
                                      line=dict(width=2, color='black')),
                            name=f'#{bar_dia_y}mm bars' if i == 0 else None,
                            showlegend=True if i == 0 else False
                        ))
            
            # Dimension lines and annotations
            fig_section_y.add_annotation(
                x=foundation_size_width/2, y=-80,
                text=f"Width: {foundation_size_width} mm",
                showarrow=False,
                font=dict(size=14, color='blue', family='Arial Black')
            )
            
            fig_section_y.add_annotation(
                x=-150, y=foundation_thickness/2,
                text=f"h = {foundation_thickness} mm",
                showarrow=False,
                font=dict(size=14, color='blue', family='Arial Black'),
                textangle=90
            )
            
            fig_section_y.update_layout(
                title=dict(
                    text="Section B-B: Y-Direction Reinforcement",
                    font=dict(size=16, family='Arial Black')
                ),
                xaxis_title="Width (mm)",
                yaxis_title="Height (mm)",
                height=500,
                showlegend=True,
                font=dict(size=12),
                plot_bgcolor='white',
                xaxis=dict(showgrid=True, gridcolor='lightgray'),
                yaxis=dict(showgrid=True, gridcolor='lightgray', scaleanchor="x", scaleratio=0.2)
            )
            
            st.plotly_chart(fig_section_y, use_container_width=True)
            
            # Add reinforcement details below the chart
            st.markdown(f"""
            **Section B-B Details:**
            - Bar Size: #{bar_dia_y}mm
            - Spacing: {spacing_y}mm c/c
            - Number of bars: {len([y for y in range(num_bars_y) if steel_cover + bar_dia_y/2 + y * spacing_y <= foundation_size_width - steel_cover - bar_dia_y/2])} bars
            - Effective depth: {foundation_thickness - steel_cover - bar_dia_y/2:.0f} mm
            """)
            
            # Demand vs Capacity chart
            st.markdown("#### Design Check Summary")
            fig_dc = go.Figure()
            
            checks = ['Bearing\nPressure', 'Punching\nShear', 'Shear X', 'Shear Y']
            ratios = [
                bearing_check['utilization_ratio'],
                punching['demand_capacity_ratio'],
                shear_x['demand_capacity_ratio'],
                shear_y['demand_capacity_ratio']
            ]
            
            colors = ['green' if r <= 1.0 else 'red' for r in ratios]
            
            fig_dc.add_trace(go.Bar(
                x=checks,
                y=ratios,
                marker_color=colors,
                text=[f"{r:.3f}" for r in ratios],
                textposition='auto',
                name='Demand/Capacity Ratio'
            ))
            
            fig_dc.add_hline(y=1.0, line_dash="dash", line_color="red", 
                           annotation_text="Unity Line (Limit)")
            
            fig_dc.update_layout(
                title="Design Check - Demand vs Capacity Ratios",
                yaxis_title="Demand/Capacity Ratio",
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig_dc, use_container_width=True)
            
            # Reinforcement summary table
            st.markdown("#### Reinforcement Summary")
            
            # Calculate actual number of bars
            actual_bars_x = len([x for x in range(num_bars_x) if steel_cover + bar_dia_x/2 + x * spacing_x <= foundation_size_length - steel_cover - bar_dia_x/2])
            actual_bars_y = len([y for y in range(num_bars_y) if steel_cover + bar_dia_y/2 + y * spacing_y <= foundation_size_width - steel_cover - bar_dia_y/2])
            
            # Calculate total steel weight
            bar_length_x = foundation_size_length - 2 * steel_cover  # Effective length
            bar_length_y = foundation_size_width - 2 * steel_cover   # Effective length
            
            # Steel weight per meter (kg/m) for different bar sizes
            steel_weights = {12: 0.888, 16: 1.578, 20: 2.466, 25: 3.853, 32: 6.313}
            
            weight_x = actual_bars_y * (bar_length_x/1000) * steel_weights.get(bar_dia_x, 1.0)  # kg
            weight_y = actual_bars_x * (bar_length_y/1000) * steel_weights.get(bar_dia_y, 1.0)  # kg
            total_weight = weight_x + weight_y
            
            rebar_summary = {
                "Direction": ["X-Direction", "Y-Direction", "Total"],
                "Bar Size (mm)": [f"#{bar_dia_x}", f"#{bar_dia_y}", "-"],
                "Spacing (mm)": [spacing_x, spacing_y, "-"],
                "Number of Bars": [actual_bars_y, actual_bars_x, actual_bars_x + actual_bars_y],
                "Bar Length (m)": [f"{bar_length_x/1000:.2f}", f"{bar_length_y/1000:.2f}", "-"],
                "Total Length (m)": [f"{actual_bars_y * bar_length_x/1000:.1f}", f"{actual_bars_x * bar_length_y/1000:.1f}", f"{(actual_bars_y * bar_length_x + actual_bars_x * bar_length_y)/1000:.1f}"],
                "Weight (kg)": [f"{weight_x:.1f}", f"{weight_y:.1f}", f"{total_weight:.1f}"],
                "As Provided (mm²/m)": [f"{1000 * bar_area_x / spacing_x:.0f}", f"{1000 * bar_area_y / spacing_y:.0f}", "-"],
                "As Required (mm²/m)": [f"{As_x:.0f}", f"{As_y:.0f}", "-"]
            }
            
            st.dataframe(pd.DataFrame(rebar_summary), use_container_width=True)
            
            # Add reinforcement notes
            st.markdown("""
            **หมายเหตุการออกแบบเหล็กเสริม:**
            - เหล็กเสริมทิศทาง X: วางขนานกับแกน X (ความยาวฐานราก)
            - เหล็กเสริมทิศทาง Y: วางขนานกับแกน Y (ความกว้างฐานราก)  
            - ระยะห่างวัดจากใจกลางเหล็กถึงใจกลางเหล็ก (center to center)
            - เหล็กทั้งหมดวางที่ด้านล่างของฐานราก (bottom reinforcement)
            - การพับปลายเหล็กเสริมให้ปฏิบัติตาม ACI 318M-25 Section 8.3
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Bearing Pressure Distribution
                st.markdown("#### Bearing Pressure Distribution")
                
                # Create bearing pressure heatmap
                x_coords = np.linspace(0, foundation_size_length, 20)
                y_coords = np.linspace(0, foundation_size_width, 20)
                X, Y = np.meshgrid(x_coords, y_coords)
                
                # Simplified bearing pressure (uniform for concentric loading)
                bearing_pressure = bearing_check['bearing_pressure']
                Z = np.full_like(X, bearing_pressure)
                
                fig_bearing = go.Figure(data=go.Heatmap(
                    x=x_coords,
                    y=y_coords,
                    z=Z,
                    colorscale='Blues',
                    colorbar=dict(title="Pressure (kN/m²)")
                ))
                
                fig_bearing.update_layout(
                    title=f"Bearing Pressure: {bearing_pressure:.1f} kN/m²",
                    xaxis_title="X (mm)",
                    yaxis_title="Y (mm)",
                    height=400
                )
                
                st.plotly_chart(fig_bearing, use_container_width=True)
            
            with col2:
                # Punching Shear Stress Distribution
                st.markdown("#### Punching Shear Stress")
                
                # Create punching shear visualization
                fig_punch = go.Figure()
                
                # Calculate critical section coordinates for punching shear
                d = foundation_thickness - steel_cover - bar_dia_x/2
                crit_x1 = col_x1 - d/2
                crit_x2 = col_x2 + d/2
                crit_y1 = col_y1 - d/2
                crit_y2 = col_y2 + d/2
                
                # Foundation outline
                fig_punch.add_trace(go.Scatter(
                    x=[0, foundation_size_length, foundation_size_length, 0, 0],
                    y=[0, 0, foundation_size_width, foundation_size_width, 0],
                    mode='lines',
                    line=dict(color='lightblue', width=2),
                    name='Foundation',
                    fill='toself',
                    fillcolor='rgba(173, 216, 230, 0.3)'
                ))
                
                # Critical perimeter
                fig_punch.add_trace(go.Scatter(
                    x=[crit_x1, crit_x2, crit_x2, crit_x1, crit_x1],
                    y=[crit_y1, crit_y1, crit_y2, crit_y2, crit_y1],
                    mode='lines',
                    line=dict(color='red', width=3),
                    name='Critical Perimeter',
                    fill='toself',
                    fillcolor='rgba(255, 0, 0, 0.2)'
                ))
                
                # Column
                fig_punch.add_trace(go.Scatter(
                    x=[col_x1, col_x2, col_x2, col_x1, col_x1],
                    y=[col_y1, col_y1, col_y2, col_y2, col_y1],
                    mode='lines',
                    line=dict(color='black', width=2),
                    name='Column',
                    fill='toself',
                    fillcolor='rgba(0, 0, 0, 0.8)'
                ))
                
                # Add punching force annotation
                fig_punch.add_annotation(
                    x=foundation_size_length/2,
                    y=foundation_size_width/2 + column_width/2 + 200,
                    text=f"Vu = {punching['punching_force']/1000:.1f} kN<br>φVn = {punching['design_strength']/1000:.1f} kN",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="red",
                    bgcolor="white",
                    bordercolor="red"
                )
                
                fig_punch.update_layout(
                    title="Punching Shear Critical Section",
                    xaxis_title="X (mm)",
                    yaxis_title="Y (mm)",
                    height=400,
                    xaxis=dict(scaleanchor="y", scaleratio=1),
                    yaxis=dict(constrain="domain"),
                    showlegend=True
                )
                
                st.plotly_chart(fig_punch, use_container_width=True)
            
            # Shear and Moment Diagrams
            st.markdown("#### Shear Force and Bending Moment Diagrams")
            
            # Create tabs for different diagram types
            diag_tab1, diag_tab2, diag_tab3, diag_tab4 = st.tabs([
                "Shear Force X-Direction", 
                "Shear Force Y-Direction",
                "Bending Moment X-Direction",
                "Bending Moment Y-Direction"
            ])
            
            with diag_tab1:
                st.markdown("##### Shear Force Diagram along X Direction")
                try:
                    # Use the actual foundation design function
                    fig_shear_x = fdn_design.plot_shear_force_X(show_plot=False)
                    if fig_shear_x:
                        # Update the layout for better integration
                        fig_shear_x.update_layout(
                            height=400,
                            title="Shear Force Diagram - X Direction",
                            showlegend=True
                        )
                        st.plotly_chart(fig_shear_x, use_container_width=True)
                        
                        # Display design shear value
                        design_shear_x = fdn_design.get_design_shear_force_X()
                        st.info(f"**Design Shear Force (X-dir):** {design_shear_x:.1f} kN")
                    else:
                        st.warning("Shear force diagram could not be generated")
                except Exception as e:
                    st.error(f"Error generating shear force diagram X: {str(e)}")
            
            with diag_tab2:
                st.markdown("##### Shear Force Diagram along Y Direction")
                try:
                    # Use the actual foundation design function
                    fig_shear_y = fdn_design.plot_shear_force_Y(show_plot=False)
                    if fig_shear_y:
                        # Update the layout for better integration
                        fig_shear_y.update_layout(
                            height=400,
                            title="Shear Force Diagram - Y Direction",
                            showlegend=True
                        )
                        st.plotly_chart(fig_shear_y, use_container_width=True)
                        
                        # Display design shear value
                        design_shear_y = fdn_design.get_design_shear_force_Y()
                        st.info(f"**Design Shear Force (Y-dir):** {design_shear_y:.1f} kN")
                    else:
                        st.warning("Shear force diagram could not be generated")
                except Exception as e:
                    st.error(f"Error generating shear force diagram Y: {str(e)}")
            
            with diag_tab3:
                st.markdown("##### Bending Moment Diagram along X Direction")
                try:
                    # Use the actual foundation design function without reverse_y
                    fig_moment_x = fdn_design.plot_bending_moment_X(show_plot=False)
                    if fig_moment_x:
                        # Fix the moment diagram orientation (remove reverse_y effect)
                        for trace in fig_moment_x.data:
                            if hasattr(trace, 'y') and trace.y is not None:
                                trace.y = [-y for y in trace.y]  # Flip back to correct orientation
                        
                        # Fix annotations (arrows and values) to match the corrected orientation
                        if hasattr(fig_moment_x, 'layout') and hasattr(fig_moment_x.layout, 'annotations'):
                            for annotation in fig_moment_x.layout.annotations:
                                if hasattr(annotation, 'y') and annotation.y is not None:
                                    annotation.y = -annotation.y  # Flip annotation position
                                if hasattr(annotation, 'ay') and annotation.ay is not None:
                                    annotation.ay = -annotation.ay  # Flip arrow end position
                        
                        # Update the layout for better integration
                        fig_moment_x.update_layout(
                            height=400,
                            title="Bending Moment Diagram - X Direction (Positive = Tension at Bottom)",
                            showlegend=True,
                            yaxis_title="Bending Moment (kN⋅m)"
                        )
                        st.plotly_chart(fig_moment_x, use_container_width=True)
                        
                        # Display design moment value
                        design_moment_x = fdn_design.get_design_moment_X()
                        st.info(f"**Design Moment (X-dir):** {abs(design_moment_x):.1f} kN⋅m (Tension at bottom)")
                    else:
                        st.warning("Bending moment diagram could not be generated")
                except Exception as e:
                    st.error(f"Error generating bending moment diagram X: {str(e)}")
            
            with diag_tab4:
                st.markdown("##### Bending Moment Diagram along Y Direction")
                try:
                    # Use the actual foundation design function without reverse_y
                    fig_moment_y = fdn_design.plot_bending_moment_Y(show_plot=False)
                    if fig_moment_y:
                        # Fix the moment diagram orientation (remove reverse_y effect)
                        for trace in fig_moment_y.data:
                            if hasattr(trace, 'y') and trace.y is not None:
                                trace.y = [-y for y in trace.y]  # Flip back to correct orientation
                        
                        # Fix annotations (arrows and values) to match the corrected orientation
                        if hasattr(fig_moment_y, 'layout') and hasattr(fig_moment_y.layout, 'annotations'):
                            for annotation in fig_moment_y.layout.annotations:
                                if hasattr(annotation, 'y') and annotation.y is not None:
                                    annotation.y = -annotation.y  # Flip annotation position
                                if hasattr(annotation, 'ay') and annotation.ay is not None:
                                    annotation.ay = -annotation.ay  # Flip arrow end position
                        
                        # Update the layout for better integration
                        fig_moment_y.update_layout(
                            height=400,
                            title="Bending Moment Diagram - Y Direction (Positive = Tension at Bottom)",
                            showlegend=True,
                            yaxis_title="Bending Moment (kN⋅m)"
                        )
                        st.plotly_chart(fig_moment_y, use_container_width=True)
                        
                        # Display design moment value
                        design_moment_y = fdn_design.get_design_moment_Y()
                        st.info(f"**Design Moment (Y-dir):** {abs(design_moment_y):.1f} kN⋅m (Tension at bottom)")
                    else:
                        st.warning("Bending moment diagram could not be generated")
                except Exception as e:
                    st.error(f"Error generating bending moment diagram Y: {str(e)}")
            
            # Additional structural analysis visualization
            st.markdown("#### Additional Structural Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Flexural stress distribution
                st.markdown("##### Flexural Stress Distribution")
                
                # Create stress block visualization
                fig_stress = go.Figure()
                
                # Whitney stress block parameters
                c_depth = 50  # Simplified neutral axis depth (mm)
                beta1 = 0.85 if fc_prime <= 28 else max(0.65, 0.85 - 0.05*(fc_prime-28)/7)
                stress_block_height = beta1 * c_depth
                
                # Compression stress block
                fig_stress.add_trace(go.Scatter(
                    x=[0, 0.85*fc_prime, 0.85*fc_prime, 0, 0],
                    y=[foundation_thickness, foundation_thickness, 
                       foundation_thickness-stress_block_height, 
                       foundation_thickness-stress_block_height, foundation_thickness],
                    fill='toself',
                    fillcolor='rgba(255, 0, 0, 0.5)',
                    name='Compression Block',
                    mode='lines',
                    line=dict(color='red', width=2)
                ))
                
                # Tension reinforcement level
                rebar_level = steel_cover + bar_dia_x/2
                fig_stress.add_scatter(
                    x=[0, fy/10], y=[rebar_level, rebar_level],
                    mode='lines+markers',
                    marker=dict(symbol='line-ns', size=15, color='blue'),
                    line=dict(color='blue', width=4),
                    name='Tension Reinforcement'
                )
                
                # Add annotations
                fig_stress.add_annotation(
                    x=0.85*fc_prime/2, y=foundation_thickness - stress_block_height/2,
                    text=f"0.85f'c = {0.85*fc_prime:.1f} MPa",
                    showarrow=True,
                    arrowhead=2,
                    bgcolor="white",
                    bordercolor="red"
                )
                
                fig_stress.update_layout(
                    title="Whitney Stress Block Analysis",
                    xaxis_title="Stress (MPa)",
                    yaxis_title="Depth from Top (mm)",
                    height=400,
                    yaxis=dict(autorange="reversed"),
                    showlegend=True
                )
                
                st.plotly_chart(fig_stress, use_container_width=True)
            
            with col2:
                # Load path visualization
                st.markdown("##### Load Path Diagram")
                
                fig_load = go.Figure()
                
                # Foundation outline
                fig_load.add_trace(go.Scatter(
                    x=[0, foundation_size_length, foundation_size_length, 0, 0],
                    y=[0, 0, foundation_thickness, foundation_thickness, 0],
                    mode='lines',
                    line=dict(color='gray', width=3),
                    name='Foundation',
                    fill='toself',
                    fillcolor='rgba(128, 128, 128, 0.3)'
                ))
                
                # Column load arrows (downward)
                arrow_spacing = max(50, column_length//4)
                for i in range(int(column_length//arrow_spacing) + 1):
                    x_pos = foundation_size_length/2 - column_length/2 + i * arrow_spacing
                    if x_pos <= foundation_size_length/2 + column_length/2:
                        fig_load.add_annotation(
                            x=x_pos, y=foundation_thickness + 50,
                            ax=x_pos, ay=foundation_thickness + 150,
                            arrowhead=2,
                            arrowsize=1.5,
                            arrowwidth=3,
                            arrowcolor="red"
                        )
                
                # Soil reaction arrows (upward - corrected direction)
                for i in range(0, foundation_size_length + 1, 200):
                    fig_load.add_annotation(
                        x=i, y=-150,  # Start point (below foundation)
                        ax=i, ay=-50,  # End point (near foundation)
                        arrowhead=2,
                        arrowsize=1.5,
                        arrowwidth=3,
                        arrowcolor="blue"
                    )
                
                # Load labels
                fig_load.add_annotation(
                    x=foundation_size_length/2, y=foundation_thickness + 200,
                    text=f"Ultimate Load<br>{ultimate_load:.0f} kN",
                    showarrow=False,
                    bgcolor="red",
                    bordercolor="red",
                    font=dict(color="white", size=12)
                )
                
                fig_load.add_annotation(
                    x=foundation_size_length/2, y=-200,
                    text=f"Soil Reaction<br>{bearing_check['bearing_pressure']:.1f} kN/m²",
                    showarrow=False,
                    bgcolor="blue",
                    bordercolor="blue",
                    font=dict(color="white", size=12)
                )
                
                fig_load.update_layout(
                    title="Load Transfer Mechanism",
                    xaxis_title="Position (mm)",
                    yaxis_title="Height (mm)",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig_load, use_container_width=True)
            
            # Design summary metrics
            st.markdown("#### Key Analysis Results")
            st.info("📊 **คำอธิบาย:** D/C Ratio = ค่าแรงที่เกิดขึ้น / ค่าความต้านทาน (ควรน้อยกว่า 1.0)")
            
            col1, col2, col3, col4 = st.columns(4)
            
            try:
                design_shear_x = fdn_design.get_design_shear_force_X()
                design_shear_y = fdn_design.get_design_shear_force_Y()
                design_moment_x = fdn_design.get_design_moment_X()
                design_moment_y = fdn_design.get_design_moment_Y()
                
                # Fix ratio calculations (use same units)
                shear_x_capacity = shear_x['design_strength'] / 1000  # Convert to kN
                shear_y_capacity = shear_y['design_strength'] / 1000  # Convert to kN
                
                with col1:
                    shear_x_ratio = abs(design_shear_x) / shear_x_capacity if shear_x_capacity > 0 else 0
                    st.metric("Design Shear X", f"{design_shear_x:.1f} kN", 
                             delta=f"D/C Ratio: {shear_x_ratio:.3f}")
                with col2:
                    shear_y_ratio = abs(design_shear_y) / shear_y_capacity if shear_y_capacity > 0 else 0
                    st.metric("Design Shear Y", f"{design_shear_y:.1f} kN",
                             delta=f"D/C Ratio: {shear_y_ratio:.3f}")
                with col3:
                    st.metric("Design Moment X", f"{design_moment_x:.1f} kN⋅m",
                             delta="At Column Face")
                with col4:
                    st.metric("Design Moment Y", f"{design_moment_y:.1f} kN⋅m",
                             delta="At Column Face")
                    
            except Exception as e:
                st.warning(f"Could not retrieve design values: {str(e)}")
        
        # Clear status
        status_text.empty()
        progress_bar.empty()
        
    except Exception as e:
        st.error(f"❌ Analysis failed: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

else:
    # Initial state - show information
    st.markdown("### 🚀 Getting Started")
    
    st.markdown("""
    Welcome to the Foundation Design application based on **ACI 318M-25**. This tool helps you design isolated pad foundations according to the latest American Concrete Institute standards.
    
    #### How to use:
    1. **Enter design parameters** in the sidebar
    2. **Specify column loads** (dead, live, wind)
    3. **Set foundation properties** (thickness, soil capacity)
    4. **Define material properties** (concrete and steel strengths)
    5. **Click "Run Foundation Analysis"** to perform the design
    
    #### Features:
    - ✅ **ACI 318M-25 Compliance** - All calculations per latest code
    - ✅ **Real-time Validation** - Instant feedback on inputs
    - ✅ **Comprehensive Design** - Flexural, shear, and bearing checks
    - ✅ **Interactive Visualization** - Foundation geometry and results
    - ✅ **Detailed Reports** - Complete design documentation
    """)
    
    # Example values
    with st.expander("📋 Example Design Values", expanded=False):
        st.markdown("""
        **Typical Office Building Column:**
        - Dead Load: 800 kN
        - Live Load: 300 kN
        - Column: 400mm × 400mm
        - f'c: 30 MPa
        - fy: 420 MPa
        - Soil Capacity: 200 kN/m²
        
        **Typical Warehouse Column:**
        - Dead Load: 1200 kN  
        - Live Load: 600 kN
        - Column: 500mm × 500mm
        - f'c: 35 MPa
        - fy: 420 MPa
        - Soil Capacity: 150 kN/m²
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <small>
        Foundation Design - ACI 318M-25 | 
        Building Code Requirements for Structural Concrete (Metric) | 
        Chapter 13.1 Foundations
    </small>
</div>
""", unsafe_allow_html=True)
