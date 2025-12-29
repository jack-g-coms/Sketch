const API_BASE = 'http://127.0.0.1:8000/ai';

export const getPrediction = (drawing) => {
    return fetch(`${API_BASE}/predict/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            drawing
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`AI API prediction error, status: ${response.status}`);
        }
        return response.json();
    });
}