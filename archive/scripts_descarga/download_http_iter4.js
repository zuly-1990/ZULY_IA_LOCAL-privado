const http = require('http');
const fs = require('fs');

const file = fs.createWriteStream("Planos y premodelado/Iter4.gz");
http.get("http://167.233.69.104:8081/Iter4.gz", function(response) {
  response.pipe(file);
  file.on("finish", () => {
      file.close();
      console.log("Download complete via HTTP");
  });
}).on("error", (err) => {
  fs.unlink("Planos y premodelado/Iter4.gz", () => {});
  console.log("Error: " + err.message);
});
