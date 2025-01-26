import os

from groq import Groq


class LLMProvider:
    def __init__(self):
        super().__init__()

        self._llm = Groq(api_key=os.getenv('GROQ_API_KEY'))

    def call_llm(self, system_prompt: str, user_prompt: str) -> str:
        chat_completion = self._llm.chat.completions.create(
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ],
            model='llama-3.3-70b-versatile'
        )

        return chat_completion.choices[0].message.content
