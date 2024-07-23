from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    Stack
)
from constructs import Construct

class AwsCdkFlaskStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the Lambda function
        my_lambda = _lambda.Function(
            self, "MyFlaskLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="lambda_handler.handler",  # Adjust if your Flask app entry point is different
            code=_lambda.Code.from_asset("App"),  # Path to your Flask app directory
            environment={
                # Environment variables can be set here if needed
            }
        )

        # Define the API Gateway
        api = apigateway.LambdaRestApi(
            self, "MyApi",
            handler=my_lambda,
            proxy=False
        )

        items = api.root.add_resource("items")
        items.add_method("ANY")  # You can change this to specific methods like GET, POST, etc.
