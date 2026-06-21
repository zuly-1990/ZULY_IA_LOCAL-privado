# Reglas de Prevención de Corrupción de Archivos
- **Cero Transferencias Binarias Directas:** Debido a inestabilidad extrema en el protocolo SSH/SFTP desde PowerShell hacia el servidor Linux `167.233.69.104`, **NUNCA** intentes descargar archivos binarios (especialmente `.blend`) usando `scp` o `sftp` directamente.
- **Protocolo Obligatorio de Descarga Segura:**
  1. Comprime el archivo en el servidor remoto usando `gzip` (`gzip -c archivo.blend > archivo.gz`).
  2. Descarga el archivo comprimido utilizando un script Node.js local (`execSync('node ssh_exec.js "base64 /opt/zuly/archivo.gz"')`).
  3. Limpia rigurosamente el string Base64 (`.replace(/\r\n/g, '').replace(/\n/g, '')`) antes de guardarlo para evitar que los saltos de línea de Windows corrompan la decodificación.
  4. Descomprime el `.gz` localmente usando `zlib` de Node.js.
  5. Este protocolo no es opcional, es una directiva estricta de Zuly para que no se vuelva a repetir ningún archivo corrupto.
