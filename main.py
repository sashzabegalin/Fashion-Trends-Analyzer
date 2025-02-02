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

# Create columns for the top metrics
col1, col2, col3 = st.columns(3)

# Column 1
with col1:
    container = st.container()
    with container:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Total Engagement</div>
            <div class="metric-value">{:,}</div>
            <div class="trend-percentage">+12.5%</div>
        </div>
        """.format(metrics_df["avg_engagement"].sum()), unsafe_allow_html=True)

# Column 2
with col2:
    container = st.container()
    with container:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Active Trends</div>
            <div class="metric-value">{}</div>
            <div class="trend-percentage">+3.2%</div>
        </div>
        """.format(len(metrics_df)), unsafe_allow_html=True)

# Column 3
with col3:
    container = st.container()
    with container:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Average Sentiment</div>
            <div class="metric-value">{:.2f}</div>
            <div class="trend-percentage">+5.8%</div>
        </div>
        """.format(metrics_df['avg_sentiment'].mean()), unsafe_allow_html=True)

# Trend Evolution Chart
trend_container = st.container()
with trend_container:
    st.markdown("""
    <div class="metric-card">
        <div class="section-title">Trend Evolution</div>
        """, unsafe_allow_html=True)

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

    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Trend Performance Grid
perf_container = st.container()
with perf_container:
    st.markdown("""
    <div class="metric-card">
        <div class="section-title">Trend Performance</div>
        """, unsafe_allow_html=True)

    for i in range(0, len(metrics_df), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < len(metrics_df):
                trend_data = metrics_df.iloc[i + j]
                with col:
                    st.markdown(f"""
                    <div class="metric-label">{trend_data["trend"]}</div>
                    <div class="metric-value">{trend_data["avg_engagement"]:,}</div>
                    <div class="trend-percentage">+{trend_data["growth_rate"]}%</div>
                    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Sentiment Analysis
sentiment_container = st.container()
with sentiment_container:
    st.markdown("""
    <div class="metric-card">
        <div class="section-title">Sentiment Analysis</div>
        """, unsafe_allow_html=True)

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

    st.plotly_chart(fig_sentiment, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)