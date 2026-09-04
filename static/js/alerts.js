/**
 * NERA (North Eastern Resilience & Autonomous Logistics Engine)
 * Module 12: Multilingual Emergency Alert Broadcast & Speech Synthesis Engine
 * 
 * Implements:
 * - Live disaster ticker and bulletin modal
 * - Dynamic 4-language localization: English, Assamese (অসমীয়া), Hindi (हिन्दी), Bengali (বাংলা)
 * - Browser Web Speech API (SpeechSynthesisUtterance) voice broadcasting for drivers
 */
let currentLanguage = 'en'; // 'en', 'as', 'hi', 'bn'
let activeAlertsList = [];

async function loadActiveAlerts() {
  try {
    const res = await fetch('/api/alerts/active');
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
  if (currentLanguage === 'as') return alertItem.message_as;
  if (currentLanguage === 'hi') return alertItem.message_hi;
  if (currentLanguage === 'bn') return alertItem.message_bn;
  return alertItem.message_en;
}

function renderAlertTicker() {
  const tickerEl = document.getElementById('ticker-message-text');
  if (!tickerEl || activeAlertsList.length === 0) return;

  const topAlert = activeAlertsList[0];
  tickerEl.innerText = `${topAlert.location_tag}: ${getLocalizedAlertMessage(topAlert)}`;
}

function renderAlertsModalList() {
  const container = document.getElementById('alerts-modal-list');
  if (!container) return;

  container.innerHTML = activeAlertsList.map(a => `
    <div style="background: rgba(255,255,255,0.03); border-left: 4px solid ${a.severity === 'CRITICAL_DANGER' ? '#ff3366' : '#ffb800'}; padding: 12px; border-radius: 6px; margin-bottom: 10px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <span style="font-weight: 700; color: #fff; font-size: 13px;">${a.location_tag}</span>
        <span style="font-size: 10px; font-family: var(--font-mono); color: var(--text-muted);">${a.timestamp}</span>
      </div>
      <div style="font-size: 12px; color: #e2e8f0; line-height: 1.4; margin-bottom: 8px;">
        ${getLocalizedAlertMessage(a)}
      </div>
      <button class="ticker-voice-btn" onclick="speakAlertMessage('${a.id}')">
        🔊 Play Multilingual Audio Broadcast
      </button>
    </div>
  `).join('');
}

function speakAlertMessage(alertId) {
  const alertItem = activeAlertsList.find(a => a.id === alertId) || activeAlertsList[0];
  if (!alertItem) return;

  const textToSpeak = getLocalizedAlertMessage(alertItem);

  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(textToSpeak);
    
    // Attempt to set matching voice language
    if (currentLanguage === 'hi') utterance.lang = 'hi-IN';
    else if (currentLanguage === 'bn') utterance.lang = 'bn-IN';
    else if (currentLanguage === 'as') utterance.lang = 'as-IN';
    else utterance.lang = 'en-IN';

    utterance.rate = 0.95;
    window.speechSynthesis.speak(utterance);
  } else {
    alert(`Audio Broadcast: ${textToSpeak}`);
  }
}

function playTopAlertAudio() {
  if (activeAlertsList.length > 0) {
    speakAlertMessage(activeAlertsList[0].id);
  }
}

function openAlertsModal() {
  document.getElementById('modal-alerts-broadcast').classList.add('open');
}

function closeAlertsModal() {
  document.getElementById('modal-alerts-broadcast').classList.remove('open');
}
