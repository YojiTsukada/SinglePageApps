import json
import time
import urllib
from datetime import datetime
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr, Key

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

    print('Insert ID : ' + str(next_id) + ' is completed.')

    return 



def invoke_lambda(request,function_name):
    clientLambda = boto3.client("lambda")
    # 引数
    params = {
        'address':request['mailaddress'],
        'message':request['message'],
    }

    res = clientLambda.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=json.dumps(params)
    )

    return res

    
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

    # send mail
    invoke_lambda(request,'sendmail')

    # read response file.
    with open("html/thanks.html", "r") as f:
        response = f.read()

    return {
        'isBase64Encoded': False,
        "statusCode": 200,
        "headers": {
            'content-type': 'text/html',
        },
        "body": response
    }
