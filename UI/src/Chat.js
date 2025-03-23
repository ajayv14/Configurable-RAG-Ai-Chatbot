// Chat.js
import React, { useState } from "react";

function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Append user message
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await fetch("http://127.0.0.1:5000/similarity_search_query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });

      const data = await response.json();

      // Extract the text content from the response array
      const botResponses = data.response.map((doc) => ({
        text: doc.content, // Extract page content only
        sender: "bot"
      }));

      setMessages([...newMessages, ...botResponses]); // Append bot responses
    } catch (error) {
      console.error("Error fetching response:", error);
    }
  };

  return (
    <div className="card p-3">
      <div className="chat-box" style={{ height: "300px", overflowY: "auto" }}>
        {messages.map((msg, index) => (
          <div key={index} className={`alert ${msg.sender === "user" ? "alert-primary" : "alert-secondary"}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-group mt-3">
        <input
          type="text"
          className="form-control"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button className="btn btn-primary" onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default Chat;
