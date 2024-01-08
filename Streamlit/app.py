import streamlit as st
import re
import requests
st.set_page_config(layout="wide")

# Function to format numbers for prompt
def fn(num):
    return f"{round(num*100)} %"

# Function to ask the FastAPI for generated text
def ask_llm(prompt: str, max_len: float, temp: float):
    # Data to send to the API
    data = {
        "prompt": prompt,
        "max_len": max_len,
        "temp": temp
        }
    
    # Api call
    server_url = "http://fastapi.docker:8000/generate_review"
    try:
        response = requests.post(server_url, json=data)
        # If successfull (200), get text. Othervise throw an error
        if response.status_code == 200:
            generated_text = response.json().get("generated_text")
        else:
            st.error("Failed to generate text. Please try again.")
        # Remove unfinished sentences and multiple newlines
        trunc_id = max(generated_text.rfind('.'), generated_text.rfind('!'), generated_text.rfind('?'))
        text_trunc = generated_text[:trunc_id + 1] if trunc_id != -1 else generated_text
        text_trunc = re.sub(r'(\n{2,})', r'\n', text_trunc)
        return text_trunc
    # If API call failed, throw an error
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
    temp = st.number_input('Temperature', value=1.0, min_value=0.0, step=.1)

tab1, tab2 = st.tabs(["Prepared prompt", "Custom prompt"])

# Tab 1 - prepared prompt
with tab1:

    # Inputs layout
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        stars_reviews = st.number_input('Stars from reviews', value=1, min_value=1, max_value=5, step=1)
    with col2:
        useful = st.number_input('Useful (%)', value=.1, min_value=0.0, max_value=1.0, step=.1)
    with col3:
        funny = st.number_input('Funny (%)',   value=.1, min_value=0.0, max_value=1.0, step=.1)
    with col4:
        cool = st.number_input('Cool (%)',     value=.1, min_value=0.0, max_value=1.0, step=.1)

    # Ask LLM
    if st.button('Generate review'):
        # Generate the prompt
        review_prompt = f"Generate a review that has {stars_reviews} stars, Usefulness = {fn(useful)}, Funny =  {fn(funny)}, and cool = {fn(cool)}."
        
        # Get an answer
        generated_text = ask_llm(prompt=review_prompt, max_len=max_len, temp=temp)

        # Output the generated review prompt and review text
        st.subheader('Prompt')
        st.text(review_prompt)

        st.subheader('Generated review')
        st.text(generated_text)

# Tab 2 - custom prompt
with tab2:

    # Get user input
    custom_prompt = st.text_input("Enter prompt", max_chars = 200)

    # Ask LLM
    if st.button('Generate text'):   

        # Get an answer
        generated_text = ask_llm(prompt=custom_prompt, max_len=max_len, temp=temp)

        st.subheader('Generated text')
        st.text(generated_text)
