# ============================================================
# DIVERSITÀ SPAZIALE URBANA
# BOLOGNA + FIRENZE
#
# Dashboard Streamlit multi-città
# VERSIONE COMPLETA DEFINITIVA
# ============================================================

from pathlib import Path
from io import BytesIO

import pandas as pd
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
    page_title="Diversità Spaziale Urbana",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. ROOT DEL REPOSITORY
# ============================================================

ROOT = Path(__file__).resolve().parent


# ============================================================
# 3. CONFIGURAZIONE DELLE CITTÀ
# ============================================================
#
# Un unico motore dashboard.
#
# Le differenze tra Bologna e Firenze sono gestite
# esclusivamente tramite configurazione.
# ============================================================

CONFIG = {

    "Bologna": {

        "nome":
            "Bologna",

        "file_poi":
            ROOT
            / "bologna_poi_classificati.gpkg",

        "file_griglia":
            ROOT
            / "griglia_indici_bologna.gpkg",

        "file_lisa":
            ROOT
            / "griglia_lisa_bologna.gpkg",

        "file_quartieri":
            ROOT
            / "quartieri_indici_popolazione_bologna.gpkg",

        "file_mappa":
            ROOT
            / "mappa_diversita_bologna.html",

        "file_shannon":
            ROOT
            / "distribuzione_shannon.png",

        "file_simpson":
            ROOT
            / "distribuzione_simpson.png",

        "file_ricchezza":
            ROOT
            / "distribuzione_ricchezza.png",

        "file_quartieri_shannon":
            ROOT
            / "confronto_shannon_quartieri.png",

        "file_densita":
            ROOT
            / "relazione_shannon_densita.png",

        "file_summary":
            None,

        "anno_popolazione":
            2024,

        "moran_i":
            0.2250,

        "moran_p":
            0.0010,

        "n_celle_moran":
            481,

        "poi_quartieri":
            7970,

        "poi_fuori_quartieri":
            5,

        "residenti_quartieri":
            392044,

        "residenti_non_indicato":
            747,

        "residenti_comune":
            392791,

        "fonte":
            "OpenStreetMap / Comune di Bologna",

        "nota_cartografica":
            None,
    },


    "Firenze": {

        "nome":
            "Firenze",

        "file_poi":
            ROOT
            / "firenze_poi_classificati.gpkg",

        "file_griglia":
            ROOT
            / "griglia_indici_firenze.gpkg",

        "file_lisa":
            ROOT
            / "griglia_lisa_firenze.gpkg",

        "file_quartieri":
            ROOT
            / "quartieri_indici_popolazione_firenze.gpkg",

        "file_mappa":
            ROOT
            / "mappa_diversita_firenze.html",

        "file_shannon":
            ROOT
            / "distribuzione_shannon_firenze.png",

        "file_simpson":
            ROOT
            / "distribuzione_simpson_firenze.png",

        "file_ricchezza":
            ROOT
            / "distribuzione_ricchezza_firenze.png",

        "file_quartieri_shannon":
            ROOT
            / "confronto_shannon_quartieri_firenze.png",

        "file_densita":
            ROOT
            / "relazione_shannon_densita_firenze.png",

        "file_summary":
            ROOT
            / "dashboard_summary_firenze.csv",

        "anno_popolazione":
            2025,

        "fonte":
            "OpenStreetMap / Comune di Firenze / ISTAT",

        "nota_cartografica":
            (
                "Per Firenze le geometrie dei quartieri "
                "sono armonizzate al perimetro comunale "
                "esclusivamente nella visualizzazione "
                "cartografica. I dati territoriali "
                "originali, l'assegnazione dei POI "
                "e gli indicatori non vengono modificati."
            ),
    },
}


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
# 5. PREPARAZIONE LOGO HD
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
        # Rimozione spazio bianco
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
        # Contrasto e nitidezza
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


        img = img.filter(
            ImageFilter.UnsharpMask(
                radius=1.4,
                percent=145,
                threshold=3,
            )
        )


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
        str(
            FILE_LOGO
        )
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
# 7. SELEZIONE CITTÀ
# ============================================================

