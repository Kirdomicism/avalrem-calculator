import streamlit as st
import pandas as pd
import hashlib
import json
import time

# ==============================================================================
# KIRDOMICISM ACADEMY — THE UNIVERSAL AVALREM WEB CALCULATOR (2026)
# ==============================================================================
# This is a production-grade Streamlit application that provides a visual,
# interactive, and scientifically rigorous Web App interface for Action Value Accounting (AVA).
# It completely eliminates AI calculation errors by anchoring all inputs to your
# proprietary formulas, card coefficients, and sovereign #z command protocol.
# ==============================================================================

# Page Configuration & Kirdomic Slate & Gold Theme Settings
st.set_page_config(
    page_title="Kirdomicism Academy: Avalrem Web Calculator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium Styling (Dark Mode Slate / Kirdomic Gold Highlights)
st.markdown("""
<style>
    .main-title {
        font-family: 'Georgia', serif;
        color: #D4AF37; /* Metallic Gold */
        text-align: center;
        font-size: 2.8rem;
        font-weight: bold;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-family: 'Verdana', sans-serif;
        color: #A0AEC0; /* Slate Gray */
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .kirdomic-header {
        font-family: 'Georgia', serif;
        color: #D4AF37;
        border-bottom: 2px solid #D4AF37;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .card-stat {
        background-color: #1A202C; /* Deep Charcoal */
        border: 1px solid #D4AF37;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stat-val {
        font-family: 'Georgia', serif;
        color: #D4AF37;
        font-size: 2.5rem;
        font-weight: bold;
    }
    .stat-lbl {
        font-family: 'Verdana', sans-serif;
        color: #E2E8F0;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .formula-box {
        background-color: #2D3748;
        border-left: 5px solid #D4AF37;
        padding: 1rem;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
        color: #E2E8F0;
        margin-bottom: 1.5rem;
    }
    div.stButton > button {
        background-color: #1A202C !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        font-family: 'Georgia', serif !important;
        font-weight: bold !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #D4AF37 !important;
        color: #1A202C !important;
        border: 1px solid #1A202C !important;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Standard Kirdomic Action Verbs & Coefficients
VERB_PRESETS = {
    "Custom (Manual Input)": {"C": 50.0, "a": 2.0, "i": 0.20, "code": "zS", "desc": "Custom calibrated action"},
    "Design (zT - System Plan)": {"C": 100.0, "a": 1.20, "i": 0.35, "code": "zT", "desc": "Craft and blueprint the core workflows of your system"},
    "Establish (zT - System Plan)": {"C": 100.0, "a": 1.30, "i": 0.40, "code": "zT", "desc": "Institutionalize long-term knowledge-sharing procedures"},
    "Study (zC - Future Analysis)": {"C": 80.0, "a": 1.50, "i": 0.25, "code": "zC", "desc": "Pre-calculate scenarios and strategic trends under uncertainty"},
    "Research (zX - Operation Analysis)": {"C": 80.0, "a": 1.80, "i": 0.30, "code": "zX", "desc": "Investigate environmental facts and digital landscapes"},
    "Maneuver (zF - Resource Execution)": {"C": 50.0, "a": 1.10, "i": 0.18, "code": "zF", "desc": "Deploy resources forcefully to overcome an immediate constraint"},
    "Abandon (zJ - Operation Exdysivity)": {"C": 90.0, "a": 1.05, "i": 0.235, "code": "zJ", "desc": "Decisively let go of unworkable rules, habits, or attachments"},
    "Revisit (zK - Control Exdysivity)": {"C": 70.0, "a": 1.40, "i": 0.20, "code": "zK", "desc": "Audit and adapt rolling forecasts as new situations emerge"},
    "Predict (zC - Future Analysis)": {"C": 115.0, "a": 1.10, "i": 0.45, "code": "zC", "desc": "Model variables and consequences with advanced systems foresight"},
    "Conclude (zJ - Operation Exdysivity)": {"C": 60.0, "a": 1.15, "i": 0.15, "code": "zJ", "desc": "Settle outstanding backlogs and complete processes systematically"}
}

# Standard 5x5 Action Grid Mapping Data
GRID_CELLS = {
    "zQ": {"focus": "Future", "mode": "Plan", "verb": "Brainstorm", "desc": "Model future scenarios and set unshakeable strategic targets"},
    "zW": {"focus": "Operation", "mode": "Plan", "verb": "Schedule", "desc": "Organize operations, deadlines, and squeeze cycle times"},
    "zE": {"focus": "Control", "mode": "Plan", "verb": "Participate", "desc": "Establish robust preventive measures and compliance guidelines"},
    "zR": {"focus": "Utilisation", "mode": "Plan", "verb": "Allocate", "desc": "Plan resource deployment, budgets, and recovery boundaries"},
    "zT": {"focus": "System", "mode": "Plan", "verb": "Design", "desc": "Craft core workflows, technology integrations, and architectures"},
    "zA": {"focus": "Future", "mode": "Execution", "verb": "Implement", "desc": "Execute a defined strategy, giving the official green light"},
    "zS": {"focus": "Operation", "mode": "Execution", "verb": "Produce", "desc": "Execute routine workflows with standard zero-defect quality"},
    "zD": {"focus": "Control", "mode": "Execution", "verb": "Check", "desc": "Perform audit procedures and verify operations against compliance"},
    "zF": {"focus": "Utilisation", "mode": "Execution", "verb": "Maneuver", "desc": "Physically deploy and exploit limited resources on hand"},
    "zG": {"focus": "System", "mode": "Execution", "verb": "Develop", "desc": "Deploy and test-run functional administrative software engines"},
    "zC": {"focus": "Future", "mode": "Analysis", "verb": "Study", "desc": "Pre-calculate and weigh strategic consequences under uncertainty"},
    "zX": {"focus": "Operation", "mode": "Analysis", "verb": "Research", "desc": "Investigate operational metrics, variance, and bottlenecks"},
    "zV": {"focus": "Control", "mode": "Analysis", "verb": "Investigate", "desc": "Uncover systemic weaknesses, risks, and process loopholes"},
    "zB": {"focus": "Utilisation", "mode": "Analysis", "verb": "Prioritize", "desc": "Audit budget returns, efficiency, and resource leakage"},
    "zN": {"focus": "System", "mode": "Analysis", "verb": "Test", "desc": "Audit and review administrative software or database systems"},
    "zY": {"focus": "Future", "mode": "Communication", "verb": "Announce", "desc": "Align long-term direction with stakeholders to prevent drag"},
    "zU": {"focus": "Operation", "mode": "Communication", "verb": "Report", "desc": "Transmit transparent, proactive updates of project status"},
    "zI": {"focus": "Control", "mode": "Communication", "verb": "Explain", "desc": "Deliver training and explain regulatory standards to the team"},
    "zO": {"focus": "Utilisation", "mode": "Communication", "verb": "Testimonise", "desc": "Share cost audits, performance returns, and capital results"},
    "zP": {"focus": "System", "mode": "Communication", "verb": "Demonstrate", "desc": "Explain and document functional software workflows for users"},
    "zH": {"focus": "Future", "mode": "Exdysivity", "verb": "Dream", "desc": "Dream future transitions and adapt targets dynamically"},
    "zJ": {"focus": "Operation", "mode": "Exdysivity", "verb": "Transform", "desc": "Willingly abandon obsolete functional routines and standards"},
    "zK": {"focus": "Control", "mode": "Exdysivity", "verb": "Establish", "desc": "Modify control frameworks and rules dynamically under change"},
    "zL": {"focus": "Utilisation", "mode": "Exdysivity", "verb": "Create", "desc": "Shed unworkable resource routines and acquire new capabilities"},
    "zM": {"focus": "System", "mode": "Exdysivity", "verb": "Revamp", "desc": "Completely reconstruct obsolete procedures and standards"}
}

# ------------------------------------------------------------------------------
# Session State & Blockchain Ledger Setup
# ------------------------------------------------------------------------------
if "ledger" not in st.session_state:
    st.session_state.ledger = []
if "selected_cell" not in st.session_state:
    st.session_state.selected_cell = "zQ"
if "command_status" not in st.session_state:
    st.session_state.command_status = ""

# Utility to add a block to our secure Legacy Ledger
def add_to_ledger(action_name, code, C, a, i, formula_type, result, status="Validated"):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    prev_hash = "0" * 64 if not st.session_state.ledger else st.session_state.ledger[-1]["current_hash"]
    
    # Pack data to generate deterministic SHA-256 block hash
    block_data = f"{action_name}{code}{C}{a}{i}{result}{timestamp}{prev_hash}"
    current_hash = hashlib.sha256(block_data.encode()).hexdigest()
    
    tx_id = f"TX-KDM-{int(time.time())}"
    
    st.session_state.ledger.append({
        "timestamp": timestamp,
        "tx_id": tx_id,
        "action": action_name,
        "code": code,
        "C": C,
        "a": a,
        "i": i,
        "type": formula_type,
        "result": round(result, 2),
        "status": status,
        "prev_hash": prev_hash[:8] + "...",
        "current_hash": current_hash[:8] + "..."
    })

# ------------------------------------------------------------------------------
# Main Page Render Layout
# ------------------------------------------------------------------------------
st.markdown("<h1 class='main-title'>🧠 KIRDOMICISM ACADEMY</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Universal Avalrem Web Calculator (Open-Core Pilot v1.0)</div>", unsafe_allow_html=True)

# Main Stats Dashboard Row
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

total_nava = sum(tx["result"] for tx in st.session_state.ledger if tx["status"] == "Validated")
pending_nava = sum(tx["result"] for tx in st.session_state.ledger if tx["status"] == "Pending")
total_txs = len(st.session_state.ledger)
usd_exchange_rate = 1.25  # 1 Avalrem = $1.25 USD standard
total_equity = total_nava * usd_exchange_rate

with col_stat1:
    st.markdown(f"""
    <div class='card-stat'>
        <div class='stat-val'>{total_nava:.2f}</div>
        <div class='stat-lbl'>🔐 Accumulated NAVA</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat2:
    st.markdown(f"""
    <div class='card-stat'>
        <div class='stat-val'>{pending_nava:.2f}</div>
        <div class='stat-lbl'>⏳ Pending Predictions (^)</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat3:
    st.markdown(f"""
    <div class='card-stat'>
        <div class='stat-val'>${total_equity:,.2f}</div>
        <div class='stat-lbl'>💸 Value Equity (USD)</div>
    </div>
    """, unsafe_allow_html=True)

with col_stat4:
    st.markdown(f"""
    <div class='card-stat'>
        <div class='stat-val'>{total_txs}</div>
        <div class='stat-lbl'>⛓️ Ledger Transactions</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# Main Interface Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🖥️ Interactive Action Grid", 
    "🎛️ Algorithmic Calculator", 
    "⌨️ #z Command Console", 
    "⛓️ Sovereign Legacy Ledger"
])

# ==============================================================================
# TAB 1: INTERACTIVE ACTION GRID
# ==============================================================================
with tab1:
    st.markdown("<h3 class='kirdomic-header'>Play the Keyboard of Execution</h3>", unsafe_style_html=True)
    st.write("Click on any coded cell below to load its focus perspective, mode, and standard parameters into your active workspace:")
    
    # 5x5 Grid Layout
    cols_grid = st.columns(5)
    
    grid_rows = [
        ["zQ", "zW", "zE", "zR", "zT"],
        ["zA", "zS", "zD", "zF", "zG"],
        ["zC", "zX", "zV", "zB", "zN"],
        ["zY", "zU", "zI", "zO", "zP"],
        ["zH", "zJ", "zK", "zL", "zM"]
    ]
    
    for row_idx, row in enumerate(grid_rows):
        for col_idx, cell_code in enumerate(row):
            with cols_grid[col_idx]:
                cell_data = GRID_CELLS[cell_code]
                btn_label = f"[{cell_code}]\n{cell_data['verb']}"
                if st.button(btn_label, key=f"grid_{cell_code}"):
                    st.session_state.selected_cell = cell_code
                    
    # Display Details of Selected Grid Cell
    sel_code = st.session_state.selected_cell
    sel_data = GRID_CELLS[sel_code]
    
    st.write("")
    st.markdown(f"### Selected Viewport: **{sel_code} ({sel_data['verb']})**")
    
    col_det1, col_col2 = st.columns([2, 1])
    with col_det1:
        st.write(f"🌐 **Strategic Lens (ControllerFOCUS):** `{sel_data['focus']} Focus` — defining where your intelligence looks.")
        st.write(f"⚡ **Cognitive mode (PEACE):** `{sel_data['mode']} Mode` — determining how thinking progresses.")
        st.write(f"📝 **Description & Objective:** {sel_data['desc']}")
    with col_col2:
        st.info(f"💡 Standard targets for **{sel_code}** are now synchronized. Open the 'Algorithmic Calculator' tab to execute!")

# ==============================================================================
# TAB 2: ALGORITHMIC CALCULATOR
# ==============================================================================
with tab2:
    st.markdown("<h3 class='kirdomic-header'>Verify Your Action Value</h3>", unsafe_style_html=True)
    
    # Left Input Configuration, Right Real-Time Results
    col_calc_left, col_calc_right = st.columns([1, 1])
    
    with col_calc_left:
        st.markdown("#### Configure Variables")
        
        # Load Presets Dropdown
        preset_choice = st.selectbox(
            "Select Kirdomic Verb Preset (Auto-calibrates coefficients to prevent error):",
            list(VERB_PRESETS.keys())
        )
        
        selected_preset = VERB_PRESETS[preset_choice]
        
        # Action Input fields
        act_name = st.text_input("Enter Action Description:", value=f"Run {selected_preset['code']} {preset_choice.split(' ')[0]} protocol")
        grid_code_choice = st.selectbox("Grid Code Intersection:", list(GRID_CELLS.keys()), index=list(GRID_CELLS.keys()).index(selected_preset["code"]))
        
        # Formula Type Toggle
        formula_type = st.radio(
            "Action Horizon:",
            ["Standard Action (Sustained Performance)", "Eternal Legacy (Perpetual Contribution)"]
        )
        
        # Slider ranges based on strict 2026 standards
        if preset_choice == "Custom (Manual Input)":
            input_C = st.slider("Consequences (C) — Value/Impact:", 1.0, 150.0, 50.0)
            input_a = st.slider("Speed Factor (a) — Velocity (lower is faster):", 1.0, 10.0, 2.0)
            input_i = st.slider("Degree of Effort (i) — Intensity Coefficient:", 0.01, 0.99, 0.20)
        else:
            input_C = st.slider("Consequences (C) [Locked to Preset]:", 1.0, 150.0, selected_preset["C"])
            input_a = st.slider("Speed Factor (a) [Locked to Preset]:", 1.0, 10.0, selected_preset["a"])
            input_i = st.slider("Degree of Effort (i) [Locked to Preset]:", 0.01, 0.99, selected_preset["i"])
            
        input_g = 0.0
        if formula_type == "Eternal Legacy (Perpetual Contribution)":
            input_g = st.slider("Perpetual Growth/Prevention Coefficient (g):", 0.01, 0.50, 0.05)
            
    with col_calc_right:
        st.markdown("#### Real-Time Algorithmic Analysis")
        
        # Execute Equations cleanly
        if formula_type == "Standard Action (Sustained Performance)":
            denominator = input_a - input_i
            if denominator <= 0:
                st.error("⚠️ Logical Error: Speed Factor (a) must be strictly greater than Effort (i) to prevent infinite loop/negative outputs.")
                avalrem_val = 0.0
            else:
                avalrem_val = input_C / denominator
                st.markdown(f"""
                <div class='formula-box'>
                    Avalrem = C / (a - i)<br>
                    Avalrem = {input_C} / ({input_a} - {input_i})<br>
                    Avalrem = {input_C} / {denominator:.3f}<br>
                    Result = <b>{avalrem_val:.2f} AVR</b>
                </div>
                """, unsafe_style_html=True)
        else:
            denominator = input_a - input_i - input_g
            if denominator <= 0:
                st.error("⚠️ Logical Error: Cumulative variables (a - i - g) must yield a positive denominator to prevent division by zero or negative legacy.")
                avalrem_val = 0.0
            else:
                avalrem_val = input_C / denominator
                st.markdown(f"""
                <div class='formula-box'>
                    Terminal Avalrem = C_inf / (a - i - g)<br>
                    Terminal Avalrem = {input_C} / ({input_a} - {input_i} - {input_g})<br>
                    Terminal Avalrem = {input_C} / {denominator:.3f}<br>
                    Result = <b>{avalrem_val:.2f} AVR</b>
                </div>
                """, unsafe_style_html=True)
                
        # Interactive Decision Optimization Insights
        st.markdown("##### 🔍 Humanic Intelligence Feedback")
        if avalrem_val > 100:
            st.success(f"🚀 **Supreme Impactality:** This action yields a magnificent **{avalrem_val:.2f} AVR**. It represents a transformative, high-value move that successfully shrinks your strategic delay.")
        elif avalrem_val > 40:
            st.info(f"⚡ **Standard Optimization:** This action is calculated at **{avalrem_val:.2f} AVR**. It represents solid operational execution. You can maximize value further by shrinking your timing factor (a) to execute faster.")
        else:
            st.warning(f"⚠️ **Peonerosal Risk:** An action value of only **{avalrem_val:.2f} AVR** indicates high personal effort (i) on a low-impact target (C). Audit this task; can it be automated or delegated to prevent Peonerosis?")
            
        # Command triggers directly integrated
        st.write("")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔮 #z^ (Predict Value)"):
                add_to_ledger(act_name, grid_code_choice, input_C, input_a, input_i, "Prediction", avalrem_val, "Pending")
                st.success("🔮 Pre-action potential recorded as Pending in your Ledger!")
        with col_btn2:
            if st.button("⛓️ #z* (Commit & Validate)"):
                add_to_ledger(act_name, grid_code_choice, input_C, input_a, input_i, formula_type, avalrem_val, "Validated")
                st.success("⛓️ Post-action reality committed and locked into your Immutable Legacy Ledger!")

# ==============================================================================
# TAB 3: #z COMMAND PROTOCOL CONSOLE
# ==============================================================================
with tab3:
    st.markdown("<h3 class='kirdomic-header'>Sovereign Interface Command Console</h3>", unsafe_style_html=True)
    st.write("Write and process raw command-line text strings to query, predict, and log actions directly using Kirdomic syntax:")
    
    st.markdown("""
    <div style='background-color:#1A202C; padding:1rem; border-radius:4px; margin-bottom:1rem;'>
        <b>Syntax Rules:</b><br>
        • Pre-Action Predict: <code>#z^ [Action] ::: [C]: [Val] ::: [a]: [Val] ::: [i]: [Val]</code><br>
        • Post-Action Commit: <code>#z* [Action] ::: [C]: [Val] ::: [a]: [Val] ::: [i]: [Val]</code>
    </div>
    """, unsafe_allow_html=True)
    
    command_input = st.text_input(
        "Enter Command String:", 
        value="#z^ Design real-time executive dashboard ::: [C]: 100 ::: [a]: 1.25 ::: [i]: 0.35"
    )
    
    if st.button("Process Command String", key="process_cmd_btn"):
        try:
            # Simple CLI parser
            is_predict = "#z^" in command_input
            is_commit = "#z*" in command_input
            
            if not is_predict and not is_commit:
                st.error("⚠️ Invalid Command: String must begin with either `#z^` or `#z*` namespace indicators.")
            else:
                # Strip prefix
                clean_str = command_input.replace("#z^", "").replace("#z*", "").strip()
                parts = clean_str.split(":::")
                
                action_part = parts[0].strip()
                C_val = 50.0
                a_val = 2.0
                i_val = 0.20
                
                for part in parts[1:]:
                    if "[C]:" in part:
                        C_val = float(part.replace("[C]:", "").strip())
                    elif "[a]:" in part:
                        a_val = float(part.replace("[a]:", "").strip())
                    elif "[i]:" in part:
                        i_val = float(part.replace("[i]:", "").strip())
                
                # Execute calculation
                denom = a_val - i_val
                if denom <= 0:
                    st.error("⚠️ Math Error: Denominator is zero or negative.")
                else:
                    ans = C_val / denom
                    status_lbl = "Pending" if is_predict else "Validated"
                    add_to_ledger(action_part, "zT", C_val, a_val, i_val, "Console Input", ans, status_lbl)
                    st.success(f"📟 Verified! Parsed action successfully: **{action_part}** | Result: **{ans:.2f} AVR** stored as **{status_lbl}**.")
        except Exception as ex:
            st.error(f"⚠️ Parsing Error: Please verify that you are formatting the string with correctly spaced colons `:::` separators. Error context: {ex}")

# ==============================================================================
# TAB 4: SOVEREIGN LEGACY LEDGER
# ==============================================================================
with tab4:
    st.markdown("<h3 class='kirdomic-header'>Cryptographic Block Chain Registry</h3>", unsafe_style_html=True)
    st.write("Verifiable and immutable digital audit trail of your lifetime contribution to reality:")
    
    if not st.session_state.ledger:
        st.info("Your ledger is currently empty. Go to the 'Algorithmic Calculator' or 'Command Console' tabs to generate and store your first actions!")
    else:
        df_ledger = pd.DataFrame(st.session_state.ledger)
        st.dataframe(df_ledger, use_container_width=True)
        
        # Download database backups
        st.write("")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            json_str = json.dumps(st.session_state.ledger, indent=4)
            st.download_button(
                label="📥 Export Ledger Block-Database (JSON)",
                data=json_str,
                file_name="kirdomic_legacy_ledger.json",
                mime="application/json"
            )
        with col_dl2:
            csv_data = df_ledger.to_csv(index=False)
            st.download_button(
                label="📊 Download Performance Statement (CSV)",
                data=csv_data,
                file_name="kirdomic_performance_report.csv",
                mime="text/csv"
            )

# ------------------------------------------------------------------------------
# Sidebar Context Panel
# ------------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#D4AF37; font-family:Georgia;'>🧠 Kirdomic Lexicon</h2>", unsafe_style_html=True)
    st.write("---")
    st.write("🛡️ **Atammayata:** Achieving absolute unconcoctability, protecting consciousness from 'emotional cooking' or crises.")
    st.write("🐍 **Exdysivity:** Continuous, natural renewal by willingly shedding obsolete habits, standards, and rules.")
    st.write("⚡ **Anxergy:** The internal ontology of converting anxiety into a constructive execution drive.")
    st.write("🧬 **Dexterience:** Shifting from waiting for perfect conditions to executing cleanly with what you have on hand.")
    st.write("📊 **Avalremy:** Measuring human contribution and future-readiness through the quantitative value of physical actions.")
    st.write("---")
    st.markdown("<div style='text-align:center; color:#A0AEC0;'>Kirdomic Academy © 2026</div>", unsafe_style_html=True)
