/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 2 & 9: Smart Resilient Routing UI Controller
 * 
 * Manages origin/destination selection, dispatches route optimization requests,
 * renders dual-corridor comparison cards, and draws interactive route polylines on Leaflet.
 */
let activeRouteResponse = null;

function populateRouteDropdowns() {
  if (!twinData || !twinData.districts) return;

  const srcSelect = document.getElementById('route-source-select');
  const dstSelect = document.getElementById('route-dest-select');

  if (!srcSelect || !dstSelect) return;

  const optionsHtml = twinData.districts.map(d => `
    <option value="${d.id}">${d.name} (${d.state})</option>
  `).join('');

  srcSelect.innerHTML = optionsHtml;
  dstSelect.innerHTML = optionsHtml;

  // Defaults: Guwahati -> Tawang
  srcSelect.value = "node_guwahati";
  dstSelect.value = "node_tawang";
}

async function planSmartRoute() {
  const src = document.getElementById('route-source-select').value;
  const dst = document.getElementById('route-dest-select').value;
  const avoidHazards = document.getElementById('chk-avoid-hazards').checked;

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
  if (!container) return;

  container.style.display = 'flex';

  const rec = data.recommended_route;
  const alt = data.alternative_route;

  // Draw on Leaflet map
  layers.activeRoute.clearLayers();
  if (alt && alt.route_id !== rec.route_id) {
    drawRouteOnMap(alt.path_coordinates, '#ffb800', true);
  }
  drawRouteOnMap(rec.path_coordinates, '#00f0ff', false);

  // Metrics HTML
  document.getElementById('route-rec-title').innerText = rec.title;
  document.getElementById('route-rec-dist').innerText = `${rec.total_distance_km} km`;
  document.getElementById('route-rec-time').innerText = `${rec.total_travel_time_hours} Hours`;
  document.getElementById('route-rec-risk').innerText = `${rec.aggregate_risk_score}/100`;
  document.getElementById('route-rec-risk').style.color = rec.aggregate_risk_score > 40 ? '#ffb800' : '#00ff88';

  document.getElementById('route-weather-adv').innerText = `🌦️ ${rec.weather_advisory}`;

  // Delta stats
  document.getElementById('route-risk-reduction').innerText = `-${data.risk_reduction_pct}% Hazard Risk`;
  document.getElementById('route-time-delta').innerText = data.delay_delta_minutes !== 0 ? 
    `${data.delay_delta_minutes > 0 ? '+' : ''}${data.delay_delta_minutes} min vs Highway` : 'Direct Route';

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
