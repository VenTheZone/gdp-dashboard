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

# Display a file directory
def browse_directory(path):
    files = os.listdir(path)
    selected_file = st.selectbox('Browse Directory', files)
    if selected_file:
        st.write(f'Selected file: {selected_file}')
        file_path = os.path.join(path, selected_file)
        if os.path.splitext(selected_file)[1] == '.csv':
            df = pd.read_csv(file_path)
            st.dataframe(df)
        elif os.path.splitext(selected_file)[1] == '.json':
            df = pd.read_json(file_path)
            st.dataframe(df)

st.title('Web Scraper')

url = st.text_input('Enter URL to scrape:')
filetype = st.selectbox('Select file type', ['csv', 'json'])  # File type selection
if st.button('Scrape'):
    if url:
        data = scrape_data(url)
        if data is not None:
            df = pd.DataFrame(data)
            saved_file = save_data(df, filetype)
            st.success(f'Data saved to {saved_file}.')
            st.download_button(label='Download', data=open(saved_file, 'rb'), file_name=f'data.{filetype}', mime=f'text/{filetype}')
        else:
            st.error('No data found or failed to scrape.')
    else:
        st.error('Please enter a valid URL.')

# Directory browsing feature
if st.button('Browse Directory'):
    browse_directory('scraped_data/')