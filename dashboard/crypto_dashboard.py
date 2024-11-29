"""Streamlined Crypto Trading Dashboard."""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
from typing import Dict, Any
import os

# Configuration and settings
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_latest_data() -> Dict[str, Any]:
    """Load the latest processed data file."""
    try:
        data_file = os.path.join(PROCESSED_DIR, 'trend_analysis.json')
        if not os.path.exists(data_file):
            return None
        
        with open(data_file, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def display_sentiment_overview(data: Dict[str, Any]):
    """Display sentiment overview metrics."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Total Analyzed Tweets",
            data.get('total_tweets', 0),
            delta=None
        )
    
    with col2:
        sentiment = data.get('average_sentiment', 0)
        st.metric(
            "Average Sentiment",
            f"{sentiment:.2%}",
            delta=None
        )

def display_crypto_mentions(data: Dict[str, Any]):
    """Display cryptocurrency mentions and metrics."""
    st.subheader("📊 Cryptocurrency Mentions")
    
    if not data.get('crypto_mentions'):
        st.info("No cryptocurrency mentions data available")
        return
    
    # Convert to DataFrame for easier manipulation
    mentions_data = []
    for coin, stats in data['crypto_mentions'].items():
        mentions_data.append({
            'Coin': coin,
            'Mentions': stats['mentions'],
            'Sentiment': stats['avg_sentiment'],
            'Engagement': stats['total_engagement']
        })
    
    df = pd.DataFrame(mentions_data)
    
    if not df.empty:
        # Create bar chart for mentions
        fig = px.bar(
            df,
            x='Coin',
            y='Mentions',
            color='Sentiment',
            title='Cryptocurrency Mentions with Sentiment',
            color_continuous_scale='RdYlGn'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display metrics table
        st.dataframe(
            df.sort_values('Mentions', ascending=False),
            hide_index=True
        )
    else:
        st.info("No data to display")

def display_trading_signals(data: Dict[str, Any]):
    """Display trading signals if available."""
    st.subheader("🎯 Trading Signals")
    
    signals = data.get('trading_signals', [])
    if not signals:
        st.info("No trading signals available for the current timeframe")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(signals)
    if not df.empty:
        # Create signal strength visualization
        fig = go.Figure()
        
        for idx, signal in enumerate(signals):
            color = 'green' if signal.get('signal_strength', 0) > 0 else 'red'
            fig.add_trace(go.Bar(
                x=[signal.get('coin', '')],
                y=[signal.get('signal_strength', 0)],
                name=signal.get('signal_type', 'NEUTRAL'),
                marker_color=color,
                text=f"{signal.get('confidence', 0):.2%}",
                textposition='auto',
            ))
        
        fig.update_layout(
            title="Signal Strength by Coin",
            yaxis_title="Signal Strength",
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display signal details
        st.dataframe(
            df[['coin', 'signal_type', 'signal_strength', 'confidence']],
            hide_index=True
        )

def main():
    """Main dashboard application."""
    st.set_page_config(
        page_title="Crypto Trading Signals",
        page_icon="📈",
        layout="wide"
    )
    
    st.title("📈 Crypto Trading Signals Dashboard")
    
    # Load data
    data = load_latest_data()
    
    if data is None:
        st.error("No data available. Please run the data processing pipeline first.")
        return
    
    # Display last update time
    st.sidebar.write("Last Updated:", data.get('timestamp', 'Unknown'))
    
    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Overview", "Mentions", "Signals"])
    
    with tab1:
        display_sentiment_overview(data)
    
    with tab2:
        display_crypto_mentions(data)
    
    with tab3:
        display_trading_signals(data)

if __name__ == "__main__":
    main()
