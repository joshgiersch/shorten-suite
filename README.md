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
(This sets up the "next URL suffix".)
  
## Lambda setup
You'll need to create two functions: 

* `shorten-suite-create`
  * In shorten-suite-create, insert the Base36.py and ShortenSuite-create.py
  * Set the APP_URL variable to the root of your shortener URL (don't forget the trailing slash!)
* `shorten-suite-get`
  * In shorten-suite-get, insert ShortenSuite-get.py; you don't need Base36.py for this one. 

## API Gateway setup

This is the bit that I found gnarliest. Set up two methods: 

### GET /{shortid} 

* Connect it to the `shorten-suite-get` Lambda function;
* In the Method Response settings:
  * Delete the 200 response code
  * Add a 301 response code, and add a Response Header called `Location`;
* In the Integration Response settings:
  * Add a 301 Method Response Status; 
  * Then add a Header Mapping: Response Header `Location` to Mapping Value `integration.response.body.location`

What this does: When the Lambda function returns a 301, it grabs the `location` field from the response body, and pipes that into the Location header of the 301 response that gets sent back to the client. The browser sees the 301 and redirects (or at least it should). 

### POST / (the Create Short URL function)
 
* Set up a Lambda proxy integration, connected to the `shorten-suite-create` Lambda function;
* In the Method Reponse settings, for HTTP status 200, add a response body, content type `application/json`. 
* You might also want to set `API Key required` to True on the Method Request, and create an API key to drive it, just so that randos can't create new URLs at your endpoint.
  * If you do this, you'll also need to set up a Usage Plan to enable the API key controls. You don't need to impose throttling or quotas; just attach it to the deployed API stage.

## TODO
* Add a check for the URL already existing
* Add the max_index json blob format
