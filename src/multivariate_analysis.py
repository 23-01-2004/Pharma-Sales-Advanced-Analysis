# src/bivariate_plotly.py

import plotly.express as px
import pandas as pd
import streamlit as st 

def multivariate_plotly_charts(df1):
    st.subheader("Multivariate Analysis")

    figs = {}
    insights = {}

    # === 1. Scatter plot: Quantity vs Sales ===
    if "Quantity" in df1.columns and "Sales" in df1.columns:
        fig_qs = px.scatter(
            df1,
            x="Quantity",
            y="Sales",
            title="Quantity vs Sales",
            opacity=0.6,
            color="Sales",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        figs["Quantity vs Sales"] = fig_qs
        # st.plotly_chart(fig_qs, use_container_width=True, key="scatter_quantity_sales")

        corr_qs = df1["Quantity"].corr(df1["Sales"])
        strength = (
            "Strong" if abs(corr_qs) >= 0.7
            else "Moderate" if abs(corr_qs) >= 0.3
            else "Weak"
        )

        direction = (
            "🔺 Positive" if corr_qs > 0
            else "🔻 Negative" if corr_qs < 0
            else "⚖️ No"
        )

        interpretation = (
            "Higher quantities tend to drive higher sales."
            if corr_qs > 0.3 else
            "Weak relationship — sales may depend on other factors."
        )
        insights["Quantity vs Sales"] = f"""
        - Correlation: `{corr_qs:.2f}` <br>
        - {direction} relationship detected <br>
        - Strength: **{strength}** <br>
        - Interpretation: {interpretation}
        """

        # st.markdown(insights, unsafe_allow_html=True)
        # st.markdown(f"**🔍 Insights: Quantity vs Sales**\n{insights['Quantity vs Sales']}")

    # === 2. Scatter plot: Price vs Sales ===
    if "Price" in df1.columns and "Sales" in df1.columns:
        fig_ps = px.scatter(
            df1,
            x="Price",
            y="Sales",
            title="Price vs Sales",
            opacity=0.6,
            color="Sales",
            color_continuous_scale="Blues",
            template="plotly_dark"
        )
        figs["Price vs Sales"] = fig_ps
        # st.plotly_chart(fig_ps, use_container_width=True, key="scatter_price_sales")

        corr_ps = df1["Price"].corr(df1["Sales"])
        strength = (
            "Strong" if abs(corr_qs) >= 0.7
            else "Moderate" if abs(corr_qs) >= 0.3
            else "Weak"
        )

        direction = (
            "🔺 Positive" if corr_qs > 0
            else "🔻 Negative" if corr_qs < 0
            else "⚖️ No"
        )

        interpretation = (
            "Higher quantities tend to drive higher sales."
            if corr_qs > 0.3 else
            "Weak relationship — sales may depend on other factors."
        )
        insights["Price vs Sales"] = f"""
         - Correlation: `{corr_qs:.2f}` <br>
        - {direction} relationship detected <br>
        - Strength: **{strength}** <br>
        - Interpretation: {interpretation}
        """
        # st.markdown(f"**🔍 Insights: Price vs Sales**\n{insights['Price vs Sales']}")

    # === 3. Correlation Heatmap ===
    if set(["Quantity", "Price", "Sales"]).issubset(df1.columns):
        corr_matrix = df1[["Quantity", "Price", "Sales"]].corr()

        fig_corr = px.imshow(
            corr_matrix,
            text_auto=".2f",
            color_continuous_scale="Blues",
            title="Correlation Heatmap: Quantity, Price, Sales",
            template="plotly_dark"
        )
        fig_corr.update_layout(width=800, height=600)
        figs["Correlation Heatmap"] = fig_corr
        # st.plotly_chart(fig_corr, use_container_width=True, key="heatmap_corr")

        insights["Correlation Heatmap"] = f"""
        - Quantity vs Sales: `{corr_matrix.loc['Quantity', 'Sales']:.2f}` <br>
        - Price vs Sales: `{corr_matrix.loc['Price', 'Sales']:.2f}`<br>
        - Quantity vs Price: `{corr_matrix.loc['Quantity', 'Price']:.2f}`<br>
        - Values closer to **+1/-1** show stronger relationships, while values near **0** show weak/no correlation.
        """
        # st.markdown(f"**🔍 Insights: Correlation Heatmap**\n{insights['Correlation Heatmap']}")

    return figs, insights  # ✅ Always return both
