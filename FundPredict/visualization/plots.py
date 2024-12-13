import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

class Plotter:
    """Class for generating visualizations."""

    @staticmethod
    def plot_funding_by_country(df):
        """
        Plot total funding by country.

        Args:
            df (pd.DataFrame): Input dataset.
        """
        try:
            funding_by_country = df.groupby('country_code')['funding_total_usd'].sum().sort_values(ascending=False)
            
            if funding_by_country.empty:
                st.warning("No data available for funding by country.")
                return

            # Create bar chart
            plt.figure(figsize=(12, 6))
            funding_by_country.plot(kind='bar', color='skyblue')
            plt.title("Total Funding by Country")
            plt.ylabel("Total Funding (USD)")
            plt.xlabel("Country")
            plt.xticks(rotation=45)
            st.pyplot(plt)  # Render the plot in Streamlit
        except KeyError as e:
            st.error(f"Missing required column: {e}")
        except Exception as e:
            st.error(f"An error occurred while plotting funding by country: {e}")

    @staticmethod
    def plot_funding_rounds_vs_total(df):
        """
        Plot funding rounds vs. total funding.

        Args:
            df (pd.DataFrame): Input dataset.
        """
        try:
            if df.empty:
                st.warning("No data available for funding rounds vs. total funding.")
                return

            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x='funding_rounds', y='funding_total_usd', hue='status', alpha=0.7)
            plt.title("Funding Rounds vs Total Funding")
            plt.xlabel("Funding Rounds")
            plt.ylabel("Total Funding (USD)")
            plt.legend(title="Status")
            st.pyplot(plt)  # Render the plot in Streamlit
        except KeyError as e:
            st.error(f"Missing required column: {e}")
        except Exception as e:
            st.error(f"An error occurred while plotting funding rounds vs. total funding: {e}")
