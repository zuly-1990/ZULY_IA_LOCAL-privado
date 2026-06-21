const { Client } = require('ssh2');
const path = require('path');

const conn = new Client();

const filesToUpload = [
  {
    local: path.join(__dirname, 'core/reasoning/chain_of_thought.py'),
    remote: '/opt/zuly/core/reasoning/chain_of_thought.py'
  },
  {
    local: path.join(__dirname, 'core/utils/nlu.py'),
    remote: '/opt/zuly/core/utils/nlu.py'
  },
  {
    local: path.join(__dirname, 'core/agent.py'),
    remote: '/opt/zuly/core/agent.py'
  },
  {
    local: path.join(__dirname, 'core/adapters/blender_adapter.py'),
    remote: '/opt/zuly/core/adapters/blender_adapter.py'
  },
  {
    local: path.join(__dirname, 'core/commands/blender_command_registry.py'),
    remote: '/opt/zuly/core/commands/blender_command_registry.py'
  },
  {
    local: path.join(__dirname, 'core/commands/blender_handlers/geonodes.py'),
    remote: '/opt/zuly/core/commands/blender_handlers/geonodes.py'
  },
  {
    local: path.join(__dirname, 'decision_engine.py'),
    remote: '/opt/zuly/decision_engine.py'
  }
];

conn.on('ready', () => {
  console.log('Client :: ready');
  conn.sftp((err, sftp) => {
    if (err) throw err;
    
    let uploaded = 0;
    filesToUpload.forEach(file => {
      sftp.fastPut(file.local, file.remote, (err) => {
        if (err) throw err;
        console.log(`Uploaded ${file.local} to ${file.remote}`);
        uploaded++;
        if (uploaded === filesToUpload.length) {
          conn.end();
        }
      });
    });
  });
}).connect({
  host: '167.233.69.104',
  port: 22,
  username: 'root',
  password: 'ZULY.server.77'
});
