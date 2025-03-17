import boto3
import logging
from botocore.exceptions import ClientError


logging.basicConfig(level=logging.INFO)

def fetch(image_urls):
    try:
        s3_client = boto3.client(
            's3',
            endpoint_url='https://s3.ir-thr-at1.arvanstorage.ir',
            aws_access_key_id='e3192682-c848-4b02-9c70-0e0c368c54af',
            aws_secret_access_key='fc5d8b0f2f09c3d37b7491b47ae0fb9f4c958b5f78977a152e21eed8c3525903'
        )

        bucket_name = 'new-online-shop'

        result = []
        
        for url in image_urls:

            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': url},
                ExpiresIn=3600
            )

            result.append(presigned_url)

        return result
    except ClientError as e:
        logging.error(e)
