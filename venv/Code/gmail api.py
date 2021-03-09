from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "G:\My Drive\Affiliate Marketing\Credentials\Google APIs\Gmail API\credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('gmail', 'v1', credentials=creds)

# Call the Gmail API
results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])

# if not labels:
#     print('No labels found.')
# else:
#     print('Labels:')def get_messages(service, user_id, label):
#   try:
#     return service.users().messages().list(userId=user_id, labelIds=label).execute()
#   except Exception as error:
#     print('An error occurred: %s' % error)
#


labels_dict = {
    'Afiliação Aceita':  'Label_2111935885913310825',
    'Afiliação Cancelada': 'Label_4351429095228833942',
    'Boleto Gerado': 'Label_3867085259550657269',
    'Comissão Alterada': 'Label_122274569783060860',
    'Produto Removido': 'Label_681057746109258041',
    'Venda Realizada': 'Label_1820613913418598401'

}



def get_messages(service, user_id, label):
    import pandas as pd

    try:
        list_messages =  service.users().messages().list(userId=user_id, labelIds=label).execute()['messages']
    except Exception as error:
        print('An error occurred: %s' % error)


    df = pd.DataFrame(columns=['subject', 'time', 'id'])
    for message_item in list_messages:
        message = service.users().messages().get(userId=user_id, id=message_item['id']).execute()
        message_name = message['payload']['headers'][15]['value']
        message_id = message_item['id']
        message_arrived = message['payload']['headers'][14]['value']
        dict_append = {'subject':message_name, 'time':message_arrived, 'id':message_id}
        df = df.append(dict_append, ignore_index=True)

    return df


df = get_messages(service, 'daedalus.tecnologia@gmail.com', labels_dict['Afiliação Aceita'])

def get_name(row):
    subject = row['subject']
    course_name = subject[18:]
    row['course_name'] = course_name
    return row['course_name']


df['course_name'] = df.apply(lambda row: get_name(row), axis=1)


import datetime as dt
data = dt.datetime.now().date()

df.to_excel(f"G:\\My Drive\\Affiliate Marketing\\gmail accepted\\gmail_asof_{dt.date.strftime(data, '%Y%m%d')}.xlsx")