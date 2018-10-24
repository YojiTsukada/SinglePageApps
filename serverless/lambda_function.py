import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

# DynamoDB
dynamodb = boto3.resource('dynamodb')


# increment sequence id
def increment_seq():
    table = dynamodb.Table('sequence')

    # get sequence id
    response = table.get_item(
        Key={
            'name': 'spa'
        }
    )

    id = response['Item']['id']
    print('Current ID : ' + str(id))

    # Next Sequence id
    next_id = id + 1
    
    # Update sequence id
    table.put_item(
    Item={
        'name': 'spa' ,
        'id': int(next_id)
       }
    )

    return 

    
def lambda_handler(event, context):
    increment_seq()

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