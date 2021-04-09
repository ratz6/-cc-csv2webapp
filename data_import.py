import boto3
import pandas
import datetime


def rl_data(dynamodb):
    table = dynamodb.Table('Cupcakes')
    file_name = 'multiTimeline.csv'
    contents = pandas.read_csv(file_name)
    arr = contents["Cupcake"].to_list()
    name = contents["Month"].to_list()
    d = {}
    for i in range(len(name)):
        d['Id'] = int(i)+1
        d['Month'] = name[i]
        d['Cupcakes'] = int(arr[i])
        d['update_time'] = "-"
        table.put_item(Item=d)
    return True


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', 'ap-south-1')
    op = rl_data(dynamodb)

    if op:
        print("Data Saved in Dynamo DB")
    else:
        print("Error")