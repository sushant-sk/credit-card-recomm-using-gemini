// src/pages/Home.jsx
import "./Home.css";
import ChatWindow from "../components/ChatWindow";

export default function Home() {
  return (
    <div className="page-wrapper">
      <div className="developer-menu">
        <div className="expandable-button">
          <button className="main-button">About the Developer - Sushant Subhash Kaddu</button>
          <div className="hidden-links">
            <a href="https://in.linkedin.com/in/sushant-kaddu-56844722b" target="_blank" rel="noreferrer">LinkedIn</a>
            <a href="https://github.com/sushant-sk" target="_blank" rel="noreferrer">GitHub</a>
            <a href="https://drive.google.com/file/d/16yN5tpl3Ys0YvZjmESpbZ-80_l4uPGOl/view?usp=drive_link" target="_blank" rel="noreferrer">Resume</a>
          </div>
        </div>
      </div>

      <main>
        <div className="hero-title">
          <h1>Credit Card Recommender</h1>
        </div>
        <ChatWindow />
      </main>
    </div>
  );
}
