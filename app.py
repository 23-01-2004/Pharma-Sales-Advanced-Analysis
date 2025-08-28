import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import numpy as np

# Import your existing modules
from src.eda_stats import summary_statistics
from src.eda_categorical import create_categorical_pie_charts
from src.top_products_pipeline import top_products_chart
from src.bivariate_analysis import sales_analysis_charts
from src.multivariate_analysis import multivariate_plotly_charts
from src.sales_analysis import generate_sales_analysis
from src.time_series_pipeline import generate_time_series_analysis
from src.geospatial_analysis import generate_geographical_sales_analysis
from src.sales_force_analysis import generate_sales_rep_analysis
from src.channel_analysis import generate_channel_analysis
from src.product_analysis import generate_product_analysis
from src.Customer_Segmentation import RFMAnalyzer


def load_custom_css():
    """Load custom CSS styling for the dashboard"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: #000000;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #000000;
        color: white;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c5aa0 0%, #1e3c72 100%);
        border-right: 2px solid rgba(255,255,255,0.1);
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
        background-size: 300% 300%;
        animation: gradient 8s ease infinite;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        font-weight: 300;
    }
    
    /* Cards and containers */
    .metric-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    
    .info-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    p, div, span {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 0.5rem;
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: rgba(255,255,255,0.7);
        font-weight: 500;
        padding: 0.75rem 1.5rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* File uploader styling */
    .stFileUploader {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 2rem;
        border: 2px dashed rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: #4ecdc4;
        background: rgba(255,255,255,0.15);
    }
    
    /* DataFrames */
    .stDataFrame > div {
        background: rgba(0,0,0,0.8) !important;
        color: white !important;
        border: 1px solid rgba(78, 205, 196, 0.3);
    }
    
    .stDataFrame table {
        background: rgba(0,0,0,0.8) !important;
        color: white !important;
    }
    
    .stDataFrame th {
        background: rgba(78, 205, 196, 0.7) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .stDataFrame td {
        background: rgba(0,0,0,0.8) !important;
        color: white !important;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    
    .stDataFrame tr:nth-child(even) td {
        background: rgba(255,255,255,0.05) !important;
    }
    
    .stDataFrame tr:hover td {
        background: rgba(78, 205, 196, 0.2) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    /* Custom metrics */
    .custom-metric {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        border-radius: 15px;
        margin: 0.5rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .custom-metric h3 {
        color: #4ecdc4 !important;
        font-size: 2rem;
        margin: 0;
        font-weight: 700;
    }
    
    .custom-metric p {
        color: rgba(255,255,255,0.8) !important;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Sidebar improvements */
    .sidebar-info {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Animation classes */
    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.6s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2rem;
        }
        .main-header p {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def create_header():
    """Create the main header section"""
    st.markdown("""
    <div class="main-header fade-in">
        <h1>Sales Data Analysis</h1>
        <p>Unlock insights from your data with powerful analytics and beautiful visualizations</p>
    </div>
    """, unsafe_allow_html=True)


def create_sidebar_info():
    """Create sidebar information and features"""
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-info">
            <h3>Dashboard Features</h3>
            <ul style="color: rgba(255,255,255,0.9);">
                <li>Interactive Visualizations</li>
                <li>Comprehensive EDA</li>
                <li>Statistical Analysis</li>
                <li>Geospatial Mapping</li>
                <li>Time Series Analysis</li>
                <li>Performance Metrics</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        with st.expander("Pro Tips", expanded=False):
            st.markdown("""
            **For best results:**
            - Use CSV files with proper headers
            - Include date columns for time analysis
            - Ensure numeric columns for statistics
            - Check for missing values beforehand
            """)
        
        with st.expander("Data Requirements", expanded=False):
            st.markdown("""
            **Expected columns (optional):**
            - Sales/Revenue data
            - Date/Time columns
            - Geographic information
            - Product categories
            - Channel information
            """)


def create_file_upload_section():
    """Create file upload section with styling"""
    st.markdown("""
    <div class="info-card slide-up">
        <h3>📂 Upload Your Dataset</h3>
        <p>Start your data exploration journey by uploading a CSV file. Our dashboard will automatically detect and analyze your data structure.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            help="Upload a CSV file to begin analysis. Maximum file size: 200MB"
        )
    return uploaded_file


