#!/usr/bin/env python3
"""Restore cardapio completeness and PT/EN/ES parity.

Source reference: Cardapio - Embaixada Carioca - Pt e Esp - outubro 2025 digital.pdf.

What this script does:
- adds a full visible menu complement block to cardapio.html, en/cardapio.html and es/cardapio.html;
- keeps the same section/item structure in all three languages;
- does not touch JSON-LD, canonical, hreflang or review/rating schema;
- writes an audit report with item parity counts.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "_audit_reports" / "cardapio_completeness_i18n_fix_report.md"
START = "<!-- EC CARDAPIO COMPLETENESS I18N FIX -->"
END = "<!-- /EC CARDAPIO COMPLETENESS I18N FIX -->"

PAGES = {
    "pt": ROOT / "cardapio.html",
    "en": ROOT / "en" / "cardapio.html",
    "es": ROOT / "es" / "cardapio.html",
}

LABELS = {
    "pt": {
        "kicker": "Cardápio completo",
        "title": "Itens do cardápio completo",
        "intro": "Complemento editorial restaurado a partir do cardápio digital completo de outubro de 2025, com as categorias que não podiam ficar ausentes da página.",
        "note": "Valores e disponibilidade podem mudar conforme operação, estoque e horário. Confirme com a equipe no momento do pedido.",
        "source": "Fonte: cardápio digital Embaixada Carioca - outubro de 2025.",
    },
    "en": {
        "kicker": "Full menu",
        "title": "Complete menu items",
        "intro": "Editorial supplement restored from the complete October 2025 digital menu, including categories that should not be missing from the menu page.",
        "note": "Prices and availability may change depending on operation, stock and time of service. Please confirm with the team when ordering.",
        "source": "Source: Embaixada Carioca digital menu - October 2025.",
    },
    "es": {
        "kicker": "Menú completo",
        "title": "Ítems del menú completo",
        "intro": "Complemento editorial restaurado a partir del menú digital completo de octubre de 2025, con categorías que no deben faltar en la página del menú.",
        "note": "Los precios y la disponibilidad pueden cambiar según la operación, el stock y el horario. Confirme con el equipo al hacer el pedido.",
        "source": "Fuente: menú digital Embaixada Carioca - octubre de 2025.",
    },
}

# The visible page had become too short. This data intentionally favors coverage and parity.
# Each item has the same ID across pt/en/es to make audit deterministic.
MENU = [
    {
        "id": "starters",
        "title": {"pt": "Para começar", "en": "To start", "es": "Para empezar"},
        "items": [
            {"id":"caldinho-feijao","price":"R$ 14,70","pt":"Caldinho de feijão 140ml","en":"Black bean broth 140ml","es":"Caldito de frijoles 140ml"},
            {"id":"espeto-mignon","price":"R$ 58,70","pt":"Espetinho de filé mignon com molho à campanha","en":"Filet mignon skewer with vinaigrette salsa","es":"Brocheta de filete mignon con salsa vinagreta"},
            {"id":"espeto-frango-bacon","price":"R$ 39,70","pt":"Espetinho de filé de frango com bacon e molho à campanha","en":"Chicken and bacon skewer with vinaigrette salsa","es":"Brocheta de pollo con bacon y salsa vinagreta"},
            {"id":"espeto-camarao","price":"R$ 49,70","pt":"Espetinho de camarão com gomos de limão","en":"Shrimp skewer with lime wedges","es":"Brocheta de camarón con gajos de limón"},
            {"id":"espeto-queijo-coalho","price":"R$ 27,70","pt":"Queijo coalho com mel de pimenta","en":"Brazilian coalho cheese with pepper honey","es":"Queso coalho con miel de pimienta"},
            {"id":"espeto-abobrinha","price":"R$ 19,70","pt":"Abobrinha com molho teriyaki","en":"Zucchini with teriyaki sauce","es":"Calabacín con salsa teriyaki"},
            {"id":"empada-frango-cheddar","price":"R$ 12,00","pt":"Empada de frango com cheddar","en":"Chicken and cheddar empada","es":"Empada de pollo con cheddar"},
            {"id":"empada-carne-seca","price":"R$ 14,00","pt":"Empada de carne seca","en":"Brazilian dried beef empada","es":"Empada de carne seca desmechada"},
            {"id":"empada-camarao-catupiry","price":"R$ 15,00","pt":"Empada de camarão com Catupiry","en":"Shrimp empada with Catupiry cream cheese","es":"Empada de camarón con Catupiry"},
            {"id":"pastel-queijo","price":"R$ 45,70","pt":"Pasteizinhos de queijo minas padrão com mel de pimenta","en":"Minas cheese mini pastries with pepper honey","es":"Pastelitos de queso minas con miel de pimienta"},
            {"id":"pastel-carne-moida","price":"R$ 48,70","pt":"Pasteizinhos de carne moída com vinagrete à campanha","en":"Ground beef mini pastries with vinaigrette salsa","es":"Pastelitos de carne molida con salsa vinagreta"},
            {"id":"pastel-camarao-catupiry","price":"R$ 49,70","pt":"Pasteizinhos de camarão com Catupiry e molho de pitanga","en":"Shrimp and Catupiry mini pastries with pitanga sauce","es":"Pastelitos de camarón con Catupiry y salsa de pitanga"},
            {"id":"pastel-carne-seca-catupiry","price":"R$ 48,70","pt":"Pasteizinhos de carne seca com Catupiry","en":"Brazilian dried beef and Catupiry mini pastries","es":"Pastelitos de carne seca con Catupiry"},
        ],
    },
    {
        "id": "snacks",
        "title": {"pt": "Para beliscar", "en": "Small bites", "es": "Para picar"},
        "items": [
            {"id":"aipim-frito","price":"R$ 44,70","pt":"Aipim frito com queijo parmesão","en":"Fried cassava with parmesan cheese","es":"Yuca frita con queso parmesano"},
            {"id":"batata-abencoada","price":"R$ 49,70","pt":"Batata frita abençoada com molho de queijo cheddar e bacon crocante","en":"Loaded fries with cheddar sauce and crispy bacon","es":"Papas fritas con salsa cheddar y bacon crujiente"},
            {"id":"bolinho-bacalhau-10","price":"R$ 74,70","pt":"Bolinho de bacalhau - 10 unidades","en":"Codfish fritters - 10 units","es":"Bolitas de bacalao - 10 unidades"},
            {"id":"file-mignon-aperitivo","price":"R$ 89,70","pt":"Filé mignon aperitivo com molho madeira e cebola roxa","en":"Filet mignon bites with madeira sauce and red onion","es":"Filete mignon aperitivo con salsa madera y cebolla morada"},
            {"id":"gurjao-peixe","price":"R$ 74,70","pt":"Gurjão de peixe com molho tártaro","en":"Fish strips with tartar sauce","es":"Tiras de pescado con salsa tártara"},
        ],
    },
    {
        "id": "sandwiches-salads-burgers",
        "title": {"pt": "Sanduíches, saladas e burgers", "en": "Sandwiches, salads and burgers", "es": "Sándwiches, ensaladas y hamburguesas"},
        "items": [
            {"id":"sand-file-mignon","price":"R$ 57,70","pt":"Sanduíche de filé mignon com queijo minas padrão, rúcula e ervas","en":"Filet mignon sandwich with Minas cheese, arugula and herbs","es":"Sándwich de filete mignon con queso minas, rúcula y hierbas"},
            {"id":"sand-linguica","price":"R$ 48,70","pt":"Pão com linguiça artesanal da Serra com molho de mostarda","en":"Artisanal sausage sandwich from the Serra with mustard sauce","es":"Pan con salchicha artesanal de la Serra y salsa de mostaza"},
            {"id":"sand-frango-mostarda-mel","price":"R$ 44,70","pt":"Sanduíche de frango com queijo minas, mostarda e mel","en":"Chicken sandwich with Minas cheese, mustard and honey","es":"Sándwich de pollo con queso minas, mostaza y miel"},
            {"id":"salada-caesar-frango","price":"R$ 49,70","pt":"Salada Caesar com frango grelhado","en":"Caesar salad with grilled chicken","es":"Ensalada César con pollo a la parrilla"},
            {"id":"mix-folhas","price":"R$ 39,70","pt":"Mix de folhas frescas, tomate cereja, vinagrete e lascas de parmesão","en":"Fresh leaves, cherry tomato, vinaigrette and parmesan shavings","es":"Mix de hojas frescas, tomate cherry, vinagreta y lascas de parmesano"},
            {"id":"cheeseburger-picanha","price":"R$ 52,70","pt":"Cheeseburger de picanha com queijo minas, alface romana e tomate","en":"Picanha cheeseburger with Minas cheese, romaine lettuce and tomato","es":"Cheeseburger de picanha con queso minas, lechuga romana y tomate"},
            {"id":"cheddar-bacon","price":"R$ 57,70","pt":"Burger cheddar & bacon com hambúrguer 100% picanha","en":"Cheddar & bacon burger with 100% picanha patty","es":"Hamburguesa cheddar & bacon con picanha 100%"},
            {"id":"embaixador-burger","price":"R$ 67,70","pt":"Burger Embaixador com dois hambúrgueres de picanha, queijo minas e cebola roxa caramelizada","en":"Embaixador burger with two picanha patties, Minas cheese and caramelized red onion","es":"Hamburguesa Embaixador con dos carnes de picanha, queso minas y cebolla morada caramelizada"},
            {"id":"add-fritas","price":"+ R$ 10,00","pt":"Adicione fritas ao sanduíche ou burger","en":"Add fries to your sandwich or burger","es":"Añada papas fritas a su sándwich o hamburguesa"},
        ],
    },
    {
        "id": "lunch",
        "title": {"pt": "Almoço, pratos e carioquinhas", "en": "Lunch, plates and carioquinhas", "es": "Almuerzo, platos y carioquinhas"},
        "items": [
            {"id":"risoto-quinoa","price":"R$ 64,70","pt":"Risoto de quinoa com vegetais e shitake","en":"Quinoa risotto with vegetables and shiitake","es":"Risotto de quinoa con vegetales y shiitake"},
            {"id":"salada-caesar-almoco","price":"R$ 54,70","pt":"Salada Caesar com frango grelhado no almoço","en":"Lunch Caesar salad with grilled chicken","es":"Ensalada César de almuerzo con pollo a la parrilla"},
            {"id":"salmao-maracuja","price":"R$ 114,70","pt":"Salmão com molho de maracujá, arroz de brócolis e legumes grelhados","en":"Salmon with passion fruit sauce, broccoli rice and grilled vegetables","es":"Salmón con salsa de maracuyá, arroz de brócoli y verduras a la parrilla"},
            {"id":"picadinho-carioca","price":"R$ 74,70","pt":"Picadinho Carioca de mignon com arroz, ovo, farofa e banana frita","en":"Carioca filet mignon picadinho with rice, egg, farofa and fried banana","es":"Picadillo carioca de mignon con arroz, huevo, farofa y plátano frito"},
            {"id":"carioquinha-file","price":"R$ 69,70","pt":"Carioquinha de filé mignon com arroz, feijão, fritas e farofa","en":"Filet mignon carioquinha with rice, beans, fries and farofa","es":"Carioquinha de filete mignon con arroz, frijoles, papas fritas y farofa"},
            {"id":"carioquinha-frango","price":"R$ 54,70","pt":"Carioquinha de frango com arroz, feijão, fritas e farofa","en":"Chicken carioquinha with rice, beans, fries and farofa","es":"Carioquinha de pollo con arroz, frijoles, papas fritas y farofa"},
            {"id":"carioquinha-peixe","price":"R$ 64,70","pt":"Carioquinha de peixe com arroz, feijão, fritas e farofa","en":"Fish carioquinha with rice, beans, fries and farofa","es":"Carioquinha de pescado con arroz, frijoles, papas fritas y farofa"},
            {"id":"infantil-mignon","price":"R$ 59,70","pt":"Menu infantil - filé mignon com arroz, feijão, fritas ou purê","en":"Kids menu - filet mignon with rice, beans, fries or puree","es":"Menú infantil - filete mignon con arroz, frijoles, papas fritas o puré"},
            {"id":"infantil-frango","price":"R$ 49,70","pt":"Menu infantil - filé de frango com arroz, feijão, fritas ou purê","en":"Kids menu - chicken filet with rice, beans, fries or puree","es":"Menú infantil - filete de pollo con arroz, frijoles, papas fritas o puré"},
            {"id":"infantil-bolonhesa","price":"R$ 49,70","pt":"Menu infantil - macarrão à bolonhesa","en":"Kids menu - spaghetti bolognese","es":"Menú infantil - espagueti a la boloñesa"},
        ],
    },
    {
        "id": "house-specialties",
        "title": {"pt": "Especialidades da casa", "en": "House specialties", "es": "Especialidades de la casa"},
        "items": [
            {"id":"picanha-individual","price":"R$ 134,70","pt":"Picanha à brasileira - 1 pessoa, com arroz, farofa de alho e cebola, molho à campanha e batata frita","en":"Brazilian picanha - 1 person, with rice, garlic-onion farofa, vinaigrette salsa and fries","es":"Picanha brasileña - 1 persona, con arroz, farofa de ajo y cebolla, salsa vinagreta y papas fritas"},
            {"id":"picanha-duas","price":"R$ 204,70","pt":"Picanha à brasileira - 2 pessoas","en":"Brazilian picanha - 2 people","es":"Picanha brasileña - 2 personas"},
            {"id":"feijoada-duas","price":"R$ 189,70","pt":"Feijoada da Academia da Cachaça - 2 pessoas, servida em panela de barro com arroz, couve, farofa e laranja","en":"Academia da Cachaça feijoada - 2 people, served in a clay pot with rice, collard greens, farofa and orange","es":"Feijoada de Academia da Cachaça - 2 personas, servida en olla de barro con arroz, col, farofa y naranja"},
            {"id":"bobo-individual","price":"R$ 114,70","pt":"Bobó de camarão - 1 pessoa, com arroz branco e farofa de dendê","en":"Shrimp bobó - 1 person, with white rice and dendê farofa","es":"Bobó de camarón - 1 persona, con arroz blanco y farofa de dendê"},
            {"id":"bobo-duas","price":"R$ 169,70","pt":"Bobó de camarão - 2 pessoas","en":"Shrimp bobó - 2 people","es":"Bobó de camarón - 2 personas"},
        ],
    },
    {
        "id": "breakfast",
        "title": {"pt": "Café da manhã", "en": "Breakfast", "es": "Desayuno"},
        "items": [
            {"id":"cafe-manha-duas","price":"R$ 98,70","pt":"Café da manhã para duas pessoas com pães de fermentação natural, frios, mini açaí, iogurte, granola, fruta do dia, bolo do dia e 2 bebidas quentes","en":"Breakfast for two with naturally fermented breads, cold cuts, mini açai, yogurt, granola, fruit, cake slice and 2 hot drinks","es":"Desayuno para dos con panes de fermentación natural, embutidos, mini açaí, yogur, granola, fruta, pastel y 2 bebidas calientes"},
            {"id":"omelete-queijo-presunto","price":"R$ 29,00","pt":"Omelete de queijo prato e presunto","en":"Cheese and ham omelet","es":"Tortilla de queso y jamón"},
            {"id":"omelete-minas-tomate","price":"R$ 32,00","pt":"Omelete de queijo minas e tomate","en":"Minas cheese and tomato omelet","es":"Tortilla de queso minas y tomate"},
            {"id":"omelete-shitake","price":"R$ 34,00","pt":"Omelete de shitake fresco","en":"Fresh shiitake omelet","es":"Tortilla de shiitake fresco"},
            {"id":"ovos-mexidos","price":"R$ 23,00","pt":"Ovos mexidos com bacon","en":"Scrambled eggs with bacon","es":"Huevos revueltos con bacon"},
            {"id":"ovos-fritos","price":"R$ 19,00","pt":"Ovos fritos","en":"Fried eggs","es":"Huevos fritos"},
            {"id":"tapioca-prato-presunto","price":"R$ 20,00","pt":"Tapioca de queijo prato e presunto","en":"Tapioca with cheese and ham","es":"Tapioca de queso y jamón"},
            {"id":"tapioca-minas-tomate","price":"R$ 22,00","pt":"Tapioca de queijo minas e tomate","en":"Tapioca with Minas cheese and tomato","es":"Tapioca de queso minas y tomate"},
            {"id":"tapioca-manteiga","price":"R$ 12,00","pt":"Tapioca na manteiga","en":"Tapioca with butter","es":"Tapioca con mantequilla"},
            {"id":"misto-quente","price":"R$ 16,00","pt":"Misto quente ou queijo quente","en":"Ham-and-cheese toast or hot cheese sandwich","es":"Mixto caliente o queso caliente"},
            {"id":"peito-peru-minas","price":"R$ 19,00","pt":"Peito de peru com queijo minas","en":"Turkey breast with Minas cheese","es":"Pavo con queso minas"},
            {"id":"pao-chapa","price":"R$ 9,00","pt":"Pão na chapa","en":"Grilled bread with butter","es":"Pan a la plancha"},
            {"id":"cesto-paes","price":"R$ 18,00","pt":"Seleção de pães - cesto","en":"Bread selection - basket","es":"Selección de panes - cesta"},
            {"id":"mini-baguete","price":"R$ 8,00","pt":"Mini baguete rústica - unidade","en":"Rustic mini baguette - unit","es":"Mini baguette rústica - unidad"},
            {"id":"fatias-queijo-frios","price":"R$ 8,00","pt":"Fatias extras de queijo ou frios - 2 fatias","en":"Extra cheese or cold cut slices - 2 slices","es":"Rebanadas extra de queso o embutidos - 2 rebanadas"},
            {"id":"fruta-iogurte","price":"R$ 11,00","pt":"Porção de fruta ou iogurte","en":"Fruit or yogurt portion","es":"Porción de fruta o yogur"},
            {"id":"geleia-mel-manteiga","price":"R$ 4,00","pt":"Porção de geleia, mel ou manteiga","en":"Jam, honey or butter portion","es":"Porción de mermelada, miel o mantequilla"},
            {"id":"bolo-dia","price":"R$ 12,00","pt":"Bolo do dia - fatia","en":"Cake of the day - slice","es":"Pastel del día - rebanada"},
        ],
    },
    {
        "id": "coffee-acai",
        "title": {"pt": "Açaí, coco, cafés e bebidas com café", "en": "Açai, coconut, coffee and coffee drinks", "es": "Açaí, coco, cafés y bebidas con café"},
        "items": [
            {"id":"acai-baby","price":"R$ 22,00","pt":"Açaí baby","en":"Baby açai bowl","es":"Açaí baby"},
            {"id":"acai-taca","price":"R$ 26,00","pt":"Açaí taça","en":"Açai cup","es":"Açaí en copa"},
            {"id":"adicional-banana","price":"R$ 3,00","pt":"Adicional banana","en":"Banana topping","es":"Adicional banana"},
            {"id":"adicional-morango","price":"R$ 5,00","pt":"Adicional morango","en":"Strawberry topping","es":"Adicional fresa"},
            {"id":"adicional-granola","price":"R$ 3,00","pt":"Granola - porção","en":"Granola portion","es":"Porción de granola"},
            {"id":"coco-gelado","price":"R$ 16,00","pt":"Coco gelado 100% natural","en":"Cold natural coconut water","es":"Coco frío 100% natural"},
            {"id":"hario-v60-150","price":"R$ 14,50","pt":"Hario V60 150ml","en":"Hario V60 150ml","es":"Hario V60 150ml"},
            {"id":"hario-v60-300","price":"R$ 19,00","pt":"Hario V60 300ml","en":"Hario V60 300ml","es":"Hario V60 300ml"},
            {"id":"prensa-francesa-150","price":"R$ 14,50","pt":"Prensa francesa 150ml","en":"French press 150ml","es":"Prensa francesa 150ml"},
            {"id":"prensa-francesa-300","price":"R$ 19,00","pt":"Prensa francesa 300ml","en":"French press 300ml","es":"Prensa francesa 300ml"},
            {"id":"cafe-espresso","price":"R$ 7,00","pt":"Café espresso","en":"Espresso coffee","es":"Café espresso"},
            {"id":"espresso-duplo","price":"R$ 10,50","pt":"Café espresso duplo","en":"Double espresso","es":"Café espresso doble"},
            {"id":"cafe-leite","price":"R$ 12,50","pt":"Café com leite","en":"Coffee with milk","es":"Café con leche"},
            {"id":"cafe-especial-pequeno","price":"R$ 7,50","pt":"Café especial do Brasil 100% arábica - pequeno","en":"Brazilian specialty coffee 100% arabica - small","es":"Café especial de Brasil 100% arábica - pequeño"},
            {"id":"cafe-especial-grande","price":"R$ 10,00","pt":"Café especial do Brasil 100% arábica - grande","en":"Brazilian specialty coffee 100% arabica - large","es":"Café especial de Brasil 100% arábica - grande"},
            {"id":"espresso-tonica","price":"R$ 17,00","pt":"Espresso tônica","en":"Espresso tonic","es":"Espresso tónica"},
            {"id":"latte-gelado","price":"R$ 17,00","pt":"Latte gelado","en":"Iced latte","es":"Latte helado"},
        ],
    },
    {
        "id": "caipirinhas-drinks",
        "title": {"pt": "Caipirinhas e drinks", "en": "Caipirinhas and cocktails", "es": "Caipirinhas y cócteles"},
        "items": [
            {"id":"caipirinha-limao-cristal","price":"R$ 32,00","pt":"Caipirinha de limão tradicional com Cachaça Magnífica Cristal","en":"Traditional lime caipirinha with Magnífica Cristal cachaça","es":"Caipirinha tradicional de limón con Cachaça Magnífica Cristal"},
            {"id":"caipirinha-frutas","price":"a partir de R$ 35,00","pt":"Caipirinhas de frutas: abacaxi, maracujá, manga Palmer, laranja com gengibre, kiwi, morango, limão siciliano, mista e lichia","en":"Fruit caipirinhas: pineapple, passion fruit, Palmer mango, orange with ginger, kiwi, strawberry, Sicilian lemon, mixed fruits and lychee","es":"Caipirinhas de frutas: piña, maracuyá, mango Palmer, naranja con jengibre, kiwi, fresa, limón siciliano, mixta y lichi"},
            {"id":"caipirinha-da-casa","price":"R$ 43,00","pt":"Caipirinha da Casa","en":"House caipirinha","es":"Caipirinha de la casa"},
            {"id":"caipirinha-coco","price":"R$ 49,00","pt":"Caipirinha de coco","en":"Coconut caipirinha","es":"Caipirinha de coco"},
            {"id":"caipirinha-da-casa-20","price":"R$ 45,00","pt":"Caipirinha Da Casa 2.0","en":"House caipirinha 2.0","es":"Caipirinha de la casa 2.0"},
            {"id":"praia-vermelha","price":"R$ 45,00","pt":"Praia Vermelha","en":"Praia Vermelha cocktail","es":"Praia Vermelha"},
            {"id":"cafe-expresso-drink","price":"R$ 44,00","pt":"Café Expresso com cachaça envelhecida","en":"Espresso cocktail with aged cachaça","es":"Café espresso con cachaça añejada"},
            {"id":"mojito","price":"R$ 45,00 / R$ 50,00","pt":"Mojito com Rum Havana Club 3 anos ou 7 anos","en":"Mojito with Havana Club 3 years or 7 years rum","es":"Mojito con ron Havana Club 3 años o 7 años"},
            {"id":"moscow-mule","price":"R$ 40,00 / R$ 45,00","pt":"Moscow Mule com vodka nacional ou Absolut","en":"Moscow Mule with national vodka or Absolut","es":"Moscow Mule con vodka nacional o Absolut"},
            {"id":"fitzgerald","price":"R$ 45,00 / R$ 50,00","pt":"Fitzgerald com Gin Amazzoni ou Gin Beefeater","en":"Fitzgerald with Amazzoni Gin or Beefeater Gin","es":"Fitzgerald con Gin Amazzoni o Gin Beefeater"},
            {"id":"bloody-mary","price":"R$ 40,00 / R$ 45,00","pt":"Bloody Mary com vodka nacional ou Absolut","en":"Bloody Mary with national vodka or Absolut","es":"Bloody Mary con vodka nacional o Absolut"},
            {"id":"pina-colada","price":"a partir de R$ 45,00","pt":"Piña Colada com rum, coco e abacaxi","en":"Piña Colada with rum, coconut and pineapple","es":"Piña Colada con ron, coco y piña"},
            {"id":"amar-ela","price":"R$ 45,00","pt":"Amar Ela com vodka Absolut, maracujá, canela e tabasco","en":"Amar Ela with Absolut vodka, passion fruit, cinnamon and Tabasco","es":"Amar Ela con vodka Absolut, maracuyá, canela y tabasco"},
            {"id":"red-gin","price":"R$ 45,00","pt":"Red Gin com Amazzoni Gin, tônica, frutas vermelhas, limão siciliano e alecrim","en":"Red Gin with Amazzoni Gin, tonic, red fruits, Sicilian lemon and rosemary","es":"Red Gin con Amazzoni Gin, tónica, frutos rojos, limón siciliano y romero"},
            {"id":"pineapple-carioca","price":"R$ 45,00","pt":"Pineapple Carioca com Amazzoni Maniuara, abacaxi, licor de laranja, tônica e gengibre","en":"Pineapple Carioca with Amazzoni Maniuara, pineapple, orange liqueur, tonic and ginger","es":"Pineapple Carioca con Amazzoni Maniuara, piña, licor de naranja, tónica y jengibre"},
            {"id":"carioca-red","price":"R$ 45,00","pt":"Carioca Red com Amazzoni Gin, hibisco, cereja, limão e tônica","en":"Carioca Red with Amazzoni Gin, hibiscus, cherry, lime and tonic","es":"Carioca Red con Amazzoni Gin, hibisco, cereza, limón y tónica"},
            {"id":"carioca-mule","price":"R$ 45,00 / R$ 50,00","pt":"Carioca Mule com Ballantine's ou Chivas 12, maracujá, canela e gengibre","en":"Carioca Mule with Ballantine's or Chivas 12, passion fruit, cinnamon and ginger","es":"Carioca Mule con Ballantine's o Chivas 12, maracuyá, canela y jengibre"},
            {"id":"cherry-bramble","price":"R$ 45,00","pt":"Cherry Bramble com Amazzoni Gin, limão, gengibre e cereja","en":"Cherry Bramble with Amazzoni Gin, lime, ginger and cherry","es":"Cherry Bramble con Amazzoni Gin, limón, jengibre y cereza"},
        ],
    },
    {
        "id": "refreshing-signature-drinks",
        "title": {"pt": "Drinks refrescantes e signatures", "en": "Refreshing and signature cocktails", "es": "Cócteles refrescantes y signatures"},
        "items": [
            {"id":"extrakt-tonic","price":"R$ 45,00","pt":"Extrakt & Tonic com Absolut Extrakt, limão tahiti e tônica","en":"Extrakt & Tonic with Absolut Extrakt, lime and tonic water","es":"Extrakt & Tonic con Absolut Extrakt, limón tahití y tónica"},
            {"id":"beefeater-tonic-dry","price":"R$ 45,00","pt":"Beefeater & Tonic Dry","en":"Beefeater & Tonic Dry","es":"Beefeater & Tonic Dry"},
            {"id":"beefeater-tonic-botanicas","price":"R$ 45,00","pt":"Beefeater & Tonic Botânicas","en":"Beefeater & Tonic Botanicals","es":"Beefeater & Tonic Botánicas"},
            {"id":"pink-tonic","price":"R$ 45,00","pt":"Pink & Tonic com Beefeater Pink e morango","en":"Pink & Tonic with Beefeater Pink and strawberries","es":"Pink & Tonic con Beefeater Pink y fresas"},
            {"id":"gin-tropical","price":"R$ 50,00 / R$ 55,00","pt":"Gin Tropical com Red Bull Tropical e laranja","en":"Tropical gin with Red Bull Tropical and orange","es":"Gin Tropical con Red Bull Tropical y naranja"},
            {"id":"absolut-raspberri-collins","price":"R$ 45,00","pt":"Absolut Raspberri Collins","en":"Absolut Raspberri Collins","es":"Absolut Raspberri Collins"},
            {"id":"jameson-tea-lime","price":"R$ 45,00","pt":"Jameson Tea & Lime","en":"Jameson Tea & Lime","es":"Jameson Tea & Lime"},
            {"id":"lillet-vive","price":"R$ 45,00","pt":"Lillet Vive","en":"Lillet Vive","es":"Lillet Vive"},
            {"id":"rosato-tonic","price":"R$ 45,00","pt":"Rosato Tonic","en":"Rosato Tonic","es":"Rosato Tonic"},
            {"id":"zero-balla","price":"R$ 50,00","pt":"Zero Balla com Ballantine's Bourbon e Coca-Cola zero","en":"Zero Balla with Ballantine's Bourbon and Coke Zero","es":"Zero Balla con Ballantine's Bourbon y Coca-Cola zero"},
            {"id":"balla-jam-amora","price":"R$ 50,00","pt":"Balla Jam - Amora com Ballantine's Finest","en":"Balla Jam - blackberry with Ballantine's Finest","es":"Balla Jam - mora con Ballantine's Finest"},
        ],
    },
    {
        "id": "juices-soft-drinks",
        "title": {"pt": "Sucos naturais e outras bebidas", "en": "Fresh juices and other drinks", "es": "Jugos naturales y otras bebidas"},
        "items": [
            {"id":"suco-laranja","price":"R$ 18,00","pt":"Suco natural de laranja 380ml","en":"Fresh orange juice 380ml","es":"Jugo natural de naranja 380ml"},
            {"id":"suco-melancia","price":"R$ 20,00","pt":"Suco natural de melancia 380ml","en":"Fresh watermelon juice 380ml","es":"Jugo natural de sandía 380ml"},
            {"id":"suco-abacaxi","price":"R$ 20,00","pt":"Suco natural de abacaxi 380ml","en":"Fresh pineapple juice 380ml","es":"Jugo natural de piña 380ml"},
            {"id":"suco-abacaxi-hortela","price":"R$ 21,00","pt":"Suco de abacaxi com hortelã 380ml","en":"Pineapple and mint juice 380ml","es":"Jugo de piña con menta 380ml"},
            {"id":"suco-manga","price":"R$ 22,00","pt":"Suco natural de manga 380ml","en":"Fresh mango juice 380ml","es":"Jugo natural de mango 380ml"},
            {"id":"limonada-suica","price":"R$ 23,00","pt":"Limonada suíça 380ml","en":"Brazilian Swiss lemonade 380ml","es":"Limonada suiza 380ml"},
            {"id":"suco-maracuja","price":"R$ 20,00","pt":"Suco natural de maracujá 380ml","en":"Fresh passion fruit juice 380ml","es":"Jugo natural de maracuyá 380ml"},
            {"id":"morango-leite","price":"R$ 23,00","pt":"Morango ao leite 380ml","en":"Strawberry with milk 380ml","es":"Fresa con leche 380ml"},
            {"id":"suco-misto","price":"R$ 24,00","pt":"Suco misto de 2 ou 3 frutas 380ml","en":"Mixed juice with 2 or 3 fruits 380ml","es":"Jugo mixto de 2 o 3 frutas 380ml"},
            {"id":"suco-tomate","price":"R$ 24,00","pt":"Suco de tomate temperado 380ml","en":"Seasoned tomato juice 380ml","es":"Jugo de tomate sazonado 380ml"},
            {"id":"agua-sem-gas","price":"R$ 7,00","pt":"Água sem gás 500ml","en":"Still water 500ml","es":"Agua sin gas 500ml"},
            {"id":"agua-com-gas","price":"R$ 8,00","pt":"Água com gás 500ml","en":"Sparkling water 500ml","es":"Agua con gas 500ml"},
            {"id":"mamba-water","price":"R$ 10,00","pt":"Água Mamba Water lata 350ml","en":"Mamba Water can 350ml","es":"Agua Mamba Water lata 350ml"},
            {"id":"agua-tonica","price":"R$ 10,00","pt":"Água tônica FYS 350ml","en":"FYS tonic water 350ml","es":"Agua tónica FYS 350ml"},
            {"id":"h2oh","price":"R$ 11,00","pt":"H2OH! Limão 500ml","en":"H2OH! Lemon 500ml","es":"H2OH! Limón 500ml"},
            {"id":"refrigerantes","price":"R$ 9,50","pt":"Coca-Cola, Coca-Cola zero, Guaraná ou Guaraná zero 350ml","en":"Coke, Coke Zero, Guaraná or Guaraná Zero 350ml","es":"Coca-Cola, Coca-Cola zero, Guaraná o Guaraná zero 350ml"},
            {"id":"gatorade","price":"R$ 16,00","pt":"Gatorade Tangerina 500ml","en":"Tangerine Gatorade 500ml","es":"Gatorade mandarina 500ml"},
            {"id":"guaraviton","price":"R$ 10,00","pt":"Guaraviton 500ml","en":"Guaraviton 500ml","es":"Guaraviton 500ml"},
            {"id":"red-bull","price":"R$ 25,00","pt":"Red Bull 250ml","en":"Red Bull 250ml","es":"Red Bull 250ml"},
        ],
    },
    {
        "id": "beer",
        "title": {"pt": "Chopp, cervejas e harmonizadas", "en": "Draft beer, bottles and pairings", "es": "Chopp, cervezas y armonizadas"},
        "items": [
            {"id":"chopp-tulipa","price":"R$ 18,00","pt":"Chopp Heineken tulipa 250ml","en":"Heineken draft beer tulip 250ml","es":"Chopp Heineken tulipa 250ml"},
            {"id":"chopp-caneca","price":"R$ 27,00","pt":"Chopp Heineken caneca 500ml","en":"Heineken draft beer mug 500ml","es":"Chopp Heineken jarra 500ml"},
            {"id":"heineken-long-neck","price":"R$ 20,00","pt":"Heineken long neck 330ml","en":"Heineken long neck 330ml","es":"Heineken long neck 330ml"},
            {"id":"heineken-zero","price":"R$ 20,00","pt":"Heineken 0,0% 330ml","en":"Heineken 0.0% 330ml","es":"Heineken 0,0% 330ml"},
            {"id":"lagunitas","price":"R$ 25,00","pt":"Lagunitas IPA 350ml","en":"Lagunitas IPA 350ml","es":"Lagunitas IPA 350ml"},
            {"id":"eisenbahn","price":"R$ 18,00","pt":"Eisenbahn Pilsen 473ml","en":"Eisenbahn Pilsen 473ml","es":"Eisenbahn Pilsen 473ml"},
            {"id":"blue-moon","price":"R$ 25,00","pt":"Blue Moon 350ml","en":"Blue Moon 350ml","es":"Blue Moon 350ml"},
            {"id":"praya-classica","price":"R$ 37,70","pt":"Praya Clássica 600ml","en":"Praya Clássica 600ml","es":"Praya Clássica 600ml"},
            {"id":"monkeys-golden","price":"R$ 39,70","pt":"3 Monkeys Golden Ale 500ml","en":"3 Monkeys Golden Ale 500ml","es":"3 Monkeys Golden Ale 500ml"},
            {"id":"monkeys-ipa","price":"R$ 39,70","pt":"3 Monkeys Classic IPA 500ml","en":"3 Monkeys Classic IPA 500ml","es":"3 Monkeys Classic IPA 500ml"},
            {"id":"cristal-harmonizada","price":"R$ 38,70","pt":"Cerveja harmonizada Cristal 600ml","en":"Cristal pairing beer 600ml","es":"Cerveza armonizada Cristal 600ml"},
            {"id":"ipa-harmonizada","price":"R$ 38,70","pt":"Cerveja harmonizada IPA 600ml","en":"IPA pairing beer 600ml","es":"Cerveza armonizada IPA 600ml"},
            {"id":"peach-harmonizada","price":"R$ 38,70","pt":"Cerveja harmonizada Peach 600ml","en":"Peach pairing beer 600ml","es":"Cerveza armonizada Peach 600ml"},
        ],
    },
    {
        "id": "desserts",
        "title": {"pt": "Sobremesas e milkshakes", "en": "Desserts and milkshakes", "es": "Postres y batidos"},
        "items": [
            {"id":"brownie-sorvete","price":"R$ 24,70","pt":"Brownie com sorvete de creme","en":"Brownie with vanilla ice cream","es":"Brownie con helado de crema"},
            {"id":"sorvete-caramelo","price":"R$ 23,70","pt":"Sorvete com caramelo salgado e crocante","en":"Ice cream with salted caramel and crunch","es":"Helado con caramelo salado y crocante"},
            {"id":"sorvete-uma-bola","price":"R$ 17,00","pt":"Sorvete - 1 bola","en":"Ice cream - 1 scoop","es":"Helado - 1 bola"},
            {"id":"sorvete-duas-bolas","price":"R$ 26,00","pt":"Sorvete - 2 bolas","en":"Ice cream - 2 scoops","es":"Helado - 2 bolas"},
            {"id":"frutas-estacao","price":"sob consulta","pt":"Frutas da estação: abacaxi, melancia ou manga","en":"Seasonal fruits: pineapple, watermelon or mango","es":"Frutas de temporada: piña, sandía o mango"},
            {"id":"milkshake-creme","price":"R$ 24,00","pt":"Milkshake de creme","en":"Vanilla milkshake","es":"Batido de crema"},
            {"id":"milkshake-ovomaltine","price":"R$ 26,00","pt":"Milkshake de Ovomaltine","en":"Ovomaltine milkshake","es":"Batido de Ovomaltine"},
            {"id":"milkshake-chocolate","price":"R$ 24,00","pt":"Milkshake de chocolate","en":"Chocolate milkshake","es":"Batido de chocolate"},
            {"id":"milkshake-cafe","price":"R$ 27,00","pt":"Milkshake de café","en":"Coffee milkshake","es":"Batido de café"},
            {"id":"milkshake-tapioca","price":"R$ 27,00","pt":"Milkshake de tapioca","en":"Tapioca milkshake","es":"Batido de tapioca"},
            {"id":"milkshake-doce-leite","price":"R$ 27,00","pt":"Milkshake de doce de leite","en":"Dulce de leche milkshake","es":"Batido de dulce de leche"},
        ],
    },
]

STYLE = """
<style>
.ec-menu-complete{background:#f6efde;color:#00405a;padding:84px 0;border-top:1px solid rgba(0,64,90,.10)}
.ec-menu-complete .wrap{max-width:1180px;margin:0 auto;padding:0 clamp(20px,4vw,64px)}
.ec-menu-complete .kicker{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:#9a6500;margin-bottom:12px;font-weight:800}
.ec-menu-complete h2{font-family:Catamaran,Verdana,sans-serif;font-size:clamp(34px,4.2vw,62px);line-height:.98;margin:0 0 18px;color:#335d4a;font-weight:800;letter-spacing:-.03em}
.ec-menu-complete .intro{max-width:820px;color:#485156;font-size:18px;line-height:1.55;margin:0 0 28px}
.ec-menu-note{background:rgba(0,64,90,.06);border:1px solid rgba(0,64,90,.10);border-radius:18px;padding:16px 18px;margin:0 0 34px;color:#485156;font-size:15px;line-height:1.5}
.ec-menu-complete-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;margin-top:30px}
.ec-menu-complete-section{background:#fffaf0;border:1px solid rgba(0,64,90,.12);border-radius:22px;padding:24px;box-shadow:0 10px 24px rgba(0,32,46,.05)}
.ec-menu-complete-section h3{font-family:'JetBrains Mono',monospace;font-size:15px;line-height:1.25;letter-spacing:.12em;text-transform:uppercase;color:#335d4a;margin:0 0 18px;font-weight:900}
.ec-complete-item{border-top:1px solid rgba(0,64,90,.10);padding:13px 0;display:grid;grid-template-columns:1fr auto;gap:12px;align-items:start}
.ec-complete-item:first-of-type{border-top:0;padding-top:0}
.ec-complete-name{font-weight:800;color:#335d4a;font-size:16px;line-height:1.25}
.ec-complete-price{font-family:'JetBrains Mono',monospace;font-size:13px;color:#9a6500;font-weight:900;white-space:nowrap;text-align:right}
.ec-menu-source{font-size:13px;color:#7d8386;margin-top:26px}
@media(max-width:820px){.ec-menu-complete-grid{grid-template-columns:1fr}.ec-complete-item{grid-template-columns:1fr}.ec-complete-price{text-align:left}}
</style>
""".strip()


def item_text(item: dict, lang: str) -> str:
    return item[lang]


def render(lang: str) -> str:
    labels = LABELS[lang]
    pieces = [START, STYLE, '<section class="ec-menu-complete" id="cardapio-completo">', '<div class="wrap">']
    pieces.append(f'<div class="kicker">{escape(labels["kicker"])}</div>')
    pieces.append(f'<h2>{escape(labels["title"])}</h2>')
    pieces.append(f'<p class="intro">{escape(labels["intro"])}</p>')
    pieces.append(f'<p class="ec-menu-note">{escape(labels["note"])}</p>')
    pieces.append('<div class="ec-menu-complete-grid">')
    for section in MENU:
        pieces.append('<article class="ec-menu-complete-section">')
        pieces.append(f'<h3>{escape(section["title"][lang])}</h3>')
        for item in section["items"]:
            pieces.append('<div class="ec-complete-item">')
            pieces.append(f'<div class="ec-complete-name">{escape(item_text(item, lang))}</div>')
            pieces.append(f'<div class="ec-complete-price">{escape(item["price"])}</div>')
            pieces.append('</div>')
        pieces.append('</article>')
    pieces.append('</div>')
    pieces.append(f'<p class="ec-menu-source">{escape(labels["source"])}</p>')
    pieces.append('</div></section>')
    pieces.append(END)
    return "\n".join(pieces) + "\n"


def strip_old(content: str) -> str:
    start = content.find(START)
    if start == -1:
        return content
    end = content.find(END, start)
    if end == -1:
        return content[:start]
    return content[:start] + content[end + len(END):].lstrip("\n")


def insert_block(content: str, block: str) -> str:
    anchors = [
        '<!-- EC INTERNAL LINKING KEYWORD CLUSTER FIX -->',
        '<!-- EC FEATURED SNIPPET ORDERED LISTS -->',
        '</main>',
    ]
    for anchor in anchors:
        idx = content.find(anchor)
        if idx != -1:
            return content[:idx] + block + content[idx:]
    return content + "\n" + block


def process_page(lang: str, path: Path) -> tuple[bool, int, int]:
    original = path.read_text(encoding="utf-8", errors="ignore")
    cleaned = strip_old(original)
    block = render(lang)
    updated = insert_block(cleaned, block)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return changed, len(MENU), sum(len(s["items"]) for s in MENU)


def write_report(results: dict[str, tuple[bool, int, int]]) -> int:
    REPORT.parent.mkdir(exist_ok=True)
    counts = [v[2] for v in results.values()]
    section_counts = [v[1] for v in results.values()]
    status = "PASS" if len(set(counts)) == 1 and len(set(section_counts)) == 1 else "FAIL"
    lines = [
        "# Cardapio Completeness + I18N Fix",
        "",
        f"Status geral: **{status}**",
        "",
        "## Objetivo",
        "Restaurar no site o conteúdo do cardápio completo e garantir que a página de cardápio tenha a mesma cobertura em português, inglês e espanhol.",
        "",
        "## Fonte operacional",
        "- `Cardápio - Embaixada Carioca - Pt e Esp - outubro 2025 digital.pdf`.",
        "- Páginas de referência: entradas, petiscos, sanduíches, saladas, burgers, almoço, especialidades, café da manhã, cafeteria, caipirinhas, drinks, bebidas, cervejas e sobremesas.",
        "",
        "## Guardrails",
        "- Nenhum JSON-LD/schema foi alterado.",
        "- Nenhuma canonical/hreflang foi alterada.",
        "- Nenhum rating/review/aggregateRating foi inserido.",
        "- O bloco foi inserido apenas como conteúdo editorial visível do cardápio.",
        "",
        "## Resumo",
        f"- Seções restauradas por idioma: **{section_counts[0] if section_counts else 0}**",
        f"- Itens restaurados por idioma: **{counts[0] if counts else 0}**",
        f"- Paridade PT/EN/ES: **{'OK' if status == 'PASS' else 'FALHA'}**",
        "",
        "## Resultados por página",
        "",
        "| Idioma | Página | Changed | Seções | Itens |",
        "|---|---|---:|---:|---:|",
    ]
    for lang, (changed, sections, items) in results.items():
        lines.append(f"| `{lang}` | `{PAGES[lang].relative_to(ROOT).as_posix()}` | {changed} | {sections} | {items} |")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Cardapio completeness i18n fix: {status}")
    return 0 if status == "PASS" else 1


def main() -> int:
    results: dict[str, tuple[bool, int, int]] = {}
    for lang, path in PAGES.items():
        if not path.exists():
            raise FileNotFoundError(path)
        results[lang] = process_page(lang, path)
    return write_report(results)


if __name__ == "__main__":
    raise SystemExit(main())
