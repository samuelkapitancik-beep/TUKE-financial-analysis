import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import numpy as np
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ako dobre hospodáriš s financiami na TUKE",
    page_icon="🎓",
    layout="wide",
)

# ── Custom CSS  (light-grey theme) ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }
.stApp { background: #f0f2f6; color: #1a1d2e; }
section[data-testid="stSidebar"] { background: #e4e7ef; }

[data-testid="metric-container"] {
    background: #ffffff; border: 1px solid #d6dae8;
    border-radius: 14px; padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
[data-testid="metric-container"] label {
    color: #7a80a0 !important; font-size: 0.75rem !important;
    text-transform: uppercase; letter-spacing: 0.1em;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #1a1d2e !important; font-size: 1.65rem !important;
    font-weight: 700; font-family: 'DM Mono', monospace;
}

[data-testid="stTabs"] [data-baseweb="tab-list"] {
    gap: 6px; background: #ffffff; border-radius: 14px;
    padding: 6px; border: 1px solid #d6dae8;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 10px; color: #7a80a0;
    font-weight: 700; font-size: 0.88rem; padding: 8px 22px;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #3a5bd9 !important; color: #ffffff !important;
}

h1 { color: #1a1d2e !important; font-weight: 800; letter-spacing: -0.04em; text-align: center; }
h2 { color: #2a2e45 !important; font-weight: 700; }
h3 { color: #2a2e45 !important; font-weight: 700; }
h4 { color: #1a1d2e !important; font-weight: 700; }
p  { color: #3a3f5a; }
hr { border-color: #d6dae8 !important; }

[data-testid="stExpander"] {
    background: #ffffff; border: 1px solid #d6dae8 !important;
    border-radius: 14px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
[data-testid="stExpander"] summary { color: #2a2e45 !important; font-weight: 700; }

textarea {
    font-family: 'DM Mono', monospace !important; font-size: 0.82rem !important;
    background: #ffffff !important; color: #2a2e45 !important;
    border: 1px solid #c8cde0 !important; border-radius: 12px !important;
}
textarea:focus {
    border-color: #3a5bd9 !important;
    box-shadow: 0 0 0 2px rgba(58,91,217,0.15) !important;
}

.info-box {
    background: #ffffff; border-left: 4px solid #3a5bd9;
    border-radius: 10px; padding: 14px 18px; margin: 8px 0 14px 0;
    font-size: 0.9rem; color: #3a3f5a; line-height: 1.7;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.loss-box {
    background: #fff5f6; border: 1px solid #f5c2c7;
    border-left: 5px solid #e03050; border-radius: 12px;
    padding: 20px 24px; margin: 4px 0 16px 0;
}
.loss-title {
    font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.12em;
    color: #c02040; font-weight: 700; margin-bottom: 6px;
}
.loss-amount {
    font-size: 2.2rem; font-weight: 800; color: #e03050;
    font-family: 'DM Mono', monospace; line-height: 1.1;
}
.loss-sub { font-size: 0.82rem; color: #a06070; margin-top: 6px; }
.miss-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 7px 2px; border-bottom: 1px solid #eaedf5;
    font-size: 0.85rem; color: #5a5f7a; gap: 8px;
}
.mr-date  { min-width: 90px; color: #8a90b0; font-size: 0.8rem; }
.mr-price { font-family: 'DM Mono', monospace; color: #1a1d2e; font-weight: 600; min-width: 60px; }
.mr-save  { font-family: 'DM Mono', monospace; color: #c02040; flex: 1; }
.mr-miss  { font-family: 'DM Mono', monospace; color: #e03050; font-weight: 700; min-width: 100px; text-align: right; }
.app-subtitle { text-align: center; color: #7a80a0; font-size: 1rem; margin-top: -8px; margin-bottom: 16px; }

[data-testid="stButton"] button[kind="primary"] {
    background: #3a5bd9 !important; border: none !important;
    color: #ffffff !important; font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important; border-radius: 10px !important; font-size: 0.9rem !important;
}
[data-testid="stButton"] button[kind="primary"]:hover { background: #2a48c0 !important; }
[data-testid="stButton"] button[kind="secondary"] {
    background: #ffffff !important; border: 1px solid #c8cde0 !important;
    color: #7a80a0 !important; font-weight: 700 !important;
    font-family: 'Syne', sans-serif !important; border-radius: 10px !important; font-size: 0.9rem !important;
}
[data-testid="stButton"] button[kind="secondary"]:hover {
    border-color: #e03050 !important; color: #e03050 !important;
}
[data-testid="stAlert"] { border-radius: 12px !important; }
</style>
""", unsafe_allow_html=True)

# ── Dotation rules ────────────────────────────────────────────────────────────
DOTATION_RULES = {
    2023: {"limits": [3.0,  7.0,  10.0],               "dotacia": 1.50},
    2024: {"limits": [4.0,  8.0,  12.0,  16.0],        "dotacia": 2.00},
    2025: {"limits": [4.20, 8.40, 12.60, 16.80],       "dotacia": 2.40},
    2026: {"limits": [4.20, 8.40, 12.60, 16.80],       "dotacia": 2.40},
}

def get_dotation_rule(year: int) -> dict:
    return DOTATION_RULES.get(year, DOTATION_RULES[2026])

# ── Canteen mapping ───────────────────────────────────────────────────────────
CANTEEN_MAP = {
    '1': 'ŠJ Němcovej 1',
    '2': 'TUKE POINT Kaviareň',
    '3': 'ŠJ Jedlíkova 7',
    '4': 'Bistro ZP Němcovej',
    '5': 'Pizzeria Forte Jedlíková 7',
    '6': 'ŠJ Urbánkova 2',
    '9': 'Libresso Němcovej 7',
}
CANTEEN_COLORS = {
    'ŠJ Němcovej 1':               '#7ab8ff',
    'TUKE POINT Kaviareň':         '#ffc83c',
    'ŠJ Jedlíkova 7':              '#48d282',
    'Bistro ZP Němcovej':          '#ff6b35',
    'Pizzeria Forte Jedlíková 7':  '#c87aff',
    'ŠJ Urbánkova 2':              '#ff4b5a',
    'Libresso Němcovej 7':         '#40d4d4',
    'Iné':                         '#8890c0',
}

def get_canteen(description: str) -> str:
    m = re.search(r'[uúUÚ]čet\s+č\.?\s*(\d+)', description, re.IGNORECASE)
    if m:
        account_no = m.group(1).lstrip('0')
        if account_no:
            return CANTEEN_MAP.get(account_no[0], 'Iné')
    return 'Iné'

# ── Missed-dotation helpers ───────────────────────────────────────────────────
def missed_dotations_for_purchase(price: float, year: int) -> dict:
    rule    = get_dotation_rule(year)
    limits  = rule['limits']
    dotacia = rule['dotacia']
    next_lim = next((lim for lim in limits if price < lim), None)
    if next_lim is None:
        return {"next_limit": None, "extra_needed": 0.0, "net_saving": 0.0, "dotacia": dotacia}
    extra_needed = round(next_lim - price, 2)
    net_saving   = round(dotacia - extra_needed, 2)
    return {"next_limit": next_lim, "extra_needed": extra_needed,
            "net_saving": net_saving, "dotacia": dotacia}

def daily_ucty(df: pd.DataFrame) -> pd.DataFrame:
    ucty = df[df['type'] == 'účet'].copy()
    ucty['price'] = ucty['amount'].abs()
    return (ucty.groupby(['date', 'year', 'month'])['price']
            .sum().reset_index())

def compute_missed_df(df: pd.DataFrame) -> pd.DataFrame:
    daily = daily_ucty(df)
    rows = []
    for _, row in daily.iterrows():
        m = missed_dotations_for_purchase(row['price'], int(row['year']))
        if m['next_limit'] is not None and m['net_saving'] > 0:
            rows.append({
                'date': row['date'], 'price': row['price'],
                'next_limit': m['next_limit'], 'extra_needed': m['extra_needed'],
                'net_saving': m['net_saving'], 'dotacia': m['dotacia'],
                'year': row['year'],
            })
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values('net_saving', ascending=False).reset_index(drop=True)

# ── Parser ────────────────────────────────────────────────────────────────────
def parse_raw_data(raw_text: str) -> pd.DataFrame:
    pattern = re.compile(
        r'(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2})\s+(.*?)\s+([-\d]+[.,]\d{2})\s*€'
    )
    records = []
    for match in pattern.finditer(raw_text):
        date_str, time_str, desc, amount_str = match.groups()
        amount = float(amount_str.replace(',', '.'))
        try:
            dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")
        except ValueError:
            continue
        dl = desc.lower()
        if 'dotác' in dl or 'dotaci' in dl:
            txn_type = 'dotácia'
        elif 'vklad' in dl or 'vyber' in dl:
            txn_type = 'vklad'
        elif 'vytvorenie objedn' in dl:
            txn_type = 'účet'
        else:
            txn_type = 'účet'

        canteen = get_canteen(desc) if txn_type == 'účet' else None

        records.append({
            'datetime': dt, 'date': dt.date(), 'time': dt.time(),
            'year': dt.year, 'month': dt.month,
            'description': desc.strip(), 'amount': amount,
            'type': txn_type, 'canteen': canteen,
        })

    if not records:
        return pd.DataFrame()
    return pd.DataFrame(records).sort_values('datetime').reset_index(drop=True)

# ── Gradient colour helper ────────────────────────────────────────────────────
def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

_GREEN  = (72,  210, 130)
_YELLOW = (255, 200,  55)
_RED    = (255,  70,  85)

def get_price_gradient_color(price: float, year: int) -> str:
    rule     = get_dotation_rule(year)
    segments = [0.0] + list(rule['limits'])
    seg_start, seg_end = segments[0], segments[-1]
    for i in range(len(segments) - 1):
        if price <= segments[i + 1]:
            seg_start, seg_end = segments[i], segments[i + 1]
            break
    else:
        seg_start = segments[-1]
        seg_end   = segments[-1] + (segments[-1] - segments[-2])
    seg_len = seg_end - seg_start
    if seg_len <= 0:
        return rgb_to_hex(_GREEN)
    t = max(0.0, min(1.0, (price - seg_start) / seg_len))
    color = lerp_color(_GREEN, _YELLOW, t / 0.5) if t <= 0.5 else lerp_color(_YELLOW, _RED, (t - 0.5) / 0.5)
    return rgb_to_hex(color)

# ── Stats ─────────────────────────────────────────────────────────────────────
def compute_stats(df: pd.DataFrame) -> dict:
    if df.empty:
        return {}
    vklady    = df[df['type'] == 'vklad']['amount'].sum()
    ucty      = df[df['type'] == 'účet']['amount'].abs().sum()
    dotacie   = df[df['type'] == 'dotácia']['amount'].sum()
    ucet_days = df[df['type'] == 'účet']['date'].nunique()
    return {
        'vklady': vklady, 'ucty': ucty, 'dotacie': dotacie,
        'avg_day': ucty / ucet_days if ucet_days else 0,
        'ucet_days': ucet_days, 'net': ucty - dotacie,
    }

# ── Chart theme ───────────────────────────────────────────────────────────────
CHART_BG   = 'rgba(0,0,0,0)'
GRID_COL   = '#dde0ea'
TITLE_FONT = dict(size=22, color='#1a1d2e', family='Syne')
AXIS_FONT  = dict(size=12, color='#5a5f7a', family='Syne')

def base_layout(**kwargs):
    d = dict(
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font=dict(color='#1a1d2e', family='Syne'),
        margin=dict(t=64, b=56, l=60, r=28),
        title_font_size=TITLE_FONT['size'],
        title_font_color=TITLE_FONT['color'],
        title_font_family=TITLE_FONT['family'],
        title_x=0.0,
    )
    d.update(kwargs)
    return d

# ═══════════════════════════════════════════════════════════════════════════════
#  RENDER HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def render_missed_section(df: pd.DataFrame):
    missed_df = compute_missed_df(df)
    if missed_df.empty:
        st.markdown(
            "<div class='info-box'>✅ Žiadne stratené dotácie – všetky dni sú optimálne.</div>",
            unsafe_allow_html=True)
        return

    total_loss = missed_df['net_saving'].sum()
    n_missed   = len(missed_df)
    st.markdown(
        f"<div class='loss-box'>"
        f"<div class='loss-title'>💸 Celková potenciálna úspora – nevyužité dotácie</div>"
        f"<div class='loss-amount'>−{total_loss:.2f} €</div>"
        f"<div class='loss-sub'>V <strong>{n_missed}</strong> dňoch stačilo dokúpiť trochu viac "
        f"a dotácia by pokryla rozdiel (a ešte niečo ostalo).</div>"
        f"</div>",
        unsafe_allow_html=True)

    with st.expander(f"🔍 Detail – {n_missed} dní s nevyužitou dotáciou"):
        st.markdown(
            "<div class='miss-row' style='font-size:0.72rem;color:#6b749e;"
            "text-transform:uppercase;letter-spacing:0.09em;border-bottom:2px solid #3a4170;padding-bottom:8px;'>"
            "<span class='mr-date'>Dátum</span><span class='mr-price'>Zaplatené</span>"
            "<span class='mr-save'>Stačilo dokúpiť</span>"
            "<span class='mr-miss'>Čistá úspora</span></div>",
            unsafe_allow_html=True)
        for _, row in missed_df.iterrows():
            st.markdown(
                f"<div class='miss-row'>"
                f"<span class='mr-date'>{row['date'].strftime('%d.%m.%Y')}</span>"
                f"<span class='mr-price'>{row['price']:.2f} €</span>"
                f"<span class='mr-save'>+{row['extra_needed']:.2f} € → "
                f"<strong>{row['next_limit']:.2f} €</strong> "
                f"<span style='color:#5a5a7a;font-size:0.78rem;'>(dotácia {row['dotacia']:.2f} €)</span></span>"
                f"<span class='mr-miss'>ušetril by si {row['net_saving']:.2f} €</span>"
                f"</div>",
                unsafe_allow_html=True)


def render_canteen_pie(df: pd.DataFrame, year=None):
    ucty = df[df['type'] == 'účet'].copy()
    ucty['price'] = ucty['amount'].abs()
    ucty['canteen'] = ucty['canteen'].fillna('Iné')

    by_canteen = ucty.groupby('canteen')['price'].sum().reset_index()
    by_canteen.columns = ['Jedáleň', 'Suma']
    by_canteen = by_canteen[by_canteen['Suma'] > 0].sort_values('Suma', ascending=False)

    if by_canteen.empty:
        return

    colors = [CANTEEN_COLORS.get(c, '#8890c0') for c in by_canteen['Jedáleň']]

    fig = go.Figure(go.Pie(
        labels=by_canteen['Jedáleň'],
        values=by_canteen['Suma'],
        hole=0.48,
        marker=dict(colors=colors, line=dict(color='#ffffff', width=2)),
        textfont=dict(color='#ffffff', size=13, family='Syne'),
        hovertemplate='%{label}<br>%{value:.2f} € (%{percent})<extra></extra>',
    ))
    fig.update_layout(**base_layout(
        title='Výdavky podľa jedálne / kaviarne',
        legend=dict(
            orientation='v', x=1.02, y=0.5,
            font=dict(color='#2a2e45', size=13, family='Syne'),
        ),
        margin=dict(t=64, b=36, l=10, r=170),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    ))
    st.plotly_chart(fig, use_container_width=True, key=f"canteen_pie_{year}")


def render_stats_and_charts(df: pd.DataFrame, year: int = None):
    stats = compute_stats(df)
    if not stats:
        st.info("Žiadne dáta pre toto obdobie.")
        return

    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Celkové vklady",  f"{stats['vklady']:.2f} €")
    c2.metric("🍽️ Celkové účty",   f"{stats['ucty']:.2f} €")
    c3.metric("🎁 Celkové dotácie", f"{stats['dotacie']:.2f} €")
    c4.metric("📊 Priemerný deň",   f"{stats['avg_day']:.2f} €")

    st.markdown(
        f"<div class='info-box'>"
        f"Čisté výdavky (účty − dotácie): "
        f"<strong style='color:#1a1d2e;'>{stats['net']:.2f} €</strong>"
        f"&nbsp;·&nbsp; Dní s nákupom: "
        f"<strong style='color:#1a1d2e;'>{stats['ucet_days']}</strong>"
        f"</div>",
        unsafe_allow_html=True)

    # Missed dotations
    st.markdown("### 💸 Nevyužité dotácie")
    render_missed_section(df)

    st.divider()
    st.markdown("### 📊 Grafy")

    # Row 1: dotácie pie + canteen pie
    col_a, col_b = st.columns(2)

    with col_a:
        fig_pie = go.Figure(go.Pie(
            labels=['Vlastné výdavky', 'Dotácie'],
            values=[max(stats['net'], 0), stats['dotacie']],
            hole=0.48,
            marker=dict(
                colors=['#ff4b5a', '#48d282'],
                line=dict(color='#ffffff', width=2),
            ),
            textfont=dict(color='#ffffff', size=13, family='Syne'),
            hovertemplate='%{label}: %{value:.2f} € (%{percent})<extra></extra>',
        ))
        fig_pie.update_layout(**base_layout(
            title='Dotácie vs Vlastné výdavky',
            legend=dict(orientation='v', x=1.02, y=0.5, font=dict(color='#2a2e45', size=13, family='Syne')),
            margin=dict(t=64, b=36, l=10, r=150),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        ))
        st.plotly_chart(fig_pie, use_container_width=True, key=f"dotacie_pie_{year}")

    with col_b:
        render_canteen_pie(df, year=year)

    # Row 2: Histogram
    st.divider()
    ucty_df = daily_ucty(df)
    if not ucty_df.empty:
        yr     = year if year else int(ucty_df['year'].mode()[0])
        limits = get_dotation_rule(yr)['limits']
        prices = ucty_df['price'].values
        bins   = [round(i * 0.20, 2) for i in range(0, int(max(prices) / 0.20) + 3)]
        counts, edges = np.histogram(prices, bins=bins)
        bar_colors = [
            get_price_gradient_color((edges[i] + edges[i+1]) / 2, yr)
            for i in range(len(edges) - 1)
        ]
        fig_hist = go.Figure()
        for i in range(len(counts)):
            fig_hist.add_trace(go.Bar(
                x=[(edges[i] + edges[i+1]) / 2], y=[counts[i]],
                width=edges[i+1] - edges[i] - 0.01,
                marker_color=bar_colors[i], showlegend=False,
                hovertemplate=f'{edges[i]:.2f}–{edges[i+1]:.2f} €: {counts[i]}x<extra></extra>',
            ))
        for lim in limits:
            fig_hist.add_vline(
                x=lim,
                line_dash='dash',
                line_color='#1a1d2e',
                line_width=2,
                annotation_text=f'{lim} €',
                annotation_font=dict(color='#1a1d2e', size=12, family='Syne'),
                annotation_position='top right',
            )
        fig_hist.update_layout(
            paper_bgcolor='#ffffff',
            plot_bgcolor='#ffffff',
            font=dict(color='#1a1d2e', family='Syne'),
            margin=dict(t=64, b=64, l=60, r=40),
            bargap=0.04,
            barmode='overlay',
        )
        fig_hist.update_layout(
            title='Histogram denných útrat (súčet účtov za deň)',
        )
        fig_hist.update_xaxes(
            title_text='Denná útrata (€)',
            tickfont=dict(size=11, color='#5a5f7a', family='Syne'),
            gridcolor='#e0e4ee',
            linecolor='#c8cde0',
            linewidth=1,
            showline=True,
            zeroline=True,
            zerolinecolor='#c8cde0',
            zerolinewidth=1,
        )
        fig_hist.update_yaxes(
            title_text='Počet dní',
            tickfont=dict(size=11, color='#5a5f7a', family='Syne'),
            gridcolor='#e0e4ee',
            linecolor='#c8cde0',
            linewidth=1,
            showline=True,
            zeroline=True,
            zerolinecolor='#c8cde0',
            zerolinewidth=1,
        )
        fig_hist.update_layout(
            title_font_size=22,
            title_font_color='#1a1d2e',
            title_font_family='Syne',
            title_x=0.0,
        )
        st.plotly_chart(fig_hist, use_container_width=True, key=f"histogram_{year}")
        st.markdown(
            "<div style='font-size:0.8rem;color:#6b749e;display:flex;align-items:center;gap:12px;'>"
            "<span style='color:#5a5f7a;font-size:0.88rem;'>Gradient v segmente:</span>"
            "<span style='display:inline-block;width:130px;height:10px;border-radius:5px;"
            "background:linear-gradient(to right,#48d282,#ffc83c,#ff4b5a);'></span>"
            "<span style='color:#1a9955;font-size:0.88rem;font-weight:700;'>výhodné</span>"
            "<span style='color:#d02040;font-size:0.88rem;font-weight:700;'>nevýhodné</span>"
            "</div>",
            unsafe_allow_html=True)

    # Row 3: Monthly chart
    st.divider()
    # Build full 12-month skeleton for every year present in data
    years_present = sorted(df['year'].unique())
    all_months = pd.DataFrame(
        [(yr, mo) for yr in years_present for mo in range(1, 13)],
        columns=['year', 'month']
    )
    ucty_m = (df[df['type'] == 'účet']
              .groupby(['year', 'month'])['amount'].sum().abs()
              .reset_index(name='ucty'))
    dot_m  = (df[df['type'] == 'dotácia']
              .groupby(['year', 'month'])['amount'].sum()
              .reset_index(name='dotacie'))
    monthly = all_months.merge(ucty_m, on=['year', 'month'], how='left').fillna(0)
    monthly = monthly.merge(dot_m,   on=['year', 'month'], how='left').fillna(0)
    monthly['net']   = monthly['ucty'] - monthly['dotacie']
    monthly['label'] = monthly.apply(
        lambda r: datetime(int(r['year']), int(r['month']), 1).strftime('%b'), axis=1)

    palette = ['#ff6b35', '#48d282', '#7ab8ff', '#ffc83c', '#c87aff']
    fig_m = go.Figure()
    for i, yr in enumerate(sorted(monthly['year'].unique())):
        m = monthly[monthly['year'] == yr]
        fig_m.add_trace(go.Bar(
            name=str(yr), x=m['label'], y=m['net'],
            marker_color=palette[i % len(palette)],
            hovertemplate='%{x}: %{y:.2f} €<extra></extra>',
        ))

    fig_m.update_layout(**base_layout(
        title='Mesačné čisté výdavky  (účty − dotácie)',
        barmode='group',
        legend=dict(orientation='h', y=1.06, font=dict(color='#2a2e45', size=14, family='Syne')),
    ))
    fig_m.update_xaxes(
        title_text='Mesiac',
        title_font=dict(size=12, color='#5a5f7a', family='Syne'),
        tickfont=dict(color='#5a5f7a', family='Syne'),
        gridcolor=GRID_COL,
    )
    fig_m.update_yaxes(
        title_text='Čisté výdavky (€)',
        title_font=dict(size=12, color='#5a5f7a', family='Syne'),
        tickfont=dict(color='#5a5f7a', family='Syne'),
        gridcolor=GRID_COL,
    )
    st.plotly_chart(fig_m, use_container_width=True, key=f"monthly_{year}")

    # Raw table
    with st.expander("🔍 Zobraziť surové transakcie"):
        disp = df[['datetime', 'description', 'amount', 'type', 'canteen']].copy()
        disp.columns = ['Dátum a čas', 'Popis', 'Suma (€)', 'Typ', 'Jedáleň']
        disp['Dátum a čas'] = disp['Dátum a čas'].dt.strftime('%d.%m.%Y %H:%M')
        st.dataframe(disp, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("# 🎓 Ako dobre hospodáriš s financiami na TUKE")
st.markdown("<div class='app-subtitle'>Osobný prehľad stravovacieho účtu · TUKE</div>", unsafe_allow_html=True)
st.divider()

with st.expander("📖 Ako to funguje – návod a popis"):
    st.markdown("""
### Čo táto aplikácia robí
Analyzuje výpisy zo stravovacieho účtu a poskytuje štatistiky, analýzu strát z nevyužitých dotácií a grafy.

---
### Ako nahrať dáta

1. Prihlás sa na **[jedalen.tuke.sk](https://jedalen.tuke.sk/)** pomocou školského konta.
2. Otvor túto adresu priamo v prehliadači:
   **[jedalen.tuke.sk/objednavky/historia-uctu?offset=0&limit=10000](https://jedalen.tuke.sk/objednavky/historia-uctu?offset=0&limit=10000)**
3. Označ všetky transakcie a skopíruj ich (**Ctrl+C**).
4. Vlož ich do textového poľa nižšie a klikni **Analyzovať**.

Aplikácia rozpozná aj riadky typu `Vytvorenie objednávky č. 07 na deň 08.11.2023 (id: 185783)`.

---
### Jedálne / prevádzky
| Prvá číslica čísla účtu | Prevádzka |
|------------------------|-----------|
| 1 | ŠJ Němcovej 1 |
| 2 | TUKE POINT Kaviareň |
| 3 | ŠJ Jedlíkova 7 |
| 4 | Bistro ZP Němcovej |
| 5 | Pizzeria Forte Jedlíková 7 |
| 6 | ŠJ Urbánkova 2 |
| 9 | Libresso Němcovej 7 |

---
### Nevyužité dotácie
Pre každý deň sa sčítajú všetky účty. Ak by dokúpenie do ďalšieho míľnika prinieslo čistú úsporu, zobrazí sa v prehľade strát.

---
### Pravidlá dotácií
| Rok | Limity (€) | Dotácia za míľnik |
|-----|-----------|-------------------|
| 2023 | 3,00 / 7,00 / 10,00 | 1,50 € |
| 2024 | 4,00 / 8,00 / 12,00 / 16,00 | 2,00 € |
| 2025–2026 | 4,20 / 8,40 / 12,60 / 16,80 | 2,40 € |
""")

st.divider()
st.markdown("### 📥 Vložte surové dáta")

# ── Session state init ────────────────────────────────────────────────────────
SAMPLE_DATA = """16.03.2026 11:18 Vklad/Vyber ŠJ Jedlíkova 7 50,00 €
13.03.2026 01:02 Výpočet dotácií 12.03.2026 7,20 €
12.03.2026 12:47 Účet č. 900249811 12.03.2026 -2,85 €
12.03.2026 12:47 Účet č. 300249812 12.03.2026 -4,50 €
11.03.2026 01:02 Výpočet dotácií 10.03.2026 4,80 €
10.03.2026 12:30 Účet č. 300249800 10.03.2026 -8,00 €
09.03.2026 11:00 Vklad/Vyber ŠJ Jedlíkova 7 30,00 €
07.03.2026 01:02 Výpočet dotácií 06.03.2026 2,40 €
06.03.2026 12:15 Účet č. 900249799 06.03.2026 -4,25 €
05.03.2026 12:20 Účet č. 200249798 05.03.2026 -3,90 €
04.03.2026 01:01 Výpočet dotácií 03.03.2026 2,40 €
03.03.2026 12:10 Účet č. 300249797 03.03.2026 -4,20 €
28.02.2026 01:02 Výpočet dotácií 27.02.2026 4,80 €
27.02.2026 12:45 Účet č. 300249780 27.02.2026 -8,40 €
26.02.2026 12:00 Účet č. 600249779 26.02.2026 -3,00 €
25.02.2026 01:01 Výpočet dotácií 24.02.2026 2,40 €
24.02.2026 12:30 Účet č. 400249778 24.02.2026 -4,30 €
20.02.2026 11:00 Vklad/Vyber ŠJ Jedlíkova 7 40,00 €
15.01.2026 01:02 Výpočet dotácií 14.01.2026 2,40 €
14.01.2026 12:20 Účet č. 500249600 14.01.2026 -4,50 €
13.01.2026 12:15 Účet č. 100249599 13.01.2026 -3,80 €
10.01.2026 01:02 Výpočet dotácií 09.01.2026 4,80 €
09.01.2026 12:00 Účet č. 300249580 09.01.2026 -8,50 €
05.01.2026 11:00 Vklad/Vyber ŠJ Jedlíkova 7 60,00 €"""

if 'raw_text' not in st.session_state:
    st.session_state['raw_text'] = SAMPLE_DATA
if 'df_submitted' not in st.session_state:
    st.session_state['df_submitted'] = None

# ── Input area ────────────────────────────────────────────────────────────────
raw_input = st.text_area(
    "Skopírujte sem celý výpis z portálu strava.sk:",
    value=st.session_state['raw_text'],
    height=200,
    key="input_area",
    placeholder="16.03.2026 11:18 Vklad/Vyber ŠJ Jedlíkova 7 50,00 €\n...",
)

col_submit, col_clear, col_spacer = st.columns([1, 1, 6])
with col_submit:
    if st.button("▶ Analyzovať", type="primary", use_container_width=True):
        st.session_state['raw_text'] = raw_input
        parsed = parse_raw_data(raw_input)
        if parsed.empty:
            st.warning("⚠️ Žiadne transakcie sa nepodarilo načítať. Skontrolujte formát dát.")
        else:
            st.session_state['df_submitted'] = parsed
        st.rerun()
with col_clear:
    if st.button("✕ Vymazať", type="secondary", use_container_width=True):
        st.session_state['raw_text'] = ""
        st.session_state['df_submitted'] = None
        st.rerun()

df_all = st.session_state.get('df_submitted')

if df_all is None or df_all.empty:
    st.info("👆 Vložte dáta a kliknite na **Analyzovať**.")
    # ── Footer (no data state) ────────────────────────────────────────────────
    st.markdown("""
    <div style='
        margin-top: 60px;
        padding: 16px 0 8px 0;
        border-top: 1px solid #d6dae8;
        text-align: center;
        color: #b0b6c8;
        font-size: 0.75rem;
        letter-spacing: 0.04em;
        line-height: 1.8;
    '>
        Samuel Kapitančík &nbsp;·&nbsp; Peter Zeleňák &nbsp;·&nbsp; 2026<br>
        <span style='font-size:0.68rem; color:#c8cdd8;'>© chlapci z ústavu</span>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

available_years = sorted(df_all['year'].unique(), reverse=True)
st.success(f"✅ Načítaných **{len(df_all)}** transakcií z rokov: {', '.join(map(str, available_years))}")
st.divider()

# ── Year rating ───────────────────────────────────────────────────────────────
# Easily configurable: list of (threshold_pct, emoji, short_text, color)
# threshold = dotacie / ucty * 100  (% of bills covered by dotations)
# Entries are checked from highest to lowest threshold.
YEAR_RATINGS = [
    (54, "🤩", "Výborne! Dotácie ti kryjú väčšinu nákladov.",          "#48d282"),
    (52, "😄", "Skvelý rok – využívaš dotácie nad priemer.",            "#7fd46a"),
    (49, "🙂", "Slušný výsledok, ešte je priestor na zlepšenie.",      "#c8d040"),
    (42, "😐", "Priemerné hospodárenie – treba si to počítať bratu.",          "#ffc83c"),
    (36, "😕", "Pod priemerom – matika nie je tvoja silná stránka.",          "#ff8c42"),
    ( 0, "😢", "Dotácie pokrývajú málo – prehodnoť svoje životné rozhodnutia.",    "#ff4b5a"),
]

def get_year_rating(ucty: float, dotacie: float):
    if ucty <= 0:
        return "❓", "Nedostatok dát", "#6b749e"
    pct = dotacie / ucty * 100
    for threshold, emoji, text, color in YEAR_RATINGS:
        if pct >= threshold:
            return emoji, f"{pct:.0f} % účtov pokrytých dotáciami – {text}", color
    return "😢", f"{pct:.0f} % – veľmi nízke využitie dotácií.", "#ff4b5a"

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_labels = ["🌐 Celkovo"] + [f"📅 {y}" for y in available_years]
tabs = st.tabs(tab_labels)

with tabs[0]:
    st.markdown("### 🌐 Celkový prehľad")
    render_stats_and_charts(df_all, year=None)

for i, yr in enumerate(available_years):
    with tabs[i + 1]:
        df_yr  = df_all[df_all['year'] == yr]
        rule   = get_dotation_rule(yr)
        limits_str = " / ".join([f"{l:.2f} €" for l in rule['limits']])

        stats_yr = compute_stats(df_yr)
        emoji, rating_text, rating_color = get_year_rating(
            stats_yr.get('ucty', 0), stats_yr.get('dotacie', 0)
        )

        # Year header with rating badge
        st.markdown(
            f"<div style='display:flex;align-items:center;gap:18px;margin-bottom:6px;'>"
            f"<span style='font-size:2.6rem;line-height:1;'>{emoji}</span>"
            f"<div>"
            f"<div style='font-size:1.5rem;font-weight:800;color:#ffffff;'>Rok {yr}</div>"
            f"<div style='font-size:0.95rem;color:{rating_color};font-weight:700;margin-top:2px;'>"
            f"{rating_text}</div>"
            f"</div>"
            f"</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            f"<div class='info-box'>"
            f"<strong>Pravidlá dotácií {yr}:</strong> "
            f"Limity: <strong style='color:#1a1d2e;'>{limits_str}</strong>"
            f"&nbsp;·&nbsp; Dotácia za míľnik: "
            f"<strong style='color:#1a8a50;'>{rule['dotacia']:.2f} €</strong>"
            f"</div>",
            unsafe_allow_html=True
        )
        render_stats_and_charts(df_yr, year=yr)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='
    margin-top: 60px;
    padding: 16px 0 8px 0;
    border-top: 1px solid #d6dae8;
    text-align: center;
    color: #b0b6c8;
    font-size: 0.75rem;
    letter-spacing: 0.04em;
    line-height: 1.8;
'>
    Samuel Kapitančík &nbsp;·&nbsp; Peter Zeleňák &nbsp;·&nbsp; 2026<br>
    <span style='font-size:0.68rem; color:#c8cdd8;'>© chlapci z ústavu</span>
</div>
""", unsafe_allow_html=True)