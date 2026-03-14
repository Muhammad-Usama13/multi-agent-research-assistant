// src/utils/api.js
import axios from "axios";

const BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

const api = axios.create({ baseURL: BASE });

export const uploadPDF = (file) => {
  const form = new FormData();
  form.append("file", file);
  return api.post("/api/upload/pdf", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const runAnalysis = (payload) =>
  api.post("/api/analysis/run", payload);

export const searchPapers = (q, max_results = 5) =>
  api.get("/api/analysis/search", { params: { q, max_results } });

export const healthCheck = () => api.get("/api/health");

export default api;
