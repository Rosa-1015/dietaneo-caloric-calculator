// URL de la API (cambiar a tu URL de producción)
const API_URL = 'http://localhost:8001';

// Obtener referencia al formulario
const form = document.getElementById('calorieForm');

// Escuchar cuando el usuario hace click en "Calcular"
form.addEventListener('submit', async (event) => {
    // Evitar que la página se recargue
    event.preventDefault();

    // Obtener los valores del formulario
    const gender = document.getElementById('gender').value;
    const weight = document.getElementById('weight').value;
    const height = document.getElementById('height').value;
    const age = document.getElementById('age').value;
    const activity = document.getElementById('activity').value;

    // Convertir comas a puntos (ej: 75,5 → 75.5)
    const normalizedWeight = weight.replace(',', '.');
    const normalizedHeight = height.replace(',', '.');
    const normalizedAge = age.replace(',', '.');

    // Mostrar indicador de carga
    showLoading();

    try {
        // Enviar los datos a la API
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

        // Obtener la respuesta en formato JSON
        const data = await response.json();

        // Ocultar el indicador de carga
        hideLoading();

        // Verificar si hubo un error
        if (data.status === 'error') {
            showError(data.message || 'Error desconocido');
            return;
        }

        // Si todo fue bien, mostrar los resultados
        displayResults(data);

    } catch (error) {
        // Si hay error de conexión, mostrar mensaje
        hideLoading();
        showError(`Error de conexión: ${error.message}`);
        console.error('Error:', error);
    }
});

/**
 * Función: Mostrar el indicador de carga
 */
function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('results').style.display = 'none';
}

/**
 * Función: Ocultar el indicador de carga
 */
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

/**
 * Función: Mostrar mensaje de error
 */
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.innerHTML = `<strong>Error:</strong> ${message}`;
    errorDiv.style.display = 'block';
    document.getElementById('results').style.display = 'none';
}

/**
 * Función: Mostrar los resultados calculados
 */
function displayResults(data) {
    // Completar el resultado principal
    document.getElementById('totalCalories').textContent =
        Math.round(data.total_calorias_diarias);

    // Completar los detalles
    document.getElementById('bmr').textContent =
        Math.round(data.calorias_en_reposo);

    // Calcular el factor de actividad a partir de los datos devueltos
    const activityFactor = (data.total_calorias_diarias + data.reduccion_edad) / data.calorias_en_reposo;
    document.getElementById('activityFactor').textContent =
        activityFactor.toFixed(2);

    document.getElementById('ageReduction').textContent =
        Math.round(data.reduccion_edad);
    document.getElementById('usedWeight').textContent =
        data.peso_utilizado_kg.toFixed(1);

    // Mostrar aviso de suplementación si es necesario
    const supplementationWarning = document.getElementById('supplementationWarning');
    if (data.suplementacion_requerida && data.aviso_suplementacion) {
        document.getElementById('supplementationText').textContent =
            data.aviso_suplementacion;
        supplementationWarning.style.display = 'block';
    } else {
        supplementationWarning.style.display = 'none';
    }

    // Mostrar recomendación profesional
    if (data.recomendacion) {
        document.getElementById('recommendationText').textContent =
            data.recomendacion;
    }

    // Mostrar aviso legal
    if (data.aviso_legal) {
        document.getElementById('legalText').textContent =
            data.aviso_legal;
    }

    // Ocultar errores y mostrar resultados
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('results').style.display = 'block';

    // Desplazarse hacia los resultados automáticamente
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Función: Reiniciar el formulario para calcular nuevamente
 */
function resetForm() {
    form.reset();
    document.getElementById('results').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    // Desplazarse hacia el formulario
    form.scrollIntoView({ behavior: 'smooth' });
}
