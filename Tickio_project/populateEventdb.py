import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tickio.settings')
django.setup()

from events.models import CategoriaEvento, Evento

def crear_categorias():
    categorias = [
        {
            'nombre': 'Conciertos Rock',
            'descripcion': '¡Vive la energía del rock en su máxima expresión! Desde el rock clásico hasta el metal más pesado, experimenta shows electrizantes con las mejores bandas nacionales e internacionales.'
        },
        {
            'nombre': 'Conciertos Pop',
            'descripcion': 'Disfruta de espectáculos únicos con tus artistas pop favoritos. Shows llenos de color, coreografías espectaculares y éxitos que te harán cantar y bailar toda la noche.'
        },
        {
            'nombre': 'Reggaeton',
            'descripcion': 'Siente el ritmo urbano en tu piel. Los mejores exponentes del género urbano traen sus beats más pegajosos y letras que harán vibrar el escenario.'
        },
        {
            'nombre': 'Vallenato',
            'descripcion': 'El folclor colombiano en su máxima expresión. Desde el vallenato tradicional hasta las nuevas fusiones, vive la magia del acordeón y las historias que solo el vallenato sabe contar.'
        },
        {
            'nombre': 'Salsa',
            'descripcion': 'Mueve tus pies al ritmo de la mejor salsa. Orquestas legendarias y nuevos talentos te harán vivir noches inolvidables llenas de sabor latino y pasos de baile.'
        },
        {
            'nombre': 'Música Electrónica',
            'descripcion': 'Adéntrate en el mundo de los beats electrónicos. Los mejores DJs nacionales e internacionales te llevarán a un viaje sonoro con producciones visuales espectaculares.'
        },
        {
            'nombre': 'Teatro',
            'descripcion': 'Desde obras clásicas hasta producciones contemporáneas, el teatro cobra vida con actuaciones memorables que te transportarán a otros mundos.'
        },
        {
            'nombre': 'Stand Up Comedy',
            'descripcion': 'Ríe sin parar con los mejores comediantes del momento. Shows irreverentes y divertidos que te harán olvidar el estrés y disfrutar del mejor humor.'
        },
        {
            'nombre': 'Fútbol',
            'descripcion': 'Siente la pasión del deporte rey. Partidos decisivos, clásicos inolvidables y torneos que hacen historia en los mejores estadios del país.'
        },
        {
            'nombre': 'Baloncesto',
            'descripcion': 'Emoción hasta el último segundo en la cancha. Disfruta del mejor baloncesto nacional e internacional con jugadas espectaculares y momentos de infarto.'
        },
        {
            'nombre': 'Festivales Gastronómicos',
            'descripcion': 'Un festín para tus sentidos. Descubre sabores únicos, aprende de chefs reconocidos y disfruta de la mejor gastronomía local e internacional.'
        },
        {
            'nombre': 'Festivales de Música',
            'descripcion': 'Múltiples escenarios, diversos géneros y experiencias inolvidables. Los mejores festivales que reúnen lo mejor de la música en un solo lugar.'
        },
        {
            'nombre': 'Música Tropical',
            'descripcion': 'Baila al ritmo de merengue, bachata y más. La alegría del Caribe en shows llenos de color y sabor que te harán mover los pies toda la noche.'
        },
        {
            'nombre': 'Jazz & Blues',
            'descripcion': 'Veladas sofisticadas con lo mejor del jazz y el blues. Experimenta la improvisación y el talento de músicos excepcionales en ambientes únicos.'
        },
        {
            'nombre': 'Música Clásica',
            'descripcion': 'Desde conciertos sinfónicos hasta recitales íntimos. Déjate llevar por la majestuosidad de la música clásica en venues con acústica perfecta.'
        }
    ]
    
    categorias_creadas = []
    for cat in categorias:
        categoria, created = CategoriaEvento.objects.get_or_create(
            nombre=cat['nombre'],
            defaults={'descripcion': cat['descripcion']}
        )
        categorias_creadas.append(categoria)
        print(f"Categoría {'creada' if created else 'actualizada'}: {categoria.nombre}")
    
    return categorias_creadas

