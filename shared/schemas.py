# pydantic models for workout tracking application
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class Exercise(BaseModel):
    """Single exercise with sets, reps, and weight"""
    name: str = Field(..., description="Exercise name, e.g., 'Bench Press'")
    sets: int = Field(gt=0, description="Number of sets")
    reps: int = Field(gt=0, description="Number of reps per set")
    weight_lbs: float = Field(ge=0, description="Weight in pounds")

    @property
    def total_volume(self) -> float:
        """Calculate total volume lifted for this exercise"""
        return self.sets * self.reps * self.weight_lbs

class WorkoutLog(BaseModel):
    """Complete workout log for a single day"""
    workout_date: date = Field(..., description="Date of workout")
    user_id: str = Field(..., description="User identifier")
    exercises: list[Exercise] = Field(..., description="List of exercises performed")
    notes: Optional[str] = Field(None, description="Optional workout notes")

    @property
    def total_volume(self) -> float:
        """Sum of ALL exercises in this workout"""
        return sum(ex.total_volume for ex in self.exercises)
    
    @property
    def exercise_count(self) -> int:
        """How many exercises in this workout"""
        return len(self.exercises)


    class Config:
        json_schema_extra = {
            "example": {
                "workout_date": "2024-06-15",
                "user_id": "nettle",
                "exercises": [
                    {
                        "name": "Bench Press",
                        "sets": 4,
                        "reps": 10,
                        "weight_lbs": 150.0
                    },
                    {
                        "name": "Squats",
                        "sets": 3,
                        "reps": 12,
                        "weight_lbs": 200.0
                    }
                ],
                "notes": "Felt strong today, increased weight on squats."
            }
        }