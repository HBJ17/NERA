/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 2 & 9: OpenStreetMap Smart Resilient Routing & Navigation Controller
 * 
 * Features:
 * - Search places & geocoding across North Eastern region
 * - Dual corridor route calculation: Shortest Highway vs AI Safe Bypass
 * - Dynamic Rerouting HUD with turn-by-turn guidance and live alerts
 */
let activeRouteResponse = null;
let currentSearchDestination = null;
let userCurrentLocation = [26.1445, 91.7362]; // Default: Guwahati

function populateRouteDropdowns() {
  if (!window.twinData || !window.twinData.districts) return;

  const srcSelect = document.getElementById('route-source-select');
  const dstSelect = document.getElementById('route-dest-select');

  if (!srcSelect || !dstSelect) return;

  const optionsHtml = window.twinData.districts.map(d => `
    <option value="${d.id}">${d.name} (${d.state})</option>
  `).join('');

  srcSelect.innerHTML = optionsHtml;
  dstSelect.innerHTML = optionsHtml;

  // Defaults: Guwahati -> Tawang
  srcSelect.value = "node_guwahati";
  dstSelect.value = "node_tawang";
}

// --- Autocomplete Destination Search ---
let searchDebounce = null;
function onDestinationSearchInput(val) {
  clearTimeout(searchDebounce);
  if (!val || val.trim().length < 2) {
    const dropdown = document.getElementById('user-search-suggestions-dropdown');
    if (dropdown) dropdown.style.display = 'none';
    return;
  }

  searchDebounce = setTimeout(async () => {
    try {
      const res = await fetch(`/api/routing/search?q=${encodeURIComponent(val)}`);
      const places = await res.json();
      renderSearchSuggestions(places);
    } catch (e) {
      console.warn("Place search fallback:", e);
    }
  }, 200);
}

function showSearchDropdown() {
  const input = document.getElementById('user-destination-input');
  if (input && input.value.trim().length >= 2) {
    onDestinationSearchInput(input.value);
  }
}

function renderSearchSuggestions(places) {
  const dropdown = document.getElementById('user-search-suggestions-dropdown');
  if (!dropdown) return;

  if (!places || places.length === 0) {
    dropdown.innerHTML = `<div style="padding: 10px; font-size: 0.8rem; color: var(--text-muted);">No locations found</div>`;
    dropdown.style.display = 'block';
    return;
  }

  dropdown.innerHTML = places.map(p => `
    <div class="user-suggestion-item" onclick="selectSearchDestination('${p.name}', '${p.district_id}', [${p.coordinates[0]}, ${p.coordinates[1]}])">
      <div>
        <div style="font-weight: 600; color: #fff; font-size: 0.85rem;">📍 ${p.name}</div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">${p.state} · ${p.type || 'District Node'}</div>
      </div>
      <button class="user-nav-btn-go" style="padding: 4px 10px; font-size: 0.72rem;">Select</button>
    </div>
  `).join('');

  dropdown.style.display = 'block';
}

function selectSearchDestination(name, districtId, coords) {
  const input = document.getElementById('user-destination-input');
  if (input) input.value = name;

  const dropdown = document.getElementById('user-search-suggestions-dropdown');
  if (dropdown) dropdown.style.display = 'none';

  currentSearchDestination = { name, districtId, coords };

  // Sync with smart routing tab dropdown
  const dstSelect = document.getElementById('route-dest-select');
  if (dstSelect && districtId) {
    dstSelect.value = districtId;
  }

  // Trigger quick route preview
  onQuickNavigateClick();
}

async function onQuickNavigateClick() {
  const dstNode = currentSearchDestination ? currentSearchDestination.districtId : (document.getElementById('route-dest-select') ? document.getElementById('route-dest-select').value : 'node_tawang');
  const srcNode = document.getElementById('route-source-select') ? document.getElementById('route-source-select').value : 'node_guwahati';

  await planSmartRoute(srcNode, dstNode);
  startActiveNavigation();
}

async function planSmartRoute(optSrc, optDst) {
  const src = optSrc || document.getElementById('route-source-select').value;
  const dst = optDst || document.getElementById('route-dest-select').value;
  const avoidHazards = document.getElementById('chk-avoid-hazards') ? document.getElementById('chk-avoid-hazards').checked : true;

  if (src === dst) {
    alert("Please select different origin and destination nodes.");
    return;
  }

  const planBtn = document.getElementById('btn-calculate-route');
  if (planBtn) {
    planBtn.innerHTML = '⚡ Computing Multi-Factor Resilient Route...';
    planBtn.disabled = true;
  }

  try {
    const res = await fetch('/api/routing/optimize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        source_id: src,
        destination_id: dst,
        avoid_high_risk: avoidHazards
      })
    });

    activeRouteResponse = await res.json();
    renderRouteResults(activeRouteResponse);
  } catch (err) {
    console.error("Routing failed:", err);
    alert("Routing optimization failed: " + err.message);
  } finally {
    if (planBtn) {
      planBtn.innerHTML = '🗺️ Calculate AI Optimal Route';
      planBtn.disabled = false;
    }
  }
}

