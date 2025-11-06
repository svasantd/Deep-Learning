"""
Shared UI components for the analytics workbench
"""
import streamlit as st
from utils.formatting import (
    format_currency, format_percentage, get_trend_color, get_trend_text,
    get_priority_marker, COLOR_GREEN, COLOR_RED, COLOR_WHITE
)


def render_breadcrumb(path):
    """
    Render breadcrumb navigation
    path: list of navigation steps, e.g., ["Portfolio", "UHC", "Oncology"]
    """
    breadcrumb_html = " > ".join([f'<span style="color: {COLOR_WHITE};">{item}</span>' for item in path])
    st.markdown(
        f'<div style="font-family: monospace; font-size: 14px; margin-bottom: 20px;">{breadcrumb_html}</div>',
        unsafe_allow_html=True
    )


def render_metric_card(label, value, trend=None, show_trend_color=True):
    """
    Render a single metric card
    """
    value_color = COLOR_WHITE
    if trend is not None and show_trend_color:
        value_color = get_trend_color(trend)

    metric_html = f"""
    <div style="
        border: 1px solid {COLOR_WHITE};
        padding: 15px;
        background-color: #1a1a1a;
        margin-bottom: 10px;
    ">
        <div style="color: {COLOR_WHITE}; font-size: 12px; font-family: monospace; margin-bottom: 5px;">
            {label}
        </div>
        <div style="color: {value_color}; font-size: 24px; font-family: monospace; font-weight: bold;">
            {value}
        </div>
    </div>
    """
    st.markdown(metric_html, unsafe_allow_html=True)


def render_payer_card(payer, on_click_key):
    """
    Render a payer card
    """
    trend_color = get_trend_color(payer["yoy_change"])
    trend_text = get_trend_text(payer["yoy_change"])

    card_html = f"""
    <div style="
        border: 1px solid {COLOR_WHITE};
        padding: 15px;
        background-color: #1a1a1a;
        margin-bottom: 15px;
        font-family: monospace;
    ">
        <div style="font-size: 18px; font-weight: bold; color: {COLOR_WHITE}; margin-bottom: 10px;">
            {payer["name"]}
        </div>
        <div style="font-size: 24px; color: {COLOR_WHITE}; margin-bottom: 8px;">
            {format_currency(payer["sgp"])}
        </div>
        <div style="font-size: 16px; color: {trend_color}; margin-bottom: 8px;">
            {trend_text} YoY
        </div>
        <div style="font-size: 14px; color: {COLOR_WHITE}; margin-bottom: 15px;">
            Margin: {format_percentage(payer["margin"], decimals=0, show_sign=False)}
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    # Button below the card
    if st.button("View Contracts", key=on_click_key, use_container_width=True):
        st.session_state.current_view = "contract"
        st.session_state.selected_payer = payer
        st.session_state.breadcrumb = ["Portfolio", payer["name"]]
        st.rerun()


def render_alert(alert):
    """
    Render an alert message
    """
    marker = get_priority_marker(alert["level"])
    color = COLOR_RED if alert["level"] == "critical" else COLOR_GREEN

    alert_html = f"""
    <div style="
        border: 1px solid {color};
        padding: 10px 15px;
        background-color: #1a1a1a;
        margin-bottom: 10px;
        font-family: monospace;
        color: {color};
    ">
        {marker} {alert["message"]}
    </div>
    """
    st.markdown(alert_html, unsafe_allow_html=True)


def render_alerts_section(alerts):
    """
    Render alerts section at top of page
    """
    if not alerts:
        return

    st.markdown(
        '<div style="font-family: monospace; font-size: 16px; font-weight: bold; color: #ffffff; margin-bottom: 10px;">ALERTS</div>',
        unsafe_allow_html=True
    )

    for alert in alerts:
        render_alert(alert)

    st.markdown("<br>", unsafe_allow_html=True)


def render_back_button(on_click_callback, label="← Back"):
    """
    Render a back button
    """
    if st.button(label, key=f"back_{label}"):
        on_click_callback()
        st.rerun()


def render_section_header(text):
    """
    Render a section header
    """
    st.markdown(
        f'<div style="font-family: monospace; font-size: 18px; font-weight: bold; color: {COLOR_WHITE}; margin: 20px 0 10px 0; border-bottom: 1px solid {COLOR_WHITE}; padding-bottom: 5px;">{text}</div>',
        unsafe_allow_html=True
    )


def render_data_table(headers, rows, column_colors=None):
    """
    Render a data table with terminal styling
    headers: list of column headers
    rows: list of lists (row data)
    column_colors: optional list of colors for each column
    """
    if column_colors is None:
        column_colors = [COLOR_WHITE] * len(headers)

    # Header row
    header_html = "<tr>"
    for header in headers:
        header_html += f'<th style="text-align: left; padding: 10px; border-bottom: 1px solid {COLOR_WHITE}; color: {COLOR_WHITE};">{header}</th>'
    header_html += "</tr>"

    # Data rows
    rows_html = ""
    for row in rows:
        rows_html += "<tr>"
        for i, cell in enumerate(row):
            color = column_colors[i] if i < len(column_colors) else COLOR_WHITE
            rows_html += f'<td style="padding: 10px; color: {color};">{cell}</td>'
        rows_html += "</tr>"

    table_html = f"""
    <table style="
        width: 100%;
        border-collapse: collapse;
        font-family: monospace;
        background-color: #1a1a1a;
        margin-bottom: 20px;
    ">
        {header_html}
        {rows_html}
    </table>
    """
    st.markdown(table_html, unsafe_allow_html=True)


def render_portfolio_header(portfolio_totals):
    """
    Render portfolio-level summary header
    """
    trend_color = get_trend_color(portfolio_totals["yoy_change"])
    trend_text = get_trend_text(portfolio_totals["yoy_change"])

    header_html = f"""
    <div style="
        border: 2px solid {COLOR_WHITE};
        padding: 20px;
        background-color: #1a1a1a;
        margin-bottom: 30px;
        font-family: monospace;
    ">
        <div style="font-size: 14px; color: {COLOR_WHITE}; margin-bottom: 5px;">
            PORTFOLIO TOTAL
        </div>
        <div style="display: flex; align-items: center; gap: 30px;">
            <div style="font-size: 32px; color: {COLOR_WHITE}; font-weight: bold;">
                {format_currency(portfolio_totals["total_sgp"])} SGP
            </div>
            <div style="font-size: 24px; color: {trend_color};">
                {trend_text} YoY
            </div>
            <div style="font-size: 20px; color: {COLOR_WHITE};">
                Margin: {format_percentage(portfolio_totals["margin"], decimals=0, show_sign=False)}
            </div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
