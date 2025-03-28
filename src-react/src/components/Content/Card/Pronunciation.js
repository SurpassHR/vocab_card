import { nanoid } from 'nanoid';
import './Pronunciation.css';

const Pronunciation = ({ pronounce }) => {
  return (
    <div className="pronunciation">
      {pronounce.map((p, _) => (
        <span key={nanoid()} className="pronunciation-item">
          {p.region} {p.symbol}
        </span>
      ))}
    </div>
  );

}

export default Pronunciation;