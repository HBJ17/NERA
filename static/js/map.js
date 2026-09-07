/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 1: Interactive Geospatial Digital Twin Map Controller
 * 
 * Manages Leaflet.js visualization of:
 * - 32 Strategic District Nodes (8 NER States)
 * - 10 Vital River Bridges & Clearance Marks
 * - Arterial Mountain Corridors (NH-27, NH-13, NH-10, NH-06)
 * - Real-time GPS Fleet Telemetry & Hazard Points
 */
let map;
let baseLayers = {};
let currentBaseLayer = null;

let layers = {
  highways: L.layerGroup(),
  bridges: L.layerGroup(),
  fleet: L.layerGroup(),
  districts: L.layerGroup(),
  hazards: L.layerGroup(),
  weather: L.layerGroup(),
  activeRoute: L.layerGroup(),
  simulation: L.layerGroup()
};

let twinData = null;

// Expose on global window object for cross-module access
window.map = null;
window.layers = layers;
window.baseLayers = baseLayers;
window.twinData = null;
window.simulationHazardLayer = null;

function initDigitalTwinMap() {
  // Center on North East India (Guwahati / Assam central coordinates)
  map = L.map('leaflet-map', {
    center: [26.2000, 92.6000],
    zoom: 7,
    minZoom: 5,
    maxZoom: 18,
    zoomControl: true
  });
  window.map = map;

  // Base Map Options (100% Free - Zero API Key Required)
  baseLayers.dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd',
    attribution: '&copy; <a href="https://carto.com/">CARTO</a> | &copy; OpenStreetMap contributors',
    maxZoom: 19
  });

  baseLayers.osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    subdomains: 'abc',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxZoom: 19
  });

  baseLayers.satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '&copy; Esri &mdash; Earthstar Geographics, USDA, USGS, AeroGRID, IGN',
    maxZoom: 18
  });

  // Default: Dark Carto / Esri Dark Canvas
  currentBaseLayer = baseLayers.dark;
  currentBaseLayer.addTo(map);

  // Add all data layer groups to map
  Object.values(layers).forEach(layer => layer.addTo(map));

  fetchTwinState();
  initUserLocation();
  initMapInteractivity();
}

function setBasemapStyle(styleKey) {
  if (!baseLayers[styleKey]) return;
  if (currentBaseLayer && map) {
    map.removeLayer(currentBaseLayer);
  }
  currentBaseLayer = baseLayers[styleKey];
  if (map) {
    currentBaseLayer.addTo(map);
    if (typeof currentBaseLayer.bringToBack === 'function') {
      currentBaseLayer.bringToBack();
    }
  }

  // Update UI buttons if any
  document.querySelectorAll('.basemap-btn').forEach(b => b.classList.remove('active'));
  const btn = document.getElementById(`btn-basemap-${styleKey}`);
  if (btn) btn.classList.add('active');
}

let isPinDropMode = false;
let pinStep = 0; // 0 = set origin, 1 = set destination
let pinOriginMarker = null;
let pinDestMarker = null;

function showToast(message, duration = 3500) {
  let toastContainer = document.getElementById('nera-toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'nera-toast-container';
    toastContainer.style.cssText = 'position: fixed; bottom: 85px; right: 24px; z-index: 9999; display: flex; flex-direction: column; gap: 8px; pointer-events: none;';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  toast.style.cssText = 'background: rgba(15, 23, 42, 0.95); border: 1px solid var(--accent-cyan, #00f0ff); color: #fff; padding: 10px 16px; border-radius: 8px; font-size: 0.85rem; font-family: Outfit, sans-serif; box-shadow: 0 8px 24px rgba(0,0,0,0.6); backdrop-filter: blur(8px); animation: fadeIn 0.25s ease; pointer-events: auto; max-width: 360px;';
  toast.innerHTML = message;
  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, duration);
}

