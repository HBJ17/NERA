/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 8: Hospital Survival Runway & Critical Medical Inventory System
 * 
 * Tracks buffer stock days for Liquid Medical Oxygen (LMO), ICU antibiotics,
 * vaccines, and food rations across strategic tertiary hospitals in the North East.
 */
function renderSuppliesRunway() {
  if (!twinData || !twinData.districts) return;

  const container = document.getElementById('supplies-hospital-list');
  if (!container) return;

  const criticalHospitals = [
    { name: "AIIMS Guwahati Regional Hub", district: "Guwahati", o2: 18.5, meds: 30, food: 45, status: "GOOD" },
    { name: "Silchar Medical College Hospital (SMCH)", district: "Silchar (Barak Valley)", o2: 4.5, meds: 6.5, food: 12, status: "CRITICAL_LOW" },
    { name: "Tawang District Civil Hospital", district: "Tawang (High Altitude)", o2: 3.8, meds: 7.0, food: 18, status: "WARNING" },
    { name: "Regional Institute of Medical Sciences (RIMS)", district: "Imphal", o2: 9.0, meds: 17.0, food: 24, status: "GOOD" },
    { name: "STNM Multispeciality Hospital", district: "Gangtok (Sikkim)", o2: 6.2, meds: 12.0, food: 22, status: "WARNING" },
    { name: "Civil Hospital Haflong", district: "Haflong (Dima Hasao)", o2: 3.0, meds: 5.0, food: 8.0, status: "CRITICAL_LOW" }
  ];

  container.innerHTML = criticalHospitals.map(h => {
    const isCritical = h.o2 < 5.0;
    const badgeColor = isCritical ? '#ff3366' : (h.o2 < 8.0 ? '#ffb800' : '#00ff88');

    return `
      <div class="cockpit-card" style="border-left: 4px solid ${badgeColor}; padding: 12px; margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div style="font-weight: 700; color: #fff; font-size: 13px;">🏥 ${h.name}</div>
          <span style="font-size: 10px; font-weight: bold; color: ${badgeColor}; font-family: var(--font-mono);">${h.status}</span>
        </div>
        <div style="font-size: 11px; color: #94a3b8;">${h.district}</div>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; margin-top: 8px;">
          <div style="background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px; text-align: center;">
            <div style="font-size: 10px; color: #94a3b8;">Oxygen</div>
            <div style="font-size: 13px; font-weight: bold; color: ${h.o2 < 5 ? '#ff3366' : '#00f0ff'}; font-family: var(--font-mono);">${h.o2}d</div>
          </div>
          <div style="background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px; text-align: center;">
            <div style="font-size: 10px; color: #94a3b8;">Antibiotics</div>
            <div style="font-size: 13px; font-weight: bold; color: #fff; font-family: var(--font-mono);">${h.meds}d</div>
          </div>
          <div style="background: rgba(0,0,0,0.3); padding: 6px; border-radius: 4px; text-align: center;">
            <div style="font-size: 10px; color: #94a3b8;">FCI Rations</div>
            <div style="font-size: 13px; font-weight: bold; color: #fff; font-family: var(--font-mono);">${h.food}d</div>
          </div>
        </div>

        ${isCritical ? `
          <button class="btn-primary" style="margin-top: 8px; font-size: 11px; padding: 4px 8px; width: 100%;" onclick="openEmergencySupplyDispatch('${h.name}')">
            🚨 Dispatch Emergency Supply Convoy
          </button>
        ` : ''}
      </div>
    `;
  }).join('');
}

function openEmergencySupplyDispatch(hospitalName) {
  alert(`⚡ DISPATCH PROTOCOL TRIGGERED: Emergency Liquid Medical Oxygen Convoy assigned from Guwahati AIIMS Depot to ${hospitalName}. AI Safe-Corridor route locked.`);
}
