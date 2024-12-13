import pandas as pd

class DataLoader:
    """Class for loading datasets."""

    @staticmethod
    def load_csv(file_path):
        """
        Load a CSV file into a DataFrame.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Loaded dataset.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise Exception(f"Error loading dataset: {e}")
