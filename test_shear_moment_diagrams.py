"""
Test Shear Force and Bending Moment Diagrams
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Foundation parameters
foundation_size = 2500  # mm
column_length = 400     # mm
foundation_thickness = 400  # mm
steel_cover = 75        # mm
bar_dia_x = 16         # mm
ultimate_load = 1606.5  # kN

# Calculate positions for critical sections
L = foundation_size  # Foundation length
a = column_length    # Column length
c = L/2             # Center position

# X-direction analysis (strip method)
x_positions = np.linspace(0, L, 100)

# Calculate distributed load per unit width
total_load = ultimate_load  # kN
q = total_load / (L/1000)**2 * 1000  # kN/m per meter width

print(f"Foundation size: {L} mm")
print(f"Column length: {a} mm")
print(f"Total load: {total_load} kN")
print(f"Distributed load: {q:.2f} kN/m per meter width")

# Shear force and moment calculation
shear_x = []
moment_x = []

for x in x_positions:
    x_m = x / 1000  # Convert to meters
    L_m = L / 1000
    c_m = c / 1000
    a_m = a / 1000
    
    if x_m <= c_m - a_m/2:  # Before column
        V = q * x_m - (total_load / L_m) * x_m
        M = q * x_m**2 / 2 - (total_load / L_m) * x_m**2 / 2
    elif x_m <= c_m + a_m/2:  # Under column
        V = q * x_m - (total_load / L_m) * x_m + total_load * (x_m - (c_m - a_m/2)) / a_m
        M = q * x_m**2 / 2 - (total_load / L_m) * x_m**2 / 2 + total_load * (x_m - (c_m - a_m/2))**2 / (2 * a_m)
    else:  # After column
        V = q * x_m - (total_load / L_m) * x_m + total_load
        M = q * x_m**2 / 2 - (total_load / L_m) * x_m**2 / 2 + total_load * (x_m - c_m)
    
    shear_x.append(V)
    moment_x.append(M)

# Create subplot for shear and moment diagrams
fig_diagrams = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Shear Force Diagram (X-Direction)', 'Bending Moment Diagram (X-Direction)'),
    vertical_spacing=0.12
)

# Shear diagram
fig_diagrams.add_trace(
    go.Scatter(x=x_positions, y=shear_x, mode='lines', name='Shear Force',
              line=dict(color='blue', width=2)),
    row=1, col=1
)

# Add zero line for shear
fig_diagrams.add_hline(y=0, line_dash="dash", line_color="gray", row=1, col=1)

# Mark critical sections for shear
d_eff = foundation_thickness - steel_cover - bar_dia_x/2
crit_shear_pos = [c - a/2 - d_eff, c + a/2 + d_eff]

for pos in crit_shear_pos:
    if 0 <= pos <= L:
        fig_diagrams.add_vline(x=pos, line_dash="dot", line_color="red", 
                             annotation_text="Critical", row=1, col=1)

# Moment diagram
fig_diagrams.add_trace(
    go.Scatter(x=x_positions, y=moment_x, mode='lines', name='Bending Moment',
              line=dict(color='red', width=2)),
    row=2, col=1
)

# Add zero line for moment
fig_diagrams.add_hline(y=0, line_dash="dash", line_color="gray", row=2, col=1)

# Mark critical sections for moment (at column face)
crit_moment_pos = [c - a/2, c + a/2]

for pos in crit_moment_pos:
    if 0 <= pos <= L:
        fig_diagrams.add_vline(x=pos, line_dash="dot", line_color="orange", 
                             annotation_text="Face of Column", row=2, col=1)

# Update layout
fig_diagrams.update_layout(
    height=600,
    title_text="Foundation Analysis - Shear Force and Bending Moment",
    showlegend=True
)

# Update axes labels
fig_diagrams.update_xaxes(title_text="Position (mm)", row=1, col=1)
fig_diagrams.update_xaxes(title_text="Position (mm)", row=2, col=1)
fig_diagrams.update_yaxes(title_text="Shear Force (kN/m)", row=1, col=1)
fig_diagrams.update_yaxes(title_text="Bending Moment (kN⋅m/m)", row=2, col=1)

# Save as HTML
fig_diagrams.write_html("test_shear_moment_diagrams.html")

print("\n✅ Shear and Moment diagrams created successfully!")
print("📁 Saved as test_shear_moment_diagrams.html")
print("🌐 Open this file in a browser to verify the diagrams")

# Print some key values
print(f"\nKey analysis results:")
print(f"  Maximum shear: {max(np.abs(shear_x)):.2f} kN/m")
print(f"  Maximum moment: {max(np.abs(moment_x)):.2f} kN⋅m/m")
print(f"  Critical shear positions: {crit_shear_pos}")
print(f"  Critical moment positions: {crit_moment_pos}")
