# streamlit run main.py

import streamlit as st

from view.dashboard_view import render_dashboard

def main():
    render_dashboard()


if __name__ == "__main__":
    main()

