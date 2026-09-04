/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 10: 'What-If' Disaster Simulation Sandbox UI Controller
 * 
 * Manages preset/custom scenario execution, evaluates isolated population metrics,
 * displays trapped hospital cargo tallies, and draws contingency detours on Leaflet.
 */
let selectedScenarioId = "scenario_sela_landslide";
let lastSimulationResult = null;

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
        Target: ${s.location}
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
    runBtn.innerHTML = '⚡ Computing Digital Twin Resilience Matrix...';
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
    applySimulationToMap(simResult);
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
  document.getElementById('sim-result-box').style.display = 'flex';
  document.getElementById('sim-title-heading').innerText = res.scenario_title;
  document.getElementById('sim-incident-loc').innerText = `📍 Disruption Epicenter: ${res.incident_location}`;

  // Metrics
  document.getElementById('sim-isolated-count').innerText = res.isolated_districts.length;
  document.getElementById('sim-pop-affected').innerText = res.total_population_affected.toLocaleString();
  document.getElementById('sim-delayed-trucks').innerText = res.delayed_vehicles.length;
  document.getElementById('sim-oxygen-at-risk').innerText = `${(res.critical_supplies_at_risk.liquid_oxygen_liters || 0).toLocaleString()} L`;

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

function applySimulationToMap(res) {
  // Update district nodes colors based on connectivity matrix
  if (twinData && twinData.districts) {
    twinData.districts.forEach(d => {
      if (res.connectivity_matrix[d.id]) {
        d.status = res.connectivity_matrix[d.id];
      }
    });
    renderDistricts(twinData.districts);
  }

  // Draw AI alternate routes if generated
  if (res.ai_generated_reroutes && res.ai_generated_reroutes.length > 0) {
    layers.activeRoute.clearLayers();
    res.ai_generated_reroutes.forEach((r, idx) => {
      drawRouteOnMap(r.path_coordinates, idx === 0 ? '#00f0ff' : '#ffb800', idx > 0);
    });
  }
}

function deployEmergencyReroutePlan() {
  if (!lastSimulationResult) return;
  alert(`🚨 EMERGENCY ACTION DEPLOYED: Dispatched AI alternate detour corridors to ${lastSimulationResult.delayed_vehicles.length} commercial drivers via satellite and mobile network.`);
  
  // Mark vehicles as rerouted
  if (twinData && twinData.fleet) {
    twinData.fleet.forEach(v => {
      v.status = "rerouted";
    });
    renderFleet(twinData.fleet);
  }
}
