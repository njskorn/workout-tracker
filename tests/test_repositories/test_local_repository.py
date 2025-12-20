"""Tests for LocalWorkoutRepository"""
from repositories.local_workout_repository import LocalWorkoutRepository
from shared.schemas import WorkoutLog, Exercise, Set, EquipmentType
from datetime import date

import pytest
import shutil
from pathlib import Path

@pytest.fixture
def temp_repo():
    """Fixture to create and clean up a temporary LocalWorkoutRepository"""
    # Setup - create repo with unique temp directory
    temp_dir = Path("test_data_temp")
    repo = LocalWorkoutRepository(base_dir=str(temp_dir))
    # run the test
    yield repo
    # cleanup after test
    if temp_dir.exists():
        shutil.rmtree(temp_dir)

def test_repository_initialization(temp_repo):
    """Test initialization of LocalWorkoutRepository"""
    
    assert temp_repo.base_dir.name == "test_data_temp"
    assert temp_repo.workouts_dir.exists()

def test_save_and_retrieve_workout(temp_repo):
    """Test saving and retrieving a workout log"""

    # arrange
    workout = WorkoutLog(
        workout_date=date(2024, 12, 10),
        user_id="test_user",
        exercises=[
            Exercise(
                name="Bench Press",
                equipment=EquipmentType.BARBELL,
                sets=[Set(reps=10, weight_lbs=20)]
            )
        ]
    )
    
    # act
    file_path = temp_repo.save(workout)
    retrieved = temp_repo.get_by_date("test_user", date(2024, 12, 10))

    # assert
    assert file_path is not None
    assert retrieved is not None
    assert retrieved.user_id == "test_user"
    assert retrieved.workout_date == date(2024, 12, 10)
    assert len(retrieved.exercises) == 1
    assert retrieved.exercises[0].name == "Bench Press"
    assert retrieved.total_volume == 200  # 10 reps * 20 lbs

def test_delete_workout(temp_repo):
    """Test deleting a workout."""
    # arrange
    workout = WorkoutLog(
        workout_date=date(2024, 12, 11),
        user_id="test_user",
        exercises=[
            Exercise(
                name="Squat",
                equipment=EquipmentType.BARBELL,
                sets=[Set(reps=5, weight_lbs=185)]
            )
        ]
    )
    
    # act
    temp_repo.save(workout)
    deleted = temp_repo.delete("test_user", date(2024, 12, 11))
    retrieved = temp_repo.get_by_date("test_user", date(2024, 12, 11))
    
    # assert
    assert deleted is True
    assert retrieved is None  # Should be gone!


def test_delete_nonexistent_workout(temp_repo):
    """Test deleting a workout that doesn't exist."""
    # arrange in temp_repo
 
    # act
    deleted = temp_repo.delete("test_user", date(2099, 1, 1))
    
    # assert
    assert deleted is False  # Didn't exist, so returns False

def test_list_dates(temp_repo):
    """Test listing all workout dates for a user."""
    # Arrange in temp_repo
    
    # Create 3 workouts on different dates
    for day in [15, 16, 17]:
        workout = WorkoutLog(
            workout_date=date(2024, 12, day),
            user_id="test_user",
            exercises=[
                Exercise(
                    name="Test",
                    equipment=EquipmentType.DUMBBELL,
                    sets=[Set(reps=10, weight_lbs=10)]
                )
            ]
        )
        temp_repo.save(workout)
    
    # Act
    dates = temp_repo.list_dates("test_user")
    
    # Assert
    assert len(dates) >= 3  # At least the 3 we just created
    assert date(2024, 12, 15) in dates
    assert date(2024, 12, 16) in dates
    assert date(2024, 12, 17) in dates

def test_get_date_range(temp_repo):
    """Test retrieving workouts in a date range."""
    # Arrange in temp_repo
    
    # Create workouts on different dates
    for day in [20, 21, 22]:
        workout = WorkoutLog(
            workout_date=date(2024, 12, day),
            user_id="test_user",
            exercises=[
                Exercise(
                    name=f"Day {day} Exercise",
                    equipment=EquipmentType.BARBELL,
                    sets=[Set(reps=8, weight_lbs=100)]
                )
            ]
        )
        temp_repo.save(workout)
    
    # Act
    workouts = temp_repo.get_date_range(
        "test_user",
        start_date=date(2024, 12, 21),
        end_date=date(2024, 12, 22)
    )
    
    # Assert
    assert len(workouts) == 2
    assert workouts[0].workout_date == date(2024, 12, 21)
    assert workouts[1].workout_date == date(2024, 12, 22)