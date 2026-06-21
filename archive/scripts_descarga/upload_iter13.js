const { Client } = require('ssh2');
const fs = require('fs');

const conn = new Client();
conn.on('ready', () => {
  conn.exec('cat > /opt/zuly/zuly_iter13.py', (err, stream) => {
    if (err) throw err;
    stream.on('close', () => {
      console.log('Uploaded zuly_iter13.py');
      conn.end();
    });
    stream.write(fs.readFileSync('zuly_iter13.py'));
    stream.end();
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  privateKey: fs.readFileSync('C:\\Users\\Admin\\.ssh\\id_rsa')
});
