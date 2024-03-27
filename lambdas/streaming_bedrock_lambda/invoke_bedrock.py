import json
import boto3
import os
from botocore.exceptions import ClientError

class InvokeBedrock:
    def __init__(self, connectionId):
        self.conn = boto3.client("apigatewaymanagementapi", endpoint_url=os.environ["api_endpoint"], region_name=os.environ["region"])
        self.bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name=os.environ["region"])
        self.params = {
            "Data":"",
            "ConnectionId": connectionId
        }


    def call_bedrock(self, request, model="anthropic.claude-3-sonnet-20240229-v1:0"):
        response = ""

        response = self.bedrock_runtime.invoke_model_with_response_stream(
            modelId=model,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": f"{request}"}],
                        }
                    ],
                }
            ),
        )

        for event in response.get("body"):
            chunk = json.loads(event["chunk"]["bytes"])
    
            if chunk['type'] == 'message_delta':
                print(f"\nStop reason: {chunk['delta']['stop_reason']}")
                print(f"Stop sequence: {chunk['delta']['stop_sequence']}")
                print(f"Output tokens: {chunk['usage']['output_tokens']}")
    
            if chunk['type'] == 'content_block_delta':
                if chunk['delta']['type'] == 'text_delta':
                    print(chunk['delta']['text'], end="")
                    self.params["Data"] = chunk['delta']['text']
                    self.conn.post_to_connection(**self.params)

"""
def lambda_handler(event, context):

    # Invoke Claude 3 with the text prompt
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    prompt = "what is AI?"
    
    try:
        response = bedrock_runtime.invoke_model_with_response_stream(
            modelId=model_id,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": prompt}],
                        }
                    ],
                }
            ),
        )

        for event in response.get("body"):
            chunk = json.loads(event["chunk"]["bytes"])
    
            if chunk['type'] == 'message_delta':
                print(f"\nStop reason: {chunk['delta']['stop_reason']}")
                print(f"Stop sequence: {chunk['delta']['stop_sequence']}")
                print(f"Output tokens: {chunk['usage']['output_tokens']}")
    
            if chunk['type'] == 'content_block_delta':
                if chunk['delta']['type'] == 'text_delta':
                    print(chunk['delta']['text'], end="")
        
        return {
               'statusCode': 200,
               'headers': {
                 'Access-Control-Allow-Headers': '*',
                 'Access-Control-Allow-Origin': '*',
                 'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
               },
                 'body': "Success"
            }
           
    except ClientError as err:
        logger.error(
            "Couldn't invoke Claude 3 Sonnet. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise

"""

"""
    try:
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 1024,
                    "messages": [
                        {
                            "role": "user",
                            "content": [{"type": "text", "text": prompt}],
                        }
                    ],
                }
            ),
        )

        # Process and print the response
        result = json.loads(response.get("body").read())
        input_tokens = result["usage"]["input_tokens"]
        output_tokens = result["usage"]["output_tokens"]
        output_list = result.get("content", [])

        print("Invocation details:")
        print(f"- The input length is {input_tokens} tokens.")
        print(f"- The output length is {output_tokens} tokens.")

        print(f"- The model returned {len(output_list)} response(s):")
        for output in output_list:
            print(output["text"])

        return {
           'statusCode': 200,
           'headers': {
             'Access-Control-Allow-Headers': '*',
             'Access-Control-Allow-Origin': '*',
             'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
           },
             'body': "Success"
        }
           
    except ClientError as err:
        logger.error(
            "Couldn't invoke Claude 3 Sonnet. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise
"""
