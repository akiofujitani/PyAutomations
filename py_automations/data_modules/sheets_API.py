from shutil import ExecError
import google.auth, os, logging
from . import json_config, log_builder
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

logger = logging.getLogger('sheets_API')


def load_creds() -> google.oauth2.credentials.Credentials:
    # If modifying these scopes, delete the file token.json.

    config_json = {}
    config_json.update(json_config.load_json_config('sheets_config.json'))

    SCOPES = config_json['SCOPE']

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):        
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.   
    if not creds or not creds.valid:
        try:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
        except Exception as error:
            logger.debug(error)
            creds = create_token('client_key.json', SCOPES)
    logger.debug(type(creds))
    return creds


def create_token(client_key: str, SCOPES: list):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_key, SCOPES)
    creds = flow.run_local_server(port=0)
    if os.path.exists('token.json'):
        os.remove('token.json')
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    return creds

def get_values(creds, spreadsheet_id, range_name) -> dict:
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """
    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    
    try:
        service = build('sheets', 'v4', credentials=creds)

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        logger.info(f"{len(rows)} rows retrieved")
        return result
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error


def batch_get_values(creds, spreadsheet_id, range_names):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
        """
    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)
        range_names = [
            # Range names ...
        ]
        result = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id, ranges=range_names).execute()
        ranges = result.get('valueRanges', [])
        logger.info(f"{len(ranges)} ranges retrieved")
        return result
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error


def update_values(creds, spreadsheet_id, range_name, value_input_option, values):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
        """
    # pylint: disable=maybe-no-member
    try:

        service = build('sheets', 'v4', credentials=creds)
        # values = [
        #     [
        #         # Cell values ...
        #     ],
        #     # Additional rows ...
        # ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        logger.info(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error


def add_sheet(creds, spreadsheet_id, sheet_name):
    try:
        service = build('sheets', 'v4', credentials=creds)

        request_body = {
            'requests' : [{
                'addSheet' : {
                    'properties' : {
                        'title' : sheet_name,
                    }
                }
            }]
        }
        result = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=request_body).execute()
        logger.info(result)
        return result
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error

def batch_update_values(spreadsheet_id, range_name,
                        value_input_option, values):
    """
        Creates the batch_update the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.\n"
            """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        values = [
            [
                # Cell values ...
            ],
            # Additional rows
        ]
        data = [
            {
                'range': range_name,
                'values': values
            },
            # Additional ranges to update ...
        ]
        body = {
            'valueInputOption': value_input_option,
            'data': data
        }
        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        logger.info(f"{(result.get('totalUpdatedCells'))} cells updated.")
        return result
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error


def append_values(creds, spreadsheet_id, range_name, value_input_option, values):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
        """
    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        # values = [
        #     [
        #         # Cell values ...
        #     ],
        #     # Additional rows ...
        # ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        logger.info(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error


def create(creds, title):
    """
    Creates the Sheet the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
        """
    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId') \
            .execute()
        logger.info(f"Spreadsheet ID: {(spreadsheet.get('spreadsheetId'))}")
        return spreadsheet.get('spreadsheetId')
    except HttpError as error:
        logger.error(f"An error occurred: {error}")
        raise error


if __name__ == '__main__':
    logger = logging.getLogger()
    log_builder.logger_setup(logger)

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '1kpZuId58YFUqHqNPftbkRYbz0AW39F5IDjNHuNFgcC8'
    RANGE_NAME = 'DOCUMENTOS!'
    RANGE = 'B:C'

    creds = load_creds()
    cell_values = get_values(creds, SPREADSHEET_ID, f'{RANGE_NAME}{RANGE}')
    logger.debug(cell_values)