# 🧠 Technical Implementation, Models & Logic Documentation
### AI-Enabled Logistics Intelligence Platform for the North Eastern Region (NER)
#### *A Comprehensive Technical Blueprint of Architectures, Mathematical Models, Algorithms, and Operational Logic*

---

## 🏗️ 1. Architecture Overview: What We Have Done

We have engineered an end-to-end, production-ready **Digital Twin Logistics Intelligence & Disaster Response Platform** tailored for the complex terrain of North East India. The system bridges physical highway and hydrological infrastructure with an in-memory graph representation, live AI hazard inference, automated network resilience stress-testing, multi-factor route optimization, and edge-resilient offline reporting.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                           PRESENTATION LAYER                                           │
│  ┌────────────────────────┬────────────────────────┬───────────────────────┬────────────────────────┐  │
│  │   SDMA / Govt Cockpit  │  Fleet Operator Center │     Driver HUD HUD    │ Essential Supplies Hub │  │
│  └────────────────────────┴────────────────────────┴───────────────────────┴────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Interactive Leaflet GIS (32 Nodes, 10 Bridges, Polylines) • Chart.js Analytics • Web Speech TTS  │  │
│  │ LocalStorage Offline Cache Queue • Multilingual Engine (English, Assamese, Hindi, Bengali)       │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────▲────────────────────────────────────────────────────┘
                                                    │ REST APIs & JSON Payloads