st.sidebar.title(
    "Area di analisi"
)


citta = st.sidebar.radio(
    "Seleziona la città",
    [
        "Bologna",
        "Firenze",
    ],
    index=0,
    key="selezione_citta",
)


cfg = (
    CONFIG[
        citta
    ]
)


# ============================================================
# 8. MODALITÀ LIGHT / DARK
# ============================================================

st.sidebar.markdown(
    "---"
)


dark_mode = st.sidebar.toggle(
    "Modalità scura",
    value=False,
    key="modalita_scura",
)


# ============================================================
# 9. PALETTE SBL
# ============================================================
#
# Palette costruita sul riferimento grafico SBL:
#
# - blu navy
# - blu petrolio
# - azzurro
# - arancione
# - bianco
# ============================================================

BLU_NAVY = "#16384F"

BLU_PETROLIO = "#24536D"

BLU = "#00649C"

AZZURRO = "#39AFD4"

AZZURRO_CHIARO = "#BDE8F4"

ARANCIONE = "#FF9828"

ARANCIONE_CHIARO = "#FFD29A"

BIANCO = "#FFFFFF"


# ============================================================
# 10. COLORI DINAMICI INTERFACCIA
# ============================================================

if dark_mode:

    SFONDO = "#0E1821"

    SIDEBAR = "#142532"

    CARD = "#192C39"

    CARD_SECONDARIA = "#203744"

    TESTO = "#F5F8FA"

    TESTO_SECONDARIO = "#B9C8D1"

    BORDO = "#34505F"

    LABEL = "#D5E0E6"

    OMBRA = (
        "rgba(0,0,0,0.30)"
    )

else:

    SFONDO = "#F5F8FA"

    SIDEBAR = "#FFFFFF"

    CARD = "#FFFFFF"

    CARD_SECONDARIA = "#EFF7FA"

    TESTO = "#173648"

    TESTO_SECONDARIO = "#677D89"

    BORDO = "#D8E6EC"

    LABEL = "#3F5C6B"

    OMBRA = (
        "rgba(22,56,79,0.08)"
    )


# ============================================================
# 11. CSS COMPLETO
# ============================================================

