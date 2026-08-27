# ============================================================
# DIVERSITÀ SPAZIALE URBANA
# BOLOGNA + FIRENZE
#
# Dashboard Streamlit multi-città
#
# STILE:
# coerente con la dashboard
# "Accessibilità della popolazione agli
# equipaggiamenti culturali"
#
# VERSIONE COMPLETA
# ============================================================

from pathlib import Path
from io import BytesIO
import base64

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
#
# Sidebar aperta di default.
#
# La sidebar verrà inoltre resa strutturalmente
# permanente tramite CSS.
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

ROOT = (
    Path(__file__)
    .resolve()
    .parent
)


# ============================================================
# 3. CONFIGURAZIONE CITTÀ
# ============================================================
#
# Un unico motore dashboard.
#
# Bologna e Firenze differiscono solo per:
# - file;
# - risultati specifici;
# - anno popolazione;
# - note metodologiche specifiche.
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
    },
}


# ============================================================
# 4. COLORI DASHBOARD
# ============================================================
#
# Palette ripresa dall'impostazione visiva della dashboard
# "Accessibilità della popolazione agli
# equipaggiamenti culturali".
#
# SIDEBAR:
# blu scuro -> petrolio -> azzurro
#
# MAIN:
# azzurro chiarissimo -> azzurro
#
# CARD:
# bianco
#
# TESTO:
# blu navy
# ============================================================

NAVY_TESTO = "#0B2942"

SIDEBAR_TOP = "#133D55"

SIDEBAR_MID = "#155974"

SIDEBAR_BOTTOM = "#269ABA"

MAIN_LEFT = "#C6F0F6"

MAIN_MID = "#9EE4F1"

MAIN_RIGHT = "#5EC8E6"

CARD = "#FDFEFF"

BIANCO = "#FFFFFF"

TESTO_SECONDARIO = "#466777"

BORDO_CHIARO = "#D5E7EC"

AZZURRO_ACCENTO = "#52C5E4"

AZZURRO_SELEZIONE = "#35AFD1"

ROSSO_SELEZIONE = "#FF5A64"

OMBRA = "rgba(11, 41, 66, 0.10)"


