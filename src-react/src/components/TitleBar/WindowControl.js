import './WindowControl.css';

const NewWindowControl = () => {
  return (
    <span className="control-button-container">
      <button className="control-button" id="minimize" onClick={electronAPI.windowControls.minimize}></button>
      <button className="control-button" id="maximize" onClick={electronAPI.windowControls.maximize}></button>
      <button className="control-button" id="close" onClick={electronAPI.windowControls.close}></button>
    </span>
  );
}

export default NewWindowControl;