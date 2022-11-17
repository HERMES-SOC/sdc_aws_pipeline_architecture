.. _repo_guide:

Repository Guide
================

This guide is to help navigate through the different repositories that are required for the SDC AWS Pipeline. The use of each repository is explained in the following sections. 


.. _sdc_aws_pipeline_architecture:

SDC AWS Pipeline Architecture
-----------------------------
This repository is what deploys all the cloud resources required for the SDC AWS Pipeline. It makes use of AWS Cloud Development Kit (CDK) to deploy the resources. The repo includes three different CDK stacks (located within the `cdk_deployment` folder) of cloud resources that to AWS:

- **SDCAWSPipelineArchitectureStack** - a stack that deploys the underlying infrastructure (S3 Buckets, ECR repositories, Timestream Databases, etc).
- **SDCAWSSortingLambdaStack** - a stack that deploys the SDC Sorting Lambda Function (as a zip deployment based off the sdc_aws_sorting_lambda repo).
- **SDCAWSProcessingLambdaStack** - a stack that deploys the SDC Processing Lambda Function (as a container image deployment based off the sdc_aws_processing_lambda repo). 

.. Note:: 
    
    The **SDCAWSSortingLambdaStack** and **SDCAWSProcessingLambdaStack** CDK stacks are dependent on the **SDCAWSPipelineArchitectureStack** CDK stack. 
    
    Also the **SDCAWSProcessingLambdaStack** stack is dependent on the SDC AWS Base Image being built and pushed to the Public ECR Repo after, which is currently being handled within it's own `GitHub repository <https://github.com/HERMES-SOC/sdc_aws_base_docker_image>`_ .

.. _sdc_aws_base_docker_image:

SDC AWS Base Docker Image
-------------------------
This repo contains a dockerfile and Python requirements file that is used to build the SDC AWS Base Docker Image. This image is used throughout the different `.devcontainer` repositories (hermes_core and instrument packages) as well as the base image for the Lambda Processing function within the file processing pipeline. 

The image is built, tested and pushed to the public ECR repository automatically through a CI/CD Pipeline allowing anyone to make changes to the base image. This repository is currently configured to run tests and linting workflows with `GitHub Actions <https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions>`_ on Pull Requests. Once the Pull Request is approved and merged into main it then triggers an AWS CodeBuild workflow to test, build and push the image to the Public ECR repository.

Link to the `GitHub repository <https://github.com/HERMES-SOC/sdc_aws_base_docker_image>`_.

Link to the `Repository Documentation <https://sdc-aws-base-docker-image.readthedocs.io/en/main/>`_.

.. Note::

    It is possible to build the image locally using the `Dockerfile` and `requirements.txt` files and then manually push the image to the Public ECR repository. However, make sure you have deployed the **SDCAWSPipelineArchitectureStack** CDK Stack first as this stack includes the creation of the Public ECR Repo.

.. _sdc_aws_sorting_lambda:

SDC AWS Sorting Lambda
----------------------

This repo contains the source code for the SDC Sorting Lambda Function that. This is the function that is triggered whenever a new file is uploaded to the incoming S3 Bucket. The function is responsible for sorting the file into the correct directory structure and then triggering the SDC Processing Lambda Function.

.. _sdc_aws_processing_lambda:

SDC AWS Processing Lambda
-------------------------



