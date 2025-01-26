import streamlit as st
from dotenv import load_dotenv

from document_handler import DocumentHandler, SummarizationMethod

load_dotenv()

st.title('Document Summarization')

st.header('File upload', divider=True)

uploaded_file = st.file_uploader('Upload a file', type=['docx'])
if uploaded_file:
    st.write(f'Uploaded file: {uploaded_file.name}')

st.header('Summarization', divider=True)

summarization_method = st.pills('Summarization mode',
                                options=['Sentence', 'Paragraph', 'Page'],
                                default='Paragraph',
                                selection_mode='single')

text_to_summarization_method = {
    'Sentence': SummarizationMethod.SENTENCE,
    'Paragraph': SummarizationMethod.PARAGRAPH,
    'Page': SummarizationMethod.PAGE
}

if st.button('Summarize document', type='secondary', icon='📝', use_container_width=True):
    if not uploaded_file:
        st.toast('You must upload a document to use summarization', icon='❌')
    else:
        st.markdown(DocumentHandler(uploaded_file).summarize(text_to_summarization_method[summarization_method]))

st.header('Question Answering', divider=True)

question = st.text_input(label='Question')
if st.button('Answer question', type='secondary', icon=None, use_container_width=True):
    if not uploaded_file:
        st.toast('You must upload a document to use question answering', icon='❌')
    elif len(question) <= 0:
        st.toast('Question is empty', icon='❌')
    else:
        st.markdown(DocumentHandler(uploaded_file).qna(question))
