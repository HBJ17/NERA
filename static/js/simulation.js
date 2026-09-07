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
    <div class="scenario-option ${s.id === selectedScenarioId ? 'selected' : ''}" data-scenario-id="${s.id}" onclick="selectScenario('${s.id}')">
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
  options.forEach(opt => {
    if (opt.getAttribute('data-scenario-id') === scenarioId) {
      opt.classList.add('selected');
    } else {
      opt.classList.remove('selected');
    }
  });
}
window.selectScenario = selectScenario;

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

  let epicenterCoords = [27.5020, 92.1030]; // default Sela Pass
  if (res.incident_location) {
    const locLower = res.incident_location.toLowerCase();
    if (locLower.includes('haflong') || locLower.includes('jatinga') || locLower.includes('dima hasao')) {
      epicenterCoords = [25.1764, 93.0189];
    } else if (locLower.includes('brahmaputra') || locLower.includes('tezpur') || locLower.includes('kaliabhumura') || locLower.includes('saraighat')) {
      epicenterCoords = [26.1754, 91.6800];
    } else if (locLower.includes('jiribam') || locLower.includes('imphal')) {
      epicenterCoords = [24.8000, 93.1200];
    } else if (locLower.includes('teesta') || locLower.includes('gangtok') || locLower.includes('siliguri')) {
      epicenterCoords = [27.1000, 88.5000];
    } else if (locLower.includes('sela') || locLower.includes('tawang')) {
      epicenterCoords = [27.5020, 92.1030];
    }
  }

  if (hazardGroup) {
    if (simulationHazardLayer && hazardGroup.hasLayer(simulationHazardLayer)) {
      hazardGroup.removeLayer(simulationHazardLayer);
    }

    simulationHazardLayer = L.circle(epicenterCoords, {
      radius: 22000,
      color: '#ff3366',
      fillColor: '#ff3366',
      fillOpacity: 0.4,
      weight: 3,
      dashArray: '6, 6'
    }).bindPopup(`
      <div style="font-family: Outfit, sans-serif;">
        <div style="color: #ff3366; font-weight: 800; font-size: 14px;">🚨 SIMULATED DISASTER ZONE</div>
        <div><strong>Scenario:</strong> ${res.scenario_title}</div>
        <div><strong>Epicenter:</strong> ${res.incident_location}</div>
        <div style="color: #ff85a2; margin-top: 4px;">Corridor closed. Survival countdown active.</div>
      </div>
    `);
    hazardGroup.addLayer(simulationHazardLayer);
    window.simulationHazardLayer = simulationHazardLayer;

    if (window.map) {
      map.flyTo(epicenterCoords, 9, { duration: 1.2 });
      setTimeout(() => {
        if (simulationHazardLayer) simulationHazardLayer.openPopup();
      }, 1200);
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

  // 6. TRIGGER LIVE TICKING ISOLATION RUNWAY COUNTDOWN HUD!
  const isoDist = (res.isolated_districts && res.isolated_districts[0]) || null;
  const distName = isoDist ? (isoDist.district_name || isoDist.name) : "Tawang";
  const oxDays = isoDist ? (isoDist.days_oxygen_left || 3.8) : 3.8;
  const foodDays = isoDist ? (isoDist.days_food_left || 20) : 20;
  const pop = res.total_population_affected || 95000;
  startLiveIsolationCountdown(distName, oxDays, foodDays, pop);

  // 7. Auto-scroll results into view in sidebar
  const resBox = document.getElementById('sim-result-box');
  if (resBox) {
    resBox.style.display = 'flex';
    setTimeout(() => resBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 300);
  }

  showToast(`💥 <b>DISASTER SIMULATION ENGAGED!</b><br>${res.scenario_title}. Ticking survival runway countdown active!`, 5000);
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
    showToast("🔄 <b>Digital Twin Network Restored</b><br>All simulated hazards cleared & direct highway corridors reopened.", 3500);
    
    // Hide simulation results box
    const box = document.getElementById('sim-result-box');
    if (box) box.style.display = 'none';

    // Hide diff box in routing tab
    const diffBox = document.getElementById('route-dynamic-reroute-diff');
    if (diffBox) diffBox.style.display = 'none';

    // Hide on-map floating hazard banner
    if (typeof hideMapHazardBanner === 'function') hideMapHazardBanner();

    // Remove simulated hazard circle from map
    const hazardGroup = (window.layers && window.layers.hazards) || (typeof layers !== 'undefined' && layers.hazards);
    if (hazardGroup && simulationHazardLayer) {
      try { hazardGroup.removeLayer(simulationHazardLayer); } catch (e) {}
      simulationHazardLayer = null;
      window.simulationHazardLayer = null;
    }

    const simGroup = (window.layers && window.layers.simulation) || (typeof layers !== 'undefined' && layers.simulation);
    if (simGroup) simGroup.clearLayers();

    // Hide hazard banner in HUD if open
    const warnBox = document.getElementById('hud-hazard-warning');
    if (warnBox) warnBox.style.display = 'none';

    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();

    // Re-calculate pristine route if dropdowns are set
    const srcSel = document.getElementById('route-source-select');
    const dstSel = document.getElementById('route-dest-select');
    if (srcSel && dstSel && srcSel.value && dstSel.value && srcSel.value !== dstSel.value && typeof planSmartRoute === 'function') {
      planSmartRoute(srcSel.value, dstSel.value);
    }
  } catch (e) {
    console.error("Reset failed:", e);
    showToast(`⚠️ Reset Notice: ${e.message}`, 3000);
  }
}
window.resetSimulationState = resetSimulationState;

