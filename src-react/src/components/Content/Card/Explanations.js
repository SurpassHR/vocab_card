import './Explanations.css';

const Explanations = ({ meaning }) => {
  return (
    <div className="explanations">
      {Object.keys(meaning).map((key, _) => {
        return (
          <div key={key} className="explanation-item">
            <span className="trait">{meaning[key].trait}</span>
            <span className="explain">
              <strong>{key != 'null' ? key : ''}</strong>
              {' ' + meaning[key].explain}
            </span>
            <br />
            {meaning[key].exampleEn.map((innerKey, index) => (
              <div key={innerKey}>
                <span className="exampleEn">{meaning[key].exampleEn[index]}</span>
                <br />
                <span className="exampleZh">{meaning[key].exampleZh[index]}</span>
              </ div>
            ))}
          </div>)
      })}
    </div>
  );
}

export default Explanations;