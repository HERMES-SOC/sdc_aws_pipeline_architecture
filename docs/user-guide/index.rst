.. _guide:

************
User's Guide
************

Welcome to our User Guide. This guide will help you to get started with downloading this code and getting the pipeline set-up and running on your own AWS account. It will walk through each step of the process and provide you with the necessary information to get started.

Prerequisites
=============
* An AWS account
* AWS Cli installed and configured
* CDK 2.0 installed on your machine
* Python 3.7 or higher
* Node.js 10.3.0 or higher
* Docker installed on your machine 

Getting Started
===============
This guide assumes that you have already set up an AWS account and have the necessary permissions to create and manage AWS resources. If you do not have an AWS account, you can sign up for one at https://aws.amazon.com/. If you are new to AWS, you can find a number of resources to help you get started at https://aws.amazon.com/getting-started/.

It also walks through the steps that would be handled by CI/CD if you were to set it up as part of your project. If you are not familiar with CI/CD, you can find a number of resources to help you get started at https://aws.amazon.com/devops/continuous-delivery/.

.. _step1:

Step 1: Download the Code
=========================
The first step is to download the code from GitHub. You can do this by running the following command:
    git clone https://github.com/HERMES-SOC/sdc_aws_pipeline_architecture.git && cd sdc_aws_pipeline_architecture

This will create a directory called sdc_aws_pipeline_architecture in your current directory. This directory contains all of the code that you will need to run the pipeline.

.. _step2:

Step 2: Install dependencies for project
========================================
The next step is to install the dependencies for the project. You can do this by running the following command:
    npip install -r requirements.txt

.. .. toctree::
..    :maxdepth: 3

..    dockerfile-changes
..    python-packages