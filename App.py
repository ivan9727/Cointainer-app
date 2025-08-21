import streamlit as st
import pandas as pd
from datetime import datetime

# --- Inicijalizacija stanja ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Datum", "Luka", "Kontejner", "Status", "Vrijeme dolaska", "Komentar"
    ])

# --- Forma ---
st.title("📦 Evidencija ulaska kontejnera")

with st.form("unos_kontejnera", clear_on_submit=True):
    datum = datetime.today().strftime("%Y-%m-%d")
    luka = st.selectbox("Luka", ["Ålesund", "Stavanger", "Haugesund", "Molde", "Førde", "Trondheim"])
    kontejner = st.text_input("Broj kontejnera")
    status = st.selectbox("Status", ["empty", "B", "T", "lastcast", "module", "7pc", "ADR", "Ikke ADR"])
    vrijeme = st.time_input("Vrijeme dolaska")
    komentar = st.text_area("Komentar")

    submit = st.form_submit_button("Dodaj zapis")

if submit and kontejner.strip() != "":
    novi_red = {
        "Datum": datum,
        "Luka": luka,
        "Kontejner": kontejner,
        "Status": status,
        "Vrijeme dolaska": vrijeme.strftime("%H:%M"),
        "Komentar": komentar,
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([novi_red])],
        ignore_index=True
    )

# --- Prikaz tablice ---
st.subheader("📑 Pregled zapisa")

if not st.session_state.data.empty:
    for i, row in st.session_state.data.iterrows():
        cols = st.columns([2, 2, 2, 2, 2, 3, 1, 1])
        cols[0].write(row["Datum"])
        cols[1].write(row["Luka"])
        cols[2].write(row["Kontejner"])
        cols[3].write(row["Status"])
        cols[4].write(row["Vrijeme dolaska"])
        cols[5].write(row["Komentar"])

        if cols[6].button("✏️ Uredi", key=f"edit_{i}"):
            # Preuzmi vrijednosti u formu
            st.session_state.edit_index = i

        if cols[7].button("🗑️ Obriši", key=f"del_{i}"):
            st.session_state.data = st.session_state.data.drop(i).reset_index(drop=True)
            st.experimental_rerun()

# --- Ako uređujemo red ---
if "edit_index" in st.session_state:
    idx = st.session_state.edit_index
    st.subheader("✏️ Uredi zapis")
    with st.form("uredi_forma"):
        luka = st.selectbox("Luka", ["Ålesund", "Stavanger", "Haugesund", "Molde", "Førde", "Trondheim"], 
                            index=["Ålesund", "Stavanger", "Haugesund", "Molde", "Førde", "Trondheim"].index(st.session_state.data.loc[idx, "Luka"]))
        kontejner = st.text_input("Broj kontejnera", value=st.session_state.data.loc[idx, "Kontejner"])
        status = st.selectbox("Status", ["empty", "B", "T", "lastcast", "module", "7pc", "ADR", "Ikke ADR"],
                              index=["empty", "B", "T", "lastcast", "module", "7pc", "ADR", "Ikke ADR"].index(st.session_state.data.loc[idx, "Status"]))
        vrijeme = st.time_input("Vrijeme dolaska")
        komentar = st.text_area("Komentar", value=st.session_state.data.loc[idx, "Komentar"])
        spremi = st.form_submit_button("💾 Spremi promjene")

    if spremi:
        st.session_state.data.loc[idx, "Luka"] = luka
        st.session_state.data.loc[idx, "Kontejner"] = kontejner
        st.session_state.data.loc[idx, "Status"] = status
        st.session_state.data.loc[idx, "Vrijeme dolaska"] = vrijeme.strftime("%H:%M")
        st.session_state.data.loc[idx, "Komentar"] = komentar
        del st.session_state["edit_index"]
        st.experimental_rerun()
