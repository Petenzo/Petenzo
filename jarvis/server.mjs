// Jarvis — lokalny asystent głosowy. Mózg: Claude Agent SDK. Interfejs: przeglądarka (public/).
// Serwer słucha wyłącznie na 127.0.0.1, bo agent może wykonywać polecenia na tym komputerze.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { query } from '@anthropic-ai/claude-agent-sdk';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const PUBLIC = path.join(ROOT, 'public');
const WORKSPACE = path.join(ROOT, 'workspace');
const MEMORY = path.join(WORKSPACE, 'memory.md');
const STATE = path.join(ROOT, '.jarvis-state.json');
const PORT = Number(process.env.JARVIS_PORT || 7777);
const USER_TITLE = process.env.JARVIS_TITLE || 'szefie';
const PERMISSION_TIMEOUT_MS = 120_000;

fs.mkdirSync(WORKSPACE, { recursive: true });
if (!fs.existsSync(MEMORY)) {
  fs.writeFileSync(
    MEMORY,
    '# Pamięć Jarvisa\n\nTu Jarvis zapisuje trwałe fakty o użytkowniku: kim jest, czym się zajmuje, jakie ma projekty i preferencje.\n',
  );
}

let state = { sessionId: null };
try {
  state = JSON.parse(fs.readFileSync(STATE, 'utf8'));
} catch {}
const saveState = () => fs.writeFileSync(STATE, JSON.stringify(state));

const clients = new Set();
const pending = new Map(); // id -> resolve(boolean)
let running = null; // { abort: AbortController }

function broadcast(event) {
  const line = `data: ${JSON.stringify(event)}\n\n`;
  for (const res of clients) res.write(line);
}

function systemAppend() {
  const memory = fs.readFileSync(MEMORY, 'utf8');
  return `
Jesteś Jarvisem — osobistym asystentem AI użytkownika, sterowanym głosem. Zwracaj się do niego "${USER_TITLE}".

Zasady rozmowy:
- Twoje odpowiedzi są czytane NA GŁOS przez syntezator mowy. Pisz czystym tekstem po polsku: bez markdownu, tabel, list z myślnikami, emoji, bloków kodu i długich adresów URL.
- Mów krótko: zwykle jedno do trzech zdań. Najpierw wynik, potem ewentualnie jedno zdanie szczegółu. Długie treści (kod, listy, raporty) zapisuj do pliku w katalogu roboczym i powiedz tylko, gdzie są i co zawierają.
- Polecenia pochodzą z rozpoznawania mowy, więc mogą zawierać przekręcone słowa. Domyśl się intencji; dopytaj tylko wtedy, gdy pomyłka zmieniłaby wynik.
- Wykonuj zadania samodzielnie do końca. Zanim zrobisz coś nieodwracalnego lub widocznego dla innych (wysłanie maila, publikacja, płatność, usunięcie), powiedz jednym zdaniem, co dokładnie zrobisz — system i tak poprosi użytkownika o potwierdzenie.
- Jeśli czegoś nie możesz zrobić, bo brakuje narzędzia lub dostępu, powiedz to wprost i podaj, co trzeba podłączyć.

Pamięć:
- Plik ${MEMORY} to Twoja trwała pamięć. Gdy dowiesz się o użytkowniku czegoś trwałego (imię, firma, projekty, preferencje, stałe polecenia), dopisz to tam zwięźle. Nie zapisuj jednorazowych zadań.
- Aktualna zawartość pamięci:
${memory}
`;
}

function describeTool(name, input = {}) {
  const short = (s, n = 140) => (String(s).length > n ? String(s).slice(0, n) + '…' : String(s));
  if (name === 'Bash') return `Polecenie: ${short(input.command)}`;
  if (name === 'Write') return `Zapis pliku: ${input.file_path}`;
  if (name === 'Edit' || name === 'NotebookEdit') return `Edycja pliku: ${input.file_path || input.notebook_path}`;
  if (name === 'Read') return `Czytam: ${input.file_path}`;
  if (name === 'Grep' || name === 'Glob') return `Szukam w plikach: ${short(input.pattern, 60)}`;
  if (name === 'WebSearch') return `Szukam w sieci: ${short(input.query, 80)}`;
  if (name === 'WebFetch') return `Otwieram stronę: ${short(input.url, 80)}`;
  if (name === 'Agent' || name === 'Task') return `Pomocnik: ${short(input.description || '', 80)}`;
  if (name.startsWith('mcp__')) {
    const [, server, ...tool] = name.split('__');
    return `${server.replaceAll('_', ' ')}: ${tool.join(' ').replaceAll('_', ' ')}`;
  }
  return name;
}

