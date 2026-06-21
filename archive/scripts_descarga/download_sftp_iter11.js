const { Client } = require('ssh2');
const fs = require('fs');

const conn = new Client();
conn.on('ready', () => {
  console.log('Client :: ready');
  conn.sftp((err, sftp) => {
    if (err) throw err;
    console.log("SFTP Ready, downloading Iter11...");
    sftp.fastGet('/opt/zuly/Iter11.gz', 'Planos y premodelado/Iter11.gz', (err) => {
      if (err) {
          console.error("Download failed", err);
      } else {
          console.log("Download complete via SFTP");
      }
      conn.end();
    });
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  privateKey: fs.readFileSync('C:\\Users\\Admin\\.ssh\\id_rsa')
});
