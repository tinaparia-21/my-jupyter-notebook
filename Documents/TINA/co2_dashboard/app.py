# MODULE 1: IMPORT REQUIRED LIBRARIES

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components

# --- GLOBAL RED GLOW PALETTES ---
RED_GLOW_BARS = ["#4A0404", "#991B1B", "#DC2626", "#EF4444", "#FCA5A5"]

RED_FUEL_MAP = {
    "Oil": "#EF4444",       # Vibrant Crimson
    "Coal": "#334155",      # Slate Charcoal
    "Gas": "#38BDF8",       # Sky Blue
    "Flaring": "#F59E0B",   # Warm Amber
    "Cement": "#94A3B8"     # Muted Grey
}

# Multi-Color Vibrant Palette for Line Graphs (High visibility on dark & light themes)
MULTI_GLOW_LINE_PALETTE = [
    "#38BDF8",  # Electric Cyan
    "#EF4444",  # Coral Crimson
    "#10B981",  # Vibrant Emerald
    "#F59E0B",  # Amber Gold
    "#A855F7",  # Neon Purple
    "#EC4899",  # Hot Pink
    "#3B82F6",  # Royal Blue
]
# MODULE 2: PAGE CONFIGURATION & DATA LOADING

st.set_page_config(
    page_title="Climate Change Awareness Portal",
    page_icon="🌏",
    layout="wide"
)

# --- SESSION STATE INITIALIZATION ---
if "user_name" not in st.session_state:
    st.session_state.user_name = ""

