import datetime
import json
import os

import gspread


GOOGLE_SERVICE_ACCOUNT_JSON = os.environ['GOOGLE_SERVICE_ACCOUNT_JSON']
creds_dict = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
gc = gspread.service_account_from_dict(creds_dict)

sheet = gc.open("bob-workouts").sheet1


def get_exercises():
    return sheet.col_values(2)[1:]


def _get_monday_of_week():
    today = datetime.date.today()
    days_since_monday = today.weekday()
    last_monday = today - datetime.timedelta(days=days_since_monday)
    date_str = last_monday.strftime("%d/%m/%Y")
    return date_str


def get_column_to_update():
    date_str = _get_monday_of_week()
    row = sheet.row_values(1)
    if date_str not in row:
        raise Exception("Date not found in row")
    return row.index(date_str) + 1


def _get_exercise_row_number(exercise_name):
    exercises = get_exercises()
    if exercise_name not in exercises:
        # TODO: can use own named exception
        raise Exception("Exercise not found")
    return exercises.index(exercise_name) + 2  # +1 for header row, +1 for 0 index


def update_workout_exercise(exercise_name, exercise_value):
    try:
        row = _get_exercise_row_number(exercise_name)
    except Exception:
        # TODO: return early ok here?
        return
    col = get_column_to_update()
    sheet.update_cell(row, col, exercise_value)


if __name__ == "__main__":
    update_workout_exercise("bicep curl", "20x20x20x20")
