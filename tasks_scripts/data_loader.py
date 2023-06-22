import boto3

# Configure AWS credentials
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
region_name = 'YOUR_REGION_NAME'  # e.g., 'us-west-2'

# Create an S3 client
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)
bucket_name = 'YOUR_BUCKET_NAME'
object_key = 'YOUR_OBJECT_KEY'  # The key/path of the CSV file in the bucket

response = s3.get_object(Bucket=bucket_name, Key=object_key)
csv_data = response['Body'].read().decode('utf-8')


