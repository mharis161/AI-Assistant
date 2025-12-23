import React, { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Upload, Database, Clock, Calendar } from "lucide-react";

function ConfidenceBadge({ level }) {
  const color =
    level === "High"
      ? "bg-green-100 text-green-700 border-green-200"
      : level === "Medium"
        ? "bg-yellow-100 text-yellow-700 border-yellow-200"
        : "bg-red-100 text-red-700 border-red-200";
  return (
    <span className={`inline-flex items-center px-2 py-0.5 text-xs font-medium border rounded-full ${color}`}>
      {level || "Low"} Confidence
    </span>
  );
}

import ReactMarkdown from 'react-markdown';

function TypewriterText({ text, onComplete, scrollToBottom }) {
  const [displayedText, setDisplayedText] = useState("");

  useEffect(() => {
    let index = 0;
    setDisplayedText("");

    // Faster speed for longer text to avoid boring the user
    // Speed decreased slightly to 10/20ms to allow ReactMarkdown to keep up without glitching
    const speed = text.length > 500 ? 10 : 25;

    const interval = setInterval(() => {
      index++;
      // Always slice from the original text to ensure data integrity
      setDisplayedText(text.slice(0, index));

      // Auto-scroll to bottom as text grows
      if (scrollToBottom) scrollToBottom();

      if (index >= text.length) {
        clearInterval(interval);
        if (onComplete) onComplete();
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <div className="markdown-content">
      <ReactMarkdown>{displayedText}</ReactMarkdown>
    </div>
  );
}

function SourcesList({ sources }) {
  if (!sources || !sources.length) return null;
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="mt-4 rounded-md bg-slate-50 p-3 border border-slate-200"
    >
      <div className="text-xs font-semibold text-slate-600 mb-2 uppercase tracking-wider">Sources</div>
      <div className="grid gap-2 sm:grid-cols-2">
        {sources.map((s, idx) => (
          <div key={`${s.document}-${idx}`} className="text-xs text-slate-600 bg-white p-2 rounded border border-slate-100 shadow-sm">
            <div className="font-medium text-slate-800 truncate" title={s.document}>{s.document}</div>
            <div className="flex justify-between mt-1 text-slate-500">
              <span>Pg {s.page ?? "N/A"}</span>
              <span>{s.section ? `§ ${s.section}` : null}</span>
              <span className="font-mono text-xs">{(s.similarity * 100).toFixed(0)}% match</span>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

function Message({ role, content, sources, confidence, timestamp, responseTime, animate }) {
  const isUser = role === "user";
  const [isTypingDone, setIsTypingDone] = useState(!animate);

  // Format Date and Time
  const dateObj = timestamp ? new Date(timestamp) : new Date();
  const dateStr = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  const timeStr = dateObj.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

  return (
    <div className={`w-full border-b border-black/5 ${isUser ? "bg-white" : "bg-slate-50/80"}`}>
      <div className="mx-auto max-w-3xl px-4 py-8 flex gap-4 sm:gap-6">
        {/* Avatar */}
        <div className="flex-shrink-0 flex flex-col items-center gap-1">
          <div className={`w-8 h-8 rounded-sm flex items-center justify-center shadow-sm ${isUser ? "bg-slate-800" : "bg-green-600"
            }`}>
            {isUser ? (
              <User className="w-5 h-5 text-white" />
            ) : (
              <Bot className="w-5 h-5 text-white" />
            )}
          </div>
        </div>

        {/* Content */}
        <div className="flex-1 min-w-0 space-y-1">
          <div className="flex items-center gap-2 mb-1">
            <span className="font-semibold text-sm text-slate-900">
              {isUser ? "You" : "AI Assistant"}
            </span>
            <span className="text-xs text-slate-400 flex items-center gap-1">
              <Calendar className="w-3 h-3" /> {dateStr}
              <Clock className="w-3 h-3 ml-1" /> {timeStr}
            </span>
            {!isUser && responseTime && (
              <span className="text-xs text-slate-400 bg-slate-100 px-1.5 py-0.5 rounded-full">
                {responseTime}s
              </span>
            )}
            {!isUser && confidence && <ConfidenceBadge level={confidence} />}
          </div>

          <div className="prose prose-slate prose-sm max-w-none leading-7 text-slate-800">
            {animate && !isUser ? (
              <TypewriterText
                text={content}
                onComplete={() => setIsTypingDone(true)}
                scrollToBottom={() => {
                  document.querySelector('#end-of-chat')?.scrollIntoView({ behavior: "smooth" });
                }}
              />
            ) : (
              <div className="markdown-content">
                <ReactMarkdown>{content}</ReactMarkdown>
              </div>
            )}
          </div>

          {/* Only show sources after typing is done */}
          {!isUser && sources && isTypingDone && <SourcesList sources={sources} />}
        </div>
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="w-full border-b border-black/5 bg-slate-50/80">
      <div className="mx-auto max-w-3xl px-4 py-8 flex gap-4 sm:gap-6">
        <div className="w-8 h-8 rounded-sm bg-green-600 flex items-center justify-center shadow-sm">
          <Bot className="w-5 h-5 text-white" />
        </div>
        <div className="flex items-center gap-1">
          <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce" />
          <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:.15s]" />
          <span className="w-2 h-2 bg-slate-400 rounded-full animate-bounce [animation-delay:.3s]" />
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Hello! I am your AI Policy Assistant. I can answer questions based strictly on the PDF documents you upload.\n\nHow can I help you today?",
      confidence: null,
      sources: [],
      timestamp: new Date().toISOString(),
      animate: false, // Don't animate initial message
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState(null);
  const [uploading, setUploading] = useState(false);
  const endRef = useRef(null);
  const fileRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSubmit(e) {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    const startTime = Date.now();

    // Add User Message
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: question,
        timestamp: new Date().toISOString()
      }
    ]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "Request failed");
      }

      const data = await res.json();
      const endTime = Date.now();
      const duration = ((endTime - startTime) / 1000).toFixed(2);

      // Add Assistant Message with animation
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          sources: data.sources,
          confidence: data.confidence,
          timestamp: new Date().toISOString(),
          responseTime: duration,
          animate: true, // Enable animation for new messages
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `❌ Error: ${err.message || "Unable to process your request."}`,
          confidence: "Low",
          sources: [],
          timestamp: new Date().toISOString(),
          animate: true,
        },
      ]);
    } finally {
      setLoading(false);
      void refreshStats();
    }
  }

  async function refreshStats() {
    try {
      const res = await fetch("/api/stats");
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch {
      // ignore stats errors
    }
  }

  async function handleUpload() {
    const file = fileRef.current?.files?.[0];
    if (!file || uploading) return;
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      const res = await fetch("/api/upload", {
        method: "POST",
        body: fd,
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `✅ ${data.message || "Upload complete."}`,
          confidence: null,
          timestamp: new Date().toISOString(),
          animate: true,
        },
      ]);
      fileRef.current.value = "";
      await refreshStats();
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `❌ Upload error: ${err.message || "Failed to upload file."}`,
          confidence: null,
          timestamp: new Date().toISOString(),
          animate: true,
        },
      ]);
    } finally {
      setUploading(false);
    }
  }

  useEffect(() => {
    void refreshStats();
  }, []);

  return (
    <div className="flex flex-col h-screen bg-white text-slate-900 font-sans">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b bg-white">
        <div className="mx-auto max-w-3xl px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-700">AI Policy Assistant</span>
            <span className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">v1.0</span>
          </div>

          <div className="flex items-center gap-3">
            {stats && (
              <div className="hidden sm:flex items-center gap-2 text-xs text-slate-500">
                <Database className="w-3.5 h-3.5" />
                <span>{stats.total_chunks} chunks</span>
              </div>
            )}
            <div className="flex items-center gap-2">
              <input id="file" ref={fileRef} type="file" accept="application/pdf" className="hidden" onChange={handleUpload} />
              <button
                onClick={() => fileRef.current?.click()}
                disabled={uploading}
                className="text-xs flex items-center gap-1.5 bg-slate-900 text-white px-3 py-1.5 rounded hover:bg-slate-800 transition disabled:opacity-50"
              >
                <Upload className="w-3.5 h-3.5" />
                {uploading ? "Uploading..." : "Upload PDF"}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <main className="flex-1 overflow-y-auto scroll-smooth">
        <div className="flex flex-col pb-32">
          {messages.map((m, idx) => (
            <Message
              key={idx}
              role={m.role}
              content={m.content}
              sources={m.sources}
              confidence={m.confidence}
              timestamp={m.timestamp}
              responseTime={m.responseTime}
              animate={m.animate}
            />
          ))}
          {loading && <TypingIndicator />}
          <div id="end-of-chat" ref={endRef} className="h-4" />
        </div>
      </main>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-white via-white to-transparent pt-10 pb-6">
        <div className="mx-auto max-w-3xl px-4">
          <form onSubmit={handleSubmit} className="relative shadow-2xl rounded-xl border border-slate-200 bg-white overflow-hidden focus-within:ring-2 focus-within:ring-slate-200 transition-shadow">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask a question about your policies..."
              className="w-full px-4 py-4 pr-12 text-slate-700 placeholder:text-slate-400 focus:outline-none text-base"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 disabled:opacity-50 transition"
            >
              <Send className="w-5 h-5" />
            </button>
          </form>
          <div className="text-center mt-2">
            <p className="text-[10px] text-slate-400">
              AI can make mistakes. Please verify important information from the source documents.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
