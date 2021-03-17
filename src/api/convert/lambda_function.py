import boto3
import os
import subprocess
import traceback
import uuid


def log(event):
    try:
        request_id = event['requestContext']['requestId']
        ip = event['requestContext']['identity']['sourceIp']
        document_url = event['queryStringParameters']['document_url']

        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(os.getenv("TABLE_NAME"))
        table.put_item(
            Item={
                'id': request_id,
                'ip': ip,
                'document_url': document_url
            }
        )
    except Exception as e:
        raise e


def lambda_handler(event, context):
    try:
        log(event)

        document_url = event['queryStringParameters']['document_url']

        txt = subprocess.Popen("curl --silent -L %s | /lib64/ld-linux-x86-64.so.2 ./bin/catdoc -" % document_url,
                               stdout=subprocess.PIPE, shell=True).communicate()[0]

        key = str(uuid.uuid4())
        s3 = boto3.resource('s3')
        obj = s3.Object(os.getenv("BUCKET_NAME"), key)
        obj.put(ACL='public-read', ContentType='text/html', Body=txt)

        return {
            'statusCode': 302,
            'headers': {
                'Location': "%s/%s" % (os.getenv("BUCKET_URL"), key)
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': repr(traceback.format_tb(e.__traceback__))
        }
