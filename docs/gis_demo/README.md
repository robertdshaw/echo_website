# PRISMA Oriente GIS demo

This local demo for Jean-Christophe Loubier contains 457 permitted event records
from the 653-event store, selected by recorded state and first_seen from
2024-09-11 through 2026-09-12 inclusive. States are Monagas and Anzoátegui.
The event store ends on 2026-09-10. Later zero counts indicate missing collection,
not evidence of stability. No inference, typing or source collection was run.

## Files and joins

| File | Contents |
|---|---|
| events.geojson | 457 events, one feature per event_id, with source counts and recorded assessments. |
| municipalities.geojson | 34 OpenStreetMap municipality polygons, 13 in Monagas and 21 in Anzoátegui. boundary_id is the OSM relation join key. Internal legacy identifiers are excluded. |
| assets.geojson | 11 configured Oriente target assets in 14 site features. Petropiar, Petromonagas and Petrocedeño each have an upgrader and producing-area point. Join on asset_id. |
| monthly_counts.csv | 6800 municipality/month/event-family rows, including zeros. total, status_* and severity_* are separate marginal counts. |
| asset_series.csv | 1155 asset/week rows, including zeros. total, type_* and status_* are marginals. type_*__status columns contain joint counts. |
| LICENSE.txt | Full Open Database Licence 1.0 for the OSM-derived geography. |
| question_series.csv | 261 stored forecast rows across 20 HC2Y questions and 28 profiles, with frozen wording, asset_id and question family. |

All files use UTF-8. GeoJSON uses WGS84 longitude, latitude in decimal degrees.
CSV blank values mean null. GeoJSON null means unknown or withheld, never zero.
Events use the taxonomy families CON, ELM, EXT, MAC, OIL, POL, SAN and SEC.
Questions use the distinct families F1 through F6. These are not interchangeable.
source_count counts contributing items, not independent outlets. source_blocks
is the sorted list of contributing registered block categories, with no source identities.
physical_verdict is the stored physical assessment and can be null.
freshness is the stored assessment, not recomputed at export time.

## Precision and counting

Facility records retain their independently sourced stored points. Municipality records
use land-only display centroids from the licensed OSM polygons. State records use
the union of those polygons. Country records and unmatched municipal locations are excluded.
The common polygons use topology-preserving simplification at 0.0001 degrees.
Centroids use a spherical Lambert cylindrical equal-area projection, with longitude
in radians and sine of latitude, then inverse projection to WGS84. Municipal land
is clipped to the full-resolution OSM coastline and excludes mapped water polygons
from the Geofabrik Venezuela extract dated 2026-09-11. Where the land centroid
falls outside land, an interior land point is used and labelled land_interior_point.
municipalities.geojson retains full_centroid_lat/lon and land_centroid_lat/lon
separately from display_centroid_lat/lon and display_centroid_method. Full administrative
polygons, including their water sectors, are preserved. None of the 335 mapped
municipality display points intersects the water mask or lies outside the land mask.
This verification concerns mapped water coverage and is not a survey of unmapped water.
No state centroid is drawn as a point. A municipality point is a place-resolution
centroid, not an exact incident location. Restricted and source-protecting evidence
forces the entire event to state geometry with null boundary_id and facility_id before
aggregation. Unknown field sensitivity withholds the event. Histories depending
on protected or disallowed evidence have null probabilities and timestamps rather
than exposing an asset-specific signal. This run coarsened 0 events
and withheld 0 question profiles.

The state filter uses stored labels. Municipalities are resolved by state and reviewed name aliases, never nearest coordinates.
2 exported points lie outside their recorded state's OSM municipality-union polygon,
including coastal José coordinates and inconsistent place matches. They are marked
point_in_state_polygon=false. 0 points have no unambiguous municipality-name
match within their recorded state and retain null boundary_id. No spatial guess repairs
these records. Monthly counts use the recorded state and municipality label matched
to an OSM relation, not a point-in-polygon reassignment. This location quality requires review
before using the package as a validated spatial event inventory.

