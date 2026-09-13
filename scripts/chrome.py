"""Shared page furniture in both languages, so a Spanish page carries no English."""

CHROME = {
    'en': {
        'skip': 'Skip to content',
        'announce': 'A closer view of Venezuela. Our lead research programme is taking shape.',
        'announce_link': 'Explore the programme',
        'menu': 'Menu',
        'nav_label': 'Main navigation',
        'tagline': 'Research on political decisions and their consequences.',
        'regions': 'Venezuela and European energy policy',
        'explore': 'Explore',
        'connect': 'Connect',
        'company': 'Company',
        'f_capabilities': 'Research capabilities',
        'f_government': 'Government affairs',
        'f_credit': 'Distressed debt',
        'f_venezuela': 'Venezuela programme',
        'f_library': 'Intelligence library',
        'f_coverage': 'Regional coverage',
        'f_how': 'How it works',
        'f_engagement': 'Working with EchoFrame',
        'f_about': 'About EchoFrame',
        'f_trust': 'Trust &amp; privacy',
        'f_samples': 'Sample briefs &amp; templates',
        'f_sources': 'Primary-source directory',
        'f_standards': 'Editorial standards',
        'privacy': 'Privacy',
        'research_mark': 'EchoFrame research',
        'top': 'Back to top',
        'description': 'Political intelligence for oil and gas government affairs teams and distressed-debt '
                       'investors. Explore asset-level questions, policy context, and the Venezuela programme.',
        'og_description': 'Research on political decisions and their consequences. Explore EchoFrame research, '
                          'coverage and how the work is done.',
    },
    'es': {
        'skip': 'Saltar al contenido',
        'announce': 'Una mirada más cercana a Venezuela. Nuestro programa principal de investigación está tomando '
                    'forma.',
        'announce_link': 'Conozca el programa',
        'menu': 'Menú',
        'nav_label': 'Navegación principal',
        'tagline': 'Investigación sobre decisiones políticas y sus consecuencias.',
        'regions': 'Venezuela y política energética europea',
        'explore': 'Explorar',
        'connect': 'Contacto',
        'company': 'La empresa',
        'f_capabilities': 'Capacidades de investigación',
        'f_government': 'Asuntos gubernamentales',
        'f_credit': 'Deuda en dificultades',
        'f_venezuela': 'Programa de Venezuela',
        'f_library': 'Biblioteca de investigación',
        'f_coverage': 'Cobertura regional',
        'f_how': 'Cómo trabajamos',
        'f_engagement': 'Trabajar con EchoFrame',
        'f_about': 'Sobre EchoFrame',
        'f_trust': 'Confianza y privacidad',
        'f_samples': 'Plantillas e informes de muestra',
        'f_sources': 'Directorio de fuentes primarias',
        'f_standards': 'Normas editoriales',
        'privacy': 'Privacidad',
        'research_mark': 'Investigación de EchoFrame',
        'top': 'Volver arriba',
        'description': 'Un registro fechado y documentado de lo que ocurre en los mercados emergentes donde la '
                       'información es escasa. Venezuela es el programa en marcha.',
        'og_description': 'Investigación sobre decisiones políticas y sus consecuencias. Venezuela y política '
                          'energética europea.',
    },
}

# Spanish labels for the navigation. The pages themselves are in English, which
# the panel label states rather than leaving the reader to discover it.
GROUPS_ES = {
    'Capabilities': 'Capacidades',
    'Who we help': 'A quién ayudamos',
    'Research': 'Investigación',
    'Company': 'La empresa',
}

ITEMS_ES = {
    'how-it-works.html': ('Cómo trabajamos', 'Los seis pasos y cómo se confirma un hecho.'),
    'capabilities.html': ('Sistema de investigación', 'El flujo de trabajo analítico completo.'),
    'actor-mapping.html': ('Actores y activos', 'Documentar las relaciones detrás de una decisión.'),
    'evidence-workspace.html': ('Espacio de evidencia', 'Fuentes, contradicciones y límites.'),
    'decision-pathways.html': ('Rutas de decisión', 'Hitos observables y disparadores de revisión.'),
    'government-affairs.html': ('Asuntos gubernamentales', 'Política, actores y activos en operación.'),
    'distressed-debt.html': ('Deuda en dificultades', 'Supuestos políticos y estudio de contrapartes.'),
    'case-study-venezuela.html': ('Caso práctico, Venezuela', 'Una valoración hecha antes del desenlace.'),
    'worked-examples.html': ('Ejemplos de trabajo', 'Cuatro encargos, descritos por tipo.'),
    'engagement.html': ('Trabajar con EchoFrame', 'Formatos, alcance y entrega.'),
    'research.html': ('Biblioteca de investigación', 'Ensayos, guías regionales y notas de programa.'),
    'sample-briefs.html': ('Plantillas e informes de muestra', 'Estructura de un informe de investigación.'),
    'sources.html': ('Directorio de fuentes primarias', 'Registros oficiales y cómo utilizarlos.'),
    'coverage.html': ('Cobertura regional', 'Dónde recopilamos y qué viene después.'),
    'about.html': ('Sobre EchoFrame', 'El propósito y el enfoque de la investigación.'),
    'frame-bureau.html': ('The Frame Bureau', 'Formar a una institución para que lleve su propia unidad de análisis.'),
    'trust.html': ('Confianza y privacidad', 'Evidencia, manejo de información y límites.'),
    'editorial-standards.html': ('Normas editoriales', 'Atribución, incertidumbre y correcciones.'),
}
