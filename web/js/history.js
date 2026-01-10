// Load and display workout history

// When page loads, fetch all workouts
document.addEventListener('DOMContentLoaded', async function() {
    await loadWorkouts();
});

// Listen for user filter changes
document.getElementById('userFilter').addEventListener('change', async function() {
    await loadWorkouts();
});

async function loadWorkouts() {
    // Get selected user filter
    const userFilter = document.getElementById('userFilter').value;
    
    // Show loading state
    const workoutList = document.getElementById('workoutList');
    workoutList.innerHTML = '<p>Loading workouts...</p>';
    
    try {
        // Build URL with optional user filter
        let url = 'http://localhost:8000/workouts';
        if (userFilter) {
            url += `?user_id=${userFilter}`;
        }
        
        // Fetch workouts
        const response = await fetch(url);
        const workouts = await response.json();
        
        // Check if any workouts found
        if (workouts.length === 0) {
            workoutList.innerHTML = '<p>No workouts found. Start logging!</p>';
            return;
        }
        
        // Display workouts
        workoutList.innerHTML = workouts.map(workout => `
            <div class="workout-card">
                <div class="workout-header">
                    <h3>${formatDate(workout.workout_date)}</h3>
                    <span class="workout-stats">
                        ${workout.num_exercises} exercise(s) • ${Math.round(workout.total_volume)} lbs
                    </span>
                </div>
                <div class="workout-exercises">
                    ${workout.exercises.map(ex => `
                        <div class="exercise-tag">
                            <strong>${ex.name}</strong>
                            <span class="exercise-details">
                                ${ex.num_sets} sets • ${ex.max_weight} lbs max • ${ex.total_reps} total reps
                            </span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');
        
        console.log(`Loaded ${workouts.length} workouts`);
        
    } catch (error) {
        console.error('Error loading workouts:', error);
        workoutList.innerHTML = '<p class="error">Error loading workouts. Please try again.</p>';
    }
}

// Format date nicely
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
        weekday: 'short',
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}