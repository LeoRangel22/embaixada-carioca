// ═══════════════════════════════════════════════════════════════════════════════
//  Google Apps Script — Avaliações GBP | Versão Final Unificada
//  Embaixada Carioca / Cantina do Mam
//
//  DOIS MODOS DE ATUALIZAÇÃO:
//
//  1. INCREMENTAL (a cada 5 min)
//     → Busca as últimas 50 avaliações
//     → Insere apenas as novas (deduplicação por review_id)
//     → Captura avaliações novas com agilidade
//
//  2. SINCRONIZAÇÃO COMPLETA (1x por dia ou 1x por semana)
//     → Reimporta todas as avaliações com paginação
//     → Atualiza respostas do proprietário em avaliações antigas
//     → Detecta avaliações removidas do Google
//     → Recalcula o Resumo com dados 100% precisos
//
// ═══════════════════════════════════════════════════════════════════════════════

// ─── CONFIGURAÇÕES ────────────────────────────────────────────────────────────

const ACCOUNT_ID  = "accounts/106083628368200012478";

// Embaixada Carioca:
const LOCATION_ID = "locations/18008728615502069543";

// Cantina do Mam (troque a linha acima por esta):
// const LOCATION_ID = "locations/7552566478256082910";

const ABA_AVALIACOES = "Avaliações";
const ABA_RESUMO     = "Resumo";
const ABA_LOG        = "Log de Execuções";

const PAGE_SIZE = 50;

// ─── CORES ────────────────────────────────────────────────────────────────────

const COR_CABECALHO   = "#1A1A2E";
const COR_OURO        = "#C9A84C";
const COR_VERDE       = "#D4EDDA";
const COR_VERMELHO    = "#F8D7DA";
const COR_LINHA_PAR   = "#F5F0E8";
const COR_LINHA_IMPAR = "#FFFFFF";
const COR_NOVA        = "#E8F4FD";   // Azul claro — avaliação nova (incremental)
const COR_ATUALIZADA  = "#FFF3CD";   // Amarelo claro — resposta atualizada (sync completa)

const STAR_MAP = {
  "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5,
  "STAR_RATING_UNSPECIFIED": 0
};

// Índice das colunas (base 1)
const COL = {
  ID: 1, AUTOR: 2, ANONIMO: 3, NOTA: 4, ESTRELAS: 5,
  COMENTARIO: 6, DATA_CRIACAO: 7, DATA_ATUALIZACAO: 8,
  RESPOSTA: 9, DATA_RESPOSTA: 10, MIDIA: 11
};
const NUM_COLUNAS = 11;


// ═══════════════════════════════════════════════════════════════════════════════
//  MODO 1 — ATUALIZAÇÃO INCREMENTAL
//  Gatilho: a cada 5 minutos
//  Objetivo: capturar avaliações novas rapidamente
// ═══════════════════════════════════════════════════════════════════════════════

