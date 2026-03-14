// src/hooks/useAnalysis.js
import { useState, useCallback } from "react";
import { uploadPDF, runAnalysis, searchPapers } from "../utils/api";
import toast from "react-hot-toast";

export const useAnalysis = () => {
  const [loading, setLoading] = useState(false);
  const [stage, setStage]     = useState("");
  const [results, setResults] = useState(null);
  const [searchResults, setSearchResults] = useState([]);

  const stages = [
    "📄 Processing document...",
    "🔍 Reader Agent analyzing...",
    "📝 Summarization Agent working...",
    "💡 Explanation Agent simplifying...",
    "🔬 Critic Agent evaluating...",
    "📊 Generating final report...",
  ];

  const simulateStages = (callback) => {
    let i = 0;
    const tick = () => {
      if (i < stages.length) {
        setStage(stages[i++]);
        setTimeout(tick, 900);
      } else {
        callback();
      }
    };
    tick();
  };

  const analyzeByQuery = useCallback(async (query) => {
    setLoading(true);
    setResults(null);
    let done = false;

    simulateStages(() => { done = true; });

    try {
      const res = await runAnalysis({ query, mode: "full" });
      // Wait for stage animation to finish
      const wait = () => done
        ? Promise.resolve()
        : new Promise((r) => setTimeout(() => r(wait()), 200));
      await wait();
      setResults(res.data);
      toast.success("Analysis complete!");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "Analysis failed.");
    } finally {
      setLoading(false);
      setStage("");
    }
  }, []);

  const analyzeByPDF = useCallback(async (file) => {
    setLoading(true);
    setResults(null);
    let done = false;
    simulateStages(() => { done = true; });

    try {
      // 1) Upload
      setStage("⬆️  Uploading PDF...");
      const upload = await uploadPDF(file);
      const { doc_id } = upload.data;

      // 2) Analyze
      const res = await runAnalysis({ doc_id, query: file.name, mode: "full" });
      const wait = () => done
        ? Promise.resolve()
        : new Promise((r) => setTimeout(() => r(wait()), 200));
      await wait();
      setResults(res.data);
      toast.success("PDF analysis complete!");
    } catch (e) {
      toast.error(e?.response?.data?.detail || "PDF analysis failed.");
    } finally {
      setLoading(false);
      setStage("");
    }
  }, []);

  const search = useCallback(async (q) => {
    try {
      const res = await searchPapers(q, 6);
      setSearchResults(res.data.results || []);
    } catch {
      toast.error("Search failed.");
    }
  }, []);

  return {
    loading,
    stage,
    results,
    searchResults,
    analyzeByQuery,
    analyzeByPDF,
    search,
    clearResults: () => setResults(null),
  };
};
