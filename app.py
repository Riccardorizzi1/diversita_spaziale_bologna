# ============================================================
# DASHBOARD STREAMLIT
# DIVERSITÀ SPAZIALE URBANA - BOLOGNA
#
# VERSIONE FINALE
# - Repository GitHub con struttura piatta
# - Logo SBL cliccabile
# - Barra Streamlit superiore nascosta
# - Tema chiaro forzato anche con Dark Mode
# - Palette aziendale
# - Correzione rendering HTML
# ============================================================

from pathlib import Path
from textwrap import dedent

import base64
import mimetypes

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
# 3. FILE DEL PROGETTO
# Tutti nella root del repository GitHub
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
#
# Il codice accetta automaticamente uno di questi nomi.
# Il file deve trovarsi nella root GitHub.
# ============================================================

POSSIBILI_LOGHI = [
    ROOT / "Logo_sbl.png",
    ROOT / "Logo_SBL.png",
    ROOT / "logo_sbl.png",
    ROOT / "logo_SBL.png",
]


FILE_LOGO = next(
    (
        file
        for file in POSSIBILI_LOGHI
        if file.exists()
    ),
    None,
)


# ============================================================
# 5. PALETTE AZIENDALE
# ============================================================

BLU = "#00649C"
BLU_MEDIO = "#2F6E9C"

AZZURRO = "#1C9FE8"
AZZURRO_CHIARO = "#A5CEEC"

ARANCIONE = "#E8901C"
ARANCIONE_CHIARO = "#E8B05D"

GRIGIO = "#495B69"
TESTO = "#1F2937"

SFONDO = "#F6F8FA"
BIANCO = "#FFFFFF"
BORDO = "#DDE3E8"


# ============================================================
# 6. CSS GENERALE
# ============================================================
#
# Obiettivi:
#
# - forza una resa chiara indipendentemente dal tema
#   selezionato dall'utente;
# - elimina la toolbar superiore di Streamlit;
# - mantiene leggibili sidebar, expander e contenuti;
# - elimina spazio inutile sopra alla dashboard.
# ============================================================

