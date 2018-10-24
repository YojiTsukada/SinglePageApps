import json

def lambda_handler(event, context):

    input_message = event['body'].split("&")
    
    request = {}
    
    for n in input_message:
        data = n.split("=")
        request[data[0]] = data[1] 


    return {
        "statusCode": 200,
        "headers": {},
        "body": json.dumps(request)
    }