import streamlit as st
import pandas as pd
import json
import random
from pathlib import Path

# ---------------------------
# Data inladen
# ---------------------------
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
recipes_path = DATA_DIR / "recipes.csv"
filters_path = DATA_DIR / "filters.json"

df = pd.read_csv(recipes_path)

with open(filters_path, "r", encoding="utf-8") as f:
    available_filters = json.load(f)

# ---------------------------
# Sidebar instellingen
# ---------------------------
st.sidebar.header("Instellingen")

selected_filters = st.sidebar.multiselect(
    "Filter opties",
    options=list(available_filters.keys()),
    format_func=lambda x: f"{x} – {available_filters[x]}"
)

leftovers = st.sidebar.text_area(
    "Welke restjes heb je nog in de koelkast?",
    placeholder="bijv: paprika, rijst, kip"
).lower().split(",")

if st.sidebar.button("Genereer weekmenu"):
    # ---------------------------
    # Filterfunctie
    # ---------------------------
    def apply_filters(df, filters):
        if not filters:
            return df
        def is_valid(tags):
            tags = eval(tags) if isinstance(tags, str) else tags
            for f in filters:
                if f == "vegetarian" and "vegetarian" not in tags:
                    return False
                if f == "vegan" and "vegan" not in tags:
                    return False
                if f == "halal" and "halal" not in tags:
                    return False
                if f == "gluten-free" and "contains-gluten" in tags:
                    return False
                if f == "lactose-free" and "contains-dairy" in tags:
                    return False
                if f == "nut-free" and "contains-nuts" in tags:
                    return False
                if f == "egg-free" and "contains-egg" in tags:
                    return False
                if f == "vegetarian" and "vegetarian" not in tags:
                    return False
                if f == "vegan" and "vegan" not in tags:
                    return False
                if f == "not-vegetarian" and "vegetarian" in tags:
                    return False

            return True
        return df[df["tags"].apply(is_valid)]

    # ---------------------------
    # Restjes functie
    # ---------------------------
    def apply_leftovers(df, leftovers):
        if not leftovers or leftovers == [""]:
            return df
        leftovers = [x.strip() for x in leftovers if x.strip()]
        return df[df["ingredients"].str.contains("|".join(leftovers), case=False, na=False)]

    # ---------------------------
    # Data filteren
    # ---------------------------
    filtered = apply_filters(df, selected_filters)
    filtered = apply_leftovers(filtered, leftovers)

    # ---------------------------
    # Weekmenu genereren
    # ---------------------------
    weekmenu = filtered.sample(min(7, len(filtered))) if len(filtered) > 0 else pd.DataFrame()

    st.header("📅 Jouw weekmenu")
    if weekmenu.empty:
        st.warning("Geen recepten gevonden met deze instellingen.")
    else:
        for i, row in weekmenu.iterrows():
            st.subheader(row["name"])
            st.write("Ingrediënten:", row["ingredients"])
            st.write("Tags:", row["tags"])
            st.markdown("---")

        st.success("Weekmenu gegenereerd ✅")