function deployEmergencyReroutePlan() {
  if (!lastSimulationResult) return;
  
  if (lastSimulationResult.ai_generated_reroutes && lastSimulationResult.ai_generated_reroutes.length > 0) {
    const r = lastSimulationResult.ai_generated_reroutes[0];
    if (window.layers && layers.activeRoute) {
      layers.activeRoute.clearLayers();
      drawRouteOnMap(r.path_coordinates, '#00ff88', false, false, '🟢 AI Safe Reroute Corridor');
    }
    showToast(`🛡️ <b>EMERGENCY REROUTE ACTIVE!</b><br>Diverting all logistics through ${r.title}.`, 4000);
  }
}

function promptTriggerPointHazard(lat, lng, edgeId = null) {
  if (window.map) {
    window.map.closePopup();
  }
  triggerPointHazard(lat, lng, 'landslide', edgeId);
}
window.promptTriggerPointHazard = promptTriggerPointHazard;

async function triggerPointHazard(lat, lng, disasterType = 'landslide', edgeId = null) {
  showToast(`⚡ <b>Simulating Disaster Hazard...</b><br>Injecting ${disasterType} blockage at coordinates [${Number(lat).toFixed(3)}, ${Number(lng).toFixed(3)}]...`, 3000);

  try {
    const payload = {
      lat: lat,
      lng: lng,
      disaster_type: disasterType,
      severity: 'TOTAL_BREACH'
    };
    if (edgeId) {
      payload.edge_id = edgeId;
    }

    const res = await fetch('/api/simulation/trigger-point', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      throw new Error(`Simulation API failed with status ${res.status}`);
    }

    const simResult = await res.json();
    lastSimulationResult = simResult;

    // 1. Switch sidebar tab to Smart Routing so the user can immediately see the route diff & instructions
    const routeTabBtn = document.querySelector('[data-tab="routing"]');
    if (routeTabBtn && typeof switchTab === 'function') {
      switchTab('routing', routeTabBtn);
    }

    // 2. Draw pulsing red hazard zone and marker on dedicated simulation layer
    const simGroup = (window.layers && window.layers.simulation) || (typeof layers !== 'undefined' && layers.simulation);
    if (simGroup) {
      if (window.map && !window.map.hasLayer(simGroup)) {
        simGroup.addTo(window.map);
      }
      simGroup.clearLayers();

      const hazardCircle = L.circle([lat, lng], {
        radius: 18000,
        color: '#ef4444',
        fillColor: '#ef4444',
        fillOpacity: 0.4,
        weight: 3,
        dashArray: '6, 6'
      });

      const hazardIcon = L.divIcon({
        className: 'custom-hazard-marker',
        html: `<div style="background: #ef4444; color: #fff; font-weight: 800; font-size: 11px; padding: 4px 10px; border-radius: 12px; border: 2px solid #fff; box-shadow: 0 0 16px #ef4444; white-space: nowrap;">💥 BLOCKED: ${simResult.severed_highway || 'Hazard Sector'}</div>`,
        iconSize: [140, 24],
        iconAnchor: [70, 12]
      });
      const hazardMarker = L.marker([lat, lng], { icon: hazardIcon });

      hazardMarker.bindPopup(`
        <div style="font-family: Outfit, sans-serif; font-size: 13px;">
          <div style="color: #ef4444; font-weight: 800; font-size: 14px;">🚨 SIMULATED DISASTER HAZARD</div>
          <div style="font-weight: 700; color: #fff; margin: 2px 0;">${simResult.severed_highway || 'Corridor'}</div>
          <div><strong>Location:</strong> ${simResult.incident_location}</div>
          <div style="color: #fca5a5; font-size: 11px; margin-top: 4px;">Status: 🚫 Severed / Total Road Closure. Dynamic AI Safe Bypass Active.</div>
        </div>
      `);

      simGroup.addLayer(hazardCircle);
      simGroup.addLayer(hazardMarker);
      hazardMarker.openPopup();
    }

    // 3. Show top on-map floating status banner
    if (typeof showMapHazardBanner === 'function') {
      showMapHazardBanner(simResult.scenario_title, simResult.severed_highway, 35);
    }

    // 4. Render simulation details in the sidebar
    renderSimulationResults(simResult);

    // 5. Refresh digital twin state so the severed road reflects on map immediately
    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();

    // 6. Trigger Real-Time Dynamic Rerouting!
    showToast(`💥 <b>Disaster Injected!</b><br>${simResult.severed_highway} blocked. Evaluating real-time diversion...`, 3000);

    // Recalculate before resolving this operation.  Callers such as the route-level
    // simulation button must not report completion while the old corridor is still
    // displayed.
    if (typeof planSmartRoute === 'function') {
      let src = document.getElementById('route-source-select') ? document.getElementById('route-source-select').value : null;
      let dst = document.getElementById('route-dest-select') ? document.getElementById('route-dest-select').value : null;

      // If user already has an active route calculated and displayed, keep their endpoints.
      if (!(window.activeRouteResponse && window.activeRouteResponse.recommended_route && src && dst && src !== dst)) {
        // If no route has been calculated, route between the two hubs connected by the severed road.
        src = simResult.source_node || 'node_guwahati';
        dst = simResult.target_node || 'node_shillong';
        const srcSel = document.getElementById('route-source-select');
        const dstSel = document.getElementById('route-dest-select');
        if (srcSel) srcSel.value = src;
        if (dstSel) dstSel.value = dst;
      }

      await planSmartRoute(src, dst);
      if (typeof startActiveNavigation === 'function') {
        startActiveNavigation();
      }
    }

    return simResult;

  } catch (err) {
    console.error("Point hazard simulation error:", err);
    showToast(`⚠️ <b>Simulation Notice:</b> ${err.message}`, 4000);
    throw err;
  }
}
window.triggerPointHazard = triggerPointHazard;

