import "./MessageBubble.css";

export default function MessageBubble({ text, isUser }) {
  return (
    <div className={`message-row ${isUser ? "justify-end" : "justify-start"}`}>
      <div className={`message-bubble ${isUser ? "user" : "bot"}`}>
        {text}
      </div>
    </div>
  );
}
