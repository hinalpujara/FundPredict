import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer

class DataPreprocessor:
    """Class for preprocessing the dataset."""

    @staticmethod
    def clean_data(df):
        """
        Cleans the dataset by removing unnecessary columns, handling missing values, and encoding categorical data.

        Args:
            df (pd.DataFrame): Input dataset.

        Returns:
            pd.DataFrame: Cleaned dataset.
        """
        # Drop unnecessary columns
        columns_to_drop = ['permalink', 'homepage_url', 'category_list', 'founded_at', 'first_funding_at', 'last_funding_at']
        df = df.drop(columns=columns_to_drop, errors='ignore')

        # Drop rows with missing values in critical columns
        df = df.dropna(subset=["funding_total_usd", "status", "country_code", "city"])

        # Normalize text columns
        df['city'] = df['city'].str.strip().str.lower()
        df['region'] = df['region'].str.strip().str.lower()
        df['country_code'] = df['country_code'].str.strip().str.lower()

        # Encode categorical variables
        le = LabelEncoder()
        df['region_encoded'] = le.fit_transform(df['region'])
        df['country_encoded'] = le.fit_transform(df['country_code'])

        # Convert funding_total_usd to numeric
        df['funding_total_usd'] = pd.to_numeric(df['funding_total_usd'], errors='coerce')

        return df

    @staticmethod
    def save_data(df, output_path):
        """
        Saves the cleaned dataset to a file.

        Args:
            df (pd.DataFrame): The cleaned dataset.
            output_path (str): File path to save the dataset.
        """
        try:
            df.to_csv(output_path, index=False)
            print(f"Dataset saved to {output_path}")
        except Exception as e:
            raise Exception(f"Error saving dataset: {e}")
