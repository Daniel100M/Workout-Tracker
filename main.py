import os
import requests
from datetime import datetime

APP_ID = os.environ['APP_ID']
API_KEY = os.environ['API_KEY']
SECRET_TOKEN = os.environ['SECRET']

WEIGHT = 60
HEIGHT = 170
AGE = 21


def parse_text():
    """
    Prompts user to specify workout.
    :return: Analysis of said workout.
    """
    # https://trackapi.nutritionix.com/v2/natural/exercise?x-app-id=&x-app-key=&query=
    url = 'https://trackapi.nutritionix.com/v2/natural/exercise'
    header = {
        'x-app-id': APP_ID,
        'x-app-key': API_KEY
    }
    parameters = {
        'query': input("Please specify your workout here: "),
        'weight_kg': WEIGHT,
        'height_cm': HEIGHT,
        'age': AGE
    }
    response = requests.post(url=url, headers=header, json=parameters)
    print(f"\nStatus code (Nutritionix): {response.status_code}")
    return response.json()


def add_workout() -> None:
    """
    Based on user input, adds another row to spreadsheet.
    :return:
    """
    url = os.environ['SHEET_ENDPOINT']
    analysis = parse_text()
    today = datetime.now()

    print(f"Analysis: {analysis}")

    header = {
        "Authorization": f'Bearer {SECRET_TOKEN}'
    }

    exercises = analysis['exercises']
    for exercise in exercises:
        entry = {
            "workout": {
                'date': today.strftime(format="%d/%m/%Y"),
                'time': today.strftime(format="%H:%M:%S"),
                'exercise': exercise['name'],
                'duration': exercise['duration_min'],
                'calories': exercise['nf_calories']
            }
        }
        # print(f"\nWorkout info: {entry['workout']}\n")

        response = requests.post(url=url, json=entry, headers=header)
        print(f"\nStatus code (Sheety): {response.status_code}")
        print(f"Message (Sheety):\n{response.text}")


add_workout()
