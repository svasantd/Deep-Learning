"""
AI Chat integration with Google Gemini
"""
import streamlit as st
from data import PORTFOLIO_DATA, get_all_drugs, get_payer_by_id
from utils.formatting import format_currency, format_percentage, get_trend_text


def initialize_chat():
    """
    Initialize chat in session state
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "gemini_configured" not in st.session_state:
        st.session_state.gemini_configured = False


def configure_gemini():
    """
    Configure Gemini API
    """
    try:
        import google.generativeai as genai

        # Check if API key is in secrets
        if "GEMINI_API_KEY" in st.secrets:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            st.session_state.gemini_configured = True
            st.session_state.genai = genai
            return True
        else:
            return False
    except Exception as e:
        st.session_state.gemini_error = str(e)
        return False


def get_portfolio_context():
    """
    Generate portfolio context for AI
    """
    context = "PORTFOLIO DATA CONTEXT:\n\n"

    for payer in PORTFOLIO_DATA["payers"]:
        context += f"Payer: {payer['name']} | SGP: {format_currency(payer['sgp'])} | YoY: {get_trend_text(payer['yoy_change'])} | Margin: {format_percentage(payer['margin'], decimals=0, show_sign=False)}\n"

        for contract in payer["contracts"]:
            context += f"  ├─ Contract: {contract['name']} | Expires: {contract['expires_days']}d | SGP: {format_currency(contract['sgp'])} | YoY: {get_trend_text(contract['yoy_change'])}\n"

            for drug in contract["drugs"]:
                context += f"     ├─ {drug['name']} | SGP: {format_currency(drug['sgp'])} | YoY: {get_trend_text(drug['yoy_change'])} | Margin: {format_percentage(drug['margin'], decimals=0, show_sign=False)}\n"

        context += "\n"

    return context


def get_system_prompt():
    """
    Generate system prompt for AI
    """
    portfolio_context = get_portfolio_context()

    prompt = f"""You are a specialty drug portfolio analytics AI assistant. You help pharmaceutical executives analyze their drug portfolio performance.

{portfolio_context}

RESPONSE STYLE:
- Be concise and terminal-like
- Use ▲/▼/→ symbols for trends
- Use bullet points with priority markers (🔴 HIGH / ▲ MED / ▼ LOW)
- No flowery language - direct and data-driven
- Always reference specific numbers from the data

AVAILABLE COMMANDS YOU CAN HELP WITH:
- "show [payer name]" - Navigate to a specific payer
- "why did [metric] change" - Explain metric changes using bridge logic
- "what should i do" - Provide action recommendations
- "top losers" - Show worst performing drugs
- "top performers" - Show best performing drugs
- "expiring soon" - Show contracts expiring <90 days
- "compare [drug a] vs [drug b]" - Compare two drugs
- "margin analysis" - Analyze margin performance across portfolio

When answering:
1. Reference specific data points
2. Identify root causes using bridge components (volume, price, cost)
3. Prioritize urgent actions (expiring contracts, margin compression)
4. Be specific about dollar impacts
"""
    return prompt


def process_chat_message(user_message):
    """
    Process user message and generate AI response
    """
    if not st.session_state.gemini_configured:
        return "⚠️ Gemini API not configured. Add GEMINI_API_KEY to .streamlit/secrets.toml"

    try:
        # Get current view context
        current_view = st.session_state.get("current_view", "payer")
        context_info = f"\n\nCURRENT VIEW: {current_view}"

        if current_view == "contract" and st.session_state.get("selected_payer"):
            payer = st.session_state.selected_payer
            context_info += f"\nSelected Payer: {payer['name']}"

        if current_view == "drug" and st.session_state.get("selected_contract"):
            contract = st.session_state.selected_contract
            context_info += f"\nSelected Contract: {contract['name']}"

        # Build full prompt
        system_prompt = get_system_prompt()
        full_prompt = f"{system_prompt}\n\n{context_info}\n\nUser question: {user_message}"

        # Call Gemini API
        genai = st.session_state.genai
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(full_prompt)

        return response.text

    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def render_chat_sidebar():
    """
    Render chat interface in sidebar
    """
    st.sidebar.markdown(
        '<div style="font-family: monospace; font-size: 18px; font-weight: bold; color: #00ff41; margin-bottom: 20px;">AI ASSISTANT</div>',
        unsafe_allow_html=True
    )

    # Initialize chat
    initialize_chat()

    # Check if Gemini is configured
    if not st.session_state.gemini_configured:
        configured = configure_gemini()
        if not configured:
            st.sidebar.warning("⚠️ Gemini API not configured\n\nAdd GEMINI_API_KEY to .streamlit/secrets.toml to enable AI chat")
            st.sidebar.markdown(
                """
                <div style="font-family: monospace; font-size: 12px; color: #ffffff; background: #1a1a1a; padding: 10px; border: 1px solid #00ff41;">
                Example queries:<br>
                • "top losers"<br>
                • "expiring soon"<br>
                • "what should i do"<br>
                • "why did margin drop"
                </div>
                """,
                unsafe_allow_html=True
            )
            return

    # Chat input
    user_message = st.sidebar.text_input("Ask AI:", key="chat_input", placeholder="e.g., 'top losers'")

    if user_message:
        # Add to history
        st.session_state.chat_history.append({
            "role": "user",
            "message": user_message
        })

        # Get AI response
        ai_response = process_chat_message(user_message)
        st.session_state.chat_history.append({
            "role": "assistant",
            "message": ai_response
        })

        # Clear input
        st.rerun()

    # Display chat history
    if st.session_state.chat_history:
        st.sidebar.markdown("---")
        st.sidebar.markdown(
            '<div style="font-family: monospace; font-size: 14px; font-weight: bold; color: #ffffff; margin-bottom: 10px;">CHAT HISTORY</div>',
            unsafe_allow_html=True
        )

        # Show last 10 messages
        for i, msg in enumerate(reversed(st.session_state.chat_history[-10:])):
            if msg["role"] == "user":
                st.sidebar.markdown(
                    f'<div style="font-family: monospace; font-size: 12px; color: #00ff41; margin-bottom: 10px;">▶ {msg["message"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.sidebar.markdown(
                    f'<div style="font-family: monospace; font-size: 12px; color: #ffffff; margin-bottom: 15px; background: #1a1a1a; padding: 10px; border-left: 2px solid #00ff41;">{msg["message"]}</div>',
                    unsafe_allow_html=True
                )

        # Clear history button
        if st.sidebar.button("Clear History", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()


def handle_command(command):
    """
    Handle specific AI commands that trigger navigation
    """
    command_lower = command.lower()

    # Show payer command
    if command_lower.startswith("show "):
        payer_name = command[5:].strip().lower()
        for payer in PORTFOLIO_DATA["payers"]:
            if payer_name in payer["name"].lower():
                st.session_state.current_view = "contract"
                st.session_state.selected_payer = payer
                st.session_state.breadcrumb = ["Portfolio", payer["name"]]
                return True

    return False
