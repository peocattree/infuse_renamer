# Please install OpenAI SDK first: `pip3 install openai`

from openai import OpenAI
import requests

deepseek_key = input("请输入你的DeepSeek API Key：")

client = OpenAI(api_key=deepseek_key, base_url="https://api.deepseek.com")


def big_model(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=False
    )
    return response.choices[0].message.content


def get_balance():
    url = "https://api.deepseek.com/user/balance"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer <{deepseek_key}>'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


def big_model_continue(user_prompt, history):
    history.append({"role": "user", "content": user_prompt})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=history,
        stream=False
    )
    assistant_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": assistant_message})
    return assistant_message, history


if __name__ == "__main__":
    # print(big_model("你是一个资深的程序员", "帮我写一个冒泡排序的代码"))
    get_balance()
