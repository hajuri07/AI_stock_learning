# ============================================================
#   APP.PY — Streamlit UI only
#   Run:    streamlit run app.py
#   Deploy: streamlit.io (free)
#
#   pip install streamlit plotly yfinance ta tensorflow groq scikit-learn
# ============================================================

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import time

from predictor import COMPANIES, run_prediction   # ← all ML lives here

# ============================================================
#   PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="StockSense AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
#   CSS — Bloomberg Terminal × Neon Noir
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@200;400;700;900&display=swap');

:root {
    --bg:      #03070f;
    --bg2:     #060d1a;
    --accent:  #00e5ff;
    --accent2: #ff6b35;
    --green:   #39ff14;
    --red:     #ff2d55;
    --gold:    #ffd60a;
    --dim:     rgba(0,229,255,0.12);
    --border:  rgba(0,229,255,0.18);
    --text:    #c8e6ff;
    --muted:   rgba(150,200,230,0.45);
    --mono:    'Share Tech Mono', monospace;
    --sans:    'Exo 2', sans-serif;
}

*, *::before, *::after { box-sizing: border-box; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: var(--sans) !important;
}

[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed; inset: 0;
    background: repeating-linear-gradient(
        0deg, transparent, transparent 2px,
        rgba(0,0,0,0.06) 2px, rgba(0,0,0,0.06) 4px
    );
    pointer-events: none; z-index: 9998;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"] { display: none !important; }

.block-container { padding: 0 2.5rem 4rem !important; max-width: 1440px !important; }

::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 2px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; font-family: var(--mono) !important; }
[data-testid="stSidebar"] .stTextInput input {
    background: rgba(0,5,15,0.9) !important;
    border: 1px solid var(--border) !important;
    color: var(--accent) !important;
    font-family: var(--mono) !important;
    font-size: 0.75rem !important;
    border-radius: 2px !important;
}
[data-testid="stSidebar"] .stTextInput label {
    font-size: 0.58rem !important;
    letter-spacing: 0.3em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}