function togglePinDropMode(btn) {
  isPinDropMode = !isPinDropMode;
  pinStep = 0;
  const pinBtn = btn || document.getElementById('btn-pin-mode');

  if (isPinDropMode) {
    if (pinBtn) pinBtn.classList.add('active');
    if (map) map.getContainer().style.cursor = 'crosshair';
    showToast("📍 <b>Pin Drop Mode Active</b><br>Click anywhere on the map to drop Origin (🚩)", 4500);
  } else {
    if (pinBtn) pinBtn.classList.remove('active');
    if (map) map.getContainer().style.cursor = '';
    showToast("Pin Drop Mode deactivated.", 2000);
  }
}

function initMapInteractivity() {
  map.on('click', (e) => {
    const lat = parseFloat(e.latlng.lat.toFixed(4));
    const lng = parseFloat(e.latlng.lng.toFixed(4));

    if (isPinDropMode) {
      if (pinStep === 0) {
        // Step 0: Set Origin
        window.customSourceCoords = [lat, lng];
        if (pinOriginMarker) map.removeLayer(pinOriginMarker);
        
        const pinIcon = L.divIcon({
          className: 'custom-pin-marker',
          html: `<div style="background: #00ff88; color: #000; font-weight: 800; font-size: 11px; padding: 4px 8px; border-radius: 12px; border: 2px solid #fff; box-shadow: 0 0 12px #00ff88; white-space: nowrap;">🚩 Origin</div>`,
          iconSize: [60, 24],
          iconAnchor: [30, 24]
        });
        pinOriginMarker = L.marker([lat, lng], { icon: pinIcon }).addTo(map);

        setRouteCoordinate('source', lat, lng, `Pin Point (${lat}, ${lng})`, false);
        pinStep = 1;
        showToast("🚩 <b>Origin Set!</b><br>Now click your Destination location on the map (🏁).", 4000);
      } else {
        // Step 1: Set Destination & Calculate Route
        window.customDestCoords = [lat, lng];
        if (pinDestMarker) map.removeLayer(pinDestMarker);

        const pinIcon = L.divIcon({
          className: 'custom-pin-marker',
          html: `<div style="background: #00f0ff; color: #000; font-weight: 800; font-size: 11px; padding: 4px 8px; border-radius: 12px; border: 2px solid #fff; box-shadow: 0 0 12px #00f0ff; white-space: nowrap;">🏁 Dest</div>`,
          iconSize: [60, 24],
          iconAnchor: [30, 24]
        });
        pinDestMarker = L.marker([lat, lng], { icon: pinIcon }).addTo(map);

        setRouteCoordinate('dest', lat, lng, `Pin Point (${lat}, ${lng})`, true);
        togglePinDropMode();
        showToast("🏁 <b>Destination Set!</b> Computing AI Resilient Corridor...", 3500);
      }
      return;
    }

    const popupContent = `
      <div style="font-family: Outfit, sans-serif; font-size: 13px; line-height: 1.4; min-width: 210px;">
        <div style="font-weight: 700; color: #00f0ff; margin-bottom: 2px;">📍 Selected Map Sector</div>
        <div style="font-size: 11px; color: #94a3b8; margin-bottom: 8px;">Lat: ${lat} · Lng: ${lng}</div>
        <div style="display: flex; flex-direction: column; gap: 6px;">
          <button class="user-nav-btn-go" style="background: linear-gradient(135deg, #ef4444, #dc2626); border-color: #f87171; color: #fff; padding: 6px 10px; font-weight: 700; font-size: 11px; box-shadow: 0 2px 10px rgba(239,68,68,0.4);" onclick="promptTriggerPointHazard(${lat}, ${lng})">
            💥 Simulate Hazard Here
          </button>
          <div style="display: flex; gap: 4px;">
            <button class="user-nav-btn-go" style="flex: 1; padding: 4px 6px; font-size: 10px;" onclick="setRouteCoordinate('source', ${lat}, ${lng}, 'Map Point (${lat}, ${lng})')">
              🚩 Set Origin
            </button>
            <button class="user-nav-btn-go" style="flex: 1; padding: 4px 6px; font-size: 10px;" onclick="setRouteCoordinate('dest', ${lat}, ${lng}, 'Map Point (${lat}, ${lng})')">
              🏁 Set Dest
            </button>
          </div>
        </div>
      </div>
    `;

    L.popup()
      .setLatLng(e.latlng)
      .setContent(popupContent)
      .openOn(map);
  });
}

