import boto3
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from botocore.utils import datetime2timestamp
from datetime import datetime
import time

tempFile = '/tmp/tempFile'

s3 = boto3.resource('s3')
bucket = s3.Bucket('s3compression')

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

def compress(object):
    fExt = object.key.split('.')[-1]
    fName = object.key.split('.')[-2]
    originalFileSize = object.size

    zipBuffer = BytesIO()
    zipFile = ZipFile(zipBuffer, mode='w', compression=ZIP_DEFLATED)


    imageFile = BytesIO()

    bucket.download_fileobj(str(object.key), imageFile)

    imageFile.seek(0)

    zipFile.writestr(object.key, imageFile.read())
    zipFile.close()

    zipBuffer.seek(0)

    timeStamp = time.time().split('.')[0]
    bucket.upload_fileobj(fName + "_" + str(timeStamp) + ".zip")

    bucketObjects = bucket.objects.all()
    compressedSize = 0

    for i in bucketObjects:
        if (i.key == fName + "_" + str(timeStamp) + ".zip"):
            compressedSize = i.size

    zipBuffer.close()

    bucket.delete_objects(
        Delete={
            'Objects': [
                {
                    'Key': object.key
                }
            ],
            'Quiet': True
        }
    )
    addJobHistory(fName + ".zip", originalFileSize, compressedSize)


    
def lambda_handler(event, context):

    obj = bucket.objects.all()
    
    for i in obj:
        fExt = i.key.split('.')[-1]
        fName = i.key.split('.')[-2]
        if fExt == 'bmp':
            compress(i)
