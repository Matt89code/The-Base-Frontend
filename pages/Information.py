import streamlit as st
import streamlit_authenticator as stauth
from streamlit.components.v1 import html
from google.cloud import vision_v1
import requests
import pandas as pd
from google.cloud.vision_v1 import AnnotateImageResponse
import json
import os
from google.oauth2 import service_account
import os.path
import PyPDF2
import docx2txt
from google.cloud import bigquery
import yaml
import uuid
from dotenv import load_dotenv, find_dotenv


with open('config.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized'])

################# NAVIGATION FUNCTION ################
def nav_page(page_name, timeout_secs=3):
    nav_script = """
        <script type="text/javascript">
            function attempt_nav_page(page_name, start_time, timeout_secs) {
                var links = window.parent.document.getElementsByTagName("a");
                for (var i = 0; i < links.length; i++) {
                    if (links[i].href.toLowerCase().endsWith("/" + page_name.toLowerCase())) {
                        links[i].click();
                        return;
                    }
                }
                var elasped = new Date() - start_time;
                if (elasped < timeout_secs * 1000) {
                    setTimeout(attempt_nav_page, 100, page_name, start_time, timeout_secs);
                } else {
                    alert("Unable to navigate to page '" + page_name + "' after " + timeout_secs + " second(s).");
                }
            }
            window.addEventListener("load", function() {
                attempt_nav_page("%s", new Date(), %d);
            });
        </script>
    """ % (page_name, timeout_secs)
    html(nav_script)



################## API ##################
def upload_api(file):
    #API Request - Youtube
    response_upload = requests.get(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/save_upload_file_tmp_upload_post',
    params={'url': file}).json()
    return response_upload

def youtube_api(user_input):
    #API Request - Youtube
    response_youtube = requests.get(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/youtube',
    params={'url': user_input}).json()
    return response_youtube

def summary_api(user_text):
    #API Request - Youtube
    response_summary = requests.get(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/summary',
    params={'text': user_text}).json()
    return response_summary

def keyword_api(user_text):
    #API Request - Youtube
    response_keyword = requests.get(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/keyword',
    params={'text': user_text}).json()
    return response_keyword

def topic_api(user_text):
    #API Request - Youtube
    response_topic = requests.get(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/topic',
    params={'text': user_text}).json()
    return response_topic

def file_api(user_text):
    #API Request - File
    response_topic = requests.post(
    'https://baseapi-qsjgkov3gq-ew.a.run.app/upload',
    params={'text': user_text}).json()
    return response_topic

def keyword_hierachy_api(keyword, user_text):
    response_hierachy = []


    for key in keyword:
        response_hierachy.append(requests.get(
        'https://baseapi-qsjgkov3gq-ew.a.run.app/full_hierachy',
        params={'keyword': key, 'text': user_text}).json())


    #hierachy preprocessing
    unwanted_words = ["entity", "collective entity", "library and information science"]
    counter = 0
    new_hierachy = []
    for keyword in response_hierachy:
        current_hierachy = []
        for word in keyword:
            if word not in unwanted_words:
                current_hierachy.append(word)
            counter += 1
        new_hierachy.append(current_hierachy)
    return new_hierachy




#page body
authenticator.logout('Logout', 'sidebar')
st.write(f'Welcome *{st.session_state.username}*')
nav_button = st.button("🧠 Memory")
if nav_button:
    nav_page("Memory")
st.markdown("""# 🆕  Information""")
st.write("\n")
tab1, tab2, tab3 = st.tabs(["Text", "File", "Handwritten"])
with tab1:
    title = st.markdown("""### ✏️ Your Title:""")
    user_title = st.text_input("", key=10)
    title = st.markdown("""### 📃 Your Text""")
    user_text = st.text_area(""'''''')
    button = st.button("Submit")
    if button and user_text:
        st.session_state['status'] = "Running"
        st.session_state['user_text'] = user_text
        st.session_state['user_title'] = user_title
        summary = summary_api(user_text)
        st.session_state['summary'] = summary

        keyword = keyword_api(user_text)
        st.session_state['keyword'] = keyword

        topic = topic_api(user_text)
        st.session_state['topic'] = topic

        keyword_hierachy = keyword_hierachy_api(keyword, user_text)
        st.session_state['keyword_hierachy'] = keyword_hierachy

        # Store data into database
        keyword_db = json.dumps(keyword)
        topic_db = json.dumps(topic)
        hierachy_db = json.dumps(keyword_hierachy)
        input_id = str(uuid.uuid4())
        username = st.session_state.username

        #loading credentials

        rows_to_insert =  [{'USER_ID': username, 'title': user_title, 'keywords':keyword_db, 'topic':topic_db, 'summary':summary, 'text': user_text, 'hierachy':hierachy_db, 'INPUT_ID': input_id}]
        errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))


        if summary and keyword and topic:
            nav_page("Knowledge")



