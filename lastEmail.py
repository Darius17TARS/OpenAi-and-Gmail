import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send' ]

# implement email ID detection to avoid replying to the same email twice // id

def myEmails():
  subjects = []
  senders = []
  ids =[]
  creds=None
  if os.path.exists('token.json'):
    creds= Credentials.from_authorized_user_file('token.json',SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh.token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json',SCOPES)
      creds = flow.run_local_server(port = 0)
    with open ('token.json', 'w') as token:
      token.write(creds.to_json())
  try:
    service = build('gmail','v1', credentials = creds) 
    result = service.users().messages().list(userId = 'me').execute()
    messages = result.get('messages')
    ids.append(messages[0]['id'])
    txt2 = service.users().messages().get(userId = 'me', id=messages[0]['id']).execute() #to get the most recent one
    for i in messages:
    
      
      
      txt = service.users().messages().get(userId = 'me', id=i['id']).execute() #to get all
      payload = txt['payload']
      headers = payload['headers']
      for i in headers:
          if i['name'] == 'Subject':
            subject = i['value']
            subjects.append(subject)
          if i['name'] == 'From':
            sender = i['value']
            senders.append(sender)
    
    try:
      if 'parts' in txt2['payload']: #checks if message is recieved or send
        dola = txt2['payload']['parts'][0]['body']['data'] 
        gola1 = dola.replace('-','+').replace('_','/')
        decodedata = base64.b64decode(gola1)
        
      else:
        dola = txt2['payload']['body']['data']
        gola1 = dola.replace('-','+').replace('_','/')
        decodedata = base64.b64decode(gola1)
        
    except HttpError as error:
      print(error)
    
    
    return senders[0], subjects[0], decodedata
  except HttpError as error:
    print(f'an error just occured:{error}')
    



myEmails()



