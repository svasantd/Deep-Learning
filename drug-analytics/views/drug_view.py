"""
Drug view - Table of drugs and deep dive with bridge chart
"""
import streamlit as st
import plotly.graph_objects as go
from views.components import render_breadcrumb, render_back_button, render_section_header
from utils.formatting import (
    format_currency, format_percentage, get_trend_color, get_trend_text,
    format_margin_change, calculate_sgp_2024,
    COLOR_WHITE, COLOR_RED, COLOR_GREEN, COLOR_BG
)


def render_drug_view(payer, contract):
    """
    Render the drug table view for a selected contract
    """
    # Breadcrumb
    breadcrumb = st.session_state.get("breadcrumb", ["Portfolio", payer["name"], contract["name"]])
    render_breadcrumb(breadcrumb)

    # Back button
    def go_back():
        st.session_state.current_view = "contract"
        st.session_state.selected_contract = None
        st.session_state.selected_drug = None
        st.session_state.breadcrumb = ["Portfolio", payer["name"]]

    render_back_button(go_back)

    # Contract summary
    trend_color = get_trend_color(contract["yoy_change"])
    trend_text = get_trend_text(contract["yoy_change"])

    summary_html = f"""
    <div style="
        border: 1px solid {COLOR_WHITE};
        padding: 20px;
        background-color: #1a1a1a;
        margin: 20px 0;
        font-family: monospace;
    ">
        <div style="font-size: 20px; color: {COLOR_WHITE}; font-weight: bold; margin-bottom: 10px;">
            {contract["name"]}
        </div>
        <div style="display: flex; gap: 30px; align-items: center; font-size: 16px;">
            <div style="color: {COLOR_WHITE};">
                SGP: {format_currency(contract["sgp"])}
            </div>
            <div style="color: {trend_color};">
                {trend_text} YoY
            </div>
            <div style="color: {COLOR_WHITE};">
                Discount: {format_percentage(contract["discount"], decimals=0, show_sign=False)}
            </div>
            <div style="color: {COLOR_WHITE};">
                Expires: {contract["expires_days"]}d
            </div>
        </div>
    </div>
    """
    st.markdown(summary_html, unsafe_allow_html=True)

    # Section header
    st.markdown(
        '<div style="font-family: monospace; font-size: 18px; font-weight: bold; color: #ffffff; margin: 30px 0 15px 0;">DRUGS</div>',
        unsafe_allow_html=True
    )

    # Render drugs as rows
    for drug in contract["drugs"]:
        render_drug_row(drug, payer, contract)

    # If a drug is selected, show deep dive
    if st.session_state.get("selected_drug"):
        render_drug_deep_dive(st.session_state.selected_drug, payer, contract)


def render_drug_row(drug, payer, contract):
    """
    Render a single drug row
    """
    trend_color = get_trend_color(drug["yoy_change"])
    trend_text = get_trend_text(drug["yoy_change"])
    margin_text = format_margin_change(drug["margin"], drug["margin_2024"])
    margin_color = get_trend_color(drug["margin"] - drug["margin_2024"])

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
                    {drug["name"]}
                </div>
                <div style="display: flex; gap: 20px; font-size: 14px;">
                    <span style="color: {COLOR_WHITE};">
                        {format_currency(drug["sgp"])}
                    </span>
                    <span style="color: {trend_color};">
                        {trend_text} YoY
                    </span>
                    <span style="color: {margin_color};">
                        Margin: {margin_text}
                    </span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(row_html, unsafe_allow_html=True)

    # Button to analyze
    if st.button("Analyze", key=f"drug_{drug['id']}"):
        st.session_state.selected_drug = drug
        st.rerun()


