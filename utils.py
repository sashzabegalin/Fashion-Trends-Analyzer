import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_trend_data():
    """Generate expanded fashion trend data"""
    trends = [
        "Sustainable Fashion", "Y2K Revival", "Oversized Blazers",
        "Cut-out Details", "Monochrome Sets", "Platform Shoes",
        "Metallic Fabrics", "Gender-fluid Fashion"
    ]

    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = []

    for trend in trends:
        base = np.random.randint(500, 1500)
        growth_factor = np.random.uniform(0.8, 1.2)
        for date in dates:
            day_of_year = date.dayofyear
            seasonal_factor = 1 + 0.3 * np.sin(2 * np.pi * day_of_year / 365)
            engagement = base * seasonal_factor * (1 + 0.001 * day_of_year) * growth_factor
            sentiment = np.random.uniform(0.3, 0.9)
            data.append({
                'date': date,
                'trend': trend,
                'engagement': int(max(0, engagement)),
                'sentiment': round(sentiment, 2),
                'mentions': int(engagement * np.random.uniform(0.8, 1.2)),
                'shares': int(engagement * np.random.uniform(0.3, 0.5)),
                'saves': int(engagement * np.random.uniform(0.1, 0.2))
            })

    return pd.DataFrame(data)

def calculate_trend_metrics(df):
    """Calculate comprehensive trend metrics"""
    latest_date = df['date'].max()
    last_30_days = df[df['date'] >= latest_date - pd.Timedelta(days=30)]
    prev_30_days = df[(df['date'] < latest_date - pd.Timedelta(days=30)) & 
                      (df['date'] >= latest_date - pd.Timedelta(days=60))]

    metrics = []
    for trend in df['trend'].unique():
        trend_data = last_30_days[last_30_days['trend'] == trend]
        prev_trend_data = prev_30_days[prev_30_days['trend'] == trend]

        current_engagement = trend_data['engagement'].mean()
        prev_engagement = prev_trend_data['engagement'].mean()
        growth_rate = ((current_engagement / prev_engagement - 1) * 100) if prev_engagement > 0 else 0

        metrics.append({
            'trend': trend,
            'avg_engagement': int(current_engagement),
            'avg_sentiment': round(trend_data['sentiment'].mean(), 2),
            'growth_rate': round(growth_rate, 1),
            'total_mentions': int(trend_data['mentions'].sum()),
            'total_shares': int(trend_data['shares'].sum()),
            'total_saves': int(trend_data['saves'].sum()),
            'engagement_rate': round((trend_data['engagement'] / trend_data['mentions']).mean() * 100, 1)
        })

    return pd.DataFrame(metrics)

def get_trend_analytics():
    """Get overall trend analytics"""
    df = generate_mock_trend_data()
    latest_date = df['date'].max()
    current_data = df[df['date'] == latest_date]

    total_engagement = current_data['engagement'].sum()
    total_mentions = current_data['mentions'].sum()

    return {
        'transfer_rate': round((total_engagement / total_mentions) * 100),
        'receive_rate': 31,  # Mock percentage
        'user_authorized': 18785,
        'analytics_increase': 78,
        'period': '3 Month'
    }