/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 11: Main Application Coordinator & Multi-Stakeholder Persona Manager
 * 
 * Orchestrates:
 * - 4 Stakeholder Personas: SDMA Command, Fleet Operator, Driver HUD, Essential Supplies
 * - Modular Tab Viewports: Twin, Simulation, Predictor, Routing, Supplies, Field Reports
 * - Live UTC & IST Synchronized Telemetry Clock
 */
let currentPersona = 'sdma'; // 'sdma', 'fleet', 'driver', 'supplies'

document.addEventListener('DOMContentLoaded', () => {
  initDigitalTwinMap();
  initPredictionControls();
  loadSimulationScenarios();
  loadActiveAlerts();
  loadFieldReportsList();
  updateOfflineBadge();
  startClock();

  // Populate dropdowns once map data is loaded
  setTimeout(() => {
    populateRouteDropdowns();
    renderDistrictGrid();
    renderSuppliesRunway();
  }, 800);
});

function startClock() {
  function updateTime() {
    const now = new Date();
    const utcStr = now.toUTCString().split(' ')[4] + ' UTC';
    const istStr = now.toLocaleTimeString('en-US', { timeZone: 'Asia/Kolkata', hour12: false }) + ' IST';
    
    const clockEl = document.getElementById('live-time-display');
    if (clockEl) {
      clockEl.innerText = `${istStr} | ${utcStr}`;
    }
  }
  updateTime();
  setInterval(updateTime, 1000);
}

function switchTab(tabId, btn) {
  // Update button active state
  document.querySelectorAll('.cockpit-tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  // Hide all tab panes
  document.querySelectorAll('.cockpit-tab-pane').forEach(p => p.style.display = 'none');

  // Show target tab
  const targetPane = document.getElementById(`tab-${tabId}`);
  if (targetPane) {
    targetPane.style.display = 'flex';
  }
}

function switchPersona(personaKey, btn) {
  currentPersona = personaKey;
  document.querySelectorAll('.persona-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  // Auto switch to relevant tab for that persona
  if (personaKey === 'sdma') {
    const tabBtn = document.querySelector('[data-tab="twin"]');
    if (tabBtn) switchTab('twin', tabBtn);
  } else if (personaKey === 'fleet') {
    const tabBtn = document.querySelector('[data-tab="twin"]');
    if (tabBtn) switchTab('twin', tabBtn);
  } else if (personaKey === 'driver') {
    const tabBtn = document.querySelector('[data-tab="routing"]');
    if (tabBtn) switchTab('routing', tabBtn);
  } else if (personaKey === 'supplies') {
    const tabBtn = document.querySelector('[data-tab="supplies"]');
    if (tabBtn) switchTab('supplies', tabBtn);
  }
}

function renderDistrictGrid() {
  const container = document.getElementById('district-matrix-grid');
  if (!container || !twinData || !twinData.districts) return;

  container.innerHTML = twinData.districts.map(d => `
    <div class="district-item status-${d.status}" onclick="focusOnDistrict([${d.coordinates[0]}, ${d.coordinates[1]}])">
      <div class="district-item-name">📍 ${d.name.split(' (')[0]}</div>
      <div class="district-item-meta">
        <span>${d.state}</span>
        <span style="font-weight: bold; text-transform: uppercase;">${d.status}</span>
      </div>
      <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">
        O2: ${d.stock_oxygen_days}d | Food: ${d.stock_rations_days}d
      </div>
    </div>
  `).join('');
}

function updateFleetOperatorView(fleet) {
  const container = document.getElementById('fleet-telemetry-list');
  if (!container) return;

  container.innerHTML = fleet.map(v => {
    let cargoClass = 'badge-rations';
    if (v.cargo_type.toLowerCase().includes('oxygen')) cargoClass = 'badge-oxygen';
    if (v.cargo_type.toLowerCase().includes('vaccine') || v.cargo_type.toLowerCase().includes('insulin')) cargoClass = 'badge-vaccine';

    return `
      <div class="fleet-card" onclick="focusOnVehicle([${v.current_coordinates[0]}, ${v.current_coordinates[1]}])">
        <div class="fleet-card-header">
          <span class="vehicle-plate">🚚 ${v.vehicle_number}</span>
          <span class="vehicle-cargo-badge ${cargoClass}">${v.cargo_priority}</span>
        </div>
        <div style="font-size: 12px; color: #fff; font-weight: 600;">${v.cargo_type}</div>
        <div class="fleet-route-desc">${v.source.split(' (')[0]} ➔ ${v.destination.split(' (')[0]}</div>
        <div class="fleet-telemetry-row">
          <span>Speed: ${v.speed_kmh} km/h</span>
          <span>ETA: ${v.eta_timestamp}</span>
          <span style="color: ${v.status === 'delayed' ? '#ffb800' : '#00ff88'}; font-weight: bold;">${v.status.toUpperCase()}</span>
        </div>
      </div>
    `;
  }).join('');
}

function focusOnDistrict(coords) {
  if (map) {
    map.setView(coords, 10, { animate: true });
  }
}

function focusOnVehicle(coords) {
  if (map) {
    map.setView(coords, 11, { animate: true });
  }
}
