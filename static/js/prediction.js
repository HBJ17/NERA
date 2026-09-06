/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 13, 14 & 16: AI Predictive Risk Modeling, Doppler Weather Engine & 4-Stream Data Fusion
 * 
 * Features:
 * - Physics-informed AI Landslide & Flood Hazard Prediction
 * - Live Doppler Weather Radar Layer Rendering on Leaflet
 * - 4-Stream Composite Risk Index (CRI) Fusion Telemetry
 */
let factorChart = null;

function initPredictionControls() {
  const rainSlider = document.getElementById('slider-rainfall');
  const slopeSlider = document.getElementById('slider-slope');
  const soilSlider = document.getElementById('slider-soil');
  const histSlider = document.getElementById('slider-history');

  [rainSlider, slopeSlider, soilSlider, histSlider].forEach(slider => {
    if (slider) {
      slider.addEventListener('input', onPredictionSliderChange);
    }
  });

  const floodRainSlider = document.getElementById('slider-flood-rainfall');
  const floodDischargeSlider = document.getElementById('slider-flood-discharge');
  const floodGaugeSlider = document.getElementById('slider-flood-gauge');

  [floodRainSlider, floodDischargeSlider, floodGaugeSlider].forEach(slider => {
    if (slider) {
      slider.addEventListener('input', onFloodSliderChange);
    }
  });

  predictLandslideRisk();
  predictFloodRisk();
  loadWeatherRadarAndFusion();
}

function onFloodSliderChange() {
  const r = document.getElementById('slider-flood-rainfall');
  const d = document.getElementById('slider-flood-discharge');
  const g = document.getElementById('slider-flood-gauge');

  if (r) document.getElementById('val-flood-rainfall').innerText = `${r.value} mm`;
  if (d) document.getElementById('val-flood-discharge').innerText = `${Number(d.value).toLocaleString()} m³/s`;
  if (g) document.getElementById('val-flood-gauge').innerText = `${g.value} m`;

  predictFloodRisk();
}

let floodDebounceTimer = null;
function predictFloodRisk() {
  clearTimeout(floodDebounceTimer);
  floodDebounceTimer = setTimeout(async () => {
    const rain = parseFloat(document.getElementById('slider-flood-rainfall')?.value || 95);
    const discharge = parseFloat(document.getElementById('slider-flood-discharge')?.value || 38000);
    const gauge = parseFloat(document.getElementById('slider-flood-gauge')?.value || 8.2);

    try {
      const res = await fetch('/api/predict/flood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rainfall_mm: rain,
          river_discharge_cumec: discharge,
          current_gauge_m: gauge,
          danger_mark_m: 8.5,
          catchment_elevation_m: 55.0
        })
      });

      const data = await res.json();
      renderFloodPrediction(data);
    } catch (err) {
      console.error("Flood prediction failed:", err);
    }
  }, 120);
}

function renderFloodPrediction(data) {
  const riskPct = data.flood_risk_pct;
  const meter = document.getElementById('flood-risk-meter');
  const tierBadge = document.getElementById('flood-risk-tier');
  const protocolText = document.getElementById('flood-action-protocol');

  if (meter) {
    meter.innerText = `${riskPct}%`;
    let color = '#00ff88';
    if (riskPct >= 25) color = '#00f0ff';
    if (riskPct >= 50) color = '#ffb800';
    if (riskPct >= 75) color = '#ff3366';
    meter.style.color = color;
  }

  if (tierBadge) {
    tierBadge.innerText = data.risk_level;
    tierBadge.className = `badge badge-${data.risk_level.toLowerCase()}`;
    tierBadge.style.background = riskPct > 50 ? 'rgba(255,51,102,0.2)' : 'rgba(0,240,255,0.2)';
    tierBadge.style.color = riskPct > 50 ? '#ff3366' : '#00f0ff';
  }

  if (protocolText) {
    protocolText.innerText = `${data.action_protocol} (Est. Inundation: ${data.inundation_risk_km2} km²)`;
  }
}

function onPredictionSliderChange() {
  const r = document.getElementById('slider-rainfall');
  const s = document.getElementById('slider-slope');
  const soil = document.getElementById('slider-soil');
  const h = document.getElementById('slider-history');

  if (r) document.getElementById('val-rainfall').innerText = `${r.value} mm`;
  if (s) document.getElementById('val-slope').innerText = `${s.value}°`;
  if (soil) document.getElementById('val-soil').innerText = `${soil.value}%`;
  if (h) document.getElementById('val-history').innerText = `${h.value} Events`;

  predictLandslideRisk();
}

let debounceTimer = null;
function predictLandslideRisk() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(async () => {
    const rain = parseFloat(document.getElementById('slider-rainfall')?.value || 120);
    const slope = parseFloat(document.getElementById('slider-slope')?.value || 35);
    const soil = parseFloat(document.getElementById('slider-soil')?.value || 80);
    const hist = parseInt(document.getElementById('slider-history')?.value || 4);

    try {
      const res = await fetch('/api/predict/landslide', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rainfall_mm: rain,
          slope_degrees: slope,
          soil_saturation_pct: soil,
          historical_landslide_count: hist,
          seismic_zone: 5
        })
      });

      const data = await res.json();
      renderLandslidePrediction(data);
    } catch (err) {
      console.error("Prediction failed:", err);
    }
  }, 100);
}

