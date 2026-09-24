const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Helper to execute fetch requests with error handling
 */
async function fetchFromApi(endpoint) {
  try {
    const res = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Accept': 'application/json',
      },
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Erro HTTP ${res.status}: ${res.statusText}`);
    }

    return await res.json();
  } catch (err) {
    console.error(`Erro ao consultar ${endpoint}:`, err);
    throw err;
  }
}

export async function fetchStatus() {
  return fetchFromApi('/');
}

export async function fetchFilmes() {
  return fetchFromApi('/filmes/');
}

export async function fetchSalas() {
  return fetchFromApi('/salas/');
}

export async function fetchTiposIngresso() {
  return fetchFromApi('/tipos-ingresso/');
}

export async function fetchSessoes() {
  return fetchFromApi('/sessoes/');
}
