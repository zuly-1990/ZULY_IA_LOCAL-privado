const { Client } = require('ssh2');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
if (args.length < 2) {
  console.log("Usage: node upload_sftp.js <localPath> <remotePath>");
  process.exit(1);
}

const conn = new Client();
const localPath = path.resolve(args[0]);
const remotePath = args[1];

conn.on('ready', () => {
  console.log('Client :: ready');
  conn.sftp((err, sftp) => {
    if (err) throw err;
    sftp.fastPut(localPath, remotePath, (err) => {
      if (err) throw err;
      console.log(`File uploaded successfully to ${remotePath}`);
      conn.end();
    });
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  password: 'ZULY.server.77'
});
