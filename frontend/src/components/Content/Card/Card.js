import { useState, React } from 'react';
import './Card.css';
import Indexer from './Indexer.js';
import Word from './Word.js';
import CardContent from './CardContent.js';

const Card = ({ wordData, currIdx, totalNum }) => {
  if (!wordData) {
    return <div className="card">No word data available.</div>;
  }

  const { word, pronounce, meaning } = wordData;
  const [hovered, setHovered] = useState(false);

  return (
    <div className="card" onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)} >
      <Indexer currIdx={currIdx} totalNum={totalNum} />
      <Word word={word} />
      <CardContent hoveredState={hovered} pronounce={pronounce} meaning={meaning} />
    </div>
  );
};

export default Card;
