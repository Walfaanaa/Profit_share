import streamlit as st
import pandas as pd

st.set_page_config(page_title="EGSA2025 Profit Sharing", layout="wide")
st.title("EGSA2025 Profit Sharing App")

# -------------------------
# Member IDs and Contributions
# -------------------------
member_ids = [
    1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010,
    1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020,
    1021, 1022, 1023
]

contributions = [
    71000.00, 83000.00, 86500.00, 43500.00, 47500.00, 83500.00,
    45500.00, 82000.00, 45500.00, 83000.00, 45500.00, 83000.00,
    82000.00, 83000.00, 43000.00, 30000.00, 42000.00, 0.00,
    15000.00, 1000.00, 1000.00, 1000.00, 41000.00
]



# Create DataFrame
df = pd.DataFrame({
    "ID": member_ids,
    "Contribution": contributions
})

st.header("Step 1: Review / Update Contributions")
edited_df = st.data_editor(df, num_rows="fixed")  # Users can edit contributions

# -------------------------
# Input: Total Profit
# -------------------------
st.header("Step 2: Enter Total Profit")
total_profit = st.number_input("Total Profit to Share", min_value=0.0, value=0.0, step=1000.0)

# -------------------------
# Calculate Profit Share
# -------------------------
if st.button("Calculate Profit Share"):
    total_contribution = edited_df["Contribution"].sum()
    
    if total_contribution > 0:
        # Calculate proportional profit
        edited_df["Profit_Share"] = edited_df["Contribution"] / total_contribution * total_profit
        st.success("Profit Share Calculated Successfully!")
        st.dataframe(edited_df)

        # -------------------------
        # Export to CSV (no openpyxl needed)
        # -------------------------
        csv_data = edited_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download Profit Share as CSV",
            data=csv_data,
            file_name="EGSA2025_Profit_Share.csv",
            mime="text/csv"
        )
    else:
        st.error("Total contribution cannot be zero!")



