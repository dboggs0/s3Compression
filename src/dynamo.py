import boto3

from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CompressionJobHistory')

def addJobHistory(fileName, originalSize, compressedSize):
    table.put_item(
        Item={
            'Date': str(datetime.now()),
            'FileName': fileName,
            'OriginalSize': originalSize,
            'CompressedSize': compressedSize
        }
    )

def getJobsOnDay(date):
    pass



