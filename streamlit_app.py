# ============================================================
# streamlit_app.py — AI Trading Dashboard (Indian Markets)
# NSE/BSE · INR · IST · iPhone Safari Optimized
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
import pytz
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Trader India",
    page_icon="🇮🇳",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# INDIAN STOCKS MASTER LIST
# ─────────────────────────────────────────────
INDIAN_STOCKS = {
    "── NIFTY 50 INDEX ──": {
        "Nifty 50":          "^NSEI",
        "Bank Nifty":        "^NSEBANK",
        "Nifty IT":          "^CNXIT",
        "Nifty Auto":        "^CNXAUTO",
        "Nifty Pharma":      "^CNXPHARMA",
        "Nifty FMCG":        "^CNXFMCG",
        "Nifty Metal":       "^CNXMETAL",
        "Nifty Realty":      "^CNXREALTY",
        "Nifty Energy":      "^CNXENERGY",
    },
    "── BANKING & FINANCE ──": {
        "HDFC Bank":         "HDFCBANK.NS",
        "ICICI Bank":        "ICICIBANK.NS",
        "State Bank (SBI)":  "SBIN.NS",
        "Kotak Mahindra":    "KOTAKBANK.NS",
        "Axis Bank":         "AXISBANK.NS",
        "IndusInd Bank":     "INDUSINDBK.NS",
        "Bank of Baroda":    "BANKBARODA.NS",
        "Punjab Natl Bank":  "PNB.NS",
        "Bajaj Finance":     "BAJFINANCE.NS",
        "Bajaj Finserv":     "BAJAJFINSV.NS",
        "Shriram Finance":   "SHRIRAMFIN.NS",
        "Muthoot Finance":   "MUTHOOTFIN.NS",
        "HDFC Life":         "HDFCLIFE.NS",
        "SBI Life":          "SBILIFE.NS",
        "ICICI Prudential":  "ICICIPRULI.NS",
    },
    "── IT & TECHNOLOGY ──": {
        "TCS":               "TCS.NS",
        "Infosys":           "INFY.NS",
        "Wipro":             "WIPRO.NS",
        "HCL Technologies":  "HCLTECH.NS",
        "Tech Mahindra":     "TECHM.NS",
        "LTIMindtree":       "LTIM.NS",
        "Mphasis":           "MPHASIS.NS",
        "Persistent Sys":    "PERSISTENT.NS",
        "Coforge":           "COFORGE.NS",
        "Hexaware":          "HEXAWARE.NS",
    },
    "── OIL, GAS & ENERGY ──": {
        "Reliance Ind.":     "RELIANCE.NS",
        "ONGC":              "ONGC.NS",
        "Coal India":        "COALINDIA.NS",
        "NTPC":              "NTPC.NS",
        "Power Grid":        "POWERGRID.NS",
        "Adani Green":       "ADANIGREEN.NS",
        "Adani Total Gas":   "ATGL.NS",
        "Adani Power":       "ADANIPOWER.NS",
        "Tata Power":        "TATAPOWER.NS",
        "GAIL India":        "GAIL.NS",
        "Indian Oil (IOC)":  "IOC.NS",
        "BPCL":              "BPCL.NS",
        "HPCL":              "HPCL.NS",
    },
    "── AUTO & EV ──": {
        "Maruti Suzuki":     "MARUTI.NS",
        "Tata Motors":       "TATAMOTORS.NS",
        "M&M":               "M&M.NS",
        "Hero MotoCorp":     "HEROMOTOCO.NS",
        "Bajaj Auto":        "BAJAJ-AUTO.NS",
        "Eicher Motors":     "EICHERMOT.NS",
        "Ashok Leyland":     "ASHOKLEY.NS",
        "TVS Motor":         "TVSMOTOR.NS",
        "Samvardhana M.":    "SAMVARDH.NS",
    },
    "── METALS & MINING ──": {
        "Tata Steel":        "TATASTEEL.NS",
        "JSW Steel":         "JSWSTEEL.NS",
        "Hindalco":          "HINDALCO.NS",
        "Vedanta":           "VEDL.NS",
        "SAIL":              "SAIL.NS",
        "NMDC":              "NMDC.NS",
        "Hindustan Zinc":    "HINDZINC.NS",
        "Jindal Steel":      "JINDALSTEL.NS",
    },
    "── PHARMA & HEALTHCARE ──": {
        "Sun Pharma":        "SUNPHARMA.NS",
        "Dr. Reddy's":       "DRREDDY.NS",
        "Cipla":             "CIPLA.NS",
        "Divi's Lab":        "DIVISLAB.NS",
        "Apollo Hospitals":  "APOLLOHOSP.NS",
        "Lupin":             "LUPIN.NS",
        "Aurobindo Pharma":  "AUROPHARMA.NS",
        "Biocon":            "BIOCON.NS",
        "Max Healthcare":    "MAXHEALTH.NS",
        "Fortis Health":     "FORTIS.NS",
    },
    "── FMCG & CONSUMER ──": {
        "Hindustan Unilever":"HINDUNILVR.NS",
        "ITC":               "ITC.NS",
        "Nestle India":      "NESTLEIND.NS",
        "Britannia":         "BRITANNIA.NS",
        "Dabur":             "DABUR.NS",
        "Godrej Consumer":   "GODREJCP.NS",
        "Marico":            "MARICO.NS",
        "Colgate-Palmolive": "COLPAL.NS",
        "Tata Consumer":     "TATACONSUM.NS",
        "Asian Paints":      "ASIANPAINT.NS",
        "Pidilite Ind.":     "PIDILITIND.NS",
    },
    "── INFRA & CONGLOMERATE ──": {
        "Larsen & Toubro":   "LT.NS",
        "Adani Enterp.":     "ADANIENT.NS",
        "Adani Ports":       "ADANIPORTS.NS",
        "DLF":               "DLF.NS",
        "Godrej Properties": "GODREJPROP.NS",
        "Prestige Estates":  "PRESTIGE.NS",
        "Oberoi Realty":     "OBEROIRLTY.NS",
        "UltraTech Cement":  "ULTRACEMCO.NS",
        "Shree Cement":      "SHREECEM.NS",
        "ACC":               "ACC.NS",
        "Ambuja Cements":    "AMBUJACEM.NS",
    },
    "── TELECOM & MEDIA ──": {
        "Bharti Airtel":     "BHARTIARTL.NS",
        "Vodafone Idea":     "IDEA.NS",
        "Tata Comm.":        "TATACOMM.NS",
        "Indus Towers":      "INDUSTOWER.NS",
        "Zee Entertainment": "ZEEL.NS",
        "Sun TV":            "SUNTV.NS",
    },
    "── E-COMMERCE & NEW AGE ──": {
        "Zomato":            "ZOMATO.NS",
        "Nykaa (FSN)":       "NYKAA.NS",
        "Paytm (One97)":     "PAYTM.NS",
        "PB Fintech":        "POLICYBZR.NS",
        "Delhivery":         "DELHIVERY.NS",
        "Nazara Tech":       "NAZARA.NS",
    },
    "── AVIATION & LOGISTICS ──": {
        "InterGlobe (IndiGo)":"INDIGO.NS",
        "SpiceJet":          "SPICEJET.NS",
        "Container Corp.":   "CONCOR.NS",
        "Blue Dart":         "BLUEDART.NS",
        "TCI Express":       "TCIEXP.NS",
    },
}

