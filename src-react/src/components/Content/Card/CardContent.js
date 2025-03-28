import './CardContent.css';
import Pronunciation from './Pronunciation.js';
import Explanations from './Explanations.js';

const CardContent = ({ hoveredState, pronounce, meaning }) => {
  return (
    <div className={hoveredState ? 'card-content' : 'card-content-hidden'}>
      <Pronunciation pronounce={pronounce} />
      <Explanations meaning={meaning} />
    </div>
  );
}

export default CardContent;