import streamlit as st
import yfinance as yf
import pandas as pd
import ta
import numpy as np

st.set_page_config(page_title="Nifty AI Live Monitor", layout="wide")
st.title("🌐 NIFTY 50 AI Live Monitor")

try:
    # 1. நிஃப்டி லைவ் விலை தரவுகளை எடுத்தல்
    nifty = yf.Ticker("^NSEI")
    hist = nifty.history(period="5d", interval="5m")
    spot_price = hist['Close'].iloc[-1]
    prev_close = hist['Close'].iloc[-2]
    change = spot_price - prev_close
    percent_change = (change / prev_close) * 100
    
    # மெட்ரிக் கார்டு டிசைன்
    st.metric("📊 Nifty 50 Live Spot Price", f"₹{spot_price:,.2f}", f"{change:+,.2f} ({percent_change:+.2f}%)")
    
    # 2. இண்டிகேட்டர்கள் கணக்கீடு (EMA 9 & RSI)
    hist['EMA9'] = ta.trend.ema_indicator(hist['Close'], window=9)
    hist['RSI'] = ta.momentum.rsi(hist['Close'], window=14)
    
    latest_ema = hist['EMA9'].iloc[-1]
    latest_rsi = hist['RSI'].iloc[-1]
    
    st.subheader("⚡ Technical Indicators & Option Data Check")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📊 Option Open Interest (OI) Summary")
        # லைவ் ஓபன் இன்ட்ரெஸ்ட் மாதிரி தரவு (உதாரணத்திற்கு 23400 ஸ்ட்ரைக்)
        call_oi, put_oi = 4500000, 6800000
        st.write(f"📈 **Call OI:** {call_oi:,} | 📊 **Put OI:** {put_oi:,}")
        
        higher_oi = "PUT (PE) பக்கம் அதிகம் ➔ (சந்தை சப்போர்ட் வலுவாக உள்ளது)" if put_oi > call_oi else "CALL (CE) பக்கம் அதிகம்"
        st.success(f"🌟 **OI Verdict:** {higher_oi}")
        
    with col2:
        st.warning("📈 Indicators Logic Status")
        ema_status = "🟢 Bullish (விலை EMA-க்கு மேலே உள்ளது)" if spot_price > latest_ema else "🩸 Bearish"
        st.write(f"🔹 **EMA 9:** ₹{latest_ema:,.2f} ➔ {ema_status}")
        
        rsi_status = "🟡 Neutral"
        if latest_rsi > 70: rsi_status = "🔴 Overbought (அதிகப்படியாக வாங்கப்பட்டுள்ளது)"
        elif latest_rsi < 30: rsi_status = "🟢 Oversold"
        st.write(f"🔹 **RSI (14):** {latest_rsi:.2f} ➔ {rsi_status}")

except Exception as e:
    st.error(f"டேட்டா புதுப்பிப்பதில் சிறு சிக்கல்: {e}")
