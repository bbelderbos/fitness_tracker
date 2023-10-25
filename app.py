import streamlit as st

from data import WorkoutTracker

tracker = WorkoutTracker()

st.title("Update Workout")

# Dropdown to select exercise
exercise_name = st.selectbox("Select an Exercise", tracker.get_exercises())

# Input field for the exercise value
exercise_value = st.text_input("Enter the exercise value (e.g., 50x12 60x10):")

# Button to trigger update
if st.button("Update Exercise"):
    if exercise_name is None:
        st.warning("Please select an exercise!")
    elif not exercise_value:
        st.warning("Please input a value for the exercise!")
    else:
        tracker.update_workout_exercise(exercise_name, exercise_value)
        st.success(f"Updated {exercise_name} with value: {exercise_value}")
