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

// Expose on global window object for cross-module coordination
window.currentRole = currentRole;
window.currentDistrictId = currentDistrictId;

document.addEventListener('DOMContentLoaded', () => {
  registerServiceWorker();
  updateNetworkStatus();
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
    populateGovDistrictDropdown();
    renderDistrictGrid();
    renderSuppliesRunway();
    initRoleState();
  }, 800);
});

// Register PWA Service Worker for offline GIS support
function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/sw.js')
        .then(reg => console.log('[NERA PWA] Service Worker registered with scope:', reg.scope))
        .catch(err => console.warn('[NERA PWA] Service Worker registration failed:', err));
    });
  }

  // Network online/offline listener
  window.addEventListener('online', updateNetworkStatus);
  window.addEventListener('offline', updateNetworkStatus);
}

function updateNetworkStatus() {
  const isOnline = navigator.onLine;
  const dot = document.getElementById('network-status-dot');
  const text = document.getElementById('network-status-text');
  const indicator = document.getElementById('network-status-indicator');

  if (isOnline) {
    if (dot) dot.style.background = 'var(--accent-green, #00ff88)';
    if (text) text.innerText = 'SATELLITE LINK ACTIVE';
    if (indicator) indicator.title = 'Online Satellite Connection Active';
    if (typeof syncOfflineReports === 'function') {
      syncOfflineReports();
    }
  } else {
    if (dot) dot.style.background = 'var(--accent-amber, #ffb800)';
    if (text) text.innerText = 'OFFLINE MOUNTAIN CACHE';
    if (indicator) indicator.title = 'Offline Mountain Mode: Cached GIS data and queued reports active';
  }
}

function populateGovDistrictDropdown() {
  const distSelect = document.getElementById('active-district-select');
  if (!distSelect || !window.twinData || !window.twinData.districts) return;

  const currentVal = distSelect.value;
  const states = {};
  window.twinData.districts.forEach(d => {
    if (!states[d.state]) states[d.state] = [];
    states[d.state].push(d);
  });

  let html = '';
  Object.keys(states).sort().forEach(stateName => {
    html += `<optgroup label="${stateName}">`;
    states[stateName].forEach(d => {
      html += `<option value="${d.id}">${d.name.split(' (')[0]} (${d.state})</option>`;
    });
    html += `</optgroup>`;
  });

  distSelect.innerHTML = html;
  if (currentVal && Array.from(distSelect.options).some(o => o.value === currentVal)) {
    distSelect.value = currentVal;
  }
}

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
  if (btn) {
    btn.classList.add('active');
  } else {
    const matchingBtn = document.querySelector(`[data-tab="${tabId}"]`);
    if (matchingBtn) matchingBtn.classList.add('active');
  }

  // Hide all tab panes
  document.querySelectorAll('.cockpit-tab-pane').forEach(p => p.style.display = 'none');

  // Show target tab
  const targetPane = document.getElementById(`tab-${tabId}`);
  if (targetPane) {
    targetPane.style.display = 'flex';
  }

  // Refresh Leaflet map dimensions if layout shifted
  if (window.map) {
    setTimeout(() => {
      try { window.map.invalidateSize(); } catch (e) {}
    }, 60);
  }

  // Tab specific refreshes
  if (tabId === 'analytics' && typeof loadAnalyticsDashboard === 'function') {
    loadAnalyticsDashboard();
  } else if (tabId === 'prediction') {
    if (typeof factorChart !== 'undefined' && factorChart) {
      try { factorChart.resize(); } catch (e) {}
    }
    if (typeof predictLandslideRisk === 'function') predictLandslideRisk();
    if (typeof predictFloodRisk === 'function') predictFloodRisk();
  } else if (tabId === 'supplies' && typeof renderSuppliesRunway === 'function') {
    renderSuppliesRunway();
  } else if (tabId === 'reports' && typeof loadFieldReportsList === 'function') {
    loadFieldReportsList();
  } else if (tabId === 'twin' && typeof renderDistrictGrid === 'function') {
    renderDistrictGrid();
  }
}

