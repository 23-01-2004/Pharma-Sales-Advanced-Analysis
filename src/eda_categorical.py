import pandas as pd
import plotly.express as px

def create_categorical_pie_charts(df):
    """
    Create pie charts for categorical columns with <= 20 unique values
    and generate dynamic insights for each column.
    
    Args:
        df (pandas.DataFrame): Input dataframe
    
    Returns:
        tuple: (figures, insights_dict)
    """
    figures = []
    insights_dict = {}
    
    # Get categorical columns
    cat_cols = df.select_dtypes(include=[object]).columns 
    print("Unique values per categorical column:")
    print(df[cat_cols].nunique())
    
    # Convert Year to numeric if present
    if 'Year' in df.columns:
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
    
    # Create pie charts and insights for each categorical column
    for col in cat_cols:
        if df[col].nunique() <= 20:
            # Group data by Year and categorical column
            grouped_data = df.groupby([col]).size().reset_index(name="Count")
            
            # Create pie chart
            fig = px.pie(
                grouped_data,
                names=col,
                values="Count",
                color=col,
                title=f"Count Plot: {col}",
                template="plotly_dark"
            )
            
            figures.append(fig)
            
            # --- Generate dynamic insights ---
            total_count = grouped_data["Count"].sum()
            top_category = grouped_data.loc[grouped_data["Count"].idxmax(), col]
            top_count = grouped_data["Count"].max()
            
            # Optional: bottom category if more than 1 category
            if grouped_data.shape[0] > 1:
                bottom_category = grouped_data.loc[grouped_data["Count"].idxmin(), col]
                bottom_count = grouped_data["Count"].min()
            else:
                bottom_category, bottom_count = None, None
            
            insight_text = f"""
 Insights for {col}
- Top Category: {top_category} with {top_count} entries ({top_count/total_count*100:.1f}% of total).
""" 
            if bottom_category:
                insight_text += f"- Lowest Category: {bottom_category} with {bottom_count} entries ({bottom_count/total_count*100:.1f}% of total).\n"
            
            insight_text += f"- Shows distribution of {col} in the dataset."
            
            insights_dict[col] = insight_text
    
    return figures, insights_dict
