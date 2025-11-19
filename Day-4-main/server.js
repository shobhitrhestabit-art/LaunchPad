const http = require("http");
const url = require("url");

// Create HTTP server
const server = http.createServer((req, res) => {
  const parsedUrl = url.parse(req.url, true);

  if (parsedUrl.pathname === "/echo") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(req.headers));
  } else if (parsedUrl.pathname === "/slow") {
    const delay = parseInt(parsedUrl.query.ms) || 1000;
    setTimeout(() => {
      res.writeHead(200, { "Content-Type": "text/plain" });
      res.end(`Response delayed by ${delay}ms`);
    }, delay);
  } else if (parsedUrl.pathname === "/cache") {
    res.writeHead(200, {
      "Content-Type": "text/plain",
      "Cache-Control": "max-age=60",
    });
    res.end("This response is cached for 60 seconds");
  } else {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("Not Found");
  }
});

// Port number
const PORT = 3000;

// Start server with success & error handling
server.listen(PORT, () => {
  console.log(`✅ Server started successfully on http://localhost:${PORT}`);
});

// Catch any server errors (e.g., port already in use)
server.on("error", (err) => {
  console.error("❌ Server failed to start:", err.message);
});
