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
  const box = document.getElementById('sim-result-box');
  if (box) box.style.display = 'flex';

  const heading = document.getElementById('sim-title-heading');
  if (heading) heading.innerText = res.scenario_title;

  const loc = document.getElementById('sim-incident-loc');
  if (loc) loc.innerText = `📍 Disruption Epicenter: ${res.incident_location}`;

  // Metrics
  const isoEl = document.getElementById('sim-isolated-count');
  if (isoEl) isoEl.innerText = res.isolated_districts.length;

  const popEl = document.getElementById('sim-pop-affected');
  if (popEl) popEl.innerText = res.total_population_affected.toLocaleString();

  const delEl = document.getElementById('sim-delayed-trucks');
  if (delEl) delEl.innerText = res.delayed_vehicles.length;

  const oxEl = document.getElementById('sim-oxygen-at-risk');
  if (oxEl) oxEl.innerText = `${(res.critical_supplies_at_risk.liquid_oxygen_liters || 0).toLocaleString()} L`;

  // Isolated Districts List
  const distList = document.getElementById('sim-isolated-districts-list');
  if (distList) {
    distList.innerHTML = res.isolated_districts.map(d => `
      <div style="background: rgba(255,51,102,0.1); border: 1px solid rgba(255,51,102,0.3); border-radius: 6px; padding: 8px; margin-bottom: 6px;">
        <div style="font-weight: 700; color: #fff; font-size: 13px;">${d.district_name} (${d.state})</div>
        <div style="font-size: 11px; color: #fca5a5; display: flex; justify-content: space-between; margin-top: 2px;">
          <span>Oxygen: ${d.days_oxygen_left}d</span>
          <span>Food: ${d.days_food_left}d</span>
          <span style="color: #ff3366; font-weight: bold;">${d.isolation_tier}</span>
        </div>
      </div>
    `).join('');
  }

  // Delayed Vehicles & Cargo
  const vehList = document.getElementById('sim-delayed-trucks-list');
  if (vehList) {
    vehList.innerHTML = res.delayed_vehicles.map(v => `
      <div style="background: rgba(255,184,0,0.1); border: 1px solid rgba(255,184,0,0.3); border-radius: 6px; padding: 8px; margin-bottom: 6px;">
        <div style="font-weight: 700; color: #ffb800; font-size: 12px; display: flex; justify-content: space-between;">
          <span>${v.vehicle_number}</span>
          <span>+${v.estimated_delay_hrs}h Delay</span>
        </div>
        <div style="font-size: 11px; color: #fff;">Cargo: ${v.cargo_type}</div>
        <div style="font-size: 11px; color: #94a3b8;">Destination: ${v.destination}</div>
      </div>
    `).join('');
  }

  // Emergency Recommendations
  const recList = document.getElementById('sim-recommendations-list');
  if (recList) {
    recList.innerHTML = res.emergency_action_recommendations.map(r => `
      <li style="font-size: 12px; color: #e2e8f0; margin-bottom: 4px;">${r}</li>
    `).join('');
  }
}

function applySimulationToAllRoles(res) {
  // 1. Refresh Digital Twin State & Map Elements
  if (typeof fetchTwinState === 'function') fetchTwinState();
  if (typeof loadActiveAlerts === 'function') loadActiveAlerts();

  // 2. Add flashing red simulated hazard zone on map
  if (window.map && window.layers && layers.hazards) {
    // Draw simulation circle in epicenter
    const simCircle = L.circle([27.2000, 92.4000], {
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
    layers.hazards.addLayer(simCircle);
  }

  // 3. User / Citizen Experience: Show Danger Alert & 1-Click Safe Reroute Prompt
  showUserSimulatedHazardAlert(res);

  // 4. Draw AI alternate corridors
  if (res.ai_generated_reroutes && res.ai_generated_reroutes.length > 0 && window.layers && layers.activeRoute) {
    layers.activeRoute.clearLayers();
    res.ai_generated_reroutes.forEach((r, idx) => {
      drawRouteOnMap(r.path_coordinates, idx === 0 ? '#00ff88' : '#00f0ff', idx > 0);
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

    // Clear hazard layers & redraw pristine twin state
    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();
    if (window.layers && layers.activeRoute) layers.activeRoute.clearLayers();
  } catch (e) {
    console.error("Reset failed:", e);
  }
}

function deployEmergencyReroutePlan() {
  if (!lastSimulationResult) return;
  alert(`🚨 EMERGENCY SAFE ROUTE ENGAGED: Navigation diverted along AI-calculated green corridor.`);
  
  if (lastSimulationResult.ai_generated_reroutes && lastSimulationResult.ai_generated_reroutes.length > 0) {
    const safeRoute = lastSimulationResult.ai_generated_reroutes[0];
    if (typeof renderRouteResults === 'function') {
      renderRouteResults({
        recommended_route: safeRoute,
        alternative_route: safeRoute,
        source_name: "Origin Hub",
        destination_name: "Destination Hub",
        delay_delta_minutes: 25,
        risk_reduction_pct: 82.0
      });
    }
  }
}
