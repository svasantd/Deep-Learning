# Specialty Drug Portfolio Analytics Workbench

A minimalist terminal-style analytics dashboard for specialty drug portfolio management, built with Streamlit and Google Gemini AI.

## Features

- **Terminal Aesthetic**: Dark theme with green (#00ff41) and red (#ff0844) indicators
- **Hierarchical Navigation**: PAYER → CONTRACT → DRUG → DEEP DIVE
- **Bridge/Waterfall Charts**: Visual breakdown of SGP changes (Volume, Price, Cost impacts)
- **AI Assistant**: Gemini-powered chat for portfolio insights and recommendations
- **Alerts System**: Proactive notifications for expiring contracts and margin issues
- **Action Items**: Prioritized recommendations (🔴 HIGH / ▲ MED / ▼ LOW)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Gemini API (optional):
Create `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your-api-key-here"
```

Get a free API key at: https://makersuite.google.com/app/apikey

## Running the App

```bash
cd drug-analytics
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### Navigation Flow

1. **Portfolio View**: See all payers with SGP, YoY change, and margin
2. **Contract View**: Click a payer to see their contracts with expiration dates
3. **Drug View**: Click a contract to see drugs with performance metrics
4. **Deep Dive**: Click "Analyze" on any drug to see:
   - Bridge chart showing SGP components
   - AI-generated insights
   - Prioritized action items

### AI Assistant

The sidebar contains an AI assistant powered by Gemini. Try queries like:

- `top losers` - Show worst performing drugs
- `expiring soon` - Contracts expiring in <90 days
- `what should i do` - Get action recommendations
- `why did margin drop` - Explain margin changes
- `compare Drug A vs Drug B` - Side-by-side comparison

### Visual Design Rules

- **Background**: #1a1a1a (dark grey)
- **Colors**: Only green (#00ff41) for positive, red (#ff0844) for negative
- **Typography**: Monospace fonts for data
- **Style**: No rounded corners, no gradients, sharp rectangles only

## Data Structure

The app uses mock data defined in `data.py`. You can modify this to connect to your own data sources.

Key metrics:
- **SGP**: Specialty Gross Profit
- **YoY Change**: Year-over-year growth
- **Margin**: Profit margin percentage
- **Bridge Components**: Volume, Price, and Cost impacts

## Project Structure

```
drug-analytics/
├── app.py                 # Main application
├── data.py               # Data layer (mock data)
├── requirements.txt      # Dependencies
├── views/
│   ├── payer_view.py     # Payer card grid
│   ├── contract_view.py  # Contract list
│   ├── drug_view.py      # Drug table + deep dive
│   └── components.py     # Shared UI components
├── ai/
│   └── chat.py           # Gemini integration
└── utils/
    └── formatting.py     # Helper functions
```

## Customization

### Adding More Data

Edit `data.py` and add payers, contracts, or drugs to the `PORTFOLIO_DATA` dictionary.

### Changing Colors

Edit color constants in `utils/formatting.py`:
```python
COLOR_GREEN = "#00ff41"
COLOR_RED = "#ff0844"
COLOR_BG = "#1a1a1a"
```

### Modifying AI Behavior

Edit the system prompt in `ai/chat.py` → `get_system_prompt()`

## Requirements

- Python 3.10+
- streamlit >=1.28.0
- plotly >=5.17.0
- google-generativeai >=0.3.0
- pandas >=2.0.0

## License

MIT License
