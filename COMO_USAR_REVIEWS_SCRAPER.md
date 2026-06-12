# Como Usar o Script de Avaliações do Google Maps

**Script:** `google_reviews_scraper.py`  
**Objetivo:** Baixar automaticamente todas as avaliações da Embaixada Carioca no Google Maps e exportar para JSON, CSV e Excel.

---

## Como Funciona

O script usa a **Manus API** para criar uma tarefa de agente que:
1. Acessa o perfil do Google Maps da Embaixada Carioca
2. Rola a página para carregar **todas** as avaliações disponíveis
3. Coleta nome do autor, nota, data, texto, idioma, respostas do proprietário e mais
4. Retorna os dados em formato JSON estruturado via **Structured Output**
5. Exporta automaticamente para `.json`, `.csv` e `.xlsx`

---

## Pré-requisitos

### 1. Instalar dependências
```bash
pip install requests openpyxl
```

### 2. Obter a Chave de API Manus
1. Acesse: [https://manus.ai/settings/api](https://manus.ai/settings/api)
2. Clique em **"Create API Key"**
3. Copie a chave gerada

---

## Como Executar

```bash
# Definir a chave de API e executar
export MANUS_API_KEY="sua-chave-aqui"
python3 google_reviews_scraper.py
```

Ou em uma única linha:
```bash
MANUS_API_KEY="sua-chave-aqui" python3 google_reviews_scraper.py
```

---

## Tempo de Execução

O script pode levar entre **5 e 20 minutos** dependendo do volume de avaliações. O progresso é exibido em tempo real no terminal.

---

## Arquivos de Saída

| Arquivo | Descrição |
| :--- | :--- |
| `reviews_embaixada_carioca.json` | Dados completos em JSON (inclui distribuição de estrelas, notas, metadados) |
| `reviews_embaixada_carioca.csv` | Tabela simples para importar no Excel ou Google Sheets |
| `reviews_embaixada_carioca.xlsx` | Planilha formatada com 3 abas: Resumo, Avaliações e Análise por Idioma |

---

## Dados Coletados por Avaliação

| Campo | Descrição |
| :--- | :--- |
| `author_name` | Nome do autor |
| `rating` | Nota de 1 a 5 estrelas |
| `date` | Data da avaliação |
| `text` | Texto completo |
| `language` | Idioma detectado (pt, en, es, fr...) |
| `is_local_guide` | Se é Guia Local do Google |
| `helpful_count` | Número de "útil" |
| `owner_reply` | Resposta do proprietário |
| `owner_reply_date` | Data da resposta do proprietário |

---

## Solução de Problemas

**`MANUS_API_KEY não definida`:**  
Defina a variável de ambiente conforme as instruções acima.

**Timeout após 30 minutos:**  
Aumente o valor de `MAX_WAIT_TIME` no script (linha ~50) e execute novamente.

**Poucas avaliações coletadas:**  
O Google Maps pode limitar a exibição de avaliações. Execute o script novamente — o agente tentará rolar mais a página.
