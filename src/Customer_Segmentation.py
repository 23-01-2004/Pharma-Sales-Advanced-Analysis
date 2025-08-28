# customer_segmentation.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class RFMAnalyzer:
    """
    A class to perform RFM (Recency, Frequency, Monetary) analysis and customer segmentation.

    Attributes:
        df (pd.DataFrame): The raw input sales data.
        rfm_df (pd.DataFrame): The calculated RFM data with customer names and cluster labels.
        optimal_k (int): The number of clusters determined by the elbow method.
    """

    def __init__(self, data_path='data/pharma-data.csv'):
        """
        Initializes the RFMAnalyzer by loading and preprocessing the data.

        Args:
            data_path (str): The path to the CSV file containing sales data.
                             Defaults to 'data/pharma-data.csv'.
        """
        self.df = None
        self.rfm_df = None
        self.optimal_k = None
        # Note: Data loading is now handled by a separate method or externally
        # to allow for flexibility when importing.

    def load_and_preprocess_data(self, data_path='data/pharma-data.csv'):
        """
        Loads the CSV data and performs initial cleaning.

        Args:
            data_path (str): The path to the CSV file.

        Raises:
            SystemExit: If the file is not found or cannot be loaded.
        """
        print("Starting data loading and preprocessing...")
        try:
            self.df = pd.read_csv(data_path)
            print(f"Data loaded successfully. Initial shape: {self.df.shape}")
        except FileNotFoundError:
            print(f"Error: File '{data_path}' not found.")
            raise SystemExit(1)
        except Exception as e:
            print(f"Error loading  {e}")
            raise SystemExit(1)

        print("Initial data info:")
        print(self.df.info())

        # Data Cleaning
        initial_rows = len(self.df)
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(subset=['Customer Name', 'Sales'], inplace=True)
        print(f"Removed {initial_rows - len(self.df)} rows due to missing data/duplicates")

        # Month Mapping
        month_mapping = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        self.df['Month'] = self.df['Month'].str.strip().str.capitalize()
        self.df['Month_Num'] = self.df['Month'].map(month_mapping)

        unmapped = self.df[self.df['Month_Num'].isna()]['Month'].unique()
        if len(unmapped) > 0:
            print(f"Warning: Unrecognized months found: {unmapped}")
        self.df.dropna(subset=['Month_Num'], inplace=True)
        self.df['Month_Num'] = self.df['Month_Num'].astype(int)

        # Year Conversion
        self.df['Year'] = pd.to_numeric(self.df['Year'], errors='coerce')
        self.df.dropna(subset=['Year'], inplace=True)
        self.df['Year'] = self.df['Year'].astype(int)

        # Create Date Column
        try:
            self.df['Date'] = pd.to_datetime(self.df[['Year', 'Month_Num']].rename(columns={'Month_Num': 'Month'}).assign(DAY=1))
        except Exception as e:
            print(f"Error creating Date column: {e}")
            raise SystemExit(1)

        # Sales Conversion
        self.df['Sales'] = pd.to_numeric(self.df['Sales'], errors='coerce')
        self.df.dropna(subset=['Sales'], inplace=True)

        print(f"Final dataset shape: {self.df.shape}")
        print("Data loading and preprocessing completed.")

    def calculate_rfm(self):
        """
        Calculates the RFM (Recency, Frequency, Monetary) values for each customer.
        """
        if self.df is None:
            raise ValueError("Data not loaded. Run load_and_preprocess_data() first.")

        print("Calculating RFM values...")
        current_date = self.df['Date'].max() + pd.DateOffset(days=1)
        print(f"Reference date for RFM analysis: {current_date}")

        self.rfm_df = self.df.groupby('Customer Name').agg({
            'Date': lambda x: (current_date - x.max()).days,  # Recency
            'Customer Name': 'count',  # Frequency
            'Sales': 'sum'  # Monetary
        }).rename(columns={'Date': 'Recency', 'Customer Name': 'Frequency', 'Sales': 'Monetary'})

        # Handle potential zero values to avoid issues in log scaling
        self.rfm_df['Frequency'] = self.rfm_df['Frequency'].replace(0, 1)
        self.rfm_df['Monetary'] = self.rfm_df['Monetary'].replace(0, 1)

        self.rfm_df = self.rfm_df.reset_index()
        print("RFM calculation completed.")
        print("RFM Statistics:")
        print(self.rfm_df.describe())

    def _find_optimal_k(self, data, max_k=10):
        """
        Finds the optimal number of clusters (k) using the Elbow method.

        Args:
            data (np.array): The scaled data to cluster.
            max_k (int): The maximum number of clusters to test.

        Returns:
            tuple: A tuple containing the optimal k (int), list of inertias,
                   and the range of k tested.
        """
        print("Finding optimal number of clusters (k)...")
        inertias = []
        k_range = range(1, max_k + 1)

        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(data)
            inertias.append(kmeans.inertia_)

        if len(inertias) < 3:
            optimal_k = 3
        else:
            diffs = np.diff(inertias)
            diffs2 = np.diff(diffs)
            if len(diffs2) > 0:
                elbow_index = np.argmax(diffs2) + 2
                optimal_k = max(2, min(elbow_index, max_k))
            else:
                optimal_k = 3

        print(f"Optimal number of clusters (k) determined: {optimal_k}")
        return optimal_k, inertias, k_range

    def perform_clustering(self):
        """
        Performs K-Means clustering on the log-scaled and standardized RFM data.
        """
        if self.rfm_df is None:
            raise ValueError("RFM data not calculated. Run calculate_rfm() first.")

        print("Performing data scaling and clustering...")
        # Log transformation and scaling
        rfm_log = np.log(self.rfm_df[['Recency', 'Frequency', 'Monetary']])
        scaler = StandardScaler()
        rfm_scaled = scaler.fit_transform(rfm_log)
        rfm_scaled_df = pd.DataFrame(rfm_scaled, columns=rfm_log.columns, index=rfm_log.index)

        # Determine optimal k and perform clustering
        self.optimal_k, inertias, k_range = self._find_optimal_k(rfm_scaled_df)
        kmeans = KMeans(n_clusters=self.optimal_k, random_state=42, n_init=10)
        self.rfm_df['Cluster'] = kmeans.fit_predict(rfm_scaled_df)
        print("Clustering completed.")

    def plot_elbow_method(self, inertias=None, k_range=None):
        """Plots the Elbow Method graph to visualize the optimal k."""
        if inertias is None or k_range is None:
             if self.rfm_df is None:
                raise ValueError("RFM data not calculated. Run calculate_rfm() and perform_clustering() first.")
             # Recalculate for plotting if not provided
             rfm_log = np.log(self.rfm_df[['Recency', 'Frequency', 'Monetary']])
             scaler = StandardScaler()
             rfm_scaled = scaler.fit_transform(rfm_log)
             rfm_scaled_df = pd.DataFrame(rfm_scaled, columns=rfm_log.columns, index=rfm_log.index)
             _, inertias, k_range = self._find_optimal_k(rfm_scaled_df)

        elbow_fig = px.line(x=list(k_range), y=inertias, markers=True,
                            labels={'x': 'Number of Clusters (k)', 'y': 'Inertia'},
                            title=f'Elbow Method for Optimal k (Optimal k = {self.optimal_k})')
        elbow_fig.update_layout(xaxis_title='Number of Clusters (k)', yaxis_title='Inertia')
        elbow_fig.add_vline(x=self.optimal_k, line_dash="dash", line_color="red",
                            annotation_text=f"Optimal k = {self.optimal_k}")
        return elbow_fig  # Return instead of show

    def generate_dashboard(self):
        """
        Generates a comprehensive Plotly dashboard visualizing the RFM analysis and clusters.
        """
        if self.rfm_df is None or self.optimal_k is None:
            raise ValueError("RFM data or clusters not available. Run calculate_rfm() and perform_clustering() first.")

        print("Generating comprehensive dashboard...")
        cluster_summary = self.rfm_df.groupby('Cluster').agg({
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': 'mean'
        }).round(2).reset_index()

        print("\nCluster Summary:")
        print(cluster_summary)

        # --- Dashboard Creation ---
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=('Recency Distribution', 'Frequency Distribution', 'Monetary Distribution',
                            'Cluster Distribution', 'Recency vs Monetary', 'Frequency vs Monetary',
                            'Top Performers by Cluster', 'Average RFM by Cluster', ''),
            specs=[[{"type": "box"}, {"type": "box"}, {"type": "box"}],
                   [{"type": "domain"}, {"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "xy"}, {"type": "bar"}, {"type": "xy"}]], # Simplified specs
            column_widths=[0.33, 0.33, 0.34],
            row_heights=[0.3, 0.3, 0.4]
        )

        colors = px.colors.qualitative.Set1

        # 1. Recency Distribution (Box Plot)
        for cluster in sorted(self.rfm_df['Cluster'].unique()):
            cluster_data = self.rfm_df[self.rfm_df['Cluster'] == cluster]
            fig.add_trace(go.Box(y=cluster_data['Recency'], name=f'Cluster {cluster}', showlegend=False), row=1, col=1)

        # 2. Frequency Distribution (Box Plot)
        for cluster in sorted(self.rfm_df['Cluster'].unique()):
            cluster_data = self.rfm_df[self.rfm_df['Cluster'] == cluster]
            fig.add_trace(go.Box(y=cluster_data['Frequency'], name=f'Cluster {cluster}', showlegend=False), row=1, col=2)

        # 3. Monetary Distribution (Box Plot)
        for cluster in sorted(self.rfm_df['Cluster'].unique()):
            cluster_data = self.rfm_df[self.rfm_df['Cluster'] == cluster]
            fig.add_trace(go.Box(y=cluster_data['Monetary'], name=f'Cluster {cluster}', showlegend=False), row=1, col=3)

        # 4. Cluster Distribution (Pie Chart)
        cluster_counts = self.rfm_df['Cluster'].value_counts().sort_index()
        fig.add_trace(go.Pie(labels=cluster_counts.index, values=cluster_counts.values, name="Cluster Distribution"), row=2, col=1)

        # 5. Scatter Plot: Recency vs Monetary
        for cluster in sorted(self.rfm_df['Cluster'].unique()):
            cluster_data = self.rfm_df[self.rfm_df['Cluster'] == cluster]
            fig.add_trace(
                go.Scatter(x=cluster_data['Recency'], y=cluster_data['Monetary'],
                           mode='markers', name=f'Cluster {cluster}',
                           marker=dict(size=8, color=colors[cluster % len(colors)]),
                           text=cluster_data['Customer Name'],
                           hovertemplate='<b>%{text}</b><br>Recency: %{x}<br>Monetary: %{y}<extra></extra>'),
                row=2, col=2
            )

        # 6. Scatter Plot: Frequency vs Monetary
        for cluster in sorted(self.rfm_df['Cluster'].unique()):
            cluster_data = self.rfm_df[self.rfm_df['Cluster'] == cluster]
            fig.add_trace(
                go.Scatter(x=cluster_data['Frequency'], y=cluster_data['Monetary'],
                           mode='markers', name=f'Cluster {cluster} (Freq vs Mon)',
                           marker=dict(size=8, color=colors[cluster % len(colors)]),
                           text=cluster_data['Customer Name'],
                           hovertemplate='<b>%{text}</b><br>Frequency: %{x}<br>Monetary: %{y}<extra></extra>',
                           showlegend=False),
                row=2, col=3
            )

        # 7. Top Performers by Cluster (Bar Chart) - Simplified
        top_performers_data = []
        for cluster in sorted(self.rfm_df['Cluster'].unique()):
            top_customers = self.rfm_df[self.rfm_df['Cluster'] == cluster].nlargest(5, 'Monetary')
            for _, row in top_customers.iterrows():
                top_performers_data.append({
                    'Cluster': f'Cluster {cluster}',
                    'Customer': row['Customer Name'],
                    'Monetary': row['Monetary']
                })
        if top_performers_data: # Check if list is not empty
            top_performers_df = pd.DataFrame(top_performers_data)
            # Group by cluster and customer for plotting
            for cluster in top_performers_df['Cluster'].unique():
                cluster_data = top_performers_df[top_performers_df['Cluster'] == cluster]
                fig.add_trace(
                    go.Bar(
                        x=cluster_data['Customer'],
                        y=cluster_data['Monetary'],
                        name=cluster,
                        text=cluster_data['Customer'],
                        textposition='auto',
                        hovertemplate='<b>%{text}</b><br>Monetary: %{y}<extra></extra>',
                        showlegend=False # To avoid clutter in legend
                    ),
                    row=3, col=1
                )

        # 8. Average RFM by Cluster (Bar Chart)
        cluster_avg = self.rfm_df.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean().round(2).reset_index()
        fig.add_trace(go.Bar(x=cluster_avg['Cluster'], y=cluster_avg['Recency'], name='Avg Recency',
                             marker_color='red', opacity=0.7), row=3, col=2)
        fig.add_trace(go.Bar(x=cluster_avg['Cluster'], y=cluster_avg['Frequency'], name='Avg Frequency',
                             marker_color='blue', opacity=0.7), row=3, col=2)
        fig.add_trace(go.Bar(x=cluster_avg['Cluster'], y=cluster_avg['Monetary'], name='Avg Monetary',
                             marker_color='green', opacity=0.7), row=3, col=2)

        # Update layout
        fig.update_layout(
            title_text=f"Comprehensive Customer Segmentation Dashboard (Optimal k = {self.optimal_k})",
            title_x=0.5,
            height=1200,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        # Update axis labels
        fig.update_xaxes(title_text="Cluster", row=1, col=1)
        fig.update_yaxes(title_text="Days", row=1, col=1)
        fig.update_xaxes(title_text="Cluster", row=1, col=2)
        fig.update_yaxes(title_text="Count", row=1, col=2)
        fig.update_xaxes(title_text="Cluster", row=1, col=3)
        fig.update_yaxes(title_text="Value", row=1, col=3)

        fig.update_xaxes(title_text="Recency", row=2, col=2)
        fig.update_yaxes(title_text="Monetary", row=2, col=2)
        fig.update_xaxes(title_text="Frequency", row=2, col=3)
        fig.update_yaxes(title_text="Monetary", row=2, col=3)

        fig.update_xaxes(title_text="Top Customers", row=3, col=1)
        fig.update_yaxes(title_text="Monetary Value", row=3, col=1)
        fig.update_xaxes(tickangle=45, row=3, col=1)

        fig.update_xaxes(title_text="Cluster", row=3, col=2)
        fig.update_yaxes(title_text="Average Value", row=3, col=2)

        return fig  # Return instead of show
        print("Dashboard generation completed.")

    # Replace the existing print_summary method in customer_segmentation.py

    # customer_segmentation.py

# ... (other parts of the file remain the same) ...

    # customer_segmentation.py

    def print_summary(self):
        """
        Returns a summary of the analysis as structured DataFrames.
        
        Returns:
            tuple: (top_customers_df, cluster_summary_df)
                Both are pandas DataFrames suitable for display.
        """
        if self.rfm_df is None:
            raise ValueError("RFM data not available. Run calculate_rfm() first.")

        # 1. Top 5 Customers by Monetary Value
        top_customers_df = (self.rfm_df.sort_values('Monetary', ascending=False)
                                    [['Customer Name', 'Monetary', 'Cluster']]
                                    .head()
                                    .reset_index(drop=True))
        top_customers_df.index = top_customers_df.index + 1 # Start index at 1 for better presentation
        top_customers_df.index.name = 'Rank'

        # 2. Summary by Clusters (Aggregated)
        cluster_summary_df = (self.rfm_df.groupby('Cluster')
                                        .agg(
                                            Customer_Count=('Customer Name', 'size'),
                                            Average_Recency=('Recency', 'mean'),
                                            Average_Frequency=('Frequency', 'mean'),
                                            Average_Monetary=('Monetary', 'mean')
                                        )
                                        .round(2)
                                        .reset_index())
        
        # Reorder columns for clarity
        cluster_summary_df = cluster_summary_df[[
            'Cluster', 'Customer_Count', 'Average_Recency', 
            'Average_Frequency', 'Average_Monetary'
        ]]

        return top_customers_df, cluster_summary_df

# ... (rest of the file remains the same) ...
    def save_results(self, output_path='customer_segmentation_results.csv'):
        """
        Saves the final RFM DataFrame with cluster labels to a CSV file.

        Args:
            output_path (str): The path where the CSV file will be saved.
                               Defaults to 'customer_segmentation_results.csv'.
        """
        if self.rfm_df is None:
            raise ValueError("RFM data not available. Run calculate_rfm() first.")

        os.makedirs(os.path.dirname(output_path), exist_ok=True) # Ensure directory exists
        self.rfm_df.to_csv(output_path, index=False)
        print(f"\nSegmentation results saved to '{output_path}'")


def main(data_file_path='data/pharma-data.csv', output_file_path='output/customer_segmentation_results.csv'):
    """
    Main function to orchestrate the customer segmentation process.
    This is the entry point when running the script directly.
    """
    # 1. Initialize the analyzer
    analyzer = RFMAnalyzer()

    # 2. Load and preprocess data
    analyzer.load_and_preprocess_data(data_path=data_file_path)

    # 3. Calculate RFM values
    analyzer.calculate_rfm()

    # 4. Perform clustering
    analyzer.perform_clustering()

    # 5. (Optional) Plot Elbow Method
    elbow_fig = analyzer.plot_elbow_method()
    elbow_fig.show()

    # 6. Generate and show the dashboard
    dashboard_fig = analyzer.generate_dashboard()
    dashboard_fig.show()

    # 7. Print summary to console
    summary_text = analyzer.print_summary()
    print(summary_text)

    # 8. Save results to CSV
    analyzer.save_results(output_path=output_file_path)


if __name__ == "__main__":
    main()