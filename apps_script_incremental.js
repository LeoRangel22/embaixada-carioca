// ═══════════════════════════════════════════════════════════════════════════════
//  Google Apps Script — Atualização Incremental de Avaliações GBP
//  Embaixada Carioca / Cantina do Mam
//
//  Estratégia: busca apenas as últimas 50 avaliações a cada execução,
//  compara com o que já existe na planilha pelo review_id,
//  e insere apenas as novas (sem duplicatas, sem reimportar tudo).
//
//  Frequência recomendada: a cada 5 minutos (mínimo do Apps Script)
//  Custo de API: 1 chamada por execução (50 avaliações por página)
// ═══════════════════════════════════════════════════════════════════════════════

// ─── CONFIGURAÇÕES — altere LOCATION_ID conforme o negócio ───────────────────

const ACCOUNT_ID  = "accounts/106083628368200012478";

// Embaixada Carioca:
const LOCATION_ID = "locations/18008728615502069543";

// Cantina do Mam (troque a linha acima por esta):
// const LOCATION_ID = "locations/7552566478256082910";

const ABA_AVALIACOES = "Avaliações";
const ABA_RESUMO     = "Resumo";
const ABA_LOG        = "Log de Execuções";

// Quantas avaliações buscar por execução (1 página = 50 = máximo da API)
const PAGE_SIZE = 50;

// ─── CORES ────────────────────────────────────────────────────────────────────

const COR_CABECALHO   = "#1A1A2E";
const COR_OURO        = "#C9A84C";
const COR_VERDE       = "#D4EDDA";
const COR_VERMELHO    = "#F8D7DA";
const COR_LINHA_PAR   = "#F5F0E8";
const COR_LINHA_IMPAR = "#FFFFFF";
const COR_NOVA        = "#E8F4FD";  // Azul claro — avaliações novas inseridas nesta execução

const STAR_MAP = {
  "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5,
  "STAR_RATING_UNSPECIFIED": 0
};


// ═══════════════════════════════════════════════════════════════════════════════
//  FUNÇÃO PRINCIPAL — Execute manualmente ou via gatilho automático
// ═══════════════════════════════════════════════════════════════════════════════

function atualizarAvaliacoes() {
  const inicio = new Date();
  let novasInseridas = 0;
  let atualizadas = 0;

  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();

    // 1. Garantir que as abas existam
    garantirAbas(ss);

    // 2. Obter access token
    const token = obterAccessToken();

    // 3. Buscar as últimas 50 avaliações da API (1 chamada apenas)
    const resultado = buscarUltimasAvaliacoes(token);
    const avaliacoesApi = resultado.avaliacoes;
    const totalGoogle   = resultado.totalGoogle;
    const notaMedia     = resultado.notaMedia;

    if (avaliacoesApi.length === 0) {
      registrarLog(ss, inicio, 0, 0, totalGoogle, "Nenhuma avaliação retornada pela API");
      return;
    }

    // 4. Carregar IDs já existentes na planilha para deduplicação
    const idsExistentes = carregarIdsExistentes(ss);

    // 5. Filtrar apenas as avaliações realmente novas
    const novas = avaliacoesApi.filter(r => !idsExistentes.has(r.reviewId));

    // 6. Inserir as novas no topo da aba (mais recentes primeiro)
    if (novas.length > 0) {
      novasInseridas = inserirNovasAvaliacoes(ss, novas);
    }

    // 7. Atualizar o Resumo com os totais atuais
    atualizarResumo(ss, totalGoogle, notaMedia, novasInseridas);

    // 8. Registrar no log
    registrarLog(ss, inicio, novasInseridas, atualizadas, totalGoogle,
      novas.length > 0 ? `${novasInseridas} nova(s) inserida(s)` : "Nenhuma avaliação nova");

    Logger.log(`✅ Concluído: ${novasInseridas} novas de ${avaliacoesApi.length} verificadas.`);

  } catch (e) {
    Logger.log("❌ Erro: " + e.message);
    try {
      const ss = SpreadsheetApp.getActiveSpreadsheet();
      registrarLog(ss, inicio, 0, 0, 0, "ERRO: " + e.message);
    } catch (_) {}
  }
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
      "Credenciais não configuradas! Vá em Configurações do Projeto → " +
      "Propriedades de Script e adicione: CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN."
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
//  BUSCA DAS ÚLTIMAS 50 AVALIAÇÕES (1 chamada de API)
// ═══════════════════════════════════════════════════════════════════════════════

