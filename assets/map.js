/* Public, approved event records only. No article fields enter the view. */
(() => {
  'use strict';
  const host = document.querySelector('[data-gis-demo]');
  if (!host) return;
  const es = host.dataset.language === 'es';
  const t = (en, spanish) => es ? spanish : en;
  const $ = id => document.getElementById(id);
  const root = host.dataset.root;
  const locale = es ? 'es-ES' : 'en-GB';
  const ns = 'http://www.w3.org/2000/svg';
  const colours = ['#5a3878', '#ad4328'];
  const FC = features => ({type: 'FeatureCollection', features});
  const el = (tag, content, cls) => {
    const node = document.createElement(tag);
    if (content !== undefined) node.textContent = content;
    if (cls) node.className = cls;
    return node;
  };
  const svgEl = (tag, attrs = {}, content) => {
    const node = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    if (content !== undefined) node.textContent = content;
    return node;
  };
  const names = {petropiar: 'Petropiar', petromonagas: 'Petromonagas', petrocedeno: 'Petrocedeño',
    bloque_carabobo: 'Bloque Carabobo', bloque_junin: 'Bloque Junín', el_furrial: 'El Furrial',
    jose_complex: t('José complex', 'Complejo de José'), jose_terminal: t('José terminal', 'Terminal de José'),
    jusepin: 'Jusepín', morichal: 'Morichal', punta_de_mata: 'Punta de Mata',
    state_monagas: 'Monagas', state_anzoategui: 'Anzoátegui', pdvsa_oriente: 'PDVSA Oriente'};
  const labels = {
    single_source: t('Single source', 'Fuente única'), corroborated: t('Corroborated', 'Corroborado'),
    contradicted: t('Contradicted', 'Contradicho'), unassessed: t('Unassessed', 'Sin evaluar'),
    low: t('Low', 'Baja'), medium: t('Medium', 'Media'), high: t('High', 'Alta'),
    stale: t('Stale', 'Sin vigencia'), fresh: t('Fresh', 'Vigente'), live: t('Current in snapshot', 'Vigente en la exportación'),
    state: t('State', 'Estado'), municipality: t('Municipality', 'Municipio'), facility: t('Facility', 'Instalación'),
    approximate: t('Approximate', 'Aproximada'), unresolved: t('Unresolved', 'Sin resolver'),
    operator: t('Operator', 'Operador'), creditor: t('Creditor', 'Acreedor'),
    ground: t('Ground reporting', 'Información sobre el terreno'), media: t('Media', 'Medios'),
    official: t('Official', 'Oficial'), physical: t('Physical observation', 'Observación física'),
    expert: t('Expert', 'Experto'), external_expert: t('External expert', 'Experto externo'),
  };
  const questionES = {
    '001': '¿OFAC modificará, revocará o dejará vencer la licencia general o específica que permite a Chevron operar Petropiar antes del 31 de marzo de 2025?',
    '002': '¿Se publicará en la Gaceta Oficial o anunciará PDVSA un cambio en la propiedad o las condiciones operativas de la empresa mixta Petromonagas antes del 30 de septiembre de 2025?',
    '003': '¿Anunciará PDVSA un nuevo socio u operador extranjero para Petrocedeño antes del 30 de septiembre de 2025?',
    '004': '¿Se publicará en la Gaceta Oficial una nueva empresa mixta o un contrato de servicios que abarque algún bloque Carabobo antes del 31 de marzo de 2026?',
    '005': '¿Se dictará una orden judicial estadounidense o un laudo arbitral que mencione cargamentos o cuentas por cobrar de la terminal de José antes del 30 de septiembre de 2025?',
    '006': '¿Habrá una paralización de al menos 48 horas que afecte a un mejorador del complejo de José, documentada por dos fuentes independientes o por un informe de terreno y una información de prensa, antes del 31 de marzo de 2025?',
    '007': '¿Habrá una paralización laboral o un cierre operativo de al menos 48 horas en los campos de Punta de Mata antes del 31 de marzo de 2025?',
    '008': '¿Perderá el complejo de José el suministro eléctrico de la red durante más de 24 horas en una misma semana antes del 31 de marzo de 2025?',
    '009': '¿Mostrarán los datos semanales de la EIA importaciones estadounidenses de crudo venezolano iguales a cero durante dos semanas consecutivas antes del 31 de marzo de 2025?',
    '010': '¿Informarán PDVSA o un socio de que el mejorador Petrocedeño ha reanudado operaciones sostenidas antes del 30 de septiembre de 2025?',
    '011': '¿Se informará de un incidente armado, robo de equipos o productos, o extorsión a un contratista en un radio de 25 km de El Furrial antes del 31 de marzo de 2025?',
    '012': '¿Asumirán las fuerzas armadas o un mando ZODI el control de acceso o la seguridad del complejo de José antes del 30 de septiembre de 2025?',
    '013': '¿Se informará de un bloqueo de una vía de acceso o puerta del complejo de José que dure al menos 12 horas antes del 31 de marzo de 2025?',
    '014': '¿Provocará un derrame de petróleo o incendio en Jusepín o sus alrededores una protesta comunitaria o una inspección oficial antes del 30 de septiembre de 2025?',
    '015': '¿Será sustituido, suspendido o destituido el gobernador de Anzoátegui antes del 30 de septiembre de 2025?',
    '016': '¿Será sustituido, suspendido o destituido el gobernador de Monagas antes del 30 de septiembre de 2025?',
    '017': '¿Será sustituido el jefe de la división Oriente de PDVSA antes del 31 de marzo de 2025?',
    '018': '¿Informarán trabajadores o contratistas de Punta de Mata de atrasos salariales o de facturas de al menos cuatro semanas antes del 31 de marzo de 2025?',
    '019': '¿Informarán contratistas del complejo de José de facturas impagadas durante al menos cuatro semanas antes del 31 de marzo de 2025?',
    '020': '¿Cambiará el canal de liquidación de las ventas de crudo de Petropiar, en cuanto a moneda, intermediario o banco, según dos fuentes independientes, antes del 30 de septiembre de 2025?',
  };
  const human = value => value == null || value === '' ? t('Unknown', 'Desconocida') : (labels[value] || String(value).replaceAll('_', ' '));
  const monthName = month => new Date(`${month}-01T12:00:00Z`).toLocaleDateString(locale, {month: 'long', year: 'numeric', timeZone: 'UTC'});
  const dateName = date => new Date(date.slice(0, 10) + 'T12:00:00Z').toLocaleDateString(locale, {day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC'});
  const cutoff = (month, asOf) => {
    const [y, m] = month.split('-').map(Number);
    const last = new Date(Date.UTC(y, m, 0)).toISOString().slice(0, 10);
    return last < asOf ? last : asOf;
  };
  const openQuestions = (questions, asset, at) => questions.filter(q => q.asset_id === asset && q.opened_at.slice(0, 10) <= at && q.resolution_date.slice(0, 10) >= at).map(q => {
    const snapshot = q.series.filter(([date]) => date.slice(0, 10) <= at).at(-1);
    return {...q, snapshot};
  });
  const completedWeeks = (rows, at) => rows.filter(([date]) => new Date(`${date}T00:00:00Z`).getTime() + 6 * 86400000 <= new Date(`${at}T00:00:00Z`).getTime());
  const eventPaint = p => ({
    radius: ({low: 4, medium: 7, high: 10})[p.severity] || 6,
    colour: p.corroboration_status === 'contradicted' ? '#ad4328' : p.corroboration_status === 'unassessed' ? '#68636c' : '#5a3878',
    opacity: p.corroboration_status === 'single_source' ? 0.45 : 1,
    fill: p.severity == null || p.corroboration_status === 'contradicted' ? 0 : 1,
  });
  function circle(feature) {
    const [lon, lat] = feature.geometry.coordinates.map(n => n * Math.PI / 180);
    const angular = 25 / 6371.0088;
    const ring = Array.from({length: 65}, (_, i) => {
      const bearing = i / 64 * Math.PI * 2;
      const y = Math.asin(Math.sin(lat) * Math.cos(angular) + Math.cos(lat) * Math.sin(angular) * Math.cos(bearing));
      const x = lon + Math.atan2(Math.sin(bearing) * Math.sin(angular) * Math.cos(lat), Math.cos(angular) - Math.sin(lat) * Math.sin(y));
      return [x * 180 / Math.PI, y * 180 / Math.PI];
    });
    return {type: 'Feature', properties: {}, geometry: {type: 'Polygon', coordinates: [ring]}};
  }
  // Pure data rules are exposed for reproducible browser checks.
  window.EchoFrameGIS = {cutoff, openQuestions, completedWeeks, eventPaint, circle};
  let catalogue, boundaries, map, mapReady = false, fallback = false, currentEvents = [];
  let index = 23, generation = 0, playing = false, timer, selectedAsset = '', loadedMonth = '';
  const cache = new Map();
  async function json(url) {
    const response = await fetch(url, {signal: AbortSignal.timeout(15000)});
    if (!response.ok) throw new Error('Data unavailable');
    return response.json();
  }
  function eventsFor(month) {
    if (!cache.has(month)) cache.set(month, json(`${root}months/${month}.json`).catch(error => {cache.delete(month); throw error;}));
    return cache.get(month);
  }
  function resetDetail() {
    $('gis-detail').replaceChildren(el('h2', t('Select an event or asset', 'Seleccione un evento o activo')),
      el('p', t('Use the map or the lists above. Records at the same location can be selected individually from the event list.', 'Utilice el mapa o las listas. Los registros que comparten ubicación se pueden seleccionar individualmente en la lista.')));
  }
  function definitionList(rows) {
    const list = el('dl');
    rows.forEach(([key, value]) => {const row = el('div'); row.append(el('dt', key), el('dd', value)); list.append(row);});
    return list;
  }
  function showEvent(id, focus = false) {
    const feature = currentEvents.find(f => f.properties.event_id === id);
    if (!feature) return;
    pause(); selectedAsset = ''; $('gis-asset').value = ''; $('gis-event').value = id;
    const p = feature.properties;
    const detail = $('gis-detail');
    detail.replaceChildren(el('h2', t('Event record', 'Registro de evento')), el('span', human(p.corroboration_status), 'gis-badge'));
    detail.append(definitionList([
      [t('Type code', 'Código de tipo'), p.type], [t('Family code', 'Código de familia'), p.family],
      [t('Severity', 'Gravedad'), human(p.severity)], [t('Status', 'Estado'), human(p.corroboration_status)],
      [t('Freshness', 'Vigencia'), human(p.freshness)], [t('First seen', 'Primera observación'), dateName(p.first_seen)],
      [t('Last seen', 'Última observación'), dateName(p.last_seen)], [t('Source count', 'Recuento de fuentes'), String(p.source_count)],
      [t('State', 'Estado territorial'), p.state], [t('Location precision', 'Precisión geográfica'), human(p.location_precision)],
    ]));
    detail.append(el('h3', t('Source blocks', 'Bloques de fuentes')));
    const blocks = el('ul'); (p.source_blocks || []).forEach(block => blocks.append(el('li', human(block))));
    detail.append(blocks.childElementCount ? blocks : el('p', t('No source blocks recorded', 'Sin bloques de fuentes registrados')));
    detail.append(el('p', t('The source count counts items. It does not establish independence. Freshness and status are stored snapshot labels.', 'El recuento cuenta elementos. No establece independencia. La vigencia y el estado son etiquetas almacenadas.')));
    if (p.location_precision !== 'facility') detail.append(el('p', t('This record does not establish an incident at a specific facility.', 'Este registro no establece un incidente en una instalación concreta.'), 'gis-detail-note'));
    if (p.point_in_state_polygon === false) detail.append(el('p', t('The stored point is outside its recorded state boundary. The location requires review.', 'El punto almacenado está fuera del límite de su estado registrado. La ubicación requiere revisión.'), 'gis-detail-note'));
    if (focus) detail.focus({preventScroll: true});
  }
  function makeChart(series, labelsX, selected, small = false) {
    const width = small ? 320 : 900, height = small ? 110 : 210, left = small ? 10 : 32, right = width - 12, bottom = height - 27, top = 15;
    const max = Math.max(1, ...series.flatMap(s => s.values));
    const x = i => left + i / Math.max(1, labelsX.length - 1) * (right - left);
    const y = value => bottom - value / max * (bottom - top);
    const svg = svgEl('svg', {viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-label': small ? t('Weekly event counts', 'Recuentos semanales de eventos') : t('Monthly corroborated event counts for both states', 'Recuentos mensuales de eventos corroborados en ambos estados')});
    svg.append(svgEl('title', {}, small ? t('Weekly event counts', 'Recuentos semanales de eventos') : t('Corroborated events by month', 'Eventos corroborados por mes')));
    svg.append(svgEl('desc', {}, t('Exact values are available in the adjacent table.', 'Los valores exactos están disponibles en la tabla adjunta.')));
    [0, max].forEach(value => {svg.append(svgEl('line', {x1: left, x2: right, y1: y(value), y2: y(value), stroke: '#dedbd7'})); if (!small) svg.append(svgEl('text', {x: 4, y: y(value) + 4, fill: '#68636c', 'font-size': 11}, value));});
    if (selected >= 0) svg.append(svgEl('line', {x1: x(selected), x2: x(selected), y1: top, y2: bottom, stroke: '#8d8295', 'stroke-dasharray': '3 4'}));
    series.forEach((s, n) => {
      if (!s.values.length) return;
      svg.append(svgEl('polyline', {points: s.values.map((v, i) => `${x(i)},${y(v)}`).join(' '), fill: 'none', stroke: colours[n], 'stroke-width': 2, ...(n ? {'stroke-dasharray': '5 3'} : {})}));
      s.values.forEach((v, i) => {const point = svgEl('circle', {cx: x(i), cy: y(v), r: small ? 1.7 : 3, fill: colours[n]}); point.append(svgEl('title', {}, `${s.name} · ${labelsX[i]} · ${v}`)); svg.append(point);});
    });
    [0, labelsX.length - 1].forEach((i, n) => {if (i >= 0) svg.append(svgEl('text', {x: x(i), y: height - 6, 'text-anchor': n ? 'end' : 'start', fill: '#68636c', 'font-size': small ? 10 : 12}, labelsX[i]));});
    return svg;
  }
  function table(headers, rows) {
    const result = el('table'), head = el('thead'), tr = el('tr'), body = el('tbody');
    headers.forEach(value => {const th = el('th', value); th.scope = 'col'; tr.append(th);}); head.append(tr);
    rows.forEach(values => {const row = el('tr'); values.forEach((value, i) => {const cell = el(i ? 'td' : 'th', String(value)); if (!i) cell.scope = 'row'; row.append(cell);}); body.append(row);});
    result.append(head, body); return result;
  }
  function showAsset(id, focus = false) {
    if (!id) return;
    selectedAsset = id; $('gis-asset').value = id; $('gis-event').value = '';
    const detail = $('gis-detail'), at = cutoff(catalogue.months[index], catalogue.export_as_of);
    detail.replaceChildren(el('h2', names[id] || human(id)));
    const sites = catalogue.assets.features.filter(f => f.properties.asset_id === id);
    if (!sites.length) detail.append(el('p', t('This question scope is a state or organisation. It has no asset pin.', 'Este ámbito corresponde a un estado o una organización. No tiene marcador de activo.')));
    sites.forEach((site, i) => {
      const p = site.properties;
      detail.append(el('h3', `${t('Site', 'Sitio')} ${i + 1} · ${human(p.type)}`));
      detail.append(el('p', site.geometry ? t('Approximate coordinates. The faint circle shows a 25 km reference radius.', 'Coordenadas aproximadas. El círculo tenue muestra un radio de referencia de 25 km.') : t('Coordinates unresolved. No map pin is shown.', 'Coordenadas sin resolver. No se muestra un marcador.')));
      if (p.coordinate_source) {
        const link = el('a', t('Coordinate source', 'Fuente de coordenadas')); link.href = p.coordinate_source; link.target = '_blank'; link.rel = 'noopener noreferrer'; detail.append(link);
      }
    });
    const weekly = completedWeeks(catalogue.asset_series[id] || [], at);
    detail.append(el('h3', t('Weekly assigned events', 'Eventos asignados por semana')));
    if (weekly.length) {
      detail.append(makeChart([{name: names[id] || id, values: weekly.map(row => row[1])}], weekly.map(row => dateName(row[0])), -1, true));
      const values = el('details', undefined, 'gis-table'); values.append(el('summary', t('Read weekly counts', 'Consultar recuentos semanales')), table([t('Week starting', 'Inicio de semana'), t('Events', 'Eventos')], weekly.map(([date, count]) => [dateName(date), count]))); detail.append(values);
    } else detail.append(el('p', t('No weekly asset series is available at this date.', 'No hay serie semanal disponible para esta fecha.')));
    detail.append(el('p', t('Counts use exact asset assignments, not proximity. Only completed weeks are shown.', 'Los recuentos usan asignaciones exactas, no proximidad. Solo se muestran semanas completas.')));
    detail.append(el('h3', t('Open questions at this date', 'Preguntas abiertas en esta fecha')),
      el('span', t('Hindcast · Provisional · Indicative', 'Retrospectiva · Provisional · Indicativa'), 'gis-badge'));
    const questions = openQuestions(catalogue.questions, id, at);
    if (!questions.length) detail.append(el('p', t('No open questions at this date. Move the month control to an earlier date to inspect the historical question set.', 'No hay preguntas abiertas en esta fecha. Seleccione un mes anterior para consultar las preguntas históricas.')));
    questions.forEach(q => {
      const item = el('article', undefined, 'gis-question');
      item.append(el('small', `${q.question_id} · ${human(q.client_profile)} · ${q.family}`));
      item.append(el('p', es ? questionES[q.question_id.slice(-3)] || q.wording : q.wording));
      item.append(el('strong', q.snapshot ? `${Math.round(q.snapshot[1] * 100)}%` : t('Unavailable', 'No disponible')));
      item.append(el('small', q.snapshot ? `${t('Stored estimate', 'Estimación almacenada')} · ${dateName(q.snapshot[0])}` : t('No stored estimate by this date', 'Sin estimación almacenada hasta esta fecha')));
      item.append(el('small', `${t('Question deadline', 'Fecha límite')} · ${dateName(q.resolution_date)}`)); detail.append(item);
    });
    detail.append(el('p', t('Retrospective estimates are not a track record. The probabilities can draw on evidence outside the map area. Profile variants are not independent forecasts.', 'Las estimaciones retrospectivas no son un historial predictivo. Las probabilidades pueden usar evidencia externa al área del mapa. Las variantes por perfil no son pronósticos independientes.')));
    if (focus) detail.focus({preventScroll: true});
  }
  function chart() {
    const series = catalogue.states.map(name => ({name, values: catalogue.state_counts[name]}));
    const key = el('div', undefined, 'gis-chart-key'); series.forEach(s => {const label = el('span'); label.append(el('i'), el('span', s.name)); key.append(label);});
    $('gis-chart').replaceChildren(makeChart(series, catalogue.months.map(monthName), index), key);
    $('gis-counts').replaceChildren(table([t('Month', 'Mes'), ...catalogue.states], catalogue.months.map((month, i) => [monthName(month), ...series.map(s => s.values[i])])));
  }
  const shade = value => value >= 4 ? '#5a3878' : value >= 2 ? '#9275ae' : value >= 1 ? '#c8b6d9' : '#e9e7e5';
  function dataLayers() {
    const month = catalogue.months[index], counts = catalogue.monthly_counts[month];
    const municipalities = FC(boundaries.municipalities.features.map(f => ({...f, properties: {...f.properties, count: counts[f.properties.boundary_id] || 0}})));
    const points = FC(currentEvents.filter(f => f.properties.location_precision !== 'state').map(f => ({...f, properties: {...f.properties, ...eventPaint(f.properties)}})));
    const states = FC(catalogue.states.filter(state => currentEvents.some(f => f.properties.location_precision === 'state' && f.properties.state === state)).map(state => ({type: 'Feature', geometry: boundaries.states[state], properties: {state}})));
    return {municipalities, points, states};
  }
  function updateMap() {
    if (!boundaries) return;
    const data = dataLayers();
    if (fallback) {drawFallback(data); return;}
    if (!mapReady) return;
    Object.entries(data).forEach(([key, value]) => map.getSource(key).setData(value));
  }
  function drawFallback(data) {
    const container = $('gis-map'); container.classList.add('gis-map-fallback');
    const svg = svgEl('svg', {viewBox: '0 0 800 520', role: 'img', 'aria-label': t('Municipality and event map. Use the record lists for details.', 'Mapa de municipios y eventos. Utilice las listas para consultar detalles.')});
    const project = ([x, y]) => [(x + 65.9) * 170, 500 - (y - 7.55) * 165];
    function shape(f, fill, opacity, stroke) {
      const polygons = f.geometry.type === 'Polygon' ? [f.geometry.coordinates] : f.geometry.coordinates;
      const path = polygons.map(p => p.map(r => r.map((c, i) => `${i ? 'L' : 'M'}${project(c).join(',')}`).join('') + 'Z').join('')).join('');
      return svgEl('path', {d: path, fill, 'fill-opacity': opacity, stroke, 'stroke-width': .6, 'fill-rule': 'evenodd'});
    }
    data.municipalities.features.forEach(f => svg.append(shape(f, shade(f.properties.count), 1, '#8d8396')));
    data.states.features.forEach(f => {const node = shape(f, '#65799c', .12, '#65799c'); node.addEventListener('click', () => showEvent(currentEvents.find(e => e.properties.state === f.properties.state && e.properties.location_precision === 'state').properties.event_id, true)); svg.append(node);});
    catalogue.assets.features.filter(f => f.geometry).forEach(f => svg.append(shape(circle(f), '#dc6540', .035, '#dc654055')));
    data.points.features.forEach(f => {const [cx, cy] = project(f.geometry.coordinates), p = f.properties; const node = svgEl('circle', {cx, cy, r: p.radius, fill: p.colour, 'fill-opacity': p.fill * p.opacity, stroke: p.colour, 'stroke-opacity': p.opacity, 'stroke-width': 1.5}); node.addEventListener('click', () => showEvent(p.event_id, true)); svg.append(node);});
    catalogue.assets.features.filter(f => f.geometry).forEach(f => {const [cx, cy] = project(f.geometry.coordinates); const point = svgEl('circle', {cx, cy, r: 5, fill: '#dc6540', stroke: '#fffefa', 'stroke-width': 1.5}); point.addEventListener('click', () => showAsset(f.properties.asset_id, true)); svg.append(point);});
    container.replaceChildren(svg, el('p', t('Simplified map. Interactive zoom is unavailable. Use the record lists to inspect every record.', 'Mapa simplificado. El zoom interactivo no está disponible. Utilice las listas para examinar todos los registros.')));
  }
  function basemapCredit(active) {
    const node = $('gis-basemap'); node.replaceChildren();
    if (active) {node.append(document.createTextNode(t('Basemap by ', 'Mapa base de '))); const link = el('a', 'OpenFreeMap'); link.href = 'https://openfreemap.org/'; node.append(link, document.createTextNode(' · © OpenMapTiles · '));}
    else node.append(document.createTextNode(t('No basemap. Municipality boundaries shown in grey. ', 'Sin mapa base. Límites municipales mostrados en gris. ')));
    const osm = el('a', '© OpenStreetMap contributors'); osm.href = 'https://www.openstreetmap.org/copyright'; node.append(osm);
  }
  async function addBasemap() {
    // The shared data + library reserve leaves 0.8 MB for optional basemap data.
    // Keep the analytical layers usable if the service fails or this budget is spent.
    let used = 0, unavailable = false;
    const remove = () => {
      if (unavailable) return; unavailable = true;
      if (map) {
        for (const id of ['base-roads', 'base-water']) if (map.getLayer(id)) map.removeLayer(id);
        if (map.getSource('openfreemap')) map.removeSource('openfreemap');
      }
      basemapCredit(false);
    };
    async function limited(url, signal) {
      if (unavailable) throw new Error('Basemap unavailable');
      const response = await fetch(url, {signal: signal || AbortSignal.timeout(6000)});
      if (!response.ok) throw new Error('Basemap unavailable');
      const reader = response.body.getReader(), chunks = []; let length = 0;
      for (;;) {
        const {done, value} = await reader.read(); if (done) break;
        used += value.byteLength;
        if (unavailable || used > 800000) {await reader.cancel(); throw new Error('Basemap budget reached');}
        length += value.byteLength; chunks.push(value);
      }
      const result = new Uint8Array(length); let offset = 0;
      chunks.forEach(chunk => {result.set(chunk, offset); offset += chunk.length;}); return result.buffer;
    }
    try {
      const style = JSON.parse(new TextDecoder().decode(await limited('https://tiles.openfreemap.org/styles/liberty')));
      const source = Object.values(style.sources).find(s => s.type === 'vector');
      if (!source) throw new Error('No vector basemap');
      const tilejson = source.url ? JSON.parse(new TextDecoder().decode(await limited(source.url))) : source;
      if (!tilejson.tiles?.length) throw new Error('No tiles');
      maplibregl.addProtocol('gis-budget', async (params, abortController) => {
        try {return {data: await limited(params.url.replace('gis-budget://', ''), abortController.signal)};}
        catch (error) {if (error.name !== 'AbortError') setTimeout(remove, 0); throw error;}
      });
      map.addSource('openfreemap', {type: 'vector', tiles: tilejson.tiles.map(url => 'gis-budget://' + url), minzoom: tilejson.minzoom || 0, maxzoom: tilejson.maxzoom || 14});
      map.addLayer({id: 'base-water', source: 'openfreemap', 'source-layer': 'water', type: 'fill', paint: {'fill-color': '#d6dfe0'}}, 'municipalities-fill');
      map.addLayer({id: 'base-roads', source: 'openfreemap', 'source-layer': 'transportation', type: 'line', paint: {'line-color': '#bcb6ac', 'line-width': .7}}, 'municipalities-fill');
      basemapCredit(true);
    } catch (_) {remove();}
  }
  async function initialiseMap() {
    try {
      if (!window.maplibregl) throw new Error('Map library unavailable');
      map = new maplibregl.Map({container: 'gis-map', style: {version: 8, sources: {}, layers: [{id: 'paper', type: 'background', paint: {'background-color': '#eeece8'}}]},
        center: [-63.65, 9.35], zoom: 6.3, minZoom: 5, maxZoom: 12, maxBounds: [[-68, 6], [-60, 12]], attributionControl: false,
        dragRotate: false, pitchWithRotate: false, touchPitch: false, cooperativeGestures: true,
        locale: es ? {'NavigationControl.ZoomIn': 'Acercar', 'NavigationControl.ZoomOut': 'Alejar', 'CooperativeGesturesHandler.WindowsHelpText': 'Use Ctrl y la rueda para ampliar el mapa', 'CooperativeGesturesHandler.MacHelpText': 'Use ⌘ y la rueda para ampliar el mapa', 'CooperativeGesturesHandler.MobileHelpText': 'Use dos dedos para mover el mapa', 'Map.Title': 'Mapa'} : {}});
      window.EchoFrameGIS.map = map;
      await new Promise((resolve, reject) => {const timeout = setTimeout(() => reject(new Error('Map timed out')), 10000); map.once('load', () => {clearTimeout(timeout); resolve();});});
      map.addControl(new maplibregl.NavigationControl({showCompass: false}), 'top-right');
      map.addControl(new maplibregl.ScaleControl({unit: 'metric'}));
      map.getCanvas().setAttribute('aria-label', t('Map. Use the event and asset lists for record details.', 'Mapa. Use las listas de eventos y activos para consultar detalles.'));
      const data = dataLayers();
      Object.entries(data).forEach(([id, value]) => map.addSource(id, {type: 'geojson', data: value}));
      map.addLayer({id: 'municipalities-fill', type: 'fill', source: 'municipalities', paint: {'fill-color': ['step', ['get', 'count'], '#e9e7e5', 1, '#c8b6d9', 2, '#9275ae', 4, '#5a3878'], 'fill-opacity': .78}});
      map.addLayer({id: 'municipalities-line', type: 'line', source: 'municipalities', paint: {'line-color': '#81788a', 'line-width': .6}});
      map.addLayer({id: 'state-records', type: 'fill', source: 'states', paint: {'fill-color': '#65799c', 'fill-opacity': .12}});
      map.addLayer({id: 'state-borders', type: 'line', source: 'states', paint: {'line-color': '#65799c', 'line-width': 1.4, 'line-dasharray': [3, 2]}});
      const resolved = catalogue.assets.features.filter(f => f.geometry);
      map.addSource('radii', {type: 'geojson', data: FC(resolved.map(circle))});
      map.addLayer({id: 'radii-fill', type: 'fill', source: 'radii', paint: {'fill-color': '#dc6540', 'fill-opacity': .035}});
      map.addLayer({id: 'radii-line', type: 'line', source: 'radii', paint: {'line-color': '#dc6540', 'line-opacity': .3, 'line-width': .7}});
      map.addLayer({id: 'event-points', type: 'circle', source: 'points', paint: {'circle-radius': ['get', 'radius'], 'circle-color': ['get', 'colour'], 'circle-opacity': ['*', ['get', 'opacity'], ['get', 'fill']], 'circle-stroke-color': ['get', 'colour'], 'circle-stroke-width': 1.7, 'circle-stroke-opacity': ['get', 'opacity']}});
      map.addSource('assets', {type: 'geojson', data: FC(resolved)});
      map.addLayer({id: 'asset-points', type: 'circle', source: 'assets', paint: {'circle-radius': 5, 'circle-color': '#dc6540', 'circle-stroke-color': '#fffefa', 'circle-stroke-width': 1.5}});
      map.on('click', event => {
        if (loadedMonth !== catalogue.months[index]) return;
        const hits = map.queryRenderedFeatures(event.point, {layers: ['asset-points', 'event-points', 'state-records']});
        const asset = hits.find(h => h.layer.id === 'asset-points'), point = hits.find(h => h.layer.id === 'event-points');
        if (asset) {pause(); showAsset(asset.properties.asset_id, true);}
        else if (point) showEvent(point.properties.event_id, true);
        else if (hits.length) showEvent(currentEvents.find(f => f.properties.location_precision === 'state' && f.properties.state === hits[0].properties.state).properties.event_id, true);
      });
      mapReady = true; updateMap(); addBasemap();
    } catch (_) {
      if (map) {map.remove(); map = null; window.EchoFrameGIS.map = null;}
      fallback = true; basemapCredit(false); updateMap();
    }
  }
  async function selectMonth(next) {
    index = next; const request = ++generation, month = catalogue.months[index];
    $('gis-month').value = index; $('gis-month-label').value = monthName(month); $('gis-month').setAttribute('aria-valuetext', monthName(month));
    $('gis-status').textContent = t('Loading records for ', 'Cargando registros de ') + monthName(month);
    $('gis-event').disabled = true; $('gis-asset').disabled = true; $('gis-retry').hidden = true;
    currentEvents = []; loadedMonth = ''; delete host.dataset.loadedMonth; updateMap(); resetDetail(); chart();
    try {
      const data = await eventsFor(month);
      if (request !== generation) return false;
      currentEvents = data.features; loadedMonth = month;
      $('gis-event').replaceChildren(new Option(t('Select an event', 'Seleccione un evento'), ''));
      currentEvents.forEach((f, i) => {const p = f.properties; $('gis-event').append(new Option(`${String(i + 1).padStart(2, '0')} · ${p.type} · ${p.state} · ${p.first_seen.slice(0, 10)}`, p.event_id));});
      $('gis-event').disabled = !currentEvents.length; $('gis-asset').disabled = false;
      const corroborated = currentEvents.filter(f => f.properties.corroboration_status === 'corroborated').length;
      const state = currentEvents.filter(f => f.properties.location_precision === 'state').length;
      $('gis-status').textContent = `${monthName(month)} · ${currentEvents.length} ${t('events', 'eventos')} · ${corroborated} ${t('corroborated', 'corroborados')} · ${state} ${t('located to a state', 'ubicados a nivel estatal')}`;
      host.dataset.loadedMonth = month;
      updateMap(); if (selectedAsset) showAsset(selectedAsset);
      return true;
    } catch (_) {
      if (request !== generation) return false;
      pause(); $('gis-status').textContent = t('This month could not be loaded. No event count is shown. Retry or choose another month.', 'No se pudo cargar este mes. No se muestra un recuento. Reintente o elija otro mes.');
      $('gis-retry').hidden = false; return false;
    }
  }
  function pause() {playing = false; clearTimeout(timer); $('gis-play').textContent = t('Play', 'Reproducir'); $('gis-play').setAttribute('aria-pressed', 'false');}
  async function step() {
    if (!playing) return;
    if (index === 23) {pause(); return;}
    await selectMonth(index + 1);
    if (playing) timer = setTimeout(step, 1300);
  }
  async function start() {
    try {
      [catalogue, boundaries] = await Promise.all([json(root + 'catalogue.json'), json(root + 'boundaries.json')]);
      const assetIds = [...new Set([...catalogue.assets.features.map(f => f.properties.asset_id), ...catalogue.questions.map(q => q.asset_id)])];
      $('gis-asset').replaceChildren(new Option(t('Select an asset or scope', 'Seleccione un activo o ámbito'), ''));
      assetIds.forEach(id => $('gis-asset').append(new Option(names[id] || human(id), id)));
      $('gis-month').disabled = false; $('gis-play').disabled = false;
      await selectMonth(23); await initialiseMap();
    } catch (_) {
      $('gis-status').textContent = t('The export could not be loaded. Reload this page to retry. No data is inferred.', 'No se pudo cargar la exportación. Recargue la página para reintentar. No se infieren datos.');
      basemapCredit(false);
    }
  }
  $('gis-event').addEventListener('change', event => showEvent(event.target.value));
  $('gis-asset').addEventListener('change', event => {pause(); showAsset(event.target.value);});
  $('gis-month').addEventListener('input', event => {pause(); selectMonth(Number(event.target.value));});
  $('gis-play').addEventListener('click', async () => {
    if (playing) {pause(); return;}
    playing = true; $('gis-play').textContent = t('Pause', 'Pausar'); $('gis-play').setAttribute('aria-pressed', 'true');
    if (index === 23) await selectMonth(0);
    if (playing) timer = setTimeout(step, 1300);
  });
  $('gis-retry').addEventListener('click', () => selectMonth(index));
  document.addEventListener('visibilitychange', () => {if (document.hidden) pause();});
  start();
})();
