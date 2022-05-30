import json
import string
from datetime import datetime
from random import choices
import uuid
import boto3
import botocore
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    print(event)

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("url_shortener")

    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    try:
        if event["requestContext"]["http"]["method"] == "POST":
            """create a short url"""
            data = json.loads(event["body"])
            url_long = data["url_long"]
            url_short = generate_short_id(url_long)
            table.put_item(
                    Item={
                        "url_short": url_short,
                        "url_long": url_long,
                        "created_date": date_time,
                        "id": str(uuid.uuid4()),
                    }
                )
            response = table.get_item(
                Key={
                    'url_short': url_short
                }
            )
            return response['Item']
        else:
            return {
                "statusCode": 400,
                "body": json.dumps("Invalid request")
            }
    except botocore.exceptions.ClientError as e:
        raise e


def generate_short_id(url):
    """generate random keys for short ulrs"""
    base_url = "myapp.com/"
    url_short = "".join(choices(string.ascii_letters + string.digits, k=6))
    return base_url + url_short
