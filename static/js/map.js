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
let layers = {
  highways: L.layerGroup(),
  bridges: L.layerGroup(),
  fleet: L.layerGroup(),
  districts: L.layerGroup(),
  hazards: L.layerGroup(),
  weather: L.layerGroup(),
  activeRoute: L.layerGroup()
};

let twinData = null;

function initDigitalTwinMap() {
  // Center on North East India (Guwahati / Assam central coordinates)
  map = L.map('leaflet-map', {
    center: [26.2000, 92.6000],
    zoom: 7,
    minZoom: 6,
    maxZoom: 13,
    zoomControl: true
  });

  // Dark CartoDB Matter tile layer
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://carto.com/">CARTO</a> | NER Digital Twin',
    maxZoom: 19
  }).addTo(map);

  // Add all layer groups to map
  Object.values(layers).forEach(layer => layer.addTo(map));

  fetchTwinState();
  initUserLocation();
}

async function fetchTwinState() {
  try {
    const res = await fetch('/api/twin/state');
    twinData = await res.json();
    renderMapElements(twinData);
    updateHudStats(twinData);
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
      fillOpacity: 0.8,
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
      </div>
    `);
    layers.districts.addLayer(circle);
  });
}

function renderFleet(fleet) {
  layers.fleet.clearLayers();

  fleet.forEach(v => {
    const isDelayed = v.status === 'delayed';
    const markerColor = isDelayed ? '#ffb800' : '#00f0ff';

    const truckIcon = L.divIcon({
      className: 'custom-truck-icon',
      html: `
        <div style="background: ${markerColor}; width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; border: 2px solid #fff; box-shadow: 0 0 12px ${markerColor}; color: #000; font-size: 13px;">
          🚚
        </div>
      `,
      iconSize: [26, 26],
      iconAnchor: [13, 13]
    });

    const marker = L.marker(v.current_coordinates, { icon: truckIcon });
    marker.bindPopup(`
      <div style="font-family: Outfit, sans-serif; font-size: 13px;">
        <div style="font-weight: 700; color: #00f0ff; font-size: 14px; margin-bottom: 2px;">🚚 ${v.vehicle_number}</div>
        <div style="font-size: 12px; color: #94a3b8; margin-bottom: 6px;">${v.vehicle_type}</div>
        <div><strong>Cargo:</strong> <span style="color: #ffb800;">${v.cargo_type}</span></div>
        <div><strong>Priority:</strong> <span style="color: #ff3366; font-weight: bold;">${v.cargo_priority}</span></div>
        <div><strong>Driver:</strong> ${v.driver_name} (${v.driver_phone})</div>
        <div><strong>Speed:</strong> ${v.speed_kmh} km/h | <strong>ETA:</strong> ${v.eta_timestamp}</div>
        <div><strong>Origin:</strong> ${v.source}</div>
        <div><strong>Destination:</strong> ${v.destination}</div>
        <div><strong>Status:</strong> <span style="color: ${isDelayed ? '#ffb800' : '#00ff88'}; font-weight: bold;">${v.status.toUpperCase()}</span> ${v.delay_minutes > 0 ? `(+${v.delay_minutes}m delay)` : ''}</div>
      </div>
    `);
    layers.fleet.addLayer(marker);
  });
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
    btnElement.classList.remove('active');
  } else {
    map.addLayer(layers[layerKey]);
    btnElement.classList.add('active');
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

function drawRouteOnMap(routeCoordinates, color = '#00f0ff', isSecondary = false) {
  if (!isSecondary) {
    layers.activeRoute.clearLayers();
  }

  const routeLine = L.polyline(routeCoordinates, {
    color: color,
    weight: isSecondary ? 4 : 6,
    opacity: isSecondary ? 0.6 : 0.95,
    dashArray: isSecondary ? '5, 10' : null
  });

  layers.activeRoute.addLayer(routeLine);

  if (!isSecondary && routeCoordinates.length >= 2) {
    const startPt = routeCoordinates[0];
    const endPt = routeCoordinates[routeCoordinates.length - 1];

    const startMarker = L.circleMarker(startPt, {
      radius: 7,
      color: '#00ff88',
      fillColor: '#00ff88',
      fillOpacity: 1
    }).bindPopup("<strong>Start Point</strong>");

    const endMarker = L.circleMarker(endPt, {
      radius: 7,
      color: '#ff3366',
      fillColor: '#ff3366',
      fillOpacity: 1
    }).bindPopup("<strong>Destination</strong>");

    layers.activeRoute.addLayer(startMarker);
    layers.activeRoute.addLayer(endMarker);
  }

  map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });
}

function updateHudStats(data) {
  document.getElementById('hud-active-trucks').innerText = data.fleet.length;
  document.getElementById('hud-connected-districts').innerText = 
    `${data.districts.filter(d => d.status === 'connected').length}/${data.districts.length}`;
  document.getElementById('hud-threat-level').innerText = data.threat_level.replace(/_/g, ' ');
  document.getElementById('hud-active-disruptions').innerText = data.active_disruptions_count;
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
