// ═══════════════════════════════════════════════════════════════════════════════
//  Google Apps Script — Avaliações GBP API → Google Sheets
//  Embaixada Carioca — Morro da Urca
//  Versão: 1.0 | Data: 2026-06-17
// ═══════════════════════════════════════════════════════════════════════════════
//
//  INSTRUÇÕES DE CONFIGURAÇÃO:
//  1. Abra o Google Sheets desejado
//  2. Vá em Extensões → Apps Script
//  3. Cole este código inteiro substituindo o conteúdo existente
//  4. Vá em Projeto → Propriedades do Projeto → Propriedades de Script
//     e adicione as seguintes chaves (NÃO coloque as credenciais diretamente
//     no código — use as Propriedades de Script para segurança):
//
//       CLIENT_ID      → seu client_id OAuth2
//       CLIENT_SECRET  → seu client_secret OAuth2
//       REFRESH_TOKEN  → seu refresh_token OAuth2
//
//  5. Salve (Ctrl+S) e execute "importarAvaliacoes"
//  6. Na primeira execução, autorize as permissões solicitadas
//
// ═══════════════════════════════════════════════════════════════════════════════

// ─── CONFIGURAÇÕES FIXAS ──────────────────────────────────────────────────────

const ACCOUNT_ID  = "accounts/106083628368200012478";
const LOCATION_ID = "locations/18008728615502069543";

// Nome das abas na planilha (serão criadas automaticamente se não existirem)
const ABA_AVALIACOES = "Avaliações";
const ABA_RESUMO     = "Resumo";

// Quantas avaliações buscar por página (máx. 50)
const PAGE_SIZE = 50;

// ─── MAPA DE ESTRELAS ─────────────────────────────────────────────────────────

const STAR_MAP = {
  "ONE":   1,
  "TWO":   2,
  "THREE": 3,
  "FOUR":  4,
  "FIVE":  5,
  "STAR_RATING_UNSPECIFIED": 0
};

// ─── CORES ────────────────────────────────────────────────────────────────────

const COR_CABECALHO   = "#1A1A2E";
const COR_OURO        = "#C9A84C";
const COR_VERDE       = "#D4EDDA";
const COR_VERMELHO    = "#F8D7DA";
const COR_LINHA_PAR   = "#F5F0E8";
const COR_LINHA_IMPAR = "#FFFFFF";


// ═══════════════════════════════════════════════════════════════════════════════
//  FUNÇÃO PRINCIPAL — Execute esta função para importar as avaliações
// ═══════════════════════════════════════════════════════════════════════════════

