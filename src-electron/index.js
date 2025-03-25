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

let server;
function startServer() {
  const { spawn } = require('child_process');

  server = spawn('venv/Scripts/python', ['server.py'], { cwd: './dist-fastapi' });

  // 监听标准输出数据
  server.stdout.on('data', (data) => {
    console.log(`stdout: ${data.toString()}`); // 将 Buffer 转换为字符串
  });

  // 监听标准错误输出数据
  server.stderr.on('data', (data) => {
    console.error(`stderr: ${data.toString()}`);
  });

  // 监听进程退出事件
  server.on('close', (code) => {
    console.log(`子进程退出，退出码 ${code}`);
  });

  server.on('error', (err) => {
    console.error(`启动子进程失败: ${err}`);
  });
}

function killServer() {
  if (server) {
    server.kill('SIGTERM');
  }
}

app.on('ready', () => {
  console.log('window ready');
  createWindow();
  startServer();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  })
  registerWindowShortcut();
})

app.on('window-all-closed', () => {
  killServer();
  if (process.platform != 'darwin') {
    app.quit();
  }
})