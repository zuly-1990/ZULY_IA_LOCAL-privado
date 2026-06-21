const { Client } = require('ssh2');

const conn = new Client();
const cmd = process.argv[2] || 'uptime';

conn.on('ready', () => {
  conn.exec(cmd, (err, stream) => {
    if (err) {
      console.error('Execution error:', err);
      process.exit(1);
    }
    stream.on('close', (code, signal) => {
      conn.end();
      process.exit(code);
    }).on('data', (data) => {
      process.stdout.write(data);
    }).stderr.on('data', (data) => {
      process.stderr.write(data);
    });
  });
}).on('error', (err) => {
  console.error('Connection error:', err);
  process.exit(1);
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  password: 'ZULY.server.77'
});
