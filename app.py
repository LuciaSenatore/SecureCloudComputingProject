import argparse
import re
from urllib.parse import urlparse
import numpy as np
import streamlit as st
import joblib
import pandas as pd
import streamlit.components.v1 as components

def set_widemode():
    st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def load(scaler_path, model_path):
    sc = joblib.load(scaler_path)
    model = joblib.load(model_path)
    return sc, model

def digit_count(url):
    digits = sum(1 for char in url if char.isnumeric())
    return digits

def letter_count(url):
    letters = sum(1 for char in url if char.isalpha())
    return letters

def has_ip_address(url):
    match = re.search(r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
                      r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'
                      r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)'
                      r'|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
                      r'([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
                      r'((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)
    return 1 if match else 0

def has_hostname(url):
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(re.escape(hostname), url)
    return 1 if match else 0

def is_https(url):
    scheme = urlparse(url).scheme
    return 1 if scheme == 'https' else 0

def url_length(url):
    return len(url)

def shortening_service(url):
    match = re.search(r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      r'tr\.im|link\.zip\.net', url)
    return 1 if match else 0

def special_characters(data):
    feature = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', '*', ',', '//']
    for i in feature:
        data[i] = data['url'].apply(lambda x: x.count(i))
    return data

def extract_features(link):
    x = np.array([[len(link),
                link.count('@'),
                link.count('?'),
                link.count('-'),
                link.count('='),
                link.count('.'),
                link.count('#'),
                link.count('%'),
                link.count('+'),
                link.count('$'),
                link.count('!'),
                link.count('*'),
                link.count(','),
                link.count('//'),
                has_hostname(link),
                is_https(link),
                digit_count(link),
                letter_count(link),
                shortening_service(link),
                has_ip_address(link)]])
    return x


def inference(link, scaler, model):
    if link == "":
        return None
    # Prepare the input data 'x' in the same format as used during training
    x = extract_features(link)

    # Scale the input data 'x' using the loaded scaler
    #x = scaler.transform(x)

    # Make predictions using the model
    prediction = model.predict(x)

    return prediction[0]



