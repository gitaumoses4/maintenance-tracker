const connect = require('connect');
const serveStatic = require('serve-static');
const dotenv = require('dotenv');

dotenv.config();
const server_port = process.env.FRONTEND_PORT || 7000;

connect().use(serveStatic(__dirname + "")).listen(server_port, function () {
  console.log("Server running on port " + server_port + "...");
});
