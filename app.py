import streamlit as st

from data import update_workout_exercise, get_exercises

st.title("Update Workout")

# Dropdown to select exercise
exercise_name = st.selectbox("Select an Exercise", get_exercises())

# Input field for the exercise value
exercise_value = st.text_input("Enter the exercise value (e.g., 50x12 60x10):")

# Button to trigger update
if st.button("Update Exercise"):
    if not exercise_value:
        st.warning("Please input a value for the exercise!")
    else:
        update_workout_exercise(exercise_name, exercise_value)
        st.success(f"Updated {exercise_name} with value: {exercise_value}")

