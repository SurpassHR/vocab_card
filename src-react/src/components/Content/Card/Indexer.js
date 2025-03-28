import './Indexer.css';

const Indexer = ({ currIdx, totalNum }) => {
  return <div className="indexer">{currIdx + '/' + totalNum}</div>;
}

export default Indexer;