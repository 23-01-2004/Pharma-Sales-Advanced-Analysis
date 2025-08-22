import pandas as pd
import plotly.express as px

def generate_channel_analysis(df1):
    figs = {}
    insights = {}

    # --- 1. Channel Performance (Pie or Stacked Bar) ---
    channel_perf = df1.groupby(["Year", "Channel"])["Sales"].sum().reset_index()
    
    # Stacked bar per year for better trend visibility
    fig_channel = px.bar(
        channel_perf,
        x="Year",
        y="Sales",
        color="Channel",
        title="Channel Sales Performance Over Years",
        labels={"Sales": "Total Sales", "Year": "Year", "Channel": "Channel"},
        template="plotly_dark"
    )
    fig_channel.update_layout(barmode='stack')
    figs["Retail vs Hospital Performance"] = fig_channel

    # Insights for Channel Performance
    total_sales = channel_perf.groupby("Channel")["Sales"].sum()
    top_channel = total_sales.idxmax()
    top_channel_sales = total_sales.max()
    bottom_channel = total_sales.idxmin()
    bottom_channel_sales = total_sales.min()
    insights["Retail vs Hospital Performance"] = f"""
Channel Sales Performance Insights
- Top Channel Overall: {top_channel} with total sales of {top_channel_sales:,.0f}.
- Lowest Channel Overall: {bottom_channel} with total sales of {bottom_channel_sales:,.0f}.
- Shows relative contribution of each channel over the years.
- Useful to identify high-performing channels and monitor trends.
"""

    # --- 2. Pricing Patterns (Violin Plot by Channel & Year) ---
    df1["Price_Per_Unit"] = df1["Sales"] / df1["Quantity"]

    fig_price_channel = px.violin(
        df1,
        x="Channel",
        y="Price_Per_Unit",
        color="Channel",
        box=True,
        points="all",
        facet_col="Year",
        title="Pricing Patterns across Channels (Violin Plot)",
        template="plotly_dark"
    )
    figs["Pricing Patterns across Channels"] = fig_price_channel

    # Insights for Pricing Patterns
    pricing_summary = df1.groupby("Channel")["Price_Per_Unit"].agg(['mean', 'median', 'min', 'max']).reset_index()
    top_priced_channel = pricing_summary.loc[pricing_summary["mean"].idxmax()]["Channel"]
    top_price_mean = pricing_summary["mean"].max()
    low_priced_channel = pricing_summary.loc[pricing_summary["mean"].idxmin()]["Channel"]
    low_price_mean = pricing_summary["mean"].min()
    insights["Pricing Patterns across Channels"] = f"""
Pricing Patterns Insights
- Highest Priced Channel on Average: {top_priced_channel} with mean price per unit of {top_price_mean:,.2f}.
- Lowest Priced Channel on Average: {low_priced_channel} with mean price per unit of {low_price_mean:,.2f}.
- Shows distribution of pricing per channel and year, including outliers.
- Useful to understand pricing strategy, channel positioning, and revenue potential.
"""

    # --- 3. Distribution Partner Effectiveness ---
    partner_perf = df1.groupby(["Year", "Sub-channel"])["Sales"].sum().reset_index()

    fig_partner = px.bar(
        partner_perf.sort_values("Sales", ascending=False),
        x="Sub-channel",
        y="Sales",
        color="Sales",
        animation_frame="Year",
        title="Distribution Partner Effectiveness",
        template="plotly_dark",
        color_continuous_scale=px.colors.sequential.Blues
    )

    fig_partner.update_layout(
        updatemenus=[{
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 2000, "redraw": True},
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
    figs["Distribution Partner Effectiveness"] = fig_partner

    # Insights for Partner Effectiveness
    partner_total_sales = partner_perf.groupby("Sub-channel")["Sales"].sum()
    top_partner = partner_total_sales.idxmax()
    top_partner_sales = partner_total_sales.max()
    bottom_partner = partner_total_sales.idxmin()
    bottom_partner_sales = partner_total_sales.min()
    insights["Distribution Partner Effectiveness"] = f"""
      Distribution Partner Effectiveness Insights
      - Top Performing Partner Overall: {top_partner} with total sales of {top_partner_sales:,.0f}.
      - Lowest Performing Partner Overall: {bottom_partner} with total sales of {bottom_partner_sales:,.0f}.
      - Shows partner contributions year over year and highlights high-performing distribution channels.
      - Useful to optimize distribution network and identify underperforming partners.
      """

    return figs, insights