function atualizarIncremental() {
  const inicio = new Date();
  let novasInseridas = 0;

  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    garantirAbas(ss);

    const token = obterAccessToken();

    // Busca apenas 1 página (50 avaliações mais recentes)
    const resultado = buscarPagina(token, PAGE_SIZE, null);
    const avaliacoesApi = resultado.avaliacoes;
    const totalGoogle   = resultado.totalGoogle;
    const notaMedia     = resultado.notaMedia;

    if (avaliacoesApi.length === 0) {
      registrarLog(ss, inicio, 0, 0, totalGoogle, "incremental", "Nenhuma avaliação retornada");
      return;
    }

    // Deduplicação: carregar IDs existentes
    const idsExistentes = carregarIdsExistentes(ss);
    const novas = avaliacoesApi.filter(r => !idsExistentes.has(r.reviewId));

    if (novas.length > 0) {
      novasInseridas = inserirNoTopo(ss, novas, COR_NOVA);
    }

    atualizarCelulasResumo(ss, totalGoogle, notaMedia);
    registrarLog(ss, inicio, novasInseridas, 0, totalGoogle, "incremental",
      novas.length > 0 ? `${novasInseridas} nova(s)` : "Sem novidades");

  } catch (e) {
    Logger.log("❌ Incremental: " + e.message);
    try {
      registrarLog(SpreadsheetApp.getActiveSpreadsheet(), inicio, 0, 0, 0, "incremental", "ERRO: " + e.message);
    } catch (_) {}
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  MODO 2 — SINCRONIZAÇÃO COMPLETA
//  Gatilho: 1x por dia (padrão) ou 1x por semana
//  Objetivo: atualizar respostas, detectar remoções, recalcular resumo
// ═══════════════════════════════════════════════════════════════════════════════

function sincronizarCompleto() {
  const inicio = new Date();
  let novasInseridas = 0;
  let atualizadas = 0;

  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    garantirAbas(ss);

    const token = obterAccessToken();

    Logger.log("🔄 Sincronização completa iniciada...");

    // 1. Buscar TODAS as avaliações da API com paginação
    const todasApi = buscarTodasAvaliacoes(token);
    const totalGoogle = todasApi.totalGoogle;
    const notaMedia   = todasApi.notaMedia;
    const avaliacoesApi = todasApi.avaliacoes;

    Logger.log(`   API retornou: ${avaliacoesApi.length} avaliações`);

    // 2. Carregar mapa de avaliações existentes na planilha (id → número da linha)
    const mapaExistentes = carregarMapaExistentes(ss);

    Logger.log(`   Planilha tem: ${Object.keys(mapaExistentes).length} avaliações`);

    // 3. Separar novas vs. já existentes
    const novas     = avaliacoesApi.filter(r => !mapaExistentes[r.reviewId]);
    const existentes = avaliacoesApi.filter(r =>  mapaExistentes[r.reviewId]);

    // 4. Inserir novas no topo
    if (novas.length > 0) {
      novasInseridas = inserirNoTopo(ss, novas, COR_NOVA);
      Logger.log(`   Novas inseridas: ${novasInseridas}`);
    }

    // 5. Atualizar avaliações existentes (resposta do proprietário pode ter mudado)
    if (existentes.length > 0) {
      // Recarregar mapa após inserção das novas (linhas mudaram)
      const mapaAtualizado = carregarMapaExistentes(ss);
      atualizadas = atualizarRespostas(ss, existentes, mapaAtualizado);
      Logger.log(`   Respostas atualizadas: ${atualizadas}`);
    }

    // 6. Recalcular e reescrever o Resumo completo
    reescreverResumo(ss, avaliacoesApi, totalGoogle, notaMedia);

    registrarLog(ss, inicio, novasInseridas, atualizadas, totalGoogle, "completa",
      `${novasInseridas} nova(s), ${atualizadas} resposta(s) atualizada(s)`);

    Logger.log(`✅ Sincronização completa: ${novasInseridas} novas, ${atualizadas} atualizadas.`);

  } catch (e) {
    Logger.log("❌ Sincronização completa: " + e.message);
    try {
      registrarLog(SpreadsheetApp.getActiveSpreadsheet(), inicio, 0, 0, 0, "completa", "ERRO: " + e.message);
    } catch (_) {}
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  ATUALIZAÇÃO DE RESPOSTAS — Detecta mudanças em avaliações existentes
// ═══════════════════════════════════════════════════════════════════════════════

function atualizarRespostas(ss, avaliacoesApi, mapaExistentes) {
  const aba = ss.getSheetByName(ABA_AVALIACOES);
  let atualizadas = 0;

  for (const review of avaliacoesApi) {
    const linhaAtual = mapaExistentes[review.reviewId];
    if (!linhaAtual) continue;

    const reply = review.reviewReply || {};
    const novaResposta   = reply.comment || "";
    const novaDataResp   = formatarData(reply.updateTime);
    const novaDataUpdate = formatarData(review.updateTime);

    // Ler valores atuais da planilha
    const valoresAtuais = aba.getRange(linhaAtual, COL.DATA_ATUALIZACAO, 1, 3).getValues()[0];
    const dataUpdateAtual = valoresAtuais[0];
    const respostaAtual   = valoresAtuais[1];
    const dataRespAtual   = valoresAtuais[2];

    // Verificar se algo mudou
    const mudou = (novaResposta !== (respostaAtual || "")) ||
                  (novaDataResp !== (dataRespAtual || "")) ||
                  (novaDataUpdate !== (dataUpdateAtual || ""));

    if (mudou) {
      aba.getRange(linhaAtual, COL.DATA_ATUALIZACAO).setValue(novaDataUpdate);
      aba.getRange(linhaAtual, COL.RESPOSTA).setValue(novaResposta);
      aba.getRange(linhaAtual, COL.DATA_RESPOSTA).setValue(novaDataResp);

      // Destacar linha em amarelo para indicar que foi atualizada
      aba.getRange(linhaAtual, 1, 1, NUM_COLUNAS).setBackground(COR_ATUALIZADA);
      atualizadas++;
    }
  }

  return atualizadas;
}


// ═══════════════════════════════════════════════════════════════════════════════
//  AUTENTICAÇÃO
// ═══════════════════════════════════════════════════════════════════════════════

function obterAccessToken() {
  const props = PropertiesService.getScriptProperties();
  const clientId     = props.getProperty("CLIENT_ID");
  const clientSecret = props.getProperty("CLIENT_SECRET");
  const refreshToken = props.getProperty("REFRESH_TOKEN");

  if (!clientId || !clientSecret || !refreshToken) {
    throw new Error(
      "Credenciais não configuradas!\n" +
      "Vá em ⚙️ Configurações do Projeto → Propriedades de Script\n" +
      "e adicione: CLIENT_ID, CLIENT_SECRET e REFRESH_TOKEN."
    );
  }

  const response = UrlFetchApp.fetch("https://oauth2.googleapis.com/token", {
    method: "post",
    contentType: "application/x-www-form-urlencoded",
    payload: {
      client_id: clientId, client_secret: clientSecret,
      refresh_token: refreshToken, grant_type: "refresh_token"
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
//  CHAMADAS DE API
// ═══════════════════════════════════════════════════════════════════════════════

function buscarPagina(token, pageSize, pageToken) {
  const accId = ACCOUNT_ID.split("/").pop();
  const locId = LOCATION_ID.split("/").pop();
  let url = `https://mybusiness.googleapis.com/v4/accounts/${accId}/locations/${locId}/reviews` +
            `?pageSize=${pageSize}&orderBy=updateTime%20desc`;
  if (pageToken) url += "&pageToken=" + encodeURIComponent(pageToken);

  const response = UrlFetchApp.fetch(url, {
    headers: { "Authorization": "Bearer " + token },
    muteHttpExceptions: true
  });

  if (response.getResponseCode() !== 200) {
    throw new Error(`Erro API: HTTP ${response.getResponseCode()} — ${response.getContentText().substring(0, 200)}`);
  }

  const data = JSON.parse(response.getContentText());
  return {
    avaliacoes:    data.reviews          || [],
    totalGoogle:   data.totalReviewCount || 0,
    notaMedia:     data.averageRating    || 0,
    nextPageToken: data.nextPageToken    || null
  };
}

function buscarTodasAvaliacoes(token) {
  let todas = [];
  let nextPageToken = null;
  let pagina = 0;
  let totalGoogle = 0;
  let notaMedia = 0;

  do {
    pagina++;
    const resultado = buscarPagina(token, PAGE_SIZE, nextPageToken);
    if (pagina === 1) {
      totalGoogle = resultado.totalGoogle;
      notaMedia   = resultado.notaMedia;
      Logger.log(`   Total Google: ${totalGoogle} | Nota: ${notaMedia.toFixed(2)}`);
    }
    todas = todas.concat(resultado.avaliacoes);
    Logger.log(`   Página ${pagina}: ${resultado.avaliacoes.length} (acumulado: ${todas.length})`);
    nextPageToken = resultado.nextPageToken;
    if (nextPageToken) Utilities.sleep(300);
  } while (nextPageToken);

  return { avaliacoes: todas, totalGoogle, notaMedia };
}


// ═══════════════════════════════════════════════════════════════════════════════
//  LEITURA DA PLANILHA
// ═══════════════════════════════════════════════════════════════════════════════

function carregarIdsExistentes(ss) {
  const aba = ss.getSheetByName(ABA_AVALIACOES);
  if (!aba || aba.getLastRow() < 2) return new Set();
  const ids = aba.getRange(2, COL.ID, aba.getLastRow() - 1, 1).getValues();
  return new Set(ids.map(r => r[0]).filter(id => id !== ""));
}

function carregarMapaExistentes(ss) {
  // Retorna { reviewId: numeroLinha }
  const aba = ss.getSheetByName(ABA_AVALIACOES);
  if (!aba || aba.getLastRow() < 2) return {};
  const ids = aba.getRange(2, COL.ID, aba.getLastRow() - 1, 1).getValues();
  const mapa = {};
  ids.forEach((row, i) => {
    if (row[0]) mapa[row[0]] = i + 2; // +2 porque começa na linha 2
  });
  return mapa;
}


// ═══════════════════════════════════════════════════════════════════════════════
//  ESCRITA NA PLANILHA
// ═══════════════════════════════════════════════════════════════════════════════

function inserirNoTopo(ss, avaliacoes, corDestaque) {
  const aba = ss.getSheetByName(ABA_AVALIACOES);

  aba.insertRowsAfter(1, avaliacoes.length);

  const linhas = avaliacoes.map(review => {
    const reviewer = review.reviewer    || {};
    const reply    = review.reviewReply || {};
    const starRaw  = review.starRating  || "STAR_RATING_UNSPECIFIED";
    const nota     = STAR_MAP[starRaw]  || 0;
    return [
      review.reviewId              || "",
      reviewer.displayName         || "Anônimo",
      reviewer.isAnonymous         ? "Sim" : "Não",
      nota,
      nota > 0 ? "⭐".repeat(nota) : "—",
      review.comment               || "",
      formatarData(review.createTime),
      formatarData(review.updateTime),
      reply.comment                || "",
      formatarData(reply.updateTime),
      (review.reviewMediaItems && review.reviewMediaItems.length > 0) ? "✓" : ""
    ];
  });

  aba.getRange(2, 1, linhas.length, NUM_COLUNAS).setValues(linhas);

  for (let i = 0; i < linhas.length; i++) {
    const linha = i + 2;
    const nota  = linhas[i][COL.NOTA - 1];
    let cor = corDestaque;
    if (nota === 5)      cor = COR_VERDE;
    else if (nota === 1) cor = COR_VERMELHO;

    aba.getRange(linha, 1, 1, NUM_COLUNAS)
       .setBackground(cor).setFontSize(9)
       .setVerticalAlignment("top").setWrap(true);
    aba.setRowHeight(linha, 60);
  }

  [COL.ANONIMO, COL.NOTA, COL.ESTRELAS, COL.MIDIA].forEach(col => {
    aba.getRange(2, col, linhas.length, 1).setHorizontalAlignment("center");
  });

  return linhas.length;
}

function atualizarCelulasResumo(ss, totalGoogle, notaMedia) {
  const aba = ss.getSheetByName(ABA_RESUMO);
  if (!aba) return;
  aba.getRange("A2:B2").merge()
     .setValue("Última atualização: " + new Date().toLocaleString("pt-BR"))
     .setBackground(COR_OURO).setFontColor("#1A1A2E")
     .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
  const abaAv = ss.getSheetByName(ABA_AVALIACOES);
  const totalLocal = abaAv ? Math.max(0, abaAv.getLastRow() - 1) : 0;
  aba.getRange("B4").setValue(totalLocal);
  aba.getRange("B5").setValue(totalGoogle);
  aba.getRange("B6").setValue(notaMedia.toFixed(2) + " ⭐");
}

function reescreverResumo(ss, avaliacoes, totalGoogle, notaMedia) {
  let aba = ss.getSheetByName(ABA_RESUMO);
  if (!aba) aba = ss.insertSheet(ABA_RESUMO, 0);
  else { aba.clearContents(); aba.clearFormats(); }

  const total       = avaliacoes.length;
  const comResposta = avaliacoes.filter(r => r.reviewReply && r.reviewReply.comment).length;
  const semResposta = total - comResposta;
  const taxaResp    = total > 0 ? (comResposta / total * 100).toFixed(1) : "0";

  const dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0};
  avaliacoes.forEach(r => {
    const n = STAR_MAP[r.starRating || "STAR_RATING_UNSPECIFIED"] || 0;
    if (n > 0) dist[n]++;
  });

  function hdr(cell, bg, sz, color) {
    cell.setFont && cell.setFont(null);
    cell.setBackground(bg || COR_CABECALHO)
        .setFontColor(color || "#FFFFFF")
        .setFontWeight("bold").setFontSize(sz || 11)
        .setHorizontalAlignment("center").setVerticalAlignment("middle");
  }
  function dat(cell, bold, center, bg) {
    cell.setFontWeight(bold ? "bold" : "normal").setFontSize(10)
        .setBackground(bg || COR_LINHA_IMPAR)
        .setHorizontalAlignment(center ? "center" : "left")
        .setVerticalAlignment("middle");
  }

  aba.getRange("A1:B1").merge().setValue("Avaliações Google — Resumo Geral");
  hdr(aba.getRange("A1"), COR_CABECALHO, 14);
  aba.setRowHeight(1, 40);

  aba.getRange("A2:B2").merge()
     .setValue("Última sincronização completa: " + new Date().toLocaleString("pt-BR"));
  hdr(aba.getRange("A2"), COR_OURO, 10, "#1A1A2E");
  aba.setRowHeight(2, 22);

  const metricas = [
    ["Total de Avaliações (local)",         total],
    ["Total no Google (oficial)",           totalGoogle],
    ["Nota Média",                          notaMedia.toFixed(2) + " ⭐"],
    ["Com Resposta do Proprietário",        `${comResposta} (${taxaResp}%)`],
    ["Sem Resposta",                        `${semResposta} (${(100 - parseFloat(taxaResp)).toFixed(1)}%)`],
    ["— DISTRIBUIÇÃO POR ESTRELAS —",       ""],
    ["⭐⭐⭐⭐⭐  (5 estrelas)",              `${dist[5]} (${(dist[5]/total*100).toFixed(1)}%)`],
    ["⭐⭐⭐⭐    (4 estrelas)",              `${dist[4]} (${(dist[4]/total*100).toFixed(1)}%)`],
    ["⭐⭐⭐      (3 estrelas)",              `${dist[3]} (${(dist[3]/total*100).toFixed(1)}%)`],
    ["⭐⭐        (2 estrelas)",              `${dist[2]} (${(dist[2]/total*100).toFixed(1)}%)`],
    ["⭐          (1 estrela)",              `${dist[1]} (${(dist[1]/total*100).toFixed(1)}%)`],
    ["— LEGENDA DE CORES —",                ""],
    ["Azul claro",                          "Avaliação nova (incremental)"],
    ["Amarelo claro",                       "Resposta atualizada (sync completa)"],
    ["Verde claro",                         "5 estrelas"],
    ["Vermelho claro",                      "1 estrela"],
  ];

  for (let i = 0; i < metricas.length; i++) {
    const linha = i + 4;
    const [chave, valor] = metricas[i];

    if (chave.startsWith("—")) {
      aba.getRange(linha, 1, 1, 2).merge().setValue(chave.replace(/—/g, "").trim());
      hdr(aba.getRange(linha, 1), COR_OURO, 11, "#1A1A2E");
      aba.setRowHeight(linha, 28);
      continue;
    }

    const bg = (i % 2 === 0) ? COR_LINHA_PAR : COR_LINHA_IMPAR;
    dat(aba.getRange(linha, 1), true, false, bg);
    dat(aba.getRange(linha, 2), false, true, bg);
    aba.getRange(linha, 1).setValue(chave);
    aba.getRange(linha, 2).setValue(valor);

    // Cor da legenda
    if (chave === "Azul claro")     aba.getRange(linha, 2).setBackground(COR_NOVA);
    if (chave === "Amarelo claro")  aba.getRange(linha, 2).setBackground(COR_ATUALIZADA);
    if (chave === "Verde claro")    aba.getRange(linha, 2).setBackground(COR_VERDE);
    if (chave === "Vermelho claro") aba.getRange(linha, 2).setBackground(COR_VERMELHO);

    aba.setRowHeight(linha, 26);
  }

  aba.setColumnWidth(1, 300);
  aba.setColumnWidth(2, 180);
}


// ═══════════════════════════════════════════════════════════════════════════════
//  LOG DE EXECUÇÕES
// ═══════════════════════════════════════════════════════════════════════════════

function registrarLog(ss, inicio, novas, atualizadas, totalGoogle, tipo, observacao) {
  const aba = ss.getSheetByName(ABA_LOG);
  if (!aba) return;
  const duracao = ((new Date() - inicio) / 1000).toFixed(1);
  aba.insertRowAfter(1);
  const linha = aba.getRange(2, 1, 1, 7);
  linha.setValues([[
    new Date().toLocaleString("pt-BR"),
    tipo === "incremental" ? "⚡ Incremental" : "🔄 Completa",
    novas,
    atualizadas,
    totalGoogle,
    duracao + "s",
    observacao
  ]]);
  const cor = tipo === "incremental" ? COR_NOVA : COR_ATUALIZADA;
  linha.setBackground(cor).setFontSize(9);
  if (aba.getLastRow() > 501) aba.deleteRow(502);
}


// ═══════════════════════════════════════════════════════════════════════════════
//  CRIAÇÃO DAS ABAS
// ═══════════════════════════════════════════════════════════════════════════════

function garantirAbas(ss) {
  if (!ss.getSheetByName(ABA_AVALIACOES)) {
    const aba = ss.insertSheet(ABA_AVALIACOES);
    const cabs = ["ID da Avaliação","Autor","Anônimo","Nota (1-5)","Estrelas",
                  "Comentário","Data de Criação","Última Atualização",
                  "Resposta do Proprietário","Data da Resposta","Tem Mídia"];
    aba.getRange(1, 1, 1, cabs.length).setValues([cabs])
       .setBackground(COR_CABECALHO).setFontColor("#FFFFFF")
       .setFontWeight("bold").setFontSize(10)
       .setHorizontalAlignment("center").setVerticalAlignment("middle");
    aba.setRowHeight(1, 30);
    aba.setFrozenRows(1);
    [160,140,70,70,100,350,150,150,300,150,80].forEach((w,i) => aba.setColumnWidth(i+1, w));
  }

  if (!ss.getSheetByName(ABA_RESUMO)) {
    reescreverResumo(ss, [], 0, 0);
  }

  if (!ss.getSheetByName(ABA_LOG)) {
    const aba = ss.insertSheet(ABA_LOG);
    const cabs = ["Data/Hora","Tipo","Novas","Respostas Atualizadas","Total Google","Duração","Observação"];
    aba.getRange(1, 1, 1, cabs.length).setValues([cabs])
       .setBackground(COR_CABECALHO).setFontColor("#FFFFFF")
       .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
    aba.setFrozenRows(1);
    [160,130,70,160,120,80,300].forEach((w,i) => aba.setColumnWidth(i+1, w));
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  UTILITÁRIOS
// ═══════════════════════════════════════════════════════════════════════════════

function formatarData(timestamp) {
  if (!timestamp) return "";
  try {
    return Utilities.formatDate(new Date(timestamp), "America/Sao_Paulo", "dd/MM/yyyy HH:mm");
  } catch (e) { return timestamp; }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  CONFIGURAÇÃO DOS GATILHOS AUTOMÁTICOS
// ═══════════════════════════════════════════════════════════════════════════════

function ativarTodosOsGatilhos() {
  // Remove todos os gatilhos existentes
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));

  // Gatilho 1: Incremental a cada 5 minutos
  ScriptApp.newTrigger("atualizarIncremental")
    .timeBased().everyMinutes(5).create();

  // Gatilho 2: Sincronização completa diária às 3h da manhã
  ScriptApp.newTrigger("sincronizarCompleto")
    .timeBased().everyDays(1).atHour(3)
    .inTimezone("America/Sao_Paulo").create();

  SpreadsheetApp.getUi().alert(
    "✅ Automação Completa Ativada!",
    "⚡ Incremental: a cada 5 minutos\n" +
    "   → Captura avaliações novas rapidamente\n\n" +
    "🔄 Sincronização completa: todos os dias às 3h\n" +
    "   → Atualiza respostas do proprietário\n\n" +
    "Novas avaliações aparecem em azul.\n" +
    "Respostas atualizadas aparecem em amarelo.",
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

function ativarSomenteIncremental() {
  removerGatilho("atualizarIncremental");
  ScriptApp.newTrigger("atualizarIncremental")
    .timeBased().everyMinutes(5).create();
  SpreadsheetApp.getUi().alert("✅ Incremental ativado (a cada 5 min).");
}

function ativarSomenteCompleto_Diario() {
  removerGatilho("sincronizarCompleto");
  ScriptApp.newTrigger("sincronizarCompleto")
    .timeBased().everyDays(1).atHour(3)
    .inTimezone("America/Sao_Paulo").create();
  SpreadsheetApp.getUi().alert("✅ Sincronização completa diária ativada (todos os dias às 3h).");
}

function ativarSomenteCompleto_Semanal() {
  removerGatilho("sincronizarCompleto");
  ScriptApp.newTrigger("sincronizarCompleto")
    .timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(3)
    .inTimezone("America/Sao_Paulo").create();
  SpreadsheetApp.getUi().alert("✅ Sincronização completa semanal ativada (toda segunda às 3h).");
}

function desativarTudo() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  SpreadsheetApp.getUi().alert("⛔ Todos os gatilhos foram desativados.");
}

function removerGatilho(nomeFuncao) {
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === nomeFuncao) ScriptApp.deleteTrigger(t);
  });
}


// ═══════════════════════════════════════════════════════════════════════════════
//  MENU PERSONALIZADO
// ═══════════════════════════════════════════════════════════════════════════════

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("🗺️ Avaliações GBP")
    .addItem("▶ Atualizar agora (incremental)", "atualizarIncremental")
    .addItem("🔄 Sincronizar tudo agora", "sincronizarCompleto")
    .addSeparator()
    .addSubMenu(SpreadsheetApp.getUi().createMenu("⏱️ Configurar automação")
      .addItem("✅ Ativar tudo (5 min + diário às 3h)", "ativarTodosOsGatilhos")
      .addSeparator()
      .addItem("⚡ Apenas incremental (5 min)", "ativarSomenteIncremental")
      .addItem("🔄 Apenas sync completa — diária (3h)", "ativarSomenteCompleto_Diario")
      .addItem("🔄 Apenas sync completa — semanal (seg 3h)", "ativarSomenteCompleto_Semanal")
      .addSeparator()
      .addItem("⛔ Desativar tudo", "desativarTudo"))
    .addSeparator()
    .addItem("⚙️ Configurar credenciais", "configurarCredenciais")
    .addToUi();
}

function configurarCredenciais() {
  SpreadsheetApp.getUi().alert(
    "⚙️ Como configurar as credenciais",
    "1. No menu do Apps Script, clique em ⚙️ Configurações do Projeto\n" +
    "2. Role até 'Propriedades de Script'\n" +
    "3. Adicione as seguintes chaves:\n\n" +
    "   CLIENT_ID      → (seu client_id)\n" +
    "   CLIENT_SECRET  → (seu client_secret)\n" +
    "   REFRESH_TOKEN  → (seu refresh_token)\n\n" +
    "4. Salve e use o menu '⏱️ Configurar automação'",
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}
