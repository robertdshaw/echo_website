"""The Spanish mirror of the home page. No English text is left on it."""

BLOCKS = [
    ('01 / Dónde recopilamos', 'Fuera de las capitales',
     'Los estados petroleros del este y el oeste de Venezuela, y a continuación Colombia, México, Ruanda y Pakistán. '
     'Trabajamos donde la información es más escasa y la exposición es mayor.'),
    ('02 / Cómo lo verificamos', 'Nada se confirma con una sola clase de fuente',
     'Los medios de comunicación cuentan como una sola clase, por muchos que publiquen la misma noticia. Los '
     'registros oficiales, la investigación independiente, los datos físicos y la información obtenida sobre el '
     'terreno son las demás. Un hecho se da por confirmado cuando coinciden clases independientes.'),
    ('03 / Qué recibe', 'Un registro, no un informe',
     'Un registro fechado de lo que ocurre en activos concretos, una lista breve de preguntas escritas con su fecha, '
     'y una probabilidad para cada una que solo se mueve cuando cambia la evidencia.'),
]


def page(intro):
    blocks = ''.join(
        f'<section class="home-claim" aria-labelledby="claim-{i}"><div class="eyebrow">{kicker}</div>'
        f'<div><h2 id="claim-{i}">{title}</h2><p>{body}</p></div></section>'
        for i, (kicker, title, body) in enumerate(BLOCKS, 1))
    return intro(
        'Inteligencia continua', 'Desde lugares que solo producen instantáneas',
        'EchoFrame construye un registro fechado y documentado de lo que ocurre en las zonas de los mercados '
        'emergentes donde la información es escasa. Pagamos a las redacciones locales por la información y los '
        'archivos que ya tienen, y contrastamos lo que publican con registros oficiales, datos físicos y mercados.'
    ) + f'<div class="home-claims container">{blocks}</div>' + (
        '<section class="prose-page container"><h2>El problema, dicho con claridad.</h2>'
        '<p>La mayor parte del riesgo político y operativo ocurre en lugares que no producen un flujo constante de '
        'información. Un campo en Monagas. Un municipio minero en Bolívar. Una ruta de suministro en el oriente de '
        'Colombia. La información de esos lugares es escasa, está repartida entre medios pequeños y casi nunca se '
        'confirma dos veces.</p>'
        '<p>Por eso el sector trabaja con instantáneas. Una empresa necesita saber algo, encarga un informe, recibe '
        'una respuesta con fecha de ese día y espera hasta la siguiente pregunta. Cada encargo empieza de cero y '
        'nadie observa lo que pasa entre uno y otro.</p>'
        '<h2>Venezuela es el programa en marcha.</h2>'
        '<p>Dos años de archivo, un registro estructurado de hechos para los estados petroleros del oriente y un '
        'acuerdo con corresponsales en preparación. Después vienen Colombia, México, Ruanda y Pakistán.</p>'
        '<p>Nuestra segunda área es la política energética y regulatoria europea, disponible para clientes que la '
        'soliciten.</p>'
        '<h2>Hablemos de sus prioridades.</h2>'
        '<p>Escríbanos indicando la región y las preguntas que le interesan. Podemos comentar el alcance de la '
        'investigación y las opciones de acceso. Las páginas de investigación de este sitio están en inglés.</p>'
        '<p>contact@echoframe.co</p></section>')
