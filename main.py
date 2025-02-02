import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_mock_trend_data, calculate_trend_metrics, get_trend_analytics
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
analytics = get_trend_analytics()

# Top metrics section
col1, col2 = st.columns([2, 1])

with col1:
    # Transfer/Receive rates
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Transfer</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">65%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-subtitle">29/user</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with subcol2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('<div class="metric-label">Receive</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-value">31%</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-subtitle">8/user</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card analytics-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Analytics</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="analytics-value">{analytics["analytics_increase"]}%</div>', unsafe_allow_html=True)
    st.markdown('<div class="analytics-subtitle">Increase</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Trend Evolution Chart
st.markdown("### Trend Evolution")
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
    font_family='Inter',
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

# Period Analytics
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-label">Period Analytic</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="period-value">{analytics["period"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-subtitle">User Authorized: {analytics["user_authorized"]:,}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">Payment Transaction</div>', unsafe_allow_html=True)
    transactions = [
        ("Repayment cash", "1,120"),
        ("Office leasing", "3,810"),
        ("Employee salary", "12,760")
    ]
    for desc, amount in transactions:
        st.markdown(f'<div class="transaction-row"><span>{desc}</span><span>${amount}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Trend Performance Grid
st.markdown("### Trend Performance")
for i in range(0, len(metrics_df), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(metrics_df):
            trend_data = metrics_df.iloc[i + j]
            with col:
                st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                st.markdown(f"#### {trend_data['trend']}")
                st.markdown(f'<div class="metric-value">{trend_data["avg_engagement"]:,}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="trend-percentage">+{trend_data["growth_rate"]}%</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-details">', unsafe_allow_html=True)
                st.markdown(f'Mentions: {trend_data["total_mentions"]:,}<br>', unsafe_allow_html=True)
                st.markdown(f'Shares: {trend_data["total_shares"]:,}<br>', unsafe_allow_html=True)
                st.markdown(f'Saves: {trend_data["total_saves"]:,}', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)