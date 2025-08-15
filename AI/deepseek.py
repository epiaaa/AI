from openai import OpenAI
import random
import re
import time

# DeepSeek_model = 'deepseek-reasoner' / 'deepseek-chat'
# DeepSeek_API_Key = 'sk-8735744e32f04635af0caa27e341a60d'
# DeepSeek_base_url = 'https://api.deepseek.com'

# DouBao_model = 'ep-20250404134802-pcddb'
# DouBao_api_key = 'b7d3f762-3dbc-4405-a1c0-22e8745ae0d0'
# DouBao_base_url = 'https://ark.cn-beijing.volces.com/api/v3'


class Conversation:
    def __init__(self, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def get_response(self, messages, model='deepseek-chat', stream=False, print_content=False):
        # start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                stream=stream,
                response_format={'type': 'json_object'},
            )
        except Exception as e:
            print(f"请求错误: {e}")
            exit()
        reasoning_content = ''
        content = ''

        if stream:
            for chunk in response:
                if model == 'deepseek-reasoner' and chunk.choices[0].delta.reasoning_content:
                    reasoning_content += chunk.choices[0].delta.reasoning_content
                    if print_content:
                        print(chunk.choices[0].delta.reasoning_content, end='')
                elif chunk.choices[0].delta.content is not None:
                    content += chunk.choices[0].delta.content
                    if print_content:
                        print(chunk.choices[0].delta.content, end='')
            print('\n')
        else:
            if model == 'deepseek-reasoner':
                reasoning_content = response.choices[0].message.reasoning_content
            content = response.choices[0].message.content
            if print_content:
                print(reasoning_content)
                print(content)
        # print(response)
        # end_time = time.time()
        # print(f"总费时: {end_time - start_time} seconds")
        return content, reasoning_content

    def chat(self, user_input, model='deepseek-chat', stream=False, print_content=False):
        messages = [{'role': 'system', 'content': '用户将提供给你 html 代码，根据用户要求输出用户需要的内容，以json文件输出'},
                    {'role': 'user', 'content': user_input}]
        response = self.get_response(messages, model=model, stream=stream, print_content=print_content)
        return response[0]

    def conversation(self, user_input, messages=None, model='deepseek-chat', stream=False, print_content=False):
        if messages is None:
            messages = [{'role': 'system', 'content': '用户将提供给你 html 代码，根据用户要求输出用户需要的内容，以json文件输出'},
                        {'role': 'user', 'content': user_input}]
        else:
            messages.append({'role': 'user', 'content': user_input})
        get_response = self.get_response(messages, model=model, stream=stream, print_content=print_content)
        return get_response[0], messages


