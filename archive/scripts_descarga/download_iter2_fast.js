const { Client } = require('ssh2');
const fs = require('fs');

const conn = new Client();
conn.on('ready', () => {
    conn.sftp((err, sftp) => {
        if (err) throw err;
        console.log("SFTP Ready, downloading...");
        sftp.fastGet('/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_2.blend', 'Planos y premodelado/Zuly_Villa_Savoye_Nodos_Iter_2.blend', (err) => {
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
