import streamlit as st

st.title("Efficient Page Replacement Algorithm Simulator")

reference_string = st.text_input("Enter Reference String (comma-separated)", "")
frames = st.number_input("Enter Number of Frames", min_value=1, value=3, step=1)
algorithm = st.selectbox("Choose Algorithm", ["FIFO", "LRU", "Optimal"])

st.button("Run Simulation")