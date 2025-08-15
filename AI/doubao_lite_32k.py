import base64
import time

from openai import OpenAI

# base_url = 'https://ark.cn-beijing.volces.com/api/v3'
# api_key = 'b7d3f762-3dbc-4405-a1c0-22e8745ae0d0'


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class DouBaoLite32k:
    def __init__(self):
        self.__lite_32k_init()

    def __lite_32k_init(self, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.messages = [{'role': 'system', 'content': '简洁回答，尽量50字以内'}]
        # self.messages = [{'role': 'system', 'content': '你是一个乐于助人的帮手。'}]

    def get_response(self, messages, stream=False, print_content=True):
        start_time = time.time()
        try:
            response = self.client.chat.completions.create(
                model='ep-20250404134802-pcddb',
                messages=messages,
                stream=stream
            )
        except Exception as e:
            print(f"请求错误: {e}")
            exit()
        content = ''

        if stream:
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    content += chunk.choices[0].delta.content
                    if print_content:
                        print(chunk.choices[0].delta.content, end='')
            print('\n')
        else:
            content = response.choices[0].message.content
            if print_content:
                print(content)

        end_time = time.time()

        # print(f'dk_api.py conversation print: response.choices[0].message{response.choices[0].message}')
        # print(f'dk_api.py conversation print: response.choices[0].message.content{content}')
        print(f"总费时: {end_time - start_time} seconds")
        return content

    def chat(self, user_input, stream=False, print_content=True):
        self.messages.append({'role': 'user', 'content': user_input})
        response = self.get_response(self.messages, stream=stream, print_content=print_content)
        self.messages.append({'role': 'assistant', 'content': response})
        return response


if __name__ == "__main__":
    print('this is vision_32k.py')
    img = r'.img/1.jpg'