function setRouteCoordinate(type, lat, lng, label, triggerPlan = true) {
  if (type === 'source') {
    window.customSourceCoords = [lat, lng];
    const srcSelect = document.getElementById('route-source-select');
    if (srcSelect) {
      let opt = Array.from(srcSelect.options).find(o => o.value === 'custom_coords');
      if (!opt) {
        opt = document.createElement('option');
        opt.value = 'custom_coords';
        srcSelect.prepend(opt);
      }
      opt.text = `📍 ${label}`;
      srcSelect.value = 'custom_coords';
    }
  } else {
    window.customDestCoords = [lat, lng];
    const dstSelect = document.getElementById('route-dest-select');
    if (dstSelect) {
      let opt = Array.from(dstSelect.options).find(o => o.value === 'custom_coords');
      if (!opt) {
        opt = document.createElement('option');
        opt.value = 'custom_coords';
        dstSelect.prepend(opt);
      }
      opt.text = `🎯 ${label}`;
      dstSelect.value = 'custom_coords';
    }
    const input = document.getElementById('user-destination-input');
    if (input) input.value = label;
  }
  map.closePopup();

  if (triggerPlan) {
    const routeTabBtn = document.querySelector('[data-tab="routing"]');
    if (routeTabBtn && typeof switchTab === 'function') {
      switchTab('routing', routeTabBtn);
    }
    if (typeof planSmartRoute === 'function') {
      planSmartRoute();
    }
  }
}

function openActiveRouteInGoogleMaps() {
  let srcCoord = null;
  let dstCoord = null;

  if (window.customSourceCoords) {
    srcCoord = window.customSourceCoords;
  } else {
    const srcSelect = document.getElementById('route-source-select');
    const srcId = srcSelect ? srcSelect.value : 'node_guwahati';
    const d = window.twinData && window.twinData.districts ? window.twinData.districts.find(x => x.id === srcId) : null;
    srcCoord = d ? d.coordinates : [26.1445, 91.7362];
  }

  if (window.customDestCoords) {
    dstCoord = window.customDestCoords;
  } else {
    const dstSelect = document.getElementById('route-dest-select');
    const dstId = dstSelect ? dstSelect.value : 'node_tawang';
    const d = window.twinData && window.twinData.districts ? window.twinData.districts.find(x => x.id === dstId) : null;
    dstCoord = d ? d.coordinates : [27.5860, 91.8650];
  }

  const url = `https://www.google.com/maps/dir/?api=1&origin=${srcCoord[0]},${srcCoord[1]}&destination=${dstCoord[0]},${dstCoord[1]}&travelmode=driving`;
  window.open(url, '_blank');
}

function openMapSettingsModal() {
  const modal = document.getElementById('modal-map-settings');
  if (modal) modal.classList.add('open');
}

function closeMapSettingsModal() {
  const modal = document.getElementById('modal-map-settings');
  if (modal) modal.classList.remove('open');
}

function saveMapApiSettings() {
  const mb = document.getElementById('setting-mapbox-key')?.value?.trim();
  const gm = document.getElementById('setting-google-key')?.value?.trim();
  if (mb) localStorage.setItem('nera_mapbox_token', mb);
  if (gm) localStorage.setItem('nera_google_token', gm);
  closeMapSettingsModal();
  showToast("✅ Map configuration saved. 100% Free OpenStreetMap & OSRM Engine default active.");
}

async function fetchTwinState() {
  try {
    const res = await fetch('/api/twin/state');
    twinData = await res.json();
    window.twinData = twinData;
    renderMapElements(twinData);
    updateHudStats(twinData);
    if (typeof populateRouteDropdowns === 'function') {
      populateRouteDropdowns();
    }
  } catch (err) {
    console.error("Failed to load Digital Twin state:", err);
  }
}

