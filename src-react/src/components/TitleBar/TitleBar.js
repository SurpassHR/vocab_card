import './TitleBar.css';
import NewWindowControl from './WindowControl.js';
import NewMenu from './Menu.js';

const TitleBar = () => {
  return (
    <div id="custom-title-bar">
      <NewMenu />
      <NewWindowControl />
    </div>
  );
}

export default TitleBar;