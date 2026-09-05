/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 11: Main Application Coordinator & Multi-Stakeholder Persona Manager
 * 
 * Orchestrates:
 * - 4 Stakeholder Personas: SDMA Command, Fleet Operator, Driver HUD, Essential Supplies
 * - Modular Tab Viewports: Twin, Simulation, Predictor, Routing, Supplies, Field Reports
 * - Live UTC & IST Synchronized Telemetry Clock
 */
let currentRole = 'admin'; // 'admin', 'user', 'gov_employee'
let currentDistrictId = 'node_kohima';
let currentPersona = 'sdma';

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
    initRoleState();
  }, 800);
});

function initRoleState() {
  const savedRole = localStorage.getItem('nera_role') || 'admin';
  const savedDist = localStorage.getItem('nera_district') || 'node_kohima';
  const roleBtn = document.getElementById(`role-btn-${savedRole === 'gov_employee' ? 'gov' : savedRole}`);
  if (roleBtn) {
    switchRoleAndPersona(savedRole, roleBtn, savedDist);
  }
}

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
  if (btn) btn.classList.add('active');

  // Hide all tab panes
  document.querySelectorAll('.cockpit-tab-pane').forEach(p => p.style.display = 'none');

  // Show target tab
  const targetPane = document.getElementById(`tab-${tabId}`);
  if (targetPane) {
    targetPane.style.display = 'flex';
  }

  if (tabId === 'analytics' && typeof loadAnalyticsDashboard === 'function') {
    loadAnalyticsDashboard();
  }
}

async function switchRoleAndPersona(roleKey, btn, optDistrict) {
  currentRole = roleKey;
  localStorage.setItem('nera_role', roleKey);
  
  // Update active button
  document.querySelectorAll('.persona-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  // Toggle district selector visibility
  const distContainer = document.getElementById('header-district-container');
  if (distContainer) {
    distContainer.style.display = roleKey === 'gov_employee' ? 'flex' : 'none';
  }

  const distSelect = document.getElementById('active-district-select');
  if (optDistrict && distSelect) {
    distSelect.value = optDistrict;
    currentDistrictId = optDistrict;
  }

  // Notify backend of role switch
  try {
    await fetch('/api/roles/switch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ role: roleKey, district_id: currentDistrictId })
    });
  } catch (e) {
    console.warn('Role switch network fallback:', e);
  }

  // Adapt UI to Role
  if (roleKey === 'admin') {
    const tabBtn = document.querySelector('[data-tab="twin"]');
    if (tabBtn) switchTab('twin', tabBtn);
    if (window.map) map.setView([26.2006, 92.9376], 7);
  } else if (roleKey === 'user') {
    const tabBtn = document.querySelector('[data-tab="routing"]');
    if (tabBtn) switchTab('routing', tabBtn);
  } else if (roleKey === 'gov_employee') {
    const tabBtn = document.querySelector('[data-tab="reports"]');
    if (tabBtn) switchTab('reports', tabBtn);
    if (distSelect) onDistrictChange(distSelect.value);
  }

  // Reload alerts according to role scope
  if (typeof loadActiveAlerts === 'function') {
    loadActiveAlerts();
  }
}

async function onDistrictChange(districtId) {
  currentDistrictId = districtId;
  localStorage.setItem('nera_district', districtId);

  try {
    const res = await fetch(`/api/district/dashboard/${districtId}`);
    const dash = await res.json();
    
    // Update Government Employee Command Banner & Metrics
    const titleEl = document.getElementById('gov-district-title');
    if (titleEl) titleEl.innerText = `🏛️ District Command: ${dash.district_name.split(' (')[0]}`;

    const badgeEl = document.getElementById('gov-officer-badge');
    if (badgeEl) badgeEl.innerText = `${dash.department} (${dash.trust_score}% Trust)`;

    const nameEl = document.getElementById('gov-officer-name');
    if (nameEl) nameEl.innerText = `Assigned: ${dash.assigned_officer}`;

    const mActive = document.getElementById('gov-metric-active');
    if (mActive) mActive.innerText = dash.metrics.active_incidents;

    const mPending = document.getElementById('gov-metric-pending');
    if (mPending) mPending.innerText = dash.metrics.pending_reports;

    const mCrit = document.getElementById('gov-metric-critical');
    if (mCrit) mCrit.innerText = dash.metrics.critical_hazards;

    const mBlock = document.getElementById('gov-metric-blockages');
    if (mBlock) mBlock.innerText = dash.metrics.road_blockages;

    const mFlood = document.getElementById('gov-metric-floods');
    if (mFlood) mFlood.innerText = dash.metrics.floods;

    const mLs = document.getElementById('gov-metric-landslides');
    if (mLs) mLs.innerText = dash.metrics.landslides;
  } catch (e) {
    console.warn("District dashboard fetch fallback:", e);
  }

  // Center map on chosen district
  if (window.twinData && window.twinData.districts) {
    const d = twinData.districts.find(x => x.id === districtId);
    if (d && window.map) {
      map.setView([d.coordinates[0], d.coordinates[1]], 9, { animate: true });
    }
  }

  if (typeof loadFieldReportsList === 'function') {
    loadFieldReportsList();
  }
  if (typeof loadActiveAlerts === 'function') {
    loadActiveAlerts();
  }
}

function switchPersona(personaKey, btn) {
  switchRoleAndPersona(personaKey === 'driver' ? 'user' : (personaKey === 'sdma' ? 'gov_employee' : 'admin'), btn);
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

async function loadAnalyticsDashboard() {
  try {
    const res = await fetch('/api/analytics/summary');
    const summary = await res.json();

    const log = summary.logistics;
    const dis = summary.disasters;
    const rep = summary.reports;

    const timeEl = document.getElementById('kpi-time-saved');
    if (timeEl) timeEl.innerText = `-${log.transit_time_savings_pct}%`;

    const fuelEl = document.getElementById('kpi-fuel-saved');
    if (fuelEl) fuelEl.innerText = `+${log.fuel_savings_estimate_pct}%`;

    const onTimeEl = document.getElementById('kpi-on-time');
    if (onTimeEl) onTimeEl.innerText = `${log.on_time_delivery_rate_pct}%`;

    const tonEl = document.getElementById('kpi-tonnage');
    if (tonEl) tonEl.innerText = `${log.total_cargo_weight_tons || 142} Tons`;

    // Render high risk district rankings
    const rankingsEl = document.getElementById('analytics-district-rankings');
    if (rankingsEl && dis.high_risk_district_rankings) {
      rankingsEl.innerHTML = dis.high_risk_district_rankings.map((r, idx) => `
        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); padding: 8px 10px; border-radius: 6px; margin-bottom: 5px;">
          <div style="font-size: 12px; font-weight: 600; color: #fff;">
            ${idx + 1}. ${r.district}
            <div style="font-size: 10px; color: var(--text-muted);">${r.primary_hazard}</div>
          </div>
          <span class="badge" style="background: rgba(255,51,102,0.2); color: #ff3366; font-size: 11px; font-weight: 700;">
            ${r.risk_index}% Risk
          </span>
        </div>
      `).join('');
    }
  } catch (e) {
    console.warn("Analytics fetch fallback:", e);
  }
}

