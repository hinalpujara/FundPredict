class Helpers:
    """Class containing utility functions."""

    @staticmethod
    def prepare_model_data(df, target, features):
        """
        Prepares data for machine learning.

        Args:
            df (pd.DataFrame): Input dataset.
            target (str): Target column name.
            features (list): List of feature column names.

        Returns:
            tuple: Features (X) and target (y).
        """
        X = df[features]
        y = (df[target] == "operating").astype(int)  # Binary target: 1 for 'operating', 0 otherwise
        return X, y
