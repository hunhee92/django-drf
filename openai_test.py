from openai import OpenAI
from api_prj.config import OPENAI_API_KEY
# OPENAI 의 키는 절대 유출되면 안되므로 config.py 에 저장하고 gitignore 사용해서 처리
client = OpenAI(
    api_key=OPENAI_API_KEY,  # 첫 생성시 여기에 api 키를 넣어야 함
)


def ask_chatgpt(user_mesaage):

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
            {"role": "user", "content": user_input}
        ]
    )
    return completion.choices[0].message.content
    # message.content 로 ai 의 답변만 볼 수 있음 초기엔 message만 적혀있고 conten : 내용 이런식으로 출력


while True:
    user_input = input("유저:")
    # 유저 인풋 (질문 받는 인풋) 위에 role user content 에 직접 입력 해도 됨
    if user_input == "exit":
        break
    response = ask_chatgpt(user_input)
    print("챗봇 : ", response, "\n\n")
