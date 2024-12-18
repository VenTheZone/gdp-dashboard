import streamlit as st
import pandas as pd
import requests
import tempfile
import os

# Web scraping function
def scrape_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        # Debugging line - print response content
        st.write('Response content:', response.text)
        return response.json()
    except requests.RequestException as e:
        st.error(f'Error fetching data: {e}')
        return None
    except ValueError as json_error:
        st.error(f'Error parsing JSON: {json_error}')
        return None

st.title('Web Scraper')

url = st.text_input('Enter URL to scrape:')
if st.button('Scrape'):
    if url:
        data = scrape_data(url)
        if data is not None:
            df = pd.DataFrame(data)
            st.write(df)

            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
                df.to_csv(temp_file.name, index=False)
                st.success(f'Data saved to {temp_file.name}. Click below to download:')
                st.download_button(label='Download CSV', data=open(temp_file.name, 'rb'), file_name='scraped_data.csv', mime='text/csv')
                
                st.code(f'File saved at: {temp_file.name}')
        else:
            st.error('No data found or failed to scrape.')
    else:
        st.error('Please enter a valid URL.');