if __name__ == '__main__':
    #set_widemode()
    sc, model = load('model/best_logistic_regression_scaler.joblib', 'best_logistic_regression_model.joblib')

    original_title = '<h1 style=" font-size: 70px; color:#14F195; margin-block-start: 0;">Fish or Phish</h1>'
    st.markdown(original_title, unsafe_allow_html=True)
    description = """<p style="font-size: 20px; color:white; text-decoration: none; ">
                        Welcome to the Phishing Verification App! This tool assists in determining whether a website might be a phishing site or not.
                        Enter the URL of the site you wish to verify, and the application will analyze various phishing indicators to assess the risk associated with that site. 
                        Please note, this is an automated assessment and does not replace caution when opening links or providing sensitive information online.
                        Enter the website's URL in the designated field below and click 'Verify' to obtain the analysis result.
                    </p>"""
    st.markdown(description, unsafe_allow_html=True)
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@100&display=swap');
            *{
               font-family: 'Public Sans', sans-serif;
            }
            [data-testid="stAppViewContainer"] {
                background-image: url("https://github.com/LuciaSenatore/SecureCloudComputingImage/blob/main/Blue%20Technology%20Patterns%20Technology%20in%20the%20Life%20of%20Consumers%20Technology%20Presentation.png?raw=true");
                background-size: cover;
                

            }
            [data-testid="stMarkdownContainer"] > p{
                color: white;
                margin: 0px;
                padding: 0px;
                text-decoration: underline;
                font-size: 18px;
                
            }
            [data-testid="stMarkdownContainer"]{
                margin: 0px;
                padding: 0px;
            }
            [data-baseweb="base-input"] {
                background-color: white;
                color: black;
            }
            [aria-label="Enter the URL of the website"]{
                color: black;
                margin: 0px;
                underline: white;
            }    
        </style>
        """,
        unsafe_allow_html=True
    )

    link = st.text_input("Enter the URL of the website", type="default", key='url_input')

    button_html = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@100&display=swap');
        * {
            margin: 0px;
            padding: 0px;
            gap: 0rem;
            font-family: 'Public Sans', sans-serif;
        }
        button {
                font-size: 20px;
                background: #14F195;
                color: white;
                fill: rgb(155, 153, 153);
                margin-top: 1em;
                margin-bottom: 1em;
                padding: 0.7em 1em;
                padding-left: 0.9em;
                display: flex;
                align-items: center;
                cursor: pointer;
                border: none;
                border-radius: 15px;
                font-weight: 1000;
            }
            button span {
                display: block;
                margin-left: 0.3em;
                transition: all 0.3s ease-in-out;
            }
            button svg {
                display: block;
                transform-origin: center center;
                transition: transform 0.3s ease-in-out;
            }
            button:hover {
                background: #9945FF;
            }
            button:hover .svg-wrapper {
                transform: scale(1.25);
                transition: 0.5s linear;
                
            }
            button:hover svg {
                transform: translateX(2.2em) scale(1.1);
                fill: #fff;
            }
            button:hover span {
                opacity: 0;
                transition: 0.5s linear;
            }
            button:active {
                transform: scale(0.95);
            }
        </style>
        <div>
            <button>
                <div class="svg-wrapper-1">
                    <div class="svg-wrapper">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 576 512"
                        width="30"
                        height="30"
                        class="icon"
                    >
                        <path
                        fill="#f2f2f3" d="M180.5 141.5C219.7 108.5 272.6 80 336 80s116.3 28.5 155.5 61.5c39.1 33 66.9 72.4 81 99.8c4.7 9.2 4.7 20.1 0 29.3c-14.1 27.4-41.9 66.8-81 99.8C452.3 403.5 399.4 432 336 432s-116.3-28.5-155.5-61.5c-16.2-13.7-30.5-28.5-42.7-43.1L48.1 379.6c-12.5 7.3-28.4 5.3-38.7-4.9S-3 348.7 4.2 336.1L50 256 4.2 175.9c-7.2-12.6-5-28.4 5.3-38.6s26.1-12.2 38.7-4.9l89.7 52.3c12.2-14.6 26.5-29.4 42.7-43.1zM448 256a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z"/>
                        </path>
                        
                    </svg>
                    </div>
                </div>
                <span>Find Phish!</span>
            </button>
        </div>
    """

    good_result_html = """
        
        <div style="position:absolute; right:0%; top:-105px; z-index: 9999; width: xyz; height: xyz; ">
                <span style=" font-size: 40px; color:#14F195; line-weight:20; display:flex; align-items: center; justify-content:center; padding:5px;"> 
                    <svg xmlns="http://www.w3.org/2000/svg" height="35" width="35" viewBox="0 0 512 512" style="margin-right:15px;">
                    <path fill=#14F195 d="M256 48a208 208 0 1 1 0 416 208 208 0 1 1 0-416zm0 464A256 256 0 1 0 256 0a256 256 0 1 0 0 512zM369 209c9.4-9.4 9.4-24.6 0-33.9s-24.6-9.4-33.9 0l-111 111-47-47c-9.4-9.4-24.6-9.4-33.9 0s-9.4 24.6 0 33.9l64 64c9.4 9.4 24.6 9.4 33.9 0L369 209z"/>
                    </svg>
                    Legit URL
                </span>    
        </div>
    """
    bad_result_html = """
        <div style="position:absolute; right:0%; top:-105px; z-index: 9999; width: xyz; height: xyz;  ">
            <span style=" font-size: 40px; color:red; line-weight:20; display:flex; align-items: center; justify-content:center; padding:5px;"> 
                <svg xmlns="http://www.w3.org/2000/svg" height="35" width="35" viewBox="0 0 512 512" style="margin-right:15px;">
                <path fill=red d="M256 32c14.2 0 27.3 7.5 34.5 19.8l216 368c7.3 12.4 7.3 27.7 .2 40.1S486.3 480 472 480H40c-14.3 0-27.6-7.7-34.7-20.1s-7-27.8 .2-40.1l216-368C228.7 39.5 241.8 32 256 32zm0 128c-13.3 0-24 10.7-24 24V296c0 13.3 10.7 24 24 24s24-10.7 24-24V184c0-13.3-10.7-24-24-24zm32 224a32 32 0 1 0 -64 0 32 32 0 1 0 64 0z"/>
                </svg>
                Phishing URL
            </span>
        </div>
    """
    none_result_html = """
        <p>
        </p>
    """
    result= None

    if components.html(button_html, height=95):
        result = inference(link, sc, model)
        
        if result == 0:
            st.markdown(good_result_html, unsafe_allow_html=True)
            result = None
        elif result == 1 or result == 2 or result == 3:
            st.markdown(bad_result_html, unsafe_allow_html=True)
            result = None
        else:
            st.markdown(none_result_html, unsafe_allow_html=True)



        
