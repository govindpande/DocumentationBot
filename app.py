import streamlit as st
from langchain.llms import OpenAI
from bs4 import BeautifulSoup
import requests
import os

# Streamlit app title
st.title('Web Content Analyzer')

# Streamlit input for URL
url = st.text_input('Enter the URL:', 'https://github.com/sushant097/Devnagari-Handwritten-Word-Recongition-with-Deep-Learning')

# Streamlit input for customizing the LLM prompt
custom_prompt = st.text_area('Customize the LLM prompt:', 'Summarize the following text semantically:')

# Function to fetch and parse web page content
def fetch_and_parse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No title found"
    meta_desc = soup.find("meta", attrs={"name": "description"})["content"] if soup.find("meta", attrs={"name": "description"}) else "No description found"
    return title, meta_desc

openai_api_key = os.getenv('OPENAI_API_KEY')  # Get the API key from the environment variable
llm = OpenAI(api_key=openai_api_key)

# Function to analyze text with Langchain and OpenAI GPT
def analyze_text_with_langchain(text, custom_prompt):
    response = llm.generate(prompts=[f"{custom_prompt}\n\n{text}"], max_tokens=100)
    return response[0]  # Assuming the response is a list of generated texts

# Button to trigger analysis
if st.button('Analyze URL'):
    title, meta_desc = fetch_and_parse(url)
    combined_text = f"{title}. {meta_desc}"
    
    st.write("Title:", title)
    st.write("Meta Description:", meta_desc)
    
    semantic_summary = analyze_text_with_langchain(combined_text, custom_prompt)
    st.write("Semantic Summary:", semantic_summary)
