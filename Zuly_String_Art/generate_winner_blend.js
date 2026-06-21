const { execSync } = require('child_process');
const fs = require('fs');

try {
    const winner = fs.readFileSync('best_attempt.txt', 'utf8').trim();
    console.log(`Generating BIM for Winner: ${winner}`);
    
    // Upload the winner's JSON sequence to the server
    execSync(`scp -i C:\\Users\\Admin\\.ssh\\id_rsa pin_sequence_${winner}.json root@167.233.69.104:/opt/zuly/pin_sequence.json`);
    
    // Upload the blender script (which reads pin_sequence.json)
    execSync(`scp -i C:\\Users\\Admin\\.ssh\\id_rsa string_art_blender.py root@167.233.69.104:/opt/zuly/`);
    
    // Run Blender on the server
    console.log("Running Blender on server...");
    execSync(`node ../ssh_exec.js "/usr/local/bin/blender --background --python /opt/zuly/string_art_blender.py"`);
    
    // The server will save it as Zuly_String_Art_3D.blend
    // We should rename it to Zuly_String_Art_${winner}.blend before compressing
    execSync(`node ../ssh_exec.js "mv /opt/zuly/Zuly_String_Art_3D.blend /opt/zuly/Zuly_String_Art_${winner}.blend"`);
    
    // Compress it
    console.log("Compressing...");
    execSync(`node ../ssh_exec.js "gzip -c /opt/zuly/Zuly_String_Art_${winner}.blend > /opt/zuly/StringArt_${winner}.gz"`);
    
    // Download it using Base64
    console.log("Downloading via Base64...");
    const base64Data = execSync(`node ../ssh_exec.js "base64 /opt/zuly/StringArt_${winner}.gz"`, { maxBuffer: 50 * 1024 * 1024 });
    const b64String = base64Data.toString().replace(/\r\n/g, '').replace(/\n/g, '').replace(/Failed to open dir \(No such file or directory\): \/run\/user\/0\/gvfs\//g, '').replace(/Client :: ready/g, '');
    fs.writeFileSync(`StringArt_${winner}.gz`, Buffer.from(b64String, 'base64'));
    
    // Decompress it locally
    console.log("Decompressing locally...");
    const zlib = require('zlib');
    const fileContents = fs.createReadStream(`StringArt_${winner}.gz`);
    const writeStream = fs.createWriteStream(`Zuly_String_Art_${winner}.blend`);
    const unzip = zlib.createGunzip();
    fileContents.pipe(unzip).pipe(writeStream);
    writeStream.on('finish', () => {
        console.log(`BIM generation and download complete for ${winner}!`);
    });

} catch(e) {
    console.error(e);
}
