from enum import Enum

from docling.document_converter import DocumentConverter
from docling_core.types.io import DocumentStream
from streamlit.runtime.uploaded_file_manager import UploadedFile

from llm_provider import LLMProvider


class SummarizationMethod(Enum):
    SENTENCE = 'Summarize the documents you are getting as a single sentence.'
    PARAGRAPH = 'Summarize the documents you are getting as a single paragraph.'
    PAGE = 'Summarize the documents you are getting as a single page.'

    def __init__(self, prompt: str):
        super().__init__()

        self._prompt = prompt

    @property
    def prompt(self) -> str:
        return self._prompt


class DocumentHandler:
    def __init__(self, document: UploadedFile):
        super().__init__()

        self._llm_provider = LLMProvider()

        self._document = document
        self._document_name = document.name

        document_stream = DocumentStream(name=self._document_name, stream=document)
        self._document_converter = DocumentConverter().convert(document_stream).document

    def document_name(self) -> str:
        return self._document_name

    def summarize(self, method: SummarizationMethod) -> str:
        return self._llm_provider.call_llm(
            system_prompt='You are a helpful assistant that specializes in summarizing documents. Use the titles and the body'
                          'of documents that you will be given to summarize them as best as possible.'
                          'Format your outputs as markdown text.'
                          f'{method.prompt}',
            user_prompt=f'Please summarize the following document titled "f{self._document_name}":'
                        ''
                        '------------'
                        ''
                        f'f{self._document_converter.export_to_markdown()}'
        )

        # return self._llm_provider.call_llm(
        #     system_prompt='אתה עוזר צ\'אט שמטרתו לתמצת מסמכים. בהינתן שם הקובץ והתוכן שתקבל אתה צריך לתמצת את המסמך.'
        #                   'אתה התשובה עליך להוציא בפורמט Markdown.'
        #                   'תתמצת את המסמך שתקבל לפסקה אחת בלבד.',
        #     user_prompt=f'בבקשה תתמצת את המסמך שהכותרת שלו היא "f{self._document_name}":'
        #                 ''
        #                 '------------'
        #                 ''
        #                 f'f{self._document_converter.export_to_markdown()}'
        # )

    def qna(self, question: str) -> str:
        # return self._llm_provider.call_llm(
        #     system_prompt='You are a helpful assistant that specializes in receiving documents and answering questions. '
        #                   'Use the titles and the body of documents that you will be given to answer the questions as '
        #                   'best as possible.'
        #                   'Format your outputs as markdown text.'
        #                   'Make sure the output is between 1 and 3 paragraphs long.',
        #     user_prompt=f'Please answer the following question: f{question}'
        #                 f''
        #                 f'You are given the following document titles "f{self._document_name}":'
        #                 ''
        #                 '------------'
        #                 ''
        #                 f'f{self._document_converter.export_to_markdown()}'
        # )

        return self._llm_provider.call_llm(
            system_prompt='אתה עוזר צ\'אט שמטרתו לענות על שאלות בהסתמך על מידע ממסמך שיינתן לך.'
                          'את התשובה עליך לכתוב בפורמט Markdown.'
                          'את התשובה תחזיר באורך שבין פסקה אחת ושלוש',
            user_prompt=f'בבקשה תענה על השאלה הבאה: f{question}'
                        f''
                        f'ניתן לך המסמך הבא שכותרתו היא "f{self._document_name}":'
                        ''
                        '------------'
                        ''
                        f'f{self._document_converter.export_to_markdown()}'
        )

    def export_as_markdown(self) -> str:
        return self._document_converter.export_to_markdown()
