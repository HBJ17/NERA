/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 10, 11 & 12: 'What-If' Disaster Simulation & Cross-Role Propagation Controller
 * 
 * Features:
 * - Real-time disaster propagation to all 3 roles (Admin, User / Citizen, Government Employee)
 * - Map visualization with flashing severed corridors & dynamic risk polygons
 * - User safe rerouting prompt with 1-click [Start Safe Route]
 * - Instant Reset & Simulation Recovery
 */
let selectedScenarioId = "scenario_sela_landslide";
let lastSimulationResult = null;
let simulationHazardLayer = null;

async function loadSimulationScenarios() {
  try {
    const res = await fetch('/api/simulation/scenarios');
    const data = await res.json();
    renderScenarioOptions(data.scenarios);
  } catch (err) {
    console.error("Failed to load scenarios:", err);
  }
}

function renderScenarioOptions(scenarios) {
  const container = document.getElementById('scenarios-container');
  if (!container) return;

  container.innerHTML = scenarios.map((s, idx) => `
    <div class="scenario-option ${s.id === selectedScenarioId ? 'selected' : ''}" onclick="selectScenario('${s.id}')">
      <div class="scenario-title">🔥 ${s.title}</div>
      <div class="scenario-desc">${s.description}</div>
      <div style="font-size: 11px; color: #00f0ff; margin-top: 4px; font-family: var(--font-mono);">
        Target Sector: ${s.location}
      </div>
    </div>
  `).join('');
}

function selectScenario(scenarioId) {
  selectedScenarioId = scenarioId;
  const options = document.querySelectorAll('.scenario-option');
  options.forEach(opt => opt.classList.remove('selected'));
  const clicked = Array.from(options).find(opt => opt.innerHTML.includes(scenarioId));
  if (clicked) clicked.classList.add('selected');
}

async function triggerWhatIfSimulation() {
  const runBtn = document.getElementById('btn-run-simulation');
  if (runBtn) {
    runBtn.innerHTML = '⚡ Propagating Digital Twin Simulation to All 3 Stakeholder Maps...';
    runBtn.disabled = true;
  }

  try {
    const res = await fetch('/api/simulation/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        scenario_id: selectedScenarioId,
        disaster_severity: 'HIGH',
        weather_multiplier: 1.8
      })
    });

    const simResult = await res.json();
    lastSimulationResult = simResult;
    renderSimulationResults(simResult);
    applySimulationToAllRoles(simResult);
  } catch (err) {
    console.error("Simulation failed:", err);
    alert("Simulation calculation failed: " + err.message);
  } finally {
    if (runBtn) {
      runBtn.innerHTML = '💥 Execute What-If Stress Simulation';
      runBtn.disabled = false;
    }
  }
}

