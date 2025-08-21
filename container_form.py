import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

# Page configuration
st.set_page_config(
    page_title="Container Entry Form",
    page_icon="📦",
    layout="wide"
)

# Initialize session state for data storage
if "container_data" not in st.session_state:
    st.session_state.container_data = pd.DataFrame(columns=[
        "Date", "Port", "Container Number", "Status", "Arrival Time", "Comment"
    ])

# Custom CSS for minimalistic design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 300;
        color: #1f1f1f;
        margin-bottom: 2rem;
        text-align: center;
    }
    .form-container {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border: 1px solid #e9ecef;
    }
    .table-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    .stButton > button {
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .delete-btn {
        background-color: #dc3545 !important;
    }
    .delete-btn:hover {
        background-color: #c82333 !important;
    }
    .edit-btn {
        background-color: #28a745 !important;
    }
    .edit-btn:hover {
        background-color: #218838 !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">📦 Container Entry Form</h1>', unsafe_allow_html=True)

# Form Section
with st.container():
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("📝 Add New Container Entry")
    
    with st.form("container_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Date field (automatically populated with today's date)
            current_date = date.today()
            date_input = st.date_input(
                "Date",
                value=current_date,
                format="YYYY-MM-DD"
            )
            
            # Port dropdown
            port = st.selectbox(
                "Port",
                options=["Ålesund", "Stavanger", "Haugesund", "Molde", "Førde", "Trondheim"],
                index=0
            )
            
            # Container Number
            container_number = st.text_input(
                "Container Number",
                placeholder="Enter container number"
            )
        
        with col2:
            # Status dropdown
            status = st.selectbox(
                "Status",
                options=["empty", "B", "T", "lastcast", "module", "7pc", "ADR", "Ikke ADR"],
                index=0
            )
            
            # Arrival Time
            arrival_time = st.time_input(
                "Arrival Time",
                value=datetime.now().time()
            )
            
            # Comment field
            comment = st.text_area(
                "Comment",
                placeholder="Enter any additional comments",
                height=100
            )
        
        # Submit button
        submit_button = st.form_submit_button(
            "➕ Add Entry",
            use_container_width=True
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

# Handle form submission
if submit_button and container_number.strip():
    new_entry = {
        "Date": date_input.strftime("%Y-%m-%d"),
        "Port": port,
        "Container Number": container_number.strip(),
        "Status": status,
        "Arrival Time": arrival_time.strftime("%H:%M"),
        "Comment": comment
    }
    
    # Add to session state
    st.session_state.container_data = pd.concat(
        [st.session_state.container_data, pd.DataFrame([new_entry])],
        ignore_index=True
    )
    
    st.success("✅ Container entry added successfully!")
    time.sleep(1)
    st.rerun()

# Data Table Section
st.markdown('<div class="table-container">', unsafe_allow_html=True)
st.subheader("📊 Container Entries")

if not st.session_state.container_data.empty:
    # Display data in a clean table format
    for index, row in st.session_state.container_data.iterrows():
        with st.container():
            st.markdown("---")
            cols = st.columns([2, 2, 2, 2, 2, 3, 1, 1])
            
            # Data columns
            cols[0].markdown(f"**{row['Date']}**")
            cols[1].markdown(f"**{row['Port']}**")
            cols[2].markdown(f"**{row['Container Number']}**")
            cols[3].markdown(f"**{row['Status']}**")
            cols[4].markdown(f"**{row['Arrival Time']}**")
            cols[5].markdown(f"*{row['Comment']}*")
            
            # Action buttons
            if cols[6].button("✏️ Edit", key=f"edit_{index}", use_container_width=True):
                st.session_state.edit_index = index
                st.session_state.edit_mode = True
            
            if cols[7].button("🗑️ Delete", key=f"delete_{index}", use_container_width=True):
                st.session_state.container_data = st.session_state.container_data.drop(index).reset_index(drop=True)
                st.success("✅ Entry deleted successfully!")
                time.sleep(1)
                st.rerun()
else:
    st.info("📋 No container entries yet. Add your first entry using the form above.")

st.markdown('</div>', unsafe_allow_html=True)

# Edit Mode Section
if "edit_mode" in st.session_state and st.session_state.edit_mode:
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    st.subheader("✏️ Edit Container Entry")
    
    edit_index = st.session_state.edit_index
    current_row = st.session_state.container_data.iloc[edit_index]
    
    with st.form("edit_container_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            edit_date = st.date_input(
                "Date",
                value=datetime.strptime(current_row['Date'], "%Y-%m-%d").date(),
                format="YYYY-MM-DD"
            )
            
            edit_port = st.selectbox(
                "Port",
                options=["Ålesund", "Stavanger", "Haugesund", "Molde", "Førde", "Trondheim"],
                index=["Ålesund", "Stavanger", "Haugesund", "Molde", "Førde", "Trondheim"].index(current_row['Port'])
            )
            
            edit_container = st.text_input(
                "Container Number",
                value=current_row['Container Number']
            )
        
        with col2:
            edit_status = st.selectbox(
                "Status",
                options=["empty", "B", "T", "lastcast", "module", "7pc", "ADR", "Ikke ADR"],
                index=["empty", "B", "T", "lastcast", "module", "7pc", "ADR", "Ikke ADR"].index(current_row['Status'])
            )
            
            edit_time = st.time_input(
                "Arrival Time",
                value=datetime.strptime(current_row['Arrival Time'], "%H:%M").time()
            )
            
            edit_comment = st.text_area(
                "Comment",
                value=current_row['Comment'],
                height=100
            )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            save_button = st.form_submit_button("💾 Save Changes", use_container_width=True)
        
        with col2:
            cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)
    
    # Handle edit form submission
    if save_button and edit_container.strip():
        st.session_state.container_data.loc[edit_index, "Date"] = edit_date.strftime("%Y-%m-%d")
        st.session_state.container_data.loc[edit_index, "Port"] = edit_port
        st.session_state.container_data.loc[edit_index, "Container Number"] = edit_container.strip()
        st.session_state.container_data.loc[edit_index, "Status"] = edit_status
        st.session_state.container_data.loc[edit_index, "Arrival Time"] = edit_time.strftime("%H:%M")
        st.session_state.container_data.loc[edit_index, "Comment"] = edit_comment
        
        st.success("✅ Entry updated successfully!")
        del st.session_state["edit_mode"]
        del st.session_state["edit_index"]
        time.sleep(1)
        st.rerun()
    
    if cancel_button:
        del st.session_state["edit_mode"]
        del st.session_state["edit_index"]
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6c757d; padding: 1rem;'>"
    "Container Entry Management System | Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)