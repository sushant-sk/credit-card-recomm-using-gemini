// src/api.js
const BASE_URL = import.meta.env.VITE_BACKEND_URL;

export async function fetchRecommendations(answers) {
  const response = await fetch(`${BASE_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(answers),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch recommendations");
  }

  return response.json();
}
