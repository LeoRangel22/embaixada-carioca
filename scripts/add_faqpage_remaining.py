#!/usr/bin/env python3
"""Add FAQPage schemas to remaining high-value pages."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAQS = {
    "cafe-da-manha-pao-de-acucar.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/cafe-da-manha-pao-de-acucar.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Tem café da manhã no Pão de Açúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sim! A Embaixada Carioca serve café da manhã na primeira parada do bondinho, no Morro da Urca (227m), com vista para o Pão de Açúcar. Funciona todos os dias das 8h30 às 11h30."}},
            {"@type": "Question", "name": "Precisa de ingresso do bondinho para o café da manhã no Pão de Açúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sim, é necessário o ingresso do Parque Bondinho Pão de Açúcar (Praça General Tibúrcio, 68, Urca). O restaurante fica na primeira estação, o Morro da Urca, sem precisar subir ao Pão de Açúcar."}},
            {"@type": "Question", "name": "Quanto custa o café da manhã no Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "O café da manhã individual custa a partir de R$79,90 na Embaixada Carioca. O ingresso do Parque Bondinho é cobrado à parte. Aceitamos cartões, PIX e dinheiro."}}
        ]
    },
    "feijoada-com-vista-rio-de-janeiro.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/feijoada-com-vista-rio-de-janeiro.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Onde comer feijoada no Rio de Janeiro com vista?",
             "acceptedAnswer": {"@type": "Answer", "text": "A Embaixada Carioca serve a feijoada mais premiada do Rio de Janeiro com vista direta para o Pão de Açúcar, no Morro da Urca dentro do Parque Bondinho. Premiada pela Veja Rio Comer & Beber 2025/2026."}},
            {"@type": "Question", "name": "A feijoada é servida todos os dias na Embaixada Carioca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sim, a feijoada completa é servida todos os dias da semana no almoço, das 11h30 às 17h. Reservas recomendadas, especialmente nos finais de semana."}},
            {"@type": "Question", "name": "Qual o preço da feijoada na Embaixada Carioca?",
             "acceptedAnswer": {"@type": "Answer", "text": "A Feijoada Completa custa R$189,70 por pessoa e inclui feijão preto, carnes, couve, laranja, farofa e arroz. Veja o cardápio completo em embaixadacarioca.com/cardapio."}}
        ]
    },
    "o-que-fazer-depois-do-bondinho-pao-de-acucar.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/o-que-fazer-depois-do-bondinho-pao-de-acucar.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "O que fazer depois do Bondinho do Pão de Açúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Depois do Bondinho, almoce ou tome café na Embaixada Carioca no Morro da Urca, explore as trilhas da Urca, visite a Praia Vermelha e caminhe pelo bairro da Urca — um dos mais charmosos do Rio de Janeiro."}},
            {"@type": "Question", "name": "Tem restaurante no Parque Bondinho Pão de Açúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sim, a Embaixada Carioca é o restaurante oficial dentro do Parque Bondinho Pão de Açúcar, localizada no Morro da Urca (primeira estação). Serve café da manhã, almoço e drinks no entardecer."}},
            {"@type": "Question", "name": "Dá para almoçar dentro do Parque Bondinho?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sim! Com o ingresso do Parque Bondinho você pode almoçar na Embaixada Carioca no Morro da Urca, com vista para o Pão de Açúcar e a Baía de Guanabara, das 11h30 às 17h."}}
        ]
    },
    "por-do-sol-morro-da-urca.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/por-do-sol-morro-da-urca.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Onde ver o pôr do sol no Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "O terraço da Embaixada Carioca no Morro da Urca é um dos melhores pontos para ver o pôr do sol no Rio de Janeiro, com vista para o Pão de Açúcar, Baía de Guanabara e Corcovado."}},
            {"@type": "Question", "name": "Tem música ao vivo no pôr do sol no Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sim! A Embaixada Carioca tem shows ao vivo no entardecer, com DJs e bandas de jazz, samba e MPB. Confira a programação no Instagram @embaixadacarioca."}}
        ]
    },
    "roteiro-meio-dia-urca-pao-de-acucar.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/roteiro-meio-dia-urca-pao-de-acucar.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Como organizar meio dia no Pão de Açúcar e Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "O roteiro ideal: chegue às 8h30 para o café da manhã na Embaixada Carioca (Morro da Urca), suba de bondinho ao Pão de Açúcar, volte para almoçar, explore as trilhas da Urca e encerre com um drink no entardecer."}},
            {"@type": "Question", "name": "Quanto tempo leva a visita ao Bondinho Pão de Açúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "A visita completa (Morro da Urca + Pão de Açúcar) leva de 2 a 4 horas. Com café da manhã ou almoço na Embaixada Carioca, reserve meio dia completo (4–5 horas) para aproveitar tudo."}},
        ]
    },
    "gastronomia-carioca.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/gastronomia-carioca.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Qual é o melhor restaurante de gastronomia carioca no Rio?",
             "acceptedAnswer": {"@type": "Answer", "text": "A Embaixada Carioca no Morro da Urca é referência em gastronomia carioca, com pratos como feijoada premiada, picanha grelhada, bobo de camarão e caipirinhas artesanais, com vista para o Pão de Açúcar."}},
            {"@type": "Question", "name": "O que é gastronomia carioca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Gastronomia carioca é a culinária típica do Rio de Janeiro, com pratos como feijoada, bolinho de bacalhau, moqueca, caipirinha e chope. A Embaixada Carioca celebra essa tradição com ingredientes frescos e vista para o Pão de Açúcar."}}
        ]
    },
    "caipirinha-com-vista-rio.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/caipirinha-com-vista-rio.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Onde tomar caipirinha com vista para o Pão de Açúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "A Embaixada Carioca serve as melhores caipirinhas do Rio de Janeiro no terraço do Morro da Urca, com vista direta para o Pão de Açúcar e a Baía de Guanabara. Aberto todos os dias até as 21h."}},
            {"@type": "Question", "name": "Qual a melhor hora para tomar drinks no Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "O entardecer (das 17h às 21h) é o horário mais especial para drinks no Morro da Urca, com o sol se pondo atrás do Pão de Açúcar e frequentemente música ao vivo na Embaixada Carioca."}}
        ]
    },
    # EN versions
    "en/feijoada-com-vista-rio-de-janeiro.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/feijoada-com-vista-rio-de-janeiro.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Where to eat feijoada in Rio de Janeiro with a view?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca serves award-winning feijoada (Brazilian black bean stew) with a direct view of Sugarloaf Mountain at Morro da Urca, inside Parque Bondinho. Awarded Best Feijoada by Veja Rio 2025/2026."}},
            {"@type": "Question", "name": "Is feijoada served every day at Embaixada Carioca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes, the complete feijoada is served every day at lunch, from 11:30 to 17:00. Reservations are recommended, especially on weekends."}}
        ]
    },
    "en/gastronomia-carioca.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/gastronomia-carioca.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "What is carioca gastronomy?",
             "acceptedAnswer": {"@type": "Answer", "text": "Carioca gastronomy is the cuisine from Rio de Janeiro, featuring dishes like feijoada (black bean stew), bolinho de bacalhau (codfish croquettes), moqueca (fish stew), and Brazil's iconic caipirinha. Embaixada Carioca celebrates this tradition at Morro da Urca with Sugarloaf views."}},
            {"@type": "Question", "name": "Best Brazilian restaurant in Rio de Janeiro?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca at Morro da Urca is consistently rated as one of the best Brazilian restaurants in Rio, combining authentic carioca cuisine with panoramic views of Sugarloaf Mountain."}}
        ]
    },
    "en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/o-que-fazer-depois-do-bondinho-pao-de-acucar.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "What to do after the Sugarloaf cable car?",
             "acceptedAnswer": {"@type": "Answer", "text": "After the cable car, have lunch or drinks at Embaixada Carioca on Morro da Urca, explore the Urca hiking trails, visit Praia Vermelha beach, and walk through the charming Urca neighborhood."}},
            {"@type": "Question", "name": "Is there a restaurant inside the Sugarloaf Cable Car Park?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes, Embaixada Carioca is the official restaurant inside Parque Bondinho Pão de Açúcar, at Morro da Urca (first cable car stop). It serves breakfast, lunch and sundowner drinks."}}
        ]
    },
    "en/por-do-sol-morro-da-urca.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/por-do-sol-morro-da-urca.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Where to watch the sunset at Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "The terrace of Embaixada Carioca at Morro da Urca is one of the best spots to watch the sunset in Rio de Janeiro, with views of Sugarloaf Mountain, Guanabara Bay and Corcovado."}},
            {"@type": "Question", "name": "Is there live music at sunset on Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Yes! Embaixada Carioca features live music at sunset — DJs, jazz bands, samba and MPB. Check the schedule on Instagram @embaixadacarioca."}}
        ]
    },
    "en/roteiro-meio-dia-urca-pao-de-acucar.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/roteiro-meio-dia-urca-pao-de-acucar.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "How to plan a half-day at Sugarloaf and Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Ideal itinerary: Arrive at 8:30 for breakfast at Embaixada Carioca (Morro da Urca), take the cable car up to Sugarloaf, return for lunch, explore the Urca trails, and end with a sundowner drink."}},
            {"@type": "Question", "name": "How long does the Sugarloaf cable car visit take?",
             "acceptedAnswer": {"@type": "Answer", "text": "The full visit (Morro da Urca + Sugarloaf peak) takes 2–4 hours. With breakfast or lunch at Embaixada Carioca, allow a full half-day (4–5 hours) to enjoy everything."}}
        ]
    },
    # ES versions
    "es/feijoada-com-vista-rio-de-janeiro.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/feijoada-com-vista-rio-de-janeiro.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Dónde comer feijoada en Río con vista?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca sirve la feijoada más premiada de Río de Janeiro con vista al Pan de Azúcar en el Morro da Urca, dentro del Parque Bondinho. Premiada como la Mejor Feijoada por Veja Rio 2025/2026."}},
            {"@type": "Question", "name": "¿La feijoada se sirve todos los días?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sí, la feijoada completa se sirve todos los días en el almuerzo, de 11:30 a 17:00. Recomendamos reservar con anticipación, especialmente los fines de semana."}}
        ]
    },
    "es/gastronomia-carioca.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/gastronomia-carioca.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Qué es la gastronomía carioca?",
             "acceptedAnswer": {"@type": "Answer", "text": "La gastronomía carioca es la cocina típica de Río de Janeiro, con platos como feijoada, bolinho de bacalhau, moqueca y caipirinha. Embaixada Carioca celebra esta tradición en el Morro da Urca con vistas al Pan de Azúcar."}},
            {"@type": "Question", "name": "¿Cuál es el mejor restaurante brasileño en Río de Janeiro?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca en el Morro da Urca combina cocina brasileña auténtica con vistas panorámicas al Pan de Azúcar, siendo uno de los restaurantes más elogiados de Río."}}
        ]
    },
    "es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/o-que-fazer-depois-do-bondinho-pao-de-acucar.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Qué hacer después del teleférico del Pan de Azúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Después del teleférico, almuerza o toma algo en Embaixada Carioca en el Morro da Urca, explora los senderos de Urca, visita la Praia Vermelha y camina por el encantador barrio de Urca."}},
            {"@type": "Question", "name": "¿Hay restaurante dentro del Parque Bondinho Pan de Azúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sí, Embaixada Carioca es el restaurante oficial dentro del Parque Bondinho Pão de Açúcar, en el Morro da Urca (primera parada). Sirve desayuno, almuerzo y bebidas al atardecer."}}
        ]
    },
    "es/por-do-sol-morro-da-urca.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/por-do-sol-morro-da-urca.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Dónde ver el atardecer en el Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "La terraza de Embaixada Carioca en el Morro da Urca es uno de los mejores puntos para ver el atardecer en Río de Janeiro, con vistas al Pan de Azúcar, la Bahía de Guanabara y el Corcovado."}},
            {"@type": "Question", "name": "¿Hay música en vivo al atardecer en el Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sí, Embaixada Carioca tiene música en vivo al atardecer — DJs, jazz, samba y MPB. Consulta la programación en Instagram @embaixadacarioca."}}
        ]
    },
    "es/roteiro-meio-dia-urca-pao-de-acucar.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/roteiro-meio-dia-urca-pao-de-acucar.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Cómo organizar medio día en el Pan de Azúcar y Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Itinerario ideal: llega a las 8:30 para desayunar en Embaixada Carioca (Morro da Urca), sube en teleférico al Pan de Azúcar, vuelve a almorzar, explora los senderos de Urca y termina con una bebida al atardecer."}},
            {"@type": "Question", "name": "¿Cuánto tiempo dura la visita al teleférico del Pan de Azúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "La visita completa (Morro da Urca + Pan de Azúcar) dura 2 a 4 horas. Con desayuno o almuerzo en Embaixada Carioca, reserva medio día completo (4–5 horas) para disfrutarlo todo."}}
        ]
    },
    "es/parque-bondinho.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/parque-bondinho.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Hay restaurante en el Parque Bondinho Pan de Azúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sí, Embaixada Carioca es el restaurante oficial dentro del Parque Bondinho Pão de Açúcar, en el Morro da Urca. Sirve desayuno, almuerzo, caipirinhas y eventos con vista panorámica."}},
            {"@type": "Question", "name": "¿Cómo llegar al Parque Bondinho Pan de Azúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "El Parque Bondinho está en Praça General Tibúrcio, 68, Urca, Río de Janeiro. Puedes llegar en taxi, Uber, bus (línea 107) o caminar desde el metro Botafogo. El restaurante está en la primera parada del teleférico."}}
        ]
    },
    "en/nossa-visao.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/nossa-visao.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "What makes Embaixada Carioca unique?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca is the only restaurant inside Parque Bondinho Pão de Açúcar, at 227 meters altitude on Morro da Urca, with panoramic views of Sugarloaf Mountain, Guanabara Bay and Rio de Janeiro."}},
        ]
    },
    "es/nossa-visao.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/nossa-visao.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Qué hace único a Embaixada Carioca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca es el único restaurante dentro del Parque Bondinho Pão de Açúcar, a 227 metros de altitud en el Morro da Urca, con vistas panorámicas al Pan de Azúcar, la Bahía de Guanabara y Río de Janeiro."}},
        ]
    },
    "en/caipirinha-com-vista-rio.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/en/caipirinha-com-vista-rio.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "Where to have caipirinha with a view of Sugarloaf Mountain?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca serves Rio's best caipirinhas on the terrace of Morro da Urca, with direct views of Sugarloaf Mountain. Open daily until 21:00."}},
            {"@type": "Question", "name": "What is the best time for drinks at Morro da Urca?",
             "acceptedAnswer": {"@type": "Answer", "text": "Sunset (5 PM–9 PM) is the most magical time for drinks at Morro da Urca, with the sun setting behind Sugarloaf and often live music at Embaixada Carioca."}}
        ]
    },
    "es/caipirinha-com-vista-rio.html": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "@id": "https://www.embaixadacarioca.com/es/caipirinha-com-vista-rio.html#faq",
        "mainEntity": [
            {"@type": "Question", "name": "¿Dónde tomar caipirinha con vista al Pan de Azúcar?",
             "acceptedAnswer": {"@type": "Answer", "text": "Embaixada Carioca sirve las mejores caipirinhas de Río en la terraza del Morro da Urca, con vista directa al Pan de Azúcar y la Bahía de Guanabara. Abierto todos los días hasta las 21h."}},
        ]
    },
}


def main():
    count = 0
    for rel, schema in FAQS.items():
        path = ROOT / rel
        if not path.exists():
            print("  MISSING " + rel)
            continue
        html = path.read_text(encoding="utf-8")
        if '"FAQPage"' in html:
            print("  skip (already has FAQPage): " + rel)
            continue
        block = '\n<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + "</script>"
        html = html.replace("</head>", block + "\n</head>", 1)
        path.write_text(html, encoding="utf-8")
        print("  added FAQPage: " + rel)
        count += 1
    print(f"\nTotal: {count} FAQPage schemas added")


if __name__ == "__main__":
    main()