Each event is counted once in its first_seen month or Monday-starting week.
The first and last periods are partial. Monthly totals allocate 303 events;
state-only and unmatched municipality records are not allocated to municipalities.
Asset totals allocate 61 events by exact stored facility_id, with no proximity
inference and no duplication for assets with several sites. Configured radius_km is
provided for the simulator but does not change membership or the signal.
Type columns cover types observed in this permitted regional export.
Carabobo and Junín block coordinates remain unresolved, with null geometry and
coordinate_source. Their configured radius is retained. Zero rows for an unresolved
asset do not establish the absence of events. Question scopes state_anzoategui, state_monagas and
pdvsa_oriente refer to state or organisational targets, not additional facility pins.

Exclusions from the full event inventory are {"outside_state_date_or_superseded": 159, "unmapped_municipality": 37}.
Corroboration counts are {"corroborated": 31, "single_source": 426}.
Severity counts are {"unknown": 457}.

## Corroboration

single_source means the evidence does not meet the independence rule, even when
several items exist. corroborated requires two media outlets with both known and
different owners and home cities, or media plus a qualifying non-media source.
contradicted requires an assertion and a denial by a normally trusted source.
unassessed means no stored verdict. Freshness is separate and becomes stale after
the configured type-specific window, normally 30 days, 7 for a stoppage and 90 for
a contract change. Physical consistency is separate and never establishes media
independence. These fields preserve the stored assessments and their limitations.

## Severity

Severity measures the explicitly supported extent of an event, not confidence,
sentiment or client favourability. The taxonomy's low, medium and high definitions
are specific to family and type. For oil operations, low affects equipment or a
shipment without established core interruption, medium interrupts one facility for
less than 48 hours or changes capacity without complete closure, and high stops
operations for at least 48 hours or affects multiple facilities. Type overrides take
precedence; reversals measure the extent restored. A denied claim's severity is
not confirmation that it occurred. Unknown extent stays null. This historical store
predates severity typing, so no severity has been inferred for this export.

## Hindcast interpretation

Every question row is labelled hindcast, provisional and indicative. These are
retrospective assumptions using later priors and v0-f4.2 rules, not forecasts made
at those historical dates, calibrated client probabilities or a track record.
The CSV preserves stored snapshots, including zero-movement updates. It does not
interpolate daily points or extend a trajectory after its question horizon.
Profiles share a question identity and are not independent observations.
All twenty histories are preserved, including admitted evidence outside the regional
geometry subset. The GIS filters do not replay or truncate their causal histories.
No outcomes or Brier scores are exported. The live board and MCP continue to
exclude all hindcasts. This explicitly requested offline demo changes no access rule.

## Legal basis and source protection

Event records only are exported, with no article text, item identifiers, actor names
or reporter identities. Frozen question wording and public gazetteer metadata are
included as requested. Every contributing parent must exist and pass
backend/legal_gate.py against the current config/source_register.yaml. Unknown,
null-basis, reserved_removed and ai_agent_optout_removed sources cannot contribute
to an exported event or derived probability. The register's documented collection
basis is not an article republication licence. The protection checks run before
geometry, counts, serialization or output writes. All databases were opened read-only.

Boundary attribution is © OpenStreetMap contributors, https://www.openstreetmap.org/copyright.
The boundary database and derived centroids are licensed under the Open Database
Licence 1.0, reproduced in LICENSE.txt. Commercial use and redistribution are
permitted under its attribution, notice and share-alike conditions. Changes comprise
selection, reviewed name matching, topology-preserving simplification, land clipping and centroid
calculation. The regional geometry is an extract of the same national boundary
snapshot used by the public map. This licence applies to the OSM-derived geography;
it does not grant rights to underlying reporting. Asset coordinate attribution is
retained per site. The event and question tables are separate parts of this collection.

## Three open limits

1. No independent second source in the east. The regional reporting network lacks
   the verified second independent local source needed to overcome this coverage gap.
   Some stored events satisfy corroboration through other eligible sources; those
   verdicts do not establish a complete independent regional reporting network.
2. Facility yield is capped by place resolution. Municipality or state reporting
   does not establish activity at a specific facility. Stored mismatches are flagged.
3. VIIRS is available from 2026-09-07 only. Earlier absence of physical evidence
   cannot establish normal operations or contradict a historical event.

## Reproduce

From the repository root with the local stores and committed licensed boundary file present, run
`./venv/Scripts/python -m backend.prisma_gis_demo --until 2026-09-12 --zip`.
The archive contains these eight files at its root and excludes itself.
No push, notification, deployment or external delivery is performed.
