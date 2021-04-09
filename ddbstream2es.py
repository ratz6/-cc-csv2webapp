# TO SEND DYNAMO_DB STREAMS TO ELASTICSEARCH.
# THE LAMBDA FUNCTION HAS A HANDLER NAMED ' sample.handler'
# THIS LAMBDA FUNCTION TRIGGERS WHEN THERE IS ANY CHANGE IN DYNAMO_DB RECORDS.
import boto3
import requests
from requests_aws4auth import AWS4Auth

region = 'ap-south-1'  # e.g. us-east-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-cucakes-es-pzl6er4a5un7wkd5tox6s5c5ti.ap-south-1.es.amazonaws.com'  # the Amazon ES domain, with https://
index = 'lambda-index'
typo = 'lambda-type'
url = host + '/' + index + '/' + typo + '/'

headers = {"Content-Type": "application/json"}


def handler(event, context):
    count = 0
    for record in event['Records']:
        print(event)
        # Get the primary key for use as the Elasticsearch ID
        ind = record['dynamodb']['Keys']['Id']['N']

        if record['eventName'] == 'REMOVE':

            document = record['dynamodb']['OldImage']
            r = requests.put(url + str(ind), auth=awsauth, json=document, headers=headers)

        elif record['eventName'] == 'MODIFY':

            document_new = record['dynamodb']['NewImage']
            new_Cupcakes = document_new['update_time']['S']
            document_old = record['dynamodb']['OldImage']
            old_Cupcakes = document_old['update_time']['S']
            if old_Cupcakes == new_Cupcakes:
                r = requests.put(url + str(ind), auth=awsauth, json=document_old, headers=headers)
            else:
                document_new = record['dynamodb']['NewImage']
                r = requests.put(url + str(ind), auth=awsauth, json=document_new, headers=headers)

        else:
            document = record['dynamodb']['NewImage']
            r = requests.put(url + str(ind), auth=awsauth, json=document, headers=headers)
        count += 1
    return str(count) + 'records processed.'