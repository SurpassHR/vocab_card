const { app, BrowserWindow, globalShortcut } = require('electron');
const path = require('path')

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 600,
    height: 1000,
    alwaysOnTop: true,
    frame: false,
    webPreferences: {
      webSecurity: false
    }
  });
  const isDev = process.env.DEV_ENV;
  if (isDev === 'true') {
    mainWindow.loadURL(`http://localhost:${process.env.REACT_PORT}`);
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadURL(path.join(__dirname, 'dist-react/index.html'));
  }
}

function registerWindowShortcut() {
  globalShortcut.register('CommandOrControl+W', () => {
    app.quit();
  })
}

app.on('ready', () => {
  console.log('window ready');
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  })
  registerWindowShortcut();
})

app.on('window-all-closed', () => {
  if (process.platform != 'darwin') {
    app.quit();
  }
})