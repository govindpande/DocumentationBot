import streamlit as st
from langchain.llms import OpenAI
from bs4 import BeautifulSoup
import requests
import os

# Streamlit app title
st.title('Welcome to DocumentationBot!!!')

# Streamlit input for URL
url = st.text_input('Enter the URL:', '')

# Streamlit input for customizing the LLM prompt
custom_prompt = st.text_area('Customize the LLM prompt:', 'Summarize the following text semantically:')

# Function to fetch and parse web page content
def fetch_and_parse(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        meta_desc = soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "No description found"
        return title, meta_desc
    except Exception as e:
        return "Failed to fetch data", str(e)

# Initialize OpenAI with the environment variable for API key
openai_api_key = os.getenv('OPENAI_API_KEY')  # Ensure this is set in your environment variables
llm = OpenAI(api_key=openai_api_key)

# Function to analyze text with Langchain and OpenAI GPT
def analyze_text_with_langchain(text, custom_prompt):
    response = llm.generate(prompts=[f"{custom_prompt}\n\n{text}"], max_tokens=100)
    return response if response else "No response"

# Main analysis trigger
if st.button('Analyze URL') and url:
    title, meta_desc = fetch_and_parse(url)
    combined_text = f"{title}. {meta_desc}"
    
    st.write("Title:", title)
    st.write("Meta Description:", meta_desc)
    
    # Ensure there's meaningful content to analyze
    if combined_text.strip() != '.':
        semantic_summary = analyze_text_with_langchain(combined_text, custom_prompt)
        st.write("Semantic Summary:", semantic_summary)
    else:
        st.write("Failed to retrieve or parse content from the URL.")


st.markdown('-----------------------------------------------------')
st.text('Developed by Govind Pande 2023')

