# sales_analysis_pipeline.py

import pandas as pd
import plotly.express as px


def sales_analysis_charts(df):
    """
    Generate multiple sales-related charts & dynamic insights:
    - Sales Trend by Year
    - Sales by Month (stacked by year)
    - Sales by Channel (stacked by year)
    - Sales by Country

    Returns:
        figs (dict): keys = {"year", "month", "channel", "country"}, values = Plotly figures
        insights (dict): keys match figs, values = markdown insight strings
    """

    figs = {}
    insights = {}

    # === Sales Trend by Year ===
    sales_by_year = df.groupby("Year")["Sales"].sum().reset_index()

    fig_sales_trend = px.bar(
        sales_by_year,
        x="Year",
        y="Sales",
        text="Sales",
        title="Total Sales Trend by Year",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_dark",
    )
    fig_sales_trend.update_traces(texttemplate="%{y:.2s}", textposition="outside")
    fig_sales_trend.update_xaxes(type="category")
    figs["year"] = fig_sales_trend

    # Insights: Yearly
    best_year = sales_by_year.loc[sales_by_year["Sales"].idxmax()]
    worst_year = sales_by_year.loc[sales_by_year["Sales"].idxmin()]
    insights["year"] = f"""
Yearly Sales Insights
- Peak Sales Year: {best_year['Year']} with **{best_year['Sales']:.2f} units**.
- Lowest Sales Year: {worst_year['Year']} with **{worst_year['Sales']:.2f} units**.
- Key Takeaway: The difference between the best and worst years is **{best_year['Sales'] - worst_year['Sales']:.2f} units**, highlighting significant annual sales variation and trends over time.
"""


    # === Sales by Month (Stacked by Year) ===
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    sales_by_month_year = df.groupby(["Month", "Year"])["Sales"].sum().reset_index()

    fig_month = px.bar(
        sales_by_month_year,
        x="Month",
        y="Sales",
        color="Year",
        text="Sales",
        title="Sales by Month (Stacked by Year)",
        template="plotly_dark",
        category_orders={"Month": month_order},
    )
    fig_month.update_traces(texttemplate="%{y:.2s}", textposition="inside")
    figs["month"] = fig_month

    # Insights: Monthly
    monthly_totals = sales_by_month_year.groupby("Month")["Sales"].sum().reset_index()
    best_month = monthly_totals.loc[monthly_totals["Sales"].idxmax()]
    worst_month = monthly_totals.loc[monthly_totals["Sales"].idxmin()]
    insights["month"] = f"""
Monthly Sales Insights
- Strongest Month: {best_month['Month']} with **{best_month['Sales']:.2f} units**.
- Weakest Month: {worst_month['Month']} with **{worst_month['Sales']:.2f} units**.
- Key Takeaway: Highlights clear seasonal trends in sales, helping to plan marketing and inventory strategies.
"""


    # === Sales by Channel (Stacked by Year) ===
    sales_by_channel_year = df.groupby(["Channel", "Year"])["Sales"].sum().reset_index()

    fig_channel = px.bar(
        sales_by_channel_year,
        x="Channel",
        y="Sales",
        color="Year",
        text="Sales",
        title="Sales by Channel (Stacked by Year)",
        template="plotly_dark",
    )
    fig_channel.update_traces(texttemplate="%{y:.2s}", textposition="inside")
    figs["channel"] = fig_channel

    # Insights: Channel
    channel_totals = sales_by_channel_year.groupby("Channel")["Sales"].sum().reset_index()
    best_channel = channel_totals.loc[channel_totals["Sales"].idxmax()]
    worst_channel = channel_totals.loc[channel_totals["Sales"].idxmin()]
    insights["channel"] = f"""
        Channel Performance Insights
        - Top-Performing Channel: {best_channel['Channel']} with **{best_channel['Sales']:.2f} units**.
        - Lowest-Performing Channel: {worst_channel['Channel']} with **{worst_channel['Sales']:.2f} units**.
        - Key Takeaway: Highlights clear performance differences between channels, helping to identify high-revenue drivers and areas needing improvement.
        """


    # === Sales by Country ===
    sales_by_country = df.groupby(["Year", "Country"])["Sales"].sum().reset_index()

    fig_country = px.bar(
        sales_by_country,
        x="Country",
        y="Sales",
        text="Sales",
        title="Sales by Country",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_dark",
    )
    fig_country.update_traces(texttemplate="%{y:.2s}", textposition="outside")
    fig_country.update_layout(xaxis=dict(categoryorder="total descending"))
    figs["country"] = fig_country

    # Insights: Country
    country_totals = sales_by_country.groupby("Country")["Sales"].sum().reset_index()
    best_country = country_totals.loc[country_totals["Sales"].idxmax()]
    worst_country = country_totals.loc[country_totals["Sales"].idxmin()]
    insights["country"] = f"""
        Country-Level Sales Insights
        - Highest Sales Country: {best_country['Country']} with **{best_country['Sales']:.2f} units**.
        - Lowest Sales Country: {worst_country['Country']} with **{worst_country['Sales']:.2f} units**.
        - Key Takeaway: Indicates significant differences in market penetration and potential areas for growth or focus.
        """

    return figs, insights
