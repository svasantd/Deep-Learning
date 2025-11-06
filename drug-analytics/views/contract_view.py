"""
Contract view - List of contracts for selected payer
"""
import streamlit as st
from views.components import render_breadcrumb, render_back_button
from utils.formatting import (
    format_currency, format_percentage, get_trend_color, get_trend_text,
    get_expiration_indicator, COLOR_WHITE, COLOR_RED, COLOR_GREEN
)


def render_contract_view(payer):
    """
    Render the contract list view for a selected payer
    """
    # Breadcrumb
    breadcrumb = st.session_state.get("breadcrumb", ["Portfolio", payer["name"]])
    render_breadcrumb(breadcrumb)

    # Back button
    def go_back():
        st.session_state.current_view = "payer"
        st.session_state.selected_payer = None
        st.session_state.breadcrumb = ["Portfolio"]

    render_back_button(go_back)

    # Payer summary
    trend_color = get_trend_color(payer["yoy_change"])
    trend_text = get_trend_text(payer["yoy_change"])

    summary_html = f"""
    <div style="
        border: 1px solid {COLOR_WHITE};
        padding: 20px;
        background-color: #1a1a1a;
        margin: 20px 0;
        font-family: monospace;
    ">
        <div style="font-size: 24px; color: {COLOR_WHITE}; font-weight: bold; margin-bottom: 10px;">
            {payer["name"]}
        </div>
        <div style="display: flex; gap: 30px; align-items: center;">
            <div style="font-size: 20px; color: {COLOR_WHITE};">
                SGP: {format_currency(payer["sgp"])}
            </div>
            <div style="font-size: 18px; color: {trend_color};">
                {trend_text} YoY
            </div>
            <div style="font-size: 18px; color: {COLOR_WHITE};">
                Margin: {format_percentage(payer["margin"], decimals=0, show_sign=False)}
            </div>
        </div>
    </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)

    # Section header
    st.markdown(
        '<div style="font-family: monospace; font-size: 18px; font-weight: bold; color: #ffffff; margin: 30px 0 15px 0;">CONTRACTS</div>',
        unsafe_allow_html=True
    )

    # Render contracts as rows
    for contract in payer["contracts"]:
        render_contract_row(contract, payer)


def render_contract_row(contract, payer):
    """
    Render a single contract row
    """
    trend_color = get_trend_color(contract["yoy_change"])
    trend_text = get_trend_text(contract["yoy_change"])
    exp_indicator = get_expiration_indicator(contract["expires_days"])
    exp_color = COLOR_RED if contract["expires_days"] < 60 else COLOR_WHITE

    row_html = f"""
    <div style="
        border: 1px solid {COLOR_WHITE};
        padding: 15px;
        background-color: #1a1a1a;
        margin-bottom: 10px;
        font-family: monospace;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="flex: 1;">
                <div style="font-size: 18px; color: {COLOR_WHITE}; font-weight: bold; margin-bottom: 5px;">
                    {contract["name"]}
                </div>
                <div style="display: flex; gap: 20px; font-size: 14px;">
                    <span style="color: {exp_color};">
                        Exp: {contract["expires_days"]}d {exp_indicator}
                    </span>
                    <span style="color: {COLOR_WHITE};">
                        {format_currency(contract["sgp"])}
                    </span>
                    <span style="color: {trend_color};">
                        {trend_text}
                    </span>
                    <span style="color: {COLOR_WHITE};">
                        Discount: {format_percentage(contract["discount"], decimals=0, show_sign=False)}
                    </span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(row_html, unsafe_allow_html=True)

    # Button to view drugs
    if st.button("View Drugs", key=f"contract_{contract['id']}"):
        st.session_state.current_view = "drug"
        st.session_state.selected_contract = contract
        st.session_state.breadcrumb = ["Portfolio", payer["name"], contract["name"]]
        st.rerun()
