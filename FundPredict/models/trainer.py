from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class ModelTrainer:
    """Class for training machine learning models."""

    @staticmethod
    def train_random_forest(X, y):
        """
        Train a Random Forest classifier and evaluate its performance.

        Args:
            X (pd.DataFrame): Features.
            y (pd.Series): Target variable.

        Returns:
            dict: Model and evaluation metrics.
        """
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        model = RandomForestClassifier(random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        report = classification_report(y_test, y_pred, output_dict=True)

        return {"model": model, "report": report}
