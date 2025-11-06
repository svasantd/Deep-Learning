"""
Test script to verify all imports work correctly
"""

print("Testing imports...")

try:
    print("✓ Importing data module...")
    from data import PORTFOLIO_DATA, get_portfolio_totals, get_urgent_alerts

    print("✓ Importing utils.formatting...")
    from utils.formatting import format_currency, format_percentage, get_trend_color

    print("✓ Importing views.components...")
    from views.components import render_breadcrumb, render_payer_card

    print("✓ Importing views.payer_view...")
    from views.payer_view import render_payer_view

    print("✓ Importing views.contract_view...")
    from views.contract_view import render_contract_view

    print("✓ Importing views.drug_view...")
    from views.drug_view import render_drug_view

    print("✓ Importing ai.chat...")
    from ai.chat import initialize_chat, get_portfolio_context

    print("\n✓ All imports successful!")

    # Test data
    print("\n=== Testing Data ===")
    totals = get_portfolio_totals()
    print(f"Portfolio Total SGP: {format_currency(totals['total_sgp'])}")
    print(f"Portfolio YoY Change: {format_percentage(totals['yoy_change'])}")
    print(f"Number of Payers: {len(PORTFOLIO_DATA['payers'])}")

    alerts = get_urgent_alerts()
    print(f"Number of Alerts: {len(alerts)}")

    print("\n✓ All tests passed! Ready to run the app.")
    print("\nRun the app with: streamlit run app.py")

except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
