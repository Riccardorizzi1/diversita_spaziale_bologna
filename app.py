# ============================================================
# DIVERSITÀ SPAZIALE URBANA - BOLOGNA
# Dashboard Streamlit
#
# VERSIONE COMPLETA DEFINITIVA
# ============================================================

from pathlib import Path
from io import BytesIO

import geopandas as gpd
import streamlit as st
import streamlit.components.v1 as components

from PIL import (
    Image,
    ImageChops,
    ImageEnhance,
    ImageFilter,
)


# ============================================================
# 1. CONFIGURAZIONE STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Diversità Spaziale Bologna",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="locked",
)


# ============================================================
# 2. ROOT DEL REPOSITORY
# ============================================================

ROOT = Path(__file__).resolve().parent


# ============================================================
# 3. FILE DEL PROGETTO
# Tutti i file sono nella root GitHub
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

    candidato = ROOT / nome

    if candidato.exists():

        FILE_LOGO = candidato
        break


URL_SBL = (
    "https://www.sblconsultancy.it/"
)


# ============================================================
# 5. PREPARAZIONE LOGO HD
# ============================================================
#
# Il logo viene:
# - ritagliato automaticamente;
# - ingrandito con LANCZOS;
# - leggermente contrastato;
# - leggermente sharpened;
# - mantenuto come PNG.
#
# Non modifica il file originale.
# ============================================================

@st.cache_data(
    show_spinner=False
)
def prepara_logo_hd(
    percorso_logo: str,
):

    with Image.open(
        percorso_logo
    ) as img:

        img = img.convert(
            "RGBA"
        )


        # ----------------------------------------------------
        # Rimozione automatica dello spazio bianco
        # ----------------------------------------------------

        rgb = Image.new(
            "RGB",
            img.size,
            "white",
        )

        rgb.paste(
            img,
            mask=img.getchannel("A"),
        )


        sfondo = Image.new(
            "RGB",
            rgb.size,
            "white",
        )


        differenza = (
            ImageChops.difference(
                rgb,
                sfondo,
            )
        )


        differenza = (
            ImageEnhance
            .Contrast(
                differenza
            )
            .enhance(
                2.0
            )
        )


        bbox = (
            differenza.getbbox()
        )


        if bbox is not None:

            sx, alto, dx, basso = bbox


            larghezza_logo = (
                dx - sx
            )

            altezza_logo = (
                basso - alto
            )


            padding_x = max(
                4,
                int(
                    larghezza_logo
                    * 0.06
                ),
            )

            padding_y = max(
                4,
                int(
                    altezza_logo
                    * 0.06
                ),
            )


            sx = max(
                0,
                sx - padding_x,
            )

            alto = max(
                0,
                alto - padding_y,
            )

            dx = min(
                img.width,
                dx + padding_x,
            )

            basso = min(
                img.height,
                basso + padding_y,
            )


            img = img.crop(
                (
                    sx,
                    alto,
                    dx,
                    basso,
                )
            )


        # ----------------------------------------------------
        # Upscaling
        # ----------------------------------------------------

        larghezza_target = max(
            1600,
            img.width,
        )


        rapporto = (
            larghezza_target
            / img.width
        )


        altezza_target = int(
            round(
                img.height
                * rapporto
            )
        )


        if (
            img.width
            != larghezza_target
        ):

            img = img.resize(
                (
                    larghezza_target,
                    altezza_target,
                ),
                Image.Resampling.LANCZOS,
            )


        # ----------------------------------------------------
        # Contrasto leggerissimo
        # ----------------------------------------------------

        img = (
            ImageEnhance
            .Contrast(
                img
            )
            .enhance(
                1.04
            )
        )


        # ----------------------------------------------------
        # Unsharp Mask
        # ----------------------------------------------------

        img = img.filter(
            ImageFilter.UnsharpMask(
                radius=1.4,
                percent=145,
                threshold=3,
            )
        )


        # ----------------------------------------------------
        # Nitidezza finale
        # ----------------------------------------------------

        img = (
            ImageEnhance
            .Sharpness(
                img
            )
            .enhance(
                1.10
            )
        )


        # ----------------------------------------------------
        # Salvataggio in memoria
        # ----------------------------------------------------

        buffer = BytesIO()


        img.save(
            buffer,
            format="PNG",
            optimize=False,
        )


        return buffer.getvalue()


# ============================================================
# 6. LOGO NELLA SIDEBAR
# ============================================================

if FILE_LOGO is not None:

    logo_hd = prepara_logo_hd(
        str(FILE_LOGO)
    )


    st.sidebar.image(
        logo_hd,
        width=155,
        link=URL_SBL,
    )

else:

    st.sidebar.link_button(
        "SBL Consultancy",
        URL_SBL,
    )


# ============================================================
# 7. MODALITÀ LIGHT / DARK
# ============================================================

dark_mode = st.sidebar.toggle(
    "Modalità scura",
    value=False,
    key="modalita_scura",
)


