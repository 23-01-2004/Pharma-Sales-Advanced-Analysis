import pandas as pd

def dataset_overview(df):
    print("=== Dataset Overview ===")
    shape_df = pd.DataFrame({'Metric': ['Shape'], 'Value': [df.shape]})

    print("\nData Types:")
    dtypes_df = pd.DataFrame(df.dtypes, columns=['Data Type'])

    print("\nMissing Values:")
    missing_df = pd.DataFrame(df.isnull().sum(), columns=['Missing Values'])

    print("\nSample Data:")
    head_df = df.head()

    return shape_df, dtypes_df, missing_df, head_df
