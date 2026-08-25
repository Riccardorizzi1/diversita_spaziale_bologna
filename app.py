# ============================================================
# DASHBOARD STREAMLIT
# DIVERSITÀ SPAZIALE URBANA - BOLOGNA
#
# VERSIONE FINALE
#
# - struttura GitHub piatta
# - sidebar sempre disponibile
# - barra Streamlit ridotta al minimo
# - logo SBL cliccabile
# - tema chiaro coerente anche da Dark Mode
# - palette aziendale
# - nessun HTML visualizzato come codice
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
# 2. ROOT
# ============================================================

ROOT = Path(__file__).resolve().parent


# ============================================================
# 3. FILE DEL PROGETTO
# Tutti nella root GitHub
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
# 4. LOGO SBL
# ============================================================

NOMI_LOGO = [
    "Logo_sbl.png",
    "Logo_SBL.png",
    "logo_sbl.png",
    "logo_SBL.png",
]

FILE_LOGO = None

for nome in NOMI_LOGO:

    candidato = (
        ROOT
        / nome
    )

    if candidato.exists():

        FILE_LOGO = candidato
        break


URL_SBL = (
    "https://www.sblconsultancy.it/"
)


# ============================================================
# 5. PALETTE AZIENDALE
# ============================================================

BLU = "#00649C"

AZZURRO = "#1C9FE8"

ARANCIONE = "#E8901C"

GRIGIO = "#495B69"

TESTO = "#1F2937"

TESTO_SECONDARIO = "#667085"

SFONDO = "#F6F8FA"

BIANCO = "#FFFFFF"

BORDO = "#DDE3E8"


# ============================================================
# 6. CSS
# ============================================================
#
# IMPORTANTE:
#
# NON nascondiamo più l'intero stHeader.
#
# Manteniamo una barra sottilissima e trasparente,
# necessaria a Streamlit per il controllo sidebar.
#
# Nascondiamo invece solo gli elementi inutili:
# Share, GitHub, menu, deploy ecc.
# ============================================================

st.html(
    f"""
    <style>

    /* ======================================================
       TEMA CHIARO
       ====================================================== */

    :root {{
        color-scheme: light !important;
    }}

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {{

        background-color:
            {SFONDO} !important;

        color:
            {TESTO} !important;
    }}


    /* ======================================================
       HEADER STREAMLIT
       ====================================================== */
       
    /*
    Non viene eliminato:
    serve per il controllo della sidebar.
    */

    header[data-testid="stHeader"] {{

        display:
            flex !important;

        visibility:
            visible !important;

        height:
            2.4rem !important;

        min-height:
            2.4rem !important;

        background:
            transparent !important;

        box-shadow:
            none !important;

        border:
            none !important;
    }}


    /* ======================================================
       NASCONDIAMO SOLO GLI ELEMENTI FASTIDIOSI
       ====================================================== */

    [data-testid="stHeaderActionElements"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="stAppDeployButton"],
    .stAppToolbar,
    #MainMenu,
    footer {{

        display:
            none !important;

        visibility:
            hidden !important;
    }}


    /* ======================================================
       CONTROLLO SIDEBAR SEMPRE DISPONIBILE
       ====================================================== */

    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {{

        display:
            flex !important;

        visibility:
            visible !important;

        opacity:
            1 !important;
    }}


    /* ======================================================
       CONTENUTO PRINCIPALE
       ====================================================== */

    .block-container {{

        max-width:
            1480px !important;

        padding-top:
            0.4rem !important;

        padding-bottom:
            2.5rem !important;

        padding-left:
            2rem !important;

        padding-right:
            2rem !important;
    }}


    /* ======================================================
       TESTI
       ====================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {{

        color:
            {TESTO} !important;
    }}

    p,
    li,
    label {{

        color:
            {TESTO} !important;
    }}


    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {{

        color:
            {TESTO} !important;
    }}


    [data-testid="stCaptionContainer"] {{

        color:
            {TESTO_SECONDARIO} !important;
    }}


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {{

        background-color:
            {BIANCO} !important;

        border-right:
            1px solid
            {BORDO} !important;
    }}


    [data-testid="stSidebarContent"] {{

        background-color:
            {BIANCO} !important;

        padding-top:
            0.7rem !important;
    }}


    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{

        color:
            {TESTO} !important;
    }}


    [data-testid="stSidebar"] hr {{

        border-color:
            {BORDO} !important;
    }}


    /* ======================================================
       NAVIGAZIONE RADIO
       ====================================================== */

    [data-testid="stRadio"],
    [data-testid="stRadio"] label {{

        color:
            {TESTO} !important;
    }}


    /* ======================================================
       KPI
       ====================================================== */

    [data-testid="stMetric"] {{

        background-color:
            {BIANCO} !important;

        border:
            1px solid
            {BORDO} !important;

        border-top:
            4px solid
            {AZZURRO} !important;

        border-radius:
            12px !important;

        padding:
            1rem
            1.1rem !important;

        min-height:
            115px;

        box-shadow:
            0 2px 8px
            rgba(
                0,
                0,
                0,
                0.045
            );
    }}


    [data-testid="stMetricValue"] {{

        color:
            {BLU} !important;

        font-weight:
            750 !important;
    }}


    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {{

        color:
            {GRIGIO} !important;

        font-weight:
            600 !important;
    }}


    /* ======================================================
       EXPANDER
       ====================================================== */

    [data-testid="stExpander"] {{

        background-color:
            {BIANCO} !important;

        border:
            1px solid
            {BORDO} !important;

        border-radius:
            10px !important;
    }}


    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {{

        background-color:
            {BIANCO} !important;

        color:
            {TESTO} !important;
    }}


    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    [data-testid="stExpander"] strong {{

        color:
            {TESTO} !important;
    }}


    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {{

        background-color:
            {BIANCO} !important;

        border-radius:
            10px !important;
    }}


    /* ======================================================
       IMMAGINI
       ====================================================== */

    [data-testid="stImage"] {{

        background-color:
            {BIANCO} !important;

        border-radius:
            10px !important;
    }}


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (
        max-width: 800px
    ) {{

        .block-container {{

            padding-left:
                1rem !important;

            padding-right:
                1rem !important;
        }}

    }}

    </style>
    """
)