function renderLandslidePrediction(data) {
  const riskPct = data.landslide_risk_pct;
  const meter = document.getElementById('pred-risk-meter');
  const tierBadge = document.getElementById('pred-risk-tier');
  const protocolText = document.getElementById('pred-action-protocol');

  if (meter) {
    meter.innerText = `${riskPct}%`;
    let color = '#00ff88';
    if (riskPct >= 25) color = '#ffb800';
    if (riskPct >= 50) color = '#ff6b35';
    if (riskPct >= 75) color = '#ff3366';
    meter.style.color = color;
  }

  if (tierBadge) {
    tierBadge.innerText = data.risk_level;
    tierBadge.className = `badge badge-${data.risk_level.toLowerCase()}`;
    tierBadge.style.background = riskPct > 50 ? 'rgba(255,51,102,0.2)' : 'rgba(0,255,136,0.2)';
    tierBadge.style.color = riskPct > 50 ? '#ff3366' : '#00ff88';
  }

  if (protocolText) {
    protocolText.innerText = data.action_protocol;
  }

  renderFactorChart(data.factor_breakdown);
}

function renderFactorChart(factors) {
  const canvas = document.getElementById('chart-factor-weights');
  if (!canvas || !factors) return;

  const labels = factors.map(f => f.name);
  const values = factors.map(f => f.contribution_pct);

  if (factorChart) {
    factorChart.data.labels = labels;
    factorChart.data.datasets[0].data = values;
    factorChart.update();
  } else {
    const ctx = canvas.getContext('2d');
    factorChart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: labels,
        datasets: [{
          data: values,
          backgroundColor: [
            '#00f0ff',
            '#ff3366',
            '#ffb800',
            '#9d4edd'
          ],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              color: '#94a3b8',
              font: { family: 'Outfit', size: 10 }
            }
          }
        }
      }
    });
  }
}

async function loadWeatherRadarAndFusion() {
  try {
    // 1. Fetch Radar Overlays for Leaflet
    const radarRes = await fetch('/api/weather/radar-overlays');
    const overlays = await radarRes.json();
    const weatherGroup = (window.layers && window.layers.weather) || (typeof layers !== 'undefined' && layers.weather);
    if (weatherGroup && Array.isArray(overlays)) {
      weatherGroup.clearLayers();
      overlays.forEach(ov => {
        const circle = L.circle(ov.coordinates, {
          radius: ov.radius_meters,
          color: ov.color,
          fillColor: ov.color,
          fillOpacity: 0.18,
          weight: 1.5,
          dashArray: '3, 6'
        }).bindPopup(`
          <div style="font-family: Outfit, sans-serif;">
            <div style="font-weight: 700; color: ${ov.color};">🌧️ Doppler Radar: ${ov.condition}</div>
            <div>Precipitation: <strong>${ov.rainfall_mm_hr} mm/hr</strong> (${ov.dbz} dBZ)</div>
          </div>
        `);
        weatherGroup.addLayer(circle);
      });
    }

    // 2. Fetch 4-Stream Data Fusion
    const fusionRes = await fetch('/api/weather/fusion/composite-risk');
    const fusionData = await fusionRes.json();
    renderDataFusionCard(fusionData);
  } catch (e) {
    console.warn("Weather & Fusion load fallback:", e);
  }
}

function renderDataFusionCard(data) {
  const container = document.getElementById('data-fusion-stream-container');
  if (!container || !data.corridors) return;

  const topRisks = data.corridors.filter(c => c.composite_risk_score > 35).slice(0, 4);

  container.innerHTML = `
    <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 6px;">
      ⚡ Fusing 4 Active Streams: Doppler Weather + PWD Health + GPS Telemetry + Field Reports
    </div>
    ${topRisks.map(c => `
      <div style="background: rgba(0,0,0,0.3); border-radius: 6px; padding: 8px; margin-bottom: 6px; border-left: 3px solid ${c.composite_risk_score > 60 ? '#ff3366' : '#ffb800'};">
        <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 700; color: #fff;">
          <span>${c.highway_code}</span>
          <span style="color: ${c.composite_risk_score > 60 ? '#ff3366' : '#ffb800'};">CRI: ${c.composite_risk_score}% (${c.risk_tier})</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; font-size: 9px; color: var(--text-muted); margin-top: 4px; font-family: var(--font-mono);">
          <span>🌧️ Rain: ${c.streams_breakdown.weather_stream_pct}%</span>
          <span>🛣️ Infra: ${c.streams_breakdown.infrastructure_stream_pct}%</span>
          <span>🚚 Delay: ${c.streams_breakdown.gps_telemetry_stream_pct}%</span>
          <span>📱 Field: ${c.streams_breakdown.field_reports_stream_pct}%</span>
        </div>
      </div>
    `).join('')}
  `;
}
