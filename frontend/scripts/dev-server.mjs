import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import { createServer } from 'node:http';
import { extname, join } from 'node:path';

const types = { '.css': 'text/css', '.html': 'text/html', '.js': 'text/javascript' };
const root = join(process.cwd(), 'src');

const server = createServer(async (request, response) => {
  const requested = request.url === '/' ? '/index.html' : request.url;
  const file = join(root, requested.replace(/^\//, ''));
  try {
    const info = await stat(file);
    if (!info.isFile()) throw new Error('Not a file');
    response.writeHead(200, { 'Content-Type': types[extname(file)] || 'application/octet-stream' });
    createReadStream(file).pipe(response);
  } catch {
    response.writeHead(404).end('Not found');
  }
});

const shutdown = () => server.close(() => process.exit(0));
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
server.listen(8080, '0.0.0.0', () => console.log('Development frontend listening on 8080'));
