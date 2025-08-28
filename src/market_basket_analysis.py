# market_basket_analysis.py

import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')


class MarketBasketAnalyzer:
    """
    A class to perform Market Basket Analysis on sales data.
    """

    def __init__(self, data_path='data/pharma-data.csv'):
        """
        Initializes the MarketBasketAnalyzer by loading and preprocessing the data.

        Args:
            data_path (str): The path to the CSV file containing sales data.
                             Defaults to 'data/pharma-data.csv'.
        """
        self.df = None
        self.transactions_df = None
        self.product_counts = None
        self.common_pairs = None
        self.basket_sizes = None

    def load_and_preprocess_data(self, data_path='data/pharma-data.csv'):
        """
        Loads the CSV data and performs initial cleaning.

        Args:
            data_path (str): The path to the CSV file.

        Raises:
            SystemExit: If the file is not found or cannot be loaded.
        """
        print("Starting data loading and preprocessing for Market Basket Analysis...")
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
        # Ensure 'Product Name' is also not null for basket analysis
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(subset=['Customer Name', 'Sales', 'Product Name'], inplace=True)
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
        print("Data loading and preprocessing for Market Basket Analysis completed.")

    def perform_analysis(self):
        """
        Performs the core Market Basket Analysis logic.
        """
        if self.df is None:
            raise ValueError("Data not loaded. Run load_and_preprocess_data() first.")

        print("Performing Market Basket Analysis...")
        
        # Define transactions: Same customer, same date, same sales rep = one transaction
        self.df['Transaction_ID'] = self.df.groupby(['Customer Name', 'Date', 'Name of Sales Rep']).ngroup()
        
        transaction_sizes = self.df.groupby('Transaction_ID').size()
        valid_transactions = transaction_sizes[transaction_sizes > 1].index
        basket_df = self.df[self.df['Transaction_ID'].isin(valid_transactions)]
        
        print(f"Total transactions: {self.df['Transaction_ID'].nunique()}")
        print(f"Transactions with multiple products: {len(valid_transactions)}")
        
        # Get unique products in each transaction
        self.transactions_df = basket_df.groupby('Transaction_ID')['Product Name'].apply(list).reset_index()
        
        # Count individual product frequencies
        self.product_counts = basket_df['Product Name'].value_counts().head(20)
        
        # Find frequent itemsets (product pairs)
        product_pairs = []
        for _, products in self.transactions_df.iterrows():
            if len(products['Product Name']) > 1:
                # Get all combinations of 2 products in each transaction
                pairs = list(combinations(sorted(set(products['Product Name'])), 2))
                product_pairs.extend(pairs)
        
        # Count pair frequencies
        pair_counts = Counter(product_pairs)
        self.common_pairs = pair_counts.most_common(15)
        
        # Calculate basket statistics
        self.basket_sizes = self.transactions_df['Product Name'].apply(len)
        
        print(f"Average basket size: {self.basket_sizes.mean():.2f}")
        print(f"Total unique products: {self.df['Product Name'].nunique()}")
        print("Market Basket Analysis completed.")

    def generate_dashboard(self):
        """
        Generates a comprehensive Plotly dashboard visualizing the Market Basket Analysis results.
        """
        if self.transactions_df is None or self.product_counts is None:
            raise ValueError("Analysis not performed. Run perform_analysis() first.")

        print("Generating Market Basket Analysis dashboard...")
        
        # Create a comprehensive dashboard with all plots (smaller size)
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Most Popular Products', 'Product Connections in Frequent Pairs', 
                            'Distribution of Items per Transaction', 'Product Connection Network'),
            specs=[[{"type": "bar"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "scatter"}]],
            horizontal_spacing=0.1,
            vertical_spacing=0.15
        )

        # 1. Product Popularity (Bar Chart)
        if len(self.product_counts) > 0:
            fig.add_trace(
                go.Bar(
                    x=self.product_counts.values,
                    y=self.product_counts.index,
                    orientation='h',
                    marker=dict(
                        color=self.product_counts.values,
                        colorscale='Viridis'
                    ),
                    text=self.product_counts.values,
                    textposition='auto'
                ),
                row=1, col=1
            )

        # 2. Product Associations (Bar Chart for Individual Products in Pairs)
        if self.common_pairs:
            products = []
            counts = []
            
            for (prod1, prod2), count in self.common_pairs:
                products.extend([prod1, prod2])
                counts.extend([count, count])
            
            fig.add_trace(
                go.Bar(
                    x=counts,
                    y=products,
                    orientation='h',
                    marker=dict(color='lightcoral'),
                    text=counts,
                    textposition='auto'
                ),
                row=1, col=2
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=[0], y=[0],
                    mode='text',
                    text=["No product associations found"],
                    showlegend=False
                ),
                row=1, col=2
            )

        # 3. Basket Size Distribution (Histogram)
        fig.add_trace(
            go.Histogram(
                x=self.basket_sizes.values,
                nbinsx=15,
                marker=dict(color='lightgreen'),
                name='Basket Sizes'
            ),
            row=2, col=1
        )

        # Add average line to histogram
        if len(self.basket_sizes) > 0:
            avg_line = go.Scatter(
                x=[self.basket_sizes.mean(), self.basket_sizes.mean()],
                y=[0, len(self.basket_sizes)//4],  # Approximate max height
                mode='lines',
                line=dict(dash='dash', color='red', width=2),
                name=f'Avg: {self.basket_sizes.mean():.1f}'
            )
            fig.add_trace(avg_line, row=2, col=1)

        # 4. Product Network (Scatter plot with connections)
        if len(self.transactions_df) > 0:
            # Get top products by frequency
            all_products = [product for products in self.transactions_df['Product Name'] for product in products]
            top_products = pd.Series(all_products).value_counts().head(12).index.tolist()
            
            # Calculate connections between top products
            connections = Counter()
            product_totals = Counter()
            
            for _, row in self.transactions_df.iterrows():
                products = set(row['Product Name'])
                # Only consider top products
                top_products_in_basket = [p for p in products if p in top_products]
                
                # Count individual product occurrences
                for product in top_products_in_basket:
                    product_totals[product] += 1
                    
                # Count connections between products
                for product in top_products_in_basket:
                    for other_product in top_products_in_basket:
                        if product != other_product:
                            connections[(product, other_product)] += 1
            
            if connections and top_products:
                # Create network visualization using scatter plot with connecting lines
                # Position nodes in a circular layout
                angles = np.linspace(0, 2*np.pi, len(top_products), endpoint=False)
                node_x = np.cos(angles) * 80
                node_y = np.sin(angles) * 80
                
                # Create edge traces (connections)
                edge_x = []
                edge_y = []
                
                for (prod1, prod2), weight in connections.items():
                    if prod1 in top_products and prod2 in top_products:
                        idx1 = top_products.index(prod1)
                        idx2 = top_products.index(prod2)
                        edge_x.extend([node_x[idx1], node_x[idx2], None])
                        edge_y.extend([node_y[idx1], node_y[idx2], None])
                
                # Edge trace (connections)
                fig.add_trace(
                    go.Scatter(
                        x=edge_x, 
                        y=edge_y,
                        line=dict(width=0.8, color='rgba(100,100,100,0.4)'),
                        hoverinfo='none',
                        mode='lines',
                        showlegend=False
                    ),
                    row=2, col=2
                )
                
                # Node trace (products)
                fig.add_trace(
                    go.Scatter(
                        x=node_x, 
                        y=node_y,
                        mode='markers+text',
                        hoverinfo='text',
                        text=top_products,
                        textposition="middle center",
                        marker=dict(
                            size=[max(product_totals[p]/max(product_totals.values())*30+8, 8) 
                                  for p in top_products],
                            color=[product_totals[p] for p in top_products],
                            colorscale='Viridis',
                            line=dict(width=1.5, color='black')
                        ),
                        hovertemplate='<b>%{text}</b><br>Frequency: %{marker.color}<extra></extra>',
                        showlegend=False
                    ),
                    row=2, col=2
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=[0], y=[0],
                        mode='text',
                        text=["Not enough connections to display"],
                        showlegend=False
                    ),
                    row=2, col=2
                )
        else:
            fig.add_trace(
                go.Scatter(
                    x=[0], y=[0],
                    mode='text',
                    text=["No transactions with multiple products"],
                    showlegend=False
                ),
                row=2, col=2
            )

        # Update layout for the entire dashboard
        fig.update_layout(
            title_text="Market Basket Analysis Dashboard",
            title_x=0.5,
            height=800,
            width = 1700,  
            showlegend=False,
            margin=dict(t=80, b=30, l=30, r=30)  
        )

        # Update axes labels
        fig.update_xaxes(title_text="Frequency", row=1, col=1)
        fig.update_yaxes(autorange="reversed", row=1, col=1)

        fig.update_xaxes(title_text="Co-occurrence Count", row=1, col=2)
        fig.update_yaxes(autorange="reversed", row=1, col=2)

        fig.update_xaxes(title_text="Number of Items", row=2, col=1)
        fig.update_yaxes(title_text="Frequency", row=2, col=1)

        fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False, row=2, col=2)
        fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False, row=2, col=2)

        # Reduce font sizes for subplot titles
        for i in fig['layout']['annotations']:
            i['font'] = dict(size=12)
            
        print("Market Basket Analysis dashboard generation completed.")
        return fig

    def print_summary(self):
        """
        Prints a summary of the Market Basket Analysis.
        """
        if self.basket_sizes is None:
            raise ValueError("Analysis not performed. Run perform_analysis() first.")

        print("\n=== MARKET BASKET ANALYSIS SUMMARY ===")
        print(f"Total transactions analyzed: {len(self.basket_sizes)}")
        print(f"Average basket size: {self.basket_sizes.mean():.2f}")
        if len(self.product_counts) > 0:
            print(f"Most popular product: {self.product_counts.index[0]} ({self.product_counts.iloc[0]} occurrences)")
        else:
            print("Most popular product: N/A")

        if self.common_pairs:
            print(f"Most common product pair: {self.common_pairs[0][0]} & {self.common_pairs[0][1][1]} ({self.common_pairs[0][1]} co-occurrences)")
        else:
            print("No product associations found (all transactions have only one product)")

    def save_results(self, output_path='market_basket_summary.csv'):
        """
        Saves a summary of the Market Basket Analysis to a CSV file.

        Args:
            output_path (str): The path where the CSV file will be saved.
                               Defaults to 'market_basket_summary.csv'.
        """
        if self.basket_sizes is None:
            raise ValueError("Analysis not performed. Run perform_analysis() first.")

        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True) # Ensure directory exists
        
        # Save results
        basket_analysis_results = pd.DataFrame([
            {'Analysis': 'Total Transactions', 'Value': len(self.basket_sizes)},
            {'Analysis': 'Average Basket Size', 'Value': round(self.basket_sizes.mean(), 2) if len(self.basket_sizes) > 0 else 0},
            {'Analysis': 'Unique Products', 'Value': self.df['Product Name'].nunique()},
            {'Analysis': 'Transactions with Multiple Products', 'Value': len(self.basket_sizes[self.basket_sizes > 1]) if len(self.basket_sizes) > 0 else 0}
        ])

        basket_analysis_results.to_csv(output_path, index=False)
        print(f"\nMarket basket summary saved to '{output_path}'")


def main(data_file_path='data/pharma-data.csv', output_file_path='output/market_basket_summary.csv'):
    """
    Main function to orchestrate the Market Basket Analysis process.
    This is the entry point when running the script directly.
    """
    # 1. Initialize the analyzer
    analyzer = MarketBasketAnalyzer()

    # 2. Load and preprocess data
    analyzer.load_and_preprocess_data(data_path=data_file_path)

    # 3. Perform analysis
    analyzer.perform_analysis()

    # 4. Generate and show the dashboard
    dashboard_fig = analyzer.generate_dashboard()
    dashboard_fig.show()

    # 5. Print summary to console
    analyzer.print_summary()

    # 6. Save results to CSV
    analyzer.save_results(output_path=output_file_path)


if __name__ == "__main__":
    main()
