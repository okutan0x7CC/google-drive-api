# $ python -V
#   Python 3.9.2
# $ pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive で参照する親ディレクトリID
GDRIVE_PARENT_DIR_ID=['']

# 参照： https://developers.google.com/drive/api/v3/about-auth
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# ~/.zshrc に定義している gcp API の認証ファイル
# 作成方法： https://developers.google.com/workspace/guides/create-credentials
CREDENTIALS_PATH = os.environ['GOOGLE_APPLICATION_CREDENTIALS']

def create(service, filePath):
    body = {
        'name': filePath,
        'parents': GDRIVE_PARENT_DIR_ID,
    }
    fileName = filePath
    media = MediaFileUpload(fileName, mimetype='text/plain', resumable=True)
    service.files().create(body=body, media_body=media).execute()


def main():

    # gcp API の認証
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    create(service, './.gcp/gcp.py')

if __name__ == "__main__":
    main()