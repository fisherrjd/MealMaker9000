from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request  # Import Request for refreshing tokens
import datetime
import os.path

# Define the scope of permissions you need for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

# GROCERY_LIST = 
# MEAL_PLAN = 


def main():
    # Load credentials from a token file if available, otherwise authenticate and save them
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Use Request() to refresh the token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Google Calendar API service
    service = build('calendar', 'v3', credentials=creds)

    # Define a new event
    event = {
        'summary': 'Movie Time',
        'location': 'Dimscord',
        'description': 'Watch thing with han',
        'start': {
            'dateTime': datetime.datetime.now().isoformat(), # use now instead of utcnow and use timezone
            'timeZone': 'America/Denver',
        },
        'end': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'America/Denver',
        },
    }

    try:
        # Insert the event into your Google Calendar
        event = service.events().insert(calendarId='primary', body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except Exception as error:
        print(f"An error occurred: {error}")

if __name__ == '__main__':
    main()