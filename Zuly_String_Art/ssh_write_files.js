const { Client } = require('ssh2');
const fs = require('fs');

const conn = new Client();
conn.on('ready', () => {
  console.log('Client :: ready');
  conn.exec('cat > /opt/zuly/string_art_blender.py', (err, stream) => {
    if (err) throw err;
    stream.on('close', () => {
      console.log('Uploaded python script');
      conn.exec('cat > /opt/zuly/pin_sequence.json', (err, stream2) => {
          if (err) throw err;
          stream2.on('close', () => {
              console.log('Uploaded JSON');
              conn.end();
          });
          stream2.write(fs.readFileSync('pin_sequence.json'));
          stream2.end();
      });
    });
    stream.write(fs.readFileSync('string_art_blender.py'));
    stream.end();
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  privateKey: fs.readFileSync('C:\\Users\\Admin\\.ssh\\id_rsa')
});
