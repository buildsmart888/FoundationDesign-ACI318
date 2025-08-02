import streamlit as st
import plotly.graph_objects as go
import numpy as np

st.title("🏗️ Foundation Design - Test App")

st.write("Testing simple Streamlit app...")

# Simple plot
x = np.linspace(0, 10, 100)
y = np.sin(x)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Sin Wave'))
fig.update_layout(title="Test Plot")

st.plotly_chart(fig, use_container_width=True)

st.success("✅ Streamlit is working!")
