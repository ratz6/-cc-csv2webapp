import json
import boto3
from boto3.dynamodb.conditions import Key
import datetime
import random


def update(d):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Cupcakes')

    table.update_item(
        Key={
            'Id': d['Id']
        },
        UpdateExpression="set Cupcakes = :c, update_time = :s",
        ExpressionAttributeValues={
            ':s': d['update_time'],
            ':c': d['Cupcakes']
        },
        ReturnValues="UPDATED_NEW"
    )


def lambda_handler(event, context):
    new = random.sample(range(1, 207), 100)
    d = {}
    for i in range(len(new)):
        d['Id'] = new[i]
        d['Cupcakes'] = random.randint(1, 101)
        now = datetime.datetime.now()
        d['update_time'] = now.strftime("%d/%m/%Y %H:%M:%S")
        update(d)
    return {
        'statusCode': 200,
        'body': json.dumps('Table Updated')
    }
