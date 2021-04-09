import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

region = 'ap-south-1'  # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = 'https://search-cucakes-es-pzl6er4a5un7wkd5tox6s5c5ti.ap-south-1.es.amazonaws.com'  # For example, search-mydomain-id.us-west-1.es.amazonaws.com
index = 'lambda-index'

headers = {"Content-Type": "application/json"}


def handler(event, context):
    a = []
    user_data = getData()
    for hit in user_data['hits']['hits']:
        d = {
            "id_final": int(hit['_source']['Id']['N']),
            "month_final": hit['_source']['Month']['S'],
            "cupcake_final": int(hit['_source']['Cupcakes']['N'])
        }
        a.append(d)
        b = sorted(a, key=lambda i: i['id_final'])
    print(b)
    op = json.dumps(b)

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False,
        "body": op
    }
    return response


def getData():
    query = {
        "size": 10000,

        "query": {
            "match_all": {}

        }
    }

    url = host + '/' + index + '/_search?size=10000'

    # Make the signed HTTP request
    response = json.loads(requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query)).text)

    return response