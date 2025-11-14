"use client";

import { useState } from "react";

interface Message {
  sender: "user" | "bot";
  text: string;
}

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { sender: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await res.json();
      console.log("API Response:", data);

      const botText = data.message?.content || JSON.stringify(data);
      const botMsg: Message = { sender: "bot", text: botText };
      setMessages(prev => [...prev, botMsg]);
    } catch (error) {
      console.error("Error:", error);
      setMessages(prev => [...prev, { sender: "bot", text: "Error connecting to Ollama" }]);
    }
  };

  return (
    <div className="border border-white/70 bg-white rounded-2xl shadow w-full max-w-lg mx-auto p-5" id="chatBoxDiv">
      <div className="h-64 overflow-y-auto mb-3 flex flex-col gap-2 bg-white border border-slate-200 rounded-xl p-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`p-2 rounded-lg font-medium ${
              msg.sender === "user"
                ? "self-end bg-blue-500 text-black"
                : "self-start bg-gray-200 text-black"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          className="flex-1 border border-gray-600 rounded-lg p-2 text-black"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type state code (e.g., CA)"
        />
        <button className="bg-gray-900 text-white px-4 rounded-lg" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}
