
var http = require('http');
var url = require('url');

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  var q = url.parse(req.url, true).query;
  var txt = q.year + " " + q.month;
  res.end(txt);
  res.end("Hello World")
}).listen(8080);

const hostname = 'localhost';
const port = 8080;

console.log(`Server running at http://${hostname}:${port}/`);
