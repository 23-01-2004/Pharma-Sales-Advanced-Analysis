import pandas as pd
import plotly.express as px

def generate_sales_rep_analysis(df1):
    figs = {}
    insights = {}

    # --- 1. Sales Rep Leaderboard (animated by year) ---
    rep_sales = df1.groupby(["Name of Sales Rep", "Year"])["Sales"].sum().reset_index()
    rep_sales_top10 = (
        rep_sales.groupby("Year")
        .apply(lambda x: x.nlargest(10, "Sales"))
        .reset_index(drop=True)
    )

    fig_rep = px.bar(
        rep_sales_top10,
        x="Sales",
        y="Name of Sales Rep",
        orientation="h",
        title="Top 10 Sales Reps by Revenue (Animated by Year)",
        labels={"Sales": "Total Revenue", "Year": "Year"},
        animation_frame="Year",
        range_x=[0, rep_sales["Sales"].max() * 1.1],
        template="plotly_dark",
        color="Sales",
        color_continuous_scale=px.colors.sequential.Blues,
    )
    figs["Sales Rep Leaderboard"] = fig_rep

    # Insights for Sales Rep Leaderboard
    top_rep_overall = rep_sales.groupby("Name of Sales Rep")["Sales"].sum().idxmax()
    top_rep_sales = rep_sales.groupby("Name of Sales Rep")["Sales"].sum().max()
   # Dynamic Sales Rep Leaderboard Insights
    rep_sales_total = rep_sales.groupby("Name of Sales Rep")["Sales"].sum().reset_index()
    total_sales_all_reps = rep_sales_total["Sales"].sum()
    avg_sales_per_rep = rep_sales_total["Sales"].mean()

    top_rep = rep_sales_total.loc[rep_sales_total["Sales"].idxmax()]
    bottom_rep = rep_sales_total.loc[rep_sales_total["Sales"].idxmin()]

    top_rep_pct = (top_rep["Sales"] / total_sales_all_reps) * 100
    bottom_rep_pct = (bottom_rep["Sales"] / total_sales_all_reps) * 100

    above_avg_reps = rep_sales_total[rep_sales_total["Sales"] > avg_sales_per_rep].shape[0]
    below_avg_reps = rep_sales_total[rep_sales_total["Sales"] <= avg_sales_per_rep].shape[0]

    sales_range = top_rep["Sales"] - bottom_rep["Sales"]

    top_3_reps = rep_sales_total.sort_values("Sales", ascending=False).head(3)
    top_3_reps_list = ", ".join([f"{row['Name of Sales Rep']} ({row['Sales']:,.0f})" for _, row in top_3_reps.iterrows()])

    insights["Sales Rep Leaderboard"] = f"""
    Sales Rep Leaderboard Insights
    - Total Sales Across All Reps: {total_sales_all_reps:,.0f}
    - Average Sales per Rep: {avg_sales_per_rep:,.0f}
    - Top Performing Rep: {top_rep['Name of Sales Rep']} with {top_rep['Sales']:,.0f} ({top_rep_pct:.1f}% of total sales)
    - Lowest Performing Rep: {bottom_rep['Name of Sales Rep']} with {bottom_rep['Sales']:,.0f} ({bottom_rep_pct:.1f}% of total sales)
    - Number of Reps Above Average: {above_avg_reps}
    - Number of Reps Below Average: {below_avg_reps}
    - Sales Range (Top - Bottom Rep): {sales_range:,.0f}
    - Top 3 Reps Overall: {top_3_reps_list}
    - Interpretation: Highlights the most consistent and top-performing reps year over year.
    - Observation: Reps performing below average may benefit from additional support, training, or targeted incentives.
    """


    # --- 2. Sales Team Contribution (Stacked Bar by Year) ---
    team_sales_year = df1.groupby(["Year", "Sales Team"])["Sales"].sum().reset_index()
    fig_team = px.bar(
        team_sales_year,
        x="Year",
        y="Sales",
        color="Sales Team",
        title="Sales Team Contribution to Total Revenue (Stacked by Year)",
        labels={"Sales": "Total Revenue", "Year": "Year", "Sales Team": "Team"},
        template="plotly_dark"
    )
    fig_team.update_layout(barmode='stack')
    figs["Sales Team Contribution"] = fig_team

    # Insights for Sales Team Contribution
    total_sales = team_sales_year.groupby("Year")["Sales"].sum().sum()
    top_team_overall = team_sales_year.groupby("Sales Team")["Sales"].sum().idxmax()
    top_team_sales = team_sales_year.groupby("Sales Team")["Sales"].sum().max()
    # Dynamic Sales Team Contribution Insights
    team_sales_total = team_sales_year.groupby("Sales Team")["Sales"].sum().reset_index()
    total_sales_all_teams = team_sales_total["Sales"].sum()
    avg_sales_per_team = team_sales_total["Sales"].mean()

    top_team = team_sales_total.loc[team_sales_total["Sales"].idxmax()]
    bottom_team = team_sales_total.loc[team_sales_total["Sales"].idxmin()]

    top_team_pct = (top_team["Sales"] / total_sales_all_teams) * 100
    bottom_team_pct = (bottom_team["Sales"] / total_sales_all_teams) * 100

    above_avg_teams = team_sales_total[team_sales_total["Sales"] > avg_sales_per_team].shape[0]
    below_avg_teams = team_sales_total[team_sales_total["Sales"] <= avg_sales_per_team].shape[0]

    sales_range = top_team["Sales"] - bottom_team["Sales"]

    top_3_teams = team_sales_total.sort_values("Sales", ascending=False).head(3)
    top_3_teams_list = ", ".join([f"{row['Sales Team']} ({row['Sales']:,.0f})" for _, row in top_3_teams.iterrows()])

    insights["Sales Team Contribution"] = f"""
    Sales Team Contribution Insights
    - Total Sales Across All Teams: {total_sales_all_teams:,.0f}
    - Average Sales per Team: {avg_sales_per_team:,.0f}
    - Top Performing Team: {top_team['Sales Team']} with {top_team['Sales']:,.0f} ({top_team_pct:.1f}% of total sales)
    - Lowest Performing Team: {bottom_team['Sales Team']} with {bottom_team['Sales']:,.0f} ({bottom_team_pct:.1f}% of total sales)
    - Number of Teams Above Average: {above_avg_teams}
    - Number of Teams Below Average: {below_avg_teams}
    - Sales Range (Top - Bottom Team): {sales_range:,.0f}
    - Top 3 Teams Overall: {top_3_teams_list}
    - Interpretation: Shows team contributions over the years and relative share of revenue.
    - Observation: Teams below average may need additional support, strategic initiatives, or recognition programs to improve performance.
    """


    # --- 3. Manager Effectiveness (Stacked Bar by Year) ---
    manager_df = df1.groupby(["Manager", "Year"])["Sales"].sum().reset_index()
    rep_count = df1.groupby(["Manager", "Year"])["Name of Sales Rep"].nunique().reset_index(name="Rep Count")
    manager_perf = manager_df.merge(rep_count, on=["Manager", "Year"])
    manager_perf["Sales per Rep"] = manager_perf["Sales"] / manager_perf["Rep Count"]

    fig_manager = px.bar(
        manager_perf,
        x="Year",
        y="Sales per Rep",
        color="Manager",
        title="Manager Effectiveness (Average Sales per Rep) Over Years",
        labels={"Sales per Rep": "Average Revenue per Representative", "Year": "Year", "Manager": "Manager"},
        template="plotly_dark"
    )
    fig_manager.update_layout(barmode='stack')
    figs["Manager Effectiveness"] = fig_manager

    # Insights for Manager Effectiveness
    top_manager_overall = manager_perf.groupby("Manager")["Sales per Rep"].mean().idxmax()
    top_manager_avg = manager_perf.groupby("Manager")["Sales per Rep"].mean().max()
    # Dynamic Manager Effectiveness Insights
    manager_total_sales = manager_perf.groupby("Manager")["Sales"].sum().reset_index()
    total_sales_all_managers = manager_total_sales["Sales"].sum()
    avg_sales_per_manager = manager_perf.groupby("Manager")["Sales per Rep"].mean().mean()

    top_manager = manager_perf.groupby("Manager")["Sales per Rep"].mean().idxmax()
    top_manager_avg = manager_perf.groupby("Manager")["Sales per Rep"].mean().max()

    bottom_manager = manager_perf.groupby("Manager")["Sales per Rep"].mean().idxmin()
    bottom_manager_avg = manager_perf.groupby("Manager")["Sales per Rep"].mean().min()

    top_manager_pct = (top_manager_avg / manager_perf["Sales per Rep"].sum()) * 100
    bottom_manager_pct = (bottom_manager_avg / manager_perf["Sales per Rep"].sum()) * 100

    above_avg_managers = manager_perf.groupby("Manager")["Sales per Rep"].mean()[lambda x: x > avg_sales_per_manager].count()
    below_avg_managers = manager_perf.groupby("Manager")["Sales per Rep"].mean()[lambda x: x <= avg_sales_per_manager].count()

    sales_range = top_manager_avg - bottom_manager_avg

    top_3_managers = manager_perf.groupby("Manager")["Sales per Rep"].mean().sort_values(ascending=False).head(3)
    top_3_managers_list = ", ".join([f"{idx} ({val:,.0f})" for idx, val in top_3_managers.items()])

    insights["Manager Effectiveness"] = f"""
    Manager Effectiveness Insights
    - Total Sales Managed by All Managers: {total_sales_all_managers:,.0f}
    - Average Sales per Manager: {avg_sales_per_manager:,.0f}
    - Top Manager Overall: {top_manager} with average sales per rep of {top_manager_avg:,.0f} ({top_manager_pct:.1f}% contribution)
    - Lowest Performing Manager: {bottom_manager} with average sales per rep of {bottom_manager_avg:,.0f} ({bottom_manager_pct:.1f}% contribution)
    - Number of Managers Above Average: {above_avg_managers}
    - Number of Managers Below Average: {below_avg_managers}
    - Sales per Rep Range (Top - Bottom Manager): {sales_range:,.0f}
    - Top 3 Managers Overall: {top_3_managers_list}
    - Interpretation: Stack bar shows yearly performance and contribution per manager, highlighting those excelling in maximizing rep productivity.
    - Observation: Managers below average may need additional training, coaching, or strategic support to improve team performance.
    """

    return figs, insights
