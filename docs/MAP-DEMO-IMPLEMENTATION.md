# Public GIS map demonstration

Prepared on branch `feat/public-demo-map` and subsequently merged into `main` at the user's request. Published on 12 September 2026 through the live deployment repository `EchoFrame-Ltd/echoframe-team-preview`.

The deployed merge commit is `27ea1045ab44edc758a30f4f45bd668c3f6a603d`. The authoring branch was merged locally as `c734aa8f2526931732d06d90de729fc81bd2b724`. Only the 32 map publication files were sent to the deployment repository. Raw export inputs and authoring documents were not published.

Live verification completed at 20:03 UTC on 12 September 2026. Both https://www.echoframe.co/map.html and https://www.echoframe.co/es/map.html returned HTTP 200, with working MapLibre layers, OpenFreeMap basemap, month controls and question details. The apex domain redirects to the same pages on `www`.

The English live payload measured **4,775,438 bytes** and the Spanish live payload measured **4,776,296 bytes**. These conservative totals include all 24 monthly event files, shared data, page resources, fonts, MapLibre, basemap tiles and the generated worker blob. Both are below 5 MB. OpenStreetMap attribution and the ODbL link were present on both live pages. Every deployed file matched the SHA-256 digest of the published Git blob.

The live Venezuela page contains the `See the map` link. The `services.html` link remains pending as requested. Live screenshots, response sizes and digest results are retained in `.preview/map-live-verification.json` and `.preview/live-map-*.png`.

The English page is `map.html`. The Spanish page is `es/map.html`. Both use the site's existing typography and colour tokens. The Venezuela page links to the demonstration. The Asset Watch link remains pending because `services.html` and `docs/services_copy.md` are absent. The earlier instruction requires Rob's copy before that service page can be written.

Local review is available at http://127.0.0.1:4173/map.html and http://127.0.0.1:4173/es/map.html while `python server.py` is running. The server serves the generated `public/` directory.

## Data and behaviour

The approved export was copied into `docs/gis_demo/` from the Venezuela analyst repository. Its eight source files remain unchanged. The original ZIP was not copied. The source README, internal paths and raw source files are excluded from `public/`.

The source contains 457 events across parts of 25 calendar months. The demonstration shows the latest 24 calendar months, October 2024 through September 2026. It contains 446 events. Eleven events from the initial partial month of September 2024 remain in the source export. September 2026 is explicitly marked as partial. The snapshot is dated 12 September 2026 and the last collected event is dated 10 September.

There are 34 municipality polygons, 14 asset site records representing 11 assets, and 20 question definitions with 28 profile variants. Two asset coordinates are unresolved. They remain accessible in the asset selector without fabricated map pins. State and organisational question scopes are selectable too.

Municipality shading uses the supplied monthly counts, aggregated across families during the static build. The state chart counts all corroborated events in their first-seen month, including state-only records. State-only events do not enter municipality counts. Asset sparklines use exact asset assignments and completed Monday-to-Sunday weeks. A 25 km circle is a reference radius, not an attribution rule.

The browser fetches the catalogue and shared boundaries once. It loads each selected month's event file on demand and caches successful requests. The build stores each state polygon once. The browser renders one area per state with records in that month. The event selector provides access to every individual record, including overlapping events. Month changes cannot move state records into point layers. A failed month clears the prior event layer and displays a retry control rather than a false zero.

All supplied events have unknown severity, so their points are hollow. The rendering rules also support low, medium and high severity, corroborated records, faded single-source records and outlined contradicted records. Two stored point and state boundary mismatches remain flagged in the detail panel.

Question panels select the latest stored probability available by the selected month end, capped by the export date. Questions disappear after their resolution horizon. No future estimate is carried backwards and no expired question is extended forwards. Every panel labels the estimates hindcast, provisional and indicative. Spanish question wording is translated for presentation. The supplied English wording remains in the data.

## Boundaries and basemap

