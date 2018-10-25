import json
import boto3
import time
import urllib
from decimal import Decimal
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

    return next_id


def insert_data(request):

    # get sequenceid
    next_id = increment_seq()

    # get unixtime
    date = time.time()

    # set table name
    table = dynamodb.Table('form_data')

    # insert
    table.put_item(
    Item={
        'id': int(next_id),
        'address':request['mailaddress'],
        'message':request['message'],
        'date': Decimal(date)
       }
    )

    return 

    
def lambda_handler(event, context):

    # url decode 
    post_data = urllib.parse.unquote(event['body'])

    # parse
    input_message = post_data.split("&")
    
    request = {}
    
    # setting post data.
    for n in input_message:
        data = n.split("=")
        request[data[0]] = data[1] 

    # insert form data.
    insert_data(request)

    return {
        'isBase64Encoded': False,
        "statusCode": 200,
        "headers": {
            'content-type': 'text/html',
        },
        "body": "<html><head><title>Thanks.</title></head><body><h2>Thank you !</h2></body></html>",
    }