function renderMapElements(data) {
  renderHighways(data.highways);
  renderBridges(data.bridges);
  renderDistricts(data.districts);
  renderFleet(data.fleet);
  renderHazards(data.highways);
}

function renderHighways(highways) {
  layers.highways.clearLayers();

  highways.forEach(edge => {
    let color = '#00ff88'; // safe green
    let dashArray = null;
    let weight = 4;

    if (edge.status === 'blocked') {
      color = '#ff3366';
      dashArray = '6, 8';
      weight = 5;
    } else if (edge.status === 'warning' || edge.landslide_risk > 50) {
      color = '#ffb800';
      weight = 4;
    }

    const polyline = L.polyline(edge.coordinates_polyline, {
      color: color,
      weight: weight,
      opacity: 0.85,
      dashArray: dashArray
    });

    const polyCoords = edge.coordinates_polyline || [];
    const midPt = polyCoords.length > 0 ? polyCoords[Math.floor(polyCoords.length / 2)] : [26.0, 92.0];
    const midLat = parseFloat(midPt[0].toFixed(4));
    const midLng = parseFloat(midPt[1].toFixed(4));

    const popupContent = `
      <div style="font-family: Outfit, sans-serif; font-size: 13px; line-height: 1.4;">
        <div style="font-weight: 700; color: ${color}; font-size: 14px; margin-bottom: 4px;">
          ${edge.highway_code}
        </div>
        <div><strong>Length:</strong> ${edge.distance_km} km | <strong>Avg Speed:</strong> ${edge.avg_speed_kmh} km/h</div>
        <div><strong>Landslide Risk:</strong> <span style="color: ${edge.landslide_risk > 50 ? '#ff3366' : '#00ff88'}">${edge.landslide_risk}%</span></div>
        <div><strong>Flood Risk:</strong> ${edge.flood_risk}% | <strong>Rain:</strong> ${edge.rainfall_mm} mm</div>
        <div><strong>Status:</strong> <span style="text-transform: uppercase; font-weight: 700;">${edge.status}</span></div>
        ${edge.closure_reason ? `<div style="color: #fca5a5; margin-top: 4px; font-size: 12px;">⚠️ ${edge.closure_reason}</div>` : ''}
        <button class="user-nav-btn-go" style="background: linear-gradient(135deg, #ef4444, #dc2626); border-color: #f87171; color: #fff; padding: 6px 10px; font-weight: 700; font-size: 11px; margin-top: 8px; width: 100%; box-shadow: 0 2px 10px rgba(239,68,68,0.4);" onclick="promptTriggerPointHazard(${midLat}, ${midLng}, '${edge.id}')">
          💥 Simulate Hazard on this Corridor
        </button>
      </div>
    `;

    polyline.bindPopup(popupContent);
    layers.highways.addLayer(polyline);
  });
}

function renderBridges(bridges) {
  layers.bridges.clearLayers();

  bridges.forEach(b => {
    const isGood = b.status === 'operational';
    const markerColor = isGood ? '#00f0ff' : '#ff3366';

    const bridgeIcon = L.divIcon({
      className: 'custom-bridge-icon',
      html: `
        <div style="background: ${markerColor}; width: 22px; height: 22px; border-radius: 4px; display: flex; align-items: center; justify-content: center; border: 2px solid #fff; box-shadow: 0 0 10px ${markerColor}; color: #000; font-size: 12px; font-weight: bold;">
          🌉
        </div>
      `,
      iconSize: [22, 22],
      iconAnchor: [11, 11]
    });

    const marker = L.marker(b.coordinates, { icon: bridgeIcon });
    marker.bindPopup(`
      <div style="font-family: Outfit, sans-serif; font-size: 13px;">
        <div style="font-weight: 700; color: #00f0ff; font-size: 14px; margin-bottom: 4px;">🌉 ${b.name}</div>
        <div><strong>River:</strong> ${b.river} (${b.state})</div>
        <div><strong>Structural Health:</strong> <span style="color: #00ff88;">${b.structural_health}%</span></div>
        <div><strong>Water Level:</strong> ${b.water_level_m}m / Danger Mark: ${b.danger_mark_m}m</div>
        <div><strong>Vulnerability:</strong> ${b.vulnerability_score}%</div>
        <div><strong>Status:</strong> <span style="color: ${isGood ? '#00ff88' : '#ff3366'}; font-weight: 700; text-transform: uppercase;">${b.status}</span></div>
      </div>
    `);
    layers.bridges.addLayer(marker);
  });
}

