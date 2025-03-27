const { contextBridge, ipcRenderer } = require('electron');

// 安全地暴露API给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  windowControls: {
    minimize: () => ipcRenderer.send('minimize-window'),
    maximize: () => ipcRenderer.send('maximize-window'),
    close: () => ipcRenderer.send('close-window')
  },
  onLoadStatus: (callback) => {
    ipcRenderer.on('load-status', (event, status) => {
      callback(status);
    });
  }
});

// 清理监听器防止内存泄漏
window.addEventListener('beforeunload', () => {
  ipcRenderer.removeAllListeners('load-status');
});