st.html(
    f"""
    <style>

    /* ======================================================
       COLOR SCHEME
       ====================================================== */

    :root {{

        color-scheme:
            {"dark" if dark_mode else "light"}
            !important;

    }}


    /* ======================================================
       APP GENERALE
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
       HEADER STREAMLIT
       NON VIENE ELIMINATO:
       serve anche per il controllo della sidebar
       ====================================================== */

    header[data-testid="stHeader"] {{

        background:
            {SFONDO} !important;

        color:
            {TESTO} !important;

        height:
            3rem !important;

    }}


    /* ======================================================
       NASCONDIAMO SOLO GLI ELEMENTI NON NECESSARI
       SENZA ELIMINARE IL CONTROLLO SIDEBAR
       ====================================================== */

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

    }}


    /* ======================================================
       CONTROLLO SIDEBAR SEMPRE ACCESSIBILE
       ====================================================== */

    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {{

        visibility:
            visible !important;

        display:
            flex !important;

    }}


    /* ======================================================
       CONTENUTO PRINCIPALE
       ====================================================== */

    .block-container {{

        max-width:
            1480px !important;

        padding-top:
            0.7rem !important;

        padding-bottom:
            3rem !important;

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
            1rem !important;

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
       LOGO SIDEBAR
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
       RADIO CITTÀ
       ====================================================== */

    [data-testid="stRadio"] > div {{

        gap:
            0.35rem !important;

    }}


    [data-testid="stRadio"] label {{

        background:
            {CARD_SECONDARIA};

        border:
            1px solid
            {BORDO};

        border-radius:
            8px;

        padding:
            7px 10px;

        margin-bottom:
            3px;

        transition:
            all 0.15s ease;

    }}


    [data-testid="stRadio"] label:hover {{

        border-color:
            {AZZURRO};

    }}


    /* ======================================================
       TESTI GENERALI
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
            0 3px 10px
            {OMBRA};

    }}


    [data-testid="stMetricValue"] {{

        color:
            {
                BLU_NAVY
                if not dark_mode
                else AZZURRO_CHIARO
            }
            !important;

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
       LINK
       ====================================================== */

    a {{

        color:
            {AZZURRO} !important;

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
# 12. INFO SIDEBAR
# ============================================================

st.sidebar.markdown(
    "---"
)


st.sidebar.caption(
    f"Comune di {citta}"
)


st.sidebar.caption(
    cfg[
        "fonte"
    ]
)


# ============================================================
# 13. CONTROLLO FILE
# ============================================================

FILE_NECESSARI = [
    cfg["file_poi"],
    cfg["file_griglia"],
    cfg["file_lisa"],
    cfg["file_quartieri"],
    cfg["file_mappa"],
    cfg["file_shannon"],
    cfg["file_simpson"],
    cfg["file_ricchezza"],
    cfg["file_quartieri_shannon"],
    cfg["file_densita"],
]


if (
    cfg[
        "file_summary"
    ]
    is not None
):

    FILE_NECESSARI.append(
        cfg[
            "file_summary"
        ]
    )


file_mancanti = [
    file
    for file
    in FILE_NECESSARI
    if not file.exists()
]


if file_mancanti:

    st.error(
        f"Mancano uno o più file "
        f"necessari per {citta}."
    )


    for file in file_mancanti:

        st.code(
            file.name
        )


    st.stop()


# ============================================================
# 14. FUNZIONI DI LETTURA
# ============================================================

@st.cache_data(
    show_spinner=False
)
def carica_gpkg(
    percorso: str,
):

    return gpd.read_file(
        percorso
    )


@st.cache_data(
    show_spinner=False
)
def carica_summary(
    percorso: str,
):

    tabella = pd.read_csv(
        percorso
    )


    return (
        tabella
        .set_index(
            "metrica"
        )[
            "valore"
        ]
        .to_dict()
    )


# ============================================================
# 15. LETTURA DATI
# ============================================================

with st.spinner(
    f"Caricamento risultati di {citta}..."
):

    poi = carica_gpkg(
        str(
            cfg[
                "file_poi"
            ]
        )
    )


    griglia = carica_gpkg(
        str(
            cfg[
                "file_griglia"
            ]
        )
    )


    lisa = carica_gpkg(
        str(
            cfg[
                "file_lisa"
            ]
        )
    )


    quartieri = carica_gpkg(
        str(
            cfg[
                "file_quartieri"
            ]
        )
    )


# ============================================================
# 16. KPI BASE
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
# 17. KPI SPECIFICI PER CITTÀ
# ============================================================

if citta == "Firenze":

    summary = carica_summary(
        str(
            cfg[
                "file_summary"
            ]
        )
    )


    moran_i = float(
        summary[
            "moran_i"
        ]
    )


    moran_p = float(
        summary[
            "moran_p"
        ]
    )


    n_celle_moran = int(
        float(
            summary[
                "n_celle_moran"
            ]
        )
    )


    poi_quartieri = int(
        float(
            summary[
                "poi_quartieri"
            ]
        )
    )


    poi_fuori_quartieri = int(
        float(
            summary[
                "poi_fuori_quartieri"
            ]
        )
    )


    residenti_quartieri = int(
        float(
            summary[
                "residenti_quartieri"
            ]
        )
    )


    residenti_non_indicato = int(
        float(
            summary[
                "residenti_non_indicato"
            ]
        )
    )


    residenti_comune = int(
        float(
            summary[
                "residenti_comune"
            ]
        )
    )


    anno_popolazione = int(
        float(
            summary[
                "anno_popolazione"
            ]
        )
    )


else:

    moran_i = (
        cfg[
            "moran_i"
        ]
    )


    moran_p = (
        cfg[
            "moran_p"
        ]
    )


    n_celle_moran = (
        cfg[
            "n_celle_moran"
        ]
    )


    poi_quartieri = (
        cfg[
            "poi_quartieri"
        ]
    )


    poi_fuori_quartieri = (
        cfg[
            "poi_fuori_quartieri"
        ]
    )


    residenti_quartieri = (
        cfg[
            "residenti_quartieri"
        ]
    )


    residenti_non_indicato = (
        cfg[
            "residenti_non_indicato"
        ]
    )


    residenti_comune = (
        cfg[
            "residenti_comune"
        ]
    )


    anno_popolazione = (
        cfg[
            "anno_popolazione"
        ]
    )


# ============================================================
# 18. FUNZIONI FORMATO ITALIANO
# ============================================================

def formato_intero(
    valore
):

    return (
        f"{int(valore):,}"
        .replace(
            ",",
            "."
        )
    )


def formato_decimale(
    valore,
    decimali=4,
):

    return (
        f"{float(valore):.{decimali}f}"
        .replace(
            ".",
            ","
        )
    )


# ============================================================
# 19. HEADER AZIENDALE
# ============================================================

st.html(
    f"""
    <div
        style="
            background:
                linear-gradient(
                    110deg,
                    {BLU_NAVY} 0%,
                    {BLU_PETROLIO} 34%,
                    {BLU} 68%,
                    {AZZURRO} 100%
                );

            border-radius:
                14px;

            padding:
                27px 31px;

            margin-bottom:
                26px;

            box-shadow:
                0 4px 14px
                {OMBRA};

            border-bottom:
                5px solid
                {ARANCIONE};
        "
    >

        <div
            style="
                color:
                    white;

                font-size:
                    33px;

                line-height:
                    1.15;

                font-weight:
                    760;

                margin-bottom:
                    9px;
            "
        >
            Diversità Spaziale Urbana – {citta}
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
            indici di diversità e
            autocorrelazione spaziale.
        </div>

    </div>
    """
)


# ============================================================
# 20. QUADRO GENERALE
# ============================================================

st.markdown(
    "## Quadro generale"
)


c1, c2, c3, c4 = (
    st.columns(4)
)


with c1:

    st.metric(
        "POI classificati",
        formato_intero(
            n_poi
        ),
    )


with c2:

    st.metric(
        "Celle della griglia",
        formato_intero(
            n_celle
        ),
    )


with c3:

    st.metric(
        "Quartieri",
        formato_intero(
            n_quartieri
        ),
    )


with c4:

    st.metric(
        "Categorie funzionali",
        formato_intero(
            n_categorie
        ),
    )


st.write("")


c5, c6, c7 = (
    st.columns(3)
)


with c5:

    st.metric(
        "Moran's I globale",
        formato_decimale(
            moran_i,
            4,
        ),
    )


with c6:

    st.metric(
        "p-value permutazionale",
        formato_decimale(
            moran_p,
            4,
        ),
    )


with c7:

    st.metric(
        "Celle Moran/LISA",
        formato_intero(
            n_celle_lisa
        ),
    )


# ============================================================
# 21. MAPPA INTERATTIVA
# ============================================================

st.markdown(
    "## Mappa interattiva"
)


st.caption(
    "Attiva o disattiva i layer della griglia, "
    "dei quartieri e delle otto categorie funzionali."
)


html_mappa = (
    cfg[
        "file_mappa"
    ]
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
# 22. INDICE DI SHANNON
# ============================================================

st.markdown(
    "## Diversità funzionale – Indice di Shannon"
)


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
                10px;

            padding:
                18px 22px;

            margin-bottom:
                22px;

            color:
                {TESTO};

            box-shadow:
                0 2px 7px
                {OMBRA};
        "
    >

        <div
            style="
                font-weight:
                    700;

                margin-bottom:
                    8px;

                color:
                    {
                        BLU
                        if not dark_mode
                        else AZZURRO_CHIARO
                    };
            "
        >
            Indicatore principale
        </div>


        <div
            style="
                line-height:
                    1.6;
            "
        >
            L'indice di Shannon misura l'equilibrio
            nella distribuzione delle otto categorie
            funzionali di POI.

            Valori più elevati indicano una maggiore
            diversità funzionale e una composizione
            maggiormente equilibrata.
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
            cfg[
                "file_shannon"
            ]
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
            cfg[
                "file_quartieri_shannon"
            ]
        ),
        caption=(
            "Indice di Shannon "
            "per quartiere"
        ),
        use_container_width=True,
    )


# ============================================================
# 23. INDICATORI COMPLEMENTARI
# ============================================================

st.markdown(
    "## Indicatori complementari"
)


g1, g2 = (
    st.columns(2)
)


with g1:

    st.image(
        str(
            cfg[
                "file_simpson"
            ]
        ),
        caption=(
            "Distribuzione dell'indice "
            "di Simpson (dominanza)"
        ),
        use_container_width=True,
    )


with g2:

    st.image(
        str(
            cfg[
                "file_ricchezza"
            ]
        ),
        caption=(
            "Distribuzione della "
            "ricchezza categoriale"
        ),
        use_container_width=True,
    )


# ============================================================
# 24. CONFRONTO TERRITORIALE
# ============================================================

st.markdown(
    "## Confronto territoriale"
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


# ------------------------------------------------------------
# Formati italiani
# ------------------------------------------------------------

tabella["POI"] = (
    tabella[
        "n_poi"
    ]
    .astype(int)
    .map(
        formato_intero
    )
)


tabella["Shannon"] = (
    tabella[
        "shannon"
    ]
    .map(
        lambda x:
        formato_decimale(
            x,
            4
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
        formato_decimale(
            x,
            4
        )
    )
)


tabella["Ricchezza"] = (
    tabella[
        "ricchezza"
    ]
    .astype(int)
)


tabella["Residenti"] = (
    tabella[
        "residenti"
    ]
    .astype(int)
    .map(
        formato_intero
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


# ------------------------------------------------------------
# Costruzione HTML
# ------------------------------------------------------------

righe_html = ""


for _, riga in (
    tabella_finale.iterrows()
):

    righe_html += f"""
    <tr>

        <td style="
            padding:12px;
            border-bottom:1px solid {BORDO};
        ">
            {riga["Quartiere"]}
        </td>

        <td style="
            padding:12px;
            border-bottom:1px solid {BORDO};
        ">
            {riga["POI"]}
        </td>

        <td style="
            padding:12px;
            border-bottom:1px solid {BORDO};
        ">
            {riga["Shannon"]}
        </td>

        <td style="
            padding:12px;
            border-bottom:1px solid {BORDO};
        ">
            {riga["Simpson dominance"]}
        </td>

        <td style="
            padding:12px;
            border-bottom:1px solid {BORDO};
        ">
            {riga["Ricchezza"]}
        </td>

        <td style="
            padding:12px;
            border-bottom:1px solid {BORDO};
        ">
            {riga["Residenti"]}
        </td>

        <td style="
            padding:12px;
            border-bottom:1px solid {BORDO};
        ">
            {riga["Densità ab./km²"]}
        </td>

    </tr>
    """


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

            box-shadow:
                0 2px 8px
                {OMBRA};
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
                            {BLU_NAVY};

                        color:
                            white;
                    "
                >

                    <th style="
                        padding:12px;
                        text-align:left;
                    ">
                        Quartiere
                    </th>

                    <th style="
                        padding:12px;
                        text-align:left;
                    ">
                        POI
                    </th>

                    <th style="
                        padding:12px;
                        text-align:left;
                    ">
                        Shannon
                    </th>

                    <th style="
                        padding:12px;
                        text-align:left;
                    ">
                        Simpson dominance
                    </th>

                    <th style="
                        padding:12px;
                        text-align:left;
                    ">
                        Ricchezza
                    </th>

                    <th style="
                        padding:12px;
                        text-align:left;
                    ">
                        Residenti
                    </th>

                    <th style="
                        padding:12px;
                        text-align:left;
                    ">
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


# ============================================================
# 25. DIVERSITÀ E DENSITÀ
# ============================================================

st.image(
    str(
        cfg[
            "file_densita"
        ]
    ),
    caption=(
        "Relazione esplorativa tra "
        "diversità funzionale "
        "e densità abitativa"
    ),
    use_container_width=True,
)


# ============================================================
# 26. AUTOCORRELAZIONE SPAZIALE
# ============================================================

st.markdown(
    "## Autocorrelazione spaziale"
)


a1, a2, a3 = (
    st.columns(3)
)


with a1:

    st.metric(
        "Moran's I",
        formato_decimale(
            moran_i,
            4,
        ),
    )


with a2:

    st.metric(
        "p-value",
        formato_decimale(
            moran_p,
            4,
        ),
    )


with a3:

    st.metric(
        "Celle analizzate",
        formato_intero(
            n_celle_moran
        ),
    )


st.html(
    f"""
    <div
        style="
            background:
                {CARD_SECONDARIA};

            border:
                1px solid
                {BORDO};

            border-left:
                5px solid
                {AZZURRO};

            border-radius:
                10px;

            padding:
                17px 21px;

            margin-top:
                10px;

            margin-bottom:
                24px;

            line-height:
                1.6;

            color:
                {TESTO};
        "
    >

        L'autocorrelazione spaziale viene valutata
        mediante contiguità <strong>Queen</strong>,
        pesi standardizzati per riga e
        <strong>999 permutazioni</strong>.

        L'analisi locale LISA distingue i cluster
        <strong>HH, LL, HL e LH</strong>.

    </div>
    """
)


# ============================================================
# 27. METODOLOGIA
# ============================================================

st.markdown(
    "## Metodologia"
)


# ------------------------------------------------------------
# POI
# ------------------------------------------------------------

with st.expander(
    "Fonti e classificazione POI",
    expanded=True,
):

    st.markdown(
        f"""
Il progetto misura la **diversità funzionale urbana**
nel Comune di **{citta}** attraverso la distribuzione
spaziale dei **Points of Interest (POI)**.

**Fonte POI:** OpenStreetMap tramite snapshot Geofabrik.

Il dataset finale comprende
**{formato_intero(n_poi)} POI**, classificati nelle otto
categorie funzionali previste:

- commercio
- ristorazione
- servizi alla persona
- istruzione
- sanità
- cultura
- trasporti
- servizi pubblici

L'impostazione costituisce un adattamento concettuale
del progetto *spatial_diversity* dell'Università
di Saragozza.
        """
    )


# ------------------------------------------------------------
# GRIGLIA
# ------------------------------------------------------------

with st.expander(
    "Griglia e indicatori"
):

    st.markdown(
        """
L'analisi locale utilizza una **griglia adattiva**
con celle di:

- **250 m**
- **500 m**
- **1.000 m**

La dimensione delle celle viene adattata alla densità
osservata dei POI.

Questa impostazione evita che una dimensione unica
produca un confronto fortemente condizionato dalla
differente concentrazione delle attività tra le aree
centrali e quelle periferiche.

### Indice di Shannon

`H = - Σ pᵢ ln(pᵢ)`

È l'indicatore principale della diversità funzionale.

Valori più elevati indicano una distribuzione più
equilibrata delle categorie.

### Simpson dominance

`D = Σ pᵢ²`

Misura il livello di dominanza delle categorie.

### Ricchezza categoriale

Numero delle categorie funzionali presenti
nell'unità spaziale.
        """
    )


# ------------------------------------------------------------
# AUTOCORRELAZIONE
# ------------------------------------------------------------

with st.expander(
    "Autocorrelazione spaziale"
):

    st.markdown(
        f"""
L'analisi viene effettuata sulle
**{formato_intero(n_celle_moran)} celle con Shannon definito**.

Configurazione utilizzata:

- contiguità Queen
- pesi standardizzati per riga
- 999 permutazioni
- seed = 42
- Moran's I = **{formato_decimale(moran_i, 4)}**
- p-value = **{formato_decimale(moran_p, 4)}**

L'analisi LISA distingue i cluster locali:

- **HH**
- **LL**
- **HL**
- **LH**
        """
    )


# ------------------------------------------------------------
# QUARTIERI
# ------------------------------------------------------------

with st.expander(
    "Scala dei quartieri"
):

    testo_quartieri = f"""
L'analisi territoriale comprende i
**{n_quartieri} quartieri ufficiali di {citta}**.

Gli indicatori vengono ricalcolati direttamente
sulla distribuzione dei POI all'interno del quartiere
e **non** come media degli Shannon delle celle.

Dei **{formato_intero(n_poi)} POI** complessivi:

- **{formato_intero(poi_quartieri)}** ricadono nei quartieri;
- **{formato_intero(poi_fuori_quartieri)}** restano
  nell'analisi a griglia e non vengono assegnati
  artificialmente.
    """


    if citta == "Firenze":

        testo_quartieri += """

### Assegnazione territoriale dei POI

Per Firenze, per l'assegnazione territoriale dei POI
alla scala dei quartieri viene utilizzato il
**representative point** delle geometrie OSM.

Questa procedura evita assegnazioni multiple dei POI
rappresentati da geometrie lineari o poligonali.

### Armonizzazione cartografica

Il confine comunale utilizzato nel progetto e le
geometrie ufficiali dei quartieri derivano da fonti
territoriali differenti e presentano piccoli
disallineamenti geometrici.

Nella **sola visualizzazione della mappa** le geometrie
dei quartieri vengono armonizzate al perimetro comunale:

- le porzioni esterne al Comune vengono ritagliate;
- le porzioni interne non coperte vengono attribuite,
  esclusivamente a fini cartografici, al quartiere con
  cui condividono la maggiore lunghezza di confine.

Questa procedura **non modifica i file territoriali
originali, l'assegnazione dei POI, la popolazione
o gli indicatori statistici**.
        """


    st.markdown(
        testo_quartieri
    )


# ------------------------------------------------------------
# POPOLAZIONE
# ------------------------------------------------------------

with st.expander(
    "Popolazione e densità"
):

    st.markdown(
        f"""
Anno di riferimento: **{anno_popolazione}**

Residenti attribuiti ai quartieri:

**{formato_intero(residenti_quartieri)}**

Residenti non attribuiti territorialmente:

**{formato_intero(residenti_non_indicato)}**

Totale riconciliato del Comune di {citta}:

**{formato_intero(residenti_comune)} residenti**

La densità abitativa è calcolata come:

**residenti / km²**
        """
    )


# ------------------------------------------------------------
# SARAGOZZA
# ------------------------------------------------------------

with st.expander(
    "Riferimento a spatial_diversity"
):

    st.markdown(
        f"""
Il progetto di **{citta}** costituisce un
**adattamento concettuale** del progetto
*spatial_diversity* dell'Università di Saragozza.

Il principio condiviso è la misurazione
dell'eterogeneità funzionale attraverso le quote
relative delle diverse funzioni e l'utilizzo
di indici di diversità.

L'applicazione sviluppata utilizza POI e unità
spaziali a griglia/quartiere, mentre il progetto
originale di Saragozza utilizza principalmente
informazioni catastali e superfici associate
agli usi immobiliari.
        """
    )


# ============================================================
# 28. FOOTER
# ============================================================

st.markdown(
    "---"
)


st.caption(
    f"Diversità Spaziale Urbana – {citta} | "
    "Workflow Python riproducibile"
)
