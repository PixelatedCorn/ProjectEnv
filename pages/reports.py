import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

#A working sample from google Ai, placeholder for now, need that sample report Diaz -PixelatedCorn
st.title("📊 Barangay Analytics & Reports Dashboard")
st.markdown("Real-time demographic breakdowns and reporting metrics for local planning.")

# Read from database
with sqlite3.connect("Residents.db") as conn:
    df = pd.read_sql_query("SELECT * FROM residents WHERE residency_status != 'Archived'", conn)

if df.empty:
    st.info("📂 The active resident registry database is currently empty.")
else:
    # Summary Cards
    total_active = len(df)
    num_seniors = len(df[df["age"] >= 60])
    num_minors = len(df[df["age"] < 18])
    num_voters = len(df[df["age"] >= 18])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("👥 Active Population", f"{total_active} pax")
    m2.metric("👵🏽👴🏽 Senior Citizens", f"{num_seniors} pax")
    m3.metric("👶🏽 Minors (<18)", f"{num_minors} pax")
    m4.metric("🗳️ Potential Voters", f"{num_voters} pax")

    st.markdown("---")

    # Dynamic Population Density Chart
    st.subheader("🏘️ Population Density by Purok / Sitio Zone")
    purok_density = df["purok"].value_counts()
    
    if not purok_density.empty:
        fig_density, ax_density = plt.subplots(figsize=(10, 3.2))
        purok_density.plot(kind="barh", color="#1E88E5", ax=ax_density)
        ax_density.set_xlabel("Number of Registered Active Residents")
        ax_density.set_ylabel("Zone Designation")
        ax_density.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig_density)
    else:
        st.info("No Purok assignments mapped yet.")

    st.markdown("---")

    # Neighborhood Inspection Table Selector
    st.subheader("🔍 Localized Zone Inspection Lookup")
    available_zones = sorted(df["purok"].dropna().unique()) if "purok" in df.columns else []
    
    if available_zones:
        selected_zone = st.selectbox("Select a Purok/Sitio to inspect:", available_zones)
        filtered_zone_df = df[df["purok"] == selected_zone]
        
        st.markdown(f"**Showing {len(filtered_zone_df)} active residents living inside {selected_zone}:**")
        display_cols = ["surname", "first_name", "sex", "age", "occupation", "last_modified_by"]
        clean_view = filtered_zone_df[display_cols].copy()
        clean_view.columns = [c.replace("_", " ").title() for c in clean_view.columns]
        st.dataframe(clean_view, use_container_width=True, hide_index=True)

    st.markdown("---")

    # --- THREE COLUMN GRAPHICAL ELEMENT BREAKDOWNS ---
    st.subheader("📈 Core Community Demographics")
    g1, g2, g3 = st.columns(3)
    
    with g1:
        st.markdown("<p style='text-align: center; font-weight: bold;'>Gender Distribution</p>", unsafe_allow_html=True)
        sex_counts = df["sex"].value_counts()
        if not sex_counts.empty:
            fig, ax = plt.subplots(figsize=(3.5, 3.5))
            ax.pie(sex_counts, labels=sex_counts.index, autopct='%1.1f%%', startangle=90, colors=["#4F8BF9", "#FA5AA6"])
            ax.axis('equal')
            st.pyplot(fig)
        else:
            st.caption("No records available.")

    with g2:
        # --- ADDED NEW CIVIL STATUS CHART BREAKDOWN ---
        st.markdown("<p style='text-align: center; font-weight: bold;'>Civil Status (Household Structures)</p>", unsafe_allow_html=True)
        civil_counts = df["civil_status"].value_counts()
        if not civil_counts.empty:
            fig3, ax3 = plt.subplots(figsize=(3.5, 3.5))
            # Renders a polished donut chart variation layout
            ax3.pie(
                civil_counts, 
                labels=civil_counts.index, 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=["#AB47BC", "#26A69A", "#FF7043", "#26C6DA"],
                wedgeprops=dict(width=0.4, edgecolor='w') # Creates the donut hole cutout styling
            )
            ax3.axis('equal')
            st.pyplot(fig3)
        else:
            st.caption("No records available.")

    with g3:
        st.markdown("<p style='text-align: center; font-weight: bold;'>Top Local Occupations</p>", unsafe_allow_html=True)
        occ_counts = df["occupation"].value_counts().head(5)
        if not occ_counts.empty and occ_counts.index.dropna().any():
            fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
            occ_counts.plot(kind="barh", color="#2E7D32", ax=ax2)
            ax2.invert_yaxis()
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.caption("No records available.")

    st.markdown("---")

    # Data Exportation Option
    st.subheader("📥 Export Records")
    export_df = df.copy()
    export_df.columns = [col.replace("_", " ").title() for col in export_df.columns]
    csv_data = export_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="💾 Download Master Resident Sheet (.csv)",
        data=csv_data,
        file_name="barangay_active_residents_report.csv",
        mime="text/csv",
        use_container_width=True
    )
