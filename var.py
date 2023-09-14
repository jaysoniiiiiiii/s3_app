import boto3
import botocore

from flask import Flask, request, jsonify
import json
from flask_cors import CORS

# from engine import *
# from variables import*
# from bucket_policy import *




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


def bucket_policy(source_bucket_name,destination_account_id,destination_account_username, source_account_access_key, source_account_secret_access_key):
    # Replace 'your_bucket_name' with the actual name of your S3 bucket
   
    source_session = boto3.session.Session(
        aws_access_key_id=source_account_access_key,
        aws_secret_access_key=source_account_secret_access_key,
        region_name='us-east-1'
    )

    print(source_bucket_name)

    # Replace 'your_new_policy' with the new bucket policy you want to set
    new_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{destination_account_id}:user/{destination_account_username}"
                },
                "Action": [
                    "s3:GetObject",
                    "s3:GetObjectTagging",
                    "s3:ListBucket"
                ],
                "Resource": [
                    f"arn:aws:s3:::{source_bucket_name}",
                    f"arn:aws:s3:::{source_bucket_name}/*"
                ]
            }
        ]
    }
    new_policy_json = json.dumps(new_policy)


                

    # Create the S3 client
    s3_client = source_session.client('s3')

    # Set the new policy for the bucket
    response = s3_client.put_bucket_policy(Bucket=source_bucket_name, Policy=new_policy_json)
    print("success")
    return "success"




def iam_policy(source_bucket_name, destination_bucket_name, destination_account_username, destination_account_access_key, destination_account_secret_access_key):
    destination_session = boto3.session.Session(
        aws_access_key_id=destination_account_access_key,
        aws_secret_access_key=destination_account_secret_access_key,
        region_name='us-east-1'
    )

    source_bucket_name = source_bucket_name
    destination_bucket_name = destination_bucket_name
    # Replace 'YOUR_USER_NAME' with the username of the IAM user you want to attach the policy to
    destination_account_username = destination_account_username

    # Replace 'YOUR_POLICY_NAME' with a unique name for your policy
    policy_name = "s3transferpolicy"

    # Replace 'YOUR_POLICY_DOCUMENT' with the JSON-formatted policy you want to attach
    # This example grants permission to list all S3 buckets in the account
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AllowAssumeRole",
                "Effect": "Allow",
                "Action": "sts:AssumeRole",
                f"Resource": "arn:aws:iam::182418951738:user/Jaysoni"
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:GetObject"
                ],
                "Resource": [
                    f"arn:aws:s3:::{source_bucket_name}",
                    f"arn:aws:s3:::{source_bucket_name}/*"
                ]
            },
            {
                "Effect": "Allow",
                "Action": [
                    "s3:ListBucket",
                    "s3:PutObjectTagging",
                    "s3:PutObject",
                    "s3:PutObjectAcl"
                ],
                "Resource": [
                    f"arn:aws:s3:::{destination_bucket_name}",
                    f"arn:aws:s3:::{destination_bucket_name}/*"
                ]
            }
        ]
    }

    # Convert the policy document dictionary to a JSON-formatted string
    policy_document_json = json.dumps(policy_document)

    # Create the IAM client
    iam_client = destination_session.client('iam')

    # Create the policy
    response = iam_client.create_policy(
        PolicyName=policy_name,
        PolicyDocument=policy_document_json
    )

    # Get the ARN of the newly created policy
    policy_arn = response['Policy']['Arn']

    # Attach the policy to the IAM user
    response = iam_client.attach_user_policy(
        UserName=destination_account_username,
        PolicyArn=policy_arn
    )




def copy_file(file_name, source_bucket_name,destination_bucket_name,source_account_access_key,source_account_secret_access_key,destination_account_access_key,destination_account_secret_access_key):
    # buckets names
    source_bucket_name = source_bucket_name
    destination_bucket_name = destination_bucket_name


    source_session = boto3.session.Session(
        aws_access_key_id=source_account_access_key,
        aws_secret_access_key=source_account_secret_access_key,
        region_name='us-east-1'
    )
    source_s3 = source_session.client('s3')

    destination_session = boto3.session.Session(
        aws_access_key_id=destination_account_access_key,
        aws_secret_access_key=destination_account_secret_access_key,
        region_name='us-east-1'
    )
    destination_s3 = destination_session.client('s3')

    response = source_s3.list_objects_v2(Bucket=source_bucket_name)


    file_name =  file_name

    try:
        copy_source = {'Bucket': source_bucket_name, 'Key': file_name}
        destination_s3.copy(copy_source, destination_bucket_name, file_name)
        print(f"File '{file_name}' moved successfully from '{source_bucket_name}' to '{destination_bucket_name}'.")

    except botocore.exceptions.ClientError as e:
        print(f"Error occurred: {e.response['Error']['Code']}")





def engine(file_name, source_bucket_name,destination_bucket_name,destination_account_id,destination_account_username, source_account_access_key, source_account_secret_access_key,destination_account_access_key, destination_account_secret_access_key):
    bucket_policy(source_bucket_name,destination_account_id,destination_account_username, source_account_access_key, source_account_secret_access_key)
    
    iam_policy(source_bucket_name, destination_bucket_name, destination_account_username, destination_account_access_key, destination_account_secret_access_key)
    
    copy_file(file_name, source_bucket_name,destination_bucket_name,source_account_access_key,source_account_secret_access_key,destination_account_access_key,destination_account_secret_access_key)
    return "successsssss"





@app.route('/add', methods=['POST'])
def variables():
    try:
        # Assuming the input will be in JSON format with 'a' and 'b' as keys
        data = request.get_json()
        # a = data.get('a')
        # b = data.get('b')

        source_bucket_name = data.get('source_bucket_name')
        source_account_id = data.get('source_account_id')
        source_account_access_key = data.get('source_account_access_key')
        source_account_secret_access_key = data.get('source_account_secret_access_key')

        destination_bucket_name = data.get('destination_bucket_name')
        destination_account_id = data.get('destination_account_id')
        destination_account_username = data.get('destination_account_username')
        destination_account_access_key = data.get('destination_account_access_key')
        destination_account_secret_access_key = data.get('destination_account_secret_access_key')
        file_name = data.get('file_name')

        
        if source_bucket_name is None or source_account_id is None or source_account_access_key is None or source_account_secret_access_key is None or destination_account_id is None or destination_account_username is None or destination_account_access_key is None or destination_account_secret_access_key is None:
            return jsonify({'error': 'Both "a" and "b" must be provided.'}), 400

        # Perform the addition operation using the logic function
        result = engine(file_name, source_bucket_name,destination_bucket_name,destination_account_id,destination_account_username, source_account_access_key, source_account_secret_access_key,destination_account_access_key, destination_account_secret_access_key)

        # Return the result as a JSON response
        return jsonify({'result': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
