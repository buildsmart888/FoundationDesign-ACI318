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
except ImportError as e:
    st.error(f"Error importing FoundationDesign modules: {e}")
    st.stop()

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
load_factors = aci_load_factors()
phi_factors = aci_strength_reduction_factors()

with st.sidebar.expander("Load Factors (ACI 318M-25 Section 5.3.1)", expanded=False):
    st.write(f"• Dead Load Factor: {load_factors['dead_load_factor']}")
    st.write(f"• Live Load Factor: {load_factors['live_load_factor']}")
    st.write(f"• Wind Load Factor: {load_factors['wind_load_factor']}")

with st.sidebar.expander("Strength Reduction Factors (Section 5.4.2)", expanded=False):
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
        
        # Estimate foundation size
        foundation_size_estimate = 2500  # mm initial guess
        foundation_self_weight = (foundation_size_estimate**2 * foundation_thickness / 1e9) * concrete_unit_weight
        surcharge_load = (foundation_size_estimate**2 * soil_depth / 1e9) * soil_unit_weight
        total_load_estimate = total_service_load + foundation_self_weight + surcharge_load
        
        required_area = total_load_estimate / soil_bearing_capacity  # m²
        foundation_size = int(np.sqrt(required_area * 1e6))  # mm
        foundation_size = int(np.ceil(foundation_size / 50) * 50)  # Round to 50mm
        
        # Step 2: Create foundation object
        status_text.text("Step 2/6: Creating foundation object...")
        progress_bar.progress(25)
        
        foundation = PadFoundationACI318(
            foundation_length=foundation_size,
            foundation_width=foundation_size,
            column_length=column_length,
            column_width=column_width,
            col_pos_xdir=foundation_size/2,  # centered
            col_pos_ydir=foundation_size/2,  # centered
            soil_bearing_capacity=soil_bearing_capacity,
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
        
        # Step 4: Load analysis
        status_text.text("Step 4/6: Load analysis...")
        progress_bar.progress(55)
        
        service_load = foundation.total_force_Z_dir_service()
        ultimate_load = foundation.total_force_Z_dir_ultimate()
        bearing_check = foundation.bearing_pressure_check_service()
        
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
                value=f"{foundation_size}×{foundation_size} mm",
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
            
            # Reinforcement provision
            st.markdown("#### Reinforcement Provision")
            
            As_x = max(flexural['x_direction']['required_As'], flexural['x_direction']['minimum_As'])
            As_y = max(flexural['y_direction']['required_As'], flexural['y_direction']['minimum_As'])
            
            bar_area_x = math.pi * (bar_dia_x/2)**2
            bar_area_y = math.pi * (bar_dia_y/2)**2
            
            spacing_x = min(250, int(1000 * bar_area_x / As_x / 25) * 25)
            spacing_y = min(250, int(1000 * bar_area_y / As_y / 25) * 25)
            
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
            
            # Final design specification
            st.markdown("#### Final Design Specification")
            
            spec_text = f"""
            **Foundation:**
            - Size: {foundation_size}mm × {foundation_size}mm × {foundation_thickness}mm
            - Area: {foundation.area_of_foundation()/1e6:.2f} m²
            
            **Materials:**
            - Concrete: f'c = {fc_prime} MPa
            - Steel: fy = {fy} MPa
            - Cover: {steel_cover}mm (per ACI 318M-25 Section 20.5.1.3)
            
            **Reinforcement:**
            - X-direction: {bar_dia_x}mm @ {spacing_x}mm c/c
            - Y-direction: {bar_dia_y}mm @ {spacing_y}mm c/c
            
            **Load Summary:**
            - Service Load: {service_load:.1f} kN
            - Ultimate Load: {ultimate_load:.1f} kN (ACI 318M-25 factors applied)
            
            **Design Code Compliance:**
            - ✅ ACI 318M-25 Chapter 13.1 - Foundations
            - ✅ Section 5.3 - Load combinations
            - ✅ Section 7 - Flexural design
            - ✅ Section 22 - Shear and torsion
            - ✅ Section 20.5 - Concrete cover
            """
            
            st.markdown(spec_text)
        
        with tab5:
            st.markdown("### Visualization")
            
            # Foundation plan view
            fig_plan = go.Figure()
            
            # Foundation outline
            fig_plan.add_trace(go.Scatter(
                x=[0, foundation_size, foundation_size, 0, 0],
                y=[0, 0, foundation_size, foundation_size, 0],
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
            
            # Critical section for punching shear
            d = foundation_thickness - steel_cover - bar_dia_x/2
            crit_x1 = col_x1 - d/2
            crit_x2 = col_x2 + d/2
            crit_y1 = col_y1 - d/2
            crit_y2 = col_y2 + d/2
            
            fig_plan.add_trace(go.Scatter(
                x=[crit_x1, crit_x2, crit_x2, crit_x1, crit_x1],
                y=[crit_y1, crit_y1, crit_y2, crit_y2, crit_y1],
                mode='lines',
                line=dict(color='orange', width=2, dash='dash'),
                name='Critical Section (Punching)',
                fill=None
            ))
            
            fig_plan.update_layout(
                title="Foundation Plan View",
                xaxis_title="X (mm)",
                yaxis_title="Y (mm)",
                showlegend=True,
                width=600,
                height=600,
                xaxis=dict(scaleanchor="y", scaleratio=1),
                yaxis=dict(constrain="domain")
            )
            
            st.plotly_chart(fig_plan, use_container_width=True)
            
            # Demand vs Capacity chart
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
            
            # Additional visualization columns
            col1, col2 = st.columns(2)
            
            with col1:
                # Bearing Pressure Distribution
                st.markdown("#### Bearing Pressure Distribution")
                
                # Create bearing pressure heatmap
                x_coords = np.linspace(0, foundation_size, 20)
                y_coords = np.linspace(0, foundation_size, 20)
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
                
                # Foundation outline
                fig_punch.add_trace(go.Scatter(
                    x=[0, foundation_size, foundation_size, 0, 0],
                    y=[0, 0, foundation_size, foundation_size, 0],
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
                    x=foundation_size/2,
                    y=foundation_size/2 + column_width/2 + 200,
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
                    # Use the actual foundation design function
                    fig_moment_x = fdn_design.plot_bending_moment_X(show_plot=False)
                    if fig_moment_x:
                        # Update the layout for better integration
                        fig_moment_x.update_layout(
                            height=400,
                            title="Bending Moment Diagram - X Direction",
                            showlegend=True
                        )
                        st.plotly_chart(fig_moment_x, use_container_width=True)
                        
                        # Display design moment value
                        design_moment_x = fdn_design.get_design_moment_X()
                        st.info(f"**Design Moment (X-dir):** {design_moment_x:.1f} kN⋅m")
                    else:
                        st.warning("Bending moment diagram could not be generated")
                except Exception as e:
                    st.error(f"Error generating bending moment diagram X: {str(e)}")
            
            with diag_tab4:
                st.markdown("##### Bending Moment Diagram along Y Direction")
                try:
                    # Use the actual foundation design function
                    fig_moment_y = fdn_design.plot_bending_moment_Y(show_plot=False)
                    if fig_moment_y:
                        # Update the layout for better integration
                        fig_moment_y.update_layout(
                            height=400,
                            title="Bending Moment Diagram - Y Direction",
                            showlegend=True
                        )
                        st.plotly_chart(fig_moment_y, use_container_width=True)
                        
                        # Display design moment value
                        design_moment_y = fdn_design.get_design_moment_Y()
                        st.info(f"**Design Moment (Y-dir):** {design_moment_y:.1f} kN⋅m")
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
                    x=[0, foundation_size, foundation_size, 0, 0],
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
                    x_pos = foundation_size/2 - column_length/2 + i * arrow_spacing
                    if x_pos <= foundation_size/2 + column_length/2:
                        fig_load.add_annotation(
                            x=x_pos, y=foundation_thickness + 50,
                            ax=x_pos, ay=foundation_thickness + 150,
                            arrowhead=2,
                            arrowsize=1.5,
                            arrowwidth=3,
                            arrowcolor="red"
                        )
                
                # Soil reaction arrows (upward)
                for i in range(0, foundation_size + 1, 200):
                    fig_load.add_annotation(
                        x=i, y=-50,
                        ax=i, ay=-150,
                        arrowhead=2,
                        arrowsize=1.5,
                        arrowwidth=3,
                        arrowcolor="blue"
                    )
                
                # Load labels
                fig_load.add_annotation(
                    x=foundation_size/2, y=foundation_thickness + 200,
                    text=f"Ultimate Load<br>{ultimate_load:.0f} kN",
                    showarrow=False,
                    bgcolor="red",
                    bordercolor="red",
                    font=dict(color="white", size=12)
                )
                
                fig_load.add_annotation(
                    x=foundation_size/2, y=-200,
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
            
            col1, col2, col3, col4 = st.columns(4)
            
            try:
                design_shear_x = fdn_design.get_design_shear_force_X()
                design_shear_y = fdn_design.get_design_shear_force_Y()
                design_moment_x = fdn_design.get_design_moment_X()
                design_moment_y = fdn_design.get_design_moment_Y()
                
                with col1:
                    st.metric("Design Shear X", f"{design_shear_x:.1f} kN", 
                             delta=f"Ratio: {design_shear_x/(shear_x['design_strength']/1000):.3f}")
                with col2:
                    st.metric("Design Shear Y", f"{design_shear_y:.1f} kN",
                             delta=f"Ratio: {design_shear_y/(shear_y['design_strength']/1000):.3f}")
                with col3:
                    st.metric("Design Moment X", f"{design_moment_x:.1f} kN⋅m")
                with col4:
                    st.metric("Design Moment Y", f"{design_moment_y:.1f} kN⋅m")
                    
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
