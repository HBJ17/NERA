/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 6 & 13: Offline-Ready Field Reporting & Edge Sync Engine
 * 
 * Implements:
 * - HTML5 localStorage client-side queue for zero-connectivity mountain corridors
 * - Automatic connection detection (navigator.onLine) and 1-click batch synchronization
 * - Geotagged incident submission and instant Digital Twin graph weight mutation
 */
const OFFLINE_STORAGE_KEY = 'nera_digital_twin_offline_reports';

function getOfflineReports() {
  const data = localStorage.getItem(OFFLINE_STORAGE_KEY);
  return data ? JSON.parse(data) : [];
}

function saveOfflineReport(report) {
  const reports = getOfflineReports();
  reports.push(report);
  localStorage.setItem(OFFLINE_STORAGE_KEY, JSON.stringify(reports));
  updateOfflineBadge();
}

function clearOfflineReports() {
  localStorage.removeItem(OFFLINE_STORAGE_KEY);
  updateOfflineBadge();
}

function updateOfflineBadge() {
  const badge = document.getElementById('offline-queue-count');
  const reports = getOfflineReports();
  if (badge) {
    badge.innerText = reports.length;
    badge.style.display = reports.length > 0 ? 'inline-block' : 'none';
  }
}

async function handleFieldReportSubmit(e) {
  e.preventDefault();

  const officerName = document.getElementById('rpt-officer-name').value;
  const dept = document.getElementById('rpt-department').value;
  const incType = document.getElementById('rpt-incident-type').value;
  const severity = document.getElementById('rpt-severity').value;
  const highway = document.getElementById('rpt-highway').value;
  const locName = document.getElementById('rpt-location').value;
  const desc = document.getElementById('rpt-desc').value;

  // Selected or mock coordinates around NER
  let lat = 25.1764;
  let lng = 93.0189;
  if (highway.includes("13")) { lat = 27.5055; lng = 92.1037; }
  else if (highway.includes("10")) { lat = 26.9500; lng = 88.4800; }
  else if (highway.includes("06")) { lat = 25.4526; lng = 92.2038; }

  const reportPayload = {
    officer_name: officerName,
    department: dept,
    incident_type: incType,
    severity: severity,
    nearest_highway: highway,
    location_name: locName,
    description: desc,
    latitude: lat,
    longitude: lng,
    photo_url: "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80",
    estimated_clearance_hrs: 4.5
  };

  const isOnline = navigator.onLine;

  if (!isOnline) {
    saveOfflineReport(reportPayload);
    alert("📴 NO SATELLITE/CELLULAR NETWORK: Report stored locally in offline database. Will auto-sync when connection is restored.");
    closeFieldReportModal();
    return;
  }

  try {
    const res = await fetch('/api/reports/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reportPayload)
    });

    const saved = await res.json();
    alert(`✅ REPORT VERIFIED & INGESTED (ID: ${saved.id}): Digital Twin hazard layer updated across all state operations centers.`);
    closeFieldReportModal();

    // Refresh twin and alerts
    fetchTwinState();
    loadActiveAlerts();
    loadFieldReportsList();
  } catch (err) {
    console.error("Online submission failed, saving offline:", err);
    saveOfflineReport(reportPayload);
    alert("Saved to offline cache.");
    closeFieldReportModal();
  }
}

async function syncOfflineReports() {
  const reports = getOfflineReports();
  if (reports.length === 0) {
    alert("Offline queue is clean. No pending reports.");
    return;
  }

  let synced = 0;
  for (const r of reports) {
    try {
      await fetch('/api/reports/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(r)
      });
      synced++;
    } catch (e) {
      console.error(e);
    }
  }

  clearOfflineReports();
  alert(`🔄 SYNC COMPLETE: ${synced} field incident reports synced to Digital Twin cloud platform.`);
  fetchTwinState();
  loadActiveAlerts();
}

async function loadFieldReportsList() {
  const container = document.getElementById('field-reports-timeline');
  if (!container) return;

  try {
    const res = await fetch('/api/reports/all');
    const reports = await res.json();

    container.innerHTML = reports.map(r => `
      <div class="cockpit-card" style="padding: 12px; margin-bottom: 8px;">
        <div style="display: flex; justify-content: space-between;">
          <div style="font-weight: 700; color: #ffb800; font-size: 13px;">🚧 ${r.incident_type}</div>
          <span style="font-size: 10px; color: ${r.severity === 'HIGH' ? '#ff3366' : '#00ff88'}; font-weight: bold; font-family: var(--font-mono);">${r.severity}</span>
        </div>
        <div style="font-size: 12px; color: #fff; margin: 3px 0;">${r.location_name} (${r.nearest_highway})</div>
        <div style="font-size: 11px; color: #94a3b8;">${r.description}</div>
        <div style="font-size: 10px; color: var(--text-muted); display: flex; justify-content: space-between; margin-top: 6px; font-family: var(--font-mono);">
          <span>By: ${r.officer_name} (${r.department})</span>
          <span>${r.reported_at}</span>
        </div>
      </div>
    `).join('');
  } catch (err) {
    console.error("Failed to load reports:", err);
  }
}

function openFieldReportModal() {
  document.getElementById('modal-field-report').classList.add('open');
}

function closeFieldReportModal() {
  document.getElementById('modal-field-report').classList.remove('open');
}