.api-status-ok   { color: #39ff14; font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.2em; }
.api-status-none { color: #ffd60a; font-family: var(--mono); font-size: 0.65rem; letter-spacing: 0.2em; }

/* ── TICKER TAPE ── */
.ticker-wrap {
    overflow: hidden; background: rgba(0,229,255,0.03);
    border-bottom: 1px solid var(--border); padding: 0.4rem 0; white-space: nowrap;
}
.ticker-inner {
    display: inline-block; animation: ticker 35s linear infinite;
    font-family: var(--mono); font-size: 0.7rem;
    color: var(--accent); letter-spacing: 0.08em;
}
.ticker-inner span { margin: 0 2.5rem; }
.ticker-inner .up   { color: var(--green); }
.ticker-inner .down { color: var(--red); }
@keyframes ticker { 0%{transform:translateX(0)} 100%{transform:translateX(-50%)} }

/* ── HERO ── */
.hero { padding: 2.5rem 0 1.5rem; text-align: center; }
.hero-eyebrow {
    font-family: var(--mono); font-size: 0.62rem;
    letter-spacing: 0.5em; color: var(--accent);
    text-transform: uppercase; opacity: 0.65; margin-bottom: 0.6rem;
}
.hero-title {
    font-family: var(--sans); font-size: clamp(3rem,8vw,6.5rem);
    font-weight: 900; line-height: 0.9; text-transform: uppercase;
    letter-spacing: -0.02em;
    background: linear-gradient(160deg, #fff 0%, var(--accent) 40%, var(--accent2) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: heroGlow 4s ease-in-out infinite alternate;
}
@keyframes heroGlow {
    from { filter: drop-shadow(0 0 20px rgba(0,229,255,0.3)); }
    to   { filter: drop-shadow(0 0 40px rgba(255,107,53,0.4)); }
}
.hero-sub {
    font-family: var(--mono); font-size: 0.72rem;
    letter-spacing: 0.3em; color: var(--muted); margin-top: 0.8rem;
}
.hero-divider {
    display: flex; align-items: center; gap: 1rem;
    margin: 1.5rem auto; max-width: 500px;
}
.hero-divider::before { content:''; flex:1; height:1px; background: linear-gradient(90deg,transparent,var(--accent)); }
.hero-divider::after  { content:''; flex:1; height:1px; background: linear-gradient(90deg,var(--accent),transparent); }
.hero-diamond {
    width:8px; height:8px; background:var(--accent); transform:rotate(45deg);
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%,100%{box-shadow:0 0 0 0 rgba(0,229,255,0.4)}
    50%{box-shadow:0 0 0 8px rgba(0,229,255,0)}
}

/* ── SELECTOR ── */
.selector-panel {
    background: linear-gradient(135deg,rgba(0,229,255,0.04),rgba(255,107,53,0.02));
    border: 1px solid var(--border); border-radius: 2px;
    padding: 1.8rem 2rem; margin-bottom: 1.5rem; position: relative;
    clip-path: polygon(0 0,calc(100% - 16px) 0,100% 16px,100% 100%,16px 100%,0 calc(100% - 16px));
}
.selector-panel::before {
    content: 'MARKET TERMINAL v2.4';
    position: absolute; top: -1px; left: 1.5rem;
    font-family: var(--mono); font-size: 0.52rem; letter-spacing: 0.3em;
    color: var(--bg); background: var(--accent); padding: 0.15rem 0.6rem;
}
[data-testid="stSelectbox"] > div > div {
    background: rgba(0,5,15,0.9) !important;
    border: 1px solid var(--border) !important; border-radius: 2px !important;
    color: var(--accent) !important; font-family: var(--mono) !important; font-size: 0.8rem !important;
}
[data-testid="stSelectbox"] label {
    font-family: var(--mono) !important; font-size: 0.58rem !important;
    letter-spacing: 0.35em !important; color: var(--muted) !important; text-transform: uppercase !important;
}
.stButton > button {
    width: 100% !important; background: transparent !important;
    border: 1px solid var(--accent) !important; color: var(--accent) !important;
    font-family: var(--mono) !important; font-size: 0.75rem !important;
    letter-spacing: 0.3em !important; text-transform: uppercase !important;
    padding: 0.8rem !important; border-radius: 0 !important; transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(0,229,255,0.08) !important;
    box-shadow: 0 0 30px rgba(0,229,255,0.25) !important; color: #fff !important;
}

/* ── PROCESS LOG ── */
.process-log {
    background: rgba(0,0,0,0.55); border: 1px solid rgba(0,229,255,0.1);
    border-left: 3px solid var(--accent); padding: 1rem 1.4rem;
    font-family: var(--mono); font-size: 0.7rem; line-height: 2; margin: 1rem 0;
}
.log-line { display:flex; align-items:flex-start; gap:0.8rem; }
.log-time  { color:var(--muted); min-width:65px; }
.log-tag   { padding:0.05rem 0.4rem; font-size:0.58rem; letter-spacing:0.08em; min-width:58px; text-align:center; }
.tag-ok    { background:rgba(57,255,20,0.12);  color:var(--green);   border:1px solid rgba(57,255,20,0.3); }
.tag-run   { background:rgba(0,229,255,0.08);  color:var(--accent);  border:1px solid rgba(0,229,255,0.25); }
.tag-ai    { background:rgba(255,107,53,0.1);  color:var(--accent2); border:1px solid rgba(255,107,53,0.3); }
.tag-warn  { background:rgba(255,214,10,0.08); color:var(--gold);    border:1px solid rgba(255,214,10,0.3); }
.log-msg   { color:var(--text); }

/* ── METRIC CARDS ── */
.metric-strip { display:grid; grid-template-columns:repeat(4,1fr); gap:0.8rem; margin:1.2rem 0; }
.mcard {
    background:var(--bg2); border:1px solid var(--border); padding:1.2rem 1.4rem;
    clip-path:polygon(0 0,calc(100% - 10px) 0,100% 10px,100% 100%,0 100%);
    animation:cardIn 0.5s cubic-bezier(0.16,1,0.3,1) both;
}
.mcard:nth-child(1){animation-delay:.05s;border-top:2px solid var(--accent);}
.mcard:nth-child(2){animation-delay:.12s;border-top:2px solid var(--green);}
.mcard:nth-child(3){animation-delay:.19s;border-top:2px solid var(--accent2);}
.mcard:nth-child(4){animation-delay:.26s;border-top:2px solid var(--gold);}
@keyframes cardIn { from{opacity:0;transform:translateY(16px) scale(0.97)} to{opacity:1;transform:translateY(0) scale(1)} }
.mcard-label { font-family:var(--mono); font-size:0.57rem; letter-spacing:0.3em; color:var(--muted); text-transform:uppercase; margin-bottom:0.5rem; }
.mcard-value { font-family:var(--mono); font-size:1.85rem; font-weight:400; line-height:1; color:#fff; }
.mcard-value.c-green  { color:var(--green);  text-shadow:0 0 20px rgba(57,255,20,0.5); }
.mcard-value.c-red    { color:var(--red);    text-shadow:0 0 20px rgba(255,45,85,0.5); }
.mcard-value.c-gold   { color:var(--gold);   text-shadow:0 0 20px rgba(255,214,10,0.4); }
.mcard-value.c-accent { color:var(--accent); text-shadow:0 0 20px rgba(0,229,255,0.4); }
.mcard-sub { font-family:var(--mono); font-size:0.58rem; color:var(--muted); margin-top:0.4rem; letter-spacing:0.1em; }

/* ── INDICATOR PILLS ── */
.ind-row { display:grid; grid-template-columns:repeat(3,1fr); gap:0.8rem; margin:1rem 0; }
.ind-card {
    background:var(--bg2); border:1px solid var(--border); padding:1rem 1.2rem;
    animation:cardIn 0.5s cubic-bezier(0.16,1,0.3,1) 0.3s both;
}
.ind-label { font-family:var(--mono); font-size:0.57rem; letter-spacing:0.28em; color:var(--muted); text-transform:uppercase; margin-bottom:0.5rem; }
.ind-value { font-family:var(--mono); font-size:1.5rem; }
.ind-bar-bg { height:3px; background:rgba(255,255,255,0.05); margin:0.5rem 0 0.3rem; border-radius:2px; overflow:hidden; }
.ind-bar-fill { height:100%; border-radius:2px; }
.ind-status { font-family:var(--mono); font-size:0.57rem; letter-spacing:0.2em; text-transform:uppercase; }

/* ── AI PANEL ── */
.ai-panel {
    background:linear-gradient(135deg,rgba(0,229,255,0.025),rgba(255,107,53,0.025));
    border:1px solid var(--border); border-left:3px solid var(--accent2);
    padding:1.8rem 2rem; margin:1rem 0; position:relative;
    animation:cardIn 0.6s cubic-bezier(0.16,1,0.3,1) 0.4s both;
    clip-path:polygon(0 0,100% 0,100% calc(100% - 14px),calc(100% - 14px) 100%,0 100%);
}
.ai-header { display:flex; align-items:center; gap:0.8rem; margin-bottom:1rem; }
.ai-dot { width:6px; height:6px; background:var(--accent2); border-radius:50%; animation:pulse 1.5s ease-in-out infinite; }
.ai-tag { font-family:var(--mono); font-size:0.58rem; letter-spacing:0.3em; color:var(--accent2); text-transform:uppercase; }
.ai-model { font-family:var(--mono); font-size:0.55rem; color:var(--muted); margin-left:auto; letter-spacing:0.08em; }
.ai-body { font-family:var(--sans); font-size:1.05rem; font-weight:300; line-height:1.8; color:rgba(200,230,255,0.9); }

/* ── SECTION LABEL ── */
.sec-label {
    font-family:var(--mono); font-size:0.58rem; letter-spacing:0.45em; color:var(--accent);
    text-transform:uppercase; opacity:0.6; margin:2rem 0 0.8rem;
    display:flex; align-items:center; gap:0.8rem;
}
.sec-label::after { content:''; flex:1; height:1px; background:linear-gradient(90deg,var(--border),transparent); }

/* ── CHART BOX ── */
.chart-box {
    border:1px solid var(--border); background:rgba(0,5,10,0.5);
    margin-bottom:0.8rem; padding:0.5rem;
    animation:cardIn 0.6s cubic-bezier(0.16,1,0.3,1) 0.2s both;
    clip-path:polygon(0 0,calc(100% - 14px) 0,100% 14px,100% 100%,14px 100%,0 calc(100% - 14px));
}

/* ── IDLE ── */
.idle-wrap { display:flex; flex-direction:column; align-items:center; padding:5rem 2rem; gap:1.5rem; }
.idle-ring { width:80px; height:80px; border:1px solid rgba(0,229,255,0.2); border-top:2px solid var(--accent); border-radius:50%; animation:spin 3s linear infinite; }
.idle-ring-inner { width:50px; height:50px; border:1px solid rgba(255,107,53,0.2); border-bottom:2px solid var(--accent2); border-radius:50%; animation:spin 2s linear infinite reverse; margin:13px auto; }
@keyframes spin { to{transform:rotate(360deg)} }
.idle-text { font-family:var(--mono); font-size:0.68rem; letter-spacing:0.4em; color:var(--muted); text-transform:uppercase; text-align:center; }

/* ── FOOTER ── */
.app-footer {
    text-align:center; padding:2rem 0; font-family:var(--mono); font-size:0.52rem;
    letter-spacing:0.35em; color:rgba(0,229,255,0.15); text-transform:uppercase;
    border-top:1px solid rgba(0,229,255,0.06); margin-top:3rem;
}
[data-testid="stDataFrame"] { border:1px solid var(--border) !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
#   SIDEBAR — API KEY INPUT
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.6rem;
                letter-spacing:0.4em;color:rgba(0,229,255,0.5);
                text-transform:uppercase;margin-bottom:1.5rem;padding-bottom:0.8rem;
                border-bottom:1px solid rgba(0,229,255,0.1)">
        ◈ StockSense AI · Config
    </div>
    """, unsafe_allow_html=True)

    groq_key = st.text_input(
        "GROQ API KEY",
        type="password",
        placeholder="gsk_...",
        help="Get your free key at console.groq.com"
    )

    if groq_key and groq_key.strip():
        st.markdown('<div class="api-status-ok">▲ KEY CONNECTED · AI READY</div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="api-status-none">◆ NO KEY · AI DISABLED</div>',
                    unsafe_allow_html=True)
        st.markdown("""
        <div style="font-family:'Share Tech Mono',monospace;font-size:0.58rem;
                    color:rgba(150,200,230,0.35);margin-top:0.8rem;line-height:1.8">
            Get a free key at<br>
            <span style="color:rgba(0,229,255,0.5)">console.groq.com</span><br><br>
            Charts + LSTM work<br>without a key.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Share Tech Mono',monospace;font-size:0.52rem;
                color:rgba(150,200,230,0.2);line-height:1.8">
        Your key is never stored.<br>
        Only used for this session.
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#   TICKER TAPE
# ============================================================
tape = (
    '<span class="up">RELIANCE ▲ 2.4%</span>'
    '<span class="down">TCS ▼ 0.8%</span>'
    '<span class="up">INFY ▲ 1.1%</span>'
    '<span class="up">HDFC ▲ 0.5%</span>'
    '<span class="down">ICICI ▼ 0.3%</span>'
    '<span class="up">ITC ▲ 1.8%</span>'
    '<span class="down">LT ▼ 0.6%</span>'
    '<span class="up">AIRTEL ▲ 2.1%</span>'
    '<span class="down">SBIN ▼ 1.2%</span>'
    '<span>NIFTY 50 · 22,450</span>'
    '<span>SENSEX · 74,120</span>'
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
    <div class="hero-eyebrow">◈ Neural Market Intelligence System ◈</div>
    <div class="hero-title">StockSense AI</div>
    <div class="hero-sub">LSTM · Groq LLaMA 3.3 · Technical Analysis · Real-time NSE Data</div>
    <div class="hero-divider"><div class="hero-diamond"></div></div>
</div>
""", unsafe_allow_html=True)


# ============================================================
#   SELECTOR
# ============================================================
st.markdown('<div class="selector-panel">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([3, 1, 1])
with c1:
    selected_name = st.selectbox("TARGET SYMBOL", list(COMPANIES.keys()), index=4)
with c2:
    period = st.selectbox("DATA WINDOW", ["3mo", "6mo", "1y"], index=1)
with c3:
    st.markdown("<br>", unsafe_allow_html=True)
    run = st.button("⬡ EXECUTE ANALYSIS")
st.markdown('</div>', unsafe_allow_html=True)

symbol       = COMPANIES[selected_name]
ticker_label = selected_name.split("·")[0].strip()


# ============================================================
#   HELPERS
# ============================================================
def plotly_layout(height=500):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,3,8,0.7)",
        font=dict(family="Exo 2, sans-serif", color="rgba(180,210,230,0.65)", size=11),
        height=height, margin=dict(l=8, r=8, t=38, b=8),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10),
                    orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor="rgba(0,229,255,0.05)", zerolinecolor="rgba(0,229,255,0.08)",
                   showspikes=True, spikecolor="rgba(0,229,255,0.3)", spikethickness=1),
        yaxis=dict(gridcolor="rgba(0,229,255,0.05)", zerolinecolor="rgba(0,229,255,0.08)"),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#03070f", bordercolor="rgba(0,229,255,0.3)",
                        font=dict(family="Share Tech Mono", size=11, color="#c8e6ff"))
    )


# ============================================================
#   ANALYSIS BLOCK
# ============================================================
if run:

    # ── Live log in UI ──────────────────────────────────────
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

    # ── Run full pipeline from predictor.py ────────────────
    try:
        result = run_prediction(
            symbol      = symbol,
            period      = period,
            groq_api_key= groq_key,
            log_callback= log_callback
        )
    except Exception as e:
        st.error(f"Pipeline error: {e}")
        st.stop()

    # ── Unpack result ───────────────────────────────────────
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

    # ============================================================
    #   METRIC CARDS
    # ============================================================
    st.markdown('<div class="sec-label">◈ Live Metrics</div>', unsafe_allow_html=True)
    c_cls = "c-green" if change_pct > 0 else "c-red" if change_pct < 0 else "c-gold"
    arrow = "▲" if change_pct > 0 else "▼" if change_pct < 0 else "◆"

    st.markdown(f"""
    <div class="metric-strip">
        <div class="mcard">
            <div class="mcard-label">Current Price</div>
            <div class="mcard-value c-accent">₹{current_price:,.2f}</div>
            <div class="mcard-sub">{ticker_label} · NSE LIVE</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">LSTM Prediction</div>
            <div class="mcard-value {c_cls}">₹{predicted_price:,.2f}</div>
            <div class="mcard-sub">TOMORROW · {arrow} {abs(change_pct):.2f}%</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Expected Change</div>
            <div class="mcard-value {c_cls}">{'+' if change_pct>0 else ''}{change_pct:.2f}%</div>
            <div class="mcard-sub">{trend}</div>
        </div>
        <div class="mcard">
            <div class="mcard-label">Volume · ATR</div>
            <div class="mcard-value c-gold">{vol_val/1e6:.1f}M</div>
            <div class="mcard-sub">ATR(14) · {atr_val:.2f}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    #   INDICATORS
    # ============================================================
    st.markdown('<div class="sec-label">◈ Technical Indicators</div>', unsafe_allow_html=True)
    rsi_col  = "#39ff14" if rsi_val < 30 else "#ff2d55" if rsi_val > 70 else "#ffd60a"
    macd_col = "#39ff14" if macd_val > 0 else "#ff2d55"
    sig_str  = "STRONG" if abs(change_pct) > 1.5 else "MODERATE" if abs(change_pct) > 0.3 else "WEAK"
    sig_col  = "#39ff14" if sig_str == "STRONG" else "#ffd60a" if sig_str == "MODERATE" else "#ff2d55"
    macd_pct = min(abs(macd_val) / max(abs(df['MACD'].max()), 0.001) * 100, 100)

    st.markdown(f"""
    <div class="ind-row">
        <div class="ind-card">
            <div class="ind-label">RSI · Relative Strength Index (14)</div>
            <div class="ind-value" style="color:{rsi_col}">{rsi_val:.1f}</div>
            <div class="ind-bar-bg"><div class="ind-bar-fill" style="width:{rsi_val:.0f}%;background:{rsi_col}"></div></div>
            <div class="ind-status" style="color:{rsi_col}">{rsi_status} · {'above 70 = overbought' if rsi_val>70 else 'below 30 = oversold' if rsi_val<30 else 'healthy zone 30–70'}</div>
        </div>
        <div class="ind-card">
            <div class="ind-label">MACD · Moving Average Convergence</div>
            <div class="ind-value" style="color:{macd_col}">{macd_val:+.3f}</div>
            <div class="ind-bar-bg"><div class="ind-bar-fill" style="width:{macd_pct:.0f}%;background:{macd_col}"></div></div>
            <div class="ind-status" style="color:{macd_col}">{macd_status} MOMENTUM · {'price rising' if macd_val>0 else 'price falling'}</div>
        </div>
        <div class="ind-card">
            <div class="ind-label">LSTM · Signal Confidence</div>
            <div class="ind-value" style="color:{sig_col}">{sig_str}</div>
            <div class="ind-bar-bg"><div class="ind-bar-fill" style="width:{'85' if sig_str=='STRONG' else '55' if sig_str=='MODERATE' else '25'}%;background:{sig_col}"></div></div>
            <div class="ind-status" style="color:{sig_col}">BASED ON {change_pct:+.2f}% PREDICTED DELTA</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    #   AI EXPLANATION
    # ============================================================
    st.markdown('<div class="sec-label">◈ AI Analysis · Groq LLaMA 3.3</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ai-panel">
        <div class="ai-header">
            <div class="ai-dot"></div>
            <div class="ai-tag">Groq · LLaMA 3.3 · 70B Versatile</div>
            <div class="ai-model">temp=0.7 · max_tokens=512</div>
        </div>
        <div class="ai-body">{explanation}</div>
    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    #   CHART 1 — FULL TECHNICAL
    # ============================================================
    st.markdown('<div class="sec-label">◈ Full Technical Chart</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    fig1 = make_subplots(rows=3, cols=1, shared_xaxes=True,
                         row_heights=[0.58, 0.21, 0.21], vertical_spacing=0.04)
    fig1.add_trace(go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing=dict(line=dict(color='#39ff14', width=1), fillcolor='rgba(57,255,20,0.7)'),
        decreasing=dict(line=dict(color='#ff2d55', width=1), fillcolor='rgba(255,45,85,0.7)'),
        name="OHLC"), row=1, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['BB_high'],
        line=dict(color='rgba(0,229,255,0.22)', width=1, dash='dot'), showlegend=False), row=1, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['BB_low'],
        fill='tonexty', fillcolor='rgba(0,229,255,0.035)',
        line=dict(color='rgba(0,229,255,0.22)', width=1, dash='dot'), showlegend=False), row=1, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['EMA_20'],
        line=dict(color='#ffd60a', width=1.5), name="EMA 20"), row=1, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['RSI'],
        line=dict(color='#aa88ff', width=1.5), name="RSI",
        fill='tozeroy', fillcolor='rgba(170,136,255,0.04)'), row=2, col=1)
    fig1.add_hline(y=70, line_dash="dot", line_color="rgba(255,45,85,0.45)",  line_width=1, row=2, col=1)
    fig1.add_hline(y=30, line_dash="dot", line_color="rgba(57,255,20,0.45)",  line_width=1, row=2, col=1)
    hist_colors = ['#39ff14' if v >= 0 else '#ff2d55' for v in df['MACD_hist']]
    fig1.add_trace(go.Bar(x=df.index, y=df['MACD_hist'],
        marker_color=hist_colors, name="Hist", opacity=0.55), row=3, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['MACD'],
        line=dict(color='#00e5ff', width=1.5), name="MACD"), row=3, col=1)
    fig1.add_trace(go.Scatter(x=df.index, y=df['MACD_signal'],
        line=dict(color='#ff6b35', width=1.5), name="Signal"), row=3, col=1)

    ly1 = plotly_layout(680)
    ly1['xaxis_rangeslider_visible'] = False
    fig1.update_layout(**ly1)
    st.plotly_chart(fig1, use_container_width=True, config=dict(displayModeBar=False))
    st.markdown('</div>', unsafe_allow_html=True)

    # ============================================================
    #   CHART 2 — PRICE + PREDICTION
    # ============================================================
    st.markdown('<div class="sec-label">◈ Price Forecast · LSTM Next-Day</div>', unsafe_allow_html=True)
    st.markdown('<div class="chart-box">', unsafe_allow_html=True)

    last_n = df.tail(45)
    pred_x = [last_n.index[-1] + pd.Timedelta(days=1)]

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=last_n.index, y=last_n['Close'], mode='lines', name='Close',
        line=dict(color='#00e5ff', width=2),
        fill='tozeroy', fillcolor='rgba(0,229,255,0.04)'
    ))
    fig2.add_trace(go.Scatter(
        x=last_n.index, y=last_n['EMA_20'], mode='lines', name='EMA 20',
        line=dict(color='#ffd60a', width=1, dash='dot')
    ))
    fig2.add_trace(go.Scatter(
        x=[last_n.index[-1], pred_x[0]],
        y=[last_n['Close'].iloc[-1], predicted_price],
        mode='lines', showlegend=False,
        line=dict(color='rgba(255,107,53,0.5)', width=1.5, dash='dash')
    ))
    fig2.add_trace(go.Scatter(
        x=pred_x, y=[predicted_price], mode='markers+text',
        marker=dict(size=18, color='#ff6b35', symbol='star',
                    line=dict(color='#ffd60a', width=2)),
        text=[f"  ₹{predicted_price:,.2f}"],
        textposition="middle right",
        textfont=dict(family="Share Tech Mono", size=12, color="#ff6b35"),
        name='LSTM Prediction'
    ))
    fig2.add_hline(y=current_price,
        line_dash="dot", line_color="rgba(0,229,255,0.3)", line_width=1,
        annotation_text=f"  Current ₹{current_price:,.2f}",
        annotation_font=dict(family="Share Tech Mono", size=10, color="rgba(0,229,255,0.5)"),
        annotation_position="left")
    fig2.update_layout(**plotly_layout(380))
    st.plotly_chart(fig2, use_container_width=True, config=dict(displayModeBar=False))
    st.markdown('</div>', unsafe_allow_html=True)

    # ============================================================
    #   CHART 3 + 4 — VOLUME & ATR
    # ============================================================
    st.markdown('<div class="sec-label">◈ Volume · Volatility</div>', unsafe_allow_html=True)
    ca, cb = st.columns(2)

    with ca:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        vol_colors = ['#39ff14' if c >= o else '#ff2d55'
                      for c, o in zip(last_n['Close'], last_n['Open'])]
        fig3 = go.Figure(go.Bar(
            x=last_n.index, y=last_n['Volume'],
            marker_color=vol_colors, opacity=0.75, name='Volume'
        ))
        fig3.update_layout(**plotly_layout(260))
        st.plotly_chart(fig3, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    with cb:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        fig4 = go.Figure(go.Scatter(
            x=df.index, y=df['ATR'],
            line=dict(color='#ff6b35', width=1.5),
            fill='tozeroy', fillcolor='rgba(255,107,53,0.06)',
            name='ATR(14)'
        ))
        fig4.update_layout(**plotly_layout(260))
        st.plotly_chart(fig4, use_container_width=True, config=dict(displayModeBar=False))
        st.markdown('</div>', unsafe_allow_html=True)

    # ============================================================
    #   RAW DATA TABLE
    # ============================================================
    st.markdown('<div class="sec-label">◈ Raw Data · Last 10 Sessions</div>', unsafe_allow_html=True)
    tbl = df[['Open','High','Low','Close','Volume','RSI','MACD','EMA_20','ATR']].tail(10).copy()
    tbl.index = tbl.index.strftime('%d %b %Y')
    tbl = tbl.round(2)
    st.dataframe(tbl, use_container_width=True, height=330)

    # ============================================================
    #   FOOTER
    # ============================================================
    st.markdown("""
    <div class="app-footer">
        StockSense AI · LSTM + Groq LLaMA 3.3 · NSE Data via yFinance ·
        Not financial advice · Educational use only
    </div>
    """, unsafe_allow_html=True)


# ============================================================
#   IDLE STATE
# ============================================================
else:
    st.markdown("""
    <div class="idle-wrap">
        <div class="idle-ring"><div class="idle-ring-inner"></div></div>
        <div class="idle-text">Select a symbol above<br>and execute analysis</div>
    </div>
    """, unsafe_allow_html=True)