def create_dataset_overview(df):
    """Create comprehensive dataset overview"""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Quick metrics
    num_rows, num_cols = df.shape
    missing_count = df.isnull().sum().sum()
    numeric_cols = len(df.select_dtypes(include=[np.number]).columns)
    categorical_cols = len(df.select_dtypes(include=['object', 'category']).columns)
    
    # Create metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="custom-metric">
            <h3>{num_rows:,}</h3>
            <p>Observations</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="custom-metric">
            <h3>{num_cols}</h3>
            <p>Attributes</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Exclude longitude, latitude, year from numeric count
    numeric_count = numeric_cols - 3
    with col3:
        st.markdown(f"""
        <div class="custom-metric">
            <h3>{numeric_count}</h3>
            <p>Numeric Features</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="custom-metric">
            <h3>{categorical_cols}</h3>
            <p>Categorical Features</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("*Note: 'longitude' & 'latitude' are coordinates, 'Year' is a time feature, so they are not considered as numeric features.*")
    
    # Data quality indicator
    if missing_count == 0:
        st.success("Perfect! No missing values detected in your dataset.")
    elif missing_count < num_rows * 0.05:
        st.info(f"Good data quality: Only {(missing_count/(num_rows*num_cols)*100):.1f}% missing values.")
    else:
        st.warning(f"Attention: {(missing_count/(num_rows*num_cols)*100):.1f}% missing values detected. Consider data cleaning.")
    
    # Sample data preview
    with st.expander("Dataset Preview (First 10 Rows)", expanded=True):
        table_html = df.head(10).to_html(index=False, table_id="preview-table")
  
        st.markdown(
            f"""
            <div style="height: 300px; overflow: auto; border: 1px solid #444; border-radius: 5px; padding: 10px;">
                <style>
                    #preview-table {{
                        width: 100%;
                        border-collapse: collapse;
                        color: white;
                        background-color: #1e1e1e;
                    }}
                    #preview-table th, #preview-table td {{
                        border: 1px solid #444;
                        padding: 8px;
                        text-align: left;
                    }}
                    #preview-table th {{
                        background-color: #4ecdc4;
                        color: black;
                        position: sticky;
                        top: 0;
                    }}
                </style>
                {table_html}
            </div>
            """,
            unsafe_allow_html=True
        )  
    # Column information
    col1, col2 = st.columns(2)
    
    with col1:
        with st.expander("Column Data Types", expanded=True):
            dtype_df = pd.DataFrame({
                'Column': df.columns,
                'Data Type': df.dtypes.astype(str),
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum()
            }).reset_index(drop=True)
            st.markdown(dtype_df.to_markdown(index=False))
    
    with col2:
        key_columns = ['Country', 'Product Class', 'Channel', 'Distributor']
        available_columns = [col for col in key_columns if col in df.columns]
        if available_columns:
            with st.expander("Key Categories Summary", expanded=True):
                for col in available_columns:
                    unique_count = df[col].nunique()
                    st.metric(label=f"Unique {col}s", value=unique_count)
    
    st.markdown("</div>", unsafe_allow_html=True)


def create_enhanced_tabs(df):
    """Create enhanced tabs with analysis functions"""
    tab_config = [
        ("Overview", "Dataset structure and key metrics"),
        ("Statistics", "Descriptive statistics and distributions"),
        ("Categorical Analysis", "Categorical data analysis"),
        ("Top Products", "Best performing products"),
        ("Numerical Analysis", "Numerical data relationships"),
        ("Multivariate Analysis", "Multi-dimensional analysis"),
        ("Sales Analysis", "Revenue and quantity insights"),
        ("Time Series Analysis", "Trends and growth patterns"),
        ("Geographical Analysis", "Location-based performance"),
        ("Sales Force Analysis", "Team and rep performance"),
        ("Products Analysis", "Product performance deep-dive"),
        ("Customer Segmentation", "Segmentation of Customers")
    ]
    
    tab_names = [config[0] for config in tab_config]
    tabs = st.tabs(tab_names)
    
    # Overview Tab
    with tabs[0]:
        st.markdown("### Dataset Overview & Key Insights")
        create_dataset_overview(df)
        
        # Additional insights
        if len(df.select_dtypes(include=[np.number]).columns) > 0:
            st.markdown("### Quick Statistical Insights")
            numeric_df = df.select_dtypes(include=[np.number])
            col1, col2 = st.columns(2)
            
            with col1:
                if len(numeric_df.columns) > 1:
                    corr_matrix = numeric_df.corr()
                    fig = px.imshow(
                        corr_matrix,
                        title="Feature Correlation Matrix",
                        color_continuous_scale="RdBu",
                        aspect="auto"
                    )
                    fig.update_layout(
                        height=400,
                        title_font_size=16,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if 'Sales' in numeric_df.columns or 'Revenue' in numeric_df.columns:
                    sales_col = 'Sales' if 'Sales' in numeric_df.columns else 'Revenue'
                    fig = px.histogram(
                        df,
                        x=sales_col,
                        title=f"Distribution of {sales_col}",
                        nbins=30,
                        color_discrete_sequence=['#4ecdc4']
                    )
                    fig.update_layout(
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white')
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics Tab
    with tabs[1]:
        st.markdown("### Comprehensive Statistical Analysis")
        with st.spinner("Generating statistical insights..."):
            try:
                stats_df = summary_statistics(df)
                stats_df = stats_df.drop(columns=["Latitude", "Longitude", "Year"], errors="ignore")
                
                # Add additional statistics
                stats_df.loc['mean'] = df.mean(numeric_only=True)
                stats_df.loc['median'] = df.median(numeric_only=True)
                stats_df.loc['mode'] = df.mode(numeric_only=True).iloc[0]
                
                st.markdown("#### Summary Statistics Table")
                st.markdown(stats_df.to_markdown(index=True))
                
                # Automated Insights
                st.markdown("#### Automated Insights")
                try:
                    insights = []
                    exclude_cols = ["Latitude", "Longitude", "Year"]
                    numeric_cols = [col for col in df.select_dtypes(include="number").columns if col not in exclude_cols]
                    
                    for col in numeric_cols:
                        col_mean = df[col].mean()
                        col_median = df[col].median()
                        col_min = df[col].min()
                        col_max = df[col].max()
                        skew = "right-skewed" if col_mean > col_median else "left-skewed"
                        
                        insights.append(
                            f"**{col}**:\n"
                            f"- The **mean** (average value) is **{col_mean:.2f}**, which shows the central tendency of {col}\n"
                            f"- The **median** (middle value when sorted) is **{col_median:.2f}**, useful when data is skewed.\n"
                            f"- The **minimum** observed value is **{col_min:.2f}**, and the **maximum** is **{col_max:.2f}**, "
                            f"indicating the overall range of {col}.\n"
                            f"- The distribution appears to be **{skew}** based on mean vs median.\n"
                        )
                    
                    st.markdown("\n".join(insights))
                except Exception as e:
                    st.error(f"Error generating insights: {e}")
                    
            except Exception as e:
                st.error(f"Error generating statistics: {str(e)}")
                st.markdown("#### Basic Statistics (Fallback)")
                basic_stats = df.describe()
                st.dataframe(basic_stats, use_container_width=True, height=400)
    
    # Categorical Analysis Tab
    with tabs[2]:
        st.markdown("### Pie Charts for Categorical Features")
        pie_charts, pie_insights = create_categorical_pie_charts(df)
        
        pie_cols = list(pie_insights.keys())
        for i in range(0, len(pie_charts), 2):
            cols = st.columns(2)
            
            cols[0].plotly_chart(pie_charts[i], use_container_width=True)
            cols[0].markdown(f"**Insights:**\n{pie_insights[pie_cols[i]]}")
            
            if i + 1 < len(pie_charts):
                cols[1].plotly_chart(pie_charts[i + 1], use_container_width=True)
                cols[1].markdown(f"**Insights:**\n{pie_insights[pie_cols[i + 1]]}")
    
    # Top Products Tab
    with tabs[3]:
        st.markdown("### Top Performing Products")
        with st.spinner("Analyzing product performance..."):
            try:
                fig = top_products_chart(df)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("#### Automated Insights")
                product_sales = df.groupby("Product Name")["Sales"].sum().reset_index()
                product_sales = product_sales.sort_values(by="Sales", ascending=False)
                top_product = product_sales.iloc[0]
                bottom_product = product_sales.iloc[-1]
                total_sales = product_sales["Sales"].sum()
                top_share = (top_product["Sales"] / total_sales) * 100
                bottom_share = (bottom_product["Sales"] / total_sales) * 100
                
                insights = []
                insights.append(
                    f"- The top-performing product is **{top_product['Product Name']}**, "
                    f"contributing **{top_product['Sales']:.2f} units** "
                    f"({top_share:.2f}% of total sales)."
                )
                insights.append(
                    f"- The lowest-performing product is **{bottom_product['Product Name']}**, "
                    f"with only **{bottom_product['Sales']:.2f} units** "
                    f"({bottom_share:.2f}% of total sales)."
                )
                insights.append(
                    f"- The dataset contains **{len(product_sales)} unique products**. "
                    f"The top 10 products together contribute "
                    f"**{product_sales.head(10)['Sales'].sum()/total_sales*100:.2f}%** of total sales."
                )
                
                st.markdown("\n".join(insights))
            except Exception as e:
                st.error(f"Error analyzing top products: {e}")
    
    # Remaining tabs with analysis functions
    analysis_configs = [
        (4, "sales_analysis_charts", "Bivariate Relationships"),
        (5, "multivariate_plotly_charts", "Multi-dimensional Analysis"),
        (6, "generate_sales_analysis", "Revenue & Quantity Deep-dive"),
        (7, "generate_time_series_analysis", "Time Series & Growth Trends"),
        (8, "generate_geographical_sales_analysis", "Geographic Performance Map"),
        (9, "generate_sales_rep_analysis", "Sales Team Performance"),
        (10, "generate_product_analysis", "Advanced Product Analytics")
    ]
    
    for tab_idx, function_name, title in analysis_configs:
        with tabs[tab_idx]:
            st.markdown(f"### {title}")
            with st.spinner(f"Generating {title.lower()}..."):
                try:
                    if function_name == "sales_analysis_charts":
                        figs, insights = sales_analysis_charts(df)
                        if figs:
                            cols = st.columns(2)
                            fig_keys = list(figs.keys())
                            for idx, key in enumerate(fig_keys):
                                with cols[idx % 2]:
                                    st.plotly_chart(figs[key], use_container_width=True)
                                    if insights and key in insights:
                                        st.markdown(insights[key])
                    
                    elif function_name in ["multivariate_plotly_charts", "generate_sales_analysis"]:
                        func = globals()[function_name]
                        figs, insights = func(df)
                        if figs:
                            for key, fig in figs.items():
                                st.plotly_chart(fig, use_container_width=True)
                                if key in insights:
                                    st.markdown(f"**Insights for {key}:**\n{insights[key]}")
                    
                    elif function_name in ["generate_time_series_analysis", "generate_geographical_sales_analysis", 
                                         "generate_sales_rep_analysis", "generate_product_analysis"]:
                        func = globals()[function_name]
                        figs, insights = func(df)
                        analysis_tabs = st.tabs(list(figs.keys()))
                        for i, key in enumerate(figs.keys()):
                            with analysis_tabs[i]:
                                st.plotly_chart(figs[key], use_container_width=True)
                                st.markdown(
                                    f"""
                                    <div style="background-color:#1e1e1e; padding:15px; border-radius:10px;
                                                border:1px solid #333; color:white; font-size:15px;">
                                        <b>Insights:</b>
                                        <ul>
                                            {''.join([f"<li>{line.strip('- ').strip()}</li>" for line in insights[key].splitlines() if line.strip()])}
                                        </ul>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                
                except Exception as e:
                    st.error(f"Error generating {title.lower()}: {str(e)}")
    
    # Customer Segmentation Tab
    with tabs[11]:
        st.markdown("### Customer Segmentation (RFM Analysis)")
        
        # Check for required columns
        base_required_columns = ['Customer Name', 'Sales']
        date_columns_options = ['Date', ['Month', 'Year']]
        
        # Check if we have Customer Name and Sales
        missing_base_cols = [col for col in base_required_columns if col not in df.columns]
        
        # Check for date columns - either 'Date' or both 'Month' and 'Year'
        has_date_column = 'Date' in df.columns
        has_month_year = 'Month' in df.columns and 'Year' in df.columns
        
        if missing_base_cols or (not has_date_column and not has_month_year):
            missing_info = []
            if missing_base_cols:
                missing_info.extend(missing_base_cols)
            if not has_date_column and not has_month_year:
                missing_info.append("Date column (either 'Date' or both 'Month' and 'Year')")
            
            st.warning(f"Required columns for RFM analysis are missing: {', '.join(missing_info)}. "
                      f"Please ensure your data includes 'Customer Name', 'Sales', and either a 'Date' column or both 'Month' and 'Year' columns.")
        else:
            # Create a working copy of the dataframe
            df_rfm = df.copy()
            
            # Create Date column if it doesn't exist but Month and Year do
            if not has_date_column and has_month_year:
                st.info("Creating Date column from Month and Year columns...")
                try:
                    # Handle both numeric months (1-12) and month names (January, February, etc.)
                    if df_rfm['Month'].dtype == 'object':
                        # Month column contains text names - convert to datetime using month names
                        df_rfm['Date'] = pd.to_datetime(df_rfm['Month'].astype(str) + ' ' + df_rfm['Year'].astype(str), format='%B %Y')
                    else:
                        # Month column contains numeric values - create date with day=1
                        df_rfm['Date'] = pd.to_datetime(df_rfm[['Year', 'Month']].assign(Day=1))
                    
                    st.success("Date column created successfully from Month and Year!")
                except Exception as e:
                    # Try alternative approach if the first method fails
                    try:
                        # Alternative: Use a more flexible datetime parser
                        df_rfm['Month_Year'] = df_rfm['Month'].astype(str) + ' ' + df_rfm['Year'].astype(str)
                        df_rfm['Date'] = pd.to_datetime(df_rfm['Month_Year'], errors='coerce')
                        # Remove the temporary column
                        df_rfm.drop('Month_Year', axis=1, inplace=True)
                        st.success("Date column created successfully using alternative method!")
                    except Exception as e2:
                        st.error(f"Error creating Date column from Month and Year: {e2}")
                        st.error("Please check that your Month column contains valid month names (e.g., 'January', 'February') or numbers (1-12), and Year column contains valid years.")
                        
                        # Show sample data for debugging
                        with st.expander("Sample Data for Debugging"):
                            st.write("Sample Month values:", df_rfm['Month'].head(10).tolist())
                            st.write("Sample Year values:", df_rfm['Year'].head(10).tolist())
                            st.write("Month column type:", df_rfm['Month'].dtype)
                            st.write("Year column type:", df_rfm['Year'].dtype)
                        st.stop()
            
            # Ensure Date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(df_rfm['Date']):
                try:
                    df_rfm['Date'] = pd.to_datetime(df_rfm['Date'])
                except Exception as e:
                    st.error(f"Error converting 'Date' column to datetime: {e}. "
                            f"Please ensure the date data is in a standard format.")
                    st.stop()
            
            with st.spinner("Running Customer Segmentation Analysis (RFM + Clustering)..."):
                try:
                    analyzer = RFMAnalyzer()
                    analyzer.df = df_rfm.copy()
                    
                    # Basic preprocessing
                    initial_rows = len(analyzer.df)
                    analyzer.df.drop_duplicates(inplace=True)
                    analyzer.df.dropna(subset=['Customer Name', 'Sales'], inplace=True)
                    
                    # Display preprocessing info
                    if initial_rows > len(analyzer.df):
                        st.info(f"Removed {initial_rows - len(analyzer.df)} duplicate/missing rows. "
                               f"Working with {len(analyzer.df)} clean records.")
                    
                    # Calculate RFM and perform clustering
                    analyzer.calculate_rfm()
                    analyzer.perform_clustering()
                    
                    # Generate visualizations
                    elbow_fig = analyzer.plot_elbow_method()
                    dashboard_fig = analyzer.generate_dashboard()
                    top_customers_df, cluster_summary_df = analyzer.print_summary() # <-- NEW LINE                    
                    st.success("Customer Segmentation Analysis Completed!")
                    
                    st.plotly_chart(elbow_fig, use_container_width=True)
                    st.plotly_chart(dashboard_fig, use_container_width=True)
                    
                    # Summary Tables
                    # Summary Tables
                    # Summary Tables
                    # Summary Tables
                    st.markdown("#### Analysis Summary")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("**Top Customers by Monetary Value**")
                        # Convert DataFrame to Markdown table string
                        top_customers_md = top_customers_df.to_markdown(index=True) # Include index (Rank)
                        st.markdown(f"```\n{top_customers_md}\n```")

                    with col2:
                        st.markdown("**Cluster Summary (Averages)**")
                        # Convert DataFrame to Markdown table string
                        cluster_summary_md = cluster_summary_df.to_markdown(index=False) # Exclude index
                        st.markdown(f"```\n{cluster_summary_md}\n```")
                                        
                        # Show date range used in analysis
                        date_range = f"Date range: {df_rfm['Date'].min().strftime('%Y-%m-%d')} to {df_rfm['Date'].max().strftime('%Y-%m-%d')}"
                        st.info(date_range)
                        
                        # Download results
                        csv = analyzer.rfm_df.to_csv(index=False)
                        st.download_button(
                            label="Download Segmentation Results (CSV)",
                            data=csv,
                            file_name='customer_segmentation_results.csv',
                            mime='text/csv',
                        )
                        
                except Exception as e:
                    st.error(f"An error occurred during Customer Segmentation: {e}")
                    # Show debug information
                    with st.expander("Debug Information"):
                        st.write("Available columns:", df_rfm.columns.tolist())
                        st.write("Data types:")
                        st.write(df_rfm.dtypes)
                        if 'Date' in df_rfm.columns:
                            st.write("Date column sample:", df_rfm['Date'].head())


