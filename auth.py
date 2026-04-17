from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ['https://www.googleapis.com/auth/blogger']

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json', SCOPES
)

creds = flow.run_local_server(port=8080)

with open('token.pkl', 'wb') as token:
    pickle.dump(creds, token)

print("Auth complete")