function renderRouteResults(data) {
  const container = document.getElementById('route-results-container');
  if (container) container.style.display = 'flex';

  const rec = data.recommended_route;
  const alt = data.alternative_route;

  // Draw on Leaflet map
  if (window.layers && layers.activeRoute) {
    layers.activeRoute.clearLayers();
    if (alt && alt.route_id !== rec.route_id) {
      drawRouteOnMap(alt.path_coordinates, '#ffb800', true);
    }
    drawRouteOnMap(rec.path_coordinates, '#00f0ff', false);

    // Zoom map to fit route
    if (rec.path_coordinates && rec.path_coordinates.length > 0 && window.map) {
      const bounds = L.latLngBounds(rec.path_coordinates);
      map.fitBounds(bounds, { padding: [40, 40] });
    }
  }

  // Update Metrics HTML if elements exist
  const titleEl = document.getElementById('route-rec-title');
  if (titleEl) titleEl.innerText = rec.title;

  const distEl = document.getElementById('route-rec-dist');
  if (distEl) distEl.innerText = `${rec.total_distance_km} km`;

  const timeEl = document.getElementById('route-rec-time');
  if (timeEl) timeEl.innerText = `${rec.total_travel_time_hours} Hours`;

  const riskEl = document.getElementById('route-rec-risk');
  if (riskEl) {
    riskEl.innerText = `${rec.aggregate_risk_score}/100`;
    riskEl.style.color = rec.aggregate_risk_score > 40 ? '#ffb800' : '#00ff88';
  }

  const advEl = document.getElementById('route-weather-adv');
  if (advEl) advEl.innerText = `🌦️ ${rec.weather_advisory}`;

  const redEl = document.getElementById('route-risk-reduction');
  if (redEl) redEl.innerText = `-${data.risk_reduction_pct}% Hazard Risk`;

  const deltaEl = document.getElementById('route-time-delta');
  if (deltaEl) {
    deltaEl.innerText = data.delay_delta_minutes !== 0 ? 
      `${data.delay_delta_minutes > 0 ? '+' : ''}${data.delay_delta_minutes} min vs Highway` : 'Direct Route';
  }

  // Turn-by-turn steps
  const turnList = document.getElementById('route-turn-steps');
  if (turnList) {
    turnList.innerHTML = rec.segments.map((seg, idx) => `
      <div class="turn-step ${seg.status === 'warning' ? 'has-warning' : ''}">
        <div style="font-weight: 700; color: #00f0ff; font-family: var(--font-mono);">${idx + 1}.</div>
        <div style="flex: 1;">
          <div style="font-weight: 600; color: #fff;">${seg.name}</div>
          <div style="font-size: 11px; color: #94a3b8; margin: 2px 0;">${seg.instructions}</div>
          <div style="font-size: 10px; color: var(--text-muted); display: flex; gap: 10px; font-family: var(--font-mono);">
            <span>Dist: ${seg.distance_km} km</span>
            <span>Est: ${seg.travel_time_min} min</span>
            <span style="color: ${seg.landslide_risk > 50 ? '#ff3366' : '#00ff88'}">LS Risk: ${seg.landslide_risk}%</span>
          </div>
        </div>
      </div>
    `).join('');
  }
}

function startActiveNavigation() {
  if (!activeRouteResponse) return;
  const rec = activeRouteResponse.recommended_route;
  const hud = document.getElementById('user-active-nav-hud');
  if (!hud) return;

  document.getElementById('hud-nav-dest-name').innerText = `${activeRouteResponse.source_name.split(' (')[0]} ➔ ${activeRouteResponse.destination_name.split(' (')[0]}`;
  document.getElementById('hud-nav-stats').innerText = `${rec.total_distance_km} km · ${rec.total_travel_time_hours} hrs · Risk ${rec.aggregate_risk_score}%`;

  if (rec.segments && rec.segments.length > 0) {
    document.getElementById('hud-turn-text').innerText = rec.segments[0].instructions;
  }

  const hasCaution = rec.segments.some(s => s.status === 'warning' || s.landslide_risk > 45);
  const warnBox = document.getElementById('hud-hazard-warning');
  if (warnBox) {
    warnBox.style.display = hasCaution ? 'block' : 'none';
    if (hasCaution) {
      document.getElementById('hud-hazard-text').innerText = "AI Safe Bypass Engaged: Avoiding active high-risk sectors ahead.";
    }
  }

  hud.style.display = 'block';
}

function closeNavigationHUD() {
  const hud = document.getElementById('user-active-nav-hud');
  if (hud) hud.style.display = 'none';
}
