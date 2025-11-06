# 🏗️ Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                      (localhost:8501)                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      STREAMLIT APP                               │
│                       (app.py)                                   │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  • Page Configuration                                     │  │
│  │  • Custom CSS (Terminal Theme)                            │  │
│  │  • Session State Management                               │  │
│  │  • View Routing Logic                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────┬─────────────────────────┬─────────────────────┬───────────┘
      │                         │                     │
      ▼                         ▼                     ▼
┌──────────┐          ┌──────────────┐      ┌─────────────────┐
│   DATA   │          │    VIEWS     │      │   AI CHAT       │
│ (data.py)│          │  (views/)    │      │  (ai/chat.py)   │
└──────────┘          └──────────────┘      └─────────────────┘
      │                     │                        │
      │                     │                        │
      ▼                     ▼                        ▼
┌──────────┐          ┌──────────────┐      ┌─────────────────┐
│ PORTFOLIO│          │  COMPONENTS  │      │  GEMINI API     │
│   DATA   │          │  • Payer     │      │  (google.ai)    │
│          │          │  • Contract  │      └─────────────────┘
│ • Payers │          │  • Drug      │
│ • Metrics│          │  • Deep Dive │
│ • Alerts │          └──────┬───────┘
└──────────┘                 │
                             ▼
                    ┌─────────────────┐
                    │   UTILITIES     │
                    │ (utils/)        │
                    │  • Formatting   │
                    │  • Colors       │
                    │  • Calculations │
                    └─────────────────┘
```

## Data Flow

### 1. Navigation Flow
```
User Click → Session State Update → st.rerun() → View Re-render
```

### 2. View Rendering Flow
```
app.py (Router)
    │
    ├─→ payer_view.py
    │       ├─→ components.render_portfolio_header()
    │       ├─→ components.render_payer_card() × N
    │       └─→ data.get_portfolio_totals()
    │
    ├─→ contract_view.py
    │       ├─→ components.render_breadcrumb()
    │       ├─→ components.render_back_button()
    │       └─→ data.selected_payer
    │
    └─→ drug_view.py
            ├─→ components.render_breadcrumb()
            ├─→ render_drug_row() × N
            └─→ render_drug_deep_dive()
                    ├─→ create_bridge_chart() [Plotly]
                    ├─→ generate_drug_insights()
                    └─→ generate_action_items()
```

### 3. AI Chat Flow
```
User Query → chat.py
    │
    ├─→ get_portfolio_context()
    ├─→ get_system_prompt()
    ├─→ Gemini API Call
    └─→ Response → Sidebar Display
```

## Component Hierarchy

```
app.py (Main)
├── Header
├── Alerts Section
│   └── data.get_urgent_alerts()
│
├── View Router
│   ├── Payer View (default)
│   │   └── Payer Cards Grid (3 cols)
│   │
│   ├── Contract View
│   │   ├── Payer Summary
│   │   └── Contract Rows
│   │
│   └── Drug View
│       ├── Contract Summary
│       ├── Drug Table
│       └── Deep Dive (conditional)
│           ├── Metrics (4 cols)
│           ├── Bridge Chart
│           ├── AI Insights
│           └── Action Items
│
└── Sidebar
    └── AI Chat Interface
