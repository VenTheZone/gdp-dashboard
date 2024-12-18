import streamlit as st
import pandas as pd
import requests
import tempfile
import os

# Web scraping function
def scrape_data(url):
    response = requests.get(url)
    # Assuming the response is in JSON format
    return response.json()

st.title('Web Scraper')

url = st.text_input('Enter URL to scrape:')
if st.button('Scrape'):
    if url:
        data = scrape_data(url)
        df = pd.DataFrame(data)
        st.write(df)

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
        df.to_csv(temp_file.name, index=False)
        st.success(f'Data saved to {temp_file.name}. Click below to download:')
        st.download_button(label='Download CSV', data=open(temp_file.name, 'rb'), file_name='scraped_data.csv', mime='text/csv')
        
        st.code(f'File saved at: {temp_file.name}')
    else:
        st.error('Please enter a valid URL.')