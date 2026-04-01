# ============================================================
#   APP.PY — StockSense AI · Streamlit UI
#   Theme: Ocean Dark — deep navy, black, gold
#   Run:   streamlit run app.py
# ============================================================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time

from predictor import COMPANIES, run_prediction

# ============================================================
#   PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="StockSense AI",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#   CSS — Ocean Dark Theme
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap');

:root {
    --bg:        #0a0e1a;
    --bg2:       #0f1524;
    --bg3:       #141929;
    --card:      #111827;
    --card2:     #1a2235;
    --navy:      #0d1b3e;
    --blue:      #1e3a6e;
    --blue2:     #2a52a0;
    --blue3:     #3d6fc4;
    --gold:      #d4a843;
    --gold2:     #e8c46a;
    --gold3:     #f5d98a;
    --up:        #00c896;
    --down:      #ff4d6a;
    --text:      #e8eaf2;
    --text2:     #9aa3bb;
    --text3:     #5a6480;
    --border:    rgba(61,111,196,0.18);
    --border2:   rgba(61,111,196,0.08);
    --serif:     'Playfair Display', Georgia, serif;
    --sans:      'DM Sans', sans-serif;
    --mono:      'DM Mono', monospace;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.block-container { padding: 0 3rem 4rem !important; max-width: 1400px !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg2); }
::-webkit-scrollbar-thumb { background: var(--blue2); border-radius: 2px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text2) !important;
    font-family: var(--sans) !important;
}
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(61,111,196,0.08) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: var(--mono) !important;
    font-size: 0.8rem !important;
    border-radius: 4px !important;
}
[data-testid="stSidebar"] .stTextInput label {
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text3) !important;
    font-family: var(--mono) !important;
}
.key-ok   { color: var(--up); font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.1em; }
.key-none { color: var(--gold); font-family: var(--mono); font-size: 0.7rem; letter-spacing: 0.1em; }

/* ── TICKER STRIP ── */
.ticker-wrap {
    overflow: hidden;
    background: var(--bg2);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 0.55rem 0;
    white-space: nowrap;
}
.ticker-inner {
    display: inline-block;
    animation: ticker 40s linear infinite;
    font-family: var(--mono);
    font-size: 0.68rem;
    color: var(--text3);
    letter-spacing: 0.06em;
}
.ticker-inner span { margin: 0 2.5rem; }
.ticker-inner .up   { color: var(--up); }
.ticker-inner .down { color: var(--down); }
.ticker-inner .mid  { color: var(--text3); }
@keyframes ticker { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }

/* ── HERO ── */
.hero {
    padding: 4rem 0 2.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-family: var(--mono);
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: var(--serif);
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 700;
    color: var(--text);
    line-height: 1.05;
    margin-bottom: 0.8rem;
    letter-spacing: -0.01em;
}
.hero-title em {
    font-style: italic;
    color: var(--gold);
}
.hero-sub {
    font-family: var(--sans);
    font-size: 1rem;
    color: var(--text2);
    font-weight: 300;
    letter-spacing: 0.02em;
}
.hero-rule {
    width: 48px;
    height: 2px;
    background: var(--gold);
    margin: 1.5rem 0;
}

/* ── SELECTOR PANEL ── */
.selector-wrap {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 2px 24px rgba(0,0,0,0.4);
}

