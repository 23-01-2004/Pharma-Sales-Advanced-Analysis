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


   ### Why Plotly Instead of Matplotlib?

_I chose Plotly over Matplotlib for the following reasons:_

 **Interactivity** – Users can hover, zoom, and filter directly within the charts, also essential information is not always possible with static display so one can hover over a particular plot for additional infographics without making the overall plot cluttered. 

 **Dynamic Dashboards** – Works seamlessly with Streamlit for real-time updates, although matplotlib also does. But the difference lies in real time dynamic change of data properly affecting the plots which I saw was much more evident in case of Plotly. 

 **Better Aesthetics** – Offers cleaner, modern, and more engaging visuals, with an array of templates, animations and color continous scale features. 

 **Ease of Integration** – Supports multiple chart types (line, bar, pie, scatter, jitter plots) with minimal code, even useful during trend analysis for time series decomposition and YoY Growth factor of different channels and sub-channels. 

Matplotlib is excellent for static plots, but Plotly brings exploratory power and engagement for end users.

   

