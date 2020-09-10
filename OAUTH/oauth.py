import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# Google's Request
from google.auth.transport.requests import Request


credentials = None

if os.path.exists("token.pickle"):
    print ("Loading Credentials from file")
    with open("token.pickle","rb") as token:
        credentials = pickle.load(token)

# If there are no valid credentials available, then either refresh the token or log in.
if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print('Refreshing Access Token...')
        credentials.refresh(Request())
    else:
        print('Fetching New Tokens...')
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secrets.json',
            scopes=[
                'https://www.googleapis.com/auth/youtube.readonly'
            ]
        )

        flow.run_local_server(port=8080, prompt='consent',
                              authorization_prompt_message='')
        credentials = flow.credentials

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as f:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, f)


youtube = build("youtube", "v3", credentials=credentials)
request  = youtube.playListItems().list(part="status", playlistId="")

response = request.execute()

for item in response["items"]:
    vid_id = item["contentDetails"]["videoId"]
    yt_link = f"https://youtu.be/{vid_id}"
    print(yt_link)