// --- LIVE DISTRICT ISOLATION COUNTDOWN CONTROLLER ---
let countdownInterval = null;
let oxygenSecondsRemaining = 91 * 3600 + 11 * 60 + 59;
let rationSecondsRemaining = 479 * 3600 + 59 * 60 + 59;

function startLiveIsolationCountdown(districtName = "Tawang", daysOxygen = 3.8, daysFood = 20, popAffected = 95000) {
  const hud = document.getElementById('disaster-countdown-hud');
  if (!hud) return;

  const titleEl = document.getElementById('cd-epicenter-title');
  if (titleEl) {
    titleEl.innerText = `${districtName.toUpperCase()} DISTRICT · HIGH-ALTITUDE ROAD CORRIDOR SEVERED`;
  }
  const popEl = document.getElementById('cd-pop-count');
  if (popEl) popEl.innerText = Number(popAffected || 95000).toLocaleString();

  // Initialize countdown seconds
  oxygenSecondsRemaining = Math.max(3600, Math.round((daysOxygen || 3.8) * 24 * 3600));
  rationSecondsRemaining = Math.max(7200, Math.round((daysFood || 20) * 24 * 3600));

  if (countdownInterval) clearInterval(countdownInterval);
  updateCountdownClocksDisplay();

  countdownInterval = setInterval(() => {
    if (oxygenSecondsRemaining > 0) oxygenSecondsRemaining--;
    if (rationSecondsRemaining > 0) rationSecondsRemaining--;
    updateCountdownClocksDisplay();
  }, 1000);

  hud.style.display = 'flex';
}

