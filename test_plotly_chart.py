"""
Test Plotly chart with correct layout properties
"""

import plotly.graph_objects as go

# Test the foundation plan view with corrected layout
fig = go.Figure()

# Foundation outline
fig.add_trace(go.Scatter(
    x=[0, 2500, 2500, 0, 0],
    y=[0, 0, 2500, 2500, 0],
    mode='lines',
    line=dict(color='blue', width=3),
    name='Foundation',
    fill='toself',
    fillcolor='rgba(135, 206, 250, 0.3)'
))

# Column outline
fig.add_trace(go.Scatter(
    x=[1050, 1450, 1450, 1050, 1050],
    y=[1050, 1050, 1450, 1450, 1050],
    mode='lines',
    line=dict(color='red', width=2),
    name='Column',
    fill='toself',
    fillcolor='rgba(255, 99, 71, 0.5)'
))

# Update layout with correct properties
fig.update_layout(
    title="Foundation Plan View - Test",
    xaxis_title="X (mm)",
    yaxis_title="Y (mm)",
    showlegend=True,
    width=600,
    height=600,
    xaxis=dict(scaleanchor="y", scaleratio=1),
    yaxis=dict(constrain="domain")
)

# Save as HTML to test
fig.write_html("test_plotly_chart.html")
print("✅ Plotly chart created successfully!")
print("📁 Saved as test_plotly_chart.html")
print("🌐 Open this file in a browser to verify the chart works correctly")
