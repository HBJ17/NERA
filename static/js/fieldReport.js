/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 4, 6 & 19: Crowdsourced Field Reporting, Photo Upload & Offline Sync Engine
 * 
 * Features:
 * - HTML5 localStorage / IndexedDB client-side queue for offline hill corridors
 * - Auto-capture Live GPS or map click coordinate picker
 * - Base64 Photo compression and preview
 * - Online / Offline auto-detection (navigator.onLine & window.addEventListener)
 * - State Machine: SUBMITTED -> PENDING_VERIFICATION -> VERIFIED -> ACTIVE_INCIDENT
 */
const OFFLINE_STORAGE_KEY = 'nera_field_reports_offline_queue';
let uploadedPhotoBase64 = null;

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

// Listen to network status changes
window.addEventListener('online', () => {
  console.log("Network online. Initiating auto-sync of offline field reports...");
  syncOfflineReports(true);
});

function openFieldReportModal() {
  const modal = document.getElementById('modal-field-report');
  if (!modal) return;

  // Set default values based on active role
  const role = window.currentRole || 'user';
  const deptSelect = document.getElementById('rpt-department');
  const officerInput = document.getElementById('rpt-officer-name');
  const emergencyCheck = document.getElementById('rpt-emergency-flag');

  if (role === 'gov_employee') {
    if (deptSelect) deptSelect.value = 'SDMA Field Officer';
    if (officerInput) officerInput.value = 'District Disaster Operations Officer';
    if (emergencyCheck) emergencyCheck.checked = false;
  } else {
    if (deptSelect) deptSelect.value = 'Local Citizen';
    if (officerInput) officerInput.value = 'Local Citizen / Commuter';
    if (emergencyCheck) emergencyCheck.checked = false;
  }

  // Populate highway dropdown dynamically from twin data
  const hwySelect = document.getElementById('rpt-highway');
  if (hwySelect && window.twinData && window.twinData.highways) {
    hwySelect.innerHTML = window.twinData.highways.map(h => `
      <option value="${h.highway_code.split(' (')[0]}">${h.highway_code} (${h.distance_km} km)</option>
    `).join('');
  }

  // Pre-fill live GPS
  acquireReportGPS();

  modal.classList.add('open');
}


function closeFieldReportModal() {
  const modal = document.getElementById('modal-field-report');
  if (modal) modal.classList.remove('open');
  uploadedPhotoBase64 = null;
  const preview = document.getElementById('rpt-photo-preview-container');
  if (preview) preview.style.display = 'none';
}

function acquireReportGPS() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        document.getElementById('rpt-lat').value = pos.coords.latitude.toFixed(4);
        document.getElementById('rpt-lng').value = pos.coords.longitude.toFixed(4);
      },
      (err) => {
        // Default to active district or Guwahati
        document.getElementById('rpt-lat').value = "25.1764";
        document.getElementById('rpt-lng').value = "93.0189";
      }
    );
  }
}