```

## Session State Structure

```python
st.session_state = {
    "current_view": "payer" | "contract" | "drug",
    "selected_payer": {payer_object} | None,
    "selected_contract": {contract_object} | None,
    "selected_drug": {drug_object} | None,
    "breadcrumb": ["Portfolio", "Payer", "Contract"],
    "chat_history": [{role, message}, ...],
    "gemini_configured": True | False
}
```

## Key Design Patterns

### 1. Hierarchical State Management
- Each navigation level stores its selection in session state
- Breadcrumb reconstructed from state
- Back buttons reset appropriate state levels

### 2. Component Reusability
- Shared UI components in `components.py`
- Formatting logic centralized in `utils/formatting.py`
- Data access through helper functions in `data.py`

### 3. Separation of Concerns
```
┌─────────────┐
│ Presentation│  → views/*.py (UI rendering)
├─────────────┤
│  Business   │  → data.py (logic, calculations)
├─────────────┤
│    Data     │  → PORTFOLIO_DATA (mock source)
└─────────────┘
```

### 4. Terminal Aesthetic Implementation
```css
/* Applied in app.py via st.markdown() */
Background → #1a1a1a
Positive   → #00ff41 (green)
Negative   → #ff0844 (red)
Neutral    → #ffffff (white)
Font       → 'Courier New', monospace
Borders    → 1px solid, no border-radius
```

## File Dependencies

```
app.py
├── imports: views.*, ai.chat, data
├── depends: streamlit
└── outputs: HTML/CSS to browser

views/payer_view.py
├── imports: components, data
└── depends: streamlit

views/contract_view.py
├── imports: components, utils.formatting
└── depends: streamlit

views/drug_view.py
├── imports: components, utils.formatting, plotly
└── depends: streamlit

views/components.py
├── imports: utils.formatting
└── depends: streamlit

ai/chat.py
├── imports: data, utils.formatting
└── depends: streamlit, google.generativeai

data.py
└── standalone (no external imports)

utils/formatting.py
└── standalone (no external imports)
```

## External Dependencies

```
streamlit >= 1.28.0
    └── Web framework + state management

plotly >= 5.17.0
    └── Bridge/Waterfall charts

google-generativeai >= 0.3.0
    └── Gemini AI integration

pandas >= 2.0.0
    └── Data manipulation (future use)
```

## Performance Considerations

### Optimizations Implemented:
1. **Lazy Loading**: Deep dive only renders when drug selected
2. **Component Caching**: Shared components reused across views
3. **Minimal Re-renders**: Strategic use of `st.rerun()`
4. **Efficient State**: Only essential data in session state

### Future Optimizations:
1. `@st.cache_data` for data loading
2. Virtualized tables for >100 drugs
3. Debounced AI queries
4. Progressive chart loading

## Security Considerations

1. **API Keys**: Stored in `.streamlit/secrets.toml` (gitignored)
2. **No User Input Execution**: All queries sanitized through Gemini
3. **Read-Only Data**: Mock data immutable
4. **Session Isolation**: Each browser session independent

## Scalability Path

### Current: Mock Data
```
PORTFOLIO_DATA (dict) → Views
```

### Future: Database Integration
```
Database → API Layer → Caching → Views
```

### Potential Architecture:
```
┌─────────────┐
│  Streamlit  │
│  Frontend   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FastAPI    │
│  Backend    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  PostgreSQL │
│  Database   │
└─────────────┘
```

## Testing Strategy

### Current:
- `test_imports.py`: Import verification
- Manual testing of navigation flows

### Recommended:
```python
# Unit tests
tests/test_data.py          # Data calculations
tests/test_formatting.py    # Formatting functions

# Integration tests
tests/test_views.py         # View rendering
tests/test_navigation.py    # Navigation flows

# E2E tests
tests/test_user_flows.py    # Complete user journeys
```

## Deployment Options

### 1. Streamlit Community Cloud (Free)
```bash
streamlit.io → Connect GitHub → Deploy
```

### 2. Docker Container
```dockerfile
FROM python:3.10
COPY . /app
RUN pip install -r requirements.txt
CMD ["streamlit", "run", "app.py"]
```

### 3. Cloud Platforms
- **AWS**: EC2 + ALB
- **GCP**: Cloud Run
- **Azure**: App Service
- **Heroku**: Direct deployment

---

**Architecture designed for:**
- ✅ Maintainability (modular structure)
- ✅ Scalability (clear upgrade path)
- ✅ Performance (efficient rendering)
- ✅ Extensibility (easy to add features)
