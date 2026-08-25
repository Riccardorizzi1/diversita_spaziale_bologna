from pathlib import Path

import geopandas as gpd
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# CONFIGURAZIONE
# ============================================================

st.set_page_config(
    page_title="Diversità Spaziale Bologna",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PERCORSI
# ============================================================

ROOT = Path(__file__).resolve().parent

DATA = ROOT / "data_processed"
OUTPUTS = ROOT / "outputs"
GRAFICI = OUTPUTS / "grafici"


FILE_POI = (
    DATA
    / "bologna_poi_classificati.gpkg"
)

FILE_GRIGLIA = (
    DATA
    / "griglia_indici_bologna.gpkg"
)

FILE_LISA = (
    DATA
    / "griglia_lisa_bologna.gpkg"
)

FILE_QUARTIERI = (
    DATA
    / "quartieri_indici_popolazione_bologna.gpkg"
)

FILE_MAPPA = (
    OUTPUTS
    / "mappa_diversita_bologna.html"
)

FILE_SHANNON = (
    GRAFICI
    / "distribuzione_shannon.png"
)

FILE_SIMPSON = (
    GRAFICI
    / "distribuzione_simpson.png"
)

FILE_RICCHEZZA = (
    GRAFICI
    / "distribuzione_ricchezza.png"
)

FILE_QUARTIERI_SHANNON = (
    GRAFICI
    / "confronto_shannon_quartieri.png"
)

FILE_DENSITA = (
    GRAFICI
    / "relazione_shannon_densita.png"
)


# ============================================================
# PALETTE AZIENDALE
# ============================================================

BLU = "#00649C"
AZZURRO = "#1C9FE8"
ARANCIONE = "#E8901C"
GRIGIO = "#495B69"
SFONDO = "#F7F9FB"


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {SFONDO};
    }}

    .block-container {{
        max-width: 1500px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }}

    h1, h2, h3 {{
        color: {BLU};
    }}

    [data-testid="stSidebar"] {{
        background-color: white;
        border-right: 1px solid #E6E9ED;
    }}

    .header-box {{
        background: linear-gradient(
            90deg,
            {BLU},
            {AZZURRO}
        );

        padding: 1.5rem 1.7rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }}

    .header-box h1 {{
        color: white;
        margin: 0;
    }}

    .header-box p {{
        color: white;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }}

    .kpi {{
        background-color: white;
        border-radius: 10px;
        padding: 1.1rem;
        border-top: 4px solid {AZZURRO};
        box-shadow: 0 1px 5px rgba(0,0,0,0.08);
        min-height: 115px;
    }}

    .kpi-value {{
        color: {BLU};
        font-size: 1.8rem;
        font-weight: 700;
    }}

    .kpi-label {{
        color: {GRIGIO};
        font-size: 0.9rem;
        font-weight: 600;
    }}

    .nota {{
        background-color: white;
        border-radius: 10px;
        border-left: 4px solid {ARANCIONE};
        padding: 1.2rem;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONTROLLO FILE
# ============================================================

file_necessari = [
    FILE_POI,
    FILE_GRIGLIA,
    FILE_LISA,
    FILE_QUARTIERI,
    FILE_MAPPA,
    FILE_SHANNON,
    FILE_SIMPSON,
    FILE_RICCHEZZA,
    FILE_QUARTIERI_SHANNON,
    FILE_DENSITA,
]


mancanti = [
    f
    for f in file_necessari
    if not f.exists()
]


if mancanti:

    st.error(
        "Mancano file necessari alla dashboard."
    )

    for f in mancanti:

        st.write(
            "-",
            f.relative_to(ROOT)
        )

    st.stop()


# ============================================================
# LETTURA DATI
# ============================================================

@st.cache_data
def carica_dati():

    poi = gpd.read_file(
        FILE_POI
    )

    griglia = gpd.read_file(
        FILE_GRIGLIA
    )

    lisa = gpd.read_file(
        FILE_LISA
    )

    quartieri = gpd.read_file(
        FILE_QUARTIERI
    )

    return poi, griglia, lisa, quartieri


poi, griglia, lisa, quartieri = (
    carica_dati()
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="header-box">

        <h1>
            Diversità Spaziale Urbana – Bologna
        </h1>

        <p>
            Analisi della mixité funzionale attraverso
            Points of Interest, indici di diversità
            e autocorrelazione spaziale.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# NAVIGAZIONE
# ============================================================

st.sidebar.title(
    "Navigazione"
)


pagina = st.sidebar.radio(
    "Sezione",
    [
        "Panoramica",
        "Mappa interattiva",
        "Quartieri",
        "Grafici esplorativi",
        "Metodologia",
    ],
)


st.sidebar.markdown("---")

st.sidebar.caption(
    "Comune di Bologna"
)

st.sidebar.caption(
    "OpenStreetMap / Comune di Bologna"
)


# ============================================================
# KPI
# ============================================================

def kpi(
    valore,
    nome,
):

    st.markdown(
        f"""
        <div class="kpi">

            <div class="kpi-value">
                {valore}
            </div>

            <div class="kpi-label">
                {nome}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# PANORAMICA
# ============================================================

if pagina == "Panoramica":

    st.subheader(
        "Quadro generale"
    )


    c1, c2, c3, c4 = (
        st.columns(4)
    )


    with c1:

        kpi(
            "7.975",
            "POI classificati",
        )


    with c2:

        kpi(
            "542",
            "Celle della griglia",
        )


    with c3:

        kpi(
            "6",
            "Quartieri",
        )


    with c4:

        kpi(
            "8",
            "Categorie funzionali",
        )


    st.write("")


    c5, c6, c7 = (
        st.columns(3)
    )


    with c5:

        kpi(
            "0,2250",
            "Moran's I",
        )


    with c6:

        kpi(
            "0,0010",
            "p-value",
        )


    with c7:

        kpi(
            "481",
            "Celle Moran/LISA",
        )


    st.write("")


    st.markdown(
        """
        <div class="nota">

        <b>Indicatore principale:
        Indice di Shannon.</b>

        <br><br>

        Valori più elevati indicano una
        distribuzione maggiormente equilibrata
        delle otto categorie funzionali.

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.write("")


    g1, g2 = st.columns(2)


    with g1:

        st.image(
            str(FILE_SHANNON),
            caption=(
                "Distribuzione dell'indice "
                "di Shannon"
            ),
            use_container_width=True,
        )


    with g2:

        st.image(
            str(FILE_QUARTIERI_SHANNON),
            caption=(
                "Diversità funzionale "
                "per quartiere"
            ),
            use_container_width=True,
        )


# ============================================================
# MAPPA
# ============================================================

elif pagina == "Mappa interattiva":

    st.subheader(
        "Mappa interattiva"
    )


    st.caption(
        "Esplora la griglia, i quartieri "
        "e gli otto layer dei POI."
    )


    html = FILE_MAPPA.read_text(
        encoding="utf-8"
    )


    components.html(
        html,
        height=820,
        scrolling=False,
    )


# ============================================================
# QUARTIERI
# ============================================================

elif pagina == "Quartieri":

    st.subheader(
        "Confronto territoriale"
    )


    colonne = [
        "quartiere",
        "n_poi",
        "shannon",
        "simpson_dominance",
        "ricchezza",
        "residenti",
        "densita_ab_kmq",
    ]


    tabella = (
        quartieri[colonne]
        .copy()
        .sort_values(
            "shannon",
            ascending=False,
        )
    )


    tabella = tabella.rename(
        columns={
            "quartiere":
                "Quartiere",

            "n_poi":
                "POI",

            "shannon":
                "Shannon",

            "simpson_dominance":
                "Simpson dominance",

            "ricchezza":
                "Ricchezza",

            "residenti":
                "Residenti",

            "densita_ab_kmq":
                "Densità ab./km²",
        }
    )


    tabella["Shannon"] = (
        tabella["Shannon"]
        .round(4)
    )


    tabella[
        "Simpson dominance"
    ] = (
        tabella[
            "Simpson dominance"
        ]
        .round(4)
    )


    tabella[
        "Densità ab./km²"
    ] = (
        tabella[
            "Densità ab./km²"
        ]
        .round(1)
    )


    st.dataframe(
        tabella,
        use_container_width=True,
        hide_index=True,
    )


    st.write("")


    g1, g2 = st.columns(2)


    with g1:

        st.image(
            str(
                FILE_QUARTIERI_SHANNON
            ),
            caption=(
                "Indice di Shannon "
                "per quartiere"
            ),
            use_container_width=True,
        )


    with g2:

        st.image(
            str(FILE_DENSITA),
            caption=(
                "Diversità funzionale "
                "e densità abitativa"
            ),
            use_container_width=True,
        )


# ============================================================
# GRAFICI
# ============================================================

elif pagina == "Grafici esplorativi":

    st.subheader(
        "Grafici esplorativi"
    )


    g1, g2 = st.columns(2)


    with g1:

        st.image(
            str(FILE_SHANNON),
            use_container_width=True,
        )


    with g2:

        st.image(
            str(FILE_SIMPSON),
            use_container_width=True,
        )


    g3, g4 = st.columns(2)


    with g3:

        st.image(
            str(FILE_RICCHEZZA),
            use_container_width=True,
        )


    with g4:

        st.image(
            str(FILE_QUARTIERI_SHANNON),
            use_container_width=True,
        )


    st.image(
        str(FILE_DENSITA),
        use_container_width=True,
    )


# ============================================================
# METODOLOGIA
# ============================================================

elif pagina == "Metodologia":

    st.subheader(
        "Nota metodologica"
    )


    st.markdown(
        """
        Il progetto misura la diversità
        funzionale urbana nel Comune di Bologna
        attraverso la distribuzione dei POI.

        L'approccio costituisce un adattamento
        concettuale del progetto
        **spatial_diversity**
        dell'Università di Saragozza.
        """
    )


    with st.expander(
        "POI e categorie",
        expanded=True,
    ):

        st.markdown(
            """
            **7.975 POI** classificati in:

            - commercio
            - ristorazione
            - servizi alla persona
            - istruzione
            - sanità
            - cultura
            - trasporti
            - servizi pubblici
            """
        )


    with st.expander(
        "Indicatori",
    ):

        st.markdown(
            """
            **Shannon**

            H = - Σ pᵢ ln(pᵢ)

            **Simpson dominance**

            D = Σ pᵢ²

            **Ricchezza categoriale**

            Numero di categorie presenti.
            """
        )


    with st.expander(
        "Autocorrelazione",
    ):

        st.markdown(
            """
            - 481 celle
            - contiguità Queen
            - 999 permutazioni
            - seed = 42
            - Moran's I = 0,2250
            - p-value = 0,0010
            """
        )


    with st.expander(
        "Quartieri",
    ):

        st.markdown(
            """
            L'analisi territoriale utilizza
            i 6 quartieri ufficiali.

            **7.970 POI** ricadono nei quartieri.

            I **5 POI** rimanenti restano
            nell'analisi a griglia.
            """
        )


    with st.expander(
        "Popolazione",
    ):

        st.markdown(
            """
            Anno di riferimento: **2024**

            Residenti nei 6 quartieri:
            **392.044**

            Senza fissa dimora:
            **747**

            Totale riconciliato:
            **392.791**
            """
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Diversità Spaziale Urbana – Bologna"
)
