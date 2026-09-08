# Correções da experiência de visita — 08/09/2026

## Escopo

Homes `index.html`, `en/index.html` e `es/index.html`. Não é uma certificação global de design, acessibilidade ou SEO.

## Alterações

- Composição do hero em fluxo: título, descrição, selos e CTAs deixam de disputar coordenadas fixas. Removido logo secundário que sobrepunha texto.
- WhatsApp preservado como link direto, sem interceptar o primeiro clique ou abrir automaticamente um falso diálogo de atendimento. Removida indicação de atendimento “Online” sem integração com disponibilidade real.
- Cardápio aponta para `/cardapio.html`, `/en/cardapio.html` e `/es/cardapio.html`.
- Como chegar aponta para `/como-chegar.html`, `/en/how-to-get-there.html` e `/es/como-llegar.html`, inclusive no rodapé e no hero. Acesso é explicado antes de solicitar rota no Maps.
- Links vazios de cardápio/endereço do rodapé foram corrigidos. O antigo placeholder de acessibilidade foi renomeado para acesso ao parque e aponta para informações de chegada, sem prometer certificação de acessibilidade.
- Horário fixo do pôr do sol e cálculo sazonal impreciso retirados. Mantidos horários informados de funcionamento; nenhuma integração meteorológica nova foi inventada.
- Selos de prêmio consolidados em um quadro: feijoada da Academia da Cachaça, Veja Rio Comer & Beber 2025/2026 e Prazeres da Mesa 2017, servida na Embaixada mediante parceria formal.
- Alegações amplas como único almoço/única opção completa e liderança absoluta em avaliações revisadas nas homes. Mantido o diferencial de vista frontal informado pelo proprietário.
- Barra mobile de reserva redundante oculta; botão de menu e seletor de idioma mobile restaurados.
- `lastmod` das homes atualizado para a data da alteração real.

## Verificações

- Teste de fonte: `python scripts/test_home_visit_experience.py`.
- JSON-LD duplicate key guard: 111 arquivos, zero pendências.
- Schema rating guard: 111 arquivos, zero pendências.
- Hreflang PT/EN/ES: PASS, score mínimo 100.
- i18n: nenhuma página PT sem equivalente EN/ES; 12 alertas editoriais de títulos/seções preexistentes permanecem.
- Comparação de JSON-LD: EN/ES inalterados. Na home PT, somente o texto de uma resposta foi ajustado para retirar “mais bem avaliado”; não foram adicionados ou removidos tipos/propriedades.
- Testes locais de layout nas três línguas, larguras 320, 390, 768, 1024 e 1440: sem colisão entre título, descrição, selos, CTAs, quadro e faixa inferior; sem overflow horizontal; sem popup automático; sem erros de JavaScript nos testes.
- Capturas locais desktop/mobile revisadas visualmente; checagem interativa de menu e idioma complementa a inspeção.

## Instagram: investigação parcial, sem alteração de conta

O endereço https://www.instagram.com/embaixadacarioca/ exibiu, sem login: “Perfil restrito. Você deve ter pelo menos 18 anos para ver este perfil. Entre para continuar.”

Não há sessão administrativa autenticada disponível. Não é possível concluir se a restrição foi configurada pelo administrador, se há regras por país ou se decorre de outra condição da plataforma. Não foi comprovada penalização algorítmica nem bloqueio geral do perfil para adultos conectados.

Próximo dado necessário: captura da configuração “Idade mínima” da conta profissional, com idade padrão e eventuais limites por país, e do status da conta. Não remover a restrição sem avaliar regras aplicáveis ao conteúdo alcoólico. Nenhuma idade, data de nascimento, política de privacidade ou restrição foi alterada.

## Limites

Não foi feita revisão integral de depoimentos, cardápio, horários de feriados ou alegações em todas as páginas internas. Não se declara “AAA+” nem incremento de conversão sem medição posterior. Os testes automatizados de conteúdo não substituem a inspeção visual.
