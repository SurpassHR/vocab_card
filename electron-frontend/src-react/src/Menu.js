import './Menu.css';

const NewMenu = () => {
  return (
    <div id="custom-menu">
      <ul>
        <li key="menu-date">日期</li>
      </ul>
      <span className="button-container">
        <button className="window-button" id="minimize"></button>
        <button className="window-button" id="maximize"></button>
        <button className="window-button" id="close"></button>
      </span>
    </div>
  )
}

export default NewMenu;