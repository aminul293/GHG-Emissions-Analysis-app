import pandas as pd
import plotly.express as px
import streamlit as st

# Load the data
file_path = "GHGs_by_Sector_and_State_2012-2020.xlsx"
excel_data = pd.ExcelFile(file_path)
ghg_data = excel_data.parse('Main')
sector_mapping = excel_data.parse('Sectors')

# Merge sector names for readability
ghg_data = ghg_data.merge(sector_mapping, on="Sector", how="left")
ghg_data.dropna(inplace=True)

# Streamlit App
st.title("GHG Emissions Analysis Dashboard")

# Dropdowns for filters
state = st.selectbox("Select State", ghg_data['State'].unique(), index=0)
year = st.selectbox("Select Year", sorted(ghg_data['Year'].unique()), index=0)

# Top States by Emissions
st.subheader("Top 10 States by Greenhouse Gas Emissions")
top_states = ghg_data.groupby('State')['FlowAmount'].sum().nlargest(10).reset_index()
top_states_chart = px.bar(top_states, x="State", y="FlowAmount",
                          color="State", title="Top 10 States by Emissions")
st.plotly_chart(top_states_chart)

# Emissions Trend for Selected State
st.subheader(f"Emissions Trend Over Time for {state}")
trend_data = ghg_data[ghg_data['State'] == state].groupby('Year')['FlowAmount'].sum().reset_index()
emissions_trend_chart = px.line(trend_data, x="Year", y="FlowAmount",
                                title=f"Emissions Trend for {state}", markers=True)
st.plotly_chart(emissions_trend_chart)

# Sector Contribution for Selected Year
st.subheader(f"Sector Contribution in {year}")
sector_data = ghg_data[ghg_data['Year'] == year].groupby('SectorName')['FlowAmount'].sum().reset_index()

# Combine smaller sectors into "Other"
threshold = 0.02 * sector_data['FlowAmount'].sum()  # 2% threshold
sector_data['Category'] = sector_data['FlowAmount'].apply(lambda x: 'Other' if x < threshold else x)
sector_data = sector_data.groupby('Category').sum().reset_index()

sector_chart = px.pie(sector_data, names="Category", values="FlowAmount",
                      title=f"Sector Contribution in {year}")
st.plotly_chart(sector_chart)
