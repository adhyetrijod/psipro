import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from collections import Counter

st.set_page_config(
    page_title="PSIPro  |  Process Safety Intelligence  |  TCIL Golmuri",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Force dark background on ALL Streamlit versions ──
st.markdown("""
<style>
html, body, [data-testid="stApp"], .main, .block-container,
[data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #020818 !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] {
    background-color: #060d1a !important;
    border-right: 1px solid #1e3a5f !important;
    min-width: 230px !important;
    display: block !important;
    visibility: visible !important;
}
[data-testid="stSidebar"] > div:first-child {
    background-color: #060d1a !important;
    padding: 0.5rem 0.3rem !important;
}
[data-testid="stSidebarContent"] {
    background-color: #060d1a !important;
}
section[data-testid="stSidebar"] {
    display: block !important;
    transform: none !important;
}
[data-testid="collapsedControl"] { display: none !important; }
/* ── ALL BUTTONS — comprehensive Streamlit 1.50 fix ── */
.stButton > button,
button[kind="secondary"],
button[kind="primary"],
button[data-testid="baseButton-secondary"],
button[data-testid="baseButton-primary"],
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"],
.stButton button {
    background-color: #0d1f35 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important;
    font-weight: 600 !important;
}
.stButton > button:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="baseButton-secondary"]:hover {
    background-color: #1e3a5f !important;
    color: #ffffff !important;
    border-color: #3b82f6 !important;
}
/* Primary buttons (active/selected) */
.stButton > button[kind="primary"],
[data-testid="stBaseButton-primary"],
[data-testid="baseButton-primary"] {
    background-color: #1d4ed8 !important;
    color: #ffffff !important;
    border-color: #3b82f6 !important;
}
/* Disabled buttons */
.stButton > button:disabled,
[data-testid="baseButton-secondary"]:disabled {
    background-color: #0a1020 !important;
    color: #475569 !important;
    border-color: #1e3a5f !important;
}
/* ── ALL p/span/label text ── */
p, span, label, div, h1, h2, h3, h4, h5, h6 {
    color: #e2e8f0;
}
.stMarkdown p { color: #e2e8f0 !important; }
/* Selectbox / dropdown fix — white text on white bg issue */
.stTextInput input, .stTextArea textarea {
    background: #0d1f35 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important;
}
/* ── SELECTBOX / DROPDOWN — complete dark fix ── */
div[data-baseweb="select"],
div[data-baseweb="select"] > div,
div[data-baseweb="select"] > div > div {
    background-color: #0d1f35 !important;
    color: #e2e8f0 !important;
    border-color: #1e3a5f !important;
}
div[data-baseweb="select"] * { color: #e2e8f0 !important; }
div[data-baseweb="select"] svg { fill: #94a3b8 !important; }

/* Dropdown popup */
div[data-baseweb="popover"],
div[data-baseweb="popover"] * {
    background-color: #0d1f35 !important;
    color: #e2e8f0 !important;
}
ul[data-baseweb="menu"],
ul[data-baseweb="menu"] * { 
    background-color: #0d1f35 !important;
    color: #e2e8f0 !important;
}
li[role="option"],
div[role="option"],
li[data-highlighted="true"] {
    background-color: #0d1f35 !important;
    color: #e2e8f0 !important;
}
li[role="option"]:hover,
div[role="option"]:hover,
li[aria-selected="true"] {
    background-color: #1e3a5f !important;
    color: #ffffff !important;
}
/* Selectbox label */
.stSelectbox label, .stSelectbox p { color: #94a3b8 !important; }
.stSelectbox div[data-testid="stMarkdownContainer"] p { color: #94a3b8 !important; }

/* Filter/text input inside selectbox */
input[aria-autocomplete="list"] {
    background-color: #0d1f35 !important;
    color: #e2e8f0 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: #0a1628 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
}
.stTabs [aria-selected="true"] {
    color: #3b82f6 !important;
    border-bottom: 2px solid #3b82f6 !important;
}
.stExpander {
    background: #0d1f35 !important;
    border: 1px solid #1e3a5f !important;
}
</style>
""", unsafe_allow_html=True)

# Minimal CSS  -  only what Streamlit actually applies reliably
st.markdown(""" <style> /* Hide chrome */ #MainMenu, footer, header {visibility: hidden;} /* Force sidebar visible */ [data-testid="stSidebar"] { display: block !important; visibility: visible !important; min-width: 220px !important; background: #060d1a !important; border-right: 1px solid #1e3a5f !important; } [data-testid="stSidebar"] > div { background: #060d1a !important; } section[data-testid="stSidebarContent"] { background: #060d1a !important; padding: 0.5rem 0.5rem !important; } [data-testid="collapsedControl"] { display: none !important; }  /* Topbar */ .sl-topbar { background: #0a1628; padding: 12px 24px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1e3a5f; margin: -1rem -1rem 0 -1rem; } .sl-brand { font-size: 1.2rem; font-weight: 900; color: #ffffff; } .sl-brand b { color: #3b82f6; } .sl-sub { font-size: 0.6rem; color: #475569; letter-spacing: 2px; text-transform: uppercase; } .sl-pill { background: rgba(237,137,54,0.2); border: 1px solid rgba(237,137,54,0.5); color: #f6ad55; font-size: 0.72rem; font-weight: 700; padding: 5px 16px; border-radius: 20px; }  /* Ticker */ .sl-ticker { background: #080d18; padding: 8px 24px; border-bottom: 1px solid #1e3a5f; margin: 0 -1rem 1rem -1rem; display: flex; gap: 2rem; overflow-x: auto; font-size: 0.75rem; } .sl-tick-item { white-space: nowrap; color: #94a3b8; } .sl-tick-item b { color: #e2e8f0; font-family: monospace; } .sl-up { color: #22c55e; font-weight: 700; } .sl-down { color: #ef4444; font-weight: 700; }  /* Industry cards on home */ .sl-ind-card { background: #0d1f35; border: 1px solid #1e3a5f; border-radius: 12px; padding: 16px; margin-bottom: 8px; cursor: pointer; } .sl-ind-name { font-size: 0.9rem; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; } .sl-ind-desc { font-size: 0.72rem; color: #64748b; margin-bottom: 10px; } .sl-ind-stat { font-size: 0.78rem; color: #94a3b8; }  /* Metric row */ .sl-metrics { display: grid; grid-template-columns: repeat(6, 1fr); gap: 1px; background: #1e3a5f; border: 1px solid #1e3a5f; border-radius: 10px; overflow: hidden; margin-bottom: 1rem; } .sl-metric { background: #0d1f35; padding: 14px 10px; text-align: center; } .sl-metric-val { font-size: 1.6rem; font-weight: 900; font-family: 'Courier New', monospace; line-height: 1; color: #e2e8f0; } .sl-metric-lbl { font-size: 0.55rem; font-weight: 700; letter-spacing: 1.5px; color: #475569; margin-top: 4px; text-transform: uppercase; }  /* Alert cards */ .sl-alert { display: flex; align-items: flex-start; gap: 12px; background: #1a0505; border: 1px solid #7f1d1d; border-left: 4px solid #ef4444; border-radius: 8px; padding: 12px 14px; margin-bottom: 8px; } .sl-alert-score { background: #ef4444; color: white; font-size: 0.68rem; font-weight: 800; padding: 4px 8px; border-radius: 6px; font-family: monospace; white-space: nowrap; flex-shrink: 0; } .sl-alert-text { font-size: 0.82rem; color: #fca5a5; line-height: 1.5; }  /* Process card */ .sl-proc { background: #0d1f35; border: 1px solid #1e3a5f; border-radius: 10px; padding: 14px; margin-bottom: 8px; } .sl-proc.hho { border-left: 4px solid #f97316; } .sl-proc.lho { border-left: 4px solid #6366f1; } .sl-proc-title { font-size: 0.88rem; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; } .sl-proc-desc { font-size: 0.73rem; color: #64748b; line-height: 1.5; margin-bottom: 8px; } .sl-tag { display: inline-block; font-size: 0.6rem; font-weight: 700; padding: 2px 8px; border-radius: 20px; margin-right: 4px; } .sl-tag-hho { background: rgba(249,115,22,0.15); color: #f97316; border: 1px solid rgba(249,115,22,0.3); } .sl-tag-lho { background: rgba(99,102,241,0.15); color: #818cf8; border: 1px solid rgba(99,102,241,0.3); } .sl-tag-psm { background: rgba(167,139,250,0.15); color: #a78bfa; border: 1px solid rgba(167,139,250,0.3); }  /* Accident row */ .sl-acc { background: #0d1f35; border: 1px solid #1e3a5f; border-radius: 8px; padding: 12px 16px; margin-bottom: 6px; display: grid; grid-template-columns: 60px 1fr 60px; gap: 12px; align-items: center; }  /* Section header */ .sl-sec { font-size: 0.68rem; font-weight: 700; letter-spacing: 2px; color: #3b82f6; text-transform: uppercase; margin: 1.5rem 0 0.6rem 0; padding-bottom: 6px; border-bottom: 1px solid #1e3a5f; }  /* Step label */ .sl-step { font-size: 1.1rem; font-weight: 800; color: #e2e8f0; margin: 1.2rem 0 0.6rem 0; } .sl-step span { color: #64748b; font-weight: 400; font-size: 0.9rem; }  /* Info card */ .sl-card { background: #0d1f35; border: 1px solid #1e3a5f; border-radius: 10px; padding: 16px; margin-bottom: 8px; font-size: 0.82rem; color: #94a3b8; line-height: 1.8; } .sl-card b { color: #e2e8f0; }  /* Risk bar */ .sl-rbar-wrap { display: flex; align-items: center; gap: 8px; margin-top: 4px; } .sl-rbar-bg { background: #1e3a5f; border-radius: 3px; height: 6px; flex: 1; } .sl-rbar-fill { height: 6px; border-radius: 3px; }  /* CIM table */ .sl-cim { border-collapse: collapse; width: 100%; font-size: 0.75rem; } .sl-cim td, .sl-cim th { border: 1px solid #1e3a5f; padding: 7px 12px; text-align: center; } .sl-cim th { background: #080d18; color: #64748b; font-size: 0.65rem; font-weight: 700; letter-spacing: 1px; } .sl-cim .y { background: rgba(239,68,68,0.15); color: #f87171; font-weight: 700; } .sl-cim .n { background: rgba(34,197,94,0.1); color: #4ade80; } .sl-cim .x { background: #1e3a5f; color: #475569; } .sl-cim .rh { background: #080d18; color: #94a3b8; font-weight: 600; text-align: left; }  /* Status badge */ .sl-status-hho { background: rgba(249,115,22,0.15); border: 1px solid rgba(249,115,22,0.4); color: #f97316; font-size: 0.66rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; } .sl-status-psm { background: rgba(167,139,250,0.15); border: 1px solid rgba(167,139,250,0.4); color: #a78bfa; font-size: 0.66rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; }  /* Chat */ .sl-chat-user { background: #1d4ed8; color: white; padding: 9px 13px; border-radius: 12px 12px 4px 12px; font-size: 0.8rem; margin: 5px 0; max-width: 80%; margin-left: auto; display: block; } .sl-chat-ai { background: #0d1f35; border: 1px solid #1e3a5f; color: #e2e8f0; padding: 9px 13px; border-radius: 12px 12px 12px 4px; font-size: 0.8rem; margin: 5px 0; max-width: 85%; white-space: pre-wrap; line-height: 1.6; display: block; }  /* Bowtie */ .sl-cause { background: rgba(59,130,246,0.1); border: 1px solid rgba(59,130,246,0.25); border-left: 3px solid #3b82f6; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; font-size: 0.8rem; color: #93c5fd; font-weight: 500; } .sl-consq { background: rgba(239,68,68,0.08); border: 1px solid rgba(239,68,68,0.2); border-left: 3px solid #ef4444; border-radius: 6px; padding: 8px 12px; margin-bottom: 6px; font-size: 0.8rem; color: #fca5a5; font-weight: 500; }  /* Playground status */ .sl-safe { background: rgba(34,197,94,0.1); border: 2px solid #22c55e; border-radius: 10px; padding: 14px; text-align: center; } .sl-warn { background: rgba(234,179,8,0.1); border: 2px solid #eab308; border-radius: 10px; padding: 14px; text-align: center; } .sl-danger { background: rgba(239,68,68,0.1); border: 2px solid #ef4444; border-radius: 10px; padding: 14px; text-align: center; } </style> """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════════════════════

HIERARCHY = {
    "Steel & Metal": {
        "Tata Steel  -  Jamshedpur Works": {
            "Iron Making": ["Inbound Logistics","Coke Plant","By Product Plant","Haldia Met Coke Plant","Sinter Plant #1","Sinter Plant #2","Sinter Plant #3","Sinter Plant #4","Raw Material Bedding","Pellet Plant","Blast Furnace A","Blast Furnace F","Blast Furnace G","Blast Furnace H","Blast Furnace I"],
            "Long Product Area": ["LD#1 & Continuous Caster","Lime Plant","New Bar Mill","Wire and Rod Mill","Merchant Mill"],
            "Flat Product Area": ["LD#2 & Slab Caster","Hot Strip Mill","LD#3 TSCR","Cold Rolling Mill","Tubes Division"],
        },
        "Tata Steel  -  Tinplate (TCIL), Golmuri": {
            "Tinplate Operations": ["ETL-1  -  Electrolytic Tinning Line 1","ETL-2  -  Electrolytic Tinning Line 2","CRM  -  Cold Rolling Mill","TFS  -  Tin Free Steel","Galvanizing Line (GI/GA)","Colour Coated Sheet (CCS)"],
            "Utilities": ["Hydrogen Plant  -  H2 Production & Supply","Propane Yard  -  Decantation, Storage & Supply"],
        },
        "Tata Steel  -  Kalinganagar, Odisha": {
            "Kalinganagar Works": ["Raw Material Handling","Coke Plant","Sinter Plant","Blast Furnace","Steel Melting Shop","Hot Strip Mill"],
        },
        "Tata Steel  -  Meramandali, Odisha": {
            "Meramandali Works": ["Inbound Logistics","Coke Oven","Sinter Plant","Direct Reduced Iron","Blast Furnace-1","Blast Furnace-2","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill"],
        },
        "Tata Metaliks  -  Kharagpur, WB": {
            "Metaliks Works": ["Blast Furnace","Ductile Iron Pipe Plant","Coke Oven"],
        },
        "JSW Steel  -  Vijayanagar, Karnataka": {
            "Vijayanagar Works": ["Coke Oven","Sinter Plant","Blast Furnace","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill","Galvanizing Line","Color Coating Line"],
        },
        "JSW Steel  -  Dolvi, Maharashtra": {
            "Dolvi Works": ["Corex Iron Making","Electric Arc Furnace","Hot Strip Mill","Wire Rod Mill"],
        },
        "AM/NS India  -  Hazira, Gujarat": {
            "Hazira Works": ["Blast Furnace","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill","Galvanizing"],
        },
        "SAIL  -  Rourkela, Odisha": {
            "RSP Works": ["Coke Oven","Blast Furnace","Steel Melting Shop","Hot Strip Mill","Cold Rolling Mill"],
        },
        "RINL  -  Visakhapatnam (Vizag), AP": {
            "Vizag Steel Plant": ["Coke Oven Battery #1-4","Sinter Plant","Blast Furnace #1","Blast Furnace #2","Blast Furnace #3","Steel Melting Shop #1","Steel Melting Shop #2","Wire Rod Mill","Medium Merchant & Structural Mill","Special Bar Mill","Submerged Arc Furnace"],
        },
    },
    "Pharma": {
        "Sun Pharma  -  Halol, Gujarat": {"API Block": ["API Synthesis Unit","Reactor Block A","Reactor Block B","Solvent Recovery"]},
        "Dr. Reddy's  -  Hyderabad": {"Formulation": ["Tablet Manufacturing","Sterile Injectables","Packaging Line"]},
        "Cipla  -  Patalganga": {"Manufacturing": ["API Plant","Oral Solids","Liquid Formulations"]},
    },
    "Oil & Gas": {
        "HPCL  -  Vizag Refinery": {"Refinery": ["Crude Distillation Unit","FCC Unit","Hydrocracker","LPG Plant","Storage & Dispatch"]},
        "BPCL  -  Mumbai Refinery": {"Refinery": ["CDU","VDU","FCCU","Reformer","Sulphur Recovery"]},
        "IOCL  -  Mathura Refinery": {"Refinery": ["Crude Unit","Naphtha Hydrotreater","FCC Unit","Merox Unit"]},
        "ONGC  -  Mumbai High": {"Offshore": ["Production Platform","Gas Compression","Water Injection","Pipeline"]},
    },
    "Food & Beverage": {
        "ITC  -  Munger Factory": {"Processing": ["Cigarette Manufacturing","Packaging Line","Boiler House","ETP"]},
        "Nestle  -  Moga Plant": {"Processing": ["Milk Reception","Spray Drying","Packaging","Utilities"]},
    },
    "Chemicals": {
        "Tata Chemicals  -  Mithapur": {"Soda Ash": ["Chlor-Alkali Plant","Soda Ash Plant","Vacuum Salt Plant"]},
        "UPL  -  Bharuch": {"Agrochemicals": ["Chlorine Plant","Pesticide Synthesis","Formulation Unit"]},
        "Deepak Nitrite  -  Nandesari": {"Nitrites": ["Sodium Nitrite Plant","Nitric Acid Plant","Colour Division"]},
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
    # ── Tata Steel PSRM Module  -  Consequence Levels ──────────────────
    "consequence_levels": {
        "L1": {"label":"L1  -  Minor","color":"#22c55e",
               "people":"First Aid Case (FAC). No fatality, no hospitalisation.",
               "community":"No off-site impact.",
               "asset":"Property damage < Rs.5 Lakhs. Minor equipment damage.",
               "environment":"Negligible. Contained on-site. No reportable release.",
               "production":"< 8 hours production loss.",
               "desc":"Minor incident. No process safety implication. Managed at supervisory level.",
               "psm_action":"Record in Near Miss/FAC register. Investigate within 5 working days. No statutory reporting.",
               "examples":["Minor chemical spill  -  contained in bund","Slip/trip  -  first aid","Minor instrument failure causing brief stoppage"]},
        "L2": {"label":"L2  -  Moderate","color":"#eab308",
               "people":"Medical Treatment Case (MTC) or Lost Time Injury (LTI). No fatality.",
               "community":"Limited off-site impact. Reversible. No public alarm.",
               "asset":"Property damage Rs.5 – 50 Lakhs.",
               "environment":"Limited release. Reversible impact. Reportable to local authority.",
               "production":"8-72 hours production loss.",
               "desc":"Moderate incident. Reportable internally. May involve process safety element.",
               "psm_action":"CAPA required within 30 days. Review by plant head. Check PSCE status. Internal report.",
               "examples":["Chemical spill requiring cleanup team","LTI from process deviation","Equipment damage Rs.5-50L"]},
        "L3": {"label":"L3  -  Serious","color":"#f97316",
               "people":"Multiple LTI or hospitalisation. Single fatality possible.",
               "community":"Significant off-site impact. Community notified. Temporary evacuation possible.",
               "asset":"Property damage Rs.50 Lakhs – 5 Crores. Major equipment destruction.",
               "environment":"Significant release. Regulatory notification required. Potential long-term impact.",
               "production":"72 hours – 1 month production loss.",
               "desc":"Serious process safety incident. Mandatory statutory reporting to PESO/CPCB.",
               "psm_action":"Immediate PESO/CPCB notification. Emergency response activation. Full RCA within 15 days. Board-level review.",
               "examples":["HHO process deviation causing fire","Toxic release above ERPG-2","Major equipment failure with injury"]},
        "L4": {"label":"L4  -  Critical","color":"#ef4444",
               "people":"Multiple hospitalisations. 1-5 fatalities.",
               "community":"Community significantly affected. Multi-area evacuation. Media coverage.",
               "asset":"Property damage Rs.5 – 50 Crores. Section/plant destroyed.",
               "environment":"Major release. Long-term environmental impact. NDRF involvement.",
               "production":"1-6 months production loss.",
               "desc":"Major process safety accident. Statutory investigation. Regulatory intervention and plant shutdown.",
               "psm_action":"PESO/District authority notification within 12h. Crisis management. External RCA team. Insurance claim.",
               "examples":["Explosion with fatality","Major fire  -  plant section destroyed","Toxic cloud reaching community boundary"]},
        "L5": {"label":"L5  -  Catastrophic","color":"#7f1d1d",
               "people":"Mass casualties. > 5 fatalities.",
               "community":"Widespread off-site impact. Mass evacuation. National media.",
               "asset":"Property damage > Rs.50 Crores. Plant total loss.",
               "environment":"Catastrophic release. Irreversible environmental damage. International reporting.",
               "production":"> 6 months or permanent closure.",
               "desc":"Catastrophic. National-level emergency response. Criminal liability. Company-level consequence.",
               "psm_action":"NDRF activation. Ministry notification. Criminal investigation. Plant closed indefinitely.",
               "examples":["BLEVE at H2 bullet farm","VCE  -  vapour cloud explosion","Bhopal-scale toxic release"]},
    },

    # ── Hazard Categories (A-scale) from Tata Steel PSRM Module ──────
    "hazard_categories": {
        "A1": {"label":"A1  -  Flammable / Explosive","color":"#f97316",
               "desc":"Substances that can ignite and combust or explode when mixed with air/oxidiser in correct proportions. Primary hazard: fire or explosion releasing thermal energy.",
               "key_properties":["Flash Point (deg C)  -  temperature above which vapour ignites","LEL/LFL %  -  Lower Explosive Limit (below = too lean to ignite)","UEL/UFL %  -  Upper Explosive Limit (above = too rich to ignite)","Auto-Ignition Temperature (AIT)  -  spontaneous ignition temperature","Minimum Ignition Energy (MIE, mJ)  -  energy needed to ignite"],
               "examples":["H2: LEL 4%, UEL 75%, MIE 0.017 mJ  -  most ignition-sensitive industrial gas","Propane: LEL 2.1%, UEL 9.5%, Flash -104deg C","Rolling oil mist: Flash >130deg C  -  combustible","DOS oil: Flash 190deg C  -  combustible"],
               "controls":["LEL/H2 continuous detectors","Elimination of all ignition sources in Zone 1/2","Ventilation to maintain <25% LEL","Explosion-proof (Ex-rated) electrical equipment","Bonding and earthing  -  static electricity prevention","ATEX-certified instruments"],
               "psm_implication":"Any process handling A1 material above threshold inventory -&gt; HHO -&gt; Full PSRM with HAZOP, Bow Tie and LOPA mandatory"},
        "A2": {"label":"A2  -  Toxic","color":"#a78bfa",
               "desc":"Substances causing harm through inhalation, skin absorption, ingestion or injection. Hazard characterised by Occupational Exposure Limits (OEL).",
               "key_properties":["TLV-TWA: Time-Weighted Average over 8h shift  -  daily exposure limit","TLV-STEL: Short-Term Exposure Limit over 15 min  -  peak limit","TLV-C (Ceiling): Never to be exceeded even instantaneously","IDLH: Immediately Dangerous to Life and Health  -  emergency value","ERPG-2/3: Emergency Response Planning Guidelines for community"],
               "examples":["Cr-VI (CrO3/Na2Cr2O7): TLV-TWA 0.05 mg/m3  -  IARC Group 1 Carcinogen","H2SO4 mist: TLV-TWA 1 mg/m3  -  corrosive to lungs","CO: TLV-TWA 25 ppm, IDLH 1200 ppm","NaOH: corrosive  -  no OEL but severe contact hazard"],
               "controls":["Continuous ambient air monitoring (mandatory for Cr-VI per MSIHC Rules 1989)","LEV  -  Local Exhaust Ventilation (min 0.5 m/s face velocity)","PPE  -  air-supplied respirator for IDLH substances","Annual medical surveillance","Engineering substitution where possible"],
               "psm_implication":"A2 material above threshold -&gt; HHO if fatality pathway exists. Cr-VI = carcinogen = chronic fatality -&gt; HHO mandatory"},
        "A3": {"label":"A3  -  Reactive / Unstable","color":"#ef4444",
               "desc":"Substances that react violently with other materials, decompose spontaneously, or become thermally unstable. Creates secondary explosive/fire/toxic hazard.",
               "key_properties":["Reactivity classification (NFPA Yellow diamond  -  0 to 4)","Heat of reaction (kJ/mol)  -  energy released","Incompatible materials list (from Chemical Interaction Matrix)","Self-accelerating decomposition temperature (SADT)","Water-reactivity rating"],
               "examples":["Na2Cr2O7: Strong oxidiser  -  reacts violently with organics -&gt; fire","CrO3: Powerful oxidiser  -  contact with organics = spontaneous ignition","Conc. H2SO4 + water: Violent exothermic, spattering","KOH + HCl: Violent exothermic neutralisation"],
               "controls":["Chemical Interaction Matrix (CIM)  -  mandatory for all HHO processes","Storage segregation  -  incompatibles physically separated","Temperature control for thermally unstable materials","Contamination prevention  -  dedicated equipment","HAZOP 'As Well As' and 'Other Than' scenarios for A3 materials"],
               "psm_implication":"A3 materials: CIM mandatory in PSI. HAZOP must include contamination and reverse-flow scenarios. Storage segregation documented in EDB"},
        "A4": {"label":"A4  -  Corrosive","color":"#3b82f6",
               "desc":"Substances that chemically destroy living tissue and corrode metals on contact. Can cause severe burns and equipment failure.",
               "key_properties":["pH (acids <2 or alkalis >12 = severe corrosive)","Corrosion rate (mm/year) for process piping","Skin/eye corrosivity classification (UN GHS)"],
               "examples":["H2SO4: pH ~0 (dilute 8-10 g/L in pickling)  -  skin/eye burns","NaOH 80-90deg C: Severe alkali burns  -  boiling alkali = HHO event","KOH lye: pH 13-14  -  strong corrosive electrolyte"],
               "controls":["Material of construction selection (MoC in EDB)","PPE: Chemical-resistant gloves, apron, face shield","Secondary containment (bunding)  -  110% volume","Emergency deluge showers within 10m","Regular corrosion monitoring (ultrasonic thickness testing)"],
               "psm_implication":"A4 materials: MoC selection documented in EDB. Corrosion monitoring plan in PSCE. NaOH at 90deg C SOL -&gt; HHO (boiling alkali)"},
        "A5": {"label":"A5  -  High Pressure / Temperature","color":"#60a5fa",
               "desc":"Stored mechanical/thermal energy. Sudden uncontrolled release causes mechanical hazard (explosion, projectile, jet) or thermal hazard (steam, molten metal).",
               "key_properties":["Design pressure (kg/cm2) vs Operating pressure","Design temperature (deg C) vs Operating temperature","MAWP (Maximum Allowable Working Pressure)","Vessel design code (IBR/ASME/IS)"],
               "examples":["H2 bullets: 14 kg/cm2 operating, 20 kg/cm2 SOL","H2 electrolyser: 1.57 MPa operating","Steam boiler: 15 bar  -  IBR registration mandatory","Hydraulic AGC CRM: 200 bar operating"],
               "controls":["Safety Relief Valves (SRV)  -  statutory per IBR/PESO for pressure vessels","Pressure transmitters with PLC interlock (PDB SOL parameter)","PESO registration and annual statutory inspection","Pressure vessel inspection (ASME, NDE testing)","Operating below MAWP at all times"],
               "psm_implication":"All pressure vessels >0.5 bar: IBR/PESO registration mandatory. SRV mandatory and prescriptive PSCE item. PDB pressure parameters = PSM Critical"},
    },

    # ── Barrier Model (Tata Steel PSRM Module  -  Detector/Logic/Actuator) ─
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
        {"layer":2,"name":"Basic Process Control System (BPCS)","side":"Prevention  -  SOC","desc":"PLC/DCS controls process within SOC (Standard Operating Condition). The normal operating control system. E.g.: Temperature controller, pressure regulator, level control. Prevents deviation from reaching SOL.","color":"#22c55e"},
        {"layer":3,"name":"Critical Alarms & Operator Response","side":"Prevention  -  SOC","desc":"Alarm alerts operator to deviation approaching SOL. Operator takes corrective action per SOP. E.g.: High-high temperature alarm triggers operator to increase cooling.","color":"#eab308"},
        {"layer":4,"name":"Safety Instrumented System (SIS / SIF)","side":"Prevention  -  SOL","desc":"Automatic safety function that trips/shuts down process when SOL is reached. Independent of BPCS. Certified to SIL (Safety Integrity Level) per IEC 61511. E.g.: Auto-trip on H2-in-O2 >1.7%, cell temperature auto-trip at 97deg C.","color":"#f97316"},
        {"layer":5,"name":"Active Physical Protection (Pre-release)","side":"Prevention","desc":"Mechanical safety device acting before loss of containment. E.g.: Pressure Relief Valve (PRV), Safety Relief Valve (SRV), rupture disk. Prescriptive statutory requirement (IBR/PESO).","color":"#f97316"},
        {"layer":6,"name":"Passive Physical Protection (Post-release)","side":"Mitigation","desc":"Physical barrier reducing consequences after loss of containment. No energy or activation required. E.g.: Bund/dike area, blast wall, catch pit, secondary containment.","color":"#ef4444"},
        {"layer":7,"name":"Plant Emergency Response","side":"Mitigation","desc":"Plant-level emergency response to contain and control the incident. E.g.: Fire brigade, emergency shutdown by operator, evacuation of plant personnel, on-site medical.","color":"#ef4444"},
        {"layer":8,"name":"Community Emergency Response","side":"Mitigation","desc":"Off-site emergency response when community is at risk. E.g.: District emergency plan, NDRF, community evacuation, public notification system.","color":"#7f1d1d"},
    ],

    # ── HAZOP Model (from Tata Steel module) ─────────────────────────
    "hazop": {
        "definition":"HAZOP (Hazard and Operability Study) critically examines a process flow sheet systematically for every conceivable and credible deviation of process variables. Process variables (temperature, pressure, flow, level, operating modes) are taken one at a time, a guide word is applied to generate a deviation, then causes and consequences are identified.",
        "purpose":"Hazard identification technique applied qualitatively to identify process hazards. Can also identify operating problems relating to equipment reliability and quality control. Incorporates prevention or containment of consequences.",
        "when_done":["Conceptual design stage  -  Coarse HAZOP","Detailed design stage  -  HAZOP of final P&IDs","Pre-commissioning  -  'As built' check against P&IDs including safety systems","Post-commissioning  -  Re-HAZOP of major risks based on running experience","Design changes during operational life  -  HAZOP of all planned changes","Revalidation every 5 years minimum"],
        "procedure":["1. Select study node (line, equipment, operating step)","2. Explain design intention and process conditions","3. Select process variable (flow, temperature, pressure, level) or task","4. Apply guide word to generate meaningful deviation","5. Identify credible causes by brainstorming","6. Examine consequences assuming all safeguards fail","7. Identify existing safeguards","8. Assess adequacy  -  judgment or risk assessment","9. Agree recommendation if safeguards are inadequate","10. Repeat for all guide words, variables, nodes"],
        "terminology":{
            "Study Nodes":"Section with definite boundary (line between two vessels). The scope of one HAZOP analysis.",
            "Design Intent":"Definition of how the plant is expected to operate  -  the normal/correct condition.",
            "Guide Words":"Words used to qualify or quantify design intention to generate deviations.",
            "Process Parameters":"Physical or chemical property associated with the process  -  temperature, pressure, flow, level, composition.",
            "Deviations":"Departure from design intent discovered by applying guide words to parameters.",
            "Causes":"Initiating events  -  reasons why deviations occur. Can be equipment failure, human error, external.",
            "Consequences":"Results of deviations assuming all safeguards fail. Loss of containment. Impact on people, asset, environment.",
            "Safeguards":"Engineered or administrative actions that prevent cause from resulting in consequence.",
            "Recommendations":"Suggestions for design changes or procedural changes when safeguards are inadequate.",
        },
        "guide_words":{
            "NONE / NO / NOT":   {"meaning":"No forward flow when there should be, or reverse flow","examples":"No flow  -  pump failure, blocked valve, closed isolation valve"},
            "MORE OF":           {"meaning":"More of any relevant physical property than there should be","examples":"High temperature, high pressure, high flow, high level"},
            "LESS OF":           {"meaning":"Less of any relevant physical property than there should be","examples":"Low flow  -  partial blockage, pump degradation, Low temperature  -  heat loss"},
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
        "definition":"Bow Tie is a risk assessment method visualising pathways from threats -&gt; Top Event (centre) -&gt; consequences. Left side = prevention (stopping top event). Right side = mitigation (limiting consequences after top event).",
        "structure":{
            "Threats / Causes":"Initiating events that could lead to top event. Each threat has a pathway to the top event.",
            "Threat Barriers (Prevention)":"Barriers that interrupt the pathway from threat to top event. Must be: Independent, Functional, Auditable. Each barrier breaks the chain.",
            "Escalation Factors":"Conditions that defeat a barrier. E.g.: Power failure defeats an active barrier. Must have Escalation Factor Controls.",
            "Top Event":"The point of loss of control  -  the uncontrolled release of energy or hazardous material. The 'waist' of the bow tie.",
            "Consequences":"Outcomes if the top event is not mitigated. Multiple consequences possible from one top event.",
            "Recovery/Mitigation Barriers":"Controls that reduce severity after top event. E.g.: Emergency response, fire suppression, evacuation, medical treatment.",
        },
        "barrier_effectiveness":{
            "Passive (Bund/Blast Wall)":{"reliability":"99%+","desc":"Always present, no activation required, independent of all systems"},
            "Active Mechanical (SRV/PRV)":{"reliability":"99%","desc":"Mechanical activation, no electrical dependency, highly reliable"},
            "Active Instrumented SIL-2 SIS":{"reliability":"99-99.9%","desc":"SIS rated to SIL-2. PFD 0.01-0.001. Tested periodically."},
            "Active Instrumented SIL-1 SIS":{"reliability":"90-99%","desc":"SIS rated to SIL-1. PFD 0.1-0.01."},
            "BPCS Control Loop":{"reliability":"90%","desc":"Normal process control. Not independent of process  -  PFD 0.1."},
            "Critical Alarm + Operator (>10 min)":{"reliability":"90%","desc":"Trained operator with sufficient time. PFD ~0.1."},
            "Administrative/Procedural":{"reliability":"50-90%","desc":"Human-dependent. PFD 0.1-1.0. Susceptible to error under stress."},
        },
    },

    # ── LOPA (from Tata Steel module) ─────────────────────────────────
    "lopa": {
        "definition":"LOPA (Layer of Protection Analysis) is a semi-quantitative risk assessment tool for analysing scenarios with higher consequence of concern (major accident scenarios). Risk compared against company risk tolerance criteria. If unacceptable: additional protection layers identified.",
        "risk_formula":"Risk = Likelihood (frequency) × Severity (consequence)  -  Risk is compared against Risk Matrix",
        "steps":["1. Select consequence scenario from HAZOP (major accident potential)","2. Identify initiating cause and its initiating event frequency (IEF, per year)","3. Identify all independent protection layers (IPLs) and their Probability of Failure on Demand (PFD)","4. Calculate mitigated consequence frequency: CF = IEF × PFD₁ × PFD2 × ... × PFDₙ","5. Compare CF against company risk tolerance criteria (Risk Matrix)","6. If risk still unacceptable: design additional IPL or upgrade existing to SIL-rated SIS","Note: LOPA is one of the tools for determining required SIL for a Safety Instrumented Function (SIF)"],
        "layers_with_pfds":[
            ("Process Design","Inherent safety  -  eliminate hazard","N/A"),
            ("BPCS (Basic Process Control System)","PLC/DCS normal control loop","PFD = 0.1"),
            ("Critical Alarm + Operator Response (>10 min available)","Trained operator with time to respond","PFD = 0.1"),
            ("Critical Alarm + Operator Response (<10 min)","Operator under time pressure","PFD = 1.0"),
            ("Safety Instrumented System  -  SIL 1","Auto-trip, PLC-based, periodic tested","PFD = 0.1 to 0.01"),
            ("Safety Instrumented System  -  SIL 2","Higher integrity SIS, more frequent testing","PFD = 0.01 to 0.001"),
            ("Safety Instrumented System  -  SIL 3","Highest SIS level for most hazardous","PFD = 0.001 to 0.0001"),
            ("Pressure Relief Valve (PRV/SRV)","Mechanical pressure protection","PFD = 0.01"),
            ("Check Valve","Mechanical reverse-flow prevention","PFD = 0.1"),
            ("Rupture Disk","One-time mechanical protection","PFD = 0.01"),
            ("Passive Bund / Dike","Physical containment post-release","PFD = 0.01"),
            ("Plant Emergency Response","On-site fire/emergency team","PFD = 0.1"),
        ],
        "tolerable_risk":"Typically &lt;= 1×10⁻⁵ per year for individual fatal risk in Indian chemical industry (ALARP principle)",
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
        "PSER": {"full":"Process Safety Emergency Response","purpose":"Emergency plan for PSI scenarios  -  fire, explosion, toxic release."},
        "PHA":  {"full":"Process Hazard Analysis (HAZOP)","purpose":"Systematic examination of all deviations using guide words. Multidisciplinary team."},
        "Audit":{"full":"PSM Compliance Audit","purpose":"Periodic verification all PSM elements are implemented and effective. Annual for HHO."},
    },
}

PLANT_META = {
    "Hydrogen Plant  -  H2 Production & Supply": {"risk":82,"hho":5,"lho":1,"psce":44,"status":"HHO"},
    "Propane Yard  -  Decantation, Storage & Supply": {"risk":88,"hho":4,"lho":0,"psce":19,"status":"HHO"},
    "ETL-1  -  Electrolytic Tinning Line 1":     {"risk":61,"hho":4,"lho":2,"psce":77,"status":"HHO"},
    "ETL-2  -  Electrolytic Tinning Line 2":     {"risk":54,"hho":4,"lho":2,"psce":12,"status":"HHO"},
    "CRM  -  Cold Rolling Mill":                 {"risk":48,"hho":3,"lho":2,"psce":8, "status":"PSI"},
    "TFS  -  Tin Free Steel":                    {"risk":45,"hho":2,"lho":3,"psce":6, "status":"PSI"},
    "Galvanizing Line (GI/GA)":                {"risk":52,"hho":3,"lho":2,"psce":9, "status":"HHO"},
    "Colour Coated Sheet (CCS)":               {"risk":50,"hho":3,"lho":2,"psce":8, "status":"HHO"},
    "Chlor-Alkali Plant":                      {"risk":78,"hho":5,"lho":2,"psce":14,"status":"HHO"},
}

# ════════════════════════════════════════════════════════════════
# PSM ACRONYM GLOSSARY (full forms)
# ════════════════════════════════════════════════════════════════
PSM_GLOSSARY = {
    "PSC":"Process Safety Classification","PSM":"Process Safety Management","PSI":"Process Safety Information",
    "PSRM":"Process Safety Risk Management","HOM":"Hazard of Material","CIM":"Chemical Interaction Matrix",
    "PDB":"Process Design Basis","PSCE":"Process Safety Critical Equipment","EDB":"Equipment Design Basis",
    "HHO":"High Hazard Operation","LHO":"Low Hazard Operation","SOC":"Standard Operating Condition",
    "SOL":"Safe Operating Limit","SRV":"Safety Relief Valve","EFCV":"Emergency Flow Control Valve",
    "ROCV":"Remote Operated Control Valve","LOPA":"Layer Of Protection Analysis","HAZOP":"Hazard and Operability Study",
    "TLV":"Threshold Limit Value","TWA":"Time-Weighted Average","STEL":"Short-Term Exposure Limit",
    "IDLH":"Immediately Dangerous to Life or Health","LD50":"Lethal Dose 50% (median lethal dose)",
    "LC50":"Lethal Concentration 50% (median lethal concentration)","NFPA":"National Fire Protection Association",
    "BLEVE":"Boiling Liquid Expanding Vapour Explosion","LEL":"Lower Explosive Limit","UEL":"Upper Explosive Limit",
    "LFL":"Lower Flammable Limit","UFL":"Upper Flammable Limit","AIT":"Auto-Ignition Temperature",
    "MIE":"Minimum Ignition Energy","BPCS":"Basic Process Control System","SIS":"Safety Instrumented System",
    "IPL":"Independent Protection Layer","SIL":"Safety Integrity Level","PFD":"Probability of Failure on Demand",
    "ACGIH":"American Conference of Governmental Industrial Hygienists","NIOSH":"National Institute for Occupational Safety and Health",
    "OSHA":"Occupational Safety and Health Administration","CCOE":"Chief Controller of Explosives",
    "PESO":"Petroleum and Explosives Safety Organisation","MSIHC":"Manufacture, Storage and Import of Hazardous Chemicals (Rules)",
    "CPCB":"Central Pollution Control Board","SPCB":"State Pollution Control Board","IBR":"Indian Boiler Regulations",
    "SMPV":"Static and Mobile Pressure Vessels (Rules)","MSDS":"Material Safety Data Sheet","SDS":"Safety Data Sheet",
    "PPE":"Personal Protective Equipment","LEV":"Local Exhaust Ventilation","SCBA":"Self-Contained Breathing Apparatus",
    "PM":"Preventive Maintenance","NDT":"Non-Destructive Testing","ER":"Emergency Response","ERPG":"Emergency Response Planning Guideline",
    "GHS":"Globally Harmonized System (of Classification and Labelling of Chemicals)","CAS":"Chemical Abstracts Service (registry number)",
    "UN":"United Nations (dangerous goods number)","FAC":"First Aid Case","LTI":"Lost Time Injury",
}

def render_glossary(extra_terms=None):
    terms = dict(PSM_GLOSSARY)
    if extra_terms:
        terms.update(extra_terms)
    with st.expander("PSM Glossary - full forms of abbreviations used on this page"):
        g_html = '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:6px;font-size:.74rem">'
        for k in sorted(terms.keys()):
            g_html += f'<div><b style="color:#f97316;font-family:monospace">{k}</b> <span style="color:#94a3b8">= {terms[k]}</span></div>'
        g_html += '</div>'
        st.markdown(g_html, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# GLOBAL INCIDENT DATABASE - "has this happened elsewhere"
# Keyed by hazard-type; shown contextually per chemical/process
# ════════════════════════════════════════════════════════════════
GLOBAL_INCIDENTS = {
    "H2SO4":[
        ("Mariupol, Ukraine (2007)","Sulphuric acid tank rupture released acid cloud, ~100 people sought medical treatment for respiratory irritation."),
        ("Mississauga, Canada","Rail tank car of sulphuric acid leaked during transfer - corrosion of unloading hose was root cause, similar to hose-failure scenarios in PDB."),
    ],
    "Cr-VI":[
        ("Hinkley, California, USA (1950s-60s)","PG&E facility contaminated groundwater with hexavalent chromium from cooling tower water treatment - subject of the Erin Brockovich case. Long-term Cr-VI exposure led to elevated cancer rates."),
        ("Kanpur, India","Tannery industry Cr-VI discharge into Ganga - groundwater contamination affecting villages, ongoing remediation under CPCB orders."),
        ("Painesville, Ohio, USA (Diamond Shamrock, 1980s)","Chromate production plant - chrome ulcers and elevated lung cancer in workers, led to OSHA Cr-VI standard tightening (2006)."),
    ],
    "Phenol":[
        ("Bhopal-adjacent industrial belt, India","Phenolic effluent discharge incidents from chemical units have caused fish kills in local water bodies multiple times over the years."),
        ("Charleston, West Virginia, USA (2014, Elk River)","Chemical spill (different compound, but similar small-molecule organic) contaminated drinking water for 300,000 people - illustrates why phenolic spills must never reach water bodies."),
    ],
    "H2":[
        ("Fukushima Daiichi, Japan (2011)","Hydrogen gas accumulation in reactor buildings from zirconium-water reaction led to multiple hydrogen explosions, breaching containment buildings."),
        ("Crawford, Texas, USA - NASA SSC Hydrogen Test Facility","Hydrogen leak during testing ignited - underscores why H2 leak detectors at 0.2% LEL and Ex-rated electricals are mandatory."),
        ("Norway, Sandvika H2 fuelling station (2019)","Hydrogen explosion at a refuelling station - incorrectly assembled plug allowed H2 leak, ignition source unknown. Station closed for months."),
    ],
    "O2":[
        ("Apollo 1, USA (1967)","Pure oxygen atmosphere in command module caused a small electrical spark to become a flash fire, killing 3 astronauts - extreme example of O2-enrichment fire acceleration."),
        ("Multiple hospital oxygen-line fires worldwide","O2-enriched atmospheres near electrical equipment or oily surfaces have repeatedly caused rapid, hard-to-extinguish fires - basis for 'no oil/grease on O2 fittings' rule."),
    ],
    "N2":[
        ("Multiple confined-space asphyxiation deaths worldwide (ongoing)","Nitrogen purging of vessels/pipelines without O2 testing before entry is one of the most common causes of industrial fatalities globally - workers collapse without warning since N2 is odourless."),
        ("Saudi Arabia, petrochemical plant N2 asphyxiation (multiple incidents)","Workers entering N2-blanketed tanks for inspection without permits have died - root cause almost always missing O2 test/permit-to-work."),
    ],
    "Propane":[
        ("San Juanico, Mexico (1984)","LPG storage facility BLEVE and chain-reaction explosions killed ~500-600 people - one of the worst LPG disasters in history, directly relevant to bullet-tank BLEVE risk."),
        ("Toronto, Canada - Sunrise Propane (2008)","Propane facility explosion forced evacuation of ~12,000 residents - overfilled cylinder/transfer error implicated, similar to liquid level SOL breach scenario."),
        ("Feyzin, France (1966)","Early classic LPG BLEVE - a leak during tanker draining ignited, fireball killed 18 - origin of many modern bund/drainage design rules for LPG yards."),
    ],
    "DOS":[
        ("General - food contact ester spills","Low-hazard esters like DOS rarely cause major incidents; the main industry concern is cross-contamination with oxidisers (Cr-VI) during storage causing localized fires in plating shops."),
    ],
    "ENSA":[
        ("General - plating brightener bath fires","Several tin/nickel plating facilities globally have reported bath fires when organic brighteners contacted Cr-VI rinse baths due to poor segregation - reinforces CIM segregation requirements."),
    ],
}

def render_global_incidents(keys, title="Has This Happened Before? - Global Incident Reference"):
    items = []
    for k in keys:
        items.extend(GLOBAL_INCIDENTS.get(k,[]))
    if not items:
        return
    st.markdown(f'<div class="sl-sec">{title}</div>', unsafe_allow_html=True)
    for loc, desc in items:
        st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:3px solid #eab308;border-radius:8px;padding:.7rem 1rem;margin-bottom:6px"><div style="font-size:.72rem;font-weight:700;color:#eab308;margin-bottom:3px">{loc}</div><div style="font-size:.76rem;color:#94a3b8;line-height:1.6">{desc}</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# LOCAL HAZARD Q&A BOT - keyword-matched, no external API
# ════════════════════════════════════════════════════════════════
BOT_KB = [
    (["bleve","boiling liquid"],"BLEVE (Boiling Liquid Expanding Vapour Explosion) occurs when a pressure vessel containing a liquid above its atmospheric boiling point fails catastrophically - usually from external fire heating the shell above the liquid level until it weakens and ruptures. The sudden depressurisation causes explosive flash-boiling and, if flammable, a massive fireball. Prevention: pressure relief valves (SRVs), fireproofing, water deluge/sprinkler cooling, and maintaining safe inventory levels."),
    (["lel","uel","explosive limit"],"LEL (Lower Explosive Limit) and UEL (Upper Explosive Limit) define the concentration range of a gas/vapour in air that can ignite. Below LEL: too lean to burn. Above UEL: too rich to burn. Between LEL and UEL: explosive range - any ignition source can cause fire/explosion. Gas detectors are typically set to alarm at 25% of LEL for early warning."),
    (["cr-vi","chromium","carcinogen","hexavalent"],"Hexavalent Chromium Cr(VI) is an IARC Group 1 confirmed human carcinogen. It causes lung, nasal and sinus cancers with a latency of 15-30 years, plus skin ulcers ('chrome holes') and respiratory irritation. ACGIH TLV-TWA is just 0.01 mg/m3 - among the lowest exposure limits of any industrial chemical, reflecting its severe long-term risk."),
    (["asphyxiant","n2","nitrogen","o2 deficient","oxygen deficient"],"Simple asphyxiants like N2, H2 and Ar displace oxygen without any chemical toxicity. At O2 19.5% - alarm threshold. At 16% - impaired judgment. At 12% - unconsciousness. At 6% - death within minutes. Because these gases are colourless and odourless, victims often collapse with NO warning - this is why O2 monitoring before confined space entry is mandatory."),
    (["soc","sol","operating limit"],"SOC (Standard Operating Condition) is the normal target range for a parameter during routine operation. SOL (Safe Operating Limit) is the outer safety boundary - breaching SOL is a Process Safety Incident requiring immediate corrective action or shutdown. The gap between SOC and SOL gives operators time to respond before a real hazard develops."),
    (["hho","lho","classification"],"A process is classified HHO (High Hazard Operation) if a credible deviation could cause: property damage >Rs.50 lakh, single or multiple fatality, OR significant environmental impact (recovery >2 months). If none of these apply, it is LHO (Low Hazard Operation) and only baseline PSI documentation is required, not full PSRM."),
    (["lopa","layer of protection"],"LOPA (Layer Of Protection Analysis) is a semi-quantitative method to verify that enough Independent Protection Layers (IPLs) exist for a hazard scenario. Each IPL has a Probability of Failure on Demand (PFD). LOPA multiplies the initiating event frequency by all IPL PFDs - if the resulting risk is still above tolerable (~1e-5/year for fatality), more IPLs or a higher SIL safety system is required."),
    (["barrier","detector","actuator"],"The barrier model (Tata Steel PSRM) says a safety barrier = Detector + Logic Solver + Actuator. A barrier only works if ALL THREE parts function. E.g. a gas detector (Detector) triggers the PLC (Logic Solver) which closes an isolation valve (Actuator). If any one component fails, the whole barrier fails - this is why each component must be tested/calibrated on schedule."),
    (["propane","lpg"],"Propane (LPG) is a Category 1 Flammable Gas, heavier than air (vapour density 1.52), so leaks pool in low areas and drains rather than dispersing upward like hydrogen. LEL 2.1%, UEL 9.5%. The biggest catastrophic risk is BLEVE if a storage bullet is exposed to fire - this is why water deluge systems and pressure relief valves are mandatory on every bullet."),
    (["hydrogen","h2 plant"],"Hydrogen is the most ignition-sensitive industrial gas - Minimum Ignition Energy just 0.017 mJ (an invisible static spark is enough). It is lighter than air so it rises and accumulates at ceilings/roofs - detector placement should be HIGH, opposite to propane (heavier than air, detectors LOW). H2 flames are invisible in daylight - UV flame detectors are needed."),
    (["psm","psrm","framework"],"PSM (Process Safety Management) is the overall discipline of identifying, evaluating and controlling hazards from highly hazardous chemicals. PSRM (Process Safety Risk Management) is Tata Steel's specific implementation framework, covering 14 elements including PSI (Process Safety Information: HOM, CIM, PDB, PSCE, EDB), HAZOP, LOPA, and emergency response."),
    (["edb","equipment design"],"EDB (Equipment Design Basis) documents WHY each piece of safety-critical equipment was selected, its manufacturer/model, design basis, maintenance schedule and what happens if it fails. Selection basis is usually one of: Consequence Based (failure leads directly to a major hazard), Prevention & Mitigation (reduces likelihood/severity), or Prescriptive (required by law/standard regardless of risk level)."),
    (["psce"],"PSCE (Process Safety Critical Equipment) is any equipment whose failure could directly cause or fail to prevent a major accident. Every PSCE item needs documented maintenance, testing and a clear consequence-of-failure statement. Categories include: Safety Monitoring (gauges/detectors), Controlled Release (EFCVs), Active Mitigation (sprinklers), Prescriptive (statutory items like SRVs), and Consequence Based (the vessels/pipework themselves)."),
]

def _proc_match(a, b):
    """Loose match between two process/sub-process names, ignoring parenthetical
    qualifiers and minor wording differences (e.g. 'Tin Plating (8 cells)' ~ 'Tin Plating')."""
    import re as _re
    def norm(s):
        s = _re.sub(r'\(.*?\)', '', s or '').strip().lower()
        return set(s.split())
    wa, wb = norm(a), norm(b)
    if not wa or not wb:
        return False
    overlap = len(wa & wb)
    return overlap >= max(1, min(len(wa), len(wb)) * 0.5)

def render_qa_bot(page_key):
    st.markdown('<div class="sl-sec">Ask about this page</div>', unsafe_allow_html=True)
    q_key = f"bot_q_{page_key}"
    q = st.text_input("Ask a question (e.g. 'what is BLEVE', 'what is LEL', 'what is Cr-VI risk')", key=q_key, placeholder="Type a question about hazards, terms, or this process...")
    if q:
        ql = q.lower()
        best = None
        for kws, ans in BOT_KB:
            if any(kw in ql for kw in kws):
                best = ans
                break
        if best:
            st.markdown(f'<div class="sl-chat-ai">{best}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="sl-chat-ai">No canned answer for that yet. Try asking about: BLEVE, LEL/UEL, Cr-VI, asphyxiants, SOC/SOL, HHO/LHO, LOPA, barriers, propane, hydrogen, PSM/PSRM, EDB, or PSCE.</div>', unsafe_allow_html=True)

PLANT_PROFILES = {
    "Propane Yard  -  Decantation, Storage & Supply": {
        "short":"PROP","processes":4,"chemicals":1,"params":11,
        "desc":"Propane Yard (BAF area), TCIL Golmuri - Propane decantation from tankers, storage in 5 bullet tanks (56 MT total), and supply to vaporizers for ETL reflow furnaces. All 4 sub-processes classified HHO. Key hazards: BLEVE risk from pressurised propane (LEL 2.1%, UEL 9.5%), 56 MT site inventory, 5 bullet tanks at 2.5-10 kg/cm2 operating pressure. Doc: PSRM/PSI/TINPL/PROP - Eff. Date: 01.05.2024.",
        "proc_cards":[
            ("Liquid Propane Decantation","Tanker to Static Tanks 1-4 via Liquid Pump (Corken USA). Operating pressure: 0-10 kg/cm2 SOC, 20 kg/cm2 SOL.","hho",["HHO","PSM Required","BLEVE Risk"]),
            ("Vapour Decantation","Tanker to Static Tanks via Vapour Compressor. Pressure: 1.5-10 kg/cm2 SOC.","hho",["HHO","PSM Required"]),
            ("Propane Bullet Storage","5 Bullet Tanks, 56 MT total inventory. Pressure: 2.5-10 kg/cm2 SOC. Temp: 15-35deg C SOC. Dual SRVs + EFCV + water sprinkler.","hho",["HHO","BLEVE Risk","PSM Required"]),
            ("Supply to Vaporizers","Bullets to Vaporizers to ETL reflow furnaces. Liquid pump supply at regulated pressure.","hho",["HHO","PSM Required"]),
        ],
        "alerts":[
            (95,"CRITICAL - BLEVE Risk | 56 MT Propane inventory | 5 bullets at 2.5-10 kg/cm2 | Vapour heavier than air - pools in low areas"),
            (88,"CRITICAL - LEL 2.1% | Any ignition source within hazardous area = explosion | Leak detection mandatory"),
            (82,"HIGH - Tank overpressure SOL 20 kg/cm2 | Dual SRV protection | Water sprinkler ROCV as mitigation"),
        ],
        "pdb_params":[
            {"sl":1,"param":"Pressure - Liquid Decantation (Tanker -> Tanks 1-4)","uom":"kg/cm2","soc_min":0,"soc_max":10,"sol_min":"0 (no flow)","sol_max":20,"sub_process":"Liquid Decantation","equipment_linked":"Liquid Pump, Sight Flow Glass, Rota Gauge","identification_low":"Tanker rota gauge + Sight Flow Glass - no flow = low/no pressure","identification_high":"Static tank pressure gauge - high pressure reading","consequence_low":"No consequence if flow stops - decantation halts.","consequence_high":"Hose rupture at 20 kg/cm2 - uncontrolled propane release - fire/explosion.","action_low":"Operator stops decantation, isolates valves, investigates pump/hose.","action_high":"Operator stops decantation immediately, isolates tanker valves.","psm_critical":"Yes"},
            {"sl":2,"param":"Pressure - Vapour Decantation (Tanker -> Tanks 1-4)","uom":"kg/cm2","soc_min":1.5,"soc_max":10,"sol_min":1,"sol_max":20,"sub_process":"Vapour Decantation","equipment_linked":"Compressor #1, Pressure gauges","identification_low":"Pressure gauge at tanker - low reading","identification_high":"Static tank pressure gauge - high reading","consequence_low":"Below 1 kg/cm2 SOL - compressor damage/cavitation.","consequence_high":"Hose/pipeline rupture at >20 kg/cm2 - propane vapour release.","action_low":"Operator closes compressor isolation valve.","action_high":"Stop vapour decantation, isolate compressor discharge.","psm_critical":"Yes"},
            {"sl":3,"param":"Liquid Pump #1 Discharge Pressure","uom":"kg/cm2","soc_min":0,"soc_max":10,"sol_min":"0 (no flow)","sol_max":20,"sub_process":"Liquid Decantation","equipment_linked":"Liquid Pump #1, Sight Flow Glass, SRV","identification_low":"Sight flow glass - no flow; pressure gauge after pump","identification_high":"Pressure gauge - high discharge reading","consequence_low":"Pump cavitation or dry running - pump damage.","consequence_high":"Pipeline rupture at >20 kg/cm2 - propane liquid release.","action_low":"Operator checks pump, connections, hose condition.","action_high":"Stop pump, isolate, investigate.","psm_critical":"Yes"},
            {"sl":4,"param":"Vapour Compressor #1 Suction/Discharge Pressure","uom":"kg/cm2","soc_min":1.5,"soc_max":10,"sol_min":1,"sol_max":20,"sub_process":"Vapour Decantation","equipment_linked":"Compressor #1, SRV at discharge","identification_low":"Pressure gauge at Compressor #1 - below 1.5 kg/cm2","identification_high":"Pressure gauge above 10 kg/cm2 - operator stops compressor","consequence_low":"Low suction - compressor damage.","consequence_high":"Pipeline rupture - propane vapour release - fire/explosion.","action_low":"Check suction, tanker vapour pressure, take corrective action.","action_high":"Stop compressor, isolate discharge line.","psm_critical":"Yes"},
            {"sl":5,"param":"Propane Tank Liquid Level (Tanks 1-5)","uom":"%","soc_min":15,"soc_max":75,"sol_min":5,"sol_max":90,"sub_process":"Bullet Storage","equipment_linked":"Level Rotogauge (all tanks), EFCV Inlet/Outlet","identification_low":"Level rotogauge - low reading triggers discharge valve closure","identification_high":"Level rotogauge - high reading triggers inlet valve closure","consequence_low":"5% SOL - vaporizer trip, pump cavitation, loss of supply.","consequence_high":"90% SOL - liquid overflow from bullet - major spill - BLEVE risk.","action_low":"Operator ensures level >15% SOC. Arrange tanker.","action_high":"Stop filling immediately at 75% SOC target. Close inlet valve.","psm_critical":"Yes"},
            {"sl":6,"param":"Propane Tank Internal Pressure (Tanks 1-5)","uom":"kg/cm2","soc_min":2.5,"soc_max":10,"sol_min":1.5,"sol_max":20,"sub_process":"Bullet Storage","equipment_linked":"Tank pressure gauge, Dual SRV, Water sprinkler ROCV","identification_low":"Static tank pressure gauge - low reading","identification_high":"Static tank pressure gauge - high reading; compressor stops at high pressure","consequence_low":"1.5 kg/cm2 SOL - tank sweating, pipeline condensation, vaporizer failure.","consequence_high":"20 kg/cm2 SOL - tank burst/BLEVE - CATASTROPHIC (L5 consequence).","action_low":"Maintain pressure >5 kg/cm2 minimum. Check for leaks.","action_high":"Dual SRVs provide pressure relief. Activate water sprinkler if temp elevated.","psm_critical":"Yes"},
            {"sl":7,"param":"Propane Tank Internal Temperature (Tanks 1-5)","uom":"deg C","soc_min":15,"soc_max":35,"sol_min":10,"sol_max":45,"sub_process":"Bullet Storage","equipment_linked":"Temperature gauge (WIKA EN13192), Water sprinkler ROCV","identification_low":"Temperature gauge - low reading","identification_high":"Temperature gauge - above 36deg C = water sprinkler activation","consequence_low":"Propane density increases - reduced flow, vaporizer performance affected.","consequence_high":"45deg C SOL - tank pressure rises sharply - potential BLEVE (L5 - CATASTROPHIC).","action_low":"Monitor. Maintain tank pressure >5 kg/cm2 to avoid low temp problems.","action_high":"Activate water sprinklers at 36deg C. Full water deluge if SOL approached.","psm_critical":"Yes"},
        ],
        "psce_items":[
            {"sl":1,"equipment":"Liquid Pump (Corken USA - 521-E-G-A-J-E)","tag":"Liq Pump #1","category":"Service & Utility","sub_process":"Liquid Decantation","justification":"Transfers liquid propane from tanker to static tanks. Failure = loss of liquid decantation. Quarterly PM mandatory. Rule-33 compliant pump.","consequence_of_failure":"Loss of liquid decantation capability. Tanker cannot be unloaded.","maintenance":"Quarterly PM. Test Certificate per Rule-33."},
            {"sl":2,"equipment":"Motor for Liquid Pump (Crampton Greaves - 5.5KW, 7.5HP)","tag":"Pump Motor #1","category":"Service & Utility","sub_process":"Liquid Decantation","justification":"Drives liquid pump. Ex-rated motor mandatory in Zone 1/2 hazardous area. Failure = pump inoperative.","consequence_of_failure":"Liquid pump stops - loss of decantation.","maintenance":"Quarterly PM."},
            {"sl":3,"equipment":"Liquid Transfer Hoses (ACME/PARKER)","tag":"40020815","category":"Prescriptive","sub_process":"Liquid Decantation","justification":"Flexible hoses connect tanker to static tanks. Failure = uncontrolled liquid propane release. Hydro-tested annually per Rule-33.","consequence_of_failure":"Hose failure -> uncontrolled propane release -> fire/explosion.","maintenance":"Annual hydro test."},
            {"sl":4,"equipment":"Pop Action Safety Valve - Liquid Decantation Line","tag":"40020810","category":"Prescriptive","sub_process":"Liquid Decantation","justification":"Pressure relief on liquid pipeline. Prevents overpressure above SOL (20 kg/cm2). Statutory requirement per Rule-33/SMPV Rules.","consequence_of_failure":"Overpressure in liquid pipeline -> hose/pipe rupture -> propane release.","maintenance":"Annual hydro test."},
            {"sl":5,"equipment":"Unloading Compressor (Corken - 91-AJFBANSNN)","tag":"Compressor #1","category":"Service & Utility","sub_process":"Vapour Decantation","justification":"Transfers propane vapour from tanker to static tanks. Failure = loss of vapour decantation. Quarterly PM. ATEX-rated in Zone 1/2.","consequence_of_failure":"Vapour decantation impossible - tanker cannot complete unloading.","maintenance":"Quarterly PM. Rule-33 compliance."},
            {"sl":6,"equipment":"Motor for Compressor (Crampton Greaves - 5.5KW, 7.5HP)","tag":"Comp Motor #1","category":"Service & Utility","sub_process":"Vapour Decantation","justification":"Drives vapour compressor. Ex-rated in Zone 1/2. Failure = compressor inoperative.","consequence_of_failure":"Compressor stops - vapour decantation lost.","maintenance":"Quarterly PM."},
            {"sl":7,"equipment":"Vapour Transfer Hoses (ACME/PARKER)","tag":"40020816","category":"Prescriptive","sub_process":"Vapour Decantation","justification":"Flexible hoses for vapour decantation. Failure = uncontrolled propane vapour release. Hydro-tested annually.","consequence_of_failure":"Hose failure -> propane vapour release -> fire/explosion.","maintenance":"Annual hydro test."},
            {"sl":8,"equipment":"Pop Action SRV - Vapour Decantation Line","tag":"40020810","category":"Prescriptive","sub_process":"Vapour Decantation","justification":"Pressure relief on vapour pipeline. Prevents overpressure above SOL. Statutory requirement.","consequence_of_failure":"Vapour line overpressure -> hose rupture -> uncontrolled propane release.","maintenance":"Annual hydro test."},
            {"sl":9,"equipment":"Pop Action SRV - Compressor Discharge Line","tag":"40020813","category":"Prescriptive","sub_process":"Vapour Decantation","justification":"Relief valve on compressor discharge. Prevents compressor overload and pipeline rupture from high discharge pressure.","consequence_of_failure":"Compressor discharge overpressure -> pipeline rupture -> propane release.","maintenance":"Annual calibration."},
            {"sl":10,"equipment":"Bullet Temperature Gauge (WIKA - EN13192)","tag":"TO BE NOMENCLATED","category":"Safety Monitoring","sub_process":"Bullet Storage","justification":"Monitors tank temperature (SOC 15-35deg C, SOL 45deg C). High temp = pressure rise = BLEVE. Only temperature monitoring on bullets. Annual calibration mandatory.","consequence_of_failure":"Tank temperature exceeds SOL undetected -> pressure rise -> BLEVE - CATASTROPHIC.","maintenance":"Annual calibration."},
            {"sl":11,"equipment":"Liquid Inlet EFCV (Chandra Engg - Rule-33 rated)","tag":"40020804","category":"Controlled Release","sub_process":"Bullet Storage","justification":"Emergency Flow Control Valve - auto-closes on excess flow (pipe rupture). Prevents catastrophic tank drainage. Prescriptive per Rule-33/SMPV.","consequence_of_failure":"EFCV fails open -> uncontrolled propane flow on pipe rupture -> BLEVE risk.","maintenance":"Calibration every 5 years."},
            {"sl":12,"equipment":"Liquid Outlet EFCV (Chandra Engg)","tag":"40020807","category":"Controlled Release","sub_process":"Bullet Storage","justification":"Emergency valve on liquid outlet - closes on excess flow. Prevents tank drainage on outlet pipeline failure.","consequence_of_failure":"Outlet EFCV fails -> uncontrolled tank emptying -> major propane release.","maintenance":"Calibration every 5 years."},
            {"sl":13,"equipment":"Bullet Pressure Gauge (WIKA - EN837-1)","tag":"TO BE NOMENCLATED","category":"Safety Monitoring","sub_process":"Bullet Storage","justification":"Primary pressure indication at bullet (SOC 2.5-10 kg/cm2, SOL 20 kg/cm2). Wrong reading = uncontrolled pressure condition. Annual calibration.","consequence_of_failure":"Incorrect pressure indication -> overpressure undetected -> tank failure.","maintenance":"Annual calibration."},
            {"sl":14,"equipment":"Vapour Inlet EFCV","tag":"TO BE NOMENCLATED","category":"Controlled Release","sub_process":"Bullet Storage","justification":"Emergency flow control on vapour inlet. Auto-closes on excess vapour flow - prevents uncontrolled release on inlet pipe failure.","consequence_of_failure":"Vapour inlet EFCV fails -> uncontrolled vapour release.","maintenance":"Calibration every 5 years."},
            {"sl":15,"equipment":"Vapour Outlet EFCV","tag":"TO BE NOMENCLATED","category":"Controlled Release","sub_process":"Bullet Storage","justification":"Emergency flow control on vapour outlet. Prevents tank emptying on outlet pipe failure.","consequence_of_failure":"Vapour outlet EFCV fails -> uncontrolled tank vapour loss.","maintenance":"Calibration every 5 years."},
            {"sl":16,"equipment":"Pop Action SRV - Common Liquid Outlet Line","tag":"40020810","category":"Prescriptive","sub_process":"Supply to Vaporizers","justification":"Pressure relief on common liquid outlet to vaporizers. Prevents overpressure propagation downstream. Statutory requirement per Rule-33.","consequence_of_failure":"Outlet line overpressure -> pipe failure -> propane release at vaporizer side.","maintenance":"Annual hydro test."},
            {"sl":17,"equipment":"Leak Detection System (Propane Gas Detectors)","tag":"TO BE NOMENCLATED","category":"Safety Monitoring","sub_process":"All","justification":"Fixed propane gas detectors in hazardous area. Alarm at 25% LEL (0.525% v/v). PRIMARY safety barrier for early detection of propane leaks before explosive concentration reached.","consequence_of_failure":"Propane leak undetected -> explosive atmosphere -> any ignition source = explosion.","maintenance":"Periodic PM."},
            {"sl":18,"equipment":"ROCV - Water Sprinkler System","tag":"TO BE NOMENCLATED","category":"Active Mitigation","sub_process":"Bullet Storage","justification":"Remote Operated Control Valve for water sprinkler/deluge on propane bullets. Activates on high tank temperature or fire. BLEVE PREVENTION - keeps bullets cool under fire exposure.","consequence_of_failure":"Water sprinkler fails -> bullets overheat under fire -> BLEVE - CATASTROPHIC.","maintenance":"Periodic PM. Flow test."},
            {"sl":19,"equipment":"Propane Bullets (Static Tanks 1-5)","tag":"Bullets 1-5","category":"Consequence Based","sub_process":"Bullet Storage","justification":"Pressure vessels storing 56 MT propane. Vessel integrity is fundamental - failure = catastrophic propane release + BLEVE = L5 consequence. CCOE approval, PESO inspection mandatory. 3rd party NDT annually.","consequence_of_failure":"Vessel failure -> 56 MT propane release -> BLEVE -> multiple fatalities, total plant destruction.","maintenance":"Annual PESO statutory inspection. 3rd party NDT. CCOE compliance."},
        ],
        "edb_items":[
            {"sl":1,"sub_process":"Liquid Decantation","hazardous_substance":"Liquid Propane","equipment":"Liquid Pump #1 (Corken USA)","tag_no":"Liq Pump #1","selection_basis":"Prevention & Mitigation Equipment","manufacturer":"Corken USA","model":"521-E-G-A-J-E, SR.NO. 265631GB","design_basis":"Positive displacement pump for liquid propane transfer. Rated for liquid propane service. Rule-33 compliant. Ex-rated for Zone 1/2 hazardous area. Quarterly PM mandatory.","consequence_of_failure":"Loss of liquid decantation - tanker cannot be unloaded.","barrier_type":"Active - Mechanical","barrier_effectiveness":"Primary liquid transfer equipment. Quarterly PM ensures reliability.","is_psce":True},
            {"sl":2,"sub_process":"Liquid Decantation","hazardous_substance":"Liquid Propane","equipment":"Liquid Transfer Hoses (ACME/PARKER)","tag_no":"40020815","selection_basis":"Consequence Based PSRM Critical","manufacturer":"ACME/PARKER","model":"N/A","design_basis":"Flexible armoured hoses rated for liquid propane service. Annual hydro test mandatory per Rule-33. Pressure rating >20 kg/cm2.","consequence_of_failure":"Hose failure -> uncontrolled liquid propane release -> fire/explosion.","barrier_type":"Passive","barrier_effectiveness":"Physical containment - prevents liquid propane release during decantation.","is_psce":True},
            {"sl":3,"sub_process":"Liquid Decantation","hazardous_substance":"Liquid Propane","equipment":"Pop Action SRV - Liquid Pipeline","tag_no":"40020810","selection_basis":"Prevention & Mitigation Equipment","manufacturer":"Chandra Engg","model":"Rule-33 rated","design_basis":"Spring-loaded pressure relief valve. Set pressure per Rule-33/SMPV Rules. Opens at SOL to prevent over-pressurisation.","consequence_of_failure":"Over-pressurisation of liquid line -> hose/pipe rupture -> propane release.","barrier_type":"Active - Mechanical","barrier_effectiveness":"Statutory pressure protection - highest reliability mechanical barrier.","is_psce":True},
            {"sl":4,"sub_process":"Vapour Decantation","hazardous_substance":"Propane Vapour","equipment":"Unloading Compressor #1 (Corken)","tag_no":"Compressor #1","selection_basis":"Prevention & Mitigation Equipment","manufacturer":"Corken","model":"91-AJFBANSNN, S.NO. 70653FM","design_basis":"Reciprocating compressor for propane vapour transfer. Ex-rated motor. Discharge pressure 10 kg/cm2 SOC max. SRV at discharge prevents overload.","consequence_of_failure":"Loss of vapour decantation - tanker cannot complete unloading.","barrier_type":"Active - Mechanical","barrier_effectiveness":"Primary vapour transfer equipment. Quarterly PM.","is_psce":True},
            {"sl":5,"sub_process":"Bullet Storage","hazardous_substance":"Liquid Propane + Propane Vapour","equipment":"Propane Bullets 1-5 (Static Tanks)","tag_no":"Bullets 1-5","selection_basis":"Consequence Based PSRM Critical + Prescriptive","manufacturer":"OEM (CCOE approved)","model":"SMPV rated pressure vessel","design_basis":"Horizontal bullet pressure vessels for LPG storage. CCOE approved design. PESO annual statutory inspection. Design pressure >20 kg/cm2. Each fitted with: Dual SRVs, EFCV (inlet+outlet), temperature gauge, pressure gauge, level rotogauge. ~11 MT each, total 56 MT.","consequence_of_failure":"Vessel failure -> catastrophic propane release -> BLEVE -> L5 consequence.","barrier_type":"Active - Mechanical","barrier_effectiveness":"CCOE/PESO statutory inspection. Dual SRVs. 3rd party NDT annually.","is_psce":True},
            {"sl":6,"sub_process":"Bullet Storage","hazardous_substance":"Liquid Propane + Propane Vapour","equipment":"Water Sprinkler System (ROCV)","tag_no":"TO BE NOMENCLATED","selection_basis":"Active Mitigation System","manufacturer":"-","model":"ROCV controlled","design_basis":"Remote-operated control valve activates water sprinkler/deluge on propane bullets. Activates when bullet temperature >36deg C or under fire exposure. Covers all 5 bullets. BLEVE prevention.","consequence_of_failure":"Bullets overheat -> pressure rises above SOL -> BLEVE - catastrophic.","barrier_type":"Active - Automatic Trip","barrier_effectiveness":"Primary BLEVE prevention mitigation.","is_psce":True},
        ],
    },
    "ETL-2  -  Electrolytic Tinning Line 2": {
        "short":"ETL-2","processes":6,"chemicals":6,"params":17,
        "desc":"ETL-2 is the second electrolytic tinning line at TCIL Golmuri, operating with SHL (Soft Melt Hot Dip Lacquering) process variant. Unlike ETL-1 which uses resistance reflow, ETL-2 uses soft melt + hot dip lacquering technology for superior formability tin plate used in aerosol and drawn-and-ironed (DWI) can manufacturing. Line speed: up to 300 mpm. Annual capacity: ~90,000 MT.",
        "proc_cards":[
            ("Coil Feeding","Hydraulic oil, DM water, compressed air. Payoff reel feeds black plate (0.14-0.36 mm). Entry looper 200m capacity.","lho",["LHO"]),
            ("Electrolytic Cleaning","NaOH 80-90deg C, H2SO4 pickling 8-10 g/L, DC current 2.5-3.5 kA. HHO classification same as ETL-1.","hho",["HHO","PSM Required"]),
            ("Tin Plating (8 cells)","SnSO4 + H2SO4 + ENSA + PSA bath. DC deposition 26-34 g/L Sn++. 8 cells.","hho",["HHO"]),
            ("Soft Melt (SHL Process)","Induction heating 232-250deg C. Lower temp than ETL-1 reflow (270deg C). H2/N2 atmosphere. DWI can grade. HHO.","hho",["HHO","PSM Required"]),
            ("Hot Dip Lacquering","DOS-based lacquer post-melt. Electrostatic. Flash point 190deg C. LHO.","lho",["LHO"]),
            ("Chemical Treatment (Cr-VI)","Chromate passivation  -  Cr-VI chemistry same as ETL-1. IARC Group 1 carcinogen. TLV 0.05 mg/m3. HHO.","hho",["HHO","PSM Required"]),
        ],
        "chemicals":[("A1","H2SO4","Corrosive, generates H2","72"),("A2","PSA","Corrosive","55"),("A3","DOS","Combustible","30"),("A4","ENSA","Irritant","40"),("A5","Na2Cr2O7","CARCINOGEN Cr-VI","95"),("A6","Sn","Heavy metal","35")],
        "alerts":[(95,"CRITICAL  -  Cr-VI (Chemical Treatment) | IARC Group 1 carcinogen | TLV 0.05 mg/m3 | Monitoring mandatory"),(88,"CRITICAL  -  Soft Melt Temp deviation | H2/N2 atmosphere | Explosive risk on seal failure"),(75,"HIGH  -  Sn2+ below SOL | DWI can spec critical | Food contact compliance")],
        "pdb_params":[
            {"sl":1,"param":"Soft Melt Strip Temperature","uom":"deg C","soc_min":232,"soc_max":250,"sol_min":232,"sol_max":255,"sub_process":"Soft Melt (SHL)","equipment_linked":"Pyrometer ETL-2, Induction heater","identification_low":"Pyrometer alarm  -  below 232deg C","identification_high":"Pyrometer alarm at 250deg C, trip at 255deg C","consequence_low":"Incomplete tin melt  -  matte surface  -  DWI formability failure  -  product rejection","consequence_high":"Strip overburn  -  H2 atmosphere disruption  -  structural damage","action_low":"Admin: Increase induction heater power. Hold product.","action_high":"ACTIVE: Pyrometer auto-trip at 255deg C. Admin: Inspect induction coil.","psm_critical":"Yes"},
            {"sl":2,"param":"Sn++ Concentration","uom":"g/L","soc_min":26,"soc_max":34,"sol_min":24,"sol_max":36,"sub_process":"Tin Plating","equipment_linked":"Sn analyser","identification_low":"Bath analysis alarm  -  SOL low","identification_high":"Bath analysis alarm  -  high Sn++","consequence_low":"UNDER-PLATING  -  DWI can fracture on drawing  -  food contamination risk","consequence_high":"Over-coating  -  material cost, specification breach","action_low":"Admin: Add SnSO4 makeup. Hold product. Active: Analyser alarm.","action_high":"Admin: Reduce current density.","psm_critical":"Yes"},
            {"sl":3,"param":"Cr-VI Bath Temperature","uom":"deg C","soc_min":40,"soc_max":45,"sol_min":40,"sol_max":45,"sub_process":"Chemical Treatment","equipment_linked":"TT-ChemTx ETL-2, LEV","identification_low":"Temperature transmitter alarm","identification_high":"Auto-bath shutdown at 45deg C SOL","consequence_low":"Incomplete passivation  -  corrosion failure in DWI drawn cans","consequence_high":"Cr-VI mist surge  -  TLV breach  -  MANDATORY SHUTDOWN per MSIHC Rules 1989","action_low":"Admin: Check heating.","action_high":"ACTIVE: Bath auto-off. Air monitor check. SHUTDOWN if Cr-VI >0.05 mg/m3.","psm_critical":"Yes"},
        ],
        "psce_items":[
            {"sl":1,"equipment":"Pyrometer  -  Soft Melt Strip Temp","tag":"Pyro-ETL2","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Soft Melt (SHL)","sap_tag":"S-ETL2-001","justification":"Primary strip temp monitoring for SHL (SOC 232-250deg C, SOL 255deg C). Auto-trip at SOL. H2/N2 atmosphere  -  deviation affects safety.","consequence_of_failure":"Strip overburn undetected -&gt; H2 atmosphere disruption -&gt; explosive risk. Under-melt -&gt; DWI product failure.","maintenance":"3-monthly calibration."},
            {"sl":2,"equipment":"Cr-VI Air Monitor ETL-2","tag":"CrVI-ETL2","psce_type":"Prescriptive","category":"Safety Monitoring & Emergency Communication","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL2-002","justification":"Prescriptive per MSIHC Rules 1989. Continuous Cr-VI monitoring. TLV 0.05 mg/m3. IARC Group 1 carcinogen.","consequence_of_failure":"Cr-VI exposure undetected -&gt; carcinogenic health effect. Statutory violation.","maintenance":"Quarterly calibration. Monthly bump test."},
        ],
        "edb_items":[
            {"sl":1,"sub_process":"Soft Melt (SHL)","hazardous_substance":"Hydrogen Gas","equipment":"Soft Melt Induction Heater","tag_no":"IH-ETL2","selection_basis":"Consequence Based","manufacturer":"Ajax Tocco / Inductotherm","model":"Induction Heating System","design_basis":"Induction heating coils melt tin at 232-250deg C. H2/N2 atmosphere. Rated for strip width up to 1050mm at 300 mpm.","consequence_of_failure":"Heater failure -&gt; incomplete melt or overshoot -&gt; strip burning -&gt; H2 atmosphere disruption.","barrier_type":"Active  -  Instrumented","barrier_effectiveness":"Pyrometer feedback loop  -  tighter temp control than resistance reflow.","is_psce":True},
        ],
    },
    "CRM  -  Cold Rolling Mill": {
        "short":"CRM","processes":5,"chemicals":4,"params":12,
        "desc":"The Cold Rolling Mill (CRM) reduces hot-rolled black plate to required thickness (0.14-0.50mm). Tandem mill with 4 rolling stands using mineral oil emulsion as lubricant/coolant. Rolling force up to 2000 kN. Strip speed up to 600 mpm. Key hazards: rolling oil emulsion mist (fire), hydraulic high-pressure systems, high-speed strip, electrical arc flash.",
        "proc_cards":[
            ("Coil Preparation","Decoiler, straightener, welder. Entry loop. Hydraulic 150-200 bar. Compressed air 5-6 bar.","lho",["LHO"]),
            ("Rolling Oil Emulsion System","Mineral oil emulsion 3-5%. Flash point >130deg C. Heated to 45-55deg C. Emulsion mist  -  fire risk.","hho",["HHO","Fire Risk"]),
            ("Tandem Rolling (4 Stands)","4-high mill. 2000 kN force. 600 mpm strip speed. 5-15 MW drives. Arc flash hazard.","hho",["HHO","Electrical"]),
            ("Strip Cleaning (Post Rolling)","Alkaline cleaning 50-70deg C. NaOH/Na2CO3 based. Mild corrosive. LHO.","lho",["LHO"]),
            ("Inspection & Recoiling","Flying shear, side trimmer, inspection, recoiler. Mechanical hazards.","lho",["LHO"]),
        ],
        "chemicals":[("C1","Rolling Oil Emulsion","Combustible mist, flash 130deg C","55"),("C2","NaOH","Corrosive alkali","45"),("C3","Hydraulic Oil","Combustible, flash 170deg C","35"),("C4","Lubricating Grease","Combustible","20")],
        "alerts":[(78,"HIGH  -  Rolling oil mist in mill housing | Flash 130deg C | Fire/explosion if ignition source"),(72,"HIGH  -  Hydraulic at 200 bar | Seal failure = oil spray onto hot strip  -  fire risk"),(65,"MEDIUM  -  Electrical arc flash at 5-15 MW drive panels | PPE mandatory")],
        "pdb_params":[
            {"sl":1,"param":"Rolling Oil Emulsion Concentration","uom":"%","soc_min":3.0,"soc_max":5.0,"sol_min":2.5,"sol_max":6.0,"sub_process":"Rolling Oil System","equipment_linked":"Conductivity analyser, dosing pump","identification_low":"Conductivity alarm  -  low concentration","identification_high":"Conductivity alarm  -  high concentration","consequence_low":"Insufficient lubrication -&gt; friction -&gt; surface defects -&gt; heat buildup -&gt; fire risk","consequence_high":"Excess emulsion mist -&gt; fire/explosion risk in mill housing","action_low":"Admin: Check dosing pump. Add makeup oil.","action_high":"Admin: Reduce dosing. Check analyser. Ensure LEV functional.","psm_critical":"Yes"},
            {"sl":2,"param":"Hydraulic System Pressure","uom":"bar","soc_min":150,"soc_max":200,"sol_min":140,"sol_max":220,"sub_process":"Tandem Rolling","equipment_linked":"Pressure transmitter, PRV, hydraulic power unit","identification_low":"Pressure transmitter alarm","identification_high":"Pressure transmitter alarm + PRV lifts","consequence_low":"Insufficient AGC hydraulic -&gt; gauge deviation -&gt; product rejection","consequence_high":"Hydraulic line rupture at 200 bar -&gt; oil spray on hot strip -&gt; fire risk","action_low":"Admin: Check hydraulic pump.","action_high":"Active: PRV mechanical protection. Admin: Inspect lines. Emergency stop if rupture.","psm_critical":"Yes"},
        ],
        "psce_items":[
            {"sl":1,"equipment":"Rolling Oil Emulsion LEV System","tag":"LEV-CRM","psce_type":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes","sub_process":"Rolling Oil System","sap_tag":"S-CRM-001","justification":"LEV removes oil mist from mill housing (flash 130deg C). Primary barrier for fire/explosion. Interlock: mill cannot run without LEV.","consequence_of_failure":"Oil mist accumulates -&gt; explosive atmosphere -&gt; fire/explosion -&gt; multiple fatalities.","maintenance":"Monthly airflow measurement. Quarterly inspection."},
            {"sl":2,"equipment":"Strip Break Detection System","tag":"SBD-CRM","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Tandem Rolling","sap_tag":"S-CRM-002","justification":"At 600 mpm, strip break causes metal flailing  -  projectile and wrap-up risk. Emergency stop triggered within 50ms.","consequence_of_failure":"Strip break undetected at 600 mpm -&gt; metal flail -&gt; fatality -&gt; wrap-up -&gt; fire.","maintenance":"Monthly functional test."},
        ],
        "edb_items":[
            {"sl":1,"sub_process":"Rolling Oil System","hazardous_substance":"Rolling Oil Emulsion (flash 130deg C)","equipment":"Rolling Oil Filtration System","tag_no":"ROF-CRM","selection_basis":"Consequence Based","manufacturer":"Voith/SMS Group","model":"Emulsion Filtration Unit","design_basis":"Filters rolling oil to remove iron fines. Clean emulsion reduces mist generation. Rated for full flow at 45-55deg C.","consequence_of_failure":"Dirty emulsion -&gt; increased mist -&gt; fire risk. Iron fines on strip -&gt; surface defects.","barrier_type":"Passive","barrier_effectiveness":"Continuous passive filtration  -  always active  -  reduces mist and fire risk.","is_psce":False},
        ],
    },
}




# ══════════════════════════════════════════════════════════════════════
# MODULE-LEVEL DATA  -  H2 PLANT
# ══════════════════════════════════════════════════════════════════════
H2_PDB_PARAMS = [
    {"sl":1,"param":"DM Water Tank Level","uom":"mm","soc_min":300,"soc_max":1000,"sol_min":100,"sol_max":1500,"sub_process":"DM Water & KOH","equipment_linked":"LIT1301, Feed Pump 1M21","identification_low":"Level transmitter alarm at 450mm","identification_high":"High level alarm at 1000mm  -  pump stop","consequence_low":"Plant trip  -  H2 generation stops. Electrolyser dry running if undetected.","consequence_high":"DM water overflow from tank  -  spillage, housekeeping/safety hazard.","action_low":"Active: auto-trip at SOL. Admin: restore DM water supply.","action_high":"Admin: pump off. Check overflow condition.","psm_critical":"No"},
    {"sl":2,"param":"DM Water Conductivity","uom":"uS/cm","soc_min":0,"soc_max":1,"sol_min":0,"sol_max":1,"sub_process":"DM Water & KOH","equipment_linked":"Conductivity meter","identification_low":"No action  -  minimum desirable","identification_high":"Conductivity meter alarm  -  block feed","consequence_low":"No consequence  -  minimum TDS desirable.","consequence_high":"High TDS -&gt; electrolyser efficiency drops -&gt; cell corrosion/scaling.","action_low":"No safeguard required.","action_high":"Admin: switch DM plant to polishing mode. Do not feed until <1 uS/cm.","psm_critical":"No"},
    {"sl":3,"param":"Electrolyser Cell Temperature","uom":"deg C","soc_min":35,"soc_max":95,"sol_min":25,"sol_max":97,"sub_process":"Electrolysis","equipment_linked":"RTD TE1001, RTD TE1003, TV1001","identification_low":"Constant HMI monitoring  -  RTD alarm","identification_high":"RTD alarm at 95deg C SOC  -  auto-trip at 97deg C SOL","consequence_low":"No consequence on low temp  -  reduced efficiency.","consequence_high":"Cell/electrode damage, KOH decomposition  -  FIRE HAZARD at extreme temp.","action_low":"No safeguard required.","action_high":"Active: PLC auto-trip at 97deg C. Admin: investigate cooling water supply.","psm_critical":"Yes"},
    {"sl":4,"param":"Rectifier DC Current","uom":"A","soc_min":800,"soc_max":1450,"sol_min":500,"sol_max":1600,"sub_process":"Electrolysis","equipment_linked":"Rectifier, Ammeter, QS1001","identification_low":"Ammeter alarm  -  H2 not transferred  -  vent from GLT","identification_high":"Ammeter alarm  -  auto-trip at SOL","consequence_low":"Insufficient energy  -  H2/O2 not generated  -  plant output zero.","consequence_high":"Overheating, cell damage, transformer overload  -  FIRE HAZARD.","action_low":"Active: QS1001 trips to vent. Admin: check rectifier, restore.","action_high":"Active: auto-trip at 1600A. Admin: investigate before restart.","psm_critical":"Yes"},
    {"sl":5,"param":"Separator Liquid Level","uom":"mm","soc_min":500,"soc_max":670,"sol_min":400,"sol_max":770,"sub_process":"Gas-Liquid Treater","equipment_linked":"LT1003, LT1001, LV1001","identification_low":"LT alarm approaching low  -  start interlock","identification_high":"LT alarm  -  lye carryover risk","consequence_low":"Plant will not start below SOL  -  gas bypass -&gt; H2-in-O2 rises.","consequence_high":"Lye into gas pipeline -&gt; purity impact, pipeline blockage.","action_low":"Active: auto-trip at SOL low. Admin: restore lye level.","action_high":"Active: auto-trip at SOL high. Admin: drain to correct level.","psm_critical":"Yes"},
    {"sl":6,"param":"Separator Pressure","uom":"MPa","soc_min":"N/A","soc_max":1.57,"sol_min":"N/A","sol_max":1.65,"sub_process":"Gas-Liquid Treater","equipment_linked":"PT1001, PV1001, SRV","identification_low":"PT1001  -  manual vent valve check","identification_high":"PT1001 alarm  -  PRV/SRV protection","consequence_low":"Transfer to purifier not possible  -  plant on vent.","consequence_high":"Overpressure  -  vessel rupture hazard  -  SRV lifts.","action_low":"Admin: close vent valve, allow pressure to build.","action_high":"Active: SRV mechanical protection. Auto-trip at 1.65 MPa.","psm_critical":"Yes"},
    {"sl":7,"param":"H2 Content in O2 (H2-in-O2)","uom":"%","soc_min":0,"soc_max":0.8,"sol_min":0,"sol_max":1.7,"sub_process":"Gas-Liquid Treater","equipment_linked":"AT1002 (PSCE #13)","identification_low":"AT1002 continuous  -  no action, minimum desirable","identification_high":"AT1002 alarm at SOC  -  auto-trip at SOL (HH)","consequence_low":"No consequence  -  minimum desirable.","consequence_high":"O2 SEPARATOR DETONATION  -  H2+O2 explosive mixture  -  CATASTROPHIC.","action_low":"No safeguard required.","action_high":"ACTIVE: auto-trip at 1.7% SOL. Investigate separator before restart.","psm_critical":"Yes"},
    {"sl":8,"param":"O2 Content in H2 (O2-in-H2)","uom":"%","soc_min":0,"soc_max":0.1,"sol_min":0,"sol_max":0.2,"sub_process":"Gas-Liquid Treater","equipment_linked":"AT1001 (PSCE #14)","identification_low":"AT1001 continuous  -  no action","identification_high":"AT1001 alarm at SOC  -  auto-trip at SOL","consequence_low":"No consequence.","consequence_high":"H2 SEPARATOR EXPLOSIVE MIXTURE  -  auto-trip at 0.2% SOL.","action_low":"No safeguard required.","action_high":"ACTIVE: auto-trip at 0.2% SOL. Full gas analysis before restart.","psm_critical":"Yes"},
    {"sl":9,"param":"H2 Detector (GLT/Purifier/DM zones)","uom":"% LEL","soc_min":0,"soc_max":0.2,"sol_min":0,"sol_max":0.9,"sub_process":"Gas-Liquid Treater","equipment_linked":"AT1701, AT1702, AT1703, Exhaust fan","identification_low":"Fixed detectors  -  no action, minimum desirable","identification_high":"Alarm  -  operator checks for H2 leak. Fan auto-starts.","consequence_low":"No consequence.","consequence_high":"H2 above LEL -&gt; fire/explosion risk  -  auto exhaust fan + plant trip.","action_low":"No safeguard required.","action_high":"Admin: evacuate zone, check leaks. Active: exhaust fan auto-start. Trip at 0.9% SOL.","psm_critical":"Yes"},
    {"sl":10,"param":"Deoxidizer Bed Temperature","uom":"deg C","soc_min":118,"soc_max":160,"sol_min":110,"sol_max":160,"sub_process":"H2 Purification","equipment_linked":"RTD at deoxy unit, Heater","identification_low":"RTD alarm on HMI  -  low temperature","identification_high":"RTD alarm  -  investigate heater","consequence_low":"O2 not removed  -  trace O2 rises  -  explosive mixture risk downstream.","consequence_high":"Catalyst damage  -  purity failure.","action_low":"Active: auto-trip below 110deg C SOL. Admin: check heater.","action_high":"Active: auto-trip at 160deg C SOL.","psm_critical":"Yes"},
    {"sl":11,"param":"Dryer A/B/C Bed Temperature","uom":"deg C","soc_min":170,"soc_max":220,"sol_min":" - ","sol_max":" - ","sub_process":"H2 Purification","equipment_linked":"RTD at each dryer, Heaters","identification_low":"RTD alarm on HMI","identification_high":"RTD alarm","consequence_low":"Poor drying  -  dew point rises  -  moisture in pipeline.","consequence_high":"Dryer damage  -  purity/dew point failure.","action_low":"Active: auto-trip on deviation. Admin: switch to standby dryer.","action_high":"Active: auto-trip. Admin: investigate heater.","psm_critical":"Yes"},
    {"sl":12,"param":"Dew Point (Purified H2)","uom":"deg C","soc_min":"N/A","soc_max":-80,"sol_min":"N/A","sol_max":-70,"sub_process":"H2 Purification","equipment_linked":"MT1101 (PSCE #23), QZ1007","identification_low":"No action  -  lower is better","identification_high":"MT1101 alarm at -80deg C  -  manual calibration check","consequence_low":"No consequence  -  lower dew point is better.","consequence_high":"Moisture in H2 pipeline  -  annealing hood corrosion, purity failure.","action_low":"No safeguard required.","action_high":"Active: auto-trip at -70deg C SOL. QZ1007 vents H2 from storage.","psm_critical":"Yes"},
    {"sl":13,"param":"Purifier Pressure (H2)","uom":"MPa","soc_min":0.6,"soc_max":1.3,"sol_min":0.5,"sol_max":1.4,"sub_process":"H2 Purification","equipment_linked":"PT1101, PV1101, PRV","identification_low":"PT1101 alarm","identification_high":"Auto PRV on high pressure","consequence_low":"Insufficient purifier performance.","consequence_high":"Overpressure  -  SRV lift  -  H2 release.","action_low":"Admin: close vent, check PV1101.","action_high":"Admin: monitor. PRV mechanical backup.","psm_critical":"Yes"},
    {"sl":14,"param":"Trace O2 at Purifier Outlet","uom":"ppm","soc_min":0,"soc_max":1,"sol_min":0,"sol_max":2,"sub_process":"H2 Purification","equipment_linked":"AT1102 (PSCE #26), QZ1007","identification_low":"AT1102 continuous  -  no action","identification_high":"AT1102 alarm  -  do NOT pass to storage","consequence_low":"Analyser may be faulty  -  safety risk if assumed safe.","consequence_high":"EXPLOSIVE mixture in bullet storage if contaminated H2 passes.","action_low":"No safeguard required.","action_high":"ACTIVE: QZ1007 auto-vent diverts from storage. Trip at >2 ppm.","psm_critical":"Yes"},
    {"sl":15,"param":"Cooling Water Tank Level","uom":"mm","soc_min":500,"soc_max":900,"sol_min":600,"sol_max":1000,"sub_process":"DM Water & KOH","equipment_linked":"LIT1501, Cooling pump","identification_low":"LIT1501 alarm at 600mm","identification_high":"Alarm at 1000mm","consequence_low":"GLT trip  -  insufficient cooling  -  cell temp rises.","consequence_high":"Overflow  -  safety/housekeeping hazard.","action_low":"Active: alarm and GLT trip at SOL low. Admin: restore supply.","action_high":"Admin: pump off. Check overflow.","psm_critical":"Yes"},
    {"sl":16,"param":"Cooling Water Temperature","uom":"deg C","soc_min":"N/A","soc_max":35,"sol_min":"N/A","sol_max":40,"sub_process":"DM Water & KOH","equipment_linked":"TE1501, TE1502, TV1001","identification_low":"No action  -  low temp required","identification_high":"Alarm on high temp","consequence_low":"No consequence  -  lower temp required.","consequence_high":"Cooling efficiency drops  -  cell temp rises  -  auto-trip at 97deg C SOL.","action_low":"No safeguard required.","action_high":"Active: auto-trip at 40deg C SOL. Admin: check cooling system.","psm_critical":"Yes"},
    {"sl":17,"param":"Cooling Water Pressure","uom":"kg/cm2","soc_min":2.5,"soc_max":3.5,"sol_min":2.0,"sol_max":6.0,"sub_process":"DM Water & KOH","equipment_linked":"PT1501","identification_low":"PT1501 alarm","identification_high":"Pressure alarm","consequence_low":"Insufficient cooling  -  temp not maintained.","consequence_high":"Pipe rupture/leakage risk.","action_low":"Active: alarm, trip at SOL low. Admin: contact DM plant.","action_high":"Active: alarm at SOL high. Admin: throttle pump.","psm_critical":"Yes"},
    {"sl":20,"param":"Bullet-1 Pressure","uom":"kg/cm2","soc_min":4,"soc_max":14,"sol_min":3,"sol_max":20,"sub_process":"H2 Bullet Storage","equipment_linked":"PG-B1, SRV1/SRV2 (PSCE #34,#35)","identification_low":"Pressure gauge during rounds","identification_high":"Gauge reading  -  SRV lifts at design pressure","consequence_low":"Insufficient H2 supply to annealing  -  production loss.","consequence_high":"SRV lift  -  H2 venting  -  BLEVE risk under fire  -  CATASTROPHIC.","action_low":"Active: PRV adjusts. Admin: restore inlet supply.","action_high":"Active: dual SRVs (PSCE #34,#35). Admin: investigate overpressure.","psm_critical":"Yes"},
    {"sl":21,"param":"Bullet-2 Pressure","uom":"kg/cm2","soc_min":4,"soc_max":14,"sol_min":3,"sol_max":20,"sub_process":"H2 Bullet Storage","equipment_linked":"PG-B2, SRV1/SRV2 (PSCE #36,#37)","identification_low":"Pressure gauge during rounds","identification_high":"SRV lifts at design pressure","consequence_low":"H2 supply interruption to annealing.","consequence_high":"Same as Bullet-1  -  BLEVE risk under fire.","action_low":"Admin: restore supply.","action_high":"Active: dual SRVs (PSCE #36,#37).","psm_critical":"Yes"},
    {"sl":22,"param":"Bullet-1 Temperature","uom":"deg C","soc_min":"N/A","soc_max":45,"sol_min":"N/A","sol_max":50,"sub_process":"H2 Bullet Storage","equipment_linked":"TG-B1 (PSCE #39)","identification_low":"No lower limit.","identification_high":"Gauge alarm  -  water spray initiated","consequence_low":"No consequence.","consequence_high":"Thermal expansion -&gt; pressure rise above SOL -&gt; SRV lift -&gt; H2 release.","action_low":"No action.","action_high":"Admin: water spray on vessel. Shutdown + inspection if SOL persists.","psm_critical":"Yes"},
    {"sl":23,"param":"Bullet-2 Temperature","uom":"deg C","soc_min":"N/A","soc_max":45,"sol_min":"N/A","sol_max":50,"sub_process":"H2 Bullet Storage","equipment_linked":"TG-B2 (PSCE #40)","identification_low":"No lower limit.","identification_high":"Gauge alarm  -  water spray","consequence_low":"No consequence.","consequence_high":"Same as Bullet-1 temperature breach.","action_low":"No action.","action_high":"Admin: water spray. Shutdown if SOL persists.","psm_critical":"Yes"},
    {"sl":24,"param":"Final Outlet Pressure from Bullet","uom":"kg/cm2","soc_min":1.2,"soc_max":2.5,"sol_min":1.0,"sol_max":3.5,"sub_process":"H2 Distribution","equipment_linked":"PRV (PSCE #43), PCV1, PCV2","identification_low":"Gauge at bullet outlet","identification_high":"PRV adjusts automatically","consequence_low":"Insufficient H2 to annealing hoods  -  quality failure.","consequence_high":"Distribution line overpressure  -  PRV adjusts. Pipe failure if PRV fails.","action_low":"Active: PRV adjusts. Admin: check bullet inventory.","action_high":"Active: PRV (PSCE #43) relieves. Admin: check valve positions.","psm_critical":"Yes"},
]

ETL1_PDB_PARAMS = [
    {"sl":1,"param":"Power Pack Hydraulic Pump Pressure","uom":"bar","soc_min":55,"soc_max":70,"sol_min":45,"sol_max":100,"sub_process":"Coil Feeding","equipment_linked":"Hydraulic power pack, actuators","identification_low":"HMI pressure indication - below SOC alarm","identification_high":"HMI pressure indication - above SOC, pressure switch set at 20 bar generates auto-trip","consequence_low":"Coil car unable to lift coil - line stoppage.","consequence_high":"Oil temperature increase with abnormal noise - hydraulic line stress, fire risk (oil flash ~150deg C).","action_low":"Admin: Monitor pressure per SOP ETL-HYD-01. Check pump, oil level.","action_high":"Active: Auto trip system per SOP ETL-HYD-01. Temperature sensor alarm with auto trip.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":2,"param":"DM Water Pressure to Welding Machine","uom":"kg/cm2","soc_min":4.5,"soc_max":5.5,"sol_min":4.5,"sol_max":5.5,"sub_process":"Coil Feeding","equipment_linked":"DM water supply, welder, flow switch","identification_low":"Pressure gauge / HMI - below SOC","identification_high":"Pressure gauge / HMI - above SOC","consequence_low":"Welding cannot initiate - line stoppage.","consequence_high":"Improper cooling due to leakage - welder damage risk.","action_low":"Admin: Check cooling water per SOP WLD-01.","action_high":"Admin: Stop welding, rectify leakage per SOP WLD-01.","psm_critical":"Yes","ref":"NSEC Welder Manual"},
    {"sl":3,"param":"Compressed Air Pressure to Welding Machine","uom":"kg/cm2","soc_min":4.5,"soc_max":5.5,"sol_min":4.5,"sol_max":6.5,"sub_process":"Coil Feeding","equipment_linked":"Compressed air supply, welder, safety valve on air accumulator","identification_low":"Pressure gauge / HMI - below SOC","identification_high":"Pressure gauge / HMI - above SOC, pressure switch interlock","consequence_low":"Welding stops, machine idle - line stoppage.","consequence_high":"Excess air released via safety valve - over-pressure event.","action_low":"Admin: Check air supply per SOP WLD-02.","action_high":"Active: Pressure switch inhibits welding; safety valve on air accumulator relieves excess.","psm_critical":"Yes","ref":"NSEC Welder Manual"},
    {"sl":4,"param":"Pre-Primary Alkali Solution Temperature (NaOH)","uom":"deg C","soc_min":80,"soc_max":90,"sol_min":80,"sol_max":90,"sub_process":"Cleaning & Rinsing","equipment_linked":"Temperature indicator on HMI, steam control valve","identification_low":"Temperature indicator on HMI - below SOC","identification_high":"Temperature indicator on HMI - above SOC, auto-coolant at SOL","consequence_low":"Improper cleaning leading to patch marks - plating defects.","consequence_high":"Burning marks causing matted strip surface - HHO event (NaOH boiling/steam/alkali burns).","action_low":"Admin: Monitor temperature per SOP CLN-01. Adjust steam valve.","action_high":"Active: Auto-bath off at SOL. Admin: Investigate steam control valve.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":5,"param":"Pre-Primary Alkali Solution Concentration (NaOH)","uom":"g/L","soc_min":25,"soc_max":30,"sol_min":25,"sol_max":30,"sub_process":"Cleaning & Rinsing","equipment_linked":"NaOH dosing system, lab test station","identification_low":"Lab test report - below SOC","identification_high":"Lab test report - above SOC","consequence_low":"Improper cleaning causing patch marks - product downgrade.","consequence_high":"Solution carryover causing surface defects - drag-out / WTP load.","action_low":"Admin: Adjust concentration per SOP CLN-02. Chemical dosing correction.","action_high":"Admin: Immediate corrective action based on lab feedback.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":6,"param":"Primary Alkali Solution Temperature (NaOH)","uom":"deg C","soc_min":80,"soc_max":90,"sol_min":80,"sol_max":90,"sub_process":"Cleaning & Rinsing","equipment_linked":"Temperature indicator on HMI, steam control valve","identification_low":"Temperature indicator on HMI - below SOC","identification_high":"Temperature indicator on HMI - above SOC","consequence_low":"Incomplete removal of contaminants - plating pinholes.","consequence_high":"Burning and matted strip surface - HHO event.","action_low":"Admin: Monitor temperature per SOP CLN-03. Adjust steam valve.","action_high":"Active: Steam flow through control valve regulated; temperature control with alarm.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":7,"param":"Primary Alkali Solution Concentration (NaOH)","uom":"g/L","soc_min":25,"soc_max":30,"sol_min":25,"sol_max":30,"sub_process":"Cleaning & Rinsing","equipment_linked":"NaOH dosing, conductivity analyser","identification_low":"Conductivity alarm - below SOC","identification_high":"Conductivity alarm - above SOC","consequence_low":"Poor cleaning of strip - chemical patches and surface defects.","consequence_high":"Excess drag-out - WTP overload.","action_low":"Admin: Correct chemical strength per SOP CLN-04. Dose correction.","action_high":"Admin: Reduce dosing. Verify by lab titration every shift.","psm_critical":"No","ref":"WEAN United Process Norms"},
    {"sl":8,"param":"Primary Cleaning Current","uom":"kA","soc_min":2.5,"soc_max":3.5,"sol_min":2.5,"sol_max":3.5,"sub_process":"Cleaning & Rinsing","equipment_linked":"DC rectifier, PLC/HMI current display, overcurrent relay","identification_low":"PLC / HMI current display - below SOC","identification_high":"PLC / HMI current display - above SOC, PLC-limited total current","consequence_low":"Ineffective electrolytic cleaning - contamination, plating pinholes.","consequence_high":"Burning leading to strip breakage - line stoppage / H2 over-evolution at cathode.","action_low":"Admin: Adjust current per SOP CLN-05.","action_high":"Active: PLC interlock restricts over-current. Admin: Stop process per SOP CLN-05 and investigate.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":9,"param":"Secondary Alkali Solution Temperature (NaOH)","uom":"deg C","soc_min":80,"soc_max":90,"sol_min":80,"sol_max":90,"sub_process":"Cleaning & Rinsing","equipment_linked":"Temperature indicator on HMI, steam control valve","identification_low":"Temperature indicator on HMI - below SOC","identification_high":"Temperature indicator on HMI - above SOC","consequence_low":"Improper final cleaning - residual contaminants on strip.","consequence_high":"Burning marks on strip - product reject / HHO event.","action_low":"Admin: Monitor temperature per SOP CLN-06. Adjust steam valve.","action_high":"Active: Temperature alarm and control loop adjusts steam valve.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":10,"param":"Secondary Alkali Solution Concentration (NaOH)","uom":"g/L","soc_min":25,"soc_max":30,"sol_min":25,"sol_max":30,"sub_process":"Cleaning & Rinsing","equipment_linked":"NaOH dosing, lab test station","identification_low":"Lab test report - below SOC","identification_high":"Lab test report - above SOC","consequence_low":"Inadequate cleaning - solution patches and surface defects.","consequence_high":"Solution patches and surface defects from excess concentration.","action_low":"Admin: Adjust solution strength per SOP CLN-07. Chemical dosing.","action_high":"Admin: Corrective action on deviation, shift-wise lab testing.","psm_critical":"No","ref":"WEAN United Process Norms"},
    {"sl":11,"param":"Secondary Cleaning Current","uom":"kA","soc_min":2.5,"soc_max":3.5,"sol_min":2.5,"sol_max":3.5,"sub_process":"Cleaning & Rinsing","equipment_linked":"DC rectifier, PLC/HMI current display","identification_low":"PLC / HMI current display - below SOC","identification_high":"PLC / HMI current display - above SOC, PLC current limitation","consequence_low":"Poor electrolytic cleaning - contamination carries to plating.","consequence_high":"Burning and strip breakage - line stoppage.","action_low":"Admin: Current adjustment per SOP CLN-08.","action_high":"Active: PLC over-current interlock. Admin: Stop process per SOP CLN-08.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":12,"param":"Pickling Acid Solution Concentration (H2SO4)","uom":"g/L","soc_min":8,"soc_max":10,"sol_min":8,"sol_max":10,"sub_process":"Cleaning & Rinsing","equipment_linked":"H2SO4 dosing, concentration analyser","identification_low":"Lab test report - below SOC","identification_high":"Lab test report - above SOC","consequence_low":"Improper removal of iron oxide - surface corrosion and defects.","consequence_high":"Over-pickling - H2 gas spike, acid mist, equipment corrosion.","action_low":"Admin: Adjust acid strength per SOP PKL-01. Chemical dosing.","action_high":"Admin: Dilute bath. Lab testing every shift, immediate corrective action.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":13,"param":"Sn++ Concentration in Plating Solution (SnSO4)","uom":"g/L","soc_min":26,"soc_max":32,"sol_min":"<26","sol_max":">32","sub_process":"Tin Plating","equipment_linked":"Sn analyser, anode system, lab test station","identification_low":"Lab test value - below SOC (twice per shift)","identification_high":"Lab test value - above SOC","consequence_low":"Improper tin coating on sheet - underplating, product reject.","consequence_high":"Loss of tin / over-coating on sheet - cost loss, specification breach.","action_low":"Admin: Adjust SnSO4 dosing per SOP PLT-01.","action_high":"Admin: Reduce/add make-up per SOP PLT-01. Immediate corrective action after lab feedback.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":14,"param":"Free Acid Concentration (Plating Bath)","uom":"g/L","soc_min":13,"soc_max":16,"sol_min":"<13","sol_max":">16","sub_process":"Tin Plating","equipment_linked":"Acid analyser, H2SO4 dosing","identification_low":"Lab test value - below SOC","identification_high":"Lab test value - above SOC","consequence_low":"Product degradation due to SCO / patch - low conductivity, dull patches.","consequence_high":"Product downgrade due to surface defect - excess acid mist, TLV breach.","action_low":"Admin: Adjust acid dosing per SOP PLT-02. Correct bath chemistry.","action_high":"Admin: Immediate chemical correction. Routine lab testing each shift.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":15,"param":"ENSA Concentration","uom":"g/L","soc_min":3,"soc_max":6,"sol_min":"<3","sol_max":">6","sub_process":"Tin Plating","equipment_linked":"ENSA dosing, lab test station","identification_low":"Lab test report - below SOC","identification_high":"Lab test report - above SOC","consequence_low":"Dull band formation - product downgrade.","consequence_high":"Product downgrade due to dull band from excess additive.","action_low":"Admin: Adjust ENSA addition per SOP PLT-03.","action_high":"Admin: Immediate corrective dosing. Lab test every shift.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":16,"param":"Sn++ : Free Acid Ratio","uom":"Ratio","soc_min":1.95,"soc_max":2.05,"sol_min":"<1.90","sol_max":">2.10","sub_process":"Tin Plating","equipment_linked":"Lab calculation from Sn and acid test results","identification_low":"Calculated from lab results - below SOC","identification_high":"Calculated from lab results - above SOC","consequence_low":"Dull band on strip - product downgrade due to surface defect.","consequence_high":"Dull band on strip - product downgrade due to surface defect.","action_low":"Admin: Adjust Sn / acid per SOP PLT-04.","action_high":"Admin: Correct ratio per SOP PLT-04. Ratio monitoring via lab test.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":17,"param":"Sulphate (SO4 2-) Concentration","uom":"g/L","soc_min":"-","soc_max":12,"sol_min":"-","sol_max":">15","sub_process":"Tin Plating","equipment_linked":"Lab test station, bleed & make-up system","identification_low":"Lab test report","identification_high":"Lab test report - above SOC","consequence_low":"No immediate consequence.","consequence_high":"Dull band formation from excess sulphate.","action_low":"Admin: Monitor sulphate level per SOP PLT-05.","action_high":"Admin: Bleed & make-up per SOP PLT-05. Bath correction based on test.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":18,"param":"Total Iron Concentration (Plating Bath)","uom":"g/L","soc_min":"-","soc_max":20,"sol_min":"-","sol_max":">25","sub_process":"Tin Plating","equipment_linked":"Lab test station, bath treatment system","identification_low":"Lab test report","identification_high":"Lab test report - above SOC","consequence_low":"Healthy solution - no effect.","consequence_high":"Deterioration of plating chemistry - product quality risk.","action_low":"Admin: Monitor iron content per SOP PLT-06.","action_high":"Admin: Bath treatment per SOP PLT-06. Corrective treatment based on result.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":19,"param":"Stannous to Free Acid Ratio (PSA)","uom":"g/L","soc_min":"-","soc_max":3,"sol_min":"-","sol_max":">3","sub_process":"Tin Plating","equipment_linked":"Lab test station","identification_low":"Lab test report","identification_high":"Lab test report - above SOC","consequence_low":"Healthy solution.","consequence_high":"Poor surface finish - product downgrade due to surface defect.","action_low":"Admin: Monitor PSA ratio per SOP PLT-07.","action_high":"Admin: Chemistry correction per SOP PLT-07. Shift-wise lab testing.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":20,"param":"Reflow Current","uom":"A","soc_min":1000,"soc_max":10000,"sol_min":1000,"sol_max":10000,"sub_process":"Reflow Furnace","equipment_linked":"PLC/HMI current display, line speed and tin melting control","identification_low":"PLC / HMI current display - below SOC","identification_high":"PLC / HMI current display - above SOC, auto interlock via reflow temperature","consequence_low":"Tin melting will not take place - dull coating, reject.","consequence_high":"Burning of strip leading to strip breakage - line shutdown, H2 fire risk.","action_low":"Admin: Adjust line speed per SOP RFL-01.","action_high":"Active: Reduce current or stop line per SOP RFL-01. Auto interlock through reflow temperature.","psm_critical":"Yes","ref":"WEAN United User Manual"},
    {"sl":21,"param":"Quench Temperature","uom":"deg C","soc_min":50,"soc_max":65,"sol_min":50,"sol_max":65,"sub_process":"Reflow Furnace","equipment_linked":"Temperature sensor on HMI, ICW inlet control valve","identification_low":"Temperature sensor on HMI - below SOC","identification_high":"Temperature sensor on HMI - above SOC","consequence_low":"Product degradation due to cold quench - shape defects, tin coating cracks.","consequence_high":"Product degradation due to hot quench - incomplete solidification, appearance defects.","action_low":"Admin: Adjust ICW inlet valve per SOP QCH-01.","action_high":"Active: Temperature feedback control through PLC adjusts ICW flow per SOP QCH-01.","psm_critical":"Yes","ref":"WEAN United User Manual"},
    {"sl":22,"param":"Strip Temperature (Reflow Exit)","uom":"deg C","soc_min":232,"soc_max":270,"sol_min":232,"sol_max":270,"sub_process":"Reflow Furnace","equipment_linked":"Strip pyrometer (PSCE #1), line speed / furnace power control","identification_low":"Strip pyrometer reading - below SOC","identification_high":"Strip pyrometer reading - above SOC, pyrometer-based interlock and alarm","consequence_low":"Tin melting will not take place - dull coating, Fe-Sn alloy not formed, REJECT.","consequence_high":"Burning of strip leading to strip breakage - conductor roll damage, H2 fire risk, SHUTDOWN.","action_low":"Admin: Adjust line speed / furnace power per SOP RFL-02.","action_high":"Active: Pyrometer-based interlock and alarm. Reduce power or stop line per SOP RFL-02.","psm_critical":"Yes","ref":"WEAN United User Manual"},
    {"sl":23,"param":"Chemical Treatment Solution Concentration","uom":"deg C","soc_min":80,"soc_max":90,"sol_min":80,"sol_max":90,"sub_process":"Chemical Treatment","equipment_linked":"Temperature indication on HMI, steam flow control valve","identification_low":"Temperature indication on HMI - below SOC","identification_high":"Temperature indication on HMI - above SOC","consequence_low":"Improper cleaning of strip causing patches - poor chromate coating.","consequence_high":"Burning marks leading to matted strip surface.","action_low":"Admin: Monitor solution heating per SOP CHT-01.","action_high":"Active: Steam flow regulated through control valve. Temperature monitoring with alarm.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":24,"param":"Chemical Treatment Solution Temperature","uom":"deg C","soc_min":40,"soc_max":45,"sol_min":40,"sol_max":45,"sub_process":"Chemical Treatment","equipment_linked":"TT-ChemTx, LEV","identification_low":"Temperature indicator / HMI - below SOC","identification_high":"Auto-bath off at 45 deg C SOL - CRITICAL Cr-VI volatilisation","consequence_low":"Less chromium coating on strip causing poor corrosion protection.","consequence_high":"Cr-VI mist surge - TLV breach - MANDATORY SHUTDOWN per MSIHC 1989.","action_low":"Admin: Monitor bath temperature per SOP CHT-02. Adjust heating.","action_high":"Active: Bath auto-off at SOL. Air monitor check. SHUTDOWN if >0.05 mg/m3 (per old TLV reference, updated to 0.01 mg/m3 ACGIH 2023).","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":25,"param":"Chemical Treatment Current","uom":"A","soc_min":300,"soc_max":2000,"sol_min":300,"sol_max":3500,"sub_process":"Chemical Treatment","equipment_linked":"Rectifier, PLC/HMI current display","identification_low":"PLC / HMI current display - below SOC","identification_high":"PLC / HMI current display - above SOC, PLC-based current limitation","consequence_low":"Insufficient passivation - corrosion failure, food safety risk.","consequence_high":"Insufficient chromium layer leading to defects - Cr-VI reduction to Cr-III, bath balance upset.","action_low":"Admin: Adjust line speed per SOP CHT-03.","action_high":"Active: PLC-based current limitation. Admin: Investigate, adjust current via PLC per SOP CHT-03.","psm_critical":"Yes","ref":"WEAN United Process Norms"},
    {"sl":26,"param":"Compressed Air Flow to Trion Oiler (Primary Air)","uom":"kg/cm2","soc_min":0.5,"soc_max":1,"sol_min":0.5,"sol_max":1,"sub_process":"Electrostatic Oiling","equipment_linked":"Trion Oiler, digital pressure display, air regulator","identification_low":"Digital pressure display - below SOC","identification_high":"Digital pressure display - above SOC","consequence_low":"Non-uniform oil coating due to improper atomisation - corrosion protection risk.","consequence_high":"Excess oil coating causing smudge band and surface defects.","action_low":"Admin: Adjust air regulator per SOP OIL-01.","action_high":"Admin: Correct air supply per SOP OIL-01. Manual air pressure regulation.","psm_critical":"Yes","ref":"Trion Inc., USA User Manual"},
    {"sl":27,"param":"Air Flow to Trion Oiler (Secondary Air)","uom":"mm WC","soc_min":60,"soc_max":300,"sol_min":60,"sol_max":300,"sub_process":"Electrostatic Oiling","equipment_linked":"Trion Oiler, air flow indicator, line speed feedback","identification_low":"Air flow indicator - below SOC","identification_high":"Air flow indicator - above SOC","consequence_low":"Non-uniform oil coating due to low secondary air - corrosion protection risk.","consequence_high":"Excess air flow causing oil loss and coating defects.","action_low":"Admin: Adjust air flow via PLC per SOP OIL-02.","action_high":"Active: Auto control through line speed feedback per SOP OIL-02.","psm_critical":"Yes","ref":"Trion Inc., USA User Manual"},
    {"sl":28,"param":"Repelling Plate Voltage","uom":"kV","soc_min":-10,"soc_max":-40,"sol_min":-10,"sol_max":-50,"sub_process":"Electrostatic Oiling","equipment_linked":"Voltage controller, electrostatic oiling plates","identification_low":"Voltage controller display - below SOC magnitude","identification_high":"Voltage controller display - above SOC magnitude","consequence_low":"Low DOS coating and oil loss - corrosion protection risk.","consequence_high":"Excess coating causing smudge band and surface defects.","action_low":"Admin: Adjust voltage based on QA feedback.","action_high":"Admin: Rectify voltage to avoid excess coating based on QA feedback.","psm_critical":"Yes","ref":"Trion Inc., USA User Manual"},
]

ETL1_EDB = [
    {"sl":1,"sub_process":"Furnace - Propane Line","hazardous_substance":"Propane Gas","equipment":"Main Strainer DN150 PN10","tag_no":"1.3","selection_basis":"Condition Based","manufacturer":"Steinhaus","model":"DN150 PN10","design_basis":"Strainer on propane supply to reflow furnace. Removes particles blocking burner nozzles. Blockage = flame-out = furnace atmosphere risk. DN150 rated for full propane flow.","consequence_of_failure":"Burner blockage -&gt; flame-out -&gt; furnace atmosphere deviation -&gt; H2 risk.","barrier_type":"Passive","barrier_effectiveness":"Continuous passive protection  -  always active.","is_psce":False},
    {"sl":2,"sub_process":"Furnace - Propane Line","hazardous_substance":"Propane Gas","equipment":"Pressure Switch IP54 PSAL 1.13","tag_no":"PSAL 1.13","selection_basis":"Annual calibration","manufacturer":"Dungs","model":"Pressure Switch IP54","design_basis":"Monitors propane supply pressure. Low pressure = burner flame-out. High pressure = overfiring. IP54 rated. Dungs certified for flammable gas. PLC interlock.","consequence_of_failure":"Propane pressure deviation undetected -&gt; burner flame-out or overfiring -&gt; H2 atmosphere risk.","barrier_type":"Active  -  Instrumented","barrier_effectiveness":"Primary propane pressure detection. Annual calibration essential.","is_psce":True},
    {"sl":3,"sub_process":"Furnace - Propane Line","hazardous_substance":"Propane Gas","equipment":"Solenoid Valve DN50 UV 1.21","tag_no":"UV 1.21","selection_basis":"6-monthly inspection","manufacturer":"Kromschroder","model":"Solenoid Valve DN50","design_basis":"SAFETY CRITICAL: auto propane shut-off on any safety signal. Fail-safe: closes on de-energise. Kromschroder certified EN 161. DN50 full propane flow.","consequence_of_failure":"Cannot auto shut-off propane -&gt; propane to unlit burners -&gt; fire/explosion.","barrier_type":"Active  -  Automatic Trip","barrier_effectiveness":"PRIMARY propane safety barrier  -  auto, fail-safe, no operator action needed.","is_psce":True},
    {"sl":4,"sub_process":"Furnace - H2 Line","hazardous_substance":"Hydrogen Gas","equipment":"H2 Pressure Switch PSAL 2.14","tag_no":"PSAL 2.14","selection_basis":"3-monthly calibration","manufacturer":"Dungs","model":"Pressure Switch","design_basis":"Monitors H2 supply pressure to reflow furnace. Low pressure = H2 loss = unsafe restart without purge. PLC interlock  -  auto-trip on low H2. Dungs H2-service certified.","consequence_of_failure":"H2 supply loss undetected -&gt; furnace atmosphere deviates -&gt; explosive atmosphere on restart.","barrier_type":"Active  -  Automatic Trip","barrier_effectiveness":"CRITICAL PSCE BARRIER  -  primary H2 supply failure detection. 3-monthly calibration.","is_psce":True},
    {"sl":5,"sub_process":"Furnace - N2 Line","hazardous_substance":"Nitrogen Gas","equipment":"N2 Pressure Switch PSAL 3.19","tag_no":"PSAL 3.19","selection_basis":"Annual calibration","manufacturer":"Dungs","model":"Pressure Switch IP54","design_basis":"Monitors N2 purge supply pressure. PLC interlock: H2 admission blocked if N2 unavailable. Critical for safe startup sequence.","consequence_of_failure":"N2 unavailability undetected -&gt; H2 admitted without purge -&gt; explosive atmosphere.","barrier_type":"Active  -  Instrumented","barrier_effectiveness":"Confirms N2 availability before H2 admission permitted.","is_psce":False},
    {"sl":6,"sub_process":"Furnace - Cooling Water","hazardous_substance":"Cooling Water","equipment":"ICW Pressure Switch PSAL 4.4","tag_no":"PSAL 4.4","selection_basis":"Annual calibration","manufacturer":"IFM","model":"Electronic Pressure Switch","design_basis":"Monitors ICW pressure to conductor rolls and quench. Low ICW = overheating = arc in H2 atmosphere.","consequence_of_failure":"ICW loss undetected -&gt; conductor roll overheating -&gt; arc -&gt; H2 fire.","barrier_type":"Active  -  Instrumented","barrier_effectiveness":"Early warning of cooling failure before roll damage.","is_psce":False},
    {"sl":7,"sub_process":"Furnace - H2 Purge","hazardous_substance":"Hydrogen Gas","equipment":"Gas Control & Safety Run","tag_no":"502.1","selection_basis":"3-yearly inspection","manufacturer":"Kromschroder/Dungs","model":"Gas Control & Safety Run","design_basis":"Combined gas safety controller  -  manages safe startup sequence for H2, propane, N2. Performs safety run checks before gas admission. EN 298 certified.","consequence_of_failure":"Gas startup without safe state verification -&gt; H2/propane admission unsafely.","barrier_type":"Active  -  Automatic Trip","barrier_effectiveness":"Orchestrates all gas safety startup  -  single point of safety coordination.","is_psce":True},
]

ETL1_CHEM_QUICKREF = {
    "A1  -  Sulphuric Acid (H2SO4)":      {"color":"#f97316","class":"Corrosive liquid, Oxidising agent","nfpa":"3-0-2(W)","tlv_twa":"1 mg/m3 (ACGIH 2023 - thoracic fraction, H2SO4 mist)"},
    "A2  -  Phenol Sulfonic Acid (PSA)":  {"color":"#eab308","class":"Corrosive liquid - p-hydroxybenzene sulphonic acid","nfpa":"3-1-0","tlv_twa":"Not established for PSA. Phenol component: 0.5 ppm (SKIN)"},
    "A3  -  Dioctyl Sebacate (DOS)":      {"color":"#22c55e","class":"Combustible liquid","nfpa":"1-1-0","tlv_twa":"10 mg/m3 (ACGIH PNOR inhalable)"},
    "A4  -  ENSA (Ethoxylated Naphthol Sulphonic Acid)": {"color":"#22c55e","class":"Proprietary plating brightener","nfpa":"2-1-1","tlv_twa":"Not established. Plating bath acid mist: 1 mg/m3 (as H2SO4)"},
    "A5  -  Sodium Dichromate (Na2Cr2O7)": {"color":"#ef4444","class":"CARCINOGEN (IARC Gr.1, ACGIH A1) - Oxidising solid, toxic","nfpa":"4-0-1 (OX)","tlv_twa":"0.01 mg/m3 as Cr(VI) (ACGIH A1)"},
    "A6  -  Chromic Acid (CrO3/Cr-VI)":   {"color":"#ef4444","class":"CARCINOGEN - Powerful oxidiser, corrosive, highly toxic","nfpa":"3-0-1 (OX)","tlv_twa":"0.05 mg/m3 as Cr (ACGIH)"},
    "H1  -  Hydrogen (H2)":   {"color":"#3b82f6","class":"Flammable gas, simple asphyxiant","nfpa":"4-0-0","tlv_twa":"Simple Asphyxiant - no OEL (LEL 4%, UEL 75%)"},
    "H2  -  Oxygen (O2)":     {"color":"#60a5fa","class":"Oxidiser, supports combustion","nfpa":"0-0-0 (OX)","tlv_twa":"Not established - oxygen enrichment hazard"},
    "H3  -  Nitrogen (N2)":   {"color":"#a78bfa","class":"Inert gas, simple asphyxiant","nfpa":"0-0-0","tlv_twa":"Simple Asphyxiant - no OEL (O2 displacement)"},
}

ETL1_PSCE = [
    {"sl":1,"equipment":"Pyrometer  -  Strip Temperature (Reflow)","tag":"Pyrometer ETL-1","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Reflow Furnace","sap_tag":"S-ETL-001","justification":"PRIMARY PSCE. Monitors strip temperature (SOC 232-270deg C). SOL 270deg C = auto-trip. Only continuous strip temperature measurement. 232deg C = tin melting point. Below -&gt; incomplete reflow. Above -&gt; strip burns.","consequence_of_failure":"Strip overheating undetected -&gt; strip burns -&gt; conductor roll damage -&gt; H2 fire risk.","maintenance":"3-monthly calibration. Annual blackbody reference calibration."},
    {"sl":2,"equipment":"H2 Pressure Switch PSAL 2.14","tag":"PSAL 2.14","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Reflow Furnace","sap_tag":"S-ETL-002","justification":"Monitors H2 supply to reflow furnace. H2 loss -&gt; furnace atmosphere compromised -&gt; explosive atmosphere on restart without purge.","consequence_of_failure":"Undetected H2 loss -&gt; unsafe restart -&gt; explosive atmosphere -&gt; explosion.","maintenance":"3-monthly calibration. Annual functional trip test."},
    {"sl":3,"equipment":"Propane Solenoid Valve UV 1.21","tag":"UV 1.21","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Reflow Furnace","sap_tag":"S-ETL-003","justification":"Auto propane shut-off on any safety signal. Fail-safe: closes on de-energise. EN 161 certified. Without this: propane cannot be auto-shut on trip.","consequence_of_failure":"Propane auto shut-off fails -&gt; continuing propane to unlit burners -&gt; explosion.","maintenance":"6-monthly inspection and functional test."},
    {"sl":4,"equipment":"Cr-VI Air Monitor (Chemical Treatment)","tag":"CrVI-Monitor","psce_type":"Prescriptive","category":"Safety Monitoring & Emergency Communication","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL-004","justification":"PRESCRIPTIVE per MSIHC Rules 1989. Continuous Cr-VI monitoring. TLV 0.05 mg/m3. IARC Group 1 carcinogen. Only warning of exposure. Alarm triggers mandatory evacuation.","consequence_of_failure":"Cr-VI exposure undetected -&gt; operators develop lung cancer (latency 10-30 years). Statutory violation.","maintenance":"Quarterly calibration. Monthly bump test. Annual NABL calibration."},
    {"sl":5,"equipment":"Chemical Treatment Bath Temperature Transmitter","tag":"TT-ChemTx","psce_type":"Consequence Based","category":"Instrumented Active Preventive","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL-005","justification":"Monitors Cr-VI bath temperature (SOC 40-45deg C, SOL 45deg C). Above 45deg C = Cr-VI volatilisation surge -&gt; TLV breach. Auto-bath shutdown at SOL.","consequence_of_failure":"Bath above 45deg C undetected -&gt; Cr-VI mist surge -&gt; carcinogen exposure -&gt; MSIHC violation.","maintenance":"6-monthly calibration. Functional test at SOL setpoint."},
    {"sl":6,"equipment":"LEV System  -  Chemical Treatment Bay","tag":"LEV-ChemTx","psce_type":"Consequence Based","category":"Active Mitigation","psm_critical":"Yes","sub_process":"Chemical Treatment","sap_tag":"S-ETL-006","justification":"LEV for Cr-VI bath enclosure. Min 0.5 m/s face velocity. Prevents Cr-VI mist escaping to plant. Interlocked  -  bath cannot run without LEV.","consequence_of_failure":"LEV failure -&gt; Cr-VI mist -&gt; area-wide carcinogen exposure -&gt; mandatory shutdown.","maintenance":"Monthly airflow measurement. Quarterly duct inspection. Annual commissioning test."},
]

ETL1_HOM_EXCEL = [
    (1, "Sulphuric Acid (H2SO4)", "-", "Reacts violently with water; reacts with metals forming hydrogen gas",
     "1 mg/m3", "3 mg/m3 (Ceiling)", "LC50 (Inhalation): 510 mg/m3; LD50 (Oral): 2140 mg/kg",
     "Not applicable", "290 deg C", "Not applicable", "Not applicable",
     "Highly corrosive; acid mist inhalation; severe chemical burns", "-"),
    (2, "Phenol Sulfonic Acid (PSA)", "-", "Reacts with strong bases; releases corrosive fumes on heating",
     "Not established", "Not established", "LC50 (Inhalation): 200 mg/L/48h; LD50 (Oral): 400-800 mg/kg",
     ">150 deg C", ">300 deg C (decomposes)", "Not established", "Not established",
     "Corrosive phenolic acid; toxic fumes; skin absorption hazard", "-"),
    (3, "Dioctyl Sebacate (DOS)", "-", "Chemically stable; incompatible with strong oxidizers",
     "Not established", "Not established", "LD50 (Oral): 900 mg/kg",
     "190 deg C", "428 deg C", "Not applicable", "Not applicable",
     "Combustible liquid; CO and CO2 released on burning", "-"),
    (4, "Ethoxylated Naphthol Sulphonic Acid (ENSA)", "-", "Incompatible with strong acids and alkalis",
     "Not established", "Not established", "Harmful by ingestion and inhalation; no numeric LD available",
     "~170 deg C", ">350 deg C (decomposes)", "Not established", "Not established",
     "Acidic surfactant; eye, skin and respiratory irritation", "-"),
    (5, "Sodium Dichromate (Na2Cr2O7)", "Oxidizer", "Strong oxidizer; reacts violently with organic material",
     "0.05 mg/m3", "Not established", "LC50 (Inhalation): 0.124 mg/L; LD50 (Oral): 50 mg/kg",
     "Not applicable", "Decomposes", "Not applicable", "Not applicable",
     "(Cr-VI); genetic toxicity; severe eye and skin damage", "-"),
    (6, "Chromic Acid (CrO3)", "Oxidizer", "Powerful oxidizing agent; explosive with organic matter",
     "0.05 mg/m3", "0.1 mg/m3 (Ceiling)", "Hexavalent chromium compound; highly toxic",
     "Not applicable", "Decomposes", "Not applicable", "Not applicable",
     "Carcinogenic; Cr-VI toxicity; severe chemical burns", "-"),
]

ETL1_PSCE_EXCEL = [
    (1, "Temp Ind Ent Hyd POR1", "No", "Yes", "No", "Yes", "Prevents overheating of hydraulic POR system"),
    (2, "Level Switch Ent Hyd POR2", "No", "Yes", "No", "Yes", "Prevents hydraulic oil level loss"),
    (3, "Level Switch Ent Hyd POR2 (LEVEL POR)", "No", "Yes", "No", "Yes", "Redundant level protection for POR"),
    (4, "Press Switch Welder Air", "No", "Yes", "No", "Yes", "Prevents welding failure due to air loss"),
    (5, "Flow Switch Up Welder Cool", "No", "Yes", "No", "Yes", "Ensures DM water flow to welder"),
    (6, "Flow Switch Mid Welder Cool", "No", "Yes", "No", "Yes", "Cooling flow continuity for welder"),
    (7, "Flow Switch Lo Welder Cool", "No", "Yes", "No", "Yes", "Prevents welder overheating"),
    (8, "Press Switch Welder Cool", "No", "Yes", "No", "Yes", "Cooling pressure protection"),
    (9, "Camera Contr Welder", "No", "Yes", "No", "Yes", "Monitoring of welding operation"),
    (10, "Entry Camera1 Welder", "No", "Yes", "No", "Yes", "Visual verification of weld quality"),
    (11, "Entry Camera2 Welder", "No", "Yes", "No", "Yes", "Redundant welding monitoring"),
    (12, "Exit Camera 1 Welder", "No", "Yes", "No", "Yes", "Detection of weld defects"),
    (13, "Exit Camera 2 Welder", "No", "Yes", "No", "Yes", "Redundant exit weld inspection"),
    (14, "I/P Conv Pri", "No", "Yes", "No", "Yes", "Accurate control valve positioning"),
    (15, "Control Val Pri", "No", "Yes", "No", "Yes", "Controls primary process flow"),
    (16, "Level Ind Pri", "No", "Yes", "No", "Yes", "Prevents overflow/dry running"),
    (17, "Level Trans Pri", "No", "Yes", "No", "Yes", "Continuous level monitoring"),
    (18, "I/P Conv Sec", "No", "Yes", "No", "Yes", "Valve actuation in secondary section"),
    (19, "Control Val Sec", "No", "Yes", "No", "Yes", "Controls secondary process parameters"),
    (20, "Level Ind Sec", "No", "Yes", "No", "Yes", "Prevents unsafe tank levels"),
    (21, "Level Trans Sec", "No", "Yes", "No", "Yes", "Continuous secondary level control"),
    (22, "Plating Temp I/P Conv Pla", "No", "Yes", "No", "Yes", "Controls plating temperature"),
    (23, "Control Val Pla", "No", "Yes", "No", "Yes", "Regulates plating bath"),
    (24, "Plating Level Ind Pla", "No", "Yes", "No", "Yes", "Prevents electrolyte overflow"),
    (25, "Level Trans Pla", "No", "Yes", "No", "Yes", "Continuous plating level monitoring"),
    (26, "I/P Conv Cooler", "No", "Yes", "No", "Yes", "Cooling control protection"),
    (27, "Control Val Cooler", "No", "Yes", "No", "Yes", "Controls cooler flow"),
    (28, "I/P Conv Chem", "No", "Yes", "No", "Yes", "Accurate chemical dosing"),
    (29, "Control Val Chem", "No", "Yes", "No", "Yes", "Prevents over‑dosing"),
    (30, "Level Ind Chem", "No", "Yes", "No", "Yes", "Chemical tank level safety"),
    (31, "Level Trans Chem", "No", "Yes", "No", "Yes", "Continuous chemical level monitoring"),
    (32, "Temp Contr Flux", "No", "Yes", "No", "Yes", "Prevents flux overheating"),
    (33, "Temp I/P Conv Flux", "No", "Yes", "No", "Yes", "Flux temperature regulation"),
    (34, "Control Val Flux", "No", "Yes", "No", "Yes", "Safe flux flow control"),
    (35, "Quench Temp I/P Conv Que", "No", "Yes", "No", "Yes", "Quench temperature control"),
    (36, "Control Val Water/Steam Que", "No", "Yes", "No", "Yes", "Controls quenching medium"),
    (37, "Contr Sec Air Oiler", "No", "Yes", "No", "Yes", "Ensures controlled lubrication air"),
    (38, "Control Val Oiler", "No", "Yes", "No", "Yes", "Prevents excess oiling"),
    (39, "I/P Conv Oiler", "No", "Yes", "No", "Yes", "Accurate oil control"),
    (40, "Port Valve Oiler", "No", "Yes", "No", "Yes", "Oil distribution control"),
    (41, "Port Valve Contr Oiler", "No", "Yes", "No", "Yes", "Controlled oil port operation"),
    (42, "Primary Air Contr Oiler", "No", "Yes", "No", "Yes", "Air supply regulation for oiler"),
    (43, "I/P Conv Steam", "No", "Yes", "No", "Yes", "Steam flow control"),
    (44, "Control Val Steam", "No", "Yes", "No", "Yes", "Prevents over‑pressure"),
    (45, "Level Trans Sump Ent", "No", "Yes", "No", "Yes", "Prevents sump overflow"),
    (46, "Level Contr Sump Ent", "No", "Yes", "No", "Yes", "Controls sump discharge"),
    (47, "Auto‑Man Sel Switch Sump Ent", "No", "Yes", "No", "Yes", "Safe manual override"),
    (48, "Level Trans Sump_Proc", "No", "Yes", "No", "Yes", "Process sump monitoring"),
    (49, "Level Contr Sump_Proc", "No", "Yes", "No", "Yes", "Prevents process flooding"),
    (50, "Level Trans Sump_Jyoti", "No", "Yes", "No", "Yes", "Jyoti sump protection"),
    (51, "Level Contr Sump_Jyoti", "No", "Yes", "No", "Yes", "Controlled sump pumping"),
    (52, "Auto‑Man Sel Switch Sump_Jyoti", "No", "Yes", "No", "Yes", "Emergency manual operation"),
    (53, "Press Switch (High) Lev Oil Mist Unit", "No", "Yes", "No", "Yes", "Over‑pressure protection"),
    (54, "Press Switch (Low) Lev Oil Mist Unit", "No", "Yes", "No", "Yes", "Lubrication failure prevention"),
    (55, "Oil Level Switch Lev Oil Mist Unit", "No", "Yes", "No", "Yes", "Prevents bearing damage"),
    (56, "Lube Oil Press Switch DDS", "No", "Yes", "No", "Yes", "Lubrication safety"),
    (57, "Lube Oil Temp Switch DDS", "No", "Yes", "No", "Yes", "Prevents oil overheating"),
    (58, "Top Flow Meter DDS", "No", "Yes", "No", "Yes", "Ensures flow to DDS"),
    (59, "Temp Trans Pri", "No", "Yes", "No", "Yes", "Primary temperature control"),
    (60, "Temp Trans Sec", "No", "Yes", "No", "Yes", "Secondary temperature control"),
    (61, "Temp Trans Plating", "No", "Yes", "No", "Yes", "Plating bath safety"),
    (62, "Temp Trans Cooler", "No", "Yes", "No", "Yes", "Cooling system protection"),
    (63, "Temp Trans Chem", "No", "Yes", "No", "Yes", "Prevents chemical overheating"),
    (64, "Temp Trans Quen", "No", "Yes", "No", "Yes", "Quench control"),
    (65, "Magnetic Flowmeter Electrolyte", "No", "Yes", "No", "Yes", "Electrolyte flow control"),
    (66, "DP Transm Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Prevents evaporator imbalance"),
    (67, "Vacuum Pressure Trans Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Prevents vacuum failure"),
    (68, "Process Controller 1 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Evaporator process control"),
    (69, "Process Controller 2 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Redundant control"),
    (70, "Process Controller 3 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Safe evaporation"),
    (71, "Process Controller 4 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Stability control"),
    (72, "Process Controller 5 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Prevents upset"),
    (73, "Process Controller 6 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Redundant safety control"),
    (74, "Process Controller 7 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Control reliability"),
    (75, "Process Controller 8 Evaporator ETL‑1", "No", "Yes", "No", "Yes", "Evaporator protection"),
    (76, "Welder Controller ETL‑1", "No", "Yes", "No", "Yes", "Welding process safety"),
    (77, "Pyrometer ETL‑1", "No", "Yes", "No", "Yes", "Reflow temperature protection"),
]
ETL1_EDB_EXCEL = [
    # Sub-process | HazSub | PSCE | Equipment | Tag No | SAP ID | Basis | Schedule | Manufacturer | Model | Ref Doc | Location | Remark
    # Sl | SubProcess | HazSub | PSCE | Tag | SAP | Basis | Sched | Mfr | Model | RefDoc | Loc | Remark
    (1,  "Furnace – Propane Line",    "Propane Gas",    "Yes", "1.3",               "901644", "Ensures clean propane supply; prevents fouling of downstream safety devices", "Condition Based",          "Steinhaus",            "Main Strainer DN150 PN10",        "Vendor Manual, FD",         "ETL-1", "Clean propane supply"),
    (2,  "Furnace – Propane Line",    "Propane Gas",    "Yes", "PSAL 1.13",         "900774", "Pressure protection to prevent unsafe propane pressure in furnace burners",   "Calibration once/year",    "Dungs",                "Pressure Switch IP54",            "Operating Manual",          "ETL-1", "PLC alarm"),
    (3,  "Furnace – Propane Line",    "Propane Gas",    "Yes", "PI 1.15",           "901047", "Local indication of propane pressure for safe operation",                     "Calibration once/year",    "Wika",                 "Capsule Gauge (Low Pressure)",    "Maintenance Checklist",     "ETL-1", "Local indication"),
    (4,  "Furnace – Propane Line",    "Propane Gas",    "Yes", "UV 1.21 / GOL 1.21","904704", "Safety shut-off of propane gas flow during abnormal furnace conditions",      "Every six months",         "Kromschröder",         "Solenoid Valve DN50",             "Vendor Manual, P&ID",       "ETL-1", "PLC feedback"),
    (5,  "Furnace – Propane Line",    "Propane Gas",    "Yes", "UV 1.22",           "904740", "Automated control of propane gas flow through PLC",                           "Every six months",         "Kromschröder",         "Solenoid Valve DN8",              "FD, Operating Manual",      "ETL-1", "PLC controlled"),
    (6,  "Furnace – Propane Line",    "Propane Gas",    "Yes", "1.23",              "900544", "Clean propane supply protection at base section",                             "Once in a year",           "Steinhaus",            "Base Strainer DN50",              "Maintenance Checklist",     "ETL-1", "Clean supply"),
    (7,  "Furnace – Propane Line",    "Propane Gas",    "Yes", "1.24",              "900545", "Safe propane gas transfer connection to furnace system",                      "Every six months",         "—",                    "Coupling DN50",                   "Vendor Manual",             "ETL-1", "Safe transfer"),
    (8,  "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "2.3",               "900147", "Prevents particulate contamination in hydrogen supply",                       "Condition Based",          "Steinhaus",            "Strainer DN80 PN10",              "FD",                        "ETL-1", "Prevent contamination"),
    (9,  "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "PC 2.6",            "904470", "Controls hydrogen pressure to prevent explosion risk",                        "Condition Based",          "RMG",                  "Pressure Control Device",         "Operating Manual",          "ETL-1", "Flow indication on HMI"),
    (10, "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "PZ 2.10",           "900009", "Over-pressure protection for hydrogen system",                               "Condition Based",          "Kromschröder",         "Safety Relief Valve",             "Vendor Manual",             "ETL-1", "Over-pressure protection"),
    (11, "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "PSAL 2.14",         "900279", "Low/high hydrogen pressure protection with PLC interlock",                   "Every three months",       "Dungs",                "Pressure Switch",                 "Maintenance Checklist",     "ETL-1", "PLC interlock"),
    (12, "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "H 2.15",            "900155", "Isolation and indication of hydrogen pressure at field",                      "Calibration once/year",    "Wika",                 "Isolation Valve",                 "FD",                        "ETL-1", "Isolation & indication"),
    (13, "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "PI 2.16",           "901338", "Continuous hydrogen pressure monitoring",                                     "Calibration once/year",    "Wika",                 "Capsule Gauge",                   "Operating Manual",          "ETL-1", "Continuous monitoring"),
    (14, "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "FTIR 2.31",         "904254", "Measurement of hydrogen flow to prevent unsafe furnace atmosphere",           "Calibration once/year",    "Endress & Hauser",     "DP Transmitter Cerabar",          "Vendor Manual",             "ETL-1", "PLC alarm"),
    (15, "Furnace – Hydrogen Line",   "Hydrogen Gas",   "Yes", "TIR 2.32",          "903137", "Monitoring hydrogen temperature to prevent abnormal furnace conditions",      "Calibration once/year",    "Reckmann",             "Temp Sensor PT-100",              "Maintenance Checklist",     "ETL-1", "PLC alarm"),
    (16, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "3.2",               "902078", "Ensures clean nitrogen supply to maintain inert furnace atmosphere",          "Condition Based",          "Steinhaus",            "Strainer DN100",                  "FD",                        "ETL-1", "Clean supply"),
    (17, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "PC 3.6",            "904576", "Controls nitrogen pressure to avoid loss of furnace inerting",               "Condition Based",          "Medenus",              "Pressure Control Device",         "Operating Manual",          "ETL-1", "Pressure control"),
    (18, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "PZ 3.15",           "900009", "Over-pressure relief to prevent nitrogen line rupture",                      "Condition Based",          "Kromschröder",         "Safety Relief Valve",             "Vendor Manual",             "ETL-1", "Over-pressure relief"),
    (19, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "PSAL 3.19",         "900171", "Pressure protection and interlock for nitrogen supply",                       "Once in a year",           "Dungs",                "Pressure Switch IP54",            "Maintenance Checklist",     "ETL-1", "PLC interlock"),
    (20, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "H 3.20",            "900155", "Isolation and monitoring of nitrogen pressure",                               "Calibration once/year",    "Wika",                 "Isolation Valve",                 "FD",                        "ETL-1", "Isolation & monitoring"),
    (21, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "PSAL 3.24",         "901467", "Redundant nitrogen pressure monitoring for safe furnace operation",           "Once in a year",           "IFM",                  "Electronic Pressure Switch",      "Operating Manual",          "ETL-1", "Redundant monitoring"),
    (22, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "FTIR 3.31",         "904254", "Flow monitoring to prevent nitrogen starvation of furnace",                  "Calibration once/year",    "Endress & Hauser",     "DP Transmitter",                  "Vendor Manual",             "ETL-1", "Flow monitoring"),
    (23, "Furnace – Nitrogen Line",   "Nitrogen Gas",   "Yes", "TIR 3.36",          "904892", "Temperature monitoring to ensure stable nitrogen conditions",                 "Once in a year",           "Reckmann",             "Temp Sensor PT-100",              "Maintenance Checklist",     "ETL-1", "Stable conditions"),
    (24, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "4.2",               "901704", "Prevents particulate ingress into cooling water system",                      "Once in a year",           "Steinhaus",            "Strainer DN350",                  "FD",                        "ETL-1", "Prevents particulate ingress"),
    (25, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "PSAL 4.4",          "901467", "Pressure protection to ensure coolant availability",                          "Once in a year",           "IFM",                  "Electronic Pressure Switch",      "Operating Manual",          "ETL-1", "PLC alarm"),
    (26, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "PI 4.6",            "900179", "Local indication of ICW pressure",                                           "Once in a year",           "Wika",                 "Diaphragm Gauge",                 "Vendor Manual",             "ETL-1", "Local indication"),
    (27, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "4.8",               "900365", "Ensures clean emergency cooling water supply",                               "Once in a year",           "Steinhaus",            "Emergency Strainer",              "Test Certificate",          "ETL-1", "Emergency supply"),
    (28, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "4.4",               "901467", "ICW pressure feedback to prevent furnace overheating",                       "Once in a year",           "IFM",                  "Electronic Pressure Switch",      "Operating Manual",          "ETL-1", "ICW feedback"),
    (29, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "H 4.5",             "900155", "Isolation of ICW pressure gauge",                                            "Calibration once/year",    "Wika",                 "Isolation Valve",                 "Maintenance Checklist",     "ETL-1", "Gauge isolation"),
    (30, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "PI 4.6",            "900179", "Local ICW pressure display for operation safety",                            "Once in a year",           "Wika",                 "Pressure Gauge (Diaphragm)",      "Vendor Manual",             "ETL-1", "Local ICW display"),
    (31, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "4.8",               "900365", "Ensures clean emergency cooling water supply (DN125)",                       "Once in a year",           "Steinhaus",            "Emergency Strainer DN125",        "Test Certificate",          "ETL-1", "Emergency supply"),
    (32, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "PSAL 4.10",         "901467", "Emergency water pressure monitoring with PLC interlock",                     "Once in a year",           "IFM",                  "Electronic Pressure Switch",      "FD",                        "ETL-1", "PLC interlock"),
    (33, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "H 4.11",            "900155", "Isolation valve for emergency pressure gauge",                               "Calibration once/year",    "Wika",                 "Isolation Valve",                 "Operating Manual",          "ETL-1", "Emergency isolation"),
    (34, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "PI 4.12",           "900179", "Emergency cooling water pressure indication",                                "Once in a year",           "Wika",                 "Pressure Gauge",                  "Vendor Manual",             "ETL-1", "Emergency indication"),
    (35, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "PSAL 4.10",         "901467", "Pressure protection for emergency cooling water availability",               "Once in a year",           "IFM",                  "Electronic Pressure Switch",      "Operating Manual",          "ETL-1", "PLC alarm"),
    (36, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "H 4.11",            "900155", "Isolation of emergency water pressure instrumentation",                      "Calibration once/year",    "Wika",                 "Isolation Valve",                 "FD",                        "ETL-1", "Isolation"),
    (37, "Furnace – Cooling Water",   "Cooling Water",  "Yes", "PI 4.12",           "900179", "Local display of emergency cooling water pressure",                          "Once in a year",           "Wika",                 "Pressure Gauge",                  "Vendor Manual",             "ETL-1", "Local display"),
    (38, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "6.2",               "900502", "Ensures unidirectional pneumatic flow",                                      "Once in a year",           "Krombach",             "Safety Check Valve",              "FD",                        "ETL-1", "Unidirectional flow"),
    (39, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "6.2",               "900502", "Prevents back-flow hazards in pneumatic system",                             "Once in a year",           "Krombach",             "Safety Check Valve DN15",         "Maintenance Checklist",     "ETL-1", "Prevent back-flow"),
    (40, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "PSAL 6.4",          "901467", "Pneumatic pressure protection and PLC interlock",                            "Once in a year",           "IFM",                  "Electronic Pressure Switch",      "FD",                        "ETL-1", "PLC interlock"),
    (41, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "H 6.5",             "900155", "Isolation of pneumatic pressure gauge",                                      "Calibration once/year",    "Wika",                 "Isolation Valve",                 "Operating Manual",          "ETL-1", "Gauge isolation"),
    (42, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "PI 6.6",            "900227", "Local pressure display for pneumatic system",                                "Once in a year",           "Wika",                 "Pressure Gauge (Diaphragm)",      "Vendor Manual",             "ETL-1", "Local display"),
    (43, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "6.2",               "900502", "Prevents reverse flow in pneumatic system",                                  "Once in a year",           "Krombach",             "Safety Check Valve",              "FD",                        "ETL-1", "Prevent reverse flow"),
    (44, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "PSAL 6.4",          "901467", "Pneumatic pressure feedback for PLC interlock",                              "Once in a year",           "IFM",                  "Electronic Pressure Switch",      "Operating Manual",          "ETL-1", "PLC interlock"),
    (45, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "H 6.5",             "900155", "Isolating valve for pneumatic pressure gauge",                               "Calibration once/year",    "Wika",                 "Isolation Valve",                 "Maintenance Checklist",     "ETL-1", "Gauge isolation"),
    (46, "Furnace – Pneumatic Line",  "Nitrogen / Air", "Yes", "PI 6.6",            "900227", "Local pneumatic pressure indication",                                        "Once in a year",           "Wika",                 "Pressure Gauge",                  "Vendor Manual",             "ETL-1", "Local indication"),
    (47, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "H 201",             "900228", "Protects against hydraulic over-pressure",                                   "Once in a year",           "Bosch Rexroth",        "High Pressure Valve",             "Operating Manual",          "ETL-1", "Over-pressure protection"),
    (48, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "H 201",             "900228", "High-pressure protection for hydraulic system",                              "Once in a year",           "Bosch Rexroth",        "High Pressure Valve",             "FD",                        "ETL-1", "High-pressure protection"),
    (49, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "202",               "900229", "Prevents reverse flow in hydraulic circuit",                                 "Once in a year",           "Bosch Rexroth",        "Non-Return Valve",                "Operating Manual",          "ETL-1", "Reverse flow prevention"),
    (50, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "UV 203",            "904587", "Controls clamping system pressure and safety",                               "Once in 3 years",          "NIVEG",                "Hydraulic Control Block",         "Vendor Manual",             "ETL-1", "Clamping safety"),
    (51, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "204.1-4",           "901738", "Safe clamping and de-clamping during furnace operation",                     "Once in a year",           "AZB Hydraulik",        "Swing Clamp Cylinder",            "Test Certificate",          "ETL-1", "Safe clamping"),
    (52, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "H 208",             "900228", "High-pressure protection for hydraulic piping",                              "Once in a year",           "Bosch Rexroth",        "High Pressure Valve",             "Maintenance Checklist",     "ETL-1", "Pressure switch"),
    (53, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "H 209",             "900228", "Redundant high-pressure hydraulic protection",                               "Once in a year",           "Bosch Rexroth",        "High Pressure Valve",             "FD",                        "ETL-1", "Redundant protection"),
    (54, "Furnace – Hydraulic Line",  "Hydraulic Oil",  "Yes", "211",               "900235", "Safe hydraulic oil flow under pressure",                                     "Once in a year",           "Bosch Rexroth",        "High Pressure Valve (Hose)",      "Operating Manual",          "ETL-1", "Safe oil flow"),
    (55, "Furnace – N₂ Purge Line",   "Nitrogen Gas",   "Yes", "UV 409",            "900243", "Provides nitrogen purge for furnace safety during abnormal conditions",      "Once in a year",           "Kromschröder",         "Solenoid Valve",                  "Vendor Manual",             "ETL-1", "Purge safety"),
    (56, "Furnace – N₂ Purge Line",   "Nitrogen Gas",   "Yes", "UV 411",            "900567", "Controlled nitrogen inlet for purge operations",                             "Once in a year",           "Bürkert",              "Globe Valve with Actuator",       "FD",                        "ETL-1", "Controlled inlet"),
    (57, "Furnace – N₂ Purge Line",   "Nitrogen Gas",   "Yes", "FE 412",            "901910", "Creates controlled pressure drop for safe nitrogen purging",                 "Once in a year",           "Dosch",                "Throttle Orifice",                "Test Certificate",          "ETL-1", "Pressure drop"),
    (58, "Furnace – N₂ Purge Line",   "Nitrogen / H₂",  "Yes", "FQIR 413",          "904443", "Measurement of purge gas flow for safety control",                           "Once in a year",           "Actaris",              "Impeller Flow Meter",             "Operating Manual",          "ETL-1", "Purge flow measurement"),
    (59, "Furnace – N₂ Purge Line",   "Nitrogen Gas",   "Yes", "414.1",             "901608", "Protects flow meter from particulate contamination",                         "Once in a year",           "Actaris",              "Strainer (Flat)",                 "Vendor Manual",             "ETL-1", "Protects flow meter"),
    (60, "Furnace – N₂ Purge Line",   "Nitrogen Gas",   "Yes", "416",               "900446", "Prevents reverse purge gas flow",                                            "Once in a year",           "Gestra",               "Non-Return Valve",                "FD",                        "ETL-1", "Prevent reverse flow"),
    (61, "Furnace – H₂ Purge Line",   "Hydrogen Gas",   "Yes", "502.1",             "901610", "Safe hydrogen purge and shutdown during furnace upset",                      "Once in 3 years",          "Kromschröder / Dungs", "Gas Control & Safety Run Unit",   "Test Certificate",          "ETL-1", "Safe purge & shutdown"),
    (62, "Furnace – H₂ Purge Line",   "Hydrogen Gas",   "Yes", "PC 502.2",          "900256", "Controls hydrogen pressure during purge operations",                         "Once in a year",           "Dungs",                "Pressure Regulator",              "Operating Manual",          "ETL-1", "Pressure control"),
    (63, "Furnace – H₂ Purge Line",   "Hydrogen Gas",   "Yes", "UV 504.1 / GOHL 504.1","901494","Hydrogen isolation and safety shut-off",                                    "Once in a year",           "Kromschröder",         "Solenoid Valve",                  "Vendor Manual",             "ETL-1", "Isolation & shut-off"),
    (64, "Furnace – H₂ Purge Line",   "Hydrogen Gas",   "Yes", "UV 504.2 / GOHL 504.2","901494","Redundant hydrogen shut-off for purge safety",                              "Once in a year",           "Kromschröder",         "Solenoid Valve DN25",             "FD",                        "ETL-1", "Redundant shut-off"),
    (65, "Furnace – Hyd. Oil Line 2", "Hydraulic Oil",  "Yes", "H 201",             "900228", "Protects hydraulic system from over-pressure",                               "Once in a year",           "Bosch Rexroth",        "High Pressure Valve",             "FD",                        "ETL-1", "Over-pressure protection"),
    (66, "Furnace – Hyd. Oil Line 2", "Hydraulic Oil",  "Yes", "202",               "900229", "Prevents reverse hydraulic flow",                                            "Once in a year",           "Bosch Rexroth",        "Non-Return Valve",                "Operating Manual",          "ETL-1", "Reverse flow prevention"),
    (67, "Furnace – Hyd. Oil Line 2", "Hydraulic Oil",  "Yes", "UV 203",            "904587", "Controls hydraulic clamping system pressure",                                "Once in 3 years",          "NIVEG",                "Hydraulic Control Block",         "Vendor Manual",             "ETL-1", "Clamping safety"),
    (68, "Furnace – Hyd. Oil Line 2", "Hydraulic Oil",  "Yes", "204.1-4",           "901738", "Safe clamping and de-clamping of cover",                                     "Once in a year",           "AZB Hydraulik",        "Swing Clamp Cylinder",            "Test Certificate",          "ETL-1", "Safe clamping"),
    (69, "Furnace – Hyd. Oil Line 2", "Hydraulic Oil",  "Yes", "H 208",             "900228", "High pressure protection for hydraulic piping",                              "Once in a year",           "Bosch Rexroth",        "High Pressure Valve",             "Maintenance Checklist",     "ETL-1", "Pressure switch"),
    (70, "Furnace – Hyd. Oil Line 2", "Hydraulic Oil",  "Yes", "H 209",             "900228", "Redundant hydraulic over-pressure protection",                               "Once in a year",           "Bosch Rexroth",        "High Pressure Valve",             "FD",                        "ETL-1", "Redundant protection"),
    (71, "Furnace – Hyd. Oil Line 2", "Hydraulic Oil",  "Yes", "211",               "900235", "Safe hydraulic oil flow under pressure",                                     "Once in a year",           "Parker",               "High Pressure Hose",              "Operating Manual",          "ETL-1", "Safe oil flow"),
    (72, "Furnace – N₂ Purge 2",      "Nitrogen Gas",   "Yes", "UV 409",            "900243", "Nitrogen purge initiation during unsafe conditions",                         "Once in a year",           "Kromschröder",         "Solenoid Valve",                  "Vendor Manual",             "ETL-1", "Purge initiation"),
    (73, "Furnace – N₂ Purge 2",      "Nitrogen Gas",   "Yes", "UV 411",            "900567", "Controlled nitrogen inlet for purging",                                      "Once in a year",           "Bürkert",              "Globe Valve with Actuator",       "FD",                        "ETL-1", "Controlled inlet"),
    (74, "Furnace – N₂ Purge 2",      "Nitrogen / H₂",  "Yes", "FQIR 413",          "904443", "Monitoring nitrogen / hydrogen purge flow",                                  "Once in a year",           "Actaris",              "Impeller Flow Meter",             "Operating Manual",          "ETL-1", "Purge monitoring"),
    (75, "Furnace – N₂ Purge 2",      "Nitrogen Gas",   "Yes", "416",               "900446", "Prevents reverse purge gas flow",                                            "Once in a year",           "Gestra",               "Non-Return Valve",                "Test Certificate",          "ETL-1", "Prevent reverse purge"),
    (76, "Furnace – N₂ Purge 2",      "Nitrogen Gas",   "Yes", "UV 409",            "900243", "Provides nitrogen purge during unsafe furnace conditions",                   "Once in a year",           "Kromschröder",         "Solenoid Valve",                  "Vendor Manual",             "ETL-1", "Purge safety"),
    (77, "Furnace – N₂ Purge 2",      "Nitrogen Gas",   "Yes", "FE 412",            "901910", "Creates controlled pressure drop for safe nitrogen purging",                 "Once in a year",           "Dosch",                "Throttle Orifice",                "Test Certificate",          "ETL-1", "Pressure drop"),
    (78, "Furnace – N₂ Purge 2",      "Nitrogen Gas",   "Yes", "414.1",             "901608", "Protects flow meter from particulate contamination",                         "Once in a year",           "Actaris",              "Strainer (Flat)",                 "Vendor Manual",             "ETL-1", "Protects flow meter"),
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
     "tlv_twa":"1 mg/m3 (ACGIH 2023  -  thoracic fraction as H2SO4 mist)","tlv_stel":"Not established (ACGIH 2023). NIOSH: 1 mg/m3 TWA. OSHA PEL: 1 mg/m3.","tlv_ceil":"Not established (ACGIH). OSHA 1971: 1 mg/m3 PEL.",
     "ld50":"2140 mg/kg (rat, oral)","lc50":"510 mg/m3/2h (rat, inhal.)",
     "flash":"N/A (not flammable)","bp":"337deg C","mp":"10deg C (conc.)","sg":"1.84 (conc.)","vp":"<0.3 hPa at 20deg C",
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
     "tlv_twa":"0.5 ppm (ACGIH  -  phenol component, SKIN designation)","tlv_stel":"15.6 ppm (NIOSH STEL  -  phenol component). ACGIH: no STEL set.","tlv_ceil":"Not established. NIOSH IDLH phenol: 250 ppm (practical ceiling for respiratory protection).",
     "ld50":"1050 mg/kg (rat, oral)","lc50":"Not established",
     "flash":">150deg C","bp":"~186deg C","mp":"~33deg C","sg":"1.28","vp":"Very low at 20deg C",
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
     "tlv_twa":"10 mg/m3 (ACGIH PNOR  -  inhalable fraction, nuisance aerosol)","tlv_stel":"3 mg/m3 (ACGIH PNOR  -  respirable fraction). No chemical-specific STEL.","tlv_ceil":"Not established. No significant vapour hazard (VP essentially zero at ambient).",
     "ld50":">5000 mg/kg (rat, oral)","lc50":"Not established",
     "flash":"190deg C (closed cup)","bp":">300deg C","mp":"-40deg C","sg":"0.914","vp":"<0.01 hPa at 20deg C",
     "odour":"Faint oily odour",
     "reactivity":"Stable under normal conditions. Incompatible with CrO3 (hazardous). Decomposition: CO, CO2 at high temperature.",
     "health":"Low acute toxicity. Mild skin/eye irritant. Not a known carcinogen.",
     "env":"Low toxicity to aquatic organisms. Biodegradable.",
     "storage":"Normal conditions. Cool, dry. Away from oxidisers.",
     "ppe":"Safety glasses, standard work gloves.",
     "emergency":"Absorb with dry material. Non-hazardous cleanup. Wash with soap and water.",
     "etl1_use":"Electrostatic oiling  -  applied at 1-2 g/m2 for corrosion protection","soc":"Per product spec","sol":"Per product spec"},
    {"code":"A4","name":"ENSA (Ethoxylated Naphthol Sulphonic Acid)","risk":40,"color":"#22c55e",
     "class":"Irritant liquid","cas":"Mixture","hazchem":"NFPA 2-1-1","nfpa":"2-1-1",
     "tlv_twa":"1 mg/m3 (H2SO4 acid mist  -  ACGIH TLV applies at plating bath)","tlv_stel":"3 mg/m3 (H2SO4 acid mist STEL  -  no ENSA-specific STEL established)","tlv_ceil":"Not established for ENSA blend.",
     "ld50":"Not established","lc50":"Not established",
     "flash":"~170deg C","bp":"~200deg C","mp":"Not established","sg":"~1.1","vp":"Low",
     "odour":"Mild aromatic/sulphonic odour",
     "reactivity":"Unstable in strongly acidic conditions at high temperature. Incompatible with strong acids and alkalis.",
     "health":"Irritant to skin, eyes, respiratory tract. Naphthol component: moderate toxicity.",
     "env":"Moderately toxic to aquatic organisms. Ethoxylate component may be persistent.",
     "storage":"Cool, dark. Away from acids and oxidisers.",
     "ppe":"Safety glasses, chemical gloves, lab coat.",
     "emergency":"Dilute with water, collect. Flush with water.",
     "etl1_use":"Plating bath brightener  -  controls grain structure of tin deposit","soc":"3-6 g/L","sol":"2-7 g/L"},
    {"code":"A5","name":"Sodium Dichromate (Na2Cr2O7)","risk":95,"color":"#ef4444",
     "class":"CARCINOGEN  -  Oxidising solid, toxic","cas":"10588-01-9","hazchem":"NFPA 4-0-2 (OX)","nfpa":"4-0-2 (OX)",
     "tlv_twa":"0.01 mg/m3 as Cr(VI) (ACGIH A1 2023) | OSHA PEL: 0.005 mg/m3 | NIOSH REL: 0.0002 mg/m3","tlv_stel":"Not established (ACGIH). OSHA Action Level: 0.0025 mg/m3 as Cr(VI).","tlv_ceil":"Not established separately (ACGIH TWA is controlling limit). OSHA: no ceiling set.",
     "ld50":"50 mg/kg (rat, oral)","lc50":"Not established",
     "flash":"N/A (oxidiser)","bp":"400deg C (decomposes)","mp":"356deg C","sg":"2.52","vp":"Negligible",
     "odour":"Odourless",
     "reactivity":"STRONG OXIDISER  -  reacts violently with organics, reducing agents, flammables. Reacts with H2SO4 to form chromic acid. Contact with combustibles can cause fire.",
     "health":"IARC Group 1 CARCINOGEN. Lung cancer, nasal/sinus cancer. TLV 0.05 mg/m3. Skin sensitiser  -  chrome ulcers. Mutagenic.",
     "env":"HIGHLY TOXIC to aquatic organisms. Extremely persistent in soil/groundwater. MSIHC Schedule chemical.",
     "storage":"Separate, cool, dry, ventilated. Away from ALL organics. Locked access. Secondary containment. MSIHC reporting >10 kg.",
     "ppe":"Class C suit. Air-supplied respirator. Face shield, rubber gloves, boots.",
     "emergency":"MAJOR SPILL: evacuate, call emergency services. Specialist cleanup. Medical attention immediately. CPCB notification within 48h.",
     "etl1_use":"Chemical treatment bath  -  electrolytic chromate passivation of tin plate","soc":"Per SDS specification","sol":"Air: <0.1 mg/m3 ceiling | Breach = SHUTDOWN"},
    {"code":"A6","name":"Chromic Acid (CrO3/Cr-VI)","risk":98,"color":"#ef4444",
     "class":"CARCINOGEN  -  Powerful oxidiser, corrosive, highly toxic","cas":"1333-82-0","hazchem":"NFPA 3-0-1 (OX)","nfpa":"3-0-1 (OX)",
     "tlv_twa":"0.05 mg/m3 as Cr (ACGIH)","tlv_stel":"0.1 mg/m3 ceiling","tlv_ceil":"0.1 mg/m3",
     "ld50":"80 mg/kg (rat, oral)","lc50":"<10 mg/m3 (rat, 4h)",
     "flash":"N/A (causes fires  -  not flammable itself)","bp":"250deg C (decomposes)","mp":"196deg C","sg":"2.70","vp":"Not applicable",
     "odour":"Acrid, metallic (vapour/mist)",
     "reactivity":"POWERFUL OXIDISER  -  contact with organics = spontaneous ignition. Reacts explosively with reducing agents. Mixed with H2SO4: chromic acid. EXPLOSIVE with alcohol/acetone/ketones.",
     "health":"IARC Group 1 CARCINOGEN (highest). Lung cancer 15-30x risk. TLV 0.05 mg/m3. Nasal perforation. Kidney damage. Mutagenic, teratogenic.",
     "env":"MOST TOXIC to aquatic organisms. Cr-VI persists for decades. Priority Hazardous Substance. MCL drinking water: 0.05 mg/L.",
     "storage":"SEPARATE locked store. NO organics within 5m. 110% secondary containment. Restricted access. MSIHC annual reporting.",
     "ppe":"MANDATORY: SCBA or airline respirator, Class C suit, face shield, heavy rubber gloves/boots. Buddy system.",
     "emergency":"EVACUATE  -  do not re-enter without SCBA. Hazmat team only. Decontaminate immediately. CPCB within 48h.",
     "etl1_use":"Chemical treatment bath  -  Cr-VI passivation (<10 mg/m2 on finished product)","soc":"Air: <0.05 mg/m3 (TLV-TWA)","sol":"Air: <0.1 mg/m3 | Breach = immediate SHUTDOWN"},
]

# ══════════════════════════════════════════════════════════════════════
# ACCIDENTS DATA (Home page incident records)
# ══════════════════════════════════════════════════════════════════════
ACCIDENTS = [
    {"industry":"Steel & Metal","plant":"Blast Furnace  -  Tata Steel","incident":"Hot metal ladle overflow  -  severe burns to 3 operators","severity":"L3","year":2022,"lesson":"Ladle inspection checklist mandatory before every pour. Level sensor calibration quarterly."},
    {"industry":"Steel & Metal","plant":"Reheating Furnace  -  JSW","incident":"Furnace explosion  -  gas buildup during restart","severity":"L4","year":2021,"lesson":"Mandatory N2 purge before gas admission. Purge interlock must be hardwired, not software only."},
    {"industry":"Chemicals","plant":"Chlor-Alkali  -  GACL","incident":"Cl2 gas leak  -  12 workers hospitalised","severity":"L3","year":2023,"lesson":"Cl2 detector calibration monthly. Emergency isolation valve must be outside exclusion zone."},
    {"industry":"Oil & Gas","plant":"Refinery  -  BPCL Mumbai","incident":"BLEVE  -  storage tank fire","severity":"L4","year":2020,"lesson":"Water spray deluge on all LPG/propane tanks. Thermographic inspection of tanks annually."},
    {"industry":"Steel & Metal","plant":"ETL-1  -  Tinplate","incident":"Cr-VI TLV breach  -  bath temperature exceeded 45deg C","severity":"L2","year":2023,"lesson":"Bath temperature auto-trip at 45deg C SOL. LEV face velocity verified monthly. Air monitor quarterly calibration."},
    {"industry":"Chemicals","plant":"H2 Plant  -  Electrolyser","incident":"H2-in-O2 analyser failure  -  explosive atmosphere formed","severity":"L3","year":2022,"lesson":"AT1002 requires 3-monthly calibration. Redundant analyser recommended. 1oo2 voting logic for auto-trip."},
    {"industry":"Oil & Gas","plant":"Pipeline  -  GAIL","incident":"H2S leak  -  worker fatality","severity":"L4","year":2021,"lesson":"H2S detector at all low points. Buddy system mandatory in H2S zones. Escape SCBA at entry points."},
    {"industry":"Steel & Metal","plant":"Coke Plant  -  SAIL","incident":"CO exposure  -  4 workers overcome","severity":"L3","year":2023,"lesson":"Fixed CO detectors at all low-lying areas. Personal CO monitor mandatory. Emergency rescue breathing apparatus."},
]

# ══════════════════════════════════════════════════════════════════════
# SHARED RENDERER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════
def render_pdb(params, dept_key="pdb"):
    st.markdown("""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.25);border-radius:10px;padding:.9rem 1.2rem;margin-bottom:1rem"> <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.78rem"> <div><b style="color:#22c55e">SOC (Standard Operating Condition)</b>  -  Normal target range. Deviation from SOC triggers identification and corrective action before reaching SOL.</div> <div><b style="color:#f97316">SOL (Safe Operating Limit)</b>  -  Outer safety boundary. Breach = Process Safety Incident. Triggers immediate corrective action or automatic plant trip.</div> </div></div>""", unsafe_allow_html=True)

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
            soc_min = str(p.get("soc_min"," - ")); soc_max = str(p.get("soc_max"," - "))
            sol_min = str(p.get("sol_min"," - ")); sol_max = str(p.get("sol_max"," - "))
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
  <div style="background:#0a1628;border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">IDENTIFICATION (below SOC)</div><div style="font-size:.73rem;color:#94a3b8">{p.get('identification_low',' - ')}</div></div>
  <div style="background:#0a1628;border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">IDENTIFICATION (above SOC)</div><div style="font-size:.73rem;color:#94a3b8">{p.get('identification_high',' - ')}</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:.6rem">
  <div style="background:rgba(234,179,8,.05);border:1px solid rgba(234,179,8,.2);border-left:3px solid #eab308;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#eab308;margin-bottom:3px">CONSEQUENCE  -  BELOW SOC/SOL</div><div style="font-size:.73rem;color:#fde68a">{p.get('consequence_low',' - ')}</div></div>
  <div style="background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.2);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:3px">CONSEQUENCE  -  ABOVE SOC/SOL</div><div style="font-size:.73rem;color:#fca5a5">{p.get('consequence_high',' - ')}</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:.4rem">
  <div style="background:rgba(34,197,94,.05);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#22c55e;margin-bottom:3px">ACTION / BARRIER  -  LOW</div><div style="font-size:.73rem;color:#4ade80">{p.get('action_low',' - ')}</div></div>
  <div style="background:rgba(34,197,94,.05);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#22c55e;margin-bottom:3px">ACTION / BARRIER  -  HIGH</div><div style="font-size:.73rem;color:#4ade80">{p.get('action_high',' - ')}</div></div>
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
            tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{bg_r}"><td style="padding:7px 10px;color:#475569;font-family:monospace">{p["sl"]}</td><td style="padding:7px 10px;color:#e2e8f0;font-weight:600;white-space:nowrap">{p["param"]}</td><td style="padding:7px 10px;color:#64748b;font-family:monospace">{p["uom"]}</td><td style="padding:7px 10px;color:#22c55e;font-family:monospace;font-weight:700">{p.get("soc_min"," - ")}</td><td style="padding:7px 10px;color:#22c55e;font-family:monospace;font-weight:700">{p.get("soc_max"," - ")}</td><td style="padding:7px 10px;color:#f97316;font-family:monospace">{p.get("sol_min"," - ")}</td><td style="padding:7px 10px;color:#f97316;font-family:monospace">{p.get("sol_max"," - ")}</td><td style="padding:7px 10px;color:#fde68a;font-size:.7rem;max-width:180px">{p.get("consequence_low"," - ")}</td><td style="padding:7px 10px;color:#fca5a5;font-size:.7rem;max-width:180px">{p.get("consequence_high"," - ")}</td><td style="padding:7px 10px;color:#4ade80;font-size:.7rem;max-width:160px">{p.get("action_low"," - ")}</td><td style="padding:7px 10px;color:#4ade80;font-size:.7rem;max-width:160px">{p.get("action_high"," - ")}</td><td style="padding:7px 10px;text-align:center;color:{crit_c};font-weight:700">{crit_txt}</td></tr>'
        tbl += '</tbody></table></div>'
        st.markdown(tbl, unsafe_allow_html=True)


def render_edb(items, dept_key="edb"):
    st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.2);border-radius:8px;padding:.8rem 1rem;margin-bottom:1rem;font-size:.78rem;color:#94a3b8"> <b style="color:#e2e8f0">Equipment Design Basis (EDB)</b>  -  Documents each piece of equipment handling/controlling hazardous substances: design parameters, safety basis, maintenance schedule, manufacturer.<br> <b style="color:#f97316">Consequence Based:</b> failure directly causes major accident &nbsp;|&nbsp; <b style="color:#a78bfa">Prevention & Mitigation:</b> installed to prevent/limit major accident </div>""", unsafe_allow_html=True)

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
            barrier_colors = {"Active  -  Instrumented":"#22c55e","Active  -  Mechanical":"#3b82f6","Administrative":"#eab308","Passive":"#a78bfa","Active  -  Automatic Trip":"#ef4444"}
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
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">TAG NO.</div><div style="font-size:.72rem;color:#f97316;font-family:monospace">{item.get('tag_no',' - ')}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">MANUFACTURER / MODEL</div><div style="font-size:.72rem;color:#94a3b8">{item.get('manufacturer',' - ')}  -  {item.get('model',' - ')}</div></div>
</div>
<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;margin-bottom:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">DESIGN BASIS & PURPOSE</div><div style="font-size:.75rem;color:#94a3b8;line-height:1.7">{item.get('design_basis',' - ')}</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px">
  <div style="background:rgba(239,68,68,.06);border:1px solid rgba(239,68,68,.2);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:3px">CONSEQUENCE OF FAILURE</div><div style="font-size:.72rem;color:#fca5a5">{item.get('consequence_of_failure',' - ')}</div></div>
  <div style="background:{bc}10;border:1px solid {bc}30;border-left:3px solid {bc};border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:{bc};margin-bottom:3px">BARRIER TYPE</div><div style="font-size:.72rem;color:#94a3b8">{btype if btype else ' - '}</div><div style="font-size:.68rem;color:#64748b;margin-top:2px">{item.get('barrier_effectiveness','')}</div></div>
  <div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:6px;padding:.6rem"><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#64748b;margin-bottom:3px">MAINTENANCE</div><div style="font-size:.72rem;color:#94a3b8">{item.get('selection_basis',' - ')}</div></div>
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
            tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 10px;color:#475569;font-family:monospace">{item["sl"]}</td><td style="padding:7px 10px;color:#e2e8f0;font-weight:600">{item["equipment"]}</td><td style="padding:7px 10px;color:#94a3b8">{item.get("sub_process","")}</td><td style="padding:7px 10px;color:#fca5a5">{item.get("hazardous_substance","")}</td><td style="padding:7px 10px;color:#f97316;font-family:monospace">{item.get("tag_no"," - ")}</td><td style="padding:7px 10px"><span style="background:rgba(59,130,246,.1);color:#60a5fa;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:20px">{item.get("barrier_type"," - ")}</span></td><td style="padding:7px 10px;color:#94a3b8;font-size:.68rem">{item.get("selection_basis"," - ")}</td><td style="padding:7px 10px;color:#64748b">{item.get("manufacturer"," - ")}</td><td style="padding:7px 10px;color:#64748b;font-family:monospace;font-size:.68rem">{item.get("model"," - ")}</td><td style="padding:7px 10px;color:#fca5a5;font-size:.7rem;max-width:160px">{item.get("consequence_of_failure"," - ")}</td><td style="padding:7px 10px;color:#64748b;font-size:.7rem;max-width:200px">{str(item.get("design_basis"," - "))[:100]}...</td></tr>'
        tbl += '</tbody></table></div>'
        st.markdown(tbl, unsafe_allow_html=True)


def render_psm_framework(plant_name="", meta=None):
    fw = PSM_FRAMEWORK

    st.markdown(f"""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem">
<div style="font-size:.9rem;font-weight:800;color:#3b82f6;margin-bottom:.3rem">PSRM  -  Process Safety Risk Management Framework</div>
<div style="font-size:.78rem;color:#94a3b8;line-height:1.8">
Based on the <b style="color:#e2e8f0">Tata Steel PSRM Module</b>  -  aligned with OSHA 29 CFR 1910.119 (Process Safety Management) and UK HSE COMAH. 
14 PSM elements mandatory for HHO processes. Barrier model: Detector + Logic Solver + Actuator = One Barrier.
</div></div>""", unsafe_allow_html=True)

    fw_tabs = st.tabs(["Consequence Levels (L1-L5)","Hazard Categories (A1-A5)","Barrier Model","Layers of Protection","HAZOP Methodology","Bow Tie","LOPA","PSI Elements (14)"])

    # ── L1-L5 ────────────────────────────────────────────────────────
    with fw_tabs[0]:
        st.markdown('''<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">
Consequence severity classified across 4 dimensions: <b style="color:#ef4444">People</b> (injury/fatality), <b style="color:#f97316">Community</b> (off-site impact), 
<b style="color:#eab308">Asset</b> (property damage), <b style="color:#22c55e">Environment</b> (release/impact). All 4 must be assessed for each scenario.
HHO threshold: ANY ONE of  -  property damage &gt;Rs.50L OR fatality potential OR significant env. impact -&gt; L3+.
</div>''', unsafe_allow_html=True)

        for lk, lv in fw["consequence_levels"].items():
            c = lv["color"]
            ex_html = "".join(f'<div style="font-size:.7rem;color:#64748b;padding:1px 0">&#8226; {e}</div>' for e in lv["examples"])
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
            ex_html = "".join(f'<div style="font-size:.7rem;color:#fca5a5;padding:1px 0">&#8226; {e}</div>' for e in av["examples"])
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

        st.markdown('<div class="sl-sec">Barrier Types  -  from Tata Steel PSRM Module</div>', unsafe_allow_html=True)
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
Inner layers prevent the top event (SOC -&gt; SOL). Outer layers mitigate consequences after loss of containment.
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
                st.markdown(f'<div style="font-size:.75rem;color:#94a3b8;padding:2px 0">&#8226; {w}</div>', unsafe_allow_html=True)
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

        st.markdown('<div class="sl-sec">Applied HAZOP  -  H2 Plant Electrolysis Node</div>', unsafe_allow_html=True)
        app_hazop = [
            ("MORE OF","Cell Temperature",">95deg C SOC (>97deg C SOL)","Cooling water valve TV1001 fails closed","Cell damage, KOH decomposition, H2 purity impact","RTD TE1001/TE1003 auto-trip at 97deg C (PSCE #9,#10)","Test TV1001 fail-safe; dual RTD voting logic"),
            ("MORE OF","H2 in O2",">0.8% SOC (>1.7% SOL)","Separator level low  -  gas bypass","O2 separator DETONATION","AT1002 auto-trip at HH (PSCE #13)","Verify AT1002 calibration  -  3-monthly; 1oo2 logic"),
            ("MORE OF","DC Current",">1450A SOC (>1600A SOL)","Rectifier malfunction","Cell damage, transformer failure, fire hazard","Overcurrent protection relay auto-trips","Annual relay calibration and functional test"),
            ("LESS OF","Separator Level","<500mm SOC (<400mm SOL)","Feed pump failure, LV1001 stuck open","H2-in-O2 rises -&gt; explosive mixture","LT1003/LT1001 level auto-trip","6-monthly level transmitter calibration"),
            ("NONE","DM Water Supply","No DM water to electrolyser","Feed pump 1M21 failure, valve closed","DM tank empties -&gt; plant trip (SOL 100mm)","LIT1301 alarm, auto-trip on low SOL","Quarterly pump test; manual valve position check"),
            ("REVERSE","Gas Separation","H2 into O2 / O2 into H2","Separator level failure both directions","Detonation risk in both separators","AT1001 + AT1002 (PSCE #13, #14)","Dual analysers; independent calibration"),
            ("OTHER THAN","H2 Purity","Contaminated H2 (O2 > 2 ppm SOL)","Deoxy bed failure  -  low temperature","Explosive O2+H2 in bullet storage","AT1102 trace O2  -  auto-vent QZ1007 (PSCE #26)","6-monthly deoxy bed inspection; AT1102 3-monthly cal."),
            ("AS WELL AS","H2 Stream","Moisture present (dew point >-70deg C SOL)","Dryer failure  -  regeneration incomplete","Pipeline corrosion, annealing hood damage, purity fail","MT1101 dew point  -  auto-trip at -70deg C (PSCE #23)","6-monthly MT1101 calibration"),
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
        st.markdown('<div class="sl-sec">Bow Tie  -  H2 Plant: H2/O2 Explosive Mixture Formation</div>', unsafe_allow_html=True)
        bt2_c1, bt2_c2, bt2_c3 = st.columns([2,1,2])
        with bt2_c1:
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin-bottom:.4rem">THREATS</div>', unsafe_allow_html=True)
            for t in ["AT1002 analyser failure","Separator level drops  -  gas bypass","Pressure control valve PV1001 failure","Operator error during startup"]:
                st.markdown(f'<div class="sl-cause">{t}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#22c55e;margin:.6rem 0 .3rem">PREVENTION BARRIERS</div>', unsafe_allow_html=True)
            for b in ["AT1002: H2-in-O2 analyser auto-trip (PSCE #13)","LT1003/LT1001: Level auto-trip (PSCE #11)","PV1001: Pressure regulating valve (PSCE #5)","Pre-startup safety checklist (SOP)"]:
                st.markdown(f'<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:5px 9px;margin-bottom:4px;font-size:.72rem;color:#4ade80">✓ {b}</div>', unsafe_allow_html=True)
        with bt2_c2:
            st.markdown(f'<div style="background:rgba(239,68,68,.15);border:2px solid #ef4444;border-radius:10px;padding:1rem;text-align:center;margin-top:1rem"><div style="font-size:.55rem;font-weight:700;color:#ef4444;letter-spacing:2px;margin-bottom:6px">TOP EVENT</div><div style="font-size:.75rem;font-weight:700;color:#e2e8f0;line-height:1.5">H2/O2 Explosive Mixture Formation</div><div style="font-size:.65rem;color:#ef4444;margin-top:6px">LOC from electrolyser</div></div>', unsafe_allow_html=True)
        with bt2_c3:
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#ef4444;margin-bottom:.4rem">CONSEQUENCES</div>', unsafe_allow_html=True)
            for c2 in ["L4: Detonation  -  electrolyser room collapse","Multiple fatalities  -  H2 plant zone","Plant shutdown 6-12 months","PESO investigation, possible prosecution"]:
                st.markdown(f'<div class="sl-consq">{c2}</div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#a78bfa;margin:.6rem 0 .3rem">MITIGATION BARRIERS</div>', unsafe_allow_html=True)
            for m in ["Blast-resistant room construction","Emergency H2 vent to elevated safe point","Emergency trip switch outside fence (PSCE #30)","NDRF pre-notification  -  H2 quantities declared"]:
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

        st.markdown('<div class="sl-sec">Independent Protection Layers (IPL)  -  PFD Values</div>', unsafe_allow_html=True)
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
            st.markdown(f'<div style="background:#0d1f35;border:1px solid {pc}40;border-left:4px solid {pc};border-radius:8px;padding:.8rem 1rem;margin-bottom:.6rem"><div style="font-size:.85rem;font-weight:700;color:{pc};margin-bottom:.3rem">{pk}</div><div style="font-size:.74rem;color:#94a3b8;margin-bottom:.5rem">Applies to: {pv["applies_to"]}  -  {pv["desc"]}</div><div>{el_html}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sl-sec">PSI Documents  -  What each covers in SafetyLens</div>', unsafe_allow_html=True)
        sl_tabs_map = {"PSC":"PSC tab","PDB":"PDB tab","HOM":"Hazard of Material tab","CIM":"Chem. Interaction tab","PSCE":"PSCE tab","EDB":"EDB tab","PHA":"PSM Framework tab"}
        for code, info in fw["psi_elements"].items():
            in_sl = sl_tabs_map.get(code,"")
            sl_badge = f'<span style="background:rgba(34,197,94,.15);color:#4ade80;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">SafetyLens: {in_sl}</span>' if in_sl else '<span style="background:rgba(99,102,241,.15);color:#a78bfa;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;margin-left:6px">Document repository</span>'
            st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:5px;display:flex;align-items:center;gap:12px"><span style="background:rgba(249,115,22,.15);color:#f97316;font-size:.72rem;font-weight:800;padding:3px 10px;border-radius:6px;min-width:48px;text-align:center">{code}</span><div><span style="font-size:.8rem;font-weight:700;color:#e2e8f0">{info["full"]}</span>{sl_badge}<div style="font-size:.72rem;color:#64748b;margin-top:2px">{info["purpose"]}</div></div></div>', unsafe_allow_html=True)

def ai_response(q):
    q = q.lower()
    if any(x in q for x in ["cr-vi","chromic","chromate","carcinogen","hexavalent"]):
        return ("Cr-VI (Chromic Acid)  -  ETL-1 Chemical Treatment:\n"
                "Risk Score: 98/100  -  CRITICAL\n"
                "TLV-TWA: 0.05 mg/m3 | Ceiling (STEL): 0.1 mg/m3\n"
                "HAZCHEM: NFPA 3-0-1 (Strong Oxidiser)\n"
                "Classification: IARC Group 1 Carcinogen\n"
                "Health effects: Lung cancer, nasal septum perforation, kidney damage\n"
                "Regulatory: Must be declared to CPCB & SPCB under MSIHC Rules 1989\n"
                "Action: Exceeding TLV = mandatory plant shutdown. Enclosed bath + LEV required.")
    if any(x in q for x in ["h2so4","sulphuric","sulfuric","pickling","acid"]):
        return ("Sulphuric Acid (H2SO4)  -  Pickling & Plating:\n"
                "Risk Score: 72/100  -  HIGH\n"
                "TLV-TWA: 1 mg/m3 | STEL: 3 mg/m3\n"
                "HAZCHEM: 2R | NFPA: 3-0-2(W)\n"
                "SOC in pickling bath: 8-10 g/L\n"
                "Hazards: Severe chemical burns, acid mist inhalation, H2 gas generation with metals\n"
                "Emergency: Deluge shower within 10 sec reach. Neutralise spill with lime.")
    if any(x in q for x in ["hho","lho","classification","highly hazardous"]):
        return ("HHO vs LHO Classification  -  ETL-1:\n\n"
                "HHO (Highly Hazardous Operation)  -  Full PSI + PHA + Bow Tie + LOPA:\n"
                "  - Cleaning & Rinsing (NaOH + H2SO4)\n"
                "  - Tin Plating (SnSO4 + PSA + ENSA)\n"
                "  - Reflow Furnace (H2 gas + Propane)\n"
                "  - Chemical Treatment (Cr-VI chromate)\n\n"
                "LHO (Lower Hazardous Operation)  -  PSI only:\n"
                "  - Coil Feeding | Electrostatic Oiling\n\n"
                "HHO criteria (any one met):\n"
                "  - Potential for fatality or multiple LTIs\n"
                "  - Property damage >50 lakhs\n"
                "  - Environmental recovery >2 months")
    if any(x in q for x in ["psce","safety critical","critical equipment"]):
        return ("PSCE (Process Safety Critical Equipment)  -  ETL-1:\n"
                "Total: 77 items (40 shown in this view)\n\n"
                "Selection basis:\n"
                "  - Consequence-based: failure = major accident\n"
                "  - Prescriptive: mandated by MSIHC / Factory Act\n\n"
                "Key items:\n"
                "  - Pyrometer ETL-1 (reflow temperature protection)\n"
                "  - PSAL 2.14 H2 Pressure Switch (explosion prevention)\n"
                "  - UV 1.21 Propane Solenoid DN50 (fire prevention)\n"
                "  - Cr-VI air monitors (carcinogen exposure)\n\n"
                "Current status: 5 items overdue for calibration  -  action required")
    if any(x in q for x in ["reflow","hydrogen","h2","furnace","strip temp"]):
        return ("Reflow Furnace  -  ETL-1 (HHO, Full PSM Required):\n"
                "Gases present: H2 (LEL 4%, UEL 77%) + N2 (purge) + Propane (LEL 2.1%, UEL 9.5%)\n"
                "Strip temperature SOC: 232-270 deg C\n"
                "Strip temperature SOL: 232-270 deg C (tight control)\n\n"
                "Safety procedures:\n"
                "  - N2 purge MUST happen BEFORE H2 introduction\n"
                "  - H2 purge on shutdown before air admission\n"
                "  - Pyrometer alarm at 270 C  -  auto-shutdown\n\n"
                "Consequence of failure:\n"
                "  - Strip temp >270 = burning + conductor roll damage\n"
                "  - H2 leak + ignition = vapour cloud explosion")
    if any(x in q for x in ["risk","61","index","score"]):
        return ("ETL-1 Risk Index: 61/100 (MEDIUM  -  approaching HIGH at 75)\n\n"
                "Risk drivers:\n"
                "  1. Cr-VI air  -  Chemical Treatment: 98/100 (CRITICAL)\n"
                "  2. Strip temp deviation  -  Reflow: 92/100 (CRITICAL)\n"
                "  3. Sn2+ concentration  -  Plating: 90/100 (CRITICAL)\n\n"
                "Threshold: >75 = HIGH (mandatory escalation to management)\n"
                "Current status: 5 PSCE items overdue, raising risk trend")
    if any(x in q for x in ["psm","msihc","compliance","osha","regulation"]):
        return ("PSM Compliance  -  ETL-1 Jamshedpur:\n\n"
                "OSHA PSM 29 CFR 1910.119:\n"
                "  Status: Partially compliant  -  PHA update pending\n\n"
                "Indian Factories Act 1948, Section 41B:\n"
                "  Status: Compliant  -  PSI documented and current\n\n"
                "MSIHC Rules 1989:\n"
                "  Status: Cr-VI quantities declared to CPCB & SPCB\n\n"
                "Required documents: PSI + PHA + Bow Tie + LOPA\n"
                "  + Operating Procedures + Emergency Response Plan")
    return (f"SafetyLens AI  -  ETL-1 Knowledge Base\n\nQuery: '{q}'\n\n"
            "I can answer questions about:\n"
            "  - Cr-VI / chromic acid risk (98/100)\n"
            "  - H2SO4 pickling acid (72/100)\n"
            "  - HHO / LHO classification\n"
            "  - PSCE items (77 total)\n"
            "  - Reflow furnace H2/propane safety\n"
            "  - Process parameters (PDB)  -  29 parameters\n"
            "  - PSM / MSIHC compliance\n"
            "  - Risk index and active alerts\n"
            "  - Flow brightening / tin melting process")

# ══════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ══════════════════════════════════════════════════════════════════════
for k, v in {"ind": None, "comp": None, "plant": None, "chat": [], "ck": 0,
              "psc_proc": "Cleaning & Rinsing", "h2_psc_proc": "Electrolysis",
              "hom_chem": "A6  -  Chromic Acid (CrO3/Cr-VI)", "h2_hom_sel": "H1  -  Hydrogen (H2)",
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
    <div class="sl-brand">PSI<b>Pro</b></div>
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

# Render live ticker bar
st.markdown(f'<div class="sl-ticker">{"".join(ticker_parts)}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# ROUTING
# ══════════════════════════════════════════════════════════════════════

# ── SIDEBAR — always visible for navigation ──────────────────────────────────
_cur_plant = st.session_state.get("plant","")
_cur_comp  = st.session_state.get("comp","")
_cur_ind   = st.session_state.get("ind","")

with st.sidebar:
    # Brand
    st.markdown('''<div style="padding:10px 4px 6px;text-align:center;border-bottom:1px solid #1e3a5f;margin-bottom:.5rem">
  <div style="font-size:1.3rem;font-weight:900;color:#fff;letter-spacing:-1px">PSI<b style="color:#3b82f6">Pro</b></div>
  <div style="font-size:.54rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin-top:2px">PROCESS SAFETY PLATFORM</div>
  <div style="font-size:.5rem;color:#475569;margin-top:2px">Tata Steel TCIL Golmuri</div>
</div>''', unsafe_allow_html=True)

    # Home button
    if st.button("⌂  Home — All Plants", key="sb_home_btn", use_container_width=True, type="primary"):
        st.session_state.plant = None
        st.session_state.comp  = None
        st.session_state.ind   = None
        st.rerun()

    # Breadcrumb
    if _cur_plant:
        short = _cur_plant.split("  -  ")[0]
        st.markdown(f'<div style="font-size:.6rem;color:#475569;padding:4px 2px;font-family:monospace">You are in: {short}</div>', unsafe_allow_html=True)

    st.markdown('<div style="font-size:.58rem;font-weight:700;letter-spacing:2px;color:#3b82f6;text-transform:uppercase;padding:8px 2px 3px">TATA STEEL · TCIL GOLMURI</div>', unsafe_allow_html=True)

    TCIL_NAV = {
        "Tinplate Operations": [
            ("ETL-1","ETL-1  -  Electrolytic Tinning Line 1"),
            ("ETL-2","ETL-2  -  Electrolytic Tinning Line 2"),
            ("CRM","CRM  -  Cold Rolling Mill"),
            ("TFS","TFS  -  Tin Free Steel"),
            ("GI/GA","Galvanizing Line (GI/GA)"),
            ("CCS","Colour Coated Sheet (CCS)"),
        ],
        "Utilities": [
            ("H2 Plant","Hydrogen Plant  -  H2 Production & Supply"),
            ("Propane Yard","Propane Yard  -  Decantation, Storage & Supply"),
        ],
    }
    _nav_idx = 0
    for _div, _plants in TCIL_NAV.items():
        st.markdown(f'<div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#475569;text-transform:uppercase;padding:5px 2px 2px;border-top:1px solid #1e3a5f;margin-top:4px">{_div}</div>', unsafe_allow_html=True)
        for _short, _full in _plants:
            _nav_idx += 1
            _pm = PLANT_META.get(_full, {})
            _s  = _pm.get("status","")
            _active = (_cur_plant == _full)
            _has_psi = bool(_pm)
            _badge = f" [{_s}]" if _s else ""
            _label = f"{'▶ ' if _active else ''}{_short}{_badge}"
            if _has_psi:
                if st.button(_label, key=f"nav_{_nav_idx}", use_container_width=True,
                             type="primary" if _active else "secondary"):
                    st.session_state.ind   = "Steel & Metal"
                    st.session_state.comp  = "Tata Steel - Tinplate (TCIL), Golmuri"
                    st.session_state.plant = _full
                    st.rerun()
            else:
                st.button(f"{_short} (PSI pending)", key=f"nav_{_nav_idx}",
                          use_container_width=True, disabled=True)

# ─────────────────────────────────────────────────────────────────────────────

if st.session_state.plant:
    plant = st.session_state.plant
    meta = PLANT_META.get(plant, {"risk": 50, "hho": 2, "lho": 2, "psce": 10, "status": "PSI"})
    is_etl1 = (plant == "ETL-1  -  Electrolytic Tinning Line 1")
    is_h2plant = (plant == "Hydrogen Plant  -  H2 Production & Supply")
    is_propane_yard = (plant == "Propane Yard  -  Decantation, Storage & Supply")
    ind_name = st.session_state.ind or ""
    comp = st.session_state.comp or ""

    div_name = ""
    if ind_name and comp:
        for dn, div_plants in HIERARCHY.get(ind_name, {}).get(comp, {}).items():
            if plant in div_plants:
                div_name = dn



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
    sc = "#f97316" if meta["status"] == "HHO" else "#3b82f6"
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:.8rem">
      <h2 style="font-size:1.4rem;font-weight:900;color:#f1f5f9;margin:0">{plant}</h2>
      <span class="sl-status-hho">{meta['status']} Active</span>
      <span class="sl-status-psm">{'Full PSM Required' if meta['hho'] >= 3 else 'PSI Required'}</span>
    </div>
    """, unsafe_allow_html=True)

    if is_propane_yard:
        profile = PLANT_PROFILES.get(plant, {})
        PROP_TAB_NAMES = ["Overview","PSC","Hazard of Material","Chem. Interaction","PDB","PSCE","EDB"]
        prop_tabs = st.tabs(PROP_TAB_NAMES)

        # ── DATA FROM EXCEL ──────────────────────────────────────
        PROP_PSC_ROWS = [
            ("1) Decantation of Liquid Propane from Tanker to Static Vessel","Liquid Propane","N","N","Y","N","N","Y","Y","Y","N","Ö","N"),
            ("2) Decantation of Gaseous Vapour from Tanker to Static Vessel","Gaseous Propane","N","N","Y","N","N","Y","Y","Y","N","Ö","N"),
            ("3) Storage of Propane Liquid and Gas inside Static Tanks","Liquid Propane + Gaseous Vapour","N","N","Y","N","N","Y","Y","Y","N","Ö","N"),
            ("4) Supply of Liquid Propane to Vaporizers","Liquid Propane","N","N","Y","N","N","Y","Y","Y","N","Ö","N"),
        ]
        PROP_PDB_ROWS = [
            (1,"Liquid Transfer Pressure (Tanker→Tank 1-4)","Kg/Cm2","—","10","<0","20","Tanker rota gauge; Sight Flow Glass detector","Pop action SV at liquid pipelines after pumps","Yes"),
            (2,"Vapour Transfer Pressure (Tanker→Tank 1-4)","Kg/Cm2","1.5","10","1","20","Pressure gauge at tanker and static tank","Pop action SV at pipelines after compressor","Yes"),
            (3,"Liquid Transfer Pressure (Tanker→Tank 5)","Kg/Cm2","—","10","<0","20","Tanker rota gauge; Sight Flow Glass detector","Pop action SV at liquid pipelines after pumps","Yes"),
            (4,"Vapour Transfer Pressure (Tanker→Tank 5)","Kg/Cm2","1.5","10","1","20","Pressure gauge at tanker and static tank","Pop action SV at pipelines after compressor","Yes"),
            (5,"Liquid Pump #1 Discharge Pressure","Kg/Cm2","—","10","<0","20","Pressure gauge after pump; Glass flow detector","Pop action SV at liquid pipelines after pumps","Yes"),
            (6,"Liquid Pump #2 Discharge Pressure","Kg/Cm2","—","10","<0","20","Pressure gauge after pump; Glass flow detector","Pop action SV at liquid pipelines after pumps","Yes"),
            (7,"Vapour Compressor #1 Suction/Discharge Pressure","Kg/Cm2","1.5","10","1","20","Pressure gauge at compressor and static tank","Pop action SV at pipelines after compressor","Yes"),
            (8,"Vapour Compressor #2 Suction/Discharge Pressure","Kg/Cm2","1.5","10","1","20","Pressure gauge at compressor and static tank","Pop action SV at pipelines after compressor","Yes"),
            (9,"Propane Tank Liquid Level (Tanks 1-5)","% of capacity","15","75","5","90","Level rotogauge at each static tank","Operator fills till 80% max only","Yes"),
            (10,"Propane Tank Inside Pressure (Tanks 1-5)","Kg/Cm2","2.5","10","1.5","20","Static tank pressure gauge; monitoring","Two safety relief valves per tank at 20 kg/cm²","Yes"),
            (11,"Propane Tank Inside Temperature (Tanks 1-5)","°C","15","35","10","45","Temperature gauge at each tank","Water sprinklers on tank at >36°C","Yes"),
        ]
        PROP_PSCE_ROWS = [
            (1,"Liquid Pump","—","Service and utility systems","—","Yes","Periodic PM"),
            (2,"Motor for Liquid Pump","—","Service and utility systems","—","Yes","Periodic PM"),
            (3,"Liquid Transfer Hoses","—","Service and utility systems","Prescriptive","Yes","Periodic PM"),
            (4,"Pop Action Safety Valve at Liquid Decantation Line","—","Instrumented systems (active Preventive)","Prescriptive","Yes","Periodic PM"),
            (5,"Unloading Compressor","—","Service and utility systems","—","Yes","Periodic PM"),
            (6,"Motor for Compressor","—","Service and utility systems","—","Yes","Periodic PM"),
            (7,"Vapour Transfer Hoses","—","Service and utility systems","Prescriptive","Yes","Periodic PM"),
            (8,"Pop Action Safety Valve at Vapor Decantation Line","Consequence Based","Instrumented systems (active Preventive)","Prescriptive","Yes","Periodic PM"),
            (9,"Pop Action Safety Valve at Compressor Discharge Line","Consequence Based","Instrumented systems (active Preventive)","Prescriptive","Yes","Periodic PM"),
            (10,"Bullets Temperature Gauge","—","Safety monitoring & emergency communication","—","Yes","Periodic PM"),
            (11,"Liquid Inlet EFCV","—","Controlled release equipment/systems","Prescriptive","Yes","Periodic PM"),
            (12,"Liquid Outlet EFCV","—","Controlled release equipment/systems","Prescriptive","Yes","Periodic PM"),
            (13,"Bullet Pressure Gauge","—","Safety monitoring & emergency communication","—","Yes","Periodic PM"),
            (14,"Vapor Inlet EFCV","—","Controlled release equipment/systems","Prescriptive","Yes","Periodic PM"),
            (15,"Vapor Outlet EFCV","—","Controlled release equipment/systems","Prescriptive","Yes","Periodic PM"),
            (16,"Pop Action Safety Valve at Common Liquid Outlet Line","Consequence Based","Instrumented systems (active Preventive)","Prescriptive","Yes","Periodic PM"),
            (17,"Leak Detection System","—","Safety monitoring & emergency communication","—","Yes","Periodic PM"),
            (18,"ROCV for Water Sprinkler System","—","Active mitigation system","—","Yes","Periodic PM"),
            (19,"Propane Tanks 1 to 5 (Entire Tank)","Consequence Based","—","Prescriptive","Yes","3rd party NDT + Hydro Test every 5 years"),
        ]
        PROP_EDB_ROWS = [
            (1,"Liquid Decantation — Tanks 1-4","Liquid Propane","Liquid Pump","Liq decantation Pump #1","TO BE GENERATED","Prevention & Mitigation","Quarterly","Corken USA","521-E-G-A-J-E S/N 265631GB","Rule-33 Cft","BAF Office",""),
            (2,"Liquid Decantation — Tanks 1-4","Liquid Propane","Motor for Liquid Pump #1","Pump Motor #1","TO BE GENERATED","Prevention & Mitigation","Quarterly","Crompton Greaves","S/N HGAM-11125 5.5kW 7.5HP","PM Checklist","BAF Office",""),
            (3,"Liquid Decantation — Tanks 1-4","Liquid Propane","Bullet Pressure Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Once/year","WIKA","EN837-1","PM Checklist","BAF Office","Wrong reading → uncontrolled pressure"),
            (4,"Liquid Decantation — Tanks 1-4","Liquid Propane","Liquid Transfer Hoses #1-4","TO BE NOMENCLATED","40020815","Consequence Based PSRM Critical","Hydro Test/year","ACME/PARKER","NA","Test Certificate","BAF Office","Uncontrolled gas release on failure"),
            (5,"Liquid Decantation — Tanks 1-4","Liquid Propane","Pop Action SV at Liquid Pipeline","TO BE NOMENCLATED","40020810","Prevention & Mitigation","Hydro Test/year","Chandra Engg","—","Test Certificate","BAF Office","Malfunction → uncontrolled propane release"),
            (6,"Liquid Decantation — Tank 5","Liquid Propane","Liquid Transfer Hoses #5","TO BE NOMENCLATED","40020815","Consequence Based PSRM Critical","Hydro Test/year","ACME/PARKER","NA","Test Certificate","BAF Office","Uncontrolled gas release"),
            (7,"Liquid Decantation — Tank 5","Liquid Propane","Propane Pump #2 for Tank #5","Pump #2","TO BE GENERATED","Prevention & Mitigation","Quarterly","Corken","22000 HGAEEU-L S/N G118760 RL","RULE-33","BAF Office",""),
            (8,"Liquid Decantation — Tank 5","Liquid Propane","Motor for Liquid Pump #2","Pump Motor #2","TO BE GENERATED","Prevention & Mitigation","Quarterly","Crompton Greaves","3.70EFL 3.7kW 1450 RPM","PM Checklist","BAF Office",""),
            (9,"Liquid Decantation — Tank 5","Liquid Propane","Bullet Pressure Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Once/year","WIKA","EN837-1","PM Checklist","BAF Office","Wrong reading → uncontrolled pressure"),
            (10,"Liquid Decantation — Tank 5","Liquid Propane","Pop Action SV at Liquid Pipeline","TO BE NOMENCLATED","40020810","Prevention & Mitigation","Hydro Test/year","Chandra Engg","—","Test Certificate","BAF Office","Malfunction → uncontrolled propane release"),
            (11,"Vapour Decantation — Tanks 1-4","Propane Vapour","Unloading Compressor #1","Compressor #1","TO BE GENERATED","Prevention & Mitigation","Quarterly","Corken","91-AJFBANSNN S/N 70653FM","RULE-33","BAF Office",""),
            (12,"Vapour Decantation — Tanks 1-4","Propane Vapour","Motor for Compressor #1","Compressor Motor #1","TO BE GENERATED","Prevention & Mitigation","Quarterly","Crompton Greaves","HHAM-12334 5.5kW 7.5HP","PM Checklist","BAF Office",""),
            (13,"Vapour Decantation — Tanks 1-4","Propane Vapour","Pop Action SV — Compressor #1 Discharge","TO BE NOMENCLATED","40020813","Prevention & Mitigation","Calibration/year","Chandra Engg","—","Test Certificate","BAF Office","Malfunction → high pressure in pipes"),
            (14,"Vapour Decantation — Tanks 1-4","Propane Vapour","Vapour Transfer Hoses #1-4","TO BE NOMENCLATED","40020816","Consequence Based PSRM Critical","Hydro Test/year","ACME/PARKER","NA","Test Certificate","BAF Office","Uncontrolled propane release"),
            (15,"Vapour Decantation — Tanks 1-4","Propane Vapour","Bullet Pressure Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Once/year","WIKA","EN837-1","PM Checklist","BAF Office","Wrong reading → uncontrolled pressure"),
            (16,"Vapour Decantation — Tanks 1-4","Propane Vapour","Pop Action SV at Vapor Pipeline","TO BE NOMENCLATED","40020810","Prevention & Mitigation","Hydro Test/year","Chandra Engg","—","Test Certificate","BAF Office","Malfunction → high pressure"),
            (17,"Vapour Decantation — Tank 5","Propane Vapour","Unloading Compressor #2","Compressor #2","TO BE GENERATED","Prevention & Mitigation","Quarterly","Corken","AM3FBANSNN-II S/N G1105 RJ","RULE-33","BAF Office",""),
            (18,"Vapour Decantation — Tank 5","Propane Vapour","Motor for Compressor #2","Compressor Motor #2","TO BE GENERATED","Prevention & Mitigation","Quarterly","Crompton Greaves","50EF4 7.5kW 10HP 1450 RPM","PM Checklist","BAF Office",""),
            (19,"Vapour Decantation — Tank 5","Propane Vapour","Pop Action SV — Compressor #2 Discharge","TO BE NOMENCLATED","40020813","Prevention & Mitigation","Calibration/year","Chandra Engg","—","Test Certificate","BAF Office","Malfunction → high pressure"),
            (20,"Vapour Decantation — Tank 5","Propane Vapour","Vapour Transfer Hoses #5","TO BE NOMENCLATED","40020816","Consequence Based PSRM Critical","Hydro Test/year","ACME/PARKER","NA","Test Certificate","BAF Office","Uncontrolled propane release"),
            (21,"Vapour Decantation — Tank 5","Propane Vapour","Bullet Pressure Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Once/year","WIKA","EN837-1","PM Checklist","BAF Office","Wrong reading → uncontrolled pressure"),
            (22,"Vapour Decantation — Tank 5","Propane Vapour","Pop Action SV at Vapor Pipeline","TO BE NOMENCLATED","40020810","Prevention & Mitigation","Hydro Test/year","Chandra Engg","—","Test Certificate","BAF Office","Malfunction → high pressure"),
            (23,"Storage Liquid — Tanks 1-4","Liquid Propane","Bullets Temperature Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Calibration/year","WIKA","EN13192","Calibration Test Cft","BAF Office","Wrong temp reading → uncontrolled temp"),
            (24,"Storage Liquid — Tanks 1-4","Liquid Propane","Inlet EFCV","TO BE NOMENCLATED","40020804","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (25,"Storage Liquid — Tanks 1-4","Liquid Propane","Outlet EFCV","TO BE NOMENCLATED","40020807","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (26,"Storage Liquid — Tank 5","Liquid Propane","Bullets Temperature Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Calibration/year","WIKA","EN13192","Calibration Test Cft","BAF Office","Wrong temp reading → uncontrolled temp"),
            (27,"Storage Liquid — Tank 5","Liquid Propane","Inlet EFCV","TO BE NOMENCLATED","40020804","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (28,"Storage Liquid — Tank 5","Liquid Propane","Outlet EFCV","TO BE NOMENCLATED","40020807","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (29,"Storage Vapour — Tanks 1-4","Propane Vapor","Bullet Pressure Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Once/year","WIKA","EN837-1","PM Checklist","BAF Office","Wrong reading → uncontrolled pressure"),
            (30,"Storage Vapour — Tanks 1-4","Propane Vapor","Inlet EFCV","TO BE NOMENCLATED","40020805","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (31,"Storage Vapour — Tanks 1-4","Propane Vapor","Outlet EFCV","TO BE NOMENCLATED","40020806","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (32,"Storage Vapour — Tanks 1-4","Propane Vapor","Safety Relief Valve at Vessel","TO BE NOMENCLATED","40020809","Prevention & Mitigation","Once/year","Chandra Engg","—","—","—","Malfunction → catastrophic explosion"),
            (33,"Storage Vapour — Tank 5","Propane Vapor","Bullet Pressure Gauge","TO BE NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Once/year","Forbes Marshall","837","Calibration Cft","BAF Office","Wrong reading → uncontrolled pressure"),
            (34,"Storage Vapour — Tank 5","Propane Vapor","Inlet EFCV","TO BE NOMENCLATED","40020805","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (35,"Storage Vapour — Tank 5","Propane Vapor","Outlet EFCV","TO BE NOMENCLATED","40020806","Consequence Based PSRM Critical","Calibration every 5 years","Chandra Engg","—","RULE-33","BAF Office",""),
            (36,"Storage Vapour — Tank 5","Propane Vapor","Safety Relief Valve at Vessel","TO BE NOMENCLATED","40020809","Prevention & Mitigation","Calibration/year","Chandra Engg","—","—","—","Malfunction → catastrophic explosion"),
            (37,"Leak Detection System","Propane Vapour","Gas Sensor","NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Calibration Yearly","World Wide Safety","—","Calibration Test Cft","BAF Office",""),
            (38,"Leak Detection System","Propane Vapour","Display Channel","NOMENCLATED","TO BE GENERATED","Prevention & Mitigation","Calibration Yearly","World Wide Safety","—","Calibration Test Cft","BAF Office",""),
            (39,"ROCV Water Sprinkler System","Propane Tanks","Mechanical Valve (ROCV)","ROCV","TO BE GENERATED","Prevention & Mitigation","Quarterly","Forbes Marshall","—","PM Checklist","BAF Office","Malfunction delays fire mitigation"),
            (40,"ROCV Water Sprinkler System","Propane Tanks","Electrical Actuator","—","TO BE GENERATED","Prevention & Mitigation","Quarterly","—","—","PM Checklist","BAF Office",""),
            (41,"Propane Tanks 1-5","Liquid + Gaseous Propane","Entire Tank (Bullet 1-5)","NOMENCLATED","TO BE GENERATED","Consequence Based PSRM Critical","3rd Party NDT + Hydro Test every 5 years","Chandra Engg","—","Test Certificate","BAF Office",""),
        ]

        # ── OVERVIEW ─────────────────────────────────────────────
        with prop_tabs[0]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Doc: PSRM/PSI/TINPL/PROP  ·  Dept: Propane Yard Installation (BAF), TCIL Golmuri  ·  Eff. Dt.: 01.05.2024</p>', unsafe_allow_html=True)
            render_glossary()

            st.markdown("""<div class="sl-metrics" style="grid-template-columns:repeat(5,1fr)">
              <div class="sl-metric"><div class="sl-metric-val" style="color:#f97316">4</div><div class="sl-metric-lbl">Processes (All HHO)</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">1</div><div class="sl-metric-lbl">Chemical</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">11</div><div class="sl-metric-lbl">PDB Parameters</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#22c55e">19</div><div class="sl-metric-lbl">PSCE Items</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#f97316">56 MT</div><div class="sl-metric-lbl">Propane Inventory</div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">Propane Yard Installation — Decantation, Storage and Supply. 5 horizontal bullets (Chandra Engg, licensed under RULE-33) storing 56 MT LPG/Propane. Supplies ETL-1 reflow furnace burners via vaporizers. 2 liquid pumps (Corken), 2 vapour compressors (Corken), dual EFCVs, dual SRVs per tank. All 4 processes are HHO. Full PSRM mandatory.</div>', unsafe_allow_html=True)

            # Active Alerts
            st.markdown('<div class="sl-sec">Active Risk Alerts</div>', unsafe_allow_html=True)
            for txt in [
                "CRITICAL — All 4 processes HHO. Full PSRM documentation and management controls required.",
                "HIGH — 56 MT propane inventory (5 tanks). BLEVE risk — dual SRVs and EFCVs mandatory per RULE-33.",
                "HIGH — Water sprinkler ROCV (Forbes Marshall) quarterly check due. Leak detection calibration due.",
            ]:
                st.markdown(f'<div class="sl-alert"><div class="sl-alert-text">{txt}</div></div>', unsafe_allow_html=True)

            # PSC Summary at top
            st.markdown('<div class="sl-sec">PSC Classification Summary — All Processes</div>', unsafe_allow_html=True)
            prop_ov_tbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.73rem;border:1px solid #1e3a5f"><thead><tr style="background:#06111f">'
            for hh in ["#","Process","Hazardous Substance","Toxic","Explosive","Flamm.","Corr.","Thermal","Press./Temp","Prop>50L","Fatality","Env.","HHO/LHO"]:
                prop_ov_tbl += f'<th style="padding:7px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            prop_ov_tbl += '</tr></thead><tbody>'
            for i, row in enumerate(PROP_PSC_ROWS):
                proc,haz,toxic,explos,flamm,corr,therm,press,propDmg,fatal,env,hho,lho = row
                prop_ov_tbl += '<tr style="border-bottom:1px solid #1e3a5f;background:rgba(249,115,22,.03)">'
                prop_ov_tbl += f'<td style="padding:7px 9px;color:#f97316;font-family:monospace;font-weight:700;border:1px solid #1e3a5f">{i+1}</td>'
                prop_ov_tbl += f'<td style="padding:7px 9px;color:#e2e8f0;font-weight:700;border:1px solid #1e3a5f">{proc}</td>'
                prop_ov_tbl += f'<td style="padding:7px 9px;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.1);color:#f97316;font-size:.62rem;padding:1px 7px;border-radius:20px">{haz}</span></td>'
                for v in [toxic,explos,flamm,corr,therm,press,propDmg,fatal,env]:
                    if v=="Y": prop_ov_tbl += '<td style="padding:7px 9px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.2);color:#f97316;font-weight:900;font-size:.72rem;padding:2px 7px;border-radius:4px">Y</span></td>'
                    else: prop_ov_tbl += '<td style="padding:7px 9px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.75rem;border:1px solid #1e3a5f">N</td>'
                prop_ov_tbl += '<td style="padding:7px 9px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.2);color:#f97316;font-size:.65rem;font-weight:800;padding:3px 10px;border-radius:20px">HHO</span></td>'
                prop_ov_tbl += '</tr>'
            prop_ov_tbl += '</tbody></table></div>'
            st.markdown(prop_ov_tbl, unsafe_allow_html=True)

            # Stats strip
            st.markdown("""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:1rem 0">
<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#f97316;font-family:monospace">4</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">HHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#ef4444;font-family:monospace">56 MT</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PROPANE INVENTORY</div></div>
<div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#22c55e;font-family:monospace">19</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PSCE ITEMS</div></div>
<div style="background:#0d1f35;border:1px solid rgba(59,130,246,.3);border-top:3px solid #3b82f6;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#3b82f6;font-family:monospace">11</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PDB PARAMETERS</div></div>
</div>""", unsafe_allow_html=True)

            # PDB Summary Table
            st.markdown('<div class="sl-sec">PDB — Process Design Basis Summary (All 11 Parameters)</div>', unsafe_allow_html=True)
            pdb_ov_hdr = ["Sl.","Parameter","UoM","SOC Min","SOC Max","SOL Min","SOL Max","PSM Critical"]
            pdb_ov_tbl = '<div style="overflow-x:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for hh in pdb_ov_hdr:
                pdb_ov_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            pdb_ov_tbl += '</tr></thead><tbody>'
            for r in PROP_PDB_ROWS:
                sl,param,uom,socmin,socmax,solmin,solmax,idc,safe,psm = r
                psm_c = "#22c55e" if psm=="Yes" else "#475569"
                pdb_ov_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:600;min-width:200px">{param}</td><td style="padding:6px 9px;color:#64748b;font-family:monospace">{uom}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{socmin}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{socmax}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace">{solmin}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{solmax}</td><td style="padding:6px 9px;text-align:center"><span style="background:{psm_c}20;color:{psm_c};font-size:.62rem;font-weight:700;padding:2px 7px;border-radius:10px">{psm}</span></td></tr>'
            pdb_ov_tbl += '</tbody></table></div>'
            st.markdown(pdb_ov_tbl, unsafe_allow_html=True)

            # PSCE Summary Table
            st.markdown('<div class="sl-sec">PSCE — Process Safety Critical Equipment (All 19 Items)</div>', unsafe_allow_html=True)
            psce_ov_hdr = ["Sl.","Equipment","Consequence Based","Prevention & Mitigation","Prescriptive","PSM Critical","Justification"]
            psce_ov_tbl = '<div style="overflow-x:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for hh in psce_ov_hdr:
                psce_ov_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            psce_ov_tbl += '</tr></thead><tbody>'
            for r in PROP_PSCE_ROWS:
                sl,equip,consq,prev,presc,psm,just = r
                is_c = bool(consq and consq!="—")
                bc = "#f97316" if is_c else "#a78bfa"
                psm_c = "#22c55e" if psm=="Yes" else "#475569"
                psce_ov_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:700;min-width:160px">{equip}</td><td style="padding:6px 9px;color:#f97316;font-size:.62rem">{consq if is_c else "—"}</td><td style="padding:6px 9px;color:#a78bfa;font-size:.62rem">{prev}</td><td style="padding:6px 9px;color:#3b82f6;font-size:.62rem">{presc}</td><td style="padding:6px 9px;text-align:center"><span style="background:{psm_c}20;color:{psm_c};font-size:.62rem;font-weight:700;padding:2px 7px;border-radius:10px">{psm}</span></td><td style="padding:6px 9px;color:#64748b;font-size:.62rem">{just}</td></tr>'
            psce_ov_tbl += '</tbody></table></div>'
            st.markdown(psce_ov_tbl, unsafe_allow_html=True)

            # Process Cards
            st.markdown('<div class="sl-sec">Process Overview — Propane Yard (PART 1)</div>', unsafe_allow_html=True)
            PROP_PROC_CARDS_OV = [
                ("1) Decantation of Liquid Propane — Tanker to Tanks 1-5",
                 "Liquid Propane at ≤10 kg/cm². Liquid Pump #1 (Corken 521-E-G-A-J-E, 5.5kW) for Tanks 1-4. Pump #2 (Corken 22000 HGAEEU-L) for Tank 5. Transfer Hoses (ACME/PARKER, SAP 40020815). Pop Action Safety Valve at liquid pipeline (SAP 40020810). Sight Flow Glass indicator. SOC: 0-10 kg/cm², SOL: <0 or >20 kg/cm².",
                 "hho",["HHO","PSM Required"]),
                ("2) Decantation of Gaseous Vapour — Tanker to Tanks 1-5",
                 "Gaseous Propane at 1.5-10 kg/cm². Unloading Compressor #1 (Corken 91-AJFBANSNN) for Tanks 1-4. Compressor #2 (Corken AM3FBANSNN-II) for Tank 5. Vapour Transfer Hoses (SAP 40020816). Pop Action SV at compressor discharge (SAP 40020813). SOC: 1.5-10 kg/cm², SOL: 1-20 kg/cm².",
                 "hho",["HHO","PSM Required"]),
                ("3) Storage of Propane Liquid & Gas in Static Tanks (1-5)",
                 "5 horizontal bullets (Chandra Engg, RULE-33 licensed). Dual SRVs per tank (SAP 40020809). EFCV Inlet (40020804/40020805) + Outlet (40020806/40020807). Temperature gauge (WIKA EN13192). Level Rotogauge at each tank. Tank Level SOC 15-75%, SOL 5-90%. Pressure SOC 2.5-10 kg/cm², SOL 1.5-20 kg/cm². Temp SOC 15-35°C, SOL 10-45°C.",
                 "hho",["HHO","PSM Required"]),
                ("4) Supply of Liquid Propane to Vaporizers (ETL-1 Furnace)",
                 "Liquid Propane supply from tanks to vaporizers for ETL-1 reflow furnace. Outlet EFCVs on each tank. ROCV for water sprinkler system (Forbes Marshall, quarterly PM). Leak detection sensor + display channel (World Wide Safety, yearly calibration). Supply pressure SOC 0-10 kg/cm², SOL <0 or >20 kg/cm².",
                 "hho",["HHO","PSM Required"]),
            ]
            PROP_OV_DETAIL = {
                "1) Decantation of Liquid Propane — Tanker to Tanks 1-5":{
                    "hazardous":["Liquid Propane: Flash point -104°C, LEL 2.1%, UEL 9.5%","Cryogenic burns from liquid contact (-42°C boiling point)","Hose rupture at pressure — massive vapour cloud","Liquid Pump (Corken) seal failure — propane at pump","Heavier than air — accumulates at ground level"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "params":"Liquid Transfer Pressure: SOC 0-10 kg/cm², SOL <0 or >20 kg/cm² | Tank Level: SOC 15-75%, SOL 5-90% | Tank Pressure: SOC 2.5-10 kg/cm², SOL 1.5-20 kg/cm²",
                    "psce":["Liquid Transfer Hoses SAP 40020815 (PSCE #3/6 — Hydro Test/year)","Pop Action SV at Liquid Pipeline SAP 40020810 (PSCE #5)","Inlet EFCV SAP 40020804 (PSCE #11 — Calibration/5yr)","Outlet EFCV SAP 40020807 (PSCE #12 — Calibration/5yr)","Liquid Pump #1 (Corken 521-E-G-A-J-E) & Pump #2 (Corken 22000 HGAEEU-L)"],
                    "barriers":["EFCV auto-isolates on excess flow (hose rupture)","Pop Action SV relieves at SOL pressure","Hydro-tested hoses every year (mandatory RULE-33)","Rotogauge + sight flow glass — operator monitoring","Leak detection sensor (World Wide Safety) in yard area"],
                },
                "2) Decantation of Gaseous Vapour — Tanker to Tanks 1-5":{
                    "hazardous":["Gaseous Propane: LEL 2.1%, UEL 9.5% — explosive in air","Compressor discharge 1.5-10 kg/cm² — seal failure = gas release","Vapour hose burst — instant propane gas cloud","Compressor motor: ignition source in Zone 1 classified area"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "params":"Vapour Transfer Pressure: SOC 1.5-10 kg/cm², SOL 1-20 kg/cm² | Compressor Discharge Pressure: SOC 1.5-10 kg/cm², SOL 1-20 kg/cm²",
                    "psce":["Vapour Transfer Hoses SAP 40020816 (PSCE #7/14 — Hydro Test/year)","Pop Action SV at Compressor Discharge SAP 40020813 (PSCE #9)","Vapour Inlet EFCV SAP 40020805 (PSCE #14)","Vapour Outlet EFCV SAP 40020806 (PSCE #15)","Compressor #1 (Corken 91-AJFBANSNN) & #2 (Corken AM3FBANSNN-II)"],
                    "barriers":["Pop Action SV: relieves compressor discharge at SOL","Vapour hoses: hydro-tested every year","EFCV: auto-isolates on excess flow (hose rupture)","Tank pressure gauge: operator monitoring SOC 2.5-10 kg/cm²","Leak detector alarm in yard area"],
                },
                "3) Storage of Propane Liquid & Gas in Static Tanks (1-5)":{
                    "hazardous":["56 MT propane — largest hazard. Dual-phase storage","BLEVE (Boiling Liquid Expanding Vapour Explosion) if exposed to fire","Tank pressure SOL 20 kg/cm² — vessel rupture catastrophic","Solar heating — pressure rise beyond SRV setpoint","EFCVs on all inlet/outlet connections — critical for leak isolation"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "params":"Tank Liquid Level: SOC 15-75%, SOL 5-90% | Tank Pressure: SOC 2.5-10 kg/cm², SOL 1.5-20 kg/cm² | Tank Temperature: SOC 15-35°C, SOL 10-45°C",
                    "psce":["Dual SRVs per tank SAP 40020809 (PSCE #16 — RULE-33 mandatory)","Liquid Inlet EFCV SAP 40020804 (PSCE #11) + Outlet SAP 40020807 (PSCE #12)","Vapour Inlet EFCV SAP 40020805 (PSCE #14) + Outlet SAP 40020806 (PSCE #15)","Temperature Gauge WIKA EN13192 (PSCE #10)","Pressure Gauge WIKA EN837-1 (PSCE #13)","Entire Tank 1-5 (PSCE #19 — 3rd party NDT + Hydro Test every 5 yrs)"],
                    "barriers":["Dual SRVs per tank — set at 20 kg/cm² SOL (RULE-33 prescriptive)","5-yearly NDT + Hydro Test on all bullets (PSCE #19)","Rotogauge: SOL 90% — stop filling","Temp gauge: SOL 45°C — water spray deluge activates","Water Sprinkler ROCV (PSCE #18): remote activation on fire"],
                },
                "4) Supply of Liquid Propane to Vaporizers (ETL-1 Furnace)":{
                    "hazardous":["Liquid propane at tank pressure in supply line to vaporizer","Supply line leak in ETL-1 bay: propane + H2 furnace = compound explosion","Vaporizer connection failure — liquid flash in furnace bay","EFCV on tank outlet: critical for isolation on supply line failure"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "params":"Supply Pressure: SOC 0-10 kg/cm², SOL <0 or >20 kg/cm²",
                    "psce":["Outlet EFCV SAP 40020807 (PSCE #12 — auto-isolates on excess flow)","Pop Action SV at Common Liquid Outlet SAP 40020810 (PSCE #16)","Leak Detection Gas Sensor in supply line area (PSCE #17)","Water Sprinkler ROCV (PSCE #18)"],
                    "barriers":["EFCV auto-isolation on excess flow (supply line rupture)","Leak detector alarm in ETL-1 propane supply area","Pop Action SV at outlet — relieves at SOL","Isolation valve at vaporizer inlet — closed during maintenance"],
                },
            }

            for name, desc, cls, tags in PROP_PROC_CARDS_OV:
                t_html = "".join(f'<span class="sl-tag sl-tag-{"hho" if t=="HHO" else "psm"}">{t}</span>' for t in tags)
                st.markdown(f'<div class="sl-proc {cls}"><div class="sl-proc-title">{name}</div><div class="sl-proc-desc">{desc}</div>{t_html}</div>', unsafe_allow_html=True)
                det = PROP_OV_DETAIL.get(name, {})
                if det:
                    if True:  # always show inline — no click needed
                        hm = det["hazard_matrix"]
                        hm_html = '<table style="border-collapse:collapse;width:100%;font-size:.72rem;margin-bottom:.8rem"><tr>'
                        for k in hm.keys():
                            hm_html += f'<th style="background:#080d18;padding:5px 8px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;text-align:center">{k}</th>'
                        hm_html += '</tr><tr>'
                        for v in hm.values():
                            vc = "#22c55e" if v=="Y" else "#475569"
                            vbg = "rgba(34,197,94,.1)" if v=="Y" else "#0d1f35"
                            hm_html += f'<td style="background:{vbg};padding:6px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;color:{vc}">{v}</td>'
                        hm_html += '</tr></table>'
                        st.markdown(hm_html, unsafe_allow_html=True)
                        d1, d2 = st.columns(2)
                        with d1:
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-bottom:.3rem">HAZARDOUS SUBSTANCES / ENERGIES</div>', unsafe_allow_html=True)
                            for h in det["hazardous"]:
                                st.markdown(f'<div style="font-size:.75rem;color:#fca5a5;padding:2px 0">&#8226; {h}</div>', unsafe_allow_html=True)
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin:.6rem 0 .3rem">SAFETY BARRIERS</div>', unsafe_allow_html=True)
                            for b in det["barriers"]:
                                st.markdown(f'<div style="font-size:.75rem;color:#22c55e;padding:2px 0">&#10003; {b}</div>', unsafe_allow_html=True)
                        with d2:
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-bottom:.3rem">PSCE ITEMS (CRITICAL EQUIPMENT)</div>', unsafe_allow_html=True)
                            for p in det["psce"]:
                                st.markdown(f'<div style="font-size:.74rem;color:#f97316;padding:2px 0">&#9679; {p}</div>', unsafe_allow_html=True)
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin:.6rem 0 .3rem">KEY PARAMETERS (SOC / SOL)</div>', unsafe_allow_html=True)
                            st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.6rem .9rem;font-size:.72rem;color:#64748b;line-height:1.7">{det["params"]}</div>', unsafe_allow_html=True)

            render_global_incidents(["Propane"])
            render_qa_bot("prop_overview")

        with prop_tabs[1]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PSC/TINPL/PROP/003  ·  Dept: Propane Yard Installation  ·  Eff. Dt.: 01.05.2024</p>', unsafe_allow_html=True)
            render_glossary()

            st.markdown('''<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:.8rem">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.2rem">PROCESS SAFETY CLASSIFICATION — PROPANE YARD INSTALLATION</div>
<div style="font-size:.62rem;color:#475569">Form No.: PSRM/PSI/PSC/TINPL/PROP/003  ·  Dept: Propane Yard Installation  ·  Process: Propane Decantation, Storage and Supply  ·  Eff. Dt.: 01.05.2024</div>
</div>''', unsafe_allow_html=True)

            # ── EXACT EXCEL PSC TABLE ──────────────────────────────
            psc_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.73rem;border:1px solid #1e3a5f"><thead>'
            psc_tbl += '<tr style="background:#06111f"><th rowspan="2" style="padding:8px 10px;text-align:left;color:#94a3b8;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;min-width:220px">PROCESS<br><span style=\\"color:#475569;font-weight:400\\">Area: Propane Yard (PART 1)</span></th>'
            psc_tbl += '<th rowspan="2" style="padding:8px 8px;text-align:center;color:#60a5fa;font-size:.58rem;font-weight:700;border:1px solid #1e3a5f;min-width:100px">HAZARDOUS SUBSTANCE</th>'
            psc_tbl += '<th colspan="5" style="padding:8px;text-align:center;color:#f97316;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(249,115,22,.08)">HAZARDOUS SUBSTANCE HAVING / CAUSING</th>'
            psc_tbl += '<th colspan="3" style="padding:8px;text-align:center;color:#ef4444;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(239,68,68,.08)">CONSEQUENCES</th>'
            psc_tbl += '<th rowspan="2" style="padding:8px 6px;text-align:center;color:#f97316;font-size:.62rem;font-weight:800;border:1px solid #1e3a5f;background:rgba(249,115,22,.12);min-width:45px">HHO</th>'
            psc_tbl += '<th rowspan="2" style="padding:8px 6px;text-align:center;color:#6366f1;font-size:.62rem;font-weight:800;border:1px solid #1e3a5f;background:rgba(99,102,241,.1);min-width:45px">LHO</th></tr>'
            psc_tbl += '<tr style="background:#06111f">'
            for hh in ["Toxic","Explosive","Flammable","Corrosive","Thermally Instable"]:
                psc_tbl += f'<th style="padding:7px 6px;text-align:center;color:#94a3b8;font-size:.57rem;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            for hh in ["Significant Property Damage (>50 Lakhs)","Potential for Fatality","Significant Environmental Impact"]:
                psc_tbl += f'<th style="padding:7px 6px;text-align:center;color:#fca5a5;font-size:.55rem;font-weight:700;border:1px solid #1e3a5f;max-width:80px">{hh}</th>'
            psc_tbl += '</tr></thead><tbody>'
            for di, drow in enumerate(PROP_PSC_ROWS):
                proc,haz,toxic,explos,flamm,corr,therm,press,propDmg,fatal,env,hho,lho = drow
                bg = "rgba(249,115,22,.04)" if di%2==0 else "rgba(249,115,22,.02)"
                psc_tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{bg}">'
                psc_tbl += f'<td style="padding:8px 10px;color:#e2e8f0;font-weight:700;border:1px solid #1e3a5f">{proc}</td>'
                psc_tbl += f'<td style="padding:8px 8px;color:#94a3b8;font-size:.68rem;border:1px solid #1e3a5f">{haz}</td>'
                for v in [toxic,explos,flamm,corr,therm]:
                    if v=="Y": psc_tbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.2);color:#f97316;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                    else: psc_tbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                for v in [press,propDmg,fatal,env]:
                    if v=="Y": psc_tbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(239,68,68,.2);color:#ef4444;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                    else: psc_tbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                hho_c = "#f97316" if hho=="Ö" else "#475569"
                lho_c = "#6366f1" if lho=="Ö" else "#475569"
                psc_tbl += f'<td style="padding:8px;text-align:center;border:1px solid #1e3a5f;font-weight:900;color:{hho_c};font-size:.9rem">{hho}</td>'
                psc_tbl += f'<td style="padding:8px;text-align:center;border:1px solid #1e3a5f;font-weight:900;color:{lho_c};font-size:.9rem">{lho}</td>'
                psc_tbl += '</tr>'
            psc_tbl += '</tbody></table></div>'
            st.markdown(psc_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.62rem;color:#475569;margin-bottom:1rem;font-family:monospace">Ö = Applicable  ·  N = Not Applicable  ·  HHO = High Hazard Operation  ·  Source: PSRM/PSI/PSC/TINPL/PROP/003</div>', unsafe_allow_html=True)

            # ── PSRM Framework Banner ──────────────────────────────
            st.markdown("""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem">
<div style="font-size:.82rem;font-weight:700;color:#f97316;margin-bottom:.5rem">PSRM CLASSIFICATION FRAMEWORK — PROPANE YARD</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.78rem;color:#94a3b8;line-height:1.8">
<div><b style="color:#f97316">HHO — All 4 Processes</b><br>Decantation (Liquid) · Decantation (Vapour) · Storage · Supply to Vaporizers<br>Requires: Full PSRM — PSI + PHA + HAZOP + Bow Tie + LOPA + Barrier Audits + SOPs + Emergency Plan</div>
<div><b style="color:#64748b">LHO — None</b><br>All Propane Yard processes involve highly flammable liquid/gas at pressure.<br>No LHO classification applicable. All 4 processes mandatorily HHO under PSRM Module.</div>
</div></div>""", unsafe_allow_html=True)

            # ── Stats strip ────────────────────────────────────────
            st.markdown("""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1rem">
<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#f97316;font-family:monospace">4</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">HHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#ef4444;font-family:monospace">56 MT</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PROPANE INVENTORY</div></div>
<div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#22c55e;font-family:monospace">19</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PSCE ITEMS</div></div>
<div style="background:#0d1f35;border:1px solid rgba(59,130,246,.3);border-top:3px solid #3b82f6;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#3b82f6;font-family:monospace">RULE-33</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">STATUTORY AUTHORITY</div></div>
</div>""", unsafe_allow_html=True)

            # ── FULL PROCESS DETAIL CARDS (ETL-1 level) ────────────
            st.markdown('<div class="sl-sec">Process Safety Classification — Full Breakdown</div>', unsafe_allow_html=True)

            PROP_PSC_CARDS = [
                {
                    "name":"1) Decantation of Liquid Propane from Tanker to Static Vessels (Tanks 1-5)",
                    "cls":"HHO","color":"#f97316",
                    "substance":"Liquid Propane (C3H8) — flash point -104°C, boiling point -42°C — at transfer pressure 0-10 kg/cm² via hoses and liquid pump",
                    "hazardous":[
                        "Liquid Propane: Extremely Flammable — flash point -104°C, LEL 2.1%, UEL 9.5%",
                        "Liquid propane at -42°C — cryogenic burns on skin contact",
                        "Hose rupture at pressure: sudden liquid flash → massive vapour cloud (LPG flash factor)",
                        "Liquid Pump (Corken): mechanical seal failure → propane release at pump",
                        "Heavier than air vapour — accumulates at ground level, flows into drains/pits",
                        "Excess Flow Check Valve (EFCV) — critical for hose rupture isolation",
                    ],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"N"},
                    "reasoning":"Flammable (Y): Liquid Propane flash point -104°C — ignites at any temperature above -104°C. Pressure (Y): transfer at 0-10 kg/cm², hose burst pressure 20 kg/cm² SOL. Property >50L (Y): Hose rupture + ignition = large pool fire or vapour cloud fire, pump and pipework damage >>50 lakhs. Fatality (Y): Vapour cloud explosion (VCE) or flash fire in decantation area = multiple fatality event. → HHO.",
                    "barriers":[
                        "Liquid Transfer Hoses (SAP 40020815): Hydro Test every year — failure at SOL >20 kg/cm² (PSCE #3)",
                        "Pop Action Safety Valve at liquid pipeline (SAP 40020810): relieves at SOL (PSCE #5)",
                        "Inlet EFCV (SAP 40020804): Calibration every 5 years — auto-isolates on excess flow (PSCE #11)",
                        "Outlet EFCV (SAP 40020807): Calibration every 5 years (PSCE #12)",
                        "Rotogauge on tanker and static tank: SOC pressure 0-10 kg/cm² operator monitoring",
                        "Sight Flow Glass: confirms flow direction and rate during decantation",
                        "Leak Detection System (World Wide Safety): area gas sensor — alarm on propane vapour",
                        "Water Sprinkler ROCV (Forbes Marshall): activated on fire detection — cools tanks",
                    ],
                    "hazop":[
                        ("Liquid Transfer Pressure HIGH",">20 kg/cm² (SOL)","Pump discharge valve closed / hose blockage","Hose burst or pump seal failure — liquid propane spray → flash vapour cloud","Pop Action SV relieves; EFCV isolates; operator shuts pump; area evacuation"),
                        ("Liquid Transfer Pressure LOW","<0 kg/cm² (SOL)","Hose kink / suction valve closed / pump failure","No flow — decantation incomplete; tanker unable to unload","Rotogauge monitoring; sight flow glass check; restart procedure"),
                        ("Hose RUPTURE","Uncontrolled release","Hose age / abrasion / overpressure","Propane liquid spray → massive vapour cloud → VCE or flash fire","EFCV auto-isolates; emergency stop pump; area evacuation; water spray"),
                        ("Pump Seal FAILURE","Propane leak at pump","Seal wear / cavitation damage","Propane release at pump — vapour cloud in yard","Leak detector alarm; pump stop; isolation valve; fire extinguisher"),
                    ],
                    "bowtie":{
                        "top_event":"Liquid propane release and vapour cloud ignition during decantation",
                        "causes":["Hose rupture due to pressure surge above SOL 20 kg/cm²","EFCV fails to close on excess flow — uncontrolled release","Pump mechanical seal failure — liquid spray at pump","Tanker operator error — overfills tank above 90% SOL level"],
                        "consequences":["VCE (Vapour Cloud Explosion) — blast wave + fireball in yard","Multiple fatalities — decantation team and tanker driver","BLEVE of adjacent static tank if fire impinges","RULE-33 violation — PESO shutdown and prosecution"],
                        "preventions":["EFCV (SAP 40020804/07): auto-isolates on excess flow (PSCE #11/12)","Pop Action SV: relieves pressure at SOL (PSCE #5)","Hydro-tested hoses every year (PSCE #3/4)","Rotogauge + operator monitoring SOC 0-10 kg/cm²"],
                        "mitigations":["Water sprinkler ROCV: immediate activation on fire (PSCE #18)","Emergency shutdown valve at tanker connection","Area evacuation route and muster point (>50m upwind)","PESO notification + fire brigade on standby during decantation"],
                    },
                    "params":"Liquid Transfer Pressure: SOC 0-10 kg/cm², SOL <0 or >20 kg/cm² | Tank Liquid Level: SOC 15-75%, SOL 5-90% | Tank Pressure: SOC 2.5-10 kg/cm², SOL 1.5-20 kg/cm²",
                },
                {
                    "name":"2) Decantation of Gaseous Vapour from Tanker to Static Vessels",
                    "cls":"HHO","color":"#f97316",
                    "substance":"Gaseous Propane vapour (C3H8) — at compressor discharge pressure 1.5-10 kg/cm² — vapour return line from tanker to static tank",
                    "hazardous":[
                        "Gaseous Propane: Extremely Flammable — LEL 2.1%, UEL 9.5% — explosive in air range",
                        "Compressor (Corken): discharge pressure 1.5-10 kg/cm² — mechanical failure = gas release",
                        "Vapour Transfer Hoses: burst pressure SOL 20 kg/cm² — sudden gas release",
                        "Compressor motor: electrical ignition source in classified hazardous area (Zone 1)",
                        "Heavier than air — propane vapour settles at ground level even in open air",
                        "Pop Action SV on compressor discharge: critical PSCE — failure to lift = overpressure",
                    ],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"N"},
                    "reasoning":"Flammable (Y): Gaseous propane at LEL 2.1% — explosive range wide. Pressure (Y): Compressor discharge 1.5-10 kg/cm², SOL 20 kg/cm². Property >50L (Y): Compressor explosion or vapour cloud fire — equipment replacement >>50 lakhs. Fatality (Y): Gas cloud ignition in yard → deflagration / VCE → fatality. → HHO.",
                    "barriers":[
                        "Vapour Transfer Hoses (SAP 40020816): Hydro Test every year (PSCE #7)",
                        "Pop Action SV at Compressor #1 Discharge (SAP 40020813): calibration every year (PSCE #9)",
                        "Pop Action SV at Vapour Pipeline (SAP 40020810): Hydro Test every year (PSCE #8)",
                        "Inlet EFCV (SAP 40020805): Calibration every 5 years (PSCE #14)",
                        "Outlet EFCV (SAP 40020806): Calibration every 5 years (PSCE #15)",
                        "Tank pressure gauge (WIKA EN837-1): monitors SOC 2.5-10 kg/cm² (PSCE #13)",
                        "Compressor discharge pressure gauge: operator monitoring",
                        "Leak Detection Display Channel: area gas detection alarm",
                    ],
                    "hazop":[
                        ("Compressor Discharge Pressure HIGH",">20 kg/cm² (SOL)","SV fails / downstream valve closed","Hose burst or pipeline failure — propane gas cloud","Pop Action SV opens; EFCV isolates; operator stops compressor; evacuation"),
                        ("Compressor FAILS","Suction or discharge valve issue","Mechanical failure / motor trip","Vapour build-up in tanker — tanker cannot leave site","Manual valve procedures; alternative compressor deployment"),
                        ("Vapour Hose RUPTURE","Uncontrolled gas release","Hose age / pressure surge / connection failure","Propane gas cloud in yard — explosion if ignited","Emergency stop compressor; EFCV auto-isolates; fire brigade"),
                        ("Tank Pressure HIGH",">20 kg/cm² (SOL)","Overfilling vapour space","SRV lifts — propane vent to atmosphere","SRV set at 20 kg/cm² (PSCE #16); operator monitoring; stop compressor"),
                    ],
                    "bowtie":{
                        "top_event":"Gaseous propane release and ignition during vapour decantation",
                        "causes":["Vapour hose rupture during compressor operation","Compressor mechanical seal failure — gas at discharge","Pop Action SV on compressor fails — overpressure → pipeline burst","Ignition from compressor motor spark or static discharge"],
                        "consequences":["Gas cloud explosion — VCE in yard","Compressor destruction — loss of vapour transfer capability","Fatality of decantation team and tanker driver","RULE-33 / PESO enforcement + shutdown"],
                        "preventions":["Pop Action SV at compressor discharge: calibrated annually (PSCE #9)","Hydro-tested vapour hoses every year (PSCE #7)","EFCV auto-isolation on excess flow (PSCE #14/15)","Compressor discharge pressure monitoring SOC 1.5-10 kg/cm²"],
                        "mitigations":["Water sprinkler ROCV on fire (PSCE #18)","Emergency compressor stop from remote location","Area evacuation + muster point upwind","PESO + fire brigade notification"],
                    },
                    "params":"Vapour Transfer Pressure: SOC 1.5-10 kg/cm², SOL 1-20 kg/cm² | Compressor Discharge Pressure: SOC 1.5-10 kg/cm², SOL 1-20 kg/cm² | Tank Pressure: SOC 2.5-10 kg/cm², SOL 1.5-20 kg/cm²",
                },
                {
                    "name":"3) Storage of Propane Liquid and Gas in Static Tanks (Bullets 1-5)",
                    "cls":"HHO","color":"#f97316",
                    "substance":"Liquid Propane + Gaseous Propane vapour simultaneously in 5 horizontal pressure vessels (Chandra Engg) — 56 MT total inventory — RULE-33 licensed",
                    "hazardous":[
                        "Dual-phase storage — liquid and vapour propane simultaneously in each bullet",
                        "Total inventory 56 MT — single largest hazard in Propane Yard",
                        "Tank pressure SOC 2.5-10 kg/cm², SOL 20 kg/cm² — IBR/RULE-33 mandatory",
                        "Tank temperature SOC 15-35°C, SOL 45°C — solar heating causes pressure rise",
                        "BLEVE (Boiling Liquid Expanding Vapour Explosion) — catastrophic vessel failure in fire",
                        "Dual SRVs per tank (SAP 40020809): statutory RULE-33 requirement — failure = uncontrolled vent",
                        "EFCVs (liquid inlet/outlet + vapour inlet/outlet): 5-yearly calibration — PSCE #11-15",
                        "Tank body: 3rd Party NDT + Hydro Test every 5 years (PSCE #19)",
                    ],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"N"},
                    "reasoning":"Flammable (Y): 56 MT propane storage — catastrophic release on vessel failure. Pressure (Y): IBR pressure vessel at 2.5-20 kg/cm² range. Property >50L (Y): Tank BLEVE = total loss of all 5 bullets + facility >>50 lakhs. Fatality (Y): BLEVE fireball radius 100m+ — multiple fatalities certain in any scenario. Most critical process in yard — ALL HHO consequences at maximum severity. → HHO.",
                    "barriers":[
                        "Dual Safety Relief Valves per tank (SAP 40020809): mandatory RULE-33, annual calibration (PSCE #16)",
                        "Liquid Inlet EFCV (SAP 40020804): 5-yearly calibration — isolates on excess flow (PSCE #11)",
                        "Liquid Outlet EFCV (SAP 40020807): 5-yearly calibration (PSCE #12)",
                        "Vapour Inlet EFCV (SAP 40020805): 5-yearly calibration (PSCE #14)",
                        "Vapour Outlet EFCV (SAP 40020806): 5-yearly calibration (PSCE #15)",
                        "Pop Action SV at Common Liquid Outlet (SAP 40020810): Hydro Test every year (PSCE #16)",
                        "Bullets Temperature Gauge (WIKA EN13192): SOC 15-35°C, SOL 45°C — operator monitoring (PSCE #10)",
                        "Bullet Pressure Gauge (WIKA EN837-1): SOC 2.5-10 kg/cm², SOL 20 kg/cm² (PSCE #13)",
                        "Entire Tank Body (PSCE #19): 3rd Party NDT + Hydro Test every 5 years (RULE-33 mandatory)",
                        "Water Sprinkler ROCV (Forbes Marshall): cools tank on fire exposure (PSCE #18)",
                        "Leak Detection Gas Sensor (World Wide Safety): propane vapour alarm in yard (PSCE #17)",
                        "Tank Liquid Level Rotogauge: SOC 15-75%, SOL 5-90% — operator level monitoring",
                    ],
                    "hazop":[
                        ("Tank Pressure HIGH",">20 kg/cm² (SOL)","SRV fails closed / solar heating / overfilling","Vessel overpressure — catastrophic rupture + BLEVE","Dual SRVs at 20 kg/cm²; operator monitoring; stop filling at 14 kg/cm² SOC max"),
                        ("Tank Temperature HIGH",">45°C (SOL)","Solar radiation / external fire / poor ventilation","Vapour pressure exceeds SRV setpoint — SRV chatters / vessel stress","Temp gauge alarm; water spray deluge; shade structure; stop filling"),
                        ("Tank Level HIGH",">90% (SOL)","Overfilling during decantation / rotogauge failure","Liquid carryover to vapour line — overpressure on compression side","Rotogauge SOL 90% — operator stop; never fill beyond 80% per SOP"),
                        ("Tank Level LOW","<5% (SOL)","Excess supply to vaporizer / EFCV failure","Vapour lock in supply — loss of supply to ETL-1 furnace","Level monitoring; vaporizer supply valve close; alternative supply"),
                        ("SRV CHATTERS","Continuous venting","Pressure cycling / over-set point","Continuous propane vent — fire risk at vent stack","SRV inspection; reduce tank pressure; operator intervention"),
                        ("External FIRE","Fire impinges on tank","Adjacent fire / ignition in yard","Tank temperature rise → pressure rise → BLEVE","Water spray deluge (PSCE #18); evacuation; fire brigade; BLEVE exclusion zone"),
                    ],
                    "bowtie":{
                        "top_event":"Propane tank BLEVE (Boiling Liquid Expanding Vapour Explosion)",
                        "causes":["External fire impinges on bullet — temperature rises uncontrolled beyond SRV capacity","Dual SRV simultaneous failure — pressure cannot be relieved","Tank body failure due to missed 5-year NDT — stress corrosion or fatigue crack","Overfilling beyond 90% SOL — liquid fills vapour space, hydraulic pressure on tank"],
                        "consequences":["BLEVE fireball — 100m+ radius incinerates everything in yard","Multiple fatalities — complete yard destruction","RULE-33 revocation — permanent closure of Propane Yard","PESO criminal prosecution of plant management"],
                        "preventions":["Dual SRVs per tank: RULE-33 mandatory (PSCE #16)","5-year NDT + Hydro Test on all bullets (PSCE #19)","Rotogauge: SOL 90% — operator stops filling","Tank temp gauge: SOL 45°C — water spray activates"],
                        "mitigations":["Water sprinkler ROCV — remote activation from >50m (PSCE #18)","Full facility evacuation — BLEVE exclusion zone 150m","Pre-positioned fire brigade with foam tender","PESO + District Emergency Authority + NDRF notification"],
                    },
                    "params":"Tank Liquid Level: SOC 15-75%, SOL 5-90% | Tank Pressure: SOC 2.5-10 kg/cm², SOL 1.5-20 kg/cm² | Tank Temperature: SOC 15-35°C, SOL 10-45°C",
                },
                {
                    "name":"4) Supply of Liquid Propane from Static Tanks to Vaporizers (ETL-1 Furnace)",
                    "cls":"HHO","color":"#f97316",
                    "substance":"Liquid Propane from outlet EFCV of tanks through supply line to vaporizers — furnace burner supply for ETL-1 Reflow Furnace",
                    "hazardous":[
                        "Liquid propane at tank pressure (2.5-10 kg/cm²) in supply pipework to vaporizer",
                        "Vaporizer: liquid propane flashes to gas — explosive vapour at vaporizer outlet",
                        "Supply line leak in furnace bay: propane + ignition sources (electrical, burner) = explosion",
                        "EFCV (SAP 40020807) on tank outlet: critical isolation on excess flow in supply line",
                        "Loss of supply to ETL-1 furnace: strip cooling in reflow — strip break / line stop",
                        "Propane heavier than air: leaks at ground level → flows along floor to ignition sources",
                    ],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"N"},
                    "reasoning":"Flammable (Y): Liquid propane supply at 2.5-10 kg/cm² — any leak ignites. Pressure (Y): supply line at tank pressure. Property >50L (Y): Supply line fire in ETL-1 bay → furnace damage + line shutdown >>50 lakhs. Fatality (Y): Vapour cloud explosion in ETL-1 bay + H2 furnace atmosphere = compound explosion hazard. → HHO.",
                    "barriers":[
                        "Outlet EFCV (SAP 40020807): auto-isolates on excess flow (loss of supply pipe) (PSCE #12)",
                        "Pop Action SV at Common Liquid Outlet Line (SAP 40020810) (PSCE #16)",
                        "Leak Detection Gas Sensor in supply line area (World Wide Safety) (PSCE #17)",
                        "Isolation valve at vaporizer inlet — closed for maintenance / emergency",
                        "Water Sprinkler ROCV: fire suppression if supply line ignites (PSCE #18)",
                        "Operator daily inspection of supply pipework for leak / corrosion",
                        "No hot work in Propane Yard or supply line area without written hot work permit",
                        "Electrical equipment in classified Zone 1 area (flameproof enclosures)",
                    ],
                    "hazop":[
                        ("Supply Pressure HIGH",">20 kg/cm² (SOL)","Vaporizer outlet blocked / downstream valve closed","Supply line overpressure — joint failure + propane release","Pop Action SV opens; EFCV isolates; operator closes supply valve"),
                        ("Supply Pressure LOW","<1.5 kg/cm²","Tank level low / EFCV partial closure","Loss of propane supply to ETL-1 furnace — strip cools","Tank level monitoring; EFCV inspection; alternative tank selection"),
                        ("Leak in Supply Line","Uncontrolled propane release","Pipe corrosion / vibration fatigue / joint failure","Propane vapour cloud in ETL-1 bay + H2 furnace = compound explosion","Leak detector alarm; isolation valve close; ETL-1 line stop; evacuation"),
                        ("EFCV FAILS OPEN","No isolation on excess flow","5-yearly calibration missed","Supply line rupture cannot be isolated","Mandatory 5-year EFCV calibration (PSCE #12); manual isolation valve as backup"),
                    ],
                    "bowtie":{
                        "top_event":"Propane leak in supply line and ignition in ETL-1 bay",
                        "causes":["Supply pipe joint failure — propane vapour in ETL-1 production bay","EFCV fails open — uncontrolled flow after pipe break","Vaporizer connection failure — liquid flash in furnace bay","Leak undetected — no gas detector coverage at supply line"],
                        "consequences":["Propane + H2 compound explosion in ETL-1 bay — catastrophic","ETL-1 line total destruction — 3-6 months shutdown","Multiple fatalities — ETL-1 operating team","PESO shutdown + insurance claim + RULE-33 investigation"],
                        "preventions":["EFCV auto-isolation on excess flow (PSCE #12)","Leak detection gas sensor in supply area (PSCE #17)","Pop Action SV at outlet line (PSCE #16)","Annual supply pipework inspection for corrosion"],
                        "mitigations":["Water sprinkler ROCV (PSCE #18)","Emergency isolation at tank outlet — remote operation","Full ETL-1 bay evacuation + H2 furnace emergency shutdown","Fire brigade + PESO notification"],
                    },
                    "params":"Supply Pressure: SOC 0-10 kg/cm², SOL <0 or >20 kg/cm² | Tank Level: SOC 15-75%, SOL 5-90% | Tank Pressure: SOC 2.5-10 kg/cm², SOL 1.5-20 kg/cm²",
                },
            ]

            for card in PROP_PSC_CARDS:
                cc = card["color"]
                st.markdown('<hr style="border:none;border-top:2px solid #1e3a5f;margin:1.5rem 0">', unsafe_allow_html=True)
                st.markdown(f'''<div style="background:{cc}10;border:1px solid {cc}40;border-left:5px solid {cc};border-radius:10px;padding:1rem 1.4rem;margin:.8rem 0"><div style="display:flex;align-items:center;gap:12px;margin-bottom:.5rem"><span style="background:{cc}20;color:{cc};border:1px solid {cc}50;font-size:.78rem;font-weight:700;padding:4px 14px;border-radius:20px">{card["cls"]}</span><span style="font-size:1.1rem;font-weight:800;color:#f1f5f9">{card["name"]}</span></div><div style="font-size:.82rem;color:#94a3b8;line-height:1.7">{card["substance"]}</div></div>''', unsafe_allow_html=True)

                d1, d2 = st.columns(2)
                with d1:
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARDOUS SUBSTANCES / ENERGIES</div>', unsafe_allow_html=True)
                    hlist = "".join(f'<div style="font-size:.78rem;color:#fca5a5;padding:3px 0;border-bottom:1px solid #1e3a5f">&#8226; {h}</div>' for h in card["hazardous"])
                    st.markdown(f'<div style="background:#1a0505;border:1px solid rgba(239,68,68,.2);border-radius:8px;padding:.8rem;margin-bottom:.8rem">{hlist}</div>', unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARD CLASSIFICATION MATRIX</div>', unsafe_allow_html=True)
                    hm = card["hazard_matrix"]
                    tblh = '<table style="border-collapse:collapse;width:100%;font-size:.72rem;margin-bottom:.8rem"><tr>'
                    for k in hm.keys():
                        tblh += f'<th style="background:#080d18;padding:5px 8px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;text-align:center">{k}</th>'
                    tblh += '</tr><tr>'
                    for v in hm.values():
                        c = "#22c55e" if v=="Y" else "#475569"
                        bg2 = "rgba(34,197,94,.1)" if v=="Y" else "#0d1f35"
                        tblh += f'<td style="background:{bg2};padding:6px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;color:{c}">{v}</td>'
                    tblh += '</tr></table>'
                    st.markdown(tblh, unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">SAFETY BARRIERS</div>', unsafe_allow_html=True)
                    for b in card["barriers"]:
                        st.markdown(f'<div style="font-size:.75rem;color:#22c55e;padding:2px 0">&#10003; {b}</div>', unsafe_allow_html=True)

                with d2:
                    cons = card["consequences"]
                    st.markdown(f'<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">CONSEQUENCE ANALYSIS  -  WHY HHO</div>', unsafe_allow_html=True)
                    for criterion, val in cons.items():
                        fc = "#ef4444" if val=="Y" else "#22c55e"
                        fbg = "rgba(239,68,68,.08)" if val=="Y" else "rgba(34,197,94,.06)"
                        st.markdown(f'<div style="background:{fbg};border:1px solid {fc}30;border-left:3px solid {fc};border-radius:6px;padding:7px 10px;margin-bottom:5px;display:flex;justify-content:space-between"><span style="font-size:.78rem;color:#e2e8f0">{criterion}</span><span style="color:{fc};font-weight:700;font-size:.82rem">{val}</span></div>', unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.6rem 0 .3rem">CLASSIFICATION REASONING</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;font-size:.74rem;color:#94a3b8;line-height:1.65">{card["reasoning"]}</div>', unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin:.6rem 0 .3rem">KEY PARAMETERS (SOC / SOL)</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.6rem .9rem;font-size:.72rem;color:#64748b;line-height:1.7">{card["params"]}</div>', unsafe_allow_html=True)

                # HAZOP
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.8rem 0 .4rem">HAZOP ANALYSIS</div>', unsafe_allow_html=True)
                htbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
                for h in ["Deviation","Parameter","Cause","Consequence","Safeguard"]:
                    htbl += f'<th style="padding:6px 9px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px">{h}</th>'
                htbl += '</tr></thead><tbody>'
                for row in card["hazop"]:
                    dev,param,cause,consq,safeg = row
                    htbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-weight:700">{dev}</td><td style="padding:6px 9px;color:#64748b;font-family:monospace">{param}</td><td style="padding:6px 9px;color:#94a3b8">{cause}</td><td style="padding:6px 9px;color:#fca5a5">{consq}</td><td style="padding:6px 9px;color:#22c55e">{safeg}</td></tr>'
                htbl += '</tbody></table></div>'
                st.markdown(htbl, unsafe_allow_html=True)

                # Bow Tie
                bt = card["bowtie"]
                st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.8rem 0 .4rem">BOW TIE ANALYSIS</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="background:#1a0505;border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:.7rem;text-align:center;margin-bottom:.6rem"><span style="color:#ef4444;font-weight:800;font-size:.85rem">TOP EVENT: {bt["top_event"]}</span></div>', unsafe_allow_html=True)
                bt1, bt2, bt3, bt4 = st.columns(4)
                with bt1:
                    st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:.3rem">CAUSES</div>', unsafe_allow_html=True)
                    for c in bt["causes"]:
                        st.markdown(f'<div class="sl-cause">{c}</div>', unsafe_allow_html=True)
                with bt2:
                    st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:.3rem">CONSEQUENCES</div>', unsafe_allow_html=True)
                    for c in bt["consequences"]:
                        st.markdown(f'<div class="sl-consq">{c}</div>', unsafe_allow_html=True)
                with bt3:
                    st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#22c55e;margin-bottom:.3rem">PREVENTIONS</div>', unsafe_allow_html=True)
                    for c in bt["preventions"]:
                        st.markdown(f'<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:7px 10px;margin-bottom:5px;font-size:.75rem;color:#86efac">{c}</div>', unsafe_allow_html=True)
                with bt4:
                    st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#f97316;margin-bottom:.3rem">MITIGATIONS</div>', unsafe_allow_html=True)
                    for c in bt["mitigations"]:
                        st.markdown(f'<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-left:3px solid #f97316;border-radius:6px;padding:7px 10px;margin-bottom:5px;font-size:.75rem;color:#fed7aa">{c}</div>', unsafe_allow_html=True)

            render_global_incidents(["Propane"])
            render_qa_bot("prop_psc")

        with prop_tabs[2]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/HOM/TINPL/PROP/001 (Doc: PSRM/PSI/HOM/TINPL/PROP/008)  ·  Dept: Propane Yard Installation  ·  Eff. Dt.: 01.05.2024</p>', unsafe_allow_html=True)
            render_glossary()

            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.4rem">HOM — HAZARD OF MATERIAL (as per PSRM/PSI/HOM/TINPL/PROP/008)</div>', unsafe_allow_html=True)
            PROP_HOM_EXCEL = [
                (1,"Propane (C3H8)","—","Non-reactive (stable hydrocarbon)","1000 ppm (ACGIH TLV-TWA)","—","LC50: 1000 ppm / LD50: Not applicable","-104°C","-42°C","2.1% vol","9.5% vol","Simple asphyxiant. Extremely Flammable Gas (Category 1). Wide flammability range 2.1-9.5%. Rapid vaporisation from liquid causes freeze burns. BLEVE risk if tank exposed to fire. Heavier than air — accumulates at ground level.","56 MT (5 tanks)"),
            ]
            hom_hdr = ["Sl.","Material","HAZCHEM Class","Reactivity","TLV","STEL","LD50 / LC50","Flash Point","Boiling Point","LFL / LEL","UFL / UEL","Other Process Hazards","Inventory"]
            hom_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.7rem"><thead><tr style="background:#080d18">'
            for hh in hom_hdr:
                hom_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            hom_tbl += '</tr></thead><tbody>'
            for r in PROP_HOM_EXCEL:
                sl,mat,cls,react,tlv,stel,ld50,flash,bp,lfl,ufl,other,inv = r
                hom_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:700;white-space:nowrap">{mat}</td><td style="padding:6px 9px;color:#94a3b8">{cls}</td><td style="padding:6px 9px;color:#94a3b8">{react}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{tlv}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{stel}</td><td style="padding:6px 9px;color:#f97316;white-space:nowrap">{ld50}</td><td style="padding:6px 9px;color:#64748b;white-space:nowrap">{flash}</td><td style="padding:6px 9px;color:#64748b;white-space:nowrap">{bp}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{lfl}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{ufl}</td><td style="padding:6px 9px;color:#fca5a5;min-width:280px">{other}</td><td style="padding:6px 9px;color:#475569">{inv}</td></tr>'
            hom_tbl += '</tbody></table></div>'
            st.markdown(hom_tbl, unsafe_allow_html=True)

            # Propane detail card
            st.markdown('''<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.4);border-left:5px solid #f97316;border-radius:12px;padding:1.2rem 1.6rem;margin:.8rem 0">
<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:.5rem;margin-bottom:.8rem">
  <div>
    <span style="background:rgba(249,115,22,.2);color:#f97316;border:1px solid rgba(249,115,22,.6);font-size:.65rem;font-weight:800;padding:3px 10px;border-radius:20px;margin-right:8px">PROPANE C3H8</span>
    <span style="font-size:1rem;font-weight:800;color:#f1f5f9">Propane (C3H8)</span>
    <div style="font-size:.74rem;color:#64748b;margin-top:.3rem">Simple Asphyxiant  ·  Category 1 Flammable Gas  ·  Heavier than air</div>
  </div>
  <div style="display:flex;gap:6px;flex-wrap:wrap">
    <span style="background:#1e3a5f;color:#60a5fa;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">CAS: 74-98-6</span>
    <span style="background:rgba(249,115,22,.15);color:#f97316;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">HAZCHEM: 2WE</span>
    <span style="background:rgba(239,68,68,.15);color:#ef4444;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">NFPA: 4-0-0</span>
  </div>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:.8rem">
  <div style="background:#080d18;border:1px solid #1e3a5f;border-top:3px solid #3b82f6;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:4px">TLV-TWA</div><div style="font-size:.74rem;font-weight:700;color:#e2e8f0">1000 ppm</div></div>
  <div style="background:#080d18;border:1px solid #1e3a5f;border-top:3px solid #a78bfa;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#a78bfa;margin-bottom:4px">STEL</div><div style="font-size:.74rem;font-weight:700;color:#e2e8f0">Not established</div></div>
  <div style="background:#1a0505;border:1px solid rgba(239,68,68,.4);border-top:3px solid #ef4444;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:4px">LEL / UEL</div><div style="font-size:.74rem;font-weight:700;color:#fca5a5">2.1% / 9.5%</div></div>
  <div style="background:#080d18;border:1px solid #1e3a5f;border-top:3px solid #22c55e;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:4px">INVENTORY</div><div style="font-size:.74rem;font-weight:700;color:#e2e8f0">56 MT</div></div>
</div>
<div style="background:#0a1020;border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.7rem">
  <div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.3rem">KEY HAZARDS</div>
  <div style="font-size:.72rem;color:#fca5a5;padding:2px 0">&#8226; Extremely Flammable Gas — Flash Point -104°C, Boiling Point -42°C</div>
  <div style="font-size:.72rem;color:#fca5a5;padding:2px 0">&#8226; BLEVE (Boiling Liquid Expanding Vapour Explosion) risk if tank exposed to fire</div>
  <div style="font-size:.72rem;color:#fca5a5;padding:2px 0">&#8226; Heavier than air — vapour accumulates at ground level, flows to drains</div>
  <div style="font-size:.72rem;color:#fca5a5;padding:2px 0">&#8226; Vapour cloud explosion risk with ignition sources</div>
  <div style="font-size:.72rem;color:#fca5a5;padding:2px 0">&#8226; Cryogenic burns from liquid propane contact (-42°C)</div>
  <div style="font-size:.72rem;color:#fca5a5;padding:2px 0">&#8226; Asphyxiation in confined spaces at high concentrations</div>
</div>
</div>''', unsafe_allow_html=True)
            render_global_incidents(["Propane"])
            render_qa_bot("prop_hom")

        # ── CIM ──────────────────────────────────────────────────
        with prop_tabs[3]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/CIM/TINPL/PROP/001 (Doc: PSRM/PSI/CIM/TINPL/PROP/007)  ·  Eff. Dt.: 01.05.2024</p>', unsafe_allow_html=True)
            render_glossary()
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.4rem">CHEMICAL INTERACTION MATRIX (CIM) — PROPANE YARD INSTALLATION</div>', unsafe_allow_html=True)

            # ── CIM Table ──────────────────────────────────────────
            cim_chems = ["Propane Liquid (C3H8)","Propane Gas (C3H8)","Air","Water"]
            cim_data = [
                ("Propane Liquid (C3H8)","NA","Non-Reactive","Non-Reactive","Non-Reactive"),
                ("Propane Gas (C3H8)","Non-Reactive","NA","Non-Reactive","Non-Reactive"),
                ("Air","Non-Reactive","Non-Reactive","NA","Non-Reactive"),
                ("Water","Non-Reactive","Non-Reactive","Non-Reactive","NA"),
            ]
            cim_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.75rem;border:1px solid #1e3a5f"><thead><tr style="background:#06111f"><th style="padding:8px 10px;color:#64748b;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;min-width:180px">Chemical / Substance</th>'
            for c in cim_chems:
                cim_tbl += f'<th style="padding:8px 10px;text-align:center;color:#60a5fa;font-size:.62rem;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap">{c}</th>'
            cim_tbl += '</tr></thead><tbody>'
            for row in cim_data:
                name = row[0]; vals = row[1:]
                cim_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:8px 10px;color:#e2e8f0;font-weight:700;border:1px solid #1e3a5f">{name}</td>'
                for v in vals:
                    if v == "NA":
                        cim_tbl += '<td style="padding:8px 10px;text-align:center;background:#060d1a;color:#475569;font-weight:700;border:1px solid #1e3a5f">NA</td>'
                    else:
                        cim_tbl += f'<td style="padding:8px 10px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(34,197,94,.12);color:#22c55e;font-size:.7rem;font-weight:700;padding:3px 10px;border-radius:20px">{v}</span></td>'
                cim_tbl += '</tr>'
            cim_tbl += '</tbody></table></div>'
            st.markdown(cim_tbl, unsafe_allow_html=True)

            st.markdown('<div style="font-size:.72rem;color:#64748b;background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:1rem">&#9432; Since Liquid Propane is a Stable Hydrocarbon, it does not react with other chemicals present at the Propane Yard. The primary hazard is from its flammable and asphyxiant properties, not chemical reactivity. The key risk is vapour cloud formation in air leading to ignition.</div>', unsafe_allow_html=True)

            # ── CAMEO Chemicals Reactivity Data ────────────────────
            st.markdown('<div class="sl-sec">CAMEO Chemicals — Reactivity Data for Propane (CAS 74-98-6)</div>', unsafe_allow_html=True)

            st.markdown("""<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.4);border-radius:10px;padding:1.2rem 1.6rem;margin-bottom:1rem">
<div style="font-size:.7rem;font-weight:700;color:#f97316;letter-spacing:1px;margin-bottom:.8rem">
  Source: CAMEO Chemicals (NOAA) — https://cameochemicals.noaa.gov/reactivity &nbsp;·&nbsp; Chemical: Propane &nbsp;·&nbsp; CAS 74-98-6
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem">
  <div>
    <div style="font-size:.65rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-bottom:.4rem">REACTIVITY PROFILE (CAMEO)</div>
    <div style="font-size:.76rem;color:#94a3b8;line-height:1.7">
      Propane is a <b style="color:#f97316">flammable gas</b>. It can be ignited by heat, sparks, or flames. Vapours are heavier than air and may travel to distant ignition sources and <b style="color:#ef4444">flash back</b>. Propane can act as a simple <b style="color:#a78bfa">asphyxiant</b> by displacing oxygen in confined spaces. Under prolonged exposure to fire or heat, the container may rupture violently — <b style="color:#ef4444">BLEVE risk</b>.
    </div>
  </div>
  <div>
    <div style="font-size:.65rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-bottom:.4rem">REACTIVITY HAZARDS WITH OTHER CHEMICALS (CAMEO)</div>
    <div style="font-size:.76rem;color:#94a3b8;line-height:1.7">
      May react violently with <b style="color:#ef4444">strong oxidizers</b> (e.g. chlorine, fluorine, O2 at high concentration). Incompatible with <b style="color:#f97316">halogenated compounds</b>. No reaction with water (Non-Reactive in CIM). No reaction with air except ignition in flammable range 2.1-9.5%.
    </div>
  </div>
</div>
</div>""", unsafe_allow_html=True)

            # CAMEO Reactivity score table
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-bottom:.4rem">CAMEO REACTIVITY CHART — PROPANE vs KEY SUBSTANCES AT PROPANE YARD</div>', unsafe_allow_html=True)
            CAMEO_REACTIVITY = [
                ("Propane (C3H8)","Air","Flammable range 2.1-9.5% — ignition = explosion/fire","HIGH","#ef4444","⚠"),
                ("Propane (C3H8)","Oxygen (O2) enriched","O2 enrichment lowers ignition energy — MORE severe ignition risk","CRITICAL","#7f1d1d","⚠⚠"),
                ("Propane (C3H8)","Strong Oxidizers (Cl2, F2)","Violent reaction — fire/explosion","HIGH","#ef4444","⚠"),
                ("Propane (C3H8)","Water (H2O)","Non-reactive — water used for cooling/fire suppression","NONE","#22c55e","✓"),
                ("Propane (C3H8)","Other Hydrocarbons","Non-reactive — may mix to form combined flammable vapour","LOW","#eab308","—"),
                ("Propane (C3H8)","KOH / NaOH (Lye)","Non-reactive","NONE","#22c55e","✓"),
                ("Propane (C3H8)","Metals (Steel)","Non-reactive — propane compatible with carbon steel at operating temp","NONE","#22c55e","✓"),
                ("Propane (C3H8)","Halogenated solvents","Possible violent reaction — avoid in propane areas","MEDIUM","#f97316","⚠"),
            ]
            cameo_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.73rem;border:1px solid #1e3a5f"><thead><tr style="background:#06111f">'
            for hh in ["Chemical A","Chemical B","Reactivity Description (CAMEO)","Risk Level","Alert"]:
                cameo_tbl += f'<th style="padding:7px 10px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            cameo_tbl += '</tr></thead><tbody>'
            for r in CAMEO_REACTIVITY:
                chemA,chemB,desc,risk,rc,alert = r
                cameo_tbl += f'<tr style="border-bottom:1px solid #1e3a5f">'
                cameo_tbl += f'<td style="padding:7px 10px;color:#e2e8f0;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap">{chemA}</td>'
                cameo_tbl += f'<td style="padding:7px 10px;color:#60a5fa;font-weight:600;border:1px solid #1e3a5f;white-space:nowrap">{chemB}</td>'
                cameo_tbl += f'<td style="padding:7px 10px;color:#94a3b8;border:1px solid #1e3a5f">{desc}</td>'
                cameo_tbl += f'<td style="padding:7px 10px;text-align:center;border:1px solid #1e3a5f"><span style="background:{rc}20;color:{rc};font-size:.65rem;font-weight:800;padding:3px 10px;border-radius:20px">{risk}</span></td>'
                cameo_tbl += f'<td style="padding:7px 10px;text-align:center;font-size:1.1rem;border:1px solid #1e3a5f;color:{rc}">{alert}</td>'
                cameo_tbl += '</tr>'
            cameo_tbl += '</tbody></table></div>'
            st.markdown(cameo_tbl, unsafe_allow_html=True)

            st.markdown('''<div style="background:#0a1020;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:1rem">
<div style="font-size:.65rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.5rem">CAMEO CHEMICALS KEY PHYSICAL CONSTANTS — PROPANE</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:.6rem;font-size:.72rem">
  <div style="background:#080d18;border:1px solid #1e3a5f;border-radius:6px;padding:.5rem;text-align:center">
    <div style="font-size:.5rem;color:#475569;font-weight:700;letter-spacing:1px">FLASH POINT</div>
    <div style="color:#ef4444;font-weight:800;margin-top:2px">-104°C</div>
  </div>
  <div style="background:#080d18;border:1px solid #1e3a5f;border-radius:6px;padding:.5rem;text-align:center">
    <div style="font-size:.5rem;color:#475569;font-weight:700;letter-spacing:1px">BOILING POINT</div>
    <div style="color:#f97316;font-weight:800;margin-top:2px">-42°C</div>
  </div>
  <div style="background:#080d18;border:1px solid #1e3a5f;border-radius:6px;padding:.5rem;text-align:center">
    <div style="font-size:.5rem;color:#475569;font-weight:700;letter-spacing:1px">LEL / UEL</div>
    <div style="color:#22c55e;font-weight:800;margin-top:2px">2.1% / 9.5%</div>
  </div>
  <div style="background:#080d18;border:1px solid #1e3a5f;border-radius:6px;padding:.5rem;text-align:center">
    <div style="font-size:.5rem;color:#475569;font-weight:700;letter-spacing:1px">VAPOUR DENSITY</div>
    <div style="color:#a78bfa;font-weight:800;margin-top:2px">1.56 (vs air=1) HEAVIER</div>
  </div>
</div>
</div>''', unsafe_allow_html=True)

            st.markdown('<div style="font-size:.65rem;color:#475569;font-family:monospace">Data Reference: CAMEO Chemicals (NOAA) — https://cameochemicals.noaa.gov/reactivity | Propane CAS 74-98-6 | For complete reactivity chart visit the CAMEO website</div>', unsafe_allow_html=True)
            render_qa_bot("prop_cim")

        with prop_tabs[4]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PDB/TINPL/PROP/001 (Doc: PSRM/PSI/PDB/TINPL/PROP/009)  ·  Dept: Propane Yard Installation  ·  Eff. Dt.: 01.05.2024</p>', unsafe_allow_html=True)
            render_glossary()
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.4rem">PROCESS DESIGN BASIS (PDB) — ALL 11 PARAMETERS WITH SOC / SOL LIMITS</div>', unsafe_allow_html=True)
            pdb_hdr = ["Sl.","Parameter","UoM","SOC Min","SOC Max","SOL Min","SOL Max","Identification / Control (SOC)","Safeguards (SOL)","PSM Critical"]
            pdb_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for hh in pdb_hdr:
                pdb_tbl += f'<th style="padding:7px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            pdb_tbl += '</tr></thead><tbody>'
            for r in PROP_PDB_ROWS:
                sl,param,uom,socmin,socmax,solmin,solmax,idcontrol,safeguard,psm = r
                pdb_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:7px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:7px 9px;color:#e2e8f0;font-weight:700;min-width:200px">{param}</td><td style="padding:7px 9px;color:#64748b;font-family:monospace">{uom}</td><td style="padding:7px 9px;color:#22c55e;font-family:monospace;font-weight:700">{socmin}</td><td style="padding:7px 9px;color:#22c55e;font-family:monospace;font-weight:700">{socmax}</td><td style="padding:7px 9px;color:#f97316;font-family:monospace">{solmin}</td><td style="padding:7px 9px;color:#f97316;font-family:monospace;font-weight:700">{solmax}</td><td style="padding:7px 9px;color:#94a3b8;min-width:200px">{idcontrol}</td><td style="padding:7px 9px;color:#64748b;min-width:200px">{safeguard}</td><td style="padding:7px 9px;text-align:center"><span style="background:rgba(239,68,68,.2);color:#f87171;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px">{psm}</span></td></tr>'
            pdb_tbl += '</tbody></table></div>'
            st.markdown(pdb_tbl, unsafe_allow_html=True)
            # Flashcards for each parameter
            st.markdown('<div class="sl-sec">Parameter Detail Cards</div>', unsafe_allow_html=True)
            for r in PROP_PDB_ROWS:
                sl,param,uom,socmin,socmax,solmin,solmax,idcontrol,safeguard,psm = r
                st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:4px solid #f97316;border-radius:10px;padding:.9rem 1.2rem;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:.6rem">
  <div><span style="color:#475569;font-size:.6rem;font-weight:700">#{sl}</span><br><span style="font-size:.88rem;font-weight:800;color:#e2e8f0">{param}</span> <span style="color:#64748b;font-size:.72rem">({uom})</span></div>
  <span style="background:rgba(239,68,68,.15);color:#ef4444;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">PSM Critical: {psm}</span>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:.6rem">
  <div style="background:#080d18;border:1px solid rgba(34,197,94,.2);border-radius:8px;padding:.5rem;text-align:center"><div style="font-size:.5rem;color:#22c55e;font-weight:700;letter-spacing:1px">SOC MIN</div><div style="font-size:.82rem;font-weight:800;color:#22c55e;font-family:monospace">{socmin}</div></div>
  <div style="background:#080d18;border:1px solid rgba(34,197,94,.2);border-radius:8px;padding:.5rem;text-align:center"><div style="font-size:.5rem;color:#22c55e;font-weight:700;letter-spacing:1px">SOC MAX</div><div style="font-size:.82rem;font-weight:800;color:#22c55e;font-family:monospace">{socmax}</div></div>
  <div style="background:#0a0505;border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.5rem;text-align:center"><div style="font-size:.5rem;color:#f97316;font-weight:700;letter-spacing:1px">SOL MIN</div><div style="font-size:.82rem;font-weight:800;color:#f97316;font-family:monospace">{solmin}</div></div>
  <div style="background:#0a0505;border:1px solid rgba(249,115,22,.2);border-radius:8px;padding:.5rem;text-align:center"><div style="font-size:.5rem;color:#f97316;font-weight:700;letter-spacing:1px">SOL MAX</div><div style="font-size:.82rem;font-weight:800;color:#f97316;font-family:monospace">{solmax}</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px">
  <div style="background:#080d18;border-radius:8px;padding:.5rem"><div style="font-size:.55rem;color:#3b82f6;font-weight:700;letter-spacing:1px;margin-bottom:3px">IDENTIFICATION / CONTROL (SOC)</div><div style="font-size:.7rem;color:#64748b;line-height:1.5">{idcontrol}</div></div>
  <div style="background:#080d18;border-radius:8px;padding:.5rem"><div style="font-size:.55rem;color:#22c55e;font-weight:700;letter-spacing:1px;margin-bottom:3px">SAFEGUARDS (SOL)</div><div style="font-size:.7rem;color:#64748b;line-height:1.5">{safeguard}</div></div>
</div>
</div>""", unsafe_allow_html=True)
            render_qa_bot("prop_pdb")

        # ── PSCE ─────────────────────────────────────────────────
        with prop_tabs[5]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PSCE/TINPL/PROP/002 (Doc: PSRM/PSI/EDB/TINPL/PROP/010)  ·  Dept: Propane Yard Installation  ·  Eff. Dt.: 01.05.2024</p>', unsafe_allow_html=True)
            render_glossary()
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.4rem">PROCESS SAFETY CRITICAL EQUIPMENT (PSCE) — PROPANE YARD  |  19 Items Identified</div>', unsafe_allow_html=True)
            psce_hdr = ["Sl.","Equipment","Consequence Based","Prevention & Mitigation","Prescriptive","PSM Critical","Justification"]
            psce_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for hh in psce_hdr:
                psce_tbl += f'<th style="padding:7px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            psce_tbl += '</tr></thead><tbody>'
            for r in PROP_PSCE_ROWS:
                sl,equip,consq,prev,presc,psm,just = r
                is_consq = bool(consq and consq != "—")
                bc = "#f97316" if is_consq else "#a78bfa"
                psce_tbl += f'<tr style="border-bottom:1px solid #1e3a5f">'
                psce_tbl += f'<td style="padding:7px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td>'
                psce_tbl += f'<td style="padding:7px 9px;color:#e2e8f0;font-weight:700;min-width:200px">{equip}</td>'
                cb_c = "#f97316" if is_consq else "#475569"
                psce_tbl += f'<td style="padding:7px 9px;color:{cb_c};font-size:.65rem">{consq if is_consq else "—"}</td>'
                psce_tbl += f'<td style="padding:7px 9px;color:#a78bfa;font-size:.65rem">{prev}</td>'
                psce_tbl += f'<td style="padding:7px 9px;text-align:center;color:{"#3b82f6" if presc!="—" else "#475569"};font-size:.65rem">{presc}</td>'
                psm_c = "#22c55e" if psm=="Yes" else "#ef4444"
                psce_tbl += f'<td style="padding:7px 9px;text-align:center"><span style="background:rgba({"34,197,94" if psm=="Yes" else "239,68,68"},.15);color:{psm_c};font-size:.65rem;font-weight:700;padding:2px 8px;border-radius:10px">{psm}</span></td>'
                psce_tbl += f'<td style="padding:7px 9px;color:#64748b;min-width:120px">{just}</td>'
                psce_tbl += '</tr>'
            psce_tbl += '</tbody></table></div>'
            st.markdown(psce_tbl, unsafe_allow_html=True)
            render_qa_bot("prop_psce")

        # ── EDB ──────────────────────────────────────────────────
        with prop_tabs[6]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/EDB/TINPL/PROP/011  ·  Dept: Propane Yard Installation  ·  Eff. Dt.: 01.05.2024  ·  Location of Docs: BAF Office</p>', unsafe_allow_html=True)
            render_glossary()
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#f97316;margin-bottom:.4rem">EQUIPMENT DESIGN BASIS (EDB) — PROPANE YARD  |  41 Items</div>', unsafe_allow_html=True)
            edb_hdr = ["Sl.","Sub-Process / Sub-System","Hazardous Substance","Equipment","Tag No. (P&ID)","SAP ID","Basis of Selection","Maint. / Calib. Schedule","Manufacturer","Model / Type","Reference Docs","Location","Remark"]
            edb_tbl = '<div style="overflow-x:auto;max-height:500px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.68rem"><thead><tr style="background:#06111f">'
            for hh in edb_hdr:
                edb_tbl += f'<th style="padding:7px 8px;text-align:left;color:#64748b;font-size:.56rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#06111f">{hh}</th>'
            edb_tbl += '</tr></thead><tbody>'
            prev_sub_p = None
            for r in PROP_EDB_ROWS:
                sl,sub,haz,equip,tag,sap,basis,sched,mfr,model,refdoc,loc,rem = r
                is_consq = "Consequence" in basis
                row_bg = "rgba(249,115,22,.04)" if is_consq else "transparent"
                if sub != prev_sub_p:
                    edb_tbl += f'<tr><td colspan="13" style="padding:5px 8px;background:#0a1628;font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#f97316;border-bottom:1px solid #1e3a5f">{sub}</td></tr>'
                    prev_sub_p = sub
                bc = "#f97316" if is_consq else "#a78bfa"
                sap_c = "#3b82f6" if sap not in ("TO BE GENERATED","—","") else "#475569"
                edb_tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{row_bg}">'
                edb_tbl += f'<td style="padding:6px 8px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#64748b;font-size:.62rem">{sub}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#fca5a5;font-size:.62rem">{haz}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#e2e8f0;font-weight:700;white-space:nowrap">{equip}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#f97316;font-family:monospace;white-space:nowrap;font-size:.62rem">{tag}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:{sap_c};font-family:monospace;font-size:.62rem;white-space:nowrap">{sap}</td>'
                edb_tbl += f'<td style="padding:6px 8px"><span style="background:{bc}15;color:{bc};font-size:.58rem;font-weight:700;padding:2px 7px;border-radius:10px;white-space:nowrap">{basis}</span></td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#64748b;white-space:nowrap;font-size:.62rem">{sched}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#94a3b8;white-space:nowrap">{mfr}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#94a3b8;white-space:nowrap;font-size:.62rem">{model}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#475569;white-space:nowrap;font-size:.62rem">{refdoc}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#475569;white-space:nowrap">{loc}</td>'
                edb_tbl += f'<td style="padding:6px 8px;color:#64748b;font-size:.6rem">{rem}</td>'
                edb_tbl += '</tr>'
            edb_tbl += '</tbody></table></div>'
            st.markdown(edb_tbl, unsafe_allow_html=True)
            render_global_incidents(["Propane"])
            render_qa_bot("prop_edb")

    elif is_h2plant:
        # ══════════════════════════════════════════════════════════
        # HYDROGEN PLANT  -  FULL PSI FROM REAL DATA
        # ══════════════════════════════════════════════════════════
        H2_TABS = ["Overview","PSC",
                   "Hazard of Material","Chem. Interaction","PDB","PSCE","EDB",
                   "Parameters"]
        h2tabs = st.tabs(H2_TABS)
        # remap: 0=Overview,1=PSC,2=HOM,3=CIM,4=PDB,5=PSCE,6=EDB,7=Parameters

        with h2tabs[0]:  # Overview
            st.markdown(f"""<div class="sl-metrics" style="grid-template-columns:repeat(5,1fr)">
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">6</div><div class="sl-metric-lbl">Sub-Processes</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#f97316">5</div><div class="sl-metric-lbl">HHO Processes</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">3</div><div class="sl-metric-lbl">Chemicals</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#e2e8f0">24</div><div class="sl-metric-lbl">Parameters</div></div>
              <div class="sl-metric"><div class="sl-metric-val" style="color:#22c55e">44</div><div class="sl-metric-lbl">PSCE Items</div></div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1rem;margin-bottom:.8rem;font-size:.78rem;color:#94a3b8;line-height:1.7">Hydrogen Plant — H2 Production and Supply. Electrolytic water splitting producing H2 (purity >99.99%) for BAF annealing hoods. Key sub-systems: Electrolyzer, Gas-Liquid Treater, H2 Purification Unit, Bullet Storage (2 × IBR vessels), Distribution. All 5 active processes are HHO. Full PSRM mandatory per Tata Steel PSRM Module.</div>', unsafe_allow_html=True)

            # Active Alerts
            st.markdown('<div class="sl-sec">Active Risk Alerts</div>', unsafe_allow_html=True)
            for txt in [
                "CRITICAL — H2 Detector at GLT (AT1701) above 0.9% LEL | Explosion risk — plant auto-trip required",
                "CRITICAL — Separator Pressure deviation (PT1001) | Overpressure — vessel rupture hazard",
                "HIGH — O2 Content in H2 above 0.2% (AT1001) | Explosive mixture — auto-vent and trip",
            ]:
                st.markdown(f'<div class="sl-alert"><div class="sl-alert-text">{txt}</div></div>', unsafe_allow_html=True)

            # PSC Summary at top (like ETL-1)
            st.markdown('<div class="sl-sec">PSC Classification Summary — All Processes</div>', unsafe_allow_html=True)
            H2_OV_PSC = [
                ("DM Water & KOH Storage/Transfer","KOH, Electric Energy","N","N","N","Y","N","N","N","N","N","LHO"),
                ("Electrolysis (H2/O2 Production)","H2, O2, DC Voltage","N","Y","Y","N","Y","Y","Y","Y","Y","HHO"),
                ("Gas/Liquid & H2/O2 Separation","H2 at 1.5 MPa","N","Y","Y","Y","N","Y","Y","Y","Y","HHO"),
                ("Purification (Deoxy + Dryer)","H2 at 0.6-1.3 MPa","N","Y","Y","N","N","Y","Y","Y","Y","HHO"),
                ("Compressed H2 Storage (Bullets)","H2 under pressure","N","Y","Y","N","N","Y","Y","Y","Y","HHO"),
                ("H2 Distribution to Annealing","H2 at pressure","N","Y","Y","N","N","Y","Y","Y","Y","HHO"),
            ]
            h2_ov_hdr = ["Process","Hazardous Substance","Toxic","Explosive","Flamm.","Corr.","Thermal","Press./Temp","Prop>50L","Fatality","Env.","HHO/LHO"]
            h2_ov_tbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.73rem;border:1px solid #1e3a5f"><thead><tr style="background:#06111f">'
            for hh in h2_ov_hdr:
                h2_ov_tbl += f'<th style="padding:7px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            h2_ov_tbl += '</tr></thead><tbody>'
            for row in H2_OV_PSC:
                proc,haz,toxic,explos,flamm,corr,therm,press,propDmg,fatal,env,cls = row
                is_hho = cls=="HHO"
                bg = "rgba(249,115,22,.03)" if is_hho else "rgba(99,102,241,.03)"
                h2_ov_tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{bg}">'
                h2_ov_tbl += f'<td style="padding:7px 9px;color:#e2e8f0;font-weight:700;border:1px solid #1e3a5f">{proc}</td>'
                h2_ov_tbl += f'<td style="padding:7px 9px;border:1px solid #1e3a5f"><span style="background:rgba(59,130,246,.1);color:#60a5fa;font-size:.62rem;padding:1px 7px;border-radius:20px">{haz}</span></td>'
                for v in [toxic,explos,flamm,corr,therm,press,propDmg,fatal,env]:
                    if v=="Y": h2_ov_tbl += '<td style="padding:7px 9px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.2);color:#f97316;font-weight:900;font-size:.72rem;padding:2px 7px;border-radius:4px">Y</span></td>'
                    else: h2_ov_tbl += '<td style="padding:7px 9px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.75rem;border:1px solid #1e3a5f">N</td>'
                cls_c = "#f97316" if is_hho else "#6366f1"
                h2_ov_tbl += f'<td style="padding:7px 9px;text-align:center;border:1px solid #1e3a5f"><span style="background:{cls_c}20;color:{cls_c};font-size:.65rem;font-weight:800;padding:3px 10px;border-radius:20px">{cls}</span></td>'
                h2_ov_tbl += '</tr>'
            h2_ov_tbl += '</tbody></table></div>'
            st.markdown(h2_ov_tbl, unsafe_allow_html=True)

            # PSRM Framework banner
            st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);border-radius:10px;padding:1rem 1.4rem;margin:1rem 0"> <div style="font-size:.82rem;font-weight:700;color:#3b82f6;margin-bottom:.5rem">PSRM CLASSIFICATION FRAMEWORK — HYDROGEN PLANT</div> <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.78rem;color:#94a3b8;line-height:1.8"> <div><b style="color:#f97316">HHO — 5 Processes</b><br>Electrolysis · Separation · Purification · Storage · Distribution<br>Requires: Full PSRM — PSI + PHA + HAZOP + Bow Tie + LOPA + Barrier Audits</div> <div><b style="color:#6366f1">LHO — 1 Process</b><br>DM Water & KOH Storage/Transfer<br>Requires: Baseline PSRM — PSI documentation only</div> </div></div>""", unsafe_allow_html=True)

            # Stats strip
            st.markdown("""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1rem">
<div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#f97316;font-family:monospace">5</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">HHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(99,102,241,.3);border-top:3px solid #6366f1;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#6366f1;font-family:monospace">1</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">LHO PROCESSES</div></div>
<div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#ef4444;font-family:monospace">3</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">CHEMICALS ONSITE</div></div>
<div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:10px;padding:.9rem;text-align:center"><div style="font-size:1.8rem;font-weight:900;color:#22c55e;font-family:monospace">44</div><div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PSCE ITEMS</div></div>
</div>""", unsafe_allow_html=True)

            # PDB Summary Table from Excel (all 24 params)
            st.markdown('<div class="sl-sec">PDB — Process Design Basis Summary (All 24 Parameters)</div>', unsafe_allow_html=True)
            h2_pdb_ov_hdr = ["Sl.","Parameter","UoM","SOC Min","SOC Max","SOL Min","SOL Max","PSM Critical"]
            h2_pdb_ov_tbl = '<div style="overflow-x:auto;max-height:340px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for hh in h2_pdb_ov_hdr:
                h2_pdb_ov_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#080d18">{hh}</th>'
            h2_pdb_ov_tbl += '</tr></thead><tbody>'
            for p in H2_PDB_PARAMS:
                psm_c = "#ef4444" if p.get("psm_critical","No")=="Yes" else "#475569"
                h2_pdb_ov_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{p["sl"]}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:600;min-width:200px">{p["param"]}</td><td style="padding:6px 9px;color:#64748b;font-family:monospace">{p["uom"]}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{p["soc_min"]}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{p["soc_max"]}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace">{p["sol_min"]}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{p["sol_max"]}</td><td style="padding:6px 9px;text-align:center"><span style="background:{psm_c}20;color:{psm_c};font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px">{p.get("psm_critical","No")}</span></td></tr>'
            h2_pdb_ov_tbl += '</tbody></table></div>'
            st.markdown(h2_pdb_ov_tbl, unsafe_allow_html=True)

            # PSCE Summary Table (all 44 items)
            st.markdown('<div class="sl-sec">PSCE — Process Safety Critical Equipment (All 44 Items)</div>', unsafe_allow_html=True)
            H2_PSCE_OV = [
                (1,"Feed Pump","Consequence Based","Service & utility","No"),(2,"Lye Pump","Consequence Based","Service & utility","No"),
                (3,"Lye Filter","Consequence Based","Service & utility","Yes"),(4,"Level Control Valve LV1001","Consequence Based","Active Preventive","Yes"),
                (5,"Pressure Control Valve PV1001","Consequence Based","Active Preventive","Yes"),(6,"CW Control Valve TV1001","Consequence Based","Active Preventive","Yes"),
                (7,"Pressure Control Valve PV1101","Consequence Based","Active Preventive","Yes"),(8,"DM Tank Level Transmitter LT1301","Consequence Based","Active Preventive","No"),
                (9,"RTD-1 at O2 line (Cell Temp)","Consequence Based","Active Preventive","Yes"),(10,"RTD-2 at O2 line (Cell Temp)","Consequence Based","Active Preventive","Yes"),
                (11,"Level Transmitter LT1003/LT1001","Consequence Based","Active Preventive","—"),(12,"Pressure Transmitter PT1001","Consequence Based","Active Preventive","Yes"),
                (13,"Analyser H2-in-O2 AT1002","Consequence Based","Active Preventive","Yes"),(14,"Analyser O2-in-H2 AT1001","Consequence Based","Active Preventive","Yes"),
                (15,"H2 Detector GLT AT1701","Consequence Based","Active Preventive","Yes"),(16,"H2 Detector Purifier AT1702","Consequence Based","Active Preventive","Yes"),
                (17,"H2 Detector DM Plant AT1703","Consequence Based","Active Preventive","Yes"),(18,"Exhaust Fan","—","Active Mitigation","No"),
                (19,"RTD at Deoxygenation Unit","Consequence Based","Active Preventive","Yes"),(20,"RTD at Dryer A/B/C","Consequence Based","Active Preventive","Yes"),
                (21,"Coolers 1131/1132/1133/1134","—","Service & utility","Yes"),(22,"Filters 1102/1103/1104/1105","—","Service & utility","Yes"),
                (23,"Dew Point Analyser MT1101","Consequence Based","Active Preventive","Yes"),(24,"Pressure Transmitter PT1101","Consequence Based","Active Preventive","Yes"),
                (25,"Filter 1151","—","Service & utility","Yes"),(26,"Trace O2 Analyser AT1102","Consequence Based","Active Preventive","Yes"),
                (27,"CW Tank Level LIT1501","Consequence Based","Active Preventive","No"),(28,"RTD at CW Line","Consequence Based","Active Preventive","Yes"),
                (29,"CW Pressure Transmitter PT1501","Consequence Based","Active Preventive","Yes"),(30,"Emergency Plant Trip Switch","—","Safety monitoring","Yes"),
                (31,"H2 Bullet #1","Consequence Based","—","Yes"),(32,"H2 Bullet #2","Consequence Based","—","Yes"),
                (33,"Pressure Gauge at Bullet 1","Consequence Based","Active Mitigation","Yes"),(34,"Safety Relief Valve #1 at Bullet 1","Consequence Based","Active Preventive","Yes"),
                (35,"Safety Relief Valve #2 at Bullet 1","Consequence Based","Active Preventive","Yes"),(36,"Safety Relief Valve #1 at Bullet 2","Consequence Based","Active Preventive","Yes"),
                (37,"Safety Relief Valve #2 at Bullet 2","Consequence Based","Active Preventive","Yes"),(38,"Pressure Gauge at Bullet 2","Consequence Based","Active Mitigation","Yes"),
                (39,"Temperature Gauge at Bullet 1","Consequence Based","Active Mitigation","Yes"),(40,"Temperature Gauge at Bullet 2","Consequence Based","Active Mitigation","Yes"),
                (41,"Pressure Control Valve #1 at Bullet Outlet","—","Controlled release","Yes"),(42,"Pressure Control Valve #2 at Bullet Outlet","—","Controlled release","Yes"),
                (43,"Pressure Relief Valve at Bullet Outlet","Consequence Based","Controlled release","Yes"),(44,"Fire Hydrant System","—","Active Mitigation","Yes"),
            ]
            psce_hdr = ["Sl.","Equipment","Basis of Selection","Type","PSM Critical"]
            psce_tbl = '<div style="overflow-x:auto;max-height:340px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for hh in psce_hdr:
                psce_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#080d18">{hh}</th>'
            psce_tbl += '</tr></thead><tbody>'
            for r in H2_PSCE_OV:
                sl,equip,basis,typ,psm = r
                is_consq = "Consequence" in basis
                bc = "#f97316" if is_consq else "#a78bfa"
                psm_c = "#22c55e" if psm=="Yes" else "#ef4444" if psm=="No" else "#475569"
                psce_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:700;min-width:200px">{equip}</td><td style="padding:6px 9px"><span style="background:{bc}15;color:{bc};font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px;white-space:nowrap">{basis}</span></td><td style="padding:6px 9px;color:#64748b;font-size:.65rem">{typ}</td><td style="padding:6px 9px;text-align:center"><span style="background:{psm_c}20;color:{psm_c};font-size:.62rem;font-weight:700;padding:2px 7px;border-radius:10px">{psm}</span></td></tr>'
            psce_tbl += '</tbody></table></div>'
            st.markdown(psce_tbl, unsafe_allow_html=True)

            # Process Cards - same format as ETL-1 (always expanded)
            st.markdown('<div class="sl-sec">Process Overview — Hydrogen Production & Supply</div>', unsafe_allow_html=True)
            h2_procs_ov = [
                ("DM Water & KOH Storage / Transfer",
                 "KOH (caustic lye 28-30%), DM water storage and transfer to electrolyser. DM tank level SOC 300-1000 mm. Conductivity SOC max 1 μS/cm. High-voltage electrical supply. KOH corrosive to skin and eyes. LHO — no explosive, flammable or toxic gas. PSI documentation only.",
                 "lho",["LHO"]),
                ("Electrolysis (H2/O2 Production) at Electrolyzer",
                 "Core process: DC current (SOC 800-1450A) splits DM water at 1.50-1.57 MPa. H2 at cathode, O2 at anode. Cell temp SOC 35-95°C. Dual lye circulating pumps (1P11/1P12). KOH electrolyte at 28-30%. H2: LEL 4%, UEL 75%. Invisible flame. Electrocution risk. Pressure vessel IBR/PESO.",
                 "hho",["HHO","PSM Required"]),
                ("Gas/Liquid & H2/O2 Separation at Separator",
                 "H2 separator (1002) and O2 separator (1003). Level SOC 500-670 mm. Pressure SOC 1.50-1.57 MPa. H2-in-O2 SOC <0.8%, SOL <1.7% (above = O2 separator explosion). LV1001 controls H2 separator level. PV1001 controls O2 separator pressure. KOH lye carryover washed.",
                 "hho",["HHO","PSM Required"]),
                ("Purification (Deoxygenation + Dryer A/B/C)",
                 "Deoxygenation bed temp SOC 118-160°C. Dryer A/B/C temp SOC 170-220°C. Dew point SOC <-80°C, SOL <-70°C (auto-trip). Trace O2 SOC <1 ppm, SOL <2 ppm (auto-vent QZ1007). Purifier pressure SOC 0.6-1.3 MPa. 4 coolers + 6 filters. H2 auto-vent valve on O2 alarm.",
                 "hho",["HHO","PSM Required"]),
                ("Compressed H2 Storage (Bullet 1 & 2)",
                 "2 × IBR pressure vessels. Pressure SOC 4-14 kg/cm², SOL 3-20 kg/cm². Temp SOC <45°C, SOL <50°C. Dual SRVs per bullet (IBR/PESO mandatory). Pressure relief valve at outlet. BLEVE risk if exposed to fire. Annual SRV inspection mandatory. PESO approved.",
                 "hho",["HHO","PSM Required"]),
                ("H2 Distribution to Annealing Hoods (BAF Lines)",
                 "H2 outlet pressure SOC 1.2-2.5 kg/cm², SOL 1-3.5 kg/cm². Distribution to all ETL-1, ETL-2 and BAF annealing lines. PRV controls outlet pressure. H2 leak at distribution joints = flammable gas cloud. Operator monitoring mandatory during H2 flow.",
                 "hho",["HHO","PSM Required"]),
            ]
            H2_OV_DETAIL = {
                "DM Water & KOH Storage / Transfer": {
                    "substance":"KOH (caustic lye 28-30%), DM water, HV electrical supply",
                    "hazardous":["KOH — corrosive to skin and eyes (TLV-C 2 mg/m³)","DM water at pressure (4.5-5 kg/cm²)","High voltage electrical supply to electrolyser"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"N","Corrosive":"Y","Thermal":"N","Pressure":"N"},
                    "params":"DM Tank Level: SOC 300-1000 mm, SOL 100-1500 mm | DM Conductivity: SOC max 1 μS/cm | CW Temp: SOC max 35°C, SOL max 40°C",
                    "psce":["Feed Pump (PSCE #1)","Lye Pump (PSCE #2)","Lye Filter (PSCE #3, PSM Critical)","DM Tank Level Transmitter LT1301 (PSCE #8)"],
                    "barriers":["Conductivity meter — blocks feed if TDS > 1 μS/cm","KOH gloves/face shield mandatory","Level alarm at 450-500mm low / 1000mm high","CW temp alarm + auto plant trip at SOL 40°C"],
                },
                "Electrolysis (H2/O2 Production) at Electrolyzer": {
                    "substance":"H2 (LEL 4%), O2 (Oxidizer), KOH lye, DC Current 800-1450A at 1.50-1.57 MPa",
                    "hazardous":["H2: Explosive LEL 4%, UEL 75% — invisible flame","O2: Oxidizer — accelerates ignition","DC Current 800-1450A — electrocution + arc flash","KOH lye — severe chemical burns","1.50-1.57 MPa IBR pressure vessel"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"Y","Pressure":"Y"},
                    "params":"Cell Temp: SOC 35-95°C, SOL 25-97°C | DC Current: SOC 800-1450A, SOL 500-1600A | Separator Level: SOC 500-670mm, SOL 400-770mm | Separator Pressure: SOC 1.50-1.57 MPa, SOL 1.65 MPa",
                    "psce":["RTD-1 at O2 line for Cell Temp (PSCE #9, PSM Critical)","RTD-2 at O2 line for Cell Temp (PSCE #10, PSM Critical)","Level Transmitter LT1003/LT1001 — Separator (PSCE #11)","Pressure Transmitter PT1001 — Separator (PSCE #12, PSM Critical)","H2 Detector GLT AT1701 (PSCE #15, PSM Critical)"],
                    "barriers":["AT1701 H2 LEL detector — auto-trip at 20% LEL","AT1002 H2-in-O2 analyser — auto-trip at 1.7% SOL","DC rectifier auto-trip at 1600A SOL","Mandatory N2 purge before H2 admission","IBR/PESO annual vessel inspection"],
                },
                "Gas/Liquid & H2/O2 Separation at Separator": {
                    "substance":"H2 at 1.50-1.57 MPa, O2, KOH lye carryover",
                    "hazardous":["H2 at 1.5 MPa — pressurized release","O2: if H2-in-O2 > 1.7% SOL = explosive mix in O2 separator","KOH lye corrosive carryover","H2 separator level loss = H2 blow-through to O2 (catastrophic)"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"Y","Thermal":"N","Pressure":"Y"},
                    "params":"H2 in O2: SOC max 0.8%, SOL max 1.7% | O2 in H2: SOC max 0.1%, SOL max 0.2% | Separator Level: SOC 500-670mm, SOL 400-770mm | Separator Pressure: SOC 1.50-1.57 MPa, SOL 1.65 MPa",
                    "psce":["Analyser H2-in-O2 AT1002 (PSCE #13, PSM Critical)","Analyser O2-in-H2 AT1001 (PSCE #14, PSM Critical)","LV1001 Level Control Valve (PSCE #4, PSM Critical)","PV1001 Pressure Control Valve (PSCE #5, PSM Critical)","H2 3-way valve QS1001 — fail-safe to vent"],
                    "barriers":["AT1002: H2-in-O2 SOL 1.7% — auto-trip + QS1001 to vent","LT1003 low-low trip at 400mm SOL — prevents H2 blow-through","QS1001 3-way valve: fail-safe to H2 vent on any trip","PV1001 O2 pressure control — SOC 1.50-1.57 MPa","IBR annual hydro test on both separator vessels"],
                },
                "Purification (Deoxygenation + Dryer A/B/C)": {
                    "substance":"H2 at 0.6-1.3 MPa through deoxy bed (118-160°C) and dryers (170-220°C)",
                    "hazardous":["H2 at 0.6-1.3 MPa at high temperature","Deoxo bed 118-160°C — catalyst runaway if O2 trace spikes","Dryer A/B/C at 170-220°C — thermal hazard","Trace O2 SOL 2 ppm — auto-vent triggers","Dew point SOL -70°C — wet H2 to annealing hoods"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"Y","Pressure":"Y"},
                    "params":"Deoxo Bed Temp: SOC 118-160°C, SOL 110-160°C | Dryer Temp A/B/C: SOC 170-220°C | Dew Point: SOC max -80°C, SOL max -70°C | Purifier Pressure: SOC 0.6-1.3 MPa, SOL 0.5-1.4 MPa | Trace O2: SOC max 1 ppm, SOL max 2 ppm",
                    "psce":["Trace O2 Analyser AT1102 (PSCE #26, PSM Critical)","Dew Point Analyser ME1101 (PSCE #23, PSM Critical)","RTD at Deoxygenation Unit (PSCE #19, PSM Critical)","RTD at Dryer A/B/C (PSCE #20, PSM Critical)","Pressure Transmitter PT1101 (PSCE #24, PSM Critical)","Coolers 1131/1132/1133/1134 (PSCE #21)","Filters 1102-1105 + 1151 (PSCE #22, #25)","PV1101 Pressure Control Valve (PSCE #7, PSM Critical)"],
                    "barriers":["AT1102: Trace O2 SOL 2 ppm — auto-opens QZ1007 H2 vent","ME1101: Dew point SOL -70°C — H2 supply trip","Deoxo bed RTD: SOL 160°C — auto shutdown + cooling","Dryer A/B/C temp monitors + auto-switch to standby","PT1101: SOL 1.4 MPa — auto-vent"],
                },
                "Compressed H2 Storage (Bullet 1 & 2)": {
                    "substance":"H2 under pressure in 2 × IBR vessels, SOC 4-14 kg/cm², SOL 20 kg/cm²",
                    "hazardous":["H2 at high pressure — BLEVE risk in fire","IBR pressure vessel — annual PESO inspection mandatory","Dual SRVs per bullet — failure = continuous H2 vent","Solar heating — pressure rise above SOC","Ignition from static discharge at vent outlet"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "params":"Bullet 1 Pressure: SOC 4-14 kg/cm², SOL 3-20 kg/cm² | Bullet 2 Pressure: SOC 4-14 kg/cm², SOL 3-20 kg/cm² | Bullet 1 Temp: SOC max 45°C, SOL max 50°C | Bullet 2 Temp: SOC max 45°C, SOL max 50°C | Outlet Pressure: SOC 1.2-2.5 kg/cm², SOL 1-3.5 kg/cm²",
                    "psce":["H2 Bullet #1 (PSCE #31, PSM Critical — Consequence Based)","H2 Bullet #2 (PSCE #32, PSM Critical — Consequence Based)","SRV #1 + SRV #2 at Bullet 1 (PSCE #34, #35 — IBR Prescriptive)","SRV #1 + SRV #2 at Bullet 2 (PSCE #36, #37 — IBR Prescriptive)","Pressure Gauge Bullet 1 (PSCE #33)","Pressure Gauge Bullet 2 (PSCE #38)","Temp Gauge Bullet 1 (PSCE #39) + Temp Gauge Bullet 2 (PSCE #40)","PRV + SRV at Bullet Outlet (PSCE #41, #42, #43)","Fire Hydrant System (PSCE #44 — Prescriptive)"],
                    "barriers":["Dual SRVs per bullet: set at 20 kg/cm² SOL (IBR mandatory)","Pressure gauge: operator monitoring SOC 4-14 kg/cm²","Temperature gauge: SOL 50°C — water spray on bullets","7.5m exclusion zone — no ignition sources","Annual IBR hydro test and NDT","Fire Hydrant System for cooling on fire exposure"],
                },
                "H2 Distribution to Annealing Hoods (BAF Lines)": {
                    "substance":"H2 at 1.2-2.5 kg/cm² through distribution piping to all ETL/BAF annealing hoods",
                    "hazardous":["H2 at pressure in distribution lines — leak = flammable cloud","H2 as protective atmosphere in annealing hoods","Flashback risk at hood interface","Distribution pipe corrosion under insulation"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                    "params":"Final Outlet Pressure: SOC 1.2-2.5 kg/cm², SOL 1-3.5 kg/cm² | Distribution pressure monitored at each annealing hood",
                    "psce":["PRV at bullet outlet — controls distribution pressure (PSCE #41/42/43)","H2 Detector AT1701/AT1702/AT1703 in various zones (PSCE #15/16/17)","Emergency Plant Trip Switch (PSCE #30 — Prescriptive)"],
                    "barriers":["H2 outlet PRV: SOC 1.2-2.5 kg/cm², auto-relief at SOL 3.5 kg/cm²","H2 LEL detector in annealing bay — alarm + evacuation trigger","Isolation valve at each annealing hood","Mandatory N2 purge of hood before H2 admission (SOP)","Annual pipe inspection for corrosion"],
                },
            }

            for name, desc, cls, tags in h2_procs_ov:
                t_html = "".join(f'<span class="sl-tag sl-tag-{"hho" if t=="HHO" else "psm" if "PSM" in t else "lho"}">{t}</span>' for t in tags)
                st.markdown(f'<div class="sl-proc {cls}"><div class="sl-proc-title">{name}</div><div class="sl-proc-desc">{desc}</div>{t_html}</div>', unsafe_allow_html=True)
                detail = H2_OV_DETAIL.get(name, {})
                if detail:
                    if True:  # always show inline — no click needed
                        cc = "#f97316" if cls=="hho" else "#6366f1"
                        # Hazard matrix row
                        hm = detail["hazard_matrix"]
                        hm_html = '<table style="border-collapse:collapse;width:100%;font-size:.72rem;margin-bottom:.8rem"><tr>'
                        for k in hm.keys():
                            hm_html += f'<th style="background:#080d18;padding:5px 8px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;text-align:center">{k}</th>'
                        hm_html += '</tr><tr>'
                        for v in hm.values():
                            vc = "#22c55e" if v=="Y" else "#475569"
                            vbg = "rgba(34,197,94,.1)" if v=="Y" else "#0d1f35"
                            hm_html += f'<td style="background:{vbg};padding:6px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;color:{vc}">{v}</td>'
                        hm_html += '</tr></table>'
                        st.markdown(hm_html, unsafe_allow_html=True)

                        d1, d2 = st.columns(2)
                        with d1:
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-bottom:.3rem">HAZARDOUS SUBSTANCES</div>', unsafe_allow_html=True)
                            for h in detail["hazardous"]:
                                st.markdown(f'<div style="font-size:.75rem;color:#fca5a5;padding:2px 0">&#8226; {h}</div>', unsafe_allow_html=True)
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin:.6rem 0 .3rem">SAFETY BARRIERS</div>', unsafe_allow_html=True)
                            for b in detail["barriers"]:
                                st.markdown(f'<div style="font-size:.75rem;color:#22c55e;padding:2px 0">&#10003; {b}</div>', unsafe_allow_html=True)
                        with d2:
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-bottom:.3rem">PSCE ITEMS (CRITICAL EQUIPMENT)</div>', unsafe_allow_html=True)
                            for p in detail["psce"]:
                                st.markdown(f'<div style="font-size:.74rem;color:#f97316;padding:2px 0">&#9679; {p}</div>', unsafe_allow_html=True)
                            st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin:.6rem 0 .3rem">KEY PARAMETERS (SOC / SOL)</div>', unsafe_allow_html=True)
                            st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.6rem .9rem;font-size:.72rem;color:#64748b;line-height:1.7">{detail["params"]}</div>', unsafe_allow_html=True)

            render_global_incidents(["H2","O2","N2"])
            render_qa_bot("h2_ov")

        with h2tabs[1]:  # PSC
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PSC/TINPL/BAF/  Rev. No.: 3  Eff. Dt.: 01.12.2020  —  Dept: Hydrogen Plant  —  Process: Hydrogen Production and Supply</p>', unsafe_allow_html=True)
            render_glossary()

            # ── EXACT EXCEL PSC TABLE ──────────────────────────────
            st.markdown('''<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:.8rem">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.2rem">PROCESS SAFETY CLASSIFICATION  —  HYDROGEN PLANT</div>
<div style="font-size:.62rem;color:#475569">Form No.: PSRM/PSI/PSC/TINPL/BAF/  ·  Rev. No.: 3/08.10.2023  ·  Eff. Dt.: 01.12.2020  ·  Doc: PSRM/PSI/PSC/TINPL/BAF/  ·  Dept: Hydrogen Plant</div>
</div>''', unsafe_allow_html=True)

            H2_PSC_EXCEL = [
                # Process | HazSub | Toxic | Explosive | Flammable | Corrosive | Thermal | Pressure/Temp | PropDmg>50L | Fatality | EnvImpact | HHO | LHO
                ("DM Water & KOH Storage / Transfer",
                 "KOH (caustic); Electrical Energy",
                 "N","N","N","Y","N","N","N","N","N","","Ö"),
                ("Electrolysis (H2/O2 Production) at Electrolyzer",
                 "H2 (Cat-1 Flammable), O2 (Oxidizer), High DC Voltage",
                 "N","Y","Y","N","Y","Y","Y","Y","Y","Ö",""),
                ("Gas/Liquid & H2/O2 Separation at Separator",
                 "H2 at Operating Pressure / Temperature",
                 "N","Y","Y","Y","N","Y","Y","Y","Y","Ö",""),
                ("Purification",
                 "H2 at Operating Pressure / Temperature",
                 "N","Y","Y","N","N","Y","Y","Y","Y","Ö",""),
                ("Compressed H2 Storage",
                 "H2 Under Pressure",
                 "N","Y","Y","N","N","Y","Y","Y","Y","Ö",""),
                ("H2 Distribution to Annealing Hoods",
                 "H2 at Pressure",
                 "N","Y","Y","N","N","Y","Y","Y","Y","Ö",""),
            ]
            H2_PSC_HDR = ["Process","Hazardous Substance / Energy","Toxic","Explosive","Flammable","Corrosive","Thermally Unstable","Pressure / Temperature","Significant Property Damage (>50 Lakhs)","Potential for Fatality","Significant Environmental Impact","HHO","LHO"]

            h2_psc_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.73rem;border:1px solid #1e3a5f"><thead>'
            h2_psc_tbl += '<tr style="background:#06111f"><th rowspan="2" style="padding:8px 10px;text-align:left;color:#94a3b8;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;min-width:200px">PROCESS<br><span style=\"color:#475569;font-weight:400\">Area: Hydrogen Plant</span></th>'
            h2_psc_tbl += '<th rowspan="2" style="padding:8px 8px;text-align:center;color:#60a5fa;font-size:.58rem;font-weight:700;border:1px solid #1e3a5f;min-width:120px">HAZARDOUS SUBSTANCE / ENERGY</th>'
            h2_psc_tbl += '<th colspan="5" style="padding:8px;text-align:center;color:#f97316;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;background:rgba(249,115,22,.08)">HAZARDOUS SUBSTANCE HAVING / CAUSING</th>'
            h2_psc_tbl += '<th colspan="3" style="padding:8px;text-align:center;color:#ef4444;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;background:rgba(239,68,68,.08)">CONSEQUENCES</th>'
            h2_psc_tbl += '<th rowspan="2" style="padding:8px 6px;text-align:center;color:#f97316;font-size:.62rem;font-weight:800;border:1px solid #1e3a5f;background:rgba(249,115,22,.12);min-width:45px">HHO</th>'
            h2_psc_tbl += '<th rowspan="2" style="padding:8px 6px;text-align:center;color:#6366f1;font-size:.62rem;font-weight:800;border:1px solid #1e3a5f;background:rgba(99,102,241,.1);min-width:45px">LHO</th></tr>'
            h2_psc_tbl += '<tr style="background:#06111f">'
            for hh in ["Toxic","Explosive","Flammable","Corrosive","Thermally Unstable"]:
                h2_psc_tbl += f'<th style="padding:7px 6px;text-align:center;color:#94a3b8;font-size:.57rem;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            for hh in ["Significant Property Damage (> 50 Lakhs)","Potential for Fatality / Multiple LTIs","Significant Environmental Impact"]:
                h2_psc_tbl += f'<th style="padding:7px 6px;text-align:center;color:#fca5a5;font-size:.55rem;font-weight:700;border:1px solid #1e3a5f;max-width:80px">{hh}</th>'
            h2_psc_tbl += '</tr></thead><tbody>'

            for di, drow in enumerate(H2_PSC_EXCEL):
                proc, haz, toxic, explos, flamm, corr, therm, press, propDmg, fatal, env, hho, lho = drow
                is_hho = hho == "Ö"
                row_bg = "rgba(249,115,22,.04)" if is_hho else "rgba(99,102,241,.03)"
                alt_bg = "rgba(249,115,22,.02)" if is_hho else "#0a1020"
                h2_psc_tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{row_bg if di%2==0 else alt_bg}">'
                h2_psc_tbl += f'<td style="padding:8px 10px;color:#e2e8f0;font-weight:700;border:1px solid #1e3a5f">{proc}</td>'
                h2_psc_tbl += f'<td style="padding:8px 8px;color:#94a3b8;font-size:.68rem;border:1px solid #1e3a5f">{haz}</td>'
                for v in [toxic,explos,flamm,corr,therm]:
                    if v == "Y":
                        h2_psc_tbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.2);color:#f97316;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                    else:
                        h2_psc_tbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                for v in [press,propDmg,fatal,env]:
                    if v == "Y":
                        h2_psc_tbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(239,68,68,.2);color:#ef4444;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                    else:
                        h2_psc_tbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                hho_c = "#f97316" if hho=="Ö" else "#475569"
                lho_c = "#6366f1" if lho=="Ö" else "#475569"
                h2_psc_tbl += f'<td style="padding:8px;text-align:center;border:1px solid #1e3a5f;font-weight:900;color:{hho_c}">{hho if hho else "—"}</td>'
                h2_psc_tbl += f'<td style="padding:8px;text-align:center;border:1px solid #1e3a5f;font-weight:900;color:{lho_c}">{lho if lho else "—"}</td>'
                h2_psc_tbl += '</tr>'
            h2_psc_tbl += '</tbody></table></div>'
            st.markdown(h2_psc_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.62rem;color:#475569;margin-bottom:1rem;font-family:monospace">Ö = Applicable  ·  N = No / Not Applicable  ·  HHO = High Hazard Operation  ·  LHO = Low Hazard Operation  ·  Source: PSRM/PSI/PSC/TINPL/BAF/ Rev.3</div>', unsafe_allow_html=True)

            # ── PSC Process Detail Cards ──────────────────────────────
            st.markdown('<div class="sl-sec">Process Safety Classification  —  Full Breakdown</div>', unsafe_allow_html=True)
            H2_PSC_CARDS = [
                {"name":"DM Water & KOH Storage / Transfer","cls":"LHO","color":"#6366f1",
                 "substance":"KOH (caustic lye 28-30%), DM water, electrical energy (HV supply)",
                 "hazardous":["KOH — corrosive to skin and eyes (TLV-C 2 mg/m³, ACGIH)","DM water at pressure (4.5-5 kg/cm²)","High voltage DC electrical supply to electrolyser","Slip hazard from lye spillage"],
                 "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"N","Corrosive":"Y","Thermal":"N","Pressure":"N"},
                 "consequences":{"Prop >50L":"N","Fatality":"N","Env. Impact":"N"},
                 "reasoning":"All 9 PSRM hazard criteria = N. KOH causes corrosive burns but no fatality pathway under credible failure. DM water at 4.5-5 kg/cm² — low energy, no explosion risk. No flammable, explosive or toxic gas present. LHO: PSI documentation only.",
                 "barriers":["KOH resistant gloves and face shield mandatory in lye handling area","DM water low-pressure interlock on feed pump","HV electrical isolation and lockout procedure","Spill containment bund around lye tank"],
                 "hazop":None,"bowtie":None,
                 "params":"DM Tank Level: SOC 300-1000 mm, SOL 100-1500 mm | Conductivity: SOC max 1 μS/cm | CW Temp: SOC max 35°C, SOL max 40°C"},
                {"name":"Electrolysis (H2/O2 Production) at Electrolyzer","cls":"HHO","color":"#f97316",
                 "substance":"H2 (Cat-1 Flammable Gas, LEL 4%), O2 (Oxidizer), KOH lye, High DC Voltage 800-1450A at 1.50-1.57 MPa",
                 "hazardous":["H2: Explosive LEL 4%, UEL 75% — colourless, odourless, invisible flame","O2: Oxidizer — accelerates ignition of all combustibles","High DC current 800-1450A — electrocution and arc flash","KOH lye at operating temperature — severe chemical burns","1.50-1.57 MPa operating pressure — IBR/PESO pressure vessel","Exothermic reaction — thermal runaway risk at high current"],
                 "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"Y","Pressure":"Y"},
                 "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                 "reasoning":"Explosive (Y): H2 produced continuously at LEL 4% — any ignition source in unventilated space = explosion. Flammable (Y): Cat-1 flammable gas production. Thermally Unstable (Y): exothermic electrolysis at high current — runaway heats lye above safe SOL. Pressure (Y): 1.5 MPa IBR vessel — rupture = massive H2 cloud release. Property >50L (Y): electrolyser replacement cost >>50 lakhs. Fatality (Y): H2 explosion + electrocution. Env (Y): H2 cloud explosion → fire → toxic combustion products.",
                 "barriers":["H2 LEL Detector AT1701 — alarm at 0.9% LEL, auto-trip at 20% LEL (PSCE #15)","O2 analyser AT1001: O2-in-H2 SOL 0.2% — auto-vent QZ1007 triggers (PSCE #14)","H2 analyser AT1002: H2-in-O2 SOL 1.7% — auto-trip electrolyser (PSCE #13)","DC current interlock SOL 1600A — automatic rectifier trip (PSCE #7)","IBR/PESO annual inspection and hydro test on all vessels","Emergency purge with N2 — hard-interlocked before restart"],
                 "hazop":[
                     ("H2 Pressure HIGH",">1.65 MPa","Pressure control valve PV1001 fails closed","Vessel overpressure — structural failure, H2 cloud, BLEVE","Pressure transmitter PT1001 alarm + auto-vent, dual SRV at 1.7 MPa"),
                     ("H2 in O2 HIGH",">1.7%","O2 separator level loss — H2 carryover","Explosive mixture in O2 separator — explosion","AT1002 auto-trip electrolyser; LV1001 level control; QS1001 3-way fail-to-vent"),
                     ("DC Current HIGH",">1600A","Rectifier malfunction / control failure","H2 over-evolution, thermal runaway, lye boil-over","Rectifier auto-trip at SOL 1600A; cell temp alarm at 97°C SOL"),
                     ("Ventilation FAILURE","Exhaust fan stops","Power cut / mechanical failure","H2 accumulates in plant building — explosive atmosphere","LEL detector auto-trip; backup exhaust fan interlock; evacuation alarm"),
                 ],
                 "bowtie":{"top_event":"H2 ignition and explosion at electrolyser",
                   "causes":["H2 accumulation due to ventilation failure","LEL detector AT1701 fails to alarm","DC current surge — H2 over-evolution beyond ventilation capacity","Ignition from arc flash at DC bus or static discharge"],
                   "consequences":["Electrolyser explosion — total loss of H2 plant","Multiple fatalities in plant building","PESO shutdown — loss of H2 supply to all BAF lines","Regulatory prosecution + CPCB notification"],
                   "preventions":["AT1701 H2 detector — auto-trip at 20% LEL","AT1002 H2-in-O2 analyser — auto-trip on >1.7%","DC rectifier current trip at 1600A SOL","Mandatory N2 purge interlock before H2 admission"],
                   "mitigations":["Blast-resistant plant building design","Roof explosion relief panels","Full plant evacuation procedure (muster at >50m upwind)","Pre-notification to PESO + emergency services"]},
                 "params":"Cell Temp: SOC 35-95°C, SOL 25-97°C | DC Current: SOC 800-1450A, SOL 500-1600A | Separator Level: SOC 500-670mm, SOL 400-770mm | Separator Pressure: SOC 1.50-1.57 MPa, SOL 1.65 MPa"},
                {"name":"Gas/Liquid & H2/O2 Separation at Separator","cls":"HHO","color":"#f97316",
                 "substance":"H2 at 1.50-1.57 MPa, O2 at operating pressure, KOH lye carryover",
                 "hazardous":["H2: Explosive at 1.5 MPa — pressurized release creates massive flammable cloud","O2: Oxidizer — any H2-in-O2 above 1.7% = explosive mixture in O2 separator","KOH lye carryover — corrosive contamination of gas streams","H2 Separator level loss — H2 blows through to O2 separator (catastrophic)","Pressure vessels — IBR/PESO statutory inspection mandatory"],
                 "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"Y","Thermal":"N","Pressure":"Y"},
                 "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                 "reasoning":"CRITICAL PROCESS — H2 and O2 must be completely separated. H2-in-O2 above 4% (LEL) in O2 separator causes violent explosion at any ignition. Analyser AT1002 monitors continuously. Level transmitter LT1003 must maintain H2 separator level above low-low trip (400mm). Pressure vessel at 1.5 MPa — IBR mandatory. All 3 HHO consequence criteria met.",
                 "barriers":["H2-in-O2 Analyser AT1002: SOL 1.7% auto-trip electrolyser + open QS1001 to vent (PSCE #13)","O2-in-H2 Analyser AT1001: SOL 0.2% — auto-vent H2 via QZ1007 (PSCE #14)","H2 Separator Level LT1003: Low-low trip at 400mm SOL — prevents H2 blow-through to O2","3-Way valve QS1001: fail-safe to H2 vent position on any trip signal","Lye Heat Exchanger (HX 1008): maintains lye at SOC temp to prevent H2 saturation","IBR/PESO annual hydro test and NDT on both separator vessels"],
                 "hazop":[
                     ("H2 in O2 HIGH",">1.7% vol","H2 separator level drops — H2 blow-through","Explosive mixture in O2 separator — catastrophic explosion","AT1002 auto-trip; LV1001 level control; LT1003 low-low trip"),
                     ("H2 Separator Level LOW","<400mm (SOL)","LV1001 fails / feed pump fails","H2 blow-through to O2 line — H2-in-O2 spike above LEL","LT1003 low-low alarm and auto-trip electrolyser"),
                     ("Separator Pressure HIGH",">1.65 MPa","PV1001 fails closed / vent valve blocked","Vessel overpressure — structural failure","Dual SRVs at 1.7 MPa; PT1001 alarm + auto-vent"),
                     ("Analyser AT1002 FAILS","No reading","Sensor failure / calibration drift","Undetected H2-in-O2 rise above 4% LEL","Manual grab sample every shift; mandatory shutdown if analyser fails >1 hour"),
                 ],
                 "bowtie":{"top_event":"H2-O2 explosive mixture ignition at separator",
                   "causes":["H2 separator level drops below 400mm — H2 blow-through to O2 stream","AT1002 analyser fails — H2-in-O2 rises undetected above LEL","LV1001 level control valve fails open — level drops rapidly","QS1001 3-way valve fails closed — H2 cannot route to vent on trip"],
                   "consequences":["O2 separator explosion — plant total destruction","Multiple fatalities — HHO consequence","PESO shutdown + regulatory prosecution","H2 supply loss to all BAF annealing lines"],
                   "preventions":["AT1002 H2-in-O2 continuous monitor SOL 1.7%","LT1003 H2 separator level trip at 400mm (SOL)","QS1001 3-way valve: fail-safe to vent","LV1001 level regulating valve: auto-control"],
                   "mitigations":["Blast-resistant separator bay","Emergency H2 vent to safe elevated location","Full plant evacuation + PESO notification","N2 purge before any restart after trip"]},
                 "params":"H2 in O2: SOC max 0.8%, SOL max 1.7% | O2 in H2: SOC max 0.1%, SOL max 0.2% | H2 Separator Level: SOC 500-670mm, SOL 400-770mm | Separator Pressure: SOC 1.50-1.57 MPa, SOL 1.65 MPa"},
                {"name":"Purification (Deoxygenation + Dryer A/B/C)","cls":"HHO","color":"#f97316",
                 "substance":"H2 at 0.6-1.3 MPa through deoxy bed (118-160°C) and dryers (170-220°C)",
                 "hazardous":["H2: Flammable at 0.6-1.3 MPa at high temperature","Deoxo bed (Pd catalyst): 118-160°C — runaway if O2 trace spikes","Dryer A/B/C: 170-220°C — thermal hazard; moisture must be <-70°C dew point","Trace O2 in H2: SOL 2 ppm — explosive mixture risk","H2 auto-vent QZ1007: opens on O2 trace alarm — uncontrolled H2 release"],
                 "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"Y","Pressure":"Y"},
                 "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                 "reasoning":"H2 at 0.6-1.3 MPa through high-temperature beds. Deoxo catalyst bed exothermic reaction with trace O2 — if O2 > SOL 2 ppm, catalyst overheats + H2 fire in bed. Dryer at 170-220°C — moisture release during regeneration + H2 = steam explosion risk. Dew point SOL -70°C — wet H2 to annealing hoods causes strip defects and potential moisture explosion in furnace.",
                 "barriers":["Trace O2 Analyser AT1102: SOL 2 ppm — auto-opens QZ1007 H2 vent (PSCE #26)","Dew Point Analyser ME1101: SOL -70°C — alarms and trips H2 supply to distribution","Deoxo bed RTD temperature: SOC 118-160°C, SOL 160°C — alarm + cooling interlock","Dryer A/B/C bed temp monitors: SOC 170-220°C — auto-switch to standby dryer","H2 purifier pressure transmitter PT1101: SOL 1.4 MPa — auto-vent","N2 purge procedure — mandatory before and after each dryer regeneration cycle"],
                 "hazop":[
                     ("Trace O2 HIGH",">2 ppm (SOL)","Upstream O2 separator partial failure / AT1002 drift","Catalyst bed overheating — H2 fire in deoxo bed","AT1102 auto-opens QZ1007 vent; AT1002 trip upstream; manual shutdown"),
                     ("Dew Point HIGH",">-70°C (SOL)","Dryer saturation / valve sequencing error","Wet H2 to annealing — furnace moisture explosion risk","ME1101 alarm + H2 supply trip; dryer switch SOP"),
                     ("Deoxo Bed Temp HIGH",">160°C","O2 spike causes exothermic runaway","Catalyst sintering — bed meltdown, H2 fire","RTD alarm, feed valve auto-close, N2 purge activation"),
                     ("Purifier Pressure HIGH",">1.4 MPa","Downstream valve closes / control failure","Vessel overpressure — rupture","PT1101 auto-vent; dual PRV at 1.5 MPa; operator manual intervention"),
                 ],
                 "bowtie":{"top_event":"H2 fire or explosion in purification unit",
                   "causes":["Trace O2 > 2 ppm SOL — exothermic reaction at deoxo catalyst","AT1102 analyser failure — undetected O2 rise","QZ1007 H2 vent valve fails closed — cannot vent on high O2 alarm","Dryer A/B/C temp > 220°C — moisture release + H2 combustion"],
                   "consequences":["Purification unit fire — >50 lakh damage","Fatality in plant area","H2 supply interruption — all BAF annealing stops","PESO investigation + regulatory action"],
                   "preventions":["AT1102 O2 trace analyser auto-trip at 2 ppm SOL","ME1101 dew point analyser H2 supply trip","Deoxo bed RTD auto-shutdown at 160°C SOL","QZ1007 H2 auto-vent: fail-safe open on loss of signal"],
                   "mitigations":["Emergency H2 plant trip button in control room","N2 purge before any restart","Fire suppression system in purification bay","PESO pre-notification protocol"]},
                 "params":"Deoxo Bed Temp: SOC 118-160°C, SOL 110-160°C | Dryer Temp A/B/C: SOC 170-220°C | Dew Point: SOC max -80°C, SOL max -70°C | Pressure: SOC 0.6-1.3 MPa, SOL 0.5-1.4 MPa | Trace O2: SOC max 1 ppm, SOL max 2 ppm"},
                {"name":"Compressed H2 Storage (Bullet 1 & Bullet 2)","cls":"HHO","color":"#f97316",
                 "substance":"H2 under pressure in 2 × IBR vessels (SOC 4-14 kg/cm², SOL 20 kg/cm²)",
                 "hazardous":["H2 at high pressure — BLEVE risk if vessel exposed to fire","Pressurized vessel — IBR/PESO statutory annual inspection mandatory","H2 release from SRV during high pressure — flammable gas cloud","Solar radiation heating — ambient temp raise increases vessel pressure","Ignition from static discharge at vent outlet"],
                 "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                 "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                 "reasoning":"H2 storage at 4-14 kg/cm² in two IBR vessels. BLEVE scenario: vessel exposed to fire → internal pressure rises beyond dual SRV capacity → vessel catastrophic failure → instant H2 release + ignition → fireball and blast wave (BLEVE). Dual SRVs per vessel are prescriptive PSRM Critical per IBR Rules. Annual PESO inspection mandatory. Bullet failure = major catastrophe.",
                 "barriers":["Dual Safety Relief Valves per bullet: SRV#1 + SRV#2 — set at 20 kg/cm² SOL (IBR mandatory)","Pressure gauge at each bullet: SOC 4-14 kg/cm², SOL 20 kg/cm² — operator monitoring","Temperature gauge: SOC max 45°C, SOL max 50°C — alerts operator to external heating","Water sprinkler / deluge on bullets — manual activation from remote station","PESO annual inspection + IBR hydro test every 5 years","No ignition sources within 7.5m exclusion zone of bullets"],
                 "hazop":[
                     ("Bullet Pressure HIGH",">20 kg/cm²","SRV fails closed / excessive filling","Vessel overpressure — catastrophic rupture + BLEVE","Dual SRV set at 20 kg/cm²; pressure gauge alarm; SOP to stop filling at 14 kg/cm²"),
                     ("Bullet Temperature HIGH",">50°C","External fire / solar radiation + inadequate ventilation","Vapour pressure rise — pressure exceeds SRV setpoint","Temp gauge alarm; water spray deluge; shade structure over bullets"),
                     ("H2 Leak at Bullet Connection","Uncontrolled release","Flange / valve packing failure","Flammable gas cloud — fire or explosion if ignited","LEL detector in storage area; no ignition sources; isolation valve SOP; N2 purge"),
                     ("SRV FAILURE","SRV chatters / fails open","Vibration / over-pressure cycling","Continuous H2 venting — gas cloud; resource loss","Dual SRV system (if one fails, other operates); regular SRV testing per IBR"),
                 ],
                 "bowtie":{"top_event":"H2 bullet BLEVE or catastrophic vessel failure",
                   "causes":["External fire impinges on H2 bullet — vessel temperature rises uncontrolled","Dual SRV failure — pressure cannot be relieved","Overfilling beyond 14 kg/cm² SOC — operator error with failed pressure gauge","Stress corrosion at vessel welds — IBR inspection missed"],
                   "consequences":["BLEVE — blast wave + fireball radius 50m+","Multiple fatalities — evacuation zone breach","Total H2 plant destruction — replacement 6-12 months","PESO criminal prosecution + plant shutdown"],
                   "preventions":["Dual SRVs at 20 kg/cm² (IBR prescriptive)","Pressure gauge + operator monitoring SOC 4-14 kg/cm²","Annual IBR hydro test and NDT","7.5m exclusion zone — no ignition sources"],
                   "mitigations":["Remote water spray deluge — manual from >20m","Blast-resistant control room","Full facility evacuation procedure","PESO + District Emergency Authority notification"]},
                 "params":"Bullet 1 Pressure: SOC 4-14 kg/cm², SOL 3-20 kg/cm² | Bullet 2 Pressure: SOC 4-14 kg/cm², SOL 3-20 kg/cm² | Bullet 1 Temp: SOC max 45°C, SOL max 50°C | Bullet 2 Temp: SOC max 45°C, SOL max 50°C | Outlet Pressure: SOC 1.2-2.5 kg/cm², SOL 1-3.5 kg/cm²"},
                {"name":"H2 Distribution to Annealing Hoods (BAF Lines)","cls":"HHO","color":"#f97316",
                 "substance":"H2 at pressure (SOC 1.2-2.5 kg/cm²) through distribution piping to all ETL-1/ETL-2/BAF annealing hoods",
                 "hazardous":["H2 at pressure in distribution lines — leak at any joint = flammable cloud","H2 as protective atmosphere in annealing hoods — accumulates if hood seals fail","Flashback risk at hood burner/H2 interface on improper sequencing","Distribution pipe corrosion under insulation — sudden failure","Isolation valve failure — loss of H2 to annealing causes strip oxidation + line loss"],
                 "hazard_matrix":{"Toxic":"N","Explosive":"Y","Flammable":"Y","Corrosive":"N","Thermal":"N","Pressure":"Y"},
                 "consequences":{"Prop >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                 "reasoning":"H2 distribution pipe failure releases flammable gas in production bay. H2 + electrical equipment ignition sources = explosion. Hood seal failure — H2 accumulates in hood enclosure, then contacts air when hood opened = deflagration. Pipe failure at PRV or joint = sudden H2 release → cloud → ignition → fatality. All 3 HHO consequences possible.",
                 "barriers":["H2 outlet PRV: SOC 1.2-2.5 kg/cm², auto-relief at SOL 3.5 kg/cm²","H2 LEL detector in annealing bay: alarm + evacuation trigger","Isolation valve at each annealing hood — closed during maintenance","Mandatory N2 purge of hood before H2 admission (SOP)","Pipe inspection: annual corrosion under insulation check","Operator continuous monitoring of distribution pressure gauge"],
                 "hazop":[
                     ("Distribution Pressure HIGH",">3.5 kg/cm²","PRV fails / downstream valve closes","Pipe overpressure — joint failure + H2 cloud","PRV auto-relief; pressure gauge alarm; operator intervention"),
                     ("H2 Leak in Bay","Uncontrolled release","Pipe corrosion / joint failure / vibration fatigue","Flammable cloud in production bay — explosion if ignited","LEL detector alarm; area evacuation; isolation valve SOP"),
                     ("Hood Seal FAILURE","H2 enters enclosure","Seal wear / improper hood lifting","H2-air mixture in hood — deflagration on contact","Mandatory N2 purge before hood opening; H2 interlock on hood lift"),
                     ("H2 Supply LOSS","Pressure <1 kg/cm²","Bullet empty / isolation valve closed inadvertently","Strip oxidation in annealing — quality loss + line stop","Pressure low alarm; automatic changeover to standby supply; operator notification"),
                 ],
                 "bowtie":{"top_event":"H2 release and ignition in production bay",
                   "causes":["Distribution pipe joint failure — H2 cloud in bay","Hood seal failure — H2 accumulation and flash on opening","PRV stuck open — continuous H2 venting into bay","Ignition from electrical equipment (motor, switch, tool spark)"],
                   "consequences":["H2 explosion in bay — equipment destruction + fatalities","Fire damage to ETL line — >50 lakh replacement","Production shutdown — loss of H2 annealing supply","PESO investigation + insurance claim"],
                   "preventions":["LEL detector in annealing bay — alarm + evacuation","PRV auto-relief at 3.5 kg/cm² SOL","Isolation valves at each hood — closed for maintenance","Annual pipe inspection for corrosion"],
                   "mitigations":["Full bay evacuation protocol","Emergency H2 isolation at plant boundary","Fire suppression in bay","PESO notification + emergency services"]},
                 "params":"Final Outlet Pressure: SOC 1.2-2.5 kg/cm², SOL 1-3.5 kg/cm² | Distribution Pipe Pressure: monitored at each annealing hood"},
            ]

            for card in H2_PSC_CARDS:
                is_hho2 = card["cls"] == "HHO"
                cc = card["color"]
                st.markdown('<hr style="border:none;border-top:2px solid #1e3a5f;margin:1.5rem 0">', unsafe_allow_html=True)
                # Header card
                st.markdown(f'''<div style="background:{cc}10;border:1px solid {cc}40;border-left:5px solid {cc};border-radius:10px;padding:1rem 1.4rem;margin:.8rem 0"><div style="display:flex;align-items:center;gap:12px;margin-bottom:.5rem"><span style="background:{cc}20;color:{cc};border:1px solid {cc}50;font-size:.78rem;font-weight:700;padding:4px 14px;border-radius:20px">{card["cls"]}</span><span style="font-size:1.1rem;font-weight:800;color:#f1f5f9">{card["name"]}</span></div><div style="font-size:.82rem;color:#94a3b8;line-height:1.7">{card["substance"]}</div></div>''', unsafe_allow_html=True)

                d1, d2 = st.columns(2)
                with d1:
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARDOUS SUBSTANCES / ENERGIES</div>', unsafe_allow_html=True)
                    hlist = "".join(f'<div style="font-size:.78rem;color:#fca5a5;padding:3px 0;border-bottom:1px solid #1e3a5f">&#8226; {h}</div>' for h in card["hazardous"])
                    st.markdown(f'<div style="background:#1a0505;border:1px solid rgba(239,68,68,.2);border-radius:8px;padding:.8rem;margin-bottom:.8rem">{hlist}</div>', unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARD CLASSIFICATION MATRIX</div>', unsafe_allow_html=True)
                    hm = card["hazard_matrix"]
                    tblh = '<table style="border-collapse:collapse;width:100%;font-size:.72rem;margin-bottom:.8rem"><tr>'
                    for k in hm.keys():
                        tblh += f'<th style="background:#080d18;padding:5px 8px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;text-align:center">{k}</th>'
                    tblh += '</tr><tr>'
                    for v in hm.values():
                        c = "#22c55e" if v=="Y" else "#475569"
                        bg2 = "rgba(34,197,94,.1)" if v=="Y" else "#0d1f35"
                        tblh += f'<td style="background:{bg2};padding:6px 8px;border:1px solid #1e3a5f;text-align:center;font-weight:700;color:{c}">{v}</td>'
                    tblh += '</tr></table>'
                    st.markdown(tblh, unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">SAFETY BARRIERS</div>', unsafe_allow_html=True)
                    for b in card["barriers"]:
                        st.markdown(f'<div style="font-size:.75rem;color:#22c55e;padding:2px 0">✓ {b}</div>', unsafe_allow_html=True)

                with d2:
                    cons = card["consequences"]
                    st.markdown(f'<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">CONSEQUENCE ANALYSIS  -  WHY {card["cls"]}</div>', unsafe_allow_html=True)
                    for criterion, val in cons.items():
                        fc = "#ef4444" if val=="Y" else "#22c55e"
                        fbg = "rgba(239,68,68,.08)" if val=="Y" else "rgba(34,197,94,.06)"
                        st.markdown(f'<div style="background:{fbg};border:1px solid {fc}30;border-left:3px solid {fc};border-radius:6px;padding:7px 10px;margin-bottom:5px;display:flex;justify-content:space-between"><span style="font-size:.78rem;color:#e2e8f0">{criterion}</span><span style="color:{fc};font-weight:700;font-size:.82rem">{val}</span></div>', unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.6rem 0 .3rem">CLASSIFICATION REASONING</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;font-size:.74rem;color:#94a3b8;line-height:1.65">{card["reasoning"]}</div>', unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin:.6rem 0 .3rem">KEY PARAMETERS (SOC / SOL)</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.6rem .9rem;font-size:.72rem;color:#64748b;line-height:1.7">{card["params"]}</div>', unsafe_allow_html=True)

                # HAZOP Table
                if card.get("hazop"):
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.8rem 0 .4rem">HAZOP ANALYSIS</div>', unsafe_allow_html=True)
                    htbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
                    for h in ["Deviation","Parameter","Cause","Consequence","Safeguard"]:
                        htbl += f'<th style="padding:6px 9px;border:1px solid #1e3a5f;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px">{h}</th>'
                    htbl += '</tr></thead><tbody>'
                    for row in card["hazop"]:
                        dev,param,cause,consq,safeg = row
                        htbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-weight:700">{dev}</td><td style="padding:6px 9px;color:#64748b;font-family:monospace">{param}</td><td style="padding:6px 9px;color:#94a3b8">{cause}</td><td style="padding:6px 9px;color:#fca5a5">{consq}</td><td style="padding:6px 9px;color:#22c55e">{safeg}</td></tr>'
                    htbl += '</tbody></table></div>'
                    st.markdown(htbl, unsafe_allow_html=True)

                # Bow Tie
                if card.get("bowtie"):
                    bt = card["bowtie"]
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.8rem 0 .4rem">BOW TIE ANALYSIS</div>', unsafe_allow_html=True)
                    st.markdown(f'<div style="background:#1a0505;border:1px solid rgba(239,68,68,.3);border-radius:8px;padding:.7rem;text-align:center;margin-bottom:.6rem"><span style="color:#ef4444;font-weight:800;font-size:.85rem">⚠ TOP EVENT: {bt["top_event"]}</span></div>', unsafe_allow_html=True)
                    bt1, bt2, bt3, bt4 = st.columns(4)
                    with bt1:
                        st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:.3rem">CAUSES</div>', unsafe_allow_html=True)
                        for c in bt["causes"]:
                            st.markdown(f'<div class="sl-cause">{c}</div>', unsafe_allow_html=True)
                    with bt2:
                        st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:.3rem">CONSEQUENCES</div>', unsafe_allow_html=True)
                        for c in bt["consequences"]:
                            st.markdown(f'<div class="sl-consq">{c}</div>', unsafe_allow_html=True)
                    with bt3:
                        st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#22c55e;margin-bottom:.3rem">PREVENTIONS</div>', unsafe_allow_html=True)
                        for c in bt["preventions"]:
                            st.markdown(f'<div style="background:rgba(34,197,94,.08);border:1px solid rgba(34,197,94,.2);border-left:3px solid #22c55e;border-radius:6px;padding:7px 10px;margin-bottom:5px;font-size:.75rem;color:#86efac">{c}</div>', unsafe_allow_html=True)
                    with bt4:
                        st.markdown('<div style="font-size:.62rem;font-weight:700;letter-spacing:1px;color:#f97316;margin-bottom:.3rem">MITIGATIONS</div>', unsafe_allow_html=True)
                        for c in bt["mitigations"]:
                            st.markdown(f'<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.2);border-left:3px solid #f97316;border-radius:6px;padding:7px 10px;margin-bottom:5px;font-size:.75rem;color:#fed7aa">{c}</div>', unsafe_allow_html=True)

            render_qa_bot("h2_psc")

        with h2tabs[2]:  # HOM
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/HOM/TINPL/ Rev.03 Eff.Dt.:08.10.2023  —  Dept: Hydrogen Plant</p>', unsafe_allow_html=True)
            render_glossary()

            # ── EXACT EXCEL HOM TABLE ──────────────────────────────
            st.markdown('''<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">HOM — HAZARD OF MATERIAL (as per PSRM/PSI/HOM/TINPL/ Rev.03)</div>''', unsafe_allow_html=True)
            H2_HOM_EXCEL = [
                # Sl | Material | Class | Reactivity | TLV | STEL | LD50/LC50 | FlashPt | BoilingPt | LFL/LEL | UFL/UEL | Other Hazards | Inventory
                (1,"Hydrogen (H2)","—","Non-reactive (inert)", "Simple Asphyxiant","Not Applicable","Not Applicable","Not Applicable","-252.9°C","4.0% vol","75% vol",
                 "Extremely Flammable Gas (H220). Very wide flammability range. Colourless, odourless, tasteless — no sensory warning. Invisible flame. Low ignition energy (0.017 mJ). Diffuses rapidly upward. Can form explosive atmosphere in enclosed space.","—"),
                (2,"Oxygen (O2)","—","Non-reactive (oxidizer)","Not Applicable","Not Applicable","Not Applicable","Not Applicable","-183°C","Not Applicable","Not Applicable",
                 "Oxygen Enrichment Hazard. Rapid oxidation and ignition risk. Accelerates combustion of all flammable materials. Contact with oil/grease = explosion hazard. O2-clean service mandatory. No sensory warning.","—"),
                (3,"Nitrogen (N2)","—","Non-reactive (inert)","Asphyxiant","Not Applicable","Not Applicable","Not Applicable","-196°C","Not Applicable","Not Applicable",
                 "Asphyxiation hazard due to oxygen displacement. High-pressure hazard during N2 purging. Can displace O2 in confined spaces — rapid incapacitation with no warning. Odourless and colourless.","—"),
            ]
            h2_hom_hdr = ["Sl.","Material","HAZCHEM Class","Reactivity","TLV","STEL","LD50 / LC50","Flash Point","Boiling Point","LFL / LEL","UFL / UEL","Other Process Hazards","Inventory"]
            h2_hom_tbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.7rem"><thead><tr style="background:#080d18">'
            for hh in h2_hom_hdr:
                h2_hom_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap">{hh}</th>'
            h2_hom_tbl += '</tr></thead><tbody>'
            for r in H2_HOM_EXCEL:
                sl,mat,cls,react,tlv,stel,ld50,flash,bp,lfl,ufl,other,inv = r
                h2_hom_tbl += f'<tr style="border-bottom:1px solid #1e3a5f">'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#e2e8f0;font-weight:700;white-space:nowrap">{mat}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#94a3b8">{cls}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#94a3b8">{react}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{tlv}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{stel}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#f97316;white-space:nowrap">{ld50}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#64748b;white-space:nowrap">{flash}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#64748b;white-space:nowrap">{bp}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{lfl}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{ufl}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#fca5a5;min-width:280px">{other}</td>'
                h2_hom_tbl += f'<td style="padding:6px 9px;color:#475569">{inv}</td></tr>'
            h2_hom_tbl += '</tbody></table></div>'
            st.markdown(h2_hom_tbl, unsafe_allow_html=True)

            # ── Chemical Detail Cards ──────────────────────────────
            st.markdown('<div class="sl-sec">Chemical Hazard Detail Cards</div>', unsafe_allow_html=True)
            H2_CHEM_CARDS = [
                {"code":"H1","name":"Hydrogen (H2)","color":"#ef4444",
                 "nfpa":"4-0-0","cas":"1333-74-0","hazchem":"2WE",
                 "class":"Extremely Flammable Gas — NFPA 4 Flammability. Category 1 Flammable Gas (H220).",
                 "tlv":"Simple Asphyxiant","stel":"Not Applicable","idlh":"Not Applicable","ld50":"Not Applicable",
                 "key_hazards":["Flammability: LEL 4%, UEL 75% — widest range of any common fuel","Colourless, odourless, invisible flame — no sensory warning","Very low ignition energy: 0.017 mJ (static spark sufficient)","Rapidly diffuses upward — can accumulate in roof spaces","BLEVE risk if heated vessel leaks in fire"],
                 "etl1_use":"Protective atmosphere in BAF annealing hoods | Purification unit storage | Distribution to all ETL lines"},
                {"code":"H2_O","name":"Oxygen (O2)","color":"#3b82f6",
                 "nfpa":"0-0-0-OX","cas":"7782-44-7","hazchem":"2W",
                 "class":"Oxidizer (UN1072). Supports and accelerates combustion. Non-flammable but promotes ignition.",
                 "tlv":"Not Applicable","stel":"Not Applicable","idlh":"Not Applicable","ld50":"Not Applicable",
                 "key_hazards":["Oxygen enrichment >23.5% — dramatically lowers ignition energy of all flammables","Contact with oil/grease = spontaneous ignition","O2-clean service required for all equipment in O2 contact","No sensory warning — monitor with O2 analyser","Vent O2 to safe elevated outdoor location"],
                 "etl1_use":"Produced as by-product at electrolyzer anode | Separated at O2 separator | Vented to atmosphere"},
                {"code":"H3","name":"Nitrogen (N2)","color":"#6366f1",
                 "nfpa":"0-0-0-SA","cas":"7727-37-9","hazchem":"2A",
                 "class":"Asphyxiant (Simple). High pressure compressed gas (UN1066). Inert, non-toxic, non-flammable.",
                 "tlv":"Asphyxiant","stel":"Not Applicable","idlh":"Asphyxia","ld50":"Not Applicable",
                 "key_hazards":["Displaces O2 in confined spaces — rapid asphyxiation with no warning","High pressure during purging — pressure vessel hazard","Colourless, odourless — no sensory warning","N2 purge before H2 admission is mandatory (prevent explosion)","Monitor O2% in area before entry"],
                 "etl1_use":"Inert purging of H2 plant before startup/shutdown | Prevents explosive H2/O2 mixture formation"},
            ]
            for card in H2_CHEM_CARDS:
                cc = card["color"]
                st.markdown(f"""<div style="background:{cc}08;border:1px solid {cc}40;border-left:5px solid {cc};border-radius:12px;padding:1.1rem 1.4rem;margin-bottom:1rem">
<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:.5rem;margin-bottom:.8rem">
  <div>
    <span style="background:{cc}20;color:{cc};border:1px solid {cc}60;font-size:.65rem;font-weight:800;padding:3px 10px;border-radius:20px;margin-right:8px">{card["code"]}</span>
    <span style="font-size:1rem;font-weight:800;color:#f1f5f9">{card["name"]}</span>
    <div style="font-size:.74rem;color:#64748b;margin-top:.3rem">{card["class"]}</div>
  </div>
  <div style="display:flex;gap:6px;flex-wrap:wrap">
    <span style="background:#1e3a5f;color:#60a5fa;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">CAS: {card["cas"]}</span>
    <span style="background:rgba(249,115,22,.15);color:#f97316;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">HAZCHEM: {card["hazchem"]}</span>
    <span style="background:rgba(167,139,250,.15);color:#a78bfa;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">NFPA: {card["nfpa"]}</span>
  </div>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:.7rem">
  <div style="background:#080d18;border:1px solid #1e3a5f;border-top:3px solid #3b82f6;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:4px">TLV-TWA</div><div style="font-size:.74rem;font-weight:700;color:#e2e8f0">{card["tlv"]}</div></div>
  <div style="background:#080d18;border:1px solid #1e3a5f;border-top:3px solid #a78bfa;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#a78bfa;margin-bottom:4px">STEL</div><div style="font-size:.74rem;font-weight:700;color:#e2e8f0">{card["stel"]}</div></div>
  <div style="background:#1a0505;border:1px solid rgba(239,68,68,.4);border-top:3px solid #ef4444;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:4px">IDLH</div><div style="font-size:.74rem;font-weight:700;color:#fca5a5">{card["idlh"]}</div></div>
  <div style="background:#080d18;border:1px solid #1e3a5f;border-top:3px solid #22c55e;border-radius:8px;padding:.6rem;text-align:center"><div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:4px">LD50 / LC50</div><div style="font-size:.74rem;font-weight:700;color:#e2e8f0">{card["ld50"]}</div></div>
</div>
<div style="background:#0a1020;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;margin-bottom:.6rem">
  <div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:.3rem">KEY HAZARDS</div>
  {''.join(f'<div style="font-size:.72rem;color:#fca5a5;padding:2px 0">&#8226; {h}</div>' for h in card["key_hazards"])}
</div>
<div style="background:{cc}10;border:1px solid {cc}30;border-radius:8px;padding:.6rem .8rem;font-size:.74rem;color:#f97316;font-weight:600">&#128269; Use: {card["etl1_use"]}</div>
</div>""", unsafe_allow_html=True)

            render_global_incidents(["H2","O2","N2"])
            render_qa_bot("h2_hom")

        with h2tabs[3]:  # CIM
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/CIM/TINPL/ Rev.03 Eff.Dt.:08.10.2023</p>', unsafe_allow_html=True)
            render_glossary()

            # Full CIM data for Hydrogen Plant  -  H2, O2, N2, KOH, H2O
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
            st.markdown('<div class="sl-sec">Chemical Interaction Grid  -  Hydrogen Plant</div>', unsafe_allow_html=True)
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
                ("HYDROGEN","Extremely Flammable Gas  -  LEL 4%, UEL 75%","Low ignition energy (0.017 mJ)","Invisible flame  -  no colour or odour"),
                ("OXYGEN","Strong Oxidiser  -  Oxygen Enrichment Hazard","Violently accelerates combustion of all flammables","Auto-trip if H2-in-O2 > 0.8% (SOC) / 1.7% (SOL)"),
                ("POTASSIUM HYDROXIDE (KOH)","Strong Base / Corrosive","Known Catalytic Activity","Generates heat with water"),
            ]
            for item in h2_react:
                name = item[0]
                props = item[1:]
                props_html = "".join(f'<div style="font-size:.75rem;color:#94a3b8;padding:2px 0">&#8226; {p}</div>' for p in props)
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


            render_qa_bot("h2_cim")
        with h2tabs[4]:  # PDB  -  full from real data
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PDB/TINPL/  ·  Rev No: 03/08.10.2023  ·  Eff. Dt.: 01.12.2020  ·  Dept: Hydrogen Plant  ·  Process: Hydrogen Production and Supply</p>', unsafe_allow_html=True)
            render_glossary()

            # ── EXACT EXCEL PDB TABLE (all 24 parameters from Excel) ──
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">PROCESS DESIGN BASIS — ALL 24 PARAMETERS WITH SOC / SOL LIMITS (Form No.: PSRM/PSI/PDB/TINPL/)</div>', unsafe_allow_html=True)

            H2_PDB_EXACT = [
                # Sl | Parameter | UoM | SOC Min | SOC Max | SOL Min | SOL Max | Consequence of SOL Deviation | Existing Safeguard (SOL) | PSM Critical
                (1,"DM Water Tank Level","mm","300","1000","100","1500","Plant trip on reaching minimum level. H2 generation stops. DM water loss / overflow risk.","Auto trip on reaching low-low level. Admin: alarm on high-high level.","No"),
                (2,"DM Water Conductivity","μS/cm","—","1","—","1","High TDS/conductivity — decrease in efficiency of electrolyser cell.","Admin: if TDS > 1 block feed to electrolyser.","No"),
                (3,"Electrolyser Cell Temperature (TE1003, TE1001)","°C","35","95","25","97","Risk of equipment damage, cell/electrode damage, high-temp KOH hazard.","Active: PLC auto-trip if temp exceeds SOL. Cooling water valve auto-adjusts.","Yes"),
                (4,"Rectifier DC Current","A","800","1450","500","1600","Overheating, cell/electrode damage, transformer overload, fire risk.","Active: Valve QS1001 trips on high current. Plant does not operate above 1450A.","Yes"),
                (5,"Separator Liquid Level","mm","500","670","400","770","Lye solution enters gas pipeline — improper separation, gas contamination.","Auto: plant trip on reaching low-low limit (400mm) / high-high limit (770mm).","Yes"),
                (6,"Separator Pressure","MPa","1.5","1.57","—","1.65","Overpressure — vessel integrity risk, rupture hazard.","Auto: plant trip on reaching HH limit 1.65 MPa. PRV present.","Yes"),
                (7,"H2 Content in O2 (H2-in-O2)","% vol","—","0.8","—","1.7","O2 separator may explode due to H2 ingress — above LEL (4%) = explosive mix.","Active: auto plant trip on reaching HH alarm (1.7%).","Yes"),
                (8,"O2 Content in H2 (O2-in-H2)","% vol","—","0.1","—","0.2","H2 separator may explode due to O2 ingress — above LOC = explosive mix.","Active: auto plant trip on reaching HH alarm (0.2%).","Yes"),
                (9,"H2 Detector (LEL % vol)","% LEL","—","0.2","—","0.9","Detection of H2 above limit — highly flammable gas cloud, explosion/fire risk.","Admin: operator checks for leakage on alarm. Active: area evacuation SOP.","Yes"),
                (10,"Deoxygenizer Bed Temperature","°C","118","160","110","160","Purity negatively impacted — dew point increases, H2 purity for annealing affected.","Active: auto plant trip on exceeding SOL temperature.","Yes"),
                (11,"Dryer A/B/C Bed Temperature","°C","170","220","—","—","Poor reaction efficiency — H2 purity affected, dryer not working in range.","Active: auto plant trip on exceeding max SOL temp.","Yes"),
                (12,"Dew Point (Purified H2)","°C","—","−80","—","−70","H2 purity affected. Specified purity not maintained — affects annealing quality.","Active: if dew point crosses SOL, auto plant trip.","Yes"),
                (13,"Purifier Pressure (H2)","MPa","0.6","1.3","0.5","1.4","Insufficient purifier performance / overpressure → vessel stress, PSV lift, leakage risk.","Admin: operator intervention. Active: auto PRV on SOL.","Yes"),
                (14,"Trace O2 at Purifier Outlet","ppm","—","1","—","2","Safety hazard if O2 mixed with H2 — explosive condition for annealing.","Active: auto vent triggered on trace O2 exceeding SOL.","Yes"),
                (15,"Cooling Water Tank Level","mm","500","900","600","1000","GLT trip / alarm. Spillage / safety hazard due to overflow.","Active: alarm and GLT auto trip on level deviation.","Yes"),
                (16,"Cooling Water Temperature","°C","—","35","—","40","Cooling efficiency drops — overheating of heat exchanger / GLT.","Active: auto plant trip.","Yes"),
                (17,"Cooling Water Pressure","kg/cm²","2.5","3.5","2","6","Insufficient cooling / pipe rupture / leakage risk.","Active: alarm on low level, plant trip on SOL. Alarm + auto trip on high.","Yes"),
                (18,"Vent Integrity","—","Crack/blockage","Damaged","Crack/blockage","Damaged","Unsafe release — failure during emergency venting — safety hazard.","Admin: operator checks vent integrity. Shutdown to repair if damaged.","No"),
                (19,"Control System / DCS Function","—","Malfunctioning","Power Off","Malfunctioning","Power Off","Loss of monitoring and control — no alarms — manual monitoring risk.","Admin: if problem persists, plant operates in manual/shutdown mode.","Yes"),
                (20,"Bullet-1 Pressure","kg/cm²","4","14","3","20","PSV lift → venting. Vessel overstress — danger to the plant and personnel.","Active: PRV available. Active: SRV available.","Yes"),
                (21,"Bullet-2 Pressure","kg/cm²","4","14","3","20","PSV lift → venting. Vessel overstress — danger to the plant and personnel.","Active: PRV available. Active: SRV available.","Yes"),
                (22,"Bullet-1 Temperature","°C","—","45","—","50","H2 storage at high temperature — safety hazard for H2 storage vessel.","Admin: water sprinkled to lower temperature.","Yes"),
                (23,"Bullet-2 Temperature","°C","—","45","—","50","H2 storage at high temperature — safety hazard for H2 storage vessel.","Admin: water sprinkled to lower temperature.","Yes"),
                (24,"Final Outlet Pressure from Bullet","kg/cm²","1.2","2.5","1","3.5","Flow interruption to user departments / excess pressure on line.","Active: PRV adjusts pressure. Admin: operator monitoring.","Yes"),
            ]

            pdb_hdr = ["Sl.","Parameter","UoM","SOC Min","SOC Max","SOL Min","SOL Max","Consequence of SOL Deviation","Existing Safeguard (SOL)","PSM Critical"]
            pdb_tbl = '<div style="overflow-x:auto;max-height:500px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.7rem"><thead><tr style="background:#080d18">'
            for hh in pdb_hdr:
                pdb_tbl += f'<th style="padding:7px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#080d18">{hh}</th>'
            pdb_tbl += '</tr></thead><tbody>'
            for r in H2_PDB_EXACT:
                sl,param,uom,socmin,socmax,solmin,solmax,consq,safeg,psm = r
                psm_c = "#22c55e" if psm=="Yes" else "#475569"
                pdb_tbl += f'<tr style="border-bottom:1px solid #1e3a5f">'
                pdb_tbl += f'<td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700;white-space:nowrap">{sl}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#e2e8f0;font-weight:700;min-width:160px">{param}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#64748b;font-family:monospace;white-space:nowrap">{uom}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700;white-space:nowrap">{socmin}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700;white-space:nowrap">{socmax}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#f97316;font-family:monospace;white-space:nowrap">{solmin}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700;white-space:nowrap">{solmax}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#fca5a5;min-width:220px;font-size:.65rem">{consq}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;color:#22c55e;min-width:200px;font-size:.65rem">{safeg}</td>'
                pdb_tbl += f'<td style="padding:6px 9px;text-align:center"><span style="background:{psm_c}20;color:{psm_c};font-size:.62rem;font-weight:700;padding:2px 7px;border-radius:10px">{psm}</span></td>'
                pdb_tbl += '</tr>'
            pdb_tbl += '</tbody></table></div>'
            st.markdown(pdb_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.62rem;color:#475569;margin-bottom:1rem;font-family:monospace">SOC = Standard Operating Condition &nbsp;·&nbsp; SOL = Safe Operating Limit &nbsp;·&nbsp; Source: PSRM/PSI/PDB/TINPL/ Rev.03 &nbsp;·&nbsp; Dept: Hydrogen Plant</div>', unsafe_allow_html=True)

            # PDB parameter cards
            st.markdown('<div class="sl-sec">Parameter Detail Cards</div>', unsafe_allow_html=True)
            render_pdb(H2_PDB_PARAMS, dept_key="h2_pdb_cards")
            render_qa_bot("h2_pdb")

        with h2tabs[5]:  # PSCE  -  full 44 items from real spreadsheet data
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/PSCE/TINPL/ Rev.03  ·  Eff. Dt.: 01.12.2020  ·  Dept: Hydrogen Plant  ·  44 PSCE Items Identified</p>', unsafe_allow_html=True)
            render_glossary()

            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">PROCESS SAFETY CRITICAL EQUIPMENT — HYDROGEN PLANT  |  44 Items (Form No.: PSRM/PSI/PSCE/TINPL/)</div>', unsafe_allow_html=True)

            H2_PSCE_EXACT = [
                # Sl | Equipment | Basis | Type | PSM Critical
                (1,"Feed Pump","Consequence Based PSRM Critical","Service and utility systems","No"),
                (2,"Lye Pump","Consequence Based PSRM Critical","Service and utility systems","No"),
                (3,"Lye Filter","Consequence Based PSRM Critical","Service and utility systems","Yes"),
                (4,"Level Control Valve (LV1001) at H2 line after separator","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (5,"Pressure Control Valve (PV1001) at O2 line after separator","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (6,"Control Valve at cooling water inlet (TV1001)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (7,"Pressure Control Valve (PV1101) at H2 line after purifier","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (8,"DM Tank Level Transmitter (LT1301)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","No"),
                (9,"Resistance Temperature Detector (RTD-1) at O2 line for Cell Temp","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (10,"Resistance Temperature Detector (RTD-2) at O2 line for Cell Temp","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (11,"Level Transmitter for Separator level (LT1003-H2, LT1001-O2)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","—"),
                (12,"Pressure Transmitter for Separator pressure (PT1001)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (13,"Analyser — H2 in O2 % (AT1002)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (14,"Analyser — O2 in H2 % (AT1001)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (15,"H2 Detector — GLT (AT1701)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (16,"H2 Detector — Purifier (AT1702)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (17,"H2 Detector — DM Plant (AT1703)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (18,"Exhaust Fan","—","Active mitigation system","No"),
                (19,"Resistance Temperature Detector (RTD) at Deoxygenation Unit","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (20,"Resistance Temperature Detector (RTD) at Dryer A, B, C","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (21,"Cooler after De-oxy, Dryer A/B/C (1131, 1132, 1133, 1134)","—","Service and utility systems","Yes"),
                (22,"Filter after De-oxy, Dryer A/B/C (1102, 1103, 1104, 1105)","—","Service and utility systems","Yes"),
                (23,"Dew Point Analyser (MT1101)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (24,"Pressure Transmitter for Purifier Pressure (PT1101)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (25,"Filter after Dryer (1151)","—","Service and utility systems","Yes"),
                (26,"Trace O2 Analyser (AT1102)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (27,"Level Transmitter for Cooling Water Tank level (LIT1501)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","No"),
                (28,"Resistance Temperature Detector (RTD) at cooling water line","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (29,"Pressure Transmitter for Cooling Water pressure (PT1501)","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (30,"Emergency Plant Trip Switch outside plant","—","Safety monitoring & emergency communication","Yes"),
                (31,"H2 Bullet #1","Consequence Based PSRM Critical","—","Yes"),
                (32,"H2 Bullet #2","Consequence Based PSRM Critical","—","Yes"),
                (33,"Pressure Gauge at Bullet 1","Consequence Based PSRM Critical","Active mitigation system","Yes"),
                (34,"Safety Relief Valve #1 at H2 Bullet 1","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (35,"Safety Relief Valve #2 at H2 Bullet 1","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (36,"Safety Relief Valve #1 at H2 Bullet 2","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (37,"Safety Relief Valve #2 at H2 Bullet 2","Consequence Based PSRM Critical","Instrumented systems (active Preventive)","Yes"),
                (38,"Pressure Gauge at Bullet 2","Consequence Based PSRM Critical","Active mitigation system","Yes"),
                (39,"Temperature Gauge at Bullet 1","Consequence Based PSRM Critical","Active mitigation system","Yes"),
                (40,"Temperature Gauge at Bullet 2","Consequence Based PSRM Critical","Active mitigation system","Yes"),
                (41,"Pressure Control Valve #1 at Outlet of H2 Bullet","—","Controlled release equipment/systems","Yes"),
                (42,"Pressure Control Valve #2 at Outlet of H2 Bullet","—","Controlled release equipment/systems","Yes"),
                (43,"Pressure Relief Valve at Bullet Outlet","Consequence Based PSRM Critical","Controlled release equipment/systems","Yes"),
                (44,"Fire Hydrant System","—","Active mitigation system","Yes"),
            ]

            psce_hdr = ["Sl.","Equipment","Basis of Selection","Type / System Category","PSM Critical"]
            psce_tbl = '<div style="overflow-x:auto;max-height:500px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.7rem"><thead><tr style="background:#080d18">'
            for hh in psce_hdr:
                psce_tbl += f'<th style="padding:7px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#080d18">{hh}</th>'
            psce_tbl += '</tr></thead><tbody>'
            for r in H2_PSCE_EXACT:
                sl,equip,basis,typ,psm = r
                is_consq = "Consequence" in basis
                bc = "#f97316" if is_consq else "#a78bfa" if basis else "#475569"
                psm_c = "#22c55e" if psm=="Yes" else "#ef4444" if psm=="No" else "#475569"
                psce_tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{"rgba(249,115,22,.03)" if is_consq else "transparent"}">'
                psce_tbl += f'<td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700;white-space:nowrap">{sl}</td>'
                psce_tbl += f'<td style="padding:6px 9px;color:#e2e8f0;font-weight:700;min-width:260px">{equip}</td>'
                psce_tbl += f'<td style="padding:6px 9px"><span style="background:{bc}15;color:{bc};font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:10px;white-space:nowrap">{basis if basis else "—"}</span></td>'
                psce_tbl += f'<td style="padding:6px 9px;color:#94a3b8;font-size:.68rem;min-width:200px">{typ}</td>'
                psce_tbl += f'<td style="padding:6px 9px;text-align:center"><span style="background:{psm_c}20;color:{psm_c};font-size:.65rem;font-weight:700;padding:3px 9px;border-radius:10px">{psm}</span></td>'
                psce_tbl += '</tr>'
            psce_tbl += '</tbody></table></div>'
            st.markdown(psce_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.62rem;color:#475569;margin-bottom:1rem;font-family:monospace">Orange = Consequence Based PSRM Critical &nbsp;·&nbsp; Purple = Prevention & Mitigation &nbsp;·&nbsp; Source: PSRM/PSI/PSCE/TINPL/ Rev.03/08.10.2023 &nbsp;·&nbsp; Dept: Hydrogen Plant</div>', unsafe_allow_html=True)
            render_qa_bot("h2_psce")

        with h2tabs[6]:  # EDB
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSRM/PSI/EDB/TINPL/PROP/001 Rev.03 Eff.Dt.:01.12.2022  —  Dept: Hydrogen Plant  —  Process: H2 Production & Supply</p>', unsafe_allow_html=True)
            render_glossary()

            # ── EXACT EXCEL EDB TABLE AT TOP ──────────────────────────
            st.markdown('''<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:.8rem">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.2rem">EQUIPMENT DESIGN BASIS  —  HYDROGEN PLANT</div>
<div style="font-size:.62rem;color:#475569">Form No.: PSRM/PSI/EDB/TINPL/PROP/001  ·  Rev. No.: 03  ·  Eff. Dt.: 01.12.2022  ·  Dept: Hydrogen Plant  ·  Location of Docs: BAF Office</div>
</div>''', unsafe_allow_html=True)

            H2_EDB_EXCEL = [
                # Sl | Sub-Process | Hazardous Substance | Equipment | Tag No | SAP ID | Basis of Selection | Schedule | Manufacturer | Model | Ref Doc | Location | Remark
                (1,  "Electrolysis of DM Water in Electrolyzer", "Hydrogen (Flammable), Lye Solution (Corrosive)", "Electrolyzer",                          "1001 / 2001",           "—",            "Consequence Based PSRM Critical",     "As per OEM schedule",        "NA",                  "—",                      "OEM Manual",          "BAF Office", "Core electrolysis unit"),
                (2,  "Electrolysis of DM Water in Electrolyzer", "Hydrogen (Flammable), Lye Solution (Corrosive)", "Feed Water Pump",                       "1M21",                  "—",            "Consequence Based PSRM Critical",     "Quarterly",                  "Milton Roy, USA",     "RB120S024X1MNN",         "OEM Manual",          "BAF Office", "DM water dosing to electrolyzer"),
                (3,  "Electrolysis of DM Water in Electrolyzer", "Hydrogen (Flammable), Lye Solution (Corrosive)", "Lye Circulating Pump",                  "1P11, 1P12",            "—",            "Consequence Based PSRM Critical",     "Quarterly",                  "DALIAN, China",       "F82-216H4M-0204Si-B-T",  "OEM Manual",          "BAF Office", "Dual pumps for redundancy"),
                (4,  "Electrolysis of DM Water in Electrolyzer", "Hydrogen (Flammable), Lye Solution (Corrosive)", "Auto Inlet Valve for DM Water Tank",    "—",                     "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Asco",                "EF8262G230",             "Vendor Manual",       "BAF Office", "Auto fill control"),
                (5,  "Electrolysis of DM Water in Electrolyzer", "Hydrogen (Flammable), Lye Solution (Corrosive)", "Manual Inlet Valve for DM Water Tank",  "—",                     "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-65TSW16T",            "Vendor Manual",       "BAF Office", "Manual isolation"),
                (6,  "Electrolysis of DM Water in Electrolyzer", "Hydrogen (Flammable)",                           "H2 Detector at DM Plant",               "AT1703",                "—",            "Prevention & Mitigation Equipment",   "Every 3 months",             "—",                   "—",                      "Calibration Record",  "BAF Office", "LEL detection at DM plant"),
                (7,  "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen (Highly Flammable), O2 (Oxidizer)",    "H2 Separator and Washer",               "1002",                  "—",            "Consequence Based PSRM Critical",     "IBR/PESO annual inspection", "NA",                  "NA",                     "OEM Manual",          "BAF Office", "Separates H2 from KOH lye carryover"),
                (8,  "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen (Highly Flammable), O2 (Oxidizer)",    "O2 Separator and Washer",               "1003",                  "—",            "Consequence Based PSRM Critical",     "IBR/PESO annual inspection", "NA",                  "NA",                     "OEM Manual",          "BAF Office", "Separates O2; statutory inspection"),
                (9,  "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen / O2",                                 "Sampling Valve — H2-in-O2 Analyser",    "J1003",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS6MM",              "Vendor Manual",       "BAF Office", "Critical — feeds AT1002 (explosion prevention)"),
                (10, "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen / O2",                                 "Sampling Valve — O2-in-H2 Analyser",    "J1004",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS6MM",              "Vendor Manual",       "BAF Office", "Critical — feeds AT1001 (explosive mix detection)"),
                (11, "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen (Flammable)",                          "By-pass Valve for H2 Vent",             "J1008",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS12MM",             "Vendor Manual",       "BAF Office", "Emergency H2 vent bypass"),
                (12, "Gas-Liquid Treater (H2/O2 Separation)",    "Oxygen (Oxidizer)",                             "By-pass Valve for O2 Vent",             "J1009",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS12MM",             "Vendor Manual",       "BAF Office", "Emergency O2 vent bypass (O2-clean service)"),
                (13, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye Solution (Corrosive)",                      "Vent Valve for Lye Heat Exchanger",     "J1010",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS8MM",              "Vendor Manual",       "BAF Office", "Lye HX vent isolation"),
                (14, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye Solution (Corrosive)",                      "Stop Valve — LT1003 Low Pressure Side", "Q1001",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63TSW8T",             "Vendor Manual",       "BAF Office", "Level transmitter impulse isolation"),
                (15, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye Solution (Corrosive)",                      "Stop Valve — LT1003 High Pressure Side","Q1002",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63TSW8T",             "Vendor Manual",       "BAF Office", "Level transmitter impulse isolation"),
                (16, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye Solution (Corrosive)",                      "Stop Valve — LT1001 Low Pressure Side", "Q1003",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63TSW8T",             "Vendor Manual",       "BAF Office", "Level transmitter impulse isolation"),
                (17, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye Solution (Corrosive)",                      "Stop Valve — LT1001 High Pressure Side","Q1004",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63TSW8T",             "Vendor Manual",       "BAF Office", "Level transmitter impulse isolation"),
                (18, "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen (Flammable)",                          "H2 Vent Valve",                         "Q1011",                 "—",            "Consequence Based PSRM Critical",     "As per schedule",            "Swagelok",            "SS-63TSW8T",             "Vendor Manual",       "BAF Office", "H2 vent during startup/shutdown purge"),
                (19, "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen (Flammable)",                          "H2 Supply Valve",                       "Q1012",                 "—",            "Consequence Based PSRM Critical",     "As per schedule",            "Swagelok",            "SS-63TSW8T",             "Vendor Manual",       "BAF Office", "H2 supply to GLT — bubble-tight"),
                (20, "Gas-Liquid Treater (H2/O2 Separation)",    "Oxygen (Oxidizer)",                             "O2 Vent Valve",                         "Q1014",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63TSW8T",             "Vendor Manual",       "BAF Office", "O2 safe vent"),
                (21, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye / H2 (Corrosive, Flammable)",              "Temperature Regulating Valve",          "TV1001",                "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Jordan Controls",     "MK78/100",               "Vendor Manual",       "BAF Office", "Controls cooling water to lye HX"),
                (22, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye / H2 (Corrosive, Flammable)",              "Liquid Level Regulating Valve",         "LV1001",                "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Jordan Controls",     "MK708/050",              "Vendor Manual",       "BAF Office", "CRITICAL: H2 separator level SOC 500-670mm"),
                (23, "Gas-Liquid Treater (H2/O2 Separation)",    "H2 / O2 (Flammable / Oxidizer)",               "Pressure Regulating Valve",             "PV1001",                "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Jordan Controls",     "MK708/050",              "Vendor Manual",       "BAF Office", "O2 separator pressure SOC 1.50-1.57 MPa"),
                (24, "Gas-Liquid Treater (H2/O2 Separation)",    "Hydrogen (Flammable)",                          "H2 Detector at GLT",                    "AT1702",                "—",            "Prevention & Mitigation Equipment",   "Every 3 months",             "—",                   "—",                      "Calibration Record",  "BAF Office", "PSCE: continuous LEL monitor; SOL 0.9% LEL"),
                (25, "Gas-Liquid Treater (H2/O2 Separation)",    "H2 (Flammable)",                                "H2 Outlet 3-Way Pneumatic Valve",       "QS1001",                "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63XTSW8T-F8-53S",     "Vendor Manual",       "BAF Office", "SAFETY: fail-safe routes H2 to vent on trip"),
                (26, "Gas-Liquid Treater (H2/O2 Separation)",    "Lye Solution (Corrosive)",                      "Lye Heat Exchanger",                    "1008",                  "—",            "Consequence Based PSRM Critical",     "Annual inspection",          "—",                   "—",                      "OEM Manual",          "BAF Office", "Cools KOH lye — failure trips at 97°C SOL"),
                (27, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "Stop Valve before H2 Inlet Pressure Gauge","J1001",             "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS12MM",             "Vendor Manual",       "BAF Office", "Gauge impulse isolation"),
                (28, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "Stop Valve before H2 Outlet Pressure Gauge","J1002",            "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS12MM",             "Vendor Manual",       "BAF Office", "Gauge impulse isolation"),
                (29, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "Stop Valve before Analyser",            "J1003",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-1KS6MM",              "Vendor Manual",       "BAF Office", "Analyser sampling isolation"),
                (30, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "N2 Inlet Check Valve",                  "H1101",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-CHF4-1",              "Vendor Manual",       "BAF Office", "Prevents H2 back-flow into N2 supply"),
                (31, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "H2 Auto Vent Valve",                    "QZ1007",                "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63TSW8T-33C",         "Vendor Manual",       "BAF Office", "SAFETY: auto-vents on O2 trace >2 ppm SOL"),
                (32, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "Filters — Deoxy + Dryers",              "1101,1102,1103,1104,1105,1151","—",    "Consequence Based PSRM Critical",     "Annual inspection",          "—",                   "—",                      "OEM Manual",          "BAF Office", "Particle filters after deoxygenation unit"),
                (33, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "Coolers after Deoxy and Dryers",        "1131, 1132, 1133, 1134","—",           "Consequence Based PSRM Critical",     "Annual inspection",          "—",                   "—",                      "OEM Manual",          "BAF Office", "4 coolers after high-temp purification stages"),
                (34, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "H2 Detector at Purification Unit",      "AT1702",                "—",            "Prevention & Mitigation Equipment",   "Every 3 months",             "—",                   "—",                      "Calibration Record",  "BAF Office", "PSCE: continuous LEL detection; SOL 0.9%"),
                (35, "Hydrogen Purification Unit",                "Hydrogen (Highly Flammable)",                   "H2 Outlet Pressure Regulator",          "PV1101",                "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Jordan Controls",     "MK708/050",              "Vendor Manual",       "BAF Office", "Controls H2 outlet pressure SOC 0.6-1.3 MPa"),
                (36, "Drainage System",                           "Lye Solution / Water with Gas Traces",          "Drainage Valve of Electrolyzer",        "Q1021, Q2021",          "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "—",                   "—",                      "Vendor Manual",       "BAF Office", "Electrolyzer drain isolation"),
                (37, "Drainage System",                           "Lye Solution (Corrosive)",                      "Drainage Valve at Bottom of Lye Tank",  "Q1312",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "—",                      "Vendor Manual",       "BAF Office", "Lye tank drain isolation"),
                (38, "Drainage System",                           "DM Water",                                      "Drainage Valve at Bottom of Water Tank","Q1305",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "—",                   "—",                      "Vendor Manual",       "BAF Office", "DM water tank drain"),
                (39, "Drainage System",                           "DM Water",                                      "Drain Valve for DM Tank",               "Q1502",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Modentic",            "V-205S 3/4 inch",            "Vendor Manual",       "BAF Office", "DM tank drain valve"),
                (40, "CW Circulation Unit",                       "Heat from GLT / Purification Unit",             "Cooling Water Inlet Valve for GLT",     "Q1051",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-67TSW24P",            "Vendor Manual",       "BAF Office", "CW inlet to GLT"),
                (41, "CW Circulation Unit",                       "Heat from GLT / Purification Unit",             "Cooling Water Outlet Valve for GLT",    "Q1052",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-67TSW24P",            "Vendor Manual",       "BAF Office", "CW outlet from GLT"),
                (42, "CW Circulation Unit",                       "Heat from GLT / Purification Unit",             "CW Inlet Valve for H2 Purification Unit","Q1141",                "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-67TSW20P",            "Vendor Manual",       "BAF Office", "CW inlet to purifier"),
                (43, "CW Circulation Unit",                       "Heat from GLT / Purification Unit",             "CW Outlet Valve for H2 Purification Unit","Q1142",               "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-67TSW20P",            "Vendor Manual",       "BAF Office", "CW outlet from purifier"),
                (44, "CW Circulation Unit",                       "Heat from GLT / Purification Unit",             "Water Inlet Valve for Water Sealer",    "Q1111",                 "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-63TSW12T",            "Vendor Manual",       "BAF Office", "Water sealer supply isolation"),
                (45, "CW Circulation Unit",                       "Heat from GLT / Purification Unit",             "Water Inlet Check Valve for Water Sealer","H1111",               "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "Swagelok",            "SS-CHF12-1",             "Vendor Manual",       "BAF Office", "Prevents backflow into water sealer supply"),
                (46, "Control Cabinet (PLC/Sensors)",             "Faulty Sensors / Wrong PLC Instruction",        "Dew Point Analyser",                    "ME1101",                "—",            "Consequence Based PSRM Critical",     "Every 6 months",             "NA",                  "MTS6",                   "Calibration Record",  "BAF Office", "PSCE: dew point SOC <-80°C; trip at <-70°C"),
                (47, "Control Cabinet (PLC/Sensors)",             "Faulty Sensors / Wrong PLC Instruction",        "Solenoid Valve 2-Position 5-Way",       "YV1001, YV1107-YV1114", "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "NA",                  "521 00 004",             "OEM Manual",          "BAF Office", "Controls safety pneumatic actuators; fail-safe"),
                (48, "Control Cabinet (PLC/Sensors)",             "Faulty Sensors / Wrong PLC Instruction",        "Solenoid Valve 2-Position 5-Way",       "YV1101-YV1103",         "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "NA",                  "521 00 008",             "OEM Manual",          "BAF Office", "Controls dryer switching solenoids"),
                (49, "Control Cabinet (PLC/Sensors)",             "Faulty Sensors / Wrong PLC Instruction",        "Instrument Air Distributor",            "QB1",                   "—",            "Prevention & Mitigation Equipment",   "As per schedule",            "NA",                  "NA",                     "OEM Manual",          "BAF Office", "Air supply to all pneumatic safety valves"),
                (50, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Pressure Gauge at Bullet 1",            "—",                     "—",            "Consequence Based PSRM Critical",     "Annual inspection (IBR)",    "—",                   "—",                      "IBR Certificate",     "BAF Office", "Local indication SOC 4-14 kg/cm²; SOL 20 kg/cm²"),
                (51, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Pressure Relief Valve at Bullet 1",     "—",                     "—",            "Consequence Based PSRM Critical",     "Annual IBR/PESO inspection", "—",                   "—",                      "PESO Certificate",    "BAF Office", "Primary overpressure protection; statutory"),
                (52, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Safety Relief Valve at Bullet 1",       "—",                     "—",            "Prevention & Mitigation Equipment",   "Annual inspection & test",   "—",                   "—",                      "PESO Certificate",    "BAF Office", "Redundant SRV; IBR statutory requirement"),
                (53, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Pressure Gauge at Bullet 2",            "—",                     "—",            "Consequence Based PSRM Critical",     "Annual inspection (IBR)",    "—",                   "—",                      "IBR Certificate",     "BAF Office", "Same spec as Bullet 1; SOL 20 kg/cm²"),
                (54, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Pressure Relief Valve at Bullet 2",     "—",                     "—",            "Consequence Based PSRM Critical",     "Annual IBR/PESO inspection", "—",                   "—",                      "PESO Certificate",    "BAF Office", "Statutory overpressure protection"),
                (55, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Safety Relief Valve at Bullet 2",       "—",                     "—",            "Prevention & Mitigation Equipment",   "Annual inspection & test",   "—",                   "—",                      "PESO Certificate",    "BAF Office", "Redundant SRV; IBR/PESO statutory"),
                (56, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Temperature Gauge at Bullet 1",         "—",                     "—",            "Consequence Based PSRM Critical",     "Annual inspection",          "—",                   "—",                      "IBR Certificate",     "BAF Office", "PSCE: SOC <45°C; SOL <50°C"),
                (57, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Temperature Gauge at Bullet 2",         "—",                     "—",            "Consequence Based PSRM Critical",     "Annual inspection",          "—",                   "—",                      "IBR Certificate",     "BAF Office", "PSCE: same spec as Bullet 1; SOL <50°C"),
                (58, "H2 Bullet Storage",                         "Hydrogen (Highly Flammable, Pressurized)",      "Pressure Relief Valve at Bullet Outlet","—",                     "—",            "Prevention & Mitigation Equipment",   "Annual inspection & test",   "—",                   "—",                      "PESO Certificate",    "BAF Office", "Overpressure protection on H2 outlet line"),
            ]

            edb_h2_hdr = ["Sl.","Sub-Process / Sub-System","Hazardous Substance","Equipment","Tag No. (P&ID)","SAP ID","Basis of Selection","Maint. / Calib. Schedule","Manufacturer","Model / Type","Reference Docs","Location","Remark"]
            edb_h2_tbl = '<div style="overflow-x:auto;max-height:500px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.68rem"><thead><tr style="background:#06111f">'
            for hh in edb_h2_hdr:
                edb_h2_tbl += f'<th style="padding:7px 8px;text-align:left;color:#64748b;font-size:.56rem;font-weight:700;letter-spacing:1px;border-bottom:2px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#06111f">{hh}</th>'
            edb_h2_tbl += '</tr></thead><tbody>'
            prev_sub = None
            for r in H2_EDB_EXCEL:
                sl, sub, haz, equip, tag, sap, basis, sched, mfr, model, refdoc, loc, rem = r
                is_consq = "Consequence" in basis
                row_bg = "rgba(249,115,22,.04)" if is_consq else "transparent"
                if sub != prev_sub:
                    edb_h2_tbl += f'<tr><td colspan="13" style="padding:5px 8px;background:#0a1628;font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;border-bottom:1px solid #1e3a5f">{sub}</td></tr>'
                    prev_sub = sub
                basis_c = "#f97316" if is_consq else "#a78bfa"
                edb_h2_tbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{row_bg}">'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#64748b;font-size:.62rem">{sub}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#fca5a5;font-size:.62rem">{haz}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#e2e8f0;font-weight:700;white-space:nowrap">{equip}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#f97316;font-family:monospace;white-space:nowrap">{tag}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#3b82f6;font-family:monospace;font-size:.62rem;white-space:nowrap">{sap}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px"><span style="background:{basis_c}15;color:{basis_c};font-size:.58rem;font-weight:700;padding:2px 7px;border-radius:10px;white-space:nowrap">{basis}</span></td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#64748b;white-space:nowrap;font-size:.62rem">{sched}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#94a3b8;white-space:nowrap">{mfr}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#94a3b8;white-space:nowrap">{model}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#475569;white-space:nowrap;font-size:.62rem">{refdoc}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#475569;white-space:nowrap">{loc}</td>'
                edb_h2_tbl += f'<td style="padding:6px 8px;color:#64748b;font-size:.62rem">{rem}</td>'
                edb_h2_tbl += '</tr>'
            edb_h2_tbl += '</tbody></table></div>'
            st.markdown(edb_h2_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.62rem;color:#475569;margin-bottom:1rem;font-family:monospace">Orange row = Consequence Based PSRM Critical &nbsp;·&nbsp; Purple badge = Prevention & Mitigation Equipment &nbsp;·&nbsp; Source: PSRM/PSI/EDB/TINPL/PROP/001 Rev.03</div>', unsafe_allow_html=True)

            # ── Barrier model ──
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:.8rem"> <div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">BARRIER MODEL  -  Each EDB item is a Detector, Logic Solver, or Actuator component of a barrier</div> <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;font-size:.7rem;margin-bottom:.4rem"> <div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:.5rem"><b style="color:#ef4444">Active  -  Automatic Trip</b><br><span style="color:#64748b">SIS function — auto-trip without human action. QS1001, QZ1007. Highest reliability.</span></div> <div style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.2);border-radius:6px;padding:.5rem"><b style="color:#3b82f6">Active  -  Instrumented</b><br><span style="color:#64748b">Monitoring with alarm — operator then acts. AT1702/1703 H2 detectors, ME1101. PFD ~0.1.</span></div> <div style="background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);border-radius:6px;padding:.5rem"><b style="color:#a78bfa">Passive</b><br><span style="color:#64748b">No activation needed — always provides protection. Filters, check valves, strainers. PFD ~0.01.</span></div> </div></div>""", unsafe_allow_html=True)

            # ── Flashcards ──
            st.markdown('<div class="sl-sec">Equipment Cards  —  Detailed Design Basis</div>', unsafe_allow_html=True)
            hf2 = st.selectbox("Filter by sub-process", ["All","Electrolysis","Gas-Liquid Treater","Hydrogen Purification Unit","Drainage System","CW Circulation Unit","Control Cabinet (PLC/Sensors)","H2 Bullet Storage"], key="h2_edb_f")
            show_h2e = H2_EDB_EXCEL if hf2=="All" else [x for x in H2_EDB_EXCEL if hf2.lower() in x[1].lower()]

            for item in show_h2e:
                sl, sub, haz, equip, tag, sap, basis, sched, mfr, model, refdoc, loc, rem = item
                is_consq = "Consequence" in basis
                bc = "#f97316" if is_consq else "#a78bfa"
                st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:4px solid {bc};border-radius:10px;padding:1rem 1.2rem;margin-bottom:8px">
<div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:.6rem">
  <div>
    <span style="color:#475569;font-size:.6rem;font-weight:700;letter-spacing:1px">#{sl} &nbsp;·&nbsp; {sub}</span><br>
    <span style="font-size:.92rem;font-weight:800;color:#e2e8f0">{equip}</span>
  </div>
  <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:flex-start">
    <span style="background:{bc}15;color:{bc};font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px;white-space:nowrap">{basis}</span>
    {f'<span style="background:rgba(239,68,68,.15);color:#ef4444;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">PSCE CRITICAL</span>' if is_consq else ""}
  </div>
</div>
<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-bottom:.6rem">
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px">TAG NO.</div><div style="font-size:.72rem;color:#f97316;font-family:monospace;margin-top:2px">{tag}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px">SAP ID</div><div style="font-size:.72rem;color:#3b82f6;font-family:monospace;margin-top:2px">{sap}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px">MANUFACTURER</div><div style="font-size:.72rem;color:#94a3b8;margin-top:2px">{mfr}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px">MODEL / TYPE</div><div style="font-size:.72rem;color:#94a3b8;margin-top:2px">{model}</div></div>
</div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:.5rem">
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px">HAZARDOUS SUBSTANCE</div><div style="font-size:.7rem;color:#fca5a5;margin-top:2px">{haz}</div></div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem"><div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px">MAINT. / CALIB. SCHEDULE</div><div style="font-size:.7rem;color:#22c55e;margin-top:2px">{sched}</div></div>
</div>
<div style="font-size:.74rem;color:#64748b;line-height:1.6;border-top:1px solid #1e3a5f;padding-top:.5rem">{rem}</div>
</div>""", unsafe_allow_html=True)

            render_global_incidents(["H2","O2","N2"])
            render_qa_bot("h2_edb")
        with h2tabs[7]:  # Parameters
            st.markdown('<p style="font-size:.75rem;color:#64748b">H2 Plant  -  All 24 Process Parameters with Sub-Process Mapping</p>', unsafe_allow_html=True)
            render_glossary()
            render_pdb(H2_PDB_PARAMS, dept_key="h2_params")

            render_qa_bot("h2_param")

    else:
        # ── ETL-1 / GENERIC PLANT  -  TABS ONLY (sidebar/nav already rendered above) ──

        TABS = ["Overview", "PSC", "Hazard of Material",
                "Chem. Interaction", "PDB", "PSCE", "EDB", "Parameters"]
        tabs = st.tabs(TABS)

        # ── OVERVIEW ──────────────────────────────────────────────────
        with tabs[0]:
            # Get plant profile if available
            profile = PLANT_PROFILES.get(plant, None)
            n_procs = profile["processes"] if profile else 6
            n_chems = profile["chemicals"] if profile else 6
            n_params = profile["params"] if profile else 13

            st.markdown(f"""
            <div class="sl-metrics" style="grid-template-columns:repeat(5,1fr)">
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
                    (98,"CRITICAL  -  Cr-VI in air (Chemical Treatment) | Risk 98/100 | Carcinogenic exposure  -  shutdown required"),
                    (92,"CRITICAL  -  Strip Exit Temperature (Reflow) | Risk 92/100 | Strip burning / tin melt failure"),
                    (90,"CRITICAL  -  Sn2+ Concentration (Tin Plating) | Risk 90/100 | Improper / over coating risk"),
                ]
            if alerts:
                st.markdown('<div class="sl-sec">Active Risk Alerts</div>', unsafe_allow_html=True)
                for score, text in alerts:
                    st.markdown(f'<div class="sl-alert"><div class="sl-alert-text">{text}</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="sl-sec">Process Overview</div>', unsafe_allow_html=True)
            procs = profile["proc_cards"] if profile else [
                ("Coil Feeding", "Hydraulic oil, DM water, compressed air for welder", "lho", ["LHO"]),
                ("Cleaning & Rinsing", "NaOH (80-90 C), H2SO4 pickling (8-10 g/L), electrolytic cleaning 2.5-3.5 kA", "hho", ["HHO", "PSM Required"]),
                ("Tin Plating", "SnSO4 + PSA + ENSA plating bath, sulphuric acid base, flow brightening at 232 C", "hho", ["HHO", "PSM Required"]),
                ("Reflow Furnace", "H2 gas (LEL 4% UEL 77%), Propane burners, strip temperature 232-270 C", "hho", ["HHO", "PSM Required"]),
                ("Chemical Treatment", "Cr-VI chromate passivation  -  CARCINOGEN, TLV-TWA 0.05 mg/m3", "hho", ["HHO", "PSM Required"]),
                ("Electrostatic Oiling", "DOS oil spray (flash point 190 C), electrostatic oiling, tension recoiling", "lho", ["LHO"]),
            ]
            ETL1_PROC_CHEMS = {
                "Coil Feeding": [],
                "Cleaning & Rinsing": ["A1  -  Sulphuric Acid (H2SO4)"],
                "Tin Plating": ["A1  -  Sulphuric Acid (H2SO4)","A2  -  Phenol Sulfonic Acid (PSA)","A4  -  ENSA (Ethoxylated Naphthol Sulphonic Acid)"],
                "Reflow Furnace": ["H1  -  Hydrogen (H2)","H2  -  Oxygen (O2)","H3  -  Nitrogen (N2)"],
                "Chemical Treatment": ["A5  -  Sodium Dichromate (Na2Cr2O7)","A6  -  Chromic Acid (CrO3/Cr-VI)"],
                "Electrostatic Oiling": ["A3  -  Dioctyl Sebacate (DOS)"],
            }
            EDB_MATCH_TERMS = {"Reflow Furnace":["Furnace"], "Chemical Treatment":["Chemical Treatment","Chem"], "Coil Feeding":["Coil"], "Cleaning & Rinsing":["Cleaning","Pickling","Alkali"], "Tin Plating":["Plating","Tin"], "Electrostatic Oiling":["Oiling","Oiler"]}

            for i, (name, desc, cls, tags) in enumerate(procs):
                t_html = "".join(
                    f'<span class="sl-tag sl-tag-{"hho" if t=="HHO" else "psm" if "PSM" in t else "lho"}">{t}</span>'
                    for t in tags
                )
                is_sel = st.session_state.get("ov_sel_process") == name
                st.markdown(f'<div class="sl-proc {cls}"><div class="sl-proc-title">{name}</div><div class="sl-proc-desc">{desc}</div>{t_html}</div>', unsafe_allow_html=True)
                # ── Process detail drill-down (chemicals, PDB, PSCE, EDB) — always shown ──
                if True:
                    sel_proc = name
                    if is_etl1:
                        rel_pdb = [p for p in ETL1_PDB_PARAMS if p.get("sub_process") == sel_proc]
                        rel_psce = [p for p in ETL1_PSCE if p.get("sub_process") == sel_proc]
                        terms = EDB_MATCH_TERMS.get(sel_proc, [sel_proc.split()[0]])
                        rel_edb = [p for p in ETL1_EDB if any(t in p.get("sub_process","") for t in terms)]
                        rel_chems = ETL1_PROC_CHEMS.get(sel_proc, [])
                    elif profile:
                        rel_pdb = [p for p in profile.get("pdb_params", []) if _proc_match(p.get("sub_process",""), sel_proc)]
                        rel_psce = [p for p in profile.get("psce_items", []) if _proc_match(p.get("sub_process",""), sel_proc)]
                        rel_edb = [p for p in profile.get("edb_items", []) if _proc_match(p.get("sub_process",""), sel_proc)]
                        rel_chems = []
                    else:
                        rel_pdb, rel_psce, rel_edb, rel_chems = [], [], [], []

                    st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-top:3px solid #f97316;border-radius:10px;padding:1.2rem 1.4rem;margin:.4rem 0 1rem">
<div style="font-size:.95rem;font-weight:700;color:#f97316;margin-bottom:.6rem">{sel_proc} - Full Details</div>""", unsafe_allow_html=True)

                    # Chemicals used (ETL-1 only - has a per-process chemical map)
                    if is_etl1:
                        if rel_chems:
                            st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#a78bfa;margin:.6rem 0 .4rem">CHEMICALS USED IN THIS PROCESS</div>', unsafe_allow_html=True)
                            for chem_key in rel_chems:
                                cd = ETL1_CHEM_QUICKREF.get(chem_key)
                                if cd:
                                    st.markdown(f'<div style="background:#080d18;border:1px solid #1e3a5f;border-left:3px solid {cd.get("color","#a78bfa")};border-radius:8px;padding:.7rem 1rem;margin-bottom:6px"><div style="font-weight:700;color:#e2e8f0;margin-bottom:3px">{chem_key}</div><div style="font-size:.74rem;color:#94a3b8">{cd.get("class","")}</div><div style="font-size:.7rem;color:#fca5a5;margin-top:3px">TLV-TWA: {cd.get("tlv_twa","N/A")} | NFPA: {cd.get("nfpa","N/A")}</div></div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div style="font-size:.74rem;color:#64748b">No hazardous chemicals directly used in this process.</div>', unsafe_allow_html=True)

                    # PDB params for this process
                    if rel_pdb:
                        st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#22c55e;margin:.6rem 0 .4rem">PDB - PROCESS DESIGN BASIS PARAMETERS</div>', unsafe_allow_html=True)
                        pdb_tbl_ov = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.73rem"><thead><tr style="background:#080d18">'
                        for h in ["#","Parameter","UoM","SOC Min","SOC Max","SOL Min","SOL Max","PSM Critical"]:
                            pdb_tbl_ov += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
                        pdb_tbl_ov += '</tr></thead><tbody>'
                        for pm in rel_pdb:
                            pdb_tbl_ov += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace">{pm["sl"]}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:600">{pm["param"]}</td><td style="padding:6px 9px;color:#64748b;font-family:monospace">{pm["uom"]}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{pm["soc_min"]}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{pm["soc_max"]}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace">{pm["sol_min"]}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{pm["sol_max"]}</td><td style="padding:6px 9px;text-align:center"><span style="background:rgba(239,68,68,.2);color:#f87171;font-size:.6rem;font-weight:700;padding:2px 7px;border-radius:10px">{pm.get("psm_critical","")}</span></td></tr>'
                        pdb_tbl_ov += '</tbody></table></div>'
                        st.markdown(pdb_tbl_ov, unsafe_allow_html=True)

                    # PSCE for this process
                    if rel_psce:
                        st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#f97316;margin:.6rem 0 .4rem">PSCE - PROCESS SAFETY CRITICAL EQUIPMENT</div>', unsafe_allow_html=True)
                        for item in rel_psce:
                            st.markdown(f'<div style="background:#080d18;border:1px solid #1e3a5f;border-left:3px solid #f97316;border-radius:7px;padding:.6rem .9rem;margin-bottom:5px"><div style="font-weight:600;color:#e2e8f0;font-size:.8rem;margin-bottom:.2rem">#{item["sl"]} {item["equipment"]}</div><div style="font-size:.72rem;color:#94a3b8;margin-bottom:.2rem">{item["justification"]}</div><div style="font-size:.7rem;color:#fca5a5"><b style="color:#ef4444">Consequence:</b> {item["consequence_of_failure"]}</div></div>', unsafe_allow_html=True)

                    # EDB for this process
                    if rel_edb:
                        st.markdown('<div style="font-size:.65rem;font-weight:700;letter-spacing:2px;color:#3b82f6;margin:.6rem 0 .4rem">EDB - EQUIPMENT DESIGN BASIS</div>', unsafe_allow_html=True)
                        for item in rel_edb:
                            st.markdown(f'<div style="background:#080d18;border:1px solid #1e3a5f;border-left:3px solid #3b82f6;border-radius:7px;padding:.6rem .9rem;margin-bottom:5px"><div style="font-weight:600;color:#e2e8f0;font-size:.8rem;margin-bottom:.2rem">{item["equipment"]} <span style="color:#475569;font-family:monospace;font-size:.7rem">({item["tag_no"]})</span></div><div style="font-size:.72rem;color:#94a3b8">Mfr: {item["manufacturer"]} | Model: {item["model"]}</div><div style="font-size:.71rem;color:#94a3b8;margin-top:3px">{item["design_basis"]}</div></div>', unsafe_allow_html=True)

                    if not (rel_pdb or rel_psce or rel_edb or (is_etl1 and rel_chems)):
                        st.markdown('<div style="font-size:.74rem;color:#64748b">Detailed PDB / PSCE / EDB drill-down for this process is being finalized.</div>', unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)


            render_global_incidents(["H2SO4","Cr-VI","Phenol","DOS","ENSA"])
            render_qa_bot("g_ov")

        # ── PSC ──────────────────────────────────────────────────────
        with tabs[1]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/PSC/001 Rev.04 Eff.Dt.:18.08.2023  -  ETL-1, Tata Steel Tinplate (TCIL), Golmuri</p>', unsafe_allow_html=True)
            render_glossary()

            # ── EXACT EXCEL PSC TABLE (Form No. PSM/PSI/PSC/001) ──
            st.markdown('''<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.2rem">PROCESS SAFETY CLASSIFICATION  —  ETL-1 ELECTROLYTIC TINNING LINE</div>
<div style="font-size:.62rem;color:#475569;margin-bottom:.8rem">Form No.: PSM/PSI/PSC/001 &nbsp;·&nbsp; Rev. No.: 04 &nbsp;·&nbsp; Eff. Dt.: 18.08.2023 &nbsp;·&nbsp; Dept: ETL 1 &nbsp;·&nbsp; Process Name: Electrolytic Tin Plating Line</div>
</div>''', unsafe_allow_html=True)

            # Exact data from Excel PSC sheet (rows 6-11, cols as per header rows 4-5)
            # Columns: Process | HazSub | Toxic | Explosive | Flammable | Corrosive | Thermally Instable | Pressure/Temp | Prop Damage >50L | Potential Fatality | Env Impact | HHO | LHO
            PSC_EXCEL_ROWS = [
                ("Coil Feeding in Entry Section",          "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "Y"),
                ("Cleaning and Rinsing of Strip",          "Y", "Y", "N", "N", "Y", "Y", "Y", "Y", "N", "N", "Y", "N"),
                ("Electrolytic Tin Plating of Strip",      "Y", "Y", "N", "N", "Y", "N", "N", "Y", "N", "N", "Y", "N"),
                ("Heating of Strip in Electrical Furnace at Reflow Section", "Y", "Y", "N", "N", "Y", "N", "N", "Y", "N", "N", "Y", "N"),
                ("Chemical Treatment and Rinsing of Strip","Y", "N", "N", "N", "N", "Y", "Y", "Y", "N", "N", "Y", "N"),
                ("Electrostatic Oiling on Strip",          "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "N", "Y"),
            ]
            PSC_EXCEL_HDR = [
                "Process",
                "Hazardous Substance / Energy in Process",
                "Toxic",
                "Explosive",
                "Flammable / Flammable Dust",
                "Corrosive",
                "Thermally Instable",
                "Pressure / Temperature",
                "Significant Property Damage (> 50 Lakhs)",
                "Potential Fatality / Multiple LTIs",
                "Significant Environmental Impact",
                "HHO",
                "LHO",
            ]
            # Build exact table
            psc_etbl = '<div style="overflow-x:auto;margin-bottom:1rem"><table style="border-collapse:collapse;width:100%;font-size:.73rem;border:1px solid #1e3a5f">'
            psc_etbl += '<thead>'
            # Header row 1 - column groups
            psc_etbl += '<tr style="background:#06111f">'
            psc_etbl += '<th rowspan="2" style="padding:8px 10px;text-align:left;color:#94a3b8;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;min-width:200px">SECTION / PROCESS<br><span style=\"color:#475569;font-weight:400\">Area: ETL 1</span></th>'
            psc_etbl += '<th rowspan="2" style="padding:8px 8px;text-align:center;color:#60a5fa;font-size:.58rem;font-weight:700;border:1px solid #1e3a5f;min-width:80px">HAZARDOUS SUBSTANCE / ENERGY</th>'
            psc_etbl += '<th colspan="5" style="padding:8px;text-align:center;color:#f97316;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;background:rgba(249,115,22,.08)">INVOLVING HAZARDOUS SUBSTANCE HAVING / CAUSING</th>'
            psc_etbl += '<th colspan="3" style="padding:8px;text-align:center;color:#ef4444;font-size:.6rem;font-weight:700;letter-spacing:1px;border:1px solid #1e3a5f;background:rgba(239,68,68,.08)">CONSEQUENCES</th>'
            psc_etbl += '<th rowspan="2" style="padding:8px 6px;text-align:center;color:#f97316;font-size:.62rem;font-weight:800;border:1px solid #1e3a5f;background:rgba(249,115,22,.12);min-width:45px">HHO</th>'
            psc_etbl += '<th rowspan="2" style="padding:8px 6px;text-align:center;color:#6366f1;font-size:.62rem;font-weight:800;border:1px solid #1e3a5f;background:rgba(99,102,241,.1);min-width:45px">LHO</th>'
            psc_etbl += '</tr>'
            # Header row 2 - sub-columns
            psc_etbl += '<tr style="background:#06111f">'
            for h in ["Toxic","Explosive","Flammable / Flammable Dust","Corrosive","Thermally Instable"]:
                psc_etbl += f'<th style="padding:7px 6px;text-align:center;color:#94a3b8;font-size:.57rem;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap;max-width:70px">{h}</th>'
            for h in ["Significant Property Damage (> 50 Lakhs)","Potential for Single / Multiple Fatality / Multiple LTIs","Significant Environmental Impact (recovery > 2 months)"]:
                psc_etbl += f'<th style="padding:7px 6px;text-align:center;color:#fca5a5;font-size:.55rem;font-weight:700;border:1px solid #1e3a5f;max-width:80px">{h}</th>'
            psc_etbl += '</tr></thead><tbody>'

            # Data rows - exact from Excel
            EXCEL_DATA = [
                # name, hazSub, toxic, explos, flamm, corr, thermal, press, propDmg, fatality, env, HHO, LHO
                ("Coil Feeding in Entry Section",                          "N","N","N","N","N","N","N","N","N","N","Y"),
                ("Cleaning and Rinsing of Strip",                          "Y","Y","N","N","Y","Y","Y","Y","N","N","Y","N"),
                ("Electrolytic Tin Plating of Strip",                      "Y","Y","N","N","Y","N","N","Y","N","N","Y","N"),
                ("Heating of Strip in Electrical Furnace at Reflow Section","Y","Y","N","N","Y","N","N","Y","N","N","Y","N"),
                ("Chemical Treatment and Rinsing of Strip",                "Y","N","N","N","N","Y","Y","Y","N","N","Y","N"),
                ("Electrostatic Oiling on Strip",                          "N","N","N","N","N","N","N","N","N","N","N","Y"),
            ]
            for di, drow in enumerate(EXCEL_DATA):
                name = drow[0]
                vals = drow[1:]  # hazSub, toxic, explos, flamm, corr, thermal, [press not in Excel cols 5-9], propDmg, fatality, env, HHO, LHO
                is_hho = vals[-2] == "Y" if len(vals) >= 2 else False
                row_bg = "rgba(249,115,22,.04)" if is_hho else "rgba(99,102,241,.03)"
                alt_bg = "rgba(249,115,22,.02)" if is_hho else "#0a1020"
                psc_etbl += f'<tr style="border-bottom:1px solid #1e3a5f;background:{row_bg if di%2==0 else alt_bg}">'
                psc_etbl += f'<td style="padding:8px 10px;color:#e2e8f0;font-weight:700;border:1px solid #1e3a5f">{name}</td>'
                # hazardous substance col
                haz = vals[0]
                haz_c = "#22c55e" if haz=="Y" else "#475569"
                psc_etbl += f'<td style="padding:8px;text-align:center;font-weight:700;font-family:monospace;color:{haz_c};border:1px solid #1e3a5f">{haz}</td>'
                # hazard type cols (toxic..thermally instable) - 5 cols
                for v in vals[1:6]:
                    if v == "Y":
                        psc_etbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.2);color:#f97316;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                    else:
                        psc_etbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                # consequence cols (propDmg, fatality, env) - 3 cols
                for v in vals[6:9]:
                    if v == "Y":
                        psc_etbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(239,68,68,.2);color:#ef4444;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                    else:
                        psc_etbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-weight:700;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                # HHO / LHO cols
                hho_val = vals[-2] if len(vals) >= 2 else "N"
                lho_val = vals[-1] if len(vals) >= 1 else "N"
                if hho_val == "Y":
                    psc_etbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(249,115,22,.25);color:#f97316;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                else:
                    psc_etbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                if lho_val == "Y":
                    psc_etbl += '<td style="padding:8px;text-align:center;border:1px solid #1e3a5f"><span style="background:rgba(99,102,241,.25);color:#818cf8;font-weight:900;font-size:.78rem;padding:3px 10px;border-radius:4px">Y</span></td>'
                else:
                    psc_etbl += '<td style="padding:8px;text-align:center;color:#2d4a6b;font-family:monospace;font-size:.8rem;border:1px solid #1e3a5f">N</td>'
                psc_etbl += '</tr>'
            psc_etbl += '</tbody></table></div>'
            st.markdown(psc_etbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.62rem;color:#475569;margin-bottom:1.2rem;font-family:monospace">Y = Yes / Applicable &nbsp;·&nbsp; N = No / Not Applicable &nbsp;·&nbsp; HHO = High Hazard Operation (Full PSRM required) &nbsp;·&nbsp; LHO = Low Hazard Operation (PSI only) &nbsp;·&nbsp; Dept: ETL 1 &nbsp;·&nbsp; Form: PSM/PSI/PSC/001 Rev.04</div>', unsafe_allow_html=True)

            # Framework banner
            st.markdown("""<div style="background:rgba(249,115,22,.08);border:1px solid rgba(249,115,22,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem"> <div style="font-size:.82rem;font-weight:700;color:#f97316;margin-bottom:.5rem">PSRM CLASSIFICATION FRAMEWORK</div> <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;font-size:.78rem;color:#94a3b8;line-height:1.8"> <div><b style="color:#f97316">HHO  -  Highly Hazardous Operation</b><br> Process with hazardous substance/energy that CAN result in:<br> &#8226; Property damage &gt; Rs.50 lakhs, OR<br> &#8226; Potential for fatality / multiple LTIs, OR<br> &#8226; Significant environmental impact<br> <b style="color:#f97316">Requires: Full PSRM</b>  -  PSI + PHA + HAZOP + Bow Tie + LOPA + Barrier Audits + SOPs + Emergency Plan</div> <div><b style="color:#6366f1">LHO  -  Lower Hazardous Operation</b><br> Process with hazardous substance/energy present BUT consequences do NOT meet any HHO threshold under normal or credible abnormal operation.<br><br> <b style="color:#6366f1">Requires: Baseline PSRM</b>  -  PSI documentation only</div> </div></div>""", unsafe_allow_html=True)

            # Stats
            st.markdown("""<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1rem"> <div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:10px;padding:.9rem;text-align:center"> <div style="font-size:1.8rem;font-weight:900;color:#f97316;font-family:monospace">4</div> <div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">HHO PROCESSES</div></div> <div style="background:#0d1f35;border:1px solid rgba(99,102,241,.3);border-top:3px solid #6366f1;border-radius:10px;padding:.9rem;text-align:center"> <div style="font-size:1.8rem;font-weight:900;color:#6366f1;font-family:monospace">2</div> <div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">LHO PROCESSES</div></div> <div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:10px;padding:.9rem;text-align:center"> <div style="font-size:1.8rem;font-weight:900;color:#ef4444;font-family:monospace">6</div> <div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">CHEMICALS ONSITE</div></div> <div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:10px;padding:.9rem;text-align:center"> <div style="font-size:1.8rem;font-weight:900;color:#22c55e;font-family:monospace">77</div> <div style="font-size:.6rem;font-weight:700;letter-spacing:1.5px;color:#475569">PSCE ITEMS</div></div> </div>""", unsafe_allow_html=True)

            # Process selector
            # All processes shown directly

            PSC_DATA = {
                "Coil Feeding": {
                    "cls":"LHO","color":"#6366f1",
                    "desc":"Entry section: payoff reel loads cold-rolled black plate. Strip welded for line continuity. Entry looper accumulates strip for uninterrupted operation. Key equipment: hydraulic power pack (55-70 bar), welder, bridle rolls, entry looper.",
                    "hazardous":["Hydraulic oil (flash point ~150deg C)","DM water at pressure (4.5-5.5 kg/cm2)","Compressed air (4.5-5.5 kg/cm2)","Mechanical pinch points at bridle rolls"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"N","Corrosive":"Y","Thermal":"N","Pressure":"Y"},
                    "consequences":{"Property >50L":"N","Fatality":"N","Env. Impact":"N"},
                    "reasoning":"Hydraulic oil leak at 55-70 bar is the primary credible hazard. However, hydraulic oil flash point (~150deg C) means ignition requires sustained heat source  -  no credible ignition scenario in normal operation. Compressed air line failure causes mechanical noise/movement but no explosive energy release sufficient for fatality. DM water at 4.5-5.5 kg/cm2 is low-pressure utility. No toxic release, no explosion risk. Consequence analysis: maximum credible event = hydraulic oil spill causing slip hazard / minor fire, well below Rs.50 lakh threshold. NO HHO CRITERIA MET.",
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
                    "desc":"Pre-primary, primary, secondary electrolytic alkali (NaOH) cleaning at 80-90deg C removes rolling oils. Followed by H2SO4 pickling (8-10 g/L) for iron oxide removal. DM/condensate water rinsing. Electrolytic current: 2.5-3.5 kA. Three chemical baths in sequence.",
                    "hazardous":["H2SO4 (Sulphuric Acid)  -  corrosive, generates H2 with metals","NaOH at 80-90deg C  -  severe alkali burns","H2 gas from electrolytic cleaning (LEL 4%)","Acid mist (TLV-TWA 1 mg/m3)","High DC current 2.5-3.5 kA"],
                    "hazard_matrix":{"Toxic":"Y","Explosive":"Y","Flammable":"N","Corrosive":"Y","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"H2SO4 at 8-10 g/L generates H2 gas when in contact with steel (Fe + H2SO4 -&gt; FeSO4 + H2↑). H2 LEL is 4%  -  accumulation in poorly ventilated cell area + electrical ignition source = explosive risk. NaOH at 80-90deg C: boiling alkali splash causes full-thickness chemical burns. Electrolytic current 2.5-3.5 kA creates H2 at cathode. Credible failure: LEV failure + H2 accumulation + current arc = H2 explosion -&gt; structural damage >Rs.50L, fatality risk. Also: H2SO4 spill to drain -&gt; WTP overload, groundwater pH impact = environmental consequence. ALL THREE HHO CRITERIA CAN BE MET.",
                    "parameters":[
                        ("NaOH Temperature","80-90deg C","80-90deg C","<80deg C: poor degreasing, oil on strip -&gt; plating pinholes","&gt;=90deg C: alkali boiling, violent steam, burn risk  -  HHO EVENT"),
                        ("NaOH Concentration","25-30 g/L","25-30 g/L","<25 g/L: insufficient cleaning, residual oil","&gt;=30 g/L: excess drag-out, waste treatment overload"),
                        ("Cleaning Current","2.5-3.5 kA","2.5-3.5 kA","<2.5 kA: inadequate electrolytic cleaning","&gt;=3.5 kA: H2 over-evolution, arc risk, cell damage"),
                        ("H2SO4 Concentration","8-10 g/L","8-10 g/L","<8 g/L: incomplete pickling, oxide layer on strip","&gt;=10 g/L: over-pickling, H2 gas spike, equipment corrosion"),
                    ],
                    "barriers":["Forced LEV ventilation above all cleaning cells","Alkali temperature transmitter + auto-alarm at 90deg C","H2SO4 concentration analyser with SOC/SOL alarm","Electrolytic current protection relay (trip at 3.5 kA)","Acid-resistant PPE mandatory zone","Emergency deluge shower within 10m"],
                    "hazop":[
                        ("NaOH Temp HIGH","Temperature exceeds 90deg C","Cooling water valve failure / steam trap blockage","Alkali boils  -  steam explosion, severe burns to operators","Temp transmitter alarm, auto-coolant valve, operator shutdown"),
                        ("H2SO4 Conc HIGH","Concentration exceeds 10 g/L","Overdose during makeup / analyser failure","Over-pickling, H2 spike, equipment corrosion, acid mist","Concentration analyser alarm, manual titration verification"),
                        ("Cleaning Current HIGH","Current >3.5 kA","Rectifier malfunction / control system failure","Excessive H2 evolution, arc, cell damage","Current protection relay auto-trip, visual ammeter check"),
                        ("LEV FAILURE","Ventilation stops","Fan failure / power cut","H2 accumulates in cell area -&gt; explosion risk","LEV flow switch alarm, backup fan interlock"),
                    ],
                    "bowtie":{
                        "top_event":"H2 accumulation and ignition in cleaning section",
                        "causes":["LEV ventilation failure","Electrolytic current >3.5 kA (H2 over-evolution)","H2SO4 concentration >10 g/L (increased H2 generation)","Electrical arc from damaged cell connections"],
                        "consequences":["Explosion  -  structural damage, line shutdown 2-4 weeks","Fatality/serious injury to cleaning section operators","Fire spread to adjacent process bays","Regulatory shutdown, PESO investigation"],
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
                        ("Sn2+ Concentration","26-32 g/L","24-34 g/L","<24 g/L: under-plating, dull band  -  PRODUCT REJECTION","&gt;=34 g/L: over-coating, excess tin loss, cost impact"),
                        ("Free Acid Concentration","13-16 g/L","11-18 g/L","<11 g/L: low conductivity, uneven plating","&gt;=18 g/L: increased acid mist, corrosivity"),
                        ("Sn2+ : Free Acid Ratio","1.95-2.05","1.90-2.10","<1.90: bath imbalance, rough deposit, sludge","&gt;=2.10: non-uniform deposition, product failure"),
                        ("ENSA Concentration","3-6 g/L","2-7 g/L","<2 g/L: dull appearance, rough tin surface","&gt;=7 g/L: bath contamination, breakdown products"),
                    ],
                    "barriers":["Daily bath analysis  -  Sn2+, free acid, ENSA verified","Current density interlock per plating cell","Acid mist LEV system above all 8 plating cells","Plating tank level transmitter (overflow alarm)","Sn-bearing wastewater to dedicated WTP stream"],
                    "hazop":[
                        ("Sn2+ LOW","<24 g/L","Anode dissolution rate low / feed failure","Under-plating  -  product downgrade, rejection","Bath analyser alarm, mandatory hold before dispatch"),
                        ("Free Acid HIGH","&gt;=18 g/L","Overdose during makeup","Acid mist surge, operator exposure","Acid mist monitor, LEV performance check"),
                        ("Current HIGH","Above set point","Rectifier malfunction","H2 evolution at cathode, arc risk","Current relay auto-trip, cell inspection"),
                        ("Bath Overflow","Level >SOL","Pump seal failure / makedown error","Sn2+ spill to floor/drain  -  environmental","Level transmitter alarm + auto pump trip"),
                    ],
                    "bowtie":{
                        "top_event":"Plating bath overflow / H2 ignition at plating cells",
                        "causes":["Bath level control failure (pump seal failure)","Over-current -&gt; H2 evolution at cathode","Sn2+ crash -&gt; emergency bath makeup spillage","ENSA decomposition  -  bath foam-over"],
                        "consequences":["Sn-bearing wastewater to drain  -  WTP failure, CPCB reportable","H2 ignition -&gt; fire in plating cell area","Product rejection  -  food safety regulatory action","Line shutdown  -  production loss >Rs.50L"],
                        "preventions":["Bath level transmitter + auto pump trip at SOL","Current protection relay on all 8 plating rectifiers","Foam detector in plating bath","Daily mandatory bath analysis verification"],
                        "mitigations":["Dedicated Sn-bearing wastewater collection pit","Fire suppression in plating bay","Product hold and 100% re-inspection protocol","CPCB emergency notification procedure"],
                    },
                },
                "Reflow Furnace": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"Resistance/induction heating melts tin at 232deg C (tin melting point) for mirror-bright finish and Fe-Sn alloy layer. H2/N2 atmosphere prevents oxidation. Strip then quenched in water (50-65deg C). CRITICAL: N2 purge mandatory before H2. H2 purge before air on shutdown. HIGHEST RISK PROCESS on ETL-1.",
                    "hazardous":["H2 gas  -  LEL 4%, UEL 77% (extremely wide explosive range)","Propane burners  -  LEL 2.1%, UEL 9.5%","Strip at 232-270deg C (above tin melting point)","H2 ignition energy: 0.017 mJ (tiny  -  almost invisible spark sufficient)","N2 asphyxiation risk if purge sequence fails"],
                    "hazard_matrix":{"Toxic":"Y","Explosive":"Y","Flammable":"Y","Corrosive":"Y","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"Y","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"H2 vapour cloud explosion is the top risk. H2 has the widest flammability range of any common industrial gas (4-77%) and the lowest ignition energy (0.017 mJ  -  a tiny static discharge). A seal failure while H2 is flowing, without proper N2 purge first, creates explosive atmosphere in seconds. Propane burners add secondary fire risk. Strip at >270deg C causes conductor roll damage, strip burning, secondary fire. A single H2 explosion in the furnace bay would cause: structural collapse, multiple fatalities, damage well exceeding Rs.50L, potential H2 line fire. This is why PSAL 2.14, UV 1.21, and Pyrometer ETL-1 are all PSCE items with mandatory calibration. ALL THREE HHO CRITERIA EXCEEDED BY LARGE MARGIN.",
                    "parameters":[
                        ("Strip Temperature","232-270deg C","232-270deg C","<232deg C: tin doesn't melt  -  dull coating, product reject","&gt;=270deg C: strip burning, conductor roll damage  -  CRITICAL SHUTDOWN"),
                        ("Quench Temperature","50-65deg C","50-65deg C","<50deg C: thermal shock, strip shape defects","&gt;=65deg C: incomplete solidification, alloy overgrowth"),
                        ("Reflow Current","1000-10000 A","1000-10000 A","<1000 A: insufficient melting energy","&gt;=10000 A: conductor roll arcing, fire risk  -  CRITICAL"),
                        ("H2 Pressure","0.5-2.0 bar","0.5-2.5 bar","<0.5 bar: H2 supply loss  -  must purge with N2 BEFORE air entry","&gt;=2.5 bar: line overpressure, seal failure risk"),
                    ],
                    "barriers":["PSAL 2.14: H2 pressure switch  -  PLC auto-trip on loss (PSCE #2)","UV 1.21: Propane solenoid auto-close on safety signal (PSCE #3)","Pyrometer ETL-1: auto-trip at 270deg C strip temperature (PSCE #1)","N2 purge interlock  -  H2 cannot be admitted without N2 purge confirmation","H2 LEL detector in furnace zone with evacuation alarm","Mandatory purge procedure (SOP) verified by shift supervisor"],
                    "hazop":[
                        ("H2 Pressure LOW","<0.5 bar","Supply valve failure / pipe leak","H2 loss -&gt; air ingress -&gt; explosive mixture on restart without purge","PSAL 2.14 auto-trip, N2 auto-purge, mandatory restart SOP"),
                        ("Strip Temp HIGH",">270deg C","Pyrometer failure / current surge","Strip burning, conductor roll damage, secondary fire","Pyrometer auto-trip, redundant thermocouple, visual alarm"),
                        ("Purge Sequence SKIPPED","N2 purge bypassed","Operator error / interlock defeat","H2 + air = explosive atmosphere in furnace","Hard interlock  -  H2 valve mechanically blocked until N2 confirmed"),
                        ("Propane Leak","Uncontrolled release","Fitting failure / valve leak","Propane + H2 = compound explosion risk","Gas detector auto-trip, UV 1.21 solenoid closure, evacuation"),
                    ],
                    "bowtie":{
                        "top_event":"H2 vapour cloud ignition and explosion in reflow furnace",
                        "causes":["H2 supply seal failure (PSAL 2.14 fails to trip)","N2 purge sequence bypassed on restart","Propane burner leak adds to explosive atmosphere","Ignition from conductor roll arc or static discharge"],
                        "consequences":["Explosion  -  furnace structure collapses","Multiple fatalities  -  HHO zone","Plant shutdown 3-6 months minimum","PESO/regulatory investigation, potential prosecution"],
                        "preventions":["PSAL 2.14 H2 pressure switch (PSCE #2)  -  auto-trip","UV 1.21 propane solenoid (PSCE #3)  -  auto-close","Hard interlocked N2 purge before H2 admission","H2 LEL continuous monitor with 20% LEL alarm"],
                        "mitigations":["Blast-resistant furnace bay design","Explosion relief panels in roof","Full HHO zone evacuation procedure","Emergency services pre-notified of H2 storage quantities"],
                    },
                },
                "Chemical Treatment": {
                    "cls":"HHO","color":"#ef4444",
                    "desc":"Electrolytic chromate passivation using Cr-VI (CrO3/Na2Cr2O7) bath at 40-45deg C. Thin chromium oxide layer for corrosion protection and lacquer adhesion. MANDATORY: enclosed bath + Local Exhaust Ventilation + continuous air monitoring. CPCB/SPCB declared quantity.",
                    "hazardous":["Chromic Acid Cr-VI  -  IARC Group 1 Carcinogen (TLV-TWA 0.05 mg/m3)","Sodium Dichromate  -  strong oxidiser, carcinogen","Cr-VI mist generation during operation","Hexavalent chromium in wastewater  -  MSIHC Schedule chemical","Skin/eye contact  -  severe burns + sensitisation"],
                    "hazard_matrix":{"Toxic":"Y","Explosive":"N","Flammable":"N","Corrosive":"Y","Thermal":"Y","Pressure":"Y"},
                    "consequences":{"Property >50L":"N","Fatality":"Y","Env. Impact":"Y"},
                    "reasoning":"Cr-VI (hexavalent chromium) is an IARC Group 1 confirmed human carcinogen causing lung cancer, nasal septum perforation, kidney damage. TLV-TWA is only 0.05 mg/m3  -  one of the lowest industrial TLVs. A single bath overflow or LEV failure can expose workers to carcinogenic levels. Long-term exposure even at low levels = cancer fatality (chronic). Cr-VI in wastewater at ppb levels contaminate groundwater for decades  -  significant environmental consequence. Mandatory CPCB declaration under MSIHC Rules 1989. Two HHO criteria clearly met: potential for fatality (carcinogen) + significant environmental impact. Even without explosion risk this is the most toxic HHO on ETL-1.",
                    "parameters":[
                        ("Bath Temperature","40-45deg C","40-45deg C","<40deg C: incomplete passivation, corrosion failure in service","&gt;=45deg C: Cr-VI volatilisation increases  -  TLV breach risk, SHUTDOWN"),
                        ("Treatment Current","300-2000 A","300-3500 A","<300 A: insufficient passivation layer","&gt;=3500 A: Cr-VI reduction to Cr-III, bath balance upset"),
                        ("Cr-VI Air Concentration","<0.05 mg/m3 TLV","<0.1 mg/m3 ceiling","N/A (minimum desirable)","&gt;=0.05 mg/m3: MANDATORY SHUTDOWN  -  MSIHC Rules 1989"),
                        ("Bath Cr-VI Level","Per SDS specification","Per SDS specification","Below spec: inadequate passivation","Above spec: increased mist generation, higher exposure risk"),
                    ],
                    "barriers":["Continuous Cr-VI air monitor  -  alarm at 0.05 mg/m3, SHUTDOWN at 0.08 mg/m3","Enclosed bath design with LEV  -  minimum 0.5 m/s face velocity","Bath temperature transmitter  -  alarm + auto-off at 45deg C","Treatment current interlock (SOC: 300-2000 A)","PPE mandatory: Class C suit + air-supplied respirator","Cr-VI wastewater to dedicated chrome reduction plant","Annual medical surveillance (lung function, urine Cr levels)"],
                    "hazop":[
                        ("Bath Temp HIGH","&gt;=45deg C","Heating element malfunction","Cr-VI volatilisation spike  -  carcinogen exposure above TLV","Air monitor alarm, auto-bath off, evacuation"),
                        ("LEV FAILURE","Ventilation off","Fan failure / power cut","Cr-VI mist accumulates  -  carcinogenic atmosphere","LEV flow switch auto-trip on bath, area evacuation"),
                        ("Bath Overflow","Level >SOL","Tank integrity / makedown error","Cr-VI spill to floor/drain  -  ground contamination","Level alarm, sealed chrome pit, bunded area"),
                        ("Air Monitor FAILS","No reading","Sensor failure / calibration drift","Undetected Cr-VI exposure","Mandatory manual monitoring if analyser fails, SOP for downtime"),
                    ],
                    "bowtie":{
                        "top_event":"Cr-VI release to plant atmosphere above TLV-TWA (0.05 mg/m3)",
                        "causes":["LEV ventilation failure (fan stops)","Bath temperature exceeds 45deg C (Cr-VI volatilisation)","Bath overflow during makedown","Air monitoring failure  -  undetected exposure"],
                        "consequences":["Carcinogen exposure  -  long-term lung cancer risk","MSIHC Rules 1989 violation  -  mandatory CPCB report","Regulatory shutdown + enforcement action","Cr-VI groundwater contamination (decadal persistence)"],
                        "preventions":["LEV flow switch  -  auto-bath trip if airflow drops","Bath temp transmitter  -  auto-off at 45deg C","Enclosed bath design minimises mist generation","Continuous Cr-VI air monitor (quarterly calibration)"],
                        "mitigations":["Air-supplied respirator (immediately if alarm)","Full area evacuation and ventilation","Medical surveillance within 24h of suspected exposure","CPCB emergency notification within 48h"],
                    },
                },
                "Electrostatic Oiling": {
                    "cls":"LHO","color":"#6366f1",
                    "desc":"Electrostatic spray of DOS (Dioctyl Sebacate) oil onto strip surface at controlled rate. Protects strip surface during storage and transport to can manufacturers. Exit looper, tension leveller, side trimmer and recoiler follow. Final product: finished tin plate coil.",
                    "hazardous":["DOS oil (flash point 190deg C)  -  combustible liquid","Electrostatic voltage 10-40 kV  -  shock hazard","Oil mist if excessive application"],
                    "hazard_matrix":{"Toxic":"N","Explosive":"N","Flammable":"N","Corrosive":"N","Thermal":"N","Pressure":"N"},
                    "consequences":{"Property >50L":"N","Fatality":"N","Env. Impact":"N"},
                    "reasoning":"DOS flash point is 190deg C  -  well above ambient process temperature. No ignition source exists at this temperature. Electrostatic 10-40 kV voltage is enclosed and earth-bonded  -  shock hazard requires deliberate bypass of safety systems. Credible failures: over-oiling (quality defect  -  lacquer bond failure), voltage arc to strip (minor marking). Maximum credible accident: small oil fire if DOS contacts sustained heat source, easily handled by local fire extinguisher. Property damage well below Rs.50L threshold. No fatality pathway. No environmental pathway (DOS is biodegradable, low toxicity). BOTH CRITERIA FOR LHO CONFIRMED  -  NO HHO THRESHOLD MET.",
                    "parameters":[
                        ("Primary Air Pressure","0.5-1.0 kg/cm2","0.5-1.0 kg/cm2","<0.5: poor atomisation, uneven oil","&gt;=1.0: oil mist generation, excess consumption"),
                        ("Secondary Air Flow","60-300 mm WC","60-300 mm WC","<60: oil drip marks on strip","&gt;=300: oil carry-over to coiler"),
                        ("Repelling Plate Voltage","-10 to -40 kV","-10 to -50 kV","Above -10 kV: poor distribution","Below -50 kV: arcing to strip surface"),
                    ],
                    "barriers":["Electrostatic voltage interlock","Earth bonding on all metalwork in oiling zone","Fire extinguisher positioned at oiling zone","Oil application weight verified per coil (g/m2 measurement)"],
                    "hazop":None,
                    "bowtie":None,
                },
            }

            for spname in list(PSC_DATA.keys()):
                sel_proc = PSC_DATA[spname]
                spcls = sel_proc["cls"]
                spcolor = sel_proc["color"]
                is_hho = spcls == "HHO"

                st.markdown('<hr style="border:none;border-top:2px solid #1e3a5f;margin:1.5rem 0">', unsafe_allow_html=True)
                st.markdown(f"""<div style="background:{spcolor}10;border:1px solid {spcolor}40;border-left:5px solid {spcolor};border-radius:10px;padding:1rem 1.4rem;margin:.8rem 0"><div style="display:flex;align-items:center;gap:12px;margin-bottom:.5rem"><span style="background:{spcolor}20;color:{spcolor};border:1px solid {spcolor}50;font-size:.78rem;font-weight:700;padding:4px 14px;border-radius:20px">{spcls}</span><span style="font-size:1.1rem;font-weight:800;color:#f1f5f9">{spname}</span></div><div style="font-size:.82rem;color:#94a3b8;line-height:1.7">{sel_proc['desc']}</div></div>""", unsafe_allow_html=True)

                d1, d2 = st.columns(2)
                with d1:
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">HAZARDOUS SUBSTANCES / ENERGIES</div>', unsafe_allow_html=True)
                    hlist = "".join(f'<div style="font-size:.78rem;color:#fca5a5;padding:3px 0;border-bottom:1px solid #1e3a5f">&#8226; {h}</div>' for h in sel_proc["hazardous"])
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
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin-bottom:.4rem">CONSEQUENCE ANALYSIS  -  WHY {}</div>'.format(spcls), unsafe_allow_html=True)
                    cons = sel_proc["consequences"]
                    for criterion, val in cons.items():
                        fc = "#ef4444" if val=="Y" else "#22c55e"
                        fbg = "rgba(239,68,68,.08)" if val=="Y" else "rgba(34,197,94,.06)"
                        ftext = "YES  -  HHO criterion MET" if val=="Y" else "NO  -  Threshold not reached"
                        st.markdown(f'<div style="background:{fbg};border-left:3px solid {fc};border-radius:6px;padding:7px 12px;margin-bottom:5px;display:flex;justify-content:space-between;align-items:center"><span style="font-size:.78rem;color:#94a3b8">{criterion}</span><span style="font-size:.72rem;font-weight:700;color:{fc}">{ftext}</span></div>', unsafe_allow_html=True)

                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#475569;margin:.6rem 0 .3rem">CLASSIFICATION REASONING</div>', unsafe_allow_html=True)
                    reason = sel_proc["reasoning"]
                    st.markdown(f'<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.9rem;font-size:.78rem;color:#94a3b8;line-height:1.75">{reason}</div>', unsafe_allow_html=True)

                # SOC/SOL Parameters with deviation cards
                st.markdown('<div class="sl-sec">Process Parameters  -  SOC / SOL / Deviation Consequences</div>', unsafe_allow_html=True)
                st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem 1rem;margin-bottom:.8rem;display:flex;gap:2rem;font-size:.78rem"> <span><b style="color:#22c55e">SOC</b> <span style="color:#64748b">= Safe Operating Condition  -  normal target range where process runs safely and on-spec</span></span> <span><b style="color:#f97316">SOL</b> <span style="color:#64748b">= Safe Operating Limit  -  breach triggers immediate corrective action or plant trip</span></span> </div>""", unsafe_allow_html=True)

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
                    st.markdown('<div class="sl-sec">HAZOP Study  -  What-If Deviation Analysis</div>', unsafe_allow_html=True)
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

                # End of per-process card
                # End of per-process card

        # ── HOM ──────────────────────────────────────────────────────

            render_qa_bot("g_psc")
        with tabs[2]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/HOM/001 Rev.06 Eff.Dt.:18.08.2023  -  Hazard of Materials | ETL-1 Electrolytic Tinning Line</p>', unsafe_allow_html=True)
            render_glossary()

            # ── PSI HOM SHEET - EXACT EXCEL TABLE (TOP) ──────────────
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">HOM - HAZARD OF MATERIAL (as per PSI HOM Sheet, Form No. PSRM/PSI/HOM/TINPL)</div>', unsafe_allow_html=True)
            hom_hdr = ["Sl.","Material","Classification","Reactivity","TLV","STEL","LD50 / LC50","Flash Point","Boiling Point","LFL / LEL","UFL / UEL","Other Process Hazards","Inventory"]
            hom_tbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.7rem"><thead><tr style="background:#080d18">'
            for h in hom_hdr:
                hom_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
            hom_tbl += '</tr></thead><tbody>'
            for r in ETL1_HOM_EXCEL:
                sl, mat, cls, react, tlv, stel, ld50, flash, bp, lfl, ufl, other, inv = r
                hom_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:600;white-space:nowrap">{mat}</td><td style="padding:6px 9px;color:#94a3b8;white-space:nowrap">{cls}</td><td style="padding:6px 9px;color:#94a3b8;min-width:220px">{react}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{tlv}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;white-space:nowrap">{stel}</td><td style="padding:6px 9px;color:#f97316;min-width:220px">{ld50}</td><td style="padding:6px 9px;color:#64748b;white-space:nowrap">{flash}</td><td style="padding:6px 9px;color:#64748b;white-space:nowrap">{bp}</td><td style="padding:6px 9px;color:#64748b;white-space:nowrap">{lfl}</td><td style="padding:6px 9px;color:#64748b;white-space:nowrap">{ufl}</td><td style="padding:6px 9px;color:#fca5a5;min-width:220px">{other}</td><td style="padding:6px 9px;color:#475569;white-space:nowrap">{inv}</td></tr>'
            hom_tbl += '</tbody></table></div>'
            st.markdown(hom_tbl, unsafe_allow_html=True)
            st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)




            # ── PSI HOM SHEET - EXACT TABLE AT TOP ──────────────
            # ── Quick Reference Comparison Table  -  All ETL-1 Chemicals ──
            st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">QUICK REFERENCE  -  ALL ETL-1 CHEMICALS (Toxicology & Regulatory Data)</div>""", unsafe_allow_html=True)
            etl1_qr_data = [
                # code, name, color, nfpa, tlv_twa, tlv_stel, tlv_ceil, idlh, ld50, lc50, hazard
                # H2SO4: ACGIH 2023 TLV-TWA 1 mg/m3 (thoracic fraction), STEL not established, Ceiling not established
                # OSHA PEL: 1 mg/m3. NIOSH REL: 1 mg/m3 TWA. IDLH: 80 mg/m3
                ("A1","Sulphuric Acid H2SO₄","#f97316","3-0-2(W)",
                 "1 mg/m³ (thoracic fraction, ACGIH 2023)","Not established (ACGIH) | OSHA: 1 mg/m³ PEL","Not established (ACGIH) | NIOSH: 1 mg/m³ TWA",
                 "80 mg/m³ (NIOSH)","2140 mg/kg (rat, oral) ✓","510 mg/m³/2H (rat) ✓","A2 Toxic · A3 Reactive with metals/bases · A4 Corrosive"),
                # PSA: No OEL for PSA itself. Parent phenol (ACGIH): TLV-TWA 0.5 ppm SKIN, no STEL, no ceiling
                # OSHA PEL phenol: 5 ppm. NIOSH REL: 5 ppm TWA, 15.6 ppm STEL
                ("A2","Phenol Sulfonic Acid (PSA)","#eab308","3-1-0",
                 "0.5 ppm (phenol component, ACGIH, SKIN designation)","15.6 ppm (NIOSH STEL for phenol component)","Not established (no ceiling for PSA or phenol, ACGIH/NIOSH)",
                 "250 ppm (NIOSH IDLH for phenol component)","~1500 mg/kg (est. from phenol analogy)","316 mg/m³/4H (phenol, RTECS) ✓","A4 Corrosive · SKIN absorption  -  systemic phenol hazard"),
                # DOS: No OEL set. ACGIH: unclassified. Nuisance aerosol limit applies: ACGIH PNOR 10 mg/m3 (respirable 3 mg/m3)
                # No STEL, no ceiling, no IDLH established
                ("A3","Dioctyl Sebacate (DOS)","#22c55e","1-1-0",
                 "10 mg/m³ (ACGIH PNOR  -  Particles Not Otherwise Regulated, inhalable fraction)","3 mg/m³ (ACGIH PNOR respirable fraction  -  no specific STEL)","Not established (no chemical-specific ceiling)",
                 "Not established (very low toxicity  -  no IDLH set)","5000 mg/kg (rat, oral) ✓ Wikipedia/ChemSpider","Not established (negligible vapour pressure  -  0.000024 Pa)","A1 Combustible (flash 210deg C) · Food contact grade FDA 21 CFR 175.105"),
                # ENSA: No OEL for blend. Acid mist (H2SO4) present in plating bath: ACGIH TLV-TWA 1 mg/m3, STEL 3 mg/m3
                # Alpha-naphthol (ACGIH): no TLV set. NIOSH: no REL
                ("A4","ENSA (Ethoxylated Naphthol Sulphonate)","#22c55e","2-1-1",
                 "1 mg/m³ (H2SO₄ acid mist at bath  -  ACGIH TLV for sulphuric acid mist applies)","3 mg/m³ (H2SO₄ STEL by analogy  -  no ENSA-specific STEL established)","Not established for ENSA blend. Acid mist ceiling: not set by ACGIH.",
                 "Not determined (no NIOSH IDLH for ENSA or α-naphthol)","~1870 mg/kg (α-naphthol, CAS 90-15-3) ✓ Fishersci","Not established for ENSA (low VP). Acid mist LC50 ref: 0.35 mg/L/2H (H2SO₄)","A2 Irritant · Aquatic toxic (α-naphthol fish LC50 ~3 mg/L)"),
                # Na2Cr2O7: ACGIH TLV-TWA 0.01 mg/m3 as Cr(VI), A1 carcinogen. No STEL (ACGIH).
                # OSHA: no separate STEL, Action Level 2.5 µg/m3. No ceiling (OSHA TWA only).
                # NIOSH REL: 0.0002 mg/m3 (0.2 µg/m3). IDLH: 15 mg/m3 as Cr(VI)
                ("A5","Sodium Dichromate Na2Cr2O₇","#ef4444","4-0-1(OX)",
                 "0.01 mg/m³ as Cr(VI) (ACGIH A1 Carcinogen, 2023) | OSHA PEL: 0.005 mg/m³ | NIOSH REL: 0.0002 mg/m³",
                 "Not established (ACGIH  -  A1 carcinogen, TWA is controlling limit) | OSHA Action Level: 0.0025 mg/m³ as Cr(VI)",
                 "Not established as separate ceiling (ACGIH)  -  TLV-TWA is the limit. Any exceedance = corrective action.",
                 "15 mg/m³ as Cr(VI) (NIOSH IDLH) ✓","50 mg/kg (rat, oral, CAS 10588-01-9) ✓ Fishersci/PubChem","0.124 mg/L/4H (rat, inhalation) ✓ Acros MSDS/RTECS HX7750000","IARC Gr.1 CARCINOGEN · ACGIH A1 · NTP Known · A3 Strong Oxidiser · Reproductive Toxin H360"),
                # CrO3: Same TLV as Na2Cr2O7 (both Cr(VI) compounds, ACGIH classifies as Cr(VI) compounds group)
                # ACGIH Ceiling: 0.05 mg/m3 (historical)  -  current TLV-TWA 0.01 mg/m3 supersedes
                # OSHA: Ceiling 0.1 mg/m3 (as CrO3, old 1971 standard)  -  superseded by 2006 Cr(VI) standard
                ("A6","Chromic Acid CrO3","#ef4444","3-0-1(OX)",
                 "0.01 mg/m³ as Cr(VI) (ACGIH A1 Carcinogen, 2023) | OSHA PEL: 0.005 mg/m³ | NIOSH REL: 0.0002 mg/m³",
                 "Not established (ACGIH 2023) | OSHA 2006 Cr(VI) rule: no separate STEL  -  TWA 0.005 mg/m³ is controlling",
                 "0.1 mg/m³ (OSHA 1971 legacy ceiling as CrO3  -  superseded by 2006 Cr(VI) PEL of 0.005 mg/m³ TWA) | ACGIH: no ceiling separate from TLV-TWA",
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

            # A-scale hazard category framework banner
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem"> <div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">HAZARD CATEGORIES (A-SCALE)  -  PSRM Classification Framework</div> <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:6px;font-size:.7rem"> <div style="background:#f97316;background:rgba(249,115,22,.12);border:1px solid rgba(249,115,22,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#f97316">A1</b><br><span style="color:#64748b;font-size:.62rem">Flammable / Explosive</span></div> <div style="background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#a78bfa">A2</b><br><span style="color:#64748b;font-size:.62rem">Toxic (TLV-based)</span></div> <div style="background:rgba(239,68,68,.12);border:1px solid rgba(239,68,68,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#ef4444">A3</b><br><span style="color:#64748b;font-size:.62rem">Reactive / Unstable</span></div> <div style="background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#3b82f6">A4</b><br><span style="color:#64748b;font-size:.62rem">Corrosive</span></div> <div style="background:rgba(96,165,250,.12);border:1px solid rgba(96,165,250,.3);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#60a5fa">A5</b><br><span style="color:#64748b;font-size:.62rem">High Pressure / Temp</span></div> </div> <div style="font-size:.7rem;color:#475569;margin-top:.5rem">A process is HHO if ANY A-category substance is present AND at least ONE of: property damage &gt;Rs.50L, potential fatality, or significant environmental impact is a credible consequence.</div> </div>""", unsafe_allow_html=True)

            # Chemical selector
            CHEM_FULL = {
                "A1  -  Sulphuric Acid (H2SO4)": {
                    "code":"A1","risk":72,"color":"#f97316",
                    "class":"Corrosive liquid, Oxidising agent","hazchem":"HAZCHEM 2R","nfpa":"3-0-2(W)","cas":"7664-93-9",
                    "tlv_twa":"1 mg/m3 (ACGIH 2023  -  thoracic fraction, H2SO4 mist)","tlv_stel":"Not established (ACGIH). NIOSH: same 1 mg/m3 TWA, no STEL.","tlv_ceil":"Not established (ACGIH) | OSHA PEL: 1 mg/m3.","ld50":"2140 mg/kg (rat, oral) ✓","lc50":"510 mg/m3/2h (rat, inhal.) ✓",
                    "flash":"N/A (not flammable)","bp":"337deg C (decomposes)","mp":"10deg C (concentrated)","sg":"1.84 (conc.)","vp":"<0.3 hPa at 20deg C",
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
                "A2  -  Phenol Sulfonic Acid (PSA)": {
                    "code":"A2","risk":55,"color":"#eab308",
                    "class":"Corrosive liquid, mixture ortho/para isomers  -  p-hydroxybenzene sulphonic acid. UN 2430. TSCA listed. GHS: H302, H314, H318.","hazchem":"HAZCHEM 2R","nfpa":"3-1-0","cas":"98-67-9",
                    "tlv_twa":"Not established (ACGIH) for PSA blend. Phenol component (CAS 108-95-2): ACGIH TLV-TWA 0.5 ppm (SKIN designation  -  systemic hazard via absorption). OSHA PEL phenol: 5 ppm TWA. NIOSH REL phenol: 5 ppm (19 mg/m3) TWA, 15.6 ppm STEL.",
                    "tlv_stel":"Not established for PSA. Phenol: ACGIH  -  no STEL set. NIOSH phenol STEL: 15.6 ppm.",
                    "tlv_ceil":"Not established for PSA. Phenol IDLH (NIOSH): 250 ppm  -  treat as upper bound for respiratory protection decisions.",
                    "idlh":"NIOSH IDLH for phenol component: 250 ppm. PSA: treat as phenol-hazard material. Respiratory protection required if generating mist/vapour above OEL guidance.",
                    "ld50":"Oral rat: ~1500 mg/kg (PSA mixture, by analogy). Phenol component (CAS 108-95-2): LD50 rat oral 317 mg/kg; dermal rat 1500 mg/kg; dermal rabbit 630 mg/kg (RTECS confirmed from Fishersci MSDS).",
                    "lc50":"Inhalation rat LC50 316 mg/m3/4H (phenol, RTECS HX9450000  -  Fishersci MSDS confirmed). Mouse inhalation LC50 177 mg/m3/4H. PSA acid mist: treat per H2SO4 mist limit 1 mg/m3 (ACGIH).",
                    "flash":">150deg C (closed cup)  -  combustible liquid, not flammable at ambient conditions","bp":"~186deg C (decomposes above this)","mp":"~33deg C (solidifies in cold storage  -  warm before use)","sg":"1.28 g/cm3 at 20deg C","vp":"<0.01 hPa at 20deg C  -  very low vapour pressure",
                    "odour":"Faint phenolic odour  -  odour threshold phenol: 0.05 ppm. Some warning property but not reliable. SKIN absorption is primary hazard route, not vapour.",
                    "reactivity":"Strong acid  -  exothermic reaction with strong bases (NaOH, KOH). Reacts with Na2Cr2O7/CrO3 (STRICTLY INCOMPATIBLE  -  oxidiser + organic acid = fire risk). Dissolves carbon steel, aluminium, copper  -  use PP, HDPE, or SS316. Decomposes >200deg C producing SO2, phenol vapour. Hygroscopic. Reacts with active metals (Fe, Al)  -  liberates H2 gas.",
                    "health":"Skin and eye corrosive. SKIN ABSORPTION  -  phenol component crosses skin barrier causing systemic toxicity (ACGIH Skin designation). CNS effects: phenol causes sudden collapse at high doses. Cardiac arrhythmia from systemic phenol. Liver/kidney damage from chronic phenol absorption. Respiratory: acid mist irritates mucous membranes, bronchospasm. Not listed as carcinogen (IARC, ACGIH).",
                    "env":"Phenol aquatically toxic: fish (fathead minnow) LC50 41 mg/L 48h; Daphnia EC50 4 mg/L 96h (Fishersci confirmed). Rapidly biodegrades in soil  -  phenol half-life <5 days. Sulphonate component more persistent. WTP treatment removes phenol effectively. Does not bioconcentrate (BCF <100).",
                    "storage":"Cool, dry, sealed. HDPE or PP-lined containers. Away from: bases, oxidisers, Cr-VI (incompatible). Hygroscopic  -  seal tightly. Secondary containment. Inspect containers for corrosion at every filling.",
                    "ppe":"Chemical splash goggles mandatory. Full face shield for bulk handling. Nitrile or neoprene gloves. PVC chemical apron. Mist: half-mask with OV/acid gas cartridge. CRITICAL: wash skin immediately  -  phenol absorbs before pain sensation.",
                    "emergency":"Skin: IMMEDIATE wash with soap + water 15+ min  -  phenol absorbs silently through intact skin, causes systemic phenol poisoning. Eye: flush 15+ min, medical. Ingestion: do NOT induce vomiting, medical immediately. Spill: absorb with dry inert material, HDPE container, do NOT flush to drain (aquatic toxic).",
                    "etl1_use":"Electrolytic tin plating bath  -  grain refiner and conductivity agent. 3-6 g/L combined with ENSA. Controls tin crystal grain size and provides bath conductivity.",
                    "soc":"3-6 g/L (combined PSA+ENSA)","sol":"2-7 g/L",
                },
                "A3  -  Dioctyl Sebacate (DOS)": {
                    "code":"A3","risk":30,"color":"#22c55e",
                    "class":"Combustible liquid","hazchem":"NFPA 1-1-0","nfpa":"1-1-0","cas":"122-62-3",
                    "tlv_twa":"10 mg/m3 (ACGIH PNOR inhalable) | 3 mg/m3 (respirable)  -  nuisance aerosol","tlv_stel":"Not established specifically. Respirable PNOR ACGIH: 3 mg/m3 (same as TWA respirable  -  no STEL set).","tlv_ceil":"Not established (negligible vapour pressure  -  essentially no ceiling needed).","ld50":"5000 mg/kg (rat, oral) ✓ Wikipedia ChemSpider","lc50":"Not established (VP 0.000024 Pa  -  no inhalation hazard at ambient)",
                    "flash":"190deg C (closed cup)","bp":">300deg C","mp":"-40deg C","sg":"0.914","vp":"<0.01 hPa at 20deg C",
                    "odour":"Faint oily odour",
                    "reactivity":"Stable under normal conditions. Incompatible with strong oxidisers (CrO3  -  hazardous reaction). High temperatures cause decomposition to CO, CO2. Not reactive with water or bases under normal conditions.",
                    "health":"Low acute toxicity. Mild skin and eye irritant. Not a known carcinogen. Oil mist at elevated temperatures may cause respiratory irritation.",
                    "env":"Low toxicity to aquatic organisms. Biodegradable. Low environmental persistence.",
                    "storage":"Normal conditions. Cool, dry. Away from strong oxidisers and ignition sources above 190deg C.",
                    "ppe":"Safety glasses, standard work gloves for routine handling.",
                    "emergency":"Spills: absorb with dry material. Non-hazardous cleanup. Person: wash with soap and water.",
                    "etl1_use":"Electrostatic oiling  -  applied to finished tin plate surface at 1-2 g/m2 for corrosion protection in storage/transport",
                    "soc":"Oil application rate per product spec","sol":"Per product spec",
                },
                "A4  -  ENSA (Ethoxylated Naphthol Sulphonic Acid)": {
                    "code":"A4","risk":40,"color":"#22c55e",
                    "class":"Proprietary plating brightener  -  ethoxylated alpha/beta naphthol sulphonate. Atotech/Enthone/MacDermid proprietary. TSCA listed components. GHS: H302, H312, H332, H315, H319.","hazchem":"NFPA 2-1-1","nfpa":"2-1-1","cas":"Mixture (naphthol sulphonate: 1321-69-3)",
                    "tlv_twa":"Not established for ENSA blend (ACGIH/NIOSH). Naphthol (alpha, CAS 90-15-3): no OEL set. Beta-naphthol (CAS 135-19-3): not listed. Plating bath acid mist (H2SO4): ACGIH TLV-TWA 1 mg/m3. Use 1 mg/m3 as practical guidance for acid mist control.",
                    "tlv_stel":"Not established. Plating acid mist STEL: 3 mg/m3 (H2SO4, by analogy).",
                    "tlv_ceil":"Not established",
                    "idlh":"Not established by NIOSH for ENSA. Parent naphthol NIOSH IDLH: not determined. Control to below LEV design level.",
                    "ld50":"Not published for proprietary blend. Alpha-naphthol (CAS 90-15-3): LD50 rat oral 1870 mg/kg. Beta-naphthol (CAS 135-19-3): LD50 rat oral 2000 mg/kg. ENSA estimated: >2000 mg/kg oral (low-moderate toxicity).",
                    "lc50":"Not established for ENSA blend. Alpha-naphthol vapour LC50: not determined (low VP at ambient  -  not significant inhalation hazard as vapour). Acid mist: LC50 rat H2SO4 mist 0.35 mg/L/2H (reference for mist control).",
                    "flash":"~170deg C (estimated)","bp":"200-250deg C (decomposes)","mp":"Liquid at ambient (unknown solidification temp)","sg":"~1.1-1.2 g/cm3","vp":"Very low at ambient  -  not a significant vapour hazard",
                    "odour":"Mild aromatic/naphthenic odour  -  detectable before significant hazard concentration in most conditions.",
                    "reactivity":"Moderately stable in dilute H2SO4 (plating bath pH 1-2). INCOMPATIBLE with: strong oxidisers (Na2Cr2O7, CrO3  -  DO NOT MIX), strong bases (>pH 12  -  hydrolysis). Decomposes above 60deg C in strongly acidic bath  -  ENSA breakdown products accumulate -&gt; plating quality deteriorates. Naphthol component: reacts with Cr-VI oxidisers  -  fire risk.",
                    "health":"Skin irritant (H315), eye irritant (H319). Naphthol component: systemic toxicity if absorbed  -  liver, kidney effects. Respiratory: acid bath mist is the primary inhalation concern (H2SO4 mist from plating bath, not ENSA vapour). No evidence of carcinogenicity (IARC not listed for ENSA or naphthol sulphonate). Chronic: monitor bath breakdown products  -  naphthol concentration should not exceed OEL guidance.",
                    "env":"Aquatic toxicity: alpha-naphthol fish LC50 ~3 mg/L (moderately toxic). Daphnia EC50 ~2-4 mg/L. Ethoxylate surfactant: moderate persistence. WTP biological treatment reduces naphthol. Naphthol sulphonate: more persistent than parent. Do not discharge untreated to surface water.",
                    "storage":"Cool, dark, sealed HDPE containers. Away from Cr-VI oxidisers (incompatible). Shelf life 12 months sealed. Protect from freezing. Segregate from Cr-VI storage (chemical incompatibility).",
                    "ppe":"Chemical splash goggles. Nitrile gloves. Lab coat. Bath area: LEV mandatory (acid mist). Half-mask with P2 particulate filter if mist exposure likely.",
                    "emergency":"Skin/Eye: flush 15+ min (naphthol absorption risk on skin). Ingestion: medical immediately  -  naphthol toxic. Spill: collect in HDPE, absorb with inert material, do NOT flush to drain (aquatic toxic). Neutralise with sodium bicarbonate before disposal.",
                    "etl1_use":"Electrolytic tin plating bath brightener  -  combined with PSA (3-6 g/L total). Controls tin grain size, produces bright mirror finish. Critical for tin plate quality specification.",
                    "soc":"3-6 g/L (combined PSA+ENSA)","sol":"2-7 g/L",
                },
                "A5  -  Sodium Dichromate (Na2Cr2O7)": {
                    "code":"A5","risk":95,"color":"#ef4444",
                    "class":"CARCINOGEN (IARC Gr.1 | ACGIH A1 | NTP Known | Cal Prop 65)  -  Oxidising solid, TOXIC, reproductive toxin, aquatic hazard. UN 3288. GHS: H272 H301 H312 H314 H317 H330 H334 H340 H350 H360 H372 H410.","hazchem":"HAZCHEM 2X","nfpa":"4-0-1 (OX)","cas":"10588-01-9 (anhydrous) | 7789-12-0 (dihydrate)",
                    "tlv_twa":"ACGIH TLV-TWA: 0.01 mg/m3 as Cr(VI)  -  2023 (A1 Confirmed Human Carcinogen). OSHA PEL: 5 µg/m3 (0.005 mg/m3) as Cr(VI)  -  29 CFR 1910.1026 (2006). NIOSH REL: 0.0002 mg/m3 (0.2 µg/m3) as Cr  -  lowest feasible concentration. INDIA: Factories Act  -  adopt ACGIH/OSHA limit.",
                    "tlv_stel":"Not established separately. OSHA Action Level: 2.5 µg/m3 as Cr(VI). Above AL: medical surveillance + air monitoring mandatory.",
                    "tlv_ceil":"ACGIH: TLV-TWA applies  -  no separate ceiling. Treat as effective ceiling due to A1 carcinogen classification. Any detectable Cr(VI) above OEL = corrective action.",
                    "idlh":"NIOSH IDLH: 15 mg/m3 as Cr(VI). IMMEDIATELY DANGEROUS TO LIFE AND HEALTH above this. Biological Exposure Index (BEI): 25 µg Cr/g creatinine (end-of-shift urine)  -  annual biological monitoring mandatory.",
                    "ld50":"Oral rat: 50 mg/kg (CAS 10588-01-9, Wikipedia/PubChem/Fishersci confirmed). Dermal rabbit: 1000 mg/kg (Acros MSDS confirmed). HIGHLY TOXIC by ingestion (GHS Category 3).",
                    "lc50":"Inhalation rat: 0.124 mg/L/4H (Acros MSDS confirmed, RTECS HX7750000). EXTREMELY TOXIC by inhalation. Note: LC50 well above IDLH  -  sub-lethal carcinogenic doses are the primary concern.",
                    "flash":"Non-flammable  -  OXIDISING SOLID. Contact with organics/combustibles causes fire without external ignition.","bp":"400deg C decomposes (no boiling)","mp":"356.7deg C (anhydrous) | Dihydrate loses crystal water at 84deg C","sg":"2.52 g/cm3","vp":"Negligible at ambient  -  DUST is the inhalation hazard, not vapour.",
                    "odour":"Odourless  -  ABSOLUTELY NO SENSORY WARNING. Carcinogen exposure occurs without any detectable smell. CONTINUOUS REAL-TIME AIR MONITORING IS MANDATORY  -  no substitutes.",
                    "reactivity":"STRONG OXIDISER  -  spontaneous ignition with: organics (paper, wood, cloth, ethanol, acetone, oils). Violently exothermic with reducing agents (FeSO4, Na2SO3, Fe). Reacts with H2SO4  -  forms CrO3 solution (chromic acid  -  even more reactive). INCOMPATIBLE: ALL organic compounds, all reducing agents, ammonium compounds (explosive at temperature), combustible metals.",
                    "health":"IARC Group 1 | ACGIH A1 | NTP Known Human Carcinogen. Primary: lung cancer (15-30x elevated risk in chromate production workers  -  Mancuso 1975, IARC 1990). Nasal cavity, sinuses, larynx cancers. Mechanism: Cr(VI) enters cells via sulphate transport channels -&gt; reduced to Cr(III) inside -&gt; DNA adducts, double-strand breaks, chromosomal aberrations. Skin: chrome ulcers (slow, painless, deep  -  CAS of ulcer documented in Indian Chrome workers). Eye: severe corrosive burns. Systemic: kidney tubular damage, liver injury. Reproductive: teratogenic, H360. Latency: 15-30 years. Annual medical surveillance mandatory under Factories Act.",
                    "env":"Cr(VI) VERY HIGHLY TOXIC to aquatic organisms. Fish LC50 (bluegill): 425-488 mg/L 96h (Fishersci). Daphnia: extremely sensitive (<1 mg/L). PERSISTENT in groundwater  -  resists biodegradation. CPCB effluent standard: Cr(VI) <0.1 mg/L final discharge. Must be chemically reduced to Cr(III) before treatment (use FeSO4 or SO2 at pH<3). MCL drinking water India: 0.05 mg/L total Cr. MSIHC Schedule  -  annual inventory to CPCB.",
                    "storage":"DEDICATED LOCKED STORE  -  all organics prohibited within 5m (incompatible). Cool, dry, ventilated. Secondary containment 110% volume. HDPE or PP-lined containers (not steel  -  corrosion). Annual CPCB inventory submission. MSIHC notification: above threshold. Fire extinguisher: water spray ONLY (no CO2 or dry powder). Restricted access  -  biometric/key control recommended.",
                    "ppe":"MANDATORY: Air-supplied respirator (SCBA or airline)  -  NO cartridge respirator acceptable for Cr-VI carcinogen work. Class B/C chemical suit. Full face shield. Heavy neoprene gloves (>0.5mm). Rubber boots. Buddy system mandatory. Annual biological monitoring: urine Cr (BEI: 25 µg/g creatinine).",
                    "emergency":"EVACUATE  -  no entry without SCBA. SPECIALIST HAZMAT RESPONSE ONLY. Spill: wet methods only (no dry sweeping  -  dust hazard). Cr(VI) reduction: FeSO4 at pH<3 then neutralise to pH 8-9. Person: immediate shower/decontamination, remove all clothing, medical examination, report to OH. CPCB notification within 48h of significant release.",
                    "etl1_use":"Chemical treatment bath  -  electrolytic chromate passivation. <10 mg Cr/m2 deposited on tinplate for corrosion protection and lacquer adhesion. MSIHC Schedule substance.",
                    "soc":"Air: <0.01 mg/m3 as Cr(VI) | Bath temp: 40-45deg C | Bath current: 300-2000A","sol":"Air OEL breach = immediate corrective action | Bath temp: >45deg C = auto-shutdown | Air Cr-VI >0.1 mg/m3 = EVACUATION",
                },
                "A6  -  Chromic Acid (CrO3/Cr-VI)": {
                    "code":"A6","risk":98,"color":"#ef4444",
                    "class":"CARCINOGEN  -  Powerful oxidiser, corrosive, highly toxic","hazchem":"NFPA 3-0-1 (OX)","nfpa":"3-0-1 (OX)","cas":"1333-82-0",
                    "tlv_twa":"0.05 mg/m3 as Cr (ACGIH)","tlv_stel":"0.1 mg/m3 ceiling","tlv_ceil":"0.1 mg/m3","ld50":"80 mg/kg (rat, oral)","lc50":"<10 mg/m3 (rat, 4h)",
                    "flash":"N/A (powerful oxidiser  -  not flammable but CAUSES fires)","bp":"250deg C (decomposes)","mp":"196deg C","sg":"2.70","vp":"Not applicable",
                    "odour":"Acrid, metallic (vapour/mist)",
                    "reactivity":"POWERFUL OXIDISER  -  contact with organics (oil, paper, wood, solvents) causes spontaneous ignition. Reacts explosively with reducing agents. Mixed with H2SO4: forms chromic acid solution. EXPLOSIVE contact with alcohol/acetone/ketones. Generates toxic Cr-VI mist when heated or agitated. Incompatible with: all organic materials, H2SO4 (exothermic), reducing agents, combustibles.",
                    "health":"IARC Group 1 CARCINOGEN  -  highest category. Causes lung cancer (15-30x normal risk with occupational exposure), nasal septum perforation, kidney cancer. TLV 0.05 mg/m3  -  one of the lowest industrial TLVs. Acute: severe skin corrosion, eye burns, nasal ulceration. Skin sensitiser. Mutagenic, teratogenic.",
                    "env":"MOST TOXIC common industrial chemical to aquatic organisms. Cr-VI persists in groundwater for decades. Classified as Priority Hazardous Substance under EU WFD. MSIHC mandatory reporting. MCL drinking water: 0.05 mg/L.",
                    "storage":"SEPARATE, locked, cool, dry store. NO organic materials within 5m. Secondary containment 110% volume. Access restricted to trained, medically cleared personnel. MSIHC annual reporting to CPCB/SPCB.",
                    "ppe":"MANDATORY: Air-supplied respirator (SCBA or airline), Class C full-body protective suit, face shield, heavy rubber gloves + boots. PPE inspection before every entry. Buddy system mandatory.",
                    "emergency":"EVACUATE  -  do not re-enter without SCBA. Specialist hazmat team only. Person contaminated: immediate SCBA removal, decontamination, emergency medical. Notify: plant emergency, CPCB (within 48h), state SPCB. Document all exposures  -  medical surveillance mandatory.",
                    "etl1_use":"Chemical treatment bath  -  Cr-VI passivation layer on tin plate (< 10 mg/m2 Cr on finished product for food can use)",
                    "soc":"Air: <0.05 mg/m3 (TLV-TWA)","sol":"Air: <0.1 mg/m3 ceiling | Breach = mandatory immediate SHUTDOWN",
                },
            }

            if "hom_chem" not in st.session_state:
                st.session_state.hom_chem = "A6  -  Chromic Acid (CrO3/Cr-VI)"

            # ── Beautified HOM Chemical Selector ──
            chem_names = list(CHEM_FULL.keys())
            chem_cols = st.columns(len(chem_names))
            for ii, cname in enumerate(chem_names):
                cd = CHEM_FULL[cname]
                rc3 = cd["color"]
                active = (st.session_state.hom_chem == cname)
                with chem_cols[ii]:
                    active_ring = f"box-shadow:0 0 0 2px {rc3};" if active else ""
                    short = cd["code"]
                    sname = cname.split("  -  ")[-1].replace("(","").replace(")","").split(" ")[0]
                    st.markdown(f'''<div style="background:{rc3}{"25" if active else "12"};border:1px solid {rc3}{"90" if active else "40"};border-top:4px solid {rc3};border-radius:10px;padding:.6rem .5rem;text-align:center;margin-bottom:4px;{active_ring}cursor:pointer">
<div style="font-size:.72rem;font-weight:900;color:{rc3};font-family:monospace;letter-spacing:1px">{short}</div>
<div style="font-size:.6rem;color:#94a3b8;margin-top:2px;line-height:1.3">{sname}</div>
</div>''', unsafe_allow_html=True)
                    if st.button(short, key=f"hom_{cname}", use_container_width=True, type="primary" if active else "secondary"):
                        st.session_state.hom_chem = cname
                        st.rerun()

            # ── Full chemical detail card  ──
            sel_chem = CHEM_FULL[st.session_state.hom_chem]
            sc2 = sel_chem["color"]
            chem_name_display = st.session_state.hom_chem.split("  -  ",1)[-1] if "  -  " in st.session_state.hom_chem else st.session_state.hom_chem
            code_display = sel_chem["code"]

            st.markdown(f"""<div style="background:linear-gradient(135deg,{sc2}15 0%,{sc2}05 100%);border:1px solid {sc2}60;border-left:5px solid {sc2};border-radius:14px;padding:1.2rem 1.6rem;margin:.8rem 0">
<div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:.5rem;margin-bottom:.6rem">
  <div>
    <span style="background:{sc2}25;color:{sc2};border:1px solid {sc2}60;font-size:.65rem;font-weight:800;padding:3px 10px;border-radius:20px;letter-spacing:1px;margin-right:8px">{code_display}</span>
    <span style="font-size:1.1rem;font-weight:800;color:#f1f5f9">{chem_name_display}</span>
  </div>
  <div style="display:flex;gap:6px;flex-wrap:wrap">
    <span style="background:#1e3a5f;color:#60a5fa;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">CAS: {sel_chem["cas"]}</span>
    <span style="background:rgba(249,115,22,.15);color:#f97316;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">HAZCHEM: {sel_chem["hazchem"]}</span>
    <span style="background:rgba(167,139,250,.15);color:#a78bfa;font-size:.6rem;font-weight:700;padding:3px 10px;border-radius:20px">NFPA: {sel_chem["nfpa"]}</span>
  </div>
</div>
<div style="font-size:.8rem;color:#94a3b8;line-height:1.6;margin-bottom:.5rem">{sel_chem["class"]}</div>
<div style="background:{sc2}12;border:1px solid {sc2}30;border-radius:8px;padding:.5rem .8rem;font-size:.78rem;color:#f97316;font-weight:600">&#128269; ETL-1 Use: {sel_chem["etl1_use"]}</div>
</div>""", unsafe_allow_html=True)

            # ── Key exposure limits strip ──
            tlv = sel_chem.get("tlv_twa","—"); stel = sel_chem.get("tlv_stel","—"); idlh = sel_chem.get("idlh","—"); ld50 = sel_chem.get("ld50","—")
            st.markdown(f'''<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:1rem">
<div style="background:#0d1f35;border:1px solid #1e3a5f;border-top:3px solid #3b82f6;border-radius:8px;padding:.7rem;text-align:center">
  <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:4px">TLV-TWA</div>
  <div style="font-size:.78rem;font-weight:700;color:#e2e8f0;line-height:1.4">{tlv[:50] if len(tlv)>50 else tlv}</div></div>
<div style="background:#0d1f35;border:1px solid #1e3a5f;border-top:3px solid #a78bfa;border-radius:8px;padding:.7rem;text-align:center">
  <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#a78bfa;margin-bottom:4px">TLV-STEL (15 min)</div>
  <div style="font-size:.78rem;font-weight:700;color:#e2e8f0;line-height:1.4">{stel[:50] if len(str(stel))>50 else stel}</div></div>
<div style="background:#1a0505;border:1px solid rgba(239,68,68,.4);border-top:3px solid #ef4444;border-radius:8px;padding:.7rem;text-align:center">
  <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin-bottom:4px">IDLH</div>
  <div style="font-size:.78rem;font-weight:700;color:#fca5a5;line-height:1.4">{str(idlh)[:50] if len(str(idlh))>50 else idlh}</div></div>
<div style="background:#0d1f35;border:1px solid #1e3a5f;border-top:3px solid #22c55e;border-radius:8px;padding:.7rem;text-align:center">
  <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#22c55e;margin-bottom:4px">LD50 / LC50</div>
  <div style="font-size:.78rem;font-weight:700;color:#e2e8f0;line-height:1.4">{ld50[:50] if len(str(ld50))>50 else ld50}</div></div>
</div>''', unsafe_allow_html=True)

            # A-category tags for this chemical
            chem_acat_map = {
                "A1  -  Sulphuric Acid (H2SO4)":    [("A2","Toxic (TLV 1 mg/m3)","#a78bfa"),("A4","Corrosive","#3b82f6"),("A3","Reactive (H2 with metals)","#ef4444")],
                "A2  -  Phenol Sulfonic Acid (PSA)":  [("A2","Irritant","#a78bfa"),("A4","Corrosive","#3b82f6")],
                "A3  -  Dioctyl Sebacate (DOS)":       [("A1","Combustible (flash 190deg C)","#f97316")],
                "A4  -  ENSA":                          [("A2","Irritant","#a78bfa")],
                "A5  -  Sodium Dichromate (Na2Cr2O7)": [("A2","CARCINOGEN IARC Gr.1 (TLV 0.05 mg/m3)","#a78bfa"),("A3","Strong Oxidiser","#ef4444")],
                "A6  -  Chromic Acid (CrO3/Cr-VI)":    [("A2","CARCINOGEN IARC Gr.1 (TLV 0.05 mg/m3)","#a78bfa"),("A3","Powerful Oxidiser","#ef4444"),("A4","Corrosive","#3b82f6")],
            }
            acats = chem_acat_map.get(st.session_state.hom_chem, [])
            if acats:
                acat_html = " ".join(f'<span style="background:{c}20;color:{c};border:1px solid {c}40;font-size:.68rem;font-weight:700;padding:3px 10px;border-radius:20px;margin-right:4px">{cat}: {desc}</span>' for cat, desc, c in acats)
                st.markdown(f'<div style="margin-bottom:.6rem">{acat_html}</div>', unsafe_allow_html=True)

            # TLV explanations
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.6rem 1rem;margin-bottom:.6rem;font-size:.72rem;color:#64748b"> <b style="color:#e2e8f0">TLV-TWA:</b> Time-Weighted Average over 8h shift  -  maximum daily exposure. &nbsp; <b style="color:#e2e8f0">TLV-STEL:</b> Short-Term Exposure Limit (15 min)  -  peak limit. &nbsp; <b style="color:#e2e8f0">TLV-C:</b> Ceiling  -  never to be exceeded even instantaneously. &nbsp; <b style="color:#ef4444">IDLH:</b> Immediately Dangerous to Life & Health  -  emergency escape value. </div>""", unsafe_allow_html=True)

            # Full data in tabs
            st.markdown('<div class="sl-sec">Physical & Toxicity Data</div>', unsafe_allow_html=True)

            st.markdown('<div style="font-size:.68rem;color:#475569;margin-bottom:.8rem">✓ = source-verified value. Sources: ACGIH TLV Booklet 2023, NIOSH Pocket Guide 2023, RTECS, Fishersci MSDS, Acros MSDS, Wikipedia (peer-reviewed), PubChem.</div>', unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            with r1:
                    st.markdown(f"""<div class="sl-card">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.6rem">EXPOSURE LIMITS (A2  -  Toxicity)</div>
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


            # htab5  -  Suppliers & Regulatory

            st.markdown('<div class="sl-sec">Suppliers & Regulatory Compliance</div>', unsafe_allow_html=True)
            sel_name = st.session_state.hom_chem

            SUPPLIER_DATA = {
                    "A1  -  Sulphuric Acid (H2SO4)": {
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
                            ("MSIHC Rules 1989","Schedule 2  -  100 MT threshold","Mandatory safety audit, emergency plan, CPCB notification"),
                            ("Factories Act 1948","Schedule to Section 41B","Safety officer mandatory above threshold"),
                            ("CPCB Hazardous Waste Rules 2016","Listed hazardous chemical","Disposal and effluent consent conditions apply"),
                            ("UN Number","UN 1830 (conc.) / UN 1832 (spent)","Class 8  -  Corrosive. Packing Group II."),
                            ("PESO (Explosives/Chemical Safety)","Licensing for bulk storage","Tank installation approval required"),
                        ],
                        "india_msds_ref":"As per Schedule 10 of MSIHC Rules 1989  -  MSDS to be maintained in Hindi and local language at plant.",
                    },
                    "A2  -  Phenol Sulfonic Acid (PSA)": {
                        "suppliers":[
                            ("Chemtex Specialty Ltd","Ahmedabad, Gujarat","India","Primary plating chemical supplier to Indian tinplate industry."),
                            ("Hindustan Tin Works","Delhi","India","Plating chemical distributor."),
                            ("Atotech GmbH","Berlin","Germany","Global plating chemistry leader. Supplies PSA for tin plating."),
                            ("Enthone (Cookson)","West Haven, Connecticut","USA","High-purity PSA for electronics and tinplate plating."),
                            ("MacDermid Alpha","USA","USA","Plating bath additive supplier  -  PSA and ENSA combined systems."),
                        ],
                        "spec":"Technical grade 98%+ purity. Low inorganic content. Supplied in 200L HDPE drums or IBC tanks.",
                        "storage_limit":"No MSIHC threshold. Store as general chemical  -  cool, dry, away from bases.",
                        "regulatory":[
                            ("REACH (if imported from EU)","SVHC check required","Verify substance is not on SVHC candidate list"),
                            ("UN Number","UN 3265","Class 8  -  Corrosive liquid, acidic, organic. PG III."),
                            ("Customs (import)","Chapter 29  -  Organic Chemicals","Import duty + GST applicable"),
                        ],
                        "india_msds_ref":"MSDS per GHS/IS 1991 standards. Maintain at workplace in English and Hindi.",
                    },
                    "A3  -  Dioctyl Sebacate (DOS)": {
                        "suppliers":[
                            ("BASF SE","Ludwigshafen","Germany","Global supplier of DOS (Dioctyl Sebacate)  -  food contact grade."),
                            ("Lanxess AG","Cologne","Germany","Plasticisers division  -  DOS for packaging applications."),
                            ("Hallstar Industrial","Chicago, USA","USA","DOS for metalworking and corrosion protection applications."),
                            ("Fine Organics Industries Ltd","Mumbai","India","Domestic DOS manufacturer. Food contact grade certified."),
                            ("Balaji Amines Ltd","Solapur, Maharashtra","India","Specialty chemical  -  esters including DOS."),
                        ],
                        "spec":"Food contact grade per FDA 21 CFR 175.105 and EU 10/2011. Purity >99%. Supplied in 200L HDPE drums.",
                        "storage_limit":"Non-regulated. Store in cool, dry conditions away from ignition sources (flash point 190deg C).",
                        "regulatory":[
                            ("FDA 21 CFR 175.105","Food contact indirect additive","Required for tin plate used in food can manufacturing"),
                            ("EU Regulation 10/2011","Plastic food contact materials","SML (Specific Migration Limit) compliance for EU export"),
                            ("FSSAI India","Food Safety Compliance","DOS on finished tin plate must meet FSSAI indirect contact limits"),
                            ("UN Number","Not regulated in transport","Combustible liquid  -  not classified as dangerous goods at ambient temp"),
                        ],
                        "india_msds_ref":"MSDS per GHS. Food contact grade certification to be maintained with each lot.",
                    },
                    "A4  -  ENSA (Ethoxylated Naphthol Sulphonic Acid)": {
                        "suppliers":[
                            ("Atotech GmbH","Berlin","Germany","Proprietary ENSA formulation for tin plating. Global standard."),
                            ("Enthone (Cookson Electronics)","West Haven, USA","USA","Tin plating brightener system including ENSA."),
                            ("MacDermid Alpha Electronics","USA","USA","Complete tin plating chemistry systems."),
                            ("Dipsol Chemicals","Osaka","Japan","ENSA and PSA for tin plating  -  ISO 9001 certified."),
                            ("Chemtex Specialty Ltd","Ahmedabad","India","Domestic distributor for plating chemicals."),
                        ],
                        "spec":"Proprietary blend  -  supplied per OEM specification. Concentration per bath formulation. 200L HDPE drums.",
                        "storage_limit":"No MSIHC threshold. Chemical stability: 12 months from manufacture date. Cool, dark storage.",
                        "regulatory":[
                            ("REACH (EU import)","Registration required >1 T/yr","Verify ECHA registration status before import"),
                            ("UN Number","UN 3265 or 3264 (pH dependent)","Class 8 corrosive  -  verify with SDS"),
                            ("Effluent discharge","ENSA breakdown products in wastewater","WTP treatment required before ETP discharge"),
                        ],
                        "india_msds_ref":"Supplier MSDS to be obtained per MSIHC Schedule 10. Naphthol component declared.",
                    },
                    "A5  -  Sodium Dichromate (Na2Cr2O7)": {
                        "suppliers":[
                            ("Lanxess AG (formerly Bayer Chemicals)","Cologne","Germany","Global leader in chromium chemicals. Na2Cr2O7 2H2O technical grade."),
                            ("Elementis Chromium","Castle Hayne, USA","USA","Large-scale Na2Cr2O7 producer for industrial use."),
                            ("SISCO Research Laboratories","Mumbai","India","Analytical grade  -  small quantities."),
                            ("Aditya Birla Chemicals","Mumbai","India","Industrial chemical distributor  -  import and supply."),
                            ("Merck KGaA","Darmstadt","Germany","Technical and reagent grade sodium dichromate."),
                        ],
                        "spec":"Technical grade min 99.5% purity as Na2Cr2O7·2H2O. Low chloride content (<0.01%). 25 kg HDPE bags or 200 kg drums.",
                        "storage_limit":"MSIHC Schedule  -  Cr-VI compound. Mandatory CPCB notification. Locked storage, restricted access, annual inventory audit.",
                        "regulatory":[
                            ("MSIHC Rules 1989","Schedule 1  -  Hexavalent Chromium compounds","Mandatory reporting to CPCB/SPCB. Safety audit. Emergency plan."),
                            ("REACH (EU)  -  SVHC","AUTHORIZATION REQUIRED for all uses in EU","Use authorisation required from ECHA  -  non-trivial compliance"),
                            ("Indian Factories Act 1948","Scheduled substance","Medical surveillance mandatory for all exposed workers  -  annual"),
                            ("CPCB Hazardous Waste Rules 2016","Cr-VI in effluent: discharge standard <0.1 mg/L","Chrome reduction plant mandatory. Effluent monitoring."),
                            ("UN Number","UN 1479","Class 5.1  -  Oxidising solid. PG II. Class 6.1 subsidiary risk (toxic)."),
                            ("Carcinogen Register","IARC Group 1  -  mandatory declaration","Annual medical surveillance, biological monitoring (urine Cr)."),
                        ],
                        "india_msds_ref":"MSDS mandatory in Hindi + English per MSIHC. IARC Group 1 carcinogen to be declared. Worker training records maintained.",
                    },
                    "A6  -  Chromic Acid (CrO3/Cr-VI)": {
                        "suppliers":[
                            ("Lanxess AG","Cologne","Germany","CrO3 technical grade  -  global leader. Supply via licensed importers only."),
                            ("Elementis Chromium","USA","USA","Chromic acid for surface treatment applications."),
                            ("Charkit Chemical","USA","USA","CrO3 for electroplating and anodising applications."),
                            ("Gujarat Alkalies and Chemicals Ltd (GACL)","Vadodara","India","Domestic Cr-VI chemical producer  -  chromic acid."),
                            ("Aditya Birla Chemicals","Mumbai","India","Licensed importer and distributor of chromium chemicals."),
                        ],
                        "spec":"Technical grade CrO3 99%+ purity. Dark red crystals. 50 kg HDPE-lined steel drums. Oxidiser  -  NO organic packing material.",
                        "storage_limit":"MSIHC Schedule. Mandatory CPCB notification. Strict segregation from ALL organics. No shared storage with any combustible. CCOE approval for quantities.",
                        "regulatory":[
                            ("MSIHC Rules 1989","Schedule 1  -  Cr-VI compounds","Mandatory major hazard installation if above threshold. CPCB annual report."),
                            ("REACH (EU)  -  AUTHORIZATION","SUNSET DATE PASSED  -  EU USE RESTRICTED","Import from EU may be restricted  -  verify with supplier"),
                            ("Indian Factories Act 1948 Schedule","Hazardous process  -  Section 87","Safety committee mandatory. Medical examination before engagement and annually."),
                            ("CPCB Hazardous Waste Rules 2016","Cr-VI in effluent: <0.1 mg/L final discharge","Zero liquid discharge target for Cr-VI industries"),
                            ("UN Number","UN 1755","Class 8  -  Corrosive liquid. PG II. Also Class 5.1 (oxidising) subsidiary."),
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
                    st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#ef4444;margin:.6rem 0 .4rem">REGULATORY COMPLIANCE  -  INDIA & INTERNATIONAL</div>', unsafe_allow_html=True)
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

            render_global_incidents(["H2SO4","Cr-VI","Phenol","DOS","ENSA"])
            render_qa_bot("g_hom")
        with tabs[3]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/HOM/002  -  Chemical Interaction Matrix  -  ETL-1 Electrolytic Tin Plating Line 1</p>', unsafe_allow_html=True)
            render_glossary()

            # Full CIM data matching the screenshots
            CHEM_NAMES = {
                "H2SO4": "SULPHURIC ACID",
                "PSA": "PHENOLSULFONIC ACID, LIQUID",
                "CrO3": "CHROMIC ACID, SOLUTION",
                "DOS": "BIS(2-ETHYLHEXYL) SEBACATE",
                "Na2Cr2O7": "SODIUM DICHROMATE",
                "NaOH": "SODIUM HYDROXIDE SOLUTION",
            }

            # Pair interaction data  -  (status, hazards, gases)
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
                        grid_html += '<td style="background:#0d2a0d;padding:8px 12px;border:1px solid #2d4a2d;color:#475569;vertical-align:top"> - </td>'
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
                gas_html += f'<div style="padding:3px 0">&#8226; {g}</div>'
            gas_html += '</div></div>'
            st.markdown(gas_html, unsafe_allow_html=True)

            # ── Reactivity alerts ──
            st.markdown('<div class="sl-sec">Reactivity Alerts</div>', unsafe_allow_html=True)
            reactivity = [
                ("SODIUM DICHROMATE","Strong Oxidising Agent"),
                ("PHENOLSULFONIC ACID, LIQUID","Known Catalytic Activity"),
                ("CHROMIC ACID, SOLUTION","Strong Oxidising Agent  -  CARCINOGEN (IARC Group 1)","Known Catalytic Activity"),
                ("SULPHURIC ACID","Strong Acid  -  corrosive, reacts with metals liberating H2 gas"),
                ("BIS(2-ETHYLHEXYL) SEBACATE (DOS)","Combustible liquid  -  incompatible with strong oxidisers"),
            ]
            for item in reactivity:
                name = item[0]
                props = item[1:]
                props_html = "".join(f'<div style="font-size:.75rem;color:#94a3b8;padding:2px 0">&#8226; {p}</div>' for p in props)
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

            render_qa_bot("g_cim")
        with tabs[4]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/PDB/001 Rev.06 Eff.Dt.:18.08.2023  -  ETL-1 Electrolytic Tin Plating Line 1, Tata Steel Tinplate (TCIL), Golmuri. All limits from WEAN United Process Norms / Supplier manuals.</p>', unsafe_allow_html=True)
            render_glossary()

            # ── EXACT EXCEL PDB TABLE  (Form No. PSM/PSI/PDB/001) ──
            st.markdown('''<div style="background:#080d18;border:1px solid #1e3a5f;border-radius:10px;padding:1rem 1.2rem;margin-bottom:1rem">
<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.2rem">PROCESS DESIGN BASIS  —  ETL-1 ELECTROLYTIC TINNING LINE</div>
<div style="font-size:.62rem;color:#475569">Form No.: PSM/PSI/PDB/001 &nbsp;·&nbsp; Rev. No.: 06 &nbsp;·&nbsp; Eff. Dt.: 18.08.2023 &nbsp;·&nbsp; Dept: ETL 1 &nbsp;·&nbsp; All 28 parameters from PDB sheet</div>
</div>''', unsafe_allow_html=True)

            # All 28 PDB rows from Excel exactly
            PDB_EXCEL = [
                # sl, param, uom, soc_min, soc_max, id_min, id_max, action_min, action_max, sol_min, sol_max, cons_min, cons_max, barrier_min, barrier_max, psm, ref, sub_proc
                (1,"Power Pack Hydraulic Pump Pressure","bar",55,70,"HMI pressure indication","HMI pressure indication","Monitor pressure – SOP ETL-HYD-01","Auto trip system – SOP ETL-HYD-01",45,100,"Coil car unable to lift coil","Oil temperature increase with abnormal noise","Pressure switch set at 20 bar generates malfunction","Temperature sensor alarm with auto trip","Yes","WEAN United Process Norms","Coil Feeding"),
                (2,"DM Water Pressure to Welding Machine","kg/cm²",4.5,5.5,"Pressure gauge / HMI","Pressure gauge / HMI","Check cooling water – SOP WLD-01","Stop welding, rectify leakage – SOP WLD-01",4.5,5.5,"Welding cannot initiate","Improper cooling due to leakage","Pressure switch interlock blocks welding","Throttle valve limits pressure to 5 kg/cm²","Yes","NSEC Welder Manual","Coil Feeding"),
                (3,"Compressed Air Pressure to Welding Machine","kg/cm²",4.5,5.5,"Pressure gauge / HMI","Pressure gauge / HMI","Check air supply – SOP WLD-02","Stop welding, rectify – SOP WLD-02",4.5,6.5,"Welding stops; machine idle","Excess air released via safety valve","Pressure switch inhibits welding","Safety valve on air accumulator","Yes","NSEC Welder Manual","Coil Feeding"),
                (4,"Pre-Primary Alkali Solution Temperature (NaOH)","°C",80,90,"Temperature indicator on HMI","Temperature indicator on HMI","Monitor temperature – SOP CLN-01","Adjust steam valve – SOP CLN-01",80,90,"Improper cleaning leading to patch marks","Burning marks causing matted strip surface","Steam control valve regulation","Temperature monitoring with alarm","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (5,"Pre-Primary Alkali Solution Concentration (NaOH)","g/L",25,30,"Lab test report","Lab test report","Adjust concentration – SOP CLN-02","Chemical dosing correction – SOP CLN-02",25,30,"Improper cleaning causing patch marks","Solution carryover causing surface defects","Shift-wise lab testing","Immediate corrective action based on lab feedback","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (6,"Primary Alkali Solution Temperature (NaOH)","°C",80,90,"Temperature indicator on HMI","Temperature indicator on HMI","Monitor temperature – SOP CLN-03","Adjust steam valve – SOP CLN-03",80,90,"Incomplete removal of contaminants","Burning and matted strip surface","Steam flow through control valve","Temperature control with alarm","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (7,"Primary Alkali Solution Concentration (NaOH)","g/L",25,30,"Lab test report","Lab test report","Correct chemical strength – SOP CLN-04","Dose correction – SOP CLN-04",25,30,"Poor cleaning of strip","Chemical patches and strip surface defects","Lab testing every shift","Immediate correction after lab feedback","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (8,"Primary Cleaning Current","kA",2.5,3.5,"PLC / HMI current display","PLC / HMI current display","Adjust current – SOP CLN-05","Stop process – SOP CLN-05",2.5,3.5,"Ineffective electrolytic cleaning","Burning leading to strip breakage","PLC-limited total current","PLC interlock to restrict over-current","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (9,"Secondary Alkali Solution Temperature (NaOH)","°C",80,90,"Temperature indicator on HMI","Temperature indicator on HMI","Monitor temperature – SOP CLN-06","Adjust steam valve – SOP CLN-06",80,90,"Improper final cleaning","Burning marks on strip","Steam valve control","Temperature alarm and control","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (10,"Secondary Alkali Solution Concentration (NaOH)","g/L",25,30,"Lab test report","Lab test report","Adjust solution strength – SOP CLN-07","Chemical dosing – SOP CLN-07",25,30,"Inadequate cleaning","Solution patches and surface defects","Shift-wise lab testing","Corrective action on deviation","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (11,"Secondary Cleaning Current","kA",2.5,3.5,"PLC / HMI current display","PLC / HMI current display","Current adjustment – SOP CLN-08","Stop process – SOP CLN-08",2.5,3.5,"Poor electrolytic cleaning","Burning and strip breakage","PLC current limitation","PLC over-current interlock","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (12,"Pickling Acid Solution Concentration (H₂SO₄)","g/L",8,10,"Lab test report","Lab test report","Adjust acid strength – SOP PKL-01","Chemical dosing – SOP PKL-01",8,10,"Improper removal of iron oxide","Surface corrosion and defects","Lab testing every shift","Immediate corrective action based on lab result","Yes","WEAN United Process Norms","Cleaning & Rinsing"),
                (13,"Sn++ Concentration in Plating Solution (SnSO₄)","g/L",26,32,"Lab test value","Lab test value","Adjust SnSO₄ dosing – SOP PLT-01","Reduce/add make-up – SOP PLT-01","<26",">32","Improper tin coating on sheet","Loss of tin / over-coating on sheet","Lab testing twice per shift","Immediate corrective action after lab feedback","Yes","WEAN United Process Norms","Tin Plating"),
                (14,"Free Acid Concentration","g/L",13,16,"Lab test value","Lab test value","Adjust acid dosing – SOP PLT-02","Correct bath chemistry – SOP PLT-02","<13",">16","Product degradation due to SCO / patch","Product downgrade due to surface defect","Routine lab testing each shift","Immediate chemical correction","Yes","WEAN United Process Norms","Tin Plating"),
                (15,"ENSA Concentration","g/L",3,6,"Lab test report","Lab test report","Adjust ENSA addition – SOP PLT-03","Correct additive dosing – SOP PLT-03","<3",">6","Dull band formation","Product downgrade due to dull band","Lab test every shift","Immediate corrective dosing","Yes","WEAN United Process Norms","Tin Plating"),
                (16,"Sn++ : Free Acid Ratio","Ratio",1.95,2.05,"Calculated from lab results","Calculated from lab results","Adjust Sn / acid – SOP PLT-04","Correct ratio – SOP PLT-04","<1.90",">2.10","Dull band on strip","Product downgrade due to surface defect","Ratio monitoring via lab test","Immediate chemistry correction","Yes","WEAN United Process Norms","Tin Plating"),
                (17,"Sulphate (SO₄²⁻) Concentration","g/L","—",12,"Lab test report","Lab test report","Monitor sulphate level – SOP PLT-05","Bleed & make-up – SOP PLT-05","—",">15","No immediate consequence","Dull band formation","Lab testing every shift","Bath correction based on test","Yes","WEAN United Process Norms","Tin Plating"),
                (18,"Total Iron Concentration","g/L","—",20,"Lab test report","Lab test report","Monitor iron content – SOP PLT-06","Bath treatment – SOP PLT-06","—",">25","Healthy solution (no effect)","Deterioration of plating chemistry","Regular lab monitoring","Corrective treatment based on result","Yes","WEAN United Process Norms","Tin Plating"),
                (19,"Stannous to Free Acid Ratio (PSA)","g/L","—",3,"Lab test report","Lab test report","Monitor PSA ratio – SOP PLT-07","Chemistry correction – SOP PLT-07","—",">3","Poor surface finish","Product downgrade due to surface defect","Shift-wise lab testing","Immediate corrective action","Yes","WEAN United Process Norms","Tin Plating"),
                (20,"Reflow Current","A",1000,10000,"PLC / HMI current display","PLC / HMI current display","Adjust line speed – SOP RFL-01","Reduce current or stop line – SOP RFL-01",1000,10000,"Tin melting will not take place causing surface defect","Burning of strip leading to strip breakage and conductor roll damage","Auto control through line speed and tin melting temperature feedback","Auto interlock through reflow temperature feedback","Yes","WEAN United User Manual","Reflow Furnace"),
                (21,"Quench Temperature","°C",50,65,"Temperature sensor on HMI","Temperature sensor on HMI","Adjust ICW inlet valve – SOP QCH-01","Adjust ICW flow – SOP QCH-01",50,65,"Product degradation due to cold quench strain","Product degradation due to hot quench strain","Auto control through ICW inlet control valve","Temperature feedback control through PLC","Yes","WEAN United User Manual","Reflow Furnace"),
                (22,"Strip Temperature (Reflow Exit)","°C",232,270,"Strip pyrometer reading","Strip pyrometer reading","Adjust line speed / furnace power – SOP RFL-02","Reduce power or stop line – SOP RFL-02",232,270,"Tin melting will not take place causing surface defect","Burning of strip leading to strip breakage and conductor roll damage","Auto control via line speed and melting temperature feedback","Pyrometer-based interlock and alarm","Yes","WEAN United User Manual","Reflow Furnace"),
                (23,"Chemical Treatment Solution Concentration","°C",80,90,"Temperature indication on HMI","Temperature indication on HMI","Monitor solution heating – SOP CHT-01","Adjust steam flow – SOP CHT-01",80,90,"Improper cleaning of strip causing patch marks","Burning marks leading to matted strip surface","Steam flow regulated through control valve","Temperature monitoring with alarm","Yes","WEAN United Process Norms","Chemical Treatment"),
                (24,"Chemical Treatment Solution Temperature","°C",40,45,"Temperature indicator / HMI","Temperature indicator / HMI","Monitor bath temperature – SOP CHT-02","Adjust heating – SOP CHT-02",40,45,"Less chromium coating on strip causing patch marks","Less chromium coating causing surface defects","Shift-wise lab testing","Immediate action after lab feedback","Yes","WEAN United Process Norms","Chemical Treatment"),
                (25,"Chemical Treatment Current","A",300,2000,"PLC / HMI current display","PLC / HMI current display","Adjust line speed – SOP CHT-03","Adjust current via PLC – SOP CHT-03",300,3500,"Insufficient chromium coating causing patch marks","Insufficient chromium layer leading to defects","Auto control based on line speed, strip width & thickness","PLC-based current limitation","Yes","WEAN United Process Norms","Chemical Treatment"),
                (26,"Compressed Air Flow to Trion Oiler (Primary Air)","kg/cm²",0.5,1,"Digital pressure display","Digital pressure display","Adjust air regulator – SOP OIL-01","Correct air supply – SOP OIL-01",0.5,1,"Non-uniform oil coating due to improper DOS atomization","Excess oil coating causing smudge band and slippage at Bridle-3","Manual control with digital display","Manual air pressure regulation","Yes","Trion Inc., USA User Manual","Electrostatic Oiling"),
                (27,"Air Flow to Trion Oiler (Secondary Air)","mm WC",60,300,"Air flow indicator","Air flow indicator","Adjust air flow via PLC – SOP OIL-02","Control air flow via line speed feedback – SOP OIL-02",60,300,"Non-uniform oil coating due to low secondary air","Excess air flow causing oil loss and coating non-uniformity","Auto control through line speed feedback","Auto control through line speed feedback","Yes","Trion Inc., USA User Manual","Electrostatic Oiling"),
                (28,"Repelling Plate Voltage","kV",-10,-40,"Voltage controller display","Voltage controller display","Adjust voltage based on QA feedback – SOP OIL-03","Rectify voltage to avoid excess coating – SOP OIL-03",-10,-50,"Low DOS coating and oil loss","Excess coating causing smudge band and slippage at Bridle-3","Manual adjustment based on QA feedback","Manual adjustment based on QA feedback","Yes","Trion Inc., USA User Manual","Electrostatic Oiling"),
            ]

            # Sub-process grouping colors
            SP_CLR = {"Coil Feeding":"#6366f1","Cleaning & Rinsing":"#3b82f6","Tin Plating":"#22c55e","Reflow Furnace":"#ef4444","Chemical Treatment":"#f97316","Electrostatic Oiling":"#a78bfa"}

            # Build multi-header table matching exact Excel layout
            pdb_tbl = '<div style="overflow-x:auto;border:1px solid #1e3a5f;border-radius:10px"><table style="border-collapse:collapse;width:100%;font-size:.68rem">'
            pdb_tbl += '<thead>'
            # Row 1: column groups
            pdb_tbl += '<tr style="background:#06111f">'
            pdb_tbl += '<th rowspan="3" style="padding:8px 8px;text-align:center;color:#64748b;font-size:.58rem;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap">Sl.<br>No.</th>'
            pdb_tbl += '<th rowspan="3" style="padding:8px 10px;text-align:left;color:#e2e8f0;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;min-width:180px">Parameter</th>'
            pdb_tbl += '<th rowspan="3" style="padding:8px 6px;text-align:center;color:#64748b;font-size:.58rem;font-weight:700;border:1px solid #1e3a5f">UoM</th>'
            pdb_tbl += '<th colspan="2" style="padding:6px;text-align:center;color:#22c55e;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(34,197,94,.08)">Standard Operating Condition (SOC)</th>'
            pdb_tbl += '<th colspan="4" style="padding:6px;text-align:center;color:#3b82f6;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(59,130,246,.08)">Control Measures to avoid SOC deviation</th>'
            pdb_tbl += '<th colspan="2" style="padding:6px;text-align:center;color:#f97316;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(249,115,22,.08)">Safe Operating Limit (SOL)</th>'
            pdb_tbl += '<th colspan="2" style="padding:6px;text-align:center;color:#ef4444;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(239,68,68,.08)">Consequence of Deviation (SOL)</th>'
            pdb_tbl += '<th colspan="2" style="padding:6px;text-align:center;color:#a78bfa;font-size:.6rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(167,139,250,.08)">Control/Measures to avoid SOL deviation (Existing Barrier)</th>'
            pdb_tbl += '<th rowspan="3" style="padding:8px 6px;text-align:center;color:#fca5a5;font-size:.58rem;font-weight:700;border:1px solid #1e3a5f;background:rgba(239,68,68,.08);min-width:55px">PSM Critical</th>'
            pdb_tbl += '<th rowspan="3" style="padding:8px 6px;text-align:center;color:#64748b;font-size:.58rem;font-weight:700;border:1px solid #1e3a5f;min-width:100px">References</th>'
            pdb_tbl += '</tr>'
            # Row 2: sub-columns
            pdb_tbl += '<tr style="background:#06111f">'
            for lbl, clr in [("Min","#22c55e"),("Max","#22c55e"),("Identification (Min)","#3b82f6"),("Identification (Max)","#3b82f6"),("Action (Min) / SOP","#3b82f6"),("Action (Max) / SOP","#3b82f6"),("Min","#f97316"),("Max","#f97316"),("Below SOL (Min)","#ef4444"),("Above SOL (Max)","#ef4444"),("Barrier (Min)","#a78bfa"),("Barrier (Max)","#a78bfa")]:
                pdb_tbl += f'<th style="padding:6px 7px;text-align:center;color:{clr};font-size:.55rem;font-weight:700;border:1px solid #1e3a5f;white-space:nowrap;opacity:.85">{lbl}</th>'
            pdb_tbl += '</tr></thead><tbody>'

            cur_sp = None
            for row in PDB_EXCEL:
                sl,param,uom,soc_min,soc_max,id_min,id_max,act_min,act_max,sol_min,sol_max,cons_min,cons_max,bar_min,bar_max,psm,ref,sp = row
                sp_clr = SP_CLR.get(sp,"#64748b")
                if sp != cur_sp:
                    cur_sp = sp
                    pdb_tbl += f'<tr><td colspan="17" style="padding:5px 10px;background:{sp_clr}18;border:1px solid {sp_clr}40;font-size:.6rem;font-weight:800;letter-spacing:1.5px;color:{sp_clr}">{sp.upper()}</td></tr>'
                psm_bg = "rgba(239,68,68,.15)" if psm=="Yes" else "#0d1f35"
                psm_c2 = "#f87171" if psm=="Yes" else "#475569"
                pdb_tbl += f'<tr style="border-bottom:1px solid #1e3a5f">'
                pdb_tbl += f'<td style="padding:6px 8px;text-align:center;color:#f97316;font-family:monospace;font-weight:700;border:1px solid #1e3a5f">{sl}</td>'
                pdb_tbl += f'<td style="padding:6px 8px;color:#e2e8f0;font-weight:600;border:1px solid #1e3a5f">{param}</td>'
                pdb_tbl += f'<td style="padding:6px 6px;text-align:center;color:#64748b;font-family:monospace;font-size:.65rem;border:1px solid #1e3a5f;white-space:nowrap">{uom}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;text-align:center;color:#22c55e;font-family:monospace;font-weight:700;background:rgba(34,197,94,.06);border:1px solid #1e3a5f">{soc_min}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;text-align:center;color:#22c55e;font-family:monospace;font-weight:700;background:rgba(34,197,94,.06);border:1px solid #1e3a5f">{soc_max}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#60a5fa;font-size:.65rem;border:1px solid #1e3a5f;min-width:120px">{id_min}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#60a5fa;font-size:.65rem;border:1px solid #1e3a5f;min-width:120px">{id_max}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#93c5fd;font-size:.64rem;border:1px solid #1e3a5f;min-width:150px">{act_min}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#93c5fd;font-size:.64rem;border:1px solid #1e3a5f;min-width:150px">{act_max}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;text-align:center;color:#f97316;font-family:monospace;font-weight:700;background:rgba(249,115,22,.06);border:1px solid #1e3a5f">{sol_min}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;text-align:center;color:#f97316;font-family:monospace;font-weight:700;background:rgba(249,115,22,.06);border:1px solid #1e3a5f">{sol_max}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#fca5a5;font-size:.64rem;border:1px solid #1e3a5f;min-width:140px">{cons_min}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#fca5a5;font-size:.64rem;border:1px solid #1e3a5f;min-width:140px">{cons_max}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#c4b5fd;font-size:.64rem;border:1px solid #1e3a5f;min-width:140px">{bar_min}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#c4b5fd;font-size:.64rem;border:1px solid #1e3a5f;min-width:140px">{bar_max}</td>'
                pdb_tbl += f'<td style="padding:6px 7px;text-align:center;background:{psm_bg};border:1px solid #1e3a5f"><span style="color:{psm_c2};font-weight:800;font-size:.65rem">{psm}</span></td>'
                pdb_tbl += f'<td style="padding:6px 7px;color:#475569;font-size:.62rem;border:1px solid #1e3a5f;white-space:nowrap">{ref}</td>'
                pdb_tbl += '</tr>'
            pdb_tbl += '</tbody></table></div>'
            st.markdown(pdb_tbl, unsafe_allow_html=True)
            st.markdown('<div style="font-size:.62rem;color:#475569;margin-bottom:1.2rem;font-family:monospace">Source: Form No. PSM/PSI/PDB/001 Rev.06 Eff.Dt.:18.08.2023 &nbsp;·&nbsp; ETL-1 Electrolytic Tin Plating Line 1 &nbsp;·&nbsp; All limits per WEAN United / Supplier Manuals &nbsp;·&nbsp; PSM Critical items tagged in SAP-PM</div>', unsafe_allow_html=True)

            # Layers of Protection context
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem"> <div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">LAYERS OF PROTECTION  -  How SOC and SOL fit in the protection model</div> <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:6px;font-size:.7rem"> <div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#22c55e">Layer 1-2</b><br><span style="color:#64748b">Process Design + BPCS control<br>-&gt; keeps within SOC</span></div> <div style="background:rgba(234,179,8,.1);border:1px solid rgba(234,179,8,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#eab308">Layer 3</b><br><span style="color:#64748b">Critical Alarms + Operator action<br>-&gt; SOC deviation detected</span></div> <div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#f97316">Layer 4-5</b><br><span style="color:#64748b">SIS auto-trip + PRV/SRV<br>-&gt; SOL breach response</span></div> <div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#ef4444">Layer 6-8</b><br><span style="color:#64748b">Bund -&gt; Plant ER -&gt; Community ER<br>-&gt; post-LOC mitigation</span></div> </div> <div style="font-size:.7rem;color:#475569;margin-top:.5rem">SOC = Layers 1-3 keep process here (prevention) &nbsp;|&nbsp; SOL breach = Layer 4 auto-trip activates (last prevention barrier) &nbsp;|&nbsp; Beyond SOL = mitigation layers activate</div> </div>""", unsafe_allow_html=True)

            pdb_data = ETL1_PDB_PARAMS
            if profile and profile.get("pdb_params"):
                pdb_data = profile["pdb_params"]
            dept = plant.replace(" ","_").replace(" - ","").replace("/","")[:8].lower()
            render_pdb(pdb_data, dept_key=dept)

        # ── PSCE ─────────────────────────────────────────────────────

            render_qa_bot("g_pdb")
        with tabs[5]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/PSCE/001 Rev.04 Eff.Dt.:18.08.2023  -  ETL-1 Electrolytic Tinning Line 1, Tata Steel Tinplate (TCIL), Golmuri. 77 PSCE items identified.</p>', unsafe_allow_html=True)
            render_glossary()

            # ── PSCE - EXACT EXCEL TABLE, ALL 77 ITEMS (TOP) ──────────────
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">PSCE - ALL 77 ITEMS (as per PSI PSCE Sheet, Form No. PSM/PSI/EDB/002)</div>', unsafe_allow_html=True)
            psce_excel_hdr = ["Sl.","Equipment","Consequence Based","Prevention & Mitigation","Prescriptive","PSCE","Justification for Process Safety"]
            psce_excel_tbl = '<div style="overflow-x:auto;max-height:480px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px"><table style="border-collapse:collapse;width:100%;font-size:.7rem"><thead><tr style="background:#080d18">'
            for h in psce_excel_hdr:
                psce_excel_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.58rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#080d18">{h}</th>'
            psce_excel_tbl += '</tr></thead><tbody>'
            for r in ETL1_PSCE_EXCEL:
                sl, eq, cons, prev, presc, p, just = r
                cons_c = "#ef4444" if cons == "Yes" else "#475569"
                prev_c = "#3b82f6" if prev == "Yes" else "#475569"
                presc_c = "#a78bfa" if presc == "Yes" else "#475569"
                p_c = "#22c55e" if p == "Yes" else "#475569"
                psce_excel_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:600;white-space:nowrap">{eq}</td><td style="padding:6px 9px;text-align:center;color:{cons_c};font-weight:700">{cons}</td><td style="padding:6px 9px;text-align:center;color:{prev_c};font-weight:700">{prev}</td><td style="padding:6px 9px;text-align:center;color:{presc_c};font-weight:700">{presc}</td><td style="padding:6px 9px;text-align:center;color:{p_c};font-weight:700">{p}</td><td style="padding:6px 9px;color:#94a3b8;min-width:240px">{just}</td></tr>'
            psce_excel_tbl += '</tbody></table></div>'
            st.markdown(psce_excel_tbl, unsafe_allow_html=True)
            st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)



            st.markdown("""<div style="background:rgba(59,130,246,.08);border:1px solid rgba(59,130,246,.25);border-radius:10px;padding:1rem 1.4rem;margin-bottom:1rem"> <div style="font-size:.82rem;font-weight:700;color:#3b82f6;margin-bottom:.6rem">PSCE FRAMEWORK  -  ETL-1 ELECTROLYTIC TINNING LINE</div> <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:.8rem;font-size:.75rem;color:#94a3b8;line-height:1.7"> <div><b style="color:#ef4444">Consequence Based PSRM Critical</b><br>Equipment whose failure could DIRECTLY CAUSE a major process safety incident  -  fire, explosion, toxic release, or environmental damage meeting HHO criteria.</div> <div><b style="color:#a78bfa">Prevention &amp; Mitigation</b><br>Equipment specifically installed to PREVENT a major accident or LIMIT its consequences. Includes SIS interlocks, safety instrumented systems, and emergency shutdown devices.</div> <div><b style="color:#f97316">Prescriptive PSM Critical</b><br>Equipment mandated by REGULATION regardless of consequence analysis  -  IBR statutory SRVs, PESO requirements, CPCB mandated monitoring (e.g. Cr-VI air monitor). Statutory requirement.</div> </div></div>""", unsafe_allow_html=True)

            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:8px;padding:.8rem 1.2rem;margin-bottom:1rem"> <div style="font-size:.72rem;font-weight:700;color:#64748b;letter-spacing:1px;margin-bottom:.5rem">BASIS OF SELECTION  -  CATEGORY DEFINITIONS (Note #1, EDB Format)</div> <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.5rem;font-size:.72rem"> <div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#3b82f6">Instrumented Active Preventive</b><br><span style="color:#64748b">SIS/interlock devices that automatically detect and prevent escalation  -  analysers with auto-trip, transmitters with PLC shutdown logic.</span></div> <div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#f97316">Active Mitigation</b><br><span style="color:#64748b">Mitigation requiring automatic activation or human action AFTER a deviation begins  -  exhaust fans, monitoring gauges, operator-activated systems.</span></div> <div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#22c55e">Passive Prevention</b><br><span style="color:#64748b">Always-active protection requiring no energy or human action  -  bunds, blast panels, physical barriers, containment.</span></div> <div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#ef4444">Safety Monitoring &amp; Emergency Comms</b><br><span style="color:#64748b">Detection and communication systems  -  Cr-VI monitors, H2 detectors, emergency PA systems, alarm panels.</span></div> <div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#a78bfa">Controlled Release</b><br><span style="color:#64748b">Equipment for safe controlled release  -  SRVs, PRVs, auto-vent valves. Prevents uncontrolled/catastrophic release.</span></div> <div style="background:#080d18;border-radius:6px;padding:.6rem"><b style="color:#94a3b8">Service &amp; Utility</b><br><span style="color:#64748b">Support systems whose failure impacts safety chain  -  cooling water, DM water, hydraulic systems. Consequence-based selection.</span></div> </div></div>""", unsafe_allow_html=True)

            st.markdown("""<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:1rem"> <div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:8px;padding:.7rem;text-align:center"> <div style="font-size:1.4rem;font-weight:900;color:#ef4444;font-family:monospace">77</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">TOTAL PSCE ITEMS</div></div> <div style="background:#0d1f35;border:1px solid rgba(59,130,246,.3);border-top:3px solid #3b82f6;border-radius:8px;padding:.7rem;text-align:center"> <div style="font-size:1.4rem;font-weight:900;color:#3b82f6;font-family:monospace">4</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">HHO PROCESSES</div></div> <div style="background:#0d1f35;border:1px solid rgba(249,115,22,.3);border-top:3px solid #f97316;border-radius:8px;padding:.7rem;text-align:center"> <div style="font-size:1.4rem;font-weight:900;color:#f97316;font-family:monospace">2</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">PRESCRIPTIVE</div></div> <div style="background:#0d1f35;border:1px solid rgba(239,68,68,.3);border-top:3px solid #ef4444;border-radius:8px;padding:.7rem;text-align:center"> <div style="font-size:1.4rem;font-weight:900;color:#ef4444;font-family:monospace">1</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">Cr-VI MONITOR (MANDATORY)</div></div> <div style="background:#0d1f35;border:1px solid rgba(34,197,94,.3);border-top:3px solid #22c55e;border-radius:8px;padding:.7rem;text-align:center"> <div style="font-size:1.4rem;font-weight:900;color:#22c55e;font-family:monospace">SAP-S</div><div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#475569">TAG ALL ITEMS</div></div> </div>""", unsafe_allow_html=True)


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

            st.markdown(f'<div style="font-size:.72rem;color:#475569;margin-bottom:.5rem">Showing {len(shown_etl)} items  -  Full 77-item list in SAP-PM module</div>', unsafe_allow_html=True)

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
    <div style="font-size:.72rem;color:#f97316;font-family:monospace">{item.get('tag',' - ')}</div>
    <div style="font-size:.62rem;color:#475569">{item.get('sap_tag',' - ')}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">SUB-PROCESS</div>
    <div style="font-size:.72rem;color:#94a3b8">{item.get('sub_process',' - ')}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">CATEGORY</div>
    <div style="font-size:.68rem;color:#94a3b8">{item.get('category', item.get('psce_type',''))}</div>
  </div>
  <div style="background:#080d18;border-radius:6px;padding:.5rem">
    <div style="font-size:.55rem;color:#475569;font-weight:700;letter-spacing:1px;margin-bottom:2px">MAINTENANCE</div>
    <div style="font-size:.68rem;color:#94a3b8">{item.get('maintenance',' - ')}</div>
  </div>
</div>
<div style="background:#0a1628;border:1px solid #1e3a5f;border-radius:8px;padding:.7rem;margin-bottom:.5rem">
  <div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#3b82f6;margin-bottom:3px">JUSTIFICATION FOR PROCESS SAFETY CRITICALITY</div>
  <div style="font-size:.75rem;color:#94a3b8;line-height:1.7">{item.get('justification',' - ')}</div>
</div>
<div style="background:rgba(239,68,68,.05);border:1px solid rgba(239,68,68,.15);border-left:3px solid #ef4444;border-radius:6px;padding:.6rem .8rem">
  <div style="font-size:.58rem;font-weight:700;letter-spacing:1px;color:#ef4444;margin-bottom:2px">CONSEQUENCE OF FAILURE</div>
  <div style="font-size:.73rem;color:#fca5a5">{item.get('consequence_of_failure',' - ')}</div>
</div>
</div>""", unsafe_allow_html=True)

        # ── EDB ──────────────────────────────────────────────────────

            render_qa_bot("g_psce")
        with tabs[6]:
            st.markdown('<p style="font-size:.75rem;color:#64748b">Form No.: PSM/PSI/EDB/001 Rev.04 Eff.Dt.:01.05.2018  -  ETL-1 Equipment Design Basis</p>', unsafe_allow_html=True)
            render_glossary()

            # ── EDB - EXACT EXCEL TABLE, ALL 77 ITEMS (TOP) ──────────────
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">EDB - EQUIPMENT DESIGN BASIS, ALL 77 ITEMS (as per PSI EDB Sheet, Form No. PSM/PSI/EDB/001)</div>', unsafe_allow_html=True)
            edb_excel_hdr = ["Sl.","Sub-Process / Sub-System","Hazardous Substance","Equipment","PSCE","Equipment No. (Tag)","SAP ID","Basis of Selection","Maint. / Calib. Schedule","Manufacturer","Model / Type","Reference Docs","Location of Docs","Remark"]
            edb_excel_tbl = '<div style="overflow-x:auto;max-height:480px;overflow-y:auto;border:1px solid #1e3a5f;border-radius:8px"><table style="border-collapse:collapse;width:100%;font-size:.68rem"><thead><tr style="background:#080d18">'
            for h in edb_excel_hdr:
                edb_excel_tbl += f'<th style="padding:6px 8px;text-align:left;color:#64748b;font-size:.56rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap;position:sticky;top:0;background:#080d18">{h}</th>'
            edb_excel_tbl += '</tr></thead><tbody>'
            for r in ETL1_EDB_EXCEL:
                sl, sub, haz, p, eqno, sap, basis, maint, mfr, model, refdoc, loc, rem = r
                p_c = "#22c55e" if p == "Yes" else "#475569"
                # Equipment name = Model column (col 9)
                equip_name = model
                edb_excel_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 8px;color:#f97316;font-family:monospace;font-weight:700">{sl}</td><td style="padding:6px 8px;color:#e2e8f0;font-weight:600;white-space:nowrap">{sub}</td><td style="padding:6px 8px;color:#94a3b8;white-space:nowrap">{haz}</td><td style="padding:6px 8px;color:#e2e8f0;font-weight:600;white-space:nowrap">{equip_name}</td><td style="padding:6px 8px;text-align:center;color:{p_c};font-weight:700">{p}</td><td style="padding:6px 8px;color:#f97316;font-family:monospace;white-space:nowrap">{eqno}</td><td style="padding:6px 8px;color:#3b82f6;font-family:monospace;font-size:.62rem;white-space:nowrap">{sap}</td><td style="padding:6px 8px;color:#94a3b8;min-width:220px">{basis}</td><td style="padding:6px 8px;color:#64748b;white-space:nowrap">{maint}</td><td style="padding:6px 8px;color:#94a3b8;white-space:nowrap">{mfr}</td><td style="padding:6px 8px;color:#64748b;white-space:nowrap">{model}</td><td style="padding:6px 8px;color:#475569;white-space:nowrap">{refdoc}</td><td style="padding:6px 8px;color:#475569;white-space:nowrap">{loc}</td><td style="padding:6px 8px;color:#475569;white-space:nowrap">{rem}</td></tr>'
            edb_excel_tbl += '</tbody></table></div>'
            st.markdown(edb_excel_tbl, unsafe_allow_html=True)
            st.markdown('<div style="height:1.2rem"></div>', unsafe_allow_html=True)



            # Barrier model from Tata Steel PSRM module
            st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:10px;padding:.8rem 1.2rem;margin-bottom:1rem"> <div style="font-size:.72rem;font-weight:700;color:#3b82f6;letter-spacing:1px;margin-bottom:.5rem">BARRIER MODEL  -  Tata Steel PSRM: Detector + Logic Solver + Actuator = ONE Barrier</div> <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:6px;font-size:.7rem;margin-bottom:.5rem"> <div style="background:rgba(59,130,246,.1);border:1px solid rgba(59,130,246,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#3b82f6">① DETECTOR</b><br><span style="color:#64748b">Sensor detects condition requiring action<br>(analyser, transmitter, detector)</span></div> <div style="background:rgba(249,115,22,.1);border:1px solid rgba(249,115,22,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#f97316">② LOGIC SOLVER</b><br><span style="color:#64748b">Decides action to take<br>(PLC, relay, operator knowledge)</span></div> <div style="background:rgba(34,197,94,.1);border:1px solid rgba(34,197,94,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#22c55e">③ ACTUATOR</b><br><span style="color:#64748b">Takes physical action<br>(valve, trip, shutdown, operator)</span></div> <div style="background:rgba(167,139,250,.1);border:1px solid rgba(167,139,250,.2);border-radius:6px;padding:.5rem;text-align:center"><b style="color:#a78bfa">BARRIER TYPE</b><br><span style="color:#64748b">Active (auto) | Passive (always-on) | Procedural (operator)</span></div> </div> <div style="font-size:.7rem;color:#475569">A barrier is effective ONLY if all 3 components are fully functional. Each EDB item below is one such barrier component or a complete barrier in the protection chain.</div> </div>""", unsafe_allow_html=True)

            edb_data = ETL1_EDB
            if profile and profile.get("edb_items"):
                edb_data = profile["edb_items"]
            dept_e = plant.replace(" ","_").replace(" - ","").replace("/","")[:8].lower()
            render_edb(edb_data, dept_key=dept_e)

        # ── PARAMETERS ───────────────────────────────────────────────

            render_global_incidents(["H2SO4","Cr-VI","Phenol","DOS","ENSA"])
            render_qa_bot("g_edb")
        with tabs[7]:
            st.markdown('<div class="sl-sec">Process Design Basis  -  All Parameters with SOC / SOL Limits & Breach Consequences</div>', unsafe_allow_html=True)
            render_glossary()

            # Full parameter data with consequences
            PARAMS_FULL = {
                "Coil Feeding": [
                    {"param":"Power Pack Hydraulic Pump Pressure","uom":"bar","soc_min":55,"soc_max":70,"sol_min":45,"sol_max":100,
                     "low_breach":"Hydraulic pressure loss  -  actuator failure, strip misalignment, entry section damage",
                     "high_breach":"Over-pressure  -  hydraulic line rupture, oil spill, fire risk (oil flash point ~150 C)"},
                    {"param":"DM Water Pressure to Welding Machine","uom":"kg/cm2","soc_min":4.5,"soc_max":5.5,"sol_min":4.5,"sol_max":5.5,
                     "low_breach":"Welder cooling loss  -  welder overheating, weld failure, strip break",
                     "high_breach":"Excess pressure  -  welder cooling circuit damage"},
                    {"param":"Compressed Air Pressure to Welding Machine","uom":"kg/cm2","soc_min":4.5,"soc_max":5.5,"sol_min":4.5,"sol_max":6.5,
                     "low_breach":"Pneumatic actuator failure  -  welder clamp fails, strip break",
                     "high_breach":"Excess pressure  -  pneumatic line damage"},
                ],
                "Cleaning & Rinsing": [
                    {"param":"Pre-Primary Alkali Temperature (NaOH)","uom":"deg C","soc_min":80,"soc_max":90,"sol_min":80,"sol_max":90,
                     "low_breach":"Poor cleaning  -  oil and grease residue on strip, plating adhesion failure, product rejection",
                     "high_breach":"NaOH boiling  -  violent steam generation, alkali splash, severe chemical burns, HHO event"},
                    {"param":"Primary NaOH Concentration","uom":"g/L","soc_min":25,"soc_max":30,"sol_min":25,"sol_max":30,
                     "low_breach":"Insufficient cleaning  -  residual oil causes plating pinholes",
                     "high_breach":"Excess alkali  -  increased drag-out, waste treatment overload"},
                    {"param":"Primary Cleaning Current","uom":"kA","soc_min":2.5,"soc_max":3.5,"sol_min":2.5,"sol_max":3.5,
                     "low_breach":"Inadequate electrolytic cleaning  -  contamination passes to plating section",
                     "high_breach":"Excessive current  -  strip overheating, electrical cell damage, arc risk"},
                    {"param":"Pickling H2SO4 Concentration","uom":"g/L","soc_min":8,"soc_max":10,"sol_min":8,"sol_max":10,
                     "low_breach":"Insufficient pickling  -  oxide layer on strip, poor plating adhesion, product downgrade",
                     "high_breach":"Excess acid  -  over-pickling, strip surface pitting, H2 gas generation, equipment corrosion"},
                ],
                "Tin Plating": [
                    {"param":"Sn++ Concentration (SnSO4)","uom":"g/L","soc_min":26,"soc_max":32,"sol_min":24,"sol_max":34,
                     "low_breach":"Under-plating  -  dull band formation, coating weight below spec, PRODUCT REJECTION",
                     "high_breach":"Over-plating  -  excess tin consumption, cost loss, coatweight above spec"},
                    {"param":"Free Acid Concentration","uom":"g/L","soc_min":13,"soc_max":16,"sol_min":11,"sol_max":18,
                     "low_breach":"Low conductivity  -  poor current distribution, uneven plating",
                     "high_breach":"Excess acid  -  increased corrosivity, operator exposure risk, equipment damage"},
                    {"param":"ENSA Concentration","uom":"g/L","soc_min":3,"soc_max":6,"sol_min":2,"sol_max":7,
                     "low_breach":"Poor plating efficiency  -  rough deposit, dull appearance",
                     "high_breach":"Excess brightener  -  plating bath contamination, breakdown products accumulate"},
                    {"param":"Sn++ : Free Acid Ratio","uom":"Ratio","soc_min":1.95,"soc_max":2.05,"sol_min":1.9,"sol_max":2.1,
                     "low_breach":"Poor bath balance  -  rough plating, increased sludge formation",
                     "high_breach":"Ratio shift  -  non-uniform tin deposition, product specification failure"},
                ],
                "Reflow Furnace": [
                    {"param":"Strip Temperature (Reflow Exit)","uom":"deg C","soc_min":232,"soc_max":270,"sol_min":232,"sol_max":270,
                     "low_breach":"Incomplete tin melting  -  matte/dull finish, poor corrosion resistance, product rejection",
                     "high_breach":"CRITICAL: Strip burning  -  conductor roll damage, unplanned shutdown, major production loss"},
                    {"param":"Quench Temperature","uom":"deg C","soc_min":50,"soc_max":65,"sol_min":50,"sol_max":65,
                     "low_breach":"Cold quench  -  thermal shock, strip shape defects",
                     "high_breach":"Hot quench  -  incomplete solidification of tin, alloy layer overgrowth"},
                    {"param":"Reflow Current","uom":"A","soc_min":1000,"soc_max":10000,"sol_min":1000,"sol_max":10000,
                     "low_breach":"Insufficient heating  -  incomplete tin melting, dull coating",
                     "high_breach":"Excess current  -  strip overheating, conductor roll arcing, fire risk"},
                ],
                "Chemical Treatment": [
                    {"param":"Chemical Treatment Solution Temperature","uom":"deg C","soc_min":40,"soc_max":45,"sol_min":40,"sol_max":45,
                     "low_breach":"Incomplete passivation  -  poor corrosion resistance, product failure in service",
                     "high_breach":"CRITICAL: Bath overheating  -  increased Cr-VI volatilisation, TLV breach, MANDATORY SHUTDOWN"},
                    {"param":"Chemical Treatment Current","uom":"A","soc_min":300,"soc_max":2000,"sol_min":300,"sol_max":3500,
                     "low_breach":"Insufficient passivation layer  -  corrosion failure, food can safety risk",
                     "high_breach":"Excess current  -  Cr-VI reduction to Cr-III, bath balance upset, passivation failure"},
                ],
                "Electrostatic Oiling": [
                    {"param":"Primary Air Pressure","uom":"kg/cm2","soc_min":0.5,"soc_max":1.0,"sol_min":0.5,"sol_max":1.0,
                     "low_breach":"Poor atomisation  -  uneven oil distribution, surface corrosion in storage",
                     "high_breach":"Excess air  -  oil mist generation, fire risk near electrostatic system"},
                    {"param":"Secondary Air Flow","uom":"mm WC","soc_min":60,"soc_max":300,"sol_min":60,"sol_max":300,
                     "low_breach":"Insufficient air  -  oil accumulation, drip marks on strip",
                     "high_breach":"Excess air  -  oil mist carry-over, contamination of downstream coiler"},
                    {"param":"Repelling Plate Voltage","uom":"kV","soc_min":-40,"soc_max":-10,"sol_min":-50,"sol_max":-10,
                     "low_breach":"Poor oil distribution  -  non-uniform coating weight",
                     "high_breach":"Excess voltage  -  arcing to strip, electrical hazard, strip marking"},
                ],
            }

            # ── Excel-format summary table at top - all parameters across sub-processes ──
            st.markdown('<div style="font-size:.68rem;font-weight:700;letter-spacing:1.5px;color:#3b82f6;margin-bottom:.4rem">PROCESS PARAMETERS - ALL SOC / SOL LIMITS (as per PSI PDB Sheet, Form No. PSM/PSI/PDB/001)</div>', unsafe_allow_html=True)
            params_tbl = '<div style="overflow-x:auto"><table style="border-collapse:collapse;width:100%;font-size:.72rem"><thead><tr style="background:#080d18">'
            for h in ["Sl.","Sub-Process","Parameter","UoM","SOC Min","SOC Max","SOL Min","SOL Max"]:
                params_tbl += f'<th style="padding:6px 9px;text-align:left;color:#64748b;font-size:.6rem;font-weight:700;letter-spacing:1px;border-bottom:1px solid #1e3a5f;white-space:nowrap">{h}</th>'
            params_tbl += '</tr></thead><tbody>'
            _sl = 0
            for proc_name, params in PARAMS_FULL.items():
                for p in params:
                    _sl += 1
                    params_tbl += f'<tr style="border-bottom:1px solid #1e3a5f"><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{_sl}</td><td style="padding:6px 9px;color:#94a3b8;white-space:nowrap">{proc_name}</td><td style="padding:6px 9px;color:#e2e8f0;font-weight:600">{p["param"]}</td><td style="padding:6px 9px;color:#64748b;font-family:monospace">{p["uom"]}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{p["soc_min"]}</td><td style="padding:6px 9px;color:#22c55e;font-family:monospace;font-weight:700">{p["soc_max"]}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace">{p["sol_min"]}</td><td style="padding:6px 9px;color:#f97316;font-family:monospace;font-weight:700">{p["sol_max"]}</td></tr>'
            params_tbl += '</tbody></table></div>'
            st.markdown(params_tbl, unsafe_allow_html=True)

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
                    with st.expander(f"{pparam}   -   SOC: {psmin} to {psmax} {puom}"):
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


            render_qa_bot("g_param")

# ══════════════════════════════════════════════════════════════════════
# HOME PAGE  -  Industry -> Company -> Division/Plant selection
# ══════════════════════════════════════════════════════════════════════

# ══════════════════════════════════════════════════════════════════════
# HOME PAGE
# ══════════════════════════════════════════════════════════════════════
else:
    # ── FRONT PAGE ────────────────────────────────────────────
    IND_META = {
        "Steel & Metal":   {"color":"#f97316","risk":"HIGH",    "incidents":2847,"icon":"S&M","desc":"Integrated steel plants, rolling mills, coating lines and associated utilities."},
        "Pharma":          {"color":"#a78bfa","risk":"MEDIUM",  "incidents":892, "icon":"RX","desc":"API synthesis, formulation, sterile injectables and packaging operations."},
        "Oil & Gas":       {"color":"#ef4444","risk":"CRITICAL","incidents":5621,"icon":"O&G","desc":"Refineries, offshore platforms, pipelines and LPG/propane handling."},
        "Food & Beverage": {"color":"#22c55e","risk":"LOW",     "incidents":341, "icon":"F&B","desc":"Processing, bottling and packaging lines with ammonia refrigeration and CO2 systems."},
        "Chemicals":       {"color":"#06b6d4","risk":"HIGH",    "incidents":3194,"icon":"CHEM","desc":"Chlor-alkali, electrolysis, bulk chemical storage and reaction units."},
    }

    # ── WELCOME HERO ──────────────────────────────────────────
    st.markdown("""
    <div style="background:linear-gradient(135deg,#020818 0%,#0a1628 40%,#0d1f35 70%,#060d1a 100%);
                padding:3rem 2rem 2.5rem;border-bottom:2px solid #1e3a5f;margin:0 -1rem 0 -1rem;
                position:relative;overflow:hidden">
      <div style="position:absolute;top:-60px;right:-60px;width:300px;height:300px;
                  background:radial-gradient(circle,rgba(59,130,246,.08) 0%,transparent 70%);
                  border-radius:50%"></div>
      <div style="position:absolute;bottom:-40px;left:-40px;width:200px;height:200px;
                  background:radial-gradient(circle,rgba(249,115,22,.06) 0%,transparent 70%);
                  border-radius:50%"></div>

      <div style="display:inline-flex;align-items:center;gap:8px;
                  background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.3);
                  border-radius:20px;padding:4px 16px;margin-bottom:1.2rem">
        <div style="width:7px;height:7px;border-radius:50%;background:#22c55e;
                    box-shadow:0 0 10px #22c55e"></div>
        <span style="color:#60a5fa;font-size:.68rem;font-weight:700;letter-spacing:2px">LIVE  ·  PSI/PSM PLATFORM</span>
      </div>

      <div style="font-size:.65rem;font-weight:700;letter-spacing:3px;color:#3b82f6;margin-bottom:.5rem;text-transform:uppercase">Welcome to</div>
      <h1 style="font-size:3rem;font-weight:900;color:#ffffff;letter-spacing:-2px;line-height:1;margin-bottom:.5rem">
        PSI<span style="color:#3b82f6">Pro</span>
        <span style="font-size:1.2rem;font-weight:400;color:#475569;letter-spacing:0;vertical-align:middle;margin-left:.5rem">PSI / PSM Platform</span>
      </h1>
      <div style="font-size:1.05rem;color:#94a3b8;margin-bottom:.4rem;font-weight:500">
        Your one-stop destination for <b style="color:#60a5fa">Process Safety Information</b> — TCIL Golmuri
      </div>
      <div style="font-size:.8rem;color:#475569;margin-bottom:1.4rem;line-height:1.7">
        Tata Steel Tinplate (TCIL) Golmuri · Tata Steel Jamshedpur · JSW Steel · AM/NS India · SAIL<br>
        Real PSI/PSM plant hierarchy · Live risk monitoring · HHO/LHO classification · PSRM framework
      </div>

      <div style="display:flex;gap:10px;flex-wrap:wrap">
        <span style="background:rgba(249,115,22,.15);border:1px solid rgba(249,115,22,.3);
                     color:#f97316;font-size:.68rem;font-weight:700;padding:5px 14px;border-radius:20px">
          PSRM Framework
        </span>
        <span style="background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.3);
                     color:#22c55e;font-size:.68rem;font-weight:700;padding:5px 14px;border-radius:20px">
          Real Excel Data
        </span>
        <span style="background:rgba(167,139,250,.12);border:1px solid rgba(167,139,250,.3);
                     color:#a78bfa;font-size:.68rem;font-weight:700;padding:5px 14px;border-radius:20px">
          HHO / LHO Classification
        </span>
        <span style="background:rgba(59,130,246,.12);border:1px solid rgba(59,130,246,.3);
                     color:#60a5fa;font-size:.68rem;font-weight:700;padding:5px 14px;border-radius:20px">
          HAZOP · Bow Tie · Barriers
        </span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── What's inside strip ───────────────────────────────────
    st.markdown("""
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#1e3a5f;
                border:1px solid #1e3a5f;border-radius:0;margin:0 -1rem 1.5rem -1rem">
      <div style="background:#080d18;padding:1rem 1.4rem;text-align:center">
        <div style="font-size:1.4rem;font-weight:900;color:#f97316;font-family:monospace">5</div>
        <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-top:2px">INDUSTRIES</div>
      </div>
      <div style="background:#080d18;padding:1rem 1.4rem;text-align:center">
        <div style="font-size:1.4rem;font-weight:900;color:#22c55e;font-family:monospace">5</div>
        <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-top:2px">PSI PROFILES LIVE</div>
      </div>
      <div style="background:#080d18;padding:1rem 1.4rem;text-align:center">
        <div style="font-size:1.4rem;font-weight:900;color:#a78bfa;font-family:monospace">9</div>
        <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-top:2px">COMPANIES / SITES</div>
      </div>
      <div style="background:#080d18;padding:1rem 1.4rem;text-align:center">
        <div style="font-size:1.4rem;font-weight:900;color:#3b82f6;font-family:monospace">150+</div>
        <div style="font-size:.55rem;font-weight:700;letter-spacing:1.5px;color:#475569;margin-top:2px">PSCE ITEMS</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── What SafetyLens covers ────────────────────────────────
    st.markdown("""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-radius:12px;
                                padding:1.2rem 1.6rem;margin-bottom:1.5rem">
      <div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                  text-transform:uppercase;margin-bottom:.8rem">What SafetyLens contains for each plant</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:.8rem;font-size:.78rem">
        <div style="color:#94a3b8"><b style="color:#f97316">PSC</b> — Process Safety Classification (HHO/LHO)</div>
        <div style="color:#94a3b8"><b style="color:#f97316">HOM</b> — Hazard of Materials (TLV, LEL, IDLH)</div>
        <div style="color:#94a3b8"><b style="color:#f97316">CIM</b> — Chemical Interaction Matrix</div>
        <div style="color:#94a3b8"><b style="color:#f97316">PDB</b> — Process Design Basis (SOC / SOL limits)</div>
        <div style="color:#94a3b8"><b style="color:#f97316">PSCE</b> — Safety Critical Equipment list</div>
        <div style="color:#94a3b8"><b style="color:#f97316">EDB</b> — Equipment Design Basis (SAP IDs)</div>
        <div style="color:#94a3b8"><b style="color:#22c55e">HAZOP</b> — What-if deviation analysis per process</div>
        <div style="color:#94a3b8"><b style="color:#22c55e">Bow Tie</b> — Causes · Preventions · Mitigations</div>
        <div style="color:#94a3b8"><b style="color:#22c55e">QA Bot</b> — Ask about any PSM term or process</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Live Accident Report  ─────────────────────────────────
    if not st.session_state.ind:
        st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                        text-transform:uppercase;margin:1.5rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
            Live Accident Report  -  Recent Industry Incidents</div>""", unsafe_allow_html=True)
        SEV_COLOR = {"L1":"#22c55e","L2":"#eab308","L3":"#f97316","L4":"#ef4444","L5":"#7f1d1d"}
        SEV_LABEL = {"L1":"L1 - Minor","L2":"L2 - Moderate","L3":"L3 - Serious","L4":"L4 - Critical","L5":"L5 - Catastrophic"}
        for acc in ACCIDENTS:
            sev = acc.get("severity","L2")
            sc = SEV_COLOR.get(sev, "#64748b")
            st.markdown(f"""<div style="background:#0d1f35;border:1px solid #1e3a5f;border-left:4px solid {sc};border-radius:10px;padding:.9rem 1.2rem;margin-bottom:8px">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:10px;flex-wrap:wrap;margin-bottom:.4rem">
                <div>
                  <span style="font-size:.6rem;font-weight:700;letter-spacing:1px;color:#475569;text-transform:uppercase">{acc['industry']} &middot; {acc['plant']} &middot; {acc['year']}</span><br>
                  <span style="font-size:.86rem;font-weight:700;color:#e2e8f0">{acc['incident']}</span>
                </div>
                <span style="background:{sc}20;color:{sc};border:1px solid {sc}50;font-size:.62rem;font-weight:800;padding:3px 10px;border-radius:6px;white-space:nowrap">{SEV_LABEL.get(sev,sev)}</span>
              </div>
              <div style="font-size:.76rem;color:#94a3b8;line-height:1.6"><b style="color:#60a5fa">Lesson Learned:</b> {acc['lesson']}</div>
            </div>""", unsafe_allow_html=True)

    # ── Step 1 — Industry ──
    st.markdown("""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                    text-transform:uppercase;margin:1.5rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
        Step 1 — Select Industry Sector</div>""", unsafe_allow_html=True)

    risk_clr_map = {"CRITICAL":"#ef4444","HIGH":"#f97316","MEDIUM":"#eab308","LOW":"#22c55e"}
    ind_cols = st.columns(len(HIERARCHY))
    for i, ind in enumerate(HIERARCHY.keys()):
        im = IND_META.get(ind, {})
        clr = im.get("color", "#3b82f6")
        n_comp = len(HIERARCHY[ind])
        n_plants = sum(len(p) for d in HIERARCHY[ind].values() for p in d.values())
        risk_level = im.get("risk","")
        risk_clr = risk_clr_map.get(risk_level, "#64748b")
        active = (st.session_state.ind == ind)
        with ind_cols[i]:
            st.markdown(f"""<div style="background:{'rgba(29,78,216,.15)' if active else '#0d1f35'};
                border:1px solid {'#1d4ed8' if active else '#1e3a5f'};
                border-top:3px solid {clr};border-radius:10px;padding:1rem;
                margin-bottom:6px;text-align:center;min-height:148px">
              <div style="display:inline-block;background:{clr}20;color:{clr};border:1px solid {clr}50;font-size:.65rem;font-weight:800;letter-spacing:1px;padding:3px 10px;border-radius:6px;margin-bottom:6px">{im.get('icon','GEN')}</div>
              <div style="font-size:.8rem;font-weight:700;color:{clr};margin-bottom:4px">{ind}</div>
              <div style="font-size:.65rem;color:#475569;margin-bottom:8px">{im.get('incidents',0):,} incidents on file</div>
              <div style="font-size:.7rem;color:{risk_clr};font-weight:700;margin-bottom:4px">{risk_level} RISK</div>
              <div style="font-size:.65rem;color:#64748b">{n_comp} companies &middot; {n_plants} plants</div>
            </div>""", unsafe_allow_html=True)
            if st.button("Select", key=f"ind_{ind}", use_container_width=True,
                         type="primary" if active else "secondary"):
                st.session_state.ind = ind
                st.session_state.comp = None
                st.session_state.plant = None
                st.rerun()

    # ── Steps 2 & 3 — Company then Plant (only when industry selected) ──
    if st.session_state.ind:
        ind_name = st.session_state.ind
        crumb_parts = [f'<span style="color:#3b82f6;font-weight:700">{ind_name}</span>']
        if st.session_state.comp:
            crumb_parts.append(f'<span style="color:#94a3b8">{st.session_state.comp}</span>')
        if st.session_state.plant:
            crumb_parts.append(f'<span style="color:#e2e8f0">{st.session_state.plant}</span>')
        bc1, bc2 = st.columns([5,1])
        with bc1:
            st.markdown(f'<div style="font-size:.72rem;color:#64748b;padding:.4rem 0">{"  ›  ".join(crumb_parts)}</div>', unsafe_allow_html=True)
        with bc2:
            if st.button("◀ Back", key="nav_back", use_container_width=True):
                if st.session_state.plant:
                    st.session_state.plant = None
                elif st.session_state.comp:
                    st.session_state.comp = None
                else:
                    st.session_state.ind = None
                st.rerun()

        st.markdown(f"""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                        text-transform:uppercase;margin:1rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
            Step 2 — Select Company / Site <span style="color:#475569;font-style:italic;letter-spacing:0;text-transform:none;font-weight:400;font-size:.8rem">/ {ind_name}</span></div>""", unsafe_allow_html=True)

        comps = list(HIERARCHY[ind_name].keys())
        for row_start in range(0, len(comps), 3):
            row_c = comps[row_start:row_start+3]
            cols = st.columns(3)
            for i, comp in enumerate(row_c):
                divisions = HIERARCHY[ind_name][comp]
                n_div = len(divisions)
                n_p = sum(len(v) for v in divisions.values())
                active = (st.session_state.comp == comp)
                with cols[i]:
                    st.markdown(f"""<div style="background:{'rgba(29,78,216,.15)' if active else '#0d1f35'};
                        border:1px solid {'#1d4ed8' if active else '#1e3a5f'};border-radius:10px;
                        padding:.9rem;margin-bottom:6px">
                      <div style="font-size:.82rem;font-weight:700;color:#e2e8f0;margin-bottom:4px">{comp}</div>
                      <div style="font-size:.68rem;color:#64748b">{n_div} divisions &middot; {n_p} plants/processes</div>
                    </div>""", unsafe_allow_html=True)
                    if st.button("Open", key=f"comp_{comp}", use_container_width=True,
                                  type="primary" if active else "secondary"):
                        st.session_state.comp = comp
                        st.session_state.plant = None
                        st.rerun()

        if st.session_state.comp:
            comp_name = st.session_state.comp
            st.markdown(f"""<div style="font-size:.68rem;font-weight:700;letter-spacing:2px;color:#3b82f6;
                            text-transform:uppercase;margin:1rem 0 .6rem;padding-bottom:6px;border-bottom:1px solid #1e3a5f">
                Step 3 — Select Plant / Process <span style="color:#475569;font-style:italic;letter-spacing:0;text-transform:none;font-weight:400;font-size:.8rem">/ {comp_name}</span></div>""", unsafe_allow_html=True)

            divisions = HIERARCHY[ind_name][comp_name]
            for div_name, plant_list in divisions.items():
                st.markdown(f'<div style="font-size:.62rem;font-weight:700;letter-spacing:2px;color:#475569;padding:6px 0 4px;text-transform:uppercase">{div_name}</div>', unsafe_allow_html=True)
                for row_start in range(0, len(plant_list), 3):
                    row_pp = plant_list[row_start:row_start+3]
                    cols = st.columns(3)
                    for i, p in enumerate(row_pp):
                        pm = PLANT_META.get(p, {})
                        status = pm.get("status", "")
                        has_psi = p in PLANT_META
                        active = (st.session_state.plant == p)
                        badge_clr = "#f97316" if status == "HHO" else "#3b82f6"
                        with cols[i]:
                            st.markdown(f"""<div style="background:{'rgba(29,78,216,.15)' if active else '#0d1f35'};
                                border:1px solid {'#1d4ed8' if active else '#1e3a5f'};
                                border-left:3px solid {badge_clr if status else '#1e3a5f'};border-radius:10px;
                                padding:.8rem;margin-bottom:6px;min-height:62px">
                              <div style="font-size:.78rem;font-weight:700;color:#e2e8f0;margin-bottom:4px">{p}</div>
                              {f'<span style="background:{badge_clr}20;color:{badge_clr};font-size:.6rem;font-weight:700;padding:2px 8px;border-radius:20px">{status}</span>' if status else '<span style="font-size:.62rem;color:#475569">PSI not yet available</span>'}
                            </div>""", unsafe_allow_html=True)
                            if has_psi:
                                if st.button("Open", key=f"plant_{p}", use_container_width=True,
                                              type="primary" if active else "secondary"):
                                    st.session_state.plant = p
                                    st.rerun()
                            else:
                                st.button("Open", key=f"plant_{p}", use_container_width=True, disabled=True)
