const API_URL = 'http://91.98.20.231:8001';

const form = document.getElementById('calorieForm');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const gender = document.getElementById('gender').value;
    const weight = document.getElementById('weight').value;
    const height = document.getElementById('height').value;
    const age = document.getElementById('age').value;
    const activity = document.getElementById('activity').value;

    const normalizedWeight = weight.replace(',', '.');
    const normalizedHeight = height.replace(',', '.');
    const normalizedAge = age.replace(',', '.');

    showLoading();

    try {
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

        const data = await response.json();

        hideLoading();

        if (data.status === 'error') {
            showError(data.message || 'Unknown error');
            return;
        }

        displayResults(data);

    } catch (error) {
        hideLoading();
        showError(`Connection error: ${error.message}`);
        console.error('Error:', error);
    }
});

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('results').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.innerHTML = `<strong>Error:</strong> ${message}`;
    errorDiv.style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

function displayResults(data) {
    document.getElementById('totalCalories').textContent =
        Math.round(data.total_calorias_diarias);

    document.getElementById('bmr').textContent =
        Math.round(data.calorias_en_reposo);

    const activityFactor = (data.total_calorias_diarias + data.reduccion_edad) / data.calorias_en_reposo;
    document.getElementById('activityFactor').textContent =
        activityFactor.toFixed(2);

    document.getElementById('ageReduction').textContent =
        Math.round(data.reduccion_edad);
    document.getElementById('usedWeight').textContent =
        data.peso_utilizado_kg.toFixed(1);

    const supplementationWarning = document.getElementById('supplementationWarning');
    if (data.suplementacion_requerida && data.aviso_suplementacion) {
        document.getElementById('supplementationText').textContent =
            data.aviso_suplementacion;
        supplementationWarning.style.display = 'block';
    } else {
        supplementationWarning.style.display = 'none';
    }

    if (data.recomendacion) {
        document.getElementById('recommendationText').textContent =
            data.recomendacion;
    }

    if (data.aviso_legal) {
        document.getElementById('legalText').textContent =
            data.aviso_legal;
    }

    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function resetForm() {
    form.reset();
    document.getElementById('results').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    form.scrollIntoView({ behavior: 'smooth' });
}