# ============================================================
# 8. COLORI AZIENDALI
# ============================================================

BLU = "#00649C"

AZZURRO = "#1C9FE8"

ARANCIONE = "#E8901C"


# ============================================================
# 9. COLORI INTERFACCIA DINAMICI
# ============================================================

if dark_mode:

    SFONDO = "#101722"

    SIDEBAR = "#151D29"

    CARD = "#1C2634"

    CARD_SECONDARIA = "#202C3B"

    TESTO = "#F4F6F8"

    TESTO_SECONDARIO = "#BEC8D4"

    BORDO = "#344153"

    LABEL = "#D5DCE5"

    OMBRA = (
        "rgba(0, 0, 0, 0.28)"
    )

else:

    SFONDO = "#F5F7F9"

    SIDEBAR = "#FFFFFF"

    CARD = "#FFFFFF"

    CARD_SECONDARIA = "#F8FAFB"

    TESTO = "#202936"

    TESTO_SECONDARIO = "#667085"

    BORDO = "#DCE3E8"

    LABEL = "#495B69"

    OMBRA = (
        "rgba(0, 0, 0, 0.045)"
    )


# ============================================================
# 10. CSS COMPLETO
# ============================================================

st.html(
    f"""
    <style>

    /* ======================================================
       MODALITÀ COLORE
       ====================================================== */

    :root {{
        color-scheme:
            {"dark" if dark_mode else "light"}
            !important;
    }}


    /* ======================================================
       APP
       ====================================================== */

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
       BARRA STREAMLIT
       ====================================================== */

    header[data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stHeaderActionElements"],
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

        height:
            0 !important;

        min-height:
            0 !important;
    }}


    /* ======================================================
       CONTENUTO PRINCIPALE
       ====================================================== */

    .block-container {{

        max-width:
            1480px !important;

        padding-top:
            1.25rem !important;

        padding-bottom:
            2.5rem !important;

        padding-left:
            2rem !important;

        padding-right:
            2rem !important;
    }}


    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"],
    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {{

        background-color:
            {SIDEBAR} !important;
    }}


    section[data-testid="stSidebar"] {{

        border-right:
            1px solid
            {BORDO} !important;
    }}


    [data-testid="stSidebarUserContent"] {{

        padding-top:
            1.2rem !important;
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
       LOGO
       ====================================================== */

    [data-testid="stSidebar"]
    [data-testid="stImage"] img {{

        image-rendering:
            auto;

        backface-visibility:
            hidden;

        transform:
            translateZ(0);
    }}


    /* ======================================================
       RADIO + TOGGLE
       ====================================================== */

    [data-testid="stRadio"] label,
    [data-testid="stWidgetLabel"] {{

        color:
            {TESTO} !important;
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
       KPI
       ====================================================== */

    [data-testid="stMetric"] {{

        background-color:
            {CARD} !important;

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
            1.15rem !important;

        min-height:
            120px;

        box-shadow:
            0 2px 8px
            {OMBRA};
    }}


    [data-testid="stMetricValue"] {{

        color:
            {TESTO} !important;

        font-weight:
            750 !important;
    }}


    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {{

        color:
            {LABEL} !important;

        font-weight:
            600 !important;
    }}


    /* ======================================================
       EXPANDER
       ====================================================== */

    [data-testid="stExpander"],
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {{

        background-color:
            {CARD} !important;

        color:
            {TESTO} !important;
    }}


    [data-testid="stExpander"] {{

        border:
            1px solid
            {BORDO} !important;

        border-radius:
            10px !important;
    }}


    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    [data-testid="stExpander"] strong {{

        color:
            {TESTO} !important;
    }}


    /* ======================================================
       IMMAGINI
       ====================================================== */

    [data-testid="stImage"] {{

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
# 11. NAVIGAZIONE
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
    key="navigazione_principale",
)


st.sidebar.markdown("---")


st.sidebar.caption(
    "Comune di Bologna"
)


st.sidebar.caption(
    "OpenStreetMap / Comune di Bologna"
)


# ============================================================
# 12. CONTROLLO FILE
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
# 13. LETTURA DATI
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
# 14. VALORI KPI
# ============================================================

n_poi = len(
    poi
)

n_celle = len(
    griglia
)

n_quartieri = len(
    quartieri
)

n_categorie = (
    poi[
        "categoria_finale"
    ]
    .nunique()
)

n_celle_lisa = len(
    lisa
)


# ============================================================
# 15. HEADER AZIENDALE
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
                25px 30px;

            margin-bottom:
                28px;
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
                    0.97;
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
# 16. PANORAMICA
# ============================================================

if pagina == "Panoramica":

    st.subheader(
        "Quadro generale"
    )


    # --------------------------------------------------------
    # KPI - RIGA 1
    # --------------------------------------------------------

    c1, c2, c3, c4 = (
        st.columns(4)
    )


    with c1:

        st.metric(
            "POI classificati",
            f"{n_poi:,}".replace(
                ",",
                "."
            ),
        )


    with c2:

        st.metric(
            "Celle della griglia",
            str(
                n_celle
            ),
        )


    with c3:

        st.metric(
            "Quartieri",
            str(
                n_quartieri
            ),
        )


    with c4:

        st.metric(
            "Categorie funzionali",
            str(
                n_categorie
            ),
        )


    st.write("")


    # --------------------------------------------------------
    # KPI - RIGA 2
    # --------------------------------------------------------

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
            str(
                n_celle_lisa
            ),
        )


    st.write("")


    # --------------------------------------------------------
    # NOTA SHANNON
    # --------------------------------------------------------

    st.html(
        f"""
        <div
            style="
                background:
                    {CARD};

                border:
                    1px solid
                    {BORDO};

                border-left:
                    5px solid
                    {ARANCIONE};

                border-radius:
                    11px;

                padding:
                    18px 22px;

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


    # --------------------------------------------------------
    # GRAFICI
    # --------------------------------------------------------

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
# 17. MAPPA INTERATTIVA
# ============================================================

elif pagina == "Mappa interattiva":

    st.subheader(
        "Mappa interattiva"
    )


    st.caption(
        "Attiva o disattiva i layer della griglia, "
        "dei quartieri e delle otto categorie POI."
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
# 18. QUARTIERI
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


    # --------------------------------------------------------
    # Formati italiani
    # --------------------------------------------------------

    tabella["POI"] = (
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


    tabella["Shannon"] = (
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
        "Simpson dominance"
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


    tabella["Ricchezza"] = (
        tabella["ricchezza"]
        .astype(int)
    )


    tabella["Residenti"] = (
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
        "Densità ab./km²"
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


    tabella_finale = (
        tabella[
            [
                "quartiere",
                "POI",
                "Shannon",
                "Simpson dominance",
                "Ricchezza",
                "Residenti",
                "Densità ab./km²",
            ]
        ]
        .rename(
            columns={
                "quartiere":
                    "Quartiere"
            }
        )
    )


    # --------------------------------------------------------
    # Costruzione righe HTML
    # --------------------------------------------------------

    righe_html = ""


    for _, riga in (
        tabella_finale.iterrows()
    ):

        righe_html += f"""
        <tr>
            <td>{riga["Quartiere"]}</td>
            <td>{riga["POI"]}</td>
            <td>{riga["Shannon"]}</td>
            <td>{riga["Simpson dominance"]}</td>
            <td>{riga["Ricchezza"]}</td>
            <td>{riga["Residenti"]}</td>
            <td>{riga["Densità ab./km²"]}</td>
        </tr>
        """


    # --------------------------------------------------------
    # Tabella
    # --------------------------------------------------------

    st.html(
        f"""
        <div
            style="
                overflow-x:
                    auto;

                background:
                    {CARD};

                border:
                    1px solid
                    {BORDO};

                border-radius:
                    10px;

                margin-bottom:
                    22px;
            "
        >

        <table
            style="
                width:
                    100%;

                border-collapse:
                    collapse;

                color:
                    {TESTO};

                font-size:
                    14px;
            "
        >

            <thead>

                <tr
                    style="
                        background:
                            {BLU};

                        color:
                            white;
                    "
                >

                    <th style="padding:12px;text-align:left;">
                        Quartiere
                    </th>

                    <th style="padding:12px;text-align:left;">
                        POI
                    </th>

                    <th style="padding:12px;text-align:left;">
                        Shannon
                    </th>

                    <th style="padding:12px;text-align:left;">
                        Simpson dominance
                    </th>

                    <th style="padding:12px;text-align:left;">
                        Ricchezza
                    </th>

                    <th style="padding:12px;text-align:left;">
                        Residenti
                    </th>

                    <th style="padding:12px;text-align:left;">
                        Densità ab./km²
                    </th>

                </tr>

            </thead>


            <tbody>
                {righe_html}
            </tbody>

        </table>

        </div>
        """
    )


    # --------------------------------------------------------
    # Grafici
    # --------------------------------------------------------

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
# 19. GRAFICI ESPLORATIVI
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
# 20. METODOLOGIA
# ============================================================

elif pagina == "Metodologia":

    st.subheader(
        "Nota metodologica"
    )


    # --------------------------------------------------------
    # Introduzione
    # --------------------------------------------------------

    st.html(
        f"""
        <div
            style="
                background:
                    {CARD};

                border:
                    1px solid
                    {BORDO};

                border-left:
                    5px solid
                    {BLU};

                border-radius:
                    11px;

                padding:
                    20px 24px;

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


    # --------------------------------------------------------
    # POI
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Griglia
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Moran / LISA
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Quartieri
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Popolazione
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # Saragozza
    # --------------------------------------------------------

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
# 21. FOOTER
# ============================================================

st.markdown("---")


st.caption(
    "Diversità Spaziale Urbana – Bologna | "
    "Workflow Python riproducibile"
)
