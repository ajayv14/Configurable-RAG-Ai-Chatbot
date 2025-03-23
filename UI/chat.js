import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { text: input, sender: "user" };
    setMessages([...messages, newMessage]);

    try {
      const response = await fetch("http://localhost:5000/similarity_search_query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: input }),
      });

      const data = await response.json();
      if (data.response) {
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: data.response.join("\n"), sender: "bot" },
        ]);
      }
    } catch (error) {
      console.error("Error fetching response:", error);
    }

    setInput("");
  };

  return (
    <div className="container mt-4">
      <h2 className="text-center">Chat with Vector Search</h2>
      <div className="card p-3">
        <div className="chat-box" style={{ height: "300px", overflowY: "scroll" }}>
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`alert ${msg.sender === "user" ? "alert-primary" : "alert-secondary"}`}
            >
              <strong>{msg.sender === "user" ? "You" : "Bot"}:</strong> {msg.text}
            </div>
          ))}
        </div>
        <div className="input-group mt-3">
          <input
            type="text"
            className="form-control"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && sendMessage()}
          />
          <button className="btn btn-primary" onClick={sendMessage}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
