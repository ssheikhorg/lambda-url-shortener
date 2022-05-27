import json
import string
from datetime import datetime
from random import choices
import uuid
import boto3



def lambda_handler(event, context):
    print("event:--", event)

    base_url = "myapp.com/"
    short_url = generate_short_id(event['url'])
    print("short_url:--", short_url)
    
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('url_shortener')

    table.put_item(Item={
        'id': str(uuid.uuid4()),
        'createdDate':date_time,
        'originalUrl': event['frequency'],
        'shortUrl': event['orderAmount']
    })



    return {
        'statusCode': 200,
        # 'body': json.dumps(f'Hello from Lambda! {short_url}'),
        'body': f"{base_url}{short_url}"
    }


def generate_short_id(short_url):
    """generate random keys for short ulrs"""
    short_url = ''.join(choices(string.ascii_letters+string.digits, k=6))
    return short_url
