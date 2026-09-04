/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 4 & 5: AI Hazard Prediction UI Controller & Chart.js Visualizer
 * 
 * Synchronizes real-time geotechnical slider inputs with backend prediction models,
 * dynamically rendering failure probabilities, action protocols, and factor contributions.
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

  // Initial trigger
  predictLandslideRisk();
}

function onPredictionSliderChange() {
  document.getElementById('val-rainfall').innerText = `${document.getElementById('slider-rainfall').value} mm`;
  document.getElementById('val-slope').innerText = `${document.getElementById('slider-slope').value}°`;
  document.getElementById('val-soil').innerText = `${document.getElementById('slider-soil').value}%`;
  document.getElementById('val-history').innerText = `${document.getElementById('slider-history').value} Events`;

  predictLandslideRisk();
}

let debounceTimer = null;
function predictLandslideRisk() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(async () => {
    const rain = parseFloat(document.getElementById('slider-rainfall').value);
    const slope = parseFloat(document.getElementById('slider-slope').value);
    const soil = parseFloat(document.getElementById('slider-soil').value);
    const hist = parseInt(document.getElementById('slider-history').value);

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

  // Render Factor Importance Chart with Chart.js
  renderFactorChart(data.factor_breakdown);
}

function renderFactorChart(factors) {
  const canvas = document.getElementById('chart-factor-weights');
  if (!canvas) return;

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