function renderDistricts(districts) {
  layers.districts.clearLayers();

  districts.forEach(d => {
    let color = '#00ff88';
    if (d.status === 'limited') color = '#ffb800';
    if (d.status === 'disconnected') color = '#ff3366';

    const circle = L.circleMarker(d.coordinates, {
      radius: 7,
      color: color,
      fillColor: color,
      fillOpacity: 0.85,
      weight: 2
    });

    circle.bindPopup(`
      <div style="font-family: Outfit, sans-serif; font-size: 13px;">
        <div style="font-weight: 700; color: #fff; font-size: 14px; margin-bottom: 4px;">📍 ${d.name} (${d.state})</div>
        <div><strong>Status:</strong> <span style="color: ${color}; font-weight: 700; text-transform: uppercase;">${d.status}</span></div>
        <div><strong>Population:</strong> ${d.population.toLocaleString()}</div>
        <div><strong>Civil Hospitals:</strong> ${d.hospitals}</div>
        <div style="margin-top: 6px; padding-top: 6px; border-top: 1px solid rgba(255,255,255,0.1);">
          <div>🏥 <strong>Oxygen Runway:</strong> ${d.stock_oxygen_days} Days</div>
          <div>📦 <strong>Food Rations:</strong> ${d.stock_rations_days} Days</div>
          <div>💊 <strong>Medicines:</strong> ${d.stock_medicines_days} Days</div>
        </div>
        ${d.critical_alert ? `<div style="color: #fca5a5; margin-top: 4px; font-size: 12px;">🚨 ${d.critical_alert}</div>` : ''}
        <div style="display: flex; gap: 4px; margin-top: 8px;">
          <button class="user-nav-btn-go" style="flex: 1; padding: 4px 6px; font-size: 11px;" onclick="setRouteDistrict('source', '${d.id}', '${d.name}')">
            🚩 From Here
          </button>
          <button class="user-nav-btn-go" style="flex: 1; padding: 4px 6px; font-size: 11px;" onclick="setRouteDistrict('dest', '${d.id}', '${d.name}')">
            🎯 To Here
          </button>
        </div>
        <button class="user-nav-btn-go" style="background: linear-gradient(135deg, #ef4444, #dc2626); border-color: #f87171; color: #fff; padding: 5px 8px; font-weight: 700; font-size: 11px; margin-top: 6px; width: 100%; box-shadow: 0 2px 10px rgba(239,68,68,0.4);" onclick="promptTriggerPointHazard(${d.coordinates[0]}, ${d.coordinates[1]})">
          💥 Simulate Hazard Here
        </button>
      </div>
    `);
    layers.districts.addLayer(circle);
  });
}

function setRouteDistrict(type, id, name) {
  if (type === 'source') {
    const srcSelect = document.getElementById('route-source-select');
    if (srcSelect) srcSelect.value = id;
  } else {
    const dstSelect = document.getElementById('route-dest-select');
    if (dstSelect) dstSelect.value = id;
    const input = document.getElementById('user-destination-input');
    if (input) input.value = name.split(' (')[0];
  }
  map.closePopup();
  if (typeof planSmartRoute === 'function') {
    planSmartRoute();
  }
}

