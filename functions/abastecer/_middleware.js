// Políticas apenas da área operacional. Páginas comerciais não são alteradas.
export async function onRequest(context) {
  const original = await context.next();
  const headers = new Headers(original.headers);
  headers.set('Cache-Control', 'no-store');
  headers.set('Permissions-Policy', 'camera=(self), microphone=(), geolocation=(), web-share=(self)');
  headers.set('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src 'self' blob:; connect-src 'self'; font-src 'self' data:; object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'");
  headers.set('X-Frame-Options', 'DENY');
  headers.set('X-Content-Type-Options', 'nosniff');
  headers.set('X-Robots-Tag', 'noindex, nofollow');
  headers.set('Referrer-Policy', 'no-referrer');
  headers.set('Strict-Transport-Security', 'max-age=86400');
  headers.set('X-Reposicao-Version', '2.7.0');
  return new Response(original.body, {status:original.status, statusText:original.statusText, headers});
}