function renderSimulationResults(res) {
  if (!res) return;
  const box = document.getElementById('sim-result-box');
  if (box) box.style.display = 'flex';

  const heading = document.getElementById('sim-title-heading');
  if (heading) heading.innerText = res.scenario_title || 'Disaster Simulation Active';

  const loc = document.getElementById('sim-incident-loc');
  if (loc) loc.innerText = `📍 Disruption Epicenter: ${res.incident_location || 'Corridor'}`;

  const isolated = Array.isArray(res.isolated_districts) ? res.isolated_districts : [];
  const totalPop = typeof res.total_population_affected === 'number' ? res.total_population_affected : 0;
  const delayed = Array.isArray(res.delayed_vehicles) ? res.delayed_vehicles : (Array.isArray(res.affected_vehicles) ? res.affected_vehicles : []);
  const supplies = res.critical_supplies_at_risk || { liquid_oxygen_liters: 0 };
  const recs = Array.isArray(res.emergency_action_recommendations) ? res.emergency_action_recommendations : [];

  // Metrics
  const isoEl = document.getElementById('sim-isolated-count');
  if (isoEl) isoEl.innerText = isolated.length;

  const popEl = document.getElementById('sim-pop-affected');
  if (popEl) popEl.innerText = totalPop.toLocaleString();

  const delEl = document.getElementById('sim-delayed-trucks');
  if (delEl) delEl.innerText = delayed.length;

  const oxEl = document.getElementById('sim-oxygen-at-risk');
  if (oxEl) oxEl.innerText = `${(supplies.liquid_oxygen_liters || 0).toLocaleString()} L`;

  // Isolated Districts List
  const distList = document.getElementById('sim-isolated-districts-list');
  if (distList) {
    distList.innerHTML = isolated.map(d => `
      <div style="background: rgba(255,51,102,0.1); border: 1px solid rgba(255,51,102,0.3); border-radius: 6px; padding: 8px; margin-bottom: 6px;">
        <div style="font-weight: 700; color: #fff; font-size: 13px;">${d.district_name || d.name} (${d.state || 'NER'})</div>
        <div style="font-size: 11px; color: #fca5a5; display: flex; justify-content: space-between; margin-top: 2px;">
          <span>Oxygen: ${d.days_oxygen_left || 0}d</span>
          <span>Food: ${d.days_food_left || 0}d</span>
          <span style="color: #ff3366; font-weight: bold;">${d.isolation_tier || 'ISOLATED'}</span>
        </div>
      </div>
    `).join('');
  }

  // Delayed Vehicles & Cargo
  const vehList = document.getElementById('sim-delayed-trucks-list');
  if (vehList) {
    vehList.innerHTML = delayed.map(v => `
      <div style="background: rgba(255,184,0,0.1); border: 1px solid rgba(255,184,0,0.3); border-radius: 6px; padding: 8px; margin-bottom: 6px;">
        <div style="font-weight: 700; color: #ffb800; font-size: 12px; display: flex; justify-content: space-between;">
          <span>${v.vehicle_number || v.vehicle_id}</span>
          <span>+${v.estimated_delay_hrs || 2}h Delay</span>
        </div>
        <div style="font-size: 11px; color: #fff;">Cargo: ${v.cargo_type || 'Relief Cargo'}</div>
        <div style="font-size: 11px; color: #94a3b8;">Destination: ${v.destination || 'District Hub'}</div>
      </div>
    `).join('');
  }

  // Emergency Recommendations
  const recList = document.getElementById('sim-recommendations-list');
  if (recList) {
    recList.innerHTML = recs.map(r => `
      <li style="font-size: 12px; color: #e2e8f0; margin-bottom: 4px;">${r}</li>
    `).join('');
  }
}