CSS = dedent(
    f"""
    <style>

    /* ======================================================
       FORZA TEMA CHIARO
       ====================================================== */

    :root {{
        color-scheme: light !important;
    }}

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background-color: {SFONDO} !important;
        color: {TESTO} !important;
    }}


    /* ======================================================
       RIMOZIONE BARRA SUPERIORE STREAMLIT
       ====================================================== */

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    #MainMenu,
    footer {{
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }}


    /* ======================================================
       CONTENITORE PRINCIPALE
       ====================================================== */

    .block-container {{
        padding-top: 1.1rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 1500px !important;
    }}


    /* ======================================================
       TESTI STREAMLIT
       ====================================================== */

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"] {{
        color: {TESTO} !important;
    }}

    h1,
    h2,
    h3,
    h4 {{
        color: {TESTO} !important;
    }}


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {{
        background-color: {BIANCO} !important;
        border-right: 1px solid {BORDO} !important;
    }}

    [data-testid="stSidebarContent"] {{
        background-color: {BIANCO} !important;
        padding-top: 1rem !important;
    }}

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {{
        color: {TESTO} !important;
    }}

    [data-testid="stSidebar"] hr {{
        border-color: {BORDO} !important;
    }}


    /* ======================================================
       HEADER AZIENDALE
       ====================================================== */

    .sbl-header {{
        background:
            linear-gradient(
                105deg,
                {BLU} 0%,
                {AZZURRO} 100%
            );

        border-radius: 14px;
        padding: 1.45rem 1.7rem;
        margin-bottom: 1.55rem;
    }}

    .sbl-header-title {{
        color: {BIANCO} !important;
        font-size: 2rem;
        line-height: 1.15;
        font-weight: 750;
        margin: 0;
    }}

    .sbl-header-subtitle {{
        color: {BIANCO} !important;
        margin-top: 0.55rem;
        margin-bottom: 0;
        font-size: 1rem;
        line-height: 1.55;
        opacity: 0.96;
    }}


    /* ======================================================
       LOGO SIDEBAR
       ====================================================== */

    .sbl-logo-container {{
        display: flex;
        align-items: center;
        justify-content: flex-start;
        margin-bottom: 1.2rem;
    }}

    .sbl-logo-container img {{
        width: 118px;
        max-width: 70%;
        height: auto;
        object-fit: contain;
    }}

    .sbl-logo-fallback {{
        display: inline-block;
        color: {BLU} !important;
        font-weight: 700;
        font-size: 1.1rem;
        text-decoration: none;
        margin-bottom: 1rem;
    }}


    /* ======================================================
       KPI
       ====================================================== */

    .sbl-kpi {{
        background-color: {BIANCO};
        border-radius: 11px;
        border: 1px solid {BORDO};
        border-top: 4px solid {AZZURRO};
        padding: 1.05rem 1.1rem;
        min-height: 112px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.045);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }}

    .sbl-kpi-value {{
        color: {BLU} !important;
        font-size: 1.8rem;
        line-height: 1.1;
        font-weight: 750;
        margin-bottom: 0.4rem;
    }}

    .sbl-kpi-label {{
        color: {GRIGIO} !important;
        font-size: 0.90rem;
        line-height: 1.3;
        font-weight: 600;
    }}


    /* ======================================================
       BOX INFORMATIVI
       ====================================================== */

    .sbl-info {{
        background-color: {BIANCO};
        border: 1px solid {BORDO};
        border-left: 5px solid {ARANCIONE};
        border-radius: 11px;
        padding: 1.15rem 1.35rem;
        margin-top: 0.5rem;
        margin-bottom: 1.2rem;
        color: {TESTO} !important;
    }}

    .sbl-info p {{
        color: {TESTO} !important;
        margin-bottom: 0.5rem;
    }}

    .sbl-method {{
        background-color: {BIANCO};
        border: 1px solid {BORDO};
        border-left: 5px solid {BLU};
        border-radius: 11px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
        color: {TESTO} !important;
    }}

    .sbl-method p {{
        color: {TESTO} !important;
    }}


    /* ======================================================
       EXPANDER
       ====================================================== */

    [data-testid="stExpander"] {{
        background-color: {BIANCO} !important;
        border: 1px solid {BORDO} !important;
        border-radius: 9px !important;
        overflow: hidden;
    }}

    [data-testid="stExpander"] summary {{
        background-color: {BIANCO} !important;
        color: {TESTO} !important;
    }}

    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    [data-testid="stExpander"] strong {{
        color: {TESTO} !important;
    }}


    /* ======================================================
       TABELLA QUARTIERI
       ====================================================== */

    .sbl-table-wrap {{
        width: 100%;
        overflow-x: auto;
        background: {BIANCO};
        border: 1px solid {BORDO};
        border-radius: 10px;
        margin-bottom: 1.2rem;
    }}

    .sbl-table {{
        width: 100%;
        border-collapse: collapse;
        font-size: 0.92rem;
        color: {TESTO};
    }}

    .sbl-table th {{
        background-color: {BLU};
        color: {BIANCO};
        padding: 0.8rem 0.75rem;
        text-align: left;
        white-space: nowrap;
    }}

    .sbl-table td {{
        padding: 0.72rem 0.75rem;
        border-bottom: 1px solid {BORDO};
        color: {TESTO};
        background-color: {BIANCO};
        white-space: nowrap;
    }}

    .sbl-table tr:last-child td {{
        border-bottom: 0;
    }}

    .sbl-table tbody tr:hover td {{
        background-color: #F0F7FB;
    }}


    /* ======================================================
       IMMAGINI
       ====================================================== */

    [data-testid="stImage"] {{
        background-color: {BIANCO} !important;
        border-radius: 10px;
    }}


    /* ======================================================
       RADIO SIDEBAR
       ====================================================== */

    [data-testid="stRadio"] {{
        color: {TESTO} !important;
    }}

    [data-testid="stRadio"] label {{
        color: {TESTO} !important;
    }}


    /* ======================================================
       LINK
       ====================================================== */

    a {{
        color: {BLU};
    }}


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (max-width: 800px) {{

        .sbl-header-title {{
            font-size: 1.55rem;
        }}

        .block-container {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

    }}

    </style>
    """
)


