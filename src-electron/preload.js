const { contextBridge, ipcRenderer } = require('electron')

// 开放窗口控制按钮 api
contextBridge.exposeInMainWorld('windowCtrlApi', {
  minimize: () => {
    ipcRenderer.send('minimize-window');
  },
  maximize: () => {
    ipcRenderer.send('maximize-window');
  },
  close: () => {
    ipcRenderer.send('close-window');
  }
});