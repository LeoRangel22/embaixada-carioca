const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'assets/event-system-link.js'), 'utf8');

for (const gtagAvailable of [true, false]) {
  const calls = [], handlers = [];
  const window = gtagAvailable ? {gtag: (...args) => calls.push(args)} : {};
  const context = {
    window, URL, location: {pathname: '/en/eventos.html', search: '?email=private@example.test'},
    document: {documentElement: {lang: 'en'}, addEventListener: (name, fn) => handlers.push(fn)},
  };
  vm.runInNewContext(source, context);
  vm.runInNewContext(source, context);
  assert.equal(handlers.length, 1, 'tracker must not register twice');
  handlers[0]({target: {closest: () => null}});
  const link = {href: 'https://leorangel22.github.io/main/formulario.html?utm_source=embaixadacarioca', closest: () => null};
  handlers[0]({target: {closest: () => link}});
  const payload = gtagAvailable ? calls[0][2] : window.dataLayer[0];
  assert.equal(gtagAvailable ? calls[0][1] : payload.event, 'ec_event_form_cta_click');
  assert.equal(payload.page_language, 'en');
  assert.equal(payload.cta_destination, 'event_system');
  assert.ok(!JSON.stringify(payload).includes('private@'));
  link.href = 'https://go.tagme.com.br/embaixadacarioca';
  handlers[0]({target: {closest: () => link}});
  assert.equal(gtagAvailable ? calls.length : window.dataLayer.length, 1, 'reservations are not event leads');
}

(async () => {
  const route = fs.readFileSync(path.join(root, 'functions/[[path]].js'), 'utf8');
  const {onRequest} = await import('data:text/javascript;base64,' + Buffer.from(route).toString('base64'));
  for (const pathname of ['/formulario', '/formulario.html']) {
    const response = await onRequest({request: new Request('https://www.embaixadacarioca.com' + pathname + '?email=private@example.test&redirect=https://evil.test')});
    assert.equal(response.status, 301);
    const target = new URL(response.headers.get('Location'));
    assert.equal(target.origin, 'https://leorangel22.github.io');
    assert.equal(target.pathname, '/main/formulario.html');
    assert.ok(!target.search.includes('private'));
    assert.ok(!target.search.includes('evil'));
  }
  console.log('PASS: handoff analytics, reservation isolation, fixed 301 redirect, no personal data forwarding');
})().catch(error => { console.error(error); process.exitCode = 1; });