def crear_eventos(categorias):
    # Diccionario de eventos por categoría
    eventos_por_categoria = {
        'Conciertos Rock': {
            'eventos': [
                "Metallica World Tour",
                "Guns N' Roses en Colombia",
                "Iron Maiden Legacy Tour",
                "Foo Fighters en Concierto",
                "Green Day Revolution"
            ],
            'organizadores': ["Ocesa Colombia", "Move Concerts", "Páramo Presenta"]
        },
        'Reggaeton': {
            'eventos': [
                "Bad Bunny World Tour",
                "Karol G - Mañana Será Bonito",
                "Daddy Yankee Legend Tour",
                "J Balvin en Concierto",
                "Feid Show"
            ],
            'organizadores': ["LiveCol", "Two Shows", "Stage Pro"]
        },
        'Vallenato': {
            'eventos': [
                "Silvestre Dangond Tour",
                "Festival Vallenato Medellín",
                "Peter Manjarrés en Vivo",
                "Jean Carlos Centeno Show",
                "Festival de Acordeones"
            ],
            'organizadores': ["Sayco", "Vallenato Productions", "Colombian Music"]
        },
        'Fútbol': {
            'eventos': [
                "Nacional vs Millonarios",
                "América vs Junior",
                "DIM vs Nacional",
                "Santa Fe vs Millonarios",
                "Colombia vs Brasil"
            ],
            'organizadores': ["Dimayor", "FCF", "Win Sports"]
        },
        'Stand Up Comedy': {
            'eventos': [
                "Andrés López Show",
                "Ricardo Quevedo Live",
                "Antonio Sanint Tour",
                "Alejandro Riaño Especial",
                "Los Comediantes de la Noche"
            ],
            'organizadores': ["Casa Comedy", "House of Comedy", "Comedy Central"]
        }
    }

    # Eventos genéricos para otras categorías
    eventos_genericos = [
        "Festival de {categoria}",
        "Gran Concierto de {categoria}",
        "Show Especial de {categoria}",
        "Noche de {categoria}",
        "Experiencia {categoria}"
    ]

    eventos_creados = 0
    for categoria in categorias:
        # Obtener eventos específicos para la categoría o usar genéricos
        if categoria.nombre in eventos_por_categoria:
            eventos = eventos_por_categoria[categoria.nombre]['eventos']
            organizadores = eventos_por_categoria[categoria.nombre]['organizadores']
        else:
            eventos = [e.format(categoria=categoria.nombre) for e in eventos_genericos]
            organizadores = ["Tu Boleta", "Prodygy", "Eventos Colombia"]

        # Crear eventos para esta categoría
        for nombre_evento in eventos[:4]:  # Limitar a 4 eventos por categoría
            fecha = datetime.now().date() + timedelta(days=random.randint(1, 365))
            
            # Seleccionar lugar apropiado según la categoría
            if categoria.nombre in ['Fútbol', 'Conciertos Rock', 'Reggaeton']:
                lugares = [
                    "Estadio Atanasio Girardot - Medellín",
                    "Estadio El Campín - Bogotá",
                    "Estadio Pascual Guerrero - Cali"
                ]
            elif categoria.nombre in ['Stand Up Comedy', 'Teatro']:
                lugares = [
                    "Teatro Pablo Tobón Uribe - Medellín",
                    "Royal Center - Bogotá",
                    "Teatro Jorge Eliécer Gaitán - Bogotá"
                ]
            else:
                lugares = [
                    "Movistar Arena - Bogotá",
                    "Plaza Mayor - Medellín",
                    "Centro de Eventos La Macarena - Medellín"
                ]

            evento = Evento.objects.create(
                nombre=nombre_evento,
                categoria=categoria,
                fecha=fecha,
                lugar=random.choice(lugares),
                organizador=random.choice(organizadores),
                cupos_disponibles=random.randint(100, 45000),
                precio=Decimal(random.randint(50000, 850000))
            )
            eventos_creados += 1
            print(f"Evento creado: {evento.nombre} - {evento.categoria.nombre} - {evento.organizador}")
    
    return eventos_creados

if __name__ == '__main__':
    try:
        print('=== Iniciando población de la base de datos ===\n')
        
        print('Creando categorías...')
        categorias = crear_categorias()
        print(f'\n¡{len(categorias)} categorías creadas exitosamente!\n')
        
        print('Creando eventos...')
        total_eventos = crear_eventos(categorias)
        print(f'\n¡{total_eventos} eventos creados exitosamente!\n')
        
        print('=== Base de datos poblada completamente ===')
    
    except Exception as e:
        print(f"\nError durante la población de la base de datos: {str(e)}")
        raise