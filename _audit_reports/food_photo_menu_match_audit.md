# Auditoria de correspondência entre fotos e cardápio

Status geral: **PENDENTE DE 2 CONFIRMAÇÕES**

## Comparação visual com o cardápio oficial

| Arquivo da foto | Identificação visual | Correspondência no cardápio | Situação |
|---|---|---|---|
| `assets/carne-seca-mandioca.webp` | Carne seca acebolada com aipim frito | O cardápio contém itens separados de carne seca e aipim, mas não este prato completo | **Confirmar se ainda é servido** |
| `assets/bobo-camarao-real.webp` | Risoto cremoso de camarão; os grãos de arroz são visíveis | O cardápio atual não lista risoto de camarão; lista bobó de camarão e risoto de quinoa | **Confirmar se ainda é servido** |
| `assets/fabio-almoco-mesa-completa.webp` | Mesa com picanha, feijoada, bolinhos, pastéis, acompanhamentos e drinks | Itens compatíveis com o cardápio, exceto a porção de carne seca com aipim que precisa de confirmação | **Legenda genérica correta** |
| `assets/fabio-almoco-salmao-pao-acucar.webp` | Salmão com molho de maracujá e Carioquinha de peixe | Ambos aparecem no cardápio | **Corrigido** |
| `assets/fabio-almoco-salmao-maracuja.webp` | Salmão com molho de maracujá, arroz de brócolis e legumes grelhados | Correspondência exata | **Corrigido** |
| `assets/fabio-almoco-picanha-fritas.webp` | Carne, arroz, feijão, farofa e fritas | Correspondência exata com Carioquinha de filé mignon; não com a Picanha à brasileira, que não leva feijão | **Corrigido** |
| `assets/fabio-feijoada-caldeiron.webp` | Feijoada em panela | Correspondência com a Feijoada da Academia da Cachaça | **Correto** |

## Mapeamentos automáticos corrigidos

- Cards de `Picanha` passam a usar `assets/almoco-picanha-grelhada.webp`.
- Cards de `Feijoada` passam a usar `assets/feijoada-panela-close-acompanhamentos.webp`.
- Cards de `Salmão` passam a usar `assets/fabio-almoco-salmao-maracuja.webp`.
- O antigo mapeamento de `Picadinho` para a foto de carne seca foi removido; a foto com arroz, feijão, farofa e fritas passa a representar `Carioquinha`.
- A imagem `assets/bobo-camarao-real.webp` não é mais usada automaticamente como `Bobó`; visualmente ela mostra um risoto.

## Confirmações necessárias

1. A porção de carne seca acebolada com aipim frito ainda faz parte do cardápio?
2. O risoto de camarão ainda faz parte do cardápio, embora não esteja listado na versão atual?
