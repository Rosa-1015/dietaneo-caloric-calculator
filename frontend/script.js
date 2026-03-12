// API endpoint (change to production URL)
const API_URL = 'http://91.98.20.231:8001';

// Get form reference
const form = document.getElementById('calorieForm');

// Listen for form submission
form.addEventListener('submit', async (event) => {
    // Prevent page reload
    event.preventDefault();

    // Get form values
    const gender = document.getElementById('gender').value;
    const weight = document.getElementById('weight').value;
    const height = document.getElementById('height').value;
    const age = document.getElementById('age').value;
    const activity = document.getElementById('activity').value;

    // Convert commas to dots (e.g., 75,5 → 75.5)
    const normalizedWeight = weight.replace(',', '.');
    const normalizedHeight = height.replace(',', '.');
    const normalizedAge = age.replace(',', '.');

    // Show loading indicator
    showLoading();

    try {
        // Send data to API
        const response = await fetch(`${API_URL}/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sexo: gender,
                peso: parseFloat(normalizedWeight),
                altura: parseFloat(normalizedHeight),
                edad: parseFloat(normalizedAge),
                nivel_actividad: parseInt(activity),
            }),
        });

        // Parse response as JSON
        const data = await response.json();

        // Hide loading indicator
        hideLoading();

        // Check for API errors
        if (data.status === 'error') {
            showError(data.message || 'Unknown error');
            return;
        }

        // Display results if successful
        displayResults(data);

    } catch (error) {
        // Handle connection errors
        hideLoading();
        showError(`Connection error: ${error.message}`);
        console.error('Error:', error);
    }
});

/**
 * Display loading indicator
 */
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('results').style.display = 'none';
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

/**
 * Display error message to user
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.innerHTML = `<strong>Error:</strong> ${message}`;
    errorDiv.style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

/**
 * Display calculated results
 */
function displayResults(data) {
    // Set main result
    document.getElementById('totalCalories').textContent =
        Math.round(data.total_calorias_diarias);

    // Set BMR
    document.getElementById('bmr').textContent =
        Math.round(data.calorias_en_reposo);

    // Calculate activity factor from API response
    const activityFactor = (data.total_calorias_diarias + data.reduccion_edad) / data.calorias_en_reposo;
    document.getElementById('activityFactor').textContent =
        activityFactor.toFixed(2);

    document.getElementById('ageReduction').textContent =
        Math.round(data.reduccion_edad);
    document.getElementById('usedWeight').textContent =
        data.peso_utilizado_kg.toFixed(1);

    // Show supplementation warning if needed
    const supplementationWarning = document.getElementById('supplementationWarning');
    if (data.suplementacion_requerida && data.aviso_suplementacion) {
        document.getElementById('supplementationText').textContent =
            data.aviso_suplementacion;
        supplementationWarning.style.display = 'block';
    } else {
        supplementationWarning.style.display = 'none';
    }

    // Display professional recommendation
    if (data.recomendacion) {
        document.getElementById('recommendationText').textContent =
            data.recomendacion;
    }

    // Display legal notice
    if (data.aviso_legal) {
        document.getElementById('legalText').textContent =
            data.aviso_legal;
    }

    // Hide errors and show results
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    // Smooth scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Reset form and hide results
 */
function resetForm() {
    form.reset();
    document.getElementById('results').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    // Smooth scroll back to form
    form.scrollIntoView({ behavior: 'smooth' });
}
