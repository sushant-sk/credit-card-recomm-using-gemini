// import "./CardSummary.css";

// export default function CardSummary({ cards }) {
//   if (!cards?.gemini_recommendation) {
//     return (
//       <div className="card-summary-empty">
//         No Gemini summary available at the moment.
//       </div>
//     );
//   }

//   return (
//     <div className="card-summary-wrapper">
//       <div className="card-summary-box">
//         <h3 className="card-summary-title">🔍 Gemini’s Summary</h3>
//         {cards.gemini_recommendation.split("\n").map((line, i) => (
//           <p key={i} className="card-summary-line">• {line}</p>
//         ))}
//       </div>
//     </div>
//   );
// }


// import "./CardSummary.css";

// export default function CardSummary({ cards }) {
//   if (!cards?.gemini_recommendation) {
//     return (
//       <div className="card-summary-empty">
//         No Gemini summary available at the moment.
//       </div>
//     );
//   }

//   const lines = cards.gemini_recommendation.split("\n").filter(line => line.trim() !== "");

//   const sections = [];
//   let currentSection = { title: null, items: [] };

//   lines.forEach((line) => {
//     if (line.startsWith("✅")) {
//       if (currentSection.title || currentSection.items.length > 0) {
//         sections.push(currentSection);
//         currentSection = { title: null, items: [] };
//       }
//       currentSection.title = line;
//     } else if (line.startsWith("⚠️") || line.startsWith("❌")) {
//       if (currentSection.title || currentSection.items.length > 0) {
//         sections.push(currentSection);
//         currentSection = { title: null, items: [] };
//       }
//       currentSection.title = line;
//     } else {
//       currentSection.items.push(line);
//     }
//   });

//   if (currentSection.title || currentSection.items.length > 0) {
//     sections.push(currentSection);
//   }

//   return (
//     <div className="card-summary-wrapper">
//       <div className="card-summary-box">
//         <h3 className="card-summary-title">🔍 Gemini’s Summary</h3>

//         <div className="card-summary-section card-summary-intro">
//           <p className="card-summary-line">{lines[0]}</p>
//         </div>

//         {sections.map((section, index) => (
//           <div className="card-summary-section" key={index}>
//             {section.title && <h4 className="card-summary-subtitle">{section.title}</h4>}
//             {section.items.map((item, idx) => (
//               <p className="card-summary-line" key={idx}>{item}</p>
//             ))}
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }


import "./CardSummary.css";

export default function CardSummary({ cards }) {
  if (!cards?.gemini_recommendation) {
    return (
      <div className="card-summary-empty">
        No Gemini summary available at the moment.
      </div>
    );
  }

  const summary = cards.gemini_recommendation;

  // Extract sections using regex
  const introMatch = summary.match(/^(.+?)\n(?=✅|⚠️|❌)/s);
  const topPicksMatch = summary.match(/✅ Top Picks.*?(?=⚠️|❌|$)/s);
  const situationalMatch = summary.match(/⚠️ Situational Picks.*?(?=❌|$)/s);
  const poorFitsMatch = summary.match(/❌ Poor Fits.*?$/s);

  return (
    <div className="card-summary-wrapper">
      <div className="card-summary-box">
        <h3 className="card-summary-title">🔍 Gemini’s Summary</h3>

        {introMatch && (
          <div className="card-summary-section intro-section">
            <p className="card-summary-subtitle">🧠 Personal Insight</p>
            <p className="card-summary-line">{introMatch[1].trim()}</p>
          </div>
        )}

        {topPicksMatch && (
          <div className="card-summary-section top-picks-section">
            <p className="card-summary-subtitle">✅ Top Picks (Best for You)</p>
            {topPicksMatch[0]
              .split("\n")
              .slice(1)
              .filter((line) => line.trim())
              .map((line, i) => (
                <p key={i} className="card-summary-line">
                  {line.trim()}
                </p>
              ))}
          </div>
        )}

        {situationalMatch && (
          <div className="card-summary-section situational-section">
            <p className="card-summary-subtitle">⚠️ Situational Picks</p>
            {situationalMatch[0]
              .split("\n")
              .slice(1)
              .filter((line) => line.trim())
              .map((line, i) => (
                <p key={i} className="card-summary-line">
                  {line.trim()}
                </p>
              ))}
          </div>
        )}

        {poorFitsMatch && (
          <div className="card-summary-section poor-fits-section">
            <p className="card-summary-subtitle">❌ Poor Fits (Avoid These)</p>
            {poorFitsMatch[0]
              .split("\n")
              .slice(1)
              .filter((line) => line.trim())
              .map((line, i) => (
                <p key={i} className="card-summary-line">
                  {line.trim()}
                </p>
              ))}
          </div>
        )}
      </div>
    </div>
  );
}
