"use client";

import ChatBox from "../components/chat_bot";

export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-3xl font-semibold text-white text-center mb-3">
        Weather Chat Guide
      </h1>
      <p className="text-white/90 text-center mb-6">
        Ask about weather alerts or previous conditions—just mention a state or city.
      </p>
      <div className="max-w-xl mx-auto mb-6 bg-white/80 border border-white/60 rounded-lg p-4 text-sm text-slate-700">
        Example: <span className="font-medium">“How are conditions in San Diego today?”</span>
      </div>
      <ChatBox />
    </main>
  );
}