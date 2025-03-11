from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request  # Import Request for refreshing tokens
import datetime
import os.path
import pytz  # Import pytz for timezone handling

# Define the scope of permissions you need for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']
MEAL_PLANNER = "e40dcfc550ffce33e40c2b0ad7a2baa20b108fe1870b59ba11761ba59a7074a4@group.calendar.google.com"
# GROCERY_LIST = 
# MEAL_PLAN = 


def create_shopping():
    # Load credentials from a token file if available, otherwise authenticate and save them

    next_sunday_10am = get_next_sunday_10am() #get next sunday at 10am using default timezone of America/Denver
    end_time = next_sunday_10am + datetime.timedelta(hours=1) # One hour event.

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
        'summary': 'Shopping ',
        'location': 'Dimscord',
        'description': 'Watch thing with han',
        'start': {
            'dateTime': next_sunday_10am.isoformat(), # use now instead of utcnow and use timezone
            'timeZone': 'America/Denver',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Denver',
        },
    }

    try:
        # Insert the event into your Google Calendar
        event = service.events().insert(calendarId=MEAL_PLANNER, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except Exception as error:
        print(f"An error occurred: {error}")


def get_next_sunday_10am(timezone_str='America/Denver'):
    """Calculates the datetime for the next coming Sunday at 10 AM in the specified timezone."""
    now = datetime.datetime.now(pytz.timezone(timezone_str))
    days_until_sunday = (6 - now.weekday()) % 7  # 6 represents Sunday
    next_sunday = now + datetime.timedelta(days=days_until_sunday)
    next_sunday_10am = next_sunday.replace(hour=10, minute=0, second=0, microsecond=0)
    return next_sunday_10am

if __name__ == '__main__':
    create_shopping()