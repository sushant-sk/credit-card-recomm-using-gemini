import "./ChatWindow.css";

import { useState, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import { fetchRecommendations } from "../api";
import CardSummary from "./CardSummary";

const questions = [
  "What is your monthly income?",
  "Do you prefer travel, shopping, or cashback rewards?",
  "Do you travel internationally often?",
  "Do you want a credit card with no annual fee?",
  "How often do you use credit cards per month (rough estimate)?",
  "What is your age and occupation?",
];

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [answers, setAnswers] = useState({});
  const [currentQ, setCurrentQ] = useState(0);
  const [input, setInput] = useState("");
  const [cards, setCards] = useState(null);
  const [isLoading, setIsLoading] = useState(false);


  useEffect(() => {
    if (messages.length === 0) {
      setMessages([{ text: questions[0], isUser: false }]);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newAnswers = {
      ...answers,
      [questions[currentQ]]: input,
    };

    const newMessages = [...messages, { text: input, isUser: true }];
    setInput("");

    if (currentQ + 1 === questions.length) {
      setMessages(newMessages);
      setAnswers(newAnswers);
      setCurrentQ(currentQ + 1);
      setIsLoading(true);

      const res = await fetchRecommendations(newAnswers);
      setCards(res.cards);
      setIsLoading(false);
      setMessages([
        ...newMessages,
        { text: "Here are the best credit card options for you:", isUser: false },
      ]);
    } else {
      newMessages.push({ text: questions[currentQ + 1], isUser: false });
      setMessages(newMessages);
      setAnswers(newAnswers);
      setCurrentQ(currentQ + 1);
    }
  };

  return (
    <div className="chat-wrapper">
      <div className={`chat-layout ${isLoading || cards ? "with-right" : "centered"}`}>
        <div className="chat-left">
          <div className="chat-box">
            {messages
              .filter((msg) => msg.text !== "Here are the best credit card options for you:")
              .map((msg, i) => (
                <div key={i} style={{ marginBottom: "0.8rem" }}>
                  <MessageBubble text={msg.text} isUser={msg.isUser} />
                </div>
              ))}

            {currentQ < questions.length && (
              <form onSubmit={handleSubmit} className="form-container">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  className="form-input"
                  placeholder="Type your answer..."
                  required
                />
                <button className="send-button">Send</button>
              </form>
            )}
          </div>
        </div>

        <div className="chat-right">
          {isLoading ? (
            <div className="loading-box">⏳ Getting Gemini’s recommendations...</div>
          ) : (
            cards && <CardSummary cards={cards} />
          )}
        </div>

      </div>  
    </div>
  );
}
