const { execSync } = require('child_process');
const fs = require('fs');

try {
    const base64Data = execSync('node ../ssh_exec.js "base64 /opt/zuly/Zuly_String_Art_3D.blend"', { maxBuffer: 50 * 1024 * 1024 });
    const b64String = base64Data.toString().split('\n').filter(l => !l.includes('Failed to open dir') && !l.includes('Client :: ready')).join('');
    fs.writeFileSync('Zuly_String_Art_3D.blend', Buffer.from(b64String, 'base64'));
    console.log("File downloaded and decoded successfully.");
} catch(e) {
    console.error(e);
}