function previewReportPhoto(e) {
  const file = e.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (event) => {
    uploadedPhotoBase64 = event.target.result;
    const img = document.getElementById('rpt-photo-preview-img');
    const container = document.getElementById('rpt-photo-preview-container');
    if (img && container) {
      img.src = uploadedPhotoBase64;
      container.style.display = 'block';
    }
  };
  reader.readAsDataURL(file);
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
  const lat = parseFloat(document.getElementById('rpt-lat').value) || 25.1764;
  const lng = parseFloat(document.getElementById('rpt-lng').value) || 93.0189;
  const isEmergency = document.getElementById('rpt-emergency-flag') ? document.getElementById('rpt-emergency-flag').checked : false;

  const role = window.currentRole || 'user';
  const isGov = role === 'gov_employee' || role === 'admin' || dept.includes('PWD') || dept.includes('SDMA');

  const reportPayload = {
    officer_name: officerName,
    department: dept,
    reporter_role: isGov ? "gov_employee" : "user",
    incident_type: incType,
    severity: severity,
    nearest_highway: highway,
    location_name: locName,
    description: desc,
    latitude: lat,
    longitude: lng,
    photo_base64: uploadedPhotoBase64,
    photo_url: uploadedPhotoBase64 ? null : "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80",
    estimated_clearance_hrs: severity === 'BLOCKING' ? 8.0 : 4.0,
    emergency_flag: isEmergency,
    confidence_score: isGov ? 92.0 : 65.0
  };

  const isOnline = navigator.onLine;

  if (!isOnline) {
    saveOfflineReport(reportPayload);
    alert("📴 NO NETWORK (HILL CORRIDOR): Report cached in Offline Storage. Will auto-sync when connection is restored.");
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
    alert(`✅ GROUND TRUTH INGESTED (ID: ${saved.id})\nStatus: ${saved.verification_status}\nTrust Score: ${saved.confidence_score}%\nDigital Twin network updated!`);
    closeFieldReportModal();

    // Refresh twin, alerts, and field feed timeline
    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();
    if (typeof loadFieldReportsList === 'function') loadFieldReportsList();
  } catch (err) {
    console.error("Submission failed, fallback to offline queue:", err);
    saveOfflineReport(reportPayload);
    alert("Saved to offline cache.");
    closeFieldReportModal();
  }
}

async function syncOfflineReports(isSilent = false) {
  const reports = getOfflineReports();
  if (reports.length === 0) {
    if (!isSilent) alert("Offline queue is empty. All reports synchronized.");
    return;
  }

  try {
    const res = await fetch('/api/reports/sync-batch', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(reports)
    });

    const data = await res.json();
    clearOfflineReports();
    if (!isSilent) alert(`🔄 SYNC COMPLETE: ${data.synced_count} offline field reports synced to server.`);
    
    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();
    if (typeof loadFieldReportsList === 'function') loadFieldReportsList();
  } catch (e) {
    console.error("Offline sync failed:", e);
    if (!isSilent) alert("Sync failed. Check network connectivity.");
  }
}

