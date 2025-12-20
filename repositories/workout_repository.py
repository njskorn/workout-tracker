"""Repository interface for workout storage"""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from shared.schemas import WorkoutLog

class WorkoutRepository(ABC):
    """Abstract base class for workout data storage

    Implementations can store data:
    - locally (LocalWorkoutRepository)
    - S3 (S3WorkoutRepository)
    - PostgresSQL (PostgresWorkoutRepository)

    The rest of the application should not need 
    to know where data is stored. It just calls 
    these methods.
    """

    @abstractmethod
    def save(self, workout: WorkoutLog) -> str:
        """Save a workout log to the repository
        
        Args:
            workout (WorkoutLog): The workout log to save
            
        Returns:
            str: The unique identifier of the saved workout
        """
        pass

    @abstractmethod
    def get_by_date(self, user_id: str, workout_date: date) -> Optional[WorkoutLog]:
        """Retrieve a workout log for a specific user and date
        
        Args:
            user_id: The ID of the user
            workout_date: The date of the workout
            
        Returns:
            Optional[WorkoutLog]: The retrieved workout log, or None if not found
        """
        pass

    @abstractmethod
    def get_date_range(
        self, 
        user_id: str, 
        start_date: date, 
        end_date: date
    ) -> List[WorkoutLog]:
        """Retrieve workout logs for a specific user within a date range
        
        Args:
            user_id: The ID of the user
            start_date: The start date of the range (inclusive)
            end_date: The end date of the range (inclusive)

        Returns:
            List[WorkoutLog]: The retrieved workout logs, sorted by date, 
            or an empty list if none found
        """
        pass

    @abstractmethod
    def delete(self, user_id: str, workout_date: date) -> bool:
        """
        Delete a workout for a specific user and date.
        
        Args:
            user_id: User identifier
            workout_date: Date of workout to delete
            
        Returns:
            True if deleted, False if workout didn't exist
        """
        pass

    @abstractmethod
    def list_dates(self, user_id: str) -> List[date]:
        """
        Get all dates that have workouts for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            List of dates with workouts, sorted chronologically
        """
        pass