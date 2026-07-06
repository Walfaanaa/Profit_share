import streamlit as st
import pandas as pd

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="EGSA2025 Profit Sharing", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size:22px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏆 EGSA2025 Profit Sharing App")

# -------------------------
# MEMBER DATA
# -------------------------
member_ids = [
    1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,
    1011,1012,1013,1014,1015,1016,1017,1018,1020,1022,
    1023,1024,1025,1026
]

contributions = [
    76000,151000,151000,74000,52500,151000,50500,124000,
    52500,151000,50500,153500,87000,88000,74000,47000,
    56600,42000,44000,56000,46000,199000,42000,44000
]

df = pd.DataFrame({
    "ID": member_ids,
    "Contribution": contributions
})

# -------------------------
# EDIT CONTRIBUTIONS
# -------------------------
st.header("Step 1: Review / Update Contributions")

edited_df = st.data_editor(
    df,
    use_container_width=True,
    num_rows="fixed"
)

# -------------------------
# PROFIT INPUT
# -------------------------
st.header("Step 2: Enter Total Profit")

total_profit = st.number_input(
    "Total Profit to Share",
    min_value=0.0,
    value=0.0,
    step=1000.0,
    format="%.2f"
)

# -------------------------
# CALCULATE BUTTON
# -------------------------
if st.button("✅ Calculate Profit Share"):

    total_contribution = edited_df["Contribution"].sum()

    if total_contribution == 0:
        st.error("Total contribution cannot be zero!")
    else:

        result = edited_df.copy()

        result["Profit Share"] = (
            result["Contribution"] /
            total_contribution *
            total_profit
        ).round(2)

        st.session_state["result"] = result
        st.session_state["total_profit"] = total_profit
        st.session_state["total_contribution"] = total_contribution

# -------------------------
# DISPLAY RESULT
# -------------------------
if "result" in st.session_state:

    result = st.session_state["result"]
    total_profit = st.session_state["total_profit"]
    total_contribution = st.session_state["total_contribution"]

    st.divider()

    st.markdown("## 📊 SUMMARY (TV DISPLAY)")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            font-size:70px;
            font-weight:bold;
            color:#003366;
            text-align:center;">
            {total_profit:,.2f}
        </div>
        <h3 style="text-align:center;">TOTAL PROFIT</h3>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            font-size:70px;
            font-weight:bold;
            color:#B22222;
            text-align:center;">
            {total_contribution:,.2f}
        </div>
        <h3 style="text-align:center;">TOTAL CONTRIBUTION</h3>
        """, unsafe_allow_html=True)

    top_winner = result.loc[result["Profit Share"].idxmax(), "ID"]

    with col3:
        st.markdown(f"""
        <div style="
            font-size:70px;
            font-weight:bold;
            color:#228B22;
            text-align:center;">
            {top_winner}
        </div>
        <h3 style="text-align:center;">TOP WINNER ID</h3>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("📋 Profit Distribution Table")

    st.dataframe(
        result,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------
    # DOWNLOAD CSV
    # -------------------------
    csv = result.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Profit Share CSV",
        data=csv,
        file_name="EGSA2025_Profit_Share.csv",
        mime="text/csv",
        use_container_width=True
    )
