/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 2 & 9: OpenStreetMap Smart Resilient Routing & Navigation Controller
 * 
 * Features:
 * - Search places & OpenStreetMap Nominatim geocoding across North Eastern region
 * - Free Real Road Driving Navigation via OpenStreetMap OSRM API (Zero API key needed)
 * - Dual corridor calculation: Shortest Highway vs AI Safe-Corridor Bypass
 * - Dynamic Rerouting HUD with turn-by-turn guidance, maneuver icons, and live hazard alerts
 */
let activeRouteResponse = null;
let currentSearchDestination = null;
let userCurrentLocation = [26.1445, 91.7362]; // Default: Guwahati
let routingMode = 'hybrid'; // 'hybrid' (OSRM + AI Resilient) or 'graph_only'

function populateRouteDropdowns() {
  if (!window.twinData || !window.twinData.districts) return;

  const srcSelect = document.getElementById('route-source-select');
  const dstSelect = document.getElementById('route-dest-select');

  if (!srcSelect || !dstSelect) return;

  // Group districts by State
  const stateMap = {};
  window.twinData.districts.forEach(d => {
    const st = d.state || 'Gateway Corridor';
    if (!stateMap[st]) stateMap[st] = [];
    stateMap[st].push(d);
  });

  // Sort states alphabetically, prioritizing Assam and West Bengal (Gateway)
  const sortedStates = Object.keys(stateMap).sort((a, b) => {
    if (a.includes('Assam')) return -1;
    if (b.includes('Assam')) return 1;
    if (a.includes('West Bengal')) return -1;
    if (b.includes('West Bengal')) return 1;
    return a.localeCompare(b);
  });

  let optionsHtml = '';
  sortedStates.forEach(st => {
    optionsHtml += `<optgroup label="📍 ${st} (${stateMap[st].length} Hubs)">`;
    stateMap[st].sort((a, b) => a.name.localeCompare(b.name)).forEach(d => {
      optionsHtml += `<option value="${d.id}">${d.name} (${d.tier || 'Hub'})</option>`;
    });
    optionsHtml += `</optgroup>`;
  });

  // Preserve selections
  const srcVal = srcSelect.value;
  const dstVal = dstSelect.value;

  srcSelect.innerHTML = optionsHtml;
  dstSelect.innerHTML = optionsHtml;

  // Defaults: Guwahati -> Tawang
  srcSelect.value = srcVal || "node_guwahati";
  dstSelect.value = dstVal || "node_tawang";
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
    <div class="user-suggestion-item" onclick="selectSearchDestination('${p.name.replace(/'/g, "\\'")}', '${p.district_id || ''}', [${p.coordinates[0]}, ${p.coordinates[1]}])">
      <div>
        <div style="font-weight: 600; color: #fff; font-size: 0.85rem;">📍 ${p.name}</div>
        <div style="font-size: 0.72rem; color: var(--text-muted);">${p.state || 'NER Location'} · ${p.type || 'District Hub'}</div>
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
  window.customDestCoords = coords;

  // Sync with smart routing tab dropdown
  const dstSelect = document.getElementById('route-dest-select');
  if (dstSelect) {
    if (districtId && Array.from(dstSelect.options).some(o => o.value === districtId)) {
      dstSelect.value = districtId;
    } else {
      let opt = Array.from(dstSelect.options).find(o => o.value === 'custom_coords');
      if (!opt) {
        opt = document.createElement('option');
        opt.value = 'custom_coords';
        dstSelect.prepend(opt);
      }
      opt.text = `🎯 ${name}`;
      dstSelect.value = 'custom_coords';
    }
  }

  // Trigger quick route preview
  onQuickNavigateClick();
}