function updateCountdownClocksDisplay() {
  const oxTimer = document.getElementById('cd-oxygen-timer');
  const ratTimer = document.getElementById('cd-ration-timer');
  const oxFill = document.getElementById('cd-oxygen-progress');
  const oxSub = document.getElementById('cd-oxygen-sub');

  if (oxTimer) {
    const h = Math.floor(oxygenSecondsRemaining / 3600);
    const m = Math.floor((oxygenSecondsRemaining % 3600) / 60);
    const s = oxygenSecondsRemaining % 60;
    oxTimer.innerText = `${h}h ${m < 10 ? '0' : ''}${m}m ${s < 10 ? '0' : ''}${s}s`;
    if (oxFill) {
      const pct = Math.min(100, Math.max(6, (oxygenSecondsRemaining / (5 * 24 * 3600)) * 100));
      oxFill.style.width = `${pct.toFixed(1)}%`;
    }
    if (oxSub) {
      const days = (oxygenSecondsRemaining / (24 * 3600)).toFixed(1);
      oxSub.innerText = `Hospital Reserves: Critical (${days} Days Remaining)`;
    }
  }

  if (ratTimer) {
    const h = Math.floor(rationSecondsRemaining / 3600);
    const m = Math.floor((rationSecondsRemaining % 3600) / 60);
    const s = rationSecondsRemaining % 60;
    ratTimer.innerText = `${h}h ${m < 10 ? '0' : ''}${m}m ${s < 10 ? '0' : ''}${s}s`;
  }
}

function closeDisasterCountdownHUD() {
  const hud = document.getElementById('disaster-countdown-hud');
  if (hud) hud.style.display = 'none';
  if (countdownInterval) clearInterval(countdownInterval);
}

