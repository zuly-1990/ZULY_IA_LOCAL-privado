const { Client } = require('ssh2');

const conn = new Client();
conn.on('ready', () => {
    conn.sftp((err, sftp) => {
        if (err) throw err;
        console.log("SFTP Ready, downloading (concurrency=1)...");
        // Using fastGet with concurrency: 1 to ensure it doesn't drop packets on slow links
        sftp.fastGet('/opt/zuly/Zuly_Villa_Savoye_Nodos_Iter_2.blend', 'Planos y premodelado/Zuly_Villa_Savoye_Nodos_Iter_2.blend', { concurrency: 1 }, (err) => {
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