# Flat map for lookup
TICKER_MAP = {}
for sector, stocks in INDIAN_STOCKS.items():
    for name, ticker in stocks.items():
        TICKER_MAP[name] = ticker

IST = pytz.timezone("Asia/Kolkata")

# ─────────────────────────────────────────────
# MOBILE-FIRST CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg: #06090f;
    --surface: #0d1320;
    --border: #1a2840;
    --accent: #ff9933;
    --accent2: #138808;
    --blue: #000080;
    --green: #00e676;
    --red: #ff1744;
    --gold: #ffd600;
    --text: #e8f4fd;
    --muted: #5a7a99;
}

html, body, [data-testid="stApp"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

.stButton > button {
    background: linear-gradient(135deg, #ff993322, #ff993311) !important;
    border: 1px solid var(--accent) !important;
    color: var(--accent) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    padding: 14px 24px !important;
    border-radius: 8px !important;
    width: 100% !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #ff993344, #ff993322) !important;
    box-shadow: 0 0 20px #ff993333 !important;
}

.stSelectbox > div > div,
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 16px !important;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 8px;
    text-align: center;
    margin-bottom: 10px;
}
.metric-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 5px;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 700;
}

.signal-buy {
    background: linear-gradient(135deg, #00e67622, #00e67611);
    border: 2px solid var(--green);
    color: var(--green);
    border-radius: 10px;
    padding: 22px;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 30px;
    font-weight: 700;
    letter-spacing: 4px;
}
.signal-sell {
    background: linear-gradient(135deg, #ff174422, #ff174411);
    border: 2px solid var(--red);
    color: var(--red);
    border-radius: 10px;
    padding: 22px;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 30px;
    font-weight: 700;
    letter-spacing: 4px;
}
.signal-hold {
    background: linear-gradient(135deg, #ffd60022, #ffd60011);
    border: 2px solid var(--gold);
    color: var(--gold);
    border-radius: 10px;
    padding: 22px;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    font-size: 30px;
    font-weight: 700;
    letter-spacing: 4px;
}

.hero {
    text-align: center;
    padding: 20px 0 12px;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: var(--accent);
    margin: 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: var(--muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    margin-top: 4px;
}

.india-flag {
    font-size: 20px;
    margin-right: 6px;
}

.section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--muted);
    letter-spacing: 3px;
    text-transform: uppercase;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
    margin: 20px 0 14px;
}

.trade-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid var(--border);
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
}

.sector-badge {
    display: inline-block;
    background: #ff993315;
    border: 1px solid #ff993340;
    color: var(--accent);
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    letter-spacing: 1px;
    padding: 3px 8px;
    border-radius: 4px;
    margin-bottom: 12px;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 14px 80px !important;
    max-width: 480px !important;
    margin: auto !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TECHNICAL INDICATOR FUNCTIONS
# ─────────────────────────────────────────────

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / (loss + 1e-9)
    return 100 - (100 / (1 + rs))

def compute_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    sig = macd.ewm(span=signal, adjust=False).mean()
    return macd, sig, macd - sig

def compute_bb(series, period=20, std=2.0):
    mid = series.rolling(period).mean()
    sigma = series.rolling(period).std()
    return mid + std * sigma, mid, mid - std * sigma

def compute_vwap(df):
    cum_vol = df["Volume"].groupby(df.index.date).cumsum()
    cum_pv = (df["Close"] * df["Volume"]).groupby(df.index.date).cumsum()
    return cum_pv / (cum_vol + 1e-9)

def compute_atr(df, period=14):
    hl = df["High"] - df["Low"]
    hpc = (df["High"] - df["Close"].shift(1)).abs()
    lpc = (df["Low"] - df["Close"].shift(1)).abs()
    tr = pd.concat([hl, hpc, lpc], axis=1).max(axis=1)
    return tr.ewm(span=period, adjust=False).mean()


# ─────────────────────────────────────────────
# VADER SENTIMENT (Indian news)
# ─────────────────────────────────────────────

def vader_sentiment(ticker):
    try:
        from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
        analyzer = SentimentIntensityAnalyzer()
        stock = yf.Ticker(ticker)
        news = stock.news or []
        headlines = [item.get("title", "") for item in news[:10] if item.get("title")]
        if not headlines:
            return 0.0, 0
        scores = [analyzer.polarity_scores(h)["compound"] for h in headlines]
        return round(float(np.mean(scores)), 3), len(scores)
    except Exception:
        return 0.0, 0


# ─────────────────────────────────────────────
# DATA PIPELINE — NSE/BSE + IST timezone
# ─────────────────────────────────────────────

@st.cache_data(ttl=300)
def load_and_process(ticker, interval):
    try:
        df = yf.download(ticker, period="5d", interval=interval,
                         auto_adjust=True, progress=False)

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
        df.dropna(inplace=True)

        if df.empty:
            return None

        # Convert to IST
        if df.index.tz is not None:
            df.index = df.index.tz_convert(IST)
        else:
            df.index = df.index.tz_localize("UTC").tz_convert(IST)

        # NSE session: 09:15 – 15:30 IST
        df = df.between_time("09:15", "15:30")

        if len(df) < 30:
            return None

        c = df["Close"]
        o, h, l, v = df["Open"], df["High"], df["Low"], df["Volume"]

        # RSI
        df["RSI"] = compute_rsi(c)

        # MACD
        df["MACD"], df["MACD_sig"], df["MACD_hist"] = compute_macd(c)
        df["MACD_cross_up"] = ((df["MACD"] > df["MACD_sig"]) &
                                (df["MACD"].shift(1) <= df["MACD_sig"].shift(1))).astype(int)
        df["MACD_cross_dn"] = ((df["MACD"] < df["MACD_sig"]) &
                                (df["MACD"].shift(1) >= df["MACD_sig"].shift(1))).astype(int)

        # Bollinger Bands
        df["BB_upper"], df["BB_mid"], df["BB_lower"] = compute_bb(c)
        df["BB_pct_b"] = (c - df["BB_lower"]) / (df["BB_upper"] - df["BB_lower"] + 1e-9)
        df["BB_width"] = (df["BB_upper"] - df["BB_lower"]) / (df["BB_mid"] + 1e-9)

        # EMAs
        for s in [9, 21, 50]:
            df[f"EMA_{s}"] = c.ewm(span=s, adjust=False).mean()
        df["EMA_bull"] = ((df["EMA_9"] > df["EMA_21"]) & (df["EMA_21"] > df["EMA_50"])).astype(int)
        df["EMA_bear"] = ((df["EMA_9"] < df["EMA_21"]) & (df["EMA_21"] < df["EMA_50"])).astype(int)

        # ATR
        df["ATR"] = compute_atr(df)
        df["ATR_pct"] = df["ATR"] / c

        # Stochastic
        ln = l.rolling(14).min(); hx = h.rolling(14).max()
        df["Stoch_K"] = 100 * (c - ln) / (hx - ln + 1e-9)
        df["Stoch_D"] = df["Stoch_K"].rolling(3).mean()

        # VWAP
        df["VWAP"] = compute_vwap(df)
        df["Price_vs_VWAP"] = (c - df["VWAP"]) / (df["VWAP"] + 1e-9)

        # OBV
        obv = [0]
        for i in range(1, len(df)):
            obv.append(obv[-1] + v.iloc[i] if c.iloc[i] > c.iloc[i-1]
                       else obv[-1] - v.iloc[i] if c.iloc[i] < c.iloc[i-1]
                       else obv[-1])
        df["OBV"] = obv
        df["OBV_slope"] = pd.Series(obv, index=df.index).diff(3)

        # Volume
        df["Vol_ratio"] = v / (v.rolling(20).mean() + 1e-9)
        df["Buy_pressure"] = (c - l) / (h - l + 1e-9)
        df["Sell_pressure"] = (h - c) / (h - l + 1e-9)

        # CMF
        mfm = ((c - l) - (h - c)) / (h - l + 1e-9)
        df["CMF"] = (mfm * v).rolling(20).sum() / (v.rolling(20).sum() + 1e-9)

        # Candlestick patterns
        body = (c - o).abs()
        uw = h - pd.concat([c, o], axis=1).max(axis=1)
        lw = pd.concat([c, o], axis=1).min(axis=1) - l
        df["Bull_Engulf"] = ((c > o) & (c.shift(1) < o.shift(1)) &
                              (c > o.shift(1)) & (o < c.shift(1))).astype(int)
        df["Bear_Engulf"] = ((c < o) & (c.shift(1) > o.shift(1)) &
                              (c < o.shift(1)) & (o > c.shift(1))).astype(int)
        df["Hammer"] = ((lw >= 2 * body) & (uw <= 0.3 * body) & (c > o)).astype(int)
        df["Shooting_Star"] = ((uw >= 2 * body) & (lw <= 0.3 * body) & (c < o)).astype(int)
        df["Doji"] = (body < 0.1 * (h - l)).astype(int)
        df["Body_ratio"] = body / (h - l + 1e-9)
        df["Candle_dir"] = np.sign(c - o)

        # Returns & volatility
        for lag in [1, 2, 3, 5]:
            df[f"Ret_{lag}"] = c.pct_change(lag)
        df["Volatility"] = df["Ret_1"].rolling(10).std()
        df["Gap"] = (o - c.shift(1)) / (c.shift(1) + 1e-9)

        # Time features (IST)
        df["Hour"] = df.index.hour
        df["Minute"] = df.index.minute
        total_min = df["Hour"] * 60 + df["Minute"]
        df["Time_sin"] = np.sin(2 * np.pi * (total_min - 555) / 375)  # 9:15–15:30 = 375 min
        df["Time_cos"] = np.cos(2 * np.pi * (total_min - 555) / 375)

        df.dropna(inplace=True)
        return df

    except Exception as e:
        st.error(f"Data error: {e}")
        return None


# ─────────────────────────────────────────────
# SIGNAL ENGINE
# ─────────────────────────────────────────────

def generate_signal(df, sentiment_score=0.0):
    latest = df.iloc[-1]
    score = 0
    breakdown = {}

    # RSI
    rsi = latest.get("RSI", 50)
    if rsi < 30:       s, label = 3, f"Strongly oversold ({rsi:.0f})"
    elif rsi < 40:     s, label = 2, f"Oversold ({rsi:.0f})"
    elif rsi < 48:     s, label = 1, f"Mild oversold ({rsi:.0f})"
    elif rsi > 70:     s, label = -3, f"Strongly overbought ({rsi:.0f})"
    elif rsi > 62:     s, label = -2, f"Overbought ({rsi:.0f})"
    elif rsi > 55:     s, label = -1, f"Mild overbought ({rsi:.0f})"
    else:              s, label = 0, f"Neutral ({rsi:.0f})"
    score += s; breakdown["RSI"] = (s, label)

    # MACD
    if latest.get("MACD_cross_up"):    s, label = 3, "Bullish crossover ✓"
    elif latest.get("MACD_hist", 0) > 0: s, label = 1, f"Positive hist ({latest.get('MACD_hist',0):.3f})"
    elif latest.get("MACD_cross_dn"):  s, label = -3, "Bearish crossover ✗"
    else:                              s, label = -1, f"Negative hist ({latest.get('MACD_hist',0):.3f})"
    score += s; breakdown["MACD"] = (s, label)

    # Bollinger Bands
    bb = latest.get("BB_pct_b", 0.5)
    if bb < 0.05:      s, label = 3, f"Below lower band ({bb:.2f})"
    elif bb < 0.25:    s, label = 2, f"Lower zone ({bb:.2f})"
    elif bb < 0.4:     s, label = 1, f"Lower-mid ({bb:.2f})"
    elif bb > 0.95:    s, label = -3, f"Above upper band ({bb:.2f})"
    elif bb > 0.75:    s, label = -2, f"Upper zone ({bb:.2f})"
    elif bb > 0.6:     s, label = -1, f"Upper-mid ({bb:.2f})"
    else:              s, label = 0, f"Mid band ({bb:.2f})"
    score += s; breakdown["Bollinger"] = (s, label)

    # EMA trend
    if latest.get("EMA_bull"):     s, label = 2, "Bullish 9>21>50 ✓"
    elif latest.get("EMA_bear"):   s, label = -2, "Bearish 9<21<50 ✗"
    else:                          s, label = 0, "Mixed structure"
    score += s; breakdown["EMA Trend"] = (s, label)

    # Stochastic
    stk = latest.get("Stoch_K", 50)
    std = latest.get("Stoch_D", 50)
    if stk < 20 and stk > std:    s, label = 2, f"Oversold + bullish ({stk:.0f})"
    elif stk < 20:                 s, label = 1, f"Oversold ({stk:.0f})"
    elif stk > 80 and stk < std:  s, label = -2, f"Overbought + bearish ({stk:.0f})"
    elif stk > 80:                 s, label = -1, f"Overbought ({stk:.0f})"
    else:                          s, label = 0, f"Normal ({stk:.0f})"
    score += s; breakdown["Stochastic"] = (s, label)

    # VWAP
    pvwap = latest.get("Price_vs_VWAP", 0)
    if pvwap > 0.008:              s, label = 2, f"Above VWAP (+{pvwap*100:.2f}%)"
    elif pvwap > 0.002:            s, label = 1, f"Slightly above VWAP"
    elif pvwap < -0.008:           s, label = -2, f"Below VWAP ({pvwap*100:.2f}%)"
    elif pvwap < -0.002:           s, label = -1, f"Slightly below VWAP"
    else:                          s, label = 0, "At VWAP"
    score += s; breakdown["VWAP"] = (s, label)

    # CMF
    cmf = latest.get("CMF", 0)
    if cmf > 0.15:     s, label = 2, f"Strong buying flow ({cmf:.2f})"
    elif cmf > 0.05:   s, label = 1, f"Mild buying ({cmf:.2f})"
    elif cmf < -0.15:  s, label = -2, f"Strong selling flow ({cmf:.2f})"
    elif cmf < -0.05:  s, label = -1, f"Mild selling ({cmf:.2f})"
    else:              s, label = 0, f"Neutral flow ({cmf:.2f})"
    score += s; breakdown["CMF"] = (s, label)

    # Volume
    vr = latest.get("Vol_ratio", 1.0)
    if vr > 2.5:   s, label = 1 if score > 0 else -1, f"Vol spike {vr:.1f}x"
    elif vr > 1.5: s, label = 0, f"Above avg ({vr:.1f}x)"
    else:          s, label = -1, f"Low volume ({vr:.1f}x)"
    score += s; breakdown["Volume"] = (s, label)

    # OBV slope
    obv_slope = latest.get("OBV_slope", 0)
    if obv_slope > 0:  s, label = 1, "OBV rising ↑"
    elif obv_slope < 0: s, label = -1, "OBV falling ↓"
    else:              s, label = 0, "OBV flat"
    score += s; breakdown["OBV"] = (s, label)

    # Sentiment
    if sentiment_score > 0.25:    s, label = 2, f"Very positive ({sentiment_score:+.2f})"
    elif sentiment_score > 0.1:   s, label = 1, f"Positive ({sentiment_score:+.2f})"
    elif sentiment_score < -0.25: s, label = -2, f"Very negative ({sentiment_score:+.2f})"
    elif sentiment_score < -0.1:  s, label = -1, f"Negative ({sentiment_score:+.2f})"
    else:                         s, label = 0, f"Neutral ({sentiment_score:+.2f})"
    score += s; breakdown["Sentiment"] = (s, label)

    # Candlestick
    if latest.get("Bull_Engulf"):    s, label = 2, "Bullish Engulfing 🕯"
    elif latest.get("Hammer"):       s, label = 2, "Hammer 🔨"
    elif latest.get("Bear_Engulf"):  s, label = -2, "Bearish Engulfing 🕯"
    elif latest.get("Shooting_Star"): s, label = -2, "Shooting Star ⭐"
    elif latest.get("Doji"):         s, label = 0, "Doji — indecision"
    else:                            s, label = 0, "No pattern"
    score += s; breakdown["Candle"] = (s, label)

    # NSE session time filter
    hour = int(latest.get("Hour", 12))
    minute = int(latest.get("Minute", 0))
    total_min = hour * 60 + minute
    in_prime = 9 * 60 + 30 <= total_min <= 15 * 60 + 15
    breakdown["Session"] = (1 if in_prime else -1,
                             "Prime hours ✓" if in_prime else "Outside prime hours ✗")

    max_score = 22
    norm = score / max_score
    signal = "BUY" if norm > 0.2 else "SELL" if norm < -0.2 else "HOLD"
    confidence = min(abs(norm) * 100, 100)
    return signal, round(confidence, 1), score, breakdown


# ─────────────────────────────────────────────
# BACKTEST
# ─────────────────────────────────────────────

def mini_backtest(df, sentiment=0.0):
    capital = 100_000.0   # ₹1 lakh starting capital
    equity = [capital]
    trades = []
    position = None

    for i in range(50, len(df)):
        window = df.iloc[:i]
        price = float(df["Close"].iloc[i])
        sig, conf, _, _ = generate_signal(window, sentiment)

        if position is None and sig == "BUY" and conf > 35:
            shares = int((capital * 0.90) / price)
            if shares > 0:
                position = {"shares": shares, "entry": price,
                            "sl": price * 0.995, "tp": price * 1.015}

        elif position:
            if price <= position["sl"]:
                pnl = (price - position["entry"]) * position["shares"]
                capital += pnl
                trades.append({"pnl": pnl, "reason": "SL"})
                position = None
            elif price >= position["tp"]:
                pnl = (price - position["entry"]) * position["shares"]
                capital += pnl
                trades.append({"pnl": pnl, "reason": "TP"})
                position = None

        equity.append(capital)

    if position:
        last = float(df["Close"].iloc[-1])
        pnl = (last - position["entry"]) * position["shares"]
        capital += pnl
        trades.append({"pnl": pnl, "reason": "EOD"})

    return trades, equity


# ─────────────────────────────────────────────
# HELPER — find sector for a stock name
# ─────────────────────────────────────────────

def get_sector(stock_name):
    for sector, stocks in INDIAN_STOCKS.items():
        if stock_name in stocks:
            return sector.replace("── ", "").replace(" ──", "")
    return "Indian Market"


# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────

# Hero
now_ist = datetime.now(IST)
market_open = (now_ist.weekday() < 5 and
               (9 * 60 + 15) <= (now_ist.hour * 60 + now_ist.minute) <= (15 * 60 + 30))
market_status = "🟢 MARKET OPEN" if market_open else "🔴 MARKET CLOSED"

st.markdown(f"""
<div class="hero">
    <h1>🇮🇳 AI TRADER</h1>
    <p>NSE · BSE · INTRADAY · IST</p>
    <p style="color:{'#00e676' if market_open else '#ff1744'};margin-top:6px;font-size:10px">{market_status}</p>
</div>
""", unsafe_allow_html=True)

# ── SECTOR + STOCK SELECTOR
st.markdown('<div class="section-title">Select Stock</div>', unsafe_allow_html=True)

sector_names = [s for s in INDIAN_STOCKS.keys()]
selected_sector = st.selectbox("Sector", sector_names, index=0)

stock_options = list(INDIAN_STOCKS[selected_sector].keys())
selected_stock = st.selectbox("Stock", stock_options, index=0)
ticker = INDIAN_STOCKS[selected_sector][selected_stock]

col1, col2 = st.columns(2)
with col1:
    interval = st.selectbox("Interval", ["5m", "15m", "1h"], index=0)
with col2:
    st.markdown(f"""
    <div style="margin-top:28px;font-family:'JetBrains Mono',monospace;
    font-size:10px;color:#5a7a99;text-align:center">
        {ticker}
    </div>""", unsafe_allow_html=True)

run = st.button("🔍 ANALYSE NOW")

if run:
    with st.spinner(f"Fetching {selected_stock} data..."):
        df = load_and_process(ticker, interval)
        sentiment_score, n_articles = vader_sentiment(ticker)
        st.session_state.update({
            "df": df, "sentiment": sentiment_score,
            "n_articles": n_articles, "ticker": ticker,
            "stock_name": selected_stock, "sector": selected_sector
        })

if "df" in st.session_state and st.session_state.get("ticker") == ticker:
    df = st.session_state["df"]
    sentiment_score = st.session_state.get("sentiment", 0.0)
    n_articles = st.session_state.get("n_articles", 0)
    stock_name = st.session_state.get("stock_name", selected_stock)
    sector = st.session_state.get("sector", "")

    if df is None or len(df) < 30:
        st.error("⚠️ Not enough intraday data. Try 15m or 1h interval, or a different stock.")
        st.stop()

    signal, confidence, raw_score, breakdown = generate_signal(df, sentiment_score)
    latest = df.iloc[-1]
    price = float(latest["Close"])
    atr = float(latest["ATR"])
    prev_close = float(df["Close"].iloc[-2])
    change = (price - prev_close) / prev_close * 100

    # Sector badge
    sector_clean = sector.replace("── ", "").replace(" ──", "")
    st.markdown(f'<span class="sector-badge">{sector_clean}</span>', unsafe_allow_html=True)

    # ── SIGNAL
    st.markdown('<div class="section-title">Current Signal</div>', unsafe_allow_html=True)
    badge_class = f"signal-{'buy' if signal=='BUY' else 'sell' if signal=='SELL' else 'hold'}"
    icon = "🟢" if signal == "BUY" else "🔴" if signal == "SELL" else "🟡"
    sub = "ENTER LONG" if signal=="BUY" else "EXIT / SHORT" if signal=="SELL" else "WAIT"
    st.markdown(f"""
    <div class="{badge_class}">
        {icon} {signal}
        <div style="font-size:12px;letter-spacing:2px;margin-top:6px;opacity:0.7">{sub}</div>
    </div>""", unsafe_allow_html=True)

    # ── PRICE SNAPSHOT
    st.markdown('<div class="section-title">Market Snapshot</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        color = "#00e676" if change >= 0 else "#ff1744"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">LTP</div>
            <div class="metric-value" style="color:{color}">₹{price:,.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        color = "#00e676" if change >= 0 else "#ff1744"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Change</div>
            <div class="metric-value" style="color:{color}">{change:+.2f}%</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Confidence</div>
            <div class="metric-value" style="color:#ff9933">{confidence:.0f}%</div>
        </div>""", unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    rsi_val = float(latest.get("RSI", 50))
    with c4:
        rsi_color = "#ff1744" if rsi_val > 70 else "#00e676" if rsi_val < 30 else "#e8f4fd"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">RSI</div>
            <div class="metric-value" style="color:{rsi_color}">{rsi_val:.1f}</div>
        </div>""", unsafe_allow_html=True)
    with c5:
        sc = sentiment_score
        sent_color = "#00e676" if sc > 0.1 else "#ff1744" if sc < -0.1 else "#ffd600"
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Sentiment</div>
            <div class="metric-value" style="color:{sent_color}">{sc:+.2f}</div>
        </div>""", unsafe_allow_html=True)
    with c6:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">ATR</div>
            <div class="metric-value" style="color:#e8f4fd">₹{atr:.2f}</div>
        </div>""", unsafe_allow_html=True)

    # ── RISK LEVELS
    if signal in ("BUY", "SELL"):
        st.markdown('<div class="section-title">Risk Levels (0.5% SL · 1.5% TP)</div>', unsafe_allow_html=True)
        if signal == "BUY":
            sl = price * 0.995; tp = price * 1.015
        else:
            sl = price * 1.005; tp = price * 0.985

        lot_size = max(1, int(10000 / price))  # approx 1 lot at ₹10k risk
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Stop Loss</div>
                <div class="metric-value" style="color:#ff1744">₹{sl:,.2f}</div>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Take Profit</div>
                <div class="metric-value" style="color:#00e676">₹{tp:,.2f}</div>
            </div>""", unsafe_allow_html=True)

        risk_amt = (price - sl) * lot_size if signal == "BUY" else (sl - price) * lot_size
        reward_amt = (tp - price) * lot_size if signal == "BUY" else (price - tp) * lot_size
        st.markdown(f"""
        <div style="background:#0d1320;border:1px solid #1a2840;border-radius:8px;
        padding:10px 14px;font-family:'JetBrains Mono',monospace;font-size:11px;
        color:#5a7a99;text-align:center;margin-bottom:8px">
            Qty: {lot_size} shares &nbsp;·&nbsp;
            Risk: ₹{risk_amt:.0f} &nbsp;·&nbsp;
            Reward: ₹{reward_amt:.0f} &nbsp;·&nbsp;
            R:R = 1:3
        </div>""", unsafe_allow_html=True)

    # ── SIGNAL BREAKDOWN
    st.markdown('<div class="section-title">Signal Breakdown</div>', unsafe_allow_html=True)
    for factor, (s, label) in breakdown.items():
        color = "#00e676" if s > 0 else "#ff1744" if s < 0 else "#5a7a99"
        arrow = "▲" if s > 0 else "▼" if s < 0 else "●"
        pts = f"+{s}" if s > 0 else str(s)
        st.markdown(f"""
        <div class="trade-row">
            <span style="color:#e8f4fd">{factor}</span>
            <span style="color:{color};font-size:11px">{arrow} {label}
                <span style="color:{color};opacity:0.6;margin-left:6px">({pts})</span>
            </span>
        </div>""", unsafe_allow_html=True)

    total_pts = sum(s for s, _ in breakdown.values())
    st.markdown(f"""
    <div style="text-align:right;font-family:'JetBrains Mono',monospace;
    font-size:11px;color:#5a7a99;margin-top:8px">
        Total score: {total_pts:+d} / 22
    </div>""", unsafe_allow_html=True)

    # ── PRICE CHART
    st.markdown('<div class="section-title">Price Chart (last 60 bars)</div>', unsafe_allow_html=True)
    chart_df = df[["Close", "EMA_9", "EMA_21", "BB_upper", "BB_lower"]].tail(60).copy()
    chart_df.columns = ["Close", "EMA 9", "EMA 21", "BB Upper", "BB Lower"]
    st.line_chart(chart_df, use_container_width=True, height=220)

    # ── BACKTEST
    st.markdown('<div class="section-title">Quick Backtest (₹1L capital)</div>', unsafe_allow_html=True)
    with st.spinner("Running backtest..."):
        trades, equity_curve = mini_backtest(df, sentiment_score)

    if trades:
        wins = [t for t in trades if t["pnl"] > 0]
        total_pnl = sum(t["pnl"] for t in trades)
        win_rate = len(wins) / len(trades) * 100
        max_dd = min(0, min(e - max(equity_curve[:i+1]) for i, e in enumerate(equity_curve)))

        b1, b2, b3 = st.columns(3)
        with b1:
            pnl_color = "#00e676" if total_pnl >= 0 else "#ff1744"
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">P&L</div>
                <div class="metric-value" style="color:{pnl_color}">₹{total_pnl:+,.0f}</div>
            </div>""", unsafe_allow_html=True)
        with b2:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Win Rate</div>
                <div class="metric-value" style="color:#ff9933">{win_rate:.0f}%</div>
            </div>""", unsafe_allow_html=True)
        with b3:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-label">Trades</div>
                <div class="metric-value" style="color:#e8f4fd">{len(trades)}</div>
            </div>""", unsafe_allow_html=True)

        eq_series = pd.Series(equity_curve, name="Equity (₹)")
        st.line_chart(eq_series, use_container_width=True, height=180)

        st.markdown('<div class="section-title">Trade Log</div>', unsafe_allow_html=True)
        for i, t in enumerate(trades[-10:]):
            color = "#00e676" if t["pnl"] > 0 else "#ff1744"
            icon = "✅" if t["pnl"] > 0 else "❌"
            st.markdown(f"""
            <div class="trade-row">
                <span style="color:#5a7a99">#{i+1} · {t['reason']}</span>
                <span style="color:{color}">{icon} ₹{t['pnl']:+,.0f}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.info("No completed trades in this window. Try 15m or 1h interval.")

    # ── FOOTER
    st.markdown(f"""
    <div style="margin-top:28px;padding:14px;background:#0d1320;border:1px solid #1a2840;
    border-radius:8px;font-family:'JetBrains Mono',monospace;font-size:10px;
    color:#5a7a99;text-align:center;line-height:1.8">
        📰 {n_articles} news headlines · Sentiment: {sentiment_score:+.3f}<br>
        🕐 IST {now_ist.strftime('%d %b %Y  %H:%M:%S')}<br>
        ⚠️ For educational purposes only. Not financial advice.
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center;padding:40px 20px;color:#5a7a99;
    font-family:'JetBrains Mono',monospace;font-size:12px;line-height:2.2">
        🇮🇳 Select a sector and stock<br>
        then tap <b style="color:#ff9933">ANALYSE NOW</b><br><br>
        <span style="font-size:10px;opacity:0.7">
        70+ Indian stocks · NSE/BSE<br>
        RSI · MACD · BB · EMA · VWAP<br>
        CMF · OBV · Stochastic<br>
        Candlesticks · VADER Sentiment
        </span>
    </div>
    """, unsafe_allow_html=True)