st.markdown(
    CSS,
    unsafe_allow_html=True,
)


# ============================================================
# 7. FUNZIONE PER CONVERTIRE IL LOGO IN BASE64
# ============================================================

def immagine_base64(
    file_path: Path,
):

    mime_type, _ = (
        mimetypes.guess_type(
            str(file_path)
        )
    )

    if mime_type is None:
        mime_type = "image/png"

    encoded = (
        base64.b64encode(
            file_path.read_bytes()
        )
        .decode("utf-8")
    )

    return (
        f"data:{mime_type};base64,"
        f"{encoded}"
    )


# ============================================================
# 8. LOGO SBL CLICCABILE
# ============================================================

if FILE_LOGO is not None:

    logo_src = (
        immagine_base64(
            FILE_LOGO
        )
    )

    logo_html = dedent(
        f"""
        <div class="sbl-logo-container">
            <a
                href="https://www.sblconsultancy.it/"
                target="_blank"
                rel="noopener noreferrer"
                title="SBL Consultancy"
            >
                <img
                    src="{logo_src}"
                    alt="SBL Consultancy"
                >
            </a>
        </div>
        """
    )

else:

    logo_html = dedent(
        f"""
        <a
            class="sbl-logo-fallback"
            href="https://www.sblconsultancy.it/"
            target="_blank"
            rel="noopener noreferrer"
        >
            SBL Consultancy
        </a>
        """
    )


st.sidebar.markdown(
    logo_html,
    unsafe_allow_html=True,
)


# ============================================================
# 9. CONTROLLO FILE NECESSARI
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
        "File mancanti:"
    )

    for file in file_mancanti:

        st.code(
            file.name
        )

    st.stop()


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
# 11. KPI
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
# 12. HEADER
# ============================================================

header_html = dedent(
    """
    <div class="sbl-header">

        <div class="sbl-header-title">
            Diversità Spaziale Urbana – Bologna
        </div>

        <div class="sbl-header-subtitle">
            Analisi della mixité funzionale urbana
            attraverso Points of Interest,
            indici di diversità e autocorrelazione spaziale.
        </div>

    </div>
    """
)


st.markdown(
    header_html,
    unsafe_allow_html=True,
)


# ============================================================
# 13. NAVIGAZIONE
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
# 14. FUNZIONE KPI
# ============================================================

def mostra_kpi(
    valore,
    etichetta,
):

    html = dedent(
        f"""
        <div class="sbl-kpi">

            <div class="sbl-kpi-value">
                {valore}
            </div>

            <div class="sbl-kpi-label">
                {etichetta}
            </div>

        </div>
        """
    )

    st.markdown(
        html,
        unsafe_allow_html=True,
    )


# ============================================================
# 15. PANORAMICA
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
            f"{n_celle}",
            "Celle della griglia",
        )


    with c3:

        mostra_kpi(
            f"{n_quartieri}",
            "Quartieri",
        )


    with c4:

        mostra_kpi(
            f"{n_categorie}",
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
            f"{n_celle_lisa}",
            "Celle Moran/LISA",
        )


    st.write("")


    info_html = dedent(
        """
        <div class="sbl-info">

            <p>
                <strong>
                    Indicatore principale:
                    Indice di Shannon.
                </strong>
            </p>

            <p>
                La diversità funzionale viene
                misurata sulla distribuzione
                di otto categorie di POI.
            </p>

            <p>
                Valori di Shannon più elevati
                indicano una composizione funzionale
                maggiormente equilibrata.
            </p>

        </div>
        """
    )


    st.markdown(
        info_html,
        unsafe_allow_html=True,
    )


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
# 16. MAPPA INTERATTIVA
# ============================================================

