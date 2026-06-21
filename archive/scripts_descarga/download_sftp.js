const { Client } = require('ssh2');
const fs = require('fs');

const conn = new Client();

conn.on('ready', () => {
  console.log('Client :: ready');
  conn.sftp((err, sftp) => {
    if (err) throw err;
    sftp.fastGet('/opt/zuly/tools/ai_agents/zuly_tutor.py', 'zuly_tutor_remote.py', {}, (err) => {
      if (err) throw err;
      console.log('File downloaded successfully.');
      conn.end();
    });
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  password: 'ZULY.server.77'
});