[data-testid="stSelectbox"] > div > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.9rem !important;
}
[data-testid="stSelectbox"] label {
    font-family: var(--mono) !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.15em !important;
    color: var(--text3) !important;
    text-transform: uppercase !important;
}
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue2) 100%) !important;
    border: 1px solid var(--blue3) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 1.5rem !important;
    border-radius: 6px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, var(--blue2) 0%, var(--blue3) 100%) !important;
    box-shadow: 0 4px 20px rgba(61,111,196,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── PROCESS LOG ── */
.process-log {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--blue3);
    border-radius: 0 6px 6px 0;
    padding: 1rem 1.4rem;
    font-family: var(--mono);
    font-size: 0.7rem;
    line-height: 2;
    margin: 1.5rem 0;
}
.log-line { display: flex; align-items: flex-start; gap: 0.8rem; }
.log-time  { color: var(--text3); min-width: 65px; }
.log-tag   { padding: 0.05rem 0.5rem; font-size: 0.58rem; letter-spacing: 0.06em; min-width: 52px; text-align: center; border-radius: 3px; }
.tag-ok    { background: rgba(0,200,150,0.12); color: var(--up); border: 1px solid rgba(0,200,150,0.3); }
.tag-run   { background: rgba(61,111,196,0.1); color: var(--blue3); border: 1px solid var(--border); }
.tag-ai    { background: rgba(212,168,67,0.12); color: var(--gold); border: 1px solid rgba(212,168,67,0.3); }
.tag-warn  { background: rgba(255,77,106,0.1);  color: var(--down); border: 1px solid rgba(255,77,106,0.25); }
.log-msg   { color: var(--text2); }

/* ── SECTION HEADER ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin: 2.5rem 0 1.2rem;
}
.sec-head-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}
.sec-head-text {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    color: var(--text3);
    text-transform: uppercase;
    white-space: nowrap;
}
.sec-head-dot {
    width: 6px;
    height: 6px;
    background: var(--gold);
    border-radius: 50%;
    flex-shrink: 0;
}

/* ── METRIC CARDS ── */
.metric-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1rem 0;
}
.mcard {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.4rem 1.6rem;
    animation: fadeUp 0.4s ease both;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.mcard::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.mcard:nth-child(1)::before { background: var(--blue3); }
.mcard:nth-child(2)::before { background: var(--gold); }
.mcard:nth-child(3)::before { background: var(--up); }
.mcard:nth-child(4)::before { background: var(--blue2); }
.mcard:nth-child(1) { animation-delay: 0.05s; }
.mcard:nth-child(2) { animation-delay: 0.1s; }
.mcard:nth-child(3) { animation-delay: 0.15s; }
.mcard:nth-child(4) { animation-delay: 0.2s; }
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.mcard-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    color: var(--text3);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.mcard-value {
    font-family: var(--serif);
    font-size: 2rem;
    font-weight: 600;
    line-height: 1;
    color: var(--text);
}
.mcard-value.c-green { color: var(--up); }
.mcard-value.c-red   { color: var(--down); }
.mcard-value.c-gold  { color: var(--gold); }
.mcard-sub {
    font-family: var(--mono);
    font-size: 0.6rem;
    color: var(--text3);
    margin-top: 0.5rem;
    letter-spacing: 0.08em;
}

/* ── INDICATOR CARDS ── */
.ind-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin: 1rem 0;
}
.ind-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.2rem 1.4rem;
    animation: fadeUp 0.4s ease 0.25s both;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.ind-label {
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.15em;
    color: var(--text3);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.ind-value {
    font-family: var(--serif);
    font-size: 1.8rem;
    font-weight: 600;
    line-height: 1;
}
.ind-bar-bg {
    height: 4px;
    background: var(--bg2);
    margin: 0.7rem 0 0.4rem;
    border-radius: 2px;
    overflow: hidden;
}
.ind-bar-fill {
    height: 100%;
    border-radius: 2px;
    transition: width 1s ease;
}
.ind-status {
    font-family: var(--mono);
    font-size: 0.6rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* ── AI EXPLANATION PANEL ── */
.ai-panel {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 2rem 2.4rem;
    margin: 1rem 0;
    animation: fadeUp 0.5s ease 0.3s both;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.ai-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 1.2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border2);
}
.ai-badge {
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue2) 100%);
    color: var(--text) !important;
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.1em;
    padding: 0.25rem 0.7rem;
    border-radius: 3px;
    text-transform: uppercase;
    border: 1px solid var(--blue3);
}
.ai-model-tag {
    font-family: var(--mono);
    font-size: 0.58rem;
    color: var(--text3);
    letter-spacing: 0.06em;
    margin-left: auto;
}
.ai-body {
    font-family: var(--sans);
    font-size: 1.05rem;
    font-weight: 300;
    line-height: 1.85;
    color: var(--text2);
}
.ai-body p { margin: 0 0 0.8rem 0; }
.ai-body p:last-child { margin-bottom: 0; }

