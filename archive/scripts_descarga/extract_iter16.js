const fs = require('fs');
const zlib = require('zlib');

const fileContents = fs.createReadStream('Planos y premodelado/Iter16.gz');
const writeStream = fs.createWriteStream('Planos y premodelado/Zuly_Villa_Savoye_Nodos_Iter_16.blend');
const unzip = zlib.createGunzip();

fileContents.pipe(unzip).pipe(writeStream);
writeStream.on('finish', () => {
    console.log("Extracted Iter 16 successfully.");
});
