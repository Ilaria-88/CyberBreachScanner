from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd
import plotly.express as px
import requests
import streamlit as st


@dataclass
class BreachRecord:
    email: str
    breach_name: str
    breach_date: str
    exposed_data: List[str]
    severity: int


def fetch_breach_data_mock(domain: str) -> List[BreachRecord]:
    """
    Simula una query verso un provider di breach intelligence.
    Questa funzione e' pronta per essere sostituita da chiamate reali
    (es. HaveIBeenPwned) mantenendo invariato il resto dell'app.
    """
    if not domain:
        return []

    # Esempio di endpoint reale (commentato):
    # url = f"https://haveibeenpwned.com/api/v3/breaches?domain={domain}"
    # headers = {"hibp-api-key": "YOUR_API_KEY", "user-agent": "CyberBreachScanner"}
    # response = requests.get(url, headers=headers, timeout=15)
    # response.raise_for_status()
    # real_data = response.json()

    # Dati mock dinamici per una simulazione realistica.
    return [
        BreachRecord(
            email=f"admin@{domain}",
            breach_name="CloudDrive Leak",
            breach_date="2021-03-14",
            exposed_data=["Email", "Phone", "Password"],
            severity=9,
        ),
        BreachRecord(
            email=f"finance@{domain}",
            breach_name="PayrollSync Exposure",
            breach_date="2022-11-02",
            exposed_data=["Email", "Salary Info"],
            severity=7,
        ),
        BreachRecord(
            email=f"support@{domain}",
            breach_name="Helpdesk Archive Breach",
            breach_date="2024-01-20",
            exposed_data=["Email", "IP Address"],
            severity=4,
        ),
    ]


def build_breach_dataframe(records: List[BreachRecord]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    rows: List[Dict[str, Any]] = []
    for rec in records:
        rows.append(
            {
                "Email": rec.email,
                "Violazione": rec.breach_name,
                "Data violazione": rec.breach_date,
                "Dati esposti": ", ".join(rec.exposed_data),
                "Gravita": rec.severity,
            }
        )

    df = pd.DataFrame(rows)
    df["Data violazione"] = pd.to_datetime(df["Data violazione"])
    return df.sort_values("Data violazione")


def calculate_risk_score(records: List[BreachRecord]) -> Dict[str, str]:
    if not records:
        return {"score": "0", "level": "Verde", "reason": "Nessuna violazione rilevata."}

    max_severity = max(r.severity for r in records)
    password_exposed = any("Password" in r.exposed_data for r in records)
    total_breaches = len(records)

    base_score = min(100, total_breaches * 15 + max_severity * 5)
    if password_exposed:
        base_score = min(100, base_score + 20)

    if base_score >= 75:
        level = "Rosso"
        reason = "Alto rischio: credenziali o dati critici esposti."
    elif base_score >= 40:
        level = "Giallo"
        reason = "Rischio medio: monitoraggio e azioni di remediation consigliati."
    else:
        level = "Verde"
        reason = "Rischio contenuto: nessuna esposizione critica rilevata."

    return {"score": str(base_score), "level": level, "reason": reason}


def plot_breach_timeline(df: pd.DataFrame) -> None:
    if df.empty:
        st.info("Nessun dato disponibile per il grafico dell'andamento temporale.")
        return

    timeline = (
        df.assign(Anno=df["Data violazione"].dt.year)
        .groupby("Anno", as_index=False)
        .size()
        .rename(columns={"size": "Numero violazioni"})
    )

    fig = px.line(
        timeline,
        x="Anno",
        y="Numero violazioni",
        markers=True,
        title="Andamento delle violazioni nel tempo",
    )
    fig.update_layout(template="plotly_dark", xaxis_title="Anno", yaxis_title="Numero violazioni")
    st.plotly_chart(fig, use_container_width=True)


def is_domain_valid(domain: str) -> bool:
    return "." in domain and " " not in domain and len(domain) >= 4


def show_header() -> None:
    st.set_page_config(
        page_title="CyberBreachScanner",
        page_icon=":shield:",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.title("CyberBreachScanner")
    st.caption("Dashboard di threat intelligence per il monitoraggio di violazioni su domini aziendali")


def main() -> None:
    show_header()

    with st.sidebar:
        st.header("Controlli")
        domain_input = st.text_input("Dominio aziendale", placeholder="esempio.com").strip().lower()
        start_scan = st.button("Avvia Scansione", type="primary")
        st.divider()
        st.markdown(
            """
            **Nota:** al momento e' attiva una sorgente dati mock.
            Il codice e' gia predisposto per integrare provider reali.
            """
        )

    st.subheader("Analisi Violazioni Email")
    st.write("Inserisci un dominio per verificare eventuali esposizioni e il relativo livello di rischio.")

    if not start_scan:
        st.info("Configura il dominio nella barra laterale e premi 'Avvia Scansione'.")
        return

    if not is_domain_valid(domain_input):
        st.error("Dominio non valido. Usa un formato tipo `azienda.com`.")
        return

    with st.spinner("Interrogazione del feed di breach intelligence in corso..."):
        # requests e' importato per favorire l'integrazione immediata di API reali.
        _ = requests.Session()
        records = fetch_breach_data_mock(domain_input)

    risk = calculate_risk_score(records)
    df = build_breach_dataframe(records)

    col1, col2, col3 = st.columns(3)
    col1.metric("Dominio analizzato", domain_input)
    col2.metric("Violazioni rilevate", len(records))
    col3.metric("Risk Score", f"{risk['score']}/100 ({risk['level']})")

    if risk["level"] == "Rosso":
        st.error(risk["reason"])
    elif risk["level"] == "Giallo":
        st.warning(risk["reason"])
    else:
        st.success(risk["reason"])

    st.markdown("### Dettaglio violazioni")
    if df.empty:
        st.success("Nessuna violazione associata al dominio analizzato.")
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("### Trend temporale")
    plot_breach_timeline(df)

    st.caption(f"Ultimo aggiornamento simulato: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
