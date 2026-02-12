// frontend/components/ChatBot.tsx
"use client";

import { useState } from "react";

export const ChatBot = () => {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<string[]>([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input) return;
    setMessages([...messages, `You: ${input}`, `Bot: I heard "${input}"`]);
    setInput("");
  };

  return (
    <div className="chatbot">
      <button onClick={() => setOpen(!open)}>
        {open ? "Close Chat" : "Chat with Bot"}
      </button>
      {open && (
        <div>
          <div style={{ maxHeight: 150, overflowY: "auto", marginTop: 10 }}>
            {messages.map((msg, i) => (
              <div key={i}>{msg}</div>
            ))}
          </div>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            style={{ width: "100%", marginTop: 5 }}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      )}
    </div>
  );
};
