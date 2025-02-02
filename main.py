import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_mock_trend_data, calculate_trend_metrics
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Fashion Trend Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Fashion Analytics Dashboard</h1>', unsafe_allow_html=True)

# Generate and process data
df = generate_mock_trend_data()
metrics_df = calculate_trend_metrics(df)

# Top metrics section
st.markdown('<div class="section-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Total Engagement</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{metrics_df["avg_engagement"].sum():,}</div>', unsafe_allow_html=True)
    st.markdown('<div class="trend-percentage">+12.5%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Active Trends</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{len(metrics_df)}</div>', unsafe_allow_html=True)
    st.markdown('<div class="trend-percentage">+3.2%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Average Sentiment</div>', unsafe_allow_html=True)
    avg_sentiment = metrics_df['avg_sentiment'].mean()
    st.markdown(f'<div class="metric-value">{avg_sentiment:.2f}</div>', unsafe_allow_html=True)
    st.markdown('<div class="trend-percentage">+5.8%</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Trend Evolution Chart
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Trend Evolution</div>', unsafe_allow_html=True)

selected_trends = st.multiselect(
    "Select trends to compare",
    options=df['trend'].unique(),
    default=df['trend'].unique()[:3]
)

filtered_df = df[df['trend'].isin(selected_trends)]
fig = px.line(filtered_df,
              x='date',
              y='engagement',
              color='trend',
              template='plotly_dark')

fig.update_layout(
    plot_bgcolor='rgba(14, 17, 23, 0.7)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font_family='Outfit',
    font_color='#FFFFFF',
    height=400,
    margin=dict(t=30, r=20, b=30, l=20),
    hovermode='x unified',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(14, 17, 23, 0.7)'
    )
)
fig.update_traces(line=dict(width=3))

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Trend Performance Grid
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Trend Performance</div>', unsafe_allow_html=True)

for i in range(0, len(metrics_df), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(metrics_df):
            trend_data = metrics_df.iloc[i + j]
            with col:
                st.markdown(f'<div class="metric-label">{trend_data["trend"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{trend_data["avg_engagement"]:,}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="trend-percentage">+{trend_data["growth_rate"]}%</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sentiment Analysis
st.markdown('<div class="section-container">', unsafe_allow_html=True)
st.markdown('<div class="metric-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Sentiment Analysis</div>', unsafe_allow_html=True)

fig_sentiment = go.Figure(data=[
    go.Bar(
        x=metrics_df['trend'],
        y=metrics_df['avg_sentiment'],
        marker_color='#0066FF',
        opacity=0.8
    )
])

fig_sentiment.update_layout(
    plot_bgcolor='rgba(14, 17, 23, 0.7)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font_family='Outfit',
    font_color='#FFFFFF',
    height=400,
    margin=dict(t=30, r=20, b=30, l=20),
    showlegend=False,
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='rgba(255, 255, 255, 0.1)')
)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig_sentiment, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)