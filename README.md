# s3Compression
S3compression is an application used to minimize AWS S3 storage utilization with the intent of keeping storage fees down. The primary purpose of this project is to demonstrate some of the features of certain AWS services as well as how to leverage them. This project utilizes the S3, EC2, DynamoDB, and Lambda services.

Automatically compress files uploaded to an AWS S3 bucket.  By default all files over 1MB that have extensions other than .zip are compressed.

## Languages And Services

* Python
* Flask
* AWS S3
* AWS EC2
* AWS Lambda
* AWS DynamoDB

## Instructions

### Source Code

All source code is available from the project&#39;s GitHub repository:

[https://github.com/dboggs0/s3Compression.git](https://github.com/dboggs0/s3Compression.git)

### Create an EC2 Instance

From the EC2 Management Console select Launch Instances, and then Launch Instances on the drop-down.

Choose an AMI. Any free-tier-eligible Linux or Windows AMI should work, but the initial development was done on Ubuntu Server 20.04.

Select the instance type. The only free-tier-eligible instance type is t2.micro, which is suitable to run this application.

Configure Security Group. Select the port over which the statistics site will be accessed. By default, the application will run on TCP port 5000. Setting the source field to &quot;0.0.0.0/0&quot; opens access to any WAN-connected host.

Click Review and Launch, then Launch.

Generate and download a key pair.

Full instructions on how to access the new instance using the key pair are available at the following link:

[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)

Upgrade the OS packages

_$ sudo apt update_

_$ sudo apt upgrade_

This process will take a few minutes. While it progresses create an AWS Security Credential.

Click Create New Access Key

Download the key file. Once the key file is downloaded it cannot be downloaded a second time. Make sure to keep the downloaded file somewhere safe.

Make note of the Access Key ID, and Secret Access Key.

Go back to the EC2 Instance Console.

Make sure that zip is installed. If not, it can be installed with the following command (Ubuntu):

_$ apt install zip_

Install the AWS CLI.

[https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html#cliv2-linux-install)

_$ curl &quot;https://awscli.amazonaws.com/awscli-exe-linux-x86\_64-2.0.30.zip&quot; -o &quot;awscliv2.zip&quot;_

_$ unzip awscliv2.zip_

_$ sudo ./aws/install_

Add your access key to the AWS CLI.

_$ aws configure_

_AWS Access Key ID [None]: \*\*\*…\*TBQQ_

_AWS Secret Access Key [None]: \*\*\*…\*K0a5A1_

_Default region name [None]: us-east-2_

_Default output format [None]:_

For a list of region codes refer here:

[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-available-regions)

Clone the GitHub repository.

_$ git clone https://github.com/dboggs0/s3Compression.git_

Install Python 3.6 or higher.

_$ sudo apt install python_

Install virtualenv.

_$ sudo apt install virtualenv_

Create a virtual environment for the project.

_$ virtualenv s3Compression_

Activate the virtual environment.

_$ cd s3Compression/bin_

_$ . activate_

Install the project dependencies.

_$ cd .._

_$ pip install -t requirements.txt_

The Statistics Site is now installed. It will be started later.

## Create an S3 Bucket

Go to S3 in the AWS Management Console.

Click &quot;Create Bucket&quot;

Name the bucket.

Make sure the Region is the same as the one for the EC2 instance.

The default name for the bucket in this project is s3compression. If you want to use a different one the code will need to be updated.

## Create a DynamoDB Table

Go to DynamoDB in the AWS Management Console.

Click &quot;Create table&quot;

The default table name for this project is CompressionJobHistory. To use the default table name fill out the form as follows:

In order to use a different table name the project code must be modified.

## Create Lambda Function

Go to Lambda in the AWS Management Console.

Click &quot;Create function&quot;

Select &quot;Author from scratch&quot;. The name of the function does not matter. Select the Python 3.8 runtime.

The lamba function configuration is not yet complete, but before proceeding further permissions must be added to the lambda function.

Go to IAM in the AWS Management Console.

Select Roles on the navigation tree.

Click &quot;Create role&quot;.

Select Lambda from the list of services.

Add AmazonDynamoDBFullAccess

Add AmazonS3FullAccess

Proceed through the wizard until the Review page. Name the role. The name does not matter

Go to Lambda in the AWS Management Console.

Open your lamda function.

Select Permissions.

Select the security role that was created in IAM.

Click &quot;Add trigger&quot;

Select S3.

Fill out the trigger configuration as follows:

Make sure to check the acknowledgement at the bottom. Be careful when modifying the project code. Recursive invocations can cost a lot of money very quickly.

Click on the Lambda symbol in the Designer.

Open the lambdaFunction.py in a text editor to copy the code. It is in the src directory of the project.

Copy the code and past it into the Function code section of the page.

Click Deploy.

At this point the statistic site can be started.

On the EC2 Instance run the following commands.

_$ export FLASK\_APP=&quot;routes.py&quot;_

_$ flask run –host=0.0.0.0_

The installation is complete.

## Using the Application

Upload any file to S3. As long as it is not a zip file the Lambda function will trigger and compress it.

To access the statistics site, get the external IP or DNS name of the EC2 instance, put it in the address bar of a web browser and add &quot;:5000&quot; to the end. The site does not auto-refresh. Refresh the browser page periodically for more current statistics.