function renderFleet(fleet) {
  layers.fleet.clearLayers();

  fleet.forEach(v => {
    const isCar = v.category === 'car';
    const isDelayed = v.status === 'delayed';

    // Normal user cars: Vibrant Blue (#00d2ff). Logistics heavy carriers: Vibrant Red (#ff3366).
    const markerColor = isCar ? '#00d2ff' : '#ff3366';
    const iconSymbol = isCar ? '🚗' : '🚚';
    const glowShadow = isCar ? 'rgba(0, 210, 255, 0.8)' : 'rgba(255, 51, 102, 0.8)';

    const vehicleIcon = L.divIcon({
      className: 'custom-vehicle-marker',
      html: `
        <div style="background: ${markerColor}; width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #ffffff; box-shadow: 0 0 12px ${glowShadow}; color: #000; font-size: 14px; cursor: pointer; transition: transform 0.2s;">
          ${iconSymbol}
        </div>
      `,
      iconSize: [28, 28],
      iconAnchor: [14, 14]
    });

    const marker = L.marker(v.current_coordinates, { icon: vehicleIcon });
    
    const categoryBadge = isCar
      ? `<span style="background: rgba(0,210,255,0.2); color: #00d2ff; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px; font-family: var(--font-mono);">CIVILIAN CAR (BLUE)</span>`
      : `<span style="background: rgba(255,51,102,0.2); color: #ff3366; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 10px; font-family: var(--font-mono);">LOGISTICS FREIGHT (RED)</span>`;

    marker.bindPopup(`
      <div style="font-family: Outfit, sans-serif; font-size: 13px; line-height: 1.4; min-width: 230px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <div style="font-weight: 700; color: ${markerColor}; font-size: 14px;">${iconSymbol} ${v.vehicle_number}</div>
          ${categoryBadge}
        </div>
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 6px;">${v.vehicle_type}</div>
        <div style="margin-bottom: 3px;"><strong>👤 Driver:</strong> <span style="color: #fff; font-weight: 600;">${v.driver_name}</span> <span style="color: #94a3b8; font-size: 11px;">(${v.driver_phone})</span></div>
        <div style="margin-bottom: 3px;"><strong>📦 Carrying:</strong> <span style="color: #ffb800; font-weight: 600;">${v.cargo_type}</span></div>
        <div style="margin-bottom: 3px;"><strong>🎯 Destination:</strong> ${v.source.split(' (')[0]} ➔ ${v.destination.split(' (')[0]}</div>
        <div style="margin-bottom: 3px;"><strong>⚡ Speed & ETA:</strong> ${v.speed_kmh} km/h · ETA: ${v.eta_timestamp}</div>
        <div style="margin-bottom: 8px;"><strong>Status:</strong> <span style="color: ${isDelayed ? '#ffb800' : '#00ff88'}; font-weight: bold;">${v.status.toUpperCase()}</span> ${v.delay_minutes > 0 ? `(+${v.delay_minutes}m delay)` : ''}</div>
        <button class="user-nav-btn-go" style="width: 100%; padding: 6px 10px; font-size: 11px; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 6px;" onclick="trackVehicleRoute('${v.id}', '${v.source.replace(/'/g, "\\'")}', '${v.destination.replace(/'/g, "\\'")}')">
          🗺️ Track Vehicle Route & Check Hazards
        </button>
      </div>
    `);
    layers.fleet.addLayer(marker);
  });
}

function trackVehicleRoute(vehicleId, source, destination) {
  // Switch to routing tab
  const routeTabBtn = document.querySelector('[data-tab="routing"]');
  if (routeTabBtn && typeof switchTab === 'function') {
    switchTab('routing', routeTabBtn);
  }

  // Find matching district IDs
  let srcId = 'node_guwahati';
  let dstId = 'node_tawang';

  if (window.twinData && window.twinData.districts) {
    const srcMatch = window.twinData.districts.find(d => source.toLowerCase().includes(d.name.toLowerCase()) || source.toLowerCase().includes(d.id.toLowerCase()));
    if (srcMatch) srcId = srcMatch.id;
    
    const dstMatch = window.twinData.districts.find(d => destination.toLowerCase().includes(d.name.toLowerCase()) || destination.toLowerCase().includes(d.id.toLowerCase()));
    if (dstMatch) dstId = dstMatch.id;
  }

  const srcSelect = document.getElementById('route-source-select');
  const dstSelect = document.getElementById('route-dest-select');
  if (srcSelect) srcSelect.value = srcId;
  if (dstSelect) dstSelect.value = dstId;

  if (typeof planSmartRoute === 'function') {
    planSmartRoute(srcId, dstId);
  }

  showToast(`🗺️ <b>Vehicle Route Active</b><br>Tracking path from ${source.split(' (')[0]} to ${destination.split(' (')[0]}`, 4000);
}

