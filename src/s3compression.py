import boto3
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from dynamo import *
import time


# Print out bucket names
#for bucket in s3.buckets.all():
#    print(bucket.name)

tempFile = '/tmp/tempFile'

s3 = boto3.resource('s3')
bucket = s3.Bucket('s3compression')

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
    timeStamp = str(time.time()).split('.')[0]
    bucket.upload_fileobj(zipBuffer, fName + "_" + str(timeStamp) + ".zip")

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
    addJobHistory(fName + "_" + str(timeStamp) + ".zip", originalFileSize, compressedSize)


    


obj = bucket.objects.all()



for i in obj:
    fExt = i.key.split('.')[-1]
    fName = i.key.split('.')[-2]
    if fExt == 'bmp':
        compress(i)


        



