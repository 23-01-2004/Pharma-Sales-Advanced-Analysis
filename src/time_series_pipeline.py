import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from statsmodels.tsa.seasonal import seasonal_decompose

def generate_time_series_analysis(df):
    df_ts = df.copy()
    figs, insights = {}, {}

    df_ts['Date'] = pd.to_datetime(df_ts['Month'].astype(str) + " " + df_ts['Year'].astype(str), format="%B %Y")
    
    # ---------------- Monthly Sales ----------------
    monthly_sales = df_ts.groupby('Date')['Sales'].sum().reset_index()
    fig_monthly = px.line(
        monthly_sales,
        x='Date',
        y='Sales',
        title="Monthly Sales Data",
        labels={'Sales': 'Total Sales'},
        template='plotly_dark',
        line_shape='spline',
        markers=True
    )
    fig_monthly.update_traces(line=dict(color="#1f77b4", width=3))  # Blue line
    figs["Monthly Sales"] = fig_monthly

    # Dynamic Insight
    latest_month = monthly_sales.iloc[-1]
    prev_month = monthly_sales.iloc[-2]
    mom_growth = ((latest_month["Sales"] - prev_month["Sales"]) / prev_month["Sales"]) * 100
    insights["Monthly Sales"] = f"""
    - Latest month ({latest_month['Date'].strftime('%B %Y')}) sales: ${latest_month['Sales']:,.0f}
    - MoM Growth: {mom_growth:+.1f}% compared to previous month  
    - Overall trend: {'📈 Increasing' if mom_growth > 0 else '📉 Decreasing'} in recent months.  
    """

    # ---------------- Yearly Sales ----------------
    yearly_sales = df_ts.groupby('Year')['Sales'].sum().reset_index()
    fig_yearly = px.bar(
        yearly_sales,
        x='Year',
        y='Sales',
        text_auto=True,
        title="Yearly Sales Trend",
        template='plotly_dark',
        color='Sales',
        color_continuous_scale=px.colors.sequential.Blues
    )
    figs["Yearly Sales"] = fig_yearly

    yoy_growth = yearly_sales['Sales'].pct_change().fillna(0) * 100
    highest_year = yearly_sales.loc[yearly_sales['Sales'].idxmax(), 'Year']
    highest_sales = yearly_sales['Sales'].max()
    lowest_year = yearly_sales.loc[yearly_sales['Sales'].idxmin(), 'Year']
    lowest_sales = yearly_sales['Sales'].min()
    last_year_yoy = yoy_growth.iloc[-1]
    avg_yoy = yoy_growth.mean()

    long_term_trend = "consistent 📈 growth" if avg_yoy > 0 else "fluctuations 📉"
    trend_implication = "sustained widening of sales" if avg_yoy > 0 else "erratic growth of sales"
    insights["Yearly Sales"] = f"""
 Yearly Sales Performance Overview

- Highest Sales Year: {highest_year} with total sales of {highest_sales:,.0f}.
- Lowest Sales Year: {lowest_year} with total sales of {lowest_sales:,.0f}.
- YoY Growth (Last Year): {last_year_yoy:+.1f}%  
- Average YoY Growth: {avg_yoy:+.1f}%  
- Long-term Trend: {long_term_trend} observed over the years.  
- Interpretation: This indicates a {trend_implication}, highlighting how the sales trajectory has evolved historically.  
- Additional Insight: The difference between highest and lowest sales years is {highest_sales - lowest_sales:,.0f}, showing the range of sales performance.  
"""

    # ---------------- Seasonal Decomposition ----------------
    target_col = "Sales"
    ts_monthly = df_ts.groupby(pd.Grouper(key="Date", freq="MS"))[target_col].sum().sort_index()
    n = len(ts_monthly)
    period = 12
    model_type = "multiplicative" if ts_monthly.min() > 0 else "additive"

    if n >= 2 * period:
        result = seasonal_decompose(ts_monthly, model=model_type, period=period, extrapolate_trend="freq")
        fig_seasonal = make_subplots(
            rows=4, cols=1, shared_xaxes=True,
            subplot_titles=("Observed", "Trend", "Seasonality", "Residuals"),
            vertical_spacing=0.1
        )
        fig_seasonal.add_trace(go.Scatter(x=result.observed.index, y=result.observed, mode="lines+markers",
                                          name="Observed", line=dict(color="#1f77b4", width=2)), row=1, col=1)
        fig_seasonal.add_trace(go.Scatter(x=result.trend.index, y=result.trend, mode="lines",
                                          name="Trend", line=dict(color="#3f87d6", width=3, dash="dot")), row=2, col=1)
        fig_seasonal.add_trace(go.Scatter(x=result.seasonal.index, y=result.seasonal, mode="lines",
                                          name="Seasonality", line=dict(color="#5fa0e6", width=2)), row=3, col=1)
        fig_seasonal.add_trace(go.Scatter(x=result.resid.index, y=result.resid, mode="lines+markers",
                                          name="Residuals", line=dict(color="#81b8f7", width=2)), row=4, col=1)
        fig_seasonal.update_layout(
            height=900, width=1100,
            title_text="Seasonal Decomposition of Sales",
            title_x=0.5,
            showlegend=True,
            template="plotly_dark",
            font=dict(size=14),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        figs["Seasonal Decomposition"] = fig_seasonal
        insights["Seasonal Decomposition"] = f"""
         Seasonal Decomposition Insights  

        - Trend: The data shows a clear long-term {'upward 📈' if result.trend.dropna().iloc[-1] > result.trend.dropna().iloc[0] else 'downward 📉'} movement.  
          - This indicates that the underlying demand/metric is {'growing steadily over time, which may suggest market expansion, improved adoption, or positive external influences.' if result.trend.dropna().iloc[-1] > result.trend.dropna().iloc[0] else 'shrinking gradually, possibly due to market saturation, reduced demand, or external challenges.'}  

        - Seasonality: Strong recurring cycles every 12 months are observed.  
          - This suggests that external factors such as **festive seasons, yearly demand surges, or recurring events** are influencing the data regularly.  
          - Seasonality patterns can help with **forecasting and resource planning (e.g., stock, manpower, or budget allocation).  

        - Residuals: The residual component indicates {'relatively stable variations ' if result.resid.std() < result.observed.std()*0.5 else 'significant irregularities '}.  
          - {'Since the residual noise is low, the model fits the data well and most variations are explained by trend and seasonality.' if result.resid.std() < result.observed.std()*0.5 else 'High residual volatility means unexpected shocks or outliers exist, which may require further investigation (e.g., promotions, economic events, or anomalies).'}  

         Key Takeaways:
        - The data can be reliably forecasted** using trend + seasonality.  
        - This decomposition is useful for strategic decision-making, such as **forecasting, anomaly detection, and planning resource allocation.
        """


    # ---------------- Product-level YoY Growth ----------------
    product_year = df_ts.groupby(['Product Name', 'Year'])['Sales'].sum().unstack().fillna(0)
    product_growth = product_year.pct_change(axis=1) * 100
    growth_long = product_growth.reset_index().melt(
        id_vars="Product Name",
        var_name="Year",
        value_name="Growth %"
    ).dropna()
    top_products = growth_long.groupby("Product Name")["Growth %"].mean().sort_values(ascending=False).head(10).index
    growth_top = growth_long[growth_long["Product Name"].isin(top_products)]
    fig_product_growth = px.bar(
        growth_top,
        x="Product Name",
        y="Growth %",
        color="Year",
        barmode="group",
        title="Top 10 Products by YoY Growth % (Grouped by Year)",
        labels={"Growth %": "Growth %"},
        template="plotly_dark",
        text_auto=".1f"
    )
    figs["Product YoY Growth"] = fig_product_growth
    insights["Product YoY Growth"] = f"""
- The top growing products in terms of Year-over-Year sales are: {', '.join(top_products[:3])}.  
- On average, these products achieved a growth rate of {growth_top['Growth %'].mean():.1f}%, which is significantly higher than the portfolio-wide average.  
- This indicates that a few high-performing products are disproportionately driving overall momentum, highlighting their importance in the sales mix.  
- Such growth concentration suggests an opportunity to:  
    Double down on marketing, distribution, and inventory of these fast-moving products.  
    Explore cross-selling or bundling strategies with slower-moving items to balance demand.  
    Monitor sustainability of this growth, as over-reliance on a small set of products can pose risk if demand trends shift.  
"""


    # ---------------- Sales Team YoY Growth ----------------
    team_year = df_ts.groupby(['Sales Team', 'Year'])['Sales'].sum().reset_index()
    team_year['YoY Growth %'] = team_year.groupby('Sales Team')['Sales'].pct_change() * 100
    team_growth = team_year.dropna(subset=['YoY Growth %'])
    fig_team_growth = px.bar(
        team_growth,
        x="Year",
        y="YoY Growth %",
        color="Sales Team",
        barmode="group",
        text=team_growth["YoY Growth %"].round(1).astype(str) + "%",
        title="Year-over-Year Growth by Sales Team (%)",
        labels={"YoY Growth %": "Growth %"},
        template="plotly_dark"
    )
    fig_team_growth.update_traces(textposition="outside")
    fig_team_growth.update_layout(
        yaxis_title="YoY Growth (%)",
        xaxis_title="Year",
        legend_title="Sales Team",
        bargap=0.25
    )
    figs["Sales Team YoY Growth"] = fig_team_growth
    insights["Sales Team YoY Growth"] = f"""
Year-over-Year (YoY) Sales Team Growth Analysis

-  Top Growth Leader: In {team_growth['Year'].max()}, the {team_growth.loc[team_growth['Year']==team_growth['Year'].max()].sort_values('YoY Growth %', ascending=False).iloc[0]['Sales Team']} team achieved the **highest YoY growth rate**, indicating strong execution and market traction.  

-  Average Growth Across Teams: The overall average YoY growth across sales teams was {team_growth['YoY Growth %'].mean():.1f}%, providing a benchmark of collective performance.  

-  Consistency vs. Variability: Growth dispersion across teams was {team_growth['YoY Growth %'].std():.1f}%. This suggests {"a healthy balance of contributions , indicating most teams are performing consistently." if team_growth['YoY Growth %'].std() < 10 else "uneven contribution , where a few teams may be driving most of the overall growth while others lag behind."}  

-  Strategic Implication: {"Focus on scaling best practices from top performers across other teams to sustain growth." if team_growth['YoY Growth %'].std() < 10 else "Investigate underperforming teams to identify structural challenges and address bottlenecks."}
"""


    return figs, insights
