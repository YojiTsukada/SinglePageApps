import boto3
import json
import urllib 
import os

client = boto3.client('ses')
 
from_address = os.environ['MAIL_ADDR']

def send_email(source, to, subject, body):
    response = client.send_email(
        Source=source,
        Destination={
            'ToAddresses': [
                to,
            ]
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': body,
                },
            }
        }
    )

    return response
 
def lambda_handler(event, context):
    subject = "Thank you for your information."
    message = urllib.parse.unquote(event['message'])
    dest_address = event['address']
    r = send_email(from_address, dest_address, subject, message)
    print(event)
    return 