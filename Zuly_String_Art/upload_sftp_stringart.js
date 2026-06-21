const { Client } = require('ssh2');
const fs = require('fs');

const conn = new Client();
conn.on('ready', () => {
  console.log('Client :: ready');
  conn.sftp((err, sftp) => {
    if (err) throw err;
    console.log("SFTP Ready, uploading files...");
    sftp.fastPut('pin_sequence.json', '/opt/zuly/pin_sequence.json', (err) => {
      if (err) console.error("Upload failed 1", err);
      else {
          console.log("Uploaded pin_sequence.json");
          sftp.fastPut('string_art_blender.py', '/opt/zuly/string_art_blender.py', (err) => {
              if (err) console.error("Upload failed 2", err);
              else {
                  console.log("Uploaded string_art_blender.py");
              }
              conn.end();
          });
      }
    });
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  privateKey: fs.readFileSync('C:\\Users\\Admin\\.ssh\\id_rsa')
});