function applySimulationToAllRoles(res) {
  // 1. Refresh Digital Twin State & Map Elements
  if (typeof fetchTwinState === 'function') fetchTwinState();
  if (typeof loadActiveAlerts === 'function') loadActiveAlerts();

  // 2. Add flashing red simulated hazard zone on map
  const hazardGroup = (window.layers && window.layers.hazards) || (typeof layers !== 'undefined' && layers.hazards);
  const activeRouteGroup = (window.layers && window.layers.activeRoute) || (typeof layers !== 'undefined' && layers.activeRoute);

  let epicenterCoords = [27.5020, 92.1030]; // default Sela
  if (res.incident_location) {
    const locLower = res.incident_location.toLowerCase();
    if (locLower.includes('haflong') || locLower.includes('jatinga') || locLower.includes('dima hasao')) {
      epicenterCoords = [25.1764, 93.0189];
    } else if (locLower.includes('brahmaputra') || locLower.includes('tezpur') || locLower.includes('kaliabhumura')) {
      epicenterCoords = [26.6000, 92.8500];
    } else if (locLower.includes('jiribam') || locLower.includes('imphal')) {
      epicenterCoords = [24.8000, 93.1200];
    } else if (locLower.includes('teesta') || locLower.includes('gangtok') || locLower.includes('siliguri')) {
      epicenterCoords = [27.1000, 88.5000];
    }
  }

  if (hazardGroup) {
    if (simulationHazardLayer && hazardGroup.hasLayer(simulationHazardLayer)) {
      hazardGroup.removeLayer(simulationHazardLayer);
    }

    simulationHazardLayer = L.circle(epicenterCoords, {
      radius: 25000,
      color: '#ff3366',
      fillColor: '#ff3366',
      fillOpacity: 0.35,
      weight: 3,
      dashArray: '6, 6'
    }).bindPopup(`
      <div style="font-family: Outfit, sans-serif;">
        <div style="color: #ff3366; font-weight: 700; font-size: 14px;">🚨 SIMULATED DISASTER ZONE</div>
        <div>${res.scenario_title}</div>
        <div><strong>Epicenter:</strong> ${res.incident_location}</div>
        <div style="color: #ff85a2; margin-top: 4px;">Corridor closed. Detour corridors active.</div>
      </div>
    `);
    hazardGroup.addLayer(simulationHazardLayer);
    window.simulationHazardLayer = simulationHazardLayer;

    if (window.map) {
      window.map.setView(epicenterCoords, 8, { animate: true });
    }
  }

  // 3. User / Citizen Experience: Show Danger Alert & 1-Click Safe Reroute Prompt
  showUserSimulatedHazardAlert(res);

  // 4. Draw AI alternate corridors
  if (res.ai_generated_reroutes && res.ai_generated_reroutes.length > 0 && activeRouteGroup) {
    activeRouteGroup.clearLayers();
    res.ai_generated_reroutes.forEach((r, idx) => {
      drawRouteOnMap(r.path_coordinates, idx === 0 ? '#00ff88' : '#00f0ff', idx > 0, false);
    });
  }

  // 5. Govt Employee experience: Update District Dashboard metrics
  if (typeof onDistrictChange === 'function' && window.currentDistrictId) {
    onDistrictChange(window.currentDistrictId);
  }
}