function applyRolePermissions(roleKey) {
  const tabTwin = document.querySelector('[data-tab="twin"]');
  const tabSimulation = document.querySelector('[data-tab="simulation"]');
  const tabPrediction = document.querySelector('[data-tab="prediction"]');
  const tabRouting = document.querySelector('[data-tab="routing"]');
  const tabSupplies = document.querySelector('[data-tab="supplies"]');
  const tabReports = document.querySelector('[data-tab="reports"]');
  const tabAnalytics = document.querySelector('[data-tab="analytics"]');
  const simHeaderBtn = document.getElementById('btn-header-simulation');
  const sihShowcaseBtn = document.getElementById('btn-header-sih-showcase');
  const officerBanner = document.getElementById('district-officer-banner');
  const userReportCard = document.getElementById('user-report-action-card');
  const reportsFilterBar = document.getElementById('reports-filter-bar');
  const reportsSectionTitle = document.getElementById('reports-section-title');
  const reportsSectionBadge = document.getElementById('reports-section-badge');

  // SIH Showcase button is always visible across all roles for hackathon evaluation
  if (sihShowcaseBtn) sihShowcaseBtn.style.display = 'inline-flex';

  if (roleKey === 'admin') {
    // Admin: ALL existing features enabled
    if (tabTwin) { tabTwin.style.display = 'inline-flex'; tabTwin.innerHTML = '🌐 Digital Twin'; }
    if (tabSimulation) tabSimulation.style.display = 'inline-flex';
    if (tabPrediction) tabPrediction.style.display = 'inline-flex';
    if (tabRouting) { tabRouting.style.display = 'inline-flex'; tabRouting.innerHTML = '🗺️ Smart Routing'; }
    if (tabSupplies) tabSupplies.style.display = 'inline-flex';
    if (tabReports) { tabReports.style.display = 'inline-flex'; tabReports.innerHTML = '📱 Field Feeds'; }
    if (tabAnalytics) tabAnalytics.style.display = 'inline-flex';
    if (simHeaderBtn) simHeaderBtn.style.display = 'inline-flex';

    if (officerBanner) officerBanner.style.display = 'block';
    if (userReportCard) userReportCard.style.display = 'none';
    if (reportsFilterBar) reportsFilterBar.style.display = 'flex';
    if (reportsSectionTitle) reportsSectionTitle.innerText = '📋 Field Reports & Verification Queue';
    if (reportsSectionBadge) reportsSectionBadge.innerText = 'LIVE VERIFICATION';

  } else if (roleKey === 'user') {
    // Citizen / User: ONLY Smart Routing and Field Reporting
    if (tabTwin) tabTwin.style.display = 'none';
    if (tabSimulation) tabSimulation.style.display = 'none';
    if (tabPrediction) tabPrediction.style.display = 'none';
    if (tabRouting) { tabRouting.style.display = 'inline-flex'; tabRouting.innerHTML = '🗺️ Smart Routing'; }
    if (tabSupplies) tabSupplies.style.display = 'none';
    if (tabReports) { tabReports.style.display = 'inline-flex'; tabReports.innerHTML = '📷 Field Reporting'; }
    if (tabAnalytics) tabAnalytics.style.display = 'none';
    if (simHeaderBtn) simHeaderBtn.style.display = 'none';

    // Hide internal government officer banner, show citizen reporting card
    if (officerBanner) officerBanner.style.display = 'none';
    if (userReportCard) userReportCard.style.display = 'block';
    if (reportsFilterBar) reportsFilterBar.style.display = 'none';
    if (reportsSectionTitle) reportsSectionTitle.innerText = '📢 Community Hazard Feed';
    if (reportsSectionBadge) reportsSectionBadge.innerText = 'CITIZEN FEED';

  } else if (roleKey === 'gov_employee') {
    // Government Employee: ONLY Field Reports Checking, Approval, and Smart Routing
    if (tabTwin) tabTwin.style.display = 'none';
    if (tabSimulation) tabSimulation.style.display = 'none';
    if (tabPrediction) tabPrediction.style.display = 'none';
    if (tabRouting) { tabRouting.style.display = 'inline-flex'; tabRouting.innerHTML = '🗺️ Smart Routing'; }
    if (tabSupplies) tabSupplies.style.display = 'none';
    if (tabReports) { tabReports.style.display = 'inline-flex'; tabReports.innerHTML = '📋 Field Approvals'; }
    if (tabAnalytics) tabAnalytics.style.display = 'none';
    if (simHeaderBtn) simHeaderBtn.style.display = 'none';

    // Show officer command banner, hide user card, show approval filter bar
    if (officerBanner) officerBanner.style.display = 'block';
    if (userReportCard) userReportCard.style.display = 'none';
    if (reportsFilterBar) reportsFilterBar.style.display = 'flex';
    if (reportsSectionTitle) reportsSectionTitle.innerText = '📋 Field Reports & Approvals';
    if (reportsSectionBadge) reportsSectionBadge.innerText = 'OFFICER QUEUE';
  }
}