function importarAvaliacoes() {
  const ui = SpreadsheetApp.getUi();

  try {
    Logger.log("▶ Iniciando importação de avaliações...");

    // 1. Obter access token via refresh token
    Logger.log("🔐 Obtendo access token...");
    const accessToken = obterAccessToken();
    Logger.log("✅ Access token obtido.");

    // 2. Buscar todas as avaliações com paginação
    Logger.log("📥 Buscando avaliações da GBP API...");
    const resultado = buscarTodasAvaliacoes(accessToken);
    const avaliacoes = resultado.avaliacoes;
    const totalGoogle = resultado.totalGoogle;
    const notaMedia   = resultado.notaMedia;

    Logger.log(`✅ ${avaliacoes.length} avaliações coletadas de ${totalGoogle} no Google.`);

    // 3. Escrever na planilha
    Logger.log("📊 Escrevendo na planilha...");
    const ss = SpreadsheetApp.getActiveSpreadsheet();

    escreverAbaAvaliacoes(ss, avaliacoes);
    escreverAbaResumo(ss, avaliacoes, totalGoogle, notaMedia);

    Logger.log("✅ Importação concluída!");

    ui.alert(
      "✅ Importação Concluída!",
      `${avaliacoes.length} avaliações importadas com sucesso.\n\n` +
      `Nota média: ${notaMedia.toFixed(2)} ⭐\n` +
      `Total no Google: ${totalGoogle}`,
      ui.ButtonSet.OK
    );

  } catch (e) {
    Logger.log("❌ Erro: " + e.message);
    ui.alert("❌ Erro na importação", e.message, ui.ButtonSet.OK);
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  AUTENTICAÇÃO — Obtém access token via refresh token
// ═══════════════════════════════════════════════════════════════════════════════

function obterAccessToken() {
  // Lê as credenciais das Propriedades de Script (seguro — não ficam no código)
  const props = PropertiesService.getScriptProperties();
  const clientId     = props.getProperty("CLIENT_ID");
  const clientSecret = props.getProperty("CLIENT_SECRET");
  const refreshToken = props.getProperty("REFRESH_TOKEN");

  if (!clientId || !clientSecret || !refreshToken) {
    throw new Error(
      "Credenciais não configuradas!\n\n" +
      "Vá em Projeto → Propriedades do Projeto → Propriedades de Script\n" +
      "e adicione: CLIENT_ID, CLIENT_SECRET e REFRESH_TOKEN."
    );
  }

  const url = "https://oauth2.googleapis.com/token";

  const response = UrlFetchApp.fetch(url, {
    method: "post",
    contentType: "application/x-www-form-urlencoded",
    payload: {
      client_id:     clientId,
      client_secret: clientSecret,
      refresh_token: refreshToken,
      grant_type:    "refresh_token"
    },
    muteHttpExceptions: true
  });

  const data = JSON.parse(response.getContentText());

  if (!data.access_token) {
    throw new Error("Falha ao obter access token: " + JSON.stringify(data));
  }

  return data.access_token;
}


// ═══════════════════════════════════════════════════════════════════════════════
//  BUSCA DE AVALIAÇÕES — Paginação automática
// ═══════════════════════════════════════════════════════════════════════════════

function buscarTodasAvaliacoes(accessToken) {
  const accId = ACCOUNT_ID.split("/").pop();
  const locId = LOCATION_ID.split("/").pop();
  const baseUrl = `https://mybusiness.googleapis.com/v4/accounts/${accId}/locations/${locId}/reviews`;

  const headers = {
    "Authorization": "Bearer " + accessToken,
    "Content-Type":  "application/json"
  };

  let todasAvaliacoes = [];
  let nextPageToken   = null;
  let pagina          = 0;
  let totalGoogle     = 0;
  let notaMedia       = 0;

  do {
    pagina++;

    let urlPagina = `${baseUrl}?pageSize=${PAGE_SIZE}&orderBy=updateTime%20desc`;
    if (nextPageToken) {
      urlPagina += "&pageToken=" + encodeURIComponent(nextPageToken);
    }

    const response = UrlFetchApp.fetch(urlPagina, {
      headers: headers,
      muteHttpExceptions: true
    });

    if (response.getResponseCode() !== 200) {
      throw new Error(
        `Erro na API (página ${pagina}): HTTP ${response.getResponseCode()}\n` +
        response.getContentText().substring(0, 300)
      );
    }

    const data = JSON.parse(response.getContentText());
    const reviews = data.reviews || [];

    if (pagina === 1) {
      totalGoogle = data.totalReviewCount || 0;
      notaMedia   = data.averageRating    || 0;
      Logger.log(`   Total no Google: ${totalGoogle} | Nota média: ${notaMedia.toFixed(2)}`);
    }

    todasAvaliacoes = todasAvaliacoes.concat(reviews);
    Logger.log(`   Página ${pagina}: ${reviews.length} avaliações (total: ${todasAvaliacoes.length}/${totalGoogle})`);

    nextPageToken = data.nextPageToken || null;

    if (nextPageToken) Utilities.sleep(300);

  } while (nextPageToken);

  return {
    avaliacoes: todasAvaliacoes,
    totalGoogle: totalGoogle,
    notaMedia:   notaMedia
  };
}


// ═══════════════════════════════════════════════════════════════════════════════
//  ESCRITA NA PLANILHA — Aba "Avaliações"
// ═══════════════════════════════════════════════════════════════════════════════

function escreverAbaAvaliacoes(ss, avaliacoes) {
  let aba = ss.getSheetByName(ABA_AVALIACOES);
  if (!aba) {
    aba = ss.insertSheet(ABA_AVALIACOES);
  } else {
    aba.clearContents();
    aba.clearFormats();
  }

  // ── Cabeçalho ──────────────────────────────────────────────────────────────
  const cabecalhos = [
    "ID da Avaliação",
    "Autor",
    "Anônimo",
    "Nota (1-5)",
    "Estrelas",
    "Comentário",
    "Data de Criação",
    "Última Atualização",
    "Resposta do Proprietário",
    "Data da Resposta",
    "Tem Mídia"
  ];

  aba.getRange(1, 1, 1, cabecalhos.length).setValues([cabecalhos]);

  const rangeCab = aba.getRange(1, 1, 1, cabecalhos.length);
  rangeCab.setBackground(COR_CABECALHO)
          .setFontColor("#FFFFFF")
          .setFontWeight("bold")
          .setFontSize(10)
          .setHorizontalAlignment("center")
          .setVerticalAlignment("middle")
          .setWrap(true);
  aba.setRowHeight(1, 30);
  aba.setFrozenRows(1);

  // ── Dados ──────────────────────────────────────────────────────────────────
  const linhas = [];

  for (const review of avaliacoes) {
    const reviewer = review.reviewer || {};
    const reply    = review.reviewReply || {};
    const starRaw  = review.starRating || "STAR_RATING_UNSPECIFIED";
    const nota     = STAR_MAP[starRaw] || 0;
    const estrelas = nota > 0 ? "⭐".repeat(nota) : "—";

    linhas.push([
      review.reviewId             || "",
      reviewer.displayName        || "Anônimo",
      reviewer.isAnonymous        ? "Sim" : "Não",
      nota,
      estrelas,
      review.comment              || "",
      formatarData(review.createTime),
      formatarData(review.updateTime),
      reply.comment               || "",
      formatarData(reply.updateTime),
      (review.reviewMediaItems && review.reviewMediaItems.length > 0) ? "✓" : ""
    ]);
  }

  if (linhas.length > 0) {
    aba.getRange(2, 1, linhas.length, cabecalhos.length).setValues(linhas);
  }

  // ── Formatação das linhas ──────────────────────────────────────────────────
  for (let i = 0; i < linhas.length; i++) {
    const linha  = i + 2;
    const nota   = linhas[i][3];
    const range  = aba.getRange(linha, 1, 1, cabecalhos.length);

    let corFundo;
    if (nota === 5)      corFundo = COR_VERDE;
    else if (nota === 1) corFundo = COR_VERMELHO;
    else                 corFundo = (i % 2 === 0) ? COR_LINHA_PAR : COR_LINHA_IMPAR;

    range.setBackground(corFundo)
         .setFontSize(9)
         .setVerticalAlignment("top")
         .setWrap(true);

    aba.setRowHeight(linha, 60);
  }

  [3, 4, 5, 11].forEach(col => {
    if (linhas.length > 0) {
      aba.getRange(2, col, linhas.length, 1).setHorizontalAlignment("center");
    }
  });

  // ── Larguras das colunas ───────────────────────────────────────────────────
  const larguras = [160, 140, 70, 70, 100, 350, 150, 150, 300, 150, 80];
  larguras.forEach((w, i) => aba.setColumnWidth(i + 1, w));

  Logger.log(`✅ Aba "${ABA_AVALIACOES}" preenchida com ${linhas.length} linhas.`);
}


// ═══════════════════════════════════════════════════════════════════════════════
//  ESCRITA NA PLANILHA — Aba "Resumo"
// ═══════════════════════════════════════════════════════════════════════════════

function escreverAbaResumo(ss, avaliacoes, totalGoogle, notaMedia) {
  let aba = ss.getSheetByName(ABA_RESUMO);
  if (!aba) {
    aba = ss.insertSheet(ABA_RESUMO, 0);
  } else {
    aba.clearContents();
    aba.clearFormats();
  }

  const total       = avaliacoes.length;
  const comResposta = avaliacoes.filter(r => r.reviewReply && r.reviewReply.comment).length;
  const semResposta = total - comResposta;
  const taxaResp    = total > 0 ? (comResposta / total * 100).toFixed(1) : "0";

  const dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0};
  for (const r of avaliacoes) {
    const nota = STAR_MAP[r.starRating || "STAR_RATING_UNSPECIFIED"] || 0;
    if (nota > 0) dist[nota]++;
  }

  // ── Título ─────────────────────────────────────────────────────────────────
  aba.getRange("A1:B1").merge()
     .setValue("Embaixada Carioca — Avaliações Google")
     .setBackground(COR_CABECALHO)
     .setFontColor("#FFFFFF")
     .setFontWeight("bold")
     .setFontSize(14)
     .setHorizontalAlignment("center")
     .setVerticalAlignment("middle");
  aba.setRowHeight(1, 40);

  aba.getRange("A2:B2").merge()
     .setValue("Extração: " + new Date().toLocaleString("pt-BR"))
     .setBackground(COR_OURO)
     .setFontColor("#1A1A2E")
     .setFontWeight("bold")
     .setFontSize(10)
     .setHorizontalAlignment("center");
  aba.setRowHeight(2, 22);

  // ── Métricas ───────────────────────────────────────────────────────────────
  const metricas = [
    ["Total de Avaliações Coletadas",       total],
    ["Total no Google (oficial)",           totalGoogle],
    ["Nota Média",                          notaMedia.toFixed(2) + " ⭐"],
    ["Com Resposta do Proprietário",        `${comResposta} (${taxaResp}%)`],
    ["Sem Resposta",                        `${semResposta} (${(100 - parseFloat(taxaResp)).toFixed(1)}%)`],
    ["DISTRIBUIÇÃO POR ESTRELAS",           ""],
    ["⭐⭐⭐⭐⭐  (5 estrelas)",              `${dist[5]} (${(dist[5]/total*100).toFixed(1)}%)`],
    ["⭐⭐⭐⭐    (4 estrelas)",              `${dist[4]} (${(dist[4]/total*100).toFixed(1)}%)`],
    ["⭐⭐⭐      (3 estrelas)",              `${dist[3]} (${(dist[3]/total*100).toFixed(1)}%)`],
    ["⭐⭐        (2 estrelas)",              `${dist[2]} (${(dist[2]/total*100).toFixed(1)}%)`],
    ["⭐          (1 estrela)",              `${dist[1]} (${(dist[1]/total*100).toFixed(1)}%)`],
  ];

  for (let i = 0; i < metricas.length; i++) {
    const linha = i + 4;
    const [chave, valor] = metricas[i];

    if (chave === "DISTRIBUIÇÃO POR ESTRELAS") {
      aba.getRange(linha, 1, 1, 2).merge()
         .setValue(chave)
         .setBackground(COR_OURO)
         .setFontColor("#1A1A2E")
         .setFontWeight("bold")
         .setFontSize(11)
         .setHorizontalAlignment("center");
      aba.setRowHeight(linha, 28);
      continue;
    }

    const corFundo = (i % 2 === 0) ? COR_LINHA_PAR : COR_LINHA_IMPAR;

    aba.getRange(linha, 1)
       .setValue(chave)
       .setBackground(corFundo)
       .setFontWeight("bold")
       .setFontSize(10)
       .setVerticalAlignment("middle");

    aba.getRange(linha, 2)
       .setValue(valor)
       .setBackground(corFundo)
       .setFontSize(10)
       .setHorizontalAlignment("center")
       .setVerticalAlignment("middle");

    aba.setRowHeight(linha, 26);
  }

  aba.setColumnWidth(1, 280);
  aba.setColumnWidth(2, 160);

  Logger.log(`✅ Aba "${ABA_RESUMO}" preenchida.`);
}


// ═══════════════════════════════════════════════════════════════════════════════
//  UTILITÁRIOS
// ═══════════════════════════════════════════════════════════════════════════════

function formatarData(timestamp) {
  if (!timestamp) return "";
  try {
    const dt = new Date(timestamp);
    return Utilities.formatDate(dt, "America/Sao_Paulo", "dd/MM/yyyy HH:mm");
  } catch (e) {
    return timestamp;
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  MENU PERSONALIZADO — Aparece automaticamente ao abrir a planilha
// ═══════════════════════════════════════════════════════════════════════════════

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("🗺️ Avaliações GBP")
    .addItem("▶ Importar todas as avaliações", "importarAvaliacoes")
    .addSeparator()
    .addItem("⚙️ Configurar credenciais", "configurarCredenciais")
    .addToUi();
}

function configurarCredenciais() {
  const ui = SpreadsheetApp.getUi();
  ui.alert(
    "⚙️ Como configurar as credenciais",
    "1. No menu do Apps Script, clique em ⚙️ Configurações do Projeto\n" +
    "2. Role até 'Propriedades de Script'\n" +
    "3. Adicione as seguintes chaves:\n\n" +
    "   CLIENT_ID      → (seu client_id)\n" +
    "   CLIENT_SECRET  → (seu client_secret)\n" +
    "   REFRESH_TOKEN  → (seu refresh_token)\n\n" +
    "4. Salve e execute 'Importar todas as avaliações'",
    ui.ButtonSet.OK
  );
}
