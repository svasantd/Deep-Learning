# Quick Start Guide

## 🚀 Run the App

### Option 1: Using the startup script
```bash
cd drug-analytics
./run.sh
```

### Option 2: Using streamlit directly
```bash
cd drug-analytics
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

## 📊 Sample Data Included

The app comes with pre-loaded sample data:
- **4 Payers**: UnitedHealthcare, Anthem, Aetna, Cigna
- **9+ Drugs** across multiple therapeutic areas
- **Realistic metrics**: SGP, margins, YoY changes, bridge components

## 🎯 Navigation Guide

### 1. Portfolio View (Starting Page)
- See all payers in a card grid
- Each card shows: Payer name, Total SGP, YoY trend, Margin
- Click "View Contracts" to drill down

### 2. Contract View
- Lists all contracts for selected payer
- Shows: Contract name, Expiration days, SGP, Discount
- Contracts expiring <60 days marked in red 🔴
- Click "View Drugs" to see drugs in contract

### 3. Drug Table View
- Lists all drugs in selected contract
- Shows: Drug name, SGP, YoY change, Margin with trend indicator
- Click "Analyze" to see deep dive

### 4. Drug Deep Dive
- **Key Metrics**: 2025 SGP, YoY change, Margin, Margin change
- **Bridge Chart**: Visual waterfall showing Volume/Price/Cost impacts
- **AI Insights**: Automated analysis of drug performance
- **Action Items**: Prioritized recommendations (🔴 HIGH / ▲ MED / ▼ LOW)

## 🤖 AI Assistant (Optional)

To enable the AI chat assistant:

1. Get a free Gemini API key:
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Create API key

2. Create secrets file:
```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

3. Edit `.streamlit/secrets.toml` and add your key:
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

4. Restart the app

### AI Commands to Try:
- `top losers` - Worst performing drugs
- `expiring soon` - Contracts expiring <90 days
- `what should i do` - Action recommendations
- `why did margin drop` - Explain margin changes
- `show Anthem` - Navigate to specific payer

## 🎨 Visual Design

**Color Palette:**
- Background: `#1a1a1a` (dark grey)
- Positive/Up: `#00ff41` (green) with ▲
- Negative/Down: `#ff0844` (red) with ▼
- Neutral: `#ffffff` (white)

**Style:**
- Monospace fonts for all data
- Sharp rectangular borders (no curves)
- High contrast terminal aesthetic
- Minimal, data-focused design

## 🔔 Alerts System

The app automatically shows alerts at the top for:
- Contracts expiring in <60 days
- Significant margin drops (>5 percentage points)
- Strong performers (>15% YoY growth)

## 📁 Project Structure

```
drug-analytics/
├── app.py                    # Main entry point
├── data.py                   # Mock data (edit to customize)
├── requirements.txt          # Python dependencies
├── run.sh                    # Startup script
├── views/
│   ├── payer_view.py        # Payer cards grid
│   ├── contract_view.py     # Contract list
│   ├── drug_view.py         # Drug table + deep dive
│   └── components.py        # Shared UI components
├── ai/
│   └── chat.py              # Gemini AI integration
└── utils/
    └── formatting.py        # Helper functions
```

## 🔧 Customization

### Add More Data
Edit `data.py` and modify the `PORTFOLIO_DATA` dictionary structure.

### Change Colors
Edit `utils/formatting.py`:
```python
COLOR_GREEN = "#00ff41"  # Change to your preferred green
COLOR_RED = "#ff0844"    # Change to your preferred red
```

### Adjust Alerts
Edit `data.py` → `get_urgent_alerts()` function to modify alert thresholds.

## 🐛 Troubleshooting

**Module not found errors:**
```bash
pip install -r requirements.txt
```

**Port already in use:**
```bash
streamlit run app.py --server.port 8502
```

**AI chat not working:**
- Check that `GEMINI_API_KEY` is in `.streamlit/secrets.toml`
- Verify API key is valid at https://makersuite.google.com/
- Check internet connection

## 💡 Tips

1. **Breadcrumb Navigation**: Always visible at top showing your current path
2. **Back Buttons**: Navigate backwards at any level
3. **Persistent State**: Your selections persist until you manually change views
4. **Alerts Click**: Click alerts to jump to relevant items (future enhancement)
5. **Keyboard**: Tab through buttons, Enter to activate

## 📈 Metrics Explained

- **SGP**: Specialty Gross Profit - Total revenue from specialty drugs
- **YoY**: Year-over-Year growth percentage
- **Margin**: Profit margin as percentage of revenue
- **Volume Impact**: Revenue change from prescription volume changes
- **Price Impact**: Revenue change from pricing changes
- **Cost Impact**: Profit impact from cost changes

## 🎓 Learning Path

**Beginners:**
1. Start by exploring the payer cards
2. Click through one complete path: Payer → Contract → Drug → Analyze
3. Observe the color coding (green = good, red = bad)
4. Read the AI insights on a drug deep dive

**Advanced:**
1. Try the AI chat commands
2. Compare multiple drugs across different payers
3. Focus on expiring contracts
4. Analyze margin compression patterns

---

**Need Help?** Check README.md for detailed documentation.