def render_drug_deep_dive(drug, payer, contract):
    """
    Render drug deep dive with bridge chart and AI insights
    """
    st.markdown("<br><br>", unsafe_allow_html=True)

    # Section header
    render_section_header(f"DEEP DIVE: {drug['name']}")

    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)

    trend_color = get_trend_color(drug["yoy_change"])
    trend_text = get_trend_text(drug["yoy_change"])
    margin_change_color = get_trend_color(drug["margin"] - drug["margin_2024"])

    with col1:
        metric_html = f"""
        <div style="border: 1px solid {COLOR_WHITE}; padding: 15px; background-color: #1a1a1a;">
            <div style="color: {COLOR_WHITE}; font-size: 12px; font-family: monospace; margin-bottom: 5px;">
                2025 SGP
            </div>
            <div style="color: {COLOR_WHITE}; font-size: 24px; font-family: monospace; font-weight: bold;">
                {format_currency(drug["sgp"])}
            </div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    with col2:
        metric_html = f"""
        <div style="border: 1px solid {COLOR_WHITE}; padding: 15px; background-color: #1a1a1a;">
            <div style="color: {COLOR_WHITE}; font-size: 12px; font-family: monospace; margin-bottom: 5px;">
                YoY CHANGE
            </div>
            <div style="color: {trend_color}; font-size: 24px; font-family: monospace; font-weight: bold;">
                {trend_text}
            </div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    with col3:
        metric_html = f"""
        <div style="border: 1px solid {COLOR_WHITE}; padding: 15px; background-color: #1a1a1a;">
            <div style="color: {COLOR_WHITE}; font-size: 12px; font-family: monospace; margin-bottom: 5px;">
                2025 MARGIN
            </div>
            <div style="color: {COLOR_WHITE}; font-size: 24px; font-family: monospace; font-weight: bold;">
                {format_percentage(drug["margin"], decimals=0, show_sign=False)}
            </div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    with col4:
        metric_html = f"""
        <div style="border: 1px solid {COLOR_WHITE}; padding: 15px; background-color: #1a1a1a;">
            <div style="color: {COLOR_WHITE}; font-size: 12px; font-family: monospace; margin-bottom: 5px;">
                MARGIN CHANGE
            </div>
            <div style="color: {margin_change_color}; font-size: 24px; font-family: monospace; font-weight: bold;">
                {format_percentage(drug["margin"] - drug["margin_2024"], decimals=0)}
            </div>
        </div>
        """
        st.markdown(metric_html, unsafe_allow_html=True)

    # Bridge chart
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_header("SGP BRIDGE ANALYSIS")

    fig = create_bridge_chart(drug)
    st.plotly_chart(fig, use_container_width=True)

    # AI Insights section
    render_section_header("AI INSIGHTS")

    insights = generate_drug_insights(drug, payer, contract)
    for insight in insights:
        st.markdown(
            f'<div style="font-family: monospace; color: {COLOR_WHITE}; margin-bottom: 8px;">• {insight}</div>',
            unsafe_allow_html=True
        )

    # Action items
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_header("RECOMMENDED ACTIONS")

    actions = generate_action_items(drug, payer, contract)
    for action in actions:
        priority_marker = action["marker"]
        action_color = COLOR_RED if priority_marker == "🔴" else COLOR_WHITE

        st.markdown(
            f'<div style="font-family: monospace; color: {action_color}; margin-bottom: 8px;">{priority_marker} {action["text"]}</div>',
            unsafe_allow_html=True
        )

    # Close button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Drugs", key="close_deep_dive"):
        st.session_state.selected_drug = None
        st.rerun()


def create_bridge_chart(drug):
    """
    Create a waterfall/bridge chart showing SGP components
    """
    # Calculate 2024 SGP
    sgp_2024 = calculate_sgp_2024(drug["sgp"], drug["yoy_change"])
    sgp_2025 = drug["sgp"]

    # Data for waterfall
    labels = ["2024 SGP", "Volume Impact", "Price Impact", "Cost Impact", "2025 SGP"]
    values = [
        sgp_2024,
        drug["volume_impact"],
        drug["price_impact"],
        drug["cost_impact"],
        sgp_2025
    ]

    # Measures: absolute for start/end, relative for impacts
    measures = ["absolute", "relative", "relative", "relative", "total"]

    # Colors: white for totals, green/red for impacts
    colors = []
    for i, measure in enumerate(measures):
        if measure == "absolute" or measure == "total":
            colors.append(COLOR_WHITE)
        else:
            if values[i] > 0:
                colors.append(COLOR_GREEN)
            else:
                colors.append(COLOR_RED)

    # Create waterfall chart
    fig = go.Figure(go.Waterfall(
        x=labels,
        y=values,
        measure=measures,
        text=[format_currency(v, decimals=1) for v in values],
        textposition="outside",
        connector={"line": {"color": COLOR_WHITE, "width": 1}},
        decreasing={"marker": {"color": COLOR_RED}},
        increasing={"marker": {"color": COLOR_GREEN}},
        totals={"marker": {"color": COLOR_WHITE}}
    ))

    # Update layout for terminal aesthetic
    fig.update_layout(
        title={
            "text": f"{drug['name']} - SGP Bridge (2024 → 2025)",
            "font": {"family": "monospace", "size": 18, "color": COLOR_WHITE},
            "x": 0
        },
        plot_bgcolor=COLOR_BG,
        paper_bgcolor=COLOR_BG,
        font={"family": "monospace", "size": 12, "color": COLOR_WHITE},
        xaxis={
            "showgrid": False,
            "showline": True,
            "linecolor": COLOR_WHITE,
            "linewidth": 1,
            "color": COLOR_WHITE
        },
        yaxis={
            "showgrid": True,
            "gridcolor": "#333333",
            "showline": True,
            "linecolor": COLOR_WHITE,
            "linewidth": 1,
            "color": COLOR_WHITE
        },
        showlegend=False,
        height=500
    )

    return fig


def generate_drug_insights(drug, payer, contract):
    """
    Generate AI-style insights for a drug
    """
    insights = []

    # YoY analysis
    if drug["yoy_change"] > 0:
        insights.append(f"▲ SGP growing at {format_percentage(drug['yoy_change'], decimals=0, show_sign=False)} YoY driven by volume ({format_currency(drug['volume_impact'])}) and price ({format_currency(drug['price_impact'])})")
    else:
        insights.append(f"▼ SGP declining at {format_percentage(abs(drug['yoy_change']), decimals=0, show_sign=False)} YoY - investigate volume and price pressures")

    # Margin analysis
    margin_change = drug["margin"] - drug["margin_2024"]
    if margin_change > 0:
        insights.append(f"▲ Margin improved by {format_percentage(margin_change, decimals=0)} - cost efficiencies in effect")
    elif margin_change < 0:
        insights.append(f"▼ Margin compressed by {format_percentage(abs(margin_change), decimals=0)} - cost pressures mounting")
    else:
        insights.append(f"→ Margin stable at {format_percentage(drug['margin'], decimals=0, show_sign=False)}")

    # Contract context
    if contract["expires_days"] < 60:
        insights.append(f"🔴 Contract expires in {contract['expires_days']} days - renewal urgency HIGH")

    # Cost impact
    if drug["cost_impact"] < 0:
        insights.append(f"Cost reduction of {format_currency(abs(drug['cost_impact']))} contributing positively to profitability")

    return insights


def generate_action_items(drug, payer, contract):
    """
    Generate prioritized action items
    """
    actions = []

    # Contract renewal
    if contract["expires_days"] < 60:
        actions.append({
            "marker": "🔴",
            "text": f"HIGH: Initiate contract renewal discussions with {payer['name']} immediately"
        })

    # Margin issues
    margin_change = drug["margin"] - drug["margin_2024"]
    if margin_change < -0.05:
        actions.append({
            "marker": "🔴",
            "text": f"HIGH: Investigate {format_percentage(abs(margin_change), decimals=0)} margin drop - review cost structure"
        })

    # Volume decline
    if drug["volume_impact"] < 0:
        actions.append({
            "marker": "▲",
            "text": f"MED: Volume declining ({format_currency(drug['volume_impact'])}) - assess market share and competition"
        })

    # Price optimization
    if drug["price_impact"] < 0:
        actions.append({
            "marker": "▲",
            "text": f"MED: Price pressure detected ({format_currency(drug['price_impact'])}) - evaluate pricing strategy"
        })

    # Positive momentum
    if drug["yoy_change"] > 0.10:
        actions.append({
            "marker": "▼",
            "text": f"LOW: Capitalize on momentum - explore expansion opportunities with {payer['name']}"
        })

    return actions
