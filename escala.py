
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId='1aF9B_zZCk3xU3OWtW3FdJvUtb47qWcTnse9d6n-sifw',
                                    range='Página1!A1:B13').execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()



# import gspread

# # Obter o ID da planilha
# spreadsheet_id = "1aF9B_zZCk3xU3OWtW3FdJvUtb47qWcTnse9d6n-sifw"

# # Autenticar com o Google Sheets API
# gc = gspread.service_account(filename='C:\\Users\\TCO\\Documents\\GitHub\\projeto-cia\\client_secret.json')


# # Abrir a planilha
# sh = gc.open_by_key(spreadsheet_id)

# # Selecionar a planilha desejada
# worksheet = sh.worksheet("Página1")

# # Obter os valores da célula A1 até B13
# values = worksheet.get("A1:B13")

# # Imprimir os valores
# for row in values:
#     print(row)

