const { Client } = require('ssh2');

const conn = new Client();
conn.on('ready', () => {
    conn.sftp((err, sftp) => {
        if (err) throw err;
        console.log("SFTP Ready, downloading compressed file...");
        sftp.fastGet('/opt/zuly/Iter3.gz', 'Planos y premodelado/Iter3.gz', (err) => {
            if (err) console.error("Download error:", err);
            else console.log("Download complete.");
            conn.end();
        });
    });
}).connect({
    host: '167.233.69.104',
    port: 22,
    username: 'root',
    password: 'ZULY.server.77'
});
