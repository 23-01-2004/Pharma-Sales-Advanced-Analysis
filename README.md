# Pharma-Sales-Advanced-Analysis


This project provides an **interactive Pharma Sales Analysis Dashboard** built with **Streamlit** and **Plotly**.  
It enables advanced data exploration, statistical insights, and visualization of sales trends for better decision-making.

---
## How to run locally 

Follow the steps below to set up and run the project on your locan enviroment : 

1. **Clone the Repository**
   ```bash
   git clone https://github.com/23-01-2004/Pharma-Sales-Advanced-Analysis.git
   cd pharma-sales-analysis
    ```
2. **Create a virtual enviroment**
   ```bash
   conda create -n pharma_env
   conda activate
   ```
3. **Install dependencies**
   ```bash
   pip install requirements.txt
   ```
4. **Run the Streamlit App**
   ```bash
   streamlit run app.py
   ```

# Dataset Info : 

The dataset used in this analysis contains pharmaceutical sales data recorded over multiple years. It includes details such as : 


   ### Why Plotly Instead of Matplotlib?

_I chose Plotly over Matplotlib for the following reasons:_

 **Interactivity** – Users can hover, zoom, and filter directly within the charts, also essential information is not always possible with static display so one can hover over a particular plot for additional infographics without making the overall plot cluttered. 

 **Dynamic Dashboards** – Works seamlessly with Streamlit for real-time updates, although matplotlib also does. But the difference lies in real time dynamic change of data properly affecting the plots which I saw was much more evident in case of Plotly. 

 **Better Aesthetics** – Offers cleaner, modern, and more engaging visuals, with an array of templates, animations and color continous scale features. 

 **Ease of Integration** – Supports multiple chart types (line, bar, pie, scatter, jitter plots) with minimal code, even useful during trend analysis for time series decomposition and YoY Growth factor of different channels and sub-channels. 

Matplotlib is excellent for static plots, but Plotly brings exploratory power and engagement for end users.

# Advanced Analysis Features : 
This project covers many advanced analysis features on the **Pharma Data** : 

| Feature                             | Description                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------- |
| **Exploratory Data Analysis (EDA)** | Provides dataset overview along with dynamic insights for every analysis done.                |
| **Data Description**                | Observations, Attributes, Categorical, Numerical and Missing Values are displayed here.       |
| **Summary Statistics**              | KPI Summary Statistics of the numerical columns excluding co-ordinates and time feature.      |
| **Category Analysis**               | Interactive pie charts and histograms to show categorical breakdowns.                         |
| **Numerical Analysis**              | Proper engaging year-wise stacked bar chart for numerical values.                             |
| **Trend Analysis**                  | Yearly and Monthly Revenue Trend, Seasonality Check using Decomposition etc.                  |
|**Sales Analysis**                   | Proper Sales Analysis on various factors based on Country, Channels etc.                      |
|**Geographical Analysis**            | Analysis plotting treemap for each city, sunburst for Channels etc                            |
|**Sales Force Analysis**             | Sales Team Contribution and Manager Effectivness throughout the years using Stacked bar Chart |
|**Product Analysis**                 | Proper life cycle trend, cross market revenue and dominant product class are displayed here.  |


# Summary : 
This dashboard transforms raw pharma sales data in to actionable insights using **Exploratory Data Analysis(EDA)**, **proper statistics** and **interactive dashboard**.
It is designed to help decision makers understand **performance trend**, **sales growth** and **distribution trends** at a glance 


   

