"""FastAPI application for workout training"""

import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.schemas import WorkoutLog
from repositories.local_workout_repository import LocalWorkoutRepository

# Create repository instance
repo = LocalWorkoutRepository(base_dir="local_storage")


app = FastAPI(
    title="Workout Training API",
    description="API for logging and analyzing workout training sessions",
    version="0.1.0"
)

# Enable CORS for all origins (for development purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # ok for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    """Health check for endpoint"""
    return {
        "message": "Workout Training API is running",
        "version": "0.1.0"
    }

@app.post("/workouts")
def create_workout(workout: WorkoutLog):
    """Endpoint to log a new workout session"""

    file_path = repo.save(workout)
    
    return {
        "message": "Workout logged successfully",
        "file_path": file_path,
        "workout_date": workout.workout_date,
        "exercises": len(workout.exercises),
        "total_volume": workout.total_volume
    }

@app.get("/workouts/{user_id}/{workout_date}")
def get_workout(user_id: str, workout_date: str):
    """Retriieve a workout by user ID and date (YYYY-MM-DD)"""
    from datetime import datetime

    # parse date string to date object
    date_obj = datetime.strptime(workout_date, "%Y-%m-%d").date()

    # get workout from repository
    workout = repo.get_by_date(user_id, date_obj)
    
    if not workout:
        return {
            "message": "No workout found for the given user and date"
        }
    
    return workout

@app.get("/exercises")
def get_exercises(
    equipment: str | None = None,
    primary_muscle: str | None = None,
    level: str | None = None
):
    """Retrieve list of supported exercises
    Query Parameters:
        equipment: Filter by equipment (e.g., 'barbell', 'dumbbell')
        primary_muscle: Filter by muscle (e.g., 'chest', 'biceps')
        level: Filter by difficulty (e.g., 'beginner', 'intermediate')"""
    
    exercises_file = Path("shared/data/exercises.json")
    
    # load JSON
    with open(exercises_file, "r") as f:
        exercises_data = json.load(f)

    if equipment:
        exercises_data = [ex for ex in exercises_data if ex.get('equipment') == equipment]
    if primary_muscle:
        exercises_data = [ex for ex in exercises_data if primary_muscle in ex.get('primaryMuscles', [])]
    if level:
        exercises_data = [ex for ex in exercises_data if ex.get('level') == level]
    
    return exercises_data