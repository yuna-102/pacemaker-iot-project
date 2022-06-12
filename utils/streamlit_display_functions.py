import streamlit as st


def display_new_line(num_line: int) -> None:
    for i in range(num_line):
        st.text(" ")
