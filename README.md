Cupcake data from CSV is being sent to plot a graph in React---


1) createTable - > To Create a table in DynamoDb with INT as primary key to keep track of the Month.
2) data_import - > Imports the CSV data into Dynamo DB
3) update_table - > Updates the random 100 rows of the table every 100 mins
4) ddbstream2es - > It is written in Lambda function which triggers whenver there is an update happening and sends the data to Elastic Seacrh
5) es2api - > It is a lambda function having a trigger with the API gateway and the lambda is designed in such a way that it fetches all data from elastic search and loads only the columns or fields needed to plot the graph in the API endpoint
6) app.js -> React app's app.js file to get the data from API and to plot the graph of Month vs Cupcakes(Interest) using recharts.
7) Result_App.txt - > Contains the link of the hosted React_App ( hopefully safe )