// Wywoływane tylko wtedy, gdy Claude Code i tak zapytałby o zgodę. Odczyty i edycje plików
// w katalogu roboczym przechodzą bez pytania; polecenia systemowe i konektory (mail itd.) pytają.
async function canUseTool(toolName, input, { signal }) {
  const target = input.file_path ? path.resolve(WORKSPACE, String(input.file_path)) : null;
  if ((toolName === 'Edit' || toolName === 'Write') && target === MEMORY) {
    return { behavior: 'allow', updatedInput: input };
  }
  const id = crypto.randomUUID();
  const summary = describeTool(toolName, input);
  broadcast({ type: 'permission', id, tool: toolName, summary });
  const allowed = await new Promise((resolve) => {
    const finish = (value) => {
      clearTimeout(timer);
      pending.delete(id);
      resolve(value);
    };
    const timer = setTimeout(() => finish(false), PERMISSION_TIMEOUT_MS);
    signal.addEventListener('abort', () => finish(false), { once: true });
    pending.set(id, finish);
  });
  broadcast({ type: 'permission_closed', id, allowed });
  return allowed
    ? { behavior: 'allow', updatedInput: input }
    : { behavior: 'deny', message: 'Użytkownik nie wyraził zgody na tę akcję.' };
}

async function ask(text) {
  const abort = new AbortController();
  running = { abort };
  broadcast({ type: 'status', state: 'thinking' });
  try {
    const stream = query({
      prompt: text,
      options: {
        cwd: WORKSPACE,
        abortController: abort,
        resume: state.sessionId || undefined,
        model: process.env.JARVIS_MODEL || undefined,
        systemPrompt: { type: 'preset', preset: 'claude_code', append: systemAppend() },
        settingSources: ['user'],
        permissionMode: 'acceptEdits',
        canUseTool,
      },
    });
    for await (const msg of stream) {
      if (msg.type === 'system' && msg.subtype === 'init') {
        state.sessionId = msg.session_id;
        saveState();
      } else if (msg.type === 'assistant' && !msg.parent_tool_use_id) {
        for (const block of msg.message.content) {
          if (block.type === 'text' && block.text.trim()) broadcast({ type: 'say', text: block.text });
          if (block.type === 'tool_use') broadcast({ type: 'tool', summary: describeTool(block.name, block.input) });
        }
      } else if (msg.type === 'result') {
        if (msg.is_error) broadcast({ type: 'error', text: `Zadanie przerwane (${msg.subtype}).` });
        broadcast({ type: 'done', cost: msg.total_cost_usd ?? null });
      }
    }
  } catch (err) {
    if (!abort.signal.aborted) {
      const message = String(err?.message || err);
      // Sesja z poprzedniego uruchomienia mogła zniknąć — następne polecenie zacznie nową rozmowę.
      if (state.sessionId) {
        state.sessionId = null;
        saveState();
      }
      broadcast({ type: 'error', text: message });
    }
  } finally {
    running = null;
    broadcast({ type: 'status', state: 'idle' });
  }
}

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.svg': 'image/svg+xml' };

function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
      if (body.length > 1e6) req.destroy();
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(body || '{}'));
      } catch (err) {
        reject(err);
      }
    });
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const allowedHosts = [`localhost:${PORT}`, `127.0.0.1:${PORT}`];
  const send = (code, data) => {
    res.writeHead(code, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(data));
  };
  // Obce strony w przeglądarce nie mogą sterować Jarvisem (ochrona przed CSRF i DNS rebinding).
  if (!allowedHosts.includes(req.headers.host)) return send(403, { error: 'forbidden' });
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'POST') {
    const origin = req.headers.origin;
    if (!origin || !allowedHosts.includes(new URL(origin).host)) return send(403, { error: 'forbidden' });
    let body;
    try {
      body = await readJson(req);
    } catch {
      return send(400, { error: 'bad json' });
    }
    if (url.pathname === '/api/ask') {
      const text = String(body.text || '').trim();
      if (!text) return send(400, { error: 'empty' });
      if (running) return send(409, { error: 'busy' });
      ask(text);
      return send(200, { ok: true });
    }
    if (url.pathname === '/api/permission') {
      const finish = pending.get(body.id);
      if (finish) finish(Boolean(body.allow));
      return send(200, { ok: Boolean(finish) });
    }
    if (url.pathname === '/api/stop') {
      running?.abort.abort();
      return send(200, { ok: true });
    }
    if (url.pathname === '/api/reset') {
      running?.abort.abort();
      state.sessionId = null;
      saveState();
      return send(200, { ok: true });
    }
    return send(404, { error: 'not found' });
  }

  if (url.pathname === '/events') {
    res.writeHead(200, { 'Content-Type': 'text/event-stream', 'Cache-Control': 'no-cache', Connection: 'keep-alive' });
    res.write(`data: ${JSON.stringify({ type: 'status', state: running ? 'thinking' : 'idle' })}\n\n`);
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  const file = path.join(PUBLIC, url.pathname === '/' ? 'index.html' : path.normalize(url.pathname));
  if (!file.startsWith(PUBLIC + path.sep) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
    return send(404, { error: 'not found' });
  }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
  fs.createReadStream(file).pipe(res);
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`\n  JARVIS online → http://localhost:${PORT}\n  Otwórz ten adres w Chrome lub Edge.\n`);
});
