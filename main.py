
import json
import os

import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()

llm_choice = [
    'mistral.mixtral-8x7b-instruct-v0:1',
    'mistral.mistral-7b-instruct-v0:2',
    'mistral.mistral-large-2402-v1:0',
    'mistral.mistral-small-2402-v1:0'
]


st.set_page_config(page_title='Ask Questions about Machine Learning')

st.sidebar.title('Ask Questions about Machine Learning')
llm_name = st.sidebar.selectbox('Language model', ['mistral.mistral-7b-instruct-v0:2'])
max_tokens = st.sidebar.number_input('max_tokens', min_value=0, value=4096)
temperature = st.sidebar.number_input('temperature', min_value=0.0, value=0.7)
top_p = st.sidebar.number_input('top_p', min_value=0.0, max_value=1.0, value=0.8)

question = st.text_area('Your Question')

if st.button('Ask!'):
    payload = json.dumps({
        'question': question,
        'llm_name': llm_name,
        'llm_config': {
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p
        },
        'source': 'streamlit'
    })

    url = os.getenv('APIURL')
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    result_dict = json.loads(response.text)

    st.write(result_dict['answer'])

    sources = [{
        'source': os.path.basename(item['metadata']['source']),
        'page': item['metadata']['page'],
        'page_content': item['page_content']
    } for item in result_dict['source_documents']]
    st.dataframe(pd.DataFrame.from_records(sources))
