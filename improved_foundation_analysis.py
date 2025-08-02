"""
Improved Foundation Analysis with Structural Engineering Calculations
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def calculate_foundation_forces(foundation_size, column_length, ultimate_load):
    """
    Calculate shear forces and bending moments for a square foundation
    using simplified beam strip method
    """
    
    # Convert to consistent units (meters)
    L = foundation_size / 1000  # Foundation length in meters
    a = column_length / 1000    # Column length in meters
    c = L / 2                   # Center position
    
    # Calculate uniform soil pressure
    q = ultimate_load / L**2    # kN/m² (uniform pressure)
    
    # For strip analysis, consider 1-meter wide strip
    q_strip = q  # kN/m per meter width
    
    # Equivalent point load from column
    P = ultimate_load  # kN
    
    # Position array
    x = np.linspace(0, L, 200)
    
    # Initialize arrays
    shear = np.zeros_like(x)
    moment = np.zeros_like(x)
    
    for i, xi in enumerate(x):
        # Shear force calculation
        if xi <= c - a/2:  # Before column
            # Only soil pressure reaction
            V = q_strip * xi
        elif xi <= c + a/2:  # Under column
            # Soil pressure + portion of column load
            load_ratio = (xi - (c - a/2)) / a
            V = q_strip * xi - P * load_ratio
        else:  # After column
            # Soil pressure - full column load
            V = q_strip * xi - P
        
        shear[i] = V
        
        # Bending moment calculation
        if xi <= c - a/2:  # Before column
            M = q_strip * xi**2 / 2
        elif xi <= c + a/2:  # Under column
            load_ratio = (xi - (c - a/2)) / a
            M = (q_strip * xi**2 / 2 - 
                 P * load_ratio * (xi - (c - a/2 + load_ratio * a/2)))
        else:  # After column
            M = (q_strip * xi**2 / 2 - 
                 P * (xi - c))
        
        moment[i] = M
    
    # Convert position back to mm
    x_mm = x * 1000
    
    return x_mm, shear, moment

# Test with typical values
foundation_size = 2500  # mm
column_length = 400     # mm
ultimate_load = 1606.5  # kN

x_pos, shear_forces, moments = calculate_foundation_forces(
    foundation_size, column_length, ultimate_load
)

# Create improved diagrams
fig = make_subplots(
    rows=3, cols=1,
    subplot_titles=(
        'Soil Pressure Distribution', 
        'Shear Force Diagram', 
        'Bending Moment Diagram'
    ),
    vertical_spacing=0.08
)

# Soil pressure distribution
L_m = foundation_size / 1000
pressure = ultimate_load / L_m**2  # Uniform pressure
fig.add_trace(
    go.Scatter(
        x=[0, foundation_size, foundation_size, 0, 0], 
        y=[pressure, pressure, pressure, pressure, pressure],
        fill='tozeroy',
        fillcolor='rgba(0, 100, 200, 0.3)',
        line=dict(color='blue', width=2),
        name='Soil Pressure'
    ),
    row=1, col=1
)

# Add column position
col_start = foundation_size/2 - column_length/2
col_end = foundation_size/2 + column_length/2
fig.add_vrect(
    x0=col_start, x1=col_end,
    fillcolor="red", opacity=0.3,
    annotation_text="Column", annotation_position="top",
    row=1, col=1
)

# Shear force diagram
fig.add_trace(
    go.Scatter(x=x_pos, y=shear_forces, mode='lines', name='Shear Force',
              line=dict(color='green', width=3)),
    row=2, col=1
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)

# Bending moment diagram
fig.add_trace(
    go.Scatter(x=x_pos, y=moments, mode='lines', name='Bending Moment',
              line=dict(color='red', width=3)),
    row=3, col=1
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", row=3, col=1)

# Mark critical sections
d_eff = 400 - 75 - 16/2  # Effective depth
crit_positions = [col_start - d_eff, col_end + d_eff]

for pos in crit_positions:
    if 0 <= pos <= foundation_size:
        fig.add_vline(x=pos, line_dash="dot", line_color="orange", 
                     annotation_text="Critical", row=2, col=1)

# Mark column faces for moment
fig.add_vline(x=col_start, line_dash="dot", line_color="purple", 
             annotation_text="Column Face", row=3, col=1)
fig.add_vline(x=col_end, line_dash="dot", line_color="purple", 
             annotation_text="Column Face", row=3, col=1)

# Update layout
fig.update_layout(
    height=800,
    title_text="Foundation Structural Analysis - ACI 318M-25",
    showlegend=True
)

# Update axes
fig.update_xaxes(title_text="Position (mm)", row=1, col=1)
fig.update_xaxes(title_text="Position (mm)", row=2, col=1) 
fig.update_xaxes(title_text="Position (mm)", row=3, col=1)
fig.update_yaxes(title_text="Pressure (kN/m²)", row=1, col=1)
fig.update_yaxes(title_text="Shear (kN/m)", row=2, col=1)
fig.update_yaxes(title_text="Moment (kN⋅m/m)", row=3, col=1)

# Save
fig.write_html("improved_foundation_analysis.html")

print("✅ Improved foundation analysis diagrams created!")
print(f"📊 Maximum shear: {max(np.abs(shear_forces)):.1f} kN/m")
print(f"📊 Maximum moment: {max(np.abs(moments)):.1f} kN⋅m/m") 
print(f"📊 Soil pressure: {pressure:.1f} kN/m²")
print("📁 Saved as improved_foundation_analysis.html")
