import os
from pathlib import Path

# Dados para EN
pages_data_en = {
    'en/cafe-da-manha-pao-de-acucar.html': {
        'title': 'Breakfast with a View in Rio de Janeiro | Embaixada Carioca',
        'desc': 'Where to have breakfast with a view in Rio? Embaixada Carioca serves breakfast every day at Morro da Urca, overlooking Sugarloaf Mountain.',
        'h1': 'Breakfast with a View in Rio de Janeiro',
        'h1_sub': 'The best way to start your day at Sugarloaf Mountain.',
        'resposta': '<strong>Embaixada Carioca</strong> is the only restaurant inside the Sugarloaf Cable Car Park that serves a full breakfast with a panoramic front view of Sugarloaf Mountain and Guanabara Bay. Served <strong>every day</strong>, from 8:30 AM to 11:30 AM.',
        'roteiro_title': 'How to fit it into your itinerary',
        'roteiro': [
            ('8:00 AM', 'Arrive at the Praia Vermelha ticket office right at opening to avoid lines.'),
            ('8:20 AM', 'Take one of the first cable cars to Morro da Urca (first stop).'),
            ('8:30 - 9:30 AM', 'Have your breakfast at Embaixada Carioca with the terrace still empty and the best light for photos.'),
            ('9:45 AM', 'Take the second cable car to the top of Sugarloaf Mountain with your energy recharged.')
        ],
        'cardapio_title': 'What to order for Breakfast',
        'cardapio_desc': 'Our menu includes à la carte options and full combos for 2 people. Highlights:',
        'cardapio_items': ['Artisanal sourdough breads', 'Creamy scrambled eggs', 'Fresh tropical fruits', 'Natural juices and specialty coffee', 'The classic warm cheese bread (pão de queijo)'],
        'faq': [
            ('Do I need to pay for the cable car to have breakfast?', 'Yes, the restaurant is located at Morro da Urca (1st stop), so a Sugarloaf Park ticket is required.'),
            ('Do I need a reservation?', 'We strongly recommend booking, especially on weekends, to secure the best tables on the terrace with a view.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Breakfast at Embaixada Carioca',
        'slug': 'en/cafe-da-manha-pao-de-acucar.html',
        'lang': 'en',
        'eyebrow': 'Cable Car Restaurant · Traditional Carioca Restaurant · Morro da Urca · Parque Bondinho Sugarloaf Mountain · Rio de Janeiro · Brazil',
        'nav_home': 'Home',
        'nav_links': [
            ('en/cafe-da-manha.html', 'Breakfast'),
            ('en/almoco.html', 'Lunch'),
            ('en/entardecer.html', 'Sunset'),
            ('en/eventos.html', 'Events'),
            ('en/cardapio.html', 'Menu'),
            ('en/guia-do-rio.html', 'Rio Guide')
        ],
        'btn_reserve': 'Book a Table →',
        'btn_reserve_full': 'Book a Table Now',
        'resposta_title': 'The Quick Answer',
        'garanta_title': 'Secure your table with a view',
        'garanta_desc': 'We recommend booking in advance to secure the best seats on the terrace.',
        'faq_title': 'Frequently Asked Questions'
    },
    'en/almoco-morro-da-urca.html': {
        'title': 'Where to Lunch at Morro da Urca and Sugarloaf | Embaixada Carioca',
        'desc': 'Looking for where to have lunch at Morro da Urca? Embaixada Carioca offers the best Brazilian gastronomy with a panoramic view at Sugarloaf Mountain.',
        'h1': 'Where to Lunch at Morro da Urca',
        'h1_sub': 'Brazilian gastronomy with the best view in Rio.',
        'resposta': '<strong>Embaixada Carioca</strong> is the top choice for lunch at Morro da Urca. Located at the first cable car stop, it offers classic Brazilian dishes, such as the famous Grilled Picanha and Award-winning Feijoada, with a panoramic view of Guanabara Bay.',
        'roteiro_title': 'How to fit lunch into your tour',
        'roteiro': [
            ('10:00 AM', 'Take the first cable car up to Morro da Urca and explore the area.'),
            ('11:00 AM', 'Take the second cable car to the top of Sugarloaf Mountain.'),
            ('12:30 PM', 'Head back down to Morro da Urca.'),
            ('1:00 PM', 'Have a relaxed lunch at Embaixada Carioca before heading down to Praia Vermelha.')
        ],
        'cardapio_title': 'Lunch Highlights',
        'cardapio_desc': 'Our specialty is authentic Carioca and Brazilian cuisine. The most ordered dishes:',
        'cardapio_items': ['Grilled Picanha (our best-selling dish)', 'Award-winning Feijoada (served every day)', 'Picadinho Carioca (traditional beef stew)', 'Authentic Cod Fritters (Bolinho de Bacalhau)', 'Heineken Draft Beer (voted 2nd best in Brazil)'],
        'faq': [
            ('What are the lunch hours?', 'We serve lunch every day, from 11:30 AM to 4:00 PM. After this time, the snacks and dinner menu remains available.'),
            ('Do you accept large groups?', 'Yes! We have the infrastructure to host tour groups and large families. We recommend booking in advance.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Lunch at Embaixada Carioca',
        'slug': 'en/almoco-morro-da-urca.html',
        'lang': 'en',
        'eyebrow': 'Cable Car Restaurant · Traditional Carioca Restaurant · Morro da Urca · Parque Bondinho Sugarloaf Mountain · Rio de Janeiro · Brazil',
        'nav_home': 'Home',
        'nav_links': [
            ('en/cafe-da-manha.html', 'Breakfast'),
            ('en/almoco.html', 'Lunch'),
            ('en/entardecer.html', 'Sunset'),
            ('en/eventos.html', 'Events'),
            ('en/cardapio.html', 'Menu'),
            ('en/guia-do-rio.html', 'Rio Guide')
        ],
        'btn_reserve': 'Book a Table →',
        'btn_reserve_full': 'Book a Table Now',
        'resposta_title': 'The Quick Answer',
        'garanta_title': 'Secure your table with a view',
        'garanta_desc': 'We recommend booking in advance to secure the best seats on the terrace.',
        'faq_title': 'Frequently Asked Questions'
    },
    'en/feijoada-com-vista-rio-de-janeiro.html': {
        'title': 'Where to Eat Feijoada in Rio de Janeiro with a View | Embaixada Carioca',
        'desc': 'The best feijoada in Rio de Janeiro with a view of Sugarloaf Mountain. Served every day at Embaixada Carioca, at Morro da Urca.',
        'h1': 'Where to Eat Feijoada in Rio de Janeiro',
        'h1_sub': 'The authentic Carioca feijoada served every day.',
        'resposta': 'If you are looking for where to eat feijoada in Rio, <strong>Embaixada Carioca</strong> serves its Award-winning Feijoada <strong>every day of the week</strong>. Voted by Veja Rio Comer & Beber as one of the best in the city, you can taste this classic with a front view of Sugarloaf Mountain.',
        'roteiro_title': 'The complete Feijoada experience',
        'roteiro': [
            ('12:00 PM', 'Arrive at Embaixada Carioca at Morro da Urca.'),
            ('12:15 PM', 'Start with our award-winning Magnífica Cachaça Caipirinha and a bean broth (caldinho de feijão).'),
            ('12:45 PM', 'Enjoy the complete Feijoada, served in traditional iron pots.'),
            ('2:30 PM', 'Finish with a typical Brazilian dessert and an espresso.')
        ],
        'cardapio_title': 'What comes with our Feijoada',
        'cardapio_desc': 'Our feijoada is prepared with selected prime meats and comes with all the classics:',
        'cardapio_items': ['Fluffy white rice', 'Crispy farofa (toasted cassava flour)', 'Sautéed collard greens', 'Pork cracklings (Torresmo)', 'Fresh orange slices'],
        'faq': [
            ('Is feijoada served during the week?', 'Yes! Unlike most restaurants in Rio that only serve it on Fridays and Saturdays, we serve our feijoada every day.'),
            ('How many people does it serve?', 'We have generous individual options and options to share (2 people).')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Feijoada at Embaixada Carioca',
        'slug': 'en/feijoada-com-vista-rio-de-janeiro.html',
        'lang': 'en',
        'eyebrow': 'Cable Car Restaurant · Traditional Carioca Restaurant · Morro da Urca · Parque Bondinho Sugarloaf Mountain · Rio de Janeiro · Brazil',
        'nav_home': 'Home',
        'nav_links': [
            ('en/cafe-da-manha.html', 'Breakfast'),
            ('en/almoco.html', 'Lunch'),
            ('en/entardecer.html', 'Sunset'),
            ('en/eventos.html', 'Events'),
            ('en/cardapio.html', 'Menu'),
            ('en/guia-do-rio.html', 'Rio Guide')
        ],
        'btn_reserve': 'Book a Table →',
        'btn_reserve_full': 'Book a Table Now',
        'resposta_title': 'The Quick Answer',
        'garanta_title': 'Secure your table with a view',
        'garanta_desc': 'We recommend booking in advance to secure the best seats on the terrace.',
        'faq_title': 'Frequently Asked Questions'
    },
    'en/caipirinha-com-vista-rio.html': {
        'title': 'Where to Drink Caipirinha in Rio with a View | Embaixada Carioca',
        'desc': 'The best caipirinha in Rio de Janeiro with a view of Sugarloaf Mountain. Award-winning Magnífica Cachaça and fresh fruits at Morro da Urca.',
        'h1': 'Where to Drink Caipirinha in Rio de Janeiro',
        'h1_sub': 'The national drink with the most iconic view in Brazil.',
        'resposta': 'To drink the authentic caipirinha in Rio with an unforgettable view, the terrace of <strong>Embaixada Carioca</strong> at Morro da Urca is the perfect place. Our caipirinha is prepared with the award-winning Magnífica Cachaça and selected fresh fruits.',
        'roteiro_title': 'The perfect moment for a drink',
        'roteiro': [
            ('4:00 PM', 'After visiting the top of Sugarloaf Mountain, head down to Morro da Urca.'),
            ('4:15 PM', 'Secure a table on the balcony of Embaixada Carioca.'),
            ('4:30 PM', 'Order our Magnífica Caipirinha accompanied by Pastéis or Cod Fritters.'),
            ('5:30 PM', 'Enjoy your drink while watching the sunset over Guanabara Bay.')
        ],
        'cardapio_title': 'Our Caipirinhas and Snacks',
        'cardapio_desc': 'Besides the classic lime caipirinha, we offer variations and the best side dishes:',
        'cardapio_items': ['Classic Lime Caipirinha with Magnífica Cachaça', 'Seasonal fruit Caipivodka (Passion Fruit, Strawberry, Kiwi)', 'Cheese and Meat Pastéis (fried pastries)', 'Cod Fritters (Bolinho de Bacalhau)', 'Assorted skewers (Espetinhos)'],
        'faq': [
            ('What caipirinha flavors do you have?', 'Besides the traditional lime, we have passion fruit, strawberry, pineapple, and kiwi, depending on the season. They can be made with cachaça, vodka, or sake.'),
            ('Can I go just for drinks?', 'Of course! Our terrace is perfect for a relaxed happy hour after the tour.')
        ],
        'schema_type': 'BarOrPub',
        'schema_name': 'Caipirinha and Drinks at Embaixada Carioca',
        'slug': 'en/caipirinha-com-vista-rio.html',
        'lang': 'en',
        'eyebrow': 'Cable Car Restaurant · Traditional Carioca Restaurant · Morro da Urca · Parque Bondinho Sugarloaf Mountain · Rio de Janeiro · Brazil',
        'nav_home': 'Home',
        'nav_links': [
            ('en/cafe-da-manha.html', 'Breakfast'),
            ('en/almoco.html', 'Lunch'),
            ('en/entardecer.html', 'Sunset'),
            ('en/eventos.html', 'Events'),
            ('en/cardapio.html', 'Menu'),
            ('en/guia-do-rio.html', 'Rio Guide')
        ],
        'btn_reserve': 'Book a Table →',
        'btn_reserve_full': 'Book a Table Now',
        'resposta_title': 'The Quick Answer',
        'garanta_title': 'Secure your table with a view',
        'garanta_desc': 'We recommend booking in advance to secure the best seats on the terrace.',
        'faq_title': 'Frequently Asked Questions'
    },
    'en/por-do-sol-morro-da-urca.html': {
        'title': 'Sunset at Sugarloaf Mountain and Morro da Urca | Embaixada Carioca',
        'desc': 'Where to watch the sunset at Sugarloaf Mountain? Embaixada Carioca at Morro da Urca offers the best view for the sunset in Rio de Janeiro.',
        'h1': 'Sunset at Sugarloaf Mountain',
        'h1_sub': 'The most spectacular sunset in Rio de Janeiro.',
        'resposta': 'The best place to watch the sunset in the Sugarloaf complex is on the terrace of <strong>Embaixada Carioca</strong>, located at Morro da Urca. You watch the sun setting behind Christ the Redeemer and Guanabara Bay with comfort, drinks, and good gastronomy.',
        'roteiro_title': 'Planning your sunset',
        'roteiro': [
            ('3:30 PM', 'Take the cable car up to enjoy the afternoon light.'),
            ('4:30 PM', 'Arrive at Embaixada Carioca at Morro da Urca and choose a table on the balcony.'),
            ('5:00 PM', 'Order a Heineken Draft Beer (voted 2nd best in Brazil) or a Caipirinha.'),
            ('5:30 - 6:00 PM', 'Enjoy the sunset spectacle (the exact time varies according to the season).')
        ],
        'cardapio_title': 'Accompaniments for the Sunset',
        'cardapio_desc': 'The perfect happy hour calls for the best Carioca snacks:',
        'cardapio_items': ['Ice-cold Heineken Draft Beer', 'Caipirinhas with Magnífica Cachaça', 'Mixed snack board', 'Artisanal Empadas', 'Special sandwiches'],
        'faq': [
            ('What time does the sun set?', 'It varies throughout the year. In summer (Dec-Feb) around 7:30 PM. In winter (Jun-Aug) around 5:15 PM. We recommend arriving 1 hour before.'),
            ('Is it very crowded at this time?', 'Sunset is the peak time at the Sugarloaf Park. Having a reservation at Embaixada Carioca guarantees your comfort away from the crowds.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Sunset at Embaixada Carioca',
        'slug': 'en/por-do-sol-morro-da-urca.html',
        'lang': 'en',
        'eyebrow': 'Cable Car Restaurant · Traditional Carioca Restaurant · Morro da Urca · Parque Bondinho Sugarloaf Mountain · Rio de Janeiro · Brazil',
        'nav_home': 'Home',
        'nav_links': [
            ('en/cafe-da-manha.html', 'Breakfast'),
            ('en/almoco.html', 'Lunch'),
            ('en/entardecer.html', 'Sunset'),
            ('en/eventos.html', 'Events'),
            ('en/cardapio.html', 'Menu'),
            ('en/guia-do-rio.html', 'Rio Guide')
        ],
        'btn_reserve': 'Book a Table →',
        'btn_reserve_full': 'Book a Table Now',
        'resposta_title': 'The Quick Answer',
        'garanta_title': 'Secure your table with a view',
        'garanta_desc': 'We recommend booking in advance to secure the best seats on the terrace.',
        'faq_title': 'Frequently Asked Questions'
    }
}

# Dados para ES
pages_data_es = {
    'es/cafe-da-manha-pao-de-acucar.html': {
        'title': 'Desayuno con Vista en Río de Janeiro | Embaixada Carioca',
        'desc': '¿Dónde desayunar con vista en Río? Embaixada Carioca sirve desayuno todos los días en el Morro da Urca, con vista al Pan de Azúcar.',
        'h1': 'Desayuno con Vista en Río de Janeiro',
        'h1_sub': 'La mejor manera de empezar el día en el Pan de Azúcar.',
        'resposta': '<strong>Embaixada Carioca</strong> es el único restaurante dentro del Parque Bondinho Pan de Azúcar que sirve un desayuno completo con vista panorámica frontal al Pan de Azúcar y la Bahía de Guanabara. Servido <strong>todos los días</strong>, de 8:30 a 11:30.',
        'roteiro_title': 'Cómo incluirlo en tu itinerario',
        'roteiro': [
            ('8:00', 'Llega a la taquilla de Praia Vermelha justo en la apertura para evitar filas.'),
            ('8:20', 'Toma uno de los primeros teleféricos hacia el Morro da Urca (primera parada).'),
            ('8:30 - 9:30', 'Toma tu desayuno en Embaixada Carioca con la terraza aún vacía y la mejor luz para fotos.'),
            ('9:45', 'Toma el segundo teleférico hasta la cima del Pan de Azúcar con la energía recargada.')
        ],
        'cardapio_title': 'Qué pedir en el Desayuno',
        'cardapio_desc': 'Nuestro menú incluye opciones a la carta y combos completos para 2 personas. Destacados:',
        'cardapio_items': ['Panes artesanales de masa madre', 'Huevos revueltos cremosos', 'Frutas tropicales frescas', 'Jugos naturales y café de especialidad', 'El clásico pan de queso caliente (pão de queijo)'],
        'faq': [
            ('¿Necesito pagar el teleférico para desayunar?', 'Sí, el restaurante está ubicado en el Morro da Urca (1ª parada), por lo que se requiere el boleto del Parque Bondinho.'),
            ('¿Se necesita reserva?', 'Recomendamos encarecidamente reservar, especialmente los fines de semana, para asegurar las mejores mesas en la terraza con vista.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Desayuno en Embaixada Carioca',
        'slug': 'es/cafe-da-manha-pao-de-acucar.html',
        'lang': 'es',
        'eyebrow': 'Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil',
        'nav_home': 'Inicio',
        'nav_links': [
            ('es/cafe-da-manha.html', 'Desayuno'),
            ('es/almoco.html', 'Almuerzo'),
            ('es/entardecer.html', 'Atardecer'),
            ('es/eventos.html', 'Eventos'),
            ('es/cardapio.html', 'Menú'),
            ('es/guia-do-rio.html', 'Guía de Río')
        ],
        'btn_reserve': 'Reservar Mesa →',
        'btn_reserve_full': 'Reservar Mesa Ahora',
        'resposta_title': 'La Respuesta Rápida',
        'garanta_title': 'Asegura tu mesa con vista',
        'garanta_desc': 'Recomendamos reservar con anticipación para asegurar los mejores lugares en la terraza.',
        'faq_title': 'Preguntas Frecuentes'
    },
    'es/almoco-morro-da-urca.html': {
        'title': 'Dónde Almorzar en el Morro da Urca y Pan de Azúcar | Embaixada Carioca',
        'desc': '¿Buscas dónde almorzar en el Morro da Urca? Embaixada Carioca ofrece la mejor gastronomía brasileña con vista panorámica en el Pan de Azúcar.',
        'h1': 'Dónde Almorzar en el Morro da Urca',
        'h1_sub': 'Gastronomía brasileña con la mejor vista de Río.',
        'resposta': '<strong>Embaixada Carioca</strong> es la principal opción para almorzar en el Morro da Urca. Ubicado en la primera parada del teleférico, ofrece platos clásicos brasileños, como la famosa Picanha a la Parrilla y la Feijoada Premiada, con vista panorámica a la Bahía de Guanabara.',
        'roteiro_title': 'Cómo incluir el almuerzo en tu paseo',
        'roteiro': [
            ('10:00', 'Sube en el primer teleférico hasta el Morro da Urca y explora la zona.'),
            ('11:00', 'Toma el segundo teleférico hasta la cima del Pan de Azúcar.'),
            ('12:30', 'Baja de regreso al Morro da Urca.'),
            ('13:00', 'Almuerza tranquilamente en Embaixada Carioca antes de bajar a Praia Vermelha.')
        ],
        'cardapio_title': 'Destacados del Almuerzo',
        'cardapio_desc': 'Nuestra especialidad es la auténtica cocina carioca y brasileña. Los platos más pedidos:',
        'cardapio_items': ['Picanha a la Parrilla (nuestro plato más vendido)', 'Feijoada Premiada (servida todos los días)', 'Picadinho Carioca (guiso tradicional de carne)', 'Auténticos Buñuelos de Bacalao (Bolinho de Bacalhau)', 'Cerveza de barril Heineken (elegida la 2ª mejor de Brasil)'],
        'faq': [
            ('¿Cuál es el horario de almuerzo?', 'Servimos almuerzo todos los días, de 11:30 a 16:00. Después de esta hora, el menú de aperitivos y cena sigue disponible.'),
            ('¿Aceptan grupos grandes?', '¡Sí! Tenemos infraestructura para recibir grupos turísticos y familias grandes. Recomendamos reservar con anticipación.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Almuerzo en Embaixada Carioca',
        'slug': 'es/almoco-morro-da-urca.html',
        'lang': 'es',
        'eyebrow': 'Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil',
        'nav_home': 'Inicio',
        'nav_links': [
            ('es/cafe-da-manha.html', 'Desayuno'),
            ('es/almoco.html', 'Almuerzo'),
            ('es/entardecer.html', 'Atardecer'),
            ('es/eventos.html', 'Eventos'),
            ('es/cardapio.html', 'Menú'),
            ('es/guia-do-rio.html', 'Guía de Río')
        ],
        'btn_reserve': 'Reservar Mesa →',
        'btn_reserve_full': 'Reservar Mesa Ahora',
        'resposta_title': 'La Respuesta Rápida',
        'garanta_title': 'Asegura tu mesa con vista',
        'garanta_desc': 'Recomendamos reservar con anticipación para asegurar los mejores lugares en la terraza.',
        'faq_title': 'Preguntas Frecuentes'
    },
    'es/feijoada-com-vista-rio-de-janeiro.html': {
        'title': 'Dónde Comer Feijoada en Río de Janeiro con Vista | Embaixada Carioca',
        'desc': 'La mejor feijoada de Río de Janeiro con vista al Pan de Azúcar. Servida todos los días en Embaixada Carioca, en el Morro da Urca.',
        'h1': 'Dónde Comer Feijoada en Río de Janeiro',
        'h1_sub': 'La auténtica feijoada carioca servida todos los días.',
        'resposta': 'Si buscas dónde comer feijoada en Río, <strong>Embaixada Carioca</strong> sirve su Feijoada Premiada <strong>todos los días de la semana</strong>. Elegida por Veja Rio Comer & Beber como una de las mejores de la ciudad, puedes degustar este clásico con vista frontal al Pan de Azúcar.',
        'roteiro_title': 'La experiencia completa de la Feijoada',
        'roteiro': [
            ('12:00', 'Llega a Embaixada Carioca en el Morro da Urca.'),
            ('12:15', 'Comienza con nuestra premiada Caipirinha de Cachaça Magnífica y un caldo de frijoles (caldinho de feijão).'),
            ('12:45', 'Disfruta de la Feijoada completa, servida en tradicionales ollas de hierro.'),
            ('14:30', 'Termina con un postre típico brasileño y un café expreso.')
        ],
        'cardapio_title': 'Qué acompaña nuestra Feijoada',
        'cardapio_desc': 'Nuestra feijoada se prepara con carnes nobles seleccionadas y viene con todos los clásicos:',
        'cardapio_items': ['Arroz blanco suelto', 'Farofa crujiente (harina de yuca tostada)', 'Col rizada salteada (couve mineira)', 'Chicharrón de cerdo (Torresmo)', 'Rodajas de naranja fresca'],
        'faq': [
            ('¿Se sirve feijoada durante la semana?', '¡Sí! A diferencia de la mayoría de los restaurantes en Río que solo la sirven los viernes y sábados, nosotros servimos nuestra feijoada todos los días.'),
            ('¿Para cuántas personas es?', 'Tenemos opciones individuales generosas y opciones para compartir (2 personas).')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Feijoada en Embaixada Carioca',
        'slug': 'es/feijoada-com-vista-rio-de-janeiro.html',
        'lang': 'es',
        'eyebrow': 'Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil',
        'nav_home': 'Inicio',
        'nav_links': [
            ('es/cafe-da-manha.html', 'Desayuno'),
            ('es/almoco.html', 'Almuerzo'),
            ('es/entardecer.html', 'Atardecer'),
            ('es/eventos.html', 'Eventos'),
            ('es/cardapio.html', 'Menú'),
            ('es/guia-do-rio.html', 'Guía de Río')
        ],
        'btn_reserve': 'Reservar Mesa →',
        'btn_reserve_full': 'Reservar Mesa Ahora',
        'resposta_title': 'La Respuesta Rápida',
        'garanta_title': 'Asegura tu mesa con vista',
        'garanta_desc': 'Recomendamos reservar con anticipación para asegurar los mejores lugares en la terraza.',
        'faq_title': 'Preguntas Frecuentes'
    },
    'es/caipirinha-com-vista-rio.html': {
        'title': 'Dónde Tomar Caipirinha en Río con Vista | Embaixada Carioca',
        'desc': 'La mejor caipirinha de Río de Janeiro con vista al Pan de Azúcar. Cachaça Magnífica premiada y frutas frescas en el Morro da Urca.',
        'h1': 'Dónde Tomar Caipirinha en Río de Janeiro',
        'h1_sub': 'La bebida nacional con la vista más icónica de Brasil.',
        'resposta': 'Para tomar la auténtica caipirinha en Río con una vista inolvidable, la terraza de <strong>Embaixada Carioca</strong> en el Morro da Urca es el lugar perfecto. Nuestra caipirinha se prepara con la premiada Cachaça Magnífica y frutas frescas seleccionadas.',
        'roteiro_title': 'El momento perfecto para un trago',
        'roteiro': [
            ('16:00', 'Después de visitar la cima del Pan de Azúcar, baja al Morro da Urca.'),
            ('16:15', 'Asegura una mesa en el balcón de Embaixada Carioca.'),
            ('16:30', 'Pide nuestra Caipirinha Magnífica acompañada de Pasteles o Buñuelos de Bacalao.'),
            ('17:30', 'Disfruta de tu bebida mientras ves el atardecer sobre la Bahía de Guanabara.')
        ],
        'cardapio_title': 'Nuestras Caipirinhas y Aperitivos',
        'cardapio_desc': 'Además de la clásica caipirinha de limón, ofrecemos variaciones y los mejores acompañamientos:',
        'cardapio_items': ['Caipirinha Clásica de Limón con Cachaça Magnífica', 'Caipivodka de frutas de temporada (Maracuyá, Fresa, Kiwi)', 'Pasteles de Queso y Carne (empanadas fritas)', 'Buñuelos de Bacalao (Bolinho de Bacalhau)', 'Brochetas variadas (Espetinhos)'],
        'faq': [
            ('¿Qué sabores de caipirinha tienen?', 'Además del tradicional limón, tenemos maracuyá, fresa, piña y kiwi, dependiendo de la temporada. Se pueden hacer con cachaça, vodka o sake.'),
            ('¿Puedo ir solo a beber?', '¡Claro! Nuestra terraza es perfecta para un happy hour relajado después del paseo.')
        ],
        'schema_type': 'BarOrPub',
        'schema_name': 'Caipirinha y Tragos en Embaixada Carioca',
        'slug': 'es/caipirinha-com-vista-rio.html',
        'lang': 'es',
        'eyebrow': 'Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil',
        'nav_home': 'Inicio',
        'nav_links': [
            ('es/cafe-da-manha.html', 'Desayuno'),
            ('es/almoco.html', 'Almuerzo'),
            ('es/entardecer.html', 'Atardecer'),
            ('es/eventos.html', 'Eventos'),
            ('es/cardapio.html', 'Menú'),
            ('es/guia-do-rio.html', 'Guía de Río')
        ],
        'btn_reserve': 'Reservar Mesa →',
        'btn_reserve_full': 'Reservar Mesa Ahora',
        'resposta_title': 'La Respuesta Rápida',
        'garanta_title': 'Asegura tu mesa con vista',
        'garanta_desc': 'Recomendamos reservar con anticipación para asegurar los mejores lugares en la terraza.',
        'faq_title': 'Preguntas Frecuentes'
    },
    'es/por-do-sol-morro-da-urca.html': {
        'title': 'Atardecer en el Pan de Azúcar y Morro da Urca | Embaixada Carioca',
        'desc': '¿Dónde ver el atardecer en el Pan de Azúcar? Embaixada Carioca en el Morro da Urca ofrece la mejor vista para el atardecer en Río de Janeiro.',
        'h1': 'Atardecer en el Pan de Azúcar',
        'h1_sub': 'El atardecer más espectacular de Río de Janeiro.',
        'resposta': 'El mejor lugar para ver el atardecer en el complejo del Pan de Azúcar es en la terraza de <strong>Embaixada Carioca</strong>, ubicada en el Morro da Urca. Observas la puesta de sol detrás del Cristo Redentor y la Bahía de Guanabara con comodidad, bebidas y buena gastronomía.',
        'roteiro_title': 'Planificando tu atardecer',
        'roteiro': [
            ('15:30', 'Sube en el teleférico para aprovechar la luz de la tarde.'),
            ('16:30', 'Llega a Embaixada Carioca en el Morro da Urca y elige una mesa en el balcón.'),
            ('17:00', 'Pide una Cerveza de barril Heineken (elegida la 2ª mejor de Brasil) o una Caipirinha.'),
            ('17:30 - 18:00', 'Disfruta del espectáculo del atardecer (la hora exacta varía según la temporada).')
        ],
        'cardapio_title': 'Acompañamientos para el Atardecer',
        'cardapio_desc': 'El happy hour perfecto pide los mejores aperitivos cariocas:',
        'cardapio_items': ['Cerveza de barril Heineken estupendamente fría', 'Caipirinhas con Cachaça Magnífica', 'Tabla de aperitivos mixtos', 'Empanadas artesanales', 'Sándwiches especiales'],
        'faq': [
            ('¿A qué hora se pone el sol?', 'Varía a lo largo del año. En verano (dic-feb) alrededor de las 19:30. En invierno (jun-ago) alrededor de las 17:15. Recomendamos llegar 1 hora antes.'),
            ('¿Está muy lleno a esta hora?', 'El atardecer es la hora pico en el Parque Bondinho. Tener una reserva en Embaixada Carioca garantiza tu comodidad lejos de las multitudes.')
        ],
        'schema_type': 'Restaurant',
        'schema_name': 'Atardecer en Embaixada Carioca',
        'slug': 'es/por-do-sol-morro-da-urca.html',
        'lang': 'es',
        'eyebrow': 'Restaurante del Teleférico · Restaurante Carioca Tradicional de Calidad · Morro da Urca · Parque Bondinho Pan de Azúcar · Río de Janeiro · Brasil',
        'nav_home': 'Inicio',
        'nav_links': [
            ('es/cafe-da-manha.html', 'Desayuno'),
            ('es/almoco.html', 'Almuerzo'),
            ('es/entardecer.html', 'Atardecer'),
            ('es/eventos.html', 'Eventos'),
            ('es/cardapio.html', 'Menú'),
            ('es/guia-do-rio.html', 'Guía de Río')
        ],
        'btn_reserve': 'Reservar Mesa →',
        'btn_reserve_full': 'Reservar Mesa Ahora',
        'resposta_title': 'La Respuesta Rápida',
        'garanta_title': 'Asegura tu mesa con vista',
        'garanta_desc': 'Recomendamos reservar con anticipación para asegurar los mejores lugares en la terraza.',
        'faq_title': 'Preguntas Frecuentes'
    }
}

# Template base para as páginas EN e ES
template = """<!DOCTYPE html>
<html lang="{lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <link rel="stylesheet" href="../assets/style.css">
    <link rel="stylesheet" href="../assets/fonts/fonts.css">
    <link rel="canonical" href="https://www.embaixadacarioca.com/{slug}">
    <link rel="alternate" hreflang="pt-BR" href="https://www.embaixadacarioca.com/{slug_pt}">
    <link rel="alternate" hreflang="en" href="https://www.embaixadacarioca.com/en/{slug_pt}">
    <link rel="alternate" hreflang="es" href="https://www.embaixadacarioca.com/es/{slug_pt}">
    <link rel="alternate" hreflang="x-default" href="https://www.embaixadacarioca.com/{slug_pt}">
    <style>
        .page-hero-content .eyebrow.hero-eyebrow {{
            color: rgba(246, 239, 222, 0.75);
            margin-bottom: 20px;
            font-size: 10px;
            letter-spacing: 0.22em;
        }}
        .page-hero-content .eyebrow.hero-eyebrow::before {{
            background: var(--amarelo, #d4a017);
        }}
    </style>
</head>
<body>
    <a href="#conteudo-principal" class="skip-nav">Skip to main content</a>
    
    <nav class="top" id="topnav">
        <div class="nav-inner">
            <a href="index.html" class="brand-mark" aria-label="Embaixada Carioca · home">
                <img src="../assets/logo-areia.svg" alt="Embaixada Carioca" class="brand-logo light" loading="lazy">
                <img src="../assets/logo-azul.svg" alt="Embaixada Carioca" class="brand-logo dark" loading="lazy">
            </a>
            <ul class="nav-links">
                {nav_links_html}
            </ul>
            <a href="https://go.tagme.com.br/embaixadacarioca" class="btn">{btn_reserve}</a>
        </div>
    </nav>

    <header class="page-hero">
        <picture>
            <source media="(max-width: 720px)" srcset="../assets/hero-mobile.webp" type="image/webp">
            <source srcset="../assets/hero.jpg" type="image/jpg">
            <img src="../assets/hero.webp" alt="{h1}" class="page-hero-photo" loading="eager" decoding="async">
        </picture>
        <div class="page-hero-overlay" aria-hidden="true"></div>
        <div class="page-hero-content">
            <div class="eyebrow hero-eyebrow">{eyebrow}</div>
            <div class="crumbs">
                <a href="index.html">{nav_home}</a> <span class="sep">/</span> <span class="here">{h1}</span>
            </div>
            <h1>{h1}</h1>
            <p class="lede">{h1_sub}</p>
        </div>
    </header>

    <main id="conteudo-principal">
        <section style="padding: 4rem 0; background: var(--areia-pale);">
            <div class="wrap" style="max-width: 800px; margin: 0 auto;">
                <div style="background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); margin-bottom: 3rem;">
                    <h2 style="color: var(--azul-escuro); margin-bottom: 1rem; font-size: 1.8rem;">{resposta_title}</h2>
                    <p style="font-size: 1.2rem; line-height: 1.6; color: var(--cinza1);">{resposta}</p>
                </div>

                <h2 style="color: var(--azul-escuro); margin-bottom: 1.5rem; font-size: 2rem;">{roteiro_title}</h2>
                <div style="margin-bottom: 3rem;">
                    {roteiro_html}
                </div>

                <h2 style="color: var(--azul-escuro); margin-bottom: 1.5rem; font-size: 2rem;">{cardapio_title}</h2>
                <p style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-bottom: 1rem;">{cardapio_desc}</p>
                <ul style="font-size: 1.1rem; line-height: 1.6; color: var(--cinza1); margin-bottom: 3rem; padding-left: 20px;">
                    {cardapio_items_html}
                </ul>

                <div style="text-align: center; margin: 4rem 0; padding: 3rem; background: var(--azul-escuro); border-radius: 8px; color: white;">
                    <h3 style="font-size: 1.8rem; margin-bottom: 1rem; color: white;">{garanta_title}</h3>
                    <p style="font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.9;">{garanta_desc}</p>
                    <a href="https://go.tagme.com.br/embaixadacarioca" class="btn" style="background: var(--amarelo); color: var(--azul-escuro); font-size: 1.2rem; padding: 1rem 2rem;">{btn_reserve_full}</a>
                </div>

                <h2 style="color: var(--azul-escuro); margin-bottom: 1.5rem; font-size: 2rem;">{faq_title}</h2>
                <div style="display: grid; gap: 1.5rem;">
                    {faq_html}
                </div>
            </div>
        </section>
    </main>

    <footer class="foot">
        <div class="wrap">
            <div class="foot-top">
                <div class="foot-brand">
                    <p class="big">Embaixada<br><span class="serif">Carioca.</span></p>
                    <p class="tagline">O consulado da gastronomia e da cultura brasileira para o mundo — no alto do Morro da Urca, Rio de Janeiro.</p>
                </div>
            </div>
            <div class="foot-bottom">
                <div>Parque Bondinho Pão de Açúcar · Rio de Janeiro</div>
                <div>© 2026 · Todos os direitos reservados</div>
            </div>
        </div>
    </footer>

    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "{schema_type}",
      "name": "{schema_name}",
      "image": "https://www.embaixadacarioca.com/assets/hero.jpg",
      "url": "https://www.embaixadacarioca.com/{slug}",
      "telephone": "+5521966837556",
      "address": {{
        "@type": "PostalAddress",
        "streetAddress": "Av. Pasteur, 520 - Morro da Urca",
        "addressLocality": "Rio de Janeiro",
        "addressRegion": "RJ",
        "postalCode": "22290-240",
        "addressCountry": "BR"
      }}
    }}
    </script>
</body>
</html>"""

def process_pages(pages_data):
    for filename, data in pages_data.items():
        slug = data['slug']
        slug_pt = slug.split('/')[-1]
        
        # Gerar HTML do roteiro
        roteiro_html = ""
        for time, desc in data['roteiro']:
            roteiro_html += f'<div style="display: flex; gap: 1rem; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid rgba(0,0,0,0.1);"><div style="font-weight: bold; color: var(--verde); min-width: 100px;">{time}</div><div style="color: var(--cinza1); line-height: 1.5;">{desc}</div></div>\n'
            
        # Gerar HTML dos itens do cardápio
        cardapio_items_html = ""
        for item in data['cardapio_items']:
            cardapio_items_html += f'<li style="margin-bottom: 0.5rem;">{item}</li>\n'
            
        # Gerar HTML do FAQ
        faq_html = ""
        for q, a in data['faq']:
            faq_html += f'<div style="background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);"><h3 style="font-size: 1.2rem; margin-bottom: 0.5rem; color: var(--azul-escuro);">{q}</h3><p style="color: var(--cinza1); line-height: 1.5;">{a}</p></div>\n'
            
        # Gerar HTML dos links de navegação
        nav_links_html = ""
        for link_url, link_text in data['nav_links']:
            # Ajustar URL para ser relativa à pasta atual
            rel_url = link_url.split('/')[-1]
            nav_links_html += f'<li><a href="{rel_url}">{link_text}</a></li>\n                '
            
        # Preencher template
        html = template.format(
            lang=data['lang'],
            slug=slug,
            slug_pt=slug_pt,
            title=data['title'],
            desc=data['desc'],
            h1=data['h1'],
            h1_sub=data['h1_sub'],
            resposta=data['resposta'],
            roteiro_title=data['roteiro_title'],
            roteiro_html=roteiro_html,
            cardapio_title=data['cardapio_title'],
            cardapio_desc=data['cardapio_desc'],
            cardapio_items_html=cardapio_items_html,
            faq_html=faq_html,
            schema_type=data['schema_type'],
            schema_name=data['schema_name'],
            eyebrow=data['eyebrow'],
            nav_home=data['nav_home'],
            nav_links_html=nav_links_html,
            btn_reserve=data['btn_reserve'],
            btn_reserve_full=data['btn_reserve_full'],
            resposta_title=data['resposta_title'],
            garanta_title=data['garanta_title'],
            garanta_desc=data['garanta_desc'],
            faq_title=data['faq_title']
        )
        
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        Path(filename).write_text(html, encoding='utf-8')
        print(f"✅ Recriada: {filename}")

print("=== Gerando páginas EN ===")
process_pages(pages_data_en)

print("\n=== Gerando páginas ES ===")
process_pages(pages_data_es)

