import './Menu.css';

const NewMenu = () => {
  return (
    <div id="custom-menu">
      <ul>
        <li key="menu-date">日期</li>
      </ul>
      <span className="button-container">
        <button className="window-button" id="minimize" onClick={electronAPI.windowControls.minimize}></button>
        <button className="window-button" id="maximize" onClick={electronAPI.windowControls.maximize}></button>
        <button className="window-button" id="close" onClick={electronAPI.windowControls.close}></button>
      </span>
    </div>
  )
}

export default NewMenu;