function renderHazards(highways) {
  layers.hazards.clearLayers();

  highways.filter(e => e.landslide_risk > 50).forEach(e => {
    // Add pulsing hazard zone around midpoint
    const midIdx = Math.floor(e.coordinates_polyline.length / 2);
    const midPt = e.coordinates_polyline[midIdx];

    const hazardZone = L.circle(midPt, {
      radius: 12000,
      color: '#ff3366',
      fillColor: '#ff3366',
      fillOpacity: 0.25,
      weight: 1,
      dashArray: '4, 4'
    });

    hazardZone.bindPopup(`
      <div style="font-family: Outfit, sans-serif; font-size: 13px;">
        <div style="color: #ff3366; font-weight: 700;">⛰️ HIGH LANDSLIDE HAZARD ZONE</div>
        <div><strong>Corridor:</strong> ${e.highway_code}</div>
        <div><strong>Risk Score:</strong> ${e.landslide_risk}%</div>
        <div><strong>Slope Gradient:</strong> ${e.slope_deg}°</div>
        <div><strong>Rainfall:</strong> ${e.rainfall_mm} mm/24h</div>
      </div>
    `);

    layers.hazards.addLayer(hazardZone);
  });
}

function toggleMapLayer(layerKey, btnElement) {
  if (map.hasLayer(layers[layerKey])) {
    map.removeLayer(layers[layerKey]);
    if (btnElement) btnElement.classList.remove('active');
  } else {
    map.addLayer(layers[layerKey]);
    if (btnElement) btnElement.classList.add('active');
  }
}

let userLocationMarker = null;

function initUserLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const coords = [pos.coords.latitude, pos.coords.longitude];
        setUserLocationMarker(coords);
      },
      () => {
        // Fallback default: Guwahati central
        setUserLocationMarker([26.1445, 91.7362]);
      }
    );
  } else {
    setUserLocationMarker([26.1445, 91.7362]);
  }
}

function setUserLocationMarker(coords) {
  if (userLocationMarker && map) {
    map.removeLayer(userLocationMarker);
  }
  userLocationMarker = L.circleMarker(coords, {
    radius: 9,
    color: '#00f0ff',
    fillColor: '#00f0ff',
    fillOpacity: 0.9,
    weight: 3
  }).bindPopup(`<div style="font-weight: 700; color: #00f0ff;">📍 You Are Here</div>`);
  if (map) {
    userLocationMarker.addTo(map);
  }
}

