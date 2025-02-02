import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_mock_trend_data, calculate_trend_metrics

st.set_page_config(
    page_title="Fashion Trend Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown('<h1 class="main-title">Fashion Analytics Dashboard</h1>', unsafe_allow_html=True)

df = generate_mock_trend_data()
metrics_df = calculate_trend_metrics(df)

def create_metric_card(label, value, percentage):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="trend-percentage">+{percentage}%</div>
    </div>
    """

# Top metrics
metrics = [
    ("Total Engagement", f"{metrics_df['avg_engagement'].sum():,}", "12.5"),
    ("Active Trends", str(len(metrics_df)), "3.2"),
    ("Average Sentiment", f"{metrics_df['avg_sentiment'].mean():.2f}", "5.8")
]

cols = st.columns(3)
for col, (label, value, percentage) in zip(cols, metrics):
    col.markdown(create_metric_card(label, value, percentage), unsafe_allow_html=True)

# Trend Evolution Chart
st.markdown('<div class="section-title">Trend Evolution</div>', unsafe_allow_html=True)
selected_trends = st.multiselect(
    "Select trends to compare",
    options=df['trend'].unique(),
    default=df['trend'].unique()[:3]
)

filtered_df = df[df['trend'].isin(selected_trends)]
fig = px.line(filtered_df, x='date', y='engagement', color='trend', template='plotly_dark')
fig.update_layout(
    plot_bgcolor='rgba(14, 17, 23, 0.7)',
    paper_bgcolor='rgba(0, 0, 0, 0)',
    font_family='Outfit',
    font_color='#FFFFFF',
    height=400,
    margin=dict(t=30, r=20, b=30, l=20),
    hovermode='x unified',
    legend=dict(
        yanchor="top", y=0.99,
        xanchor="left", x=0.01,
        bgcolor='rgba(14, 17, 23, 0.7)'
    )
)
fig.update_traces(line=dict(width=3))
st.plotly_chart(fig, use_container_width=True)

# Trend Performance Grid
st.markdown('<div class="section-title">Trend Performance</div>', unsafe_allow_html=True)
st.markdown('<div class="trend-metrics-grid">', unsafe_allow_html=True)
for _, trend_data in metrics_df.iterrows():
    growth_class = "positive" if trend_data["growth_rate"] > 0 else "negative"
    st.markdown(f"""
        <div class="trend-metric-item">
            <div class="metric-label">{trend_data["trend"]}</div>
            <div class="metric-value">{trend_data["avg_engagement"]:,}</div>
            <div class="trend-percentage {growth_class}">{'+' if trend_data["growth_rate"] > 0 else ''}{trend_data["growth_rate"]}%</div>
        </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sentiment Analysis
st.markdown('<div class="section-title">Sentiment Analysis</div>', unsafe_allow_html=True)
fig_sentiment = go.Figure(data=[
    go.Bar(x=metrics_df['trend'], y=metrics_df['avg_sentiment'],
           marker_color='#0066FF', opacity=0.8)
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