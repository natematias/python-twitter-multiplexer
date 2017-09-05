from app.connections.twitter_connect import *
import http.client as http_client
#http_client.HTTPConnection.debuglevel = 1

connection = TwitterConnect()
print("Twitter API details:")
print(connection.api.__dict__)
print()
print("NOW QUERY GETFRIENDS")

for i in list(range(0,10)):
    y = connection.query(connection.api.GetFriends)
    print("Called GetFriends. API Consumer Key {0} status: {1}".format(connection.api._consumer_key, connection.api.rate_limit.resources['friends']['/friends/list']))
    print()
