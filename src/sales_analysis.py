import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def generate_sales_analysis(df):
    """
    Generate sales analysis plots and insights:
    - Top Products by Revenue & Quantity
    - Country & City Rankings
    - Channel/Sub-channel Performance
    - Pareto Analysis
    Returns: (figures, insights)
    """
    df_analysis = df.copy()
    figs, insights = {}, {}

    # ---------------- Top 10 Products ----------------
    top_products_sales = df_analysis.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    top_products_qty = df_analysis.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()

    # Revenue chart
    fig_sales = px.bar(
        top_products_sales,
        x="Sales", y="Product Name",
        orientation="h",
        title="Top 10 Products by Revenue",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_dark"
    )
    fig_sales.update_layout(yaxis=dict(autorange="reversed"))
    figs["Top Products by Revenue"] = fig_sales
    insights["Top Products by Revenue"] = f"""
    - The product **{top_products_sales.iloc[0,0]}** is the highest revenue generator with ${top_products_sales.iloc[0,1]:,.2f}.  
    - Together, the top 10 products contribute **{top_products_sales['Sales'].sum()/df_analysis['Sales'].sum()*100:.1f}%** of total revenue.  
    - This suggests a concentrated product mix where a few products drive most of the sales.  
    """

    # Quantity chart
    fig_qty = px.bar(
        top_products_qty,
        x="Quantity", y="Product Name",
        orientation="h",
        title="Top 10 Products by Quantity",
        color="Quantity",
        color_continuous_scale="Blues",
        template="plotly_dark"
    )
    fig_qty.update_layout(yaxis=dict(autorange="reversed"))
    figs["Top Products by Quantity"] = fig_qty
    insights["Top Products by Quantity"] = f"""
    - The product **{top_products_qty.iloc[0,0]}** leads in units sold (**{top_products_qty.iloc[0,1]:,.0f} units**).  
    - Interestingly, the highest quantity product may differ from the highest revenue product, highlighting the impact of pricing.  
    """

    # ---------------- Country Rankings ----------------
    country_sales = df_analysis.groupby('Country')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig_country = px.bar(
        country_sales,
        x="Country", y="Sales",
        title="Country Rankings by Revenue",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_dark"
    )
    figs["Country Rankings"] = fig_country
    insights["Country Rankings"] = f"""
    - **{country_sales.iloc[0,0]}** contributes the most revenue (${country_sales.iloc[0,1]:,.2f}).  
    - The top 3 countries account for **{country_sales.head(3)['Sales'].sum()/country_sales['Sales'].sum()*100:.1f}%** of overall revenue.  
    - Focused expansion in lower-performing regions may unlock untapped potential.  
    """

    # ---------------- Top 10 Cities ----------------
    city_sales = df_analysis.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_city = px.bar(
        city_sales,
        x="Sales", y="City",
        orientation="h",
        title="Top 10 Cities by Revenue",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_dark"
    )
    fig_city.update_layout(yaxis=dict(autorange="reversed"))
    figs["Top Cities"] = fig_city
    insights["Top Cities"] = f"""
    - **{city_sales.iloc[0,0]}** is the top-performing city with ${city_sales.iloc[0,1]:,.2f}.  
    - The top 10 cities represent **{city_sales['Sales'].sum()/df_analysis['Sales'].sum()*100:.1f}%** of revenue.  
    - Urban markets appear to dominate overall performance.  
    """

    # ---------------- Channel Performance ----------------
    channel_sales = df_analysis.groupby('Channel')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig_channel = px.bar(
        channel_sales,
        x="Channel", y="Sales",
        title="Channel Performance by Revenue",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_dark"
    )
    figs["Channel Performance"] = fig_channel
    insights["Channel Performance"] = f"""
    - The **{channel_sales.iloc[0,0]}** channel dominates with ${channel_sales.iloc[0,1]:,.2f}.  
    - Some channels underperform, suggesting potential for salesforce realignment.  
    """

    # ---------------- Sub-channel Performance ----------------
    subchannel_sales = df_analysis.groupby('Sub-channel')['Sales'].sum().sort_values(ascending=False).reset_index()
    fig_subchannel = px.bar(
        subchannel_sales,
        x="Sub-channel", y="Sales",
        title="Sub-channel Performance by Revenue",
        color="Sales",
        color_continuous_scale="Blues",
        template="plotly_dark"
    )
    figs["Sub-channel Performance"] = fig_subchannel
    insights["Sub-channel Performance"] = f"""
    - Within sub-channels, **{subchannel_sales.iloc[0,0]}** is the leader (${subchannel_sales.iloc[0,1]:,.2f}).  
    - Distribution across sub-channels shows where customer engagement is most effective.  
    """

    # ---------------- Pareto Analysis ----------------
    product_sales = df_analysis.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
    cumulative_share = product_sales.cumsum() / product_sales.sum() * 100
    top20 = product_sales.head(20).reset_index()
    top20["Cumulative %"] = cumulative_share.head(20).values

    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(
        x=top20["Product Name"],
        y=top20["Sales"],
        name="Revenue",
        marker=dict(color="lightblue")
    ))
    fig_pareto.add_trace(go.Scatter(
        x=top20["Product Name"],
        y=top20["Cumulative %"],
        mode="lines+markers",
        name="Cumulative %",
        yaxis="y2",
        line=dict(color="red")
    ))
    fig_pareto.update_layout(
        title="Pareto Analysis (Top 20 Products)",
        xaxis=dict(title="Product Name", tickangle=45),
        yaxis=dict(title="Revenue"),
        yaxis2=dict(
            title="Cumulative % of Revenue",
            overlaying="y",
            side="right"
        ),
        template="plotly_dark"
    )
    figs["Pareto Analysis"] = fig_pareto
    insights["Pareto Analysis"] = f"""
    - The **80/20 rule** holds true: top 20 products contribute **{cumulative_share.head(20).iloc[-1]:.1f}%** of revenue.  
    - This means a small portion of products drives the majority of sales.  
    - Strategic focus on these products can maximize business impact.  
    """

    return figs, insights
