from googleapiclient.discovery import build

api_key = "AIzaSyBxeDNmY58khMIkFyV0uDStwXpkW3U1JPU"
youtube = build('youtube', 'v3', developerKey=api_key)
req = youtube.search().list(q='nba highlight', part='snippet', type='video')
print(type(req))
print(type(youtube))
print(req.execute())