# ============================================================
# 7. CONTROLLO FILE
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
    for file
    in FILE_NECESSARI
    if not file.exists()
]


if file_mancanti:

    st.error(
        "Mancano uno o più file "
        "necessari alla dashboard."
    )

    for file in file_mancanti:

        st.code(
            file.name
        )

    st.stop()


# ============================================================
# 8. LOGO SBL
# ============================================================

if FILE_LOGO is not None:

    st.sidebar.image(
        str(FILE_LOGO),
        width=115,
        link=URL_SBL,
    )

else:

    st.sidebar.link_button(
        "SBL Consultancy",
        URL_SBL,
    )


# ============================================================
# 9. NAVIGAZIONE
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
# 10. LETTURA DATI
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
# 11. HEADER AZIENDALE
# ============================================================

st.html(
    f"""
    <div
        style="
            background:
                linear-gradient(
                    105deg,
                    {BLU} 0%,
                    {AZZURRO} 100%
                );

            border-radius:
                14px;

            padding:
                24px
                28px;

            margin-bottom:
                26px;
        "
    >

        <div
            style="
                color:
                    white;

                font-size:
                    32px;

                line-height:
                    1.15;

                font-weight:
                    750;

                margin-bottom:
                    9px;
            "
        >
            Diversità Spaziale Urbana – Bologna
        </div>

        <div
            style="
                color:
                    white;

                font-size:
                    16px;

                line-height:
                    1.5;

                opacity:
                    0.96;
            "
        >
            Analisi della mixité funzionale urbana
            attraverso Points of Interest,
            indici di diversità e autocorrelazione spaziale.
        </div>

    </div>
    """
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

        st.metric(
            "POI classificati",
            "7.975",
        )


    with c2:

        st.metric(
            "Celle della griglia",
            "542",
        )


    with c3:

        st.metric(
            "Quartieri",
            "6",
        )


    with c4:

        st.metric(
            "Categorie funzionali",
            "8",
        )


    st.write("")


    c5, c6, c7 = (
        st.columns(3)
    )


    with c5:

        st.metric(
            "Moran's I globale",
            "0,2250",
        )


    with c6:

        st.metric(
            "p-value permutazionale",
            "0,0010",
        )


    with c7:

        st.metric(
            "Celle Moran/LISA",
            "481",
        )


    st.write("")


    st.html(
        f"""
        <div
            style="
                background:
                    {BIANCO};

                border:
                    1px solid
                    {BORDO};

                border-left:
                    5px solid
                    {ARANCIONE};

                border-radius:
                    11px;

                padding:
                    18px
                    22px;

                margin-bottom:
                    22px;

                color:
                    {TESTO};
            "
        >

            <div
                style="
                    font-weight:
                        700;

                    margin-bottom:
                        9px;
                "
            >
                Indicatore principale:
                Indice di Shannon
            </div>

            <div
                style="
                    line-height:
                        1.6;
                "
            >
                La diversità funzionale viene misurata
                sulla distribuzione di otto categorie di POI.

                Valori di Shannon più elevati indicano
                una composizione funzionale maggiormente
                equilibrata.
            </div>

        </div>
        """
    )


    g1, g2 = (
        st.columns(2)
    )


    with g1:

        st.image(
            str(
                FILE_SHANNON
            ),
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


    tabella = (
        quartieri[
            [
                "quartiere",
                "n_poi",
                "shannon",
                "simpson_dominance",
                "ricchezza",
                "residenti",
                "densita_ab_kmq",
            ]
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


    tabella["POI"] = (
        tabella["POI"]
        .astype(int)
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


    tabella["Ricchezza"] = (
        tabella["Ricchezza"]
        .astype(int)
    )


    tabella["Residenti"] = (
        tabella["Residenti"]
        .astype(int)
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
        hide_index=True,
        use_container_width=True,
    )


    st.write("")


    g1, g2 = (
        st.columns(2)
    )


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
            str(
                FILE_DENSITA
            ),
            caption=(
                "Diversità funzionale "
                "e densità abitativa"
            ),
            use_container_width=True,
        )


# ============================================================
# 15. GRAFICI ESPLORATIVI
# ============================================================

elif pagina == "Grafici esplorativi":

    st.subheader(
        "Grafici esplorativi"
    )


    g1, g2 = (
        st.columns(2)
    )


    with g1:

        st.image(
            str(
                FILE_SHANNON
            ),
            caption=(
                "Distribuzione dell'indice "
                "di Shannon"
            ),
            use_container_width=True,
        )


    with g2:

        st.image(
            str(
                FILE_SIMPSON
            ),
            caption=(
                "Distribuzione dell'indice "
                "di Simpson (dominanza)"
            ),
            use_container_width=True,
        )


    g3, g4 = (
        st.columns(2)
    )


    with g3:

        st.image(
            str(
                FILE_RICCHEZZA
            ),
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
                "Diversità funzionale "
                "per quartiere"
            ),
            use_container_width=True,
        )


    st.image(
        str(
            FILE_DENSITA
        ),
        caption=(
            "Relazione esplorativa tra "
            "diversità funzionale "
            "e densità abitativa"
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


    st.html(
        f"""
        <div
            style="
                background:
                    {BIANCO};

                border:
                    1px solid
                    {BORDO};

                border-left:
                    5px solid
                    {BLU};

                border-radius:
                    11px;

                padding:
                    20px
                    24px;

                margin-bottom:
                    20px;

                color:
                    {TESTO};

                line-height:
                    1.65;
            "
        >

            <div
                style="
                    margin-bottom:
                        12px;
                "
            >
                Il progetto misura la
                <strong>
                    diversità funzionale urbana
                </strong>
                nel Comune di Bologna attraverso
                la distribuzione spaziale dei
                <strong>
                    Points of Interest (POI)
                </strong>.
            </div>

            <div>
                L'impostazione costituisce un
                <strong>
                    adattamento dell'approccio
                    concettuale del progetto
                    spatial_diversity
                    dell'Università di Saragozza
                </strong>
                agli obiettivi specifici
                dell'analisi di Bologna.
            </div>

        </div>
        """
    )


    with st.expander(
        "Fonti e classificazione POI",
        expanded=True,
    ):

        st.markdown(
            """
**Fonte POI:** OpenStreetMap, tramite snapshot Geofabrik.

Il dataset finale comprende **7.975 POI**, classificati nelle otto categorie funzionali previste:

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
L'analisi locale utilizza una griglia adattiva con celle di:

- **250 m**
- **500 m**
- **1.000 m**

Le dimensioni vengono adattate alla densità osservata dei POI.

**Indice di Shannon**

`H = - Σ pᵢ ln(pᵢ)`

È l'indicatore principale di diversità funzionale.

**Simpson dominance**

`D = Σ pᵢ²`

Misura la dominanza delle categorie.

**Ricchezza categoriale**

Numero delle categorie funzionali presenti nell'unità spaziale.
            """
        )


    with st.expander(
        "Autocorrelazione spaziale"
    ):

        st.markdown(
            """
L'analisi viene effettuata sulle **481 celle con Shannon definito**.

- contiguità Queen
- pesi standardizzati per riga
- 999 permutazioni
- seed = 42
- Moran's I = **0,2250**
- p-value = **0,0010**

L'analisi LISA distingue i cluster locali **HH, LL, HL e LH**.
            """
        )


    with st.expander(
        "Scala dei quartieri"
    ):

        st.markdown(
            """
L'analisi territoriale comprende i **6 quartieri ufficiali di Bologna**.

Gli indicatori vengono ricalcolati direttamente sulla distribuzione dei POI del quartiere e non come media degli Shannon delle celle.

Dei **7.975 POI** complessivi:

- **7.970** ricadono nei quartieri ufficiali;
- **5** restano nell'analisi a griglia e non vengono assegnati artificialmente.
            """
        )


    with st.expander(
        "Popolazione e densità"
    ):

        st.markdown(
            """
Anno di riferimento: **2024**

Residenti attribuiti ai sei quartieri:

**392.044**

Residenti senza fissa dimora:

**747**

Totale riconciliato del Comune di Bologna:

**392.791 residenti**

La densità abitativa è calcolata come residenti per km².
            """
        )


    with st.expander(
        "Riferimento a spatial_diversity"
    ):

        st.markdown(
            """
Il progetto di Bologna costituisce un **adattamento concettuale** del progetto *spatial_diversity* dell'Università di Saragozza.

Il principio condiviso è la misurazione dell'eterogeneità funzionale attraverso le quote relative delle diverse funzioni e l'utilizzo di indici di diversità.

L'applicazione di Bologna utilizza POI e unità spaziali a griglia/quartiere, mentre il progetto originale di Saragozza utilizza principalmente informazioni catastali e superfici associate agli usi immobiliari.
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