def pdf_to_text(file):
    """Extract text in a PDF file."""

    pdfReader = PyPDF2.PdfFileReader(file)

    pageObj = pdfReader.getPage(pdfReader.numPages-1)

    text = pageObj.extractText()

    return text

def docx_to_text(file):
    """Extract text in a DOCX file."""

    text = docx2txt.process(file)

    return text


def detect_document(file):
    """Extract text in an image(JPEG, JPG, PNG)."""

    credentials = service_account.Credentials.from_service_account_file('google_credential.json')
    # env_path = find_dotenv()
    # load_dotenv()
    # CREDENTIAL_KEY = os.getenv('Credential')
    # credentials = service_account.Credentials.from_service_account_info(json.loads(CREDENTIAL_KEY))

    file = file.read()

    client = vision_v1.ImageAnnotatorClient(credentials = credentials)

    image = vision_v1.Image(content=file)

    response = client.document_text_detection(image=image)

    text = json.loads(AnnotateImageResponse.to_json(response))

    text = text['textAnnotations'][0]['description']

    return text

def file_to_text(file):

    extension = os.path.splitext(file.name)[1].strip(".")

    if extension in ['pdf']:
        text = pdf_to_text(file)

    elif extension in ['docx']:
        text = docx_to_text(file)

    elif extension in ['jpeg','jpg','png']:
        text = detect_document(file)

    return text
with tab2:
    title = st.markdown("""### ✏️ Your Title:""")
    user_title = st.text_input("", key=2)
    st.markdown("""### 📁 Upload your File""")
    uploaded_files = st.file_uploader("Choose .pdf/.docs/.png/.jpeg file", accept_multiple_files=False)
    submit_button = st.button("Submit", key=1)
    if uploaded_files is not None and submit_button:
        user_text = file_to_text(uploaded_files)
        if user_text:
            st.session_state['status'] = "Running"
            st.session_state['user_text'] = user_text
            st.session_state['user_title'] = user_title
            summary = summary_api(user_text)
            st.session_state['summary'] = summary

            keyword = keyword_api(user_text)
            st.session_state['keyword'] = keyword

            topic = topic_api(user_text)
            st.session_state['topic'] = topic

            keyword_hierachy = keyword_hierachy_api(keyword, user_text)
            st.session_state['keyword_hierachy'] = keyword_hierachy

            # Store data into google bigquery
            keyword_db = json.dumps(keyword)
            topic_db = json.dumps(topic)
            hierachy_db = json.dumps(keyword_hierachy)
            input_id = str(uuid.uuid4())
            username = st.session_state.username

            # loading creadentials
            rows_to_insert =  [{'USER_ID': username, 'title': user_title, 'keywords':keyword_db, 'topic':topic_db, 'summary':summary, 'text': user_text, 'hierachy':hierachy_db, 'INPUT_ID': input_id}]
            errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
            if errors == []:
                print("New rows have been added.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))

            if summary and keyword and topic:
                nav_page("Knowledge")



with tab3:
    title = st.markdown("""### ✏️ Your Title:""")
    user_title = st.text_input("", key=3)
    st.markdown("""### 📝 Upload your Handwritten-Text""")
    uploaded_files = st.file_uploader("Take a Picture and upload as .pdf/.docs/.png/.jpeg file", accept_multiple_files=False, key = 22)
    submit_button = st.button("Submit", key=33)
    if uploaded_files is not None and submit_button:
        user_text = file_to_text(uploaded_files)
        if user_text:
            st.session_state['status'] = "Running"
            st.session_state['user_text'] = user_text
            st.session_state['user_title'] = user_title
            summary = summary_api(user_text)
            st.session_state['summary'] = summary

            keyword = keyword_api(user_text)
            st.session_state['keyword'] = keyword

            topic = topic_api(user_text)
            st.session_state['topic'] = topic

            keyword_hierachy = keyword_hierachy_api(keyword, user_text)
            st.session_state['keyword_hierachy'] = keyword_hierachy

            # Store data into database
            keyword_db = json.dumps(keyword)
            topic_db = json.dumps(topic)
            hierachy_db = json.dumps(keyword_hierachy)
            input_id = str(uuid.uuid4())
            username = st.session_state.username

            project_id = 'lewagon-project-356008'
            table_id = 'lewagon-project-356008.user_infos.input_storage'
            credentials = service_account.Credentials.from_service_account_file('google_credential.json')
            client = bigquery.Client(credentials=credentials,project=project_id)
            # Construct a BigQuery client object.
            # TODO(developer): Set table_id to the ID of table to append to.
            # table_id = "your-project.your_dataset.your_table"
            rows_to_insert =  [{'USER_ID': username, 'title': user_title, 'keywords':keyword_db, 'topic':topic_db, 'summary':summary, 'text': user_text, 'hierachy':hierachy_db, 'INPUT_ID': input_id}]
            errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
            if errors == []:
                print("New rows have been added.")
            else:
                print("Encountered errors while inserting rows: {}".format(errors))

            if summary and keyword and topic:
                nav_page("Knowledge")