async function onQuickNavigateClick() {
  let dstNode = 'node_tawang';
  if (currentSearchDestination) {
    if (currentSearchDestination.districtId) {
      dstNode = currentSearchDestination.districtId;
    } else if (currentSearchDestination.coords) {
      dstNode = 'custom_coords';
    }
  } else {
    const dstSelect = document.getElementById('route-dest-select');
    if (dstSelect) dstNode = dstSelect.value;
  }

  const srcNode = document.getElementById('route-source-select') ? document.getElementById('route-source-select').value : 'node_guwahati';

  await planSmartRoute(srcNode, dstNode);
  startActiveNavigation();
}

async function planSmartRoute(optSrc, optDst) {
  const srcSelect = document.getElementById('route-source-select');
  const dstSelect = document.getElementById('route-dest-select');

  let src = optSrc || (srcSelect ? srcSelect.value : 'node_guwahati');
  let dst = optDst || (dstSelect ? dstSelect.value : 'node_tawang');
  const avoidHazards = document.getElementById('chk-avoid-hazards') ? document.getElementById('chk-avoid-hazards').checked : true;

  if (src === 'custom_coords' && window.customSourceCoords) {
    if (window.twinData && window.twinData.districts) {
      const [cLat, cLng] = window.customSourceCoords;
      let closest = window.twinData.districts[0];
      let minD = Infinity;
      window.twinData.districts.forEach(d => {
        const dist = Math.hypot(d.coordinates[0] - cLat, d.coordinates[1] - cLng);
        if (dist < minD) {
          minD = dist;
          closest = d;
        }
      });
      src = closest.id;
    } else {
      src = 'node_guwahati';
    }
  }

  if (dst === 'custom_coords' && window.customDestCoords) {
    // Map to closest district node
    if (window.twinData && window.twinData.districts) {
      const [cLat, cLng] = window.customDestCoords;
      let closest = window.twinData.districts[0];
      let minD = Infinity;
      window.twinData.districts.forEach(d => {
        const dist = Math.hypot(d.coordinates[0] - cLat, d.coordinates[1] - cLng);
        if (dist < minD) {
          minD = dist;
          closest = d;
        }
      });
      dst = closest.id;
    }
  }

  // Update UI dropdowns to match selected route
  if (srcSelect && Array.from(srcSelect.options).some(o => o.value === src)) {
    srcSelect.value = src;
  }
  if (dstSelect && Array.from(dstSelect.options).some(o => o.value === dst)) {
    dstSelect.value = dst;
  }

  if (src === dst) {
    alert("Please select different origin and destination nodes.");
    return;
  }

  const planBtn = document.getElementById('btn-calculate-route');
  if (planBtn) {
    planBtn.innerHTML = '⚡ Computing Real Road & AI Resilient Corridor...';
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
    window.activeRouteResponse = activeRouteResponse;
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

  const hasBypass = alt && alt.path_coordinates && (alt.route_id !== rec.route_id || (alt.segments && alt.segments.some(s => s.status === 'blocked')));
  const isBlockedBypass = hasBypass && (alt.segments && alt.segments.some(s => s.status === 'blocked' || s.landslide_risk > 70));

  // Draw on Leaflet map
  if (window.layers && layers.activeRoute) {
    layers.activeRoute.clearLayers();
    if (hasBypass) {
      // Draw the blocked / original severed route in crimson red with dashed lines
      drawRouteOnMap(alt.path_coordinates, isBlockedBypass ? '#ef4444' : '#ffb800', true, false, isBlockedBypass ? '🔴 Original Impassable Highway (Blocked)' : '🟡 Alternative Secondary Route', isBlockedBypass);
    }
    // Draw the recommended AI safe route in vibrant neon emerald / cyan
    drawRouteOnMap(rec.path_coordinates, hasBypass ? '#00ff88' : '#00f0ff', false, false, '🟢 AI Recommended Safe Corridor');

    // Zoom map to fit route
    if (rec.path_coordinates && rec.path_coordinates.length > 0 && window.map) {
      const bounds = L.latLngBounds(rec.path_coordinates);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }

  // Render Dynamic Reroute Diff Box if bypass is active
  const diffBox = document.getElementById('route-dynamic-reroute-diff');
  if (diffBox) {
    if (hasBypass) {
      const distDelta = Math.max(0, Math.round(rec.total_distance_km - (alt.total_distance_km || rec.total_distance_km)));
      const timeDeltaMins = data.delay_delta_minutes || 0;
      
      diffBox.innerHTML = `
        <div class="reroute-diff-card">
          <div class="diff-status-bar">
            <span class="diff-badge-danger">🔴 SEVERED DIRECT CORRIDOR</span>
            <span style="font-weight: 800; color: #fff; font-size: 1rem;">➔</span>
            <span class="diff-badge-success">🟢 AI RESILIENT BYPASS ACTIVE</span>
          </div>
          
          <div class="diff-columns-grid">
            <div class="diff-pane diff-pane-severed">
              <div class="diff-pane-title" style="color: #fca5a5;">
                <span>🚫</span> Direct Highway
              </div>
              <div class="diff-metric-row">
                <span>Distance:</span>
                <strong>${alt.total_distance_km} km</strong>
              </div>
              <div class="diff-metric-row">
                <span>Speed / Status:</span>
                <strong style="color: #ef4444;">0 km/h (BLOCKED)</strong>
              </div>
              <div class="diff-metric-row">
                <span>Hazard Risk:</span>
                <strong style="color: #ef4444;">${alt.aggregate_risk_score}/100 ⚠️</strong>
              </div>
            </div>

            <div class="diff-pane diff-pane-safe">
              <div class="diff-pane-title" style="color: #86efac;">
                <span>🛡️</span> AI Safe Corridor
              </div>
              <div class="diff-metric-row">
                <span>Distance:</span>
                <strong>${rec.total_distance_km} km (+${distDelta} km)</strong>
              </div>
              <div class="diff-metric-row">
                <span>Transit Time:</span>
                <strong>${rec.total_travel_time_hours} hrs (+${timeDeltaMins} min)</strong>
              </div>
              <div class="diff-metric-row">
                <span>Hazard Risk:</span>
                <strong style="color: #00ff88;">${rec.aggregate_risk_score}/100 🟢</strong>
              </div>
            </div>
          </div>

          <div class="diff-cargo-alert">
            🚚 <strong>Critical Supplies Safeguarded:</strong> Rerouted convoy carrying Liquid Medical Oxygen (-183°C) & Vaccines away from hill failure zone.
          </div>
        </div>
      `;
      diffBox.style.display = 'block';
    } else {
      diffBox.style.display = 'none';
    }
  }

  // Update Metrics HTML if elements exist
  const titleEl = document.getElementById('route-rec-title');
  if (titleEl) {
    titleEl.innerHTML = hasBypass ? `🛡️ <strong>AI Dynamic Resilient Safe Bypass</strong>` : `🗺️ <strong>AI Optimal Safe Corridor</strong>`;
    titleEl.style.color = hasBypass ? '#00ff88' : 'var(--accent-cyan)';
  }

  const distEl = document.getElementById('route-rec-dist');
  if (distEl) distEl.innerText = `${rec.total_distance_km} km`;

  const timeEl = document.getElementById('route-rec-time');
  if (timeEl) timeEl.innerText = `${rec.total_travel_time_hours} Hours`;

  const riskEl = document.getElementById('route-rec-risk');
  if (riskEl) {
    riskEl.innerText = `${rec.aggregate_risk_score}/100`;
    riskEl.style.color = rec.aggregate_risk_score > 40 ? '#ef4444' : '#00ff88';
  }

  const advEl = document.getElementById('route-weather-adv');
  if (advEl) advEl.innerText = `🌦️ ${rec.weather_advisory}`;

  const redEl = document.getElementById('route-risk-reduction');
  if (redEl) {
    if (data.red_zones_avoided > 0) {
      redEl.innerText = `🛡️ ${data.red_zones_avoided} Red Zones Bypassed`;
      redEl.style.color = '#00ff88';
    } else if (rec.red_zone_count === 0) {
      redEl.innerText = `🟢 0 Red Hazard Zones`;
      redEl.style.color = '#00ff88';
    } else {
      redEl.innerText = `-${data.risk_reduction_pct}% Hazard Risk`;
    }
  }

  const deltaEl = document.getElementById('route-time-delta');
  if (deltaEl) {
    let deltaText = data.delay_delta_minutes !== 0 ? 
      `⏱️ ${data.delay_delta_minutes > 0 ? '+' : ''}${data.delay_delta_minutes} min detour vs direct line` : '🟢 Direct Clear Corridor';
    if (rec.red_zone_count === 0) {
      deltaText += ' · 🟢 100% Passable (Zero Hazards)';
    }
    deltaEl.innerText = deltaText;
  }

  // Populate AI Scientific Risk Breakdown Card
  const aiData = rec.ai_risk_breakdown || data.ai_risk_breakdown;
  const aiCard = document.getElementById('route-ai-risk-card');
  if (aiCard && aiData) {
    aiCard.style.display = 'block';
    
    const badge = document.getElementById('route-ai-tier-badge');
    if (badge) {
      const isZeroRed = rec.red_zone_count === 0;
      badge.innerText = isZeroRed ? `🟢 ZERO RED ZONES (${rec.aggregate_risk_score}%)` : `${aiData.risk_level || 'EVALUATED'} (${rec.aggregate_risk_score}%)`;
      let bg = isZeroRed ? 'rgba(0,255,136,0.25)' : 'rgba(0,255,136,0.2)';
      let col = '#00ff88';
      if (rec.aggregate_risk_score > 60) {
        bg = 'rgba(255,51,102,0.25)';
        col = '#ff3366';
      } else if (rec.aggregate_risk_score > 35) {
        bg = 'rgba(255,184,0,0.25)';
        col = '#ffb800';
      }
      badge.style.background = bg;
      badge.style.color = col;
    }

    const formulaEl = document.getElementById('route-ai-formula-text');
    if (formulaEl && aiData.model_formula) {
      formulaEl.innerText = aiData.model_formula;
    }

    const barsEl = document.getElementById('route-ai-factor-bars');
    if (barsEl && aiData.factors) {
      barsEl.innerHTML = aiData.factors.map(f => {
        let barColor = '#00f0ff';
        if (f.contribution_pct > 35) barColor = '#ff3366';
        else if (f.contribution_pct > 25) barColor = '#ffb800';
        return `
          <div>
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; margin-bottom: 2px;">
              <span style="color: #cbd5e1; font-weight: 600;">${f.name}</span>
              <span style="color: ${barColor}; font-family: var(--font-mono); font-weight: 700;">${f.contribution_pct}%</span>
            </div>
            <div style="background: rgba(255,255,255,0.08); height: 5px; border-radius: 99px; overflow: hidden;">
              <div style="background: ${barColor}; width: ${Math.min(100, f.contribution_pct * 1.8)}%; height: 100%; border-radius: 99px;"></div>
            </div>
            <div style="font-size: 0.68rem; color: #64748b; margin-top: 1px;">${f.description}</div>
          </div>
        `;
      }).join('');
    }

    const statsEl = document.getElementById('route-ai-env-stats');
    if (statsEl && aiData.environmental_telemetry) {
      const env = aiData.environmental_telemetry;
      statsEl.innerHTML = `
        <div>🌧️ Avg Rain: <strong style="color: #fff;">${env.avg_rainfall_mm} mm</strong></div>
        <div>📐 Max Slope: <strong style="color: #fff;">${env.max_slope_deg || env.max_slope_degrees || 12}°</strong></div>
        <div>💧 Soil Sat: <strong style="color: #fff;">${env.soil_moisture_pct}%</strong></div>
        <div>🌋 Fault Line: <strong style="color: #ff3366;">Zone V (Himalayan)</strong></div>
      `;
    }

    const protoEl = document.getElementById('route-ai-protocol-text');
    if (protoEl && aiData.action_protocol) {
      protoEl.innerHTML = `🛡️ <strong>Safety Directive:</strong> ${aiData.action_protocol}`;
    }
  }

  // Turn-by-turn steps with visual icons
  const turnList = document.getElementById('route-turn-steps');
  if (turnList) {
    turnList.innerHTML = rec.segments.map((seg, idx) => {
      let icon = '⬆️';
      if (seg.instructions.toLowerCase().includes('right')) icon = '↗️';
      if (seg.instructions.toLowerCase().includes('left')) icon = '↖️';
      if (seg.status === 'warning') icon = '⚠️';
      if (seg.status === 'blocked') icon = '🚫';

      const isHighRisk = seg.landslide_risk > 50 || seg.flood_risk > 50 || seg.status !== 'open';

      return `
        <div class="turn-step ${isHighRisk ? 'has-warning' : ''}">
          <div style="font-size: 1.1rem; margin-right: 4px;">${icon}</div>
          <div style="font-weight: 700; color: #00f0ff; font-family: var(--font-mono);">${idx + 1}.</div>
          <div style="flex: 1;">
            <div style="font-weight: 600; color: #fff;">${seg.name}</div>
            <div style="font-size: 11px; color: #94a3b8; margin: 2px 0;">${seg.instructions}</div>
            <div style="font-size: 10px; color: var(--text-muted); display: flex; gap: 10px; font-family: var(--font-mono);">
              <span>Dist: ${seg.distance_km} km</span>
              <span>Est: ${seg.travel_time_min} min</span>
              <span style="color: ${isHighRisk ? '#ff3366' : '#00ff88'}; font-weight: 600;">
                ${isHighRisk ? '⚠️ Red Hazard: ' : '🟢 Safe: '}${seg.landslide_risk}%
              </span>
            </div>
          </div>
        </div>
      `;
    }).join('');
  }
}

function startActiveNavigation() {
  if (!activeRouteResponse) return;
  const rec = activeRouteResponse.recommended_route;
  const hud = document.getElementById('user-active-nav-hud');
  if (!hud) return;

  const srcLabel = activeRouteResponse.source_name.split(' (')[0];
  const dstLabel = activeRouteResponse.destination_name.split(' (')[0];

  document.getElementById('hud-nav-dest-name').innerText = `${srcLabel} ➔ ${dstLabel}`;
  document.getElementById('hud-nav-stats').innerText = `${rec.total_distance_km} km · ${rec.total_travel_time_hours} hrs · Risk ${rec.aggregate_risk_score}%`;

  if (rec.segments && rec.segments.length > 0) {
    document.getElementById('hud-turn-text').innerText = rec.segments[0].instructions;
  }

  const hasCaution = rec.segments.some(s => s.status === 'warning' || s.landslide_risk > 45 || s.status === 'blocked');
  const warnBox = document.getElementById('hud-hazard-warning');
  if (warnBox) {
    warnBox.style.display = hasCaution ? 'block' : 'none';
    if (hasCaution) {
      document.getElementById('hud-hazard-text').innerText = "AI Safe Bypass Active: Diverting away from active hill slide sectors.";
    }
  }

  const hudStats = document.querySelector('.map-hud-stats');
  if (hudStats) hudStats.style.display = 'none';

  hud.style.display = 'block';
}

function closeNavigationHUD() {
  const hud = document.getElementById('user-active-nav-hud');
  if (hud) hud.style.display = 'none';
  const hudStats = document.querySelector('.map-hud-stats');
  if (hudStats) hudStats.style.display = 'flex';
}


