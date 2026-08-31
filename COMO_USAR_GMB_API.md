# Como Usar a Google My Business API para Baixar Avaliações

**Script:** `gmb_reviews_api.py`  
**API:** Google Business Profile API v4 (oficial)  
**Objetivo:** Baixar todas as avaliações da Embaixada Carioca diretamente pela API oficial do Google, sem scraping.

**Estado em 31/08/2026:** este continua sendo o método preferencial. O endpoint oficial `accounts.locations.reviews.list` retorna avaliações paginadas, média e contagem total para uma localização verificada. Acesso à API e permissões da conta continuam sendo pré-requisitos.

---

## Visão Geral do Fluxo

```
Google Cloud Console
  → Criar projeto
  → Ativar "My Business API"
  → Criar credenciais OAuth2
  → Baixar credentials.json

python3 gmb_reviews_api.py
  → Abre navegador para autorização (1ª vez)
  → Salva token.json para execuções futuras
  → Baixa todas as avaliações via API
  → Exporta para JSON + CSV + Excel
```

---

## Passo 1 — Instalar Dependências

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 \
            google-api-python-client openpyxl requests
```

---

## Passo 2 — Criar Projeto no Google Cloud Console

1. Acesse: [console.cloud.google.com](https://console.cloud.google.com/)
2. Clique em **"Selecionar projeto"** → **"Novo projeto"**
3. Nome: `embaixada-carioca-reviews` → Clique em **Criar**

---

## Passo 3 — Ativar a Google My Business API

1. No menu lateral, vá em **"APIs e serviços"** → **"Biblioteca"**
2. Pesquise por: `My Business API`
3. Clique em **"Google My Business API"** → **"Ativar"**

> **Atenção:** A Google My Business API requer aprovação para uso em produção. Para uso pessoal (acesso à sua própria conta), o acesso de teste é suficiente.

---

## Passo 4 — Criar Credenciais OAuth2

1. Vá em **"APIs e serviços"** → **"Credenciais"**
2. Clique em **"+ Criar credenciais"** → **"ID do cliente OAuth"**
3. Se solicitado, configure a **"Tela de consentimento OAuth"**:
   - Tipo de usuário: **Externo**
   - Nome do app: `Embaixada Carioca Reviews`
   - E-mail de suporte: seu e-mail
   - Salve e continue
4. De volta em Credenciais:
   - Tipo de aplicativo: **App para computador**
   - Nome: `Reviews Scraper`
   - Clique em **Criar**
5. Clique em **"Baixar JSON"**
6. Renomeie o arquivo para `credentials.json`
7. Coloque na mesma pasta do script `gmb_reviews_api.py`

---

## Passo 5 — Adicionar Usuário de Teste (se necessário)

Se a tela de consentimento estiver em modo "Teste":

1. Vá em **"APIs e serviços"** → **"Tela de consentimento OAuth"**
2. Role até **"Usuários de teste"**
3. Clique em **"+ Add users"**
4. Adicione o e-mail da conta Google que gerencia a Embaixada Carioca

---

## Passo 6 — Executar o Script

```bash
python3 gmb_reviews_api.py
```

**Na primeira execução:**
- Um navegador abrirá automaticamente
- Faça login com a conta Google que tem acesso ao Perfil da Empresa da Embaixada Carioca
- Clique em **"Permitir"** para autorizar o acesso
- O token é salvo em `token.json` — execuções futuras são automáticas

---

## Arquivos de Saída

| Arquivo | Descrição |
| :--- | :--- |
| `reviews_embaixada_carioca.json` | Dados completos com metadados, distribuição de estrelas e todas as avaliações |
| `reviews_embaixada_carioca.csv` | Tabela para importar no Google Sheets ou Excel |
| `reviews_embaixada_carioca.xlsx` | Planilha formatada com 3 abas: **Resumo**, **Avaliações** e **Análise por Nota** |

---

## Dados Coletados por Avaliação

| Campo | Descrição |
| :--- | :--- |
| `review_id` | ID único da avaliação no Google |
| `author_name` | Nome do autor |
| `is_anonymous` | Se o autor escolheu ser anônimo |
| `rating` | Nota de 1 a 5 estrelas |
| `comment` | Texto completo da avaliação |
| `create_time` | Data de criação |
| `update_time` | Data da última atualização |
| `owner_reply` | Resposta do proprietário |
| `owner_reply_time` | Data da resposta do proprietário |
| `has_media` | Se a avaliação contém fotos |
| `media_count` | Número de fotos na avaliação |

---

## Diferença em Relação ao Script Anterior

| Característica | `google_reviews_scraper.py` | `gmb_reviews_api.py` |
| :--- | :--- | :--- |
| Método | Manus API (agente + scraping) | API oficial do Google |
| Autenticação | Chave Manus API | OAuth2 Google |
| Dados retornados | Dependente do que o agente vê | Dados estruturados completos |
| ID único por avaliação | ❌ | ✅ |
| Timestamps precisos | ❌ | ✅ (ISO 8601) |
| Velocidade | 5–20 minutos | 1–2 minutos |
| Requer aprovação | ❌ | ⚠️ (modo teste é suficiente) |

---

## Solução de Problemas

**`Access blocked: This app's request is invalid`:**  
Adicione seu e-mail como usuário de teste na tela de consentimento OAuth.

**`HttpError 403: The caller does not have permission`:**  
A conta Google usada não tem acesso ao Perfil da Empresa. Use a conta proprietária ou gerente.

**`HttpError 404: Requested entity was not found`:**  
O local não foi encontrado. O script listará todos os locais disponíveis para você escolher.

**Token expirado:**  
Delete o arquivo `token.json` e execute o script novamente para reautorizar.
