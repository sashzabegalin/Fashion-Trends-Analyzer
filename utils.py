import pandas as pd
import numpy as np

def generate_mock_trend_data():
    """Generate mock fashion trend data"""
    trends = [
        "Sustainable Fashion",
        "Y2K Revival",
        "Oversized Blazers",
        "Cut-out Details",
        "Monochrome Sets",
        "Platform Shoes",
        "Metallic Fabrics",
        "Gender-fluid Fashion",
        "Digital Fashion NFTs",
        "Bio-fabricated Materials",
        "Smart Adaptive Clothing",
        "Upcycled Vintage"
    ]

    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    data = []

    for trend in trends:
        base = np.random.randint(500, 1500)
        for date in dates:
            engagement = base + np.random.normal(0, 100)
            sentiment = np.random.uniform(0.3, 0.9)
            data.append({
                'date': date,
                'trend': trend,
                'engagement': int(max(0, engagement)),
                'sentiment': round(sentiment, 2)
            })

    return pd.DataFrame(data)

def calculate_trend_metrics(df):
    """Calculate key metrics for trends"""
    latest_date = df['date'].max()
    last_30_days = df[df['date'] >= latest_date - pd.Timedelta(days=30)]

    metrics = []
    for trend in df['trend'].unique():
        trend_data = last_30_days[last_30_days['trend'] == trend]
        metrics.append({
            'trend': trend,
            'avg_engagement': int(trend_data['engagement'].mean()),
            'avg_sentiment': round(trend_data['sentiment'].mean(), 2),
            'growth_rate': round((trend_data['engagement'].iloc[-1] / trend_data['engagement'].iloc[0] - 1) * 100, 1)
        })

    return pd.DataFrame(metrics)