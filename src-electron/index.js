const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path')
const { spawn } = require('child_process');

let mainWindow;
async function createWindow() {
  // 先创建窗口但不立即加载内容
  mainWindow = new BrowserWindow({
    width: 600,
    height: 1000,
    frame: false,
    show: false, // 初始隐藏窗口
    webPreferences: {
      webSecurity: true,
      preload: path.resolve(__dirname, './preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // 添加加载指示器
  mainWindow.on('ready-to-show', () => {
    mainWindow.show();
  });

  const isDev = process.env.DEV_ENV;
  try {
    if (isDev === 'true') {
      await mainWindow.loadURL(`http://localhost:${process.env.REACT_PORT}`);
      mainWindow.webContents.openDevTools();
    } else {
      await mainWindow.loadURL(path.join(__dirname, 'dist-react/index.html'));
    }
  } catch (err) {
    console.error('加载窗口内容失败:', err);
  }
}

let server;
function startServer() {
  server = spawn('potapp-server', [], { cwd: './' });
  console.log(`启动后端 pid: ${server.pid}`);

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

function killWin32Server() {
  if (server && server.pid) {
    const command = 'taskkill /IM potapp-server.exe /F';
    spawn('cmd', ['/c', command]);
  }
}

function killLinuxServer() {
  if (server && server.pid) {
    const command = `kill -INT -${server.pid}`;
    spawn("sh", ["-c", command]);
  }
}

function actionCloseAllWindows() {
  const platform = process.platform;
  if (platform == 'win32') {
    killWin32Server();
  } else if (platform == 'linux') {
    killLinuxServer();
  }
  server.kill("SIGINT");
  server.kill("SIGTERM");
  server.kill("SIGKILL");

  if (platform != 'darwin') {
    app.quit();
  }
}

function actionMinimizeWindow() {
  mainWindow.minimize();
}

function actionMaximizeWindow() {
  if (mainWindow.isMaximized()) {
    mainWindow.unmaximize();
  } else {
    mainWindow.maximize();
  }
}

// 注册进程间通信
function registerIPCMsg() {
  // 窗口控制 api
  ipcMain.on('close-window', actionCloseAllWindows);
  ipcMain.on('minimize-window', actionMinimizeWindow);
  ipcMain.on('maximize-window', actionMaximizeWindow);
}

app.on('ready', async () => {
  console.log('应用准备就绪');
  try {
    // 先启动后端服务
    await startServer();
    console.log('后端服务已启动');

    // 然后创建窗口
    await createWindow();
    console.log('窗口已创建');

    registerIPCMsg();
    console.log('IPC消息已注册');
  } catch (err) {
    console.error('启动失败:', err);
    app.quit();
  }

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', actionCloseAllWindows)
