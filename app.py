# app.py — ROI PX Day (melhorado)
# Visão: UMA LINHA POR CNPJ (sem somar dias entre CNPJs) + Expander de Diagnóstico
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from io import BytesIO
import unicodedata
import re
from typing import Optional, Tuple, List

st.set_page_config(page_title="ROI PX Day — Relatório", page_icon="📊", layout="wide")

# ==============================
# Config / Regex pré-compilados
# ==============================
SUFIXOS_EXCLUIR = [
    r"LTDA", r"S\.?A\.?", r"EIRELI", r"ME", r"MEI",
    r"TRANSPORTES", r"LOGISTICA", r"COMERCIO", r"INDUSTRIA",
    r"TRANSPORTADORA", r"OPERADOR[AE]? LOG[ÍI]STIC[OA]",
    r"OPERA(C|Ç)ÕES LOG[ÍI]STIC[OA]S?"
]
# Junta padrões com OR; usamos IGNORECASE para não precisar duplicar maiúsc/minúsc
SUFIXOS_RE = re.compile(r"\b(?:" + "|".join(SUFIXOS_EXCLUIR) + r")\b", flags=re.IGNORECASE)
# Permitir CNPJ com/sem máscara
CNPJ_RE = re.compile(r"\d{2}\.?\