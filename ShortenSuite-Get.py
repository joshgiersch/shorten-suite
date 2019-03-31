import json
import boto3

ddb = boto3.resource('dynamodb', region_name = 'us-east-1').Table('shorten-suite-urls')

def lambda_handler(event={}, context={}):
    short_id = event.get('short_id')

    try:
        item = ddb.get_item(Key={'short_id': short_id})
        long_url = item.get('Item').get('long_url')
       
    except:
        return {
            'statusCode': 404
        }

    return {
        "statusCode": 301,
        "location": long_url
    }
