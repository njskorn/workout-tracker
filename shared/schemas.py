# pydantic models for workout tracking application
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from enum import Enum

class EquipmentType(str, Enum):
    """Type of equipment used for exercise"""
    BARBELL = "barbell"           # Weight is total (bar + plates)
    DUMBBELL = "dumbbell"         # Weight is per hand
    KETTLEBELL = "kettlebell"     # Weight is per hand
    MACHINE = "machine"           # Weight on machine
    BODYWEIGHT = "bodyweight"     # No external weight (weight_lbs=0)
    CABLE = "cable"               # Cable machine
    BAND = "band"                 # Resistance band

class Set(BaseModel):
    """Single set of an exercise with optional goal tracking"""
    reps: int = Field(gt=0, description="Reps actually performed")
    weight_lbs: float = Field(ge=0, description="Weight used (per hand for dumbbells/kettlebells)")
    goal_reps: int | None = Field(None, gt=0, description="Planned reps")
    goal_weight_lbs: float | None = Field(None, ge=0, description="Planned weight")
    
    @property
    def volume(self) -> float:
        """Volume for this set: reps × weight"""
        return self.reps * self.weight_lbs
    
    @property
    def goal_volume(self) -> float:
        """Planned volume, falling back to actual if no goal set"""
        goal_r = self.goal_reps or self.reps
        goal_w = self.goal_weight_lbs or self.weight_lbs
        return goal_r * goal_w

class Exercise(BaseModel):
    """Exercise with multiple sets, allowing variable reps/weight per set"""
    name: str = Field(min_length=1, max_length=100, description="Exercise name, e.g., 'Bench Press'")
    sets: list[Set] = Field(min_length=1, description="Sets performed")
    equipment: EquipmentType = Field(description="Equipment type")
    notes: str | None = Field(None, max_length=500, description="Exercise-specific notes")
    
    @property
    def total_volume(self) -> float:
        """Total volume: sum of all set volumes"""
        return sum(s.volume for s in self.sets)
    
    @property
    def goal_volume(self) -> float:
        """Planned volume: sum of all goal volumes"""
        return sum(s.goal_volume for s in self.sets)
    
    @property
    def volume_achievement(self) -> float:
        """Achievement ratio (1.0 = 100% of goal achieved)"""
        if self.goal_volume == 0:
            return 1.0
        return self.total_volume / self.goal_volume
    
    @property
    def set_count(self) -> int:
        """Number of sets performed"""
        return len(self.sets)

class WorkoutLog(BaseModel):
    """Complete workout log for a single day"""
    workout_date: date = Field(description="Date of workout")
    user_id: str = Field(min_length=1, description="User identifier")
    exercises: list[Exercise] = Field(min_length=1, description="Exercises performed")
    notes: str | None = Field(None, max_length=1000, description="Workout notes")

    @property
    def total_volume(self) -> float:
        """Sum of all exercise volumes"""
        return sum(ex.total_volume for ex in self.exercises)

    @property
    def goal_volume(self) -> float:
        """Sum of all exercise goal volumes"""
        return sum(ex.goal_volume for ex in self.exercises)

    @property
    def volume_achievement(self) -> float:
        """Overall achievement ratio (1.0 = 100% of goal achieved)"""
        if self.goal_volume == 0:
            return 1.0
        return (self.total_volume / self.goal_volume)
    
    @property
    def exercise_count(self) -> int:
        """How many exercises in this workout"""
        return len(self.exercises)



    model_config = {
        "json_schema_extra": {
            "example": {
                "workout_date": "2024-12-05",
                "user_id": "nettle",
                "exercises": [
                    {
                        "name": "Shoulder Press",
                        "equipment": "dumbbell",
                        "sets": [
                            {"reps": 12, "weight_lbs": 30.0, "goal_reps": 12, "goal_weight_lbs": 30.0},
                            {"reps": 10, "weight_lbs": 30.0, "goal_reps": 10, "goal_weight_lbs": 30.0},
                            {"reps": 9, "weight_lbs": 30.0, "goal_reps": 10, "goal_weight_lbs": 30.0},
                            {"reps": 7, "weight_lbs": 30.0, "goal_reps": 8, "goal_weight_lbs": 30.0}
                        ],
                        "notes": "Felt strong on first two sets"
                    }
                ],
                "notes": "Good shoulder workout!"
            }
        }
    }