function buscarUltimasAvaliacoes(accessToken) {
  const accId = ACCOUNT_ID.split("/").pop();
  const locId = LOCATION_ID.split("/").pop();
  const url = `https://mybusiness.googleapis.com/v4/accounts/${accId}/locations/${locId}/reviews` +
              `?pageSize=${PAGE_SIZE}&orderBy=updateTime%20desc`;

  const response = UrlFetchApp.fetch(url, {
    headers: { "Authorization": "Bearer " + accessToken },
    muteHttpExceptions: true
  });

  if (response.getResponseCode() !== 200) {
    throw new Error(`Erro na API: HTTP ${response.getResponseCode()} — ${response.getContentText().substring(0, 200)}`);
  }

  const data = JSON.parse(response.getContentText());
  return {
    avaliacoes:  data.reviews          || [],
    totalGoogle: data.totalReviewCount || 0,
    notaMedia:   data.averageRating    || 0
  };
}


// ═══════════════════════════════════════════════════════════════════════════════
//  DEDUPLICAÇÃO — Carrega todos os IDs já existentes na planilha
// ═══════════════════════════════════════════════════════════════════════════════

function carregarIdsExistentes(ss) {
  const aba = ss.getSheetByName(ABA_AVALIACOES);
  if (!aba || aba.getLastRow() < 2) return new Set();

  // Coluna 1 = ID da Avaliação
  const ids = aba.getRange(2, 1, aba.getLastRow() - 1, 1).getValues();
  return new Set(ids.map(row => row[0]).filter(id => id !== ""));
}


// ═══════════════════════════════════════════════════════════════════════════════
//  INSERÇÃO — Adiciona novas avaliações no TOPO da aba (mais recentes primeiro)
// ═══════════════════════════════════════════════════════════════════════════════