async function verifyReportAction(reportId, action) {
  try {
    const res = await fetch(`/api/reports/verify/${reportId}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: action,
        verifier_name: window.currentRole === 'gov_employee' ? "District Emergency Officer" : "AI-GIS Commander",
        verifier_department: "SDMA / PWD Division",
        notes: action === "CONFIRM" ? "Ground team verified blockage." : "False report / cleared."
      })
    });

    const data = await res.json();
    alert(`Report ${reportId} marked as ${data.report.verification_status}!`);
    loadFieldReportsList();
    if (typeof fetchTwinState === 'function') fetchTwinState();
    if (typeof loadActiveAlerts === 'function') loadActiveAlerts();
  } catch (e) {
    console.error("Verification failed:", e);
    alert("Verification request failed.");
  }
}

let currentReportFilter = 'all';

function setReportsFilter(filterKey, btn) {
  currentReportFilter = filterKey;
  document.querySelectorAll('.report-filter-btn').forEach(b => {
    b.classList.remove('active');
    b.style.background = 'transparent';
    b.style.color = 'var(--text-muted)';
  });
  if (btn) {
    btn.classList.add('active');
    btn.style.background = 'rgba(255,255,255,0.12)';
    btn.style.color = '#fff';
  }
  loadFieldReportsList();
}

async function loadFieldReportsList() {
  const container = document.getElementById('field-reports-timeline');
  if (!container) return;

  try {
    const res = await fetch('/api/reports/all');
    const reports = await res.json();

    const role = window.currentRole || 'admin';
    const districtId = window.currentDistrictId || 'node_kohima';

    // If Govt Employee, prioritize or filter to assigned district
    let displayReports = reports;
    if (role === 'gov_employee' && window.twinData && window.twinData.districts) {
      const d = window.twinData.districts.find(x => x.id === districtId);
      const dName = d ? d.name.split(' (')[0].toLowerCase() : '';
      if (dName) {
        const districtMatches = reports.filter(r => 
          (r.location_name && r.location_name.toLowerCase().includes(dName)) || 
          (r.nearest_highway && r.nearest_highway.toLowerCase().includes(dName))
        );
        if (districtMatches.length > 0) {
          displayReports = districtMatches;
        }
      }
    }

    // Apply Quick Filter (All / Pending / Verified)
    if (currentReportFilter === 'pending') {
      displayReports = displayReports.filter(r => r.verification_status === 'PENDING_VERIFICATION');
    } else if (currentReportFilter === 'verified') {
      displayReports = displayReports.filter(r => r.verification_status !== 'PENDING_VERIFICATION');
    }

    if (!displayReports || displayReports.length === 0) {
      container.innerHTML = `
        <div style="padding: 20px; text-align: center; color: var(--text-muted); font-size: 0.8rem; background: rgba(0,0,0,0.2); border-radius: var(--radius-md);">
          ${currentReportFilter === 'pending' ? '✨ No pending reports awaiting approval in this queue.' : 'No active incident reports found.'}
        </div>
      `;
      return;
    }

    container.innerHTML = displayReports.map(r => {
      const isPending = r.verification_status === 'PENDING_VERIFICATION';
      const isVerified = r.verification_status === 'ACTIVE_INCIDENT' || r.verification_status === 'PWD_CONFIRMED' || r.verification_status === 'VERIFIED_AI';
      const statusColor = isVerified ? '#00ff88' : (isPending ? '#ffb800' : '#ff3366');

      // Only Government Employee and Admin can approve or reject reports
      const showVerifyButtons = (role === 'gov_employee' || role === 'admin') && isPending;

      return `
        <div class="cockpit-card" style="padding: 12px; margin-bottom: 10px; border-left: 4px solid ${statusColor}; background: rgba(15, 23, 42, 0.65);">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: 700; color: #fff; font-size: 13px;">
              ${r.incident_type} (${r.nearest_highway})
            </div>
            <span class="badge" style="background: rgba(255,255,255,0.08); color: ${statusColor}; font-size: 10px; font-weight: 700;">
              ${r.verification_status.replace(/_/g, ' ')} (${r.confidence_score || 65}% Trust)
            </span>
          </div>

          <div style="font-size: 11px; color: var(--text-muted); margin: 3px 0;">
            📍 ${r.location_name} · By: <strong style="color: #fff;">${r.officer_name}</strong> (${r.department || 'Citizen'}) · ${r.reported_at || 'Recently'}
          </div>

          <div style="font-size: 12px; color: var(--text-secondary); margin: 6px 0; line-height: 1.3;">
            ${r.description}
          </div>

          ${r.photo_base64 || r.photo_url ? `
            <div style="margin: 6px 0;">
              <img src="${r.photo_base64 || r.photo_url}" alt="Evidence" style="max-height: 90px; border-radius: 6px; border: 1px solid var(--border-subtle);">
            </div>
          ` : ''}

          ${showVerifyButtons ? `
            <div style="display: flex; gap: 8px; margin-top: 8px;">
              <button class="btn-primary" style="padding: 6px 12px; font-size: 11px; flex: 1; background: #00ff88; color: #000; font-weight: 700;" onclick="verifyReportAction('${r.id}', 'CONFIRM')">
                ✓ Approve & Propagate
              </button>
              <button class="btn-secondary" style="padding: 6px 12px; font-size: 11px; flex: 1; border-color: #ff3366; color: #ff3366;" onclick="verifyReportAction('${r.id}', 'REJECT')">
                ✕ Reject / Clear
              </button>
            </div>
          ` : (role === 'user' ? `
            <div style="margin-top: 6px; font-size: 10px; color: ${isVerified ? '#00ff88' : '#ffb800'}; display: flex; align-items: center; gap: 4px;">
              ${isVerified ? '✅ Officially verified by Emergency District Command' : '⏳ Submitted by commuter · Awaiting district authority review'}
            </div>
          ` : '')}
        </div>
      `;
    }).join('');
  } catch (e) {
    console.error("Failed to load reports timeline:", e);
  }
}