function drawRouteOnMap(routeCoordinates, color = '#00f0ff', isSecondary = false, clearFirst = false, label = '', isBlocked = false) {
  if (clearFirst && layers.activeRoute) {
    layers.activeRoute.clearLayers();
  }

  const isDanger = isBlocked || color === '#ef4444' || color === '#ff3366';
  const isSafe = color === '#00ff88' || color === '#10b981';

  const routeLine = L.polyline(routeCoordinates, {
    color: isDanger ? '#ef4444' : (isSafe ? '#00ff88' : color),
    weight: isDanger ? 6 : (isSafe ? 7 : (isSecondary ? 4 : 6)),
    opacity: isDanger ? 0.85 : (isSecondary ? 0.75 : 0.95),
    dashArray: isDanger ? '8, 8' : (isSecondary ? '6, 8' : null)
  });

  if (label) {
    routeLine.bindTooltip(label, { sticky: true, className: isDanger ? 'badge-danger-tooltip' : 'badge-safe-tooltip' });
  }

  if (layers.activeRoute) {
    layers.activeRoute.addLayer(routeLine);
  }

  if (!isSecondary && routeCoordinates.length >= 2) {
    const startPt = routeCoordinates[0];
    const endPt = routeCoordinates[routeCoordinates.length - 1];

    const startIcon = L.divIcon({
      className: 'start-route-pin',
      html: `<div style="background: #00ff88; color: #030712; font-weight: 800; font-size: 11px; padding: 2px 8px; border-radius: 12px; border: 2px solid #fff; box-shadow: 0 0 10px #00ff88; white-space: nowrap;">🚩 ORIGIN</div>`,
      iconSize: [70, 22],
      iconAnchor: [35, 11]
    });
    const startMarker = L.marker(startPt, { icon: startIcon }).bindPopup("<strong>🚩 Origin Hub</strong>");

    const endIcon = L.divIcon({
      className: 'dest-route-pin',
      html: `<div style="background: #00f0ff; color: #030712; font-weight: 800; font-size: 11px; padding: 2px 8px; border-radius: 12px; border: 2px solid #fff; box-shadow: 0 0 10px #00f0ff; white-space: nowrap;">🏁 DESTINATION</div>`,
      iconSize: [100, 22],
      iconAnchor: [50, 11]
    });
    const endMarker = L.marker(endPt, { icon: endIcon }).bindPopup("<strong>🏁 Target Destination</strong>");

    layers.activeRoute.addLayer(startMarker);
    layers.activeRoute.addLayer(endMarker);
  }

  if (map && routeCoordinates && routeCoordinates.length >= 2) {
    try {
      const bounds = routeLine.getBounds();
      if (bounds && bounds.isValid()) {
        map.fitBounds(bounds, { padding: [50, 50] });
      }
    } catch (e) {
      console.warn("fitBounds fallback:", e);
    }
  }
}

function showMapHazardBanner(incidentName = 'Disaster Blockade Active', highwayCode = 'Corridor', delayMins = 35) {
  let banner = document.getElementById('floating-map-hazard-banner');
  if (!banner) {
    banner = document.createElement('div');
    banner.id = 'floating-map-hazard-banner';
    banner.className = 'map-hazard-banner';
    const mapContainer = document.getElementById('map-view');
    if (mapContainer) mapContainer.appendChild(banner);
  }

  banner.innerHTML = `
    <span style="font-size: 1.1rem; animation: pulse 1s infinite;">💥</span>
    <div>
      <div style="font-weight: 800; color: #fca5a5; font-size: 0.82rem;">🚨 SEVERED: ${highwayCode}</div>
      <div style="font-size: 0.72rem; color: #94a3b8;">🟢 AI Safe Bypass active (+${delayMins} min detour)</div>
    </div>
    <button class="map-hazard-btn-reset" onclick="resetSimulationState()">🔄 Reset Highway</button>
  `;
  banner.style.display = 'flex';
}

function hideMapHazardBanner() {
  const banner = document.getElementById('floating-map-hazard-banner');
  if (banner) banner.style.display = 'none';
}
window.showMapHazardBanner = showMapHazardBanner;
window.hideMapHazardBanner = hideMapHazardBanner;


function updateHudStats(data) {
  const trkEl = document.getElementById('hud-active-trucks');
  if (trkEl) trkEl.innerText = `${data.fleet.length} Trucks`;

  const distEl = document.getElementById('hud-connected-districts');
  if (distEl) {
    distEl.innerText = `${data.districts.filter(d => d.status === 'connected').length}/${data.districts.length}`;
  }

  const threatEl = document.getElementById('hud-threat-level');
  if (threatEl) threatEl.innerText = data.threat_level.replace(/_/g, ' ');

  const disEl = document.getElementById('hud-active-disruptions');
  if (disEl) disEl.innerText = data.active_disruptions_count;
}

// Auto-refresh fleet telemetry every 5 seconds
setInterval(() => {
  if (twinData) {
    fetch('/api/fleet/live')
      .then(res => res.json())
      .then(fleet => {
        twinData.fleet = fleet;
        renderFleet(fleet);
        if (typeof updateFleetOperatorView === 'function') {
          updateFleetOperatorView(fleet);
        }
      })
      .catch(console.error);
  }
}, 5000);
