const { Client } = require('ssh2');
const conn = new Client();
const cmd = `pkill -f zuly_scraper_arquitectura.py || echo "Scraper no estaba corriendo"`;

conn.on('ready', () => {
  conn.exec(cmd, (err, stream) => {
    if (err) throw err;
    stream.on('close', (code, signal) => {
      conn.end();
      process.exit(code);
    }).on('data', (data) => {
      process.stdout.write(data);
    }).stderr.on('data', (data) => {
      process.stderr.write(data);
    });
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  password: 'ZULY.server.77'
});
