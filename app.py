#!/usr/bin/env python3
import os
import yaml
import aws_cdk as cdk
from cdk_deployment.sdc_aws_pipeline_architecture import SDCAWSPipelineArchitectureStack
from cdk_deployment.sdc_aws_processing_lambda import SDCAWSProcessingLambdaStack
from cdk_deployment.sdc_aws_sorting_lambda import SDCAWSSortingLambdaStack

# Initialize constants to be parsed from config.yaml
config = {}

# Read YAML file and parse variables
try:
    with open("./config.yaml", "r") as f:
        loaded_config = yaml.safe_load(f)
        print("config.yaml loaded successfully")

        bucket_list = []
        public_ecr_repo_list = []
        private_ecr_repo_list = []
        for key, value in loaded_config.items():
            if "BUCKET_NAME" in key:
                bucket_list.append(value)
            if "PUBLIC_ECR_NAME" in key:
                public_ecr_repo_list.append(value)
            if "PRIVATE_ECR_NAME" in key:
                private_ecr_repo_list.append(value)

            config[key] = value

        # Initialize other constants after loading YAML file
        config["INSTR_TO_BUCKET_NAME"] = [
            f"{config['MISSION_NAME']}-{this_instr}"
            for this_instr in config["INSTR_NAMES"]
        ]
        config["BUCKET_LIST"] = bucket_list + config["INSTR_TO_BUCKET_NAME"]
        config["ECR_PUBLIC_REPO_LIST"] = public_ecr_repo_list
        config["ECR_PRIVATE_REPO_LIST"] = private_ecr_repo_list

except FileNotFoundError:
    print("config.yaml not found. Check to make sure it exists in the root directory.")
    exit(1)


app = cdk.App()


# Initialize Deployment Stack
SDCAWSPipelineArchitectureStack(
    app,
    "SDCAWSPipelineArchitectureStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=config["DEPLOYMENT_REGION"]
    ),
    config=config,
)

# Initialize Processing Lambda Stack
SDCAWSProcessingLambdaStack(
    app,
    "SDCAWSProcessingLambdaStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=config["DEPLOYMENT_REGION"]
    ),
    config=config,
)

# Initialize Sorting Lambda Stack
SDCAWSSortingLambdaStack(
    app,
    "SDCAWSSortingLambdaStack",
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=config["DEPLOYMENT_REGION"]
    ),
    config=config,
)

# Synthesize Cloudformation Template
app.synth()