async function switchRoleAndPersona(roleKey, btn, optDistrict) {
  currentRole = roleKey;
  window.currentRole = roleKey;
  localStorage.setItem('nera_role', roleKey);
  
  // Update active button
  document.querySelectorAll('.persona-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  // Apply strict role permissions to tabs & features
  applyRolePermissions(roleKey);

  // Toggle district selector visibility
  const distContainer = document.getElementById('header-district-container');
  if (distContainer) {
    distContainer.style.display = roleKey === 'gov_employee' ? 'flex' : 'none';
  }

  const distSelect = document.getElementById('active-district-select');
  if (optDistrict && distSelect) {
    distSelect.value = optDistrict;
    currentDistrictId = optDistrict;
    window.currentDistrictId = optDistrict;
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

  // Adapt UI to Role: Activate role's primary tab
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
  if (typeof loadFieldReportsList === 'function') {
    loadFieldReportsList();
  }
}

async function onDistrictChange(districtId) {
  currentDistrictId = districtId;
  window.currentDistrictId = districtId;
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
    const isCar = v.category === 'car';
    const icon = isCar ? '🚗' : '🚚';
    const borderCol = isCar ? 'rgba(0,210,255,0.4)' : 'rgba(255,51,102,0.4)';
    const tagBg = isCar ? 'rgba(0,210,255,0.2)' : 'rgba(255,51,102,0.2)';
    const tagCol = isCar ? '#00d2ff' : '#ff3366';
    const catLabel = isCar ? 'CIVILIAN CAR' : (v.cargo_priority || 'LOGISTICS');

    return `
      <div class="fleet-card" style="border-left: 3px solid ${tagCol}; background: rgba(15,23,42,0.6);" onclick="focusOnVehicle([${v.current_coordinates[0]}, ${v.current_coordinates[1]}])">
        <div class="fleet-card-header">
          <span class="vehicle-plate" style="color: ${tagCol}; font-weight: 700;">${icon} ${v.vehicle_number}</span>
          <span class="vehicle-cargo-badge" style="background: ${tagBg}; color: ${tagCol}; border: 1px solid ${borderCol}; font-size: 10px;">${catLabel}</span>
        </div>
        <div style="font-size: 12px; color: #fff; font-weight: 600; margin-top: 2px;">📦 ${v.cargo_type}</div>
        <div style="font-size: 11px; color: #94a3b8;">👤 Driver: <strong style="color: #cbd5e1;">${v.driver_name}</strong></div>
        <div class="fleet-route-desc">🎯 ${v.source.split(' (')[0]} ➔ ${v.destination.split(' (')[0]}</div>
        <div class="fleet-telemetry-row">
          <span>Speed: ${v.speed_kmh} km/h</span>
          <span>ETA: ${v.eta_timestamp}</span>
          <span style="color: ${v.status === 'delayed' ? '#ffb800' : '#00ff88'}; font-weight: bold;">${v.status.toUpperCase()}</span>
        </div>
        <div style="margin-top: 6px;">
          <button class="user-nav-btn-go" style="width: 100%; padding: 4px 8px; font-size: 11px;" onclick="event.stopPropagation(); trackVehicleRoute('${v.id}', '${v.source.replace(/'/g, "\\'")}', '${v.destination.replace(/'/g, "\\'")}')">
            🗺️ Track Route Live
          </button>
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

    // Render high risk district rankings (DVI)
    const rankingsEl = document.getElementById('analytics-district-rankings');
    if (rankingsEl) {
      try {
        const dviRes = await fetch('/api/analytics/dvi-matrix');
        const dviData = await dviRes.json();
        const topDvi = (dviData.matrix || []).slice(0, 5);
        if (topDvi.length > 0) {
          rankingsEl.innerHTML = topDvi.map((r, idx) => `
            <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(0,0,0,0.3); padding: 8px 10px; border-radius: 6px; margin-bottom: 5px; border-left: 3px solid ${r.color};">
              <div style="font-size: 12px; font-weight: 600; color: #fff;">
                ${idx + 1}. ${r.district_name.split(' (')[0]} (${r.state})
                <div style="font-size: 10px; color: var(--text-muted);">${r.primary_vulnerability} · O₂ Runway: <strong style="color: ${r.oxygen_days_left < 5 ? '#ff3366' : '#00ff88'}">${r.oxygen_days_left}d</strong></div>
              </div>
              <span class="badge" style="background: rgba(${r.color === '#ff3366' ? '255,51,102' : '255,184,0'},0.2); color: ${r.color}; font-size: 11px; font-weight: 700;">
                DVI ${r.dvi_score}
              </span>
            </div>
          `).join('');
        }
      } catch (dviErr) {
        console.warn("DVI load fallback:", dviErr);
      }
    }

    // Render SPOF Bottlenecks List
    const spofEl = document.getElementById('analytics-spof-list');
    if (spofEl) {
      try {
        const spofRes = await fetch('/api/analytics/spof-bottlenecks');
        const spofData = await spofRes.json();
        if (spofData.bottlenecks) {
          spofEl.innerHTML = spofData.bottlenecks.map(b => `
            <div style="background: rgba(0,0,0,0.35); border: 1px solid rgba(239,68,68,0.25); border-radius: 6px; padding: 10px;">
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px;">
                <div style="font-weight: 700; color: #fff; font-size: 0.82rem;">${b.corridor_name}</div>
                <span class="badge" style="background: rgba(239,68,68,0.2); color: #fca5a5; font-size: 9px;">${b.severity_tier}</span>
              </div>
              <div style="font-size: 0.72rem; color: #cbd5e1; margin-bottom: 4px;">${b.critical_supply_impact}</div>
              <div style="font-size: 0.68rem; color: var(--accent-cyan);">
                🚢 <strong>Bypass Alternatives:</strong> ${(b.alternative_options || []).join(' · ')}
              </div>
            </div>
          `).join('');
        }
      } catch (spofErr) {
        console.warn("SPOF load fallback:", spofErr);
      }
    }
  } catch (e) {
    console.warn("Analytics fetch fallback:", e);
  }
}

function openSihShowcaseModal() {
  const modal = document.getElementById('modal-sih-showcase');
  if (modal) modal.classList.add('open');
}

function closeSihShowcaseModal() {
  const modal = document.getElementById('modal-sih-showcase');
  if (modal) modal.classList.remove('open');
}

async function runJuryDemoScenario(type) {
  closeSihShowcaseModal();
  if (type === 'disaster_detour') {
    // Ensure admin mode is active so simulation controls are fully interactive
    if (typeof currentRole !== 'undefined' && currentRole !== 'admin') {
      const adminBtn = document.getElementById('role-btn-admin');
      if (adminBtn) await switchRoleAndPersona('admin', adminBtn);
    }
    const simTab = document.querySelector('[data-tab="simulation"]');
    if (simTab) simTab.click();
    setTimeout(() => {
      if (typeof selectScenarioCard === 'function') {
        selectScenarioCard('scenario_sela_landslide');
      }
      const runBtn = document.getElementById('btn-run-simulation');
      if (runBtn) runBtn.click();
    }, 300);
  } else if (type === 'field_closed_loop') {
    openFieldReportModal();
    setTimeout(() => {
      const loc = document.getElementById('rpt-location-name');
      const desc = document.getElementById('rpt-description');
      const sev = document.getElementById('rpt-severity');
      if (loc) loc.value = "Sela Pass Summit (NH-13, 13,700 ft)";
      if (desc) desc.value = "Massive rockfall and frozen debris completely blocking arterial corridor to Tawang.";
      if (sev) sev.value = "BLOCKING";
      showToast("💡 <b>Demo 2 Prepared:</b> Geotagged incident loaded. Click 'Submit Incident Report' to trigger live PWD verification and dynamic rerouting.", 4500);
    }, 200);
  } else if (type === 'data_fusion_dvi') {
    if (typeof currentRole !== 'undefined' && currentRole !== 'admin') {
      const adminBtn = document.getElementById('role-btn-admin');
      if (adminBtn) await switchRoleAndPersona('admin', adminBtn);
    }
    const anTab = document.querySelector('[data-tab="analytics"]');
    if (anTab) anTab.click();
    if (typeof loadDviMatrix === 'function') loadDviMatrix();
  }
}

async function exportDisasterSitrep() {
  try {
    const res = await fetch('/api/analytics/summary');
    const summary = await res.json();
    const dviRes = await fetch('/api/analytics/dvi-matrix');
    const dviData = await dviRes.json();
    const topCutoff = (dviData.matrix || []).slice(0, 5);

    const win = window.open('', '_blank');
    if (!win) {
      alert("Please allow popups to view the Disaster Logistics SITREP.");
      return;
    }

    win.document.write(`
      <!DOCTYPE html>
      <html>
      <head>
        <title>NERA | Disaster Logistics Situation Report (SITREP)</title>
        <style>
          body { font-family: 'Segoe UI', Arial, sans-serif; padding: 30px; color: #1e293b; background: #fff; line-height: 1.5; }
          h1 { color: #0f172a; border-bottom: 2px solid #0284c7; padding-bottom: 8px; font-size: 24px; }
          .badge { background: #fee2e2; color: #b91c1c; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 12px; }
          table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 13px; }
          th, td { border: 1px solid #cbd5e1; padding: 8px 12px; text-align: left; }
          th { background: #f1f5f9; font-weight: 600; }
          .print-btn { background: #0284c7; color: #fff; padding: 8px 18px; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; margin-bottom: 20px; }
          @media print { .print-btn { display: none; } }
        </style>
      </head>
      <body>
        <button class="print-btn" onclick="window.print()">🖨️ Print / Save as PDF</button>
        <h1>🚚 NERA: Disaster Logistics Situation Report (SITREP)</h1>
        <p><strong>Region:</strong> North Eastern Region (8 States) &nbsp;|&nbsp; <strong>Classification:</strong> OFFICIAL EMERGENCY BRIEFING &nbsp;|&nbsp; <strong>Generated:</strong> ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })} IST</p>
        
        <h3>1. Executive Logistics & Freight Status</h3>
        <ul>
          <li><strong>Active Freight Convoys:</strong> ${summary.logistics?.active_freight_convoys || 12} Trucks (${summary.logistics?.total_cargo_weight_tons || 142} Tons)</li>
          <li><strong>Delayed Convoys:</strong> <span class="badge">${summary.logistics?.delayed_convoys_count || 1} Delayed</span></li>
          <li><strong>On-Time Delivery Rate:</strong> ${summary.logistics?.on_time_delivery_rate_pct || 94.8}%</li>
          <li><strong>Verification Accuracy Rate:</strong> ${summary.reports?.verification_accuracy_rate_pct || 92.8}%</li>
        </ul>

        <h3>2. Top Critical Vulnerability Districts (DVI Rankings)</h3>
        <table>
          <thead>
            <tr>
              <th>Rank</th>
              <th>District</th>
              <th>State</th>
              <th>DVI Score</th>
              <th>Primary Hazard</th>
              <th>Oxygen Runway</th>
            </tr>
          </thead>
          <tbody>
            ${topCutoff.map((d, i) => `
              <tr>
                <td>${i + 1}</td>
                <td><strong>${d.district_name}</strong></td>
                <td>${d.state}</td>
                <td><strong>${d.dvi_score} / 100</strong></td>
                <td>${d.primary_vulnerability}</td>
                <td>${d.oxygen_days_left} Days</td>
              </tr>
            `).join('')}
          </tbody>
        </table>

        <h3>3. Multi-Modal Emergency Dispatch SOPs</h3>
        <ul>
          <li><strong>Brahmaputra NW-2 Barge Corridors:</strong> Pandu Port (Guwahati) ➔ Tezpur / Dibrugarh operational for bulk food grains and petroleum.</li>
          <li><strong>Tactical Airbridge Sorties:</strong> IAF Mi-17 and Pawan Hans helicopters on standby for medical oxygen transport to high-altitude passes.</li>
          <li><strong>Border Roads Organisation (BRO):</strong> Project Vartak & Project Pushpak Bailey bridge deployment lead time: 14 - 18 hours.</li>
        </ul>

        <h3>4. Emergency Hotlines</h3>
        <p>National SOS: <strong>112</strong> &nbsp;|&nbsp; NHIDCL Road Help: <strong>1033</strong> &nbsp;|&nbsp; NDRF 1st Bn Control: <strong>+91-361-2840284</strong> &nbsp;|&nbsp; BRO Vartak: <strong>+91-3712-259123</strong></p>
      </body>
      </html>
    `);
    win.document.close();
  } catch (err) {
    console.error("Failed to export SITREP:", err);
  }
}


