# shorten-suite
A serverless URL shortener (Lambda + API Gateway + DynamoDB) 

## Introduction

Shorten Suite implements RESTful APIs for creating and retrieving shortened URLs (bit.ly style). 

There are two endpoints: 

`POST /create` takes a JSON object of the form `{"long_url": "(url)"}`, and returns the corresponding short URL created. 
`GET /{short_url}` takes no input, and returns a 301 redirect to the corresponding long url, or a 404 if there's no long URL corresponding to the short URL. 

## DynamoDB setup

1) Set up a completely default DynamoDB table called `shorten-suite-urls`. 
2) Insert an item as follows: (TODO: fix this) 
`{"short_id": "max_index"}
{"max_index": "1"}`
This sets up the "next URL suffix". 
  
## Lambda setup
You'll need to create two functions: 

* `shorten-suite-create`
** In shorten-suite-create, insert the Base36.py and ShortenSuite-create.py
** Set the APP_URL variable to the root of your shortener URL (don't forget the trailing slash!)
* `shorten-suite-get`
** In shorten-suite-get, insert ShortenSuite-get.py; you don't need Base36.py for this one. 

## API Gateway setup

TODO: 

* Add a check for the URL already existing
* Add the max_index json blob format
* Document required API Gateway configuration (including security on the POST method) 
