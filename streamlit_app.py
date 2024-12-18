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

# Create a directory based on file type
def save_data(df, filetype):
    folder_name = f'scraped_data/{filetype}'
    os.makedirs(folder_name, exist_ok=True)  # Create directories if they don't exist
    filename = f'{folder_name}/data.{filetype}'
    if filetype == 'csv':
        df.to_csv(filename, index=False)
    elif filetype == 'json':
        df.to_json(filename, orient='records')
    return filename

st.title('Web Scraper')

url = st.text_input('Enter URL to scrape:')
filetype = st.selectbox('Select file type', ['csv', 'json'])  # File type selection
if st.button('Scrape'):
    if url:
        data = scrape_data(url)
        if data is not None:
            df = pd.DataFrame(data)
            st.write(df)

            # Save data based on file type
            saved_file = save_data(df, filetype)
            st.success(f'Data saved to {saved_file}. Click below to download:')
            st.download_button(label='Download', data=open(saved_file, 'rb'), file_name=f'data.{filetype}', mime=f'text/{filetype}')
            
            st.code(f'File saved at: {saved_file}')
        else:
            st.error('No data found or failed to scrape.')
    else:
        st.error('Please enter a valid URL.')