elif pagina == "Mappa interattiva":

    st.subheader(
        "Mappa interattiva"
    )


    st.caption(
        "Attiva o disattiva i layer "
        "della griglia, dei quartieri "
        "e delle otto categorie POI."
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
# 17. QUARTIERI
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


    # --------------------------------------------------------
    # Formattazione leggibile
    # --------------------------------------------------------

    tabella["n_poi"] = (
        tabella["n_poi"]
        .astype(int)
        .map(
            lambda x:
            f"{x:,}".replace(
                ",",
                "."
            )
        )
    )


    tabella["shannon"] = (
        tabella["shannon"]
        .map(
            lambda x:
            f"{x:.4f}".replace(
                ".",
                ","
            )
        )
    )


    tabella[
        "simpson_dominance"
    ] = (
        tabella[
            "simpson_dominance"
        ]
        .map(
            lambda x:
            f"{x:.4f}".replace(
                ".",
                ","
            )
        )
    )


    tabella["ricchezza"] = (
        tabella["ricchezza"]
        .astype(int)
    )


    tabella["residenti"] = (
        tabella["residenti"]
        .astype(int)
        .map(
            lambda x:
            f"{x:,}".replace(
                ",",
                "."
            )
        )
    )


    tabella[
        "densita_ab_kmq"
    ] = (
        tabella[
            "densita_ab_kmq"
        ]
        .map(
            lambda x:
            f"{x:,.1f}"
            .replace(
                ",",
                "X"
            )
            .replace(
                ".",
                ","
            )
            .replace(
                "X",
                "."
            )
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


    tabella_html = (
        tabella.to_html(
            index=False,
            classes="sbl-table",
            border=0,
            escape=True,
        )
    )


    st.markdown(
        (
            '<div class="sbl-table-wrap">'
            + tabella_html
            + "</div>"
        ),
        unsafe_allow_html=True,
    )


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
# 18. GRAFICI ESPLORATIVI
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
                "Distribuzione dell'indice "
                "di Shannon"
            ),
            use_container_width=True,
        )


    with g2:

        st.image(
            str(FILE_SIMPSON),
            caption=(
                "Distribuzione dell'indice "
                "di Simpson (dominanza)"
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
                "Diversità funzionale "
                "per quartiere"
            ),
            use_container_width=True,
        )


    st.image(
        str(FILE_DENSITA),
        caption=(
            "Relazione esplorativa tra "
            "diversità funzionale "
            "e densità abitativa"
        ),
        use_container_width=True,
    )


# ============================================================
# 19. METODOLOGIA
# ============================================================

elif pagina == "Metodologia":

    st.subheader(
        "Nota metodologica"
    )


    metodo_html = dedent(
        """
        <div class="sbl-method">

            <p>
                Il progetto misura la
                <strong>
                    diversità funzionale urbana
                </strong>
                nel Comune di Bologna attraverso
                la distribuzione spaziale dei
                <strong>
                    Points of Interest (POI)
                </strong>.
            </p>

            <p>
                L'impostazione costituisce un
                <strong>
                    adattamento dell'approccio
                    concettuale del progetto
                    spatial_diversity
                    dell'Università di Saragozza
                </strong>
                agli obiettivi specifici
                dell'analisi di Bologna e alla
                disponibilità di dati aperti.
            </p>

        </div>
        """
    )


    st.markdown(
        metodo_html,
        unsafe_allow_html=True,
    )


    with st.expander(
        "Fonti e classificazione POI",
        expanded=True,
    ):

        st.markdown(
            """
**Fonte dei POI:** OpenStreetMap, tramite snapshot Geofabrik.

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

Gli indicatori vengono ricalcolati direttamente sulla distribuzione delle categorie POI del quartiere e non come media degli Shannon delle celle.

Dei **7.975 POI** complessivi:

- **7.970** ricadono nei quartieri ufficiali;
- **5** restano nell'analisi a griglia e non vengono assegnati artificialmente a un quartiere.
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

L'applicazione di Bologna utilizza tuttavia POI e unità spaziali a griglia/quartiere, mentre il progetto originale di Saragozza utilizza principalmente informazioni catastali e superfici associate agli usi immobiliari.
            """
        )


# ============================================================
# 20. FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Diversità Spaziale Urbana – Bologna | "
    "Workflow Python riproducibile"
)
