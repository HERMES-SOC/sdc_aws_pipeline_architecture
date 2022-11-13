import os
from datetime import datetime
from aws_cdk import (
    Stack,
    aws_lambda,
    aws_ecr,
    aws_iam,
    Duration,
    aws_s3,
    aws_s3_notifications,
    Tags,
)
from constructs import Construct
import logging


class SDCAWSProcessingLambdaStack(Stack):
    def __init__(
        self, scope: Construct, construct_id: str, config: dict, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ECR Repo Name
        repo_name = config["PROCESSING_LAMBDA_PRIVATE_ECR_NAME"]

        # Get SDC Processing Lambda ECR Repo
        ecr_repository = aws_ecr.Repository.from_repository_name(
            self, id=f"{repo_name}_repo", repository_name=repo_name
        )

        # Get time tag enviromental variable
        TAG = os.getenv("TAG") if os.getenv("TAG") is not None else "latest"

        # Create Container Image ECR Function
        sdc_aws_processing_function = aws_lambda.DockerImageFunction(
            scope=self,
            id=f"{repo_name}_function",
            function_name=f"{repo_name}_function",
            description=(
                "SWSOC Processing Lambda function deployed using AWS CDK Python"
            ),
            timeout=Duration.minutes(10),
            code=aws_lambda.DockerImageCode.from_ecr(ecr_repository, tag_or_digest=TAG),
            environment={"LAMBDA_ENVIRONMENT": "PRODUCTION"},
        )

        # Give Lambda Read/Write Access to all Timestream Tables
        sdc_aws_processing_function.add_to_role_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=[
                    "timestream:WriteRecords",
                    "timestream:DescribeEndpoints",
                    "timestream:DescribeDatabase",
                    "timestream:DescribeTable",
                ],
                resources=["*"],
            )
        )
        # Grant Access to Repo
        ecr_repository.grant_pull_push(sdc_aws_processing_function)

        # Apply Standard Tags to CW Event
        self._apply_standard_tags(sdc_aws_processing_function)

        # Attach bucket event to lambda function with target
        for bucket in config["INSTR_TO_BUCKET_NAME"]:
            # Get the incoming bucket from S3
            lambda_bucket = aws_s3.Bucket.from_bucket_name(
                self, f"aws_sdc_{bucket}", bucket
            )
            lambda_bucket.grant_read_write(sdc_aws_processing_function)

            # Add Trigger to the Bucket to call Lambda
            for data_level in config["VALID_DATA_LEVELS"]:
                lambda_bucket.add_event_notification(
                    aws_s3.EventType.OBJECT_CREATED,
                    aws_s3_notifications.LambdaDestination(sdc_aws_processing_function),
                    aws_s3.NotificationKeyFilter(prefix=data_level),
                )

        logging.info("Function created successfully: %s", sdc_aws_processing_function)

    def _apply_standard_tags(self, construct):
        """
        This function applies the default tags to the different resources created
        """

        # Standard Purpose Tag
        Tags.of(construct).add(
            "Purpose", "SWSOC Pipeline", apply_to_launched_instances=True
        )

        # Standard Last Modified Tag
        Tags.of(construct).add("Last Modified", str(datetime.today()))

        # Environment Name
        environment_name = (
            "Production"
            if os.getenv("CDK_ENVIRONMENT") == "PRODUCTION"
            else "Development"
        )

        # Standard Environment Tag
        Tags.of(construct).add("Environment", environment_name)

        # Git Version Tag If It Exists
        if os.getenv("GIT_TAG"):
            Tags.of(construct).add("Version", os.getenv("GIT_TAG"))
