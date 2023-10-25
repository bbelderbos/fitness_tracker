import datetime
import json
import os

import gspread

GOOGLE_SERVICE_ACCOUNT_JSON = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]


class ExerciseNotFoundError(Exception):
    """Raised when the specified exercise is not found in the sheet."""


class DateNotFoundError(Exception):
    """Raised when the specified date is not found in the sheet."""


class WorkoutTracker:
    def __init__(self, sheet_name: str = "bob-workouts") -> None:
        creds_dict = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
        gc = gspread.service_account_from_dict(creds_dict)
        self.sheet = gc.open(sheet_name).sheet1

    def get_exercises(self) -> list[str]:
        return self.sheet.col_values(2)[1:]

    def _get_monday_of_week(self) -> str:
        today = datetime.date.today()
        days_since_monday = today.weekday()
        last_monday = today - datetime.timedelta(days=days_since_monday)
        return last_monday.strftime("%d/%m/%Y")

    def get_column_to_update(self) -> int:
        date_str = self._get_monday_of_week()
        row = self.sheet.row_values(1)
        if date_str not in row:
            raise DateNotFoundError(f"Date {date_str} not found in row")
        return row.index(date_str) + 1

    def _get_exercise_row_number(self, exercise_name: str) -> int:
        exercises = self.get_exercises()
        if exercise_name not in exercises:
            raise ExerciseNotFoundError(f"Exercise {exercise_name} not found")
        return exercises.index(exercise_name) + 2  # +1 for header row, +1 for 0 index

    def update_workout_exercise(self, exercise_name: str, exercise_value: str) -> None:
        # we assume unique exercises for now
        try:
            row = self._get_exercise_row_number(exercise_name)
        except ExerciseNotFoundError:
            return None
        col = self.get_column_to_update()
        self.sheet.update_cell(row, col, exercise_value)
        return None


if __name__ == "__main__":
    tracker = WorkoutTracker()
    tracker.update_workout_exercise("bicep curl", "20x20x20x20")