# --- RESPONSIVE & DUAL-THEME WELCOME GATE ---
if not st.session_state.user_name:
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(
            """
            <div style="
                background: var(--background-secondary, rgba(2, 132, 199, 0.05));
                border: 2px solid #0284c7;
                border-radius: 18px;
                padding: 36px 32px 24px 32px;
                text-align: center;
                box-shadow: 0 0 20px rgba(2, 132, 199, 0.25);
                margin-bottom: 20px;
                width: 100%;
                box-sizing: border-box;
            ">
                <div style="font-size: 46px; margin-bottom: 12px; line-height: 1;">🌍</div>
                <h2 style="
                    font-size: 26px; 
                    font-weight: 800; 
                    letter-spacing: -0.3px; 
                    margin: 0 0 12px 0;
                    color: inherit;
                ">
                    Climate Change Awareness Portal
                </h2>
                <p style="
                    font-size: 15px; 
                    opacity: 0.85; 
                    margin: 0;
                    line-height: 1.6;
                    color: inherit;
                    font-weight: 500;
                ">
                    Welcome! Please enter your name below to unlock interactive emissions analytics and global sustainability data.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form(key="welcome_form"):
            input_name = st.text_input(
                "Enter your name to proceed:", placeholder="e.g. Alex"
            )
            submit_button = st.form_submit_button(
                "Explore Dashboard →", use_container_width=True
            )

            if submit_button:
                if input_name.strip():
                    st.session_state.user_name = input_name.strip()
                    st.rerun()
                else:
                    st.warning("Please enter your name to proceed.")

    st.stop()

# --- PERSONALIZED RESPONSIVE WELCOME BANNER ---
st.markdown(
    f"""
    <div style="
        margin-top: 40px;
        margin-bottom: 24px;
        background-color: var(--background-secondary, rgba(2, 132, 199, 0.06));
        border: 1.5px solid #0284c7;
        border-radius: 14px;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 12px;
        box-shadow: 0 4px 16px rgba(2, 132, 199, 0.1);
        box-sizing: border-box;
    ">
        <div style="display: flex; align-items: center; gap: 14px; min-width: 220px; flex: 1;">
            <span style="font-size: 28px; line-height: 1;">👋</span>
            <div>
                <h3 style="
                    margin: 0; 
                    font-size: 18px; 
                    font-weight: 700; 
                    color: inherit;
                    letter-spacing: -0.2px;
                ">
                    Welcome back, {st.session_state.user_name}!
                </h3>
                <p style="
                    margin: 3px 0 0 0; 
                    font-size: 13px; 
                    opacity: 0.75;
                    color: inherit;
                ">
                    Explore real-time climate trajectories, fuel mix analytics, and trade dynamics.
                </p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- RESPONSIVE DASHBOARD NAVIGATION & CLEAN DUAL-THEME STYLING ---
st.markdown(
    """
    <style>
        /* --- GLOBAL RESPONSIVE LAYOUT & FOOTER CLEARANCE --- */
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 120px !important;
        }
        
        h1 {
            overflow: visible !important;
            line-height: 1.3 !important;
        }

        /* --- CLEAN NAVIGATION BUTTONS (DYNAMIC LIGHT & DARK MODE) --- */
        div[data-testid="stRadio"] > div {
            flex-direction: row !important;
            flex-wrap: wrap !important;
            gap: 8px !important;
        }

        /* 1. Base unselected radio buttons */
        div[data-testid="stRadio"] div[role="radiogroup"] label {
            background-color: var(--background-secondary, rgba(2, 132, 199, 0.08)) !important;
            border: 1.5px solid #0284c7 !important;
            border-radius: 8px !important;
            padding: 6px 14px !important;
            margin: 3px 2px !important;
            transition: all 0.2s ease-in-out !important;
            cursor: pointer !important;
        }

        /* High-contrast text for unselected options in Light AND Dark theme */
        div[data-testid="stRadio"] div[role="radiogroup"] label * {
            color: var(--text-color, inherit) !important;
            font-weight: 600 !important;
            opacity: 1 !important;
            visibility: visible !important;
        }

        /* 2. Selected active button (Solid Blue Fill) */
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
            background-color: #0284c7 !important;
            border-color: #0284c7 !important;
            box-shadow: none !important;
        }

        /* Crisp white text for selected button */
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) * {
            color: #ffffff !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }

        /* 3. Hover effect */
        div[data-testid="stRadio"] div[role="radiogroup"] label:hover:not(:has(input:checked)) {
            background-color: rgba(2, 132, 199, 0.25) !important;
            border-color: #38bdf8 !important;
        }

        /* 4. Kill default radio circles & outer card shadows/glows */
        div[data-testid="stRadio"] label > div:first-child {
            display: none !important;
        }

        div[data-testid="stRadio"],
        div[data-testid="stRadio"] > div,
        div[role="radiogroup"] {
            box-shadow: none !important;
            background: transparent !important;
            border: none !important;
        }

        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stRadio"]) {
            box-shadow: none !important;
            background: transparent !important;
            border: none !important;
            filter: none !important;
        }

        /* --- SIDEBAR TOGGLE BUTTON STYLING --- */
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarExpandedControl"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: auto !important;
        }

        [data-testid="stSidebarCollapsedControl"] button svg,
        [data-testid="stSidebarExpandedControl"] button svg {
            display: none !important;
        }

        [data-testid="stSidebarCollapsedControl"] button::after,
        [data-testid="stSidebarExpandedControl"] button::after {
            content: "⚙️ Filters";
            font-size: 14px !important;
            font-weight: 700 !important;
            white-space: nowrap !important;
            letter-spacing: 0.5px !important;
            padding: 6px 16px !important;
            border-radius: 20px !important;
            color: #0284c7 !important;
            background-color: rgba(2, 132, 199, 0.12) !important;
            border: 1.5px solid #0284c7 !important;
            box-shadow: 0 0 10px rgba(2, 132, 199, 0.25) !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="stSidebarCollapsedControl"] button:hover::after,
        [data-testid="stSidebarExpandedControl"] button:hover::after {
            background-color: rgba(2, 132, 199, 0.25) !important;
            box-shadow: 0 0 14px rgba(56, 189, 248, 0.5) !important;
            transform: scale(1.05) !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- GLOBAL PLOTLY GRAPH STYLER ---
def apply_custom_chart_style(fig, height=380):
    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12, color="#262730"),
        hoverlabel=dict(
            bgcolor="#ffffff",
            font_size=13,
            font_family="Arial, sans-serif",
            bordercolor="#d0d0d0"
        )
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#f0f0f0")
    return fig

# 2. Optimized Data Loading Function
# MODULE 2: SAFE DATASET LOAD & PREPROCESSING
# Pass ttl=86400 (seconds in 24 hours) or "24h"
@st.cache_data(ttl="24h")
def load_dataset():
    url = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
    df = pd.read_csv(url)
    
    # 1. Filter years >= 1950
    df = df[df['year'] >= 1950].copy()
    
    # 2. Extract valid sovereign countries
    valid_iso = df['iso_code'].notna()
    is_not_owid = df['iso_code'].str.startswith('OWID', na=False) == False
    
    country_df = df[valid_iso & is_not_owid].copy()
    
    return df, country_df

raw_df, country_df = load_dataset()

# MODULE 3: SIDEBAR CONTROLS & GLOBAL FILTERS

st.sidebar.title("🔍 Report Filters")
st.sidebar.markdown("Configure global parameters applied across dashboard pages.")

# --- VISITOR COUNTER BADGE SQUARE ---
st.sidebar.markdown("""
    <div style="
        background: var(--background-secondary, rgba(0, 230, 118, 0.05));
        border: 2px solid #00E676;
        border-radius: 10px;
        padding: 14px 10px;
        margin-top: 10px;
        margin-bottom: 15px;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.35);
        text-align: center;
        word-wrap: break-word;
    ">
        <h5 style="margin: 0 0 8px 0; font-size: 0.9rem; color: #00E676; display: flex; align-items: center; justify-content: center; gap: 6px;">
            🌍 <span>Portal Views</span>
        </h5>
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fclimate-change-awareness-portal.streamlit.app&count_bg=%2300E676&title_bg=%231E293B&icon=&icon_color=%23E7E7E7&title=Views&edge_flat=false" 
             style="max-width: 100%; height: auto; margin-top: 2px;" 
             alt="Visitor Count"/>
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# # 1. Year Range Selection (Equivalent to a Date Slicer)
min_year = int(country_df['year'].min())
max_year = int(country_df['year'].max())

selected_year_range = st.sidebar.slider(
    label="Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(1990, max_year),  # Default starting selection range
    step=1,
    key="year_range_slider"
)

# Store the upper year (e.g., 2013) so the Quiz can automatically pick it up
st.session_state['selected_year'] = selected_year_range[1]

# 2. Country Selection (Equivalent to a Multi-Select Dropdown Slicer)
available_countries = sorted(country_df['country'].unique().tolist())
default_countries = ["India", "United States", "China", "Germany", "United Kingdom"]

selected_countries = st.sidebar.multiselect(
    label="Select Countries for Analysis",
    options=available_countries,
    default=default_countries
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

# CARD 1: PORTAL VIEWS COUNTER
st.sidebar.markdown(
    """
    <div style="
        background: var(--background-secondary, rgba(0, 230, 118, 0.05));
        border: 2px solid #00E676;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 12px;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.35);
        color: var(--text-color, inherit);
        word-wrap: break-word;
    ">
        <h5 style="margin: 0 0 6px 0; font-size: 0.9rem; color: #00E676; display: flex; align-items: center; gap: 6px;">
            🌍 <span>Portal Views Counter</span>
        </h5>
        <p style="margin: 0; font-size: 0.78rem; opacity: 0.92; line-height: 1.4;">
            <b>What this shows:</b> Real-time visitor traffic and dynamic interaction counter monitoring global engagement across all dashboard pages.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# CARD 2: GLOBAL FILTER CONTROLS
st.sidebar.markdown(
    """
    <div style="
        background: var(--background-secondary, rgba(0, 230, 118, 0.05));
        border: 2px solid #00E676;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 15px;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.35);
        color: var(--text-color, inherit);
        word-wrap: break-word;
    ">
        <h5 style="margin: 0 0 6px 0; font-size: 0.9rem; color: #00E676; display: flex; align-items: center; gap: 6px;">
            ⚙️ <span>Global Filter Controls</span>
        </h5>
        <p style="margin: 0; font-size: 0.78rem; opacity: 0.92; line-height: 1.4;">
            <b>What this controls:</b> Cross-filters the entire dashboard. Adjusting the year slider or selecting country tags dynamically updates all charts, trajectory lines, and maps site-wide.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 3. Dynamic Data Filtering Logic (with empty fallback)
active_country_filter = selected_countries if selected_countries else available_countries

filtered_country_df = country_df[
    (country_df['country'].isin(active_country_filter)) &
    (country_df['year'] >= selected_year_range[0]) &
    (country_df['year'] <= selected_year_range[1])
]

# Filter aggregate dataset (includes World/Continents) based on selected year range
filtered_raw_df = raw_df[
    (raw_df['year'] >= selected_year_range[0]) &
    (raw_df['year'] <= selected_year_range[1])
]

# MODULE 4: MULTI-PAGE TAB NAVIGATION & PAGE 1 (EXECUTIVE SUMMARY)

# Header Title Block
# MODULE 4: MULTI-PAGE TAB NAVIGATION (9-PAGE WEBSITE STRUCTURE)

st.title("🌍 Climate Change Awareness Portal")
st.markdown("A comprehensive web platform analyzing global carbon emissions, energy dynamics, and climate equity.")

# --- FIRST-TIME VISITOR GLOSSARY EXPANDER ---
with st.expander("📖 New here? Quick Guide to Abbreviations & Metrics"):
    st.markdown(
        """
        * **CO₂ (Carbon Dioxide):** The main greenhouse gas driving climate change, produced by burning fossil fuels, industry, and land-use changes.
        * **Mt (Million Metric Tonnes):** The standard unit for large-scale gas emissions (1 Mt = 1 billion kilograms).
        * **Per Capita (per person):** Total national emissions divided by population, showing average individual footprint.
        * **Production CO₂:** Emissions produced strictly within a country's physical geographic borders.
        * **Consumption CO₂ (Trade-Adjusted):** Emissions adjusted for international trade (Production + Imported Goods - Exported Goods).
        """
    )
st.markdown("<br>", unsafe_allow_html=True)

# =============================================================================
# NAVIGATION CONTAINER CSS (REMOVES WRAPPER BOX & BOTTOM GLOW)
# =============================================================================
st.markdown(
    """
    <style>
        /* 1. Remove box-shadow and background card styling from the radio container */
        div[data-testid="stRadio"] {
            box-shadow: none !important;
            background: transparent !important;
            border: none !important;
            padding: 0px !important;
        }

        /* 2. Target outer wrapper div holding the radio group to kill the bottom glow */
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stRadio"]) {
            box-shadow: none !important;
            background: transparent !important;
            border: none !important;
            filter: none !important;
        }
        
        /* 3. Strip shadow on option group level */
        div[role="radiogroup"] {
            box-shadow: none !important;
        }

        /* 4. VISUAL SELECTION HIGHLIGHT: Turn ONLY the selected button solid blue */
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
            background-color: #0284c7 !important;
            border-color: #0284c7 !important;
        }

        /* Force crisp white text and icons inside the selected button */
        div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) * {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        /* Ensure Quiz Form Question Labels are Fully Visible */
        div[data-testid="stForm"] div[data-testid="stRadio"] > label p {
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            color: var(--text-color, inherit) !important;
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
            margin-bottom: 8px !important;
        }

        /* Custom Sidebar Toggle styling to display ⚙️ Filters icon */
        [data-testid="stSidebarCollapseButton"] button::before,
        [data-testid="stSidebarExpandButton"] button::before {
            content: "⚙️ Filters";
            font-weight: 600;
            font-size: 14px;
            color: #31333F;
        }
        
        /* Hide the default tiny arrow icon inside the button */
        [data-testid="stSidebarCollapseButton"] button svg,
        [data-testid="stSidebarExpandButton"] button svg {
            display: none !important;
        }

        /* Hide radio circles across all Streamlit versions */
        div[data-testid="stRadio"] input[type="radio"],
        div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child,
        div[data-testid="stRadio"] label > div:first-child {
            display: none !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Include tab_home, tab1 through tab6, tab_action, and tab_about
# --- NAVIGATION SELECTOR ---
selected_tab = st.radio(
    label="Navigation",
    options=[
        "🏠 Home", 
        "📊 Executive Summary", 
        "📈 Country Trends", 
        "🗺️ Global Map", 
        "🔌 Fuel Breakdown", 
        "⚖️ Equity & Per Capita", 
        "📁 Data Explorer", 
        "💡 Take Action", 
        "🎯 Knowledge Quiz",
        "ℹ️ About & Tech Stack"
    ],
    label_visibility="collapsed",
    horizontal=True,
    key="main_nav_radio"  # <-- FORCES FRESH RE-RENDER
)

st.markdown("---")

# =============================================================================
# TAB: HOME & OVERVIEW
# =============================================================================
if selected_tab == "🏠 Home":
    # --- CUSTOM STYLING FOR NATIVE CONTAINERS ---
    st.markdown(
        """
        <style>
            /* 1. Outer Container: Thicker border & subtle accent background */
            [data-testid="stVerticalBlock"] > div:has(div[data-testid="stVerticalBlockBorderWrapper"]) {
                border-width: 2px !important;
                border-color: #0284c7 !important;
                border-radius: 12px !important;
            }

            /* 2. Inner Cards: Colored background adaptive for Light/Dark mode */
            [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"] {
                background-color: var(--background-primary, rgba(255, 255, 255, 0.03)) !important;
                border: 1px solid rgba(148, 163, 184, 0.25) !important;
                border-radius: 10px !important;
                padding: 12px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease,border-color 0.25s ease !important;
            }

            /* Hover effect for interactive feel */
            [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlockBorderWrapper"]:hover {
                transform: translateY(-4px) !important;
                border-color: #0284c7 !important;
                box-shadow: 0 10px 20px -5px rgba(2, 132, 199, 0.25) !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # --- OUTER DASHBOARD CONTAINER ---
    with st.container(border=True):
        st.subheader("Welcome to the Climate Awareness Data Portal")

        # Mission Banner
        st.info(
            "**Mission Statement:** This platform provides data-driven insights into global greenhouse gas emissions, enabling students, researchers, and policymakers to explore carbon trajectories and energy transitions."
        )

        st.markdown("")  # Spacing

        # Two Side-by-Side Inner Cards
        col_obj, col_ins = st.columns(2)

        # Left Card: Key Objectives
        with col_obj:
            with st.container(border=True):
                st.markdown("### 🎯 Key Objectives")
                st.markdown(
                    """
                * **Track Global Trajectories:** Monitor national carbon outputs from 1950 to present day.
                * **Evaluate Energy Mix:** Analyze contributions of coal, oil, gas, and industry.
                * **Promote Equity:** Distinguish absolute national emissions from individual per-capita impacts.
                * **Provide Open Access:** Download processed datasets for independent research.
                """
                )

        # Right Card: Key Insights
        with col_ins:
            with st.container(border=True):
                st.markdown("### 📌 Key Insights at a Glance")
                st.markdown(
                    """
                * **Top Emitters:** A small group of industrial nations accounts for over 50% of current annual CO₂ output.
                * **Historical Responsibility:** Western economies account for the majority of cumulative historical emissions since 1950.
                * **Trade Discrepancy:** High-income nations often import embedded carbon through manufactured goods.
                """
                )

    st.markdown("---")

    st.markdown("### 🌡️ EFFECTS OF CLIMATE CHANGE")
    st.caption("Hover over any card to pause scrolling and inspect details.")

    carousel_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: transparent;
        }

        .carousel-container {
            width: 100%;
            overflow: hidden;
            position: relative;
            padding: 6px 0;
        }

        .carousel-track {
            display: flex;
            gap: 16px;
            width: max-content;
            animation: scroll-carousel 25s linear infinite;
        }

        .carousel-container:hover .carousel-track {
            animation-play-state: paused;
        }

        /* Square Card Styling with Tight Interior Alignment */
        .carousel-card {
            width: 240px;
            height: 200px;
            flex-shrink: 0;
            background: rgba(2, 132, 199, 0.07);
            border: 2px solid #0284c7;
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
            color: #0284c7;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: flex-start; /* Keeps content closely grouped at top */
        }

        .carousel-card h4 {
            margin: 0 0 8px 0; /* Minimal bottom gap under title */
            font-size: 1rem;
            color: #0284c7;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .carousel-card p {
            margin: 0;
            font-size: 0.82rem;
            line-height: 1.4;
            color: inherit;
            opacity: 0.95;
        }

        @keyframes scroll-carousel {
            0% { transform: translateX(0); }
            100% { transform: translateX(calc(-256px * 4)); }
        }
    </style>
    </head>
    <body>

    <div class="carousel-container">
        <div class="carousel-track">
            <!-- CARD 1 -->
            <div class="carousel-card">
                <h4>🌊 Rising Sea Levels</h4>
                <p><b>Impact:</b> Thermal expansion & glacier melt cause sea level rise.<br><br><b>Consequence:</b> Displaces coastal communities and accelerates land erosion.</p>
            </div>

            <!-- CARD 2 -->
            <div class="carousel-card">
                <h4>🔥 Extreme Weather</h4>
                <p><b>Impact:</b> Atmospheric warming traps intense heat and moisture.<br><br><b>Consequence:</b> Causes prolonged droughts, wildfires, and violent storms.</p>
            </div>

            <!-- CARD 3 -->
            <div class="carousel-card">
                <h4>🌾 Food & Water Security</h4>
                <p><b>Impact:</b> Erratic rainfall disrupts global agricultural cycles.<br><br><b>Consequence:</b> Reduces global crop yields and increases water scarcity.</p>
            </div>

            <!-- CARD 4 -->
            <div class="carousel-card">
                <h4>🏜️ Ecosystem Loss</h4>
                <p><b>Impact:</b> Oceans absorb excess CO₂, driving acidification.<br><br><b>Consequence:</b> Bleaches coral reefs and disrupts marine food webs.</p>
            </div>

            <!-- DUPLICATE SET FOR INFINITE LOOP -->
            <div class="carousel-card">
                <h4>🌊 Rising Sea Levels</h4>
                <p><b>Impact:</b> Thermal expansion & glacier melt cause sea level rise.<br><br><b>Consequence:</b> Displaces coastal communities and accelerates land erosion.</p>
            </div>
            <div class="carousel-card">
                <h4>🔥 Extreme Weather</h4>
                <p><b>Impact:</b> Atmospheric warming traps intense heat and moisture.<br><br><b>Consequence:</b> Causes prolonged droughts, wildfires, and violent storms.</p>
            </div>
            <div class="carousel-card">
                <h4>🌾 Food & Water Security</h4>
                <p><b>Impact:</b> Erratic rainfall disrupts global agricultural cycles.<br><br><b>Consequence:</b> Reduces global crop yields and increases water scarcity.</p>
            </div>
            <div class="carousel-card">
                <h4>🏜️ Ecosystem Loss</h4>
                <p><b>Impact:</b> Oceans absorb excess CO₂, driving acidification.<br><br><b>Consequence:</b> Bleaches coral reefs and disrupts marine food webs.</p>
            </div>
        </div>
    </div>

    </body>
    </html>
    """

    # Render with matching height frame
    components.html(carousel_html, height=225)
    st.markdown("---")
    st.markdown(
        "**Use the navigation menu above to explore interactive dashboards, maps, and reports.**"
    )

# =============================================================================
# PAGE 1: EXECUTIVE SUMMARY  (INTERACTIVE / CROSS-FILTERED)
# =============================================================================
elif selected_tab == "📊 Executive Summary":

    # --- SESSION STATE INIT ---
    st.session_state.setdefault("focus_country", None)
    focus_country = st.session_state.focus_country
    latest_sel_year = selected_year_range[1]

    # --- STYLING: REMOVE DOUBLE BORDERS & APPLY BLUE HOVER GLOW ---
    st.markdown(
        """
        <style>
            /* Completely strip Streamlit's default nested container borders */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: none !important;
                box-shadow: none !important;
            }

            /* Single Outer Rectangle */
            div[class*="st-key-exec_summary_box"] {
                background-color: var(--background-secondary, rgba(2, 132, 199, 0.03)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 16px !important;
                padding: 24px !important;
                margin-top: 10px !important;
                margin-bottom: 20px !important;
            }

            /* Single Inner Metric & Chart Cards */
            div[class*="st-key-kpi_square_"],
            div[class*="st-key-chart_card_"] {
                background-color: var(--background-primary, rgba(255, 255, 255, 0.04)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 10px !important;
                padding: 16px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            /* Card Hover Effects: Elevation Lift + Glowing Shadow */
            div[class*="st-key-kpi_square_"]:hover,
            div[class*="st-key-chart_card_"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 10px 20px -4px rgba(2, 132, 199, 0.4) !important;
            }

            /* KPI Typography adjustments */
            div[class*="st-key-kpi_square_"] [data-testid="stMetricValue"] {
                font-size: clamp(1.1rem, 1.4vw, 1.5rem) !important;
                font-weight: 700 !important;
                color: var(--text-color, inherit) !important;
            }

            div[class*="st-key-kpi_square_"] [data-testid="stMetricLabel"] {
                font-size: clamp(0.75rem, 0.9vw, 0.88rem) !important;
                color: var(--text-color, inherit) !important;
                opacity: 0.85;
            }

            /* Reset Button Styling with Matching Hover Shadow */
            div[class*="st-key-exec_reset_btn"] button {
                border: 1.5px solid #0284c7 !important;
                border-radius: 8px !important;
                font-weight: 600 !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            div[class*="st-key-exec_reset_btn"] button:hover {
                transform: translateY(-3px) !important;
                border-color: #0284c7 !important;
                box-shadow: 0 8px 16px -4px rgba(2, 132, 199, 0.45) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Helper function to remove grid lines and adjust backgrounds cleanly across themes
    def clean_chart_layout(fig, height=280):
        fig.update_layout(
            height=height,
            margin=dict(l=10, r=10, t=25, b=10),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False),
            hovermode="closest",
            hoverlabel=dict(
                font_size=14,
                font_family="Arial",
                bgcolor="rgba(15, 23, 42, 0.95)",
                bordercolor="#0284c7",
            ),
        )
        fig.update_traces(
            hovertemplate="<b>%{fullData.name}</b><br>Value: %{y:,.1f}<extra></extra>"
        )
        return fig

    # --- OUTER CONTAINER FOR THE ENTIRE PAGE ---
    with st.container(key="exec_summary_box"):

        st.markdown("### Executive Summary & High-Level KPIs")
        st.caption(
            "Global metrics and high-level totals based on selected time range."
        )
        st.markdown("<br>", unsafe_allow_html=True)

        # --- FOCUS / RESET CONTROL BAR ---
        ctrl_col1, ctrl_col2 = st.columns([1.2, 4.8])
        with ctrl_col1:
            st.markdown('<div class="st-key-exec_reset_btn">', unsafe_allow_html=True)
            if st.button(
                "🔄 Reset View",
                use_container_width=True,
                disabled=(focus_country is None),
            ):
                st.session_state.focus_country = None
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with ctrl_col2:
            if focus_country:
                st.success(
                    f"🔎 Drilled into **{focus_country}**. Click another bar to switch, or Reset to return to Global view."
                )
            else:
                st.info(
                    "👆 Click any bar in the chart below — KPIs and charts will filter to that country."
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # --- RESOLVE KPI VALUES BASED ON FOCUS STATE ---
        if focus_country:
            focus_row = country_df[
                (country_df["country"] == focus_country)
                & (country_df["year"] == latest_sel_year)
            ]
            if not focus_row.empty:
                kpi_co2 = focus_row["co2"].values[0]
                kpi_coal = focus_row["coal_co2"].values[0]
                kpi_percap = focus_row["co2_per_capita"].values[0]
            else:
                kpi_co2, kpi_coal, kpi_percap = 0.0, 0.0, 0.0
            kpi_label = focus_country
        else:
            world_latest_df = raw_df[
                (raw_df["country"] == "World")
                & (raw_df["year"] == latest_sel_year)
            ]
            if not world_latest_df.empty:
                kpi_co2 = world_latest_df["co2"].values[0]
                kpi_coal = world_latest_df["coal_co2"].values[0]
                kpi_percap = world_latest_df["co2_per_capita"].values[0]
            else:
                kpi_co2, kpi_coal, kpi_percap = 0.0, 0.0, 0.0
            kpi_label = "Global"

        # --- KPI ROW: 3 SINGLE CARDS ---
        kcol1, kcol2, kcol3 = st.columns(3)
        with kcol1:
            with st.container(key="kpi_square_1"):
                st.metric(
                    label=f"CO₂ Output — {kpi_label} ({latest_sel_year})",
                    value=f"{kpi_co2:,.1f} Mt",
                    help="Total million tonnes of CO₂ produced."
                )   

        with kcol2:
            with st.container(key="kpi_square_2"):
                st.metric(
                    label=f"Coal CO₂ — {kpi_label} ({latest_sel_year})",
                    value=f"{kpi_coal:,.1f} Mt",
                    help="Emissions specifically originating from coal combustion."
                )

        with kcol3:
            with st.container(key="kpi_square_3"):
                st.metric(
                    label=f"Per Capita — {kpi_label}",
                    value=f"{kpi_percap:,.2f} t",
                    help="Average metric tonnes of CO₂ emitted per person."
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # --- CHART 1: TOP 10 EMITTERS ---
        st.markdown(f"#### Top 10 CO₂ Emitting Nations in {latest_sel_year}")

        top10_df = (
            country_df[country_df["year"] == latest_sel_year]
            .sort_values(by="co2", ascending=False)
            .head(10)
        )

        if not top10_df.empty:
            with st.container(key="chart_card_top10"):
                fig_top10 = px.bar(
                    top10_df,
                    x="co2",
                    y="country",
                    orientation="h",
                    text="co2",
                    labels={"co2": "CO₂ Emissions (Mt)", "country": ""},
                    color="co2",
                    color_continuous_scale=RED_GLOW_BARS,
                    template="plotly_white",
                )

                fig_top10 = clean_chart_layout(fig_top10, height=280)
                fig_top10.update_layout(
                    yaxis=dict(autorange="reversed"),
                    coloraxis_showscale=False,
                    hovermode="closest",
                )

                fig_top10.update_traces(
                    texttemplate="%{text:.1f}",
                    textposition="outside",
                    hovertemplate="<b>%{y}</b><br>CO₂: %{x:,.1f} Mt<extra></extra>",
                )

                top10_event = st.plotly_chart(
                    fig_top10,
                    use_container_width=True,
                    on_select="rerun",
                    selection_mode="points",
                    key="top10_bar_chart",
                )

                if top10_event and top10_event.get("selection", {}).get("points"):
                    clicked_point = top10_event["selection"]["points"][0]
                    clicked_country = clicked_point.get("y")
                    if (
                        clicked_country
                        and clicked_country != st.session_state.focus_country
                    ):
                        st.session_state.focus_country = clicked_country
                        st.rerun()

                st.caption(
                    "Click a bar to drill down into that country. Click **Reset View** above to clear filters."
                )
        else:
            st.info("No data available for selected parameters.")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- CHART 2 & 3: TREND LINE + FUEL MIX ---
        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            with st.container(key="chart_card_trend"):
                if focus_country:
                    st.markdown(f"**📈 {focus_country} vs. World Trend**")
                    trend_country_df = country_df[
                        (country_df["country"] == focus_country)
                        & (
                            country_df["year"].between(
                                selected_year_range[0], selected_year_range[1]
                            )
                        )
                    ][["year", "co2"]].copy()
                    trend_country_df["Series"] = focus_country

                    trend_world_df = raw_df[
                        (raw_df["country"] == "World")
                        & (
                            raw_df["year"].between(
                                selected_year_range[0], selected_year_range[1]
                            )
                        )
                    ][["year", "co2"]].copy()
                    trend_world_df["Series"] = "World"

                    trend_plot_df = pd.concat(
                        [trend_country_df, trend_world_df]
                    )
                else:
                    st.markdown("**📈 Selected Countries Trend**")
                    trend_plot_df = filtered_country_df.rename(
                        columns={"country": "Series"}
                    )

                if not trend_plot_df.empty:
                    fig_trend = px.line(
                        trend_plot_df,
                        x="year",
                        y="co2",
                        color="Series",  # Added line coloring mapping by country/series name
                        color_discrete_sequence=MULTI_GLOW_LINE_PALETTE,  # Swapped to multi-glow palette
                        markers=True,
                        labels={
                            "co2": "CO₂ (Mt)",
                            "year": "Year",
                            "Series": "",
                        },
                        template="plotly_white",
                    )
                    fig_trend = clean_chart_layout(fig_trend, height=280)
                
                    # Transparent background override for dark/light mode responsiveness
                    fig_trend.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        hovermode="closest",
                        legend=dict(
                            orientation="v",
                            yanchor="top",
                            y=1.0,
                            xanchor="left",
                            x=1.02,
                            font=dict(size=10),
                        ),
                        margin=dict(l=10, r=120, t=20, b=10),
                    )

                    fig_trend.update_traces(
                        line=dict(width=2.5),
                        marker=dict(size=6),
                        hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>CO₂: %{y:,.1f} Mt<extra></extra>"
                    )
                    st.plotly_chart(
                        fig_trend,
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )
                else:
                    st.info("No trend data available.")

        with chart_col2:
            with st.container(key="chart_card_fuel"):
                fuel_label = focus_country if focus_country else "World"
                st.markdown(f"**🔥 Fuel Mix — {fuel_label} ({latest_sel_year})**")
                

                fuel_sources = [
                    "coal_co2",
                    "oil_co2",
                    "gas_co2",
                    "flaring_co2",
                    "cement_co2",
                ]

                if focus_country:
                    fuel_row = country_df[
                        (country_df["country"] == focus_country)
                        & (country_df["year"] == latest_sel_year)
                    ]
                else:
                    fuel_row = raw_df[
                        (raw_df["country"] == "World")
                        & (raw_df["year"] == latest_sel_year)
                    ]

                if not fuel_row.empty:
                    fuel_vals = {}
                    for src in fuel_sources:
                        label = src.replace("_co2", "").capitalize()
                        val = (
                            fuel_row[src].values[0]
                            if src in fuel_row.columns
                            else 0
                        )
                        fuel_vals[label] = val if pd.notna(val) else 0

                    fuel_pie_df = pd.DataFrame(
                        {
                            "Source": ["Oil", "Coal", "Gas", "Cement", "Flaring"],
                            "Emissions": [
                                fuel_vals.get("Oil", 0),
                                fuel_vals.get("Coal", 0),
                                fuel_vals.get("Gas", 0),
                                fuel_vals.get("Cement", 0),
                                fuel_vals.get("Flaring", 0),
                            ],
                        }
                    )
                    fuel_pie_df = fuel_pie_df[fuel_pie_df["Emissions"] > 0]

                    if not fuel_pie_df.empty:
                        fig_fuel_pie = px.pie(
                            fuel_pie_df,
                            names="Source",
                            values="Emissions",
                            hole=0.40,  # Slightly tighter hole so donut ring looks fuller
                            color="Source",
                            color_discrete_map=RED_FUEL_MAP,
                            template="plotly_white",
                        )

                        # Tooltip, inside labels, and dark/light responsive styling
                        fig_fuel_pie.update_traces(
                            textinfo="percent+label",
                            textposition="inside",
                            hovertemplate="<b>%{label}</b><br>Emissions: %{value:,.2f} Mt<br>Share: %{percent}<extra></extra>",
                        )

                        # Transparent background & tight margins to maximize chart circle size
                        fig_fuel_pie.update_layout(
                            showlegend=False,
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            margin=dict(t=10, b=10, l=10, r=10),
                            height=280,
                        )

                        # Single responsive render call
                        st.plotly_chart(
                            fig_fuel_pie,
                            use_container_width=True,
                            config={"displayModeBar": False},
                        )
                    else:
                        st.info("No fuel-mix data available.")
                else:
                    st.info("No fuel-mix data available.")
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-top: 15px;
            margin-bottom: 25px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Top 10 Emitters</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Ranks the highest absolute CO₂ producing nations globally for the selected snapshot year, measured in Megatonnes (Mt).<br>
                <b>User Takeaway:</b> Identifies macroeconomic emission concentration, showing which core industrial economies generate the largest share of global carbon output. Click any bar to cross-filter the remaining dashboard metrics to that specific nation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
                """
                <div style="
                    background: var(--background-secondary, rgba(2, 132, 199, 0.05));
                    border: 2px solid #0284c7;
                    border-radius: 10px;
                    padding: 16px 20px;
                    margin-top: 15px;
                    margin-bottom: 25px;
                    box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
                    color: var(--text-color, inherit);
                ">
                    <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                        💡 <span>Chart Purpose & Data Guide: Trajectory Trends</span>
                    </h5>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                        <b>What this shows:</b> Tracks multi-decade historical CO₂ emission trajectories across selected comparison countries.<br>
                        <b>User Takeaway:</b> Helps observe historical acceleration, stabilization, or decline phases to compare national economic transitions over long horizons.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown(
                """
                <div style="
                    background: var(--background-secondary, rgba(2, 132, 199, 0.05));
                    border: 2px solid #0284c7;
                    border-radius: 10px;
                    padding: 16px 20px;
                    margin-top: 15px;
                    margin-bottom: 25px;
                    box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
                    color: var(--text-color, inherit);
                ">
                    <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                        💡 <span>Chart Purpose & Data Guide: Fuel Breakdown</span>
                    </h5>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                        <b>What this shows:</b> Illustrates the proportional share of carbon emissions categorized by primary energy source (Coal, Oil, Gas, Flaring, Cement).<br>
                        <b>User Takeaway:</b> Highlights whether emissions are heavily driven by power generation, transportation fuel, or heavy industry.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

# =============================================================================
# PAGE 2: COUNTRY TRENDS & COMPARATIVE ANALYSIS
# =============================================================================
elif selected_tab == "📈 Country Trends":

    # --- CLEAN SINGLE-BORDER SCOPED CSS WITH HOVER EFFECTS ---
    st.markdown(
        """
        <style>
            /* Strip default Streamlit container nested borders */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: none !important;
                box-shadow: none !important;
            }

            /* Single Outer Wrapper Box */
            div[class*="st-key-trends_outer_box"] {
                background-color: var(--background-secondary, rgba(2, 132, 199, 0.03)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 16px !important;
                padding: 24px !important;
                margin-top: 10px !important;
                margin-bottom: 20px !important;
            }

            /* Single Inner Chart & Table Cards */
            div[class*="st-key-trends_inner_card"] {
                background-color: var(--background-primary, rgba(255, 255, 255, 0.04)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 12px !important;
                padding: 16px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            /* Card Hover Effects: Elevation Lift + Glowing Shadow */
            div[class*="st-key-trends_inner_card"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 10px 20px -4px rgba(2, 132, 199, 0.4) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Section Header
    st.header("📈 Country-Level Emissions Trends")
    st.caption("Compare historical emissions across selected nations over time.")
    st.markdown("<br>", unsafe_allow_html=True)

    # --- TOP SECTION: Annual Trajectory Chart ---
    with st.container(key="trends_outer_box_1"):
        st.subheader("Annual CO₂ Emissions Trajectory (Million Tonnes)")
        st.markdown("<br>", unsafe_allow_html=True)

        with st.container(key="trends_inner_card_1"):
            fig_line = px.line(
                filtered_country_df,
                x="year",
                y="co2",
                color="country",
                markers=True,
                labels={"co2": "CO₂ Emissions (Mt)", "year": "Year"},
                template="plotly_white",
            )
            fig_line.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20),
                legend_title_text="Country",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False),
            )
            st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BOTTOM SECTION: Cumulative Bar & Summary Table Grid ---
    with st.container(key="trends_outer_box_2"):
        num_countries = len(filtered_country_df["country"].unique())

        # Aggregate Data Calculations
        cum_df = (
            filtered_country_df.groupby("country")["co2"].sum().reset_index()
        )

        stats_df = (
            filtered_country_df.groupby("country")["co2"]
            .agg(Avg_Mt="mean", Peak_Mt="max", Min_Mt="min")
            .reset_index()
            .round(1)
        )
        stats_df.columns = ["Country", "Avg (Mt)", "Peak (Mt)", "Min (Mt)"]

        # CONDITION 1: Stacked Layout with Horizontal Bars for Large Selections (> 10 countries)
        if num_countries > 10:
            st.subheader("Cumulative Emissions")
            with st.container(key="trends_inner_card_2"):
                cum_df_sorted = cum_df.sort_values(by="co2", ascending=True)

                fig_bar = px.bar(
                    cum_df_sorted,
                    x="co2",
                    y="country",
                    color="co2",
                    color_discrete_sequence=MULTI_GLOW_LINE_PALETTE,
                    orientation="h",
                    labels={"co2": "Total CO₂ (Mt)", "country": "Country"},
                    template="plotly_white",
                )

                fig_bar.update_traces(
                    marker_line_width=0,
                    width=0.6,
                    hovertemplate="<b>%{y}</b><br>Total CO₂: %{x:+1,.1f} Mt<extra></extra>",
                )
                fig_bar.update_layout(
                    height=max(450, num_countries * 28),
                    showlegend=False,
                    margin=dict(l=10, r=20, t=20, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=True, zeroline=False, gridcolor="rgba(128,128,128,0.2)"),
                    yaxis=dict(showgrid=False, zeroline=False),
                )

                st.plotly_chart(
                    fig_bar, use_container_width=True, config={"displayModeBar": False}
                )

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader("Statistical Summary")
            with st.container(key="trends_inner_card_3"):
                st.caption("Summary metrics for the selected time range:")
                st.dataframe(
                    stats_df, use_container_width=True, hide_index=True
                )

        # CONDITION 2: Side-by-Side Grid Layout for Small Selections (<= 10 countries)
        else:
            col_left, col_right = st.columns(2)

            with col_left:
                st.subheader("Cumulative Emissions")
                with st.container(key="trends_inner_card_2"):
                    fig_bar = px.bar(
                        cum_df,
                        x="country",
                        y="co2",
                        color="co2",
                        color_continuous_scale="Viridis",
                        labels={"co2": "Total CO₂ (Mt)", "country": "Country"},
                        template="plotly_white",
                    )
                    fig_bar.update_layout(
                        height=360,
                        margin=dict(l=10, r=10, t=20, b=10),
                        showlegend=False,
                        coloraxis_showscale=False,
                        bargap=0.3,
                        xaxis=dict(
                            title="",
                            categoryorder="total descending",
                            tickangle=-30,
                            automargin=True,
                            tickfont=dict(size=11),
                            showgrid=False,
                        ),
                        yaxis=dict(title="Total CO₂ (Mt)", showgrid=False),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                    )
                    st.plotly_chart(
                        fig_bar,
                        use_container_width=True,
                        config={"displayModeBar": False, "responsive": True},
                    )

            with col_right:
                st.subheader("Statistical Summary")
                with st.container(key="trends_inner_card_3"):
                    st.caption("Summary metrics for the selected time range:")
                    st.dataframe(
                        stats_df,
                        use_container_width=True,
                        hide_index=True,
                        height=280,
                    )
    # ==============================================================================
    # 📍 COUNTRY TRENDS TAB: STACKED INDIVIDUAL FULL-WIDTH GUIDES (Below Main Box)
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)

    # --- GUIDE 1: ANNUAL CO2 EMISSIONS TRAJECTORY ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-top: 15px;
            margin-bottom: 20px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Annual CO₂ Emissions Trajectory</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Tracks annual historical emissions (in Megatonnes) across selected comparison nations from 1990 to the present.<br>
                <b>User Takeaway:</b> Reveals structural trends over time, helping users distinguish between rapidly industrializing developing nations with rising growth slopes versus post-industrial economies showing declining or stabilized emissions trends.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- GUIDE 2: CUMULATIVE EMISSIONS ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Cumulative Emissions</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Aggregates the total volume of CO₂ emitted by each selected country over the entire chosen timeframe.<br>
                <b>User Takeaway:</b> Evaluates historical responsibility and long-term carbon debt. Because CO₂ persists in the atmosphere for decades, total cumulative volume provides a clearer metric for historical climate impact than single-year snapshots.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- GUIDE 3: STATISTICAL SUMMARY TABLE ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 25px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Statistical Summary</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Provides key descriptive metrics (Average, Peak historical emissions, and Minimum emissions) for each nation in the selected range.<br>
                <b>User Takeaway:</b> Offers precise numerical reference values for analytical comparison. Users can evaluate how far current emission levels deviate from a nation's historical peak or average annual output.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# PAGE 3: GLOBAL DISTRIBUTION MAP
# =============================================================================
elif selected_tab == "🗺️ Global Map":

    # --- CLEAN SINGLE-BORDER SCOPED CSS WITH HOVER EFFECTS ---
    st.markdown(
        """
        <style>
            /* Strip default Streamlit container nested borders */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: none !important;
                box-shadow: none !important;
            }

            /* Single Outer Wrapper Box */
            div[class*="st-key-spatial_main_card"] {
                background-color: var(--background-secondary, rgba(2, 132, 199, 0.03)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 16px !important;
                padding: 24px !important;
                margin-top: 10px !important;
                margin-bottom: 20px !important;
            }

            /* Dedicated Inner Map Card & Rankings Card */
            div[class*="st-key-spatial_map_wrapper"],
            div[class*="st-key-spatial_rankings_card"] {
                background-color: var(--background-primary, rgba(255, 255, 255, 0.04)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 12px !important;
                padding: 16px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            /* Card Hover Effects: Elevation Lift + Glowing Shadow */
            div[class*="st-key-spatial_map_wrapper"]:hover,
            div[class*="st-key-spatial_rankings_card"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 10px 20px -4px rgba(2, 132, 199, 0.4) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## 🗺️ Global CO₂ Spatial Distribution")
    st.caption(
        "Geographic representation of emissions, economic indicators, and fuel metrics across all world nations."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    # Main Card Wrapping Controls and Map
    with st.container(key="spatial_main_card"):
        map_col1, map_col2 = st.columns([1.2, 3.8])

        with map_col1:
            st.markdown("##### 🎛️ Map Controls")

            metric_options = {
                "Total CO₂ (Mt)": "co2",
                "Per Capita CO₂ (Tonnes)": "co2_per_capita",
                "Coal CO₂ (Mt)": "coal_co2",
                "Gross Domestic Product ($)": "gdp",
            }

            selected_label = st.selectbox(
                "Select Map Metric", list(metric_options.keys())
            )
            selected_metric = metric_options[selected_label]

            selected_map_year = st.slider(
                "Select Map Year",
                min_value=1950,
                max_value=2024,
                value=2024,
                step=1,
            )

        # Filter Data for Selected Year
        map_df = country_df[
            (country_df["year"] == selected_map_year)
            & (country_df["country"] != "World")
        ].copy()

        # GDP Fallback handling
        if selected_metric == "gdp" and (
            selected_metric not in map_df.columns
            or map_df[selected_metric].dropna().empty
        ):
            st.warning(
                f"⚠️ GDP data for {selected_map_year} is unavailable in this dataset. Displaying latest available record."
            )

        with map_col2:
            # Dedicated Card Container around Map
            with st.container(key="spatial_map_wrapper"):
                if not map_df.empty and selected_metric in map_df.columns:
                    fig_map = px.choropleth(
                        map_df,
                        locations="iso_code",
                        color="co2",
                        hover_name="country",
                        color_continuous_scale=["#FFEDD5", "#FCA5A5", "#EF4444", "#991B1B"], # Uniform Red Glow
                        range_color=(0, map_df["co2"].quantile(0.95)),
                        projection="natural earth",
                        template="plotly_white",
                    )

                    fig_map.update_layout(
                        margin=dict(l=0, r=0, t=30, b=0),
                        height=420,
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        geo=dict(
                            showframe=False,
                            showcoastlines=True,
                            bgcolor="rgba(0,0,0,0)",
                            landcolor="rgba(128, 128, 128, 0.15)",
                            coastlinecolor="rgba(2, 132, 199, 0.4)",
                        ),
                    )

                    fig_map.update_traces(
                        hovertemplate="<b>%{hovertext}</b><br>"
                        + f"{selected_label}: "
                        + "%{z:,.1f}<extra></extra>"
                    )

                    st.plotly_chart(fig_map, use_container_width=True)
                else:
                    st.info("No spatial data available for the chosen parameters.")

    st.markdown("<br>", unsafe_allow_html=True)

    # TOP 5 RANKINGS CARD AT THE BOTTOM
    with st.container(key="spatial_rankings_card"):
        st.markdown(
            f"##### 📊 Top 5 Nations by {selected_label} ({selected_map_year})"
        )

        if not map_df.empty and selected_metric in map_df.columns:
            top_spatial_df = (
                map_df.dropna(subset=[selected_metric])
                .sort_values(by=selected_metric, ascending=False)
                .head(5)[["country", selected_metric]]
                .reset_index(drop=True)
            )
            top_spatial_df.columns = ["Nation", selected_label]

            st.dataframe(
                top_spatial_df, use_container_width=True, hide_index=True
            )
        else:
            st.info("No spatial data available for this year.")
    # ==============================================================================
    # 📍 GLOBAL MAP TAB: STACKED INDIVIDUAL FULL-WIDTH GUIDES (Below Main Boxes)
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)

    # --- GUIDE 1: GLOBAL SPATIAL MAP ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-top: 15px;
            margin-bottom: 20px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Global CO₂ Spatial Distribution</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Visualizes worldwide spatial distribution of carbon metrics using a choropleth map across all countries for any selected year from 1950 to the present.<br>
                <b>User Takeaway:</b> Highlights geographic concentration and regional disparities in emissions. Adjusting the metric control allows direct switching between absolute volume, economic intensity, and per capita views.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- GUIDE 2: TOP 5 NATIONS TABLE ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 25px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Top 5 Nations Ranking</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Extracts a clean, ranked summary table of the five highest emitting nations for the currently selected spatial map year.<br>
                <b>User Takeaway:</b> Provides exact numeric baseline values for quick quantitative comparison alongside the spatial map without requiring visual color estimates.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# PAGE 4: FUEL BREAKDOWN
# =============================================================================
elif selected_tab == "🔌 Fuel Breakdown":

    # --- CLEAN SINGLE-BORDER SCOPED CSS WITH HOVER EFFECTS ---
    st.markdown(
        """
        <style>
            /* Strip default Streamlit container nested borders */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: none !important;
                box-shadow: none !important;
            }

            /* Single Outer Wrapper Box */
            div[class*="st-key-fuel_main_card"] {
                background-color: var(--background-secondary, rgba(2, 132, 199, 0.03)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 16px !important;
                padding: 24px !important;
                margin-top: 10px !important;
                margin-bottom: 20px !important;
            }

            /* Single Inner Chart Cards */
            div[class*="st-key-fuel_inner_card_"] {
                background-color: var(--background-primary, rgba(255, 255, 255, 0.04)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 12px !important;
                padding: 16px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            /* Card Hover Effects: Elevation Lift + Glowing Shadow */
            div[class*="st-key-fuel_inner_card_"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 10px 20px -4px rgba(2, 132, 199, 0.4) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## 🔌 Fuel Source & Sectoral Analysis")
    st.caption(
        "Examine the carbon contribution breakdown across Coal, Oil, Gas, Cement, and Gas Flaring."
    )
    st.markdown("<br>", unsafe_allow_html=True)

    fuel_year = selected_year_range[1]

    # --- MAIN OUTER CONTAINER ---
    with st.container(key="fuel_main_card"):

        # --- SELECTION SLICER / FILTER ---
        available_entities = sorted(country_df["country"].dropna().unique().tolist())
        default_entity = "World" if "World" in available_entities else available_entities[0]

        selected_fuel_entity = st.selectbox(
            "🎯 Select Country / Entity for Fuel Breakdown Analysis:",
            options=available_entities,
            index=available_entities.index(default_entity)
            if default_entity in available_entities
            else 0,
            key="fuel_entity_slicer",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # Filter dataset dynamically based on selected entity
        entity_fuel_df = country_df[country_df["country"] == selected_fuel_entity].copy()

        fuel_cols = ["coal_co2", "oil_co2", "gas_co2", "flaring_co2", "cement_co2"]
        fuel_labels = {
            "coal_co2": "Coal",
            "oil_co2": "Oil",
            "gas_co2": "Gas",
            "flaring_co2": "Flaring",
            "cement_co2": "Cement",
        }

        chart_col1, chart_col2 = st.columns(2)

        # LEFT CHART: Fuel Distribution Donut Chart for Selected Entity & Year
        with chart_col1:
            with st.container(key="fuel_inner_card_1"):
                st.markdown(f"####  {selected_fuel_entity} Share ({fuel_year})")

                fuel_df_year = entity_fuel_df[entity_fuel_df["year"] == fuel_year]
                
                if not fuel_df_year.empty:
                    fuel_totals = fuel_df_year[fuel_cols].sum().reset_index()
                    fuel_totals.columns = ["Source_Key", "Emissions"]
                    fuel_totals["Source"] = fuel_totals["Source_Key"].map(fuel_labels)
                else:
                    fuel_totals = pd.DataFrame()

                if not fuel_totals.empty and fuel_totals["Emissions"].sum() > 0:
                    fig_fuel_donut = px.pie(
                        fuel_totals,
                        names="Source",
                        values="Emissions",
                        hole=0.45,
                        template="plotly_white",
                        color="Source",
                        color_discrete_map={
                            "Coal": "#333333",
                            "Oil": "#D9534F",
                            "Gas": "#5BC0DE",
                            "Flaring": "#F0AD4E",
                            "Cement": "#8E8E8E",
                        },
                    )
                    fig_fuel_donut.update_layout(
                        height=420,
                        margin=dict(l=20, r=20, t=30, b=90),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=-0.18,
                            xanchor="center",
                            x=0.5,
                        ),
                    )
                    fig_fuel_donut.update_traces(
                        textinfo="percent+label",textposition="inside",
                        hovertemplate="<b>%{label}</b><br>Emissions: %{value:,.1f} Mt<br>Share: %{percent}<extra></extra>",
                    )
                    st.plotly_chart(
                        fig_fuel_donut,
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )
                else:
                    st.info(
                        f"No breakdown data available for {selected_fuel_entity} in {fuel_year}."
                    )

        # RIGHT CHART: Historical Stacked Area Chart for Selected Entity
        with chart_col2:
            with st.container(key="fuel_inner_card_2"):
                st.markdown(f"#### 📈 {selected_fuel_entity} Evolution Over Time")

                hist_fuel_df = entity_fuel_df[
                    (entity_fuel_df["year"] >= selected_year_range[0])
                    & (entity_fuel_df["year"] <= selected_year_range[1])
                ]

                if not hist_fuel_df.empty:
                    hist_fuel_melted = hist_fuel_df.melt(
                        id_vars=["year"],
                        value_vars=fuel_cols,
                        var_name="Source_Key",
                        value_name="Emissions",
                    )
                    hist_fuel_melted["Source"] = hist_fuel_melted["Source_Key"].map(fuel_labels)
                else:
                    hist_fuel_melted = pd.DataFrame()

                if not hist_fuel_melted.empty and hist_fuel_melted["Emissions"].sum() > 0:
                    fig_fuel_area = px.area(
                        hist_fuel_melted,
                        x="year",
                        y="Emissions",
                        color="Source",
                        labels={"Emissions": "CO₂ (Mt)", "year": "Year"},
                        template="plotly_white",
                        color_discrete_map={
                            "Coal": "#333333",
                            "Oil": "#D9534F",
                            "Gas": "#5BC0DE",
                            "Flaring": "#F0AD4E",
                            "Cement": "#8E8E8E",
                        },
                    )
                    fig_fuel_area.update_layout(
                        height=400,
                        margin=dict(l=20, r=20, t=80, b=40),
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        xaxis=dict(
                            title=dict(text="Year", standoff=15)  # Add clear spacing to X-axis label
                        ),
                        yaxis=dict(showgrid=False, zeroline=False),
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1,
                        ),
                    )
                    fig_fuel_area.update_traces(
                        hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Emissions: %{y:,.1f} Mt<extra></extra>"
                    )
                    st.plotly_chart(
                        fig_fuel_area,
                        use_container_width=True,
                        config={"displayModeBar": False},
                    )
                else:
                    st.info(
                        f"No historical fuel data recorded for {selected_fuel_entity} across selected years."
                    )
    # ==============================================================================
    # 📍 FUEL BREAKDOWN TAB: STACKED INDIVIDUAL FULL-WIDTH GUIDES (Below Main Box)
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)

    # --- GUIDE 1: FUEL SHARE DONUT CHART ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-top: 15px;
            margin-bottom: 20px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Fuel Source Distribution</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Breaks down the chosen nation's carbon footprint by specific fossil fuel and industrial sources (Oil, Coal, Gas, Cement, Flaring) for the selected snapshot year.<br>
                <b>User Takeaway:</b> Pinpoints primary drivers of national emissions—distinguishing between heavy coal reliance (power generation), oil dominance (transportation), or natural gas reliance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- GUIDE 2: FUEL EVOLUTION STACKED AREA CHART ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 25px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Fuel Evolution Over Time</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Tracks how the absolute volume and proportional mix of energy sources have shifted historically across decades.<br>
                <b>User Takeaway:</b> Highlights national energy transition efforts, revealing whether a country is actively phasing out high-emission energy sources like coal in favor of cleaner alternatives or expanding overall fuel demand.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# =============================================================================
# PAGE 5: EQUITY & PER CAPITA ANALYSIS
# =============================================================================
elif selected_tab == "⚖️ Equity & Per Capita":

    # --- CLEAN SINGLE-BORDER SCOPED CSS WITH HOVER EFFECTS ---
    st.markdown(
        """
        <style>
            /* Strip default Streamlit container nested borders */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: none !important;
                box-shadow: none !important;
            }

            /* Main Card Wrappers */
            div[class*="st-key-equity_main_card"],
            div[class*="st-key-explorer_main_card"] {
                background-color: var(--background-secondary, rgba(2, 132, 199, 0.03)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 16px !important;
                padding: 24px !important;
                margin-top: 10px !important;
                margin-bottom: 20px !important;
            }

            /* Inner Containers, KPI Cards, and Section Cards */
            div[class*="st-key-equity_kpi_card_"],
            div[class*="st-key-card_equity_"],
            div[class*="st-key-explorer_inner_card"] {
                background-color: var(--background-primary, rgba(255, 255, 255, 0.04)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 12px !important;
                padding: 18px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            /* Card Hover Effects: Elevation Lift + Glowing Shadow */
            div[class*="st-key-equity_kpi_card_"]:hover,
            div[class*="st-key-card_equity_"]:hover,
            div[class*="st-key-explorer_inner_card"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 10px 20px -4px rgba(2, 132, 199, 0.4) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.header("⚖️ Climate Equity & Per Capita Analysis")
    st.caption("Examine emissions normalized by population size and trade consumption.")
    st.markdown("<br>", unsafe_allow_html=True)

    # Active countries filter logic
    active_countries = (
        selected_countries
        if selected_countries
        else ["China", "United States", "India", "Germany", "United Kingdom"]
    )

    equity_2024 = country_df[
        (country_df["year"] == 2024)
        & (country_df["country"].isin(active_countries))
    ].copy()

    # --- TOP KPI METRIC CARDS ---
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

    with kpi_col1:
        with st.container(key="equity_kpi_card_1"):
            avg_pc = (
                equity_2024["co2_per_capita"].mean()
                if not equity_2024.empty and "co2_per_capita" in equity_2024.columns
                else 0.0
            )
            st.metric(
                label="Selected Avg Per Capita (2024)",
                value=f"{avg_pc:.2f} t",
                delta="Metric Tonnes / Person",
            )

    with kpi_col2:
        with st.container(key="equity_kpi_card_2"):
            if not equity_2024.empty and "co2_per_capita" in equity_2024.columns:
                top_row = equity_2024.sort_values(by="co2_per_capita", ascending=False).iloc[0]
                top_nation = top_row["country"]
                top_val = top_row["co2_per_capita"]
            else:
                top_nation, top_val = "N/A", 0.0
            st.metric(
                label="Highest Selected Per Capita",
                value=f"{top_val:.2f} t",
                delta=f"Highest: {top_nation}",
            )

    with kpi_col3:
        with st.container(key="equity_kpi_card_3"):
            tot_pop = (
                equity_2024["population"].sum() / 1e6
                if not equity_2024.empty and "population" in equity_2024.columns
                else 0.0
            )
            st.metric(
                label="Combined Selected Population",
                value=f"{tot_pop:,.1f} M",
                delta="2024 Total",
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MAIN CONTENT WRAPPER ---
    with st.container(key="equity_main_card"):

        # CARD 1: Per Capita CO2 Bar Chart
        with st.container(key="card_equity_per_capita"):
            st.markdown("##### 📊 Per Capita CO₂ Emissions (2024)")

            if not equity_2024.empty and "co2_per_capita" in equity_2024.columns:
                fig_per_capita = px.bar(
                    equity_2024,
                    x="country",
                    y="co2_per_capita",
                    color="co2_per_capita",
                    color_continuous_scale="Viridis",
                    text_auto=".2f",
                    title="Metric Tonnes of CO₂ per Person in 2024",
                    labels={
                        "co2_per_capita": "CO₂ per Capita (Tonnes)",
                        "country": "Country",
                    },
                    template="plotly_white",
                )

                fig_per_capita.update_layout(
                    height=380,
                    coloraxis_showscale=False,
                    bargap=0.35,
                    xaxis=dict(
                        title="Country",
                        categoryorder="total descending",
                        tickangle=0,
                        showgrid=False,
                    ),
                    yaxis=dict(title="CO₂ per Capita (Tonnes)", showgrid=False),
                    margin=dict(l=50, r=40, t=40, b=40),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )

                fig_per_capita.update_traces(
                    textposition="outside",
                    hovertemplate="<b>%{x}</b><br>Per Capita CO₂: %{y:.2f} Tonnes<extra></extra>",
                    cliponaxis=False
                )

                st.plotly_chart(fig_per_capita, use_container_width=True)
            else:
                st.info("No per capita data available for selected nations in 2024.")

        st.markdown("<br>", unsafe_allow_html=True)

        # CARD 2: Production vs. Consumption CO2 (Trade-Adjusted)
        with st.container(key="card_equity_trade"):
            st.markdown("##### 📦 Production CO₂ vs. Consumption CO₂ (Trade-Adjusted)")
            st.caption(
                "**Production CO₂** measures emissions within domestic borders. **Consumption CO₂** adjusts for net trade (subtracting emissions from exported goods and adding imported goods)."
            )

            all_countries = sorted(
                country_df[country_df["country"] != "World"]["country"].unique()
            )
            trade_country = st.selectbox(
                "Select a Country to Analyze Trade-Adjusted Impact",
                all_countries,
                index=(
                    all_countries.index("India")
                    if "India" in all_countries
                    else 0
                ),
            )

            trade_df = country_df[country_df["country"] == trade_country].copy()

            if not trade_df.empty:
                trade_cols = {
                    "co2": "Production CO₂",
                    "consumption_co2": "Consumption CO₂",
                }

                trade_melted = trade_df.melt(
                    id_vars=["year"],
                    value_vars=[col for col in trade_cols.keys() if col in trade_df.columns],
                    var_name="Type_Raw",
                    value_name="CO2_Emissions",
                )
                trade_melted["Type"] = trade_melted["Type_Raw"].map(trade_cols)

                fig_trade = px.line(
                    trade_melted.dropna(subset=["CO2_Emissions"]),
                    x="year",
                    y="CO2_Emissions",
                    color="Type",
                    markers=True,
                    title=f"Production vs. Consumption CO₂ Trajectory for {trade_country}",
                    labels={"CO2_Emissions": "CO₂ Emissions (Mt)", "year": "Year"},
                    template="plotly_white",
                )

                fig_trade.update_layout(
                    height=380,
                    hovermode="x unified",
                    margin=dict(l=10, r=10, t=40, b=10),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False, zeroline=False),
                )

                st.plotly_chart(fig_trade, use_container_width=True)
            else:
                st.info("No trade-adjusted data available for this nation.")

    # ==============================================================================
    # 📍 EQUITY & PER CAPITA TAB: STACKED INDIVIDUAL FULL-WIDTH GUIDES (Below Main Box)
    # ==============================================================================
    st.markdown("<br>", unsafe_allow_html=True)

    # --- GUIDE 1: PER CAPITA SUMMARY METRICS ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-top: 15px;
            margin-bottom: 20px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Per Capita KPI Overview</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Summarizes key high-level population metrics across selected nations, including average per capita output, peak individual footprint, and combined population size.<br>
                <b>User Takeaway:</b> Establishes an baseline for global climate equity, showing how overall national emissions translate into per-person carbon footprints relative to total population size.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- GUIDE 2: PER CAPITA CO2 EMISSIONS BAR CHART ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Per Capita CO₂ Comparison</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Ranks nations by individual carbon footprint (measured in Metric Tonnes per person) for the snapshot year.<br>
                <b>User Takeaway:</b> Standardizes emissions by population size, demonstrating that nations with high absolute emissions may have lower individual carbon footprints than highly industrialized smaller nations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --- GUIDE 3: PRODUCTION VS. CONSUMPTION CO2 DUAL LINE CHART ---
    st.markdown(
        """
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.05));
            border: 2px solid #0284c7;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 25px;
            box-shadow: 0 0 14px rgba(2, 132, 199, 0.45);
            color: var(--text-color, inherit);
        ">
            <h5 style="margin: 0 0 8px 0; font-size: 1.05rem; color: #0284c7; display: flex; align-items: center; gap: 8px;">
                💡 <span>Chart Purpose & Data Guide: Trade-Adjusted (Production vs. Consumption)</span>
            </h5>
            <p style="margin: 0; font-size: 0.9rem; opacity: 0.92; line-height: 1.55;">
                <b>What this shows:</b> Compares territorial emissions (Production CO₂) with trade-adjusted emissions (Consumption CO₂), accounting for imported and exported embedded carbon.<br>
                <b>User Takeaway:</b> Uncovers carbon outsourcing dynamics—highlighting whether a nation is a net exporter of manufactured carbon goods or a net importer consuming products manufactured elsewhere.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# =============================================================================
# PAGE 6: DATA EXPLORER & EXPORT OPTIONS
# =============================================================================
elif selected_tab == "📁 Data Explorer":
    st.header("📁 Raw Data Explorer & CSV Export")
    st.markdown("Inspect underlying tabular data filtered by your sidebar selections.")
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not filtered_country_df.empty:
        # 1. Column Selection Picker
        all_columns = filtered_country_df.columns.tolist()
        default_cols = ['country', 'year', 'iso_code', 'co2', 'co2_per_capita', 'coal_co2', 'oil_co2', 'gas_co2', 'population', 'gdp']
        
        # Keep only defaults that exist in the loaded dataset
        valid_defaults = [c for c in default_cols if c in all_columns]
        
        selected_columns = st.multiselect(
            label="Select Dataset Columns to Display",
            options=all_columns,
            default=valid_defaults
        )
        
        # Display Interactive Dataframe
        view_df = filtered_country_df[selected_columns].sort_values(by=['country', 'year'], ascending=[True, False])
        st.dataframe(view_df, use_container_width=True, height=400)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 2. One-Click CSV Export Button
        @st.cache_data
        def convert_df_to_csv(df_to_convert):
            return df_to_convert.to_csv(index=False).encode('utf-8')
            
        csv_data = convert_df_to_csv(view_df)
        
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_data,
            file_name=f"co2_emissions_data_{selected_year_range[0]}_{selected_year_range[1]}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    else:
        st.warning("⚠️ Please select at least one country in the sidebar filters.")

# =============================================================================
# TAB: TAKE ACTION & SOLUTIONS
# =============================================================================
elif selected_tab == "💡 Take Action":

    # --- CLEAN SINGLE-BORDER SCOPED CSS WITH HOVER EFFECTS ---
    st.markdown(
        """
        <style>
            /* Strip default Streamlit container nested borders */
            [data-testid="stVerticalBlockBorderWrapper"] {
                border: none !important;
                box-shadow: none !important;
            }

            /* Single Outer Wrapper Box */
            div[class*="st-key-action_main_card"] {
                background-color: var(--background-secondary, rgba(2, 132, 199, 0.03)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 16px !important;
                padding: 24px !important;
                margin-top: 10px !important;
                margin-bottom: 20px !important;
            }

            /* Single Inner Action Cards */
            div[class*="st-key-action_inner_card_"] {
                background-color: var(--background-primary, rgba(255, 255, 255, 0.04)) !important;
                border: 1.5px solid #0284c7 !important;
                border-radius: 12px !important;
                padding: 20px !important;
                transition: transform 0.25s ease, box-shadow 0.25s ease !important;
            }

            /* Card Hover Effects: Elevation Lift + Glowing Shadow */
            div[class*="st-key-action_inner_card_"]:hover {
                transform: translateY(-4px) !important;
                box-shadow: 0 10px 20px -4px rgba(2, 132, 199, 0.4) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- OUTER MAIN CONTAINER ---
    with st.container(key="action_main_card"):
        st.markdown("## 💡 Climate Solutions & Individual Action")
        st.caption(
            "Addressing climate change requires systemic policy shifts alongside individual accountability."
        )
        st.markdown("<hr style='border: 0.5px solid rgba(2, 132, 199, 0.2); margin: 15px 0 25px 0;'>", unsafe_allow_html=True)

        col_left, col_right = st.columns(2)

        # LEFT COLUMN: Systemic & Policy Solutions
        with col_left:
            with st.container(key="action_inner_card_1"):
                st.markdown("### 🏛️ Systemic & Policy Solutions")
                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown(
                    """
                    * **Renewable Transition:** Accelerating grid adoption of solar, wind, and hydro power.
                    * **Carbon Pricing:** Implementing cap-and-trade systems or carbon taxes on industrial emitters.
                    * **Electrification:** Transitioning public transport and personal vehicles away from fossil fuels.
                    * **Reforestation:** Protecting native ecosystems and supporting natural carbon sinks.
                    """
                )

        # RIGHT COLUMN: Individual Steps
        with col_right:
            with st.container(key="action_inner_card_2"):
                st.markdown("### 👤 Individual Steps for Footprint Reduction")
                st.markdown("<br>", unsafe_allow_html=True)

                st.markdown(
                    """
                    * **Energy Efficiency:** Switch to high-efficiency LED lighting and smart thermostats.
                    * **Sustainable Transport:** Prioritize public transit, carpooling, or electric mobility.
                    * **Dietary Awareness:** Reduce food waste and lower consumption of carbon-intensive food sources.
                    * **Digital & Energy Audit:** Monitor personal electrical usage and reduce idle appliance draw.
                    """
                )
    st.markdown("---")

    st.markdown("### 🌿 CLIMATE ACTION PRECAUTIONS")
    st.caption("Hover over any card to pause scrolling and inspect practical steps.")

    action_carousel_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: transparent;
        }

        .carousel-container {
            width: 100%;
            overflow: hidden;
            position: relative;
            padding: 6px 0;
        }

        .carousel-track {
            display: flex;
            gap: 16px;
            width: max-content;
            animation: scroll-carousel 30s linear infinite;
        }

        .carousel-container:hover .carousel-track {
            animation-play-state: paused;
        }

        /* Square Card Styling with Tight Top Alignment */
        .carousel-card {
            width: 260px;
            height: 260px;
            flex-shrink: 0;
            background: var(--background-secondary, rgba(16, 185, 129, 0.07));
            border: 2px solid #10b981;
            border-radius: 14px;
            padding: 16px;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
            color: #10b981;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }

        .carousel-card h4 {
            margin: 0 0 8px 0;
            font-size: 1rem;
            color: #10b981;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .carousel-card p b {
            color: #10b981;
        }

        @keyframes scroll-carousel {
            0% { transform: translateX(0); }
            100% { transform: translateX(calc(-256px * 5)); }
        }
    </style>
    </head>
    <body>

    <div class="carousel-container">
        <div class="carousel-track">
            <!-- CARD 1 -->
            <div class="carousel-card">
                <h4>💡 Conserve Energy</h4>
                <p><b>Action:</b> Switch to LED bulbs & unplug idle devices.<br><br><b>Impact:</b> Reduces carbon emissions from fossil-fuel-based power plants.</p>
            </div>

            <!-- CARD 2 -->
            <div class="carousel-card">
                <h4>🚲 Sustainable Mobility</h4>
                <p><b>Action:</b> Use public transit, carpool, bike, or walk.<br><br><b>Impact:</b> Cuts down urban vehicle greenhouse gas emissions drastically.</p>
            </div>

            <!-- CARD 3 -->
            <div class="carousel-card">
                <h4>💧 Water Conservation</h4>
                <p><b>Action:</b> Fix leaks & practice mindful water usage daily.<br><br><b>Impact:</b> Preserves vital freshwater reserves and saves energy used for pumping.</p>
            </div>

            <!-- CARD 4 -->
            <div class="carousel-card">
                <h4>♻️ Zero Waste Lifestyle</h4>
                <p><b>Action:</b> Reduce single-use plastics, reuse, and recycle.<br><br><b>Impact:</b> Decreases landfill waste, methane release, and ocean pollution.</p>
            </div>

            <!-- CARD 5 -->
            <div class="carousel-card">
                <h4>🌳 Plant & Protect</h4>
                <p><b>Action:</b> Support local greenery, tree plantation & urban trails.<br><br><b>Impact:</b> Enhances biodiversity, lowers local temperatures, and absorbs CO₂.</p>
            </div>

            <!-- DUPLICATE SET FOR INFINITE LOOP -->
            <div class="carousel-card">
                <h4>💡 Conserve Energy</h4>
                <p><b>Action:</b> Switch to LED bulbs & unplug idle devices.<br><br><b>Impact:</b> Reduces carbon emissions from fossil-fuel-based power plants.</p>
            </div>
            <div class="carousel-card">
                <h4>🚲 Sustainable Mobility</h4>
                <p><b>Action:</b> Use public transit, carpool, bike, or walk.<br><br><b>Impact:</b> Cuts down urban vehicle greenhouse gas emissions drastically.</p>
            </div>
            <div class="carousel-card">
                <h4>💧 Water Conservation</h4>
                <p><b>Action:</b> Fix leaks & practice mindful water usage daily.<br><br><b>Impact:</b> Preserves vital freshwater reserves and saves energy used for pumping.</p>
            </div>
            <div class="carousel-card">
                <h4>♻️ Zero Waste Lifestyle</h4>
                <p><b>Action:</b> Reduce single-use plastics, reuse, and recycle.<br><br><b>Impact:</b> Decreases landfill waste, methane release, and ocean pollution.</p>
            </div>
            <div class="carousel-card">
                <h4>🌳 Plant & Protect</h4>
                <p><b>Action:</b> Support local greenery, tree plantation & urban trails.<br><br><b>Impact:</b> Enhances biodiversity, lowers local temperatures, and absorbs CO₂.</p>
            </div>
        </div>
    </div>

    </body>
    </html>
    """

    components.html(action_carousel_html, height=280)

# =============================================================================
# TAB: KNOWLEDGE QUIZ (DYNAMIC + FIXED AWARENESS)
# =============================================================================
elif "Knowledge Quiz" in selected_tab:
    st.markdown("<br>", unsafe_allow_html=True)

    # --- 1. FETCH DYNAMIC SIDEBAR FILTER VALUES ---
    current_country = st.session_state.get('selected_country', 'Global')
    slider_val = st.session_state.get('year_range_slider', (1990, 2024))

    # Extract start and end years from range slider
    if isinstance(slider_val, (tuple, list)) and len(slider_val) == 2:
        start_year, end_year = slider_val[0], slider_val[1]
    else:
        start_year, end_year = 1990, slider_val

    if isinstance(current_country, list):
        primary_country = current_country[0] if len(current_country) > 0 else "Global"
    else:
        primary_country = current_country

    # --- 2. MULTI-DASHBOARD GROUND TRUTH EXTRACTION ---
    # Simplified Options & Precise Matching Strings
    dash1_top_fuel = "Coal"
    dash2_trend = "Net Increase in annual emissions"
    dash3_rank = "Top 10 High-Emitting Contributor"
    dash4_dominant_share = "Coal emissions dominated over Gas"
    dash5_cumulative = "High Volume Cumulative Emissions (> 5,000 Mt)"
    dash6_per_capita_trend = "High Intensity (> 8 tonnes/person)"

    if 'df' in locals() and not df.empty:
        # DASHBOARD 1: Fuel Mix Dashboard (Selected Year Snapshot)
        q1_df = df[(df['country'] == primary_country) & (df['year'] == end_year)]
        fuel_cols = ['coal', 'oil', 'gas', 'flaring', 'cement']
        if not q1_df.empty and all(c in q1_df.columns for c in fuel_cols):
            fuels = q1_df.iloc[0][fuel_cols].dropna()
            if not fuels.empty and fuels.max() > 0:
                dash1_top_fuel = fuels.idxmax().capitalize()

        # DASHBOARD 2: Historical Trajectory Dashboard (Start Year vs End Year)
        q2_start_df = df[(df['country'] == primary_country) & (df['year'] == start_year)]
        q2_end_df = df[(df['country'] == primary_country) & (df['year'] == end_year)]
        if not q2_start_df.empty and not q2_end_df.empty and 'co2' in df.columns:
            co2_start = q2_start_df.iloc[0]['co2'] if not pd.isna(q2_start_df.iloc[0]['co2']) else 0
            co2_end = q2_end_df.iloc[0]['co2'] if not pd.isna(q2_end_df.iloc[0]['co2']) else 0
            if co2_end >= co2_start:
                dash2_trend = "Net Increase in annual emissions"
            else:
                dash2_trend = "Net Decrease in annual emissions"

        # DASHBOARD 3: Global Ranking & Spatial Map Dashboard
        q3_global_df = df[df['year'] == end_year].sort_values(by='co2', ascending=False)
        if not q3_global_df.empty and primary_country in q3_global_df['country'].values:
            top_10 = q3_global_df.head(10)['country'].tolist()
            if primary_country in top_10:
                dash3_rank = "Top 10 High-Emitting Contributor"
            else:
                dash3_rank = "Outside Top 10 High-Emitting Contributors"

        # DASHBOARD 4: Fuel Structural Ratio (Coal vs Gas Comparison Dashboard)
        if not q1_df.empty and 'coal' in q1_df.columns and 'gas' in q1_df.columns:
            c_val = q1_df.iloc[0]['coal'] if not pd.isna(q1_df.iloc[0]['coal']) else 0
            g_val = q1_df.iloc[0]['gas'] if not pd.isna(q1_df.iloc[0]['gas']) else 0
            if c_val >= g_val:
                dash4_dominant_share = "Coal emissions dominated over Gas"
            else:
                dash4_dominant_share = "Gas emissions dominated over Coal"

        # DASHBOARD 5: Cumulative Volume Dashboard (Sum over Selected Range)
        q5_range_df = df[(df['country'] == primary_country) & (df['year'] >= start_year) & (df['year'] <= end_year)]
        if not q5_range_df.empty and 'co2' in q5_range_df.columns:
            total_co2 = q5_range_df['co2'].sum()
            if total_co2 > 5000:
                dash5_cumulative = "High Volume Cumulative Emissions (> 5,000 Mt)"
            elif total_co2 >= 500:
                dash5_cumulative = "Moderate Volume Cumulative Emissions (500 - 5,000 Mt)"
            else:
                dash5_cumulative = "Low Volume Cumulative Emissions (< 500 Mt)"

        # DASHBOARD 6: Per Capita Intensity Analytics Dashboard
        if not q1_df.empty and 'co2_per_capita' in q1_df.columns:
            cap_val = q1_df.iloc[0]['co2_per_capita']
            if not pd.isna(cap_val):
                if cap_val > 8.0:
                    dash6_per_capita_trend = "High Intensity (> 8 tonnes/person)"
                elif cap_val >= 2.0:
                    dash6_per_capita_trend = "Moderate Intensity (2 - 8 tonnes/person)"
                else:
                    dash6_per_capita_trend = "Low Intensity (< 2 tonnes/person)"

    # --- 3. DYNAMIC HEADER BANNER (LIGHT/DARK ADAPTIVE) ---
    st.markdown(
        f"""
        <div style="
            background: var(--background-secondary, rgba(2, 132, 199, 0.08));
            border: 2px solid #0284c7;
            border-radius: 12px;
            padding: 18px 22px;
            margin-bottom: 24px;
        ">
            <h3 style="margin: 0; font-size: 1.25rem; color: var(--text-color, inherit);">
                🎯 Cross-Dashboard Data Challenge
            </h3>
            <p style="margin: 6px 0 0 0; font-size: 0.9rem; opacity: 0.9; color: var(--text-color, inherit);">
                Test your analysis across <b>6 distinct dashboard perspectives</b> for <b>{primary_country}</b> ({start_year}–{end_year}) alongside global climate principles!
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- 4. INTERACTIVE QUIZ FORM ---
    with st.form(key=f"multi_dashboard_quiz_{primary_country}_{end_year}"):
        
        st.markdown("### 📊 Part 1: Cross-Dashboard Insights")
        
        # Q1: Fuel Mix Dashboard
        st.markdown(f"**1. [Fuel Mix Dashboard] What was the top primary fuel source for {primary_country} in {end_year}?**")
        q1_user = st.radio("q1", ["Coal", "Oil", "Gas", "Flaring", "Cement"], index=None, label_visibility="collapsed")
        st.markdown("---")

        # Q2: Trend Trajectory Dashboard
        st.markdown(f"**2. [Trajectory Dashboard] Comparing {start_year} to {end_year}, what was the overall emission direction for {primary_country}?**")
        q2_user = st.radio("q2", ["Net Increase in annual emissions", "Net Decrease in annual emissions"], index=None, label_visibility="collapsed")
        st.markdown("---")

        # Q3: Global Map & Ranking Dashboard
        st.markdown(f"**3. [Spatial & Ranking Dashboard] Where did {primary_country} stand globally in total emissions during {end_year}?**")
        q3_user = st.radio("q3", ["Top 10 High-Emitting Contributor", "Outside Top 10 High-Emitting Contributors"], index=None, label_visibility="collapsed")
        st.markdown("---")

        # Q4: Fuel Comparative Dashboard
        st.markdown(f"**4. [Fuel Structural Breakdown] In {end_year}, how did Coal compare to Gas for {primary_country}?**")
        q4_user = st.radio("q4", ["Coal emissions dominated over Gas", "Gas emissions dominated over Coal"], index=None, label_visibility="collapsed")
        st.markdown("---")

        # Q5: Cumulative Emissions Dashboard
        st.markdown(f"**5. [Cumulative Analytics Dashboard] What was the total aggregate CO2 impact of {primary_country} from {start_year} to {end_year}?**")
        q5_user = st.radio("q5", [
            "High Volume Cumulative Emissions (> 5,000 Mt)",
            "Moderate Volume Cumulative Emissions (500 - 5,000 Mt)",
            "Low Volume Cumulative Emissions (< 500 Mt)"
        ], index=None, label_visibility="collapsed")
        st.markdown("---")

        # Q6: Per Capita Dashboard
        st.markdown(f"**6. [Per Capita Dashboard] How was the carbon footprint per person classified for {primary_country} in {end_year}?**")
        q6_user = st.radio("q6", [
            "High Intensity (> 8 tonnes/person)",
            "Moderate Intensity (2 - 8 tonnes/person)",
            "Low Intensity (< 2 tonnes/person)"
        ], index=None, label_visibility="collapsed")

        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("---")

        # PART 2: GLOBAL CLIMATE ACTION & AWARENESS (4 QUESTIONS)
        st.markdown("### 🌍 Part 2: Global Climate Action & Awareness ")
        
        st.markdown("**7. Which individual or system-level action yields the highest long-term impact on reducing global carbon footprints?**")
        q7_user = st.radio("q7", [
            "Switching off lights when leaving a room",
            "Transitioning to renewable energy sources & energy-efficient systems",
            "Using paper cups instead of plastic",
            "Printing documents on both sides"
        ], index=None, label_visibility="collapsed")
        st.markdown("---")

        st.markdown("**8. What is the primary global temperature limit target set by the Paris Agreement?**")
        q8_user = st.radio("q8", [
            "Limit global warming to well below 2.0°C (preferably 1.5°C) above pre-industrial levels",
            "Stop all industrial production by 2030",
            "Ban all internal combustion vehicles immediately",
            "Freeze carbon emission levels with zero reductions"
        ], index=None, label_visibility="collapsed")
        st.markdown("---")

        st.markdown("**9. What does the term 'Net Zero' emissions mean in global climate policy?**")
        q9_user = st.radio("q9", [
            "Completely eliminating all human activity on earth",
            "Balancing greenhouse gases emitted with an equivalent amount removed from the atmosphere",
            "Stopping all usage of electricity worldwide",
            "Reducing industrial tax rates to zero for clean tech companies"
        ], index=None, label_visibility="collapsed")
        st.markdown("---")

        st.markdown("**10. Which greenhouse gas accounts for the largest share of human-driven global warming overall?**")
        q10_user = st.radio("q10", [
            "Carbon Dioxide (CO2)",
            "Methane (CH4)",
            "Nitrous Oxide (N2O)",
            "Fluorinated Gases"
        ], index=None, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        submit_quiz = st.form_submit_button("Submit & Evaluate Answers →", use_container_width=True)

    # --- 5. EVALUATION FEEDBACK WITH ACCURACY DONUT CHART ---
    if submit_quiz:
        user_answers = [q1_user, q2_user, q3_user, q4_user, q5_user, q6_user, q7_user, q8_user, q9_user, q10_user]
        
        if any(ans is None for ans in user_answers):
            st.warning("⚠️ Please answer all 10 questions before submitting!")
        else:
            score = 0
            
            # Target Answers for Part 2
            q7_target = "Transitioning to renewable energy sources & energy-efficient systems"
            q8_target = "Limit global warming to well below 2.0°C (preferably 1.5°C) above pre-industrial levels"
            q9_target = "Balancing greenhouse gases emitted with an equivalent amount removed from the atmosphere"
            q10_target = "Carbon Dioxide (CO2)"

            # Strict Text-Matching Evaluations
            c1 = (q1_user == dash1_top_fuel); score += 1 if c1 else 0
            c2 = (q2_user == dash2_trend); score += 1 if c2 else 0
            c3 = (q3_user == dash3_rank); score += 1 if c3 else 0
            c4 = (q4_user == dash4_dominant_share); score += 1 if c4 else 0
            c5 = (q5_user == dash5_cumulative); score += 1 if c5 else 0
            c6 = (q6_user == dash6_per_capita_trend); score += 1 if c6 else 0
            c7 = (q7_user == q7_target); score += 1 if c7 else 0
            c8 = (q8_user == q8_target); score += 1 if c8 else 0
            c9 = (q9_user == q9_target); score += 1 if c9 else 0
            c10 = (q10_user == q10_target); score += 1 if c10 else 0

            incorrect_count = 10 - score
            st.session_state['latest_quiz_score'] = score

            st.markdown("<br>", unsafe_allow_html=True)
            
            # Layout Grid: Score Card + Donut Chart Side-by-Side
            col_score, col_chart = st.columns([1, 1.2], gap="medium")

            with col_score:
                st.markdown("<br>", unsafe_allow_html=True)
                if score >= 9:
                    st.success(f"🎉 **Outstanding Score ({score}/10)!** Exceptional mastery across all interactive dashboard modules.")
                elif score >= 6:
                    st.info(f"👍 **Great Job ({score}/10)!** Solid performance interpreting cross-dashboard data.")
                else:
                    st.warning(f"📚 **Score: {score}/10.** Review the cross-dashboard answer key below.")

                st.markdown(
                    f"""
                    <div style="
                        background: var(--background-secondary, rgba(128, 128, 128, 0.08));
                        border-radius: 10px;
                        padding: 14px 18px;
                        border: 1px solid rgba(128, 128, 128, 0.2);
                        margin-top: 10px;
                    ">
                        <span style="color: #00E676; font-weight: bold; font-size: 1.1rem;">✔ Correct Answers: {score}</span><br>
                        <span style="color: #FF1744; font-weight: bold; font-size: 1.1rem;">✖ Incorrect Answers: {incorrect_count}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with col_chart:
                # Determine dynamic colors and labels to prevent visual overlap
                fig_donut = go.Figure(data=[go.Pie(
                    labels=['Correct', 'Incorrect'],
                    values=[score, incorrect_count],
                    hole=0.65,
                    marker=dict(
                        colors=['#00E676', '#FF1744'],
                        line=dict(color='rgba(0,0,0,0)', width=0)
                    ),
                    textinfo='percent',
                    textposition='none',  # Hides overlapping clutter on 0% or 100% edge slices
                    hoverinfo='label+value',
                    sort=False
                )])

                fig_donut.update_layout(
                    title=dict(
                        text="<b>Quiz Performance Breakout</b>",
                        font=dict(size=15, color="var(--text-color, inherit)"),
                        x=0.5,
                        xanchor='center'
                    ),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.25,
                        xanchor="center",
                        x=0.5,
                        font=dict(color="var(--text-color, inherit)")
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=35, b=35, l=10, r=10),
                    height=220,
                    annotations=[dict(
                        text=f"<b>{int((score/10)*100)}%</b>",
                        x=0.5, y=0.5,
                        font=dict(size=24, color="var(--text-color, inherit)"),
                        showarrow=False
                    )]
                )

                # Render responsive chart
                st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})

                st.markdown("<br><div style='margin-bottom: 25px;'></div>", unsafe_allow_html=True)

            # Answer Key Section (Fixed Q8 Display Variable)
            with st.expander("🔍 View Cross-Dashboard Answer Key", expanded=True):
                st.markdown("#### Part 1: Cross-Dashboard Insights Evaluation")
                st.markdown(f"**Q1 (Fuel Mix Dashboard):** **{dash1_top_fuel}** *(Your choice: {q1_user} — {'✅ Correct' if c1 else '❌ Incorrect'})*")
                st.markdown(f"**Q2 (Trajectory Dashboard):** **{dash2_trend}** *(Your choice: {q2_user} — {'✅ Correct' if c2 else '❌ Incorrect'})*")
                st.markdown(f"**Q3 (Spatial & Ranking Dashboard):** **{dash3_rank}** *(Your choice: {q3_user} — {'✅ Correct' if c3 else '❌ Incorrect'})*")
                st.markdown(f"**Q4 (Structural Breakdown):** **{dash4_dominant_share}** *(Your choice: {q4_user} — {'✅ Correct' if c4 else '❌ Incorrect'})*")
                st.markdown(f"**Q5 (Cumulative Analytics):** **{dash5_cumulative}** *(Your choice: {q5_user} — {'✅ Correct' if c5 else '❌ Incorrect'})*")
                st.markdown(f"**Q6 (Per Capita Dashboard):** **{dash6_per_capita_trend}** *(Your choice: {q6_user} — {'✅ Correct' if c6 else '❌ Incorrect'})*")

                st.markdown("<br>#### Part 2: Global Climate Principles Evaluation", unsafe_allow_html=True)
                st.markdown(f"**Q7 (Impact Strategy):** **{q7_target}** *(Your choice: {q7_user} — {'✅ Correct' if c7 else '❌ Incorrect'})*")
                st.markdown(f"**Q8 (Paris Target):** **{q8_target}** *(Your choice: {q8_user} — {'✅ Correct' if c8 else '❌ Incorrect'})*")
                st.markdown(f"**Q9 (Net Zero Definition):** **{q9_target}** *(Your choice: {q9_user} — {'✅ Correct' if c9 else '❌ Incorrect'})*")
                st.markdown(f"**Q10 (Primary GHG):** **{q10_target}** *(Your choice: {q10_user} — {'✅ Correct' if c10 else '❌ Incorrect'})*")

    st.markdown("<br><hr>", unsafe_allow_html=True)

   # --- 6. POST-EVALUATION FEEDBACK & CSV SAVING ---
    st.markdown("### 💬 Dashboard & Quiz Feedback")
    st.caption("Now that you've reviewed your score and answer key, share your thoughts to record your response!")

    # Retrieve user details from session state
    session_user_name = st.session_state.get('user_name', st.session_state.get('username', 'Anonymous User'))
    
    # Check if quiz was completed in current session
    has_taken_quiz = 'latest_quiz_score' in st.session_state
    latest_score = st.session_state.get('latest_quiz_score', None)

    with st.form(key="quiz_feedback_form"):
        user_feedback = st.text_area(
            "Share your feedback or suggestions:", 
            placeholder="How was your experience navigating the dashboard and quiz?", 
            height=100
        )
        
        submit_feedback = st.form_submit_button("Submit Score & Feedback →", use_container_width=True)

        if submit_feedback:
            import csv
            import os
            from datetime import date

            csv_file = "quiz_responses.csv"
            file_exists = os.path.isfile(csv_file)
            submission_date = date.today().strftime("%Y-%m-%d")
            score_display = f"{latest_score}/10" if has_taken_quiz else "Not Taken"

            rows = []
            user_found = False

            if file_exists:
                with open(csv_file, mode="r", encoding="utf-8") as f:
                    reader = list(csv.reader(f))
                    if reader:
                        header = reader[0]
                        rows.append(header)
                        for row in reader[1:]:
                            # Update existing row if user name matches
                            if len(row) >= 2 and row[1] == session_user_name:
                                rows.append([row[0], session_user_name, score_display, submission_date, user_feedback])
                                user_found = True
                            else:
                                rows.append(row)

            if not file_exists:
                rows.append(["ID", "Name", "Quiz Score", "Date", "Feedback"])

            if not user_found:
                next_id = len(rows)
                rows.append([next_id, session_user_name, score_display, submission_date, user_feedback])

            # Write updated dataset back to CSV
            with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)

            # User-friendly success notification
            st.success(f"🎉 Thank you, {session_user_name}! Your feedback has been successfully submitted.")

# =============================================================================
# TAB: ABOUT & TECH STACK
# =============================================================================
elif selected_tab == "ℹ️ About & Tech Stack":
    # Dynamic CSS ensuring high contrast in both Light & Dark themes
    st.markdown(
        """
        <style>
            .tech-card {
                background-color: var(--background-secondary, rgba(2, 132, 199, 0.03));
                border: 1.5px solid #0284c7;
                border-radius: 12px;
                padding: 20px;
                height: 100%;
                min-height: 220px;
                transition: transform 0.25s ease, box-shadow 0.25s ease;
                box-sizing: border-box;
            }

            .tech-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 10px 20px -5px rgba(2, 132, 199, 0.35);
            }

            .tech-card h4 {
                color: var(--text-color, inherit);
                margin-top: 0;
                margin-bottom: 12px;
                font-size: 1.1rem;
                font-weight: 600;
            }

            /* Badge with dynamic theme-aware colors */
            .tech-badge {
                background-color: rgba(2, 132, 199, 0.12);
                border: 1px solid #0284c7;
                border-radius: 6px;
                padding: 6px 12px;
                font-family: monospace;
                font-weight: 700;
                font-size: 0.92rem;
                color: #0369a1; /* High-contrast blue for light mode */
                margin-bottom: 14px;
                display: inline-block;
            }

            /* Auto-adjust badge text for dark theme */
            @media (prefers-color-scheme: dark) {
                .tech-badge {
                    color: #38bdf8 !important; /* Vibrant sky blue for dark mode */
                    background-color: rgba(2, 132, 199, 0.2) !important;
                }
            }

            .tech-desc {
                color: var(--text-color, inherit);
                font-size: 0.88rem;
                opacity: 0.85;
                line-height: 1.5;
                margin: 0;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("## ℹ️ Project Documentation & Technical Architecture")
    st.markdown("---")

    st.markdown("### 💻 Technology Stack")

    # 3-Column Layout with Direct HTML Single Cards
    col_tech1, col_tech2, col_tech3 = st.columns(3)

    with col_tech1:
        st.markdown(
            """
            <div class="tech-card">
                <h4>Frontend Framework</h4>
                <div class="tech-badge">Streamlit (Python)</div>
                <p class="tech-desc">Renders reactive web layouts, sidebars, metrics, and multi-page tabs.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_tech2:
        st.markdown(
            """
            <div class="tech-card">
                <h4>Data Processing</h4>
                <div class="tech-badge">Pandas & NumPy</div>
                <p class="tech-desc">Handles memory management, dynamic filtering, group aggregation, and caching.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_tech3:
        st.markdown(
            """
            <div class="tech-card">
                <h4>Data Visualization</h4>
                <div class="tech-badge">Plotly Express & Objects</div>
                <p class="tech-desc">Generates responsive line charts, choropleth maps, area graphs, and pie visuals.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("---")

    # Dataset & Methodology Section
    st.markdown("### 📊 Dataset & Methodology")
    st.markdown(
        """
        * **Primary Data Source:** Our World in Data (OWID) $\\text{CO}_2$ Dataset.
        * **Scope:** Global country-level emissions from 1950 onwards.
        * **Preprocessing:** Filtered aggregate region entities via ISO codes and applied `@st.cache_data` for optimized page load times.
        """
    )

# =============================================================================
# GLOBAL STICKY FOOTER (DARK & BOLD ACCENT)
# =============================================================================
st.markdown("""
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #1e293b;
            color: #f8fafc;
            text-align: center;
            padding: 10px 0px;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.3px;
            border-top: 2px solid #0284c7;
            box-shadow: 0px -2px 10px rgba(0, 0, 0, 0.15);
            z-index: 999;
        }
        .footer b {
            color: #38bdf8;
        }
    </style>
    <div class="footer">
        💡 <b>Navigation Hint:</b> Use the top navigation buttons to switch between interactive dashboards, spatial maps, and analysis reports.
    </div>
""", unsafe_allow_html=True)