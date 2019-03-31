import Base36
import boto3
import json

APP_URL = "http://jg.sg/"
RESERVED_WORDS = ["create","max_index"]

ddb = boto3.resource('dynamodb', region_name = 'us-east-1').Table('shorten-suite-urls')

def get_next_id():
    max_index = ddb.get_item(Key={"short_id": "max_index"})["Item"]["max_index"]
    next_id = Base36.encode(Base36.decode(max_index)+1)
    while next_id in RESERVED_WORDS:
        next_id = Base36.encode(Base36.decode(max_index)+1)
    response = ddb.put_item(Item={'short_id': "max_index", "max_index": next_id})
    return next_id

def lambda_handler(event={}, context={}):
    try:
        long_url = event['body']
        short_id = get_next_id()
        short_url = APP_URL + short_id
        response = ddb.put_item(Item={'short_id': short_id, 'long_url': long_url})

    except:
        return {
            "statusCode": 500,
            "body": ""
        }

    return {
        "statusCode": 200,
        "body": short_url
    }
