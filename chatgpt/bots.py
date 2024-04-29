from openai import OpenAI
from django.conf import settings


client = OpenAI(
    api_key=settings.OPENAI_API_KEY,  # 첫 생성시 여기에 api 키를 넣어야 함
)


def translate_bot(user_message):

    system_instructions = """
        이제부터 너는 Django 프레임워크에 대해 설명하고 
        사용자가 Django 프레임워크에 대해 어려움을 겪고 있다고 가정하고 도와주는 챗봇이 되어야해.
        다른 코딩 언어나 프레임워크에 대해 설명하거나 다른 주제로 이야기하는 것은 금지야.
        Django 공식문서의 링크를 제공하거나 Django 프레임워크에 대한 설명도 추가해줘.
        """
    # 시스템 (AI 설정) 아래 sys content 에 직접 입력 가능

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_message}
        ]
    )

    return completion.choices[0].message.content
