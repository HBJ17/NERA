/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 8, 9, 15 & 17: Role-Scoped Emergency Alerts, Multilingual TTS Voice & Emergency Broadcast
 * 
 * Features:
 * - Role-Scoped Ticker Scope: Admin (Regional), User (Local Transit), Govt Employee (District Specific)
 * - Multilingual Localization: English, Assamese (অসমীয়া), Hindi (हिन्दी), Bengali (বাংলা)
 * - Web Speech API SpeechSynthesis text-to-speech with priority escalation (Normal -> Warning -> Critical Auto-Voice)
 */
let currentLanguage = 'en'; // 'en', 'as', 'hi', 'bn'
let activeAlertsList = [];

async function loadActiveAlerts() {
  try {
    const role = window.currentRole || 'admin';
    const districtId = window.currentDistrictId || 'node_kohima';
    const res = await fetch(`/api/alerts/scoped?role=${role}&district_id=${districtId}`);
    activeAlertsList = await res.json();
    renderAlertTicker();
    renderAlertsModalList();
  } catch (err) {
    console.error("Failed to load alerts:", err);
  }
}

function setAppLanguage(lang) {
  currentLanguage = lang;
  renderAlertTicker();
  renderAlertsModalList();
}

function getLocalizedAlertMessage(alertItem) {
  if (currentLanguage === 'as') return alertItem.message_as || alertItem.message_en;
  if (currentLanguage === 'hi') return alertItem.message_hi || alertItem.message_en;
  if (currentLanguage === 'bn') return alertItem.message_bn || alertItem.message_en;
  return alertItem.message_en;
}

function renderAlertTicker() {
  const tickerEl = document.getElementById('ticker-message-text');
  if (!tickerEl || activeAlertsList.length === 0) return;

  const role = window.currentRole || 'admin';
  const topAlert = activeAlertsList[0];

  let prefix = "🚨 LIVE REGIONAL ALERT";
  if (role === 'user') {
    prefix = "📍 YOUR LOCALITY";
  } else if (role === 'gov_employee') {
    const distSelect = document.getElementById('active-district-select');
    const dName = distSelect ? distSelect.options[distSelect.selectedIndex]?.text?.split(' (')[0] : "District";
    prefix = `📍 DISTRICT: ${dName.toUpperCase()}`;
  }

  tickerEl.innerHTML = `<strong>${prefix}</strong> — <span style="color: ${topAlert.severity === 'CRITICAL_DANGER' ? '#ff85a2' : '#ffb800'};">${topAlert.location_tag}</span>: ${getLocalizedAlertMessage(topAlert)}`;
}

function renderAlertsModalList() {
  const container = document.getElementById('alerts-modal-list');
  if (!container) return;

  const role = window.currentRole || 'admin';

  container.innerHTML = `
    <div style="font-size: 0.78rem; color: var(--text-muted); margin-bottom: 8px;">
      Showing bulletins for: <strong style="color: var(--accent-cyan); text-transform: uppercase;">${role} VIEW</strong>
    </div>
    ${activeAlertsList.map(a => `
      <div style="background: rgba(255,255,255,0.03); border-left: 4px solid ${a.severity === 'CRITICAL_DANGER' ? '#ff3366' : '#ffb800'}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <span style="font-weight: 700; color: #fff; font-size: 13px;">${a.location_tag}</span>
          <span style="font-size: 10px; font-family: var(--font-mono); color: var(--text-muted);">${a.timestamp}</span>
        </div>
        <div style="font-size: 12px; color: #e2e8f0; line-height: 1.4; margin-bottom: 8px;">
          ${getLocalizedAlertMessage(a)}
        </div>
        <button class="ticker-voice-btn" onclick="speakAlertMessage('${a.id}')">
          🔊 Play Voice Announcement
        </button>
      </div>
    `).join('')}
  `;
}

function speakAlertMessage(alertId) {
  const alertItem = activeAlertsList.find(a => a.id === alertId) || activeAlertsList[0];
  if (!alertItem) return;

  const textToSpeak = getLocalizedAlertMessage(alertItem);

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    
    if (currentLanguage === 'hi') utterance.lang = 'hi-IN';
    else if (currentLanguage === 'bn') utterance.lang = 'bn-IN';
    else if (currentLanguage === 'as') utterance.lang = 'as-IN';
    else utterance.lang = 'en-IN';

    utterance.rate = 0.92;
    window.speechSynthesis.speak(utterance);
  } else {
    alert(`Voice Broadcast: ${textToSpeak}`);
  }
}

function playTopAlertAudio() {
  if (activeAlertsList.length > 0) {
    speakAlertMessage(activeAlertsList[0].id);
  }
}

function openAlertsModal() {
  const modal = document.getElementById('modal-alerts-broadcast');
  if (modal) modal.classList.add('open');
}

function closeAlertsModal() {
  const modal = document.getElementById('modal-alerts-broadcast');
  if (modal) modal.classList.remove('open');
}
