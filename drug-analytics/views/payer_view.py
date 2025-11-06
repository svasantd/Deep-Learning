"""
Payer view - Grid of payer cards
"""
import streamlit as st
from views.components import render_payer_card, render_portfolio_header, render_breadcrumb
from data import PORTFOLIO_DATA, get_portfolio_totals


def render_payer_view():
    """
    Render the payer selection view with cards in a grid
    """
    # Breadcrumb
    render_breadcrumb(["Portfolio"])

    # Portfolio header with totals
    portfolio_totals = get_portfolio_totals()
    render_portfolio_header(portfolio_totals)

    # Section header
    st.markdown(
        '<div style="font-family: monospace; font-size: 18px; font-weight: bold; color: #ffffff; margin-bottom: 20px;">SELECT PAYER</div>',
        unsafe_allow_html=True
    )

    # Render payers in grid (3 columns)
    payers = PORTFOLIO_DATA["payers"]
    cols_per_row = 3

    for i in range(0, len(payers), cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < len(payers):
                with cols[j]:
                    render_payer_card(payers[idx], f"payer_card_{payers[idx]['id']}")
