from utils import StockAPI
import streamlit as st

# Initalize the web app
st.set_page_config(page_title="Stock Market Project", layout="wide")

# Import the stock api client
client = StockAPI()

# Add a title to webpage
st.title("Stock Market Project")

# Add author name as subheader
st.subheader("by Utkarsh Gaikwad")

# Add company name as input
company = st.text_input("Company Name :")

# If company name is input then
if company:
    # Get the symbol for given company
    search = client.symbol_search(company)
    option = st.selectbox("Company Symbol", options=search.keys())
    selected = search[option]

    # Disply the name, currency, region for each symbol
    st.success(f"Name : {selected[0]}")
    st.success(f"Region : {selected[1]}")
    st.success(f"Currency : {selected[2]}")

    # Create a submit button
    submit = st.button("Submit", type="primary")

    # After pressing submit button
    if submit:
        df = client.get_daily_prices(option)
        fig = client.plot_candlestick(df)
        st.plotly_chart(fig)
