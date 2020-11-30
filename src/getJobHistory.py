import boto3
from boto3.dynamodb.conditions import Key
import humanfriendly

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CompressionJobHistory')
#tableDict = table.scan()

def getItemList():
    tableDict = table.scan()
    return tableDict["Items"]

def getStats(ItemList):
    totalItems = 0
    totalUploadBytes = 0
    totalCompressedBytes = 0
    dateList = []

    for i in ItemList:
        
        totalItems += 1
        day = i["Date"].split(' ')[0]
        if day not in dateList:
            dateList.append(day)
        
        totalUploadBytes += i['OriginalSize']
        totalCompressedBytes += i['CompressedSize']

    avgFilesPerDay = totalItems / len(dateList)
    totalBytesSaved = humanfriendly.format_size(totalUploadBytes - totalCompressedBytes)
    percentBytesSaved = '%2.2f' % ((1 - totalCompressedBytes / totalUploadBytes) * 100 )
    percentBytesSaved = percentBytesSaved + "%"

    '''
    print("Total files:\t" + str(totalItems))
    print("Average files per day:\t" + str(avgFilesPerDay))
    print("Total bytes uploaded:\t" + str(totalUploadBytes))
    print("Total bytes after compression:\t" + str(totalCompressedBytes))
    print("Total bytes saved\t" + str(totalBytesSaved))
    print("Percent saved\t" + str(percentBytesSaved) )
    '''    

    return {"totalItems": totalItems, 
        "avgFilesPerDay": avgFilesPerDay, 
        "totalUploadBytes": humanfriendly.format_size(totalUploadBytes),
        "totalCompressedBytes": humanfriendly.format_size(totalCompressedBytes),
        "totalBytesSaved": totalBytesSaved, 
        "percentBytesSaved": percentBytesSaved
    }


#print(tableDict["Items"])  #list of dictionaries
#dictionary looks like this:
# {'CompressedSize': Decimal('2635'), 'Date': '2020-11-28 08:26:20.053450', 'FileName': 'smiley.zip', 'OriginalSize': Decimal('308214')}

if __name__ == "__main__":

    statsDict = getStats(tableDict["Items"])

    print("Total files:\t" + str(statsDict['totalItems']))
    print("Average files per day:\t" + str(statsDict['avgFilesPerDay']))
    print("Total bytes uploaded:\t" + str(statsDict['totalUploadBytes']))
    print("Total bytes after compression:\t" + str(statsDict['totalCompressedBytes']))
    print("Total bytes saved\t" + str(statsDict['totalBytesSaved']))
    print("Percent saved\t" + str(statsDict['percentBytesSaved']) )