function showUserSimulatedHazardAlert(res) {
  const hud = document.getElementById('user-active-nav-hud');
  if (hud) {
    hud.style.display = 'block';
    const warnBox = document.getElementById('hud-hazard-warning');
    if (warnBox) {
      warnBox.style.display = 'block';
      warnBox.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <span>🚨 <strong>Route Severed:</strong> ${res.incident_location}</span>
          <button class="btn-primary" style="padding: 2px 8px; font-size: 10px; background: #00ff88; color: #000;" onclick="deployEmergencyReroutePlan()">
            ✓ Start Safe Route
          </button>
        </div>
      `;
    }
  }
}

async function resetSimulationState() {
  try {
    const res = await fetch('/api/simulation/reset', { method: 'POST' });
    const data = await res.json();
    alert("🔄 Digital Twin simulation state reset. Highway network restored to baseline.");
    
    // Hide simulation results box
    const box = document.getElementById('sim-result-box');
    if (box) box.style.display = 'none';

    // Remove simulated hazard circle from map
    const hazardGroup = (window.layers && window.layers.hazards) || (typeof layers !== 'undefined' && layers.hazards);
    if (hazardGroup && simulationHazardLayer) {
      try { hazardGroup.removeLayer(simulationHazardLayer); } catch (e) {}
      simulationHazardLayer = null;
      window.simulationHazardLayer = null;
    }

    // Hide hazard banner in HUD if open
    const warnBox = document.getElementById('hud-hazard-warning');
    if (warnBox) warnBox.style.display = 'none';

    // Clear active routes and redraw pristine twin state
    const activeRouteGroup = (window.layers && window.layers.activeRoute) || (typeof layers !== 'undefined' && layers.activeRoute);
    if (activeRouteGroup) activeRouteGroup.clearLayers();

    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();
  } catch (e) {
    console.error("Reset failed:", e);
  }
}

function deployEmergencyReroutePlan() {
  if (!lastSimulationResult) return;
  
  if (lastSimulationResult.ai_generated_reroutes && lastSimulationResult.ai_generated_reroutes.length > 0) {
    const safeRoute = lastSimulationResult.ai_generated_reroutes[0];
    
    // Switch to routing tab
    const routeTabBtn = document.querySelector('[data-tab="routing"]');
    if (routeTabBtn && typeof switchTab === 'function') {
      switchTab('routing', routeTabBtn);
    }

    if (typeof renderRouteResults === 'function') {
      renderRouteResults({
        recommended_route: safeRoute,
        alternative_route: safeRoute,
        source_name: "Strategic Origin Hub",
        destination_name: "Target Relief Destination",
        delay_delta_minutes: 25,
        risk_reduction_pct: 82.0
      });
    }

    if (typeof startActiveNavigation === 'function') {
      startActiveNavigation();
    }
  }

  alert(`🚨 EMERGENCY SAFE ROUTE ENGAGED:\n\nNavigation diverted along AI-calculated green corridor bypass. Severed mountain sector avoided.`);
}

function promptTriggerPointHazard(lat, lng) {
  if (window.map) {
    window.map.closePopup();
  }
  // Directly trigger point hazard without relying on native confirm dialogs that can be blocked
  triggerPointHazard(lat, lng, 'landslide');
}
window.promptTriggerPointHazard = promptTriggerPointHazard;

async function triggerPointHazard(lat, lng, disasterType = 'landslide') {
  showToast(`⚡ <b>Simulating Hazard...</b><br>Injecting disaster blockage at (${lat}, ${lng})...`, 2500);

  try {
    const res = await fetch('/api/simulation/trigger-point', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        lat: lat,
        lng: lng,
        disaster_type: disasterType,
        severity: 'TOTAL_BREACH'
      })
    });

    if (!res.ok) {
      throw new Error(`Simulation API failed with status ${res.status}`);
    }

    const simResult = await res.json();
    lastSimulationResult = simResult;

    // 1. Draw pulsing red hazard zone and marker on dedicated simulation layer
    const simGroup = (window.layers && window.layers.simulation) || (typeof layers !== 'undefined' && layers.simulation);
    if (simGroup) {
      if (window.map && !window.map.hasLayer(simGroup)) {
        simGroup.addTo(window.map);
      }
      simGroup.clearLayers();

      const hazardCircle = L.circle([lat, lng], {
        radius: 16000,
        color: '#ff3366',
        fillColor: '#ff3366',
        fillOpacity: 0.45,
        weight: 3,
        dashArray: '6, 6'
      });

      const hazardIcon = L.divIcon({
        className: 'custom-hazard-marker',
        html: `<div style="background: #ff3366; color: #fff; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 12px; border: 2px solid #fff; box-shadow: 0 0 16px #ff3366; white-space: nowrap; animation: pulse 1s infinite;">💥 BLOCKED: ${simResult.severed_highway || 'Hazard Sector'}</div>`,
        iconSize: [140, 24],
        iconAnchor: [70, 12]
      });
      const hazardMarker = L.marker([lat, lng], { icon: hazardIcon });

      hazardMarker.bindPopup(`
        <div style="font-family: Outfit, sans-serif; font-size: 13px;">
          <div style="color: #ff3366; font-weight: 800; font-size: 14px;">🚨 SIMULATED DISASTER HAZARD</div>
          <div style="font-weight: 700; color: #fff; margin: 2px 0;">${simResult.severed_highway || 'Corridor'}</div>
          <div><strong>Location:</strong> ${simResult.incident_location}</div>
          <div style="color: #fca5a5; font-size: 11px; margin-top: 4px;">Status: Severed / Total Road Closure. Dynamic AI Safe Bypass Active.</div>
        </div>
      `);

      simGroup.addLayer(hazardCircle);
      simGroup.addLayer(hazardMarker);
      hazardMarker.openPopup();
    }

    // 2. Render simulation details in the sidebar
    renderSimulationResults(simResult);

    // 3. Refresh digital twin state so the severed road reflects on map immediately
    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();

    // 4. Trigger Real-Time Dynamic Rerouting!
    showToast(`💥 <b>Disaster Injected!</b><br>${simResult.severed_highway} blocked. Evaluating real-time diversion...`, 3000);

    setTimeout(() => {
      if (typeof planSmartRoute === 'function') {
        showToast(`🔄 <b>REAL-TIME DYNAMIC REROUTE TRIGGERED!</b><br>AI safely calculating alternate corridor around blockage...`, 4000);

        let src = document.getElementById('route-source-select') ? document.getElementById('route-source-select').value : null;
        let dst = document.getElementById('route-dest-select') ? document.getElementById('route-dest-select').value : null;

        // If user already has an active route calculated and displayed, keep their endpoints
        if (window.activeRouteResponse && window.activeRouteResponse.recommended_route && src && dst && src !== dst) {
          // Keep user's active route origin and destination
        } else {
          // If no route calculated yet, route between the two hubs connected by the severed road
          src = simResult.source_node || 'node_guwahati';
          dst = simResult.target_node || 'node_shillong';
          const srcSel = document.getElementById('route-source-select');
          const dstSel = document.getElementById('route-dest-select');
          if (srcSel) srcSel.value = src;
          if (dstSel) dstSel.value = dst;
        }

        planSmartRoute(src, dst).then(() => {
          if (typeof startActiveNavigation === 'function') {
            startActiveNavigation();
          }
        });
      }
    }, 400);

  } catch (err) {
    console.error("Point hazard simulation error:", err);
    showToast(`⚠️ <b>Simulation Notice:</b> ${err.message}`, 4000);
  }
}
window.triggerPointHazard = triggerPointHazard;

async function simulateRouteHazard() {
  const btn = document.getElementById('btn-simulate-route-hazard');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '⚡ Simulating Landslide & Calculating AI Safe Detour...';
  }

  try {
    // If no active route exists or route has less than 2 points, first plan Guwahati -> Shillong corridor
    if (!window.activeRouteResponse || !window.activeRouteResponse.recommended_route || !window.activeRouteResponse.recommended_route.path_coordinates || window.activeRouteResponse.recommended_route.path_coordinates.length < 2) {
      showToast(`⚡ <b>Planning Baseline Arterial Corridor...</b><br>Computing Guwahati ➔ Shillong highway...`, 2500);
      if (typeof planSmartRoute === 'function') {
        await planSmartRoute('node_guwahati', 'node_shillong');
      }
    }

    // Determine hazard injection coordinate along active corridor
    let pt = [25.8200, 91.8600]; // Nongpoh mountain highway pass default
    if (window.activeRouteResponse && window.activeRouteResponse.recommended_route && window.activeRouteResponse.recommended_route.path_coordinates && window.activeRouteResponse.recommended_route.path_coordinates.length > 2) {
      const coords = window.activeRouteResponse.recommended_route.path_coordinates;
      pt = coords[Math.floor(coords.length * 0.45)] || pt;
    }

    showToast(`⚡ <b>Disaster Blockage Injected!</b><br>Landslide at [${pt[0].toFixed(3)}, ${pt[1].toFixed(3)}]. AI computing live dynamic diversion...`, 3500);
    await triggerPointHazard(pt[0], pt[1], 'landslide');
  } catch (err) {
    console.error("simulateRouteHazard error:", err);
    showToast(`⚠️ <b>Hazard Simulation Notice:</b> ${err.message}`, 4000);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '⚠️ SIMULATE REAL-TIME HAZARD & AUTO-DETOUR';
    }
  }
}
window.simulateRouteHazard = simulateRouteHazard;



