import json
import string
from datetime import datetime
from random import choices
import uuid
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    print(event)
    dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
    table = dynamodb.Table("shortener")

    base_url = "myapp.com"
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    if event["routeKey"] == "POST /":
        data = json.loads(event["body"])
        original_url = data["originalUrl"]
        short_url = generate_short_id(original_url)
        response = table.put_item(
                Item={
                    "shortUrl": f"{base_url}/{short_url}",
                    "originalUrl": original_url,
                    "createdDate": date_time,
                    "id": str(uuid.uuid4()),
                }
            )
        print("data_table: ", response)
        return response
        # return {
        #     "statusCode": 201,
        #     'body': json.dumps("URI has been created")
        # }
    
    if event["routeKey"] == "GET /":
        dynamo_responses = table.query(KeyConditionExpression=Key('shortUrl').eq(event["queryStringParameters"]["shortUrl"]))

        print("dynamo_responses:", dynamo_responses['Items'][0])
        return {
            'statusCode': 200,
            # 'data': json.dumps(dynamo_responses['Items'][0])
            'data': dynamo_responses
        }


def generate_short_id(url):
    """generate random keys for short ulrs"""
    short_url = "".join(choices(string.ascii_letters + string.digits, k=6))
    return short_url
