import json
import boto3


def handler(event, context):
    print(event)

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("url_shortener")
    
    if event["requestContext"]["http"]["method"] == "GET":
        """get long url data with short url"""

        response = table.get_item(
            Key={
                'url_short': event["queryStringParameters"]["url_short"]
            }
        )
        print(response['Item'])
        return response['Item']
    else:
        return {
            "statusCode": 400,
            "body": json.dumps("Invalid request")
        }