function triggerAirbridgeDispatch() {
  showToast("🚁 <b>IAF & BRO Airbridge Dispatched!</b><br>Mi-17V5 heavy helicopter carrying 2,000L cryogenic oxygen dispatched from Tezpur ALG to Tawang ALG.", 5000);
  if (window.layers && layers.activeRoute) {
    const airCorridor = [
      [26.7090, 92.7960], // Tezpur ALG
      [27.1500, 92.4500],
      [27.5861, 91.8594]  // Tawang ALG
    ];
    drawRouteOnMap(airCorridor, '#00ff88', false, false);
    if (window.map) {
      const bounds = L.latLngBounds(airCorridor);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }
}

function triggerEmergencyDetourPreview() {
  const simTab = document.querySelector('[data-tab="simulation"]');
  if (simTab) simTab.click();
  const box = document.getElementById('sim-result-box');
  if (box) {
    box.style.display = 'flex';
    box.scrollIntoView({ behavior: 'smooth' });
  }
}

window.closeDisasterCountdownHUD = closeDisasterCountdownHUD;
window.startLiveIsolationCountdown = startLiveIsolationCountdown;
window.triggerAirbridgeDispatch = triggerAirbridgeDispatch;
window.triggerEmergencyDetourPreview = triggerEmergencyDetourPreview;

async function simulateRouteHazard() {
  const btn = document.getElementById('btn-simulate-route-hazard');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '⚡ Simulating Landslide & Recalculating AI Safe Corridor...';
  }

  try {
    const srcSel = document.getElementById('route-source-select');
    const dstSel = document.getElementById('route-dest-select');
    
    let src = srcSel ? srcSel.value : 'node_guwahati';
    let dst = dstSel ? dstSel.value : 'node_tawang';

    if (!src || !dst || src === dst) {
      src = 'node_guwahati';
      dst = 'node_tawang';
      if (srcSel) srcSel.value = src;
      if (dstSel) dstSel.value = dst;
    }

    // Ensure we have active route data for these endpoints
    if (!window.activeRouteResponse || !window.activeRouteResponse.recommended_route) {
      if (typeof planSmartRoute === 'function') {
        await planSmartRoute(src, dst);
      }
    }

    // Identify hazard point on the currently calculated route
    let hazardPt = null;
    let hazardEdgeId = null;
    if (window.activeRouteResponse && window.activeRouteResponse.recommended_route) {
      const rec = window.activeRouteResponse.recommended_route;
      if (rec.segments && rec.segments.length > 0) {
        // Pick an intermediate segment (preferably middle or 1st mountain pass)
        const targetIdx = rec.segments.length > 1 ? Math.floor(rec.segments.length / 2) : 0;
        const targetSeg = rec.segments[targetIdx];
        if (targetSeg.coordinates && targetSeg.coordinates.length > 0) {
          hazardPt = targetSeg.coordinates[Math.floor(targetSeg.coordinates.length / 2)];
          hazardEdgeId = targetSeg.edge_id || null;
        }
      }
      if (!hazardPt && rec.path_coordinates && rec.path_coordinates.length > 0) {
        hazardPt = rec.path_coordinates[Math.floor(rec.path_coordinates.length / 2)];
      }
    }

    // Fallback: calculate midpoint between nodes
    if (!hazardPt && window.twinData && window.twinData.districts) {
      const nSrc = window.twinData.districts.find(d => d.id === src);
      const nDst = window.twinData.districts.find(d => d.id === dst);
      if (nSrc && nDst) {
        hazardPt = [
          (nSrc.coordinates[0] + nDst.coordinates[0]) / 2,
          (nSrc.coordinates[1] + nDst.coordinates[1]) / 2
        ];
      }
    }

    if (!hazardPt) {
      hazardPt = [27.0800, 92.1800]; // Default Balemu-Kalaktang Pass
    }

    showToast(`💥 <b>Simulating Hazard on Active Route...</b><br>Injecting rockfall failure at coordinates [${hazardPt[0].toFixed(3)}, ${hazardPt[1].toFixed(3)}]...`, 3000);

    // Inject point hazard at this sector
    // Pass the selected route segment ID as well as its point.  A coordinate-only
    // lookup can choose a crossing or adjacent corridor instead of this route.
    await triggerPointHazard(hazardPt[0], hazardPt[1], 'landslide', hazardEdgeId);

    // Focus map on the hazard area
    if (window.map) {
      map.setView(hazardPt, 9, { animate: true });
    }
  } catch (err) {
    console.error("simulateRouteHazard error:", err);
    showToast(`⚠️ <b>Hazard Simulation Notice:</b> ${err.message}`, 4000);
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = '💥 Simulate Hazard on Route';
    }
  }
}
window.simulateRouteHazard = simulateRouteHazard;



