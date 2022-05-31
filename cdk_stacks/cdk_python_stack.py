from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    RemovalPolicy,
    aws_iam as _iam,
)
from constructs import Construct


class UrlShortenerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DDB table to store the Long and Short URLs with Short URL as the partition key
        url_shortener_table = _dynamodb.Table(
            self,
            "url-shortener-table",
            partition_key=_dynamodb.Attribute(
                name="shortUrl", 
                type=_dynamodb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # AutoScaling of RCUs with a Target Utilization of 70%
        url_shortener_table.auto_scale_read_capacity(
            min_capacity=5, max_capacity=500
        ).scale_on_utilization(target_utilization_percent=70)

        # AutoScaling of WCUs with a Target Utilization of 70%
        url_shortener_table.auto_scale_write_capacity(
            min_capacity=5, max_capacity=500
        ).scale_on_utilization(target_utilization_percent=70)

        # Lambda function with custom code to handle shortening/unshortening logic
        create_url_shortener_lambda = _lambda.Function(self, "create_url_shortener_lambda",
            code=_lambda.Code.from_asset("lambda"),
            handler="create.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(10),
            environment={
                "URL_SHORTENER_TABLE": url_shortener_table.table_name,
            }
        )
        # A Custom IAM Policy statement to grant DDB access to the Lambda function
        ddb_policy_statement = _iam.PolicyStatement(
            actions=["dynamodb:*", "apigateway:*", "lambda:*"],
            effect=_iam.Effect.ALLOW,
            resources=[url_shortener_table.table_arn, create_url_shortener_lambda.function_arn],
        )
        # Attaching DDB Policy statement with the Lambda IAM Role
        create_url_shortener_lambda.add_to_role_policy(ddb_policy_statement)
