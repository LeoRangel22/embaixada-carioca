# Como usar o script de inspeção de URLs do GSC

**Script:** `gsc_reindex.py`  
**Objetivo real:** Verificar o status de indexação de URLs da Embaixada Carioca pela URL Inspection API.

> **Correção de documentação — 31/08/2026:** apesar do nome legado, o script não solicita reindexação. O método `urlInspection.index.inspect` apenas retorna informações da URL no índice do Google. Para páginas comuns do restaurante, use a inspeção manual do Search Console e o sitemap. A Indexing API do Google é restrita a páginas com `JobPosting` ou `BroadcastEvent` dentro de `VideoObject`.

---

## Pré-requisitos

### 1. Instalar as dependências Python

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

---

### 2. Configurar as Credenciais do Google Cloud

Este script usa OAuth 2.0 para autenticar com o Google Search Console. Siga os passos abaixo **uma única vez**:

#### Passo 1 — Criar o Projeto no Google Cloud Console
1. Acesse [https://console.cloud.google.com/](https://console.cloud.google.com/)
2. Clique em **"Selecionar projeto"** → **"Novo Projeto"**
3. Dê um nome (ex: `embaixada-carioca-seo`) e clique em **Criar**

#### Passo 2 — Ativar a API do Search Console
1. No menu lateral, vá em **"APIs e Serviços" → "Biblioteca"**
2. Pesquise por **"Google Search Console API"**
3. Clique em **"Ativar"**

#### Passo 3 — Criar as Credenciais OAuth 2.0
1. Vá em **"APIs e Serviços" → "Credenciais"**
2. Clique em **"+ Criar Credenciais" → "ID do cliente OAuth"**
3. Se solicitado, configure a **Tela de Consentimento OAuth**:
   - Tipo: **Externo**
   - Nome do app: `Embaixada Carioca SEO`
   - E-mail de suporte: seu e-mail
   - Salve e continue
4. De volta em "Criar ID do cliente OAuth":
   - Tipo de aplicativo: **App para computador**
   - Nome: `gsc-reindex-script`
   - Clique em **Criar**
5. Clique em **"Baixar JSON"** e salve o arquivo como:
   ```
   credentials.json
   ```
   na mesma pasta do script `gsc_reindex.py`

#### Passo 4 — Adicionar o Usuário como Testador (se necessário)
1. Vá em **"APIs e Serviços" → "Tela de Consentimento OAuth"**
2. Em **"Usuários de teste"**, clique em **"+ Add Users"**
3. Adicione o e-mail da conta Google que tem acesso ao GSC da Embaixada Carioca

---

### 3. Verificar Propriedade no GSC (se ainda não verificado)

A conta Google usada para autenticar deve ser **proprietária verificada** da propriedade `https://www.embaixadacarioca.com/` no Google Search Console.

---

## Como Executar

```bash
# Na pasta onde estão os arquivos credentials.json e gsc_reindex.py:
python3 gsc_reindex.py
```

**Na primeira execução:**
- Um navegador abrirá automaticamente pedindo autorização
- Faça login com a conta Google que tem acesso ao GSC
- Clique em **"Permitir"**
- O token será salvo em `token.json` para execuções futuras (sem precisar autorizar novamente)

---

## O que o script faz

O script inspeciona e reporta o status de indexação de **3 grupos de URLs**. Ele não envia pedido de indexação:

| Grupo | URLs | Descrição |
| :--- | :---: | :--- |
| Alta Prioridade | 6 | Páginas com canonical e noindex corrigidos nesta sessão |
| KWs de Ouro | 11 | Páginas otimizadas para restaurante/café/almoço + Pão de Açúcar |
| Core | 6 | Homepage e páginas principais |

### Status de Retorno

| Ícone | Verdict | Significado |
| :---: | :--- | :--- |
| ✅ | `PASS` | Página indexada com sucesso |
| ⚪ | `NEUTRAL` | Página encontrada mas não indexada (ex: excluída por canonical) |
| ❌ | `FAIL` | Página com erro de indexação |
| ⚠️ | `ERRO` | Erro na chamada da API |

---

## Saída do Script

O script gera um arquivo `relatorio_reindexacao_YYYYMMDD_HHMMSS.json` com todos os resultados para acompanhamento.

O nome do arquivo de saída também é legado; interprete-o como relatório de inspeção.

## Como solicitar indexação corretamente

1. Confirme que a URL é canônica, indexável, está no sitemap e responde `200`.
2. Abra a URL Inspection no Search Console.
3. Execute o teste da URL publicada.
4. Use “Solicitar indexação” somente para uma URL canônica nova ou materialmente alterada.
5. Não solicite indexação de aliases, `/index.html`, variantes `.com.br` ou URLs que redirecionam.

Referências oficiais:

- URL Inspection API: `https://developers.google.com/webmaster-tools/v1/urlInspection.index/inspect`
- Limites da Indexing API: `https://developers.google.com/search/apis/indexing-api/v3/quickstart`

---

## Quota da API

- **URL Inspection API:** 2.000 requisições por dia (gratuito)
- O script processa 23 URLs com delay de 1,5s entre cada uma (~35 segundos no total)

---

## Solução de Problemas

**Erro `credentials.json não encontrado`:**  
Certifique-se de que o arquivo foi salvo com o nome exato `credentials.json` na mesma pasta do script.

**Erro `403 Forbidden`:**  
A conta Google não tem permissão de proprietário verificado no GSC para a propriedade `https://www.embaixadacarioca.com/`.

**Erro `Token expirado`:**  
Delete o arquivo `token.json` e execute o script novamente para reautenticar.
