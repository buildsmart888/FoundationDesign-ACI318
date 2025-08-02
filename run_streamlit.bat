@echo off
echo Installing Streamlit requirements...
pip install -r requirements_streamlit.txt

echo Starting Foundation Design Streamlit App...
streamlit run streamlit_app.py --server.port 8501

pause
