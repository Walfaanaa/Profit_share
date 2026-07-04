import streamlit as st
import pandas as pd

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="EGSA2025 Profit Sharing", layout="wide")

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 22px;
}
</style>
""", unsafe_allow_html=True)

st.title("EGSA2025 Profit Sharing App")

# -------------------------
# MEMBER DATA
# -------------------------
member_ids = [1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,
              1013,1014,1015,1016,1017,1018,1020,1022,1023,1024,1025,1026]

contributions = [76000,151000,151000,74000,52500,151000,50500,124000,52500,151000,
                 50500,153500,87000,88000,74000,47000,56600,42000,44000,56000,
                 46000,199000,42000,44000]

df = pd.DataFrame({
    "ID": member_ids,
    "Contribution": contributions
})

# -------------------------
# EDIT DATA
# -------------------------
st.header("Step 1: Review / Update Contributions")
edited_df = st.data_editor(df, num_rows="fixed")

# -------------------------
# TOTAL PROFIT INPUT
# -------------------------
st.header("Step 2: Enter Total Profit")
total_profit = st.number_input(
    "Total Profit to Share",
    min_value=0.0,
    value=0.0,
    step=1000.0
)

# -------------------------
# CALCULATION
# -------------------------
if st.button("Calculate Profit Share"):

    total_contribution = edited_df["Contribution"].sum()

    if total_contribution > 0:

        edited_df["Profit_Share"] = (
            edited_df["Contribution"] / total_contribution * total_profit
        )

        # -------------------------
        # BIG SUMMARY DISPLAY (TV MODE)
        # -------------------------
        st.markdown("## 📊 SUMMARY (TV DISPLAY)")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="font-size:70px;font-weight:bold;color:#003366;text-align:center;">
                {total_profit:,.0f}
            </div>
            <div style="text-align:center;">TOTAL PROFIT</div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="font-size:70px;font-weight:bold;color:#B22222;text-align:center;">
                {total_contribution:,.0f}
            </div>
            <div style="text-align:center;">TOTAL CONTRIBUTION</div>
            """, unsafe_allow_html=True)

        with col3:
            top_winner = edited_df.loc[edited_df["Profit_Share"].idxmax(), "ID"]

            st.markdown(f"""
            <div style="font-size:70px;font-weight:bold;color:#228B22;text-align:center;">
                {top_winner}
            </div>
            <div style="text-align:center;">TOP WINNER ID</div>
            """, unsafe_allow_html=True)

        # -------------------------
        # FULL TABLE
        # -------------------------
        st.subheader("📋 Full Profit Distribution Table")
        st.dataframe(edited_df, use_container_width=True)

        # -------------------------
        # DOWNLOAD CSV
        # -------------------------
        csv_data = edited_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download Profit Share CSV",
            data=csv_data,
            file_name="EGSA2025_Profit_Share.csv",
            mime="text/csv"
        )

    else:
        st.error("Total contribution cannot be zero!")
