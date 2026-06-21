const fs = require('fs');
const zlib = require('zlib');

const fileContents = fs.createReadStream('Planos y premodelado/Iter100.gz');
const writeStream = fs.createWriteStream('Planos y premodelado/Zuly_Villa_Savoye_Nodos_Iter_100_Ciudad.blend');
const unzip = zlib.createGunzip();

fileContents.pipe(unzip).pipe(writeStream);
writeStream.on('finish', () => {
    console.log("Extracted successfully.");
});
