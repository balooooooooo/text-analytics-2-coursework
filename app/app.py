import streamlit as st
import requests
st.set_page_config(layout="wide")

# Title and instructions
st.title('Review Generator')
st.write('Generate a review for a Restaurant from the yelp open dataset.')

# Inputs layout
col1, col2 = st.columns(2)

# First row inputs
with col1:
    stars_reviews = st.number_input('Stars from reviews', value=1, min_value=1, max_value=5, step=1)

with col2:
    stars_business = st.number_input('Stars from business', value=1.0, min_value=1.0, max_value=5.0, step=0.5)

# Inputs layout
col1, col2, col3 = st.columns(3)
with col1:
    useful = st.number_input('Useful', value=.5, min_value=0.0, max_value=1.0, step=.1)
with col2:
    funny = st.number_input('Funny',   value=.5, min_value=0.0, max_value=1.0, step=.1)
with col3:
    cool = st.number_input('Cool',     value=.5, min_value=0.0, max_value=1.0, step=.1)

if st.button('Generate review'):
    # Generate the review prompt and review text
    review_prompt = f"""
You have a Restaurant with the following Metadata:
Stars for the review = {stars_reviews}, Stars for the business: {stars_business}, Usefulness = {useful}, Funny: {funny}, Cool: {cool};
Generate a review. The single review can have as many sentencs as you like, but must end clearly."""
    
    # Api call
    server_url = "http://127.0.0.1:8000/generate_text"  # Replace with your FastAPI server URL
    data = {"prompt": review_prompt}
    try:
        response = requests.post(server_url, json=data)

        if response.status_code == 200:
            generated_text = response.json().get("generated_text")
        else:
            st.error("Failed to generate text. Please try again.")
    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")

    # Output the generated review prompt and review text
    st.subheader('Prompt')
    st.text(review_prompt)

    st.subheader('Generated review')
    st.text(generated_text)
