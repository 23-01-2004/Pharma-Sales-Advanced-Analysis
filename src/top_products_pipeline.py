# top_products_pipeline.py

import pandas as pd
import plotly.express as px

def top_products_chart(df):
    """
    Generate a bar chart for Top 10 Products by Sales
    """
    print("===Top Products by Sales===")

    top_product = (
        df.groupby(["Product Name"])["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_product = px.bar(
        top_product,
        x="Sales",
        y="Product Name",
        orientation="h",
        text="Sales",
        color="Sales",
        title="Top 10 Products by Sale",
        color_continuous_scale="magma"
    )

    fig_product.update_layout(
        xaxis_title="Sales",
        yaxis_title="Product Name",
        template="plotly_white"
    )
    return fig_product
