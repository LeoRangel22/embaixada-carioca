const LEGACY_REDIRECTS = new Map([
  ["/general-3", "/"],
  ["/inquiry-services-page", "/eventos.html"],
  ["/caf%C3%A9-da-manh%C3%A3-com-a-melhor-vista-do-rio", "/cafe-da-manha-com-vista-rio-de-janeiro.html"],
  ["/en/como-chegar.html", "/en/how-to-get-there.html"],
  ["/restaurante-urca.html", "/restaurante-morro-da-urca.html"],
]);

function redirect(requestUrl, destination) {
  const target = new URL(destination, requestUrl);
  target.search = new URL(requestUrl).search;
  return new Response(null, {
    status: 301,
    headers: {
      Location: target.pathname + target.search,
      "Cache-Control": "public, max-age=3600",
    },
  });
}

async function storedHtml(context, publicPath) {
  const assetPath = `/_html${publicPath}.txt`;
  const assetUrl = new URL(assetPath, context.request.url);
  const assetRequest = new Request(assetUrl, context.request);
  const response = await context.env.ASSETS.fetch(assetRequest);

  if (response.status !== 200) return null;

  const headers = new Headers(response.headers);
  headers.set("Content-Type", "text/html; charset=UTF-8");
  headers.set("X-Canonical-HTML", "preserved");
  return new Response(context.request.method === "HEAD" ? null : response.body, {
    status: 200,
    headers,
  });
}

export async function onRequest(context) {
  const url = new URL(context.request.url);
  const path = url.pathname;

  // Fixed destination: do not forward arbitrary query strings or contact data.
  if (path === "/formulario" || path === "/formulario.html") {
    return new Response(null, {
      status: 301,
      headers: {
        Location: "https://leorangel22.github.io/main/formulario.html?utm_source=embaixadacarioca&utm_medium=website&utm_campaign=eventos&utm_content=formulario",
        "Cache-Control": "public, max-age=3600",
      },
    });
  }

  if (path.startsWith("/_html/")) {
    return new Response("Not found", { status: 404 });
  }

  if (LEGACY_REDIRECTS.has(path)) {
    return redirect(context.request.url, LEGACY_REDIRECTS.get(path));
  }

  if (path === "/") {
    return (await storedHtml(context, "/index.html")) || context.next();
  }

  if (path === "/en/" || path === "/es/") {
    return (await storedHtml(context, `${path}index.html`)) || context.next();
  }

  if (path.endsWith("/index.html")) {
    return redirect(context.request.url, path.slice(0, -"index.html".length));
  }

  if (path.endsWith(".html")) {
    return (await storedHtml(context, path)) || context.next();
  }

  if (!path.endsWith("/") && !path.split("/").pop().includes(".")) {
    const canonicalPath = `${path}.html`;
    if (await storedHtml(context, canonicalPath)) {
      return redirect(context.request.url, canonicalPath);
    }
  }

  return context.next();
}
