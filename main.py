import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_mock_trend_data, calculate_trend_metrics
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Fashion Trend Analysis",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header section
st.markdown('<h1 class="main-title">FASHION TREND ANALYSIS</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the Future of Fashion Through Data</p>', unsafe_allow_html=True)

# Layout columns for header images
col1, col2 = st.columns(2)
with col1:
    st.image("https://images.unsplash.com/photo-1571924849183-a68a3879348d", use_container_width=True)
with col2:
    st.image("https://images.unsplash.com/photo-1543617648-16c14553d5e8", use_container_width=True)

# Generate and process data
df = generate_mock_trend_data()
metrics_df = calculate_trend_metrics(df)

# Trend Metrics Section
st.markdown("### Key Trend Metrics")
metric_cols = st.columns(4)
for idx, row in metrics_df.head(4).iterrows():
    with metric_cols[idx]:
        st.markdown(f'<div class="trend-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">{row["avg_engagement"]:,}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-label">{row["trend"]}</div>', unsafe_allow_html=True)
        st.markdown(f'Growth: {row["growth_rate"]}%', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# Trend Visualization Section
st.markdown("### Trend Evolution")
selected_trends = st.multiselect(
    "Select trends to compare",
    options=df['trend'].unique(),
    default=df['trend'].unique()[:3]
)

# Time series plot
filtered_df = df[df['trend'].isin(selected_trends)]
fig = px.line(filtered_df, 
              x='date', 
              y='engagement',
              color='trend',
              template='plotly_white')
fig.update_layout(
    plot_bgcolor='rgba(255, 255, 255, 0.7)',
    paper_bgcolor='rgba(255, 255, 255, 0)',
    font_family='Space Grotesk',
    height=500,
    margin=dict(t=30, r=20, b=30, l=20),
    hovermode='x unified',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.7)'
    )
)
fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)

# Trend Cards Section
st.markdown("### Trending Now")
trend_cols = st.columns(3)
trend_images = [
    "https://images.unsplash.com/photo-1520006403909-838d6b92c22e",
    "https://images.unsplash.com/photo-1519748771451-a94c596fad67",
    "https://images.unsplash.com/photo-1493655161922-ef98929de9d8"
]

for idx, (col, img) in enumerate(zip(trend_cols, trend_images)):
    with col:
        st.markdown(f'<div class="trend-card">', unsafe_allow_html=True)
        st.image(img, use_container_width=True)
        trend_data = metrics_df.iloc[idx]
        st.markdown(f"#### {trend_data['trend']}")
        st.markdown(f"Engagement: {trend_data['avg_engagement']:,}")
        st.markdown(f"Sentiment: {trend_data['avg_sentiment']:.2f}")
        st.markdown('</div>', unsafe_allow_html=True)

# Sentiment Analysis Section
st.markdown("### Sentiment Analysis")
fig_sentiment = px.bar(
    metrics_df,
    x='trend',
    y='avg_sentiment',
    color='avg_sentiment',
    color_continuous_scale='blues',
    template='plotly_white'
)
fig_sentiment.update_layout(
    plot_bgcolor='rgba(255, 255, 255, 0.7)',
    paper_bgcolor='rgba(255, 255, 255, 0)',
    font_family='Space Grotesk',
    height=400,
    margin=dict(t=30, r=20, b=30, l=20),
    hoverlabel=dict(
        bgcolor='rgba(255, 255, 255, 0.7)',
        font_size=14
    )
)
st.plotly_chart(fig_sentiment, use_container_width=True)

# Footer
st.markdown("---")
st.markdown('<p class="subtitle">Powered by Advanced Fashion Analytics</p>', unsafe_allow_html=True)