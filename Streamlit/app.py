# streamlit run app/app.py
import streamlit as st
import re
import requests
st.set_page_config(layout="wide")

def ask_llm(prompt: str, max_len: float, temp: float):
    data = {
        "prompt": prompt,
        "max_len": max_len,
        "temp": temp
        }
    
    # Api call
    server_url = "http://fastapi.docker:8000/generate_review"  # Replace with your FastAPI server URL
    try:
        response = requests.post(server_url, json=data)

        if response.status_code == 200:
            generated_text = response.json().get("generated_text")
        else:
            st.error("Failed to generate text. Please try again.")

        trunc_id = max(generated_text.rfind('.'), generated_text.rfind('!'), generated_text.rfind('?'))
        text_trunc = generated_text[:trunc_id + 1] if trunc_id != -1 else generated_text
        text_trunc = re.sub(r'(\n{2,})', r'\n', text_trunc)
        return text_trunc
    except requests.RequestException as e:
        st.error(f"An error occurred: {e}")
        

# Title and instructions
st.title('Review Generator')
st.write('Generate a review for a Restaurant from the yelp open dataset.')

# Global inputs
col1, col2 = st.columns(2)
with col1:
    max_len = st.number_input('Maximum length',   value=120, min_value=50, max_value=200, step=1)
with col2:
    temp = st.number_input('Temperature', value=.6, min_value=0.0, max_value=1.0, step=.1)


tab1, tab2 = st.tabs(["Prepared prompt", "Custom prompt"])

with tab1:

    # Inputs layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        stars_reviews = st.number_input('Stars from reviews', value=1, min_value=1, max_value=5, step=1)
    with col2:
        useful = st.number_input('Useful', value=.5, min_value=0.0, max_value=1.0, step=.1)
    with col3:
        funny = st.number_input('Funny',   value=.5, min_value=0.0, max_value=1.0, step=.1)
    with col4:
        cool = st.number_input('Cool',     value=.5, min_value=0.0, max_value=1.0, step=.1)

    # Ask LLM
    if st.button('Generate review'):
        # Generate the prompt
        review_prompt = f"""
    You have a Restaurant with the following Metadata:
    Stars for the review = {stars_reviews}, Usefulness = {round(useful, 2)}, Funny: {round(funny, 2)}, Cool: {round(cool, 2)};
    Generate a review."""
        
        # Get an answer
        generated_text = ask_llm(prompt=review_prompt, max_len=max_len, temp=temp)

        # Output the generated review prompt and review text
        st.subheader('Prompt')
        st.text(review_prompt)

        st.subheader('Generated review')
        st.text(generated_text)

with tab2:

    # Get user input
    custom_prompt = st.text_input("Enter prompt", max_chars = 200)

    # Ask LLM
    if st.button('Generate text'):   

        # Get an answer
        generated_text = ask_llm(prompt=custom_prompt, max_len=max_len, temp=temp)

        st.subheader('Generated text')
        st.text(generated_text)