The supplied export uses OpenStreetMap boundaries rather than GADM. Attribution therefore credits OpenStreetMap contributors and includes the ODbL licence and a link to the derived boundary database. No GADM attribution is invented. Display coordinates are rounded to five decimal places without changing event precision. The supplied administrative areas retain their water areas.

MapLibre GL JS and CSS are pinned to `5.24.0` on cdnjs. OpenFreeMap supplies the keyless basemap. The page uses its vector water and road layers without an additional font or sprite download. Both provider availability and its tile requests are handled separately from the event data. A grey municipality map remains if the provider is unavailable or the optional basemap transfer allowance is exhausted. A local inline SVG map and the record selectors remain available if MapLibre or WebGL cannot load.

References used for integration are the [OpenFreeMap quick start](https://openfreemap.org/quick_start/), [MapLibre protocol documentation](https://maplibre.org/maplibre-gl-js/docs/API/functions/addProtocol/) and [cdnjs library listing](https://cdnjs.com/libraries/maplibre-gl).

## Field handling

No article headline or article text fields were present in the supplied export. None had to be removed from event records. Event properties use an explicit allowlist. The build rejects a nested field named `title`, `headline`, `text`, `body`, `reporter`, `actor`, `item_id`, `item_ids` or `actor_names`. Question `wording` is retained because the requested question panel requires the fixed question definition. SVG accessibility titles are chart descriptions, not article titles.

The following reductions apply to the browser payload only. The original input files are retained unchanged.

| Input | Browser treatment |
| --- | --- |
| Repeated state event geometry | Stored once per state and joined for display. No point substitution. |
| Municipality centroid fields | `display_centroid_lat`, `display_centroid_lon`, `display_centroid_method`, `full_centroid_lat`, `full_centroid_lon`, `land_centroid_lat` and `land_centroid_lon` are omitted. The browser uses the approved event geometry. |
| Asset `coordinate_source` | The attribution URL is retained. Internal file paths and accompanying research notes are omitted. Unresolved values remain null. |
| Monthly count columns | Only municipality and month corroborated totals are sent for shading. The build sums families. Status and severity marginals remain in the source CSV. |
| Asset weekly count columns | The chart uses `asset_id`, `week_start` and `total`. Status marginals, `type_*` marginals and joint type/status columns remain in the source CSV. |
| Question `availability` | Omitted from the browser payload. Explicit hindcast, provisional and indicative flags remain, along with dates, profiles, wording and every stored probability snapshot. |

The complete generated GIS data occupies **2,096,735 bytes**, including all 24 monthly files and the boundary licence. The browser check conservatively totals the full data directory plus measured page resources, including fonts, MapLibre, the basemap and the generated worker blob. The measured total is about **4.78 MB**, below 5 MB. The build caps data at 2.5 MB and the browser caps optional basemap data at 0.8 MB.

## Verification

Run `python scripts/build.py`, start `python server.py`, then run `python scripts/check_site.py` and `python scripts/check_map.py`.

The map check verifies exact event membership against the supplied export, municipality and state counts, state geometry, forbidden fields, unresolved assets, coordinate source filtering, month caching, rapid month changes, failed requests and retry, actual map selection, 25 km radii, all severity and corroboration styles, provisional question timing, completed-week filtering, playback, the size budget and English and Spanish layouts at 320, 390, 768 and 1440 pixels. It exercises both basemap failure and CDN failure. When the existing local axe script is available, it checks WCAG A and AA accessibility too.

The site link checker passes for 35 published HTML pages. `python scripts/refinement_check.py` also passes across all 35 pages at 320, 390, 768 and 1440 pixels, with no browser page errors. Its contact checks use mocked responses only. Browser artefacts and request sizes are kept locally in `.preview/`, which is excluded from publication.

## Files changed

The exact task file list follows. Generated files under `public/` are local build output and are ignored by Git. Existing unrelated changes in the working tree were retained.

<!-- FILE_MANIFEST -->

- `assets/gis-demo/LICENSE.txt`
- `assets/gis-demo/boundaries.json`
- `assets/gis-demo/catalogue.json`
- `assets/gis-demo/months/2024-10.json`
- `assets/gis-demo/months/2024-11.json`
- `assets/gis-demo/months/2024-12.json`
- `assets/gis-demo/months/2025-01.json`
- `assets/gis-demo/months/2025-02.json`
- `assets/gis-demo/months/2025-03.json`
- `assets/gis-demo/months/2025-04.json`
- `assets/gis-demo/months/2025-05.json`
- `assets/gis-demo/months/2025-06.json`
- `assets/gis-demo/months/2025-07.json`
- `assets/gis-demo/months/2025-08.json`
- `assets/gis-demo/months/2025-09.json`
- `assets/gis-demo/months/2025-10.json`
- `assets/gis-demo/months/2025-11.json`
- `assets/gis-demo/months/2025-12.json`
- `assets/gis-demo/months/2026-01.json`
- `assets/gis-demo/months/2026-02.json`
- `assets/gis-demo/months/2026-03.json`
- `assets/gis-demo/months/2026-04.json`
- `assets/gis-demo/months/2026-05.json`
- `assets/gis-demo/months/2026-06.json`
- `assets/gis-demo/months/2026-07.json`
- `assets/gis-demo/months/2026-08.json`
- `assets/gis-demo/months/2026-09.json`
- `assets/map.css`
- `assets/map.js`
- `docs/MAP-DEMO-IMPLEMENTATION.md`
- `docs/gis_demo/LICENSE.txt`
- `docs/gis_demo/README.md`
- `docs/gis_demo/asset_series.csv`
- `docs/gis_demo/assets.geojson`
- `docs/gis_demo/events.geojson`
- `docs/gis_demo/monthly_counts.csv`
- `docs/gis_demo/municipalities.geojson`
- `docs/gis_demo/question_series.csv`
- `es/map.html`
- `map.html`
- `public/assets/gis-demo/LICENSE.txt`
- `public/assets/gis-demo/boundaries.json`
- `public/assets/gis-demo/catalogue.json`
- `public/assets/gis-demo/months/2024-10.json`
- `public/assets/gis-demo/months/2024-11.json`
- `public/assets/gis-demo/months/2024-12.json`
- `public/assets/gis-demo/months/2025-01.json`
- `public/assets/gis-demo/months/2025-02.json`
- `public/assets/gis-demo/months/2025-03.json`
- `public/assets/gis-demo/months/2025-04.json`
- `public/assets/gis-demo/months/2025-05.json`
- `public/assets/gis-demo/months/2025-06.json`
- `public/assets/gis-demo/months/2025-07.json`
- `public/assets/gis-demo/months/2025-08.json`
- `public/assets/gis-demo/months/2025-09.json`
- `public/assets/gis-demo/months/2025-10.json`
- `public/assets/gis-demo/months/2025-11.json`
- `public/assets/gis-demo/months/2025-12.json`
- `public/assets/gis-demo/months/2026-01.json`
- `public/assets/gis-demo/months/2026-02.json`
- `public/assets/gis-demo/months/2026-03.json`
- `public/assets/gis-demo/months/2026-04.json`
- `public/assets/gis-demo/months/2026-05.json`
- `public/assets/gis-demo/months/2026-06.json`
- `public/assets/gis-demo/months/2026-07.json`
- `public/assets/gis-demo/months/2026-08.json`
- `public/assets/gis-demo/months/2026-09.json`
- `public/assets/map.css`
- `public/assets/map.js`
- `public/es/map.html`
- `public/map.html`
- `public/venezuela.html`
- `scripts/build.py`
- `scripts/check_map.py`
- `scripts/map_data.py`
- `scripts/map_page.py`
- `scripts/programme.py`
- `venezuela.html`
