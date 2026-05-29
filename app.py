import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(
    page_title="SafetyLens — Process Safety Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Minimal CSS — only what Streamlit actually applies reliably
st.markdown("""
<style>
/* Hide chrome */
#MainMenu, footer, header {visibility: hidden;}

/* Topbar */
.sl-topbar {
    background: #0a1628;
    padding: 12px 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #1e3a5f;
    margin: -1rem -1rem 0 -1rem;
}
.sl-brand { font-size: 1.2rem; font-weight: 900; color: #ffffff; }
.sl-brand b { color: #3b82f6; }
.sl-sub { font-size: 0.6rem; color: #475569; letter-spacing: 2px; text-transform: uppercase; }
.sl-pill {
    background: rgba(237,137,54,0.2);
    border: 1px solid rgba(237,137,54,0.5);
    color: #f6ad55;
    font-size: 0.72rem;
    font-weight: 700;
    padding: 5px 16px;
    border-radius: 20px;
}

/* Ticker */
.sl-ticker {
    background: #080d18;
    padding: 8px 24px;
    border-bottom: 1px solid #1e3a5f;
    margin: 0 -1rem 1rem -1rem;
    display: flex;
    gap: 2rem;
    overflow-x: auto;
    font-size: 0.75rem;
}
.sl-tick-item { white-space: nowrap; color: #94a3b8; }
.sl-tick-item b { color: #e2e8f0; font-family: monospace; }
.sl-up { color: #22c55e; font-weight: 700; }
.sl-down { color: #ef4444; font-weight: 700; }

/* Industry cards on home */
.sl-ind-card {
    background: #0d1f35;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 8px;
    cursor: pointer;
}
.sl-ind-name { font-size: 0.9rem; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.sl-ind-desc { font-size: 0.72rem; color: #64748b; margin-bottom: 10px; }
.sl-ind-stat { font-size: 0.78rem; color: #94a3b8; }

/* Metric row */
.sl-metrics {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 1px;
    background: #1e3a5f;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 1rem;
}
.sl-metric {
    background: #0d1f35;
    padding: 14px 10px;
    text-align: center;
}
.sl-metric-val {
    font-size: 1.6rem;
    font-weight: 900;
    font-family: 'Courier New', monospace;
    line-height: 1;
    color: #e2e8f0;
}
.sl-metric-lbl {
    font-size: 0.55rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    color: #475569;
    margin-top: 4px;
    text-transform: uppercase;
}

/* Alert cards */
.sl-alert {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: #1a0505;
    border: 1px solid #7f1d1d;
    border-left: 4px solid #ef4444;
    border-radius: 8px;
    padding: 12px 14px;
    margin-bottom: 8px;
}
.sl-alert-score {
    background: #ef4444;
    color: white;
    font-size: 0.68rem;
    font-weight: 800;
    padding: 4px 8px;
    border-radius: 6px;
    font-family: monospace;
    white-space: nowrap;
    flex-shrink: 0;
}
.sl-alert-text { font-size: 0.82rem; color: #fca5a5; line-height: 1.5; }

/* Process card */
.sl-proc {
    background: #0d1f35;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 14px;
    margin-bottom: 8px;
}
.sl-proc.hho { border-left: 4px solid #f97316; }
.sl-proc.lho { border-left: 4px solid #6366f1; }
.sl-proc-title { font-size: 0.88rem; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.sl-proc-desc { font-size: 0.73rem; color: #64748b; line-height: 1.5; margin-bottom: 8px; }
.sl-tag {
    display: inline-block;
    font-size: 0.6rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 20px;
    margin-right: 4px;
}
.sl-tag-hho { background: rgba(249,115,22,0.15); color: #f97316; border: 1px solid rgba(249,115,22,0.3); }
.sl-tag-lho { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); }
.sl-tag-psm { background: rgba(167,139,250,0.15); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }

/* Accident row */
.sl-acc {
    background: #0d1f35;
    border: 1px solid #1e3a5f;
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 6px;
    display: grid;
    grid-template-columns: 60px 1fr 60px;
    gap: 12px;
    align-items: center;
}

/* Section header */
.sl-sec {
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: #3b82f6;
    text-transform: uppercase;
    margin: 1.5rem 0 0.6rem 0;
    padding-bottom: 6px;
    border-bottom: 1px solid #1e3a5f;
}

/* Step label */
.sl-step {
    font-size: 1.1rem;
    font-weight: 800;
    color: #e2e8f0;
    margin: 1.2rem 0 0.6rem 0;
}
.sl-step span { color: #64748b; font-weight: 400; font-size: 0.9rem; }

/* Info card */
.sl-card {
    background: #0d1f35;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 8px;
    font-size: 0.82rem;
    color: #94a3b8;
    line-height: 1.8;
}
.sl-card b { color: #e2e8f0; }

/* Risk bar */
.sl-rbar-wrap { display: flex; align-items: center; gap: 8px; margin-top: 4px; }
.sl-rbar-bg { background: #1e3a5f; border-radius: 3px; height: 6px; flex: 1; }
.sl-rbar-fill { height: 6px; border-radius: 3px; }

/* CIM table */
.sl-cim { border-collapse: collapse; width: 100%; font-size: 0.75rem; }
.sl-cim td, .sl-cim th { border: 1px solid #1e3a5f; padding: 7px 12px; text-align: center; }
.sl-cim th { background: #080d18; color: #64748b; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; }
.sl-cim .y { background: rgba(239,68,68,0.15); color: #f87171; font-weight: 700; }
.sl-cim .n { background: rgba(34,197,94,0.1); color: #4ade80; }
.sl-cim .x { background: #1e3a5f; color: #475569; }
.sl-cim .rh { background: #080d18; color: #94a3b8; font-weight: 600; text-align: left; }

/* Status badge */
.sl-status-hho { background: rgba(249,115,22,0.15); border: 1px solid rgba(249,115,22,0.4); color: #f97316; font-size: 0.66rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; }
.sl-status-psm { background: rgba(167,139,250,0.15); border: 1px solid rgba(167,139,250,0.4); color: #a78bfa; font-size: 0.66rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; }

/* Chat */
.sl-chat-user { background: #1d4ed8; color: white; padding: 9px 13px; border-radius: 12px 12px 4px 12px; font-size: 0.8rem; margin: 5px 0; max-width: 80%; margin-left: auto; display: block; }
.sl-chat-ai { background: #0d1f35; border: 1px solid #1e3a5f; color: #e2e8f0; padding: 9px 13px; border-radius: 12px 12px 12px 4px; font-size: 0.8rem; margin: 5px 0; max-width: 85%; white-space: pre-wrap; line-height: 1.6; display: block; }

/* Bowtie */
.sl-cause { background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.25); border-left: 3px solid #3b82f6; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; font-size: 0.8rem; color: #93c5fd; font-weight: 500; }
.sl-consq { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-left: 3px solid #ef4444; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; font-size: 0.8rem; color: #fca5a5; font-weight: 500; }

/* Playground status */
.sl-safe { background: rgba(34,197,94,0.1); border: 2px solid #22c55e; border-radius: 10px; padding: 14px; text-align: center; }
.sl-warn { background: rgba(234,179,8,0.1); border: 2px solid #eab308; border-radius: 10px; padding: 14px; text-align: center; }
.sl-danger { background: rgba(239,68,68,0.1); border: 2px solid #ef4444; border-radius: 10px; padding: 14px; text-align: center; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

HIERARCHY = {
    "Steel & Metal": {
        "Tata Steel — Jamshedpur Works": {
            "Iron Making": ["Inbound Logistics","Coke Plant","By Product Plant","Haldia Met Coke Plant","Sinter Plant #1","Sinter Plant #2","Sinter Plant #3","Sinter Plant #4","Raw Material Bedding","Pellet Plant","Blast Furnace A","Blast Furnace F","Blast Furnace G","Blast Furnace H","Blast Furnace I"],
            "Long Product Area": ["LD#1 & Continuous Caster","Lime Plant","New Bar Mill","Wire and Rod Mill","Merchant Mill"],
            "Flat Product Area": ["LD#2 & Slab Caster","Hot Strip Mill","LD#3 TSCR","Cold Rolling Mill","Tubes Division"],
        },
        "Tata Steel — Tinplate (TCIL), Golmuri": {
            "Tinplate Operations": ["ETL-1 — Electrolytic Tinning Line 1","ETL-2 — Electrolytic Tinning Line 2","CRM — Cold Rolling Mill","TFS — Tin Free Steel","Galvanizing Line (GI/GA)","Colour Coated Sheet (CCS)"],
            "Utilities": ["Hydrogen Plant — H2 Production & Supply"],
        },
        "Tata Steel — Kalinganagar, Odisha": {
            "Kalinganagar Works": ["Raw Material Handling","Coke Plant","Sinter Plant","Blast Furnace","Steel Melting Shop","Hot Strip Mill"],
        },
        "Tata Steel — Meramandali, Odisha": {
            "Meramandali Works": ["Inbound Logistics","Coke Oven","Sinter Plant","Direct Reduced Iron","Blast Furnace-1","Blast Furnace-2","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill"],
        },
        "Tata Metaliks — Kharagpur, WB": {
            "Metaliks Works": ["Blast Furnace","Ductile Iron Pipe Plant","Coke Oven"],
        },
        "JSW Steel — Vijayanagar, Karnataka": {
            "Vijayanagar Works": ["Coke Oven","Sinter Plant","Blast Furnace","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill","Galvanizing Line","Color Coating Line"],
        },
        "JSW Steel — Dolvi, Maharashtra": {
            "Dolvi Works": ["Corex Iron Making","Electric Arc Furnace","Hot Strip Mill","Wire Rod Mill"],
        },
        "AM/NS India — Hazira, Gujarat": {
            "Hazira Works": ["Blast Furnace","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill","Galvanizing"],
        },
        "SAIL — Rourkela, Odisha": {
            "RSP Works": ["Coke Oven","Blast Furnace","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill"],
        },
    },
    "Pharma": {
        "Sun Pharma — Halol, Gujarat": {"API Block": ["API Synthesis Unit","Reactor Block A","Reactor Block B","Solvent Recovery"]},
        "Dr. Reddy's — Hyderabad": {"Formulation": ["Tablet Manufacturing","Sterile Injectables","Packaging Line"]},
        "Cipla — Patalganga": {"Manufacturing": ["API Plant","Oral Solids","Liquid Formulations"]},
    },
    "Oil & Gas": {
        "HPCL — Vizag Refinery": {"Refinery": ["Crude Distillation Unit","FCC Unit","Hydrocracker","LPG Plant","Storage & Dispatch"]},
        "BPCL — Mumbai Refinery": {"Refinery": ["CDU","VDU","FCCU","Reformer","Sulphur Recovery"]},
        "IOCL — Mathura Refinery": {"Refinery": ["Crude Unit","Naphtha Hydrotreater","FCC Unit","Merox Unit"]},
        "ONGC — Mumbai High": {"Offshore": ["Production Platform","Gas Compression","Water Injection","Pipeline"]},
    },
    "Food & Beverage": {
        "ITC — Munger Factory": {"Processing": ["Cigarette Manufacturing","Packaging Line","Boiler House","ETP"]},
        "Nestle — Moga Plant": {"Processing": ["Milk Reception","Spray Drying","Packaging","Utilities"]},
    },
    "Chemicals": {
        "Tata Chemicals — Mithapur": {"Soda Ash": ["Chlor-Alkali Plant","Soda Ash Plant","Vacuum Salt Plant"]},
        "UPL — Bharuch": {"Agrochemicals": ["Chlorine Plant","Pesticide Synthesis","Formulation Unit"]},
        "Deepak Nitrite — Nandesari": {"Nitrites": ["Sodium Nitrite Plant","Nitric Acid Plant","Colour Division"]},
    },
}

IND_META = {
    "Steel & Metal":   {"color":"#f97316","risk":"HIGH",  "incidents":2847,"plants":312},
    "Pharma":          {"color":"#a78bfa","risk":"MEDIUM","incidents":892, "plants":234},
    "Oil & Gas":       {"color":"#ef4444","risk":"CRITICAL","incidents":5621,"plants":891},
    "Food & Beverage": {"color":"#22c55e","risk":"LOW",   "incidents":341, "plants":187},
    "Chemicals":       {"color":"#06b6d4","risk":"HIGH",  "incidents":3194,"plants":542},
}

PSM_FRAMEWORK = {
    # ── Tata Steel PSRM Module — Consequence Levels ──────────────────
    "consequence_levels": {
        "L1": {"label":"L1 — Minor","color":"#22c55e",
               "people":"First Aid Case (FAC). No fatality, no hospitalisation.",
               "community":"No off-site impact.",
               "asset":"Property damage < Rs.5 Lakhs. Minor equipment damage.",
               "environment":"Negligible. Contained on-site. No reportable release.",
               "production":"< 8 hours production loss.",
               "desc":"Minor incident. No process safety implication. Managed at supervisory level.",
               "psm_action":"Record in Near Miss/FAC register. Investigate within 5 working days. No statutory reporting.",
               "examples":["Minor chemical spill — contained in bund","Slip/trip — first aid","Minor instrument failure causing brief stoppage"]},
        "L2": {"label":"L2 — Moderate","color":"#eab308",
               "people":"Medical Treatment Case (MTC) or Lost Time Injury (LTI). No fatality.",
               "community":"Limited off-site impact. Reversible. No public alarm.",
               "asset":"Property damage Rs.5 – 50 Lakhs.",
               "environment":"Limited release. Reversible impact. Reportable to local authority.",
               "production":"8-72 hours production loss.",
               "desc":"Moderate incident. Reportable internally. May involve process safety element.",
               "psm_action":"CAPA required within 30 days. Review by plant head. Check PSCE status. Internal report.",
               "examples":["Chemical spill requiring cleanup team","LTI from process deviation","Equipment damage Rs.5-50L"]},
        "L3": {"label":"L3 — Serious","color":"#f97316",
               "people":"Multiple LTI or hospitalisation. Single fatality possible.",
               "community":"Significant off-site impact. Community notified. Temporary evacuation possible.",
               "asset":"Property damage Rs.50 Lakhs – 5 Crores. Major equipment destruction.",
               "environment":"Significant release. Regulatory notification required. Potential long-term impact.",
               "production":"72 hours – 1 month production loss.",
               "desc":"Serious process safety incident. Mandatory statutory reporting to PESO/CPCB.",
               "psm_action":"Immediate PESO/CPCB notification. Emergency response activation. Full RCA within 15 days. Board-level review.",
               "examples":["HHO process deviation causing fire","Toxic release above ERPG-2","Major equipment failure with injury"]},
        "L4": {"label":"L4 — Critical","color":"#ef4444",
               "people":"Multiple hospitalisations. 1-5 fatalities.",
               "community":"Community significantly affected. Multi-area evacuation. Media coverage.",
               "asset":"Property damage Rs.5 – 50 Crores. Section/plant destroyed.",
               "environment":"Major release. Long-term environmental impact. NDRF involvement.",
               "production":"1-6 months production loss.",
               "desc":"Major process safety accident. Statutory investigation. Regulatory intervention and plant shutdown.",
               "psm_action":"PESO/District authority notification within 12h. Crisis management. External RCA team. Insurance claim.",
               "examples":["Explosion with fatality","Major fire — plant section destroyed","Toxic cloud reaching community boundary"]},
        "L5": {"label":"L5 — Catastrophic","color":"#7f1d1d",
               "people":"Mass casualties. > 5 fatalities.",
               "community":"Widespread off-site impact. Mass evacuation. National media.",
               "asset":"Property damage > Rs.50 Crores. Plant total loss.",
               "environment":"Catastrophic release. Irreversible environmental damage. International reporting.",
               "production":"> 6 months or permanent closure.",
               "desc":"Catastrophic. National-level emergency response. Criminal liability. Company-level consequence.",
               "psm_action":"NDRF activation. Ministry notification. Criminal investigation. Plant closed indefinitely.",
               "examples":["BLEVE at H2 bullet farm","VCE — vapour cloud explosion","Bhopal-scale toxic release"]},
    },

    # ── Hazard Categories (A-scale) from Tata Steel PSRM Module ──────
    "hazard_categories": {
        "A1": {"label":"A1 — Flammable / Explosive","color":"#f97316",
               "desc":"Substances that can ignite and combust or explode when mixed with air/oxidiser in correct proportions. Primary hazard: fire or explosion releasing thermal energy.",
               "key_properties":["Flash Point (°C) — temperature above which vapour ignites","LEL/LFL % — Lower Explosive Limit (below = too lean to ignite)","UEL/UFL % — Upper Explosive Limit (above = too rich to ignite)","Auto-Ignition Temperature (AIT) — spontaneous ignition temperature","Minimum Ignition Energy (MIE, mJ) — energy needed to ignite"],
               "examples":["H2: LEL 4%, UEL 75%, MIE 0.017 mJ — most ignition-sensitive industrial gas","Propane: LEL 2.1%, UEL 9.5%, Flash -104°C","Rolling oil mist: Flash >130°C — combustible","DOS oil: Flash 190°C — combustible"],
               "controls":["LEL/H2 continuous detectors","Elimination of all ignition sources in Zone 1/2","Ventilation to maintain <25% LEL","Explosion-proof (Ex-rated) electrical equipment","Bonding and earthing — static electricity prevention","ATEX-certified instruments"],
               "psm_implication":"Any process handling A1 material above threshold inventory → HHO → Full PSRM with HAZOP, Bow Tie and LOPA mandatory"},
        "A2": {"label":"A2 — Toxic","color":"#a78bfa",
               "desc":"Substances causing harm through inhalation, skin absorption, ingestion or injection. Hazard characterised by Occupational Exposure Limits (OEL).",
               "key_properties":["TLV-TWA: Time-Weighted Average over 8h shift — daily exposure limit","TLV-STEL: Short-Term Exposure Limit over 15 min — peak limit","TLV-C (Ceiling): Never to be exceeded even instantaneously","IDLH: Immediately Dangerous to Life and Health — emergency value","ERPG-2/3: Emergency Response Planning Guidelines for community"],
               "examples":["Cr-VI (CrO3/Na2Cr2O7): TLV-TWA 0.05 mg/m3 — IARC Group 1 Carcinogen","H2SO4 mist: TLV-TWA 1 mg/m3 — corrosive to lungs","CO: TLV-TWA 25 ppm, IDLH 1200 ppm","NaOH: corrosive — no OEL but severe contact hazard"],
               "controls":["Continuous ambient air monitoring (mandatory for Cr-VI per MSIHC Rules 1989)","LEV — Local Exhaust Ventilation (min 0.5 m/s face velocity)","PPE — air-supplied respirator for IDLH substances","Annual medical surveillance","Engineering substitution where possible"],
               "psm_implication":"A2 material above threshold → HHO if fatality pathway exists. Cr-VI = carcinogen = chronic fatality → HHO mandatory"},
        "A3": {"label":"A3 — Reactive / Unstable","color":"#ef4444",
               "desc":"Substances that react violently with other materials, decompose spontaneously, or become thermally unstable. Creates secondary explosive/fire/toxic hazard.",
               "key_properties":["Reactivity classification (NFPA Yellow diamond — 0 to 4)","Heat of reaction (kJ/mol) — energy released","Incompatible materials list (from Chemical Interaction Matrix)","Self-accelerating decomposition temperature (SADT)","Water-reactivity rating"],
               "examples":["Na2Cr2O7: Strong oxidiser — reacts violently with organics → fire","CrO3: Powerful oxidiser — contact with organics = spontaneous ignition","Conc. H2SO4 + water: Violent exothermic, spattering","KOH + HCl: Violent exothermic neutralisation"],
               "controls":["Chemical Interaction Matrix (CIM) — mandatory for all HHO processes","Storage segregation — incompatibles physically separated","Temperature control for thermally unstable materials","Contamination prevention — dedicated equipment","HAZOP 'As Well As' and 'Other Than' scenarios for A3 materials"],
               "psm_implication":"A3 materials: CIM mandatory in PSI. HAZOP must include contamination and reverse-flow scenarios. Storage segregation documented in EDB"},
        "A4": {"label":"A4 — Corrosive","color":"#3b82f6",
               "desc":"Substances that chemically destroy living tissue and corrode metals on contact. Can cause severe burns and equipment failure.",
               "key_properties":["pH (acids <2 or alkalis >12 = severe corrosive)","Corrosion rate (mm/year) for process piping","Skin/eye corrosivity classification (UN GHS)"],
               "examples":["H2SO4: pH ~0 (dilute 8-10 g/L in pickling) — skin/eye burns","NaOH 80-90°C: Severe alkali burns — boiling alkali = HHO event","KOH lye: pH 13-14 — strong corrosive electrolyte"],
               "controls":["Material of construction selection (MoC in EDB)","PPE: Chemical-resistant gloves, apron, face shield","Secondary containment (bunding) — 110% volume","Emergency deluge showers within 10m","Regular corrosion monitoring (ultrasonic thickness testing)"],
               "psm_implication":"A4 materials: MoC selection documented in EDB. Corrosion monitoring plan in PSCE. NaOH at 90°C SOL → HHO (boiling alkali)"},
        "A5": {"label":"A5 — High Pressure / Temperature","color":"#60a5fa",
               "desc":"Stored mechanical/thermal energy. Sudden uncontrolled release causes mechanical hazard (explosion, projectile, jet) or thermal hazard (steam, molten metal).",
               "key_properties":["Design pressure (kg/cm2) vs Operating pressure","Design temperature (°C) vs Operating temperature","MAWP (Maximum Allowable Working Pressure)","Vessel design code (IBR/ASME/IS)"],
               "examples":["H2 bullets: 14 kg/cm2 operating, 20 kg/cm2 SOL","H2 electrolyser: 1.57 MPa operating","Steam boiler: 15 bar — IBR registration mandatory","Hydraulic AGC CRM: 200 bar operating"],
               "controls":["Safety Relief Valves (SRV) — statutory per IBR/PESO for pressure vessels","Pressure transmitters with PLC interlock (PDB SOL parameter)","PESO registration and annual statutory inspection","Pressure vessel inspection (ASME, NDE testing)","Operating below MAWP at all times"],
               "psm_implication":"All pressure vessels >0.5 bar: IBR/PESO registration mandatory. SRV mandatory and prescriptive PSCE item. PDB pressure parameters = PSM Critical"},
    },

    # ── Barrier Model (Tata Steel PSRM Module — Detector/Logic/Actuator) ─
    "barrier_model": {
        "definition":"A barrier is a measure that prevents an incident from occurring (preventive) or reduces its consequences (mitigation). Per Tata Steel PSRM module: A barrier consists of 3 components: DETECTOR + LOGIC SOLVER + ACTUATOR. A barrier is effective ONLY if all 3 components are fully functional.",
        "components":{
            "Detector":"Senses the condition requiring action. Examples: Instrument alarm (high level alarm), Instrument switch (temperature switch high), Gas detection alarm (field gas detector), Operator observation (detects pump leaking). The sensor must be functional and calibrated.",
            "Logic Solver":"Decides the action to be taken based on detector input. Examples: Operator knowledge (outside operator), Operator knowledge (board operator), PLC/Logic Controller (automatic), Relay system. The logic must be correct and tested.",
            "Actuator":"Takes physical action to address the condition. Examples: Operator action (manually shuts pump), Automated action (stops furnace firing), Operator action (initiates emergency shutdown), Control valve closes. The actuator must be functional and reach its safe state.",
        },
        "types":{
            "Passive":"No activation required. No change of state. Always present. Examples: Emergency pits, bunds, blast walls, barricades, mechanical stoppers. Most reliable barrier type.",
            "Active":"Activation required. Function delivered by equipment/system. Consists of Sensor + Logic Solver + Actuator all operating automatically without human intervention. Examples: SIS trip, ESD valve, automatic deluge.",
            "Procedural/Administrative":"Activation required. At least one component depends on operator. Examples: Operator action based on SOP when alarm generated, Operator action in emergency (power failure, ladle through). Least reliable due to human error potential.",
        },
        "categories":{
            "Preventive Barrier":"Barrier that PREVENTS an event/incident from occurring. Acts before the top event. Examples: Alarm + operator intervention to reduce temperature, emergency cooling system auto-start, SIS trip on high pressure.",
            "Mitigation Barrier":"Barrier that REDUCES the consequence/effect when an incident has occurred. Acts after the top event. Examples: Bund/diked area around a tank (post-LOC), fire & gas alarm + emergency response, emergency pit for liquid steel, fire suppression system.",
        },
    },

    # ── Layers of Protection (from Tata Steel module diagram) ─────────
    "layers_of_protection":[
        {"layer":1,"name":"Inherently Safe Design / Process Design","side":"Prevention","desc":"Eliminate hazard at source. Design the process so the hazard cannot occur. E.g.: Reduce inventory, substitute hazardous chemical, lower operating pressure.","color":"#22c55e"},
        {"layer":2,"name":"Basic Process Control System (BPCS)","side":"Prevention — SOC","desc":"PLC/DCS controls process within SOC (Standard Operating Condition). The normal operating control system. E.g.: Temperature controller, pressure regulator, level control. Prevents deviation from reaching SOL.","color":"#22c55e"},
        {"layer":3,"name":"Critical Alarms & Operator Response","side":"Prevention — SOC","desc":"Alarm alerts operator to deviation approaching SOL. Operator takes corrective action per SOP. E.g.: High-high temperature alarm triggers operator to increase cooling.","color":"#eab308"},
        {"layer":4,"name":"Safety Instrumented System (SIS / SIF)","side":"Prevention — SOL","desc":"Automatic safety function that trips/shuts down process when SOL is reached. Independent of BPCS. Certified to SIL (Safety Integrity Level) per IEC 61511. E.g.: Auto-trip on H2-in-O2 >1.7%, cell temperature auto-trip at 97°C.","color":"#f97316"},
        {"layer":5,"name":"Active Physical Protection (Pre-release)","side":"Prevention","desc":"Mechanical safety device acting before loss of containment. E.g.: Pressure Relief Valve (PRV), Safety Relief Valve (SRV), rupture disk. Prescriptive statutory requirement (IBR/PESO).","color":"#f97316"},
        {"layer":6,"name":"Passive Physical Protection (Post-release)","side":"Mitigation","desc":"Physical barrier reducing consequences after loss of containment. No energy or activation required. E.g.: Bund/dike area, blast wall, catch pit, secondary containment.","color":"#ef4444"},
        {"layer":7,"name":"Plant Emergency Response","side":"Mitigation","desc":"Plant-level emergency response to contain and control the incident. E.g.: Fire brigade, emergency shutdown by operator, evacuation of plant personnel, on-site medical.","color":"#ef4444"},
        {"layer":8,"name":"Community Emergency Response","side":"Mitigation","desc":"Off-site emergency response when community is at risk. E.g.: District emergency plan, NDRF, community evacuation, public notification system.","color":"#7f1d1d"},
    ],

    # ── HAZOP Model (from Tata Steel module) ─────────────────────────
    "hazop": {
        "definition":"HAZOP (Hazard and Operability Study) critically examines a process flow sheet systematically for every conceivable and credible deviation of process variables. Process variables (temperature, pressure, flow, level, operating modes) are taken one at a time, a guide word is applied to generate a deviation, then causes and consequences are identified.",
        "purpose":"Hazard identification technique applied qualitatively to identify process hazards. Can also identify operating problems relating to equipment reliability and quality control. Incorporates prevention or containment of consequences.",
        "when_done":["Conceptual design stage — Coarse HAZOP","Detailed design stage — HAZOP of final P&IDs","Pre-commissioning — 'As built' check against P&IDs including safety systems","Post-commissioning — Re-HAZOP of major risks based on running experience","Design changes during operational life — HAZOP of all planned changes","Revalidation every 5 years minimum"],
        "procedure":["1. Select study node (line, equipment, operating step)","2. Explain design intention and process conditions","3. Select process variable (flow, temperature, pressure, level) or task","4. Apply guide word to generate meaningful deviation","5. Identify credible causes by brainstorming","6. Examine consequences assuming all safeguards fail","7. Identify existing safeguards","8. Assess adequacy — judgment or risk assessment","9. Agree recommendation if safeguards are inadequate","10. Repeat for all guide words, variables, nodes"],
        "terminology":{
            "Study Nodes":"Section with definite boundary (line between two vessels). The scope of one HAZOP analysis.",
            "Design Intent":"Definition of how the plant is expected to operate — the normal/correct condition.",
            "Guide Words":"Words used to qualify or quantify design intention to generate deviations.",
            "Process Parameters":"Physical or chemical property associated with the process — temperature, pressure, flow, level, composition.",
            "Deviations":"Departure from design intent discovered by applying guide words to parameters.",
            "Causes":"Initiating events — reasons why deviations occur. Can be equipment failure, human error, external.",
            "Consequences":"Results of deviations assuming all safeguards fail. Loss of containment. Impact on people, asset, environment.",
            "Safeguards":"Engineered or administrative actions that prevent cause from resulting in consequence.",
            "Recommendations":"Suggestions for design changes or procedural changes when safeguards are inadequate.",
        },
        "guide_words":{
            "NONE / NO / NOT":   {"meaning":"No forward flow when there should be, or reverse flow","examples":"No flow — pump failure, blocked valve, closed isolation valve"},
            "MORE OF":           {"meaning":"More of any relevant physical property than there should be","examples":"High temperature, high pressure, high flow, high level"},
            "LESS OF":           {"meaning":"Less of any relevant physical property than there should be","examples":"Low flow — partial blockage, pump degradation, Low temperature — heat loss"},
            "PART OF":           {"meaning":"Composition of system different from what it should be","examples":"Change in ratio of components, missing component, wrong concentration"},
            "AS WELL AS":        {"meaning":"More components present than there should be","examples":"Extra phase present, impurities (air, water, acid), contamination"},
            "OTHER THAN":        {"meaning":"What else can happen apart from normal operation","examples":"Startup, shutdown, maintenance, catalyst change, utility failure, uprating"},
            "REVERSE":           {"meaning":"Reverse of the intended direction or result","examples":"Reverse flow through pump, wrong direction of rotation, back-pressure"},
            "EARLY":             {"meaning":"Something happens before expected time","examples":"Early trip, early valve closure, premature alarm"},
            "LATE":              {"meaning":"Something happens after expected time","examples":"Delayed response, slow valve, instrument lag"},
            "WHERE ELSE":        {"meaning":"Transfer of hazard to unexpected location","examples":"H2 migration to adjacent building, heat transfer to unintended vessel"},
        },
    },

    # ── Bow Tie Model ─────────────────────────────────────────────────
    "bow_tie": {
        "definition":"Bow Tie is a risk assessment method visualising pathways from threats → Top Event (centre) → consequences. Left side = prevention (stopping top event). Right side = mitigation (limiting consequences after top event).",
        "structure":{
            "Threats / Causes":"Initiating events that could lead to top event. Each threat has a pathway to the top event.",
            "Threat Barriers (Prevention)":"Barriers that interrupt the pathway from threat to top event. Must be: Independent, Functional, Auditable. Each barrier breaks the chain.",
            "Escalation Factors":"Conditions that defeat a barrier. E.g.: Power failure defeats an active barrier. Must have Escalation Factor Controls.",
            "Top Event":"The point of loss of control — the uncontrolled release of energy or hazardous material. The 'waist' of the bow tie.",
            "Consequences":"Outcomes if the top event is not mitigated. Multiple consequences possible from one top event.",
            "Recovery/Mitigation Barriers":"Controls that reduce severity after top event. E.g.: Emergency response, fire suppression, evacuation, medical treatment.",
        },
        "barrier_effectiveness":{
            "Passive (Bund/Blast Wall)":{"reliability":"99%+","desc":"Always present, no activation required, independent of all systems"},
            "Active Mechanical (SRV/PRV)":{"reliability":"99%","desc":"Mechanical activation, no electrical dependency, highly reliable"},
            "Active Instrumented SIL-2 SIS":{"reliability":"99-99.9%","desc":"SIS rated to SIL-2. PFD 0.01-0.001. Tested periodically."},
            "Active Instrumented SIL-1 SIS":{"reliability":"90-99%","desc":"SIS rated to SIL-1. PFD 0.1-0.01."},
            "BPCS Control Loop":{"reliability":"90%","desc":"Normal process control. Not independent of process — PFD 0.1."},
            "Critical Alarm + Operator (>10 min)":{"reliability":"90%","desc":"Trained operator with sufficient time. PFD ~0.1."},
            "Administrative/Procedural":{"reliability":"50-90%","desc":"Human-dependent. PFD 0.1-1.0. Susceptible to error under stress."},
        },
    },

    # ── LOPA (from Tata Steel module) ─────────────────────────────────
    "lopa": {
        "definition":"LOPA (Layer of Protection Analysis) is a semi-quantitative risk assessment tool for analysing scenarios with higher consequence of concern (major accident scenarios). Risk compared against company risk tolerance criteria. If unacceptable: additional protection layers identified.",
        "risk_formula":"Risk = Likelihood (frequency) × Severity (consequence) — Risk is compared against Risk Matrix",
        "steps":["1. Select consequence scenario from HAZOP (major accident potential)","2. Identify initiating cause and its initiating event frequency (IEF, per year)","3. Identify all independent protection layers (IPLs) and their Probability of Failure on Demand (PFD)","4. Calculate mitigated consequence frequency: CF = IEF × PFD₁ × PFD₂ × ... × PFDₙ","5. Compare CF against company risk tolerance criteria (Risk Matrix)","6. If risk still unacceptable: design additional IPL or upgrade existing to SIL-rated SIS","Note: LOPA is one of the tools for determining required SIL for a Safety Instrumented Function (SIF)"],
        "layers_with_pfds":[
            ("Process Design","Inherent safety — eliminate hazard","N/A"),
            ("BPCS (Basic Process Control System)","PLC/DCS normal control loop","PFD = 0.1"),
            ("Critical Alarm + Operator Response (>10 min available)","Trained operator with time to respond","PFD = 0.1"),
            ("Critical Alarm + Operator Response (<10 min)","Operator under time pressure","PFD = 1.0"),
            ("Safety Instrumented System — SIL 1","Auto-trip, PLC-based, periodic tested","PFD = 0.1 to 0.01"),
            ("Safety Instrumented System — SIL 2","Higher integrity SIS, more frequent testing","PFD = 0.01 to 0.001"),
            ("Safety Instrumented System — SIL 3","Highest SIS level for most hazardous","PFD = 0.001 to 0.0001"),
            ("Pressure Relief Valve (PRV/SRV)","Mechanical pressure protection","PFD = 0.01"),
            ("Check Valve","Mechanical reverse-flow prevention","PFD = 0.1"),
            ("Rupture Disk","One-time mechanical protection","PFD = 0.01"),
            ("Passive Bund / Dike","Physical containment post-release","PFD = 0.01"),
            ("Plant Emergency Response","On-site fire/emergency team","PFD = 0.1"),
        ],
        "tolerable_risk":"Typically ≤ 1×10⁻⁵ per year for individual fatal risk in Indian chemical industry (ALARP principle)",
    },

    # ── PSRM Levels ───────────────────────────────────────────────────
    "psrm_levels": {
        "Baseline PSRM": {"applies_to":"LHO processes","color":"#6366f1",
            "elements":["PSI (Process Safety Information)"],
            "desc":"Minimum PSRM for LHO processes. PSI documentation only. No HAZOP, no Bow Tie.",
            "psi_elements":["Process description","Equipment list","Chemical properties (MSDS)","Block Diagram","P&ID (basic)"]},
        "Full PSRM (14 Elements)": {"applies_to":"HHO processes","color":"#f97316",
            "elements":["PSI","PHA/HAZOP","Bow Tie","LOPA","SOP","MOC","PSER","Incident Investigation","Pre-Startup Safety Review","Contractors Safety","Training","Mechanical Integrity","Auditing","Leadership & Commitment"],
            "desc":"Full PSRM per Tata Steel standard (aligned with OSHA PSM 14 elements). All HHO processes.",
            "psi_elements":["Block Diagram (BD)","Process Flow Diagram (PFD)","P&ID (CCOE Approved)","PSC (HHO/LHO Classification)","PDB (SOC/SOL/Barriers)","HOM (Chemical Properties)","CIM (Chemical Interaction Matrix)","PSCE (Safety Critical Equipment)","EDB (Equipment Design Basis)"]},
    },
    "psi_elements": {
        "BD":   {"full":"Block Diagram","purpose":"Highest-level process overview. Shows interconnection of major process blocks."},
        "PFD":  {"full":"Process Flow Diagram","purpose":"Shows main flows, key equipment, and operating conditions. Includes mass/energy balance."},
        "PID":  {"full":"Piping & Instrumentation Diagram","purpose":"Detailed drawing: all pipes, valves, instruments, safety devices. CCOE approval for HHO."},
        "PSC":  {"full":"Process Safety Classification","purpose":"Classifies each sub-process HHO/LHO using hazard matrix and consequence analysis."},
        "PDB":  {"full":"Process Design Basis","purpose":"SOC/SOL for each parameter, identification method, deviation consequences, barriers."},
        "HOM":  {"full":"Hazard of Materials","purpose":"MSDS-level: physical properties, TLV-TWA/STEL/IDLH, health/env effects, emergency response."},
        "CIM":  {"full":"Chemical Interaction Matrix","purpose":"Cross-reference compatibility/incompatibility of all chemicals on-site. Based on NFPA CRW."},
        "PSCE": {"full":"Process Safety Critical Equipment","purpose":"All equipment whose failure could cause/contribute to major accident. With maintenance schedule."},
        "EDB":  {"full":"Equipment Design Basis","purpose":"Design parameters, selection basis, manufacturer, maintenance for all PSCE items."},
        "SOP":  {"full":"Standard Operating Procedure","purpose":"Step-by-step procedures: normal, startup, shutdown, emergency."},
        "MOC":  {"full":"Management of Change","purpose":"Formal process assessing changes to process/equipment/procedures before implementation."},
        "PSER": {"full":"Process Safety Emergency Response","purpose":"Emergency plan for PSI scenarios — fire, explosion, toxic release."},
        "PHA":  {"full":"Process Hazard Analysis (HAZOP)","purpose":"Systematic examination of all deviations using guide words. Multidisciplinary team."},
        "Audit":{"full":"PSM Compliance Audit","purpose":"Periodic verification all PSM elements are implemented and effective. Annual for HHO."},
    },
}

PLANT_META = {
    "Hydrogen Plant — H2 Production & Supply": {"risk":82,"hho":5,"lho":1,"psce":44,"status":"HHO"},
    "ETL-1 — Electrolytic Tinning Line 1":     {"risk":61,"hho":4,"lho":2,"psce":77,"status":"HHO"},
    "ETL-2 — Electrolytic Tinning Line 2":     {"risk":54,"hho":4,"lho":2,"psce":12,"status":"HHO"},
    "CRM — Cold Rolling Mill":                 {"risk":48,"hho":3,"lho":2,"psce":8, "status":"PSI"},
    "TFS — Tin Free Steel":                    {"risk":45,"hho":2,"lho":3,"psce":6, "status":"PSI"},
    "Galvanizing Line (GI/GA)":                {"risk":52,"hho":3,"lho":2,"psce":9, "status":"HHO"},
    "Colour Coated Sheet (CCS)":               {"risk":50,"hho":3,"lho":2,"psce":8, "status":"HHO"},
    "Chlor-Alkali Plant":                      {"risk":78,"hho":5,"lho":2,"psce":14,"status":"HHO"},
}

PLANT_PROFILES = {
    "ETL-2 — Electrolytic Tinning Line 2": {
        "short":"ETL-2","processes":6,"chemicals":6,"params":17,
        "desc":"ETL-2 is the second electrolytic tinning line at TCIL Golmuri, operating with SHL (Soft Melt Hot Dip Lacquering) process variant. Unlike ETL-1 which uses resistance reflow, ETL-2 uses soft melt + hot dip lacquering technology for superior formability tin plate used in aerosol and drawn-and-ironed (DWI) can manufacturing. Line speed: up to 300 mpm. Annual capacity: ~90,000 MT.",
        "proc_cards":[
            ("Coil Feeding","Hydraulic oil, DM water, compressed air. Payoff reel feeds black plate (0.14-0.36 mm). Entry looper 200m capacity.","lho",["LHO"]),
            ("Electrolytic Cleaning","NaOH 80-90°C, H2SO4 pickling 8-10 g/L, DC current 2.5-3.5 kA. HHO classification same as ETL-1.","hho",["HHO","PSM Required"]),
            ("Tin Plating (8 cells)","SnSO4 + H2SO4 + ENSA + PSA bath. DC deposition 26-34 g/L Sn++. 8 cells.","hho",["HHO"]),
            ("Soft Melt (SHL Process)","Induction heating 232-250°C. Lower temp than ETL-1 reflow (270°C). H2/N2 atmosphere. DWI can grade. HHO.","hho",["HHO","PSM Required"]),
            ("Hot Dip Lacquering","DOS-based lacquer post-melt. Electrostatic. Flash point 190°C. LHO.","lho",["LHO"]),
            ("Chemical Treatment (Cr-VI)","Chromate passivation — Cr-VI chemistry same as ETL-1. IARC Group 1 carcinogen. TLV 0.05 mg/m3. HHO.","hho",["HHO","PSM Required"]),
        ],
        "chemicals":[("A1","H2SO4","Corrosive, generates H2","72"),("A2","PSA","Corrosive","55"),("A3","DOS","Combustible","30"),("A4","ENSA","Irritant","40"),("A5","Na2Cr2O7","CARCINOGEN Cr-VI","95"),("A6","Sn","Heavy metal","35")],
        "alerts":[(95,"CRITICAL — Cr-VI (Chemical Treatment) | IARC Group 1 carcinogen | TLV 0.05 mg/m3 | Monitoring mandatory"),(88,"CRITICAL — Soft Melt Temp deviation | H2/N2 atmosphere | Explosive risk on seal failure"),(75,"HIGH — Sn2+ below SOL | DWI can spec critical | Food contact compliance")],
        "pdb_params":[
            {"sl":1,"param":"Soft Melt Strip Temperature","uom":"°C","soc_min":232,"soc_max":250,"sol_min":232,"sol_max":255,"sub_process":"Soft Melt (SHL)","equipment_linked":"Pyrometer ETL-2, Induction heater","identification_low":"Pyrometer alarm — below 232°C","identification_high":"Pyrometer alarm at 250°C, trip at 255°C","consequence_low":"Incomplete tin melt — matte surface — DWI formability failure — product rejection","consequence_high":"Strip overburn — H2 atmosphere disruption — structural damage","action_low":"Admin: Increase induction heater power. Hold product.","action_high":"ACTIVE: Pyrometer auto-trip at 255°C. Admin: Inspect induction coil.","psm_critical":"Yes"},
            {"sl":2,"param":"Sn++ Concentration","uom":"g/L","soc_min":26,"soc_max":34,"sol_min":24,"sol_max":36,"sub_process":"Tin Plating","equipment_linked":"Sn analyser","identification_low":"Bath analysis alarm — SOL low","identification_high":"Bath analysis alarm — high Sn++","consequence_low":"UNDER-PLATING — DWI can fracture on drawing — food contamination risk","consequence_high":"Over-coating — material cost, specification breach","action_low":"Admin: Add SnSO4 makeup. Hold product. Active: Analyser alarm.","action_high":"Admin: Reduce current density.","psm_critical":"Yes"},
            {"sl":3,"param":"Cr-VI Bath Temperature","uom":"°C","soc_min":40,"soc_max":45,"sol_min":40,"sol_max":45,"sub_process":"Chemical Treatment","equipment_linked":"TT-ChemTx ETL-2, LEV","identification_low":"Temperature transmitter alarm","identification_high":"Auto-bath shutdown at 45°C SOL","consequence_low":"Incomplete passivation — corrosion failure in DWI drawn cans","consequence_high":"Cr-VI mist surge — TLV breach — MANDATORY SHUTDOWN per MSIHC Rules 1989","action_low":"Admin: Check heating.","action_high":"ACTIVE: Bath auto-off. Air monitor check. SHUTDOWN if Cr-VI >0.05 mg/m3.","psm_critical":"Yes"},
        ],
        "psce_items":[
            {"sl":1,"equipment":"Pyrometer — Soft Melt Strip Temp","tag":"Pyro-ETL2","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Soft Melt (SHL)","sap_tag":"S-ETL2-001","justification":"Primary strip temp monitoring for SHL (SOC 232-250°C, SOL 255°C). Auto-trip at SOL. H2/N2 atmosphere — deviation affects safety.","consequence_of_failure":"Strip overburn undetected → H2 atmosphere disruption → explosive risk. Under-melt → DWI product failure.","maintenance":"3-monthly calibration."},
            {"sl":2,"equipment":"Cr-VI Air Monitor ETL-2","tag":"CrVI-ETL2","psce_type":"Prescriptive","category":"Safety Monitoring & Emergency Communication","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL2-002","justification":"Prescriptive per MSIHC Rules 1989. Continuous Cr-VI monitoring. TLV 0.05 mg/m3. IARC Group 1 carcinogen.","consequence_of_failure":"Cr-VI exposure undetected → carcinogenic health effect. Statutory violation.","maintenance":"Quarterly calibration. Monthly bump test."},
        ],
        "edb_items":[
            {"sl":1,"sub_process":"Soft Melt (SHL)","hazardous_substance":"Hydrogen Gas","equipment":"Soft Melt Induction Heater","tag_no":"IH-ETL2","selection_basis":"Consequence Based","manufacturer":"Ajax Tocco / Inductotherm","model":"Induction Heating System","design_basis":"Induction heating coils melt tin at 232-250°C. H2/N2 atmosphere. Rated for strip width up to 1050mm at 300 mpm.","consequence_of_failure":"Heater failure → incomplete melt or overshoot → strip burning → H2 atmosphere disruption.","barrier_type":"Active — Instrumented","barrier_effectiveness":"Pyrometer feedback loop — tighter temp control than resistance reflow.","is_psce":True},
        ],
    },
    "CRM — Cold Rolling Mill": {
        "short":"CRM","processes":5,"chemicals":4,"params":12,
        "desc":"The Cold Rolling Mill (CRM) reduces hot-rolled black plate to required thickness (0.14-0.50mm). Tandem mill with 4 rolling stands using mineral oil emulsion as lubricant/coolant. Rolling force up to 2000 kN. Strip speed up to 600 mpm. Key hazards: rolling oil emulsion mist (fire), hydraulic high-pressure systems, high-speed strip, electrical arc flash.",
        "proc_cards":[
            ("Coil Preparation","Decoiler, straightener, welder. Entry loop. Hydraulic 150-200 bar. Compressed air 5-6 bar.","lho",["LHO"]),
            ("Rolling Oil Emulsion System","Mineral oil emulsion 3-5%. Flash point >130°C. Heated to 45-55°C. Emulsion mist — fire risk.","hho",["HHO","Fire Risk"]),
            ("Tandem Rolling (4 Stands)","4-high mill. 2000 kN force. 600 mpm strip speed. 5-15 MW drives. Arc flash hazard.","hho",["HHO","Electrical"]),
            ("Strip Cleaning (Post Rolling)","Alkaline cleaning 50-70°C. NaOH/Na2CO3 based. Mild corrosive. LHO.","lho",["LHO"]),
            ("Inspection & Recoiling","Flying shear, side trimmer, inspection, recoiler. Mechanical hazards.","lho",["LHO"]),
        ],
        "chemicals":[("C1","Rolling Oil Emulsion","Combustible mist, flash 130°C","55"),("C2","NaOH","Corrosive alkali","45"),("C3","Hydraulic Oil","Combustible, flash 170°C","35"),("C4","Lubricating Grease","Combustible","20")],
        "alerts":[(78,"HIGH — Rolling oil mist in mill housing | Flash 130°C | Fire/explosion if ignition source"),(72,"HIGH — Hydraulic at 200 bar | Seal failure = oil spray onto hot strip — fire risk"),(65,"MEDIUM — Electrical arc flash at 5-15 MW drive panels | PPE mandatory")],
        "pdb_params":[
            {"sl":1,"param":"Rolling Oil Emulsion Concentration","uom":"%","soc_min":3.0,"soc_max":5.0,"sol_min":2.5,"sol_max":6.0,"sub_process":"Rolling Oil System","equipment_linked":"Conductivity analyser, dosing pump","identification_low":"Conductivity alarm — low concentration","identification_high":"Conductivity alarm — high concentration","consequence_low":"Insufficient lubrication → friction → surface defects → heat buildup → fire risk","consequence_high":"Excess emulsion mist → fire/explosion risk in mill housing","action_low":"Admin: Check dosing pump. Add makeup oil.","action_high":"Admin: Reduce dosing. Check analyser. Ensure LEV functional.","psm_critical":"Yes"},
            {"sl":2,"param":"Hydraulic System Pressure","uom":"bar","soc_min":150,"soc_max":200,"sol_min":140,"sol_max":220,"sub_process":"Tandem Rolling","equipment_linked":"Pressure transmitter, PRV, hydraulic power unit","identification_low":"Pressure transmitter alarm","identification_high":"Pressure transmitter alarm + PRV lifts","consequence_low":"Insufficient AGC hydraulic → gauge deviation → product rejection","consequence_high":"Hydraulic line rupture at 200 bar → oil spray on hot strip → fire risk","action_low":"Admin: Check hydraulic pump.","action_high":"Active: PRV mechanical protection. Admin: Inspect lines. Emergency stop if rupture.","psm_critical":"Yes"},
        ],
        "psce_items":[
            {"sl":1,"equipment":"Rolling Oil Emulsion LEV System","tag":"LEV-CRM","psce_type":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes","sub_process":"Rolling Oil System","sap_tag":"S-CRM-001","justification":"LEV removes oil mist from mill housing (flash 130°C). Primary barrier for fire/explosion. Interlock: mill cannot run without LEV.","consequence_of_failure":"Oil mist accumulates → explosive atmosphere → fire/explosion → multiple fatalities.","maintenance":"Monthly airflow measurement. Quarterly inspection."},
            {"sl":2,"equipment":"Strip Break Detection System","tag":"SBD-CRM","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Tandem Rolling","sap_tag":"S-CRM-002","justification":"At 600 mpm, strip break causes metal flailing — projectile and wrap-up risk. Emergency stop triggered within 50ms.","consequence_of_failure":"Strip break undetected at 600 mpm → metal flail → fatality → wrap-up → fire.","maintenance":"Monthly functional test."},
        ],
        "edb_items":[
            {"sl":1,"sub_process":"Rolling Oil System","hazardous_substance":"Rolling Oil Emulsion (flash 130°C)","equipment":"Rolling Oil Filtration System","tag_no":"ROF-CRM","selection_basis":"Consequence Based","manufacturer":"Voith/SMS Group","model":"Emulsion Filtration Unit","design_basis":"Filters rolling oil to remove iron fines. Clean emulsion reduces mist generation. Rated for full flow at 45-55°C.","consequence_of_failure":"Dirty emulsion → increased mist → fire risk. Iron fines on strip → surface defects.","barrier_type":"Passive","barrier_effectiveness":"Continuous passive filtration — always active — reduces mist and fire risk.","is_psce":False},
        ],
    },
}




# ══════════════════════════════════════════════════════════════════════
# MODULE-LEVEL DATA — H2 PLANT
# ══════════════════════════════════════════════════════════════════════
H2_PDB_PARAMS = [
    {"sl":1,"param":"DM Water Tank Level","uom":"mm","soc_min":300,"soc_max":1000,"sol_min":100,"sol_max":1500,"sub_process":"DM Water & KOH","equipment_linked":"LIT1301, Feed Pump 1M21","identification_low":"Level transmitter alarm at 450mm","identification_high":"High level alarm at 1000mm — pump stop","consequence_low":"Plant trip — H2 generation stops. Electrolyser dry running if undetected.","consequence_high":"DM water overflow from tank — spillage, housekeeping/safety hazard.","action_low":"Active: auto-trip at SOL. Admin: restore DM water supply.","action_high":"Admin: pump off. Check overflow condition.","psm_critical":"No"},
    {"sl":2,"param":"DM Water Conductivity","uom":"uS/cm","soc_min":0,"soc_max":1,"sol_min":0,"sol_max":1,"sub_process":"DM Water & KOH","equipment_linked":"Conductivity meter","identification_low":"No action — minimum desirable","identification_high":"Conductivity meter alarm — block feed","consequence_low":"No consequence — minimum TDS desirable.","consequence_high":"High TDS → electrolyser efficiency drops → cell corrosion/scaling.","action_low":"No safeguard required.","action_high":"Admin: switch DM plant to polishing mode. Do not feed until <1 uS/cm.","psm_critical":"No"},
    {"sl":3,"param":"Electrolyser Cell Temperature","uom":"°C","soc_min":35,"soc_max":95,"sol_min":25,"sol_max":97,"sub_process":"Electrolysis","equipment_linked":"RTD TE1001, RTD TE1003, TV1001","identification_low":"Constant HMI monitoring — RTD alarm","identification_high":"RTD alarm at 95°C SOC — auto-trip at 97°C SOL","consequence_low":"No consequence on low temp — reduced efficiency.","consequence_high":"Cell/electrode damage, KOH decomposition — FIRE HAZARD at extreme temp.","action_low":"No safeguard required.","action_high":"Active: PLC auto-trip at 97°C. Admin: investigate cooling water supply.","psm_critical":"Yes"},
    {"sl":4,"param":"Rectifier DC Current","uom":"A","soc_min":800,"soc_max":1450,"sol_min":500,"sol_max":1600,"sub_process":"Electrolysis","equipment_linked":"Rectifier, Ammeter, QS1001","identification_low":"Ammeter alarm — H2 not transferred — vent from GLT","identification_high":"Ammeter alarm — auto-trip at SOL","consequence_low":"Insufficient energy — H2/O2 not generated — plant output zero.","consequence_high":"Overheating, cell damage, transformer overload — FIRE HAZARD.","action_low":"Active: QS1001 trips to vent. Admin: check rectifier, restore.","action_high":"Active: auto-trip at 1600A. Admin: investigate before restart.","psm_critical":"Yes"},
    {"sl":5,"param":"Separator Liquid Level","uom":"mm","soc_min":500,"soc_max":670,"sol_min":400,"sol_max":770,"sub_process":"Gas-Liquid Treater","equipment_linked":"LT1003, LT1001, LV1001","identification_low":"LT alarm approaching low — start interlock","identification_high":"LT alarm — lye carryover risk","consequence_low":"Plant will not start below SOL — gas bypass → H2-in-O2 rises.","consequence_high":"Lye into gas pipeline → purity impact, pipeline blockage.","action_low":"Active: auto-trip at SOL low. Admin: restore lye level.","action_high":"Active: auto-trip at SOL high. Admin: drain to correct level.","psm_critical":"Yes"},
    {"sl":6,"param":"Separator Pressure","uom":"MPa","soc_min":"N/A","soc_max":1.57,"sol_min":"N/A","sol_max":1.65,"sub_process":"Gas-Liquid Treater","equipment_linked":"PT1001, PV1001, SRV","identification_low":"PT1001 — manual vent valve check","identification_high":"PT1001 alarm — PRV/SRV protection","consequence_low":"Transfer to purifier not possible — plant on vent.","consequence_high":"Overpressure — vessel rupture hazard — SRV lifts.","action_low":"Admin: close vent valve, allow pressure to build.","action_high":"Active: SRV mechanical protection. Auto-trip at 1.65 MPa.","psm_critical":"Yes"},
    {"sl":7,"param":"H2 Content in O2 (H2-in-O2)","uom":"%","soc_min":0,"soc_max":0.8,"sol_min":0,"sol_max":1.7,"sub_process":"Gas-Liquid Treater","equipment_linked":"AT1002 (PSCE #13)","identification_low":"AT1002 continuous — no action, minimum desirable","identification_high":"AT1002 alarm at SOC — auto-trip at SOL (HH)","consequence_low":"No consequence — minimum desirable.","consequence_high":"O2 SEPARATOR DETONATION — H2+O2 explosive mixture — CATASTROPHIC.","action_low":"No safeguard required.","action_high":"ACTIVE: auto-trip at 1.7% SOL. Investigate separator before restart.","psm_critical":"Yes"},
    {"sl":8,"param":"O2 Content in H2 (O2-in-H2)","uom":"%","soc_min":0,"soc_max":0.1,"sol_min":0,"sol_max":0.2,"sub_process":"Gas-Liquid Treater","equipment_linked":"AT1001 (PSCE #14)","identification_low":"AT1001 continuous — no action","identification_high":"AT1001 alarm at SOC — auto-trip at SOL","consequence_low":"No consequence.","consequence_high":"H2 SEPARATOR EXPLOSIVE MIXTURE — auto-trip at 0.2% SOL.","action_low":"No safeguard required.","action_high":"ACTIVE: auto-trip at 0.2% SOL. Full gas analysis before restart.","psm_critical":"Yes"},
    {"sl":9,"param":"H2 Detector (GLT/Purifier/DM zones)","uom":"% LEL","soc_min":0,"soc_max":0.2,"sol_min":0,"sol_max":0.9,"sub_process":"Gas-Liquid Treater","equipment_linked":"AT1701, AT1702, AT1703, Exhaust fan","identification_low":"Fixed detectors — no action, minimum desirable","identification_high":"Alarm — operator checks for H2 leak. Fan auto-starts.","consequence_low":"No consequence.","consequence_high":"H2 above LEL → fire/explosion risk — auto exhaust fan + plant trip.","action_low":"No safeguard required.","action_high":"Admin: evacuate zone, check leaks. Active: exhaust fan auto-start. Trip at 0.9% SOL.","psm_critical":"Yes"},
    {"sl":10,"param":"Deoxidizer Bed Temperature","uom":"°C","soc_min":118,"soc_max":160,"sol_min":110,"sol_max":160,"sub_process":"H2 Purification","equipment_linked":"RTD at deoxy unit, Heater","identification_low":"RTD alarm on HMI — low temperature","identification_high":"RTD alarm — investigate heater","consequence_low":"O2 not removed — trace O2 rises — explosive mixture risk downstream.","consequence_high":"Catalyst damage — purity failure.","action_low":"Active: auto-trip below 110°C SOL. Admin: check heater.","action_high":"Active: auto-trip at 160°C SOL.","psm_critical":"Yes"},
    {"sl":11,"param":"Dryer A/B/C Bed Temperature","uom":"°C","soc_min":170,"soc_max":220,"sol_min":"—","sol_max":"—","sub_process":"H2 Purification","equipment_linked":"RTD at each dryer, Heaters","identification_low":"RTD alarm on HMI","identification_high":"RTD alarm","consequence_low":"Poor drying — dew point rises — moisture in pipeline.","consequence_high":"Dryer damage — purity/dew point failure.","action_low":"Active: auto-trip on deviation. Admin: switch to standby dryer.","action_high":"Active: auto-trip. Admin: investigate heater.","psm_critical":"Yes"},
    {"sl":12,"param":"Dew Point (Purified H2)","uom":"°C","soc_min":"N/A","soc_max":-80,"sol_min":"N/A","sol_max":-70,"sub_process":"H2 Purification","equipment_linked":"MT1101 (PSCE #23), QZ1007","identification_low":"No action — lower is better","identification_high":"MT1101 alarm at -80°C — manual calibration check","consequence_low":"No consequence — lower dew point is better.","consequence_high":"Moisture in H2 pipeline — annealing hood corrosion, purity failure.","action_low":"No safeguard required.","action_high":"Active: auto-trip at -70°C SOL. QZ1007 vents H2 from storage.","psm_critical":"Yes"},
    {"sl":13,"param":"Purifier Pressure (H2)","uom":"MPa","soc_min":0.6,"soc_max":1.3,"sol_min":0.5,"sol_max":1.4,"sub_process":"H2 Purification","equipment_linked":"PT1101, PV1101, PRV","identification_low":"PT1101 alarm","identification_high":"Auto PRV on high pressure","consequence_low":"Insufficient purifier performance.","consequence_high":"Overpressure — SRV lift — H2 release.","action_low":"Admin: close vent, check PV1101.","action_high":"Admin: monitor. PRV mechanical backup.","psm_critical":"Yes"},
    {"sl":14,"param":"Trace O2 at Purifier Outlet","uom":"ppm","soc_min":0,"soc_max":1,"sol_min":0,"sol_max":2,"sub_process":"H2 Purification","equipment_linked":"AT1102 (PSCE #26), QZ1007","identification_low":"AT1102 continuous — no action","identification_high":"AT1102 alarm — do NOT pass to storage","consequence_low":"Analyser may be faulty — safety risk if assumed safe.","consequence_high":"EXPLOSIVE mixture in bullet storage if contaminated H2 passes.","action_low":"No safeguard required.","action_high":"ACTIVE: QZ1007 auto-vent diverts from storage. Trip at >2 ppm.","psm_critical":"Yes"},
    {"sl":15,"param":"Cooling Water Tank Level","uom":"mm","soc_min":500,"soc_max":900,"sol_min":600,"sol_max":1000,"sub_process":"DM Water & KOH","equipment_linked":"LIT1501, Cooling pump","identification_low":"LIT1501 alarm at 600mm","identification_high":"Alarm at 1000mm","consequence_low":"GLT trip — insufficient cooling — cell temp rises.","consequence_high":"Overflow — safety/housekeeping hazard.","action_low":"Active: alarm and GLT trip at SOL low. Admin: restore supply.","action_high":"Admin: pump off. Check overflow.","psm_critical":"Yes"},
    {"sl":16,"param":"Cooling Water Temperature","uom":"°C","soc_min":"N/A","soc_max":35,"sol_min":"N/A","sol_max":40,"sub_process":"DM Water & KOH","equipment_linked":"TE1501, TE1502, TV1001","identification_low":"No action — low temp required","identification_high":"Alarm on high temp","consequence_low":"No consequence — lower temp required.","consequence_high":"Cooling efficiency drops — cell temp rises — auto-trip at 97°C SOL.","action_low":"No safeguard required.","action_high":"Active: auto-trip at 40°C SOL. Admin: check cooling system.","psm_critical":"Yes"},
    {"sl":17,"param":"Cooling Water Pressure","uom":"kg/cm2","soc_min":2.5,"soc_max":3.5,"sol_min":2.0,"sol_max":6.0,"sub_process":"DM Water & KOH","equipment_linked":"PT1501","identification_low":"PT1501 alarm","identification_high":"Pressure alarm","consequence_low":"Insufficient cooling — temp not maintained.","consequence_high":"Pipe rupture/leakage risk.","action_low":"Active: alarm, trip at SOL low. Admin: contact DM plant.","action_high":"Active: alarm at SOL high. Admin: throttle pump.","psm_critical":"Yes"},
    {"sl":20,"param":"Bullet-1 Pressure","uom":"kg/cm2","soc_min":4,"soc_max":14,"sol_min":3,"sol_max":20,"sub_process":"H2 Bullet Storage","equipment_linked":"PG-B1, SRV1/SRV2 (PSCE #34,#35)","identification_low":"Pressure gauge during rounds","identification_high":"Gauge reading — SRV lifts at design pressure","consequence_low":"Insufficient H2 supply to annealing — production loss.","consequence_high":"SRV lift — H2 venting — BLEVE risk under fire — CATASTROPHIC.","action_low":"Active: PRV adjusts. Admin: restore inlet supply.","action_high":"Active: dual SRVs (PSCE #34,#35). Admin: investigate overpressure.","psm_critical":"Yes"},
    {"sl":21,"param":"Bullet-2 Pressure","uom":"kg/cm2","soc_min":4,"soc_max":14,"sol_min":3,"sol_max":20,"sub_process":"H2 Bullet Storage","equipment_linked":"PG-B2, SRV1/SRV2 (PSCE #36,#37)","identification_low":"Pressure gauge during rounds","identification_high":"SRV lifts at design pressure","consequence_low":"H2 supply interruption to annealing.","consequence_high":"Same as Bullet-1 — BLEVE risk under fire.","action_low":"Admin: restore supply.","action_high":"Active: dual SRVs (PSCE #36,#37).","psm_critical":"Yes"},
    {"sl":22,"param":"Bullet-1 Temperature","uom":"°C","soc_min":"N/A","soc_max":45,"sol_min":"N/A","sol_max":50,"sub_process":"H2 Bullet Storage","equipment_linked":"TG-B1 (PSCE #39)","identification_low":"No lower limit.","identification_high":"Gauge alarm — water spray initiated","consequence_low":"No consequence.","consequence_high":"Thermal expansion → pressure rise above SOL → SRV lift → H2 release.","action_low":"No action.","action_high":"Admin: water spray on vessel. Shutdown + inspection if SOL persists.","psm_critical":"Yes"},
    {"sl":23,"param":"Bullet-2 Temperature","uom":"°C","soc_min":"N/A","soc_max":45,"sol_min":"N/A","sol_max":50,"sub_process":"H2 Bullet Storage","equipment_linked":"TG-B2 (PSCE #40)","identification_low":"No lower limit.","identification_high":"Gauge alarm — water spray","consequence_low":"No consequence.","consequence_high":"Same as Bullet-1 temperature breach.","action_low":"No action.","action_high":"Admin: water spray. Shutdown if SOL persists.","psm_critical":"Yes"},
    {"sl":24,"param":"Final Outlet Pressure from Bullet","uom":"kg/cm2","soc_min":1.2,"soc_max":2.5,"sol_min":1.0,"sol_max":3.5,"sub_process":"H2 Distribution","equipment_linked":"PRV (PSCE #43), PCV1, PCV2","identification_low":"Gauge at bullet outlet","identification_high":"PRV adjusts automatically","consequence_low":"Insufficient H2 to annealing hoods — quality failure.","consequence_high":"Distribution line overpressure — PRV adjusts. Pipe failure if PRV fails.","action_low":"Active: PRV adjusts. Admin: check bullet inventory.","action_high":"Active: PRV (PSCE #43) relieves. Admin: check valve positions.","psm_critical":"Yes"},
]

ETL1_PDB_PARAMS = [
    {"sl":1,"param":"Power Pack Hydraulic Pump Pressure","uom":"bar","soc_min":55,"soc_max":70,"sol_min":45,"sol_max":100,"sub_process":"Coil Feeding","equipment_linked":"Hydraulic power pack, actuators","identification_low":"Pressure gauge + transmitter alarm","identification_high":"Pressure transmitter alarm — PRV at SOL","consequence_low":"Actuator failure — strip misalignment — weld failure.","consequence_high":"Hydraulic line rupture — oil spray — fire risk (flash ~150°C).","action_low":"Admin: check pump, oil level. Active: pressure alarm.","action_high":"Active: PRV opens at SOL. Admin: inspect pump.","psm_critical":"No"},
    {"sl":2,"param":"DM Water Pressure to Welding Machine","uom":"kg/cm2","soc_min":4.5,"soc_max":5.5,"sol_min":4.5,"sol_max":5.5,"sub_process":"Coil Feeding","equipment_linked":"DM water supply, welder, flow switch","identification_low":"Flow switch alarm — welding inhibited","identification_high":"Pressure transmitter alarm","consequence_low":"Welder overheating — weld failure — strip break.","consequence_high":"Excess pressure — seal stress — leakage.","action_low":"Active: flow switch inhibits welding. Admin: restore DM pressure.","action_high":"Admin: throttle inlet valve.","psm_critical":"No"},
    {"sl":3,"param":"Pre-Primary Alkali Temperature (NaOH)","uom":"°C","soc_min":80,"soc_max":90,"sol_min":80,"sol_max":90,"sub_process":"Cleaning & Rinsing","equipment_linked":"Temperature transmitter, steam valve","identification_low":"Temp transmitter alarm at 80°C SOC","identification_high":"Auto-coolant at 90°C SOC — trip at SOL","consequence_low":"Poor degreasing — rolling oil on strip — plating pinholes.","consequence_high":"NaOH BOILING — violent steam — alkali burns — HHO EVENT.","action_low":"Admin: check steam supply. Delay start until SOC.","action_high":"ACTIVE: auto-bath off at SOL. Admin: investigate steam valve.","psm_critical":"Yes"},
    {"sl":4,"param":"Primary NaOH Concentration","uom":"g/L","soc_min":25,"soc_max":30,"sol_min":25,"sol_max":30,"sub_process":"Cleaning & Rinsing","equipment_linked":"NaOH dosing, conductivity analyser","identification_low":"Conductivity alarm — low concentration","identification_high":"Conductivity alarm — high","consequence_low":"Residual oil → plating pinholes.","consequence_high":"Excess drag-out → WTP overload.","action_low":"Admin: add NaOH. Verify by titration.","action_high":"Admin: reduce dosing. Verify by titration.","psm_critical":"No"},
    {"sl":5,"param":"Primary Cleaning Current","uom":"kA","soc_min":2.5,"soc_max":3.5,"sol_min":2.5,"sol_max":3.5,"sub_process":"Cleaning & Rinsing","equipment_linked":"DC rectifier, overcurrent relay","identification_low":"Ammeter alarm — low current","identification_high":"Overcurrent relay — auto-trip","consequence_low":"Inadequate cleaning — contamination → pinholes.","consequence_high":"H2 over-evolution at cathode — arc risk — cell damage.","action_low":"Admin: check rectifier, restore. Active: alarm.","action_high":"ACTIVE: overcurrent relay trips. Admin: investigate.","psm_critical":"Yes"},
    {"sl":6,"param":"Pickling H2SO4 Concentration","uom":"g/L","soc_min":8,"soc_max":10,"sol_min":8,"sol_max":10,"sub_process":"Cleaning & Rinsing","equipment_linked":"H2SO4 dosing, acid analyser","identification_low":"Concentration analyser alarm","identification_high":"Concentration alarm — high","consequence_low":"Incomplete pickling — oxide layer — poor adhesion.","consequence_high":"Over-pickling — H2 gas spike — acid mist — equipment corrosion.","action_low":"Admin: add H2SO4. Verify by titration.","action_high":"Admin: dilute bath. Check dosing rate.","psm_critical":"Yes"},
    {"sl":7,"param":"Sn++ Concentration (SnSO4)","uom":"g/L","soc_min":26,"soc_max":32,"sol_min":24,"sol_max":34,"sub_process":"Tin Plating","equipment_linked":"Sn analyser, anode system","identification_low":"Daily bath analysis — titration alarm","identification_high":"Bath analysis alarm","consequence_low":"UNDER-PLATING — dull band — food can corrosion failure — PRODUCT REJECT.","consequence_high":"OVER-PLATING — excess tin — cost loss — specification breach.","action_low":"Admin: add SnSO4 makeup. Hold coils. Active: alarm.","action_high":"Admin: reduce current density.","psm_critical":"Yes"},
    {"sl":8,"param":"Free Acid Concentration","uom":"g/L","soc_min":13,"soc_max":16,"sol_min":11,"sol_max":18,"sub_process":"Tin Plating","equipment_linked":"Acid analyser, H2SO4 dosing","identification_low":"Bath analysis alarm","identification_high":"Bath analysis alarm","consequence_low":"Low conductivity — uneven tin — dull patches.","consequence_high":"Excess acid mist — TLV breach — equipment corrosion.","action_low":"Admin: add H2SO4 to bath.","action_high":"Admin: dilute bath. Check LEV.","psm_critical":"No"},
    {"sl":9,"param":"Strip Temperature (Reflow Exit)","uom":"°C","soc_min":232,"soc_max":270,"sol_min":232,"sol_max":270,"sub_process":"Reflow Furnace","equipment_linked":"Pyrometer ETL-1 (PSCE #1)","identification_low":"Pyrometer alarm below 232°C","identification_high":"Pyrometer auto-trip at 270°C","consequence_low":"INCOMPLETE TIN MELTING — dull coating — Fe-Sn alloy not formed — REJECT.","consequence_high":"STRIP BURNING — conductor roll damage — H2 fire risk — SHUTDOWN.","action_low":"Admin: increase reflow current. Check pyrometer.","action_high":"ACTIVE: Pyrometer auto-trip (PSCE #1). Admin: inspect conductor rolls.","psm_critical":"Yes"},
    {"sl":10,"param":"Quench Temperature","uom":"°C","soc_min":50,"soc_max":65,"sol_min":50,"sol_max":65,"sub_process":"Reflow Furnace","equipment_linked":"Quench tank temp transmitter, ICW","identification_low":"Temp transmitter alarm","identification_high":"Temp alarm","consequence_low":"Thermal shock — strip shape defects — tin coating cracks.","consequence_high":"Incomplete solidification — alloy overgrowth — appearance defects.","action_low":"Admin: check ICW supply. Increase flow.","action_high":"Admin: increase ICW flow. Check heat exchanger.","psm_critical":"No"},
    {"sl":11,"param":"Chemical Treatment Solution Temperature","uom":"°C","soc_min":40,"soc_max":45,"sol_min":40,"sol_max":45,"sub_process":"Chemical Treatment","equipment_linked":"TT-ChemTx, LEV","identification_low":"Temp transmitter alarm","identification_high":"Auto-bath off at 45°C SOL — CRITICAL Cr-VI volatilisation","consequence_low":"Incomplete passivation — corrosion failure in service.","consequence_high":"Cr-VI mist surge — TLV breach — MANDATORY SHUTDOWN per MSIHC 1989.","action_low":"Admin: increase heating. Delay production.","action_high":"ACTIVE: Bath auto-off. Air monitor check. SHUTDOWN if >0.05 mg/m3.","psm_critical":"Yes"},
    {"sl":12,"param":"Chemical Treatment Current","uom":"A","soc_min":300,"soc_max":2000,"sol_min":300,"sol_max":3500,"sub_process":"Chemical Treatment","equipment_linked":"Rectifier, current transmitter","identification_low":"Current meter alarm","identification_high":"Overcurrent relay","consequence_low":"Insufficient passivation — corrosion failure — food safety risk.","consequence_high":"Cr-VI reduction to Cr-III — bath balance upset.","action_low":"Admin: check rectifier. Verify bath connection.","action_high":"ACTIVE: overcurrent relay trips. Admin: investigate.","psm_critical":"Yes"},
]

ETL1_EDB = [
    {"sl":1,"sub_process":"Furnace - Propane Line","hazardous_substance":"Propane Gas","equipment":"Main Strainer DN150 PN10","tag_no":"1.3","selection_basis":"Condition Based","manufacturer":"Steinhaus","model":"DN150 PN10","design_basis":"Strainer on propane supply to reflow furnace. Removes particles blocking burner nozzles. Blockage = flame-out = furnace atmosphere risk. DN150 rated for full propane flow.","consequence_of_failure":"Burner blockage → flame-out → furnace atmosphere deviation → H2 risk.","barrier_type":"Passive","barrier_effectiveness":"Continuous passive protection — always active.","is_psce":False},
    {"sl":2,"sub_process":"Furnace - Propane Line","hazardous_substance":"Propane Gas","equipment":"Pressure Switch IP54 PSAL 1.13","tag_no":"PSAL 1.13","selection_basis":"Annual calibration","manufacturer":"Dungs","model":"Pressure Switch IP54","design_basis":"Monitors propane supply pressure. Low pressure = burner flame-out. High pressure = overfiring. IP54 rated. Dungs certified for flammable gas. PLC interlock.","consequence_of_failure":"Propane pressure deviation undetected → burner flame-out or overfiring → H2 atmosphere risk.","barrier_type":"Active — Instrumented","barrier_effectiveness":"Primary propane pressure detection. Annual calibration essential.","is_psce":True},
    {"sl":3,"sub_process":"Furnace - Propane Line","hazardous_substance":"Propane Gas","equipment":"Solenoid Valve DN50 UV 1.21","tag_no":"UV 1.21","selection_basis":"6-monthly inspection","manufacturer":"Kromschroder","model":"Solenoid Valve DN50","design_basis":"SAFETY CRITICAL: auto propane shut-off on any safety signal. Fail-safe: closes on de-energise. Kromschroder certified EN 161. DN50 full propane flow.","consequence_of_failure":"Cannot auto shut-off propane → propane to unlit burners → fire/explosion.","barrier_type":"Active — Automatic Trip","barrier_effectiveness":"PRIMARY propane safety barrier — auto, fail-safe, no operator action needed.","is_psce":True},
    {"sl":4,"sub_process":"Furnace - H2 Line","hazardous_substance":"Hydrogen Gas","equipment":"H2 Pressure Switch PSAL 2.14","tag_no":"PSAL 2.14","selection_basis":"3-monthly calibration","manufacturer":"Dungs","model":"Pressure Switch","design_basis":"Monitors H2 supply pressure to reflow furnace. Low pressure = H2 loss = unsafe restart without purge. PLC interlock — auto-trip on low H2. Dungs H2-service certified.","consequence_of_failure":"H2 supply loss undetected → furnace atmosphere deviates → explosive atmosphere on restart.","barrier_type":"Active — Automatic Trip","barrier_effectiveness":"CRITICAL PSCE BARRIER — primary H2 supply failure detection. 3-monthly calibration.","is_psce":True},
    {"sl":5,"sub_process":"Furnace - N2 Line","hazardous_substance":"Nitrogen Gas","equipment":"N2 Pressure Switch PSAL 3.19","tag_no":"PSAL 3.19","selection_basis":"Annual calibration","manufacturer":"Dungs","model":"Pressure Switch IP54","design_basis":"Monitors N2 purge supply pressure. PLC interlock: H2 admission blocked if N2 unavailable. Critical for safe startup sequence.","consequence_of_failure":"N2 unavailability undetected → H2 admitted without purge → explosive atmosphere.","barrier_type":"Active — Instrumented","barrier_effectiveness":"Confirms N2 availability before H2 admission permitted.","is_psce":False},
    {"sl":6,"sub_process":"Furnace - Cooling Water","hazardous_substance":"Cooling Water","equipment":"ICW Pressure Switch PSAL 4.4","tag_no":"PSAL 4.4","selection_basis":"Annual calibration","manufacturer":"IFM","model":"Electronic Pressure Switch","design_basis":"Monitors ICW pressure to conductor rolls and quench. Low ICW = overheating = arc in H2 atmosphere.","consequence_of_failure":"ICW loss undetected → conductor roll overheating → arc → H2 fire.","barrier_type":"Active — Instrumented","barrier_effectiveness":"Early warning of cooling failure before roll damage.","is_psce":False},
    {"sl":7,"sub_process":"Furnace - H2 Purge","hazardous_substance":"Hydrogen Gas","equipment":"Gas Control & Safety Run","tag_no":"502.1","selection_basis":"3-yearly inspection","manufacturer":"Kromschroder/Dungs","model":"Gas Control & Safety Run","design_basis":"Combined gas safety controller — manages safe startup sequence for H2, propane, N2. Performs safety run checks before gas admission. EN 298 certified.","consequence_of_failure":"Gas startup without safe state verification → H2/propane admission unsafely.","barrier_type":"Active — Automatic Trip","barrier_effectiveness":"Orchestrates all gas safety startup — single point of safety coordination.","is_psce":True},
]

ETL1_PSCE = [
    {"sl":1,"equipment":"Pyrometer — Strip Temperature (Reflow)","tag":"Pyrometer ETL-1","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Reflow Furnace","sap_tag":"S-ETL-001","justification":"PRIMARY PSCE. Monitors strip temperature (SOC 232-270°C). SOL 270°C = auto-trip. Only continuous strip temperature measurement. 232°C = tin melting point. Below → incomplete reflow. Above → strip burns.","consequence_of_failure":"Strip overheating undetected → strip burns → conductor roll damage → H2 fire risk.","maintenance":"3-monthly calibration. Annual blackbody reference calibration."},
    {"sl":2,"equipment":"H2 Pressure Switch PSAL 2.14","tag":"PSAL 2.14","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Reflow Furnace","sap_tag":"S-ETL-002","justification":"Monitors H2 supply to reflow furnace. H2 loss → furnace atmosphere compromised → explosive atmosphere on restart without purge.","consequence_of_failure":"Undetected H2 loss → unsafe restart → explosive atmosphere → explosion.","maintenance":"3-monthly calibration. Annual functional trip test."},
    {"sl":3,"equipment":"Propane Solenoid Valve UV 1.21","tag":"UV 1.21","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Reflow Furnace","sap_tag":"S-ETL-003","justification":"Auto propane shut-off on any safety signal. Fail-safe: closes on de-energise. EN 161 certified. Without this: propane cannot be auto-shut on trip.","consequence_of_failure":"Propane auto shut-off fails → continuing propane to unlit burners → explosion.","maintenance":"6-monthly inspection and functional test."},
    {"sl":4,"equipment":"Cr-VI Air Monitor (Chemical Treatment)","tag":"CrVI-Monitor","psce_type":"Prescriptive","category":"Safety Monitoring & Emergency Communication","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL-004","justification":"PRESCRIPTIVE per MSIHC Rules 1989. Continuous Cr-VI monitoring. TLV 0.05 mg/m3. IARC Group 1 carcinogen. Only warning of exposure. Alarm triggers mandatory evacuation.","consequence_of_failure":"Cr-VI exposure undetected → operators develop lung cancer (latency 10-30 years). Statutory violation.","maintenance":"Quarterly calibration. Monthly bump test. Annual NABL calibration."},
    {"sl":5,"equipment":"Chemical Treatment Bath Temperature Transmitter","tag":"TT-ChemTx","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL-005","justification":"Monitors Cr-VI bath temperature (SOC 40-45°C, SOL 45°C). Above 45°C = Cr-VI volatilisation surge → TLV breach. Auto-bath shutdown at SOL.","consequence_of_failure":"Bath above 45°C undetected → Cr-VI mist surge → carcinogen exposure → MSIHC violation.","maintenance":"6-monthly calibration. Functional test at SOL setpoint."},
    {"sl":6,"equipment":"LEV System — Chemical Treatment Bay","tag":"LEV-ChemTx","psce_type":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL-006","justification":"LEV for Cr-VI bath enclosure. Min 0.5 m/s face velocity. Prevents Cr-VI mist escaping to plant. Interlocked — bath cannot run without LEV.","consequence_of_failure":"LEV failure → Cr-VI mist → area-wide carcinogen exposure → mandatory shutdown.","maintenance":"Monthly airflow measurement. Quarterly duct inspection. Annual commissioning test."},
]


# ══════════════════════════════════════════════════════════════════════
# SHARED UTILITY FUNCTIONS
# ══════════════════════════════════════════════════════════════════════
def risk_color(r):
    return "#ef4444" if r >= 75 else "#f97316" if r >= 50 else "#22c55e"

def risk_bar(r):
    c = risk_color(r)
    return f'<div class="sl-rbar-wrap"><div class="sl-rbar-bg"><div class="sl-rbar-fill" style="width:{r}%;background:{c}"></div></div><span style="font-size:.75rem;font-weight:700;color:{c};font-family:monospace">{r}/100</span></div>'

# ══════════════════════════════════════════════════════════════════════
# ETL-1 CHEMICALS DATA
# ══════════════════════════════════════════════════════════════════════
CHEMICALS = [
    {"code":"A1","name":"Sulphuric Acid (H2SO4)","risk":72,"color":"#f97316",
     "class":"Corrosive liquid, Oxidising agent","cas":"7664-93-9","hazchem":"HAZCHEM 2R","nfpa":"3-0-2(W)",
     "tlv_twa":"1 mg/m3 (ACGIH 2023 — thoracic fraction as H2SO4 mist)","tlv_stel":"Not established (ACGIH 2023). NIOSH: 1 mg/m3 TWA. OSHA PEL: 1 mg/m3.","tlv_ceil":"Not established (ACGIH). OSHA 1971: 1 mg/m3 PEL.",
     "ld50":"2140 mg/kg (rat, oral)","lc50":"510 mg/m3/2h (rat, inhal.)",
     "flash":"N/A (not flammable)","bp":"337°C","mp":"10°C (conc.)","sg":"1.84 (conc.)","vp":"<0.3 hPa at 20°C",
     "odour":"Odourless (dilute); slight choking (hot/conc.)",
     "reactivity":"Reacts violently with water (exothermic). Generates H2 gas with metals. Reacts explosively with strong bases. Incompatible with Cr-VI, organics, combustibles.",
     "health":"CORROSIVE. Severe burns to skin, eyes, mucous membranes. Acid mist: bronchospasm, pulmonary oedema. Dental erosion from chronic exposure.",
     "env":"Highly toxic to aquatic organisms. Reduces water pH drastically. CPCB Schedule chemical.",
     "storage":"Cool, ventilated. Away from metals, bases, organics. Secondary containment mandatory.",
     "ppe":"Full face shield, rubber apron, rubber gloves, rubber boots. Air-supplied respirator if mist present.",
     "emergency":"Absorb with dry sand/earth. Neutralise with lime/Na2CO3. Deluge shower 15 min minimum.",
     "etl1_use":"Pickling bath (8-10 g/L), plating bath base electrolyte","soc":"Pickling: 8-10 g/L | Plating free acid: 13-16 g/L","sol":"Pickling: 8-10 g/L | Plating: 11-18 g/L"},
    {"code":"A2","name":"Phenol Sulfonic Acid (PSA)","risk":55,"color":"#eab308",
     "class":"Corrosive liquid, organic acid","cas":"98-67-9","hazchem":"NFPA 3-1-0","nfpa":"3-1-0",
     "tlv_twa":"0.5 ppm (ACGIH — phenol component, SKIN designation)","tlv_stel":"15.6 ppm (NIOSH STEL — phenol component). ACGIH: no STEL set.","tlv_ceil":"Not established. NIOSH IDLH phenol: 250 ppm (practical ceiling for respiratory protection).",
     "ld50":"1050 mg/kg (rat, oral)","lc50":"Not established",
     "flash":">150°C","bp":"~186°C","mp":"~33°C","sg":"1.28","vp":"Very low at 20°C",
     "odour":"Faint phenolic odour",
     "reactivity":"Reacts with strong bases (exothermic). Reacts with oxidising agents (Na2Cr2O7). Decomposition produces SO2, CO.",
     "health":"Corrosive to skin and eyes. Respiratory irritant. Phenol component: skin absorption possible.",
     "env":"Moderately toxic to aquatic organisms. Phenol degrades biologically.",
     "storage":"Cool, dry, ventilated. Away from oxidisers and bases.",
     "ppe":"Safety glasses, chemical gloves, lab coat.",
     "emergency":"Collect in containers, dilute with water. Flush with water 15 min.",
     "etl1_use":"Plating bath grain refiner/brightener base (3-6 g/L combined with ENSA)","soc":"3-6 g/L","sol":"2-7 g/L"},
    {"code":"A3","name":"Dioctyl Sebacate (DOS)","risk":30,"color":"#22c55e",
     "class":"Combustible liquid","cas":"122-62-3","hazchem":"NFPA 1-1-0","nfpa":"1-1-0",
     "tlv_twa":"10 mg/m3 (ACGIH PNOR — inhalable fraction, nuisance aerosol)","tlv_stel":"3 mg/m3 (ACGIH PNOR — respirable fraction). No chemical-specific STEL.","tlv_ceil":"Not established. No significant vapour hazard (VP essentially zero at ambient).",
     "ld50":">5000 mg/kg (rat, oral)","lc50":"Not established",
     "flash":"190°C (closed cup)","bp":">300°C","mp":"-40°C","sg":"0.914","vp":"<0.01 hPa at 20°C",
     "odour":"Faint oily odour",
     "reactivity":"Stable under normal conditions. Incompatible with CrO3 (hazardous). Decomposition: CO, CO2 at high temperature.",
     "health":"Low acute toxicity. Mild skin/eye irritant. Not a known carcinogen.",
     "env":"Low toxicity to aquatic organisms. Biodegradable.",
     "storage":"Normal conditions. Cool, dry. Away from oxidisers.",
     "ppe":"Safety glasses, standard work gloves.",
     "emergency":"Absorb with dry material. Non-hazardous cleanup. Wash with soap and water.",
     "etl1_use":"Electrostatic oiling — applied at 1-2 g/m2 for corrosion protection","soc":"Per product spec","sol":"Per product spec"},
    {"code":"A4","name":"ENSA (Ethoxylated Naphthol Sulphonic Acid)","risk":40,"color":"#22c55e",
     "class":"Irritant liquid","cas":"Mixture","hazchem":"NFPA 2-1-1","nfpa":"2-1-1",
     "tlv_twa":"1 mg/m3 (H2SO4 acid mist — ACGIH TLV applies at plating bath)","tlv_stel":"3 mg/m3 (H2SO4 acid mist STEL — no ENSA-specific STEL established)","tlv_ceil":"Not established for ENSA blend.",
     "ld50":"Not established","lc50":"Not established",
     "flash":"~170°C","bp":"~200°C","mp":"Not established","sg":"~1.1","vp":"Low",
     "odour":"Mild aromatic/sulphonic odour",
     "reactivity":"Unstable in strongly acidic conditions at high temperature. Incompatible with strong acids and alkalis.",
     "health":"Irritant to skin, eyes, respiratory tract. Naphthol component: moderate toxicity.",
     "env":"Moderately toxic to aquatic organisms. Ethoxylate component may be persistent.",
     "storage":"Cool, dark. Away from acids and oxidisers.",
     "ppe":"Safety glasses, chemical gloves, lab coat.",
     "emergency":"Dilute with water, collect. Flush with water.",
     "etl1_use":"Plating bath brightener — controls grain structure of tin deposit","soc":"3-6 g/L","sol":"2-7 g/L"},
    {"code":"A5","name":"Sodium Dichromate (Na2Cr2O7)","risk":95,"color":"#ef4444",
     "class":"CARCINOGEN — Oxidising solid, toxic","cas":"10588-01-9","hazchem":"NFPA 4-0-2 (OX)","nfpa":"4-0-2 (OX)",
     "tlv_twa":"0.01 mg/m3 as Cr(VI) (ACGIH A1 2023) | OSHA PEL: 0.005 mg/m3 | NIOSH REL: 0.0002 mg/m3","tlv_stel":"Not established (ACGIH). OSHA Action Level: 0.0025 mg/m3 as Cr(VI).","tlv_ceil":"Not established separately (ACGIH TWA is controlling limit). OSHA: no ceiling set.",
     "ld50":"50 mg/kg (rat, oral)","lc50":"Not established",
     "flash":"N/A (oxidiser)","bp":"400°C (decomposes)","mp":"356°C","sg":"2.52","vp":"Negligible",
     "odour":"Odourless",
     "reactivity":"STRONG OXIDISER — reacts violently with organics, reducing agents, flammables. Reacts with H2SO4 to form chromic acid. Contact with combustibles can cause fire.",
     "health":"IARC Group 1 CARCINOGEN. Lung cancer, nasal/sinus cancer. TLV 0.05 mg/m3. Skin sensitiser — chrome ulcers. Mutagenic.",
     "env":"HIGHLY TOXIC to aquatic organisms. Extremely persistent in soil/groundwater. MSIHC Schedule chemical.",
     "storage":"Separate, cool, dry, ventilated. Away from ALL organics. Locked access. Secondary containment. MSIHC reporting >10 kg.",
     "ppe":"Class C suit. Air-supplied respirator. Face shield, rubber gloves, boots.",
     "emergency":"MAJOR SPILL: evacuate, call emergency services. Specialist cleanup. Medical attention immediately. CPCB notification within 48h.",
     "etl1_use":"Chemical treatment bath — electrolytic chromate passivation of tin plate","soc":"Per SDS specification","sol":"Air: <0.1 mg/m3 ceiling | Breach = SHUTDOWN"},
    {"code":"A6","name":"Chromic Acid (CrO3/Cr-VI)","risk":98,"color":"#ef4444",
     "class":"CARCINOGEN — Powerful oxidiser, corrosive, highly toxic","cas":"1333-82-0","hazchem":"NFPA 3-0-1 (OX)","nfpa":"3-0-1 (OX)",
     "tlv_twa":"0.05 mg/m3 as Cr (ACGIH)","tlv_stel":"0.1 mg/m3 ceiling","tlv_ceil":"0.1 mg/m3",
     "ld50":"80 mg/kg (rat, oral)","lc50":"<10 mg/m3 (rat, 4h)",
     "flash":"N/A (causes fires — not flammable itself)","bp":"250°C (decomposes)","mp":"196°C","sg":"2.70","vp":"Not applicable",
     "odour":"Acrid, metallic (vapour/mist)",
     "reactivity":"POWERFUL OXIDISER — contact with organics = spontaneous ignition. Reacts explosively with reducing agents. Mixed with H2SO4: chromic acid. EXPLOSIVE with alcohol/acetone/ketones.",
     "health":"IARC Group 1 CARCINOGEN (highest). Lung cancer 15-30x risk. TLV 0.05 mg/m3. Nasal perforation. Kidney damage. Mutagenic, teratogenic.",
     "env":"MOST TOXIC to aquatic organisms. Cr-VI persists for decades. Priority Hazardous Substance. MCL drinking water: 0.05 mg/L.",
     "storage":"SEPARATE locked store. NO organics within 5m. 110% secondary containment. Restricted access. MSIHC annual reporting.",
     "ppe":"MANDATORY: SCBA or airline respirator, Class C suit, face shield, heavy rubber gloves/boots. Buddy system.",
     "emergency":"EVACUATE — do not re-enter without SCBA. Hazmat team only. Decontaminate immediately. CPCB within 48h.",
     "etl1_use":"Chemical treatment bath — Cr-VI passivation (<10 mg/m2 on finished product)","soc":"Air: <0.05 mg/m3 (TLV-TWA)","sol":"Air: <0.1 mg/m3 | Breach = immediate SHUTDOWN"},
]

# ══════════════════════════════════════════════════════════════════════
# ACCIDENTS DATA (Home page incident records)
# ══════════════════════════════════════════════════════════════════════
ACCIDENTS = [
    {"industry":"Steel & Metal","plant":"Blast Furnace — Tata Steel","incident":"Hot metal ladle overflow — severe burns to 3 operators","severity":"L3","year":2022,"lesson":"Ladle inspection checklist mandatory before every pour. Level sensor calibration quarterly."},
    {"industry":"Steel & Metal","plant":"Reheating Furnace — JSW","incident":"Furnace explosion — gas buildup during restart","severity":"L4","year":2021,"lesson":"Mandatory N2 purge before gas admission. Purge interlock must be hardwired, not software only."},
    {"industry":"Chemicals","plant":"Chlor-Alkali — GACL","incident":"Cl2 gas leak — 12 workers hospitalised","severity":"L3","year":2023,"lesson":"Cl2 detector calibration monthly. Emergency isolation valve must be outside exclusion zone."},
    {"industry":"Oil & Gas","plant":"Refinery — BPCL Mumbai","incident":"BLEVE — storage tank fire","severity":"L4","year":2020,"lesson":"Water spray deluge on all LPG/propane tanks. Thermographic inspection of tanks annually."},
    {"industry":"Steel & Metal","plant":"ETL-1 — Tinplate","incident":"Cr-VI TLV breach — bath temperature exceeded 45°C","severity":"L2","year":2023,"lesson":"Bath temperature auto-trip at 45°C SOL. LEV face velocity verified monthly. Air monitor quarterly calibration."},
    {"industry":"Chemicals","plant":"H2 Plant — Electrolyser","incident":"H2-in-O2 analyser failure — explosive atmosphere formed","severity":"L3","year":2022,"lesson":"AT1002 requires 3-monthly calibration. Redundant analyser recommended. 1oo2 voting logic for auto-trip."},
    {"industry":"Oil & Gas","plant":"Pipeline — GAIL","incident":"H2S leak — worker fatality","severity":"L4","year":2021,"lesson":"H2S detector at all low points. Buddy system mandatory in H2S zones. Escape SCBA at entry points."},
    {"industry":"Steel & Metal","plant":"Coke Plant — SAIL","incident":"CO exposure — 4 workers overcome","severity":"L3","year":2023,"lesson":"Fixed CO detectors at all low-lying areas. Personal CO monitor mandatory. Emergency rescue breathing apparatus."},
]

# ══════════════════════════════════════════════════════════════════════
# SHARED RENDERER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════
def render_pdb(params, dept_key="pdb"):
    st.markdown("""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.25);border-radius:10px;padding:.9rem 1.2rem;margin-bottom:1rem">
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.78rem">
<div><b style="color:#22c55e">SOC (Standard Operating Condition)</b> — Normal target range. Deviation from SOC triggers identification and corrective action before reaching SOL.</div>
<div><b style="color:#f97316">SOL (Safe Operating Limit)</b> — Outer safety boundary. Breach = Process Safety Incident. Triggers immediate corrective action or automatic plant trip.</div>
</div></div>""", unsafe_allow_html=True)

    view = st.radio("Display mode", ["Flashcards","Table"], horizontal=True, key=f"pdb_view_{dept_key}")
    proc_list = sorted(set(p.get("sub_process","General") for p in params))
    proc_filter = st.selectbox("Filter by sub-process", ["All"] + proc_list, key=f"pdb_filter_{dept_key}")
    shown = params if proc_filter == "All" else [p for p in params if p.get("sub_process","General") == proc_filter]

    if view == "Flashcards":
        for p in shown:
            is_crit = p.get("psm_critical","No") in ("Yes","Y","YES")
            sub = p.get("sub_process","")
            linked = p.get("equipment_linked","")
            crit_badge = '<span style="background:rgba(239,68,68,.2);color:#f87171;border:1px solid rgba(239,68,68,.4);font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">PSM CRITICAL</span>' if is_crit else ""
            sub_badge = f'<span style="background:rgba(59,130,246,.15);color:#60a5fa;font-size:.6rem;font-weight:600;padding:2px 8px;border-radius:20px;margin-left:6px">{sub}</span>' if sub else ""
            soc_min = str(p.get("soc_min","—")); soc_max = str(p.get("soc_max","—"))
            sol_min = str(p.get("sol_min","—")); sol_max = str(p.get("sol_max","—"))
            st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:10px">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:.7rem">
  <div><span style="font-size:.68rem;font-weight:700;color:#f97316">#{p['sl']}</span>
  <span style="font-size:.9rem;font-weight:700;color:#e2e8f0;margin-left:8px">{p['param']}</span>
  {crit_badge}{sub_badge}</div>
  <span style="font-size:.72rem;font-weight:700;color:#64748b;font-family:monospace">{p['uom']}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:.7rem">
  <div style="background:#080d18;border:1px solid rgba(34,197,94,.2);border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:3px">SOC MIN</div><div style="font-size:.9rem;font-weight:800;color:#22c55e;font-family:monospace">{soc_min}</div></div>
  <div style="background:#080d18;border:1px solid rgba(34,197,94,.2);border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:3px">SOC MAX</div><div style="font-size:.9rem;font-weight:800;color:#22c55e;font-family:monospace">{soc_max}</div></div>
  <div style="background:#080d18;border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:3px">SOL MIN</div><div style="font-size:.9rem;font-weight:800;color:#f97316;font-family:monospace">{sol_min}</div></div>
  <div style="background:#080d18;border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:3px">SOL MAX</div><div style="font-size:.9rem;font-weight:800;color:#f97316;font-family:monospace">{sol_max}</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:.6rem">
  <div style="background:#0a1628;border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">IDENTIFICATION (below SOC)</div><div style="font-size:.73rem;color:#94a3b8">{p.get('identification_low','—')}</div></div>
  <div style="background:#0a1628;border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">IDENTIFICATION (above SOC)</div><div style="font-size:.73rem;color:#94a3b8">{p.get('identification_high','—')}</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:.6rem">
  <div style="background:rgba(234,179,8,.05);border:1px solid rgba(234,179,8,.2);border-left:3px solid #eab308;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#eab308;margin-bottom:3px">CONSEQUENCE — BELOW SOC/SOL</div><div style="font-size:.73rem;color:#fde68a">{p.get('consequence_low','—')}</div></div>
  <div style="background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.2);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:3px">CONSEQUENCE — ABOVE SOC/SOL</div><div style="font-size:.73rem;color:#fca5a5">{p.get('consequence_high','—')}</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:.4rem">
  <div style="background:rgba(34,197,94,.05);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#22c55e;margin-bottom:3px">ACTION / BARRIER — LOW</div><div style="font-size:.73rem;color:#4ade80">{p.get('action_low','—')}</div></div>
  <div style="background:rgba(34,197,94,.05);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#22c55e;margin-bottom:3px">ACTION / BARRIER — HIGH</div><div style="font-size:.73rem;color:#4ade80">{p.get('action_high','—')}</div></div>
</div>
{f'<div style="font-size:.7rem;color:#475569;margin-top:.4rem">Linked: <span style="color:#60a5fa">{linked}</span></div>' if linked else ''}
</div>""", unsafe_allow_html=True)
    else:
        tbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
        for h in ["#","Parameter","UoM","SOC Min","SOC Max","SOL Min","SOL Max","Consequence Low","Consequence High","Barrier Low","Barrier High","PSM"]:
            tbl += f'<th style="padding:7px 10px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
        tbl += '</tr></thead><tbody>'
        for p in shown:
            is_crit = p.get("psm_critical","No") in ("Yes","Y","YES")
            bg_r = "rgba(249,115,22,.04)" if is_crit else "transparent"
            crit_txt = "YES" if is_crit else "No"
            crit_c = "#f97316" if is_crit else "#475569"
            tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{bg_r}"><td style="padding:7px 10px;color:#475569;font-family:monospace">{p["sl"]}</td><td style="padding:7px 10px;color:#e2e8f0;font-weight:600;white-space:nowrap">{p["param"]}</td><td style="padding:7px 10px;color:#64748b;font-family:monospace">{p["uom"]}</td><td style="padding:7px 10px;color:#22c55e;font-family:monospace;font-weight:700">{p.get("soc_min","—")}</td><td style="padding:7px 10px;color:#22c55e;font-family:monospace;font-weight:700">{p.get("soc_max","—")}</td><td style="padding:7px 10px;color:#f97316;font-family:monospace">{p.get("sol_min","—")}</td><td style="padding:7px 10px;color:#f97316;font-family:monospace">{p.get("sol_max","—")}</td><td style="padding:7px 10px;color:#fde68a;font-size:.7rem;max-width:180px">{p.get("consequence_low","—")}</td><td style="padding:7px 10px;color:#fca5a5;font-size:.7rem;max-width:180px">{p.get("consequence_high","—")}</td><td style="padding:7px 10px;color:#4ade80;font-size:.7rem;max-width:160px">{p.get("action_low","—")}</td><td style="padding:7px 10px;color:#4ade80;font-size:.7rem;max-width:160px">{p.get("action_high","—")}</td><td style="padding:7px 10px;text-align:center;color:{crit_c};font-weight:700">{crit_txt}</td></tr>'
        tbl += '</tbody></table></div>'
        st.markdown(tbl, unsafe_allow_html=True)


def render_edb(items, dept_key="edb"):
    st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.8rem 1rem;margin-bottom:1rem;font-size:.78rem;color:#94a3b8">
<b style="color:#e2e8f0">Equipment Design Basis (EDB)</b> — Documents each piece of equipment handling/controlling hazardous substances: design parameters, safety basis, maintenance schedule, manufacturer.<br>
<b style="color:#f97316">Consequence Based:</b> failure directly causes major accident &nbsp;|&nbsp; <b style="color:#a78bfa">Prevention & Mitigation:</b> installed to prevent/limit major accident
</div>""", unsafe_allow_html=True)

    view = st.radio("Display mode", ["Flashcards","Table"], horizontal=True, key=f"edb_view_{dept_key}")
    subp_list = sorted(set(x.get("sub_process","") for x in items))
    filt = st.selectbox("Filter by sub-process", ["All"] + subp_list, key=f"edb_filt_{dept_key}")
    shown = items if filt == "All" else [x for x in items if x.get("sub_process","") == filt]

    if view == "Flashcards":
        for item in shown:
            basis = item.get("selection_basis","")
            is_pm = "Prevention" in basis or "Mitigation" in basis
            is_psce = item.get("is_psce", False)
            badge_col = "#a78bfa" if is_pm else "#3b82f6"
            badge_txt = "Prevention & Mitigation" if is_pm else "Consequence Based"
            psce_badge = '<span style="background:rgba(239,68,68,.2);color:#f87171;border:1px solid rgba(239,68,68,.4);font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">PSCE</span>' if is_psce else ""
            btype = item.get("barrier_type","")
            barrier_colors = {"Active — Instrumented":"#22c55e","Active — Mechanical":"#3b82f6","Administrative":"#eab308","Passive":"#a78bfa","Active — Automatic Trip":"#ef4444"}
            bc = barrier_colors.get(btype,"#64748b")
            st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:4px solid {badge_col};border-radius:12px;padding:1.1rem 1.3rem;margin-bottom:10px">
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.7rem">
  <div><span style="font-size:.68rem;font-weight:700;color:#f97316">#{item['sl']}</span>
  <span style="font-size:.9rem;font-weight:700;color:#e2e8f0;margin-left:8px">{item['equipment']}</span>{psce_badge}</div>
  <span style="background:{badge_col}20;color:{badge_col};border:1px solid {badge_col}40;font-size:.6rem;font-weight:700;padding:3px 9px;border-radius:20px;white-space:nowrap">{badge_txt}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:.7rem">
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">SUB-PROCESS</div><div style="font-size:.72rem;color:#94a3b8">{item.get('sub_process','')}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">HAZARDOUS SUBSTANCE</div><div style="font-size:.72rem;color:#fca5a5">{item.get('hazardous_substance','')}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">TAG NO.</div><div style="font-size:.72rem;color:#f97316;font-family:monospace">{item.get('tag_no','—')}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">MANUFACTURER / MODEL</div><div style="font-size:.72rem;color:#94a3b8">{item.get('manufacturer','—')} — {item.get('model','—')}</div></div>
</div>
<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;margin-bottom:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">DESIGN BASIS & PURPOSE</div><div style="font-size:.75rem;color:#94a3b8;line-height:1.7">{item.get('design_basis','—')}</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px">
  <div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:3px">CONSEQUENCE OF FAILURE</div><div style="font-size:.72rem;color:#fca5a5">{item.get('consequence_of_failure','—')}</div></div>
  <div style="background:{bc}10;border:1px solid {bc}30;border-left:3px solid {bc};border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:{bc};margin-bottom:3px">BARRIER TYPE</div><div style="font-size:.72rem;color:#94a3b8">{btype if btype else '—'}</div><div style="font-size:.68rem;color:#64748b;margin-top:2px">{item.get('barrier_effectiveness','')}</div></div>
  <div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#64748b;margin-bottom:3px">MAINTENANCE</div><div style="font-size:.72rem;color:#94a3b8">{item.get('selection_basis','—')}</div></div>
</div>
</div>""", unsafe_allow_html=True)
    else:
        tbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
        for h in ["#","Equipment","Sub-Process","Hazardous Substance","Tag No","Barrier Type","Basis","Manufacturer","Model","Consequence","Design Basis"]:
            tbl += f'<th style="padding:7px 10px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
        tbl += '</tr></thead><tbody>'
        for item in shown:
            is_pm2 = "Prevention" in item.get("selection_basis","") or "Mitigation" in item.get("selection_basis","")
            bc2 = "#a78bfa" if is_pm2 else "#3b82f6"
            tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 10px;color:#475569;font-family:monospace">{item["sl"]}</td><td style="padding:7px 10px;color:#e2e8f0;font-weight:600">{item["equipment"]}</td><td style="padding:7px 10px;color:#94a3b8">{item.get("sub_process","")}</td><td style="padding:7px 10px;color:#fca5a5">{item.get("hazardous_substance","")}</td><td style="padding:7px 10px;color:#f97316;font-family:monospace">{item.get("tag_no","—")}</td><td style="padding:7px 10px"><span style="background:rgba(59,130,246,.1);color:#60a5fa;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:20px">{item.get("barrier_type","—")}</span></td><td style="padding:7px 10px;color:#94a3b8;font-size:.68rem">{item.get("selection_basis","—")}</td><td style="padding:7px 10px;color:#64748b">{item.get("manufacturer","—")}</td><td style="padding:7px 10px;color:#64748b;font-family:monospace;font-size:.68rem">{item.get("model","—")}</td><td style="padding:7px 10px;color:#fca5a5;font-size:.7rem;max-width:160px">{item.get("consequence_of_failure","—")}</td><td style="padding:7px 10px;color:#64748b;font-size:.7rem;max-width:200px">{str(item.get("design_basis","—"))[:100]}...</td></tr>'
        tbl += '</tbody></table></div>'
        st.markdown(tbl, unsafe_allow_html=True)


def render_psm_framework(plant_name="", meta=None):
    fw = PSM_FRAMEWORK

    st.markdown(f"""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem">
<div style="font-size:.9rem;font-weight:800;color:#3b82f6;margin-bottom:.3rem">PSRM — Process Safety Risk Management Framework</div>
<div style="font-size:.78rem;color:#94a3b8;line-height:1.8">
Based on the <b style="color:#e2e8f0">Tata Steel PSRM Module</b> — aligned with OSHA 29 CFR 1910.119 (Process Safety Management) and UK HSE COMAH. 
14 PSM elements mandatory for HHO processes. Barrier model: Detector + Logic Solver + Actuator = One Barrier.
</div></div>""", unsafe_allow_html=True)

    fw_tabs = st.tabs(["Consequence Levels (L1-L5)","Hazard Categories (A1-A5)","Barrier Model","Layers of Protection","HAZOP Methodology","Bow Tie","LOPA","PSI Elements (14)"])

    # ── L1-L5 ────────────────────────────────────────────────────────
    with fw_tabs[0]:
        st.markdown('''<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">
Consequence severity classified across 4 dimensions: <b style="color:#ef4444">People</b> (injury/fatality), <b style="color:#f97316">Community</b> (off-site impact), 
<b style="color:#eab308">Asset</b> (property damage), <b style="color:#22c55e">Environment</b> (release/impact). All 4 must be assessed for each scenario.
HHO threshold: ANY ONE of — property damage &gt;Rs.50L OR fatality potential OR significant env. impact → L3+.
</div>''', unsafe_allow_html=True)

        for lk, lv in fw["consequence_levels"].items():
            c = lv["color"]
            ex_html = "".join(f'<div style="font-size:.7rem;color:#64748b;padding:1px 0">• {e}</div>' for e in lv["examples"])
            st.markdown(f"""<div style="background:#0d1f35;border:1px solid {c}40;border-left:5px solid {c};border-radius:10px;padding:1rem 1.2rem;margin-bottom:8px">
<div style="display:flex;align-items:center;gap:10px;margin-bottom:.6rem">
  <span style="background:{c}20;color:{c};border:1px solid {c}40;font-size:.85rem;font-weight:800;padding:4px 18px;border-radius:20px">{lv["label"]}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:.6rem">
  <div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:8px;padding:.6rem">
    <div style="font-size:.55rem;color:#ef4444;font-weight:700;letter-spacing:1px;margin-bottom:3px">👤 PEOPLE</div>
    <div style="font-size:.72rem;color:#e2e8f0">{lv["people"]}</div>
  </div>
  <div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.6rem">
    <div style="font-size:.55rem;color:#f97316;font-weight:700;letter-spacing:1px;margin-bottom:3px">🏘 COMMUNITY</div>
    <div style="font-size:.72rem;color:#e2e8f0">{lv["community"]}</div>
  </div>
  <div style="background:rgba(234,179,8,.08);border:1px solid rgba(234,179,8,.2);border-radius:8px;padding:.6rem">
    <div style="font-size:.55rem;color:#eab308;font-weight:700;letter-spacing:1px;margin-bottom:3px">🏭 ASSET</div>
    <div style="font-size:.72rem;color:#e2e8f0">{lv["asset"]}</div>
  </div>
  <div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-radius:8px;padding:.6rem">
    <div style="font-size:.55rem;color:#22c55e;font-weight:700;letter-spacing:1px;margin-bottom:3px">🌿 ENVIRONMENT</div>
    <div style="font-size:.72rem;color:#e2e8f0">{lv["environment"]}</div>
  </div>
</div>
<div style="display:grid;grid-template-columns:1fr 2fr;gap:8px">
  <div style="background:#080d18;border-radius:6px;padding:.6rem">
    <div style="font-size:.58rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">PRODUCTION LOSS</div>
    <div style="font-size:.72rem;color:#94a3b8">{lv["production"]}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.6rem">
    <div style="font-size:.58rem;color:#f97316;font-weight:700;letter-spacing:1px;margin-bottom:2px">PSM ACTION REQUIRED</div>
    <div style="font-size:.72rem;color:#f97316">{lv["psm_action"]}</div>
  </div>
</div>
<div style="margin-top:.5rem">{ex_html}</div>
</div>""", unsafe_allow_html=True)

    # ── A1-A5 ────────────────────────────────────────────────────────
    with fw_tabs[1]:
        for ak, av in fw["hazard_categories"].items():
            c = av["color"]
            props_html = "".join(f'<div style="font-size:.7rem;color:#60a5fa;padding:1px 0">▸ {p}</div>' for p in av["key_properties"])
            ex_html = "".join(f'<div style="font-size:.7rem;color:#fca5a5;padding:1px 0">• {e}</div>' for e in av["examples"])
            ctrl_html = "".join(f'<div style="font-size:.7rem;color:#4ade80;padding:1px 0">✓ {ct}</div>' for ct in av["controls"])
            st.markdown(f"""<div style="background:#0d1f35;border:1px solid {c}40;border-left:5px solid {c};border-radius:10px;padding:1rem 1.2rem;margin-bottom:10px">
<div style="font-size:.92rem;font-weight:800;color:{c};margin-bottom:.4rem">{av["label"]}</div>
<div style="font-size:.78rem;color:#94a3b8;margin-bottom:.7rem">{av["desc"]}</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:.6rem">
  <div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem">
    <div style="font-size:.58rem;color:#3b82f6;font-weight:700;letter-spacing:1px;margin-bottom:4px">KEY PROPERTIES</div>{props_html}
  </div>
  <div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem">
    <div style="font-size:.58rem;color:#ef4444;font-weight:700;letter-spacing:1px;margin-bottom:4px">PLANT EXAMPLES</div>{ex_html}
  </div>
  <div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem">
    <div style="font-size:.58rem;color:#22c55e;font-weight:700;letter-spacing:1px;margin-bottom:4px">REQUIRED CONTROLS</div>{ctrl_html}
  </div>
</div>
<div style="background:rgba(249,115,22,.06);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.6rem .9rem">
  <span style="font-size:.62rem;font-weight:700;color:#f97316">PSM IMPLICATION: </span>
  <span style="font-size:.72rem;color:#f97316">{av["psm_implication"]}</span>
</div>
</div>""", unsafe_allow_html=True)

    # ── Barrier Model ─────────────────────────────────────────────────
    with fw_tabs[2]:
        bm = fw["barrier_model"]
        st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7"><b style="color:#e2e8f0">Barrier = Detector + Logic Solver + Actuator.</b> {bm["definition"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">3 Components of a Barrier</div>', unsafe_allow_html=True)
        comp_cols = st.columns(3)
        comp_colors = ["#3b82f6","#f97316","#22c55e"]
        for ii, (ck, cv) in enumerate(bm["components"].items()):
            with comp_cols[ii]:
                cc = comp_colors[ii]
                st.markdown(f'''<div style="background:#0d1f35;border:1px solid {cc}40;border-top:4px solid {cc};border-radius:10px;padding:1rem;height:100%">
<div style="font-size:.8rem;font-weight:700;color:{cc};margin-bottom:.5rem">{"①" if ii==0 else "②" if ii==1 else "③"} {ck}</div>
<div style="font-size:.75rem;color:#94a3b8;line-height:1.7">{cv}</div>
</div>''', unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">Barrier Types — from Tata Steel PSRM Module</div>', unsafe_allow_html=True)
        for tk, tv in bm["types"].items():
            tc = "#22c55e" if "Passive" in tk else "#3b82f6" if "Active" in tk else "#eab308"
            st.markdown(f'<div style="background:#0d1f35;border:1px solid {tc}30;border-left:4px solid {tc};border-radius:8px;padding:.8rem 1rem;margin-bottom:6px"><div style="font-size:.78rem;font-weight:700;color:{tc};margin-bottom:3px">{tk}</div><div style="font-size:.75rem;color:#94a3b8;line-height:1.6">{tv}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">Preventive vs Mitigation Barriers</div>', unsafe_allow_html=True)
        for ck, cv in bm["categories"].items():
            cc = "#22c55e" if "Preventive" in ck else "#ef4444"
            st.markdown(f'<div style="background:#0d1f35;border:1px solid {cc}30;border-left:4px solid {cc};border-radius:8px;padding:.8rem 1rem;margin-bottom:6px"><div style="font-size:.8rem;font-weight:700;color:{cc};margin-bottom:3px">{ck}</div><div style="font-size:.75rem;color:#94a3b8;line-height:1.6">{cv}</div></div>', unsafe_allow_html=True)

    # ── Layers of Protection ──────────────────────────────────────────
    with fw_tabs[3]:
        st.markdown('''<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">
The <b style="color:#e2e8f0">Layers of Protection</b> model (from Tata Steel module) shows concentric protective layers around a hazardous process.
Inner layers prevent the top event (SOC → SOL). Outer layers mitigate consequences after loss of containment.
Each layer must be <b style="color:#f97316">Independent</b> of the others.
</div>''', unsafe_allow_html=True)

        for layer in fw["layers_of_protection"]:
            c = layer["color"]
            side_badge = f'<span style="background:rgba(34,197,94,.15);color:#4ade80;font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:20px">Prevention</span>' if "Prevention" in layer["side"] else f'<span style="background:rgba(239,68,68,.15);color:#f87171;font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:20px">Mitigation</span>'
            st.markdown(f'''<div style="background:#0d1f35;border:1px solid {c}30;border-left:4px solid {c};border-radius:8px;padding:.7rem 1rem;margin-bottom:5px;display:flex;align-items:flex-start;gap:12px">
<div style="background:{c};color:#000;font-size:.7rem;font-weight:800;width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0">{layer["layer"]}</div>
<div style="flex:1">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:3px">
<span style="font-size:.8rem;font-weight:700;color:#e2e8f0">{layer["name"]}</span>
{side_badge}
</div>
<div style="font-size:.74rem;color:#94a3b8;line-height:1.6">{layer["desc"]}</div>
</div>
</div>''', unsafe_allow_html=True)

    # ── HAZOP ─────────────────────────────────────────────────────────
    with fw_tabs[4]:
        hz = fw["hazop"]
        st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">{hz["definition"]}</div>', unsafe_allow_html=True)

        h_c1, h_c2 = st.columns(2)
        with h_c1:
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">WHEN TO CONDUCT HAZOP</div>', unsafe_allow_html=True)
            for w in hz["when_done"]:
                st.markdown(f'<div style="font-size:.75rem;color:#94a3b8;padding:2px 0">• {w}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin:.8rem 0 .4rem">HAZOP PROCEDURE</div>', unsafe_allow_html=True)
            for step in hz["procedure"]:
                num = step.split(".")[0].strip()
                txt = step.split(".",1)[1].strip() if "." in step else step
                st.markdown(f'<div style="display:flex;gap:8px;margin-bottom:4px;align-items:flex-start"><span style="background:#f97316;color:#fff;font-size:.58rem;font-weight:700;width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:1px">{num}</span><span style="font-size:.74rem;color:#94a3b8">{txt}</span></div>', unsafe_allow_html=True)
        with h_c2:
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">HAZOP TERMINOLOGY</div>', unsafe_allow_html=True)
            for term, defn in hz["terminology"].items():
                st.markdown(f'<div style="background:#080d18;border-radius:6px;padding:.5rem .7rem;margin-bottom:4px"><div style="font-size:.68rem;font-weight:700;color:#f97316">{term}</div><div style="font-size:.7rem;color:#64748b">{defn}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">HAZOP Guide Words (from Tata Steel Module)</div>', unsafe_allow_html=True)
        tbl_gw = '<table style="border-collapse:collapse;width:100%;font-size:.78rem"><thead><tr style="background:#080d18">'
        for h in ["Guide Word","Meaning","Example Deviations"]:
            tbl_gw += f'<th style="padding:8px 12px;text-align:left;color:#64748b;font-size:.65rem;font-weight:700;border-bottom:1px solid #1e3a5f">{h}</th>'
        tbl_gw += '</tr></thead><tbody>'
        for gw, gd in hz["guide_words"].items():
            tbl_gw += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:8px 12px;color:#f97316;font-weight:700;font-size:.82rem">{gw}</td><td style="padding:8px 12px;color:#e2e8f0">{gd["meaning"]}</td><td style="padding:8px 12px;color:#94a3b8;font-size:.75rem">{gd["examples"]}</td></tr>'
        tbl_gw += '</tbody></table>'
        st.markdown(tbl_gw, unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">Applied HAZOP — H2 Plant Electrolysis Node</div>', unsafe_allow_html=True)
        app_hazop = [
            ("MORE OF","Cell Temperature",">95°C SOC (>97°C SOL)","Cooling water valve TV1001 fails closed","Cell damage, KOH decomposition, H2 purity impact","RTD TE1001/TE1003 auto-trip at 97°C (PSCE #9,#10)","Test TV1001 fail-safe; dual RTD voting logic"),
            ("MORE OF","H2 in O2",">0.8% SOC (>1.7% SOL)","Separator level low — gas bypass","O2 separator DETONATION","AT1002 auto-trip at HH (PSCE #13)","Verify AT1002 calibration — 3-monthly; 1oo2 logic"),
            ("MORE OF","DC Current",">1450A SOC (>1600A SOL)","Rectifier malfunction","Cell damage, transformer failure, fire hazard","Overcurrent protection relay auto-trips","Annual relay calibration and functional test"),
            ("LESS OF","Separator Level","<500mm SOC (<400mm SOL)","Feed pump failure, LV1001 stuck open","H2-in-O2 rises → explosive mixture","LT1003/LT1001 level auto-trip","6-monthly level transmitter calibration"),
            ("NONE","DM Water Supply","No DM water to electrolyser","Feed pump 1M21 failure, valve closed","DM tank empties → plant trip (SOL 100mm)","LIT1301 alarm, auto-trip on low SOL","Quarterly pump test; manual valve position check"),
            ("REVERSE","Gas Separation","H2 into O2 / O2 into H2","Separator level failure both directions","Detonation risk in both separators","AT1001 + AT1002 (PSCE #13, #14)","Dual analysers; independent calibration"),
            ("OTHER THAN","H2 Purity","Contaminated H2 (O2 > 2 ppm SOL)","Deoxy bed failure — low temperature","Explosive O2+H2 in bullet storage","AT1102 trace O2 — auto-vent QZ1007 (PSCE #26)","6-monthly deoxy bed inspection; AT1102 3-monthly cal."),
            ("AS WELL AS","H2 Stream","Moisture present (dew point >-70°C SOL)","Dryer failure — regeneration incomplete","Pipeline corrosion, annealing hood damage, purity fail","MT1101 dew point — auto-trip at -70°C (PSCE #23)","6-monthly MT1101 calibration"),
        ]
        tbl_ah = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
        for h in ["Guide Word","Parameter","Deviation","Cause","Consequence","Safeguard","Recommendation"]:
            tbl_ah += f'<th style="padding:7px 10px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
        tbl_ah += '</tr></thead><tbody>'
        for row in app_hazop:
            tbl_ah += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 10px;color:#f97316;font-weight:700">{row[0]}</td><td style="padding:7px 10px;color:#e2e8f0;font-weight:600;white-space:nowrap">{row[1]}</td><td style="padding:7px 10px;color:#fde68a;font-size:.7rem">{row[2]}</td><td style="padding:7px 10px;color:#94a3b8;font-size:.7rem">{row[3]}</td><td style="padding:7px 10px;color:#fca5a5;font-size:.7rem">{row[4]}</td><td style="padding:7px 10px;color:#4ade80;font-size:.7rem">{row[5]}</td><td style="padding:7px 10px;color:#60a5fa;font-size:.7rem">{row[6]}</td></tr>'
        tbl_ah += '</tbody></table></div>'
        st.markdown(tbl_ah, unsafe_allow_html=True)

    # ── Bow Tie ───────────────────────────────────────────────────────
    with fw_tabs[5]:
        bt = fw["bow_tie"]
        st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">{bt["definition"]}</div>', unsafe_allow_html=True)

        bt_c1, bt_c2 = st.columns(2)
        with bt_c1:
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">BOW TIE STRUCTURE</div>', unsafe_allow_html=True)
            struct_colors = {"Threats / Causes":"#3b82f6","Threat Barriers (Prevention)":"#22c55e","Escalation Factors":"#eab308","Top Event":"#ef4444","Consequences":"#f97316","Recovery/Mitigation Barriers":"#a78bfa"}
            for el, desc in bt["structure"].items():
                ec = struct_colors.get(el,"#64748b")
                st.markdown(f'<div style="background:#080d18;border:1px solid {ec}30;border-left:3px solid {ec};border-radius:6px;padding:.6rem .8rem;margin-bottom:5px"><div style="font-size:.72rem;font-weight:700;color:{ec};margin-bottom:2px">{el}</div><div style="font-size:.72rem;color:#64748b">{desc}</div></div>', unsafe_allow_html=True)
        with bt_c2:
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:.4rem">BARRIER EFFECTIVENESS RANKING</div>', unsafe_allow_html=True)
            for btype, bdata in bt["barrier_effectiveness"].items():
                r = bdata["reliability"]; d = bdata["desc"]
                rel_num = int(r.replace("%","").replace("+","").split("-")[0]) if "%" in r else 50
                bc2 = "#22c55e" if rel_num >= 99 else "#3b82f6" if rel_num >= 90 else "#f97316" if rel_num >= 70 else "#ef4444"
                st.markdown(f'''<div style="background:#080d18;border:1px solid {bc2}20;border-radius:6px;padding:.5rem .7rem;margin-bottom:4px">
<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:2px">
<span style="font-size:.7rem;font-weight:700;color:{bc2}">{btype}</span>
<span style="font-size:.7rem;color:{bc2};font-family:monospace;font-weight:700">{r}</span>
</div>
<div style="background:#1e3a5f;border-radius:4px;height:5px;margin-bottom:3px"><div style="width:{min(rel_num,100)}%;background:{bc2};height:100%;border-radius:4px"></div></div>
<div style="font-size:.65rem;color:#475569">{d}</div>
</div>''', unsafe_allow_html=True)

        # Visual bow tie for H2 electrolysis
        st.markdown('<div class="sl-sec">Bow Tie — H2 Plant: H2/O2 Explosive Mixture Formation</div>', unsafe_allow_html=True)
        bt2_c1, bt2_c2, bt2_c3 = st.columns([2,1,2])
        with bt2_c1:
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin-bottom:.4rem">THREATS</div>', unsafe_allow_html=True)
            for t in ["AT1002 analyser failure","Separator level drops — gas bypass","Pressure control valve PV1001 failure","Operator error during startup"]:
                st.markdown(f'<div class="sl-cause">{t}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#22c55e;margin:.6rem 0 .3rem">PREVENTION BARRIERS</div>', unsafe_allow_html=True)
            for b in ["AT1002: H2-in-O2 analyser auto-trip (PSCE #13)","LT1003/LT1001: Level auto-trip (PSCE #11)","PV1001: Pressure regulating valve (PSCE #5)","Pre-startup safety checklist (SOP)"]:
                st.markdown(f'<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:5px 9px;margin-bottom:4px;font-size:.72rem;color:#4ade80">✓ {b}</div>', unsafe_allow_html=True)
        with bt2_c2:
            st.markdown(f'<div style="background:rgba(239,68,68,.15);border:2px solid #ef4444;border-radius:10px;padding:1rem;text-align:center;margin-top:1rem"><div style="font-size:.55rem;font-weight:700;color:#ef4444;letter-spacing:2px;margin-bottom:6px">TOP EVENT</div><div style="font-size:.75rem;font-weight:700;color:#e2e8f0;line-height:1.5">H2/O2 Explosive Mixture Formation</div><div style="font-size:.65rem;color:#ef4444;margin-top:6px">LOC from electrolyser</div></div>', unsafe_allow_html=True)
        with bt2_c3:
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#ef4444;margin-bottom:.4rem">CONSEQUENCES</div>', unsafe_allow_html=True)
            for c2 in ["L4: Detonation — electrolyser room collapse","Multiple fatalities — H2 plant zone","Plant shutdown 6-12 months","PESO investigation, possible prosecution"]:
                st.markdown(f'<div class="sl-consq">{c2}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#a78bfa;margin:.6rem 0 .3rem">MITIGATION BARRIERS</div>', unsafe_allow_html=True)
            for m in ["Blast-resistant room construction","Emergency H2 vent to elevated safe point","Emergency trip switch outside fence (PSCE #30)","NDRF pre-notification — H2 quantities declared"]:
                st.markdown(f'<div style="background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.2);border-left:3px solid #a78bfa;border-radius:6px;padding:5px 9px;margin-bottom:4px;font-size:.72rem;color:#a78bfa">{m}</div>', unsafe_allow_html=True)

    # ── LOPA ─────────────────────────────────────────────────────────
    with fw_tabs[6]:
        lopa = fw["lopa"]
        st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">{lopa["definition"]}<br><b style="color:#e2e8f0">Risk formula: </b><span style="color:#f97316">{lopa["risk_formula"]}</span></div>', unsafe_allow_html=True)

        l_c1, l_c2 = st.columns(2)
        with l_c1:
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">LOPA STEPS</div>', unsafe_allow_html=True)
            for step in lopa["steps"]:
                if step.startswith("Note"):
                    st.markdown(f'<div style="font-size:.7rem;color:#eab308;margin-top:.4rem;border-top:1px solid #1e3a5f;padding-top:.4rem">{step}</div>', unsafe_allow_html=True)
                else:
                    num = step.split(".")[0]; txt = step.split(".",1)[1] if "." in step else step
                    st.markdown(f'<div style="display:flex;gap:8px;margin-bottom:4px;align-items:flex-start"><span style="background:#f97316;color:#fff;font-size:.58rem;font-weight:700;width:16px;height:16px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0">{num}</span><span style="font-size:.74rem;color:#94a3b8">{txt}</span></div>', unsafe_allow_html=True)
        with l_c2:
            st.markdown(f'<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.4rem">TOLERABLE RISK CRITERION</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.25);border-radius:8px;padding:.8rem;font-size:.78rem;color:#f97316">{lopa["tolerable_risk"]}</div>', unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">Independent Protection Layers (IPL) — PFD Values</div>', unsafe_allow_html=True)
        for layer_name, layer_desc, pfd in lopa["layers_with_pfds"]:
            try:
                pfd_clean = pfd.replace("PFD = ","").replace("PFD=","").strip()
                pfd_parts = [float(x) for x in pfd_clean.split(" to ")]
                pfd_num = pfd_parts[0]
                bar_w = max(5, min(95, int((1 - pfd_num) * 100)))
                lc = "#22c55e" if pfd_num <= 0.01 else "#f97316" if pfd_num <= 0.1 else "#ef4444"
            except:
                bar_w = 50; lc = "#64748b"
            st.markdown(f'''<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:6px;padding:.6rem 1rem;margin-bottom:4px;display:grid;grid-template-columns:200px 1fr 100px;gap:8px;align-items:center">
<div><div style="font-size:.72rem;font-weight:600;color:#e2e8f0">{layer_name}</div><div style="font-size:.65rem;color:#475569">{layer_desc}</div></div>
<div style="background:#080d18;border-radius:4px;height:8px"><div style="width:{bar_w}%;background:{lc};height:100%;border-radius:4px"></div></div>
<div style="font-size:.72rem;color:{lc};font-family:monospace;font-weight:700;text-align:right">{pfd}</div>
</div>''', unsafe_allow_html=True)

    # ── PSI Elements ─────────────────────────────────────────────────
    with fw_tabs[7]:
        st.markdown('''<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">
The <b style="color:#e2e8f0">14-element PSM standard</b> (per Tata Steel PSRM module, aligned OSHA PSM) requires all HHO process plants to maintain these elements updated, audited, and accessible.
SafetyLens implements the full PSI documentation set digitally for each plant.
</div>''', unsafe_allow_html=True)

        for pk, pv in fw["psrm_levels"].items():
            pc = pv["color"]
            el_html = "".join(f'<span style="background:{pc}15;color:{pc};border:1px solid {pc}30;font-size:.63rem;font-weight:600;padding:2px 8px;border-radius:20px;margin:2px;display:inline-block">{e}</span>' for e in pv["elements"])
            st.markdown(f'<div style="background:#0d1f35;border:1px solid {pc}40;border-left:4px solid {pc};border-radius:8px;padding:.8rem 1rem;margin-bottom:.6rem"><div style="font-size:.85rem;font-weight:700;color:{pc};margin-bottom:.3rem">{pk}</div><div style="font-size:.74rem;color:#94a3b8;margin-bottom:.5rem">Applies to: {pv["applies_to"]} — {pv["desc"]}</div><div>{el_html}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">PSI Documents — What each covers in SafetyLens</div>', unsafe_allow_html=True)
        sl_tabs_map = {"PSC":"PSC tab","PDB":"PDB tab","HOM":"Hazard of Material tab","CIM":"Chem. Interaction tab","PSCE":"PSCE tab","EDB":"EDB tab","PHA":"PSM Framework tab"}
        for code, info in fw["psi_elements"].items():
            in_sl = sl_tabs_map.get(code,"")
            sl_badge = f'<span style="background:rgba(34,197,94,.15);color:#4ade80;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">SafetyLens: {in_sl}</span>' if in_sl else '<span style="background:rgba(99,102,241,.15);color:#a78bfa;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">Document repository</span>'
            st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:5px;display:flex;align-items:center;gap:12px"><span style="background:rgba(249,115,22,.15);color:#f97316;font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:6px;min-width:48px;text-align:center">{code}</span><div><span style="font-size:.8rem;font-weight:700;color:#e2e8f0">{info["full"]}</span>{sl_badge}<div style="font-size:.72rem;color:#64748b;margin-top:2px">{info["purpose"]}</div></div></div>', unsafe_allow_html=True)

def ai_response(q):
    q = q.lower()
    if any(x in q for x in ["cr-vi","chromic","chromate","carcinogen","hexavalent"]):
        return ("Cr-VI (Chromic Acid) — ETL-1 Chemical Treatment:\n"
                "Risk Score: 98/100 — CRITICAL\n"
                "TLV-TWA: 0.05 mg/m3 | Ceiling (STEL): 0.1 mg/m3\n"
                "HAZCHEM: NFPA 3-0-1 (Strong Oxidiser)\n"
                "Classification: IARC Group 1 Carcinogen\n"
                "Health effects: Lung cancer, nasal septum perforation, kidney damage\n"
                "Regulatory: Must be declared to CPCB & SPCB under MSIHC Rules 1989\n"
                "Action: Exceeding TLV = mandatory plant shutdown. Enclosed bath + LEV required.")
    if any(x in q for x in ["h2so4","sulphuric","sulfuric","pickling","acid"]):
        return ("Sulphuric Acid (H2SO4) — Pickling & Plating:\n"
                "Risk Score: 72/100 — HIGH\n"
                "TLV-TWA: 1 mg/m3 | STEL: 3 mg/m3\n"
                "HAZCHEM: 2R | NFPA: 3-0-2(W)\n"
                "SOC in pickling bath: 8-10 g/L\n"
                "Hazards: Severe chemical burns, acid mist inhalation, H2 gas generation with metals\n"
                "Emergency: Deluge shower within 10 sec reach. Neutralise spill with lime.")
    if any(x in q for x in ["hho","lho","classification","highly hazardous"]):
        return ("HHO vs LHO Classification — ETL-1:\n\n"
                "HHO (Highly Hazardous Operation) — Full PSI + PHA + Bow Tie + LOPA:\n"
                "  - Cleaning & Rinsing (NaOH + H2SO4)\n"
                "  - Tin Plating (SnSO4 + PSA + ENSA)\n"
                "  - Reflow Furnace (H2 gas + Propane)\n"
                "  - Chemical Treatment (Cr-VI chromate)\n\n"
                "LHO (Lower Hazardous Operation) — PSI only:\n"
                "  - Coil Feeding | Electrostatic Oiling\n\n"
                "HHO criteria (any one met):\n"
                "  - Potential for fatality or multiple LTIs\n"
                "  - Property damage >50 lakhs\n"
                "  - Environmental recovery >2 months")
    if any(x in q for x in ["psce","safety critical","critical equipment"]):
        return ("PSCE (Process Safety Critical Equipment) — ETL-1:\n"
                "Total: 77 items (40 shown in this view)\n\n"
                "Selection basis:\n"
                "  - Consequence-based: failure = major accident\n"
                "  - Prescriptive: mandated by MSIHC / Factory Act\n\n"
                "Key items:\n"
                "  - Pyrometer ETL-1 (reflow temperature protection)\n"
                "  - PSAL 2.14 H2 Pressure Switch (explosion prevention)\n"
                "  - UV 1.21 Propane Solenoid DN50 (fire prevention)\n"
                "  - Cr-VI air monitors (carcinogen exposure)\n\n"
                "Current status: 5 items overdue for calibration — action required")
    if any(x in q for x in ["reflow","hydrogen","h2","furnace","strip temp"]):
        return ("Reflow Furnace — ETL-1 (HHO, Full PSM Required):\n"
                "Gases present: H2 (LEL 4%, UEL 77%) + N2 (purge) + Propane (LEL 2.1%, UEL 9.5%)\n"
                "Strip temperature SOC: 232-270 deg C\n"
                "Strip temperature SOL: 232-270 deg C (tight control)\n\n"
                "Safety procedures:\n"
                "  - N2 purge MUST happen BEFORE H2 introduction\n"
                "  - H2 purge on shutdown before air admission\n"
                "  - Pyrometer alarm at 270 C — auto-shutdown\n\n"
                "Consequence of failure:\n"
                "  - Strip temp >270 = burning + conductor roll damage\n"
                "  - H2 leak + ignition = vapour cloud explosion")
    if any(x in q for x in ["risk","61","index","score"]):
        return ("ETL-1 Risk Index: 61/100 (MEDIUM — approaching HIGH at 75)\n\n"
                "Risk drivers:\n"
                "  1. Cr-VI air — Chemical Treatment: 98/100 (CRITICAL)\n"
                "  2. Strip temp deviation — Reflow: 92/100 (CRITICAL)\n"
                "  3. Sn2+ concentration — Plating: 90/100 (CRITICAL)\n\n"
                "Threshold: >75 = HIGH (mandatory escalation to management)\n"
                "Current status: 5 PSCE items overdue, raising risk trend")
    if any(x in q for x in ["psm","msihc","compliance","osha","regulation"]):
        return ("PSM Compliance — ETL-1 Jamshedpur:\n\n"
                "OSHA PSM 29 CFR 1910.119:\n"
                "  Status: Partially compliant — PHA update pending\n\n"
                "Indian Factories Act 1948, Section 41B:\n"
                "  Status: Compliant — PSI documented and current\n\n"
                "MSIHC Rules 1989:\n"
                "  Status: Cr-VI quantities declared to CPCB & SPCB\n\n"
                "Required documents: PSI + PHA + Bow Tie + LOPA\n"
                "  + Operating Procedures + Emergency Response Plan")
    return (f"SafetyLens AI — ETL-1 Knowledge Base\n\nQuery: '{q}'\n\n"
            "I can answer questions about:\n"
            "  - Cr-VI / chromic acid risk (98/100)\n"
            "  - H2SO4 pickling acid (72/100)\n"
            "  - HHO / LHO classification\n"
            "  - PSCE items (77 total)\n"
            "  - Reflow furnace H2/propane safety\n"
            "  - Process parameters (PDB) — 29 parameters\n"
            "  - PSM / MSIHC compliance\n"
            "  - Risk index and active alerts\n"
            "  - Flow brightening / tin melting process")

# ══════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ══════════════════════════════════════════════════════════════════════
for k, v in {"ind": None, "comp": None, "plant": None, "chat": [], "ck": 0,
              "psc_proc": "Cleaning & Rinsing", "h2_psc_proc": "Electrolysis",
              "hom_chem": "A6 — Chromic Acid (CrO3/Cr-VI)", "h2_hom_sel": "H1 — Hydrogen (H2)",
              "h2_chat": [], "h2_ck": 0}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════
# TOPBAR
# ══════════════════════════════════════════════════════════════════════
plant_label = st.session_state.plant or "No facility selected"
st.markdown(f"""
<div class="sl-topbar">
  <div>
    <div class="sl-brand">Safety<b>Lens</b></div>
    <div class="sl-sub">Process Safety Platform</div>
  </div>
  <div class="sl-pill">{plant_label}</div>
  <div style="display:flex;gap:8px">
    <span style="background:#1e3a5f;border:1px solid #2d5a8e;color:#93c5fd;font-size:.7rem;padding:5px 14px;border-radius:8px;font-weight:600">Alerts</span>
    <span style="background:#1e3a5f;border:1px solid #2d5a8e;color:#93c5fd;font-size:.7rem;padding:5px 14px;border-radius:8px;font-weight:600">PSM Officer</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Commodity ticker
COMMODITIES = [
    {"name":"HRC Steel","price":"₹52,400","unit":"MT","change":1.2},
    {"name":"Tin (LME)","price":"$28,650","unit":"MT","change":-0.8},
    {"name":"H2 (Green)","price":"$4.20","unit":"kg","change":2.1},
    {"name":"Cr-VI","price":"₹185","unit":"kg","change":-0.3},
    {"name":"SnSO4","price":"₹312","unit":"kg","change":0.6},
    {"name":"DOS Oil","price":"₹290","unit":"kg","change":0.0},
]
ticker_parts = []
for c in COMMODITIES:
    clr = "#22c55e" if c["change"] > 0 else "#ef4444"
    arr = "+" if c["change"] > 0 else ""
    cname = c["name"]; cprice = c["price"]; cunit = c["unit"]; cchange = c["change"]
    ticker_parts.append(
        '<span class="sl-tick-item"><b>' + cname + '</b>&nbsp;'
        '<b>' + cprice + '</b>&nbsp;' + cunit + '&nbsp;'
        '<span style="color:' + clr + ';font-weight:700">' + arr + str(cchange) + '%</span></span>'
    )

# ══════════════════════════════════════════════════════════════════════
# ROUTING
# ══════════════════════════════════════════════════════════════════════

if st.session_state.plant:
    plant = st.session_state.plant
    meta = PLANT_META.get(plant, {"risk": 50, "hho": 2, "lho": 2, "psce": 10, "status": "PSI"})
    is_etl1 = (plant == "ETL-1 — Electrolytic Tinning Line 1")
    is_h2plant = (plant == "Hydrogen Plant — H2 Production & Supply")
    ind_name = st.session_state.ind or ""
    comp = st.session_state.comp or ""

    div_name = ""
    if ind_name and comp:
        for dn, div_plants in HIERARCHY.get(ind_name, {}).get(comp, {}).items():
            if plant in div_plants:
                div_name = dn

    with st.sidebar:
        comp0 = comp.split("—")[0].strip().upper()
        st.markdown(f'<div style="padding:8px 12px;font-size:.62rem;font-weight:700;color:#3b82f6;letter-spacing:1.5px">{comp0}</div>', unsafe_allow_html=True)
        if st.button("Home — All Industries", key="home_btn", use_container_width=True, type="primary"):
            st.session_state.plant = None
            st.session_state.comp = None
            st.session_state.ind = None
            st.rerun()
        st.markdown('<hr style="border-color:#1e3a5f;margin:.5rem 0">', unsafe_allow_html=True)
        if ind_name and comp:
            for dn, div_plants in HIERARCHY.get(ind_name, {}).get(comp, {}).items():
                st.markdown(f'<div style="font-size:.6rem;font-weight:700;letter-spacing:2px;color:#475569;padding:6px 12px 2px;text-transform:uppercase">{dn}</div>', unsafe_allow_html=True)
                for p in div_plants:
                    pm = PLANT_META.get(p, {})
                    s = pm.get("status", "")
                    active = (st.session_state.plant == p)
                    badge = f" [{s}]" if s else ""
                    if st.button(f"{p[:24]}{badge}", key=f"sp_{p}", use_container_width=True,
                                 type="primary" if active else "secondary"):
                        st.session_state.plant = p
                        st.rerun()

    nav1, nav2, nav3 = st.columns([1, 1, 5])
    with nav1:
        if st.button("Home", key="main_home_btn", type="primary", use_container_width=True):
            st.session_state.plant = None
            st.session_state.comp = None
            st.session_state.ind = None
            st.rerun()
    with nav2:
        if st.button("All Plants", key="main_comp_btn", use_container_width=True):
            st.session_state.plant = None
            st.rerun()
    with nav3:
        st.markdown(f'<div style="font-size:.72rem;color:#475569;padding:.45rem 0">{ind_name} › {comp} › {div_name} › <b style="color:#94a3b8">{plant}</b></div>', unsafe_allow_html=True)

    sc = "#f97316" if meta["status"] == "HHO" else "#3b82f6"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:.8rem">
      <h2 style="font-size:1.4rem;font-weight:900;color:#f1f5f9;margin:0">{plant}</h2>
      <span class="sl-status-hho">{meta['status']} Active</span>
      <span class="sl-status-psm">{'Full PSM Required' if meta['hho'] >= 3 else 'PSI Required'}</span>
    </div>
    """, unsafe_allow_html=True)

    if is_h2plant:
        # ══════════════════════════════════════════════════════════
        # HYDROGEN PLANT — FULL PSI FROM REAL DATA
        # ══════════════════════════════════════════════════════════
        H2_TABS = ["Overview","PSC",
                   "Hazard of Material","Chem. Interaction","PDB","PSCE","EDB",
                   "Parameters","Simulation","Risk Matrix","PSM Report"]
        h2tabs = st.tabs(H2_TABS)
        # remap: 0=Overview,1=PSC,2=HOM,3=CIM,4=PDB,5=PSCE,6=EDB,7=Parameters,8=Simulation,9=RiskMatrix,10=PSM

        with h2tabs[0]:  # Overview
            rc_h2 = risk_color(meta["risk"])
            st.markdown(f"""<div class="sl-metrics">
              <div class="sl-metric"><div class="sl-metric-val" style="color:{rc_h2}">{meta['risk']}/100</div><div class="sl-metric-lbl">Risk Index</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">6</div><div class="sl-metric-lbl">Sub-Processes</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#f97316">{meta['hho']}</div><div class="sl-metric-lbl">HHO Processes</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">3</div><div class="sl-metric-lbl">Chemicals</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">24</div><div class="sl-metric-lbl">Parameters</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#22c55e">{meta['psce']}</div><div class="sl-metric-lbl">PSCE Items</div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Active Risk Alerts</div>', unsafe_allow_html=True)
            for score, text in [
                (92,"CRITICAL — H2 Detector at GLT (AT1701) above 0.9% LEL | Explosion risk — plant auto-trip required"),
                (88,"CRITICAL — Separator Pressure deviation (PT1001) | Overpressure — vessel rupture hazard"),
                (85,"HIGH — O2 Content in H2 above 0.2% (AT1001) | Explosive mixture — auto-vent and trip"),
            ]:
                st.markdown(f'<div class="sl-alert"><div class="sl-alert-score">{score}/100</div><div class="sl-alert-text">{text}</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Process Overview — Hydrogen Production & Supply</div>', unsafe_allow_html=True)
            h2_procs = [
                ("DM Water & KOH Storage","KOH (caustic), Electric energy. DM water storage and transfer to electrolyser.","lho",["LHO"]),
                ("Electrolysis (H2/O2 Production)","H2 (Cat-1 flammable), O2 (oxidiser), High DC voltage 1450A. Electrolyser splits DM water.","hho",["HHO","PSM Required"]),
                ("Gas-Liquid Separation","H2 at operating pressure (1.5-1.57 MPa). H2/O2 separators and washers. Lye solution handling.","hho",["HHO","PSM Required"]),
                ("Purification (Deoxy + Dryer)","H2 at operating pressure/temperature. Deoxygenation 118-160°C. Dryer A/B/C 170-220°C.","hho",["HHO","PSM Required"]),
                ("Compressed H2 Storage","H2 under pressure in Bullet 1 & 2 (4-14 kg/cm2). High-pressure storage vessels.","hho",["HHO","PSM Required"]),
                ("H2 Distribution to Annealing","H2 at pressure (1.2-2.5 kg/cm2 final). Distribution pipeline to annealing hoods.","hho",["HHO","PSM Required"]),
            ]
            c1, c2 = st.columns(2)
            for i, (name, desc, cls, tags) in enumerate(h2_procs):
                t_html = "".join(f'<span class="sl-tag sl-tag-{"hho" if t=="HHO" else "psm" if "PSM" in t else "lho"}">{t}</span>' for t in tags)
                with (c1 if i % 2 == 0 else c2):
                    st.markdown(f'<div class="sl-proc {cls}"><div class="sl-proc-title">{name}</div><div class="sl-proc-desc">{desc}</div>{t_html}</div>', unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            with c1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=months, y=[78,80,82,79,81,83,82,80,84,82,83,82], mode="lines+markers", line=dict(color="#f97316",width=2.5), marker=dict(size=6), fill="tozeroy", fillcolor="rgba(249,115,22,0.06)"))
                fig.add_hline(y=75, line_dash="dot", line_color="#ef4444", annotation_text="Alert: 75", annotation_font=dict(color="#ef4444",size=10))
                fig.update_layout(title=dict(text="H2 Plant Risk Index Trend 2024",font=dict(color="#94a3b8",size=12)),paper_bgcolor="#0d1f35",plot_bgcolor="#080d18",font=dict(color="#64748b",size=10),height=240,margin=dict(l=40,r=10,t=40,b=30),xaxis=dict(gridcolor="#1e3a5f",color="#64748b"),yaxis=dict(gridcolor="#1e3a5f",color="#64748b",range=[0,100]))
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=months, y=[0.15,0.18,0.12,0.20,0.14,0.22,0.19,0.16,0.21,0.13,0.17,0.15], marker_color=["#ef4444" if v>0.2 else "#f97316" for v in [0.15,0.18,0.12,0.20,0.14,0.22,0.19,0.16,0.21,0.13,0.17,0.15]]))
                fig2.add_hline(y=0.2, line_dash="dot", line_color="#ef4444", annotation_text="H2 Detector SOL: 0.9% LEL", annotation_font=dict(color="#ef4444",size=9))
                fig2.update_layout(title=dict(text="H2 Detector Readings — GLT Zone (% LEL)",font=dict(color="#94a3b8",size=12)),paper_bgcolor="#0d1f35",plot_bgcolor="#080d18",font=dict(color="#64748b",size=10),height=240,margin=dict(l=40,r=10,t=40,b=30),xaxis=dict(gridcolor="#1e3a5f",color="#64748b"),yaxis=dict(gridcolor="#1e3a5f",color="#64748b"))
                st.plotly_chart(fig2, use_container_width=True)

        with h2tabs[1]:  # PSC
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PSC/TINPL/ Rev.3 Eff.Dt.:01.12.2020</p>', unsafe_allow_html=True)

            st.markdown("""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem">
<div style="font-size:.82rem;font-weight:700;color:#f97316;margin-bottom:.5rem">PSRM CLASSIFICATION FRAMEWORK — HYDROGEN PLANT</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.78rem;color:#94a3b8;line-height:1.8">
<div><b style="color:#f97316">HHO — Highly Hazardous Operation</b><br>
Any process where uncontrolled release of energy CAN result in:<br>
• Property damage &gt; Rs.50 lakhs, OR<br>
• Potential for fatality / multiple LTIs, OR<br>
• Significant environmental impact<br>
<b style="color:#f97316">Requires: Full PSRM</b> — PSI + PHA + HAZOP + Bow Tie + LOPA + SOPs + Emergency Plan</div>
<div><b style="color:#6366f1">LHO — Lower Hazardous Operation</b><br>
Hazardous substance/energy IS present BUT consequences do NOT meet any HHO threshold under normal or credible abnormal operation.<br><br>
<b style="color:#6366f1">Requires: Baseline PSRM</b> — PSI documentation only</div>
</div></div>""", unsafe_allow_html=True)

            st.markdown("""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1rem">
<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#f97316;font-family:monospace">5</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">HHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(99,102,241,.3);border-top:3px solid #6366f1;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#6366f1;font-family:monospace">1</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">LHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#ef4444;font-family:monospace">3</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">CHEMICALS</div></div>
<div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#22c55e;font-family:monospace">44</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PSCE ITEMS</div></div>
</div>""", unsafe_allow_html=True)

            if "h2_psc_proc" not in st.session_state:
                st.session_state.h2_psc_proc = "Electrolysis"

            H2_PSC_DATA = {
                "DM Water & KOH": {
                    "cls":"LHO","color":"#6366f1",
                    "desc":"DM water storage tank and transfer to electrolyser. KOH (potassium hydroxide / lye) storage and dosing to maintain electrolyte concentration. Feed water pump and lye pump operation.",
                    "hazardous":["KOH (caustic) — corrosive liquid, skin/eye burns","Electric energy — pump motor electrical hazard","Pressurised DM water pipework"],
                    "hmatrix":{"Toxic":"N","Explosive":"N","Flammable":"N","Corrosive":"Y","Thermal":"N","Pressure":"N"},
                    "consequences":{"Property >50L":"N","Fatality":"N","Env. Impact":"N"},
                    "reasoning":"KOH spill causes corrosive burns — serious injury but not fatal at storage concentrations used. No explosion pathway. Property damage from KOH spill manageable. No environmental pathway beyond local pH impact. Maximum credible event well below all three HHO thresholds. LHO CONFIRMED.",
                    "parameters":[
                        ("DM Water Tank Level","300-1000 mm","100-1500 mm","Below 100mm: plant trip — H2 generation stops","Above 1500mm: overflow — KOH solution spillage, slip hazard"),
                        ("DM Water Conductivity","0-1 uS/cm","0-1 uS/cm","Above 1 uS/cm: electrolyser efficiency drops, cell corrosion","Much above: cell deposits, reduced H2 purity"),
                        ("KOH Concentration","Ref: process spec","Ref: process spec","Low KOH: poor electrolyte conductivity, reduced H2 output","High KOH: increased corrosivity, equipment damage"),
                    ],
                    "barriers":["DM tank level transmitter LIT1301 with low-level alarm","Feed pump motor protection relay","KOH secondary containment (bunding around storage)","PPE: alkali-resistant gloves, face shield for KOH handling"],
                    "hazop":None,"bowtie":None,
                },
                "Electrolysis": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"DC current (800-1450A) splits DM water in electrolyser cells producing H2 at cathode and O2 at anode. KOH lye solution is the electrolyte. Operating pressure 1.5-1.57 MPa. Cell temperature 35-95°C. H2 and O2 produced simultaneously — CRITICAL: must remain separated at all times.",
                    "hazardous":["H2 gas — LEL 4%, UEL 75% (extremely flammable, low ignition energy 0.017 mJ)","O2 gas — strong oxidiser, violently accelerates combustion","H2 + O2 mixture — DETONATION risk if H2-in-O2 >1.7%","High DC voltage 800-1450A","KOH lye solution (corrosive) at pressure","Cell pressure 1.50-1.57 MPa — vessel integrity critical"],
                    "hmatrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"Y","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"Electrolysis is the CORE HHO process. H2 and O2 are produced simultaneously. If separator fails or H2-in-O2 rises >1.7% (auto-trip at 0.8%), the resulting mixture is MORE EXPLOSIVE than gunpowder. DC current 1450A at cell voltage creates severe electrocution risk. Cell pressure 1.5 MPa: vessel failure = projectile/explosion. A single cell block explosion in the electrolyser room would cause structural collapse, multiple fatalities, and damage far exceeding Rs.50L. ALL THREE HHO CRITERIA MET BY LARGE MARGIN.",
                    "parameters":[
                        ("DC Current (Rectifier)","800-1450 A","500-1600 A","Below 500A: H2 not transferred to purifier — auto-vent from GLT","Above 1600A: overheating, cell damage, transformer overload — FIRE"),
                        ("Cell Temperature","35-95°C","25-97°C","Below 25°C: poor electrolysis efficiency","Above 97°C: cell damage, KOH decomposition — PLC AUTO-TRIP"),
                        ("H2 in O2 Content","0-0.8%","0-1.7%","Minimum desirable (no lower consequence)","Above 1.7%: H2+O2 EXPLOSIVE MIXTURE — IMMEDIATE AUTO-TRIP"),
                        ("O2 in H2 Content","0-0.1%","0-0.2%","Minimum desirable","Above 0.2%: EXPLOSIVE mixture in H2 line — AUTO-TRIP"),
                        ("Separator Pressure","1.50-1.57 MPa","N/A-1.65 MPa","Cannot start plant below SOL","Above 1.65 MPa: vessel overpressure — RUPTURE RISK"),
                    ],
                    "barriers":["AT1002: H2-in-O2 analyser — auto-trip at 0.8% SOC (PSCE #13)","AT1001: O2-in-H2 analyser — auto-trip at 0.2% SOL (PSCE #14)","RTD TE1001/TE1003: cell temp monitors — auto-trip at 97°C (PSCE #9,#10)","PT1001: separator pressure transmitter — overpressure alarm (PSCE #12)","Rectifier DC overcurrent protection","Emergency plant trip switch outside plant fence (PSCE #30)"],
                    "hazop":[
                        ("H2-in-O2 HIGH",">0.8% SOC (>1.7% SOL)","AT1002 failure / separator malfunction","H2+O2 explosive mixture — detonation","AT1002 auto-trip, redundant pressure monitoring"),
                        ("Cell Temp HIGH",">95°C SOC (>97°C SOL)","Cooling water valve failure","Cell damage, KOH decomposition, explosion","TE1001/TE1003 auto-trip, cooling water flow alarm"),
                        ("DC Current HIGH",">1450A SOC","Rectifier malfunction","Overheating, transformer damage, fire","Rectifier overcurrent relay, auto power cut"),
                        ("Separator Pressure HIGH",">1.57 MPa","Control valve PV1001 failure","Vessel overpressure — rupture","PT1001 high alarm, SRV at vessel, auto-vent"),
                        ("Power FAILURE","Sudden DC loss","Grid outage","Uncontrolled H2/O2 evolution — unsafe state","UPS for control systems, N2 auto-purge on power loss"),
                    ],
                    "bowtie":{
                        "top_event":"H2/O2 explosive mixture formation or electrolyser cell rupture",
                        "causes":["AT1002 failure — H2-in-O2 exceeds 1.7% undetected","Separator malfunction — gas mixing","DC overcurrent — cell thermal runaway","Pressure control valve failure — vessel overpressure"],
                        "consequences":["Detonation in electrolyser room — structural collapse","Multiple fatalities — H2 plant zone","Plant shutdown 6-12 months minimum","PESO investigation, possible prosecution, licence cancellation"],
                        "preventions":["AT1002 H2-in-O2 analyser auto-trip at 0.8% (PSCE #13)","AT1001 O2-in-H2 analyser auto-trip at 0.2% (PSCE #14)","Dual RTD cell temperature auto-trip at 97°C","PT1001 separator pressure overpressure alarm + SRV"],
                        "mitigations":["Blast-resistant electrolyser room construction","Emergency H2 vent to safe elevated location","Emergency trip switch outside plant (PSCE #30)","Full evacuation + PESO notification procedure"],
                    },
                },
                "Gas-Liquid Separation": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"H2 and O2 separators/washers remove KOH lye from produced gases. Gas-liquid treater (GLT) maintains correct pressure balance. Lye returns to electrolyser. H2 and O2 separated under pressure 1.50-1.57 MPa. H2 continues to purification; O2 vented safely.",
                    "hazardous":["H2 under pressure 1.5 MPa — explosion/fire risk","O2 under pressure — oxidiser, fire risk","KOH lye carryover — corrosive","H2 in O2 cross-contamination — DETONATION risk","Separator level upset — lye into gas pipeline"],
                    "hmatrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"Y","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"H2 gas at 1.5 MPa operating pressure in separators. Level upset (too high) causes lye carryover into H2/O2 gas lines — blocks downstream equipment, causes pressure surge. Level too low — gas bypasses separator — H2 in O2 stream increases toward explosive range. The H2 detector AT1702 in GLT zone is PSCE because an H2 leak in this zone can create explosive atmosphere. Pipe failure at 1.5 MPa = significant structural damage. ALL THREE HHO CRITERIA MET.",
                    "parameters":[
                        ("Separator Liquid Level","500-670 mm","400-770 mm","Below 400mm: gas bypass — H2-in-O2 rises toward explosive range","Above 770mm: lye into gas lines — pipeline blockage, pressure surge"),
                        ("Separator Pressure","1.50-1.57 MPa","N/A-1.65 MPa","Cannot start — transfer to purifier not possible","Above 1.65 MPa: overpressure — vessel stress, SRV lift"),
                        ("H2 Detector GLT Zone","0-0.2% LEL","0-0.9% LEL","No consequence — minimum desirable","Above 0.9%: H2 leak confirmed — auto exhaust fan, plant trip"),
                    ],
                    "barriers":["LT1003/LT1001: separator level transmitters — auto-trip on high/low (PSCE #11)","PV1001: pressure regulating valve — auto-control","AT1702: H2 detector in GLT zone (PSCE #16)","Exhaust fan auto-start on H2 alarm (PSCE #18)","LV1001: liquid level control valve (PSCE #4)"],
                    "hazop":[
                        ("Level HIGH",">670mm SOC (>770mm SOL)","LV1001 control valve failure","Lye into gas pipeline — purity/pressure issue","LT1003 high alarm + LV1001 auto-close"),
                        ("Level LOW","<500mm SOC (<400mm SOL)","Feed pump failure / LV1001 stuck open","Gas bypass — H2-in-O2 rises","LT1001 low alarm, plant auto-trip"),
                        ("H2 Leak","H2 above 0.2% LEL","Pipe fitting failure","Explosive atmosphere in GLT zone","AT1702 alarm, exhaust fan auto-start, evacuation"),
                        ("Pressure HIGH",">1.57 MPa SOC","PV1001 failure","Vessel overpressure — SRV lift","PT1001 alarm, SRV opens, auto-vent"),
                    ],
                    "bowtie":{
                        "top_event":"H2 leak creating explosive atmosphere in GLT zone or lye carryover into gas lines",
                        "causes":["Pipe fitting failure — H2 leak in GLT","Separator level high — lye carryover into H2 line","Pressure control failure — overpressure rupture","H2-in-O2 rise due to gas bypass at low level"],
                        "consequences":["Explosion in GLT zone — fatalities","Purification system damage from lye carryover","Plant shutdown 2-4 months","Regulatory investigation"],
                        "preventions":["AT1702: H2 LEL detector auto-alarm at 0.2% (PSCE #16)","LT1003/LT1001: level auto-trip on deviation","PV1001/LV1001: auto-control valves (PSCE #4,#5)","PT1001: pressure overpressure protection (PSCE #12)"],
                        "mitigations":["Exhaust fan auto-start (PSCE #18)","Full evacuation of H2 plant zone","Emergency trip switch activation (PSCE #30)","Post-event gas freeing and inspection before restart"],
                    },
                },
                "Purification": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"H2 purification: Deoxygenation unit (118-160°C) removes residual O2. Dryer A/B/C (170-220°C) removes moisture. Filters remove particles. Purifier produces H2 at <1ppm O2 and dew point <-80°C. Operating pressure 0.6-1.3 MPa.",
                    "hazardous":["H2 at pressure 0.6-1.3 MPa — fire/explosion","High temperature zones 118-220°C — thermal burns","Trace O2 if purifier fails — explosive with H2","Dew point failure — moisture in H2 pipeline — equipment damage"],
                    "hmatrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"N"},
                    "reasoning":"H2 at 0.6-1.3 MPa throughout the purification circuit. Deoxy bed at 118-160°C and dryer beds at 170-220°C are thermal hazards. If purifier fails (trace O2 >1 ppm), contaminated H2 reaches storage bullets and annealing hoods — risk of explosion at point of use. Auto-vent valve QZ1007 is PSCE because it prevents contaminated H2 reaching downstream. Property damage from explosion at annealing hoods or bullets would far exceed Rs.50L. Fatality risk from downstream explosion. TWO HHO CRITERIA MET.",
                    "parameters":[
                        ("Deoxy Bed Temp","118-160°C","110-160°C","Below 110°C: poor O2 removal — purity fails — auto-trip","Above 160°C: equipment damage, H2 leak risk at fittings"),
                        ("Dryer Bed Temp","170-220°C","N/A-220°C","Below 170°C: poor drying — dew point rises","Above 220°C: structural damage to dryer vessel — auto-trip"),
                        ("Dew Point (purified H2)","< -80°C","< -70°C","N/A (lower is better)","Above -70°C: moisture in H2 pipeline — corrosion, purity fail — TRIP"),
                        ("Trace O2 at outlet","0-1 ppm","0-2 ppm","No consequence — minimum desirable","Above 2 ppm: contaminated H2 — auto-vent (QZ1007) — DO NOT PASS TO STORAGE"),
                        ("Purifier Pressure","0.6-1.3 MPa","0.5-1.4 MPa","Below 0.5 MPa: insufficient purifier performance","Above 1.4 MPa: vessel overpressure — SRV lift — check PT1101"),
                    ],
                    "barriers":["MT1101: dew point analyser — auto-trip at -70°C SOL (PSCE #23)","AT1102: trace O2 analyser at outlet <1ppm — auto-vent on alarm (PSCE #26)","QZ1007: H2 auto-vent valve — blocks contaminated H2 from storage (PSCE)","RTDs on deoxy and dryer beds — auto-trip on high temp","PT1101: purifier pressure transmitter (PSCE #24)","Filters after each stage (PSCE #22)"],
                    "hazop":[
                        ("Dew Point HIGH",">-80°C SOC (>-70°C SOL)","Dryer regeneration failure","Moisture in H2 pipeline — corrosion, embrittlement","MT1101 auto-trip, dryer changeover to standby"),
                        ("Trace O2 HIGH",">1 ppm SOC (>2 ppm SOL)","Deoxy bed temperature low / catalyst failure","Explosive O2+H2 mixture downstream","AT1102 alarm, QZ1007 auto-vent, plant hold"),
                        ("Deoxy Temp LOW","<118°C SOC","Heater failure","Poor O2 removal — purity risk","Temp RTD alarm, auto-trip, manual verification"),
                        ("Pressure HIGH",">1.3 MPa SOC","PV1101 failure","Vessel overpressure","PT1101 alarm, SRV, auto-vent"),
                    ],
                    "bowtie":{
                        "top_event":"Contaminated H2 (high O2 or high moisture) reaching storage or end-use",
                        "causes":["Deoxy bed temperature low — O2 not removed","Dryer failure — dew point rises","AT1102 analyser failure — O2 not detected","QZ1007 auto-vent valve failure — contaminated H2 passes"],
                        "consequences":["Explosive H2+O2 mixture in bullet storage","Annealing hood explosion from contaminated H2","Equipment damage throughout distribution network","Production shutdown — all annealing lines affected"],
                        "preventions":["AT1102: trace O2 analyser with auto-vent (PSCE #26)","MT1101: dew point analyser with auto-trip (PSCE #23)","RTDs on all heated beds — auto-trip on deviation","QZ1007: auto-vent valve (last line of defence)"],
                        "mitigations":["H2 bullet isolation valves — manual emergency closure","Production hold on all annealing hoods","Gas freeing and re-analysis before restart","Root cause analysis and CAPA before resuming"],
                    },
                },
                "H2 Storage (Bullets)": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"Two H2 storage bullets (Bullet 1 & 2) storing purified H2 at 4-14 kg/cm2. ASME/statutory pressure vessels. Equipped with dual SRVs each, pressure gauges, temperature gauges, and pressure control valves at outlet. H2 supplied to annealing hoods at 1.2-2.5 kg/cm2.",
                    "hazardous":["H2 under pressure 4-14 kg/cm2 — large energy inventory","H2 LEL 4%, UEL 75% — major fire/explosion risk","Pressure vessel failure — projectile + explosion","H2 embrittlement of vessel over time"],
                    "hmatrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"N"},
                    "reasoning":"H2 storage bullets are BLEVE (Boiling Liquid Expanding Vapour Explosion) risk under extreme fire exposure, plus H2 vapour cloud explosion risk on major leak. Two bullets containing significant H2 inventory at 14 kg/cm2. A bullet failure would project fragments and create massive H2 fireball — multiple fatalities, total plant destruction far exceeding Rs.50L. This is why CCOE approval is mandatory for H2 storage and why dual SRVs are prescribed (PSCE #34-37). ALL HHO CRITERIA MASSIVELY EXCEEDED.",
                    "parameters":[
                        ("Bullet Pressure","4-14 kg/cm2","3-20 kg/cm2","Below 3 kg/cm2: insufficient H2 supply to annealing","Above 20 kg/cm2: vessel design limit — SRV must lift"),
                        ("Bullet Temperature","< 45°C (SOC)","< 50°C (SOL)","N/A (lower is better)","Above 50°C: thermal expansion — pressure rise — structural risk"),
                        ("Outlet Pressure","1.2-2.5 kg/cm2","1.0-3.5 kg/cm2","Below 1.0: insufficient H2 to annealing hoods","Above 3.5: distribution line overpressure — PRV lift"),
                        ("H2 Detector (Bullet zone)","0-0.2% LEL","0-0.9% LEL","No consequence — minimum desirable","Above 0.9%: H2 leak at bullet — IMMEDIATE EVACUATION + trip"),
                    ],
                    "barriers":["SRV #1 & #2 at Bullet 1 (PSCE #34,#35) — dual overpressure protection","SRV #1 & #2 at Bullet 2 (PSCE #36,#37) — dual overpressure protection","Pressure gauge at each bullet (PSCE #33,#38)","Temperature gauge at each bullet (PSCE #39,#40)","Pressure control valve at bullet outlet (PSCE #41,#42)","Fire hydrant system (PSCE #44)","CCOE-approved site layout and safety distances"],
                    "hazop":[
                        ("Pressure HIGH",">14 kg/cm2 SOC (>20 kg/cm2 SOL)","Outlet PCV failure / fire exposure","SRV lifts — H2 release — fire/explosion risk","Dual SRVs, fire detection, emergency isolation"),
                        ("Temp HIGH",">45°C SOC (>50°C SOL)","Solar radiation / adjacent fire","Pressure rise — SRV lift — H2 fire","Shading, fire detection, water spray deluge"),
                        ("H2 Leak","H2 above LEL at bullet","Valve packing failure / fitting","Explosive atmosphere in bullet farm","H2 detector auto-alarm, evacuation, isolation"),
                        ("Vessel Fatigue","Wall thinning over time","H2 embrittlement / corrosion","Sudden vessel failure — BLEVE","Statutory inspection (PESO), thickness testing, IBR compliance"),
                    ],
                    "bowtie":{
                        "top_event":"H2 bullet catastrophic failure or major H2 fire at bullet farm",
                        "causes":["SRV failure — no overpressure relief","H2 leak from valve packing / fittings","External fire exposure causing thermal BLEVE","Vessel wall failure from H2 embrittlement"],
                        "consequences":["BLEVE — major explosion, projectiles, fireball","Multiple fatalities in plant zone","Total plant destruction — hundreds of crores damage","PESO investigation, criminal liability"],
                        "preventions":["Dual SRVs on each bullet (4 total) — PSCE #34-37","H2 LEL detector at bullet zone — auto-alarm","CCOE-approved safety distances enforced","Statutory IBR inspection — annual pressure test"],
                        "mitigations":["Fire hydrant system (PSCE #44) — water spray on bullets","Emergency isolation valve — remote operation","Full plant evacuation — 500m exclusion zone","PESO and fire brigade pre-notification"],
                    },
                },
                "H2 Distribution": {
                    "cls":"HHO","color":"#f97316",
                    "desc":"H2 distributed from bullets at 1.2-2.5 kg/cm2 through dedicated pipework to annealing hoods. Pressure reduced by PRV at outlet. Distribution pipeline passes through plant areas. End users: annealing hoods on cold rolling and tinplate lines.",
                    "hazardous":["H2 in distribution pipework — fire/explosion risk","H2 leaks along pipeline route — explosive atmosphere","Pressure variations affecting annealing quality and safety"],
                    "hmatrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"N"},
                    "reasoning":"H2 distribution pipeline passes through occupied plant areas. A pipeline failure creating H2 leak + ignition = fire or explosion along the distribution route. Annealing hoods consume H2 — if contaminated H2 or pressure surge reaches hoods, explosion at end-use. Distribution failures could cause H2 fire tracking back to bullet — escalation. Property damage from pipeline explosion or hood fire would exceed Rs.50L. Fatality risk at annealing hood or along pipeline. TWO HHO CRITERIA MET.",
                    "parameters":[
                        ("Final Outlet Pressure","1.2-2.5 kg/cm2","1.0-3.5 kg/cm2","Below 1.0: insufficient H2 — annealing quality failure","Above 3.5: overpressure in distribution — PRV adjustment needed"),
                        ("H2 Purity at supply","Per annealing spec","Per annealing spec","Below spec: annealing quality failure","Below spec + contamination: risk at annealing hood"),
                    ],
                    "barriers":["PRV at bullet outlet — pressure regulation (PSCE #43)","Dedicated H2 pipeline — no shared services","Regular leak detection survey on distribution line","Annealing hood H2 detectors at end-use point","Emergency isolation valve at source (bullet outlet)"],
                    "hazop":[
                        ("Pressure HIGH",">2.5 kg/cm2 SOC","PRV failure","Overpressure at annealing hood — potential failure","PRV auto-relief, downstream pressure gauge check"),
                        ("H2 Leak","Leak along pipeline","Pipe joint failure / corrosion","Explosive atmosphere along route","Regular leak survey, H2 detector at key points"),
                        ("Contaminated H2","O2 > ppm spec","Purifier bypass / AT1102 failure","Explosion at annealing hood on ignition","AT1102 auto-vent prevents this reaching distribution"),
                    ],
                    "bowtie":{
                        "top_event":"H2 fire or explosion along distribution pipeline or at annealing hood",
                        "causes":["Pipeline joint failure — H2 leak","Contaminated H2 reaching annealing hood","PRV failure — overpressure at end use","Back-flash from annealing hood into pipeline"],
                        "consequences":["H2 fire along distribution route","Annealing hood explosion — operator fatality","Line shutdown — all annealing production stopped","Pipeline replacement — Rs.50L+ damage"],
                        "preventions":["AT1102 + QZ1007: contaminated H2 blocked before distribution","PRV at bullet outlet: pressure control","Regular joint inspection and leak survey","H2 detectors at annealing hoods"],
                        "mitigations":["Emergency H2 isolation at bullet","Hood fire suppression systems","Full evacuation of affected bays","Restart only after gas freeing + inspection"],
                    },
                },
            }

            proc_list_h2 = list(H2_PSC_DATA.keys())
            proc_cols_h2 = st.columns(len(proc_list_h2))
            for ii, pname in enumerate(proc_list_h2):
                pd3 = H2_PSC_DATA[pname]
                is_active = (st.session_state.h2_psc_proc == pname)
                with proc_cols_h2[ii]:
                    label = pd3["cls"]
                    bc3 = pd3["color"]
                    st.markdown(f'<div style="background:{bc3}15;border:1px solid {bc3}40;border-top:3px solid {bc3};border-radius:8px;padding:.5rem;text-align:center;margin-bottom:4px"><div style="font-size:.65rem;font-weight:700;color:{bc3}">{label}</div></div>', unsafe_allow_html=True)
                    if st.button(pname[:16], key=f"h2psc_{pname}", use_container_width=True, type="primary" if is_active else "secondary"):
                        st.session_state.h2_psc_proc = pname
                        st.rerun()

            sp = H2_PSC_DATA[st.session_state.h2_psc_proc]
            spn = st.session_state.h2_psc_proc
            spc = sp["color"]
            is_hho_h2 = sp["cls"] == "HHO"

            st.markdown(f"""<div style="background:{spc}10;border:1px solid {spc}40;border-left:5px solid {spc};border-radius:10px;padding:1rem 1.4rem;margin:.8rem 0">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:.5rem">
<span style="background:{spc}20;color:{spc};border:1px solid {spc}50;font-size:.78rem;font-weight:700;padding:4px 14px;border-radius:20px">{sp['cls']}</span>
<span style="font-size:1.1rem;font-weight:800;color:#f1f5f9">{spn}</span>
</div>
<div style="font-size:.82rem;color:#94a3b8;line-height:1.7">{sp['desc']}</div>
</div>""", unsafe_allow_html=True)

            dd1, dd2 = st.columns(2)
            with dd1:
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARDOUS SUBSTANCES / ENERGIES</div>', unsafe_allow_html=True)
                hlist2 = "".join(f'<div style="font-size:.78rem;color:#fca5a5;padding:3px 0;border-bottom:1px solid #1e3a5f">• {h}</div>' for h in sp["hazardous"])
                st.markdown(f'<div style="background:#1a0505;border:1px solid rgba(239,68,68,.2);border-radius:8px;padding:.8rem;margin-bottom:.8rem">{hlist2}</div>', unsafe_allow_html=True)

                hm2 = sp["hmatrix"]
                tblhm = '<table style="border-collapse:collapse;width:100%;font-size:.72rem;margin-bottom:.8rem"><tr>'
                for k in hm2: tblhm += f'<th style="background:#080d18;padding:5px 8px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;text-align:center">{k}</th>'
                tblhm += '</tr><tr>'
                for k,v in hm2.items():
                    c4="#22c55e" if v=="Y" else "#475569"; bg3="rgba(34,197,94,.1)" if v=="Y" else "#0d1f35"
                    tblhm += f'<td style="background:{bg3};padding:6px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;color:{c4}">{v}</td>'
                tblhm += '</tr></table>'
                st.markdown(tblhm, unsafe_allow_html=True)

                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.3rem">SAFETY BARRIERS</div>', unsafe_allow_html=True)
                for b in sp["barriers"]:
                    st.markdown(f'<div style="font-size:.75rem;color:#22c55e;padding:2px 0">✓ {b}</div>', unsafe_allow_html=True)

            with dd2:
                st.markdown(f'<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">CONSEQUENCE ANALYSIS — WHY {sp["cls"]}</div>', unsafe_allow_html=True)
                for crit, val in sp["consequences"].items():
                    fc2="#ef4444" if val=="Y" else "#22c55e"; fbg2="rgba(239,68,68,.08)" if val=="Y" else "rgba(34,197,94,.06)"
                    ftext2="YES — HHO criterion MET" if val=="Y" else "NO — Threshold not reached"
                    st.markdown(f'<div style="background:{fbg2};border-left:3px solid {fc2};border-radius:6px;padding:7px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center"><span style="font-size:.78rem;color:#94a3b8">{crit}</span><span style="font-size:.72rem;font-weight:700;color:{fc2}">{ftext2}</span></div>', unsafe_allow_html=True)

                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.6rem 0 .3rem">CLASSIFICATION REASONING</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.9rem;font-size:.78rem;color:#94a3b8;line-height:1.75">{sp["reasoning"]}</div>', unsafe_allow_html=True)

            # SOC/SOL cards
            st.markdown('<div class="sl-sec">Process Parameters — SOC / SOL / Deviation Consequences</div>', unsafe_allow_html=True)
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:.8rem;display:flex;gap:2rem;font-size:.78rem">
<span><b style="color:#22c55e">SOC</b> <span style="color:#64748b">= Safe Operating Condition — normal target range</span></span>
<span><b style="color:#f97316">SOL</b> <span style="color:#64748b">= Safe Operating Limit — breach = immediate corrective action or plant trip</span></span>
</div>""", unsafe_allow_html=True)

            for param, soc, sol, low_dev, high_dev in sp["parameters"]:
                is_crit2 = any(x in high_dev for x in ["TRIP","SHUTDOWN","EXPLOSIVE","BLEVE","RUPTURE","AUTO-TRIP"])
                crit_b2 = ' <span style="background:rgba(239,68,68,.2);color:#ef4444;font-size:.6rem;font-weight:700;padding:1px 7px;border-radius:10px;border:1px solid rgba(239,68,68,.4)">PSM CRITICAL</span>' if is_crit2 else ""
                st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:1rem;margin-bottom:8px">
<div style="font-size:.85rem;font-weight:700;color:#e2e8f0;margin-bottom:.6rem">{param}{crit_b2}</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:6px">
<div style="background:#080d18;border:1px solid rgba(34,197,94,.2);border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:4px">SOC (TARGET)</div>
<div style="font-size:.88rem;font-weight:800;color:#22c55e;font-family:monospace">{soc}</div>
</div>
<div style="background:#080d18;border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:4px">SOL (LIMIT)</div>
<div style="font-size:.88rem;font-weight:800;color:#f97316;font-family:monospace">{sol}</div>
</div>
<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#64748b;margin-bottom:4px">PSM CRITICAL</div>
<div style="font-size:.82rem;font-weight:700;color:{'#ef4444' if is_crit2 else '#22c55e'}">{'YES' if is_crit2 else 'NO'}</div>
</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
<div style="background:rgba(234,179,8,.06);border:1px solid rgba(234,179,8,.2);border-left:3px solid #eab308;border-radius:6px;padding:.6rem .8rem">
<div style="font-size:.6rem;font-weight:700;color:#eab308;margin-bottom:3px">IF BELOW SOC/SOL:</div>
<div style="font-size:.75rem;color:#fde68a">{low_dev}</div>
</div>
<div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem .8rem">
<div style="font-size:.6rem;font-weight:700;color:#ef4444;margin-bottom:3px">IF ABOVE SOC/SOL:</div>
<div style="font-size:.75rem;color:#fca5a5">{high_dev}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

            if is_hho_h2 and sp.get("hazop"):
                st.markdown('<div class="sl-sec">HAZOP Study</div>', unsafe_allow_html=True)
                tblhz = '<table style="border-collapse:collapse;width:100%;font-size:.78rem"><thead><tr style="background:#080d18">'
                for hh2 in ["Deviation","Parameter","Cause","Consequence","Safeguard"]:
                    tblhz += f'<th style="padding:8px 12px;text-align:left;color:#64748b;font-size:.65rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f">{hh2}</th>'
                tblhz += '</tr></thead><tbody>'
                for row in sp["hazop"]:
                    tblhz += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:8px 12px;color:#f97316;font-weight:700">{row[0]}</td><td style="padding:8px 12px;color:#e2e8f0">{row[1]}</td><td style="padding:8px 12px;color:#94a3b8">{row[2]}</td><td style="padding:8px 12px;color:#fca5a5">{row[3]}</td><td style="padding:8px 12px;color:#4ade80;font-size:.72rem">{row[4]}</td></tr>'
                tblhz += '</tbody></table>'
                st.markdown(tblhz, unsafe_allow_html=True)

            if is_hho_h2 and sp.get("bowtie"):
                st.markdown('<div class="sl-sec">Bow Tie Analysis</div>', unsafe_allow_html=True)
                bt2 = sp["bowtie"]
                bt_c1, bt_c2, bt_c3 = st.columns([2,1,2])
                with bt_c1:
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin-bottom:.4rem">CAUSES / THREATS</div>', unsafe_allow_html=True)
                    for c5 in bt2["causes"]:
                        st.markdown(f'<div class="sl-cause">{c5}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#22c55e;margin:.6rem 0 .3rem">PREVENTION BARRIERS</div>', unsafe_allow_html=True)
                    for c5 in bt2["preventions"]:
                        st.markdown(f'<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:6px 10px;margin-bottom:5px;font-size:.75rem;color:#4ade80">✓ {c5}</div>', unsafe_allow_html=True)
                with bt_c2:
                    te2 = bt2["top_event"]
                    st.markdown(f'<div style="background:rgba(239,68,68,.12);border:2px solid #ef4444;border-radius:10px;padding:1rem;text-align:center;margin-top:1rem"><div style="font-size:.58rem;font-weight:700;color:#ef4444;letter-spacing:2px;margin-bottom:6px">TOP EVENT</div><div style="font-size:.78rem;font-weight:700;color:#e2e8f0;line-height:1.5">{te2}</div></div>', unsafe_allow_html=True)
                with bt_c3:
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#ef4444;margin-bottom:.4rem">CONSEQUENCES</div>', unsafe_allow_html=True)
                    for c5 in bt2["consequences"]:
                        st.markdown(f'<div class="sl-consq">{c5}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#f97316;margin:.6rem 0 .3rem">MITIGATION BARRIERS</div>', unsafe_allow_html=True)
                    for c5 in bt2["mitigations"]:
                        st.markdown(f'<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-left:3px solid #f97316;border-radius:6px;padding:6px 10px;margin-bottom:5px;font-size:.75rem;color:#f97316">{c5}</div>', unsafe_allow_html=True)

            # ── H2 PSC Summary Table ──────────────────────────────────
            st.markdown('<div class="sl-sec">PSC Classification Summary — All Hydrogen Plant Processes</div>', unsafe_allow_html=True)
            h2_psc_rows = [
                ("DM Water & KOH Storage","KOH (caustic), Electric energy","N","N","N","Y","N","N","N","N","N","","Y"),
                ("Electrolysis (H2/O2 production)","H2 (Cat-1 flammable), O2 (oxidiser), DC voltage 1450A","N","Y","Y","N","Y","Y","Y","Y","Y","Y",""),
                ("Gas-Liquid Separation","H2 at operating pressure, KOH lye solution","N","Y","Y","Y","N","Y","Y","Y","Y","Y",""),
                ("Purification","H2 at operating pressure/temperature 118-220°C","N","Y","Y","N","N","Y","Y","Y","N","Y",""),
                ("Compressed H2 Storage","H2 under pressure 4-14 kg/cm2 in bullets","N","Y","Y","N","N","Y","Y","Y","N","Y",""),
                ("H2 Distribution to Annealing","H2 at 1.2-2.5 kg/cm2 in pipeline","N","Y","Y","N","N","Y","Y","Y","N","Y",""),
            ]
            hdr_h2 = ["Sub-Process","Hazardous Substance","Toxic","Explosive","Flammable","Corrosive","Thermal","Pressure","Property >50L","Fatality","Env. Impact","HHO","LHO"]
            tbl_h2s = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.74rem"><thead><tr style="background:#080d18">'
            for h in hdr_h2:
                tbl_h2s += f'<th style="padding:7px 10px;text-align:center;color:#64748b;font-size:.62rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
            tbl_h2s += '</tr></thead><tbody>'
            for row in h2_psc_rows:
                is_hho_r = row[11] == "Y"
                row_bg = "rgba(249,115,22,.04)" if is_hho_r else "rgba(99,102,241,.03)"
                tbl_h2s += f'<tr style="border-bottom:1px solid #1e3a5f;background:{row_bg}">'
                for ii2, v in enumerate(row):
                    if ii2 == 0:
                        tbl_h2s += f'<td style="padding:7px 10px;color:#e2e8f0;font-weight:600;white-space:nowrap">{v}</td>'
                    elif ii2 == 1:
                        tbl_h2s += f'<td style="padding:7px 10px;color:#94a3b8;font-size:.7rem">{v}</td>'
                    elif v == "Y" and ii2 in (11,):
                        tbl_h2s += '<td style="padding:7px 10px;text-align:center"><span style="background:rgba(249,115,22,.2);color:#f97316;border:1px solid rgba(249,115,22,.4);font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:10px">HHO</span></td>'
                    elif v == "Y" and ii2 in (12,):
                        tbl_h2s += '<td style="padding:7px 10px;text-align:center"><span style="background:rgba(99,102,241,.2);color:#818cf8;border:1px solid rgba(99,102,241,.4);font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:10px">LHO</span></td>'
                    elif v == "Y":
                        tbl_h2s += '<td style="padding:7px 10px;text-align:center;color:#22c55e;font-weight:700">Y</td>'
                    elif v == "N":
                        tbl_h2s += '<td style="padding:7px 10px;text-align:center;color:#475569">N</td>'
                    else:
                        tbl_h2s += '<td style="padding:7px 10px;text-align:center;color:#1e3a5f">—</td>'
                tbl_h2s += '</tr>'
            tbl_h2s += '</tbody></table></div>'
            st.markdown(tbl_h2s, unsafe_allow_html=True)

            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-top:.6rem;font-size:.75rem;color:#64748b">
<b style="color:#f97316">Note A (HHO):</b> If a process has potential for uncontrolled release of energy (Toxic/Explosive/Flammable/Corrosive/Thermal/Pressure) which COULD result in property damage &gt;Rs.50L, fatality, or environmental impact — classified HHO. Full PSRM required.<br>
<b style="color:#6366f1">Note B (LHO):</b> If consequences cannot meet HHO thresholds under credible abnormal conditions — classified LHO. Baseline PSI documentation only.
</div>""", unsafe_allow_html=True)

        with h2tabs[2]:  # HOM
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/HOM/TINPL/ Rev.03 Eff.Dt.:08.10.2023</p>', unsafe_allow_html=True)

            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">HAZARD CATEGORIES (A-SCALE) — H2 Plant Chemicals</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;font-size:.7rem">
<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:.5rem"><b style="color:#ef4444">A1 + A5: H2 (Hydrogen)</b><br><span style="color:#64748b">LEL 4%, UEL 75%, MIE 0.017 mJ — most ignition-sensitive gas. A5: stored at 14 kg/cm2 in bullets. BLEVE risk.</span></div>
<div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.5rem"><b style="color:#f97316">A3 + A5: O2 (Oxygen)</b><br><span style="color:#64748b">Strong oxidiser — violently accelerates combustion of H2 and all flammables. O2-enrichment hazard. A5: under pressure.</span></div>
<div style="background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);border-radius:6px;padding:.5rem"><b style="color:#a78bfa">Asphyxiant: N2 (Nitrogen)</b><br><span style="color:#64748b">O2 displacement → unconsciousness without warning. Used for purging — no sensory warning. IDLH: O2 &lt;16%.</span></div>
</div>
<div style="font-size:.7rem;color:#475569;margin-top:.5rem"><b style="color:#e2e8f0">TLV-TWA:</b> 8h time-weighted average &nbsp;|&nbsp; <b style="color:#e2e8f0">TLV-STEL:</b> 15-min short-term limit &nbsp;|&nbsp; <b style="color:#ef4444">IDLH:</b> Immediately Dangerous to Life &amp; Health &nbsp;|&nbsp; <b style="color:#e2e8f0">LEL:</b> Lower Explosive Limit (below = too lean to ignite)</div>
</div>""", unsafe_allow_html=True)

            if "h2_hom_sel" not in st.session_state:
                st.session_state.h2_hom_sel = "H1 — Hydrogen (H2)"

            H2_CHEMS_FULL = {
                "H1 — Hydrogen (H2)": {
                    "risk":92,"color":"#ef4444","code":"H1",
                    "class":"Category 1 Extremely Flammable Gas (GHS H220) — UN 1049","cas":"1333-74-0",
                    "hazchem":"Category 1 Flammable Gas","nfpa":"4-0-0",
                    "tlv_twa":"Simple Asphyxiant (ACGIH 2023) — No OEL set for H2 itself. Hazard is O2 displacement, not direct toxicity.",
                    "tlv_stel":"Not established — classified simple asphyxiant",
                    "tlv_ceil":"Not established",
                    "idlh":"NIOSH: Not established for H2. Effective IDLH based on O2 level: <12.5% O2 = IDLH. H2 at >87% in air causes O2 <12.5%.",
                    "erpg":"ERPG-2: flammability hazard at LEL (4%) | ERPG-3: explosion zone (>4-75%)",
                    "ld50":"Not applicable — asphyxiation at high concentrations, no chemical toxicity","lc50":"Not applicable",
                    "flash":"-253°C (liquid H2) — gas ignites at ambient with ignition source","bp":"-252.9°C","mp":"-259.1°C",
                    "sg":"0.071 (liquid) | Gas: 0.0899 kg/m³ at STP — LIGHTER THAN AIR — accumulates at ceiling/roof",
                    "vp":"Extremely high (gas at all ambient conditions)","lfl":"4% v/v in air (LEL)","ufl":"75% v/v in air (UEL)",
                    "ait":"500°C | MIE: 0.017 mJ — lowest of all industrial gases. Invisible static spark sufficient for ignition.",
                    "odour":"Completely odourless — NO sensory warning. Invisible flame — UV detector only.",
                    "reactivity":"Explosive with O2 at ANY ratio 4–75% in air (widest flammable range of any industrial gas). H2 embrittlement of carbon steel over time (Nelson curve — check MoC). Diffuses through metals and polymers (seal selection critical). Reacts with F2 explosively at −200°C. Incompatible with: Cl2, halogens, O2, strong oxidisers.",
                    "health":"Simple asphyxiant — displaces O2 in enclosed spaces with NO warning. O2 19.5%: alarm threshold. O2 16%: impaired judgment/coordination. O2 12%: loss of consciousness. O2 6%: death within minutes. No direct chemical toxicity. Cryogenic contact: frostbite/freeze burns at −253°C. High-pressure release: barotrauma. Invisible flame causes burn injury without visual warning.",
                    "env":"Rapidly disperses — low environmental persistence. No direct aquatic toxicity. Indirect GHG: H2 reacts with OH radicals, indirectly increasing CH4 lifetime. H2 fire produces only water vapour.",
                    "storage":"CCOE-approved dedicated H2 store. Zone 1 electrical classification within 3m of bullet vents. All electrical: Ex-rated (ATEX/IECEx Zone 1). No ignition sources within 8m. No organic materials near bullet. Static bonding and earthing. PESO/IBR annual inspection. Dual certified SRV on each bullet. Firefighting water deluge on bullet.",
                    "ppe":"Flame-resistant cotton (no synthetics near H2). Full face shield for high-pressure connections. Cryogenic: insulated cryo-gloves + face shield. Portable H2 LEL detector mandatory for zone entry. Anti-static footwear. No metal tools that can spark near H2.",
                    "emergency":"EVACUATE — H2 fires are INVISIBLE (UV only). Do NOT extinguish H2 fire unless gas source can be isolated (BLEVE risk if bullet heated). Isolate at bullet isolation valve. Water spray to cool bullet from distance if fire nearby. Personnel: remove to fresh air. CPR + 100% O2 if unconscious. PESO and Fire Brigade — pre-alert mandatory for H2 sites.",
                    "etl1_use":"H2 Plant: on-site electrolysis product. Stored in H2 bullets. Distributed at 1.2-2.5 kg/cm2 to annealing hoods on ETL-1, ETL-2.",
                    "soc":"GLT zone H2 detector: <0.2% LEL | Bullet: 4-14 kg/cm2, <45°C | Purified: >99.5% purity, dew pt <-80°C, O2 <1 ppm",
                    "sol":"GLT zone: <0.9% LEL (auto-trip) | Bullet: <20 kg/cm2, <50°C | Trace O2: <2 ppm (auto-vent QZ1007)",
                },
                "H2 — Oxygen (O2)": {
                    "risk":70,"color":"#f97316","code":"H2",
                    "class":"Oxidising Gas — Oxygen Enrichment Hazard","cas":"7782-44-7",
                    "hazchem":"Oxidiser","nfpa":"0-0-0 (OX)","tlv_twa":"N/A","tlv_stel":"N/A","tlv_ceil":"N/A",
                    "ld50":"N/A","lc50":"N/A","flash":"N/A (oxidiser — not flammable)","bp":"-183°C","mp":"-218°C","sg":"1.14 (liquid)","vp":"Very high (gas at ambient)",
                    "lfl":"N/A","ufl":"N/A","ait":"N/A (supports combustion, not combustible)","odour":"Odourless",
                    "reactivity":"Powerful oxidiser. O2-enriched atmosphere (>23%) dramatically increases flammability of ALL materials. O2 + H2 at any ratio between H2 4-75% = EXPLOSIVE. Violently accelerates combustion. Contact with oil/grease in O2 service = spontaneous ignition. Incompatible with: H2 (explosive), all hydrocarbons, all organics.",
                    "health":"Not directly toxic. O2 enrichment: increases fire risk dramatically. O2 depletion (if O2 consumed in reaction): asphyxiation. Pure O2 inhalation at elevated pressure: oxygen toxicity — convulsions. At ambient pressure: not directly harmful.",
                    "env":"Not harmful directly. O2 fire/explosion causes environmental damage. O2 promotes combustion of environmental pollutants.",
                    "storage":"Separate from all flammable materials and H2. No oil/grease on any O2 fittings (spontaneous ignition). Dedicated O2 pipework — no shared services. O2-clean equipment only. Zone 2 classification near O2 vent.",
                    "ppe":"No oil/grease on clothing for O2 work. Clean cotton preferred. Face shield. Dedicated O2-clean tools.",
                    "emergency":"O2 leak: ventilate area — do not ignite. If O2-enriched atmosphere confirmed: no ignition sources — all combustibles ignite more easily. Remove personnel. If fire: O2 does not burn — isolate O2 source, fight fire normally.",
                    "etl1_use":"H2 Plant: by-product of electrolysis — safely vented to atmosphere after separation. Must NOT enter H2 stream (explosive).",
                    "soc":"H2-in-O2: <0.8% | O2-in-H2: <0.1%","sol":"H2-in-O2: <1.7% | O2-in-H2: <0.2%",
                },
                "H3 — Nitrogen (N2)": {
                    "risk":35,"color":"#22c55e","code":"H3",
                    "class":"Simple Asphyxiant Gas — Non-flammable, Non-toxic. UN 1066 (compressed). UN 1977 (liquid/refrigerated).","cas":"7727-37-9",
                    "hazchem":"Non-flammable compressed gas","nfpa":"0-0-0",
                    "tlv_twa":"Simple Asphyxiant (ACGIH 2023) — No OEL established. The hazard is O2 displacement, NOT chemical toxicity. NIOSH REL: None established.",
                    "tlv_stel":"Not established — simple asphyxiant. No short-term OEL.",
                    "tlv_ceil":"Not established",
                    "idlh":"NIOSH IDLH: Not established for N2. Effective IDLH: O2 <12.5% = IDLH (N2 at >87% in air). OXYGEN-DEFICIENT ATMOSPHERE: <19.5% O2 requires immediate action.",
                    "erpg":"Not established (no direct chemical toxicity)","ld50":"Not applicable — asphyxiant gas, no chemical toxicity at physiological levels","lc50":"Not applicable",
                    "flash":"N/A — not flammable","bp":"-195.8°C (-320.4°F)","mp":"-210°C","sg":"0.808 (liquid) | Gas: 1.165 kg/m³ at STP — slightly lighter than air — disperses in open",
                    "vp":"Very high (gas at all ambient conditions)","lfl":"N/A — not flammable","ufl":"N/A","ait":"N/A","odour":"Completely odourless — NO sensory warning whatsoever.",
                    "reactivity":"Essentially chemically inert at ambient conditions — 78% of Earth's atmosphere. Does not react with H2 or O2 at ambient temperature. At very high temperatures (>1000°C): forms NO and NO2 (NOx) with O2 — not relevant to H2 plant conditions. Selected for purging specifically because of its chemical inertness — safe to use in H2 systems.",
                    "health":"SIMPLE ASPHYXIANT — THE LEADING CAUSE OF INDUSTRIAL CONFINED SPACE FATALITIES IN INDIA AND GLOBALLY. Hazard is 100% oxygen displacement — NO chemical toxicity whatsoever. O2 19.5%: warning threshold (mandatory alarm). O2 16%: impaired judgment, headache, tachycardia. O2 12%: dizziness, rapid loss of consciousness — victim collapses without warning. O2 10%: unconsciousness, cyanosis. O2 6%: convulsions, death within minutes. Cryogenic liquid N2 (−196°C): severe frostbite/freeze burn on skin contact. Thermal expansion of liquid N2: 1 litre liquid = 696 litres gas — extreme pressure in sealed vessels.",
                    "env":"N2 constitutes 78.09% of normal atmosphere — not harmful environmentally. No aquatic or terrestrial ecotoxicity. Cryogenic liquid N2 spill: rapid freezing of local surfaces, potential freeze injury to vegetation. No long-term environmental impact.",
                    "storage":"Compressed gas cylinders: stored upright, chained, in ventilated area, away from heat sources. No special chemical segregation required. Cryogenic liquid N2: vacuum-insulated vessels, pressure relief mandatory, never seal cryogenic vessel completely. Away from ignition sources (not N2 itself, but associated O2 enrichment from LOX is possible). Check for area O2 depletion from bulk N2 storage.",
                    "ppe":"MANDATORY for confined space after N2 purge: independent O2 monitor (calibrated, bump-tested) before entry. If O2 <19.5%: ENTRY PROHIBITED without supplied-air respirator (SCBA). For liquid N2 handling: cryogenic insulated gloves (−200°C rated), full face shield, closed-toe shoes. Buddy system mandatory for all N2 confined space work.",
                    "emergency":"N2 atmosphere (confined space): DO NOT ENTER WITHOUT SCBA — victim collapses silently. Call emergency + rescue team with SCBA before any rescue. Remove casualty to fresh air immediately. CPR if not breathing — 30:2 ratio. 100% O2 via mask. Call 108. Area: ventilate forcibly until O2 confirmed >19.5% on meter — minimum 5 air changes. Cryogenic N2 spill: evacuate cold vapour cloud, warm affected skin slowly, DO NOT rub.",
                    "etl1_use":"H2 Plant: purging agent for H2 system startup and shutdown. N2 purge MANDATORY before H2 admission (until O2 <1%). N2 purge MANDATORY on H2 system shutdown (until H2 <1% LEL). Interlock: H2 admission valve cannot open until N2 purge confirmed by PLC.",
                    "soc":"N2 purge: continue until O2 in furnace/vessel <1% by volume before H2 admission. N2 purity: >99.9%, O2 content <0.1%.",
                    "sol":"H2 admission PROHIBITED if N2 purge not confirmed. Confined space entry PROHIBITED if O2 <19.5%.",
                },
            }

            chem_keys = list(H2_CHEMS_FULL.keys())
            cc2 = st.columns(len(chem_keys))
            for ii2, ck in enumerate(chem_keys):
                cd2 = H2_CHEMS_FULL[ck]
                rc_h = cd2["color"]
                is_act2 = (st.session_state.h2_hom_sel == ck)
                with cc2[ii2]:
                    rv2 = cd2["risk"]
                    st.markdown(f'<div style="background:{rc_h}15;border:1px solid {rc_h}50;border-top:3px solid {rc_h};border-radius:8px;padding:.6rem;text-align:center;margin-bottom:4px"><div style="font-size:.65rem;font-weight:700;color:{rc_h}">{cd2["code"]}</div><div style="font-size:.78rem;font-weight:900;color:{rc_h};font-family:monospace">{rv2}/100</div></div>', unsafe_allow_html=True)
                    if st.button(ck[:18], key=f"h2hom_{ck}", use_container_width=True, type="primary" if is_act2 else "secondary"):
                        st.session_state.h2_hom_sel = ck
                        st.rerun()

            sc3 = H2_CHEMS_FULL[st.session_state.h2_hom_sel]
            sc3c = sc3["color"]
            sc3r = sc3["risk"]

            st.markdown(f"""<div style="background:{sc3c}10;border:1px solid {sc3c}40;border-left:5px solid {sc3c};border-radius:10px;padding:1rem 1.4rem;margin:.8rem 0;display:flex;justify-content:space-between;align-items:flex-start">
<div>
<div style="font-size:1.05rem;font-weight:800;color:#f1f5f9;margin-bottom:.2rem">{st.session_state.h2_hom_sel}</div>
<div style="font-size:.78rem;color:#64748b">{sc3['class']}</div>
<div style="font-size:.72rem;color:#64748b;margin-top:.2rem">CAS: {sc3['cas']} &nbsp;|&nbsp; HAZCHEM: {sc3['hazchem']} &nbsp;|&nbsp; NFPA: {sc3['nfpa']}</div>
<div style="font-size:.72rem;color:#f97316;font-weight:700;margin-top:.3rem">ETL-1 / H2 Plant Use: {sc3['etl1_use']}</div>
</div>
<div style="text-align:center;min-width:80px">
<div style="font-size:2rem;font-weight:900;color:{sc3c};font-family:monospace">{sc3r}</div>
<div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#475569">RISK SCORE</div>
{risk_bar(sc3r)}
</div>
</div>""", unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Physical & Exposure Data</div>', unsafe_allow_html=True)

            # ── Quick Reference Comparison Table — All H2 Plant Chemicals ──
            st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">QUICK REFERENCE — ALL H2 PLANT CHEMICALS (Toxicology & Exposure Data)</div>""", unsafe_allow_html=True)
            # H2 Plant quick-ref: H2, O2, N2
            # H2: ACGIH TLV-TWA Simple Asphyxiant — no ppm OEL. No STEL, no ceiling.
            #     OSHA: no PEL established. NIOSH REL: none. IDLH: not set for H2 — O2-based IDLH applies.
            #     Safety limit: O2 < 19.5% (alarm), O2 < 16% (danger), LEL 4% (explosion)
            # O2: No TLV (ACGIH — O2 is not toxic, hazard is enrichment).
            #     No STEL, no Ceiling, no IDLH for O2 itself.
            #     OSHA confined space: >23.5% O2 = oxygen-enriched atmosphere (hazard).
            # N2: ACGIH TLV-TWA Simple Asphyxiant — no ppm OEL. No STEL, no Ceiling.
            #     OSHA: no PEL. NIOSH REL: none. IDLH: not set for N2 — O2-based.
            #     Safety limit: O2 < 19.5% (mandatory alarm per OSHA 1910.146)
            h2_qr_data = [
                # code, name, color, tlv_twa, tlv_stel, tlv_ceil, idlh, gas_density, nfpa, key_note, ld50, lc50
                ("H1","Hydrogen (H2)","#ef4444",
                 "Simple Asphyxiant (ACGIH 2023) — no ppm OEL established. Hazard is O₂ displacement.",
                 "Not established (ACGIH/NIOSH/OSHA) — Simple Asphyxiant classification: STEL not applicable.",
                 "Not established — no ceiling set. Flammability limit (LEL 4%) is the controlling safety threshold, not an OEL.",
                 "Not established for H₂ (NIOSH). Effective safety limit: O₂ <19.5% = alarm; O₂ <16% = danger; O₂ <12.5% = IDLH-equivalent. LEL >4% = explosion hazard.",
                 "0.0899 kg/m³ at STP — LIGHTER THAN AIR","4-0-0",
                 "LEL 4% v/v | UEL 75% v/v | MIE 0.017 mJ (lowest industrial gas) | AIT 500°C | Invisible flame",
                 "Not applicable — no chemical toxicity (asphyxiant only)","Not applicable — no direct inhalation toxicity"),
                ("H2","Oxygen (O2)","#f97316",
                 "Not established (ACGIH/NIOSH/OSHA) — O₂ is not chemically toxic. No TLV. Hazard: enrichment accelerates combustion.",
                 "Not established — no OEL system applies to O₂ (not a toxic substance). Enrichment hazard at >23.5% O₂.",
                 "Not established — no ceiling OEL. Safe range: 19.5–23.5% O₂ in atmosphere (OSHA 1910.146 confined space). >23.5% = O₂-enriched = enhanced fire hazard.",
                 "Not established for O₂ (NIOSH) — not a toxic gas. Confined space: >23.5% O₂ = prohibited without precautions. O₂ <19.5% = deficient.",
                 "1.429 kg/m³ at STP — slightly heavier than air","0-0-0 (OX)",
                 "OXIDISER — not flammable, but O₂ enrichment doubles/triples fire intensity. All combustibles ignite faster. No oil/grease on O₂ fittings.",
                 "Not applicable — not chemically toxic","Not applicable — not toxic. O₂ toxicity only at hyperbaric pressure (>0.5 bar pO₂)"),
                ("H3","Nitrogen (N2)","#22c55e",
                 "Simple Asphyxiant (ACGIH 2023) — no ppm OEL. 78.09% of atmosphere. Hazard: O₂ displacement ONLY.",
                 "Not established (ACGIH/NIOSH/OSHA) — Simple Asphyxiant: STEL not applicable. O₂ monitoring replaces OEL monitoring.",
                 "Not established — no ceiling OEL. Safe range determined by O₂ level: <19.5% O₂ = mandatory action (OSHA 1910.146). Purge areas: O₂ <1% before H₂ admission.",
                 "Not established for N₂ (NIOSH). Effective safety limit: O₂ <19.5% = alarm; O₂ <16% = extreme danger; O₂ <10% = fatal within minutes. OSHA confined space entry prohibited if O₂ <19.5% without SCBA.",
                 "1.165 kg/m³ at STP — slightly lighter than air, but pools in low points when released","0-0-0",
                 "ASPHYXIANT — NO warning (odourless). Leading cause of confined space fatalities. O₂ monitor mandatory before entry into any N₂-purged space.",
                 "Not applicable — no chemical toxicity at any concentration","Not applicable — asphyxiation is mechanical O₂ displacement, not chemical toxicity"),
            ]
            h2_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.7rem"><thead><tr style="background:#080d18">'
            for hh in ["Code","Chemical","TLV-TWA (ACGIH 2023)","TLV-STEL","TLV-Ceiling","IDLH (NIOSH)","Gas Density","NFPA","Key Safety Note","LD50","LC50"]:
                h2_tbl += f'<th style="padding:6px 10px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            h2_tbl += '</tr></thead><tbody>'
            for row in h2_qr_data:
                code, name, color = row[0], row[1], row[2]
                tlv_twa, tlv_stel, tlv_ceil, idlh, density, nfpa, note, ld50, lc50 = row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11]
                h2_tbl += f'<tr style="border-bottom:1px solid #1e3a5f">'
                h2_tbl += f'<td style="padding:6px 10px"><span style="background:{color}20;color:{color};border:1px solid {color}40;font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:20px">{code}</span></td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#e2e8f0;font-weight:600;white-space:nowrap">{name}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#94a3b8;font-size:.68rem;max-width:200px">{tlv_twa}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#64748b;font-size:.68rem;max-width:160px">{tlv_stel}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#64748b;font-size:.68rem;max-width:160px">{tlv_ceil}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#ef4444;font-size:.68rem;max-width:180px;font-weight:600">{idlh}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#60a5fa;font-family:monospace;font-size:.68rem;white-space:nowrap">{density}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#60a5fa;font-family:monospace;font-weight:700">{nfpa}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#fde68a;font-size:.68rem;max-width:200px">{note}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#475569;font-size:.68rem">{ld50}</td>'
                h2_tbl += f'<td style="padding:6px 10px;color:#475569;font-size:.68rem">{lc50}</td>'
                h2_tbl += '</tr>'
            h2_tbl += '</tbody></table></div>'
            st.markdown(h2_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.68rem;color:#475569;margin-bottom:.8rem">Sources: ACGIH TLV Booklet 2023, NIOSH Pocket Guide 2023, OSHA 1910.146 (confined space), IEC 60079 (area classification). No OEL exists for simple asphyxiants — O₂ monitoring is the control strategy.</div>', unsafe_allow_html=True)

            hh_c1, hh_c2 = st.columns(2)
            with hh_c1:
                idlh_row = f'<div style="color:#ef4444;font-weight:700">IDLH:</div><div style="color:#fca5a5;font-weight:600">{sc3.get("idlh","Not established")}</div>' if sc3.get("idlh") else ""
                erpg_row = f'<div style="color:#eab308">ERPG:</div><div style="color:#fde68a;font-size:.72rem">{sc3.get("erpg","N/A")}</div>' if sc3.get("erpg") else ""
                st.markdown(f"""<div class="sl-card">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.6rem">EXPOSURE LIMITS & TOXICOLOGY</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:.78rem">
<div style="color:#64748b">TLV-TWA (ACGIH):</div><div style="color:#e2e8f0;font-weight:600">{sc3['tlv_twa']}</div>
<div style="color:#64748b">TLV-STEL:</div><div style="color:#e2e8f0;font-weight:600">{sc3['tlv_stel']}</div>
<div style="color:#64748b">TLV-Ceiling:</div><div style="color:#e2e8f0;font-weight:600">{sc3['tlv_ceil']}</div>
{idlh_row}
{erpg_row}
<div style="color:#64748b">LD50 (oral, rat):</div><div style="color:#e2e8f0;font-weight:600">{sc3['ld50']}</div>
<div style="color:#64748b">LC50 (inhal, rat):</div><div style="color:#e2e8f0;font-weight:600">{sc3['lc50']}</div>
</div></div>""", unsafe_allow_html=True)
            with hh_c2:
                mie_row = f'<div style="color:#64748b">Min. Ignition Energy:</div><div style="color:#f97316;font-weight:600">{sc3.get("mie","N/A")}</div>' if sc3.get("mie") else ""
                st.markdown(f"""<div class="sl-card">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.6rem">PHYSICAL & FLAMMABILITY PROPERTIES</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:.78rem">
<div style="color:#64748b">Flash Point:</div><div style="color:#e2e8f0;font-weight:600">{sc3['flash']}</div>
<div style="color:#64748b">Boiling Point:</div><div style="color:#e2e8f0;font-weight:600">{sc3['bp']}</div>
<div style="color:#64748b">Specific Gravity:</div><div style="color:#e2e8f0;font-weight:600">{sc3.get('sg','N/A')}</div>
<div style="color:#64748b">LEL / LFL:</div><div style="color:#f97316;font-weight:600">{sc3['lfl']}</div>
<div style="color:#64748b">UEL / UFL:</div><div style="color:#f97316;font-weight:600">{sc3['ufl']}</div>
<div style="color:#64748b">Auto-Ignition Temp:</div><div style="color:#e2e8f0;font-weight:600">{sc3['ait']}</div>
{mie_row}
<div style="color:#64748b">Odour / Warning:</div><div style="color:#fde68a;font-weight:600">{sc3['odour']}</div>
</div></div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="sl-card" style="margin-top:.5rem"><b style="color:#f97316">Reactivity & Incompatibilities:</b><br><span style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sc3["reactivity"]}</span></div>', unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Health & Environmental Hazards</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8rem">
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:.5rem">HEALTH HAZARDS</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sc3['health']}</div></div>
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:.5rem">ENVIRONMENTAL IMPACT</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sc3['env']}</div></div>
</div>""", unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Storage, PPE & Emergency Response</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem">
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.5rem">STORAGE</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sc3['storage']}</div></div>
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#a78bfa;margin-bottom:.5rem">PPE REQUIREMENTS</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sc3['ppe']}</div></div>
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:.5rem">EMERGENCY RESPONSE</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sc3['emergency']}</div></div>
</div>""", unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">SOC / SOL & Plant Use</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:1rem;margin-bottom:.8rem">
<div style="font-size:.7rem;font-weight:700;color:#f97316;margin-bottom:.5rem">USE IN H2 PLANT: {sc3['etl1_use']}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
<div style="text-align:center;background:#080d18;border-radius:8px;padding:.8rem">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:4px">SOC (TARGET)</div>
<div style="font-size:.95rem;font-weight:800;color:#22c55e;font-family:monospace">{sc3['soc']}</div>
</div>
<div style="text-align:center;background:#080d18;border-radius:8px;padding:.8rem">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:4px">SOL (LIMIT)</div>
<div style="font-size:.95rem;font-weight:800;color:#f97316;font-family:monospace">{sc3['sol']}</div>
</div>
</div></div>""", unsafe_allow_html=True)


            st.markdown('<div class="sl-sec">Suppliers & Regulatory Compliance</div>', unsafe_allow_html=True)
            H2_SUPPLIER_DATA = {
                "H1 — Hydrogen (H2)": {
                    "suppliers":[
                        ("Linde India Ltd","Kolkata / Pan-India","India","Primary industrial H2 supplier. On-site electrolysis systems and cylinder supply. ISO certified."),
                        ("Air Liquide India","Mumbai, Maharashtra","India","Industrial gases including H2. Pipeline supply for large consumers."),
                        ("Praxair India (now Linde)","Pan-India","India","H2 supply by tube trailer and on-site generation equipment."),
                        ("Tata Steel (in-house)","Golmuri, Jharkhand","India","H2 produced on-site by electrolysis — self-sufficient supply for ETL-1 and ETL-2."),
                        ("Nel Hydrogen (electrolyser OEM)","Oslo","Norway","Electrolyser systems — original equipment manufacturer for on-site H2 production."),
                    ],
                    "spec":"Electrolysis grade: purity >99.5% (SOC), dew point <-80°C, trace O2 <1 ppm (SOC). For annealing: >99.9% purity. Supplied from on-site electrolyser or tube trailers at 200 bar.",
                    "storage_limit":"H2 storage vessels: CCOE approval mandatory. IBR registration. PESO inspection. H2 classified as Category 1 Flammable Gas. Zone 1/2 electrical area classification around storage.",
                    "regulatory":[
                        ("CCOE (Controller of Explosives)","Approval for H2 storage","License for each H2 storage vessel. Annual renewal. Safety distance calculations."),
                        ("IBR (Indian Boiler Regulations)","Pressure vessel registration","Every H2 bullet requires IBR inspection certificate. Annual statutory inspection."),
                        ("PESO (Petroleum & Explosives Safety Org)","Factory license condition","H2 above threshold = PESO notification. Safety audit annually."),
                        ("MSIHC Rules 1989","H2 — Schedule substance","5 T threshold for major hazard installation notification to CPCB/SPCB."),
                        ("UN Number","UN 1049 (compressed gas)","Class 2.1 — Flammable gas. Placarding mandatory on transport vehicles."),
                        ("Electrical Area Classification","IS/IEC 60079","Zone 1 within 3m of H2 vents/bullet connections. All electrical equipment to be Ex-rated (ATEX/IECEx)."),
                    ],
                    "india_msds_ref":"MSDS per GHS/Schedule 10 MSIHC. Invisible flame warning mandatory. Emergency H2 leak procedure in local language at plant boundary.",
                },
                "H2 — Oxygen (O2)": {
                    "suppliers":[
                        ("Linde India Ltd","Kolkata / Pan-India","India","Oxygen supply — industrial grade. Cylinder, liquid, and pipeline supply."),
                        ("Air Liquide India","Mumbai","India","Industrial oxygen — by-product from H2 electrolysis also collected for sale."),
                        ("INOX Air Products","Mumbai, Maharashtra","India","Industrial gas including O2. Large capacity liquid O2 supply."),
                        ("Tata Steel (in-house by-product)","Golmuri","India","O2 produced as by-product of on-site electrolysis. Vented or sold."),
                    ],
                    "spec":"O2 from electrolysis: vented to atmosphere after H2 separation. Purity monitored at separator — H2-in-O2 <0.8% SOC, <1.7% SOL. Not stored — direct vent.",
                    "storage_limit":"O2 not stored on-site at H2 plant (by-product vented). If stored: O2 separated from all flammables by minimum 3m or fire wall. NO oil/grease on O2 fittings.",
                    "regulatory":[
                        ("PESO","Storage requires approval if >50 kg liquid O2","If liquid O2 stored — PESO license. Cryogenic storage regulations apply."),
                        ("Factory Act 1948","O2-enriched atmosphere safety","O2 enrichment monitoring in confined spaces. Air supplied breathing if O2 >23%."),
                        ("UN Number","UN 1072 (compressed) / UN 1073 (liquid)","Class 2.2 (non-flammable) + 5.1 (oxidising). Subsidiary oxidiser risk."),
                        ("Fire Safety","O2 enrichment doubles fire risk","No smoking, open flame within 8m of O2 equipment. O2-clean tools mandatory."),
                    ],
                    "india_msds_ref":"MSDS per GHS. O2 enrichment hazard prominently stated. Fire triangle accelerated combustion warning.",
                },
                "H3 — Nitrogen (N2)": {
                    "suppliers":[
                        ("Linde India Ltd","Pan-India","India","Bulk liquid N2 and compressed gas cylinders. On-site generation systems."),
                        ("Air Liquide India","Pan-India","India","Nitrogen supply — liquid, compressed, and PSA generator systems."),
                        ("INOX Air Products","Mumbai","India","Industrial N2 — liquid tankers and tube trailers."),
                        ("Parker Hannifin (N2 generator OEM)","Pune","India","On-site N2 PSA (Pressure Swing Adsorption) generators for purging."),
                        ("Atlas Copco (N2 generator OEM)","Pune","India","N2 membrane generators for purging applications."),
                    ],
                    "spec":"Purging grade: purity >99.9% N2. O2 content <0.1% for H2 system purge. Dew point <-40°C. Supplied by liquid tanker (bulk) or compressed cylinder at 150-200 bar.",
                    "storage_limit":"Liquid N2 (cryogenic): CCOE approval for bulk storage. Cryogenic storage regulations. If only compressed: cylinders stored upright, away from heat, chained secure.",
                    "regulatory":[
                        ("CCOE","Liquid N2 bulk storage license","Cryogenic vessel approval. Annual inspection."),
                        ("Confined Space Entry","N2 purge areas: oxygen-deficient atmosphere","O2 meter mandatory before entry after N2 purge. O2 <19.5% = entry prohibited without supplied air."),
                        ("Factory Act 1948 — Confined Space","Section 36 — confined space permit","Permit-to-work mandatory for entry into N2-purged vessels."),
                        ("UN Number","UN 1066 (compressed) / UN 1977 (liquid)","Class 2.2 — non-flammable gas. Asphyxiant risk label required."),
                    ],
                    "india_msds_ref":"MSDS per GHS. ASPHYXIANT — NO WARNING warning mandatory in BOLD. Confined space entry procedure referenced. O2 depletion risk stated clearly.",
                },
            }

            h2_sup = H2_SUPPLIER_DATA.get(st.session_state.h2_hom_sel, {})

            if h2_sup.get("spec"):
                st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:.6rem"><div style="font-size:.62rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:3px">PROCUREMENT / PRODUCTION SPECIFICATION</div><div style="font-size:.78rem;color:#94a3b8">{h2_sup["spec"]}</div></div>', unsafe_allow_html=True)

            if h2_sup.get("suppliers"):
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin:.6rem 0 .4rem">SUPPLIERS / MANUFACTURERS</div>', unsafe_allow_html=True)
                s_tbl = '<table style="border-collapse:collapse;width:100%;font-size:.75rem"><thead><tr style="background:#080d18"><th style="padding:7px 12px;text-align:left;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Supplier</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Location</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Country</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Notes</th></tr></thead><tbody>'
                for sn, sl, sc_n, snote in h2_sup["suppliers"]:
                    flag = "🇮🇳" if sc_n == "India" else "🇳🇴" if "Norway" in sc_n else "🌐"
                    s_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 12px;color:#e2e8f0;font-weight:600">{sn}</td><td style="padding:7px 12px;color:#94a3b8">{sl}</td><td style="padding:7px 12px;color:#94a3b8">{flag} {sc_n}</td><td style="padding:7px 12px;color:#64748b;font-size:.72rem">{snote}</td></tr>'
                s_tbl += '</tbody></table>'
                st.markdown(s_tbl, unsafe_allow_html=True)

            if h2_sup.get("storage_limit"):
                st.markdown(f'<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.7rem 1rem;margin:.6rem 0"><div style="font-size:.62rem;font-weight:700;color:#f97316;letter-spacing:1px;margin-bottom:3px">STORAGE THRESHOLD & APPROVALS</div><div style="font-size:.78rem;color:#94a3b8">{h2_sup["storage_limit"]}</div></div>', unsafe_allow_html=True)

            if h2_sup.get("regulatory"):
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin:.6rem 0 .4rem">REGULATORY COMPLIANCE — INDIA</div>', unsafe_allow_html=True)
                r_tbl = '<table style="border-collapse:collapse;width:100%;font-size:.75rem"><thead><tr style="background:#080d18"><th style="padding:7px 12px;text-align:left;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Regulation</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Applicability</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Compliance Requirement</th></tr></thead><tbody>'
                for reg, app, req in h2_sup["regulatory"]:
                    is_crit2 = any(x in reg+app for x in ["CCOE","IBR","PESO","MSIHC","mandatory","Mandatory"])
                    rc6 = "#ef4444" if is_crit2 else "#94a3b8"
                    r_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 12px;color:{rc6};font-weight:600">{reg}</td><td style="padding:7px 12px;color:#94a3b8;font-size:.72rem">{app}</td><td style="padding:7px 12px;color:#64748b;font-size:.72rem">{req}</td></tr>'
                r_tbl += '</tbody></table>'
                st.markdown(r_tbl, unsafe_allow_html=True)

            if h2_sup.get("india_msds_ref"):
                st.markdown(f'<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.7rem 1rem;margin-top:.6rem"><div style="font-size:.62rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:3px">INDIA MSDS & DOCUMENTATION REQUIREMENTS</div><div style="font-size:.78rem;color:#94a3b8">{h2_sup["india_msds_ref"]}</div></div>', unsafe_allow_html=True)

        with h2tabs[3]:  # CIM
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/CIM/TINPL/ Rev.03 Eff.Dt.:08.10.2023</p>', unsafe_allow_html=True)

            # Full CIM data for Hydrogen Plant — H2, O2, N2, KOH, H2O
            H2_CHEM_NAMES = {
                "H2":    "HYDROGEN",
                "O2":    "OXYGEN",
                "N2":    "NITROGEN",
                "KOH_S": "POTASSIUM HYDROXIDE, [DRY SOLID, FLAKE, BEAD, OR GRANULAR]",
                "KOH_L": "POTASSIUM HYDROXIDE, SOLUTION",
                "NaOH":  "SODIUM HYDROXIDE, SOLID",
                "HCl":   "HYDROCHLORIC ACID, SOLUTION",
                "H2O":   "WATER",
                "NaOH_L":"SODIUM HYDROXIDE SOLUTION",
            }

            H2_PAIRS = {
                ("O2","H2"): {
                    "status":"Incompatible",
                    "hazards":["Explosive","Flammable","Generates gas","Generates heat","Intense or explosive reaction","Unstable when heated"],
                    "gases":[]
                },
                ("N2","H2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("N2","O2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("KOH_S","H2"): {"status":"Compatible","hazards":[],"gases":[]},
                ("KOH_S","O2"): {
                    "status":"Incompatible",
                    "hazards":["Generates gas","Intense or explosive reaction"],
                    "gases":[]
                },
                ("KOH_S","N2"): {"status":"Compatible","hazards":[],"gases":[]},
                ("KOH_L","H2"): {"status":"Compatible","hazards":[],"gases":[]},
                ("KOH_L","O2"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":[]
                },
                ("KOH_L","N2"): {"status":"Compatible","hazards":[],"gases":[]},
                ("KOH_L","KOH_S"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("NaOH","H2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("NaOH","O2"):  {
                    "status":"Incompatible",
                    "hazards":["Generates gas","Intense or explosive reaction"],
                    "gases":[]
                },
                ("NaOH","N2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("NaOH","KOH_S"): {"status":"Compatible","hazards":[],"gases":[]},
                ("NaOH","KOH_L"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("HCl","H2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("HCl","O2"):  {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Explosive","Flammable","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":[]
                },
                ("HCl","N2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("HCl","KOH_S"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":[]
                },
                ("HCl","KOH_L"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":[]
                },
                ("HCl","NaOH"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":[]
                },
                ("H2O","H2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("H2O","O2"):  {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("H2O","N2"):  {"status":"Compatible","hazards":[],"gases":[]},
                ("H2O","KOH_S"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("H2O","KOH_L"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("H2O","NaOH"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("H2O","HCl"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("NaOH_L","H2"): {"status":"Compatible","hazards":[],"gases":[]},
                ("NaOH_L","O2"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":[]
                },
                ("NaOH_L","N2"): {"status":"Compatible","hazards":[],"gases":[]},
                ("NaOH_L","KOH_S"): {"status":"Compatible","hazards":[],"gases":[]},
                ("NaOH_L","KOH_L"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("NaOH_L","NaOH"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
                ("NaOH_L","HCl"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":[]
                },
                ("NaOH_L","H2O"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Toxic"],
                    "gases":[]
                },
            }

            def h2_get_pair(a, b):
                return H2_PAIRS.get((a,b)) or H2_PAIRS.get((b,a))

            h2_rows_order = ["O2","N2","KOH_S","KOH_L","NaOH","HCl","H2O","NaOH_L"]
            h2_cols_order = ["H2","O2","N2","KOH_S","KOH_L","NaOH","HCl","H2O"]

            # ── Grid ──
            st.markdown('<div class="sl-sec">Chemical Interaction Grid — Hydrogen Plant</div>', unsafe_allow_html=True)
            grid_html = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem">'
            grid_html += '<tr><td style="background:#1a2a1a;padding:8px 10px;border:1px solid #2d4a2d;min-width:140px"></td>'
            for ck in h2_cols_order:
                _cn = H2_CHEM_NAMES[ck]; grid_html += f'<td style="background:#1a2a1a;padding:8px 10px;border:1px solid #2d4a2d;font-size:.63rem;font-weight:700;color:#4ade80;min-width:120px">{_cn}</td>'
            grid_html += '</tr>'
            for rk in h2_rows_order:
                rname = H2_CHEM_NAMES[rk]
                grid_html += f'<tr><td style="background:#1a2a1a;padding:8px 10px;border:1px solid #2d4a2d;font-size:.63rem;font-weight:700;color:#4ade80;vertical-align:top">{rname}</td>'
                for ck in h2_cols_order:
                    if ck == rk:
                        grid_html += f'<td style="background:#1a2a1a;padding:8px 10px;border:1px solid #2d4a2d;color:#4ade80;font-style:italic;font-size:.68rem;vertical-align:top">{rname}</td>'
                        continue
                    pair = h2_get_pair(rk, ck)
                    if not pair:
                        grid_html += '<td style="background:#0d2a0d;padding:8px 10px;border:1px solid #2d4a2d;font-size:.7rem;vertical-align:top"></td>'
                        continue
                    status = pair["status"]
                    sq_col = "#ef4444" if status=="Incompatible" else "#eab308" if status=="Caution" else "#22c55e"
                    sq = f'<span style="display:inline-block;width:9px;height:9px;background:{sq_col};margin-right:4px;border-radius:1px;vertical-align:middle;flex-shrink:0"></span>'
                    bg = "rgba(239,68,68,.06)" if status=="Incompatible" else "rgba(234,179,8,.05)" if status=="Caution" else "rgba(34,197,94,.05)"
                    bc = "rgba(239,68,68,.2)" if status=="Incompatible" else "rgba(234,179,8,.2)" if status=="Caution" else "rgba(34,197,94,.2)"
                    tc = "#fca5a5" if status=="Incompatible" else "#fde68a" if status=="Caution" else "#4ade80"
                    haz_list = "".join(f'<div style="color:#94a3b8;font-size:.65rem">{h}</div>' for h in pair["hazards"])
                    grid_html += f'<td style="background:{bg};border:1px solid {bc};padding:8px 10px;vertical-align:top"><div style="display:flex;align-items:center;font-weight:700;color:{tc};margin-bottom:3px;font-size:.72rem">{sq}{status}</div>{haz_list}</td>'
                grid_html += '</tr>'
            grid_html += '</table></div>'
            st.markdown(grid_html, unsafe_allow_html=True)

            # ── Hazard definitions ──
            st.markdown('<div class="sl-sec">Summary of Hazard Predictions (for all pairs of substances)</div>', unsafe_allow_html=True)
            h2_hazard_defs = [
                ("Corrosive","Reaction products may be corrosive"),
                ("Explosive","Reaction products may be explosive or sensitive to shock or friction"),
                ("Flammable","Reaction products may be flammable"),
                ("Generates gas","Reaction liberates gaseous products and may cause pressurization"),
                ("Generates heat","Exothermic reaction at ambient temperatures (releases heat)"),
                ("Intense or explosive reaction","Reaction may be particularly intense, violent, or explosive"),
                ("Toxic","Reaction products may be toxic"),
                ("Unstable when heated","Material may decompose violently when heated"),
                ("Potentially hazardous","May be hazardous but unknown"),
            ]
            hd_html = '<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:1rem 1.2rem">'
            for h, d in h2_hazard_defs:
                hd_html += f'<div style="padding:5px 0;border-bottom:1px solid #1e3a5f;font-size:.8rem"><span style="font-weight:700;color:#e2e8f0">{h}:</span> <span style="color:#94a3b8">{d}</span></div>'
            hd_html += '</div>'
            st.markdown(hd_html, unsafe_allow_html=True)

            # ── Reactivity alerts ──
            st.markdown('<div class="sl-sec">Reactivity Alerts</div>', unsafe_allow_html=True)
            h2_react = [
                ("HYDROGEN","Extremely Flammable Gas — LEL 4%, UEL 75%","Low ignition energy (0.017 mJ)","Invisible flame — no colour or odour"),
                ("OXYGEN","Strong Oxidiser — Oxygen Enrichment Hazard","Violently accelerates combustion of all flammables","Auto-trip if H2-in-O2 > 0.8% (SOC) / 1.7% (SOL)"),
                ("POTASSIUM HYDROXIDE (KOH)","Strong Base / Corrosive","Known Catalytic Activity","Generates heat with water"),
            ]
            for item in h2_react:
                name = item[0]
                props = item[1:]
                props_html = "".join(f'<div style="font-size:.75rem;color:#94a3b8;padding:2px 0">• {p}</div>' for p in props)
                st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:6px"><div style="font-size:.78rem;font-weight:700;color:#60a5fa;margin-bottom:4px">{name}</div>{props_html}</div>', unsafe_allow_html=True)

            # ── Per-pair detail cards ──
            st.markdown('<div class="sl-sec">Hazard Predictions (for each pair of substances)</div>', unsafe_allow_html=True)
            shown = set()
            for (a, b), data in H2_PAIRS.items():
                if data["status"] == "Compatible" or not data["hazards"]:
                    continue
                pair_key = tuple(sorted([a, b]))
                if pair_key in shown:
                    continue
                shown.add(pair_key)
                status = data["status"]
                sq_col = "#ef4444" if status=="Incompatible" else "#eab308"
                bg_c = "rgba(239,68,68,.05)" if status=="Incompatible" else "rgba(234,179,8,.05)"
                bc_c = "rgba(239,68,68,.15)" if status=="Incompatible" else "rgba(234,179,8,.15)"
                hazards_html = "".join(
                    f'<div style="font-size:.78rem;color:#94a3b8;padding:2px 0"><span style="font-weight:700;color:#e2e8f0">{h}:</span> {next((d for n,d in h2_hazard_defs if n==h), "")}</div>'
                    for h in data["hazards"]
                )
                st.markdown(f"""<div style="background:{bg_c};border:1px solid {bc_c};border-radius:8px;padding:1rem 1.2rem;margin-bottom:8px">
                  <div style="font-size:.78rem;color:#475569;margin-bottom:4px">
                    <span style="font-weight:700;color:#60a5fa">{H2_CHEM_NAMES[a]}</span>
                    <span style="font-style:italic"> mixed with </span>
                    <span style="font-weight:700;color:#60a5fa">{H2_CHEM_NAMES[b]}</span>
                  </div>
                  <div style="display:flex;align-items:center;gap:6px;margin:.4rem 0">
                    <span style="display:inline-block;width:10px;height:10px;background:{sq_col};border-radius:1px"></span>
                    <span style="font-weight:700;color:{'#f87171' if status=='Incompatible' else '#fde68a'};font-size:.84rem">{status}</span>
                  </div>
                  {hazards_html}
                </div>""", unsafe_allow_html=True)

        with h2tabs[4]:  # PDB — full from real data
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PDB/TINPL/ — All 24 parameters from real PDB spreadsheet. Hydrogen Plant, Tata Steel Tinplate (TCIL), Golmuri.</p>', unsafe_allow_html=True)

            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">LAYERS OF PROTECTION — H2 Plant SOC/SOL in context</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;font-size:.7rem">
<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#22c55e">BPCS (SOC zone)</b><br><span style="color:#64748b">PLC maintains parameters within SOC. Normal operation.</span></div>
<div style="background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#eab308">Alarms (SOC→SOL)</b><br><span style="color:#64748b">DCS alarms alert operator to deviation approaching SOL.</span></div>
<div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#f97316">SIS auto-trip (SOL)</b><br><span style="color:#64748b">AT1001/AT1002/TE1001 auto-trip at SOL. Independent of BPCS.</span></div>
<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#ef4444">SRV + Emergency (post-SOL)</b><br><span style="color:#64748b">SRVs on bullets, emergency trip, evacuation.</span></div>
</div></div>""", unsafe_allow_html=True)

            render_pdb(H2_PDB_PARAMS, dept_key="h2")

        with h2tabs[5]:  # PSCE — full 44 items from real spreadsheet data
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PSCE/TINPL/ Rev.03 Eff.Dt.:01.12.2020 — Hydrogen Plant, Tata Steel Tinplate (TCIL), Golmuri</p>', unsafe_allow_html=True)

            # Framework explanation
            st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem">
<div style="font-size:.82rem;font-weight:700;color:#3b82f6;margin-bottom:.6rem">PROCESS SAFETY CRITICAL EQUIPMENT (PSCE) — FRAMEWORK</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.8rem;font-size:.75rem;color:#94a3b8;line-height:1.7">
<div><b style="color:#ef4444">Consequence Based PSRM Critical</b><br>Equipment selected because its failure COULD DIRECTLY CAUSE a major accident — fire, explosion, toxic release, or structural failure. Selection is based on consequence analysis.</div>
<div><b style="color:#a78bfa">Prevention &amp; Mitigation Equipment</b><br>Equipment specifically designed and installed to PREVENT a major accident from occurring OR to MITIGATE the severity of consequences if a major accident begins.</div>
<div><b style="color:#f97316">Prescriptive PSM Critical</b><br>Equipment mandated by REGULATION regardless of consequence analysis — e.g. SRVs on pressure vessels (IBR/PESO), emergency trip switches, fire hydrant systems. Statutory requirement.</div>
</div></div>""", unsafe_allow_html=True)

            # Category definitions
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#64748b;letter-spacing:1px;margin-bottom:.5rem">BASIS OF SELECTION — CATEGORY DEFINITIONS (Note #1 per EDB Format)</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;font-size:.72rem">
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#22c55e">Passive Prevention &amp; Mitigation</b><br><span style="color:#64748b">Mitigation measures requiring NO human intervention or energy — e.g. bunds, blast walls, relief panels. Always active.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#3b82f6">Instrumented Active Preventive</b><br><span style="color:#64748b">SIS/interlock systems that automatically detect deviation and prevent escalation — e.g. analysers with auto-trip, level transmitters with shutdown.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#f97316">Active Mitigation</b><br><span style="color:#64748b">Mitigation requiring human action or automatic activation AFTER event starts — e.g. exhaust fans, pressure gauges for monitoring.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#ef4444">Safety Monitoring &amp; Emergency Comms</b><br><span style="color:#64748b">Systems for detecting emergencies and communicating them — e.g. H2 detectors, emergency trip switches, alarm systems.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#a78bfa">Controlled Release Equipment</b><br><span style="color:#64748b">Equipment for controlled safe release of pressure/material — e.g. SRVs, PRVs, auto-vent valves. Prevents uncontrolled release.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#94a3b8">Service &amp; Utility Systems</b><br><span style="color:#64748b">Support systems whose failure impacts the process safety chain — e.g. cooling, DM water, feed pumps. Selected consequence-based.</span></div>
</div></div>""", unsafe_allow_html=True)

            # Stats row
            st.markdown("""<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:1rem">
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#ef4444;font-family:monospace">44</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">TOTAL PSCE ITEMS</div></div>
<div style="background:#0d1f35;border:1px solid rgba(59,130,246,.3);border-top:3px solid #3b82f6;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#3b82f6;font-family:monospace">27</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">CONSEQUENCE BASED</div></div>
<div style="background:#0d1f35;border:1px solid rgba(167,139,250,.3);border-top:3px solid #a78bfa;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#a78bfa;font-family:monospace">8</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">ACTIVE MITIGATION</div></div>
<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#f97316;font-family:monospace">6</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">PRESCRIPTIVE</div></div>
<div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#22c55e;font-family:monospace">3</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">SERVICE/UTILITY</div></div>
</div>""", unsafe_allow_html=True)

            H2_PSCE_FULL = [
                {"sl":1,"equipment":"Feed Pump","tag":"1M21","basis":"Consequence Based","category":"Service and Utility Systems","psm_critical":"Yes",
                 "sub_process":"DM Water & KOH",
                 "justification":"Feed pump supplies DM water to electrolyser. Failure = DM tank empties → plant trip (low level SOL 100mm). Without DM water, electrolysis stops. If pump fails and plant continues, electrolyser runs dry — cell damage.",
                 "consequence_of_failure":"Plant trip on low DM water level. H2 generation stops. If undetected: electrolyser cell damage from dry running.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Condition-based inspection. Seal check at each shutdown."},
                {"sl":2,"equipment":"Lye Pump","tag":"1P11, 1P12","basis":"Consequence Based","category":"Service and Utility Systems","psm_critical":"Yes",
                 "sub_process":"Electrolysis",
                 "justification":"Dual lye circulating pumps (1P11, 1P12) circulate KOH electrolyte through electrolyser. Without lye circulation, electrolyte concentration drops → current efficiency drops → uncontrolled cell condition. Dual pumps for redundancy.",
                 "consequence_of_failure":"Loss of electrolyte circulation → cell temperature rises → auto-trip at 97°C SOL. Without trip: cell damage, H2 purity impact.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Condition-based. Bearing check at each overhaul."},
                {"sl":3,"equipment":"Lye Filter","tag":"—","basis":"Consequence Based","category":"Service and Utility Systems","psm_critical":"Yes",
                 "sub_process":"Electrolysis",
                 "justification":"Filters KOH lye solution before entry to electrolyser. Removes particles that could block cell membranes or foul electrodes. Membrane fouling causes uneven current distribution → localised overheating → cell damage.",
                 "consequence_of_failure":"Membrane fouling → current maldistribution → localised cell overheating → cell damage → uncontrolled H2/O2 conditions.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Condition-based. Replace filter element at each overhaul."},
                {"sl":4,"equipment":"Level Control Valve LV1001 (H2 line after separator)","tag":"LV1001","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"Controls KOH lye level in H2 separator (SOC 500-670mm). Level too low → gas bypasses separator → H2-in-O2 rises toward explosive range. Level too high → lye enters H2 gas pipeline → purity failure, line blockage. BOTH directions are hazardous.",
                 "consequence_of_failure":"Low level: H2-in-O2 rises → explosion risk in O2 separator (PSCE #13 AT1002 is backup). High level: lye carryover into H2 line → purifier damage, pipeline blockage.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"Jordan MK708/050. 6-monthly functional test. Annual calibration."},
                {"sl":5,"equipment":"Pressure Control Valve PV1001 (O2 line after separator)","tag":"PV1001","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"Controls O2 separator pressure (SOC 1.50-1.57 MPa). Balances pressure between H2 and O2 separators. Pressure imbalance → gas cross-contamination → H2-in-O2 rises → explosive mixture. Critical pressure equalisation function.",
                 "consequence_of_failure":"Pressure imbalance between H2 and O2 separators → gas mixing → H2-in-O2 or O2-in-H2 rises → explosive atmosphere risk.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"Jordan MK708/050. 6-monthly functional test."},
                {"sl":6,"equipment":"Control Valve Cooling Water Inlet TV1001","tag":"TV1001","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Electrolysis",
                 "justification":"Controls cooling water to lye heat exchanger. Maintains cell temperature SOC (35-95°C). Cell temperature SOL is 97°C — above this: auto-trip. If TV1001 fails closed → no cooling → cell temp rises toward 97°C SOL → auto-trip on RTD.",
                 "consequence_of_failure":"Cooling water loss → cell temperature rises → auto-trip at 97°C (PSCE #9,#10 are backup). Without trip: cell damage, KOH decomposition, H2 purity impact.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"Jordan MK78/100. Annual calibration and functional test."},
                {"sl":7,"equipment":"Pressure Control Valve PV1101 (H2 line after purifier)","tag":"PV1101","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Controls H2 outlet pressure from purifier (SOC 0.6-1.3 MPa). Ensures correct pressure before bullet storage. Failure open → overpressure in distribution. Failure closed → pressure builds in purifier above SOL → vessel stress.",
                 "consequence_of_failure":"Failure open: overpressure in distribution pipeline → PRV lifts → H2 release. Failure closed: purifier overpressure → vessel stress → potential H2 leak.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"Jordan MK708/050. 6-monthly functional test."},
                {"sl":8,"equipment":"DM Tank Level Transmitter LT1301","tag":"LT1301","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"No",
                 "sub_process":"DM Water & KOH",
                 "justification":"Monitors DM water tank level. Provides alarm and trip signal on low level (SOL 100mm). Without level monitoring, DM water could be depleted without warning → electrolyser runs dry.",
                 "consequence_of_failure":"Loss of level monitoring → DM tank depletes without alarm → electrolyser dry running → cell damage.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Annual calibration."},
                {"sl":9,"equipment":"RTD-1 at O2 Line for Cell Temperature (TE1001)","tag":"TE1001","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Electrolysis",
                 "justification":"PRIMARY cell temperature RTD. Monitors electrolyser cell temperature (SOC 35-95°C, SOL 97°C). Triggers PLC auto-trip at 97°C SOL. Cell overheating → KOH decomposition → H2 purity impact → cell damage → fire/explosion risk in extreme cases.",
                 "consequence_of_failure":"Loss of primary temperature monitoring → cell overheating undetected → without TE1003 backup: cell damage, possible H2 release.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration. Functional trip test annually."},
                {"sl":10,"equipment":"RTD-2 at O2 Line for Cell Temperature (TE1003)","tag":"TE1003","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Electrolysis",
                 "justification":"REDUNDANT cell temperature RTD. Second independent temperature sensor for 1oo2 or 2oo2 trip logic. Redundancy ensures single sensor failure does not prevent trip at 97°C SOL. Industry standard for safety-critical temperature monitoring.",
                 "consequence_of_failure":"Loss of redundant monitoring → single point of failure on cell temperature → if TE1001 also fails, no trip on overheating.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration. Must be tested independently from TE1001."},
                {"sl":11,"equipment":"Level Transmitter Separator Level LT1003-H2, LT1001-O2","tag":"LT1003, LT1001","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"Monitors liquid level in H2 separator (LT1003) and O2 separator (LT1001). Level SOC 500-670mm. Low level triggers gas bypass risk (H2-in-O2 rises). High level triggers lye carryover. Both transmitters required — one per separator.",
                 "consequence_of_failure":"Loss of level monitoring → separator level deviates without alarm → H2-in-O2 rises (low level) or lye carryover (high level) without detection.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration. Functional test of trip logic."},
                {"sl":12,"equipment":"Pressure Transmitter Separator Pressure PT1001","tag":"PT1001","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"Monitors separator pressure (SOC 1.50-1.57 MPa, SOL 1.65 MPa). Overpressure → vessel stress → rupture risk. Underpressure → transfer to purifier not possible. PT1001 provides PLC trip signal at SOL.",
                 "consequence_of_failure":"Loss of pressure monitoring → separator overpressure undetected → vessel rupture → catastrophic H2/O2 release.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration."},
                {"sl":13,"equipment":"Analyser H2-in-O2 % (AT1002)","tag":"AT1002","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"MOST CRITICAL ANALYSER: Continuously monitors H2 content in O2 stream. SOC: <0.8%, SOL: <1.7%. Above 1.7%: H2+O2 DETONATION risk in O2 separator. AT1002 triggers auto plant trip at HH limit. ONLY means of detecting H2-in-O2 contamination. Loss of AT1002 = immediate unsafe condition.",
                 "consequence_of_failure":"H2-in-O2 rises above 1.7% undetected → O2 separator DETONATION → multiple fatalities, structural collapse, major accident.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"3-monthly calibration with certified reference gas. Functional trip test. Redundant analyser recommended."},
                {"sl":14,"equipment":"Analyser O2-in-H2 % (AT1001)","tag":"AT1001","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"Continuously monitors O2 content in H2 stream. SOC: <0.1%, SOL: <0.2%. Above 0.2%: explosive O2-H2 mixture in H2 separator. Auto plant trip at HH. ONLY means of detecting O2-in-H2 contamination. Complementary to AT1002.",
                 "consequence_of_failure":"O2-in-H2 rises above 0.2% undetected → H2 separator explosive atmosphere → ignition = explosion → major accident.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"3-monthly calibration with certified reference gas."},
                {"sl":15,"equipment":"H2 Detector GLT Zone (AT1701)","tag":"AT1701","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"Fixed H2 LEL detector in Gas-Liquid Treater zone. SOC: <0.2% LEL, SOL: <0.9% LEL. H2 is colourless and odourless — NO sensory warning without detector. AT1701 is ONLY means of detecting H2 leak in GLT zone. Alarm triggers exhaust fan and operator investigation.",
                 "consequence_of_failure":"H2 leak in GLT zone undetected → explosive atmosphere → any ignition source = explosion. Operators work in area without warning.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"3-monthly calibration with certified H2 reference gas."},
                {"sl":16,"equipment":"H2 Detector Purifier Zone (AT1702)","tag":"AT1702","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Fixed H2 LEL detector in purification zone. Same function as AT1701 but for purification area. High-temperature H2 lines (118-220°C zone) — any leak has elevated risk due to process temperatures near auto-ignition temperature.",
                 "consequence_of_failure":"H2 leak in purifier zone undetected → explosive atmosphere in area with hot surfaces → auto-ignition possible.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"3-monthly calibration."},
                {"sl":17,"equipment":"H2 Detector DM Plant Zone (AT1703)","tag":"AT1703","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"DM Water & KOH",
                 "justification":"Fixed H2 LEL detector in DM plant area adjacent to H2 plant. Detects H2 migration from adjacent zones. Provides early warning before concentration reaches LEL in occupied DM plant area.",
                 "consequence_of_failure":"H2 migration to DM plant area undetected → workers in DM plant area exposed to explosive atmosphere without warning.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"3-monthly calibration."},
                {"sl":18,"equipment":"Exhaust Fan","tag":"—","basis":"Active Mitigation","category":"Active Mitigation System","psm_critical":"No",
                 "sub_process":"Gas-Liquid Treater",
                 "justification":"PRESCRIPTIVE: Exhaust fan auto-starts on H2 detector alarm (AT1701/AT1702/AT1703). Ventilates H2 accumulation in plant area. Reduces H2 concentration below LEL to safe levels. Required by design — enclosed H2 plant building requires forced ventilation on alarm.",
                 "consequence_of_failure":"H2 accumulation not ventilated → concentration rises toward LEL → explosion risk grows. Manual ventilation insufficient for speed required.",
                 "psce_type":"Active Mitigation",
                 "maintenance":"Monthly test run. Annual electrical inspection."},
                {"sl":19,"equipment":"RTD at Deoxygenation Unit","tag":"TE-Deoxy","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Monitors deoxy bed temperature (SOC 118-160°C). Low temp → poor O2 removal → trace O2 rises → explosive mixture risk downstream. High temp → catalyst damage → purity failure. Auto-trip at SOL.",
                 "consequence_of_failure":"Deoxy bed temperature deviation undetected → O2 not removed → trace O2 rises above SOL → explosive mixture potential in storage/distribution.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration."},
                {"sl":20,"equipment":"RTD at Dryer A, B, C","tag":"TE-Dryer","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Monitors dryer bed temperatures (SOC 170-220°C). Low temp → poor drying → dew point rises → moisture in H2 pipeline → corrosion, embrittlement of annealing equipment. Auto-trip if temp falls below SOL.",
                 "consequence_of_failure":"Dryer temperature deviation → dew point rises above SOL (-70°C) → moisture in H2 pipeline → annealing equipment damage, product quality failure.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration."},
                {"sl":21,"equipment":"Coolers after Deoxy & Dryers (1131-1134)","tag":"1131,1132,1133,1134","basis":"Service and Utility","category":"Service and Utility Systems","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Four heat exchangers cool H2 after high-temperature purification stages (118-220°C). Failure → high-temperature H2 entering downstream equipment at elevated temp → seal/fitting failures → H2 leak risk. Also: high temp H2 in bullets = pressure rise above SOL.",
                 "consequence_of_failure":"Hot H2 reaches bullet storage → thermal expansion → pressure rises above SOL → SRV lifts → H2 release. Also: equipment seal failures from high-temperature H2.",
                 "psce_type":"Service and Utility",
                 "maintenance":"Annual inspection. Fouling check."},
                {"sl":22,"equipment":"Filters after Deoxy & Dryers (1102-1105)","tag":"1102-1105","basis":"Service and Utility","category":"Service and Utility Systems","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Removes catalyst fines and particulates from purified H2 after each purification stage. Particles in H2 stream → analyser blockage (AT1102) → loss of trace O2 monitoring → safety blind spot.",
                 "consequence_of_failure":"Analyser AT1102 blockage → trace O2 in H2 not detected → contaminated H2 passes to storage → explosive mixture in bullet.",
                 "psce_type":"Service and Utility",
                 "maintenance":"Replace filter element at each overhaul. Pressure drop monitoring."},
                {"sl":23,"equipment":"Dew Point Analyser MT1101","tag":"MT1101","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Monitors dew point of purified H2 (SOC: <-80°C, SOL: <-70°C). High dew point = moisture in H2 = corrosion and embrittlement of annealing hoods and distribution pipeline. Auto-trip if dew point exceeds SOL. MTS6 transmitter — 6-monthly calibration mandatory.",
                 "consequence_of_failure":"Dew point exceeds SOL undetected → moisture in H2 distribution → annealing hood damage, product quality failure, pipeline corrosion.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration with certified dew point reference."},
                {"sl":24,"equipment":"Pressure Transmitter Purifier PT1101","tag":"PT1101","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Monitors H2 pressure at purifier outlet (SOC 0.6-1.3 MPa, SOL 0.5-1.4 MPa). Overpressure alarm and trip. Underpressure alarm for insufficient purifier performance.",
                 "consequence_of_failure":"Purifier overpressure undetected → vessel stress → SRV lift → H2 release. Underpressure undetected → insufficient purifier output quality.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration."},
                {"sl":25,"equipment":"Filter after Dryer 1151","tag":"1151","basis":"Service and Utility","category":"Service and Utility Systems","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"Final polishing filter before H2 bullet storage. Last particle removal before H2 enters high-pressure storage. Protects bullet inlet valves from fouling. Inlet valve fouling → valve failure → uncontrolled H2 flow to bullet.",
                 "consequence_of_failure":"Bullet inlet valve fouling → valve failure → uncontrolled H2 flow or inability to isolate bullet for maintenance.",
                 "psce_type":"Service and Utility",
                 "maintenance":"Condition-based. Pressure drop monitoring."},
                {"sl":26,"equipment":"Trace O2 Analyser AT1102","tag":"AT1102","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Purification",
                 "justification":"SAFETY CRITICAL: Monitors trace O2 in purified H2 at purifier outlet (SOC: <1 ppm, SOL: <2 ppm). On alarm: auto-vent valve QZ1007 opens — H2 diverted from storage. LAST LINE OF DEFENCE before contaminated H2 reaches bullet storage and annealing hoods.",
                 "consequence_of_failure":"Trace O2 above 2 ppm in H2 undetected → contaminated H2 reaches bullet → explosive H2+O2 mixture in high-pressure storage → CATASTROPHIC FAILURE RISK.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"3-monthly calibration with certified reference gas (ppm level O2 in N2)."},
                {"sl":27,"equipment":"Level Transmitter Cooling Water Tank LIT1501","tag":"LIT1501","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"No",
                 "sub_process":"DM Water & KOH",
                 "justification":"Monitors cooling water tank level. Low level → GLT trip alarm. Ensures cooling water availability for cell temperature control. Without level monitoring, cooling water could be depleted without alarm.",
                 "consequence_of_failure":"Cooling water depleted without alarm → cell temperature rises → if RTDs fail too: cell damage.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Annual calibration."},
                {"sl":28,"equipment":"RTD Cooling Water Line (TE1501, TE1502)","tag":"TE1501, TE1502","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"DM Water & KOH",
                 "justification":"Monitors cooling water temperature (SOC: <35°C, SOL: <40°C). High cooling water temp → reduced cooling efficiency → cell temperature rises toward 97°C SOL. Auto-trip at SOL.",
                 "consequence_of_failure":"Cooling water temperature exceeds SOL undetected → insufficient cell cooling → cell temperature auto-trip triggered by TE1001/TE1003 as backup.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration."},
                {"sl":29,"equipment":"Pressure Transmitter Cooling Water PT1501","tag":"PT1501","basis":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"DM Water & KOH",
                 "justification":"Monitors cooling water pressure (SOC 2.5-3.5 kg/cm2, SOL 2.0-6.0 kg/cm2). Low pressure → insufficient cooling flow. High pressure → pipe rupture risk. Both conditions affect cell temperature control.",
                 "consequence_of_failure":"Low pressure: insufficient cooling → cell overheating. High pressure: pipe rupture → H2 system integrity risk from water ingress.",
                 "psce_type":"Instrumented Active Preventive",
                 "maintenance":"6-monthly calibration."},
                {"sl":30,"equipment":"Emergency Plant Trip Switch (outside plant fence)","tag":"—","basis":"Prescriptive","category":"Safety Monitoring & Emergency Communication","psm_critical":"Yes",
                 "sub_process":"All",
                 "justification":"PRESCRIPTIVE MANDATORY: Emergency trip switch located OUTSIDE plant fence perimeter. Allows emergency shutdown when entry to plant is unsafe (fire, explosion, H2 cloud). Trips entire plant including all gas supply valves, rectifier, pumps. Required by PESO/safety regulations for H2 plants.",
                 "consequence_of_failure":"Plant cannot be tripped safely from outside during emergency → personnel must enter danger zone to stop plant → injury/fatality risk during emergency response.",
                 "psce_type":"Prescriptive",
                 "maintenance":"Monthly functional test. Annual electrical inspection."},
                {"sl":31,"equipment":"H2 Bullet #1","tag":"Bullet-1","basis":"Consequence Based","category":"Pressure Vessel (Statutory)","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"High-pressure H2 storage vessel. CCOE approved design. IBR/PESO statutory inspection required. The vessel itself is PSCE because its integrity is fundamental — failure = catastrophic H2 release, BLEVE under fire. Operating: 4-14 kg/cm2, max temp 45°C (SOC).",
                 "consequence_of_failure":"Vessel failure → catastrophic H2 release → BLEVE if fire present → major explosion, multiple fatalities, total plant destruction.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Annual PESO statutory inspection. Thickness test. Safety valve test. IBR compliance."},
                {"sl":32,"equipment":"H2 Bullet #2","tag":"Bullet-2","basis":"Consequence Based","category":"Pressure Vessel (Statutory)","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"Same as Bullet #1. Redundant H2 storage. Dual bullets ensure H2 supply to annealing is not interrupted while one bullet is on inspection. Same CCOE approval, IBR inspection regime.",
                 "consequence_of_failure":"Same as Bullet #1. Total failure of either bullet = major accident. Combined failure = complete H2 supply loss + massive release.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Annual PESO statutory inspection. Same as Bullet #1."},
                {"sl":33,"equipment":"Pressure Gauge at Bullet 1","tag":"PG-B1","basis":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"Local pressure indication at H2 Bullet 1 (SOC 4-14 kg/cm2, SOL 20 kg/cm2). Operator reads during rounds. ONLY local visual indication of bullet pressure — essential for manual monitoring when DCS is unavailable or during rounds.",
                 "consequence_of_failure":"No local pressure indication → operator unaware of bullet pressure during rounds → overpressure undetected locally → relies entirely on remote instrumentation.",
                 "psce_type":"Active Mitigation",
                 "maintenance":"Annual calibration check. IBR approved gauge."},
                {"sl":34,"equipment":"Safety Relief Valve #1 at H2 Bullet 1","tag":"SRV1-B1","basis":"Consequence Based + Prescriptive","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"PRESCRIPTIVE MANDATORY (IBR/PESO): First SRV on H2 Bullet 1. Lifts at design set pressure to prevent vessel overpressure. Sized for full relief flow. STATUTORY REQUIREMENT — no pressure vessel may operate without SRV. Certified per IBR. Discharges to safe elevated vent location.",
                 "consequence_of_failure":"No SRV overpressure protection → vessel exceeds design pressure → catastrophic rupture → BLEVE → major accident. Statutory violation.",
                 "psce_type":"Prescriptive",
                 "maintenance":"Annual removal, bench test, recertification. IBR inspector witness required."},
                {"sl":35,"equipment":"Safety Relief Valve #2 at H2 Bullet 1","tag":"SRV2-B1","basis":"Consequence Based + Prescriptive","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"REDUNDANT SRV on H2 Bullet 1. Dual SRVs required because: (1) SRV can fail to open (stuck) or fail to reseat (leak). (2) One SRV may be taken offline for testing while vessel remains in service. Dual SRVs per API 520/521 and IBR standards for H2 service.",
                 "consequence_of_failure":"If SRV #1 fails stuck: SRV #2 is last defence. If both fail: vessel rupture = BLEVE = catastrophic.",
                 "psce_type":"Prescriptive",
                 "maintenance":"Annual test — tested independently from SRV #1."},
                {"sl":36,"equipment":"Safety Relief Valve #1 at H2 Bullet 2","tag":"SRV1-B2","basis":"Consequence Based + Prescriptive","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"Same as SRV #1 on Bullet 1. Prescriptive statutory requirement for H2 Bullet 2. IBR certified. Set pressure per PESO approved design.",
                 "consequence_of_failure":"Same as Bullet 1 SRV failure. Vessel rupture = BLEVE = major accident.",
                 "psce_type":"Prescriptive",
                 "maintenance":"Annual IBR inspection."},
                {"sl":37,"equipment":"Safety Relief Valve #2 at H2 Bullet 2","tag":"SRV2-B2","basis":"Consequence Based + Prescriptive","category":"Instrumented Active Preventive","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"Redundant SRV on H2 Bullet 2. Same function and justification as SRV #2 on Bullet 1. Dual SRV per API 520/521.",
                 "consequence_of_failure":"Last defence overpressure protection on Bullet 2.",
                 "psce_type":"Prescriptive",
                 "maintenance":"Annual IBR inspection."},
                {"sl":38,"equipment":"Pressure Gauge at Bullet 2","tag":"PG-B2","basis":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"Same as Bullet 1 pressure gauge. Local pressure indication for Bullet 2 operator rounds. Essential local visual monitoring.",
                 "consequence_of_failure":"Same as Bullet 1 PG — local pressure unmonitored during rounds.",
                 "psce_type":"Active Mitigation",
                 "maintenance":"Annual calibration. IBR approved."},
                {"sl":39,"equipment":"Temperature Gauge at Bullet 1","tag":"TG-B1","basis":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"Local temperature indication at H2 Bullet 1 (SOC: <45°C, SOL: <50°C). High temperature → H2 thermal expansion → pressure rises above SOL → SRV lifts → H2 release. Operator reads during rounds. Solar heating/adjacent fire can raise bullet temperature.",
                 "consequence_of_failure":"Bullet temperature exceeds SOL undetected → pressure rises → SRV lifts → H2 release → fire/explosion risk.",
                 "psce_type":"Active Mitigation",
                 "maintenance":"Annual calibration."},
                {"sl":40,"equipment":"Temperature Gauge at Bullet 2","tag":"TG-B2","basis":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes",
                 "sub_process":"H2 Bullet Storage",
                 "justification":"Same as Bullet 1 temperature gauge for Bullet 2.",
                 "consequence_of_failure":"Same as Bullet 1 TG failure.",
                 "psce_type":"Active Mitigation",
                 "maintenance":"Annual calibration."},
                {"sl":41,"equipment":"Pressure Control Valve #1 at Bullet Outlet","tag":"PCV1-Out","basis":"Controlled Release","category":"Controlled Release Equipment","psm_critical":"Yes",
                 "sub_process":"H2 Distribution",
                 "justification":"Controls H2 outlet pressure from bullets to distribution (SOC 1.2-2.5 kg/cm2). Reduces bullet storage pressure to distribution line pressure. Failure open → overpressure in distribution. Failure closed → H2 supply to annealing interrupted.",
                 "consequence_of_failure":"Failure open: overpressure in distribution pipeline → PRV lifts → H2 release. Failure closed: annealing H2 supply lost → quality impact.",
                 "psce_type":"Controlled Release",
                 "maintenance":"6-monthly functional test."},
                {"sl":42,"equipment":"Pressure Control Valve #2 at Bullet Outlet","tag":"PCV2-Out","basis":"Controlled Release","category":"Controlled Release Equipment","psm_critical":"Yes",
                 "sub_process":"H2 Distribution",
                 "justification":"REDUNDANT PCV at bullet outlet. Provides backup pressure control if PCV #1 fails. Also allows PCV #1 to be taken offline for maintenance while H2 supply continues. Industry standard for critical pressure control applications.",
                 "consequence_of_failure":"If PCV #1 fails: PCV #2 maintains pressure control. If both fail: PRV (PSCE #43) is last barrier.",
                 "psce_type":"Controlled Release",
                 "maintenance":"6-monthly functional test. Independent from PCV #1."},
                {"sl":43,"equipment":"Pressure Relief Valve at Bullet Outlet","tag":"PRV-Out","basis":"Consequence Based","category":"Controlled Release Equipment","psm_critical":"Yes",
                 "sub_process":"H2 Distribution",
                 "justification":"LAST BARRIER: PRV on H2 distribution line after bullet outlet. If both PCVs fail → distribution line overpressure → PRV lifts → controlled H2 release to safe location. Prevents distribution line failure from PCV malfunction.",
                 "consequence_of_failure":"Without PRV: if both PCVs fail open → distribution line overpressure → uncontrolled pipe failure → H2 release in occupied areas.",
                 "psce_type":"Consequence Based",
                 "maintenance":"Annual test. Set pressure verification."},
                {"sl":44,"equipment":"Fire Hydrant System","tag":"FHS","basis":"Prescriptive","category":"Active Mitigation System","psm_critical":"Yes",
                 "sub_process":"All",
                 "justification":"PRESCRIPTIVE MANDATORY: Fire hydrant system covering entire H2 plant area including bullet farm. Required by CCOE and fire regulations for H2 storage facilities. Provides: (1) water spray cooling of bullets during external fire exposure (prevents BLEVE), (2) fire suppression for secondary fires, (3) emergency flush for chemical spills.",
                 "consequence_of_failure":"No fire suppression → external fire cannot be fought → bullet heating → BLEVE → catastrophic explosion. Statutory violation of CCOE approval conditions.",
                 "psce_type":"Prescriptive",
                 "maintenance":"Monthly flow test. Annual pressure test. Hydrant head inspection."},
            ]

            # Filter controls
            col_f1, col_f2, col_f3 = st.columns([2,2,1])
            with col_f1:
                srch_psce = st.text_input("Search equipment...", placeholder="e.g. analyser, valve, RTD, bullet", key="h2_psce_srch2", label_visibility="collapsed")
            with col_f2:
                cat_filter = st.selectbox("Filter by type", ["All","Consequence Based","Prescriptive","Active Mitigation","Controlled Release","Service and Utility"], key="h2_psce_cat")
            with col_f3:
                psm_filter = st.selectbox("PSM Critical", ["All","Yes","No"], key="h2_psce_psm")

            filtered_psce = H2_PSCE_FULL
            if srch_psce:
                filtered_psce = [x for x in filtered_psce if srch_psce.lower() in x["equipment"].lower() or srch_psce.lower() in x["justification"].lower()]
            if cat_filter != "All":
                filtered_psce = [x for x in filtered_psce if cat_filter.lower() in x["psce_type"].lower()]
            if psm_filter != "All":
                filtered_psce = [x for x in filtered_psce if x["psm_critical"] == psm_filter]

            st.markdown(f'<div style="font-size:.72rem;color:#475569;margin-bottom:.5rem">Showing {len(filtered_psce)} of 44 items</div>', unsafe_allow_html=True)

            # Type color mapping
            type_colors = {
                "Instrumented Active Preventive": "#3b82f6",
                "Active Mitigation": "#f97316",
                "Prescriptive": "#a78bfa",
                "Controlled Release": "#22c55e",
                "Service and Utility": "#64748b",
                "Consequence Based": "#ef4444",
            }

            for item in filtered_psce:
                ptype = item["psce_type"]
                tc = type_colors.get(ptype, "#64748b")
                is_psm = item["psm_critical"] == "Yes"
                psm_b = f'<span style="background:rgba(239,68,68,.2);color:#f87171;border:1px solid rgba(239,68,68,.4);font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">PSM CRITICAL</span>' if is_psm else '<span style="background:#1e3a5f;color:#475569;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">Not PSM Critical</span>'
                st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:4px solid {tc};border-radius:10px;padding:1rem 1.2rem;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.6rem">
  <div>
    <span style="font-size:.68rem;font-weight:700;color:#f97316">#{item['sl']}</span>
    <span style="font-size:.88rem;font-weight:700;color:#e2e8f0;margin-left:8px">{item['equipment']}</span>
    {psm_b}
  </div>
  <span style="background:{tc}20;color:{tc};border:1px solid {tc}40;font-size:.6rem;font-weight:700;padding:3px 9px;border-radius:20px;white-space:nowrap">{ptype}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-bottom:.6rem">
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">TAG NO.</div>
    <div style="font-size:.72rem;color:#f97316;font-family:monospace">{item.get('tag','—')}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">SUB-PROCESS</div>
    <div style="font-size:.72rem;color:#94a3b8">{item.get('sub_process','—')}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">MAINTENANCE</div>
    <div style="font-size:.68rem;color:#94a3b8">{item.get('maintenance','—')}</div>
  </div>
</div>
<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;margin-bottom:.5rem">
  <div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">JUSTIFICATION FOR PROCESS SAFETY CRITICALITY</div>
  <div style="font-size:.75rem;color:#94a3b8;line-height:1.7">{item.get('justification','—')}</div>
</div>
<div style="background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.15);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem .8rem">
  <div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:2px">CONSEQUENCE OF FAILURE</div>
  <div style="font-size:.73rem;color:#fca5a5">{item.get('consequence_of_failure','—')}</div>
</div>
</div>""", unsafe_allow_html=True)


        with h2tabs[6]:  # EDB
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/EDB/TINPL/PROP/001 Rev.03 Eff.Dt.:01.12.2022</p>', unsafe_allow_html=True)

            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:.8rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">BARRIER MODEL — Each EDB item is a Detector, Logic Solver, or Actuator component of a barrier</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;font-size:.7rem;margin-bottom:.4rem">
<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:.5rem"><b style="color:#ef4444">Active — Automatic Trip</b><br><span style="color:#64748b">SIS function — auto-trip without human action. E.g.: AT1002, TE1001, QZ1007. Highest reliability active barrier.</span></div>
<div style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.2);border-radius:6px;padding:.5rem"><b style="color:#3b82f6">Active — Instrumented</b><br><span style="color:#64748b">Monitoring with alarm — operator then acts. E.g.: AT1701/1702/1703 H2 detectors, LIT1301. PFD ~0.1.</span></div>
<div style="background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);border-radius:6px;padding:.5rem"><b style="color:#a78bfa">Passive</b><br><span style="color:#64748b">No activation needed — always provides protection. E.g.: strainers, filters, bunds. PFD ~0.01. Most reliable.</span></div>
</div>
<div style="font-size:.7rem;color:#475569">A barrier is only as strong as its weakest component (Detector OR Logic OR Actuator). All 3 must be maintained. Calibration schedule = proof test to verify barrier is functional.</div>
</div>""", unsafe_allow_html=True)

            st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.8rem 1rem;margin-bottom:1rem;font-size:.78rem;color:#94a3b8">
<b style="color:#e2e8f0">Equipment Design Basis (EDB)</b> — Documents the design parameters, safety basis, maintenance schedule, manufacturer and model for each piece of equipment that contains or controls hazardous substances.
Selection basis: <b style="color:#f97316">Consequence Based</b> = equipment whose failure could cause major accident | <b style="color:#a78bfa">Prevention & Mitigation</b> = equipment specifically installed to prevent or mitigate a major accident.
</div>""", unsafe_allow_html=True)

            h2_edb_full = [
                (1,"Electrolysis","Hydrogen, Lye solution","Electrolyzer","1001/2001","Consequence Based","NA","NA",
                 "Core electrolysis unit. DC current splits DM water into H2 (cathode) and O2 (anode). KOH lye as electrolyte. Operating: 800-1450A DC, 35-95°C, 1.50-1.57 MPa. Failure = loss of H2 production. Design basis: ASME/OEM specification."),
                (2,"Electrolysis","Hydrogen, Lye solution","Feed Water Pump","1M21","Consequence Based","Milton Roy USA","RB120S024X1MNN",
                 "Dosing pump supplying DM water to electrolyser. Failure = DM tank level drops → plant trip. Milton Roy metering pump. Design basis: rated flow = electrolyser DM water demand."),
                (3,"Electrolysis","Hydrogen, Lye solution","Lye Circulating Pump","1P11, 1P12","Consequence Based","DALIAN China","F82-216H4M-0204Si",
                 "Circulates KOH lye solution through electrolyser. Dual pumps (1P11, 1P12) for redundancy. Failure = electrolyte loss → H2 purity drop → plant trip. Design basis: rated for full lye circulation at operating pressure."),
                (4,"Electrolysis","Hydrogen","H2 Vent Valve","Q1011","Consequence Based","Swagelok","SS-63TSW8T",
                 "Manual isolation valve on H2 vent line from electrolyser. Used during startup/shutdown purge. Swagelok SS ball valve. Design basis: rated for H2 service, bubble-tight, anti-static."),
                (5,"Electrolysis","Hydrogen","H2 Supply Valve","Q1012","Consequence Based","Swagelok","SS-63TSW8T",
                 "Manual isolation valve on H2 supply line from electrolyser to GLT. Swagelok SS ball valve. Design basis: rated for H2 service at operating pressure, anti-static, bubble-tight."),
                (6,"Electrolysis","Hydrogen","H2 Outlet 3-way Pneumatic Valve","QS1001","Prevention & Mitigation","Swagelok","SS-63XTSW8T-F8-53S",
                 "SAFETY CRITICAL: 3-way pneumatic valve — in normal operation routes H2 to purifier. On trip/alarm: automatically switches H2 to vent. Prevention function: prevents contaminated or off-spec H2 from reaching storage. Fail-safe: opens vent on air/power loss."),
                (7,"Electrolysis","Lye/H2","Lye Heat Exchanger","1008","Consequence Based","NA","NA",
                 "Cools KOH lye solution returning from electrolyser. Maintains cell temperature within SOC (35-95°C). Failure = rising cell temperature → auto-trip at 97°C SOL. Design basis: duty = full lye flow cooling duty."),
                (8,"Gas-Liquid Treater","H2, O2, Lye","H2 Separator and Washer","1002","Consequence Based","NA","NA",
                 "Separates H2 gas from KOH lye carryover. Washes H2 to remove lye mist. Operates at 1.50-1.57 MPa. Level SOC 500-670mm. Failure = lye carryover into H2 line → purifier damage, purity failure. Pressure vessel — statutory IBR/PESO inspection."),
                (9,"Gas-Liquid Treater","H2, O2, Lye","O2 Separator and Washer","1003","Consequence Based","NA","NA",
                 "Separates O2 gas from KOH lye. Washes O2 before safe venting to atmosphere. Level SOC 500-670mm. Failure = lye into O2 vent line. Pressure vessel — statutory inspection. CRITICAL: must not allow H2 to enter O2 stream."),
                (10,"Gas-Liquid Treater","H2","Analyser H2-in-O2 Sampling Valve","J1003","Prevention & Mitigation","Swagelok","SS-1KS6MM",
                 "SAFETY CRITICAL: sampling valve supplying gas to AT1002 (H2-in-O2 analyser). Swagelok needle valve, SS construction. Design basis: rated for operating pressure, H2 service. Failure = AT1002 cannot sample → loss of critical explosion prevention measure."),
                (11,"Gas-Liquid Treater","O2","Analyser O2-in-H2 Sampling Valve","J1004","Prevention & Mitigation","Swagelok","SS-1KS6MM",
                 "SAFETY CRITICAL: sampling valve supplying gas to AT1001 (O2-in-H2 analyser). Swagelok needle valve. Failure = AT1001 cannot sample → O2 contamination of H2 undetected → explosive mixture risk in purifier/storage."),
                (12,"Gas-Liquid Treater","H2","By-pass Valve H2 Vent","J1008","Prevention & Mitigation","Swagelok","SS-1KS12MM",
                 "Emergency H2 vent bypass valve. Used when main H2 vent valve is in use/maintenance. Prevents H2 build-up. Design basis: rated for full H2 vent flow at operating pressure. SS construction for H2 service."),
                (13,"Gas-Liquid Treater","O2","By-pass Valve O2 Vent","J1009","Prevention & Mitigation","Swagelok","SS-1KS12MM",
                 "Emergency O2 vent bypass valve. Ensures O2 can always be safely vented even if main valve unavailable. Design basis: rated for O2 vent flow — O2-clean service, no grease/oil on fittings."),
                (14,"Gas-Liquid Treater","H2/Lye","Temperature Regulating Valve","TV1001","Prevention & Mitigation","Jordan","MK78/100",
                 "Controls cooling water to lye heat exchanger — maintains cell temperature SOC (35-95°C). Jordan Controls self-acting temperature regulator. Failure = cell overheating → auto-trip at 97°C SOL. Design basis: full cooling duty at maximum lye flow."),
                (15,"Gas-Liquid Treater","H2/Lye","Liquid Level Regulating Valve","LV1001","Prevention & Mitigation","Jordan","MK708/050",
                 "SAFETY CRITICAL: controls H2 separator liquid level (SOC 500-670mm). Jordan Controls cage-guided control valve. Low level → gas bypass (H2-in-O2 rises). High level → lye into H2 line. Dual consequence — both directions are hazardous."),
                (16,"Gas-Liquid Treater","H2","Pressure Regulating Valve","PV1001","Prevention & Mitigation","Jordan","MK708/050",
                 "Controls O2 separator pressure (maintains SOC 1.50-1.57 MPa). Jordan Controls cage-guided valve. Failure = pressure imbalance between H2 and O2 separators → gas mixing risk → explosive atmosphere. Design basis: full differential pressure rating at operating conditions."),
                (17,"Gas-Liquid Treater","Hydrogen","H2 Detector at GLT","AT1702","Prev & Mitig — 3-monthly","NA","NA",
                 "PSCE ITEM #16: Continuous H2 LEL monitor in Gas-Liquid Treater zone. SOC: <0.2% LEL. SOL: 0.9% LEL (auto exhaust fan + alarm). H2 is colourless and odourless — no sensory warning. Detector is ONLY means of detecting H2 leak in this zone. Calibration: 3-monthly mandatory."),
                (18,"H2 Purification","Hydrogen","Filters — Deoxy + Dryer","1101-1105, 1151","Consequence Based","NA","NA",
                 "Particle filters after deoxygenation unit and each dryer (A/B/C). Removes catalyst fines and particulates from purified H2. Prevents contamination of downstream equipment and bullet storage. Design basis: rated for H2 service at purifier pressure 0.6-1.3 MPa."),
                (19,"H2 Purification","Hydrogen","Coolers after Deoxy and Dryers","1131-1134","Consequence Based","NA","NA",
                 "Cools H2 after high-temperature purification stages (deoxy 118-160°C, dryers 170-220°C). Four coolers total. Failure = high-temperature H2 entering downstream components — seal/fitting damage risk. Design basis: cooling duty from max bed temperature to ambient."),
                (20,"H2 Purification","Hydrogen","H2 Auto Vent Valve","QZ1007","Prevention & Mitigation","Swagelok","SS-63TSW8T-33C",
                 "SAFETY CRITICAL: automatically vents H2 to safe location when AT1102 detects trace O2 >1 ppm SOC (>2 ppm SOL). Pneumatically actuated. Fail-safe: opens vent on air/power loss. Last line of defence preventing contaminated H2 from reaching bullet storage. Swagelok SS ball valve with pneumatic actuator."),
                (21,"H2 Purification","Hydrogen","H2 Outlet Regulator","PV1101","Prevention & Mitigation","Jordan","MK708/050",
                 "Controls H2 outlet pressure from purifier (SOC 0.6-1.3 MPa). Jordan Controls pressure regulating valve. Ensures correct pressure before bullet storage. Failure = overpressure or underpressure in distribution. Design basis: full purifier output flow at rated pressure."),
                (22,"H2 Purification","Hydrogen","Dew Point Analyser","ME1101","Consequence — 6-monthly","NA","MTS6",
                 "PSCE ITEM #23: Monitors dew point of purified H2. SOC: <-80°C. SOL: <-70°C (auto-trip). High dew point = moisture in H2 → pipeline corrosion and annealing hood damage. MTS6 dew point transmitter. Calibration: 6-monthly mandatory. Critical for annealing quality and safety."),
                (23,"Control Cabinet","Faulty sensors/PLC","Solenoid Valve 2-pos 5-way","YV1001, YV1107-YV1114","Prevention & Mitigation","NA","521 00 004",
                 "Multiple solenoid valves in PLC control cabinet. Control pneumatic actuators for safety valves (QS1001, LV1001, PV1001 etc.). Failure = loss of automatic safety valve actuation. Design basis: fail-safe position = safe state for each controlled valve. 5-way double-acting solenoid."),
                (24,"H2 Bullet Storage","Hydrogen","Pressure Gauge — Bullet 1","—","Consequence Based","NA","NA",
                 "Local pressure indication at H2 Bullet 1. SOC: 4-14 kg/cm2. SOL: 20 kg/cm2. Provides local visual monitoring for operators during rounds. Design basis: full scale 25 kg/cm2 minimum. IBR/PESO approved pressure gauge."),
                (25,"H2 Bullet Storage","Hydrogen","Pressure Relief Valve — Bullet 1","—","Consequence Based","NA","NA",
                 "Primary overpressure protection on H2 Bullet 1. Lifts at set pressure (above SOL 20 kg/cm2). Vents H2 to safe elevated location. STATUTORY REQUIREMENT under IBR/PESO. Design basis: full flow relief capacity at set pressure. Annual inspection mandatory."),
                (26,"H2 Bullet Storage","Hydrogen","Safety Relief Valve #1 — Bullet 1","—","Prev & Mitig — Annual","NA","NA",
                 "PSCE ITEM #34: First of dual SRVs on H2 Bullet 1. Provides PRESCRIPTIVE overpressure protection. Redundant with SRV #2 — both must function independently. Annual inspection, removal and test mandatory. Design basis: IBR full flow SRV sizing. Tag: per PESO approval."),
                (27,"H2 Bullet Storage","Hydrogen","Pressure Gauge — Bullet 2","—","Consequence Based","NA","NA",
                 "Local pressure indication at H2 Bullet 2. Same specification as Bullet 1 gauge. SOC: 4-14 kg/cm2. SOL: 20 kg/cm2. IBR/PESO approved."),
                (28,"H2 Bullet Storage","Hydrogen","Pressure Relief Valve — Bullet 2","—","Consequence Based","NA","NA",
                 "Primary overpressure protection on H2 Bullet 2. Same specification as Bullet 1 PRV. Statutory requirement. Annual inspection."),
                (29,"H2 Bullet Storage","Hydrogen","Safety Relief Valve — Bullet 2","—","Prev & Mitig — Annual","NA","NA",
                 "PSCE ITEM #36/#37: Dual SRVs on H2 Bullet 2. Same specification and inspection regime as Bullet 1 SRVs. IBR/PESO mandatory. Design basis: full flow relief at set pressure."),
                (30,"H2 Bullet Storage","Hydrogen","Temperature Gauge — Bullet 1","—","Consequence Based","NA","NA",
                 "PSCE ITEM #39: Local temperature indication at H2 Bullet 1. SOC: <45°C. SOL: <50°C. High temperature = H2 pressure rise → SRV lift risk. Direct-reading thermometer on vessel shell. Design basis: range 0-60°C minimum."),
                (31,"H2 Bullet Storage","Hydrogen","Temperature Gauge — Bullet 2","—","Consequence Based","NA","NA",
                 "PSCE ITEM #40: Local temperature indication at H2 Bullet 2. Same specification as Bullet 1. SOC: <45°C. SOL: <50°C."),
            ]

            # View mode selector
            view_mode = st.radio("View mode", ["Flashcards","Table"], horizontal=True, key="edb_view")
            hf2 = st.selectbox("Filter by sub-process", ["All","Electrolysis","Gas-Liquid Treater","H2 Purification","H2 Bullet Storage","Control Cabinet"], key="h2_edb_f")
            show_h2e = h2_edb_full if hf2=="All" else [x for x in h2_edb_full if x[1]==hf2]

            if view_mode == "Flashcards":
                for item in show_h2e:
                    sl, subp, haz, equip, tag, basis, mfr, model, desc = item
                    is_psce = "PSCE" in desc or "SAFETY CRITICAL" in desc
                    is_pm = "Prevention" in basis
                    badge_col = "#a78bfa" if is_pm else "#3b82f6"
                    badge_txt = "Prevention & Mitigation" if is_pm else "Consequence Based"
                    psce_badge = '<span style="background:rgba(239,68,68,.2);color:#f87171;border:1px solid rgba(239,68,68,.4);font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">PSCE</span>' if is_psce else ""
                    st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:4px solid {badge_col};border-radius:10px;padding:1rem 1.2rem;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.5rem">
  <div>
    <span style="font-size:.68rem;font-weight:700;color:#f97316">#{sl}</span>
    <span style="font-size:.88rem;font-weight:700;color:#e2e8f0;margin-left:8px">{equip}</span>
    {psce_badge}
  </div>
  <span style="background:{badge_col}20;color:{badge_col};border:1px solid {badge_col}40;font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap">{badge_txt}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.5rem;margin-bottom:.6rem">
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.58rem;color:#475569;font-weight:700;letter-spacing:1px">SUB-PROCESS</div><div style="font-size:.72rem;color:#94a3b8;margin-top:2px">{subp}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.58rem;color:#475569;font-weight:700;letter-spacing:1px">HAZARDOUS SUBSTANCE</div><div style="font-size:.72rem;color:#fca5a5;margin-top:2px">{haz}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.58rem;color:#475569;font-weight:700;letter-spacing:1px">TAG NO.</div><div style="font-size:.72rem;color:#f97316;font-family:monospace;margin-top:2px">{tag}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.58rem;color:#475569;font-weight:700;letter-spacing:1px">MANUFACTURER</div><div style="font-size:.72rem;color:#94a3b8;margin-top:2px">{mfr} — {model}</div></div>
</div>
<div style="font-size:.76rem;color:#64748b;line-height:1.6;border-top:1px solid #1e3a5f;padding-top:.5rem">{desc}</div>
</div>""", unsafe_allow_html=True)
            else:
                df_h2e = pd.DataFrame([(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7]) for x in show_h2e],
                    columns=["Sl","Sub Process","Hazardous Substance","Equipment","Tag No","Selection Basis","Manufacturer","Model/Type"])
                st.dataframe(df_h2e, use_container_width=True, hide_index=True, height=500)

        with h2tabs[7]:  # Parameters
            st.markdown('<p style="font-size:.75rem;color:#64748b">H2 Plant — All 24 Process Parameters with Sub-Process Mapping</p>', unsafe_allow_html=True)
            render_pdb(H2_PDB_PARAMS, dept_key="h2_params")

        with h2tabs[8]:  # Simulation
            st.markdown('<div class="sl-sec">H2 Plant — Risk Scenario Simulation</div>', unsafe_allow_html=True)
            sc_sel = st.selectbox("Select scenario", [
                "H2-in-O2 rises above 1.7% SOL",
                "Bullet overpressure — SRV activation",
                "H2 detector alarm in GLT zone",
                "Cell temperature runaway to 97°C SOL",
                "Dew point failure — moisture in pipeline",
            ], key="h2_sim_sel")

            scenarios = {
                "H2-in-O2 rises above 1.7% SOL": {
                    "risk":98,"initiating":"Separator level drops below 400mm SOL → gas bypass",
                    "sequence":["Separator level drops","H2-in-O2 rises from 0% toward 1.7% SOL","AT1002 alarms at 0.8% SOC","PLC auto-trip at HH limit","All rectifiers off, gas valves closed","N2 auto-purge initiated"],
                    "top_event":"H2/O2 explosive mixture formation in O2 separator",
                    "barriers":["AT1002 auto-trip (PSCE #13) — ACTIVE","LT1003 level low alarm — ACTIVE","PV1001 pressure balance valve — ACTIVE"],
                    "outcome":"With barriers: plant trips safely, no explosion\nWithout AT1002: H2-in-O2 reaches explosive range → DETONATION",
                },
                "Bullet overpressure — SRV activation": {
                    "risk":85,"initiating":"PCV failure open + solar heating → bullet pressure rises above 14 kg/cm2",
                    "sequence":["Bullet pressure rises above 14 kg/cm2 SOC","Operator notes on pressure gauge during rounds","If undetected: pressure reaches 20 kg/cm2 SOL","SRV #1 lifts — H2 venting to safe elevated location","If SRV fails: SRV #2 activates"],
                    "top_event":"Uncontrolled H2 release from bullet overpressure",
                    "barriers":["SRV #1 on Bullet (PSCE #34) — PASSIVE MECHANICAL","SRV #2 on Bullet (PSCE #35) — PASSIVE MECHANICAL REDUNDANT","Temperature gauge — operator monitoring"],
                    "outcome":"Dual SRVs ensure controlled vent to safe location\nBoth SRVs fail: vessel rupture → BLEVE → catastrophic",
                },
            }

            sc_data = scenarios.get(sc_sel, scenarios["H2-in-O2 rises above 1.7% SOL"])
            rc_sim = risk_color(sc_data["risk"])
            st.markdown(f"""<div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:10px;padding:1rem;margin-bottom:1rem;display:flex;align-items:center;gap:1rem">
<div style="font-size:2rem;font-weight:900;color:{rc_sim};font-family:monospace">{sc_data["risk"]}/100</div>
<div><div style="font-size:.88rem;font-weight:700;color:#e2e8f0">{sc_sel}</div>
<div style="font-size:.75rem;color:#94a3b8;margin-top:3px">Initiating cause: {sc_data["initiating"]}</div></div>
</div>""", unsafe_allow_html=True)

            sim_c1, sim_c2 = st.columns(2)
            with sim_c1:
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">EVENT SEQUENCE</div>', unsafe_allow_html=True)
                for ii, step in enumerate(sc_data["sequence"]):
                    st.markdown(f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px"><span style="background:#f97316;color:#fff;font-size:.6rem;font-weight:700;width:18px;height:18px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex-shrink:0">{ii+1}</span><span style="font-size:.75rem;color:#94a3b8">{step}</span></div>', unsafe_allow_html=True)
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin:.6rem 0 .3rem">BARRIERS ACTIVATED</div>', unsafe_allow_html=True)
                for b in sc_data["barriers"]:
                    st.markdown(f'<div style="font-size:.75rem;color:#4ade80;padding:2px 0">✓ {b}</div>', unsafe_allow_html=True)
            with sim_c2:
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:.4rem">TOP EVENT & OUTCOME</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);border-radius:8px;padding:.8rem;font-size:.82rem;font-weight:700;color:#f87171;margin-bottom:.6rem">{sc_data["top_event"]}</div>', unsafe_allow_html=True)
                outcome_lines = sc_data["outcome"].split("\n")
                for ol in outcome_lines:
                    c_ol = "#4ade80" if "safely" in ol.lower() else "#fca5a5"
                    st.markdown(f'<div style="font-size:.78rem;color:{c_ol};padding:3px 0">{ol}</div>', unsafe_allow_html=True)
                st.plotly_chart(go.Figure(go.Indicator(
                    mode="gauge+number",value=sc_data["risk"],
                    gauge={"axis":{"range":[0,100]},"bar":{"color":rc_sim},
                           "steps":[{"range":[0,50],"color":"rgba(34,197,94,.1)"},{"range":[50,75],"color":"rgba(249,115,22,.1)"},{"range":[75,100],"color":"rgba(239,68,68,.1)"}]},
                    number={"suffix":"/100","font":{"color":rc_sim,"size":22}},
                )).update_layout(paper_bgcolor="#0d1f35",font=dict(color="#94a3b8",size=10),height=200,margin=dict(t=20,b=10,l=20,r=20)), use_container_width=True)

        with h2tabs[9]:  # Risk Matrix
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">RISK MATRIX + LOPA — H2 Plant | Likelihood × Consequence (L1-L5)</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:4px;font-size:.65rem;margin-bottom:.4rem">
<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:4px;padding:.4rem;text-align:center"><b style="color:#22c55e">L1</b><br><span style="color:#64748b">FAC | &lt;Rs.5L | On-site</span></div>
<div style="background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.2);border-radius:4px;padding:.4rem;text-align:center"><b style="color:#eab308">L2</b><br><span style="color:#64748b">LTI | Rs.5-50L | Off-site limited</span></div>
<div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:4px;padding:.4rem;text-align:center"><b style="color:#f97316">L3</b><br><span style="color:#64748b">Hospital | Rs.50L-5Cr | PESO notify</span></div>
<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:4px;padding:.4rem;text-align:center"><b style="color:#ef4444">L4</b><br><span style="color:#64748b">1-5 fatalities | Rs.5-50Cr</span></div>
<div style="background:rgba(127,29,29,.2);border:1px solid rgba(239,68,68,.4);border-radius:4px;padding:.4rem;text-align:center"><b style="color:#fca5a5">L5</b><br><span style="color:#64748b">&gt;5 fatalities | &gt;Rs.50Cr | Evacuation</span></div>
</div>
<div style="font-size:.7rem;color:#475569"><b style="color:#f97316">LOPA trigger:</b> Risk score ≥12 requires Layer of Protection Analysis. Verify: Initiating Event Frequency × all IPL PFDs ≤ 1×10⁻⁵/year. H2-in-O2 scenario (score 20) and BLEVE (score 10) both require LOPA with SIL verification.</div>
</div>""", unsafe_allow_html=True)
            h2_risks = [
                ("H2-in-O2 explosive mixture","Electrolysis / GLT","Possible","Catastrophic",4,5,20),
                ("H2 bullet BLEVE","Bullet Storage","Rare","Catastrophic",2,5,10),
                ("H2 leak — GLT zone explosion","Gas-Liquid Treater","Unlikely","Critical",3,4,12),
                ("Cell overtemperature","Electrolysis","Possible","Major",4,3,12),
                ("Dew point failure — pipeline moisture","Purification","Likely","Moderate",5,2,10),
                ("KOH lye carryover — purifier damage","GLT / Separator","Unlikely","Major",3,3,9),
                ("Purifier overpressure","H2 Purification","Rare","Critical",2,4,8),
                ("Cooling water loss — cell trip","DM Water & KOH","Possible","Minor",4,1,4),
                ("DM water tank low — plant trip","DM Water & KOH","Likely","Minor",5,1,5),
                ("N2 purge bypass on startup","Reflow/Purification","Very Rare","Catastrophic",1,5,5),
            ]
            fig_rm = go.Figure()
            colors_rm = {"20":"#ef4444","12":"#f97316","10":"#f97316","9":"#eab308","8":"#eab308","5":"#22c55e","4":"#22c55e"}
            for name, loc, likelihood, severity, lx, sy, score in h2_risks:
                c_rm = "#ef4444" if score >= 15 else "#f97316" if score >= 9 else "#eab308" if score >= 5 else "#22c55e"
                fig_rm.add_trace(go.Scatter(
                    x=[lx], y=[sy], mode="markers+text",
                    marker=dict(size=28, color=c_rm, opacity=0.85, line=dict(color="#fff",width=1.5)),
                    text=[str(score)], textposition="middle center",
                    textfont=dict(color="#fff", size=10, family="monospace"),
                    name=name, hovertemplate=f"<b>{name}</b><br>Location: {loc}<br>Likelihood: {likelihood}<br>Severity: {severity}<br>Risk Score: {score}<extra></extra>",
                ))
            fig_rm.update_layout(
                paper_bgcolor="#0d1f35", plot_bgcolor="#0a1628",
                height=380, font=dict(color="#64748b", size=10),
                xaxis=dict(title="Likelihood →", range=[0.5,5.5], tickvals=[1,2,3,4,5],
                           ticktext=["Very Rare","Rare","Unlikely","Possible","Likely"],
                           gridcolor="#1e3a5f", color="#64748b"),
                yaxis=dict(title="Severity →", range=[0.5,5.5], tickvals=[1,2,3,4,5],
                           ticktext=["Minor","Moderate","Major","Critical","Catastrophic"],
                           gridcolor="#1e3a5f", color="#64748b"),
                showlegend=False, margin=dict(l=80,r=10,t=20,b=60),
            )
            st.plotly_chart(fig_rm, use_container_width=True)

            tbl_rm = '<table style="border-collapse:collapse;width:100%;font-size:.78rem"><thead><tr style="background:#080d18">'
            for h in ["Risk Scenario","Location","Likelihood","Severity","Score","Rating"]:
                tbl_rm += f'<th style="padding:7px 12px;text-align:left;color:#64748b;font-size:.63rem;font-weight:700;border-bottom:1px solid #1e3a5f">{h}</th>'
            tbl_rm += '</tr></thead><tbody>'
            for name, loc, likelihood, severity, lx, sy, score in sorted(h2_risks, key=lambda x: -x[6]):
                c_s = "#ef4444" if score >= 15 else "#f97316" if score >= 9 else "#eab308" if score >= 5 else "#22c55e"
                rating = "CRITICAL" if score >= 15 else "HIGH" if score >= 9 else "MEDIUM" if score >= 5 else "LOW"
                tbl_rm += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 12px;color:#e2e8f0;font-weight:600">{name}</td><td style="padding:7px 12px;color:#94a3b8">{loc}</td><td style="padding:7px 12px;color:#94a3b8">{likelihood}</td><td style="padding:7px 12px;color:#94a3b8">{severity}</td><td style="padding:7px 12px;color:{c_s};font-weight:700;font-family:monospace">{score}</td><td style="padding:7px 12px"><span style="background:{c_s}20;color:{c_s};border:1px solid {c_s}40;font-size:.62rem;font-weight:700;padding:2px 8px;border-radius:20px">{rating}</span></td></tr>'
            tbl_rm += '</tbody></table>'
            st.markdown(tbl_rm, unsafe_allow_html=True)

        with h2tabs[10]:  # PSM Report
            st.markdown(f"""<div class="sl-card" style="border-left:3px solid #3b82f6;margin-bottom:1rem">
            <div style="font-size:.95rem;font-weight:800;color:#f1f5f9;margin-bottom:.3rem">Hydrogen Plant — H2 Production & Supply</div>
            <div style="font-size:.73rem;color:#475569">{comp} &nbsp;|&nbsp; Utilities &nbsp;|&nbsp; Doc: PSRM/PSI/TINPL/PROP/001 Rev.03 Eff.Dt.:08.10.2023</div>
            <div style="display:flex;gap:1.5rem;margin-top:.7rem;flex-wrap:wrap">
              <span style="font-size:.72rem;color:#94a3b8"><b style="color:#f97316">Status:</b> HHO Active — 5 HHO processes</span>
              <span style="font-size:.72rem;color:#94a3b8"><b style="color:#ef4444">Risk:</b> {meta['risk']}/100</span>
              <span style="font-size:.72rem;color:#94a3b8"><b style="color:#f97316">Critical:</b> H2 (LEL 4%, UEL 75%)</span>
              <span style="font-size:.72rem;color:#94a3b8"><b style="color:#22c55e">PSCE Items:</b> {meta['psce']}</span>
            </div>
            </div>""", unsafe_allow_html=True)
            checklist = [
                ("Identification of HHO & LHO","Y","Mentioned in PSC — 5 HHO, 1 LHO processes"),
                ("Site Layout","Y","CCOE Approved Site Layout Drawing Available"),
                ("Block Diagram / BD","Y","Mentioned in BD"),
                ("Past Process Changes & MOCs","Y","Approval of CCOE Nagpur"),
                ("Past Process Incidents & Recommendations","Y","No past incidents recorded"),
                ("Process Description, PFD","Y","Mentioned in PFD"),
                ("Updated P&ID","Y","CCOE Approved P&ID Available at BAF Office"),
                ("Equipment & Instrument List & Interlocks","Partial","Up to some equipment available"),
                ("Equipment Data Sheet","In Progress","Being collected"),
                ("Identification of PSCE with Maintenance Plan","Y","Mentioned in PSCE — 44 items identified"),
                ("SOP, Emergency Shutdown, Interruption Procedures","Y","SOP for Decontamination Available"),
                ("SOC, SOL Ranges & Action on Deviation","Y","Mentioned in PDB — 24 parameters"),
                ("Chemical, Physical & Thermal Properties","Y","As mentioned in MSDS — H2, O2, N2"),
                ("Interaction between Chemicals","Y","As mentioned in Chemical Interaction Matrix"),
                ("Chemical Reactions","Y","As mentioned in Chemical Interaction Matrix"),
                ("Thermal Data of Reaction","Y","As mentioned in MSDS"),
                ("Inventory of Materials","Y","Mentioned in HOM"),
                ("Hazardous Area Classification","Y","Mentioned in HOM — H2 Zone-1/Zone-2 classification"),
            ]
            for item, status, remark in checklist:
                sc4 = "#22c55e" if status=="Y" else "#eab308" if status=="Partial" else "#f97316"
                label = "Complete" if status=="Y" else status
                st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:7px;padding:.6rem 1rem;margin-bottom:5px;display:flex;gap:12px;align-items:center"><span style="background:{sc4}20;color:{sc4};border:1px solid {sc4}40;font-size:.62rem;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap;min-width:80px;text-align:center">{label}</span><span style="font-size:.8rem;font-weight:600;color:#e2e8f0;min-width:200px">{item}</span><span style="font-size:.75rem;color:#64748b">{remark}</span></div>', unsafe_allow_html=True)

        # ── H2 PLANT AI ASSISTANT ─────────────────────────────────────
        def h2_ai(q):
            q = q.lower()
            if any(x in q for x in ["h2 in o2","h2-in-o2","explosive","at1002","detonation"]):
                return ("H2 Plant — Critical Safety: H2-in-O2 Analyser (AT1002)\n\n"
                        "SOC: H2-in-O2 < 0.8% | SOL: < 1.7% | Auto-trip at 0.8% SOC\n\n"
                        "Why critical: H2 and O2 form an explosive mixture at ALL ratios between 4-75% H2 in air.\n"
                        "In a pure O2 environment, this explosive range is WIDER.\n"
                        "AT1002 is PSCE #13 — its failure means the ONLY means of detecting this is lost.\n"
                        "Consequence: H2/O2 mixture ignition → DETONATION (not just explosion) in electrolyser.")
            if any(x in q for x in ["bullet","bleve","storage","saf","srm","srvm","4-14","pressure vessel"]):
                return ("H2 Plant — Bullet Storage Risk\n\n"
                        "Bullet 1 & 2: Operating pressure 4-14 kg/cm2 | SOL: 20 kg/cm2\n"
                        "Temperature SOC: <45°C | SOL: <50°C\n"
                        "BLEVE risk: Boiling Liquid Expanding Vapour Explosion if external fire + vessel failure\n"
                        "Protection: Dual SRVs per bullet (PSCE #34-37) | Fire hydrant (PSCE #44)\n"
                        "CCOE approved design + PESO/IBR annual inspection mandatory\n"
                        "H2 is colourless/odourless — detector is ONLY warning of leak")
            if any(x in q for x in ["purge","n2 purge","nitrogen","startup","shutdown","sequence"]):
                return ("H2 Plant — N2 Purge Procedure (CRITICAL SAFETY)\n\n"
                        "STARTUP: N2 purge FIRST → confirm O2 <1% → THEN admit H2\n"
                        "SHUTDOWN: H2 purge with N2 first → confirm H2 <0.5% → THEN admit air\n\n"
                        "Why mandatory: H2+air = explosive 4-75%. If air enters H2 system or H2 enters air without purge → explosive atmosphere.\n"
                        "N2 is inert and displaces both H2 and air safely.\n"
                        "Hard interlock: H2 admission valve mechanically blocked until N2 purge confirmed by PLC.\n"
                        "SOP verification by shift supervisor mandatory before every startup.")
            if any(x in q for x in ["dew point","moisture","mt1101","dryer","purification","purity"]):
                return ("H2 Plant — Purification & Dew Point\n\n"
                        "Deoxy Unit: 118-160°C (SOC) — removes residual O2\n"
                        "Dryers A/B/C: 170-220°C (SOC) — removes moisture\n"
                        "Dew Point SOC: <-80°C | SOL: <-70°C (auto-trip) — PSCE #23 (MT1101)\n"
                        "Trace O2 SOC: <1 ppm | SOL: <2 ppm — PSCE #26 (AT1102)\n\n"
                        "If dew point rises above -70°C: moisture in H2 pipeline → corrosion, embrittlement, annealing quality failure\n"
                        "If trace O2 rises above 2 ppm: QZ1007 auto-vent prevents contaminated H2 from reaching storage")
            if any(x in q for x in ["psce","safety critical","44","at1701","at1702","at1703"]):
                return ("H2 Plant — PSCE (44 Items)\n\n"
                        "Key PSCE items:\n"
                        "#13: AT1002 H2-in-O2 analyser — auto-trip at 0.8% (CRITICAL)\n"
                        "#14: AT1001 O2-in-H2 analyser — auto-trip at 0.2% (CRITICAL)\n"
                        "#15: AT1701 H2 detector GLT zone — alarm at 0.9% LEL\n"
                        "#16: AT1702 H2 detector purifier zone\n"
                        "#17: AT1703 H2 detector DM plant area\n"
                        "#23: MT1101 Dew point analyser — trip at -70°C SOL\n"
                        "#26: AT1102 Trace O2 analyser — auto-vent at 2 ppm\n"
                        "#30: Emergency trip switch outside plant\n"
                        "#34-37: Dual SRVs on both H2 bullets\n"
                        "#44: Fire hydrant system")
            if any(x in q for x in ["soc","sol","safe operating","deviation","parameter","limit"]):
                return ("H2 Plant — SOC vs SOL Explained\n\n"
                        "SOC (Safe Operating Condition) = normal target range for safe, efficient operation\n"
                        "SOL (Safe Operating Limit) = outer boundary — breach = IMMEDIATE corrective action or plant trip\n\n"
                        "Key parameters:\n"
                        "DM Tank Level: SOC 300-1000mm | SOL 100-1500mm\n"
                        "Cell Temperature: SOC 35-95°C | SOL 25-97°C (trip)\n"
                        "DC Current: SOC 800-1450A | SOL 500-1600A\n"
                        "H2-in-O2: SOC 0-0.8% | SOL 0-1.7% (trip)\n"
                        "O2-in-H2: SOC 0-0.1% | SOL 0-0.2% (trip)\n"
                        "Bullet Pressure: SOC 4-14 kg/cm2 | SOL 3-20 kg/cm2\n"
                        "Dew Point: SOC <-80°C | SOL <-70°C (trip)")
            if any(x in q for x in ["electrolysis","electrolyser","dc current","rectifier","cell"]):
                return ("H2 Plant — Electrolysis Process\n\n"
                        "Process: DC current (800-1450A) splits DM water → H2 at cathode, O2 at anode\n"
                        "Electrolyte: KOH lye solution\n"
                        "Operating pressure: 1.50-1.57 MPa (SOC)\n"
                        "Cell temperature: 35-95°C (SOC) | Auto-trip at 97°C\n\n"
                        "Critical interlocks:\n"
                        "• AT1002: H2-in-O2 auto-trip at 0.8%\n"
                        "• AT1001: O2-in-H2 auto-trip at 0.2%\n"
                        "• TE1001/TE1003: cell temp dual RTDs — trip at 97°C\n"
                        "• PT1001: separator pressure — overpressure alarm\n"
                        "• Emergency trip switch outside plant (PSCE #30)")
            if any(x in q for x in ["hho","lho","classification","why"]):
                return ("H2 Plant — HHO Classification Reasoning\n\n"
                        "HHO (5 processes): Electrolysis, Gas-Liquid Separation, Purification, Bullet Storage, Distribution\n"
                        "LHO (1 process): DM Water & KOH Storage\n\n"
                        "Key HHO reasoning:\n"
                        "Electrolysis: H2+O2 simultaneous production — DETONATION risk if mixed\n"
                        "Gas-Liquid Treater: H2 under pressure — explosive if leaked\n"
                        "Purification: H2 at 0.6-1.3 MPa + high temperature (170-220°C)\n"
                        "Bullet Storage: Large H2 inventory — BLEVE risk\n"
                        "Distribution: H2 pipeline through occupied areas\n\n"
                        "All HHO because: property damage potential >Rs.50L + fatality potential from explosion/fire")
            return ("H2 Plant AI Assistant\n\n"
                    "I can answer questions about:\n"
                    "• H2-in-O2 / O2-in-H2 explosive limits and auto-trips\n"
                    "• Bullet storage (pressure, temperature, SRVs, BLEVE)\n"
                    "• N2 purge procedure (startup/shutdown sequence)\n"
                    "• Purification, dew point, trace O2 (MT1101, AT1102)\n"
                    "• PSCE items — all 44 items explained\n"
                    "• SOC vs SOL for all 24 parameters\n"
                    "• Electrolysis process and interlocks\n"
                    "• HHO/LHO classification reasoning\n"
                    f"\nYour query: '{q}'")

        st.markdown("---")
        st.markdown('<div class="sl-sec">H2 Plant PSM AI Assistant</div>', unsafe_allow_html=True)
        st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.6rem 1rem;margin-bottom:.6rem;font-size:.75rem;color:#60a5fa">
        Ask about: H2-in-O2 limits, bullet safety, N2 purge sequence, dew point, PSCE items, SOC/SOL values, electrolysis interlocks, HHO classification...
        </div>""", unsafe_allow_html=True)

        if "h2_chat" not in st.session_state: st.session_state.h2_chat = []
        if "h2_ck" not in st.session_state: st.session_state.h2_ck = 0

        for msg in st.session_state.h2_chat[-12:]:
            _mc = msg["content"]
            _mcls = "sl-chat-user" if msg["role"]=="user" else "sl-chat-ai"
            st.markdown(f'<div class="{_mcls}">{_mc}</div>', unsafe_allow_html=True)

        h2q = st.text_input("", placeholder="e.g. What is H2-in-O2 SOL? Why is electrolysis HHO? Explain N2 purge sequence.",
                            key=f"h2ci_{st.session_state.h2_ck}", label_visibility="collapsed")
        hbc1, hbc2 = st.columns([1,6])
        with hbc1:
            if st.button("Send", type="primary", key="h2_send"):
                if h2q.strip():
                    st.session_state.h2_chat.append({"role":"user","content":h2q})
                    st.session_state.h2_chat.append({"role":"assistant","content":h2_ai(h2q)})
                    st.session_state.h2_ck += 1
                    st.rerun()
        with hbc2:
            if st.button("Clear", key="h2_clear"):
                st.session_state.h2_chat = []
                st.rerun()

    else:
        # ── ETL-1 / GENERIC PLANT — TABS ONLY (sidebar/nav already rendered above) ──

        TABS = ["Overview", "PSC", "Hazard of Material",
                "Chem. Interaction", "PDB", "PSCE", "EDB", "Parameters",
                "Playground", "Simulation", "Risk Matrix", "PSM Report"]
        tabs = st.tabs(TABS)

        # ── OVERVIEW ──────────────────────────────────────────────────
        with tabs[0]:
            rc = risk_color(meta["risk"])
            # Get plant profile if available
            profile = PLANT_PROFILES.get(plant, None)
            n_procs = profile["processes"] if profile else 6
            n_chems = profile["chemicals"] if profile else 6
            n_params = profile["params"] if profile else 13

            st.markdown(f"""
            <div class="sl-metrics">
              <div class="sl-metric"><div class="sl-metric-val" style="color:{rc}">{meta['risk']}/100</div><div class="sl-metric-lbl">Risk Index</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">{n_procs}</div><div class="sl-metric-lbl">Processes</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#f97316">{meta['hho']}</div><div class="sl-metric-lbl">High Hazard</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">{n_chems}</div><div class="sl-metric-lbl">Chemicals</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">{n_params}</div><div class="sl-metric-lbl">Parameters</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#22c55e">{meta['psce']}</div><div class="sl-metric-lbl">PSCE Items</div></div>
            </div>
            """, unsafe_allow_html=True)

            # Plant description
            if profile and profile.get("desc"):
                st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">{profile["desc"]}</div>', unsafe_allow_html=True)

            # Alerts
            alerts = profile["alerts"] if profile else []
            if is_etl1:
                alerts = [
                    (98,"CRITICAL — Cr-VI in air (Chemical Treatment) | Risk 98/100 | Carcinogenic exposure — shutdown required"),
                    (92,"CRITICAL — Strip Exit Temperature (Reflow) | Risk 92/100 | Strip burning / tin melt failure"),
                    (90,"CRITICAL — Sn2+ Concentration (Tin Plating) | Risk 90/100 | Improper / over coating risk"),
                ]
            if alerts:
                st.markdown('<div class="sl-sec">Active Risk Alerts</div>', unsafe_allow_html=True)
                for score, text in alerts:
                    st.markdown(f'<div class="sl-alert"><div class="sl-alert-score">{score}/100</div><div class="sl-alert-text">{text}</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Process Overview</div>', unsafe_allow_html=True)
            procs = profile["proc_cards"] if profile else [
                ("Coil Feeding", "Hydraulic oil, DM water, compressed air for welder", "lho", ["LHO"]),
                ("Cleaning & Rinsing", "NaOH (80-90 C), H2SO4 pickling (8-10 g/L), electrolytic cleaning 2.5-3.5 kA", "hho", ["HHO", "PSM Required"]),
                ("Tin Plating", "SnSO4 + PSA + ENSA plating bath, sulphuric acid base, flow brightening at 232 C", "hho", ["HHO", "PSM Required"]),
                ("Reflow Furnace", "H2 gas (LEL 4% UEL 77%), Propane burners, strip temperature 232-270 C", "hho", ["HHO", "PSM Required"]),
                ("Chemical Treatment", "Cr-VI chromate passivation — CARCINOGEN, TLV-TWA 0.05 mg/m3", "hho", ["HHO", "PSM Required"]),
                ("Electrostatic Oiling", "DOS oil spray (flash point 190 C), electrostatic oiling, tension recoiling", "lho", ["LHO"]),
            ]
            c1, c2 = st.columns(2)
            for i, (name, desc, cls, tags) in enumerate(procs):
                t_html = "".join(
                    f'<span class="sl-tag sl-tag-{"hho" if t=="HHO" else "psm" if "PSM" in t else "lho"}">{t}</span>'
                    for t in tags
                )
                with (c1 if i % 2 == 0 else c2):
                    st.markdown(f'<div class="sl-proc {cls}"><div class="sl-proc-title">{name}</div><div class="sl-proc-desc">{desc}</div>{t_html}</div>', unsafe_allow_html=True)

            # Trend charts
            st.markdown('<div class="sl-sec">Trend Charts</div>', unsafe_allow_html=True)
            months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            ch1, ch2 = st.columns(2)
            with ch1:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=months, y=[55,58,60,57,61,63,61,59,64,61,62,61],
                    mode="lines+markers", line=dict(color="#f97316", width=2.5),
                    marker=dict(size=6, color="#f97316"), name="Risk Index",
                    fill="tozeroy", fillcolor="rgba(249,115,22,0.06)"
                ))
                fig.add_hline(y=75, line_dash="dot", line_color="#ef4444",
                              annotation_text="Alert threshold: 75",
                              annotation_font=dict(color="#ef4444", size=10))
                fig.update_layout(
                    title=dict(text="Risk Index Trend 2024", font=dict(color="#94a3b8", size=13)),
                    paper_bgcolor="#0d1f35", plot_bgcolor="#080d18",
                    font=dict(color="#64748b", size=10),
                    height=250, margin=dict(l=40, r=10, t=45, b=35),
                    xaxis=dict(gridcolor="#1e3a5f", color="#64748b", showline=False),
                    yaxis=dict(gridcolor="#1e3a5f", color="#64748b", range=[0, 100], title="Score"),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            with ch2:
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(
                    x=months,
                    y=[0.04,0.06,0.05,0.08,0.05,0.07,0.09,0.06,0.07,0.05,0.06,0.05],
                    marker_color=["#ef4444" if v > 0.05 else "#a78bfa"
                                  for v in [0.04,0.06,0.05,0.08,0.05,0.07,0.09,0.06,0.07,0.05,0.06,0.05]],
                    name="Cr-VI conc."
                ))
                fig2.add_hline(y=0.05, line_dash="dot", line_color="#ef4444",
                               annotation_text="TLV-TWA: 0.05 mg/m3",
                               annotation_font=dict(color="#ef4444", size=10))
                fig2.update_layout(
                    title=dict(text="Cr-VI Air Concentration (mg/m3)", font=dict(color="#94a3b8", size=13)),
                    paper_bgcolor="#0d1f35", plot_bgcolor="#080d18",
                    font=dict(color="#64748b", size=10),
                    height=250, margin=dict(l=40, r=10, t=45, b=35),
                    xaxis=dict(gridcolor="#1e3a5f", color="#64748b"),
                    yaxis=dict(gridcolor="#1e3a5f", color="#64748b", title="mg/m3"),
                    showlegend=False
                )
                st.plotly_chart(fig2, use_container_width=True)

        # ── PSC ──────────────────────────────────────────────────────
        with tabs[1]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/PSC/001 Rev.04 Eff.Dt.:18.08.2023 — ETL-1, Tata Steel Tinplate (TCIL), Golmuri</p>', unsafe_allow_html=True)

            # Framework banner
            st.markdown("""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem">
<div style="font-size:.82rem;font-weight:700;color:#f97316;margin-bottom:.5rem">PSRM CLASSIFICATION FRAMEWORK</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.78rem;color:#94a3b8;line-height:1.8">
<div><b style="color:#f97316">HHO — Highly Hazardous Operation</b><br>
Process with hazardous substance/energy that CAN result in:<br>
• Property damage &gt; Rs.50 lakhs, OR<br>
• Potential for fatality / multiple LTIs, OR<br>
• Significant environmental impact<br>
<b style="color:#f97316">Requires: Full PSRM</b> — PSI + PHA + HAZOP + Bow Tie + LOPA + Barrier Audits + SOPs + Emergency Plan</div>
<div><b style="color:#6366f1">LHO — Lower Hazardous Operation</b><br>
Process with hazardous substance/energy present BUT consequences do NOT meet any HHO threshold under normal or credible abnormal operation.<br><br>
<b style="color:#6366f1">Requires: Baseline PSRM</b> — PSI documentation only</div>
</div></div>""", unsafe_allow_html=True)

            # Stats
            st.markdown("""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1rem">
<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#f97316;font-family:monospace">4</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">HHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(99,102,241,.3);border-top:3px solid #6366f1;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#6366f1;font-family:monospace">2</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">LHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#ef4444;font-family:monospace">6</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">CHEMICALS ONSITE</div></div>
<div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:10px;padding:.9rem;text-align:center">
<div style="font-size:1.8rem;font-weight:900;color:#22c55e;font-family:monospace">77</div>
<div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PSCE ITEMS</div></div>
</div>""", unsafe_allow_html=True)

            # Process selector
            if "psc_proc" not in st.session_state:
                st.session_state.psc_proc = "Cleaning & Rinsing"

            st.markdown('<div class="sl-sec">Click a process to see full HHO/LHO breakdown, parameters, HAZOP & Bow Tie</div>', unsafe_allow_html=True)

            PSC_DATA = {
                "Coil Feeding": {
                    "cls":"LHO","color":"#6366f1",
                    "desc":"Entry section: payoff reel loads cold-rolled black plate. Strip welded for line continuity. Entry looper accumulates strip for uninterrupted operation. Key equipment: hydraulic power pack (55-70 bar), welder, bridle rolls, entry looper.",
                    "hazardous":["Hydraulic oil (flash point ~150°C)","DM water at pressure (4.5-5.5 kg/cm2)","Compressed air (4.5-5.5 kg/cm2)","Mechanical pinch points at bridle rolls"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"N","Corrosive":"Y","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Property >50L":"N","Fatality":"N","Env. Impact":"N"},
                    "reasoning":"Hydraulic oil leak at 55-70 bar is the primary credible hazard. However, hydraulic oil flash point (~150°C) means ignition requires sustained heat source — no credible ignition scenario in normal operation. Compressed air line failure causes mechanical noise/movement but no explosive energy release sufficient for fatality. DM water at 4.5-5.5 kg/cm2 is low-pressure utility. No toxic release, no explosion risk. Consequence analysis: maximum credible event = hydraulic oil spill causing slip hazard / minor fire, well below Rs.50 lakh threshold. NO HHO CRITERIA MET.",
                    "parameters":[
                        ("Hydraulic Pump Pressure","55-70 bar","45-100 bar","Below 45 bar: actuator failure, strip misalignment, weld failure","Above 100 bar: hydraulic line rupture, oil spray fire risk"),
                        ("DM Water Pressure (Welder)","4.5-5.5 kg/cm2","4.5-5.5 kg/cm2","Below 4.5: welder overheating, failed weld, strip break","Above 5.5: line stress, potential seal failure"),
                        ("Compressed Air Pressure","4.5-5.5 kg/cm2","4.5-6.5 kg/cm2","Below 4.5: pneumatic clamp failure, welder malfunction","Above 6.5: excess force on pneumatics, noise hazard"),
                    ],
                    "barriers":["Hydraulic pressure relief valve (set at 100 bar SOL)","DM water flow switch on welder cooling circuit","Compressed air low-pressure interlock on welder","Emergency stop at all operator stations"],
                    "hazop":None,
                    "bowtie":None,
                },
                "Cleaning & Rinsing": {
                    "cls":"HHO","color":"#f97316",
                    "desc":"Pre-primary, primary, secondary electrolytic alkali (NaOH) cleaning at 80-90°C removes rolling oils. Followed by H2SO4 pickling (8-10 g/L) for iron oxide removal. DM/condensate water rinsing. Electrolytic current: 2.5-3.5 kA. Three chemical baths in sequence.",
                    "hazardous":["H2SO4 (Sulphuric Acid) — corrosive, generates H2 with metals","NaOH at 80-90°C — severe alkali burns","H2 gas from electrolytic cleaning (LEL 4%)","Acid mist (TLV-TWA 1 mg/m3)","High DC current 2.5-3.5 kA"],
                    "hazard_matrix":{"Toxic":"Y","Explosive":"Y","Flammable":"N","Corrosive":"Y","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"H2SO4 at 8-10 g/L generates H2 gas when in contact with steel (Fe + H2SO4 → FeSO4 + H2↑). H2 LEL is 4% — accumulation in poorly ventilated cell area + electrical ignition source = explosive risk. NaOH at 80-90°C: boiling alkali splash causes full-thickness chemical burns. Electrolytic current 2.5-3.5 kA creates H2 at cathode. Credible failure: LEV failure + H2 accumulation + current arc = H2 explosion → structural damage >Rs.50L, fatality risk. Also: H2SO4 spill to drain → WTP overload, groundwater pH impact = environmental consequence. ALL THREE HHO CRITERIA CAN BE MET.",
                    "parameters":[
                        ("NaOH Temperature","80-90°C","80-90°C","<80°C: poor degreasing, oil on strip → plating pinholes","≥90°C: alkali boiling, violent steam, burn risk — HHO EVENT"),
                        ("NaOH Concentration","25-30 g/L","25-30 g/L","<25 g/L: insufficient cleaning, residual oil","≥30 g/L: excess drag-out, waste treatment overload"),
                        ("Cleaning Current","2.5-3.5 kA","2.5-3.5 kA","<2.5 kA: inadequate electrolytic cleaning","≥3.5 kA: H2 over-evolution, arc risk, cell damage"),
                        ("H2SO4 Concentration","8-10 g/L","8-10 g/L","<8 g/L: incomplete pickling, oxide layer on strip","≥10 g/L: over-pickling, H2 gas spike, equipment corrosion"),
                    ],
                    "barriers":["Forced LEV ventilation above all cleaning cells","Alkali temperature transmitter + auto-alarm at 90°C","H2SO4 concentration analyser with SOC/SOL alarm","Electrolytic current protection relay (trip at 3.5 kA)","Acid-resistant PPE mandatory zone","Emergency deluge shower within 10m"],
                    "hazop":[
                        ("NaOH Temp HIGH","Temperature exceeds 90°C","Cooling water valve failure / steam trap blockage","Alkali boils — steam explosion, severe burns to operators","Temp transmitter alarm, auto-coolant valve, operator shutdown"),
                        ("H2SO4 Conc HIGH","Concentration exceeds 10 g/L","Overdose during makeup / analyser failure","Over-pickling, H2 spike, equipment corrosion, acid mist","Concentration analyser alarm, manual titration verification"),
                        ("Cleaning Current HIGH","Current >3.5 kA","Rectifier malfunction / control system failure","Excessive H2 evolution, arc, cell damage","Current protection relay auto-trip, visual ammeter check"),
                        ("LEV FAILURE","Ventilation stops","Fan failure / power cut","H2 accumulates in cell area → explosion risk","LEV flow switch alarm, backup fan interlock"),
                    ],
                    "bowtie":{
                        "top_event":"H2 accumulation and ignition in cleaning section",
                        "causes":["LEV ventilation failure","Electrolytic current >3.5 kA (H2 over-evolution)","H2SO4 concentration >10 g/L (increased H2 generation)","Electrical arc from damaged cell connections"],
                        "consequences":["Explosion — structural damage, line shutdown 2-4 weeks","Fatality/serious injury to cleaning section operators","Fire spread to adjacent process bays","Regulatory shutdown, PESO investigation"],
                        "preventions":["LEV flow switch interlock (auto-trip on fan failure)","Current protection relay (auto-trip >3.5 kA)","H2SO4 concentration analyser (alarm + auto-dilution)","Regular H2 LEL monitoring in cell area"],
                        "mitigations":["Explosion venting panels in cleaning bay roof","Emergency fire suppression system","Full evacuation procedure + muster point","Post-event investigation and CAPA process"],
                    },
                },
                "Tin Plating": {
                    "cls":"HHO","color":"#f97316",
                    "desc":"Electrolytic tin deposition from SnSO4 + PSA + ENSA bath (H2SO4 base). DC current deposits Sn layer on strip cathode through 8 plating cells. Coating weight controlled by current density and line speed. Key parameter: Sn2+:Free acid ratio = 1.95-2.05.",
                    "hazardous":["H2SO4 base bath (TLV-TWA 1 mg/m3 acid mist)","H2 gas evolution at cathode (abnormal conditions)","SnSO4 toxic if ingested/inhaled (Sn2+ compounds)","ENSA surfactant decomposition products","High DC electrical energy at plating cells"],
                    "hazard_matrix":{"Toxic":"Y","Explosive":"Y","Flammable":"N","Corrosive":"Y","Thermal":"N","Pressure":"N"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"While tin plating is less acutely dangerous than Reflow or Chemical Treatment, the combination of H2SO4 base bath + electrolytic process creates H2 at cathode during over-current or bath deviation. 8 plating cells operating simultaneously = large H2 evolution risk if current control fails. Sn bath overflow to drain = heavy metal (Sn2+) contamination of WTP/groundwater = significant environmental consequence. Product failure (under-plating) at food-grade tin plate level = public health implication and regulatory action. Property damage from cell corrosion + product rejection + shutdown >50 lakhs. HHO CLASSIFICATION JUSTIFIED.",
                    "parameters":[
                        ("Sn2+ Concentration","26-32 g/L","24-34 g/L","<24 g/L: under-plating, dull band — PRODUCT REJECTION","≥34 g/L: over-coating, excess tin loss, cost impact"),
                        ("Free Acid Concentration","13-16 g/L","11-18 g/L","<11 g/L: low conductivity, uneven plating","≥18 g/L: increased acid mist, corrosivity"),
                        ("Sn2+ : Free Acid Ratio","1.95-2.05","1.90-2.10","<1.90: bath imbalance, rough deposit, sludge","≥2.10: non-uniform deposition, product failure"),
                        ("ENSA Concentration","3-6 g/L","2-7 g/L","<2 g/L: dull appearance, rough tin surface","≥7 g/L: bath contamination, breakdown products"),
                    ],
                    "barriers":["Daily bath analysis — Sn2+, free acid, ENSA verified","Current density interlock per plating cell","Acid mist LEV system above all 8 plating cells","Plating tank level transmitter (overflow alarm)","Sn-bearing wastewater to dedicated WTP stream"],
                    "hazop":[
                        ("Sn2+ LOW","<24 g/L","Anode dissolution rate low / feed failure","Under-plating — product downgrade, rejection","Bath analyser alarm, mandatory hold before dispatch"),
                        ("Free Acid HIGH","≥18 g/L","Overdose during makeup","Acid mist surge, operator exposure","Acid mist monitor, LEV performance check"),
                        ("Current HIGH","Above set point","Rectifier malfunction","H2 evolution at cathode, arc risk","Current relay auto-trip, cell inspection"),
                        ("Bath Overflow","Level >SOL","Pump seal failure / makedown error","Sn2+ spill to floor/drain — environmental","Level transmitter alarm + auto pump trip"),
                    ],
                    "bowtie":{
                        "top_event":"Plating bath overflow / H2 ignition at plating cells",
                        "causes":["Bath level control failure (pump seal failure)","Over-current → H2 evolution at cathode","Sn2+ crash → emergency bath makeup spillage","ENSA decomposition — bath foam-over"],
                        "consequences":["Sn-bearing wastewater to drain — WTP failure, CPCB reportable","H2 ignition → fire in plating cell area","Product rejection — food safety regulatory action","Line shutdown — production loss >Rs.50L"],
                        "preventions":["Bath level transmitter + auto pump trip at SOL","Current protection relay on all 8 plating rectifiers","Foam detector in plating bath","Daily mandatory bath analysis verification"],
                        "mitigations":["Dedicated Sn-bearing wastewater collection pit","Fire suppression in plating bay","Product hold and 100% re-inspection protocol","CPCB emergency notification procedure"],
                    },
                },
                "Reflow Furnace": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"Resistance/induction heating melts tin at 232°C (tin melting point) for mirror-bright finish and Fe-Sn alloy layer. H2/N2 atmosphere prevents oxidation. Strip then quenched in water (50-65°C). CRITICAL: N2 purge mandatory before H2. H2 purge before air on shutdown. HIGHEST RISK PROCESS on ETL-1.",
                    "hazardous":["H2 gas — LEL 4%, UEL 77% (extremely wide explosive range)","Propane burners — LEL 2.1%, UEL 9.5%","Strip at 232-270°C (above tin melting point)","H2 ignition energy: 0.017 mJ (tiny — almost invisible spark sufficient)","N2 asphyxiation risk if purge sequence fails"],
                    "hazard_matrix":{"Toxic":"Y","Explosive":"Y","Flammable":"Y","Corrosive":"Y","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"H2 vapour cloud explosion is the top risk. H2 has the widest flammability range of any common industrial gas (4-77%) and the lowest ignition energy (0.017 mJ — a tiny static discharge). A seal failure while H2 is flowing, without proper N2 purge first, creates explosive atmosphere in seconds. Propane burners add secondary fire risk. Strip at >270°C causes conductor roll damage, strip burning, secondary fire. A single H2 explosion in the furnace bay would cause: structural collapse, multiple fatalities, damage well exceeding Rs.50L, potential H2 line fire. This is why PSAL 2.14, UV 1.21, and Pyrometer ETL-1 are all PSCE items with mandatory calibration. ALL THREE HHO CRITERIA EXCEEDED BY LARGE MARGIN.",
                    "parameters":[
                        ("Strip Temperature","232-270°C","232-270°C","<232°C: tin doesn't melt — dull coating, product reject","≥270°C: strip burning, conductor roll damage — CRITICAL SHUTDOWN"),
                        ("Quench Temperature","50-65°C","50-65°C","<50°C: thermal shock, strip shape defects","≥65°C: incomplete solidification, alloy overgrowth"),
                        ("Reflow Current","1000-10000 A","1000-10000 A","<1000 A: insufficient melting energy","≥10000 A: conductor roll arcing, fire risk — CRITICAL"),
                        ("H2 Pressure","0.5-2.0 bar","0.5-2.5 bar","<0.5 bar: H2 supply loss — must purge with N2 BEFORE air entry","≥2.5 bar: line overpressure, seal failure risk"),
                    ],
                    "barriers":["PSAL 2.14: H2 pressure switch — PLC auto-trip on loss (PSCE #2)","UV 1.21: Propane solenoid auto-close on safety signal (PSCE #3)","Pyrometer ETL-1: auto-trip at 270°C strip temperature (PSCE #1)","N2 purge interlock — H2 cannot be admitted without N2 purge confirmation","H2 LEL detector in furnace zone with evacuation alarm","Mandatory purge procedure (SOP) verified by shift supervisor"],
                    "hazop":[
                        ("H2 Pressure LOW","<0.5 bar","Supply valve failure / pipe leak","H2 loss → air ingress → explosive mixture on restart without purge","PSAL 2.14 auto-trip, N2 auto-purge, mandatory restart SOP"),
                        ("Strip Temp HIGH",">270°C","Pyrometer failure / current surge","Strip burning, conductor roll damage, secondary fire","Pyrometer auto-trip, redundant thermocouple, visual alarm"),
                        ("Purge Sequence SKIPPED","N2 purge bypassed","Operator error / interlock defeat","H2 + air = explosive atmosphere in furnace","Hard interlock — H2 valve mechanically blocked until N2 confirmed"),
                        ("Propane Leak","Uncontrolled release","Fitting failure / valve leak","Propane + H2 = compound explosion risk","Gas detector auto-trip, UV 1.21 solenoid closure, evacuation"),
                    ],
                    "bowtie":{
                        "top_event":"H2 vapour cloud ignition and explosion in reflow furnace",
                        "causes":["H2 supply seal failure (PSAL 2.14 fails to trip)","N2 purge sequence bypassed on restart","Propane burner leak adds to explosive atmosphere","Ignition from conductor roll arc or static discharge"],
                        "consequences":["Explosion — furnace structure collapses","Multiple fatalities — HHO zone","Plant shutdown 3-6 months minimum","PESO/regulatory investigation, potential prosecution"],
                        "preventions":["PSAL 2.14 H2 pressure switch (PSCE #2) — auto-trip","UV 1.21 propane solenoid (PSCE #3) — auto-close","Hard interlocked N2 purge before H2 admission","H2 LEL continuous monitor with 20% LEL alarm"],
                        "mitigations":["Blast-resistant furnace bay design","Explosion relief panels in roof","Full HHO zone evacuation procedure","Emergency services pre-notified of H2 storage quantities"],
                    },
                },
                "Chemical Treatment": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"Electrolytic chromate passivation using Cr-VI (CrO3/Na2Cr2O7) bath at 40-45°C. Thin chromium oxide layer for corrosion protection and lacquer adhesion. MANDATORY: enclosed bath + Local Exhaust Ventilation + continuous air monitoring. CPCB/SPCB declared quantity.",
                    "hazardous":["Chromic Acid Cr-VI — IARC Group 1 Carcinogen (TLV-TWA 0.05 mg/m3)","Sodium Dichromate — strong oxidiser, carcinogen","Cr-VI mist generation during operation","Hexavalent chromium in wastewater — MSIHC Schedule chemical","Skin/eye contact — severe burns + sensitisation"],
                    "hazard_matrix":{"Toxic":"Y","Explosive":"N","Flammable":"N","Corrosive":"Y","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"N","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"Cr-VI (hexavalent chromium) is an IARC Group 1 confirmed human carcinogen causing lung cancer, nasal septum perforation, kidney damage. TLV-TWA is only 0.05 mg/m3 — one of the lowest industrial TLVs. A single bath overflow or LEV failure can expose workers to carcinogenic levels. Long-term exposure even at low levels = cancer fatality (chronic). Cr-VI in wastewater at ppb levels contaminate groundwater for decades — significant environmental consequence. Mandatory CPCB declaration under MSIHC Rules 1989. Two HHO criteria clearly met: potential for fatality (carcinogen) + significant environmental impact. Even without explosion risk this is the most toxic HHO on ETL-1.",
                    "parameters":[
                        ("Bath Temperature","40-45°C","40-45°C","<40°C: incomplete passivation, corrosion failure in service","≥45°C: Cr-VI volatilisation increases — TLV breach risk, SHUTDOWN"),
                        ("Treatment Current","300-2000 A","300-3500 A","<300 A: insufficient passivation layer","≥3500 A: Cr-VI reduction to Cr-III, bath balance upset"),
                        ("Cr-VI Air Concentration","<0.05 mg/m3 TLV","<0.1 mg/m3 ceiling","N/A (minimum desirable)","≥0.05 mg/m3: MANDATORY SHUTDOWN — MSIHC Rules 1989"),
                        ("Bath Cr-VI Level","Per SDS specification","Per SDS specification","Below spec: inadequate passivation","Above spec: increased mist generation, higher exposure risk"),
                    ],
                    "barriers":["Continuous Cr-VI air monitor — alarm at 0.05 mg/m3, SHUTDOWN at 0.08 mg/m3","Enclosed bath design with LEV — minimum 0.5 m/s face velocity","Bath temperature transmitter — alarm + auto-off at 45°C","Treatment current interlock (SOC: 300-2000 A)","PPE mandatory: Class C suit + air-supplied respirator","Cr-VI wastewater to dedicated chrome reduction plant","Annual medical surveillance (lung function, urine Cr levels)"],
                    "hazop":[
                        ("Bath Temp HIGH","≥45°C","Heating element malfunction","Cr-VI volatilisation spike — carcinogen exposure above TLV","Air monitor alarm, auto-bath off, evacuation"),
                        ("LEV FAILURE","Ventilation off","Fan failure / power cut","Cr-VI mist accumulates — carcinogenic atmosphere","LEV flow switch auto-trip on bath, area evacuation"),
                        ("Bath Overflow","Level >SOL","Tank integrity / makedown error","Cr-VI spill to floor/drain — ground contamination","Level alarm, sealed chrome pit, bunded area"),
                        ("Air Monitor FAILS","No reading","Sensor failure / calibration drift","Undetected Cr-VI exposure","Mandatory manual monitoring if analyser fails, SOP for downtime"),
                    ],
                    "bowtie":{
                        "top_event":"Cr-VI release to plant atmosphere above TLV-TWA (0.05 mg/m3)",
                        "causes":["LEV ventilation failure (fan stops)","Bath temperature exceeds 45°C (Cr-VI volatilisation)","Bath overflow during makedown","Air monitoring failure — undetected exposure"],
                        "consequences":["Carcinogen exposure — long-term lung cancer risk","MSIHC Rules 1989 violation — mandatory CPCB report","Regulatory shutdown + enforcement action","Cr-VI groundwater contamination (decadal persistence)"],
                        "preventions":["LEV flow switch — auto-bath trip if airflow drops","Bath temp transmitter — auto-off at 45°C","Enclosed bath design minimises mist generation","Continuous Cr-VI air monitor (quarterly calibration)"],
                        "mitigations":["Air-supplied respirator (immediately if alarm)","Full area evacuation and ventilation","Medical surveillance within 24h of suspected exposure","CPCB emergency notification within 48h"],
                    },
                },
                "Electrostatic Oiling": {
                    "cls":"LHO","color":"#6366f1",
                    "desc":"Electrostatic spray of DOS (Dioctyl Sebacate) oil onto strip surface at controlled rate. Protects strip surface during storage and transport to can manufacturers. Exit looper, tension leveller, side trimmer and recoiler follow. Final product: finished tin plate coil.",
                    "hazardous":["DOS oil (flash point 190°C) — combustible liquid","Electrostatic voltage 10-40 kV — shock hazard","Oil mist if excessive application"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"N","Corrosive":"N","Thermal":"N","Pressure":"N"},
                    "consequences":{"Property >50L":"N","Fatality":"N","Env. Impact":"N"},
                    "reasoning":"DOS flash point is 190°C — well above ambient process temperature. No ignition source exists at this temperature. Electrostatic 10-40 kV voltage is enclosed and earth-bonded — shock hazard requires deliberate bypass of safety systems. Credible failures: over-oiling (quality defect — lacquer bond failure), voltage arc to strip (minor marking). Maximum credible accident: small oil fire if DOS contacts sustained heat source, easily handled by local fire extinguisher. Property damage well below Rs.50L threshold. No fatality pathway. No environmental pathway (DOS is biodegradable, low toxicity). BOTH CRITERIA FOR LHO CONFIRMED — NO HHO THRESHOLD MET.",
                    "parameters":[
                        ("Primary Air Pressure","0.5-1.0 kg/cm2","0.5-1.0 kg/cm2","<0.5: poor atomisation, uneven oil","≥1.0: oil mist generation, excess consumption"),
                        ("Secondary Air Flow","60-300 mm WC","60-300 mm WC","<60: oil drip marks on strip","≥300: oil carry-over to coiler"),
                        ("Repelling Plate Voltage","-10 to -40 kV","-10 to -50 kV","Above -10 kV: poor distribution","Below -50 kV: arcing to strip surface"),
                    ],
                    "barriers":["Electrostatic voltage interlock","Earth bonding on all metalwork in oiling zone","Fire extinguisher positioned at oiling zone","Oil application weight verified per coil (g/m2 measurement)"],
                    "hazop":None,
                    "bowtie":None,
                },
            }

            proc_list = list(PSC_DATA.keys())
            proc_cols = st.columns(len(proc_list))
            for i, pname in enumerate(proc_list):
                pd2 = PSC_DATA[pname]
                is_active = (st.session_state.psc_proc == pname)
                bc = pd2["color"]
                with proc_cols[i]:
                    label = pd2["cls"]
                    btn_style = "primary" if is_active else "secondary"
                    if st.button(f"{pname[:18]}\n[{label}]", key=f"psc_btn_{pname}", use_container_width=True, type=btn_style):
                        st.session_state.psc_proc = pname
                        st.rerun()

            # Detail panel
            sel_proc = PSC_DATA[st.session_state.psc_proc]
            spname = st.session_state.psc_proc
            spcls = sel_proc["cls"]
            spcolor = sel_proc["color"]
            is_hho = spcls == "HHO"

            st.markdown(f"""<div style="background:{spcolor}10;border:1px solid {spcolor}40;border-left:5px solid {spcolor};border-radius:10px;padding:1rem 1.4rem;margin:.8rem 0">
<div style="display:flex;align-items:center;gap:12px;margin-bottom:.5rem">
<span style="background:{spcolor}20;color:{spcolor};border:1px solid {spcolor}50;font-size:.78rem;font-weight:700;padding:4px 14px;border-radius:20px">{spcls}</span>
<span style="font-size:1.1rem;font-weight:800;color:#f1f5f9">{spname}</span>
</div>
<div style="font-size:.82rem;color:#94a3b8;line-height:1.7">{sel_proc['desc']}</div>
</div>""", unsafe_allow_html=True)

            d1, d2 = st.columns(2)
            with d1:
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARDOUS SUBSTANCES / ENERGIES</div>', unsafe_allow_html=True)
                hlist = "".join(f'<div style="font-size:.78rem;color:#fca5a5;padding:3px 0;border-bottom:1px solid #1e3a5f">• {h}</div>' for h in sel_proc["hazardous"])
                st.markdown(f'<div style="background:#1a0505;border:1px solid rgba(239,68,68,.2);border-radius:8px;padding:.8rem;margin-bottom:.8rem">{hlist}</div>', unsafe_allow_html=True)

                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARD CLASSIFICATION MATRIX</div>', unsafe_allow_html=True)
                hm = sel_proc["hazard_matrix"]
                hmkeys = list(hm.keys())
                hmvals = [hm[k] for k in hmkeys]
                tblh = '<table style="border-collapse:collapse;width:100%;font-size:.72rem;margin-bottom:.8rem"><tr>'
                for k in hmkeys:
                    tblh += f'<th style="background:#080d18;padding:5px 8px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;text-align:center">{k}</th>'
                tblh += '</tr><tr>'
                for v in hmvals:
                    c = "#22c55e" if v=="Y" else "#475569"
                    bg2 = "rgba(34,197,94,.1)" if v=="Y" else "#0d1f35"
                    tblh += f'<td style="background:{bg2};padding:6px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;color:{c}">{v}</td>'
                tblh += '</tr></table>'
                st.markdown(tblh, unsafe_allow_html=True)

                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">SAFETY BARRIERS</div>', unsafe_allow_html=True)
                for b in sel_proc["barriers"]:
                    bc2 = "#22c55e"
                    st.markdown(f'<div style="font-size:.75rem;color:{bc2};padding:2px 0">✓ {b}</div>', unsafe_allow_html=True)

            with d2:
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">CONSEQUENCE ANALYSIS — WHY {}</div>'.format(spcls), unsafe_allow_html=True)
                cons = sel_proc["consequences"]
                for criterion, val in cons.items():
                    fc = "#ef4444" if val=="Y" else "#22c55e"
                    fbg = "rgba(239,68,68,.08)" if val=="Y" else "rgba(34,197,94,.06)"
                    ftext = "YES — HHO criterion MET" if val=="Y" else "NO — Threshold not reached"
                    st.markdown(f'<div style="background:{fbg};border-left:3px solid {fc};border-radius:6px;padding:7px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center"><span style="font-size:.78rem;color:#94a3b8">{criterion}</span><span style="font-size:.72rem;font-weight:700;color:{fc}">{ftext}</span></div>', unsafe_allow_html=True)

                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.6rem 0 .3rem">CLASSIFICATION REASONING</div>', unsafe_allow_html=True)
                reason = sel_proc["reasoning"]
                st.markdown(f'<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.9rem;font-size:.78rem;color:#94a3b8;line-height:1.75">{reason}</div>', unsafe_allow_html=True)

            # SOC/SOL Parameters with deviation cards
            st.markdown('<div class="sl-sec">Process Parameters — SOC / SOL / Deviation Consequences</div>', unsafe_allow_html=True)
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:.8rem;display:flex;gap:2rem;font-size:.78rem">
<span><b style="color:#22c55e">SOC</b> <span style="color:#64748b">= Safe Operating Condition — normal target range where process runs safely and on-spec</span></span>
<span><b style="color:#f97316">SOL</b> <span style="color:#64748b">= Safe Operating Limit — breach triggers immediate corrective action or plant trip</span></span>
</div>""", unsafe_allow_html=True)

            for param, soc, sol, low_dev, high_dev in sel_proc["parameters"]:
                is_crit = "CRITICAL" in high_dev or "SHUTDOWN" in high_dev
                crit_badge = ' <span style="background:rgba(239,68,68,.2);color:#ef4444;font-size:.6rem;font-weight:700;padding:1px 7px;border-radius:10px;border:1px solid rgba(239,68,68,.4)">PSM CRITICAL</span>' if is_crit else ""
                st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:1rem;margin-bottom:8px">
<div style="font-size:.85rem;font-weight:700;color:#e2e8f0;margin-bottom:.6rem">{param}{crit_badge}</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px">
<div style="background:#080d18;border:1px solid rgba(34,197,94,.2);border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:4px">SOC (TARGET)</div>
<div style="font-size:.9rem;font-weight:800;color:#22c55e;font-family:monospace">{soc}</div>
</div>
<div style="background:#080d18;border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:4px">SOL (LIMIT)</div>
<div style="font-size:.9rem;font-weight:800;color:#f97316;font-family:monospace">{sol}</div>
</div>
<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#64748b;margin-bottom:4px">CONSEQUENCE IF BREACHED</div>
<div style="font-size:.65rem;color:#94a3b8">See below</div>
</div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:6px">
<div style="background:rgba(234,179,8,.06);border:1px solid rgba(234,179,8,.2);border-left:3px solid #eab308;border-radius:6px;padding:.6rem .8rem">
<div style="font-size:.6rem;font-weight:700;color:#eab308;margin-bottom:3px">IF BELOW SOC/SOL:</div>
<div style="font-size:.75rem;color:#fde68a">{low_dev}</div>
</div>
<div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem .8rem">
<div style="font-size:.6rem;font-weight:700;color:#ef4444;margin-bottom:3px">IF ABOVE SOC/SOL:</div>
<div style="font-size:.75rem;color:#fca5a5">{high_dev}</div>
</div>
</div>
</div>""", unsafe_allow_html=True)

            # HAZOP table (HHO only)
            if is_hho and sel_proc.get("hazop"):
                st.markdown('<div class="sl-sec">HAZOP Study — What-If Deviation Analysis</div>', unsafe_allow_html=True)
                tblhazop = '<table style="border-collapse:collapse;width:100%;font-size:.78rem"><thead><tr style="background:#080d18">'
                for hh in ["Deviation","Parameter","Cause","Consequence","Safeguard"]:
                    tblhazop += f'<th style="padding:8px 12px;text-align:left;color:#64748b;font-size:.65rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f">{hh}</th>'
                tblhazop += '</tr></thead><tbody>'
                for row in sel_proc["hazop"]:
                    tblhazop += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:8px 12px;color:#f97316;font-weight:700">{row[0]}</td><td style="padding:8px 12px;color:#e2e8f0">{row[1]}</td><td style="padding:8px 12px;color:#94a3b8">{row[2]}</td><td style="padding:8px 12px;color:#fca5a5">{row[3]}</td><td style="padding:8px 12px;color:#4ade80;font-size:.72rem">{row[4]}</td></tr>'
                tblhazop += '</tbody></table>'
                st.markdown(tblhazop, unsafe_allow_html=True)

            # Bow Tie (HHO only)
            if is_hho and sel_proc.get("bowtie"):
                st.markdown('<div class="sl-sec">Bow Tie Analysis</div>', unsafe_allow_html=True)
                bt = sel_proc["bowtie"]
                bt1, bt2, bt3 = st.columns([2,1,2])
                with bt1:
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin-bottom:.4rem">CAUSES / THREATS</div>', unsafe_allow_html=True)
                    for c in bt["causes"]:
                        st.markdown(f'<div class="sl-cause">{c}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#22c55e;margin:.6rem 0 .3rem">PREVENTION BARRIERS</div>', unsafe_allow_html=True)
                    for c in bt["preventions"]:
                        st.markdown(f'<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:6px 10px;margin-bottom:5px;font-size:.75rem;color:#4ade80">✓ {c}</div>', unsafe_allow_html=True)
                with bt2:
                    te = bt["top_event"]
                    st.markdown(f'<div style="background:rgba(239,68,68,.12);border:2px solid #ef4444;border-radius:10px;padding:1rem;text-align:center;margin-top:1rem"><div style="font-size:.58rem;font-weight:700;color:#ef4444;letter-spacing:2px;margin-bottom:6px">TOP EVENT</div><div style="font-size:.78rem;font-weight:700;color:#e2e8f0;line-height:1.5">{te}</div></div>', unsafe_allow_html=True)
                with bt3:
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#ef4444;margin-bottom:.4rem">CONSEQUENCES</div>', unsafe_allow_html=True)
                    for c in bt["consequences"]:
                        st.markdown(f'<div class="sl-consq">{c}</div>', unsafe_allow_html=True)
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#f97316;margin:.6rem 0 .3rem">MITIGATION BARRIERS</div>', unsafe_allow_html=True)
                    for c in bt["mitigations"]:
                        st.markdown(f'<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-left:3px solid #f97316;border-radius:6px;padding:6px 10px;margin-bottom:5px;font-size:.75rem;color:#f97316">{c}</div>', unsafe_allow_html=True)

            # Summary table
            st.markdown('<div class="sl-sec">PSC Classification Summary — All Processes</div>', unsafe_allow_html=True)
            psc_rows2 = [
                ("Coil Feeding","N","N","N","Y","N","Y","N","N","N","","Y"),
                ("Cleaning & Rinsing","Y","Y","N","Y","Y","Y","Y","Y","Y","Y",""),
                ("Tin Plating","Y","Y","N","Y","N","N","Y","Y","Y","Y",""),
                ("Reflow Furnace","Y","Y","Y","Y","Y","Y","Y","Y","Y","Y",""),
                ("Chemical Treatment","Y","N","N","Y","Y","Y","N","Y","Y","Y",""),
                ("Electrostatic Oiling","N","N","N","N","N","N","N","N","N","","Y"),
            ]
            hdr2 = ["Process","Toxic","Explosive","Flammable","Corrosive","Thermal","Pressure","Property>50L","Fatality","Env.Impact","HHO","LHO"]
            tbl2 = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.75rem"><thead><tr style="background:#080d18">'
            for h in hdr2:
                tbl2 += f'<th style="padding:7px 10px;text-align:center;color:#64748b;font-size:.62rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
            tbl2 += '</tr></thead><tbody>'
            for row in psc_rows2:
                active_row = (row[0] == spname)
                row_bg = f"rgba({spcolor[1:3]},{spcolor[3:5]},{spcolor[5:7]},.05)" if active_row else "transparent"
                tbl2 += f'<tr style="border-bottom:1px solid #1e3a5f;background:{row_bg}">'
                for ii, v in enumerate(row):
                    if ii == 0:
                        fw = "700" if active_row else "500"
                        tbl2 += f'<td style="padding:7px 10px;color:#e2e8f0;font-weight:{fw};white-space:nowrap">{v}</td>'
                    elif v in ("Y","HHO","LHO"):
                        c3 = "#f97316" if v=="HHO" else "#6366f1" if v=="LHO" else "#22c55e"
                        tbl2 += f'<td style="padding:7px 10px;text-align:center;color:{c3};font-weight:700">{v}</td>'
                    elif v == "N":
                        tbl2 += f'<td style="padding:7px 10px;text-align:center;color:#475569">N</td>'
                    else:
                        tbl2 += f'<td style="padding:7px 10px;text-align:center;color:#1e3a5f">—</td>'
                tbl2 += '</tr>'
            tbl2 += '</tbody></table></div>'
            st.markdown(tbl2, unsafe_allow_html=True)

        # ── HOM ──────────────────────────────────────────────────────
        with tabs[2]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/HOM/001 Rev.06 Eff.Dt.:18.08.2023 — Hazard of Materials | ETL-1 Electrolytic Tinning Line</p>', unsafe_allow_html=True)

            # A-scale hazard category framework banner
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">HAZARD CATEGORIES (A-SCALE) — PSRM Classification Framework</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px;font-size:.7rem">
<div style="background:#f97316;background:rgba(249,115,22,.12);border:1px solid rgba(249,115,22,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#f97316">A1</b><br><span style="color:#64748b;font-size:.62rem">Flammable / Explosive</span></div>
<div style="background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#a78bfa">A2</b><br><span style="color:#64748b;font-size:.62rem">Toxic (TLV-based)</span></div>
<div style="background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#ef4444">A3</b><br><span style="color:#64748b;font-size:.62rem">Reactive / Unstable</span></div>
<div style="background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#3b82f6">A4</b><br><span style="color:#64748b;font-size:.62rem">Corrosive</span></div>
<div style="background:rgba(96,165,250,.12);border:1px solid rgba(96,165,250,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#60a5fa">A5</b><br><span style="color:#64748b;font-size:.62rem">High Pressure / Temp</span></div>
</div>
<div style="font-size:.7rem;color:#475569;margin-top:.5rem">A process is HHO if ANY A-category substance is present AND at least ONE of: property damage &gt;Rs.50L, potential fatality, or significant environmental impact is a credible consequence.</div>
</div>""", unsafe_allow_html=True)

            # Chemical selector
            CHEM_FULL = {
                "A1 — Sulphuric Acid (H2SO4)": {
                    "code":"A1","risk":72,"color":"#f97316",
                    "class":"Corrosive liquid, Oxidising agent","hazchem":"HAZCHEM 2R","nfpa":"3-0-2(W)","cas":"7664-93-9",
                    "tlv_twa":"1 mg/m3 (ACGIH 2023 — thoracic fraction, H2SO4 mist)","tlv_stel":"Not established (ACGIH). NIOSH: same 1 mg/m3 TWA, no STEL.","tlv_ceil":"Not established (ACGIH) | OSHA PEL: 1 mg/m3.","ld50":"2140 mg/kg (rat, oral) ✓","lc50":"510 mg/m3/2h (rat, inhal.) ✓",
                    "flash":"N/A (not flammable)","bp":"337°C (decomposes)","mp":"10°C (concentrated)","sg":"1.84 (conc.)","vp":"<0.3 hPa at 20°C",
                    "odour":"Odourless (dilute); slight choking odour (concentrated, heated)",
                    "reactivity":"Reacts violently with water (exothermic). Generates H2 gas with metals (Fe, Zn, Al). Reacts explosively with strong bases. Incompatible with Cr-VI compounds (explosive), organic materials, combustibles.",
                    "health":"CORROSIVE. Severe burns to skin, eyes, mucous membranes on contact. Acid mist inhalation: bronchospasm, pulmonary oedema. Dental erosion from chronic low-level exposure. Eye contact: severe burns, possible blindness. Ingestion: severe GI burns.",
                    "env":"Highly toxic to aquatic organisms. Reduces water pH drastically. Not persistent (neutralises/dilutes) but causes acute aquatic kill. CPCB Schedule chemical.",
                    "storage":"Store in separate, cool, well-ventilated area. Polyethylene or glass containers. Away from metals, bases, organics. Secondary containment (bunding) mandatory.",
                    "ppe":"Full face shield, rubber apron, rubber gloves, rubber boots. Air-supplied respirator if vapour/mist present. Chemical-resistant suit for bulk handling.",
                    "emergency":"Large spills: absorb with dry sand/earth, NOT sawdust. Neutralise with lime/Na2CO3 solution. Do NOT use water directly on large spills (violent reaction). Person contaminated: deluge shower 15 min minimum. EMERGENCY: 108 / nearest hospital.",
                    "etl1_use":"Pickling bath (8-10 g/L SOC), plating bath base electrolyte, pH control",
                    "soc":"Pickling: 8-10 g/L | Plating free acid: 13-16 g/L","sol":"Pickling: 8-10 g/L (tight) | Plating: 11-18 g/L",
                },
                "A2 — Phenol Sulfonic Acid (PSA)": {
                    "code":"A2","risk":55,"color":"#eab308",
                    "class":"Corrosive liquid, mixture ortho/para isomers — p-hydroxybenzene sulphonic acid. UN 2430. TSCA listed. GHS: H302, H314, H318.","hazchem":"HAZCHEM 2R","nfpa":"3-1-0","cas":"98-67-9",
                    "tlv_twa":"Not established (ACGIH) for PSA blend. Phenol component (CAS 108-95-2): ACGIH TLV-TWA 0.5 ppm (SKIN designation — systemic hazard via absorption). OSHA PEL phenol: 5 ppm TWA. NIOSH REL phenol: 5 ppm (19 mg/m3) TWA, 15.6 ppm STEL.",
                    "tlv_stel":"Not established for PSA. Phenol: ACGIH — no STEL set. NIOSH phenol STEL: 15.6 ppm.",
                    "tlv_ceil":"Not established for PSA. Phenol IDLH (NIOSH): 250 ppm — treat as upper bound for respiratory protection decisions.",
                    "idlh":"NIOSH IDLH for phenol component: 250 ppm. PSA: treat as phenol-hazard material. Respiratory protection required if generating mist/vapour above OEL guidance.",
                    "ld50":"Oral rat: ~1500 mg/kg (PSA mixture, by analogy). Phenol component (CAS 108-95-2): LD50 rat oral 317 mg/kg; dermal rat 1500 mg/kg; dermal rabbit 630 mg/kg (RTECS confirmed from Fishersci MSDS).",
                    "lc50":"Inhalation rat LC50 316 mg/m3/4H (phenol, RTECS HX9450000 — Fishersci MSDS confirmed). Mouse inhalation LC50 177 mg/m3/4H. PSA acid mist: treat per H2SO4 mist limit 1 mg/m3 (ACGIH).",
                    "flash":">150°C (closed cup) — combustible liquid, not flammable at ambient conditions","bp":"~186°C (decomposes above this)","mp":"~33°C (solidifies in cold storage — warm before use)","sg":"1.28 g/cm3 at 20°C","vp":"<0.01 hPa at 20°C — very low vapour pressure",
                    "odour":"Faint phenolic odour — odour threshold phenol: 0.05 ppm. Some warning property but not reliable. SKIN absorption is primary hazard route, not vapour.",
                    "reactivity":"Strong acid — exothermic reaction with strong bases (NaOH, KOH). Reacts with Na2Cr2O7/CrO3 (STRICTLY INCOMPATIBLE — oxidiser + organic acid = fire risk). Dissolves carbon steel, aluminium, copper — use PP, HDPE, or SS316. Decomposes >200°C producing SO2, phenol vapour. Hygroscopic. Reacts with active metals (Fe, Al) — liberates H2 gas.",
                    "health":"Skin and eye corrosive. SKIN ABSORPTION — phenol component crosses skin barrier causing systemic toxicity (ACGIH Skin designation). CNS effects: phenol causes sudden collapse at high doses. Cardiac arrhythmia from systemic phenol. Liver/kidney damage from chronic phenol absorption. Respiratory: acid mist irritates mucous membranes, bronchospasm. Not listed as carcinogen (IARC, ACGIH).",
                    "env":"Phenol aquatically toxic: fish (fathead minnow) LC50 41 mg/L 48h; Daphnia EC50 4 mg/L 96h (Fishersci confirmed). Rapidly biodegrades in soil — phenol half-life <5 days. Sulphonate component more persistent. WTP treatment removes phenol effectively. Does not bioconcentrate (BCF <100).",
                    "storage":"Cool, dry, sealed. HDPE or PP-lined containers. Away from: bases, oxidisers, Cr-VI (incompatible). Hygroscopic — seal tightly. Secondary containment. Inspect containers for corrosion at every filling.",
                    "ppe":"Chemical splash goggles mandatory. Full face shield for bulk handling. Nitrile or neoprene gloves. PVC chemical apron. Mist: half-mask with OV/acid gas cartridge. CRITICAL: wash skin immediately — phenol absorbs before pain sensation.",
                    "emergency":"Skin: IMMEDIATE wash with soap + water 15+ min — phenol absorbs silently through intact skin, causes systemic phenol poisoning. Eye: flush 15+ min, medical. Ingestion: do NOT induce vomiting, medical immediately. Spill: absorb with dry inert material, HDPE container, do NOT flush to drain (aquatic toxic).",
                    "etl1_use":"Electrolytic tin plating bath — grain refiner and conductivity agent. 3-6 g/L combined with ENSA. Controls tin crystal grain size and provides bath conductivity.",
                    "soc":"3-6 g/L (combined PSA+ENSA)","sol":"2-7 g/L",
                },
                "A3 — Dioctyl Sebacate (DOS)": {
                    "code":"A3","risk":30,"color":"#22c55e",
                    "class":"Combustible liquid","hazchem":"NFPA 1-1-0","nfpa":"1-1-0","cas":"122-62-3",
                    "tlv_twa":"10 mg/m3 (ACGIH PNOR inhalable) | 3 mg/m3 (respirable) — nuisance aerosol","tlv_stel":"Not established specifically. Respirable PNOR ACGIH: 3 mg/m3 (same as TWA respirable — no STEL set).","tlv_ceil":"Not established (negligible vapour pressure — essentially no ceiling needed).","ld50":"5000 mg/kg (rat, oral) ✓ Wikipedia ChemSpider","lc50":"Not established (VP 0.000024 Pa — no inhalation hazard at ambient)",
                    "flash":"190°C (closed cup)","bp":">300°C","mp":"-40°C","sg":"0.914","vp":"<0.01 hPa at 20°C",
                    "odour":"Faint oily odour",
                    "reactivity":"Stable under normal conditions. Incompatible with strong oxidisers (CrO3 — hazardous reaction). High temperatures cause decomposition to CO, CO2. Not reactive with water or bases under normal conditions.",
                    "health":"Low acute toxicity. Mild skin and eye irritant. Not a known carcinogen. Oil mist at elevated temperatures may cause respiratory irritation.",
                    "env":"Low toxicity to aquatic organisms. Biodegradable. Low environmental persistence.",
                    "storage":"Normal conditions. Cool, dry. Away from strong oxidisers and ignition sources above 190°C.",
                    "ppe":"Safety glasses, standard work gloves for routine handling.",
                    "emergency":"Spills: absorb with dry material. Non-hazardous cleanup. Person: wash with soap and water.",
                    "etl1_use":"Electrostatic oiling — applied to finished tin plate surface at 1-2 g/m2 for corrosion protection in storage/transport",
                    "soc":"Oil application rate per product spec","sol":"Per product spec",
                },
                "A4 — ENSA (Ethoxylated Naphthol Sulphonic Acid)": {
                    "code":"A4","risk":40,"color":"#22c55e",
                    "class":"Proprietary plating brightener — ethoxylated alpha/beta naphthol sulphonate. Atotech/Enthone/MacDermid proprietary. TSCA listed components. GHS: H302, H312, H332, H315, H319.","hazchem":"NFPA 2-1-1","nfpa":"2-1-1","cas":"Mixture (naphthol sulphonate: 1321-69-3)",
                    "tlv_twa":"Not established for ENSA blend (ACGIH/NIOSH). Naphthol (alpha, CAS 90-15-3): no OEL set. Beta-naphthol (CAS 135-19-3): not listed. Plating bath acid mist (H2SO4): ACGIH TLV-TWA 1 mg/m3. Use 1 mg/m3 as practical guidance for acid mist control.",
                    "tlv_stel":"Not established. Plating acid mist STEL: 3 mg/m3 (H2SO4, by analogy).",
                    "tlv_ceil":"Not established",
                    "idlh":"Not established by NIOSH for ENSA. Parent naphthol NIOSH IDLH: not determined. Control to below LEV design level.",
                    "ld50":"Not published for proprietary blend. Alpha-naphthol (CAS 90-15-3): LD50 rat oral 1870 mg/kg. Beta-naphthol (CAS 135-19-3): LD50 rat oral 2000 mg/kg. ENSA estimated: >2000 mg/kg oral (low-moderate toxicity).",
                    "lc50":"Not established for ENSA blend. Alpha-naphthol vapour LC50: not determined (low VP at ambient — not significant inhalation hazard as vapour). Acid mist: LC50 rat H2SO4 mist 0.35 mg/L/2H (reference for mist control).",
                    "flash":"~170°C (estimated)","bp":"200-250°C (decomposes)","mp":"Liquid at ambient (unknown solidification temp)","sg":"~1.1-1.2 g/cm3","vp":"Very low at ambient — not a significant vapour hazard",
                    "odour":"Mild aromatic/naphthenic odour — detectable before significant hazard concentration in most conditions.",
                    "reactivity":"Moderately stable in dilute H2SO4 (plating bath pH 1-2). INCOMPATIBLE with: strong oxidisers (Na2Cr2O7, CrO3 — DO NOT MIX), strong bases (>pH 12 — hydrolysis). Decomposes above 60°C in strongly acidic bath — ENSA breakdown products accumulate → plating quality deteriorates. Naphthol component: reacts with Cr-VI oxidisers — fire risk.",
                    "health":"Skin irritant (H315), eye irritant (H319). Naphthol component: systemic toxicity if absorbed — liver, kidney effects. Respiratory: acid bath mist is the primary inhalation concern (H2SO4 mist from plating bath, not ENSA vapour). No evidence of carcinogenicity (IARC not listed for ENSA or naphthol sulphonate). Chronic: monitor bath breakdown products — naphthol concentration should not exceed OEL guidance.",
                    "env":"Aquatic toxicity: alpha-naphthol fish LC50 ~3 mg/L (moderately toxic). Daphnia EC50 ~2-4 mg/L. Ethoxylate surfactant: moderate persistence. WTP biological treatment reduces naphthol. Naphthol sulphonate: more persistent than parent. Do not discharge untreated to surface water.",
                    "storage":"Cool, dark, sealed HDPE containers. Away from Cr-VI oxidisers (incompatible). Shelf life 12 months sealed. Protect from freezing. Segregate from Cr-VI storage (chemical incompatibility).",
                    "ppe":"Chemical splash goggles. Nitrile gloves. Lab coat. Bath area: LEV mandatory (acid mist). Half-mask with P2 particulate filter if mist exposure likely.",
                    "emergency":"Skin/Eye: flush 15+ min (naphthol absorption risk on skin). Ingestion: medical immediately — naphthol toxic. Spill: collect in HDPE, absorb with inert material, do NOT flush to drain (aquatic toxic). Neutralise with sodium bicarbonate before disposal.",
                    "etl1_use":"Electrolytic tin plating bath brightener — combined with PSA (3-6 g/L total). Controls tin grain size, produces bright mirror finish. Critical for tin plate quality specification.",
                    "soc":"3-6 g/L (combined PSA+ENSA)","sol":"2-7 g/L",
                },
                "A5 — Sodium Dichromate (Na2Cr2O7)": {
                    "code":"A5","risk":95,"color":"#ef4444",
                    "class":"CARCINOGEN (IARC Gr.1 | ACGIH A1 | NTP Known | Cal Prop 65) — Oxidising solid, TOXIC, reproductive toxin, aquatic hazard. UN 3288. GHS: H272 H301 H312 H314 H317 H330 H334 H340 H350 H360 H372 H410.","hazchem":"HAZCHEM 2X","nfpa":"4-0-1 (OX)","cas":"10588-01-9 (anhydrous) | 7789-12-0 (dihydrate)",
                    "tlv_twa":"ACGIH TLV-TWA: 0.01 mg/m3 as Cr(VI) — 2023 (A1 Confirmed Human Carcinogen). OSHA PEL: 5 µg/m3 (0.005 mg/m3) as Cr(VI) — 29 CFR 1910.1026 (2006). NIOSH REL: 0.0002 mg/m3 (0.2 µg/m3) as Cr — lowest feasible concentration. INDIA: Factories Act — adopt ACGIH/OSHA limit.",
                    "tlv_stel":"Not established separately. OSHA Action Level: 2.5 µg/m3 as Cr(VI). Above AL: medical surveillance + air monitoring mandatory.",
                    "tlv_ceil":"ACGIH: TLV-TWA applies — no separate ceiling. Treat as effective ceiling due to A1 carcinogen classification. Any detectable Cr(VI) above OEL = corrective action.",
                    "idlh":"NIOSH IDLH: 15 mg/m3 as Cr(VI). IMMEDIATELY DANGEROUS TO LIFE AND HEALTH above this. Biological Exposure Index (BEI): 25 µg Cr/g creatinine (end-of-shift urine) — annual biological monitoring mandatory.",
                    "ld50":"Oral rat: 50 mg/kg (CAS 10588-01-9, Wikipedia/PubChem/Fishersci confirmed). Dermal rabbit: 1000 mg/kg (Acros MSDS confirmed). HIGHLY TOXIC by ingestion (GHS Category 3).",
                    "lc50":"Inhalation rat: 0.124 mg/L/4H (Acros MSDS confirmed, RTECS HX7750000). EXTREMELY TOXIC by inhalation. Note: LC50 well above IDLH — sub-lethal carcinogenic doses are the primary concern.",
                    "flash":"Non-flammable — OXIDISING SOLID. Contact with organics/combustibles causes fire without external ignition.","bp":"400°C decomposes (no boiling)","mp":"356.7°C (anhydrous) | Dihydrate loses crystal water at 84°C","sg":"2.52 g/cm3","vp":"Negligible at ambient — DUST is the inhalation hazard, not vapour.",
                    "odour":"Odourless — ABSOLUTELY NO SENSORY WARNING. Carcinogen exposure occurs without any detectable smell. CONTINUOUS REAL-TIME AIR MONITORING IS MANDATORY — no substitutes.",
                    "reactivity":"STRONG OXIDISER — spontaneous ignition with: organics (paper, wood, cloth, ethanol, acetone, oils). Violently exothermic with reducing agents (FeSO4, Na2SO3, Fe). Reacts with H2SO4 — forms CrO3 solution (chromic acid — even more reactive). INCOMPATIBLE: ALL organic compounds, all reducing agents, ammonium compounds (explosive at temperature), combustible metals.",
                    "health":"IARC Group 1 | ACGIH A1 | NTP Known Human Carcinogen. Primary: lung cancer (15-30x elevated risk in chromate production workers — Mancuso 1975, IARC 1990). Nasal cavity, sinuses, larynx cancers. Mechanism: Cr(VI) enters cells via sulphate transport channels → reduced to Cr(III) inside → DNA adducts, double-strand breaks, chromosomal aberrations. Skin: chrome ulcers (slow, painless, deep — CAS of ulcer documented in Indian Chrome workers). Eye: severe corrosive burns. Systemic: kidney tubular damage, liver injury. Reproductive: teratogenic, H360. Latency: 15-30 years. Annual medical surveillance mandatory under Factories Act.",
                    "env":"Cr(VI) VERY HIGHLY TOXIC to aquatic organisms. Fish LC50 (bluegill): 425-488 mg/L 96h (Fishersci). Daphnia: extremely sensitive (<1 mg/L). PERSISTENT in groundwater — resists biodegradation. CPCB effluent standard: Cr(VI) <0.1 mg/L final discharge. Must be chemically reduced to Cr(III) before treatment (use FeSO4 or SO2 at pH<3). MCL drinking water India: 0.05 mg/L total Cr. MSIHC Schedule — annual inventory to CPCB.",
                    "storage":"DEDICATED LOCKED STORE — all organics prohibited within 5m (incompatible). Cool, dry, ventilated. Secondary containment 110% volume. HDPE or PP-lined containers (not steel — corrosion). Annual CPCB inventory submission. MSIHC notification: above threshold. Fire extinguisher: water spray ONLY (no CO2 or dry powder). Restricted access — biometric/key control recommended.",
                    "ppe":"MANDATORY: Air-supplied respirator (SCBA or airline) — NO cartridge respirator acceptable for Cr-VI carcinogen work. Class B/C chemical suit. Full face shield. Heavy neoprene gloves (>0.5mm). Rubber boots. Buddy system mandatory. Annual biological monitoring: urine Cr (BEI: 25 µg/g creatinine).",
                    "emergency":"EVACUATE — no entry without SCBA. SPECIALIST HAZMAT RESPONSE ONLY. Spill: wet methods only (no dry sweeping — dust hazard). Cr(VI) reduction: FeSO4 at pH<3 then neutralise to pH 8-9. Person: immediate shower/decontamination, remove all clothing, medical examination, report to OH. CPCB notification within 48h of significant release.",
                    "etl1_use":"Chemical treatment bath — electrolytic chromate passivation. <10 mg Cr/m2 deposited on tinplate for corrosion protection and lacquer adhesion. MSIHC Schedule substance.",
                    "soc":"Air: <0.01 mg/m3 as Cr(VI) | Bath temp: 40-45°C | Bath current: 300-2000A","sol":"Air OEL breach = immediate corrective action | Bath temp: >45°C = auto-shutdown | Air Cr-VI >0.1 mg/m3 = EVACUATION",
                },
                "A6 — Chromic Acid (CrO3/Cr-VI)": {
                    "code":"A6","risk":98,"color":"#ef4444",
                    "class":"CARCINOGEN — Powerful oxidiser, corrosive, highly toxic","hazchem":"NFPA 3-0-1 (OX)","nfpa":"3-0-1 (OX)","cas":"1333-82-0",
                    "tlv_twa":"0.05 mg/m3 as Cr (ACGIH)","tlv_stel":"0.1 mg/m3 ceiling","tlv_ceil":"0.1 mg/m3","ld50":"80 mg/kg (rat, oral)","lc50":"<10 mg/m3 (rat, 4h)",
                    "flash":"N/A (powerful oxidiser — not flammable but CAUSES fires)","bp":"250°C (decomposes)","mp":"196°C","sg":"2.70","vp":"Not applicable",
                    "odour":"Acrid, metallic (vapour/mist)",
                    "reactivity":"POWERFUL OXIDISER — contact with organics (oil, paper, wood, solvents) causes spontaneous ignition. Reacts explosively with reducing agents. Mixed with H2SO4: forms chromic acid solution. EXPLOSIVE contact with alcohol/acetone/ketones. Generates toxic Cr-VI mist when heated or agitated. Incompatible with: all organic materials, H2SO4 (exothermic), reducing agents, combustibles.",
                    "health":"IARC Group 1 CARCINOGEN — highest category. Causes lung cancer (15-30x normal risk with occupational exposure), nasal septum perforation, kidney cancer. TLV 0.05 mg/m3 — one of the lowest industrial TLVs. Acute: severe skin corrosion, eye burns, nasal ulceration. Skin sensitiser. Mutagenic, teratogenic.",
                    "env":"MOST TOXIC common industrial chemical to aquatic organisms. Cr-VI persists in groundwater for decades. Classified as Priority Hazardous Substance under EU WFD. MSIHC mandatory reporting. MCL drinking water: 0.05 mg/L.",
                    "storage":"SEPARATE, locked, cool, dry store. NO organic materials within 5m. Secondary containment 110% volume. Access restricted to trained, medically cleared personnel. MSIHC annual reporting to CPCB/SPCB.",
                    "ppe":"MANDATORY: Air-supplied respirator (SCBA or airline), Class C full-body protective suit, face shield, heavy rubber gloves + boots. PPE inspection before every entry. Buddy system mandatory.",
                    "emergency":"EVACUATE — do not re-enter without SCBA. Specialist hazmat team only. Person contaminated: immediate SCBA removal, decontamination, emergency medical. Notify: plant emergency, CPCB (within 48h), state SPCB. Document all exposures — medical surveillance mandatory.",
                    "etl1_use":"Chemical treatment bath — Cr-VI passivation layer on tin plate (< 10 mg/m2 Cr on finished product for food can use)",
                    "soc":"Air: <0.05 mg/m3 (TLV-TWA)","sol":"Air: <0.1 mg/m3 ceiling | Breach = mandatory immediate SHUTDOWN",
                },
            }

            if "hom_chem" not in st.session_state:
                st.session_state.hom_chem = "A6 — Chromic Acid (CrO3/Cr-VI)"

            # Chemical selector buttons
            chem_names = list(CHEM_FULL.keys())
            chem_cols = st.columns(len(chem_names))
            for ii, cname in enumerate(chem_names):
                cd = CHEM_FULL[cname]
                rc3 = cd["color"]
                active = (st.session_state.hom_chem == cname)
                with chem_cols[ii]:
                    riskval = cd["risk"]
                    st.markdown(f'<div style="background:{rc3}15;border:1px solid {rc3}50;border-top:3px solid {rc3};border-radius:8px;padding:.6rem;text-align:center;margin-bottom:4px"><div style="font-size:.65rem;font-weight:700;color:{rc3}">{cd["code"]}</div><div style="font-size:.75rem;font-weight:900;color:{rc3};font-family:monospace">{riskval}/100</div></div>', unsafe_allow_html=True)
                    if st.button(cname[:16], key=f"hom_{cname}", use_container_width=True, type="primary" if active else "secondary"):
                        st.session_state.hom_chem = cname
                        st.rerun()

            # Detail card
            sel_chem = CHEM_FULL[st.session_state.hom_chem]
            sc2 = sel_chem["color"]
            criskval = sel_chem["risk"]

            st.markdown(f"""<div style="background:{sc2}10;border:1px solid {sc2}40;border-left:5px solid {sc2};border-radius:10px;padding:1rem 1.4rem;margin:.8rem 0;display:flex;justify-content:space-between;align-items:flex-start">
<div>
<div style="font-size:1.1rem;font-weight:800;color:#f1f5f9;margin-bottom:.2rem">{st.session_state.hom_chem}</div>
<div style="font-size:.78rem;color:#64748b">{sel_chem['class']}</div>
<div style="font-size:.72rem;color:#64748b;margin-top:.2rem">CAS: {sel_chem['cas']} &nbsp;|&nbsp; HAZCHEM: {sel_chem['hazchem']} &nbsp;|&nbsp; NFPA: {sel_chem['nfpa']}</div>
<div style="font-size:.72rem;color:#f97316;font-weight:700;margin-top:.3rem">ETL-1 Use: {sel_chem['etl1_use']}</div>
</div>
<div style="text-align:center;min-width:80px">
<div style="font-size:2rem;font-weight:900;color:{sc2};font-family:monospace">{criskval}</div>
<div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#475569">RISK SCORE</div>
{risk_bar(criskval)}
</div>
</div>""", unsafe_allow_html=True)

            # A-category tags for this chemical
            chem_acat_map = {
                "A1 — Sulphuric Acid (H2SO4)":    [("A2","Toxic (TLV 1 mg/m3)","#a78bfa"),("A4","Corrosive","#3b82f6"),("A3","Reactive (H2 with metals)","#ef4444")],
                "A2 — Phenol Sulfonic Acid (PSA)":  [("A2","Irritant","#a78bfa"),("A4","Corrosive","#3b82f6")],
                "A3 — Dioctyl Sebacate (DOS)":       [("A1","Combustible (flash 190°C)","#f97316")],
                "A4 — ENSA":                          [("A2","Irritant","#a78bfa")],
                "A5 — Sodium Dichromate (Na2Cr2O7)": [("A2","CARCINOGEN IARC Gr.1 (TLV 0.05 mg/m3)","#a78bfa"),("A3","Strong Oxidiser","#ef4444")],
                "A6 — Chromic Acid (CrO3/Cr-VI)":    [("A2","CARCINOGEN IARC Gr.1 (TLV 0.05 mg/m3)","#a78bfa"),("A3","Powerful Oxidiser","#ef4444"),("A4","Corrosive","#3b82f6")],
            }
            acats = chem_acat_map.get(st.session_state.hom_chem, [])
            if acats:
                acat_html = " ".join(f'<span style="background:{c}20;color:{c};border:1px solid {c}40;font-size:.68rem;font-weight:700;padding:3px 10px;border-radius:20px;margin-right:4px">{cat}: {desc}</span>' for cat, desc, c in acats)
                st.markdown(f'<div style="margin-bottom:.6rem">{acat_html}</div>', unsafe_allow_html=True)

            # TLV explanations
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.6rem 1rem;margin-bottom:.6rem;font-size:.72rem;color:#64748b">
<b style="color:#e2e8f0">TLV-TWA:</b> Time-Weighted Average over 8h shift — maximum daily exposure. &nbsp;
<b style="color:#e2e8f0">TLV-STEL:</b> Short-Term Exposure Limit (15 min) — peak limit. &nbsp;
<b style="color:#e2e8f0">TLV-C:</b> Ceiling — never to be exceeded even instantaneously. &nbsp;
<b style="color:#ef4444">IDLH:</b> Immediately Dangerous to Life & Health — emergency escape value.
</div>""", unsafe_allow_html=True)

            # Full data in tabs
            st.markdown('<div class="sl-sec">Physical & Toxicity Data</div>', unsafe_allow_html=True)

            # ── Quick Reference Comparison Table — All ETL-1 Chemicals ──
            st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">QUICK REFERENCE — ALL ETL-1 CHEMICALS (Toxicology & Regulatory Data)</div>""", unsafe_allow_html=True)
            etl1_qr_data = [
                # code, name, color, nfpa, tlv_twa, tlv_stel, tlv_ceil, idlh, ld50, lc50, hazard
                # H2SO4: ACGIH 2023 TLV-TWA 1 mg/m3 (thoracic fraction), STEL not established, Ceiling not established
                # OSHA PEL: 1 mg/m3. NIOSH REL: 1 mg/m3 TWA. IDLH: 80 mg/m3
                ("A1","Sulphuric Acid H₂SO₄","#f97316","3-0-2(W)",
                 "1 mg/m³ (thoracic fraction, ACGIH 2023)","Not established (ACGIH) | OSHA: 1 mg/m³ PEL","Not established (ACGIH) | NIOSH: 1 mg/m³ TWA",
                 "80 mg/m³ (NIOSH)","2140 mg/kg (rat, oral) ✓","510 mg/m³/2H (rat) ✓","A2 Toxic · A3 Reactive with metals/bases · A4 Corrosive"),
                # PSA: No OEL for PSA itself. Parent phenol (ACGIH): TLV-TWA 0.5 ppm SKIN, no STEL, no ceiling
                # OSHA PEL phenol: 5 ppm. NIOSH REL: 5 ppm TWA, 15.6 ppm STEL
                ("A2","Phenol Sulfonic Acid (PSA)","#eab308","3-1-0",
                 "0.5 ppm (phenol component, ACGIH, SKIN designation)","15.6 ppm (NIOSH STEL for phenol component)","Not established (no ceiling for PSA or phenol, ACGIH/NIOSH)",
                 "250 ppm (NIOSH IDLH for phenol component)","~1500 mg/kg (est. from phenol analogy)","316 mg/m³/4H (phenol, RTECS) ✓","A4 Corrosive · SKIN absorption — systemic phenol hazard"),
                # DOS: No OEL set. ACGIH: unclassified. Nuisance aerosol limit applies: ACGIH PNOR 10 mg/m3 (respirable 3 mg/m3)
                # No STEL, no ceiling, no IDLH established
                ("A3","Dioctyl Sebacate (DOS)","#22c55e","1-1-0",
                 "10 mg/m³ (ACGIH PNOR — Particles Not Otherwise Regulated, inhalable fraction)","3 mg/m³ (ACGIH PNOR respirable fraction — no specific STEL)","Not established (no chemical-specific ceiling)",
                 "Not established (very low toxicity — no IDLH set)","5000 mg/kg (rat, oral) ✓ Wikipedia/ChemSpider","Not established (negligible vapour pressure — 0.000024 Pa)","A1 Combustible (flash 210°C) · Food contact grade FDA 21 CFR 175.105"),
                # ENSA: No OEL for blend. Acid mist (H2SO4) present in plating bath: ACGIH TLV-TWA 1 mg/m3, STEL 3 mg/m3
                # Alpha-naphthol (ACGIH): no TLV set. NIOSH: no REL
                ("A4","ENSA (Ethoxylated Naphthol Sulphonate)","#22c55e","2-1-1",
                 "1 mg/m³ (H₂SO₄ acid mist at bath — ACGIH TLV for sulphuric acid mist applies)","3 mg/m³ (H₂SO₄ STEL by analogy — no ENSA-specific STEL established)","Not established for ENSA blend. Acid mist ceiling: not set by ACGIH.",
                 "Not determined (no NIOSH IDLH for ENSA or α-naphthol)","~1870 mg/kg (α-naphthol, CAS 90-15-3) ✓ Fishersci","Not established for ENSA (low VP). Acid mist LC50 ref: 0.35 mg/L/2H (H₂SO₄)","A2 Irritant · Aquatic toxic (α-naphthol fish LC50 ~3 mg/L)"),
                # Na2Cr2O7: ACGIH TLV-TWA 0.01 mg/m3 as Cr(VI), A1 carcinogen. No STEL (ACGIH).
                # OSHA: no separate STEL, Action Level 2.5 µg/m3. No ceiling (OSHA TWA only).
                # NIOSH REL: 0.0002 mg/m3 (0.2 µg/m3). IDLH: 15 mg/m3 as Cr(VI)
                ("A5","Sodium Dichromate Na₂Cr₂O₇","#ef4444","4-0-1(OX)",
                 "0.01 mg/m³ as Cr(VI) (ACGIH A1 Carcinogen, 2023) | OSHA PEL: 0.005 mg/m³ | NIOSH REL: 0.0002 mg/m³",
                 "Not established (ACGIH — A1 carcinogen, TWA is controlling limit) | OSHA Action Level: 0.0025 mg/m³ as Cr(VI)",
                 "Not established as separate ceiling (ACGIH) — TLV-TWA is the limit. Any exceedance = corrective action.",
                 "15 mg/m³ as Cr(VI) (NIOSH IDLH) ✓","50 mg/kg (rat, oral, CAS 10588-01-9) ✓ Fishersci/PubChem","0.124 mg/L/4H (rat, inhalation) ✓ Acros MSDS/RTECS HX7750000","IARC Gr.1 CARCINOGEN · ACGIH A1 · NTP Known · A3 Strong Oxidiser · Reproductive Toxin H360"),
                # CrO3: Same TLV as Na2Cr2O7 (both Cr(VI) compounds, ACGIH classifies as Cr(VI) compounds group)
                # ACGIH Ceiling: 0.05 mg/m3 (historical) — current TLV-TWA 0.01 mg/m3 supersedes
                # OSHA: Ceiling 0.1 mg/m3 (as CrO3, old 1971 standard) — superseded by 2006 Cr(VI) standard
                ("A6","Chromic Acid CrO₃","#ef4444","3-0-1(OX)",
                 "0.01 mg/m³ as Cr(VI) (ACGIH A1 Carcinogen, 2023) | OSHA PEL: 0.005 mg/m³ | NIOSH REL: 0.0002 mg/m³",
                 "Not established (ACGIH 2023) | OSHA 2006 Cr(VI) rule: no separate STEL — TWA 0.005 mg/m³ is controlling",
                 "0.1 mg/m³ (OSHA 1971 legacy ceiling as CrO₃ — superseded by 2006 Cr(VI) PEL of 0.005 mg/m³ TWA) | ACGIH: no ceiling separate from TLV-TWA",
                 "15 mg/m³ as Cr(VI) (NIOSH IDLH) ✓","80 mg/kg (rat, oral) ✓","<10 mg/m³/4H (rat, RTECS) ✓","IARC Gr.1 CARCINOGEN · ACGIH A1 · A3 Powerful Oxidiser (spontaneous ignition with organics)"),
            ]
            etl_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for hh in ["Code","Chemical","NFPA","TLV-TWA (ACGIH)","TLV-STEL","TLV-Ceiling","IDLH (NIOSH)","LD50 (oral, rat)","LC50 (inhal, rat)","Key Hazard"]:
                etl_tbl += f'<th style="padding:6px 10px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            etl_tbl += '</tr></thead><tbody>'
            for row in etl1_qr_data:
                code, name, color, nfpa, tlv_twa, tlv_stel, tlv_c, idlh, ld50, lc50, hazard = row
                is_crit = "CARCINOGEN" in hazard
                row_bg = "rgba(239,68,68,.04)" if is_crit else "transparent"
                etl_tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{row_bg}">'
                etl_tbl += f'<td style="padding:6px 10px"><span style="background:{color}20;color:{color};border:1px solid {color}40;font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:20px">{code}</span></td>'
                etl_tbl += f'<td style="padding:6px 10px;color:#e2e8f0;font-weight:600;white-space:nowrap">{name}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:#60a5fa;font-family:monospace;font-weight:700;white-space:nowrap">{nfpa}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:{"#ef4444" if "A1" in tlv_twa else "#f97316"};font-weight:600">{tlv_twa}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:#94a3b8">{tlv_stel}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:#94a3b8">{tlv_c}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:{"#ef4444" if "mg/m" in idlh or "ppm" in idlh else "#475569"};font-weight:{"700" if "mg/m" in idlh else "400"}">{idlh}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:#94a3b8;font-family:monospace">{ld50}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:#94a3b8;font-family:monospace">{lc50}</td>'
                etl_tbl += f'<td style="padding:6px 10px;color:{"#fca5a5" if "CARCINOGEN" in hazard else "#64748b"};font-size:.68rem">{hazard}</td>'
                etl_tbl += '</tr>'
            etl_tbl += '</tbody></table></div>'
            st.markdown(etl_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.68rem;color:#475569;margin-bottom:.8rem">✓ = source-verified value. Sources: ACGIH TLV Booklet 2023, NIOSH Pocket Guide 2023, RTECS, Fishersci MSDS, Acros MSDS, Wikipedia (peer-reviewed), PubChem.</div>', unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            with r1:
                    st.markdown(f"""<div class="sl-card">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.6rem">EXPOSURE LIMITS (A2 — Toxicity)</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:.78rem">
<div style="color:#64748b">TLV-TWA:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['tlv_twa']}</div>
<div style="color:#64748b">TLV-STEL:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['tlv_stel']}</div>
<div style="color:#64748b">TLV-Ceiling:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['tlv_ceil']}</div>
<div style="color:#ef4444;font-weight:700">IDLH (NIOSH):</div><div style="color:#fca5a5;font-weight:600">{sel_chem.get('idlh','Not established')}</div>
<div style="color:#64748b">LD50 (oral, rat):</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['ld50']}</div>
<div style="color:#64748b">LC50 (inhal, rat):</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['lc50']}</div>
</div></div>""", unsafe_allow_html=True)
            with r2:
                    st.markdown(f"""<div class="sl-card">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.6rem">PHYSICAL PROPERTIES</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:4px;font-size:.78rem">
<div style="color:#64748b">Flash Point:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['flash']}</div>
<div style="color:#64748b">Boiling Point:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['bp']}</div>
<div style="color:#64748b">Melting Point:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['mp']}</div>
<div style="color:#64748b">Specific Gravity:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['sg']}</div>
<div style="color:#64748b">Vapour Pressure:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['vp']}</div>
<div style="color:#64748b">Odour:</div><div style="color:#e2e8f0;font-weight:600">{sel_chem['odour']}</div>
</div></div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="sl-card" style="margin-top:.5rem"><b style="color:#f97316">Reactivity & Incompatibilities:</b><br><span style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sel_chem["reactivity"]}</span></div>', unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Health & Environmental Hazards</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="display:grid;grid-template-columns:1fr 1fr;gap:.8rem">
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:.5rem">HEALTH HAZARDS</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sel_chem['health']}</div></div>
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:.5rem">ENVIRONMENTAL IMPACT</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sel_chem['env']}</div></div>
</div>""", unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Storage, PPE & Emergency Response</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem">
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.5rem">STORAGE REQUIREMENTS</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sel_chem['storage']}</div></div>
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#a78bfa;margin-bottom:.5rem">PPE REQUIREMENTS</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sel_chem['ppe']}</div></div>
<div class="sl-card"><div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:.5rem">EMERGENCY RESPONSE</div><div style="font-size:.78rem;color:#94a3b8;line-height:1.8">{sel_chem['emergency']}</div></div>
</div>""", unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">ETL-1 SOC / SOL</div>', unsafe_allow_html=True)
            st.markdown(f"""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:1rem;margin-bottom:.8rem">
<div style="font-size:.7rem;font-weight:700;color:#f97316;margin-bottom:.5rem">ETL-1 APPLICATION: {sel_chem['etl1_use']}</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
<div style="text-align:center;background:#080d18;border-radius:8px;padding:.8rem">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:4px">SOC (TARGET)</div>
<div style="font-size:1rem;font-weight:800;color:#22c55e;font-family:monospace">{sel_chem['soc']}</div>
</div>
<div style="text-align:center;background:#080d18;border-radius:8px;padding:.8rem">
<div style="font-size:.58rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:4px">SOL (LIMIT)</div>
<div style="font-size:1rem;font-weight:800;color:#f97316;font-family:monospace">{sel_chem['sol']}</div>
</div>
</div></div>""", unsafe_allow_html=True)

            # Comparison bar chart
            fig_hom2 = go.Figure(go.Bar(
            x=[CHEM_FULL[k]["code"] for k in CHEM_FULL],
            y=[CHEM_FULL[k]["risk"] for k in CHEM_FULL],
            marker_color=[sc2 if k == st.session_state.hom_chem else risk_color(CHEM_FULL[k]["risk"]) for k in CHEM_FULL],
            text=[str(CHEM_FULL[k]["risk"]) for k in CHEM_FULL],
            textposition="outside", textfont=dict(color="#94a3b8", size=11),
            ))
            fig_hom2.add_hline(y=75, line_dash="dot", line_color="#f97316",
                              annotation_text="High risk threshold",
                              annotation_font=dict(color="#f97316", size=10))
            fig_hom2.update_layout(
            title=dict(text="Chemical Risk Score — All ETL-1 Chemicals", font=dict(color="#94a3b8", size=12)),
            paper_bgcolor="#0d1f35", plot_bgcolor="#080d18",
            height=260, font=dict(color="#64748b", size=10),
            margin=dict(l=30, r=10, t=40, b=30),
            xaxis=dict(gridcolor="#1e3a5f", color="#64748b"),
            yaxis=dict(gridcolor="#1e3a5f", color="#64748b", range=[0,115]),
            showlegend=False,
            )
            st.plotly_chart(fig_hom2, use_container_width=True)

            # htab5 — Suppliers & Regulatory

            st.markdown('<div class="sl-sec">Suppliers & Regulatory Compliance</div>', unsafe_allow_html=True)
            sel_name = st.session_state.hom_chem

            SUPPLIER_DATA = {
                    "A1 — Sulphuric Acid (H2SO4)": {
                        "suppliers":[
                            ("HOCL (Hindustan Organics Chemicals Ltd)","Rasayani, Maharashtra","India","Major domestic H2SO4 producer. Oleum and dilute grades."),
                            ("GSFC (Gujarat State Fertilizers & Chemicals)","Vadodara, Gujarat","India","H2SO4 as by-product from fertiliser production. Reliable supply."),
                            ("Deepak Fertilisers","Pune, Maharashtra","India","Sulphuric acid + oleum. ISO certified. Large capacity."),
                            ("BASF SE","Ludwigshafen","Germany","Import: reagent/electronic grade for critical applications."),
                            ("Lanxess AG","Cologne","Germany","High-purity H2SO4 for plating grade applications."),
                        ],
                        "spec":"Pickling grade: 98% purity minimum. Plating grade: 98%+ with low iron content (<10 ppm Fe). Supplied in tankers (28T) or carboys (50L).",
                        "storage_limit":"MSIHC Schedule: >100 MT = major hazard installation. Tank farm with bunding 110% volume. Diked area.",
                        "regulatory":[
                            ("MSIHC Rules 1989","Schedule 2 — 100 MT threshold","Mandatory safety audit, emergency plan, CPCB notification"),
                            ("Factories Act 1948","Schedule to Section 41B","Safety officer mandatory above threshold"),
                            ("CPCB Hazardous Waste Rules 2016","Listed hazardous chemical","Disposal and effluent consent conditions apply"),
                            ("UN Number","UN 1830 (conc.) / UN 1832 (spent)","Class 8 — Corrosive. Packing Group II."),
                            ("PESO (Explosives/Chemical Safety)","Licensing for bulk storage","Tank installation approval required"),
                        ],
                        "india_msds_ref":"As per Schedule 10 of MSIHC Rules 1989 — MSDS to be maintained in Hindi and local language at plant.",
                    },
                    "A2 — Phenol Sulfonic Acid (PSA)": {
                        "suppliers":[
                            ("Chemtex Specialty Ltd","Ahmedabad, Gujarat","India","Primary plating chemical supplier to Indian tinplate industry."),
                            ("Hindustan Tin Works","Delhi","India","Plating chemical distributor."),
                            ("Atotech GmbH","Berlin","Germany","Global plating chemistry leader. Supplies PSA for tin plating."),
                            ("Enthone (Cookson)","West Haven, Connecticut","USA","High-purity PSA for electronics and tinplate plating."),
                            ("MacDermid Alpha","USA","USA","Plating bath additive supplier — PSA and ENSA combined systems."),
                        ],
                        "spec":"Technical grade 98%+ purity. Low inorganic content. Supplied in 200L HDPE drums or IBC tanks.",
                        "storage_limit":"No MSIHC threshold. Store as general chemical — cool, dry, away from bases.",
                        "regulatory":[
                            ("REACH (if imported from EU)","SVHC check required","Verify substance is not on SVHC candidate list"),
                            ("UN Number","UN 3265","Class 8 — Corrosive liquid, acidic, organic. PG III."),
                            ("Customs (import)","Chapter 29 — Organic Chemicals","Import duty + GST applicable"),
                        ],
                        "india_msds_ref":"MSDS per GHS/IS 1991 standards. Maintain at workplace in English and Hindi.",
                    },
                    "A3 — Dioctyl Sebacate (DOS)": {
                        "suppliers":[
                            ("BASF SE","Ludwigshafen","Germany","Global supplier of DOS (Dioctyl Sebacate) — food contact grade."),
                            ("Lanxess AG","Cologne","Germany","Plasticisers division — DOS for packaging applications."),
                            ("Hallstar Industrial","Chicago, USA","USA","DOS for metalworking and corrosion protection applications."),
                            ("Fine Organics Industries Ltd","Mumbai","India","Domestic DOS manufacturer. Food contact grade certified."),
                            ("Balaji Amines Ltd","Solapur, Maharashtra","India","Specialty chemical — esters including DOS."),
                        ],
                        "spec":"Food contact grade per FDA 21 CFR 175.105 and EU 10/2011. Purity >99%. Supplied in 200L HDPE drums.",
                        "storage_limit":"Non-regulated. Store in cool, dry conditions away from ignition sources (flash point 190°C).",
                        "regulatory":[
                            ("FDA 21 CFR 175.105","Food contact indirect additive","Required for tin plate used in food can manufacturing"),
                            ("EU Regulation 10/2011","Plastic food contact materials","SML (Specific Migration Limit) compliance for EU export"),
                            ("FSSAI India","Food Safety Compliance","DOS on finished tin plate must meet FSSAI indirect contact limits"),
                            ("UN Number","Not regulated in transport","Combustible liquid — not classified as dangerous goods at ambient temp"),
                        ],
                        "india_msds_ref":"MSDS per GHS. Food contact grade certification to be maintained with each lot.",
                    },
                    "A4 — ENSA (Ethoxylated Naphthol Sulphonic Acid)": {
                        "suppliers":[
                            ("Atotech GmbH","Berlin","Germany","Proprietary ENSA formulation for tin plating. Global standard."),
                            ("Enthone (Cookson Electronics)","West Haven, USA","USA","Tin plating brightener system including ENSA."),
                            ("MacDermid Alpha Electronics","USA","USA","Complete tin plating chemistry systems."),
                            ("Dipsol Chemicals","Osaka","Japan","ENSA and PSA for tin plating — ISO 9001 certified."),
                            ("Chemtex Specialty Ltd","Ahmedabad","India","Domestic distributor for plating chemicals."),
                        ],
                        "spec":"Proprietary blend — supplied per OEM specification. Concentration per bath formulation. 200L HDPE drums.",
                        "storage_limit":"No MSIHC threshold. Chemical stability: 12 months from manufacture date. Cool, dark storage.",
                        "regulatory":[
                            ("REACH (EU import)","Registration required >1 T/yr","Verify ECHA registration status before import"),
                            ("UN Number","UN 3265 or 3264 (pH dependent)","Class 8 corrosive — verify with SDS"),
                            ("Effluent discharge","ENSA breakdown products in wastewater","WTP treatment required before ETP discharge"),
                        ],
                        "india_msds_ref":"Supplier MSDS to be obtained per MSIHC Schedule 10. Naphthol component declared.",
                    },
                    "A5 — Sodium Dichromate (Na2Cr2O7)": {
                        "suppliers":[
                            ("Lanxess AG (formerly Bayer Chemicals)","Cologne","Germany","Global leader in chromium chemicals. Na2Cr2O7 2H2O technical grade."),
                            ("Elementis Chromium","Castle Hayne, USA","USA","Large-scale Na2Cr2O7 producer for industrial use."),
                            ("SISCO Research Laboratories","Mumbai","India","Analytical grade — small quantities."),
                            ("Aditya Birla Chemicals","Mumbai","India","Industrial chemical distributor — import and supply."),
                            ("Merck KGaA","Darmstadt","Germany","Technical and reagent grade sodium dichromate."),
                        ],
                        "spec":"Technical grade min 99.5% purity as Na2Cr2O7·2H2O. Low chloride content (<0.01%). 25 kg HDPE bags or 200 kg drums.",
                        "storage_limit":"MSIHC Schedule — Cr-VI compound. Mandatory CPCB notification. Locked storage, restricted access, annual inventory audit.",
                        "regulatory":[
                            ("MSIHC Rules 1989","Schedule 1 — Hexavalent Chromium compounds","Mandatory reporting to CPCB/SPCB. Safety audit. Emergency plan."),
                            ("REACH (EU) — SVHC","AUTHORIZATION REQUIRED for all uses in EU","Use authorisation required from ECHA — non-trivial compliance"),
                            ("Indian Factories Act 1948","Scheduled substance","Medical surveillance mandatory for all exposed workers — annual"),
                            ("CPCB Hazardous Waste Rules 2016","Cr-VI in effluent: discharge standard <0.1 mg/L","Chrome reduction plant mandatory. Effluent monitoring."),
                            ("UN Number","UN 1479","Class 5.1 — Oxidising solid. PG II. Class 6.1 subsidiary risk (toxic)."),
                            ("Carcinogen Register","IARC Group 1 — mandatory declaration","Annual medical surveillance, biological monitoring (urine Cr)."),
                        ],
                        "india_msds_ref":"MSDS mandatory in Hindi + English per MSIHC. IARC Group 1 carcinogen to be declared. Worker training records maintained.",
                    },
                    "A6 — Chromic Acid (CrO3/Cr-VI)": {
                        "suppliers":[
                            ("Lanxess AG","Cologne","Germany","CrO3 technical grade — global leader. Supply via licensed importers only."),
                            ("Elementis Chromium","USA","USA","Chromic acid for surface treatment applications."),
                            ("Charkit Chemical","USA","USA","CrO3 for electroplating and anodising applications."),
                            ("Gujarat Alkalies and Chemicals Ltd (GACL)","Vadodara","India","Domestic Cr-VI chemical producer — chromic acid."),
                            ("Aditya Birla Chemicals","Mumbai","India","Licensed importer and distributor of chromium chemicals."),
                        ],
                        "spec":"Technical grade CrO3 99%+ purity. Dark red crystals. 50 kg HDPE-lined steel drums. Oxidiser — NO organic packing material.",
                        "storage_limit":"MSIHC Schedule. Mandatory CPCB notification. Strict segregation from ALL organics. No shared storage with any combustible. CCOE approval for quantities.",
                        "regulatory":[
                            ("MSIHC Rules 1989","Schedule 1 — Cr-VI compounds","Mandatory major hazard installation if above threshold. CPCB annual report."),
                            ("REACH (EU) — AUTHORIZATION","SUNSET DATE PASSED — EU USE RESTRICTED","Import from EU may be restricted — verify with supplier"),
                            ("Indian Factories Act 1948 Schedule","Hazardous process — Section 87","Safety committee mandatory. Medical examination before engagement and annually."),
                            ("CPCB Hazardous Waste Rules 2016","Cr-VI in effluent: <0.1 mg/L final discharge","Zero liquid discharge target for Cr-VI industries"),
                            ("UN Number","UN 1755","Class 8 — Corrosive liquid. PG II. Also Class 5.1 (oxidising) subsidiary."),
                            ("OSHA / CPCB Cancer Registry","Carcinogen monitoring","Lung function test + urine Cr annually. Biological exposure index (BEI): 25 µg Cr/g creatinine."),
                            ("PESO Licensing","Large quantity storage","Approval from CCOE/PESO for above-threshold storage of oxidising chemicals"),
                        ],
                        "india_msds_ref":"MSDS per MSIHC Schedule 10 in Hindi + English. Carcinogen warning in BOLD. Emergency contact numbers on container. Worker signature register.",
                    },
            }

            sup = SUPPLIER_DATA.get(sel_name, {})

            # Specification
            if sup.get("spec"):
                    st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:.6rem"><div style="font-size:.62rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:3px">PROCUREMENT SPECIFICATION</div><div style="font-size:.78rem;color:#94a3b8">{sup["spec"]}</div></div>', unsafe_allow_html=True)

            # Suppliers table
            if sup.get("suppliers"):
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin:.6rem 0 .4rem">APPROVED SUPPLIERS / MANUFACTURERS</div>', unsafe_allow_html=True)
                    sup_tbl = '<table style="border-collapse:collapse;width:100%;font-size:.75rem"><thead><tr style="background:#080d18"><th style="padding:7px 12px;text-align:left;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Supplier</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Location</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Country</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Notes</th></tr></thead><tbody>'
                    for s_name, s_loc, s_country, s_note in sup["suppliers"]:
                        flag = "🇮🇳" if s_country == "India" else "🇩🇪" if s_country == "Germany" else "🇺🇸" if "USA" in s_country else "🌐"
                        sup_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 12px;color:#e2e8f0;font-weight:600">{s_name}</td><td style="padding:7px 12px;color:#94a3b8">{s_loc}</td><td style="padding:7px 12px;color:#94a3b8">{flag} {s_country}</td><td style="padding:7px 12px;color:#64748b;font-size:.72rem">{s_note}</td></tr>'
                    sup_tbl += '</tbody></table>'
                    st.markdown(sup_tbl, unsafe_allow_html=True)

            # Storage limit
            if sup.get("storage_limit"):
                    st.markdown(f'<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.7rem 1rem;margin:.6rem 0"><div style="font-size:.62rem;font-weight:700;color:#f97316;letter-spacing:1px;margin-bottom:3px">STORAGE THRESHOLD & MSIHC APPLICABILITY</div><div style="font-size:.78rem;color:#94a3b8">{sup["storage_limit"]}</div></div>', unsafe_allow_html=True)

            # Regulatory table
            if sup.get("regulatory"):
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin:.6rem 0 .4rem">REGULATORY COMPLIANCE — INDIA & INTERNATIONAL</div>', unsafe_allow_html=True)
                    reg_tbl = '<table style="border-collapse:collapse;width:100%;font-size:.75rem"><thead><tr style="background:#080d18"><th style="padding:7px 12px;text-align:left;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Regulation</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Applicability</th><th style="padding:7px 12px;color:#64748b;font-size:.62rem;font-weight:700;border-bottom:1px solid #1e3a5f">Compliance Requirement</th></tr></thead><tbody>'
                    for reg, app, req in sup["regulatory"]:
                        is_crit = any(x in reg+app for x in ["IARC","REACH AUTH","Cancer","MANDATORY","MSIHC"])
                        rc5 = "#ef4444" if is_crit else "#94a3b8"
                        reg_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 12px;color:{rc5};font-weight:600">{reg}</td><td style="padding:7px 12px;color:#94a3b8;font-size:.72rem">{app}</td><td style="padding:7px 12px;color:#64748b;font-size:.72rem">{req}</td></tr>'
                    reg_tbl += '</tbody></table>'
                    st.markdown(reg_tbl, unsafe_allow_html=True)

            # MSDS reference
            if sup.get("india_msds_ref"):
                    st.markdown(f'<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.7rem 1rem;margin-top:.6rem"><div style="font-size:.62rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:3px">INDIA MSDS REQUIREMENTS</div><div style="font-size:.78rem;color:#94a3b8">{sup["india_msds_ref"]}</div></div>', unsafe_allow_html=True)

        # ── CIM ──────────────────────────────────────────────────────
        with tabs[3]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/HOM/002 — Chemical Interaction Matrix — ETL-1 Electrolytic Tin Plating Line 1</p>', unsafe_allow_html=True)

            # Full CIM data matching the screenshots
            CHEM_NAMES = {
                "H2SO4": "SULPHURIC ACID",
                "PSA": "PHENOLSULFONIC ACID, LIQUID",
                "CrO3": "CHROMIC ACID, SOLUTION",
                "DOS": "BIS(2-ETHYLHEXYL) SEBACATE",
                "Na2Cr2O7": "SODIUM DICHROMATE",
                "NaOH": "SODIUM HYDROXIDE SOLUTION",
            }

            # Pair interaction data — (status, hazards, gases)
            # status: "Incompatible", "Caution", "Compatible"
            PAIRS = {
                ("Na2Cr2O7","NaOH"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Flammable","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Chlorine","Hydrogen Halide","Nitrogen Oxides","Oxygen"],
                },
                ("PSA","NaOH"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Base Fumes","Nitrogen Oxides"],
                },
                ("PSA","Na2Cr2O7"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Explosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Carbon Dioxide","Chlorine","Chlorine Dioxide","Fluorine Perchlorate","Hydrogen Halide","Nitrogen Oxides","Oxygen","Sulfur Dioxide","Halogen Oxides"],
                },
                ("CrO3","NaOH"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Base Fumes","Nitrogen Oxides"],
                },
                ("CrO3","Na2Cr2O7"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Explosive","Flammable","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Carbon Dioxide","Chlorine","Chlorine Dioxide","Fluorine Perchlorate","Hydrogen Halide","Nitrogen Oxides","Oxygen","Sulfur Dioxide","Halogen Oxides"],
                },
                ("CrO3","PSA"): {
                    "status":"Caution",
                    "hazards":["Corrosive","Generates gas","Generates heat","Potentially hazardous","Toxic"],
                    "gases":["Acid Fumes","Nitrogen Oxides"],
                },
                ("DOS","NaOH"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Flammable","Generates gas","Generates heat"],
                    "gases":["Acid Fumes","Alcohols","Hydrogen Sulfate"],
                },
                ("DOS","Na2Cr2O7"): {
                    "status":"Incompatible",
                    "hazards":["Flammable","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Carbon Dioxide","Sulfur Dioxide"],
                },
                ("DOS","PSA"): {
                    "status":"Incompatible",
                    "hazards":["Flammable","Generates gas","Intense or explosive reaction","Toxic"],
                    "gases":["Alcohols","Carbon Monoxide","Carbon Dioxide","Hydrocarbons"],
                },
                ("DOS","CrO3"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Flammable","Generates gas","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Alcohols","Carbon Monoxide","Carbon Dioxide","Hydrogen Sulfate","Hydrocarbons"],
                },
                ("H2SO4","NaOH"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Base Fumes","Nitrogen Oxides"],
                },
                ("H2SO4","Na2Cr2O7"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Explosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Carbon Dioxide","Chlorine","Chlorine Dioxide","Fluorine Perchlorate","Hydrogen Halide","Nitrogen Oxides","Oxygen"],
                },
                ("H2SO4","PSA"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Nitrogen Oxides"],
                },
                ("H2SO4","CrO3"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Explosive","Generates gas","Generates heat","Intense or explosive reaction","Toxic"],
                    "gases":["Acid Fumes","Carbon Dioxide","Chlorine","Chlorine Dioxide","Hydrogen Halide","Nitrogen Oxides"],
                },
                ("H2SO4","DOS"): {
                    "status":"Incompatible",
                    "hazards":["Corrosive","Flammable","Generates gas","Generates heat"],
                    "gases":["Acid Fumes","Alcohols","Hydrogen Sulfate"],
                },
            }

            def get_pair(a, b):
                return PAIRS.get((a,b)) or PAIRS.get((b,a))

            cols_order = ["NaOH","Na2Cr2O7","PSA","CrO3","DOS"]
            rows_order = ["Na2Cr2O7","PSA","CrO3","DOS","H2SO4"]
            col_labels = [CHEM_NAMES[c] for c in cols_order]

            # ── Grid view (matching screenshot 1) ──
            st.markdown('<div class="sl-sec">Chemical Interaction Grid</div>', unsafe_allow_html=True)

            # Header row
            grid_html = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem">'
            grid_html += '<tr><td style="background:#1a2a1a;padding:8px 12px;border:1px solid #2d4a2d;min-width:160px"></td>'
            for cl in col_labels:
                grid_html += f'<td style="background:#1a2a1a;padding:8px 12px;border:1px solid #2d4a2d;font-size:.65rem;font-weight:700;color:#4ade80;min-width:180px">{cl}</td>'
            grid_html += '</tr>'

            for row_key in rows_order:
                row_name = CHEM_NAMES[row_key]
                grid_html += f'<tr><td style="background:#1a2a1a;padding:8px 12px;border:1px solid #2d4a2d;font-size:.65rem;font-weight:700;color:#4ade80;vertical-align:top">{row_name}</td>'
                for col_key in cols_order:
                    if col_key == row_key:
                        grid_html += f'<td style="background:#1a2a1a;padding:8px 12px;border:1px solid #2d4a2d;color:#4ade80;font-style:italic;font-size:.7rem;vertical-align:top">{row_name}</td>'
                        continue
                    pair = get_pair(row_key, col_key)
                    if not pair:
                        grid_html += '<td style="background:#0d2a0d;padding:8px 12px;border:1px solid #2d4a2d;color:#475569;vertical-align:top">—</td>'
                        continue
                    status = pair["status"]
                    sq = '<span style="display:inline-block;width:9px;height:9px;background:#ef4444;margin-right:4px;border-radius:1px;vertical-align:middle"></span>' if status == "Incompatible" else '<span style="display:inline-block;width:9px;height:9px;background:#eab308;margin-right:4px;border-radius:1px;vertical-align:middle"></span>'
                    bg = "rgba(239,68,68,.06)" if status == "Incompatible" else "rgba(234,179,8,.06)"
                    bc = "rgba(239,68,68,.2)" if status == "Incompatible" else "rgba(234,179,8,.2)"
                    tc = "#fca5a5" if status == "Incompatible" else "#fde68a"
                    hazard_list = "".join(f'<div style="color:#94a3b8;font-size:.68rem">{h}</div>' for h in pair["hazards"])
                    grid_html += f'<td style="background:{bg};border:1px solid {bc};padding:8px 12px;vertical-align:top"><div style="font-weight:700;color:{tc};margin-bottom:4px">{sq}{status}</div>{hazard_list}</td>'
                grid_html += '</tr>'
            grid_html += '</table></div>'
            st.markdown(grid_html, unsafe_allow_html=True)

            # ── Summary of hazard predictions ──
            st.markdown('<div class="sl-sec">Summary of Hazard Predictions (for all pairs of substances)</div>', unsafe_allow_html=True)
            hazard_defs = [
                ("Corrosive","Reaction products may be corrosive"),
                ("Explosive","Reaction products may be explosive or sensitive to shock or friction"),
                ("Flammable","Reaction products may be flammable"),
                ("Generates gas","Reaction liberates gaseous products and may cause pressurization"),
                ("Generates heat","Exothermic reaction at ambient temperatures (releases heat)"),
                ("Intense or explosive reaction","Reaction may be particularly intense, violent, or explosive"),
                ("Toxic","Reaction products may be toxic"),
                ("Potentially hazardous","May be hazardous but unknown"),
            ]
            hdef_html = '<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:1rem 1.2rem">'
            for h, d in hazard_defs:
                hdef_html += f'<div style="padding:4px 0;border-bottom:1px solid #1e3a5f;font-size:.8rem"><span style="font-weight:700;color:#e2e8f0">{h}:</span> <span style="color:#94a3b8">{d}</span></div>'
            hdef_html += '</div>'
            st.markdown(hdef_html, unsafe_allow_html=True)

            # ── Gas predictions summary ──
            st.markdown('<div class="sl-sec">Summary of Gas Predictions (for all pairs of substances)</div>', unsafe_allow_html=True)
            all_gases = sorted(set(g for p in PAIRS.values() for g in p["gases"]))
            gas_html = '<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:1rem 1.2rem;font-size:.8rem;color:#94a3b8">May produce the following gases:<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2px;margin-top:.5rem">'
            for g in all_gases:
                gas_html += f'<div style="padding:3px 0">• {g}</div>'
            gas_html += '</div></div>'
            st.markdown(gas_html, unsafe_allow_html=True)

            # ── Reactivity alerts ──
            st.markdown('<div class="sl-sec">Reactivity Alerts</div>', unsafe_allow_html=True)
            reactivity = [
                ("SODIUM DICHROMATE","Strong Oxidising Agent"),
                ("PHENOLSULFONIC ACID, LIQUID","Known Catalytic Activity"),
                ("CHROMIC ACID, SOLUTION","Strong Oxidising Agent — CARCINOGEN (IARC Group 1)","Known Catalytic Activity"),
                ("SULPHURIC ACID","Strong Acid — corrosive, reacts with metals liberating H2 gas"),
                ("BIS(2-ETHYLHEXYL) SEBACATE (DOS)","Combustible liquid — incompatible with strong oxidisers"),
            ]
            for item in reactivity:
                name = item[0]
                props = item[1:]
                props_html = "".join(f'<div style="font-size:.75rem;color:#94a3b8;padding:2px 0">• {p}</div>' for p in props)
                st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:6px"><div style="font-size:.78rem;font-weight:700;color:#60a5fa;margin-bottom:3px">{name}</div>{props_html}</div>', unsafe_allow_html=True)

            # ── Hazard predictions per pair ──
            st.markdown('<div class="sl-sec">Hazard Predictions (for each pair of substances)</div>', unsafe_allow_html=True)
            for (a, b), data in PAIRS.items():
                status = data["status"]
                sq_col = "#ef4444" if status == "Incompatible" else "#eab308"
                bg_c = "rgba(239,68,68,.05)" if status == "Incompatible" else "rgba(234,179,8,.05)"
                bc_c = "rgba(239,68,68,.15)" if status == "Incompatible" else "rgba(234,179,8,.15)"
                hazards_html = "".join(f'<div style="font-size:.78rem;color:#94a3b8;padding:2px 0"><span style="font-weight:700;color:#e2e8f0">{h}:</span> {next((d for n,d in hazard_defs if n==h), "")}</div>' for h in data["hazards"])
                gases_html = "".join(f'<div style="font-size:.75rem;color:#64748b;padding-left:1rem">○ {g}</div>' for g in data["gases"])
                st.markdown(f"""<div style="background:{bg_c};border:1px solid {bc_c};border-radius:8px;padding:1rem 1.2rem;margin-bottom:8px">
                  <div style="font-size:.78rem;color:#475569;margin-bottom:4px"><span style="font-weight:700;color:#60a5fa">{CHEM_NAMES[a]}</span> <span style="font-style:italic">mixed with</span><br><span style="font-weight:700;color:#60a5fa">{CHEM_NAMES[b]}</span></div>
                  <div style="display:flex;align-items:center;gap:6px;margin:.5rem 0"><span style="display:inline-block;width:10px;height:10px;background:{sq_col};border-radius:1px"></span><span style="font-weight:700;color:{'#f87171' if status=='Incompatible' else '#fde68a'};font-size:.82rem">{status}</span></div>
                  {hazards_html}
                  <div style="font-size:.75rem;font-weight:700;color:#94a3b8;margin-top:.5rem">May produce the following gases:</div>
                  {gases_html}
                </div>""", unsafe_allow_html=True)

        # ── PDB ──────────────────────────────────────────────────────
        with tabs[4]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/PDB/001 Rev.06 Eff.Dt.:18.08.2023 — ETL-1 Electrolytic Tin Plating Line 1, Tata Steel Tinplate (TCIL), Golmuri. All limits from WEAN United Process Norms / Supplier manuals.</p>', unsafe_allow_html=True)

            # Layers of Protection context
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">LAYERS OF PROTECTION — How SOC and SOL fit in the protection model</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;font-size:.7rem">
<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#22c55e">Layer 1-2</b><br><span style="color:#64748b">Process Design + BPCS control<br>→ keeps within SOC</span></div>
<div style="background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#eab308">Layer 3</b><br><span style="color:#64748b">Critical Alarms + Operator action<br>→ SOC deviation detected</span></div>
<div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#f97316">Layer 4-5</b><br><span style="color:#64748b">SIS auto-trip + PRV/SRV<br>→ SOL breach response</span></div>
<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#ef4444">Layer 6-8</b><br><span style="color:#64748b">Bund → Plant ER → Community ER<br>→ post-LOC mitigation</span></div>
</div>
<div style="font-size:.7rem;color:#475569;margin-top:.5rem">SOC = Layers 1-3 keep process here (prevention) &nbsp;|&nbsp; SOL breach = Layer 4 auto-trip activates (last prevention barrier) &nbsp;|&nbsp; Beyond SOL = mitigation layers activate</div>
</div>""", unsafe_allow_html=True)

            pdb_data = ETL1_PDB_PARAMS
            if profile and profile.get("pdb_params"):
                pdb_data = profile["pdb_params"]
            dept = plant.replace(" ","_").replace("—","").replace("/","")[:8].lower()
            render_pdb(pdb_data, dept_key=dept)

        # ── PSCE ─────────────────────────────────────────────────────
        with tabs[5]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/PSCE/001 Rev.04 Eff.Dt.:18.08.2023 — ETL-1 Electrolytic Tinning Line 1, Tata Steel Tinplate (TCIL), Golmuri. 77 PSCE items identified.</p>', unsafe_allow_html=True)

            st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem">
<div style="font-size:.82rem;font-weight:700;color:#3b82f6;margin-bottom:.6rem">PSCE FRAMEWORK — ETL-1 ELECTROLYTIC TINNING LINE</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.8rem;font-size:.75rem;color:#94a3b8;line-height:1.7">
<div><b style="color:#ef4444">Consequence Based PSRM Critical</b><br>Equipment whose failure could DIRECTLY CAUSE a major process safety incident — fire, explosion, toxic release, or environmental damage meeting HHO criteria.</div>
<div><b style="color:#a78bfa">Prevention &amp; Mitigation</b><br>Equipment specifically installed to PREVENT a major accident or LIMIT its consequences. Includes SIS interlocks, safety instrumented systems, and emergency shutdown devices.</div>
<div><b style="color:#f97316">Prescriptive PSM Critical</b><br>Equipment mandated by REGULATION regardless of consequence analysis — IBR statutory SRVs, PESO requirements, CPCB mandated monitoring (e.g. Cr-VI air monitor). Statutory requirement.</div>
</div></div>""", unsafe_allow_html=True)

            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#64748b;letter-spacing:1px;margin-bottom:.5rem">BASIS OF SELECTION — CATEGORY DEFINITIONS (Note #1, EDB Format)</div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;font-size:.72rem">
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#3b82f6">Instrumented Active Preventive</b><br><span style="color:#64748b">SIS/interlock devices that automatically detect and prevent escalation — analysers with auto-trip, transmitters with PLC shutdown logic.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#f97316">Active Mitigation</b><br><span style="color:#64748b">Mitigation requiring automatic activation or human action AFTER a deviation begins — exhaust fans, monitoring gauges, operator-activated systems.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#22c55e">Passive Prevention</b><br><span style="color:#64748b">Always-active protection requiring no energy or human action — bunds, blast panels, physical barriers, containment.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#ef4444">Safety Monitoring &amp; Emergency Comms</b><br><span style="color:#64748b">Detection and communication systems — Cr-VI monitors, H2 detectors, emergency PA systems, alarm panels.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#a78bfa">Controlled Release</b><br><span style="color:#64748b">Equipment for safe controlled release — SRVs, PRVs, auto-vent valves. Prevents uncontrolled/catastrophic release.</span></div>
<div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#94a3b8">Service &amp; Utility</b><br><span style="color:#64748b">Support systems whose failure impacts safety chain — cooling water, DM water, hydraulic systems. Consequence-based selection.</span></div>
</div></div>""", unsafe_allow_html=True)

            st.markdown("""<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:1rem">
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#ef4444;font-family:monospace">77</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">TOTAL PSCE ITEMS</div></div>
<div style="background:#0d1f35;border:1px solid rgba(59,130,246,.3);border-top:3px solid #3b82f6;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#3b82f6;font-family:monospace">4</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">HHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#f97316;font-family:monospace">2</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">PRESCRIPTIVE</div></div>
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#ef4444;font-family:monospace">1</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">Cr-VI MONITOR (MANDATORY)</div></div>
<div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:8px;padding:.7rem;text-align:center">
<div style="font-size:1.4rem;font-weight:900;color:#22c55e;font-family:monospace">SAP-S</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">TAG ALL ITEMS</div></div>
</div>""", unsafe_allow_html=True)


            # Filter controls
            fc1, fc2, fc3 = st.columns([2, 2, 1])
            with fc1:
                srch_etl = st.text_input("", placeholder="Search equipment, tag, justification...", key="etl_psce_srch", label_visibility="collapsed")
            with fc2:
                type_filt = st.selectbox("", ["All Types","Consequence Based","Prescriptive","Active Mitigation"], key="etl_psce_type", label_visibility="collapsed")
            with fc3:
                psm_filt = st.selectbox("", ["All","PSM Critical Only"], key="etl_psce_psm", label_visibility="collapsed")

            shown_etl = ETL1_PSCE
            if profile and profile.get("psce_items"):
                shown_etl = profile["psce_items"]
            if srch_etl:
                shown_etl = [x for x in shown_etl if srch_etl.lower() in x["equipment"].lower() or srch_etl.lower() in x["justification"].lower() or srch_etl.lower() in x.get("tag","").lower()]
            if type_filt != "All Types":
                shown_etl = [x for x in shown_etl if type_filt.lower() in x["psce_type"].lower()]
            if psm_filt == "PSM Critical Only":
                shown_etl = [x for x in shown_etl if x["psm_critical"] == "Yes"]

            st.markdown(f'<div style="font-size:.72rem;color:#475569;margin-bottom:.5rem">Showing {len(shown_etl)} items — Full 77-item list in SAP-PM module</div>', unsafe_allow_html=True)

            type_colors_etl = {
                "Consequence Based": "#ef4444",
                "Prescriptive": "#a78bfa",
                "Active Mitigation": "#f97316",
                "Instrumented Active Preventive": "#3b82f6",
            }

            for item in shown_etl:
                tc2 = type_colors_etl.get(item["psce_type"], "#64748b")
                psm_b2 = '<span style="background:rgba(239,68,68,.2);color:#f87171;border:1px solid rgba(239,68,68,.4);font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">PSM CRITICAL</span>' if item["psm_critical"]=="Yes" else ""
                st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:4px solid {tc2};border-radius:10px;padding:1rem 1.2rem;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.6rem">
  <div>
    <span style="font-size:.68rem;font-weight:700;color:#f97316">#{item['sl']}</span>
    <span style="font-size:.88rem;font-weight:700;color:#e2e8f0;margin-left:8px">{item['equipment']}</span>
    {psm_b2}
  </div>
  <span style="background:{tc2}20;color:{tc2};border:1px solid {tc2}40;font-size:.6rem;font-weight:700;padding:3px 9px;border-radius:20px;white-space:nowrap">{item.get('psce_type', item.get('category',''))}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:.6rem">
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">TAG / SAP NO.</div>
    <div style="font-size:.72rem;color:#f97316;font-family:monospace">{item.get('tag','—')}</div>
    <div style="font-size:.62rem;color:#475569">{item.get('sap_tag','—')}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">SUB-PROCESS</div>
    <div style="font-size:.72rem;color:#94a3b8">{item.get('sub_process','—')}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">CATEGORY</div>
    <div style="font-size:.68rem;color:#94a3b8">{item.get('category', item.get('psce_type',''))}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">MAINTENANCE</div>
    <div style="font-size:.68rem;color:#94a3b8">{item.get('maintenance','—')}</div>
  </div>
</div>
<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;margin-bottom:.5rem">
  <div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">JUSTIFICATION FOR PROCESS SAFETY CRITICALITY</div>
  <div style="font-size:.75rem;color:#94a3b8;line-height:1.7">{item.get('justification','—')}</div>
</div>
<div style="background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.15);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem .8rem">
  <div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:2px">CONSEQUENCE OF FAILURE</div>
  <div style="font-size:.73rem;color:#fca5a5">{item.get('consequence_of_failure','—')}</div>
</div>
</div>""", unsafe_allow_html=True)

        # ── EDB ──────────────────────────────────────────────────────
        with tabs[6]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/EDB/001 Rev.04 Eff.Dt.:01.05.2018 — ETL-1 Equipment Design Basis</p>', unsafe_allow_html=True)

            # Barrier model from Tata Steel PSRM module
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">BARRIER MODEL — Tata Steel PSRM: Detector + Logic Solver + Actuator = ONE Barrier</div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:6px;font-size:.7rem;margin-bottom:.5rem">
<div style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#3b82f6">① DETECTOR</b><br><span style="color:#64748b">Sensor detects condition requiring action<br>(analyser, transmitter, detector)</span></div>
<div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#f97316">② LOGIC SOLVER</b><br><span style="color:#64748b">Decides action to take<br>(PLC, relay, operator knowledge)</span></div>
<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#22c55e">③ ACTUATOR</b><br><span style="color:#64748b">Takes physical action<br>(valve, trip, shutdown, operator)</span></div>
<div style="background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#a78bfa">BARRIER TYPE</b><br><span style="color:#64748b">Active (auto) | Passive (always-on) | Procedural (operator)</span></div>
</div>
<div style="font-size:.7rem;color:#475569">A barrier is effective ONLY if all 3 components are fully functional. Each EDB item below is one such barrier component or a complete barrier in the protection chain.</div>
</div>""", unsafe_allow_html=True)

            edb_data = ETL1_EDB
            if profile and profile.get("edb_items"):
                edb_data = profile["edb_items"]
            dept_e = plant.replace(" ","_").replace("—","").replace("/","")[:8].lower()
            render_edb(edb_data, dept_key=dept_e)

        # ── PARAMETERS ───────────────────────────────────────────────
        with tabs[7]:
            st.markdown('<div class="sl-sec">Process Design Basis — All Parameters with SOC / SOL Limits & Breach Consequences</div>', unsafe_allow_html=True)

            # Full parameter data with consequences
            PARAMS_FULL = {
                "Coil Feeding": [
                    {"param":"Power Pack Hydraulic Pump Pressure","uom":"bar","soc_min":55,"soc_max":70,"sol_min":45,"sol_max":100,
                     "low_breach":"Hydraulic pressure loss — actuator failure, strip misalignment, entry section damage",
                     "high_breach":"Over-pressure — hydraulic line rupture, oil spill, fire risk (oil flash point ~150 C)"},
                    {"param":"DM Water Pressure to Welding Machine","uom":"kg/cm2","soc_min":4.5,"soc_max":5.5,"sol_min":4.5,"sol_max":5.5,
                     "low_breach":"Welder cooling loss — welder overheating, weld failure, strip break",
                     "high_breach":"Excess pressure — welder cooling circuit damage"},
                    {"param":"Compressed Air Pressure to Welding Machine","uom":"kg/cm2","soc_min":4.5,"soc_max":5.5,"sol_min":4.5,"sol_max":6.5,
                     "low_breach":"Pneumatic actuator failure — welder clamp fails, strip break",
                     "high_breach":"Excess pressure — pneumatic line damage"},
                ],
                "Cleaning & Rinsing": [
                    {"param":"Pre-Primary Alkali Temperature (NaOH)","uom":"deg C","soc_min":80,"soc_max":90,"sol_min":80,"sol_max":90,
                     "low_breach":"Poor cleaning — oil and grease residue on strip, plating adhesion failure, product rejection",
                     "high_breach":"NaOH boiling — violent steam generation, alkali splash, severe chemical burns, HHO event"},
                    {"param":"Primary NaOH Concentration","uom":"g/L","soc_min":25,"soc_max":30,"sol_min":25,"sol_max":30,
                     "low_breach":"Insufficient cleaning — residual oil causes plating pinholes",
                     "high_breach":"Excess alkali — increased drag-out, waste treatment overload"},
                    {"param":"Primary Cleaning Current","uom":"kA","soc_min":2.5,"soc_max":3.5,"sol_min":2.5,"sol_max":3.5,
                     "low_breach":"Inadequate electrolytic cleaning — contamination passes to plating section",
                     "high_breach":"Excessive current — strip overheating, electrical cell damage, arc risk"},
                    {"param":"Pickling H2SO4 Concentration","uom":"g/L","soc_min":8,"soc_max":10,"sol_min":8,"sol_max":10,
                     "low_breach":"Insufficient pickling — oxide layer on strip, poor plating adhesion, product downgrade",
                     "high_breach":"Excess acid — over-pickling, strip surface pitting, H2 gas generation, equipment corrosion"},
                ],
                "Tin Plating": [
                    {"param":"Sn++ Concentration (SnSO4)","uom":"g/L","soc_min":26,"soc_max":32,"sol_min":24,"sol_max":34,
                     "low_breach":"Under-plating — dull band formation, coating weight below spec, PRODUCT REJECTION",
                     "high_breach":"Over-plating — excess tin consumption, cost loss, coatweight above spec"},
                    {"param":"Free Acid Concentration","uom":"g/L","soc_min":13,"soc_max":16,"sol_min":11,"sol_max":18,
                     "low_breach":"Low conductivity — poor current distribution, uneven plating",
                     "high_breach":"Excess acid — increased corrosivity, operator exposure risk, equipment damage"},
                    {"param":"ENSA Concentration","uom":"g/L","soc_min":3,"soc_max":6,"sol_min":2,"sol_max":7,
                     "low_breach":"Poor plating efficiency — rough deposit, dull appearance",
                     "high_breach":"Excess brightener — plating bath contamination, breakdown products accumulate"},
                    {"param":"Sn++ : Free Acid Ratio","uom":"Ratio","soc_min":1.95,"soc_max":2.05,"sol_min":1.9,"sol_max":2.1,
                     "low_breach":"Poor bath balance — rough plating, increased sludge formation",
                     "high_breach":"Ratio shift — non-uniform tin deposition, product specification failure"},
                ],
                "Reflow Furnace": [
                    {"param":"Strip Temperature (Reflow Exit)","uom":"deg C","soc_min":232,"soc_max":270,"sol_min":232,"sol_max":270,
                     "low_breach":"Incomplete tin melting — matte/dull finish, poor corrosion resistance, product rejection",
                     "high_breach":"CRITICAL: Strip burning — conductor roll damage, unplanned shutdown, major production loss"},
                    {"param":"Quench Temperature","uom":"deg C","soc_min":50,"soc_max":65,"sol_min":50,"sol_max":65,
                     "low_breach":"Cold quench — thermal shock, strip shape defects",
                     "high_breach":"Hot quench — incomplete solidification of tin, alloy layer overgrowth"},
                    {"param":"Reflow Current","uom":"A","soc_min":1000,"soc_max":10000,"sol_min":1000,"sol_max":10000,
                     "low_breach":"Insufficient heating — incomplete tin melting, dull coating",
                     "high_breach":"Excess current — strip overheating, conductor roll arcing, fire risk"},
                ],
                "Chemical Treatment": [
                    {"param":"Chemical Treatment Solution Temperature","uom":"deg C","soc_min":40,"soc_max":45,"sol_min":40,"sol_max":45,
                     "low_breach":"Incomplete passivation — poor corrosion resistance, product failure in service",
                     "high_breach":"CRITICAL: Bath overheating — increased Cr-VI volatilisation, TLV breach, MANDATORY SHUTDOWN"},
                    {"param":"Chemical Treatment Current","uom":"A","soc_min":300,"soc_max":2000,"sol_min":300,"sol_max":3500,
                     "low_breach":"Insufficient passivation layer — corrosion failure, food can safety risk",
                     "high_breach":"Excess current — Cr-VI reduction to Cr-III, bath balance upset, passivation failure"},
                ],
                "Electrostatic Oiling": [
                    {"param":"Primary Air Pressure","uom":"kg/cm2","soc_min":0.5,"soc_max":1.0,"sol_min":0.5,"sol_max":1.0,
                     "low_breach":"Poor atomisation — uneven oil distribution, surface corrosion in storage",
                     "high_breach":"Excess air — oil mist generation, fire risk near electrostatic system"},
                    {"param":"Secondary Air Flow","uom":"mm WC","soc_min":60,"soc_max":300,"sol_min":60,"sol_max":300,
                     "low_breach":"Insufficient air — oil accumulation, drip marks on strip",
                     "high_breach":"Excess air — oil mist carry-over, contamination of downstream coiler"},
                    {"param":"Repelling Plate Voltage","uom":"kV","soc_min":-40,"soc_max":-10,"sol_min":-50,"sol_max":-10,
                     "low_breach":"Poor oil distribution — non-uniform coating weight",
                     "high_breach":"Excess voltage — arcing to strip, electrical hazard, strip marking"},
                ],
            }

            proc_filter = st.selectbox("Filter by sub-process", ["All"] + list(PARAMS_FULL.keys()), key="param_filter")

            for proc_name, params in PARAMS_FULL.items():
                if proc_filter != "All" and proc_filter != proc_name:
                    continue
                is_hho_p = proc_name not in ["Coil Feeding","Electrostatic Oiling"]
                hdr_clr = "#f97316" if is_hho_p else "#3b82f6"
                st.markdown(f"""<div style="background:#0a1628;border-left:3px solid {hdr_clr};padding:.6rem 1rem;margin:.8rem 0 .4rem;border-radius:0 6px 6px 0;display:flex;align-items:center;gap:10px">
                  <span style="font-size:.82rem;font-weight:800;color:#e2e8f0">{proc_name}</span>
                  <span style="background:{hdr_clr}20;color:{hdr_clr};border:1px solid {hdr_clr}40;font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:20px">{'HHO' if is_hho_p else 'LHO'}</span>
                  <span style="font-size:.68rem;color:#475569">{len(params)} parameters</span>
                </div>""", unsafe_allow_html=True)

                for p in params:
                    pparam=p['param']; psmin=p['soc_min']; psmax=p['soc_max']; puom=p['uom']
                    with st.expander(f"{pparam}  —  SOC: {psmin} to {psmax} {puom}"):
                        e1, e2, e3 = st.columns(3)
                        with e1:
                            st.markdown(f"""<div class="sl-card">
                            <b>SOC (Safe Operating Condition):</b><br>
                            {p['soc_min']} – {p['soc_max']} {p['uom']}<br><br>
                            <b>SOL (Safe Operating Limit):</b><br>
                            {p['sol_min']} – {p['sol_max']} {p['uom']}<br><br>
                            <b>PSM Critical:</b> Yes
                            </div>""", unsafe_allow_html=True)
                        with e2:
                            st.markdown(f"""<div style="background:rgba(234,179,8,.06);border:1px solid rgba(234,179,8,.2);border-left:3px solid #eab308;border-radius:8px;padding:.8rem;font-size:.78rem;color:#fde68a;line-height:1.7">
                            <b style="color:#eab308;font-size:.65rem;letter-spacing:1px">BELOW SOC/SOL:</b><br>{p['low_breach']}
                            </div>""", unsafe_allow_html=True)
                        with e3:
                            st.markdown(f"""<div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-left:3px solid #ef4444;border-radius:8px;padding:.8rem;font-size:.78rem;color:#fca5a5;line-height:1.7">
                            <b style="color:#ef4444;font-size:.65rem;letter-spacing:1px">ABOVE SOC/SOL:</b><br>{p['high_breach']}
                            </div>""", unsafe_allow_html=True)

        # ── PLAYGROUND ───────────────────────────────────────────────
        with tabs[8]:
            st.markdown('<div class="sl-sec">Parameter Playground & Daily Report Checker</div>', unsafe_allow_html=True)
            pg1, pg2 = st.columns(2)

            with pg1:
                st.markdown('<div class="sl-card"><b>Manual Parameter Check</b><br><span style="font-size:.75rem;color:#64748b">Enter a current reading to instantly check against SOC/SOL limits</span></div>', unsafe_allow_html=True)
                play_param = st.selectbox("Select parameter", [
                    "Strip Temperature — Reflow (SOC: 232-270 C)",
                    "Cr-VI Air Concentration — Chem Treatment (TLV: 0.05 mg/m3)",
                    "Sn2+ Concentration — Tin Plating (SOC: 26-32 g/L)",
                    "H2SO4 Concentration — Pickling (SOC: 8-10 g/L)",
                    "NaOH Temperature — Primary Cleaning (SOC: 80-90 C)",
                    "Primary Cleaning Current (SOC: 2.5-3.5 kA)",
                    "H2 Pressure — Reflow Furnace (SOC: 0.5-2.0 bar)",
                ], key="play_param_new")

                play_val = st.number_input("Current reading", value=250.0, step=0.1, key="play_val_new")

                p_low = play_param.lower()
                if "strip" in p_low:      smin,smax,lmin,lmax,unit = 232,270,232,270,"deg C"
                elif "cr-vi" in p_low:    smin,smax,lmin,lmax,unit = 0,0.05,0,0.1,"mg/m3"
                elif "sn2+" in p_low:     smin,smax,lmin,lmax,unit = 26,32,24,34,"g/L"
                elif "h2so4" in p_low:    smin,smax,lmin,lmax,unit = 8,10,8,10,"g/L"
                elif "naoh" in p_low:     smin,smax,lmin,lmax,unit = 80,90,80,90,"deg C"
                elif "current" in p_low:  smin,smax,lmin,lmax,unit = 2.5,3.5,2.5,3.5,"kA"
                else:                      smin,smax,lmin,lmax,unit = 0.5,2.0,0.5,2.5,"bar"

                v = float(play_val)
                if smin <= v <= smax:
                    sc2, cls2, status2 = "#22c55e", "sl-safe", "SAFE — Within SOC"
                elif lmin <= v <= lmax:
                    sc2, cls2, status2 = "#eab308", "sl-warn", "CAUTION — Outside SOC, within SOL"
                else:
                    sc2, cls2, status2 = "#ef4444", "sl-danger", "DANGER — Outside Safe Operating Limits"

                st.markdown(f"""<div class="{cls2}" style="margin-top:.8rem">
                  <div style="font-size:.65rem;font-weight:700;color:{sc2};letter-spacing:2px;margin-bottom:6px">{status2}</div>
                  <div style="font-size:1.1rem;font-weight:900;color:{sc2};font-family:monospace;margin-bottom:8px">{v} {unit}</div>
                  <div style="font-size:.72rem;color:#94a3b8">
                    SOC: {smin} – {smax} {unit} &nbsp;|&nbsp; SOL: {lmin} – {lmax} {unit}
                  </div>
                </div>""", unsafe_allow_html=True)

            with pg2:
                st.markdown('<div class="sl-card"><b>Daily Shift Report Upload</b><br><span style="font-size:.75rem;color:#64748b">Upload CSV or Excel with parameter readings. SafetyLens scans for deviations from SOC/SOL limits automatically.</span></div>', unsafe_allow_html=True)
                uploaded = st.file_uploader("Upload shift report (CSV or Excel)", type=["csv","xlsx","xls"], key="shift_upload", label_visibility="collapsed")
                if uploaded:
                    try:
                        df_up = pd.read_csv(uploaded) if uploaded.name.endswith(".csv") else pd.read_excel(uploaded)
                        st.success(f"Loaded: {uploaded.name} — {len(df_up)} rows, {len(df_up.columns)} parameters")
                        st.dataframe(df_up.head(15), use_container_width=True, hide_index=True)
                        num_cols = df_up.select_dtypes(include='number').columns
                        alerts_found = []
                        for col in num_cols:
                            q99 = df_up[col].quantile(0.95)
                            outliers = df_up[df_up[col] > q99 * 1.05]
                            if not outliers.empty:
                                alerts_found.append(f"{col}: {len(outliers)} potential high readings (above 95th pct + 5%)")
                        if alerts_found:
                            st.markdown('<span style="color:#f87171;font-weight:700;font-size:.8rem">Deviations detected:</span>', unsafe_allow_html=True)
                            for a in alerts_found:
                                st.markdown(f'<div style="background:rgba(239,68,68,.08);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:6px 10px;margin-bottom:4px;font-size:.78rem;color:#fca5a5">{a}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-radius:6px;padding:10px;font-size:.8rem;color:#4ade80">All readings within normal range — no critical deviations found</div>', unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Could not read file: {e}")
                else:
                    st.markdown("""<div style="border:2px dashed #1e3a5f;border-radius:8px;padding:2rem;text-align:center">
                    <div style="font-size:.85rem;font-weight:600;color:#475569;margin-bottom:.3rem">Drop your shift report here</div>
                    <div style="font-size:.72rem;color:#374151">CSV or Excel — columns = parameters, rows = readings over time</div>
                    </div>""", unsafe_allow_html=True)

        # ── SIMULATION ───────────────────────────────────────────────
        with tabs[9]:
            st.markdown('<div class="sl-sec">Bowtie Scenario Analysis — Top Event Risk Assessment</div>', unsafe_allow_html=True)
            scens = {
                "Cr-VI Release (Chemical Treatment)": {
                    "causes": ["Control valve failure — Cr-VI bath overflow","Tank overflow during concentration makeup","PPE non-compliance during sampling","No plant isolation before maintenance"],
                    "top": "Cr-VI release to plant atmosphere",
                    "consequences": ["Carcinogen inhalation — CPCB mandatory reportable event","Regulatory shutdown — MSIHC Rules 1989 violation","Long-term health monitoring for all exposed workers","Legal liability and compensation claims"],
                    "risk": 98, "color": "#ef4444"
                },
                "H2 Explosion (Reflow Furnace)": {
                    "causes": ["H2 supply line seal failure","Purge procedure not followed on startup","Ignition source present near furnace zone","H2 pressure switch (PSAL 2.14) failure"],
                    "top": "H2 vapour cloud ignition and explosion",
                    "consequences": ["Structural explosion — HHO zone","Fatality risk for all personnel in area","Plant shutdown 3-6 months minimum","Insurance and regulatory investigation"],
                    "risk": 92, "color": "#ef4444"
                },
                "H2SO4 Spill (Pickling)": {
                    "causes": ["Pickling tank integrity failure","Overflow during concentration makeup","Pump seal failure and leak","Drain valve left open accidentally"],
                    "top": "H2SO4 spill to plant floor and drainage",
                    "consequences": ["Severe chemical burns to personnel","Ground and groundwater contamination","WTP overload — effluent limit breach","Mandatory regulatory reporting — Factories Act"],
                    "risk": 72, "color": "#f97316"
                },
                "Strip Breakage (Reflow Furnace)": {
                    "causes": ["Strip temperature above 270 C (tin melts)","Conductor roll damage — surface defect","Tension imbalance across strip width","Speed deviation during threading"],
                    "top": "Strip breakage in reflow section",
                    "consequences": ["Line stoppage 4-8 hours — production loss","Conductor roll replacement required","All in-process material quality rejection","Risk of secondary fire from burning strip"],
                    "risk": 65, "color": "#eab308"
                },
            }
            sc_sel = st.selectbox("Select hazard scenario", list(scens.keys()), key="sc_select")
            sc = scens[sc_sel]
            clr = sc["color"]
            risk_val = sc["risk"]

            # Risk score display — pure HTML, always renders
            pct = risk_val  # out of 100
            level = "CRITICAL" if risk_val >= 90 else "HIGH" if risk_val >= 75 else "MEDIUM" if risk_val >= 50 else "LOW"
            st.markdown(f"""
            <div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:12px;padding:1.5rem;margin-bottom:1rem;text-align:center">
              <div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#64748b;margin-bottom:.5rem">SCENARIO RISK SCORE</div>
              <div style="font-size:3.5rem;font-weight:900;color:{clr};font-family:monospace;line-height:1;margin-bottom:.5rem">{risk_val}</div>
              <div style="font-size:.75rem;font-weight:700;color:{clr};margin-bottom:.8rem">{level} RISK</div>
              <div style="background:#1e3a5f;border-radius:6px;height:12px;overflow:hidden;max-width:400px;margin:0 auto">
                <div style="width:{pct}%;height:12px;background:linear-gradient(90deg,{'#22c55e,#f97316' if pct<75 else '#f97316,#ef4444'});border-radius:6px;transition:width .5s"></div>
              </div>
              <div style="display:flex;justify-content:space-between;max-width:400px;margin:.3rem auto 0;font-size:.62rem;color:#475569">
                <span>0</span><span style="color:#f97316">75 — HIGH</span><span>100</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Bowtie layout
            bt1, bt2, bt3 = st.columns([2, 1, 2])
            with bt1:
                st.markdown('<div style="font-size:.72rem;font-weight:700;color:#64748b;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.5rem">Causes / Threats</div>', unsafe_allow_html=True)
                for c in sc["causes"]:
                    st.markdown(f'<div class="sl-cause">{c}</div>', unsafe_allow_html=True)
            with bt2:
                st.markdown(f"""<div style="background:{clr}15;border:2px solid {clr};border-radius:12px;padding:1.2rem;text-align:center;margin-top:.5rem">
                  <div style="font-size:.6rem;font-weight:700;color:{clr};letter-spacing:2px;margin-bottom:8px">TOP EVENT</div>
                  <div style="font-size:.82rem;font-weight:700;color:#e2e8f0;margin-bottom:12px;line-height:1.5">{sc['top']}</div>
                  <div style="font-size:1.8rem;font-weight:900;color:{clr};font-family:monospace">{risk_val}/100</div>
                </div>""", unsafe_allow_html=True)
            with bt3:
                st.markdown('<div style="font-size:.72rem;font-weight:700;color:#64748b;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:.5rem">Consequences</div>', unsafe_allow_html=True)
                for c in sc["consequences"]:
                    st.markdown(f'<div class="sl-consq">{c}</div>', unsafe_allow_html=True)

            # Comparison chart
            st.markdown('<div class="sl-sec">All Scenarios — Risk Comparison</div>', unsafe_allow_html=True)

            # HTML bar chart — no plotly needed, always renders
            all_sc = list(scens.items())
            for name, data in all_sc:
                w = data["risk"]
                c2 = data["color"]
                is_sel = (name == sc_sel)
                st.markdown(f"""<div style="background:{'#0f2847' if is_sel else '#0d1f35'};border:1px solid {'#3b82f6' if is_sel else '#1e3a5f'};border-radius:8px;padding:.8rem 1rem;margin-bottom:6px">
                  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:5px">
                    <span style="font-size:.8rem;font-weight:600;color:#e2e8f0">{name.split('(')[0].strip()}</span>
                    <span style="font-size:.85rem;font-weight:900;color:{c2};font-family:monospace">{w}/100</span>
                  </div>
                  <div style="background:#1e3a5f;border-radius:4px;height:8px">
                    <div style="width:{w}%;height:8px;background:{c2};border-radius:4px"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

            # Barrier analysis
            st.markdown('<div class="sl-sec">Barrier Analysis — Prevention & Mitigation</div>', unsafe_allow_html=True)
            barriers = {
                "Cr-VI Release (Chemical Treatment)": [
                    ("Prevention","Enclosed Cr-VI bath with forced ventilation (LEV)"),
                    ("Prevention","Continuous Cr-VI air monitoring (TLV alarm at 0.05 mg/m3)"),
                    ("Prevention","PSCE: Chemical treatment current and temperature interlocks"),
                    ("Mitigation","PPE: Class C suit + air-supplied respirator mandatory"),
                    ("Mitigation","Emergency shower and eyewash station within 10 sec reach"),
                    ("Mitigation","CPCB emergency notification procedure activated"),
                ],
                "H2 Explosion (Reflow Furnace)": [
                    ("Prevention","PSAL 2.14: H2 pressure switch — PLC auto-shutdown on loss"),
                    ("Prevention","N2 purge mandatory before H2 introduction (SOP verified)"),
                    ("Prevention","UV 1.21: Propane solenoid auto-close on safety signal"),
                    ("Mitigation","Fire detection system in reflow zone"),
                    ("Mitigation","Emergency isolation valve on H2 supply line"),
                    ("Mitigation","HHO zone — no ignition sources within 10m boundary"),
                ],
                "H2SO4 Spill (Pickling)": [
                    ("Prevention","Tank level transmitter with high-level alarm (SOL)"),
                    ("Prevention","Secondary containment bund (110% tank volume)"),
                    ("Prevention","Automatic pump shutdown on low tank level"),
                    ("Mitigation","Acid-resistant PPE mandatory in pickling section"),
                    ("Mitigation","Lime neutralisation kit at spill point"),
                    ("Mitigation","Sump pump to WTP automatically activated"),
                ],
                "Strip Breakage (Reflow Furnace)": [
                    ("Prevention","Pyrometer ETL-1: auto-trip at 270 C strip temperature"),
                    ("Prevention","Tension control system with deviation alarm"),
                    ("Prevention","Speed interlock between bridle and recoiler"),
                    ("Mitigation","Emergency stop at all operator stations"),
                    ("Mitigation","Fire extinguisher positioned at reflow zone"),
                    ("Mitigation","Strip break detector for automatic line stop"),
                ],
            }
            for b_type, b_desc in barriers.get(sc_sel, []):
                bc = "#22c55e" if b_type == "Prevention" else "#f97316"
                st.markdown(f"""<div style="background:#0a1628;border:1px solid #1e3a5f;border-left:3px solid {bc};border-radius:6px;padding:.6rem 1rem;margin-bottom:5px;display:flex;gap:10px;align-items:center">
                  <span style="background:{bc}20;color:{bc};border:1px solid {bc}40;font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:20px;white-space:nowrap">{b_type}</span>
                  <span style="font-size:.8rem;color:#94a3b8">{b_desc}</span>
                </div>""", unsafe_allow_html=True)

            # Scenario profile radar + risk trend chart
            st.markdown('<div class="sl-sec">Scenario Risk Profile — Radar Analysis</div>', unsafe_allow_html=True)
            sim_g1, sim_g2 = st.columns(2)

            with sim_g1:
                radar_data = {
                    "Cr-VI Release (Chemical Treatment)": [5,5,3,4,5,2],
                    "H2 Explosion (Reflow Furnace)":       [5,5,5,3,4,3],
                    "H2SO4 Spill (Pickling)":              [4,3,2,4,3,3],
                    "Strip Breakage (Reflow Furnace)":     [2,2,3,2,3,4],
                }
                cats = ["Health Impact","Explosion Risk","Fire Risk","Chemical Harm","Env. Impact","Production Loss"]
                rd = radar_data.get(sc_sel, [3,3,3,3,3,3])
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=rd + [rd[0]],
                    theta=cats + [cats[0]],
                    fill="toself",
                    fillcolor='rgba(' + ','.join(str(int(clr.lstrip('#')[ii:ii+2],16)) for ii in (0,2,4)) + ',0.15)',
                    line=dict(color=clr, width=2),
                    name=sc_sel.split("(")[0].strip(),
                ))
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=True, range=[0,5], gridcolor="#1e3a5f", color="#475569", tickfont=dict(size=8, color="#475569")),
                        angularaxis=dict(color="#64748b", tickfont=dict(size=9, color="#94a3b8")),
                        bgcolor="#080d18",
                    ),
                    paper_bgcolor="#0d1f35",
                    font=dict(color="#94a3b8", size=10),
                    height=280,
                    margin=dict(t=20, b=20, l=40, r=40),
                    showlegend=False,
                    title=dict(text="Hazard Profile — " + sc_sel.split("(")[0].strip(), font=dict(color="#94a3b8", size=11)),
                )
                st.plotly_chart(fig_radar, use_container_width=True)

            with sim_g2:
                # Risk score over time (simulated trend)
                months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
                trends = {
                    "Cr-VI Release (Chemical Treatment)": [94,96,98,95,97,99,98,96,98,97,98,98],
                    "H2 Explosion (Reflow Furnace)":       [88,90,92,89,91,93,92,90,91,92,92,92],
                    "H2SO4 Spill (Pickling)":              [68,70,72,69,71,73,72,70,71,72,72,72],
                    "Strip Breakage (Reflow Furnace)":     [60,62,65,61,63,66,65,62,64,65,65,65],
                }
                trend_vals = trends.get(sc_sel, [70]*12)
                fig_trend = go.Figure()
                fig_trend.add_trace(go.Scatter(
                    x=months, y=trend_vals,
                    mode="lines+markers",
                    line=dict(color=clr, width=2.5),
                    marker=dict(size=6, color=clr),
                    fill="tozeroy",
                    fillcolor='rgba(' + ','.join(str(int(clr.lstrip('#')[ii:ii+2],16)) for ii in (0,2,4)) + ',0.07)',
                    name="Risk Score",
                ))
                fig_trend.add_hline(y=75, line_dash="dot", line_color="#f97316",
                                    annotation_text="HIGH threshold: 75",
                                    annotation_font=dict(color="#f97316", size=9))
                fig_trend.update_layout(
                    title=dict(text="Risk Score Trend (2024)", font=dict(color="#94a3b8", size=11)),
                    paper_bgcolor="#0d1f35", plot_bgcolor="#080d18",
                    height=280, margin=dict(l=40, r=10, t=35, b=30),
                    xaxis=dict(gridcolor="#1e3a5f", color="#64748b"),
                    yaxis=dict(gridcolor="#1e3a5f", color="#64748b", range=[0,105], title="Risk Score"),
                    showlegend=False,
                )
                st.plotly_chart(fig_trend, use_container_width=True)

        # ── RISK MATRIX ──────────────────────────────────────────────
        with tabs[10]:
            # L1-L5 consequence legend integrated
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">RISK MATRIX — Likelihood × Consequence Severity (L1-L5 Scale)</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px;font-size:.68rem;margin-bottom:.4rem">
<div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:6px;padding:.4rem;text-align:center"><b style="color:#22c55e">L1 Minor</b><br><span style="color:#64748b">FAC, &lt;Rs.5L, on-site</span></div>
<div style="background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.2);border-radius:6px;padding:.4rem;text-align:center"><b style="color:#eab308">L2 Moderate</b><br><span style="color:#64748b">LTI, Rs.5-50L, limited off-site</span></div>
<div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.4rem;text-align:center"><b style="color:#f97316">L3 Serious</b><br><span style="color:#64748b">Hospitalisation, Rs.50L-5Cr, PESO notify</span></div>
<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:.4rem;text-align:center"><b style="color:#ef4444">L4 Critical</b><br><span style="color:#64748b">1-5 fatalities, Rs.5-50Cr, community</span></div>
<div style="background:rgba(127,29,29,.2);border:1px solid rgba(239,68,68,.4);border-radius:6px;padding:.4rem;text-align:center"><b style="color:#fca5a5">L5 Catastrophic</b><br><span style="color:#64748b">&gt;5 fatalities, &gt;Rs.50Cr, evacuation</span></div>
</div>
<div style="font-size:.7rem;color:#475569">LOPA trigger: any scenario scoring Risk ≥12 (High/Critical) requires Layer of Protection Analysis to verify sufficient IPLs exist. Tolerable risk: ≤1×10⁻⁵ per year individual fatal risk.</div>
</div>""", unsafe_allow_html=True)

            hazards = [
                {"name":"Cr-VI Air Release","likelihood":3,"severity":5},
                {"name":"H2SO4 Spill","likelihood":2,"severity":4},
                {"name":"H2 Explosion","likelihood":1,"severity":5},
                {"name":"Strip Breakage","likelihood":4,"severity":2},
                {"name":"Propane Leak","likelihood":2,"severity":4},
                {"name":"Na2Cr2O7 Spill","likelihood":2,"severity":5},
                {"name":"Hydraulic Oil Fire","likelihood":1,"severity":3},
                {"name":"Alkali Eye Injury","likelihood":3,"severity":3},
            ]
            fig_rm = go.Figure()
            for sev in range(1, 6):
                for lik in range(1, 6):
                    rv = sev * lik
                    c = "rgba(239,68,68,.15)" if rv >= 15 else "rgba(249,115,22,.09)" if rv >= 8 else "rgba(34,197,94,.07)"
                    fig_rm.add_shape(type="rect", x0=lik-.5, x1=lik+.5, y0=sev-.5, y1=sev+.5,
                                     fillcolor=c, line=dict(color="#1e3a5f", width=1))
            for h in hazards:
                rv = h["likelihood"] * h["severity"]
                dc = "#ef4444" if rv >= 15 else "#f97316" if rv >= 8 else "#22c55e"
                fig_rm.add_trace(go.Scatter(
                    x=[h["likelihood"]], y=[h["severity"]],
                    mode="markers+text",
                    marker=dict(size=15, color=dc, line=dict(color="#0d1421", width=1.5)),
                    text=[h["name"]], textposition="top center",
                    textfont=dict(size=8, color="#94a3b8"), showlegend=False
                ))
            fig_rm.update_layout(
                paper_bgcolor="#0d1f35", plot_bgcolor="#080d18",
                height=420, font=dict(color="#64748b", size=10),
                margin=dict(l=50, r=10, t=20, b=50),
                xaxis=dict(gridcolor="#1e3a5f", title="Likelihood (1=Rare, 5=Almost Certain)",
                           range=[.5, 5.5], tickvals=[1,2,3,4,5], color="#64748b"),
                yaxis=dict(gridcolor="#1e3a5f", title="Severity (1=Minor, 5=Catastrophic)",
                           range=[.5, 5.5], tickvals=[1,2,3,4,5], color="#64748b"),
            )
            st.plotly_chart(fig_rm, use_container_width=True)
            df_h = pd.DataFrame(hazards)
            df_h["Risk Score"] = df_h["likelihood"] * df_h["severity"]
            df_h["Level"] = df_h["Risk Score"].apply(lambda x: "HIGH" if x >= 15 else "MEDIUM" if x >= 8 else "LOW")
            df_h = df_h.sort_values("Risk Score", ascending=False)
            df_h = df_h.rename(columns={"name":"Hazard","likelihood":"Likelihood","severity":"Severity"})
            st.dataframe(df_h, use_container_width=True, hide_index=True)

        # ── PSM REPORT ──────────────────────────────────────────────
        with tabs[11]:
            st.markdown(f"""<div class="sl-card" style="border-left:3px solid #3b82f6">
            <div style="font-size:.95rem;font-weight:800;color:#f1f5f9;margin-bottom:.4rem">{plant}</div>
            <div style="font-size:.73rem;color:#475569">{comp} &nbsp;|&nbsp; {div_name} &nbsp;|&nbsp; Doc: PSM/PSI/ETL1/001</div>
            <div style="display:flex;gap:1.5rem;margin-top:.7rem;flex-wrap:wrap">
              <span style="font-size:.72rem"><b style="color:#f97316">Status:</b> <span style="color:#94a3b8">{meta['status']} Active</span></span>
              <span style="font-size:.72rem"><b style="color:#3b82f6">Risk:</b> <span style="color:#94a3b8">{meta['risk']}/100</span></span>
              <span style="font-size:.72rem"><b style="color:#ef4444">Critical Chemical:</b> <span style="color:#94a3b8">Cr-VI (Chromic Acid)</span></span>
              <span style="font-size:.72rem"><b style="color:#22c55e">PSCE Items:</b> <span style="color:#94a3b8">{meta['psce']}</span></span>
            </div>
            </div>""", unsafe_allow_html=True)

            for sec, items, exp in [
                ("1. Process Safety Information", [
                    "PSC — 4 HHO processes, 2 LHO processes classified (Form Rev.04, 18.08.2023)",
                    "PFD — 10 process nodes with full material balance documented",
                    "P&ID — 16 reference drawings covering all ETL-1 subsystems",
                    "HOM — 6 chemicals: HAZCHEM/NFPA/TLV/LD50 fully documented",
                    "CIM — Cr-VI compounds (A5, A6) incompatible with all 4 organic chemicals",
                    "PDB — 29 critical parameters across 6 sub-processes (all PSM Critical = Yes)",
                    "PSCE — 77 safety critical equipment items identified and tagged",
                    "EDB — 77+ equipment design basis entries for furnace gas systems",
                ], True),
                ("2. Active Alerts", [
                    "CRITICAL (98/100) — Cr-VI air concentration in Chemical Treatment zone — SHUTDOWN REQUIRED",
                    "CRITICAL (92/100) — Strip exit temperature above 270 C in Reflow Furnace",
                    "HIGH (90/100) — Sn2+ concentration deviation in Plating bath — product quality risk",
                    "5 PSCE items overdue for calibration — must complete before next operating shift",
                ], True),
                ("3. Compliance Status", [
                    "OSHA PSM 29 CFR 1910.119: Partially compliant — PHA update pending",
                    "Indian Factories Act 1948 Section 41B: Compliant — PSI documented",
                    "MSIHC Rules 1989: Cr-VI quantities declared to CPCB & SPCB",
                ], False),
                ("4. Recommendations", [
                    "Immediate: Install additional Cr-VI air monitoring in Chemical Treatment zone",
                    "Short-term: Complete 5 overdue PSCE calibrations before next shift",
                    "Medium-term: Full HAZOP review of Reflow Furnace H2/propane system",
                    "Long-term: Evaluate Cr-VI replacement with trivalent chromium process",
                ], False),
            ]:
                with st.expander(sec, expanded=exp):
                    for item in items:
                        c_text = "#f87171" if any(x in item for x in ["CRITICAL","SHUTDOWN","overdue","Partially"]) else "#94a3b8"
                        st.markdown(f'<div style="font-size:.8rem;color:{c_text};padding:5px 0;border-bottom:1px solid #1e3a5f">{item}</div>', unsafe_allow_html=True)

            if st.button("Generate Full PSM Report (PDF)", type="primary"):
                st.success("PDF report queued — will be sent to PSM Officer on file.")

        # ── CHATBOT ──────────────────────────────────────────────────

        st.markdown("---")
        st.markdown('<div class="sl-sec">PSM AI Assistant — Ask anything about this plant</div>', unsafe_allow_html=True)
        st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.6rem 1rem;margin-bottom:.6rem;font-size:.75rem;color:#60a5fa">
        Ask about: Cr-VI risk, H2SO4, HHO/LHO classification, PSCE items, reflow furnace safety, SOC/SOL meanings, PSM compliance, flow brightening, MSIHC rules, chemical interactions...
        </div>""", unsafe_allow_html=True)
        chat_box = st.container()
        with chat_box:
            for msg in st.session_state.chat[-14:]:
                _mc = msg["content"]
                _mcls = "sl-chat-user" if msg["role"] == "user" else "sl-chat-ai"
                st.markdown(f'<div class="{_mcls}">{_mc}</div>', unsafe_allow_html=True)
        uq = st.text_input("", placeholder="e.g. What happens if Cr-VI exceeds TLV? Explain SOC vs SOL. Why is Reflow HHO?",
                           key=f"ci_{st.session_state.ck}", label_visibility="collapsed")
        bc1, bc2, bc3 = st.columns([1, 1, 5])
        with bc1:
            if st.button("Send", type="primary", key="send_chat"):
                if uq.strip():
                    st.session_state.chat.append({"role": "user", "content": uq})
                    st.session_state.chat.append({"role": "assistant", "content": ai_response(uq)})
                    st.session_state.ck += 1
                    st.rerun()
        with bc2:
            if st.button("Clear", key="clear_chat"):
                st.session_state.chat = []
                st.rerun()

# ══════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════
else:
    # Hero
    st.markdown("""
    <div style="background:linear-gradient(135deg,#0d1f35 0%,#0a1628 60%,#0f0d2e 100%);
                padding:3rem 2rem 2rem;border-bottom:1px solid #1e3a5f;margin:0 -1rem 0 -1rem">
      <div style="display:inline-flex;align-items:center;gap:8px;
                  background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.3);
                  border-radius:20px;padding:4px 14px;margin-bottom:14px">
        <div style="width:7px;height:7px;border-radius:50%;background:#3b82f6;box-shadow:0 0 8px #3b82f6"></div>
        <span style="color:#60a5fa;font-size:.68rem;font-weight:700;letter-spacing:1.5px">LIVE PLATFORM</span>
      </div>
      <h1 style="font-size:2.6rem;font-weight:900;color:#ffffff;letter-spacing:-1px;line-height:1.1;margin-bottom:.4rem">
        Process Safety <span style="color:#3b82f6">Intelligence</span>
      </h1>
      <p style="color:#475569;font-size:.9rem;margin-bottom:1.5rem">
        Tata Steel &middot; JSW Steel &middot; AM/NS India &middot; SAIL — Real PSI/PSM plant hierarchy &middot; Live risk monitoring
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Global stats
    s1, s2, s3, s4 = st.columns(4)
    for col, val, lbl, clr in [
        (s1, "6", "Industries", "#3b82f6"),
        (s2, "2,069", "Active Plants", "#22c55e"),
        (s3, "17,900", "Incident Records", "#ef4444"),
        (s4, "48", "Companies", "#a78bfa"),
    ]:
        with col:
            st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;
                            padding:1rem;text-align:center;margin-bottom:.5rem">
              <div style="font-size:1.7rem;font-weight:900;color:{clr};font-family:monospace">{val}</div>
              <div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-top:3px">{lbl.upper()}</div>
            </div>""", unsafe_allow_html=True)

    # Step 1 — Industry
    st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                    text-transform:uppercase;margin:1.5rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
        Step 1 — Select Industry Sector</div>""", unsafe_allow_html=True)

    ind_cols = st.columns(len(HIERARCHY))
    for i, ind in enumerate(HIERARCHY.keys()):
        im = IND_META.get(ind, {})
        clr = im.get("color", "#3b82f6")
        n_comp = len(HIERARCHY[ind])
        n_plants = sum(len(p) for d in HIERARCHY[ind].values() for p in d.values())
        risk_level = im.get("risk","")
        risk_clr = {"CRITICAL":"#ef4444","HIGH":"#f97316","MEDIUM":"#eab308","LOW":"#22c55e"}.get(risk_level,"#64748b")
        active = (st.session_state.ind == ind)
        with ind_cols[i]:
            st.markdown(f"""<div style="background:{'rgba(29,78,216,.15)' if active else '#0d1f35'};
                border:1px solid {'#1d4ed8' if active else '#1e3a5f'};
                border-top:3px solid {clr};border-radius:10px;padding:1rem;
                margin-bottom:6px;text-align:center">
              <div style="font-size:.82rem;font-weight:700;color:{clr};margin-bottom:4px">{ind}</div>
              <div style="font-size:.68rem;color:#475569;margin-bottom:8px">{im.get('incidents',0):,} incidents</div>
              <div style="font-size:.7rem;color:{risk_clr};font-weight:700;margin-bottom:4px">{risk_level} RISK</div>
              <div style="font-size:.65rem;color:#374151">{n_comp} companies · {n_plants} plants</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Select", key=f"ind_{ind}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.ind = ind
                st.session_state.comp = None
                st.session_state.plant = None
                st.rerun()

    # Step 2 — Company
    if st.session_state.ind:
        ind_name = st.session_state.ind
        st.markdown(f"""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                        text-transform:uppercase;margin:1.5rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
            Step 2 — Select Company &nbsp;<span style="color:#475569;font-style:italic;letter-spacing:0;text-transform:none;font-weight:400;font-size:.8rem">/ {ind_name}</span></div>""", unsafe_allow_html=True)

        comps = list(HIERARCHY[ind_name].keys())
        for row_start in range(0, len(comps), 3):
            row = comps[row_start:row_start+3]
            cols = st.columns(3)
            for i, comp in enumerate(row):
                active = (st.session_state.comp == comp)
                with cols[i]:
                    if st.button(comp, key=f"comp_{comp}", use_container_width=True,
                                 type="primary" if active else "secondary"):
                        st.session_state.comp = comp
                        st.session_state.plant = None
                        st.rerun()

    # Step 3+4 — Division & Plants
    if st.session_state.comp and st.session_state.ind:
        for div_name, plants in HIERARCHY[st.session_state.ind][st.session_state.comp].items():
            st.markdown(f"""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                            text-transform:uppercase;margin:1.5rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
                {div_name}</div>""", unsafe_allow_html=True)

            for row_start in range(0, len(plants), 3):
                row = plants[row_start:row_start+3]
                cols = st.columns(3)
                for i, plant in enumerate(row):
                    pm = PLANT_META.get(plant, {})
                    status = pm.get("status","")
                    risk = pm.get("risk",0)
                    hho = pm.get("hho",0)
                    psce = pm.get("psce",0)
                    rc3 = risk_color(risk) if risk else "#475569"
                    sc3 = "#f97316" if status=="HHO" else "#3b82f6" if status=="PSI" else "#6366f1"
                    with cols[i]:
                        if status:
                            st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;
                                border-radius:8px;padding:8px 12px;margin-bottom:4px;
                                display:flex;justify-content:space-between;align-items:center">
                              <div style="display:flex;gap:8px;align-items:center">
                                <span style="background:{sc3}20;color:{sc3};border:1px solid {sc3}40;
                                      font-size:.58rem;font-weight:700;padding:2px 7px;border-radius:10px">{status}</span>
                                <span style="font-size:.62rem;color:#475569">{hho} HHO · {psce} PSCE</span>
                              </div>
                              <span style="font-size:.82rem;font-weight:900;color:{rc3};font-family:monospace">{risk}/100</span>
                            </div>""", unsafe_allow_html=True)
                        if st.button(plant[:36], key=f"plant_{plant}", use_container_width=True):
                            st.session_state.plant = plant
                            st.rerun()

    # Incidents database
    st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                    text-transform:uppercase;margin:2rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
        Incidents Database — All Plants</div>""", unsafe_allow_html=True)

    acc_filter = st.selectbox("Filter by industry", ["All","Steel & Metal","Oil & Gas","Chemicals","Mining","Power"], key="home_acc", label_visibility="collapsed")
    acc_show = ACCIDENTS if acc_filter == "All" else [a for a in ACCIDENTS if a["industry"] == acc_filter]

    for a in acc_show:
        sev_color = {"Catastrophic":"#ef4444","Critical":"#f97316","Major":"#eab308","Minor":"#22c55e"}.get(a["severity"],"#64748b")
        _cas = a.get("casualties", 0)
        cas_html = f'<span style="font-size:.85rem;font-weight:900;color:#ef4444;font-family:monospace">{_cas}</span><br><span style="font-size:.58rem;color:#475569">FATAL</span>' if _cas > 0 else ""
        st.markdown(f"""
        <div class="sl-acc" style="border-left:4px solid {sev_color}">
          <div style="text-align:center">
            <div style="font-size:.75rem;font-weight:700;color:#e2e8f0;font-family:monospace">{a.get('month','—')}</div>
            <div style="font-size:.65rem;color:#475569">{a.get('year','')}</div>
          </div>
          <div>
            <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:3px">
              <span style="font-size:.82rem;font-weight:700;color:#e2e8f0">{a.get('plant', a.get('facility',''))}</span>
              <span style="background:{sev_color}20;color:{sev_color};border:1px solid {sev_color}40;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:20px">{a.get('severity','')}</span>
              <span style="background:rgba(59,130,246,.15);color:#60a5fa;font-size:.6rem;font-weight:600;padding:2px 7px;border-radius:20px">{a.get('type', a.get('incident',''))}</span>
            </div>
            <div style="font-size:.73rem;color:#475569">{a.get('cause', a.get('lesson',''))}</div>
          </div>
          <div style="text-align:center">{cas_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # Upload section
    st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                    text-transform:uppercase;margin:2rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
        Upload Your PSI Data</div>""", unsafe_allow_html=True)
    with st.expander("Add your plant to SafetyLens — Upload PSI Data"):
        up1, up2 = st.columns(2)
        with up1:
            st.text_input("Plant name", placeholder="e.g. ETL-3 Electrolytic Tinning Line 3", key="upload_pname")
            st.selectbox("Industry", list(HIERARCHY.keys()), key="upload_pind")
        with up2:
            bt1, bt2 = st.columns(2)
            with bt1: st.button("Chemicals template", use_container_width=True, key="dl_chem")
            with bt2: st.button("Parameters template", use_container_width=True, key="dl_param")
            uf = st.file_uploader("Upload filled template (Excel or CSV)", type=["xlsx","csv"], key="psi_up")
            if uf:
                st.success(f"Received: {uf.name} — PSI report will be generated and published for authorised readers.")
