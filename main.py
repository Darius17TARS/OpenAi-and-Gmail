import os
import openai
import os.path
import sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
from lastEmail import myEmails





SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send' ]
openai.api_key = ""
openai.api_key = os.getenv("OPENAI_API_KEY")

content = myEmails()
addressee = content[0]
subject_content = content[1]

def getPrompt():
 global answer
 completion = openai.ChatCompletion.create(
   model="gpt-3.5-turbo",
    messages=[
     {"role": "user", "content": content[2].decode("utf-8")}
    ]
   )

 answer = completion.choices[0].message
 

    


def sendEmails(promptAnswer):
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
        message = EmailMessage()

        message.set_content(promptAnswer)

        message['To'] = addressee
        message['From'] = 'dariuspromter@gmail.com' #change to the auth2 project identificated email
        message['Subject'] = subject_content 

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
            .decode()

        create_message = {
            'raw': encoded_message
        }
        
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())
        print(send_message)
        print(F'Message Id: {send_message["id"]}')
  except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
  return send_message


def main():
  getPrompt()
  sendEmails(answer)




if __name__ == '__main__':
  exit (main())
    
