import boto3

s3 = boto3.client('s3')

def get_s3_image_info(bucket, image_name):
    s3_response = s3.head_object(Bucket=bucket, Key=image_name)
    created_image_time = s3_response['LastModified'].strftime("%d-%m-%Y %H:%M:%S")
    image_url = f"https://{bucket}.s3.amazonaws.com/{image_name}"
    return created_image_time, image_url
