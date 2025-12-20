"""Local filesystem implementation of WorkoutRepository"""
from pathlib import Path
from datetime import date
from typing import List, Optional
import json

from shared.schemas import WorkoutLog
from repositories.workout_repository import WorkoutRepository

class LocalWorkoutRepository(WorkoutRepository):
    """
    Stores workouts as JSON files on local filesystem.
    
    Directory structure:
        base_dir/
        └── workouts/
            └── {user_id}/
                └── {year}/
                    └── {month}/
                        └── {day}.json
    
    Example: local_storage/workouts/nettle/2024/12/05.json
    """
    
    def __init__(self, base_dir: str = "local_storage"):
        """
        Initialize repository.
        
        Args:
            base_dir: Base directory for storing workout files
        """
        self.base_dir = Path(base_dir)
        self.workouts_dir = self.base_dir / "workouts"
        # Create base directory if it doesn't exist
        self.workouts_dir.mkdir(parents=True, exist_ok=True)

    def _get_workout_path(self, user_id: str, workout_date: date) -> Path:
        """Construct the file path for a given user's workout on a specific date"""
        return (self.workouts_dir / user_id / 
                str(workout_date.year) / 
                f"{workout_date.month:02d}" / 
                f"{workout_date.day:02d}.json")

    def save(self, workout: WorkoutLog) -> str:
        """Save a workout to local filesystem."""
        file_path = self._get_workout_path(workout.user_id, workout.workout_date)
        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # Serialize workout to JSON
        workout_json = workout.model_dump_json(indent=2)
        # Write to file
        file_path.write_text(workout_json)
        return str(file_path)

    def get_by_date(self, user_id: str, workout_date: date) -> Optional[WorkoutLog]:
        """Retrieve a workout for a specific user and date."""
        file_path = self._get_workout_path(user_id, workout_date)
        if not file_path.exists():
            return None

        # Read JSON file
        workout_json = file_path.read_text()
        # Deserialize to WorkoutLog
        workout = WorkoutLog.model_validate_json(workout_json)
        return workout

    def get_date_range(self, user_id: str, start_date: date, end_date: date) -> List[WorkoutLog]:
        """Retrieve all workouts for a user in a date range."""
        workouts = []
        
        # Get all workout dates for user
        all_dates = self.list_dates(user_id)

        for workout_date in all_dates:
            if start_date <= workout_date <= end_date:
                workout = self.get_by_date(user_id, workout_date)
                if workout:
                    workouts.append(workout)
        
        # Sort workouts by date
        workouts.sort(key=lambda w: w.workout_date)
        return workouts

    def delete(self, user_id: str, workout_date: date) -> bool:
        """Delete a workout for a specific user and date."""
        file_path = self._get_workout_path(user_id, workout_date)
        
        if not file_path.exists():
            return False
        
        file_path.unlink()  # Delete the file
        return True

    def list_dates(self, user_id: str) -> List[date]:
        """Get all dates that have workouts for a user."""
        # get user directory
        user_dir = self.workouts_dir / user_id
        
        if not user_dir.exists():
            return []
        
        dates = []

        for year_dir in user_dir.iterdir():
            if not year_dir.is_dir():
                continue
            
            for month_dir in year_dir.iterdir():
                if not month_dir.is_dir():
                    continue
                
                for day_file in month_dir.glob("*.json"):
                    # Parse date from directory structure
                    year = int(year_dir.name)
                    month = int(month_dir.name)
                    day = int(day_file.stem)  # filename without .json
                    
                    dates.append(date(year, month, day))
        
        # Sort dates chronologically
        dates.sort()
        return dates