# ============================================================
# 5. LOGO SBL
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
# 6. PREPARAZIONE LOGO HD
# ============================================================
#
# Il logo:
#
# - non viene sovrascritto;
# - viene ritagliato automaticamente;
# - viene portato ad alta risoluzione;
# - viene ricampionato con LANCZOS;
# - riceve una leggera correzione di contrasto;
# - riceve una Unsharp Mask controllata.
#
# L'immagine finale rimane in memoria.
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
        # Fondo bianco per identificazione bbox
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


        fondo = Image.new(
            "RGB",
            rgb.size,
            "white",
        )


        differenza = (
            ImageChops.difference(
                rgb,
                fondo,
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


        # ----------------------------------------------------
        # Crop automatico
        # ----------------------------------------------------

        if bbox is not None:

            sx, alto, dx, basso = bbox


            larghezza_logo = (
                dx - sx
            )

            altezza_logo = (
                basso - alto
            )


            padding_x = max(
                6,
                int(
                    larghezza_logo
                    * 0.06
                ),
            )


            padding_y = max(
                6,
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
        # Alta risoluzione
        # ----------------------------------------------------

        larghezza_target = max(
            1800,
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
        # Contrasto controllato
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
                radius=1.3,
                percent=140,
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
                1.08
            )
        )


        # ----------------------------------------------------
        # PNG in memoria
        # ----------------------------------------------------

        buffer = BytesIO()


        img.save(
            buffer,
            format="PNG",
            optimize=False,
        )


        return (
            buffer.getvalue()
        )


# ============================================================
# 7. LOGO HD
# ============================================================

logo_hd = None

logo_base64 = None


if FILE_LOGO is not None:

    logo_hd = prepara_logo_hd(
        str(
            FILE_LOGO
        )
    )


    logo_base64 = (
        base64
        .b64encode(
            logo_hd
        )
        .decode(
            "utf-8"
        )
    )


# ============================================================
# 8. CSS COMPLETO
# ============================================================
#
# PUNTI IMPORTANTI:
#
# 1. nessuna banda superiore Streamlit;
# 2. sidebar sempre visibile;
# 3. sidebar non collassabile;
# 4. nessuno spazio vuoto superiore;
# 5. colori uguali all'impostazione Accessibilità;
# 6. main content su gradiente azzurro;
# 7. card bianche.
# ============================================================

st.html(
    f"""
    <style>

    /* ======================================================
       RESET BASE
       ====================================================== */

    html,
    body {{

        margin:
            0 !important;

        padding:
            0 !important;

        background:
            {MAIN_LEFT} !important;

    }}


    /* ======================================================
       ELIMINAZIONE BANDA SUPERIORE STREAMLIT
       ====================================================== */

    header[data-testid="stHeader"] {{

        height:
            0 !important;

        min-height:
            0 !important;

        max-height:
            0 !important;

        background:
            transparent !important;

        border:
            none !important;

    }}


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

    }}


    /* ======================================================
       SIDEBAR SEMPRE APERTA
       ====================================================== */

    section[data-testid="stSidebar"] {{

        display:
            block !important;

        visibility:
            visible !important;

        transform:
            none !important;

        left:
            0 !important;

        margin-left:
            0 !important;

        min-width:
            355px !important;

        width:
            355px !important;

        max-width:
            355px !important;

        background:
            linear-gradient(
                180deg,
                {SIDEBAR_TOP} 0%,
                {SIDEBAR_MID} 48%,
                {SIDEBAR_BOTTOM} 100%
            )
            !important;

        border-right:
            1px solid
            rgba(
                255,
                255,
                255,
                0.16
            )
            !important;

        box-shadow:
            5px 0 18px
            rgba(
                11,
                41,
                66,
                0.12
            );

    }}


    section[data-testid="stSidebar"] > div {{

        width:
            355px !important;

        min-width:
            355px !important;

        max-width:
            355px !important;

    }}


    [data-testid="stSidebarContent"],
    [data-testid="stSidebarUserContent"] {{

        background:
            transparent !important;

    }}


    [data-testid="stSidebarUserContent"] {{

        padding-top:
            2.1rem !important;

        padding-left:
            1.4rem !important;

        padding-right:
            1.4rem !important;

    }}


    /* ======================================================
       DISABILITAZIONE COLLASSO SIDEBAR
       ====================================================== */

    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {{

        display:
            none !important;

        visibility:
            hidden !important;

    }}


    /* ======================================================
       TESTI SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {{

        color:
            white !important;

    }}


    section[data-testid="stSidebar"]
    [data-testid="stCaptionContainer"] {{

        color:
            rgba(
                255,
                255,
                255,
                0.78
            )
            !important;

    }}


    section[data-testid="stSidebar"] hr {{

        border:
            none !important;

        border-top:
            1px solid
            rgba(
                255,
                255,
                255,
                0.25
            )
            !important;

        margin-top:
            1.4rem !important;

        margin-bottom:
            1.4rem !important;

    }}


    /* ======================================================
       RADIO CITTÀ
       ====================================================== */

    section[data-testid="stSidebar"]
    [data-testid="stRadio"] > div {{

        gap:
            0.55rem !important;

    }}


    section[data-testid="stSidebar"]
    [data-testid="stRadio"] label {{

        width:
            100% !important;

        min-height:
            52px !important;

        display:
            flex !important;

        align-items:
            center !important;

        padding:
            0.7rem
            0.9rem !important;

        border-radius:
            11px !important;

        border:
            1px solid
            rgba(
                255,
                255,
                255,
                0.20
            )
            !important;

        background:
            rgba(
                255,
                255,
                255,
                0.06
            )
            !important;

        transition:
            0.15s ease !important;

    }}


    section[data-testid="stSidebar"]
    [data-testid="stRadio"] label:hover {{

        background:
            rgba(
                255,
                255,
                255,
                0.12
            )
            !important;

        border-color:
            rgba(
                255,
                255,
                255,
                0.38
            )
            !important;

    }}


    section[data-testid="stSidebar"]
    [data-testid="stRadio"]
    label:has(input:checked) {{

        background:
            rgba(
                80,
                198,
                228,
                0.24
            )
            !important;

        border:
            1px solid
            rgba(
                126,
                220,
                240,
                0.70
            )
            !important;

    }}


    section[data-testid="stSidebar"]
    input[type="radio"] {{

        accent-color:
            {ROSSO_SELEZIONE} !important;

    }}


    /* ======================================================
       APP / MAIN
       ====================================================== */

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{

        background:
            linear-gradient(
                100deg,
                {MAIN_LEFT} 0%,
                {MAIN_MID} 45%,
                {MAIN_RIGHT} 100%
            )
            !important;

        color:
            {NAVY_TESTO} !important;

    }}


    [data-testid="stMainBlockContainer"] {{

        background:
            transparent !important;

    }}


    /* ======================================================
       CONTENUTO PRINCIPALE
       ====================================================== */

    .block-container {{

        max-width:
            1540px !important;

        padding-top:
            1.55rem !important;

        padding-bottom:
            3.5rem !important;

        padding-left:
            3rem !important;

        padding-right:
            3rem !important;

    }}


    /* ======================================================
       TESTI MAIN
       ====================================================== */

    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4,
    [data-testid="stMain"] h5,
    [data-testid="stMain"] h6 {{

        color:
            {NAVY_TESTO} !important;

    }}


    [data-testid="stMain"] p,
    [data-testid="stMain"] li,
    [data-testid="stMain"] label,
    [data-testid="stMarkdownContainer"] {{

        color:
            {NAVY_TESTO} !important;

    }}


    [data-testid="stMain"]
    [data-testid="stCaptionContainer"] {{

        color:
            {TESTO_SECONDARIO} !important;

    }}


    /* ======================================================
       KPI
       ====================================================== */

    [data-testid="stMetric"] {{

        background:
            {CARD} !important;

        border:
            1px solid
            rgba(
                255,
                255,
                255,
                0.60
            )
            !important;

        border-radius:
            16px !important;

        padding:
            1.15rem
            1.35rem !important;

        min-height:
            128px !important;

        box-shadow:
            0 5px 14px
            {OMBRA}
            !important;

    }}


    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {{

        color:
            {NAVY_TESTO} !important;

        font-weight:
            500 !important;

        font-size:
            0.98rem !important;

    }}


    [data-testid="stMetricValue"] {{

        color:
            {NAVY_TESTO} !important;

        font-size:
            2.25rem !important;

        line-height:
            1.1 !important;

        font-weight:
            760 !important;

    }}


    /* ======================================================
       EXPANDER
       ====================================================== */

    [data-testid="stExpander"],
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {{

        background:
            rgba(
                253,
                254,
                255,
                0.96
            )
            !important;

        color:
            {NAVY_TESTO}
            !important;

    }}


    [data-testid="stExpander"] {{

        border:
            1px solid
            rgba(
                255,
                255,
                255,
                0.70
            )
            !important;

        border-radius:
            13px !important;

        box-shadow:
            0 3px 10px
            rgba(
                11,
                41,
                66,
                0.06
            );

    }}


    [data-testid="stExpander"] summary *,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    [data-testid="stExpander"] strong {{

        color:
            {NAVY_TESTO}
            !important;

    }}


    /* ======================================================
       IMMAGINI
       ====================================================== */

    [data-testid="stImage"] img {{

        border-radius:
            10px !important;

    }}


    /* ======================================================
       IFRAME MAPPA
       ====================================================== */

    iframe {{

        border-radius:
            12px !important;

        background:
            white !important;

        box-shadow:
            0 5px 15px
            rgba(
                11,
                41,
                66,
                0.10
            )
            !important;

    }}


    /* ======================================================
       MOBILE
       ====================================================== */

    @media (
        max-width: 900px
    ) {{

        section[data-testid="stSidebar"] {{

            min-width:
                285px !important;

            width:
                285px !important;

            max-width:
                285px !important;

        }}


        section[data-testid="stSidebar"] > div {{

            min-width:
                285px !important;

            width:
                285px !important;

            max-width:
                285px !important;

        }}


        .block-container {{

            padding-left:
                1.2rem !important;

            padding-right:
                1.2rem !important;

        }}

    }}

    </style>
    """
)


# ============================================================
# 9. HEADER SIDEBAR
# ============================================================

if logo_hd is not None:

    st.sidebar.image(
        logo_hd,
        width=125,
        link=URL_SBL,
    )

else:

    st.sidebar.link_button(
        "SBL Consultancy",
        URL_SBL,
    )


st.sidebar.markdown(
    """
### Diversità spaziale

Popolazione, funzioni urbane  
e mixité territoriale
"""
)


st.sidebar.markdown(
    "---"
)


# ============================================================
# 10. SELEZIONE TERRITORIALE
# ============================================================

st.sidebar.markdown(
    "### Selezione territoriale"
)


citta = st.sidebar.radio(
    "Comune",
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
# 11. INFORMAZIONI SIDEBAR
# ============================================================

st.sidebar.markdown(
    "---"
)


st.sidebar.markdown(
    "### Area selezionata"
)


st.sidebar.markdown(
    f"**Comune di {citta}**"
)


st.sidebar.caption(
    cfg[
        "fonte"
    ]
)


# ============================================================
# 12. CONTROLLO FILE
# ============================================================

FILE_NECESSARI = [
    cfg[
        "file_poi"
    ],
    cfg[
        "file_griglia"
    ],
    cfg[
        "file_lisa"
    ],
    cfg[
        "file_quartieri"
    ],
    cfg[
        "file_mappa"
    ],
    cfg[
        "file_shannon"
    ],
    cfg[
        "file_simpson"
    ],
    cfg[
        "file_ricchezza"
    ],
    cfg[
        "file_quartieri_shannon"
    ],
    cfg[
        "file_densita"
    ],
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
# 13. FUNZIONI LETTURA DATI
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
# 14. LETTURA DATI
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
# 15. KPI BASE
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
# 16. KPI SPECIFICI
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
# 17. FORMATI ITALIANI
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


def formato_densita(
    valore
):

    return (
        f"{float(valore):,.1f}"
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


# ============================================================
# 18. HEADER PRINCIPALE
# ============================================================
#
# Nessun rettangolo scuro.
#
# Come nella dashboard Accessibilità:
# - logo a sinistra;
# - titolo navy;
# - sottotitolo;
# - tutto direttamente sullo sfondo azzurro.
# ============================================================

if logo_base64 is not None:

    html_logo_header = f"""
        <a
            href="{URL_SBL}"
            target="_blank"
            style="
                display:flex;
                align-items:center;
                justify-content:center;
                background:white;
                width:90px;
                height:90px;
                border-radius:2px;
                flex:0 0 90px;
                overflow:hidden;
            "
        >

            <img
                src="data:image/png;base64,{logo_base64}"
                style="
                    width:82px;
                    height:auto;
                    display:block;
                "
            >

        </a>
    """

else:

    html_logo_header = ""


st.html(
    f"""
    <div
        style="
            display:flex;
            align-items:flex-start;
            gap:18px;
            margin-bottom:34px;
            padding-top:8px;
        "
    >

        {html_logo_header}


        <div
            style="
                flex:1;
                padding-top:0;
            "
        >

            <div
                style="
                    color:{NAVY_TESTO};
                    font-size:42px;
                    line-height:1.12;
                    font-weight:800;
                    letter-spacing:-0.7px;
                    margin-bottom:14px;
                "
            >
                Diversità Spaziale Urbana – {citta}
            </div>


            <div
                style="
                    color:{NAVY_TESTO};
                    font-size:17px;
                    line-height:1.65;
                    max-width:1120px;
                "
            >
                Analisi della mixité funzionale urbana
                attraverso Points of Interest,
                indici di diversità e
                autocorrelazione spaziale.
            </div>

        </div>

    </div>
    """
)


# ============================================================
# 19. QUADRO GENERALE
# ============================================================

st.markdown(
    f"# {citta}"
)


st.markdown(
    "## KPI principali"
)


# ============================================================
# 20. KPI - PRIMA RIGA
# ============================================================

c1, c2, c3, c4 = (
    st.columns(
        4,
        gap="medium",
    )
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


# ============================================================
# 21. KPI - SECONDA RIGA
# ============================================================

c5, c6, c7 = (
    st.columns(
        3,
        gap="medium",
    )
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


st.write("")


# ============================================================
# 22. MAPPA INTERATTIVA
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
# 23. SHANNON
# ============================================================

st.markdown(
    "## Diversità funzionale – Indice di Shannon"
)


st.html(
    f"""
    <div
        style="
            background:
                rgba(
                    253,
                    254,
                    255,
                    0.96
                );

            border-radius:
                14px;

            padding:
                20px 23px;

            margin-bottom:
                22px;

            box-shadow:
                0 4px 12px
                {OMBRA};

            color:
                {NAVY_TESTO};
        "
    >

        <div
            style="
                font-weight:
                    750;

                font-size:
                    17px;

                margin-bottom:
                    8px;
            "
        >
            Indicatore principale
        </div>


        <div
            style="
                line-height:
                    1.65;

                font-size:
                    15px;
            "
        >

            L'indice di Shannon misura
            l'equilibrio nella distribuzione
            delle otto categorie funzionali
            di POI.

            Valori più elevati indicano
            una maggiore diversità funzionale
            e una composizione maggiormente
            equilibrata.

        </div>

    </div>
    """
)


# ============================================================
# 24. GRAFICI SHANNON
# ============================================================

g1, g2 = (
    st.columns(
        2,
        gap="medium",
    )
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
# 25. INDICATORI COMPLEMENTARI
# ============================================================

st.markdown(
    "## Indicatori complementari"
)


g1, g2 = (
    st.columns(
        2,
        gap="medium",
    )
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
# 26. CONFRONTO TERRITORIALE
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


tabella[
    "POI"
] = (
    tabella[
        "n_poi"
    ]
    .astype(int)
    .map(
        formato_intero
    )
)


tabella[
    "Shannon"
] = (
    tabella[
        "shannon"
    ]
    .map(
        lambda x:
        formato_decimale(
            x,
            4,
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
            4,
        )
    )
)


tabella[
    "Ricchezza"
] = (
    tabella[
        "ricchezza"
    ]
    .astype(int)
)


tabella[
    "Residenti"
] = (
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
        formato_densita
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


# ============================================================
# 27. TABELLA HTML
# ============================================================

righe_html = ""


for _, riga in (
    tabella_finale.iterrows()
):

    righe_html += f"""
    <tr>

        <td>
            {riga["Quartiere"]}
        </td>

        <td>
            {riga["POI"]}
        </td>

        <td>
            {riga["Shannon"]}
        </td>

        <td>
            {riga["Simpson dominance"]}
        </td>

        <td>
            {riga["Ricchezza"]}
        </td>

        <td>
            {riga["Residenti"]}
        </td>

        <td>
            {riga["Densità ab./km²"]}
        </td>

    </tr>
    """


st.html(
    f"""
    <div
        style="
            overflow-x:auto;

            background:
                {CARD};

            border-radius:
                15px;

            box-shadow:
                0 5px 14px
                {OMBRA};

            margin-bottom:
                25px;
        "
    >

        <table
            style="
                width:100%;
                border-collapse:collapse;
                color:{NAVY_TESTO};
                font-size:14px;
            "
        >

            <thead>

                <tr
                    style="
                        background:
                            {SIDEBAR_TOP};

                        color:
                            white;
                    "
                >

                    <th>
                        Quartiere
                    </th>

                    <th>
                        POI
                    </th>

                    <th>
                        Shannon
                    </th>

                    <th>
                        Simpson dominance
                    </th>

                    <th>
                        Ricchezza
                    </th>

                    <th>
                        Residenti
                    </th>

                    <th>
                        Densità ab./km²
                    </th>

                </tr>

            </thead>


            <tbody>

                {righe_html}

            </tbody>

        </table>

    </div>


    <style>

        table th {{

            padding:
                13px 14px;

            text-align:
                left;

            font-weight:
                650;

        }}


        table td {{

            padding:
                12px 14px;

            border-bottom:
                1px solid
                {BORDO_CHIARO};

        }}


        table tbody tr:last-child td {{

            border-bottom:
                none;

        }}

    </style>
    """
)


# ============================================================
# 28. SHANNON E DENSITÀ
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
# 29. AUTOCORRELAZIONE
# ============================================================

st.markdown(
    "## Autocorrelazione spaziale"
)


a1, a2, a3 = (
    st.columns(
        3,
        gap="medium",
    )
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
                rgba(
                    253,
                    254,
                    255,
                    0.94
                );

            border-radius:
                14px;

            padding:
                19px 22px;

            margin-top:
                12px;

            margin-bottom:
                28px;

            color:
                {NAVY_TESTO};

            line-height:
                1.65;

            box-shadow:
                0 4px 12px
                {OMBRA};
        "
    >

        L'autocorrelazione spaziale viene
        analizzata mediante contiguità
        <strong>Queen</strong>,
        pesi standardizzati per riga e
        <strong>999 permutazioni</strong>.

        L'analisi locale LISA distingue
        i cluster
        <strong>HH, LL, HL e LH</strong>.

    </div>
    """
)


# ============================================================
# 30. METODOLOGIA
# ============================================================

st.markdown(
    "## Metodologia"
)


# ============================================================
# 30A. FONTI E POI
# ============================================================

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
**{formato_intero(n_poi)} POI**, classificati nelle
otto categorie funzionali previste:

- commercio
- ristorazione
- servizi alla persona
- istruzione
- sanità
- cultura
- trasporti
- servizi pubblici

L'impostazione costituisce un adattamento concettuale
del progetto *spatial_diversity*
dell'Università di Saragozza.
        """
    )


# ============================================================
# 30B. GRIGLIA
# ============================================================

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

Questa impostazione permette di limitare le differenze
derivanti dal forte contrasto tra aree urbane ad alta
concentrazione di POI e aree periferiche a minore
densità funzionale.

### Indice di Shannon

`H = - Σ pᵢ ln(pᵢ)`

È l'indicatore principale della diversità funzionale.

Valori più elevati indicano una distribuzione
maggiormente equilibrata delle categorie.

### Simpson dominance

`D = Σ pᵢ²`

Misura il livello di dominanza delle categorie.

### Ricchezza categoriale

Numero delle categorie funzionali presenti
nell'unità spaziale.
        """
    )


# ============================================================
# 30C. AUTOCORRELAZIONE
# ============================================================

with st.expander(
    "Autocorrelazione spaziale"
):

    st.markdown(
        f"""
L'analisi viene effettuata sulle
**{formato_intero(n_celle_moran)} celle
con Shannon definito**.

Configurazione:

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


# ============================================================
# 30D. QUARTIERI
# ============================================================

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

- **{formato_intero(poi_quartieri)}**
  ricadono nei quartieri;
- **{formato_intero(poi_fuori_quartieri)}**
  restano nell'analisi a griglia
  e non vengono assegnati artificialmente.
    """


    if citta == "Firenze":

        testo_quartieri += """

### Assegnazione territoriale dei POI

Per l'assegnazione territoriale dei POI alla scala
dei quartieri viene utilizzato il
**representative point** delle geometrie OSM.

La procedura evita assegnazioni multiple dei POI
rappresentati da geometrie lineari o poligonali.

### Armonizzazione cartografica

Il confine comunale utilizzato nel progetto
e le geometrie ufficiali dei quartieri provengono
da fonti territoriali differenti e presentano
disallineamenti geometrici.

Nella **sola visualizzazione cartografica**
le geometrie dei quartieri vengono armonizzate
al perimetro comunale:

- le porzioni esterne al Comune vengono ritagliate;
- le porzioni interne non coperte vengono attribuite,
  esclusivamente a fini cartografici,
  al quartiere con cui condividono
  la maggiore lunghezza di confine.

Questa procedura **non modifica i file territoriali
originali, l'assegnazione dei POI, la popolazione
o gli indicatori statistici**.
        """


    st.markdown(
        testo_quartieri
    )


# ============================================================
# 30E. POPOLAZIONE
# ============================================================

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


# ============================================================
# 30F. SPATIAL DIVERSITY
# ============================================================

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

L'applicazione sviluppata utilizza POI
e unità spaziali a griglia/quartiere,
mentre il progetto originale di Saragozza
utilizza principalmente informazioni catastali
e superfici associate agli usi immobiliari.
        """
    )


# ============================================================
# 31. FOOTER
# ============================================================

st.markdown(
    "---"
)


st.caption(
    f"Diversità Spaziale Urbana – {citta} | "
    "Workflow Python riproducibile"
)
