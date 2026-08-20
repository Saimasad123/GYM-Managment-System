import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

const cache = new Map();
const CACHE_TTL_MS = 30_000;

function getCacheKey(config) {
  return `${config.method}:${config.url}`;
}

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => {
    if (response.config.method === "get") {
      const key = getCacheKey(response.config);
      cache.set(key, {
        data: response.data,
        timestamp: Date.now(),
      });
    }

    return response;
  },
  (error) => {
    if (error.config && error.config.method === "get") {
      const key = getCacheKey(error.config);
      const entry = cache.get(key);

      if (entry && Date.now() - entry.timestamp < CACHE_TTL_MS) {
        return Promise.resolve({
          data: entry.data,
          status: 200,
          statusText: "OK",
          headers: {},
          config: error.config,
        });
      }

      cache.delete(key);
    }

    return Promise.reject(error);
  }
);

export function clearCache() {
  cache.clear();
}

export function clearCacheFor(url) {
  for (const key of cache.keys()) {
    if (key.includes(url)) {
      cache.delete(key);
    }
  }
}

export default api;
