const fs = require('fs');
const zlib = require('zlib');

const fileContents = fs.createReadStream('StringArt.gz');
const writeStream = fs.createWriteStream('Zuly_String_Art_3D.blend');
const unzip = zlib.createGunzip();

fileContents.pipe(unzip).pipe(writeStream);
writeStream.on('finish', () => {
    console.log("Extracted String Art successfully.");
});
