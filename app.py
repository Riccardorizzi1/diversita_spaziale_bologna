# ============================================================
# DASHBOARD STREAMLIT
# Diversità Spaziale Urbana - Bologna
#
# VERSIONE GITHUB - STRUTTURA PIATTA
# Tutti i file sono nella root del repository
# ============================================================

from pathlib import Path

import geopandas as gpd
import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# 1. CONFIGURAZIONE PAGINA
# ============================================================

st.set_page_config(
    page_title="Diversità Spaziale Bologna",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. ROOT DEL REPOSITORY
# ============================================================

ROOT = Path(__file__).resolve().parent


# ============================================================
# 3. FILE NELLA ROOT
# ============================================================

FILE_POI = (
    ROOT
    / "bologna_poi_classificati.gpkg"
)

FILE_GRIGLIA = (
    ROOT
    / "griglia_indici_bologna.gpkg"
)

FILE_LISA = (
    ROOT
    / "griglia_lisa_bologna.gpkg"
)

FILE_QUARTIERI = (
    ROOT
    / "quartieri_indici_popolazione_bologna.gpkg"
)

FILE_MAPPA = (
    ROOT
    / "mappa_diversita_bologna.html"
)

FILE_SHANNON = (
    ROOT
    / "distribuzione_shannon.png"
)

FILE_SIMPSON = (
    ROOT
    / "distribuzione_simpson.png"
)

FILE_RICCHEZZA = (
    ROOT
    / "distribuzione_ricchezza.png"
)

FILE_QUARTIERI_SHANNON = (
    ROOT
    / "confronto_shannon_quartieri.png"
)

FILE_DENSITA = (
    ROOT
    / "relazione_shannon_densita.png"
)


# ============================================================
# 4. PALETTE AZIENDALE
# ============================================================

BLU = "#00649C"
AZZURRO = "#1C9FE8"
ARANCIONE = "#E8901C"
GRIGIO = "#495B69"
SFONDO = "#F7F9FB"


# ============================================================
# 5. CSS
# ============================================================

st.markdown(
    f"""
    <style>

    .stApp {{
        background-color: {SFONDO};
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    h1, h2, h3 {{
        color: {BLU};
    }}

    [data-testid="stSidebar"] {{
        background-color: #FFFFFF;
        border-right: 1px solid #E6E9ED;
    }}

    .dashboard-header {{
        padding: 1.4rem 1.6rem;

        background: linear-gradient(
            90deg,
            {BLU},
            {AZZURRO}
        );

        border-radius: 12px;
        margin-bottom: 1.5rem;
    }}

    .dashboard-header h1 {{
        color: white;
        margin: 0;
        font-size: 2rem;
    }}

    .dashboard-header p {{
        color: white;
        margin-top: 0.5rem;
        margin-bottom: 0;
        font-size: 1rem;
        opacity: 0.95;
    }}

    .kpi-card {{
        background-color: white;
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        border-top: 4px solid {AZZURRO};
        box-shadow: 0 1px 5px rgba(0,0,0,0.08);
        min-height: 115px;
    }}

    .kpi-value {{
        color: {BLU};
        font-size: 1.9rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }}

    .kpi-label {{
        color: {GRIGIO};
        font-size: 0.9rem;
        font-weight: 600;
    }}

    .section-box {{
        background-color: white;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        border-left: 4px solid {ARANCIONE};
        margin-bottom: 1rem;
    }}

    .method-box {{
        background-color: white;
        border-radius: 10px;
        padding: 1.3rem 1.5rem;
        border-left: 4px solid {BLU};
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 6. CONTROLLO FILE NECESSARI
# ============================================================

FILE_NECESSARI = [
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


file_mancanti = [
    file
    for file in FILE_NECESSARI
    if not file.exists()
]


if file_mancanti:

    st.error(
        "Mancano uno o più file necessari "
        "per avviare la dashboard."
    )

    st.write(
        "File trovati nella root del repository:"
    )

    for file in sorted(ROOT.iterdir()):

        if file.is_file():

            st.code(
                file.name
            )

    st.write(
        "File necessari mancanti:"
    )

    for file in file_mancanti:

        st.code(
            file.name
        )

    st.stop()


# ============================================================
# 7. LETTURA DATI CON CACHE
# ============================================================

@st.cache_data(
    show_spinner=False
)
def carica_poi():

    return gpd.read_file(
        FILE_POI
    )


@st.cache_data(
    show_spinner=False
)
def carica_griglia():

    return gpd.read_file(
        FILE_GRIGLIA
    )


@st.cache_data(
    show_spinner=False
)
def carica_lisa():

    return gpd.read_file(
        FILE_LISA
    )


@st.cache_data(
    show_spinner=False
)
def carica_quartieri():

    return gpd.read_file(
        FILE_QUARTIERI
    )


with st.spinner(
    "Caricamento risultati..."
):

    poi = carica_poi()
    griglia = carica_griglia()
    lisa = carica_lisa()
    quartieri = carica_quartieri()


# ============================================================
# 8. KPI
# ============================================================

n_poi = len(poi)

n_celle = len(griglia)

n_quartieri = len(quartieri)

n_categorie = (
    poi[
        "categoria_finale"
    ]
    .nunique()
)

n_celle_lisa = len(lisa)


# ============================================================
# 9. HEADER
# ============================================================

st.markdown(
    """
    <div class="dashboard-header">

        <h1>
            Diversità Spaziale Urbana – Bologna
        </h1>

        <p>
            Analisi della mixité funzionale urbana
            attraverso Points of Interest,
            indici di diversità e
            autocorrelazione spaziale.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 10. SIDEBAR
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
# 11. FUNZIONE KPI
# ============================================================

def mostra_kpi(
    valore,
    etichetta,
):

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-value">
                {valore}
            </div>

            <div class="kpi-label">
                {etichetta}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 12. PANORAMICA
# ============================================================

if pagina == "Panoramica":

    st.subheader(
        "Quadro generale"
    )


    c1, c2, c3, c4 = (
        st.columns(4)
    )


    with c1:

        mostra_kpi(
            f"{n_poi:,}".replace(
                ",",
                "."
            ),
            "POI classificati",
        )


    with c2:

        mostra_kpi(
            n_celle,
            "Celle della griglia",
        )


    with c3:

        mostra_kpi(
            n_quartieri,
            "Quartieri",
        )


    with c4:

        mostra_kpi(
            n_categorie,
            "Categorie funzionali",
        )


    st.write("")


    c5, c6, c7 = (
        st.columns(3)
    )


    with c5:

        mostra_kpi(
            "0,2250",
            "Moran's I globale",
        )


    with c6:

        mostra_kpi(
            "0,0010",
            "p-value permutazionale",
        )


    with c7:

        mostra_kpi(
            n_celle_lisa,
            "Celle Moran/LISA",
        )


    st.write("")


    st.markdown(
        """
        <div class="section-box">

        <b>Indicatore principale:
        Indice di Shannon.</b>

        <br><br>

        La diversità funzionale viene misurata
        sulla distribuzione di otto categorie
        di POI.

        Valori di Shannon più elevati indicano
        una composizione funzionale
        maggiormente equilibrata.

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
            str(
                FILE_QUARTIERI_SHANNON
            ),
            caption=(
                "Diversità funzionale "
                "per quartiere"
            ),
            use_container_width=True,
        )


# ============================================================
# 13. MAPPA
# ============================================================

elif pagina == "Mappa interattiva":

    st.subheader(
        "Mappa interattiva"
    )


    st.caption(
        "Attiva o disattiva i layer della "
        "griglia, dei quartieri e delle "
        "otto categorie POI."
    )


    html_mappa = (
        FILE_MAPPA
        .read_text(
            encoding="utf-8"
        )
    )


    components.html(
        html_mappa,
        height=820,
        scrolling=False,
    )


# ============================================================
# 14. QUARTIERI
# ============================================================

elif pagina == "Quartieri":

    st.subheader(
        "Confronto territoriale"
    )


    colonne_tabella = [
        "quartiere",
        "n_poi",
        "shannon",
        "simpson_dominance",
        "ricchezza",
        "residenti",
        "densita_ab_kmq",
    ]


    tabella = (
        quartieri[
            colonne_tabella
        ]
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
# 15. GRAFICI
# ============================================================

elif pagina == "Grafici esplorativi":

    st.subheader(
        "Grafici esplorativi"
    )


    g1, g2 = st.columns(2)


    with g1:

        st.image(
            str(FILE_SHANNON),
            caption=(
                "Distribuzione Shannon"
            ),
            use_container_width=True,
        )


    with g2:

        st.image(
            str(FILE_SIMPSON),
            caption=(
                "Distribuzione "
                "Simpson dominance"
            ),
            use_container_width=True,
        )


    g3, g4 = st.columns(2)


    with g3:

        st.image(
            str(FILE_RICCHEZZA),
            caption=(
                "Distribuzione della "
                "ricchezza categoriale"
            ),
            use_container_width=True,
        )


    with g4:

        st.image(
            str(
                FILE_QUARTIERI_SHANNON
            ),
            caption=(
                "Shannon per quartiere"
            ),
            use_container_width=True,
        )


    st.image(
        str(FILE_DENSITA),
        caption=(
            "Relazione esplorativa tra "
            "diversità funzionale e "
            "densità abitativa"
        ),
        use_container_width=True,
    )


# ============================================================
# 16. METODOLOGIA
# ============================================================

elif pagina == "Metodologia":

    st.subheader(
        "Nota metodologica"
    )


    st.markdown(
        """
        <div class="method-box">

        Il progetto misura la diversità
        funzionale urbana nel Comune di Bologna
        attraverso la distribuzione spaziale
        dei <b>Points of Interest (POI)</b>.

        <br><br>

        L'impostazione costituisce un
        <b>adattamento dell'approccio concettuale
        del progetto spatial_diversity
        dell'Università di Saragozza</b>.

        </div>
        """,
        unsafe_allow_html=True,
    )


    with st.expander(
        "Fonti e classificazione POI",
        expanded=True,
    ):

        st.markdown(
            """
            **Fonte POI:** OpenStreetMap /
            Geofabrik.

            **7.975 POI** classificati in
            otto categorie:

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
        "Griglia e indicatori"
    ):

        st.markdown(
            """
            Griglia adattiva con celle di:

            - 250 m
            - 500 m
            - 1.000 m

            **Shannon**

            H = - Σ pᵢ ln(pᵢ)

            **Simpson dominance**

            D = Σ pᵢ²

            **Ricchezza categoriale**

            Numero delle categorie presenti.
            """
        )


    with st.expander(
        "Autocorrelazione spaziale"
    ):

        st.markdown(
            """
            - 481 celle analizzate
            - contiguità Queen
            - 999 permutazioni
            - seed = 42
            - Moran's I = 0,2250
            - p-value = 0,0010

            LISA distingue i cluster
            HH, LL, HL e LH.
            """
        )


    with st.expander(
        "Scala dei quartieri"
    ):

        st.markdown(
            """
            L'analisi territoriale comprende
            i **6 quartieri ufficiali di Bologna**.

            **7.970 POI** ricadono all'interno
            dei quartieri.

            I restanti **5 POI** rimangono
            nell'analisi a griglia.
            """
        )


    with st.expander(
        "Popolazione e densità"
    ):

        st.markdown(
            """
            Anno di riferimento:
            **2024**

            Residenti nei sei quartieri:
            **392.044**

            Senza fissa dimora:
            **747**

            Totale riconciliato:
            **392.791**
            """
        )


# ============================================================
# 17. FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Diversità Spaziale Urbana – Bologna | "
    "Workflow Python riproducibile"
)
