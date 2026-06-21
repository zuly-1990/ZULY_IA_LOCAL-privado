const { execSync } = require('child_process');
const fs = require('fs');

try {
    const base64Data = execSync('node ssh_exec.js "base64 /opt/zuly/Iter13.gz"', { maxBuffer: 50 * 1024 * 1024 });
    const b64String = base64Data.toString().replace(/\r\n/g, '').replace(/\n/g, '').replace(/Failed to open dir \(No such file or directory\): \/run\/user\/0\/gvfs\//g, '').replace(/Client :: ready/g, '');
    fs.writeFileSync('Planos y premodelado/Iter13.gz', Buffer.from(b64String, 'base64'));
    console.log("GZ File downloaded and decoded successfully without corruption.");
} catch(e) {
    console.error(e);
}
