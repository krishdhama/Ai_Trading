// Central API client for all backend requests.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }

  return response.json();
}

export const api = {
  initScenario: () => request("/scenario/init"),
  nextDay: () => request("/scenario/next-day", { method: "POST" }),
  executeTrade: (payload) =>
    request("/trade", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  analyzeBehavior: (payload) =>
    request("/analyze-behavior", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getAIFeedback: (payload) =>
    request("/ai-feedback", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  getPortfolio: () => request("/portfolio"),
  getTradeHistory: () => request("/trade-history"),
};
