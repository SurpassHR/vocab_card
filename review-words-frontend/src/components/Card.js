import React from 'react';
import './Card.css';

const Card = ({ wordData }) => {
  if (!wordData) {
    return <div>No word data available.</div>;
  }

  const { word, pronounce, explanations, example } = wordData;

  return (
    <div className="card">
      <div className="word">{word}</div>
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
    </div>
  );
};

export default Card;
