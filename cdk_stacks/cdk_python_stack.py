from aws_cdk.aws_apigatewayv2_alpha import (
    CorsHttpMethod,
    HttpApi,
    HttpMethod,
    CorsPreflightOptions,
    HttpStage,
)
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from aws_cdk.aws_iam import (
    Role,
    PolicyStatement,
    ManagedPolicy,
    ServicePrincipal,
    Effect,
)

from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    RemovalPolicy,
    CfnOutput,
)
from constructs import Construct


class UrlShortenerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # # DDB table to store the Long and Short URLs with Short URL as the partition key
        # url_shortener_table = _dynamodb.Table(
        #     self,
        #     "url-shortener-table",
        #     partition_key=_dynamodb.Attribute(
        #         name="shortUrl", type=_dynamodb.AttributeType.STRING
        #     ),
        #     read_capacity=5,
        #     write_capacity=5,
        #     removal_policy=RemovalPolicy.DESTROY,
        # )

        # # AutoScaling of RCUs with a Target Utilization of 70%
        # url_shortener_table.auto_scale_read_capacity(
        #     min_capacity=5, max_capacity=500
        # ).scale_on_utilization(target_utilization_percent=70)

        # # AutoScaling of WCUs with a Target Utilization of 70%
        # url_shortener_table.auto_scale_write_capacity(
        #     min_capacity=5, max_capacity=500
        # ).scale_on_utilization(target_utilization_percent=70)

        # Lambda function with custom code to handle shortening/unshortening logic
        create_url_shortener_lambda = _lambda.Function(
            self,
            "create_url_shortener_lambda",
            code=_lambda.Code.from_asset("lambda"),
            handler="create.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(10),
            # environment={
            #     "URL_SHORTENER_TABLE": url_shortener_table.table_name,
            # },
        )

        # Lambda function with custom code to handle shortening/unshortening logic
        get_url_shortener_lambda = _lambda.Function(
            self,
            "get_url_shortener_lambda",
            code=_lambda.Code.from_asset("lambda"),
            handler="read.handler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            timeout=Duration.seconds(10),
            # environment={
            #     "URL_SHORTENER_TABLE": url_shortener_table.table_name,
            # },
        )

        # # A Custom IAM Policy statement to grant DDB access to the Lambda function
        # ddb_policy_statement = PolicyStatement(
        #     actions=["dynamodb:*"],
        #     effect=Effect.ALLOW,
        #     resources=[
        #         url_shortener_table.table_arn,
        #         get_url_shortener_lambda.function_arn,
        #     ],
        # )

        # # IAM Role for the AWS Lambda function which creates the branch resources
        # create_branch_role = Role(
        #     self,
        #     "LambdaCreateBranchRole",
        #     assumed_by=ServicePrincipal("lambda.amazonaws.com"),
        # )
        # create_branch_role.add_managed_policy(
        #     ManagedPolicy.from_aws_managed_policy_name(
        #         "service-role/AWSLambdaBasicExecutionRole"
        #     )
        # )
        # create_branch_role.add_to_policy(
        #     PolicyStatement(
        #         actions=["dynamodb:*"],

        #     )
        # )

        # # Attaching DDB Policy statement with the Lambda IAM Role
        # create_url_shortener_lambda.add_to_role_policy(ddb_policy_statement)
        # get_url_shortener_lambda.add_to_role_policy(ddb_policy_statement)

        # create our HTTP Api
        http_api = HttpApi(
            self,
            "url-shortener-api",
            description="URL Shortener API",
            cors_preflight=CorsPreflightOptions(
                allow_origins=["*"],
                allow_headers=["*"],
                allow_methods=[
                    CorsHttpMethod.GET,
                    CorsHttpMethod.POST,
                    CorsHttpMethod.OPTIONS,
                ],
                max_age=Duration.days(1),
            ),
        )

        # create integration for the Lambda function
        get_integration = HttpLambdaIntegration(
            "GetShortenerIntegration", get_url_shortener_lambda
        )
        create_integration = HttpLambdaIntegration(
            "CreateShortenerIntegration", create_url_shortener_lambda
        )

        # add route for GET /{shortUrl}
        http_api.add_routes(
            path="/{shortUrl}", methods=[HttpMethod.GET], integration=get_integration
        )

        # add route for POST /
        http_api.add_routes(
            path="/", methods=[HttpMethod.POST], integration=create_integration
        )

        # add an Output with the API Url
        CfnOutput(
            self,
            "url-shortener-api-url",
            value=http_api.url,
            description="URL Shortener API URL",
        )
