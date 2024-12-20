import streamlit as st
import pandas as pd
from data.loader import DataLoader
from data.preprocessing import DataPreprocessor
from utils.helpers import Helpers
from visualization.plots import Plotter


# Load and preprocess data
@st.cache_data
def load_and_clean_data(file_path):
    """
    Load and clean the dataset.
    
    Args:
        file_path (str): Path to the dataset CSV file.
        
    Returns:
        pd.DataFrame: Cleaned dataset.
    """
    df = DataLoader.load_csv(file_path)
    df_cleaned = DataPreprocessor.clean_data(df)
    return df_cleaned


# Streamlit App
def main():
    st.title("Startup Insights and Recommendations")
    st.sidebar.header("Explore Startups")

    # Load the dataset
    file_path = "src/big_startup_secsees_dataset.csv"
    df = load_and_clean_data(file_path)

    # Global Analysis
    st.header("Top-Funded Startups Globally")
    top_funded_global = df.groupby('name')['funding_total_usd'].sum().sort_values(ascending=False).head(10)
    st.write("Top 10 Funded Startups Globally")
    st.dataframe(top_funded_global.reset_index().rename(columns={"name": "Startup Name", "funding_total_usd": "Total Funding (USD)"}))

    # Regional Analysis
    st.header("Explore Funding by Region")
    country_options = df['country_code'].dropna().unique()

    # Country selection
    selected_country = st.selectbox("Select a Country", sorted(country_options))
    if selected_country:
        city_options = df[df['country_code'] == selected_country]['city'].dropna().unique()
        if city_options.size == 0:
            st.warning(f"No cities available for the selected country: {selected_country}.")
        else:
            selected_city = st.selectbox("Select a City", sorted(city_options))
            
            if selected_city:
                st.subheader(f"Funding Data for {selected_city}")
                city_data = df[
                    (df['country_code'] == selected_country) &
                    (df['city'] == selected_city)
                ]
                city_data = city_data.rename(columns={
                    'name': 'Startup Name',
                    'funding_total_usd': 'Total Funding (USD)',
                    'status': 'Operational Status'
                })
                st.dataframe(city_data)

                # Download city-specific data
                st.download_button(
                    label="Download City Data",
                    data=city_data.to_csv(index=False),
                    file_name=f"{selected_city}_funding_data.csv",
                    mime="text/csv"
                )

    # Recommendations
    st.header("Region Recommendations")
    if selected_country:
        st.write(f"Identifying regions in **{selected_country}** with high success rates and significant funding...")
        
        # Filter funding data for the selected country
        country_data = df[df['country_code'] == selected_country]
        region_funding = country_data.groupby('region')['funding_total_usd'].sum()
        
        if not region_funding.empty:
            recommended_region = region_funding.idxmax()
            st.write(f"**Recommended Region for Investment in {selected_country}:** {recommended_region}")
            st.bar_chart(region_funding, use_container_width=True)
        else:
            st.write(f"No funding data available for regions in {selected_country}.")
    else:
        st.write("Please select a country to see region recommendations.")

    # Funding Trends and Insights
    st.header(f"Funding Trends and Insights for {selected_city}")
    if selected_city:
        # Filter data for the selected city
        city_company_funding = df[df['city'] == selected_city][['name', 'funding_total_usd']]

        if not city_company_funding.empty:
            # Sort companies by funding amount in descending order
            city_company_funding = city_company_funding.sort_values(by='funding_total_usd', ascending=False).head(10)
            
            # Horizontal bar chart using matplotlib
            import matplotlib.pyplot as plt

            fig, ax = plt.subplots()
            ax.barh(city_company_funding['name'], city_company_funding['funding_total_usd'], color='skyblue')
            ax.set_xlabel("Funding Total (USD)")
            ax.set_ylabel("Company Name")
            ax.set_title(f"Top 10 Companies by Funding in {selected_city}")
            ax.invert_yaxis()  # To display the highest-funded company at the top

            st.pyplot(fig)
        else:
            st.warning(f"No funding data available for companies in {selected_city}.")



if __name__ == "__main__":
    main()
