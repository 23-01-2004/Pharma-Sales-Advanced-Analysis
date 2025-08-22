# geographical_sales_pipeline.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def generate_geographical_sales_analysis(df):
    """
    Generate geographical sales analysis plots and insights:
    - Total Sales by Country (Choropleth)
    - Sales Density by City & Country (Treemap)
    - Sales by Channel/Sub-channel (Sunburst)
    - Sales Heatmap: Country vs Channel
    Returns:
        figs: dictionary of Plotly figures
        insights: dictionary of dynamic textual insights
    """
    figs = {}
    insights = {}

    # ===============================
    # 1. Total Sales by Country (Choropleth)
    # ===============================
    country_sales = df.groupby("Country")["Sales"].sum().reset_index()
    fig_country = px.choropleth(
        country_sales,
        locations="Country",
        locationmode="country names",
        color="Sales",
        hover_name="Country",
        color_continuous_scale="RdBu",
        title="Total Sales by Country",
        template="plotly_white"
    )
    fig_country.update_geos(
        projection_type="natural earth",
        fitbounds="locations",
        showcountries=True
    )

    # Add country names as scatter_geo overlay
    fig_country.add_trace(
        go.Scattergeo(
            locations=country_sales['Country'],
            locationmode='country names',
            text=country_sales['Country'],
            mode='text',
            showlegend=False
        )
    )
    figs["Country Sales Map"] = fig_country

    top_country = country_sales.loc[country_sales['Sales'].idxmax()]
    bottom_country = country_sales.loc[country_sales['Sales'].idxmin()]
    total_sales = country_sales['Sales'].sum()
    avg_sales = country_sales['Sales'].mean()
    top_country_pct = (top_country['Sales'] / total_sales) * 100
    bottom_country_pct = (bottom_country['Sales'] / total_sales) * 100
    above_avg_countries = country_sales[country_sales['Sales'] > avg_sales].shape[0]
    below_avg_countries = country_sales[country_sales['Sales'] <= avg_sales].shape[0]
    sales_range = top_country['Sales'] - bottom_country['Sales']

    insights["Country Sales Map"] = f"""
    Geographical Sales Overview
    - Total Sales Across All Countries:{total_sales:,.0f}
    - Average Sales per Country: {avg_sales:,.0f}
    - Top Performing Country: {top_country['Country']} with {top_country['Sales']:,.0f} ({top_country_pct:.1f}% of total sales)
    - Lowest Performing Country: {bottom_country['Country']} with {bottom_country['Sales']:,.0f} ({bottom_country_pct:.1f}% of total sales)
    - Sales Range (Top - Bottom Country):{sales_range:,.0f}
    - Interpretation: The sales distribution shows regions with highest commercial activity, and highlights potential markets for targeted growth strategies.
    - Observation: Countries contributing below the average may require focused marketing or operational initiatives to boost revenue.
    """


    # ===============================
    # 2. Sales Density by City & Country (Treemap)
    # ===============================
    fig_city = px.treemap(
        df,
        path=["Country", "City"],
        values="Sales",
        color="Sales",
        color_continuous_scale="RdBu",
        title="Sales Density by Country & City",
        template="plotly_white"
    )
    figs["City Sales Treemap"] = fig_city

    # Insights for Treemap
    top_city = df.groupby("City")["Sales"].sum().idxmax()
    top_city_sales = df.groupby("City")["Sales"].sum().max()
    # Dynamic City-Level Sales Insights
    city_sales = df.groupby("City")["Sales"].sum().reset_index()
    total_city_sales = city_sales['Sales'].sum()
    avg_city_sales = city_sales['Sales'].mean()

    top_city = city_sales.loc[city_sales['Sales'].idxmax()]
    bottom_city = city_sales.loc[city_sales['Sales'].idxmin()]

    top_city_pct = (top_city['Sales'] / total_city_sales) * 100
    bottom_city_pct = (bottom_city['Sales'] / total_city_sales) * 100

    above_avg_cities = city_sales[city_sales['Sales'] > avg_city_sales].shape[0]
    below_avg_cities = city_sales[city_sales['Sales'] <= avg_city_sales].shape[0]

    city_sales_range = top_city['Sales'] - bottom_city['Sales']

    top_3_cities = city_sales.sort_values('Sales', ascending=False).head(3)
    top_3_cities_list = ", ".join([f"{row['City']} ({row['Sales']:,.0f})" for _, row in top_3_cities.iterrows()])

    insights["City Sales Treemap"] = f"""
     City-Level Sales Insights
    - Total Sales Across All Cities: {total_city_sales:,.0f}
    - Average Sales per City: {avg_city_sales:,.0f}
    - Top Performing City: {top_city['City']} with {top_city['Sales']:,.0f} ({top_city_pct:.1f}% of total sales)
    - Lowest Performing City: {bottom_city['City']} with {bottom_city['Sales']:,.0f} ({bottom_city_pct:.1f}% of total sales)
    - Number of Cities Above Average: {above_avg_cities}
    - Number of Cities Below Average: {below_avg_cities}
    - Sales Range (Top - Bottom City): {city_sales_range:,.0f}
    - Top 3 Cities by Sales: {top_3_cities_list}
    - Interpretation: The treemap highlights high-performing urban markets and identifies cities with potential for growth or focused marketing strategies.
    - Observation: Cities below average may need operational or promotional attention to improve revenue contribution.
    """


    # ===============================
    # 3. Sales by Channel/Sub-channel (Sunburst)
    # ===============================
    fig_channel = px.sunburst(
        df,
        path=["Country", "Channel", "Sub-channel"],
        values="Sales",
        color="Sales",
        color_continuous_scale="Blues",
        title="Sales Density by Channel and Sub-Channel",
        template="plotly_white"
    )
    figs["Channel Sunburst"] = fig_channel

    # Insights for Sunburst
    top_channel = df.groupby("Channel")["Sales"].sum().idxmax()
    top_channel_sales = df.groupby("Channel")["Sales"].sum().max()
    # Dynamic Channel & Sub-Channel Insights
    channel_sales = df.groupby("Channel")["Sales"].sum().reset_index()
    total_channel_sales = channel_sales['Sales'].sum()
    avg_channel_sales = channel_sales['Sales'].mean()

    top_channel = channel_sales.loc[channel_sales['Sales'].idxmax()]
    bottom_channel = channel_sales.loc[channel_sales['Sales'].idxmin()]

    top_channel_pct = (top_channel['Sales'] / total_channel_sales) * 100
    bottom_channel_pct = (bottom_channel['Sales'] / total_channel_sales) * 100

    above_avg_channels = channel_sales[channel_sales['Sales'] > avg_channel_sales].shape[0]
    below_avg_channels = channel_sales[channel_sales['Sales'] <= avg_channel_sales].shape[0]

    channel_sales_range = top_channel['Sales'] - bottom_channel['Sales']

    # Top 3 channels
    top_3_channels = channel_sales.sort_values('Sales', ascending=False).head(3)
    top_3_channels_list = ", ".join([f"{row['Channel']} ({row['Sales']:,.0f})" for _, row in top_3_channels.iterrows()])

    # Top sub-channel for top channel
    top_sub_channel = df[df['Channel'] == top_channel['Channel']].groupby('Sub-channel')['Sales'].sum().idxmax()
    top_sub_channel_sales = df[df['Channel'] == top_channel['Channel']].groupby('Sub-channel')['Sales'].sum().max()

    insights["Channel Sunburst"] = f"""
    Channel & Sub-Channel Performance
    - Total Sales Across All Channels: {total_channel_sales:,.0f}
    - Average Sales per Channel: {avg_channel_sales:,.0f}
    - Top Channel: {top_channel['Channel']} with {top_channel['Sales']:,.0f} ({top_channel_pct:.1f}% of total sales)
    - Lowest Channel: {bottom_channel['Channel']} with {bottom_channel['Sales']:,.0f} ({bottom_channel_pct:.1f}% of total sales)
    - Number of Channels Above Average: {above_avg_channels}
    - Number of Channels Below Average: {below_avg_channels}
    - Sales Range (Top - Bottom Channel): {channel_sales_range:,.0f}
    - Top 3 Channels by Sales: {top_3_channels_list}
    - Top Sub-Channel of {top_channel['Channel']}: {top_sub_channel} with {top_sub_channel_sales:,.0f} in sales
    - Interpretation: The sunburst shows hierarchical contribution of channels and sub-channels, helping identify which segments drive revenue.
    - Observation: Channels or sub-channels performing below average may need operational focus, marketing campaigns, or portfolio review.
    """


    # ===============================
    # 4. Sales Heatmap: Country vs Channel
    # ===============================
    fig_kpi = px.density_heatmap(
        df,
        x="Country",
        y="Channel",
        z="Sales",
        color_continuous_scale="Blues",
        title="Sales Heatmap: Country vs Channel",
        template="plotly_white"
    )
    figs["Country-Channel Heatmap"] = fig_kpi

    # Insights for Heatmap
    pivot = df.pivot_table(index='Channel', columns='Country', values='Sales', aggfunc='sum').fillna(0)
    max_val = pivot.max().max()
    max_idx = pivot.stack().idxmax()
    # Dynamic Country vs Channel Heatmap Insights
    pivot = df.pivot_table(index='Channel', columns='Country', values='Sales', aggfunc='sum').fillna(0)
    max_val = pivot.max().max()
    max_idx = pivot.stack().idxmax()
    min_val = pivot.min().min()
    min_idx = pivot.stack().idxmin()

    total_comb_sales = pivot.values.sum()
    avg_comb_sales = pivot.values.mean()
    comb_sales_range = max_val - min_val

    max_pct = (max_val / total_comb_sales) * 100
    min_pct = (min_val / total_comb_sales) * 100

    # Top 3 combinations
    top_combs = pivot.stack().sort_values(ascending=False).head(3)
    top_3_combs_list = ", ".join([f"Country: {idx[1]}, Channel: {idx[0]} ({val:,.0f})" for idx, val in top_combs.items()])

    # Count above/below average
    above_avg_combs = (pivot > avg_comb_sales).sum().sum()
    below_avg_combs = (pivot <= avg_comb_sales).sum().sum()

    insights["Country-Channel Heatmap"] = f"""
     Country vs Channel Heatmap Insights
    - Total Sales Across All Combinations: {total_comb_sales:,.0f}
    - Average Sales per Country-Channel Combination: {avg_comb_sales:,.0f}
    - Highest Sales Combination: Country: {max_idx[1]}, Channel: {max_idx[0]} with {max_val:,.0f} ({max_pct:.1f}% of total sales)
    - Lowest Sales Combination: Country: {min_idx[1]}, Channel: {min_idx[0]} with {min_val:,.0f} ({min_pct:.1f}% of total sales)
    - Number of Combinations Above Average: {above_avg_combs}
    - Number of Combinations Below Average: {below_avg_combs}
    - Sales Range (Max - Min): {comb_sales_range:,.0f}
    - Top 3 Country-Channel Combinations: {top_3_combs_list}
    - Interpretation: Heatmap highlights which channels perform best in each country and identifies underperforming areas with potential for growth.
    - **Observation:** Combinations below average may need strategic interventions, marketing campaigns, or operational improvements.
    """


    return figs, insights
