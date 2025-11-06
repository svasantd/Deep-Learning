"""
Specialty Drug Portfolio Analytics Workbench
Main application entry point
"""
import streamlit as st
from views.payer_view import render_payer_view
from views.contract_view import render_contract_view
from views.drug_view import render_drug_view
from views.components import render_alerts_section
from ai.chat import render_chat_sidebar
from data import get_urgent_alerts


# Page configuration
st.set_page_config(
    page_title="Drug Portfolio Analytics",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for terminal aesthetic
def apply_custom_css():
    """
    Apply custom CSS for dark terminal theme
    """
    st.markdown("""
    <style>
    /* Global styles */
    .main {
        background-color: #1a1a1a;
    }

    .stApp {
        background-color: #1a1a1a;
    }

    /* Text styles */
    body, p, h1, h2, h3, h4, h5, h6, span, div {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1a1a1a;
        border-right: 1px solid #00ff41;
    }

    /* Buttons */
    .stButton button {
        background-color: #1a1a1a;
        color: #00ff41;
        border: 1px solid #00ff41;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
        padding: 8px 16px;
        transition: all 0.2s;
    }

    .stButton button:hover {
        background-color: #00ff41;
        color: #1a1a1a;
        border: 1px solid #00ff41;
    }

    /* Text input */
    .stTextInput input {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid #00ff41;
        border-radius: 0px;
        font-family: 'Courier New', monospace;
    }

    /* Remove streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Column spacing */
    [data-testid="column"] {
        padding: 0 10px;
    }

    /* Markdown styling */
    .markdown-text-container {
        font-family: 'Courier New', monospace !important;
    }

    /* Headers */
    h1, h2, h3 {
        color: #00ff41 !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_session_state():
    """
    Initialize session state variables
    """
    if "current_view" not in st.session_state:
        st.session_state.current_view = "payer"

    if "selected_payer" not in st.session_state:
        st.session_state.selected_payer = None

    if "selected_contract" not in st.session_state:
        st.session_state.selected_contract = None

    if "selected_drug" not in st.session_state:
        st.session_state.selected_drug = None

    if "breadcrumb" not in st.session_state:
        st.session_state.breadcrumb = ["Portfolio"]


def render_header():
    """
    Render main app header
    """
    st.markdown("""
    <div style="
        border: 2px solid #00ff41;
        padding: 20px;
        margin-bottom: 30px;
        background-color: #1a1a1a;
    ">
        <h1 style="
            margin: 0;
            color: #00ff41;
            font-family: 'Courier New', monospace;
            font-size: 28px;
            text-align: center;
        ">
            💊 SPECIALTY DRUG PORTFOLIO ANALYTICS
        </h1>
        <div style="
            text-align: center;
            color: #ffffff;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            margin-top: 10px;
        ">
            PAYER → CONTRACT → DRUG → INSIGHTS
        </div>
    </div>
    """, unsafe_allow_html=True)


def main():
    """
    Main application function
    """
    # Apply custom styling
    apply_custom_css()

    # Initialize session state
    initialize_session_state()

    # Render header
    render_header()

    # Render alerts at top
    alerts = get_urgent_alerts()
    render_alerts_section(alerts)

    # Route to appropriate view
    current_view = st.session_state.current_view

    if current_view == "payer":
        render_payer_view()

    elif current_view == "contract":
        if st.session_state.selected_payer:
            render_contract_view(st.session_state.selected_payer)
        else:
            st.error("No payer selected")
            st.session_state.current_view = "payer"
            st.rerun()

    elif current_view == "drug":
        if st.session_state.selected_payer and st.session_state.selected_contract:
            render_drug_view(
                st.session_state.selected_payer,
                st.session_state.selected_contract
            )
        else:
            st.error("No contract selected")
            st.session_state.current_view = "payer"
            st.rerun()

    # Render AI chat sidebar
    render_chat_sidebar()


if __name__ == "__main__":
    main()