┌───────────────────────────────────────────────────▼────────────────────────────────────────────────────┐
│                                       FASTAPI APPLICATION LAYER                                        │
│  ┌──────────────────────┬──────────────────────┬──────────────────────┬─────────────────────────────┐  │
│  │   /api/twin/*        │   /api/predict/*     │   /api/routing/*     │   /api/simulation/*         │  │
│  │   Digital Twin State │   AI Hazard Models   │   Resilient Route    │   What-If Sandbox           │  │
│  ├──────────────────────┼──────────────────────┼──────────────────────┼─────────────────────────────┤  │
│  │   /api/fleet/*       │   /api/reports/*     │   /api/alerts/*      │   /health & /docs           │  │
│  │   GPS Telemetry      │   Field Ingestion    │   Multilingual Alert │   OpenAPI / Swagger         │  │
│  └──────────────────────┴──────────────────────┴──────────────────────┴─────────────────────────────┘  │
└───────────────────────────────────────────────────▲────────────────────────────────────────────────────┘
                                                    │ Memory References & Service Calls
┌───────────────────────────────────────────────────▼────────────────────────────────────────────────────┐
│                                        CORE SERVICE & LOGIC LAYER                                      │
│  ┌──────────────────────────────────────────────┐    ┌──────────────────────────────────────────────┐  │
│  │         SmartRouteEngine (NetworkX)          │    │          DisasterSimulationEngine            │  │
│  │ • Dual-Graph Architecture (Distance vs Risk) │    │ • Graph Partitioning & Cut-Off Analysis      │  │
│  │ • Dynamic Dijkstra / A* Routing Algorithm    │    │ • Connected Components Evaluation            │  │
│  │ • Yen's K-Shortest Simple Paths Detours      │    │ • Cargo & Hospital At-Risk Aggregations      │  │
│  └──────────────────────────────────────────────┘    └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐    ┌──────────────────────────────────────────────┐  │
│  │              AIPredictionEngine              │    │             FleetAndFieldManager             │  │
│  │ • Empirical GSI/IMD Landslide Ensemble       │    │ • Micro-Telemetry GPS Jitter Simulation      │  │
│  │ • Soil Pore-Pressure & Slope Failure Model   │    │ • Dynamic Field Ingestion & Graph Mutation   │  │
│  │ • Gauge Exceedance River Flood Model         │    │ • Automatic Alert Synthesis in 4 Languages   │  │
│  └──────────────────────────────────────────────┘    └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐  │
│  │                                digital_twin_data (Topology Store)                                │  │
│  │ • 32 Strategic District Nodes  • 10 Vital Bridges  • Highway Polyline Vectors  • Fleet Datasets  │  │
│  └──────────────────────────────────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔬 2. Module-by-Module Technical Deep Dive

---

### Module 1: AI Geological & Hydrological Hazard Prediction Suite
* **Source Files**: [`app/services/ai_predictor.py`](file:///c:/Users/hbj17/Downloads/SIH/app/services/ai_predictor.py), [`app/routers/prediction.py`](file:///c:/Users/hbj17/Downloads/SIH/app/routers/prediction.py), [`static/js/prediction.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/prediction.js)

#### 1. What We Have Done:
* Implemented two high-precision hazard prediction endpoints:
  * `POST /api/predict/landslide`: Computes slope failure probability and factor weights.
  * `POST /api/predict/flood`: Computes river overflow probability, time-to-inundation, and bridge submergence depth.
* Built interactive frontend UI controls with synchronized real-time sliders (Rainfall, Slope, Soil Saturation, Historical Recurrence) and a dynamic Chart.js donut chart rendering factor importance.

#### 2. Model Used:
* **Physics-Informed GSI / IMD Empirical Weighted Ensemble Model** for hill-slope failure.
* **Hydrodynamic Gauge-Exceedance Discharge Model** for river basin flood inundation.

#### 3. Logic & Mathematical Formulation:

##### A. Landslide Failure Probability Algorithm:
The model computes 4 sub-scores and 1 attenuation factor based on geotechnical and meteorological parameters:

1. **Precipitation Sub-Score ($S_{\text{rain}} \in [0, 100]$)**:
   Accounts for non-linear pore-water pressure buildup:
   $$S_{\text{rain}}(r) = \begin{cases} 
   \left(\frac{r}{15}\right) \times 15, & \text{if } r \le 15\text{ mm} \\ 
   15 + \left(\frac{r - 15}{35}\right) \times 35, & \text{if } 15 < r \le 50\text{ mm} \\ 
   50 + \left(\frac{r - 50}{70}\right) \times 35, & \text{if } 50 < r \le 120\text{ mm} \\ 
   \min\left(100, 85 + \left(\frac{r - 120}{100}\right) \times 15\right), & \text{if } r > 120\text{ mm} 
   \end{cases}$$

2. **Slope Angle Sub-Score ($S_{\text{slope}} \in [0, 100]$)**:
   Models peak shear vulnerability between $25^\circ$ and $45^\circ$:
   $$S_{\text{slope}}(\theta) = \begin{cases} 
   5.0, & \text{if } \theta < 10^\circ \\ 
   10 + \left(\frac{\theta - 10}{15}\right) \times 40, & \text{if } 10^\circ \le \theta < 25^\circ \\ 
   50 + \left(\frac{\theta - 25}{20}\right) \times 45, & \text{if } 25^\circ \le \theta \le 45^\circ \\ 
   \max\left(60, 95 - (\theta - 45) \times 1.5\right), & \text{if } \theta > 45^\circ \text{ (Rock face / scree)} 
   \end{cases}$$

3. **Soil Volumetric Saturation Sub-Score ($S_{\text{soil}} \in [0, 100]$)**:
   $$S_{\text{soil}}(\sigma) = \begin{cases} 
   \sigma \times 0.4, & \text{if } \sigma < 40\% \\ 
   16 + \left(\frac{\sigma - 40}{35}\right) \times 45, & \text{if } 40\% \le \sigma < 75\% \\ 
   61 + \left(\frac{\sigma - 75}{25}\right) \times 39, & \text{if } \sigma \ge 75\% 
   \end{cases}$$

4. **Historical & Seismic Score ($S_{\text{hist}} \in [0, 100]$)**:
   $$S_{\text{hist}}(h, z) = \min\left(100.0, \; h \times 16.0 + z \times 6.0\right)$$
   *(where $h$ is the 10-year historical landslide count, and $z$ is the Seismic Zone, default 5 for NER)*.

5. **Vegetation NDVI Attenuation ($A_{\text{veg}}$)**:
   $$A_{\text{veg}}(\text{NDVI}) = \max\left(0.0, \; (\text{NDVI} - 0.2) \times 20.0\right)$$

6. **Weighted Ensemble Risk Synthesis**:
   $$\text{RawRisk} = \Big(0.35 \cdot S_{\text{rain}} + 0.30 \cdot S_{\text{slope}} + 0.20 \cdot S_{\text{soil}} + 0.15 \cdot S_{\text{hist}}\Big) - A_{\text{veg}}$$
   $$\text{FinalRisk} = \text{clamp}\Big(2.0, \; 99.4, \; \text{round}(\text{RawRisk}, 1)\Big)$$

7. **Factor Contribution Percentage ($C_i$)**:
   $$C_i = \left(\frac{W_i \cdot S_i}{\sum_{k} W_k \cdot S_k}\right) \times 100\%$$

##### B. River Basin Flood & Submergence Inundation Logic:
Given gauge difference $\Delta g = \text{CurrentGauge} - \text{DangerMark}$:
* **If $\Delta g \ge 0$ (Water above danger mark)**:
  $$\text{BaseRisk} = 75.0 + \min\left(24.0, \; \left(\frac{\Delta g}{2.0}\right) \times 20.0\right)$$
  $$T_{\text{inundation}} = \max\left(0.5, \; 4.0 - (\Delta g \times 1.5)\right) \text{ hours}$$
  $$D_{\text{submergence}} = 0.4 + (\Delta g \times 0.8) \text{ meters}$$
* **If $-1.0 \le \Delta g < 0$ (Approaching danger mark)**:
  $$\text{BaseRisk} = 45.0 + (1.0 + \Delta g) \times 25.0$$
  $$T_{\text{inundation}} = 8.0 - ((1.0 + \Delta g) \times 4.0) \text{ hours}, \quad D_{\text{submergence}} = 0.0\text{ m}$$
* **If $\Delta g < -1.0$ (Safe river levels)**:
  $$\text{BaseRisk} = \max(5.0, \; 20.0 + \Delta g \times 8.0), \quad T_{\text{inundation}} = 24.0\text{ hours}$$
* **Rainfall Multiplier**:
  If $\text{Rainfall} > 50\text{ mm}$, $\text{Risk} = \min(99.0, \; \text{BaseRisk} + (\text{Rainfall} - 50) \times 0.25)$.

---

### Module 2: Multi-Factor Resilient Routing & Safe-Corridor Engine
* **Source Files**: [`app/services/routing_engine.py`](file:///c:/Users/hbj17/Downloads/SIH/app/services/routing_engine.py), [`app/routers/routing.py`](file:///c:/Users/hbj17/Downloads/SIH/app/routers/routing.py), [`static/js/routing.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/routing.js)

#### 1. What We Have Done:
* Designed a dual-graph network architecture inside Python using `networkx`.
* Implemented route optimization API `POST /api/routing/optimize` taking origin, destination, cargo priority, and dynamic hazard exclusion constraints.
* Provided simultaneous computation and visual comparison of:
  1. *Primary Shortest Highway Route* (Standard shortest distance).
  2. *AI Safe-Corridor Route* (Risk-minimized bypass).
  3. *Secondary Strategic Detour* (Yen's $K$-shortest backup).
* Generated full turn-by-turn navigation itineraries with polyline GIS coordinates and segment hazard warnings.

#### 2. Model Used:
* **Graph Theory Modeling**: Undirected weighted graph $G(V, E)$ where $|V| = 32$ district hubs and $|E| = 45+$ inter-district corridors.
* **Shortest Path Optimization**: Dijkstra's Algorithm ($O(|E| + |V|\log|V|)$) and Yen's $K$-Shortest Loopless Paths Algorithm.

#### 3. Logic & Cost Function Algorithm:

```
                  ┌──────────────────────────────────────────────┐
                  │          Input: Source & Destination         │
                  └──────────────────────┬───────────────────────┘
                                         │
                 ┌───────────────────────┴───────────────────────┐
                 ▼                                               ▼
   ┌───────────────────────────┐                   ┌───────────────────────────┐
   │ Graph 1: G_distance       │                   │ Graph 2: G_resilient      │
   │ Weight = Physical Dist    │                   │ Weight = Dynamic Cost Fcn │
   └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                 │                                               │
                 ▼                                               ▼
   ┌───────────────────────────┐                   ┌───────────────────────────┐
   │ Run Shortest Path         │                   │ Apply Dynamic Exclusions  │
   │ (Dijkstra on G_distance)  │                   │ (Avoid nodes/edges)       │
   └─────────────┬─────────────┘                   └─────────────┬─────────────┘
                 │                                               │
                 │                                               ▼
                 │                                 ┌───────────────────────────┐
                 │                                 │ Run Resilient Path Search │
                 │                                 │ (Dijkstra on G_resilient) │
                 │                                 └─────────────┬─────────────┘
                 │                                               │
                 │                                               ▼
                 │                                 ┌───────────────────────────┐
                 │                                 │ Compute Yen's K=2 Detour  │
                 │                                 │ (Shortest simple paths)   │
                 │                                 └─────────────┬─────────────┘
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         │
                                         ▼
                 ┌──────────────────────────────────────────────┐
                 │ Synthesize Response:                         │
                 │ • Total Distance & Travel Time               │
                 │ • Weighted Aggregate Risk Score              │
                 │ • Landslide & Flood Exposure km              │
                 │ • Turn-by-Turn Navigation & Polyline Points  │
                 └──────────────────────────────────────────────┘
```

##### Dynamic Edge Cost Equation:
For each road segment $e = (u, v)$ with distance $d$, landslide risk $R_{\text{ls}} \in [0, 100]$, flood risk $R_{\text{fl}} \in [0, 100]$, rainfall $r$, and status $S$:

$$\text{Weight}(e) = d \times \left(1.0 + 1.8 \cdot \frac{R_{\text{ls}}}{100} + 1.2 \cdot \frac{R_{\text{fl}}}{100} + 0.6 \cdot \min\left(1.0, \frac{r}{100}\right)\right) \times P(S)$$

Where Status Penalty $P(S)$ is defined as:
$$P(S) = \begin{cases} 
1.0, & \text{if } S = \text{"open"} \\ 
2.2, & \text{if } S = \text{"warning"} \\ 
10.0, & \text{if } S = \text{"critical"} \\ 
99,999.0, & \text{if } S = \text{"blocked"} 
\end{cases}$$

##### Aggregate Route Risk Metric:
$$\bar{R}_{\text{route}} = \frac{\sum_{i=1}^{M} \Big(\max\left(R_{\text{ls}, i}, \; 0.8 \cdot R_{\text{fl}, i}\right) \times d_i\Big)}{\sum_{i=1}^{M} d_i}$$

##### Hazard Exposure Distances:
$$D_{\text{ls\_exposure}} = \sum_{i: R_{\text{ls}, i} > 40} d_i, \qquad D_{\text{flood\_exposure}} = \sum_{i: R_{\text{fl}, i} > 30} d_i$$

---

### Module 3: "What-If" Disaster Simulation & Network Resilience Sandbox
* **Source Files**: [`app/services/simulation_engine.py`](file:///c:/Users/hbj17/Downloads/SIH/app/services/simulation_engine.py), [`app/routers/simulation.py`](file:///c:/Users/hbj17/Downloads/SIH/app/routers/simulation.py), [`static/js/simulation.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/simulation.js)

#### 1. What We Have Done:
* Implemented the disaster stress-testing endpoint `POST /api/simulation/run` and scenarios catalog `GET /api/simulation/scenarios`.
* Engineered automated network isolation detection, population impact calculations, active cargo at-risk evaluation, and autonomous detour synthesis.
* Built preset scenarios (Sela Pass closure, Saraighat bridge flood, Haflong embankment collapse, Teesta gorge cut) and custom simulation capabilities.

#### 2. Model Used:
* **Graph Partitioning & Reachability Analysis**: Connected component analysis and single-source shortest path validation across dynamic subgraphs $G' = (V, E \setminus \{e_{\text{severed}}\})$.
* **Supply Chain Runway & Population Exposure Aggregation Model**.

#### 3. Logic & Execution Flow:

1. **Topology Cloning & Edge Severance**:
   Copies district nodes and filters out the target severed edge $e_{\text{target}}$:
   $$G_{\text{sim}} = (V, E \setminus \{e_{\text{target}}\})$$

2. **District Reachability Evaluation**:
   Designates Guwahati (`node_guwahati`) as the primary logistics gateway. For every node $v \in V$:
   $$\text{HasPath} = \text{nx.has\_path}(G_{\text{sim}}, \; \text{source}=\text{Guwahati}, \; \text{target}=v)$$
   * If $\text{HasPath} = \text{False} \implies \text{Status}(v) = \text{"disconnected"}$ (Isolation Tier: `FULLY_CUT_OFF`).
   * If $\text{HasPath} = \text{True}$:
     $$\text{LengthRatio} = \frac{\text{dist}_{G_{\text{sim}}}(\text{Guwahati}, v)}{\text{dist}_{G_{\text{orig}}}(\text{Guwahati}, v)}$$
     * If $\text{LengthRatio} > 1.5 \implies \text{Status}(v) = \text{"limited"}$ (Isolation Tier: `RESTRICTED_ACCESS`).
     * Else $\implies \text{Status}(v) = \text{"connected"}$.

3. **Population Impact Aggregation**:
   $$\text{TotalPopulationImpacted} = \sum_{v \in V_{\text{isolated}}} \text{Population}(v)$$

4. **Trapped Freight Identification & Supplies Aggregation**:
   Iterates through all active fleet vehicles $v \in \text{Fleet}$:
   * If vehicle's active route segment equals $e_{\text{target}} \implies \text{Delay} = +5.5\text{ hrs}$, Status = `REROUTING_DISPATCHED`.
   * If vehicle's destination is `disconnected` $\implies \text{Delay} = +12.0\text{ hrs}$, reroute note = `Awaiting Helicopter Air-Drop / Bailey Bridge`.
   * If vehicle's destination is `limited` $\implies \text{Delay} = +3.5\text{ hrs}$, reroute note = `Rerouted via Long-Distance Arterial Highway`.
   * Aggregates trapped inventory:
     $$\text{Oxygen}_{\text{at\_risk}} = \sum \text{Liters}, \quad \text{Vaccines}_{\text{at\_risk}} = \sum \text{Tons}, \quad \text{Rations}_{\text{at\_risk}} = \sum \text{Tons}, \quad \text{Fuel}_{\text{at\_risk}} = \sum \text{KL}$$

5. **Autonomous Detour Synthesis**:
   Calls `SmartRouteEngine.optimize_route` between the severed endpoints $u$ and $v$ with `custom_avoid_edges=[target_edge]` to output immediate bypass corridors.

---

### Module 4: Real-Time GPS Fleet Telemetry & Critical Cargo Tracker
* **Source Files**: [`app/services/fleet_tracker.py`](file:///c:/Users/hbj17/Downloads/SIH/app/services/fleet_tracker.py), [`app/routers/fleet.py`](file:///c:/Users/hbj17/Downloads/SIH/app/routers/fleet.py), [`static/js/app.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/app.js)

#### 1. What We Have Done:
* Implemented `GET /api/fleet/live` returning real-time vehicle positions, cargo details, speeds, and ETAs.
* Built vehicle priority categorization (`CRITICAL_LIFE_SAVING`, `HIGH`, `STANDARD`).
* Developed micro-movement telemetry simulation and direct map-card camera focus.

#### 2. Model Used:
* **Kinematic Micro-Displacement Model**: Deterministic pseudo-random GPS jitter along active route vectors.
* **Cargo Priority-Triage Dispatching**.

#### 3. Logic & Implementation:
* **Micro-Telemetry Jitter Algorithm**:
  When `/api/twin/state` is queried, `fleet_manager.tick_telemetry()` is invoked:
  $$\Delta \text{lat} = 0.0008 \times \begin{cases} +1.0, & \text{if vehicle\_id is even} \\ -0.5, & \text{if vehicle\_id is odd} \end{cases}$$
  $$\Delta \text{lng} = 0.0009 \times \begin{cases} +1.0, & \text{if vehicle\_id is even} \\ -0.5, & \text{if vehicle\_id is odd} \end{cases}$$
  $$\text{Lat}_{t+1} = \text{round}(\text{Lat}_t + \Delta \text{lat}, 5), \qquad \text{Lng}_{t+1} = \text{round}(\text{Lng}_t + \Delta \text{lng}, 5)$$
* **Map Focus Handler**: Clicking any fleet card triggers smooth Leaflet coordinate centering (`map.setView([lat, lng], 11, {animate: true})`).

---

### Module 5: Offline-Ready Field Incident Ingestion & Edge Sync Engine
* **Source Files**: [`app/services/fleet_tracker.py`](file:///c:/Users/hbj17/Downloads/SIH/app/services/fleet_tracker.py), [`app/routers/reports.py`](file:///c:/Users/hbj17/Downloads/SIH/app/routers/reports.py), [`static/js/fieldReport.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/fieldReport.js)

#### 1. What We Have Done:
* Implemented `POST /api/reports/submit` and `GET /api/reports/all`.
* Built an offline-first modal reporting workflow with simulated geotagging and photo evidence attachment.
* Constructed a `localStorage` offline buffer queue with automatic status badges and manual/automatic batch flush synchronization.
* Engineered real-time propagation of field incidents directly into digital twin road edge weights and emergency alert feeds.

#### 2. Model Used:
* **Edge Storage Queue & Eventual Consistency Pattern**.
* **Fuzzy Highway Code Matcher & Topological Graph Mutator**.

#### 3. Logic & Flowchart:

```
[User submits incident report]
              │
              ▼
   Is browser online? (navigator.onLine)
        ├── NO ──► [Store JSON in localStorage queue] ──► [Update offline counter badge]
        │
        └── YES ──► POST /api/reports/submit
                          │
                          ▼
             [Assign UUID: rpt_xxxxxx]
             [Set Verification: PWD_CONFIRMED / VERIFIED_AI]
             [Prepend to Global Reports List]
                          │
                          ▼
             _propagate_field_report_to_twin()
             ├─ 1. Normalize reported highway code (strip '-', ' ')
             ├─ 2. Find matching edge in digital twin graph
             ├─ 3. If severity is HIGH or BLOCKING:
             │     • Set edge status = "warning"
             │     • Elevate edge landslide_risk = max(risk, 85.0%)
             │     • Append closure_reason text
             └─ 4. Synthesize live multilingual emergency alert:
                   • English (en)
                   • Assamese (as)
                   • Hindi (hi)
                   • Bengali (bn)
                   • Prepend to global alerts broadcast list
```

---

### Module 6: Multilingual Emergency Alert Broadcast & Speech Synthesis Engine
* **Source Files**: [`app/routers/alerts.py`](file:///c:/Users/hbj17/Downloads/SIH/app/routers/alerts.py), [`static/js/alerts.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/alerts.js)

#### 1. What We Have Done:
* Implemented `GET /api/alerts/active` delivering active bulletins with full localization.
* Created a rolling ticker at the top of the command header with voice audio broadcast triggers.
* Implemented multi-language switching across **English**, **অসমীয়া (Assamese)**, **हिन्दी (Hindi)**, and **বাংলা (Bengali)**.
* Integrated browser-native Text-to-Speech (TTS) audio synthesis.

#### 2. Model Used:
* **W3C Web Speech API (`SpeechSynthesis` & `SpeechSynthesisUtterance`)**.
* **Locale-Aware Audio Synthesis Dispatcher**.

#### 3. Logic & Audio Engine:
* **Language Selection Matrix**:
  ```javascript
  function getLocalizedAlertMessage(alertItem) {
    if (currentLanguage === 'as') return alertItem.message_as;
    if (currentLanguage === 'hi') return alertItem.message_hi;
    if (currentLanguage === 'bn') return alertItem.message_bn;
    return alertItem.message_en;
  }
  ```
* **Speech Synthesis Dispatch**:
  ```javascript
  const utterance = new SpeechSynthesisUtterance(textToSpeak);
  if (currentLanguage === 'hi') utterance.lang = 'hi-IN';
  else if (currentLanguage === 'bn') utterance.lang = 'bn-IN';
  else if (currentLanguage === 'as') utterance.lang = 'as-IN';
  else utterance.lang = 'en-IN';
  utterance.rate = 0.95;
  window.speechSynthesis.speak(utterance);
  ```

---

### Module 7: Hospital Survival Runway & Critical Medical Inventory System
* **Source Files**: [`static/js/supplies.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/supplies.js), [`app/models/schemas.py`](file:///c:/Users/hbj17/Downloads/SIH/app/models/schemas.py)

#### 1. What We Have Done:
* Monitored buffer runway (in days) for Liquid Medical Oxygen ($O_2$), ICU Antibiotics, and FCI Food Rations across 6 strategic regional hospitals (AIIMS Guwahati, SMCH Silchar, Tawang Civil Hospital, RIMS Imphal, STNM Gangtok, Haflong Civil Hospital).
* Built automated triaging with early warning threshold alerts and one-click emergency supply convoy dispatching.

#### 2. Model Used:
* **Inventory Depletion Runway Model**: Stock runway $T_{\text{runway}} = \frac{\text{CurrentStock}}{\text{DailyBurnRate}}$.

#### 3. Logic & Classification Rules:
* **Oxygen Stock Triage**:
  $$\text{TriageStatus}(O_2) = \begin{cases} 
  \text{CRITICAL\_LOW} \; (\text{Red, } \#\text{ff3366}), & \text{if } O_2 < 5.0 \text{ days} \\ 
  \text{WARNING} \; (\text{Amber, } \#\text{ffb800}), & \text{if } 5.0 \le O_2 < 8.0 \text{ days} \\ 
  \text{GOOD} \; (\text{Green, } \#\text{00ff88}), & \text{if } O_2 \ge 8.0 \text{ days} 
  \end{cases}$$
* **Emergency Dispatch Trigger**:
  If $\text{TriageStatus} == \text{"CRITICAL\_LOW"}$, a high-priority dispatch button is rendered that locks an emergency cryogenic oxygen convoy route from the AIIMS Guwahati regional reserve depot.

---

### Module 8: Multi-Stakeholder Command Cockpit & Persona Management
* **Source Files**: [`static/js/app.js`](file:///c:/Users/hbj17/Downloads/SIH/static/js/app.js), [`static/index.html`](file:///c:/Users/hbj17/Downloads/SIH/static/index.html), [`static/css/style.css`](file:///c:/Users/hbj17/Downloads/SIH/static/css/style.css)

#### 1. What We Have Done:
* Designed a unified, dark-mode glassmorphic interface with 4 persona modes:
  1. `sdma`: State Disaster Management Authority / Government Command.
  2. `fleet`: Commercial Fleet Operator.
  3. `driver`: Truck Driver HUD Navigation.
  4. `supplies`: Essential Medical Supplies Coordinator.
* Built dynamic tab navigation (Twin, Simulation, Predictor, Routing, Supplies, Reports), live IST/UTC clocks, and map layer toggles.

#### 2. Model Used:
* **State-Driven Single Page Application (SPA) Controller**.

#### 3. Logic & Persona State Transition:
* When a user selects a persona, the system updates active CSS states and automatically navigates the cockpit to the most relevant operational tab:
  $$\text{switchPersona}(P) \implies \begin{cases} 
  \text{switchTab}(\text{"twin"}), & \text{if } P = \text{"sdma"} \lor P = \text{"fleet"} \\ 
  \text{switchTab}(\text{"routing"}), & \text{if } P = \text{"driver"} \\ 
  \text{switchTab}(\text{"supplies"}), & \text{if } P = \text{"supplies"} 
  \end{cases}$$

---

## 📊 3. Summary Compendium of Mathematical Formulas

| Mathematical Function / Formula | Operational Purpose | Applied In Module |
|---|---|---|
| $S_{\text{rain}}(r) = \text{Piecewise}(r)$ | Non-linear rainfall pore-water pressure curve | AI Landslide Predictor |
| $S_{\text{slope}}(\theta) = \text{Piecewise}(\theta)$ | Peak shear failure threshold ($25^\circ-45^\circ$) | AI Landslide Predictor |
| $S_{\text{soil}}(\sigma) = \text{Piecewise}(\sigma)$ | Volumetric soil moisture saturation curve | AI Landslide Predictor |
| $S_{\text{hist}}(h, z) = \min(100, 16h + 6z)$ | 10-year seismic & recurrence index | AI Landslide Predictor |
| $\text{RawRisk} = \sum W_i S_i - A_{\text{veg}}$ | Weighted ensemble slope failure score | AI Landslide Predictor |
| $C_i = (W_i S_i / \sum W_k S_k) \times 100\%$ | Factor importance breakdown percentage | AI Landslide Predictor |
| $T_{\text{inundation}} = 4.0 - (\Delta g \times 1.5)$ | Flood surge time-to-submergence (hours) | AI Flood Predictor |
| $\text{Cost}(e) = d \cdot (1 + 1.8 R_{\text{ls}} + 1.2 R_{\text{fl}} + 0.6 r) \cdot P(S)$ | Hazard-weighted dynamic edge cost | Resilient Routing Engine |
| $\bar{R}_{\text{route}} = \frac{\sum \max(R_{\text{ls}}, 0.8 R_{\text{fl}}) \cdot d}{\sum d}$ | Aggregate route risk index ($0-100$) | Resilient Routing Engine |
| $\Delta R = \bar{R}_{\text{primary}} - \bar{R}_{\text{resilient}}$ | AI safety advantage / risk reduction % | Resilient Routing Engine |
| $\Delta t = (T_{\text{resilient}} - T_{\text{primary}}) \times 60$ | Time delta (minutes) for safety bypass | Resilient Routing Engine |
| $\text{nx.has\_path}(G_{\text{sim}}, \text{src}, \text{dst})$ | Connected component reachability | Disaster Simulation Sandbox |
| $\text{Pop}_{\text{affected}} = \sum_{v \in V_{\text{cut\_off}}} \text{Pop}(v)$ | Total isolated population quantification | Disaster Simulation Sandbox |
| $\text{Stock}_{\text{at\_risk}} = \sum_{v \in \text{Trapped}} \text{Cargo}(v)$ | Liters $O_2$, Vaccine tons, Grain tons trapped | Disaster Simulation Sandbox |

---

## 🛠️ 4. Technology Stack & Implementation Mapping

* **Backend Language & Framework**: Python 3.10+, FastAPI, Uvicorn ASGI.
* **Graph & Algorithms**: NetworkX (`Graph`, `shortest_path`, `shortest_simple_paths`, `has_path`, `shortest_path_length`).
* **Data Validation & Schemas**: Pydantic v2 (`BaseModel`, `Field`).
* **Geospatial & Mapping**: Leaflet.js v1.9.4, OpenStreetMap Tiles.
* **Charts & Visualizations**: Chart.js (Doughnut & Bar charts).
* **Audio & Speech**: HTML5 Web Speech API (`SpeechSynthesisUtterance`).
* **Edge Storage**: Browser `window.localStorage` Offline Cache.
* **Styling & UI**: Modern Vanilla CSS3 (Custom Glassmorphism, CSS Grid, Flexbox, JetBrains Mono & Outfit typography).
* **Containerization**: Docker, Docker Compose, Railway.app cloud deployment.
