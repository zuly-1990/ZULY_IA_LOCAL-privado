const http = require('http');
const fs = require('fs');

const file = fs.createWriteStream("Planos y premodelado/Zuly_Villa_Savoye_Nodos_Iter_2.blend");
http.get("http://167.233.69.104:8080/Zuly_Villa_Savoye_Nodos_Iter_2.blend", function(response) {
  response.pipe(file);
  file.on("finish", () => {
      file.close();
      console.log("Download complete");
  });
}).on("error", (err) => {
  fs.unlink("Planos y premodelado/Zuly_Villa_Savoye_Nodos_Iter_2.blend", () => {});
  console.log("Error: " + err.message);
});
