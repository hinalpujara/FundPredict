from data.loader import DataLoader
from data.preprocessing import DataPreprocessor
from utils.helpers import Helpers
from visualization.plots import Plotter
from models.trainer import ModelTrainer

if __name__ == "__main__":
    # Load dataset
    data_path = "src/big_startup_secsees_dataset.csv"
    df = DataLoader.load_csv(data_path)

    # Preprocess data
    df_cleaned = DataPreprocessor.clean_data(df)

    # Save the cleaned dataset
    cleaned_data_path = "cleaned_startup_dataset.csv"
    DataPreprocessor.save_data(df_cleaned, cleaned_data_path)

    # Perform EDA
    print("Performing Exploratory Data Analysis...")
    Plotter.plot_funding_by_country(df_cleaned)
    Plotter.plot_funding_rounds_vs_total(df_cleaned)

    # Prepare data for modeling
    X, y = Helpers.prepare_model_data(df_cleaned, target="status", features=["funding_rounds", "funding_total_usd", "region_encoded", "country_encoded"])

    # Train and evaluate model
    model_results = ModelTrainer.train_random_forest(X, y)
    print("Model Evaluation:\n", model_results["report"])

    # Visualize feature importance
    print("Visualizing Feature Importance...")
    Plotter.plot_feature_importance(model_results["model"], X.columns)
