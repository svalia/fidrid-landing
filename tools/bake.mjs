import { spawn } from 'node:child_process';
import { writeFileSync } from 'node:fs';

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const url = process.argv[2];
const out = process.argv[3];

const chrome = spawn(CHROME, [
  '--headless=new', '--disable-gpu', '--no-sandbox',
  '--allow-file-access-from-files',
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=/tmp/claude-chrome-bake',
  '--window-size=1440,900',
  'about:blank',
], { stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function waitForPort() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      if (r.ok) return;
    } catch {}
    await sleep(250);
  }
  throw new Error('Chrome не поднялся');
}

await waitForPort();
const tab = await (await fetch(`http://127.0.0.1:${PORT}/json/new?${encodeURIComponent(url)}`, { method: 'PUT' })).json();
const ws = new WebSocket(tab.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));

let id = 0;
const pending = new Map();
ws.addEventListener('message', e => {
  const m = JSON.parse(e.data);
  if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); }
});
function send(method, params = {}) {
  const i = ++id;
  ws.send(JSON.stringify({ id: i, method, params }));
  return new Promise(r => pending.set(i, r));
}

await send('Page.enable');
await send('Runtime.enable');
await send('Page.navigate', { url });
await sleep(9000);

const EXTRACT = String.raw`
(() => {
  // 1. Материализуем правила, которые support.js вложил через CSSOM insertRule
  for (const el of document.querySelectorAll('style')) {
    if (el.textContent.trim()) continue;
    const sheet = el.sheet;
    if (!sheet) continue;
    let css = '';
    try {
      for (const rule of sheet.cssRules) css += rule.cssText + '\n';
    } catch (e) { continue; }
    if (css) el.textContent = '\n' + css;
  }
  // Chrome при сериализации DOM теряет сокращённое свойство background
  // у элементов с background-clip:text (градиентный текст) - текст получается
  // прозрачным без заливки. Возвращаем градиент из вычисленных стилей.
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    const clip = cs.backgroundClip || cs.webkitBackgroundClip;
    if (clip === 'text' && !el.style.backgroundImage && cs.backgroundImage !== 'none') {
      el.style.backgroundImage = cs.backgroundImage;
    }
  }

  return document.documentElement.outerHTML;
})()
`;

const res = await send('Runtime.evaluate', { expression: EXTRACT, returnByValue: true, awaitPromise: false });
const html = res.result?.result?.value;
if (!html) { console.error('ОШИБКА:', JSON.stringify(res).slice(0, 800)); process.exit(1); }
writeFileSync(out, '<!DOCTYPE html>\n' + html, 'utf8');
console.log('OK, байт:', html.length);
ws.close();
chrome.kill();
process.exit(0);
