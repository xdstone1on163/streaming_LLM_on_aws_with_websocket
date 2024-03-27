import json
from invoke_bedrock import InvokeBedrock

def lambda_handler(event, context):
    body = json.loads(event["body"])
    request = body["query"]
    connectionId = event["requestContext"]["connectionId"]
    print("connetionId:  "+str(connectionId))
    ivk = InvokeBedrock(connectionId)
    ivk.call_bedrock(request)

    return {
        "statusCode": 200,
        "body": "Success"
    }
