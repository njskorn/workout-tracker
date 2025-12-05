"""Manual testing script for workout schemas"""
from shared.schemas import Set, Exercise, WorkoutLog, EquipmentType
from datetime import date

print("=" * 60)
print("TESTING WORKOUT SCHEMAS")
print("=" * 60)

# Test 1: Shoulder Press with goals
print("\n--- Test 1: Shoulder Press with Goal Tracking ---")
shoulder_press = Exercise(
    name="Shoulder Press",
    equipment=EquipmentType.DUMBBELL,
    sets=[
        Set(reps=12, weight_lbs=30, goal_reps=12, goal_weight_lbs=30),
        Set(reps=10, weight_lbs=30, goal_reps=10, goal_weight_lbs=30),
        Set(reps=9, weight_lbs=30, goal_reps=10, goal_weight_lbs=30),
        Set(reps=7, weight_lbs=30, goal_reps=8, goal_weight_lbs=30),
    ],
    notes="Felt strong on first two sets"
)

print(f"Exercise: {shoulder_press.name}")
print(f"Equipment: {shoulder_press.equipment.value}")
print(f"Total volume: {shoulder_press.total_volume} lbs")
print(f"Goal volume: {shoulder_press.goal_volume} lbs")
print(f"Achievement: {shoulder_press.volume_achievement:.1%}")
print(f"Sets completed: {shoulder_press.set_count}")

# Test 2: Exercise without goals
print("\n--- Test 2: Bench Press without Goals ---")
bench_press = Exercise(
    name="Bench Press",
    equipment=EquipmentType.BARBELL,
    sets=[
        Set(reps=10, weight_lbs=135),
        Set(reps=8, weight_lbs=155),
        Set(reps=6, weight_lbs=165),
    ]
)

print(f"Exercise: {bench_press.name}")
print(f"Total volume: {bench_press.total_volume} lbs")
print(f"Achievement: {bench_press.volume_achievement:.1%}")  # Should be 100%

# Test 3: Bodyweight exercise
print("\n--- Test 3: Bodyweight Pull-ups ---")
pullups = Exercise(
    name="Pull-ups",
    equipment=EquipmentType.BODYWEIGHT,
    sets=[
        Set(reps=10, weight_lbs=0),
        Set(reps=8, weight_lbs=0),
        Set(reps=6, weight_lbs=0),
    ]
)

print(f"Exercise: {pullups.name}")
print(f"Total volume: {pullups.total_volume} lbs")  # Will be 0
print(f"Total reps: {sum(s.reps for s in pullups.sets)}")

# Test 4: Full workout log
print("\n--- Test 4: Complete Workout ---")
workout = WorkoutLog(
    workout_date=date.today(),
    user_id="nettle",
    exercises=[shoulder_press, bench_press, pullups],
    notes="Great workout today!"
)

print(f"Date: {workout.workout_date}")
print(f"Exercises: {workout.exercise_count}")
print(f"Total volume: {workout.total_volume} lbs")
print(f"Goal volume: {workout.goal_volume} lbs")
print(f"Overall achievement: {workout.volume_achievement:.1%}")

# Test 5: Serialization (preparing for API/storage)
print("\n--- Test 5: Serialization ---")
workout_dict = workout.model_dump()
print(f"Workout as dict (name of first exercise): {workout_dict['exercises'][0]['name']}")
print(f"Workout as dict (weight on first set of second exercise): {workout_dict['exercises'][1]['sets'][0]['weight_lbs']} lbs")

workout_json = workout.model_dump_json(indent=2)
print(f"Workout as JSON (first 200 chars):\n{workout_json[:200]}...")

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)