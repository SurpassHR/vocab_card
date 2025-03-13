import { useState, React } from 'react';
import './Card.css';

const Card = ({ wordData, currIdx, totalNum }) => {
  if (!wordData) {
    return <div>No word data available.</div>;
  }

  const { word, pronounce, explanations, example } = wordData;
  const [hovered, setHovered] = useState(false);

  return (
    <div className="card"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="index">{currIdx + '/' + totalNum}</div>
      <div className="word">{word}</div>
      {hovered &&
        <>
          <div className="pronunciation">
            {pronounce.map((p, index) => (
              <span key={index} className="pronunciation-item">
                {p.region} {p.symbol}
              </span>
            ))}
          </div>
          <div className="explanations">
            {explanations.map((exp, index) => (
              <div key={index} className="explanation-item">
                <span className="trait">{exp.trait}</span>
                <span className="meaning">{exp.meaning}</span>
                <span className="explain">{exp.explain}</span>
              </div>
            ))}
          </div>
          <div className="examples">
            {example.map((ex, index) => (
              <div key={index} className="example-item">
                <span className="exampleEn">{ex.exampleEn}</span>
                <span className="exampleZh">{ex.exampleZh}</span>
              </div>
            ))}
          </div>
        </>
      }
    </div>
  );
};

export default Card;