/* ── CHART CARD ── */
.chart-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.5rem;
    margin-bottom: 1rem;
    animation: fadeUp 0.5s ease 0.2s both;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}

/* ── IDLE STATE ── */
.idle-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 6rem 2rem;
    gap: 1.2rem;
    text-align: center;
}
.idle-icon {
    width: 56px;
    height: 56px;
    border: 1px solid var(--border);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    color: var(--gold);
    background: var(--card);
}
.idle-title {
    font-family: var(--serif);
    font-size: 1.5rem;
    color: var(--text);
    font-weight: 600;
}
.idle-sub {
    font-family: var(--sans);
    font-size: 0.875rem;
    color: var(--text2);
    font-weight: 300;
    max-width: 320px;
    line-height: 1.6;
}

/* ── FOOTER ── */
.app-footer {
    text-align: center;
    padding: 2.5rem 0;
    font-family: var(--mono);
    font-size: 0.58rem;
    letter-spacing: 0.2em;
    color: var(--text3);
    text-transform: uppercase;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}

/* dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden;
}
[data-testid="stDataFrame"] * {
    background: var(--card) !important;
    color: var(--text2) !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
#   SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding: 2rem 1.5rem 1.5rem;">
        <div style="font-family:'DM Mono',monospace;font-size:0.6rem;letter-spacing:0.25em;
                    color:rgba(154,163,187,0.5);text-transform:uppercase;margin-bottom:0.5rem">
            Configuration
        </div>
        <div style="font-family:'Playfair Display',serif;font-size:1.5rem;
                    color:#e8eaf2;font-weight:600;margin-bottom:1.5rem;
                    padding-bottom:1.5rem;border-bottom:1px solid rgba(61,111,196,0.18)">
            StockSense
        </div>
    </div>
    """, unsafe_allow_html=True)

    groq_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com"
    )

    if groq_key and groq_key.strip():
        st.markdown('<div style="padding:0 1.5rem"><div class="key-ok">✓ Key connected — AI ready</div></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:0 1.5rem"><div class="key-none">○ No key — AI disabled</div></div>',
                    unsafe_allow_html=True)

    st.markdown("""
    <div style="padding: 1.5rem 1.5rem 0; margin-top:1rem;
                border-top:1px solid rgba(61,111,196,0.12)">
        <div style="font-family:'DM Sans',sans-serif;font-size:0.78rem;
                    color:rgba(154,163,187,0.4);line-height:1.7;font-weight:300">
            Your key is used only for this session and never stored anywhere.
            Get a free key at console.groq.com
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#   TICKER STRIP
# ============================================================
tape = (
    '<span class="up">RELIANCE ▲ 2.4%</span>'
    '<span class="mid">·</span>'
    '<span class="down">TCS ▼ 0.8%</span>'
    '<span class="mid">·</span>'
    '<span class="up">INFY ▲ 1.1%</span>'
    '<span class="mid">·</span>'
    '<span class="up">HDFC ▲ 0.5%</span>'
    '<span class="mid">·</span>'
    '<span class="down">ICICI ▼ 0.3%</span>'
    '<span class="mid">·</span>'
    '<span class="up">ITC ▲ 1.8%</span>'
    '<span class="mid">·</span>'
    '<span class="down">LT ▼ 0.6%</span>'
    '<span class="mid">·</span>'
    '<span class="up">AIRTEL ▲ 2.1%</span>'
    '<span class="mid">·</span>'
    '<span class="down">SBIN ▼ 1.2%</span>'
    '<span class="mid">·</span>'
    '<span>NIFTY 50 &nbsp;22,450</span>'
    '<span class="mid">·</span>'
    '<span>SENSEX &nbsp;74,120</span>'
    '<span class="mid">·</span>'
    '<span class="up">GOLD ▲ 0.4%</span>'
)
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-inner">{tape}{tape}</div></div>',
    unsafe_allow_html=True
)


# ============================================================
#   HERO
# ============================================================
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">◆ Neural Market Intelligence</div>
    <div class="hero-title">StockSense <em>AI</em></div>
    <div class="hero-rule"></div>
    <div class="hero-sub">
        Real-time NSE data · LSTM price forecasting · AI-powered plain-English analysis
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
#   SELECTOR
# ============================================================
st.markdown('<div class="selector-wrap">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    selected_name = st.selectbox("Select Company", list(COMPANIES.keys()), index=4)
with c2:
    period = st.selectbox("Time Window", ["3mo", "6mo", "1y"], index=1)
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("Run Analysis →")
st.markdown('</div>', unsafe_allow_html=True)

symbol       = COMPANIES[selected_name]
ticker_label = selected_name.split("·")[0].strip()


# ============================================================
#   CHART STYLING  — ocean dark background, gold accents
# ============================================================
def plotly_layout(height=500):
    return dict(
        paper_bgcolor="#111827",
        plot_bgcolor="#0f1524",
        font=dict(family="DM Mono, monospace", color="#9aa3bb", size=11),
        height=height,
        margin=dict(l=12, r=12, t=40, b=12),
        legend=dict(
            bgcolor="rgba(17,24,39,0.9)",
            bordercolor="rgba(61,111,196,0.2)",
            borderwidth=1,
            font=dict(size=10, color="#9aa3bb"),
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        xaxis=dict(
            gridcolor="rgba(61,111,196,0.08)",
            zerolinecolor="rgba(61,111,196,0.15)",
            showspikes=True,
            spikecolor="rgba(212,168,67,0.5)",
            spikethickness=1,
            linecolor="rgba(61,111,196,0.2)",
            tickfont=dict(color="#5a6480", size=10),
        ),
        yaxis=dict(
            gridcolor="rgba(61,111,196,0.08)",
            zerolinecolor="rgba(61,111,196,0.15)",
            linecolor="rgba(61,111,196,0.2)",
            tickfont=dict(color="#5a6480", size=10),
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="#1a2235",
            bordercolor="rgba(61,111,196,0.3)",
            font=dict(family="DM Mono", size=11, color="#e8eaf2")
        )
    )


def sec(label):
    st.markdown(f"""
    <div class="sec-head">
        <div class="sec-head-dot"></div>
        <div class="sec-head-text">{label}</div>
        <div class="sec-head-line"></div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#   ANALYSIS
# ============================================================
if run:

    log_ph = st.empty()
    logs   = []

    def log_callback(tag, cls, msg):
        import datetime
        t = datetime.datetime.now().strftime("%H:%M:%S")
        logs.append((t, tag, cls, msg))
        html = '<div class="process-log">'
        for lt, tg, tc, m in logs:
            html += (f'<div class="log-line">'
                     f'<span class="log-time">{lt}</span>'
                     f'<span class="log-tag {tc}">{tg}</span>'
                     f'<span class="log-msg">{m}</span></div>')
        html += '</div>'
        log_ph.markdown(html, unsafe_allow_html=True)

    try:
        result = run_prediction(
            symbol=symbol,
            period=period,
            groq_api_key=groq_key,
            log_callback=log_callback
        )
    except Exception as e:
        st.error(f"Analysis failed: {e}")
        st.stop()

    df              = result["df"]
    current_price   = result["current_price"]
    predicted_price = result["predicted_price"]
    change_pct      = result["change_pct"]
    trend           = result["trend"]
    rsi_val         = result["rsi"]
    macd_val        = result["macd"]
    atr_val         = result["atr"]
    vol_val         = result["volume"]
    rsi_status      = result["rsi_status"]
    macd_status     = result["macd_status"]
    explanation     = result["explanation"]

    # ── Metric Cards ─────────────────────────────────────────
    sec("Overview")
    c_cls = "c-green" if change_pct > 0 else "c-red" if change_pct < 0 else "c-gold"
    arrow = "▲" if change_pct > 0 else "▼" if change_pct < 0 else "—"

    st.markdown(f"""
    <div class="metric-strip">
        <div class="mcard">
            <div class="mcard-label">Current Price</div>
            <div class="mcard-value">₹{current_price:,.2f}</div>
            <div class="mcard-sub">{ticker_label} · Live NSE</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">LSTM Forecast</div>
            <div class="mcard-value {c_cls}">₹{predicted_price:,.2f}</div>
            <div class="mcard-sub">Tomorrow · {arrow} {abs(change_pct):.2f}%</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Expected Move</div>
            <div class="mcard-value {c_cls}">{'+' if change_pct > 0 else ''}{change_pct:.2f}%</div>
            <div class="mcard-sub">{trend}</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Volume</div>
            <div class="mcard-value c-gold">{vol_val/1e6:.1f}M</div>
            <div class="mcard-sub">ATR(14) · {atr_val:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Indicators ───────────────────────────────────────────
    sec("Technical Indicators")
    rsi_col  = "#00c896" if rsi_val < 30 else "#ff4d6a" if rsi_val > 70 else "#d4a843"
    macd_col = "#00c896" if macd_val > 0 else "#ff4d6a"
    sig_str  = "Strong" if abs(change_pct) > 1.5 else "Moderate" if abs(change_pct) > 0.3 else "Weak"
    sig_col  = "#00c896" if sig_str == "Strong" else "#d4a843" if sig_str == "Moderate" else "#ff4d6a"
    macd_pct = min(abs(macd_val) / max(abs(df['MACD'].max()), 0.001) * 100, 100)

    st.markdown(f"""
    <div class="ind-row">
        <div class="ind-card">
            <div class="ind-label">RSI · Relative Strength (14)</div>
            <div class="ind-value" style="color:{rsi_col}">{rsi_val:.1f}</div>
            <div class="ind-bar-bg">
                <div class="ind-bar-fill" style="width:{rsi_val:.0f}%;background:{rsi_col};opacity:0.8"></div>
            </div>
            <div class="ind-status" style="color:{rsi_col}">{rsi_status} · {'Overbought above 70' if rsi_val > 70 else 'Oversold below 30' if rsi_val < 30 else 'Healthy range 30–70'}</div>
        </div>
        <div class="ind-card">
            <div class="ind-label">MACD · Momentum Trend</div>
            <div class="ind-value" style="color:{macd_col}">{macd_val:+.3f}</div>
            <div class="ind-bar-bg">
                <div class="ind-bar-fill" style="width:{macd_pct:.0f}%;background:{macd_col};opacity:0.8"></div>
            </div>
            <div class="ind-status" style="color:{macd_col}">{macd_status} · {'Upward momentum' if macd_val > 0 else 'Downward momentum'}</div>
        </div>
        <div class="ind-card">
            <div class="ind-label">LSTM · Forecast Confidence</div>
            <div class="ind-value" style="color:{sig_col}">{sig_str}</div>
            <div class="ind-bar-bg">
                <div class="ind-bar-fill" style="width:{'85' if sig_str == 'Strong' else '50' if sig_str == 'Moderate' else '22'}%;background:{sig_col};opacity:0.8"></div>
            </div>
            <div class="ind-status" style="color:{sig_col}">Based on {change_pct:+.2f}% predicted delta</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── AI Explanation ────────────────────────────────────────
    sec("AI Analysis · Groq LLaMA 3.3")
    explanation_html = "".join(
        f"<p>{para.strip()}</p>"
        for para in explanation.replace("\n\n", "\n").split("\n")
        if para.strip()
    )
    st.markdown(f"""
    <div class="ai-panel">
        <div class="ai-header">
            <span class="ai-badge">Groq · LLaMA 3.3 · 70B</span>
            <span class="ai-model-tag">Plain-English Explanation</span>
        </div>
        <div class="ai-body">{explanation_html}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Chart 1: Full Technical ───────────────────────────────
    sec("Full Technical Chart")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    fig1 = make_subplots(rows=3, cols=1, shared_xaxes=True,
                         row_heights=[0.58, 0.21, 0.21], vertical_spacing=0.04)

    # Candlestick — bright green/red on dark background
    fig1.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing=dict(line=dict(color='#00c896', width=1), fillcolor='rgba(0,200,150,0.8)'),
        decreasing=dict(line=dict(color='#ff4d6a', width=1), fillcolor='rgba(255,77,106,0.8)'),
        name="OHLC"), row=1, col=1)

    # Bollinger Bands — subtle blue
    fig1.add_trace(go.Scatter(x=df.index, y=df['BB_high'],
        line=dict(color='rgba(61,111,196,0.4)', width=1, dash='dot'), showlegend=False), row=1, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['BB_low'],
        fill='tonexty', fillcolor='rgba(61,111,196,0.05)',
        line=dict(color='rgba(61,111,196,0.4)', width=1, dash='dot'), showlegend=False), row=1, col=1)

    # EMA — gold
    fig1.add_trace(go.Scatter(x=df.index, y=df['EMA_20'],
        line=dict(color='#d4a843', width=1.8), name="EMA 20"), row=1, col=1)

    # RSI — ocean blue
    fig1.add_trace(go.Scatter(x=df.index, y=df['RSI'],
        line=dict(color='#3d6fc4', width=1.5), name="RSI",
        fill='tozeroy', fillcolor='rgba(61,111,196,0.08)'), row=2, col=1)
    fig1.add_hline(y=70, line_dash="dot", line_color="rgba(255,77,106,0.5)",  line_width=1, row=2, col=1)
    fig1.add_hline(y=30, line_dash="dot", line_color="rgba(0,200,150,0.5)",   line_width=1, row=2, col=1)

    # MACD — green/red histogram, gold signal
    hist_colors = ['rgba(0,200,150,0.7)' if v >= 0 else 'rgba(255,77,106,0.7)' for v in df['MACD_hist']]
    fig1.add_trace(go.Bar(x=df.index, y=df['MACD_hist'],
        marker_color=hist_colors, name="Histogram"), row=3, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['MACD'],
        line=dict(color='#3d6fc4', width=1.5), name="MACD"), row=3, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'],
        line=dict(color='#d4a843', width=1.5), name="Signal"), row=3, col=1)

    ly1 = plotly_layout(680)
    ly1['xaxis_rangeslider_visible'] = False
    # apply dark bg to all subplots
    ly1['xaxis2'] = dict(**ly1.get('xaxis', {}))
    ly1['xaxis3'] = dict(**ly1.get('xaxis', {}))
    ly1['yaxis2'] = dict(**ly1.get('yaxis', {}))
    ly1['yaxis3'] = dict(**ly1.get('yaxis', {}))
    fig1.update_layout(**ly1)
    st.plotly_chart(fig1, use_container_width=True, config=dict(displayModeBar=False))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Chart 2: Price + Prediction ──────────────────────────
    sec("Price Forecast · LSTM Next-Day")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)

    last_n = df.tail(45)
    pred_x = [last_n.index[-1] + pd.Timedelta(days=1)]

    fig2 = go.Figure()
    # Price line — bright blue
    fig2.add_trace(go.Scatter(
        x=last_n.index, y=last_n['Close'], mode='lines', name='Close Price',
        line=dict(color='#3d6fc4', width=2),
        fill='tozeroy', fillcolor='rgba(61,111,196,0.07)'
    ))
    # EMA — gold dashed
    fig2.add_trace(go.Scatter(
        x=last_n.index, y=last_n['EMA_20'], mode='lines', name='EMA 20',
        line=dict(color='#d4a843', width=1.2, dash='dot')
    ))
    # Connector to forecast — gold dashed
    fig2.add_trace(go.Scatter(
        x=[last_n.index[-1], pred_x[0]],
        y=[last_n['Close'].iloc[-1], predicted_price],
        mode='lines', showlegend=False,
        line=dict(color='rgba(212,168,67,0.6)', width=1.5, dash='dash')
    ))
    # Forecast point — gold diamond
    fig2.add_trace(go.Scatter(
        x=pred_x, y=[predicted_price], mode='markers+text',
        marker=dict(size=14, color='#d4a843', symbol='diamond',
                    line=dict(color='#f5d98a', width=2)),
        text=[f"  ₹{predicted_price:,.2f}"],
        textposition="middle right",
        textfont=dict(family="DM Mono", size=12, color="#d4a843"),
        name='LSTM Forecast'
    ))
    # Current price line
    fig2.add_hline(y=current_price,
        line_dash="dot", line_color="rgba(154,163,187,0.3)", line_width=1,
        annotation_text=f"  Current ₹{current_price:,.2f}",
        annotation_font=dict(family="DM Mono", size=10, color="rgba(154,163,187,0.6)"),
        annotation_position="left")
    fig2.update_layout(**plotly_layout(380))
    st.plotly_chart(fig2, use_container_width=True, config=dict(displayModeBar=False))
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Chart 3 + 4: Volume & ATR ────────────────────────────
    sec("Volume · Volatility")
    ca, cb = st.columns(2)

    with ca:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        vol_colors = ['rgba(0,200,150,0.75)' if c >= o else 'rgba(255,77,106,0.75)'
                      for c, o in zip(last_n['Close'], last_n['Open'])]
        fig3 = go.Figure(go.Bar(
            x=last_n.index, y=last_n['Volume'],
            marker_color=vol_colors, name='Volume'
        ))
        fig3.update_layout(**plotly_layout(260))
        st.plotly_chart(fig3, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig4 = go.Figure(go.Scatter(
            x=df.index, y=df['ATR'],
            line=dict(color='#d4a843', width=1.5),
            fill='tozeroy', fillcolor='rgba(212,168,67,0.07)',
            name='ATR(14)'
        ))
        fig4.update_layout(**plotly_layout(260))
        st.plotly_chart(fig4, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Raw Data Table ────────────────────────────────────────
    sec("Raw Data · Last 10 Sessions")
    tbl = df[['Open', 'High', 'Low', 'Close', 'Volume', 'RSI', 'MACD', 'EMA_20', 'ATR']].tail(10).copy()
    tbl.index = tbl.index.strftime('%d %b %Y')
    tbl = tbl.round(2)
    st.dataframe(tbl, use_container_width=True, height=330)

    # ── Footer ────────────────────────────────────────────────
    st.markdown("""
    <div class="app-footer">
        StockSense AI · LSTM + Groq LLaMA 3.3 · NSE Data via yFinance ·
        Not financial advice · For educational use only
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#   IDLE
# ============================================================
else:
    st.markdown("""
    <div class="idle-wrap">
        <div class="idle-icon">◆</div>
        <div class="idle-title">Ready to analyse</div>
        <div class="idle-sub">
            Select a company and time window above,
            then click Run Analysis to get started.
        </div>
    </div>
    """, unsafe_allow_html=True)
