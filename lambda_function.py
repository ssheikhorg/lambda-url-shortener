import json
import string
from random import choices

import boto3



def lambda_handler(event, context):
    print("event:--", event)

    base_url = "myapp.com/"
    short_url = generate_short_id(event['url'])
    print("short_url:--", short_url)
    
    return {
        'statusCode': 200,
        # 'body': json.dumps(f'Hello from Lambda! {short_url}'),
        'body': f"{base_url}{short_url}"
    }


def generate_short_id(short_url):
    """generate random keys for short ulrs"""
    short_url = ''.join(choices(string.ascii_letters+string.digits, k=6))
    return short_url
