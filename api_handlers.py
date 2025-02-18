from openai import OpenAI
import datetime
import os

class BaseAPIHandler:
    
    
    def __init__(self):
        self.client = None
        self.system_message = "You are a helpful assistant."
        self.BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
        #self.MODEL_NAME = "qwen-max"

    def _create_client(self, api_key):
        return OpenAI(
            api_key=api_key,
            base_url=self.BASE_URL
        )
    

    def _logStart(self,content):
        #content:(answer,end_reason,question,token)实现日志记录,日志位于log文件夹内
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 获取当前时间并格式化
        log_dir = "./logs"  # 定义日志文件夹路径
        if not os.path.exists(log_dir):  # 如果日志文件夹不存在，则创建
            os.makedirs(log_dir)
        file_log_path = os.path.join(log_dir, "log.txt")  # 构建完整的日志文件路径
        
        with open(file_log_path, 'a', encoding='utf-8') as log:  # 以追加模式打开日志文件
            log.write(f"时间{now}\n结束原因:{content[1]}\n问题:{content[2]}\n回答:{content[0]}\n总token:{content[3]}") 

class APIWithoutHistory(BaseAPIHandler):
    def send_request(self, content, api_key, modal_name):
        client = self._create_client(api_key)
        completion = client.chat.completions.create(
            model=modal_name,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": content}
            ]
        )

        self._logStart((
            completion.choices[0].message.content,
            completion.choices[0].finish_reason,
            content,
            completion.usage.total_tokens
            ))

        return completion.choices[0].message.content

class APIWithHistory(BaseAPIHandler):
    def __init__(self):
        super().__init__()
        self.history = []

    def send_request(self, content, api_key, modal_name):
        client = self._create_client(api_key)
        
        if not self.history:
            self.history.append({"role": "system", "content": self.system_message})
            
        self.history.append({"role": "user", "content": content})
        
        completion = client.chat.completions.create(
            model=modal_name,
            messages=self.history
        )
        
        response = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": response})

        self._logStart((
            response,
            completion.choices[0].finish_reason,
            self.history,
            completion.usage.total_tokens
        ))

        return response

    def clear_history(self):
        self.history = []


class APIImageWithoutHistory(BaseAPIHandler):
    def send_request(self, content, api_key, modal_name,image):
        client = self._create_client(api_key)
        completion = client.chat.completions.create(
            model=modal_name,
            messages=[
                {"role": "system", "content": self.system_message},
                {"role": "user", "content": [
                    {"type": "image_url","image_url": image},
                    {"type": "text", "text": content}
                    ]
                }
            ]
        )

        self._logStart((
            completion.choices[0].message.content,
            completion.choices[0].finish_reason,
            f"图片输入+{content}",
            completion.usage.total_tokens
            ))

        return completion.choices[0].message.content

if __name__ == "__main__":
    pass