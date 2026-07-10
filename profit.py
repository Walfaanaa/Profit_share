import streamlit as st
import pandas as pd
from io import BytesIO

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="EGSA2025 Profit Sharing",
    layout="wide"
)

import streamlit as st

st.set_page_config(page_title="EGSA2025 Profit Sharing", layout="wide")

LOGO_URL = "https://raw.githubusercontent.com/Walfaanaa/Profit_share/main/EGSA.png"

left, center, right = st.columns([3, 1, 3])

with center:
    st.image(LOGO_URL, width=320)

st.markdown(
    """
    <h1 style="text-align:center; color:#6A0DAD;">
        Kabajamtoota Qaalii Miseentoota EGSA2025 Baga Bara Baajataa 2019
        Qooddannaa Gahee Keessaniin Isin Ga'e.
    </h1>
    """,
    unsafe_allow_html=True,
)

# MEMBER DATA
# =====================================
member_ids = [
1001,1002,1003,1004,1005,1006,1007,1008,
1009,1010,1011,1012,1013,1014,1015,1016,
1017,1018,1020,1022,1023,1024,1025,1026
]

contributions = [
76000,151000,151000,74000,52500,151000,
50500,124000,52500,151000,50500,153500,
87000,88000,74000,47000,56600,42000,
44000,56000,46000,199000,42000,44000
]

df = pd.DataFrame({
    "ID": member_ids,
    "Contribution": contributions
})

# =====================================
# STEP 1
# =====================================
st.header("Step 1: Review / Update Contributions")

edited_df = st.data_editor(
    df,
    num_rows="fixed",
    use_container_width=True
)

# =====================================
# STEP 2
# =====================================
st.header("Step 2: Enter Total Profit")

total_profit = st.number_input(
    "Total Profit",
    min_value=0.0,
    value=0.0,
    step=1000.0,
    format="%.2f"
)

if st.button("✅ Calculate Profit Share", use_container_width=True):

    total_contribution = edited_df["Contribution"].sum()

    if total_contribution == 0:
        st.error("Contribution cannot be zero.")
    else:

        result = edited_df.copy()

        # Percentage ownership
        result["Ownership %"] = (
            result["Contribution"] / total_contribution * 100
        ).round(2)

        # Profit allocated
        result["Profit Share"] = (
            result["Contribution"]
            / total_contribution
            * total_profit
        ).round(2)

        # Final amount received
        result["Final Amount"] = (
    result["Contribution"]
    + result["Profit Share"]
).round().astype(int)

        st.session_state["result"] = result
        st.session_state["profit"] = total_profit
        st.session_state["contribution"] = total_contribution
# =====================================
# SHOW RESULT
# =====================================
if "result" in st.session_state:

    result = st.session_state["result"]
    total_profit = st.session_state["profit"]
    total_contribution = st.session_state["contribution"]

    st.divider()

    st.markdown("## 📊 SUMMARY")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div style="
        font-size:70px;
        font-weight:bold;
        color:#003366;
        text-align:center;">
        {total_profit:,.2f}
        </div>

        <h3 style="text-align:center;">
        TOTAL PROFIT
        </h3>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="
        font-size:70px;
        font-weight:bold;
        color:#B22222;
        text-align:center;">
        {total_contribution:,.2f}
        </div>

        <h3 style="text-align:center;">
        TOTAL CONTRIBUTION
        </h3>
        """, unsafe_allow_html=True)

    top_member = result.loc[result["Profit Share"].idxmax(), "ID"]

    with c3:
        st.markdown(f"""
        <div style="
        font-size:70px;
        font-weight:bold;
        color:green;
        text-align:center;">
        {top_member}
        </div>

        <h3 style="text-align:center;">
        TOP WINNER ID
        </h3>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📋 Profit Distribution")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    # =====================================
    # CREATE EXCEL FILE
    # =====================================
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        result.to_excel(
            writer,
            index=False,
            sheet_name="Profit Share"
        )

    excel_data = output.getvalue()

    st.download_button(
        label="📥 Download Excel File",
        data=excel_data,
        file_name="EGSA2025_Profit_Share.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
