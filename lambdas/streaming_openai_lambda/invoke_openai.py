import boto3
import os
import openai

class InvokeOpenai:
    def __init__(self, connectionId):
        self.conn = boto3.client("apigatewaymanagementapi", endpoint_url=os.environ["api_endpoint"], region_name=os.environ["region"])
        self.params = {
            "Data":"",
            "ConnectionId": connectionId
        }

    def get_openai_key(self):
        return os.environ["openai_key"]
    
    def call_openai(self, request, model="gpt-3.5-turbo"):
        openai.api_key = self.get_openai_key()
        response = ""
        
        for resp in openai.ChatCompletion.create(
                model=model,
                messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": f"{request}"}
                    ],
                stream=True,
                stop=None
            ):
            if "content" in resp.choices[0]["delta"]:
                res = resp.choices[0]["delta"]["content"]
                response += res
                if res != '':
                    self.params["Data"] = res
                    self.conn.post_to_connection(**self.params)