function inserirNovasAvaliacoes(ss, novas) {
  const aba = ss.getSheetByName(ABA_AVALIACOES);
  const numColunas = 11;

  // Inserir linhas logo abaixo do cabeçalho (linha 1)
  aba.insertRowsAfter(1, novas.length);

  const linhas = novas.map(review => {
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

  const range = aba.getRange(2, 1, linhas.length, numColunas);
  range.setValues(linhas);

  // Formatar as linhas novas com cor azul clara para destacar
  for (let i = 0; i < linhas.length; i++) {
    const linha = i + 2;
    const nota  = linhas[i][3];

    // Avaliações novas ficam em azul claro por padrão,
    // mas 5⭐ mantém verde e 1⭐ mantém vermelho
    let corFundo = COR_NOVA;
    if (nota === 5)      corFundo = COR_VERDE;
    else if (nota === 1) corFundo = COR_VERMELHO;

    aba.getRange(linha, 1, 1, numColunas)
       .setBackground(corFundo)
       .setFontSize(9)
       .setVerticalAlignment("top")
       .setWrap(true);

    aba.setRowHeight(linha, 60);
  }

  // Centralizar colunas: Anônimo, Nota, Estrelas, Tem Mídia
  [3, 4, 5, 11].forEach(col => {
    aba.getRange(2, col, linhas.length, 1).setHorizontalAlignment("center");
  });

  return linhas.length;
}


// ═══════════════════════════════════════════════════════════════════════════════
//  ATUALIZAÇÃO DO RESUMO
// ═══════════════════════════════════════════════════════════════════════════════

function atualizarResumo(ss, totalGoogle, notaMedia, novasInseridas) {
  const aba = ss.getSheetByName(ABA_RESUMO);
  if (!aba) return;

  // Atualizar apenas os campos dinâmicos: total, nota média e última atualização
  // Linha 2 = data da última atualização
  aba.getRange("A2:B2").merge()
     .setValue("Última atualização: " + new Date().toLocaleString("pt-BR"))
     .setBackground(COR_OURO)
     .setFontColor("#1A1A2E")
     .setFontWeight("bold")
     .setFontSize(10)
     .setHorizontalAlignment("center");

  // Linha 4 = Total de avaliações coletadas (conta as linhas da aba)
  const abaAv = ss.getSheetByName(ABA_AVALIACOES);
  const totalLocal = abaAv ? Math.max(0, abaAv.getLastRow() - 1) : 0;
  aba.getRange("B4").setValue(totalLocal);
  aba.getRange("B5").setValue(totalGoogle);
  aba.getRange("B6").setValue(notaMedia.toFixed(2) + " ⭐");
}


// ═══════════════════════════════════════════════════════════════════════════════
//  LOG DE EXECUÇÕES
// ═══════════════════════════════════════════════════════════════════════════════

function registrarLog(ss, inicio, novas, atualizadas, totalGoogle, observacao) {
  const aba = ss.getSheetByName(ABA_LOG);
  if (!aba) return;

  const duracao = ((new Date() - inicio) / 1000).toFixed(1);

  // Inserir nova linha no topo do log (abaixo do cabeçalho)
  aba.insertRowAfter(1);
  aba.getRange(2, 1, 1, 6).setValues([[
    new Date().toLocaleString("pt-BR"),
    novas,
    atualizadas,
    totalGoogle,
    duracao + "s",
    observacao
  ]]);

  // Manter apenas as últimas 500 execuções no log
  if (aba.getLastRow() > 501) {
    aba.deleteRow(502);
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  CRIAÇÃO DAS ABAS (se não existirem)
// ═══════════════════════════════════════════════════════════════════════════════

function garantirAbas(ss) {
  // Aba Avaliações
  if (!ss.getSheetByName(ABA_AVALIACOES)) {
    const aba = ss.insertSheet(ABA_AVALIACOES);
    const cabecalhos = [
      "ID da Avaliação", "Autor", "Anônimo", "Nota (1-5)", "Estrelas",
      "Comentário", "Data de Criação", "Última Atualização",
      "Resposta do Proprietário", "Data da Resposta", "Tem Mídia"
    ];
    aba.getRange(1, 1, 1, cabecalhos.length).setValues([cabecalhos]);
    const rangeCab = aba.getRange(1, 1, 1, cabecalhos.length);
    rangeCab.setBackground(COR_CABECALHO).setFontColor("#FFFFFF")
            .setFontWeight("bold").setFontSize(10)
            .setHorizontalAlignment("center").setVerticalAlignment("middle");
    aba.setRowHeight(1, 30);
    aba.setFrozenRows(1);
    const larguras = [160, 140, 70, 70, 100, 350, 150, 150, 300, 150, 80];
    larguras.forEach((w, i) => aba.setColumnWidth(i + 1, w));
  }

  // Aba Resumo
  if (!ss.getSheetByName(ABA_RESUMO)) {
    const aba = ss.insertSheet(ABA_RESUMO, 0);
    aba.getRange("A1:B1").merge()
       .setValue("Avaliações Google — Atualização Automática")
       .setBackground(COR_CABECALHO).setFontColor("#FFFFFF")
       .setFontWeight("bold").setFontSize(14).setHorizontalAlignment("center");
    aba.setRowHeight(1, 40);

    const metricas = [
      ["Total de Avaliações (local)", ""],
      ["Total no Google (oficial)",   ""],
      ["Nota Média",                  ""],
      ["Frequência de Atualização",   "A cada 5 minutos"],
      ["Última Avaliação Nova",       "—"],
    ];
    metricas.forEach(([k, v], i) => {
      const linha = i + 4;
      const bg = (i % 2 === 0) ? COR_LINHA_PAR : COR_LINHA_IMPAR;
      aba.getRange(linha, 1).setValue(k).setBackground(bg).setFontWeight("bold").setFontSize(10);
      aba.getRange(linha, 2).setValue(v).setBackground(bg).setFontSize(10).setHorizontalAlignment("center");
    });
    aba.setColumnWidth(1, 280);
    aba.setColumnWidth(2, 160);
  }

  // Aba Log
  if (!ss.getSheetByName(ABA_LOG)) {
    const aba = ss.insertSheet(ABA_LOG);
    const cabecalhos = ["Data/Hora", "Novas Inseridas", "Atualizadas", "Total Google", "Duração", "Observação"];
    aba.getRange(1, 1, 1, cabecalhos.length).setValues([cabecalhos]);
    aba.getRange(1, 1, 1, cabecalhos.length)
       .setBackground(COR_CABECALHO).setFontColor("#FFFFFF")
       .setFontWeight("bold").setFontSize(10).setHorizontalAlignment("center");
    aba.setFrozenRows(1);
    [160, 120, 100, 120, 80, 300].forEach((w, i) => aba.setColumnWidth(i + 1, w));
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  UTILITÁRIOS
// ═══════════════════════════════════════════════════════════════════════════════

function formatarData(timestamp) {
  if (!timestamp) return "";
  try {
    return Utilities.formatDate(new Date(timestamp), "America/Sao_Paulo", "dd/MM/yyyy HH:mm");
  } catch (e) {
    return timestamp;
  }
}


// ═══════════════════════════════════════════════════════════════════════════════
//  CONFIGURAÇÃO DO GATILHO AUTOMÁTICO (execute uma única vez)
// ═══════════════════════════════════════════════════════════════════════════════

function ativarAtualizacaoAutomatica() {
  // Remove gatilhos anteriores para evitar duplicatas
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === "atualizarAvaliacoes") {
      ScriptApp.deleteTrigger(t);
    }
  });

  // Cria gatilho a cada 5 minutos (mínimo permitido pelo Apps Script)
  ScriptApp.newTrigger("atualizarAvaliacoes")
    .timeBased()
    .everyMinutes(5)
    .create();

  SpreadsheetApp.getUi().alert(
    "✅ Automação Ativada!",
    "As avaliações serão verificadas automaticamente a cada 5 minutos.\n\n" +
    "Custo por execução: 1 chamada de API (50 avaliações verificadas).\n" +
    "Novas avaliações aparecem no topo da aba, destacadas em azul.",
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}

function desativarAtualizacaoAutomatica() {
  let removidos = 0;
  ScriptApp.getProjectTriggers().forEach(t => {
    if (t.getHandlerFunction() === "atualizarAvaliacoes") {
      ScriptApp.deleteTrigger(t);
      removidos++;
    }
  });
  SpreadsheetApp.getUi().alert(
    removidos > 0 ? "⛔ Automação desativada." : "ℹ️ Nenhum gatilho ativo encontrado."
  );
}


// ═══════════════════════════════════════════════════════════════════════════════
//  MENU PERSONALIZADO
// ═══════════════════════════════════════════════════════════════════════════════

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu("🗺️ Avaliações GBP")
    .addItem("▶ Atualizar agora (últimas 50)", "atualizarAvaliacoes")
    .addSeparator()
    .addItem("⏱️ Ativar atualização a cada 5 min", "ativarAtualizacaoAutomatica")
    .addItem("⛔ Desativar atualização automática", "desativarAtualizacaoAutomatica")
    .addSeparator()
    .addItem("📥 Importação completa (todas as avaliações)", "importarAvaliacoes")
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
    "4. Salve e execute 'Ativar atualização a cada 5 min'",
    SpreadsheetApp.getUi().ButtonSet.OK
  );
}


// ═══════════════════════════════════════════════════════════════════════════════
//  IMPORTAÇÃO COMPLETA (use apenas na primeira vez ou para reprocessar tudo)
// ═══════════════════════════════════════════════════════════════════════════════

function importarAvaliacoes() {
  const ui = SpreadsheetApp.getUi();
  const resposta = ui.alert(
    "⚠️ Importação Completa",
    "Isso irá apagar a aba atual e reimportar TODAS as avaliações.\n" +
    "Pode demorar vários minutos.\n\nDeseja continuar?",
    ui.ButtonSet.YES_NO
  );
  if (resposta !== ui.Button.YES) return;

  try {
    const token = obterAccessToken();
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    garantirAbas(ss);

    // Limpar aba de avaliações mantendo o cabeçalho
    const aba = ss.getSheetByName(ABA_AVALIACOES);
    if (aba.getLastRow() > 1) {
      aba.deleteRows(2, aba.getLastRow() - 1);
    }

    // Buscar todas com paginação
    const accId = ACCOUNT_ID.split("/").pop();
    const locId = LOCATION_ID.split("/").pop();
    const baseUrl = `https://mybusiness.googleapis.com/v4/accounts/${accId}/locations/${locId}/reviews`;
    const headers = { "Authorization": "Bearer " + token };

    let todasAvaliacoes = [];
    let nextPageToken = null;
    let pagina = 0;
    let totalGoogle = 0;
    let notaMedia = 0;

    do {
      pagina++;
      let url = `${baseUrl}?pageSize=50&orderBy=updateTime%20desc`;
      if (nextPageToken) url += "&pageToken=" + encodeURIComponent(nextPageToken);

      const r = UrlFetchApp.fetch(url, { headers, muteHttpExceptions: true });
      if (r.getResponseCode() !== 200) throw new Error("Erro API página " + pagina);

      const data = JSON.parse(r.getContentText());
      if (pagina === 1) { totalGoogle = data.totalReviewCount || 0; notaMedia = data.averageRating || 0; }
      todasAvaliacoes = todasAvaliacoes.concat(data.reviews || []);
      nextPageToken = data.nextPageToken || null;
      if (nextPageToken) Utilities.sleep(300);

    } while (nextPageToken);

    // Inserir em lote
    if (todasAvaliacoes.length > 0) {
      inserirNovasAvaliacoes(ss, todasAvaliacoes);
    }

    atualizarResumo(ss, totalGoogle, notaMedia, todasAvaliacoes.length);
    ui.alert("✅ Importação completa!", `${todasAvaliacoes.length} avaliações importadas.`, ui.ButtonSet.OK);

  } catch (e) {
    ui.alert("❌ Erro", e.message, ui.ButtonSet.OK);
  }
}