def create_footer():
    """Create footer section"""
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: rgba(255,255,255,0.05); 
                border-radius: 15px; margin-top: 2rem;">
        <h4>Advanced EDA Dashboard</h4>
        <p>Built using Streamlit | Powered by Python & Plotly</p>
        <p style="font-size: 0.8rem; opacity: 0.7;">Dashboard version 2.0</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="Advanced EDA Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo',
            'Report a bug': "https://github.com/your-repo/issues",
            'About': "# Advanced EDA Dashboard\nPowerful data exploration made easy!"
        }
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Create header
    create_header()
    
    # Create sidebar
    create_sidebar_info()
    
    # File upload section
    uploaded_file = create_file_upload_section()
    
    if uploaded_file is not None:
        try:
            # Load data with progress
            with st.spinner("Loading your dataset..."):
                df = pd.read_csv(uploaded_file)
            
            # Success message
            st.success(f"Dataset loaded successfully! {len(df):,} rows × {len(df.columns)} columns")
            
            # Enhanced usage guide
            with st.expander("How to Use This Dashboard", expanded=False):
                st.markdown("""
                <div class="info-card">
                    <h4>Quick Start Guide</h4>
                    **1. Overview Tab**
                    - Get instant insights about your dataset structure
                    - View data quality metrics and sample data
                    - Understand column types and missing values
                    
                    **2. Analysis Tabs**
                    - Navigate through specialized analysis sections
                    - Each tab focuses on specific data aspects
                    - Interactive charts with hover details and animations
                    
                    **3. Interactive Features**
                    - Hover over charts for detailed information
                    - Use play buttons on animated charts
                    - Expand sections for deeper insights
                    - Export visualizations using chart toolbar
                    
                    **4. Pro Tips**
                    - Start with Overview for data understanding
                    - Use Time Series for temporal patterns
                    - Check Geographic analysis for location insights
                    - Compare metrics across different dimensions
                </div>
                """, unsafe_allow_html=True)
            
            # Create enhanced tabs
            create_enhanced_tabs(df)
            
        except Exception as e:
            st.error(f"Error loading dataset: {str(e)}")
            st.info("Please ensure your CSV file is properly formatted with headers.")
            
            # Show common issues
            with st.expander("Common Issues & Solutions"):
                st.markdown("""
                **File Format Issues:**
                - Ensure file has `.csv` extension
                - Check for proper comma separation
                - Verify encoding (UTF-8 recommended)
                
                **Data Structure:**
                - First row should contain column headers
                - Avoid special characters in column names
                - Check for consistent data types in columns
                
                **File Size:**
                - Maximum recommended size: 200MB
                - Consider sampling large datasets
                - Remove unnecessary columns before upload
                """)
    else:
        # Enhanced landing page when no file is uploaded
        st.markdown("""
        <div class="info-card fade-in">
            <h3>Welcome to Advanced EDA Dashboard</h3>
            <p>Transform your data analysis experience with our comprehensive exploratory data analysis tool.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Feature showcase
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4>Smart Analytics</h4>
                <p>Automated statistical analysis, correlation detection, and distribution insights with interactive visualizations.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4>Beautiful Visuals</h4>
                <p>Professional-grade charts with animations, hover effects, and customizable color schemes.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4>Lightning Fast</h4>
                <p>Optimized performance for large datasets with efficient processing and caching.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Sample dataset suggestions
        st.markdown("### Try with Sample Data")
        st.info("""
        **Don't have a dataset?** Try these sample datasets:
        - Sales performance data with geographic and temporal dimensions
        - Customer analytics with demographic and behavioral features
        - Product performance metrics across multiple channels
        - Time series data with seasonal patterns
        """)
        
        # What makes this dashboard special
        with st.expander("What Makes This Dashboard Special", expanded=False):
            st.markdown("""
            **Advanced Features:**
            - **Smart Data Detection**: Automatically identifies data types and suggests analyses
            - **Interactive Animations**: Time-based animations show data evolution
            - **Multi-dimensional Analysis**: Explore relationships across multiple variables
            - **Geographic Insights**: Built-in mapping for location-based data
            - **Performance Optimized**: Handles large datasets efficiently
            - **Export Ready**: Download insights and visualizations
            
            **Perfect For:**
            - Business analysts exploring sales data
            - Data scientists conducting initial analysis
            - Researchers analyzing survey data
            - Students learning data analysis
            - Anyone wanting to understand their data better
            
            **Supported Analysis Types:**
            - Descriptive statistics and distributions
            - Correlation and relationship analysis
            - Time series and trend analysis
            - Geographic and spatial analysis
            - Categorical data exploration
            - Performance benchmarking
            """)
    
    # Footer
    create_footer()


def create_download_section(df):
    """Create a section for downloading processed data and insights"""
    st.markdown("### Download Your Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Download Summary Stats"):
            stats_df = summary_statistics(df)
            csv = stats_df.to_csv(index=True)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"summary_stats_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Download Data Profile"):
            # Create a comprehensive data profile
            profile_data = {
                'Observations': [len(df)],
                'Attributes': [len(df.columns)],
                'Missing_Values': [df.isnull().sum().sum()],
                'Numeric_Columns': [len(df.select_dtypes(include=[np.number]).columns)],
                'Categorical_Columns': [len(df.select_dtypes(include=['object', 'category']).columns)],
                'Memory_Usage_MB': [df.memory_usage(deep=True).sum() / 1024 / 1024]
            }
            profile_df = pd.DataFrame(profile_data)
            csv = profile_df.to_csv(index=False)
            st.download_button(
                label="Download Profile",
                data=csv,
                file_name=f"data_profile_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col3:
        if st.button("Generate Report"):
            st.info("Comprehensive report generation coming soon!")


def add_performance_monitoring():
    """Add performance monitoring for large datasets"""
    if 'performance_metrics' not in st.session_state:
        st.session_state.performance_metrics = {
            'load_time': 0,
            'analysis_time': 0,
            'memory_usage': 0
        }


def create_advanced_filters(df):
    """Create advanced filtering options for large datasets"""
    st.sidebar.markdown("### Advanced Filters")
    
    # Date range filter if date columns exist
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        date_col = st.sidebar.selectbox("Select Date Column", date_cols)
        if date_col:
            min_date = df[date_col].min()
            max_date = df[date_col].max()
            date_range = st.sidebar.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
    
    # Numeric filters
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        selected_numeric = st.sidebar.selectbox("Filter by Numeric Column", ["None"] + list(numeric_cols))
        if selected_numeric != "None":
            min_val, max_val = float(df[selected_numeric].min()), float(df[selected_numeric].max())
            filter_range = st.sidebar.slider(
                f"{selected_numeric} Range",
                min_val, max_val, (min_val, max_val)
            )
    
    # Categorical filters
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) > 0:
        selected_cat = st.sidebar.selectbox("Filter by Category", ["None"] + list(cat_cols))
        if selected_cat != "None":
            unique_values = df[selected_cat].unique()
            if len(unique_values) <= 50:  # Only show multiselect for reasonable number of options
                selected_values = st.sidebar.multiselect(
                    f"Select {selected_cat} values",
                    unique_values,
                    default=unique_values[:10] if len(unique_values) > 10 else unique_values
                )


def create_data_quality_dashboard(df):
    """Create a comprehensive data quality assessment"""
    st.markdown("### Data Quality Assessment")
    
    # Calculate quality metrics
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    
    # Quality score calculation
    quality_factors = {
        'Completeness': completeness,
        'Uniqueness': (df.drop_duplicates().shape[0] / df.shape[0]) * 100,
        'Consistency': 100 - (df.select_dtypes(include=['object']).apply(lambda x: x.str.strip()).isna().sum().sum() / df.select_dtypes(include=['object']).size * 100) if len(df.select_dtypes(include=['object']).columns) > 0 else 100
    }
    
    # Overall quality score
    overall_quality = sum(quality_factors.values()) / len(quality_factors)
    
    # Display quality metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Quality Score", f"{overall_quality:.1f}%",
                 delta="Excellent" if overall_quality > 90 else "Good" if overall_quality > 75 else "Needs Improvement")
    
    with col2:
        st.metric("Data Completeness", f"{completeness:.1f}%")
    
    with col3:
        duplicate_pct = (1 - df.drop_duplicates().shape[0] / df.shape[0]) * 100
        st.metric("Duplicate Records", f"{duplicate_pct:.1f}%")
    
    with col4:
        outlier_cols = df.select_dtypes(include=[np.number]).columns
        outliers = 0
        for col in outlier_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers += ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        outlier_pct = (outliers / len(df)) * 100
        st.metric("Potential Outliers", f"{outlier_pct:.1f}%")


# Run the main application
if __name__ == "__main__":
    main()