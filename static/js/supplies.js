/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 8: Hospital Survival Runway & Critical Medical Inventory System
 * 
 * Tracks buffer stock days for Liquid Medical Oxygen (LMO), ICU antibiotics,
 * vaccines, and food rations across strategic tertiary hospitals in all 32 North East districts.
 */
let supplyFilter = 'all'; // 'all', 'critical', 'warning'

function renderSuppliesRunway(filterMode = 'all') {
  supplyFilter = filterMode;
  if (!window.twinData || !window.twinData.districts) return;

  const container = document.getElementById('supplies-hospital-list');
  if (!container) return;

  let districts = [...window.twinData.districts];

  if (supplyFilter === 'critical') {
    districts = districts.filter(d => d.stock_oxygen_days < 5.0 || d.stock_medicines_days < 8.0);
  } else if (supplyFilter === 'warning') {
    districts = districts.filter(d => d.stock_oxygen_days < 9.0);
  }

  // Sort by lowest oxygen days first
  districts.sort((a, b) => a.stock_oxygen_days - b.stock_oxygen_days);

  container.innerHTML = `
    <div style="display: flex; gap: 6px; margin-bottom: 10px;">
      <button class="user-nav-btn-go ${supplyFilter === 'all' ? 'active' : ''}" style="padding: 3px 8px; font-size: 11px;" onclick="renderSuppliesRunway('all')">
        All Districts (${window.twinData.districts.length})
      </button>
      <button class="user-nav-btn-go ${supplyFilter === 'critical' ? 'active' : ''}" style="padding: 3px 8px; font-size: 11px; background: rgba(255,51,102,0.2); color: #ff3366; border-color: #ff3366;" onclick="renderSuppliesRunway('critical')">
        🚨 Critical Oxygen (<5d)
      </button>
      <button class="user-nav-btn-go ${supplyFilter === 'warning' ? 'active' : ''}" style="padding: 3px 8px; font-size: 11px; background: rgba(255,184,0,0.2); color: #ffb800; border-color: #ffb800;" onclick="renderSuppliesRunway('warning')">
        ⚠️ Warning (<9d)
      </button>
    </div>
    ${districts.map(d => {
      const isCritical = d.stock_oxygen_days < 5.0;
      const isWarning = d.stock_oxygen_days < 9.0;
      const statusLabel = isCritical ? 'CRITICAL_LOW' : (isWarning ? 'WARNING' : 'STABLE');
      const badgeColor = isCritical ? '#ff3366' : (isWarning ? '#ffb800' : '#00ff88');
      const hospName = `${d.name.split(' (')[0]} District Civil & Referral Hospital`;

      return `
        <div class="cockpit-card" style="border-left: 4px solid ${badgeColor}; padding: 12px; margin-bottom: 8px;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: 700; color: #fff; font-size: 13px;">🏥 ${hospName}</div>
            <span style="font-size: 10px; font-weight: bold; color: ${badgeColor}; font-family: var(--font-mono);">${statusLabel}</span>
          </div>
          <div style="font-size: 11px; color: #94a3b8; margin: 2px 0;">📍 ${d.name} (${d.state}) · ${d.hospitals} Civil Hospitals</div>
          
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 8px;">
            <div style="background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px; text-align: center;">
              <div style="font-size: 10px; color: #94a3b8;">Liquid Oxygen</div>
              <div style="font-size: 13px; font-weight: bold; color: ${isCritical ? '#ff3366' : (isWarning ? '#ffb800' : '#00f0ff')}; font-family: var(--font-mono);">${d.stock_oxygen_days}d</div>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px; text-align: center;">
              <div style="font-size: 10px; color: #94a3b8;">ICU Meds</div>
              <div style="font-size: 13px; font-weight: bold; color: #fff; font-family: var(--font-mono);">${d.stock_medicines_days}d</div>
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px; text-align: center;">
              <div style="font-size: 10px; color: #94a3b8;">FCI Rations</div>
              <div style="font-size: 13px; font-weight: bold; color: #fff; font-family: var(--font-mono);">${d.stock_rations_days}d</div>
            </div>
          </div>

          ${isWarning ? `
            <button class="btn-primary" style="margin-top: 8px; font-size: 11px; padding: 5px 8px; width: 100%; background: ${isCritical ? '#ff3366' : 'linear-gradient(135deg, #00f0ff, #0077ff)'}; color: ${isCritical ? '#fff' : '#000'}; font-weight: 700;" onclick="openEmergencySupplyDispatch('${hospName.replace(/'/g, "\\'")}', '${d.id}', [${d.coordinates[0]}, ${d.coordinates[1]}])">
              ⚡ Dispatch Emergency LMO Convoy (Green Corridor)
            </button>
          ` : ''}
        </div>
      `;
    }).join('')}
  `;
}

async function openEmergencySupplyDispatch(hospitalName, districtId, coords) {
  // Plan route from AIIMS Guwahati Regional Hub to Target Hospital
  if (typeof planSmartRoute === 'function') {
    await planSmartRoute("node_guwahati", districtId);
  }

  // Switch to routing tab and focus map
  const routeTabBtn = document.querySelector('[data-tab="routing"]');
  if (routeTabBtn && typeof switchTab === 'function') {
    switchTab('routing', routeTabBtn);
  }

  const activeMap = window.map || (typeof map !== 'undefined' ? map : null);
  if (activeMap && coords) {
    activeMap.setView(coords, 9, { animate: true });
  }

  if (typeof startActiveNavigation === 'function') {
    startActiveNavigation();
  }

  alert(`🚨 EMERGENCY GREEN CORRIDOR ACTIVATED:\n\nConvoy: AS-01-GC-9281 (Liquid Medical Oxygen 16,000L)\nOrigin: AIIMS Guwahati Regional Hub\nDestination: ${hospitalName}\n\nNavigation HUD locked with zero-traffic clearance priority.`);
}

