import pandas as pd
import plotly.express as px

def generate_product_analysis(df1):
    figs = {}
    insights = {}

    # --- 1. Product Life Cycle Trend ---
    prod_trend = df1.groupby(["Year", "Product Name"])["Sales"].sum().reset_index()

    fig_product = px.line(
        prod_trend,
        x="Product Name",
        y="Sales",
        animation_frame="Year",
        color="Product Name",
        title="Product Life Cycle Trend",
        markers=True,
        template="plotly_dark"
    )
    fig_product.update_xaxes(showticklabels=False)
    fig_product.update_layout(
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 1800, "redraw": True},
                                    "fromcurrent": True,
                                    "transition": {"duration": 2000}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }]
        }]
    )
    figs["Product Life Cycle Trend"] = fig_product

    # Insights for Product Life Cycle Trend
    prod_total_sales = prod_trend.groupby("Product Name")["Sales"].sum()
    top_product = prod_total_sales.idxmax()
    top_sales = prod_total_sales.max()
    bottom_product = prod_total_sales.idxmin()
    bottom_sales = prod_total_sales.min()
    insights["Product Life Cycle Trend"] = f"""
Product Life Cycle Insights
- Top Selling Product Overall: {top_product} with total sales of {top_sales:,.0f}.
- Lowest Selling Product: {bottom_product} with total sales of {bottom_sales:,.0f}.
- Shows yearly sales trajectory for each product.
- Useful for identifying mature, growing, and declining products.
- Highlights products needing marketing support or discontinuation consideration.
"""

    # --- 2. Product Class Performance Over Time ---
    class_trend = df1.groupby(["Year", "Product Class"])["Sales"].sum().reset_index()

    fig_class = px.area(
        class_trend,
        x="Year",
        y="Sales",
        color="Product Class",
        title="Product Class Performance Over Time",
        template="plotly_dark"
    )
    fig_class.update_xaxes(type="category")
    figs["Product Class Performance"] = fig_class

    # Insights for Product Class Performance
    class_total_sales = class_trend.groupby("Product Class")["Sales"].sum()
    top_class = class_total_sales.idxmax()
    top_class_sales = class_total_sales.max()
    bottom_class = class_total_sales.idxmin()
    bottom_class_sales = class_total_sales.min()
    insights["Product Class Performance"] = f"""
Product Class Performance Insights
- Top Performing Product Class: {top_class} with total sales of {top_class_sales:,.0f}.
- Lowest Performing Product Class: {bottom_class} with total sales of {bottom_class_sales:,.0f}.
- Shows cumulative sales trends of product classes over years.
- Useful for portfolio optimization and prioritizing high-growth product classes.
"""

    # --- 3. Cross Market Product Performance ---
    prod_market = df1.groupby(["Product Name", "Country"])["Sales"].mean().reset_index()

    fig_prod_market = px.line(
        prod_market,
        x="Product Name",
        y="Sales",
        color="Country",
        title="Cross-Market Product Performance",
        template="plotly_dark"
    )
    fig_prod_market.update_xaxes(showticklabels=False)
    figs["Cross Market Product Performance"] = fig_prod_market

    # Insights for Cross Market Product Performance
    market_total_sales = prod_market.groupby("Country")["Sales"].sum()
    top_country = market_total_sales.idxmax()
    top_country_sales = market_total_sales.max()
    bottom_country = market_total_sales.idxmin()
    bottom_country_sales = market_total_sales.min()
    insights["Cross Market Product Performance"] = f"""
      Cross-Market Product Insights
      - Highest Revenue Country: {top_country} with total sales of {top_country_sales:,.0f}.
      - Lowest Revenue Country: {bottom_country} with total sales of {bottom_country_sales:,.0f}.
      - Shows how each product performs in different markets.
      - Useful for targeting markets for expansion or resource allocation.
      """

    return figs, insights
