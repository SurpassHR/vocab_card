const { app, BrowserWindow, globalShortcut } = require('electron');
const path = require('path')

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    alwaysOnTop: true,
    frame: false
  });
  const isDev = process.env.DEV_ENV;
  const url = isDev === 'true' ? `http://127.0.0.1:${process.env.REACT_PORT}` : path.join(__dirname, '../dist-react/index.html');
  mainWindow.loadURL(url);
  mainWindow.webContents.openDevTools();
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