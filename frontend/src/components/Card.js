import { useState, React } from 'react';
import './Card.css';
import { nanoid } from 'nanoid';

const Card = ({ wordData, currIdx, totalNum }) => {
  if (!wordData) {
    return <div>No word data available.</div>;
  }

  const { word, pronounce, meaning } = wordData;
  const [hovered, setHovered] = useState(false);

  return (
    <div className="card"
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
    >
      <div className="index">{currIdx + '/' + totalNum}</div>
      <div className="word">{word}</div>
      <div className={hovered ? 'card-content' : 'card-content-hidden'}>
        <div className="pronunciation">
          {pronounce.map((p, index) => (
            <span key={index} className="pronunciation-item">
              {p.region} {p.symbol}
            </span>
          ))}
        </div>
        <div className="explanations">
          {Object.keys(meaning).map((key, index) => {
            return (
              <div key={index} className="explanation-item">
                <span className="trait">{meaning[key].trait}</span>
                <span className="explain">
                  <strong>{key != 'null' ? key : ''}</strong>
                  {' ' + meaning[key].explain}
                </span>
                <br />
                {meaning[key].exampleEn.map((_, index) => (
                  <>
                    <span key={nanoid()} className="exampleEn">{meaning[key].exampleEn[index]}</span>
                    <br />
                    <span key={nanoid()} className="exampleZh">{meaning[key].exampleZh[index]}</span>
                  </>
                ))}
              </div>)
          })}
        </div>
      </div>
    </div>
  );
};

export default Card;
