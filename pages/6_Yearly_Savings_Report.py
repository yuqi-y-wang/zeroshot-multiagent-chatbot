import streamlit as st
import base64
import os

# Function to display PDF
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="1000" height="700" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Form for user input
    
email = st.text_input("Email")
company = st.selectbox("Company", ["", "Rudin Management Company Inc.", "JPMorgan Chase", "Boston Properties"], index=0, key='company_select')

# Update session state when company changes
if st.session_state.company_select != company:
    st.session_state.company_select = company
    print(f"Company changed to {company}")

st.write("Current company selected:", st.session_state.company_select)
# Conditional Site ID based on company selection
if st.session_state.get('company_select') == "Rudin Management Company Inc.":
    site_id = st.selectbox("Site Name",[
    "345 Park Avenue",
    "355 Lexington Avenue",
    "One Battery Park Plaza",
    "One Whitehall Street",
    "3 Times Square",
    "32 Avenue Of The Americas",
    "40 East 52nd Street",
    "41 Madison Avenue",
    "55 Broad Street",
    "80 Pine Street",
    "415 Madison Avenue",
    "560 Lexington Avenue",
    "641 Lexington Avenue",
    "845 Third Avenue",
    "1675 Broadway",
    "211 East 70th Street",
    "254 East 68th Street",
    "The Greenwich Lane",
    "20 West 86th Street",
    "25 West 81st Street",
    "27 West 86th Street",
    "40 Park Avenue",
    "40 West 86th Street",
    "110 Wall Street",
    "115 West 86th Street",
    "136 East 55th Street",
    "144 West 86th Street",
    "215 East 68th Street",
    "241 Central Park West",
    "295 Central Park West",
    "300 East 57th Street",
    "544 East 86th Street",
    "945 Fifth Avenue",
    "1085 Park Avenue"
], disabled=False)
elif st.session_state.get('company_select') == "JPMorgan Chase":
    site_id = st.selectbox("Site Name", [
    "383 Madison",
    "4 Chase Metrotech Center",
    "575 Washington Blvd",
    "One Christina Center",
    "Three Christina Center",
    "Delaware Technology Center",
    "DTC 1",
    "DTC 2",
    "Newark Corporate Center",
    "NCC 3",
    "NCC 4",
    "NCC 5",
    "Easton Vision",
    "Indianapolis West Corporate Center",
    "625 Freeport Parkway",
    "Wiseman 1",
    "Wiseman 2",
    "Stone Oak (Building A)",
    "Stone Oak (Building B)",
    "Stone Oak (Building C)",
    "Orlando - Building 550",
    "Orlando - Building 600",
    "7301 Baymeadows Way (Main Building)",
    "7255 Baymeadows Way (Horizons)",
    "Chase Tower Chicago",
    "1111 Polaris Parkway",
    "Highland Oaks 1",
    "Highland Oaks 2",
    "Highland Oaks 3",
    "Tempe North Building F",
    "Tempe North Building G",
    "Tempe South (Campus)",
    "Tempe South Building 2104",
    "Tempe South Building 2118",
    "Legacy West Building A",
    "Legacy West Building B",
    "Legacy West Building C",
    "Legacy West Building F",
    "McCoy - Building 370",
    "McCoy - Building 380",
    "237 Park",
    "390 Madison",
    "390 Madison Showcase",
    "Bowen Building"
], disabled=False)
elif st.session_state.get('company_select') == "Boston Properties":
   site_id = st.selectbox("Site Name", [
    "399 Park Avenue",
    "599 Lexington Avenue",
    "601 Lexington Avenue",
    "767 Fifth Avenue",
    "Dock 72",
    "101 Carnegie Center",
    "103 Carnegie Center",
    "104 Carnegie Center",
    "202 Carnegie Center",
    "210 Carnegie Center",
    "212 Carnegie Center",
    "214 Carnegie Center",
    "302 Carnegie Center",
    "502 Carnegie Center",
    "506 Carnegie Center",
    "105 Carnegie Center",
    "206 Carnegie Center",
    "211 Carnegie Center",
    "504 Carnegie Center",
    "508 Carnegie Center",
    "510 Carnegie Center",
    "701 Carnegie Center",
    "804 Carnegie Center"
], disabled=False) 
else:
    # Disable Site ID dropdown if no company is selected
    site_id = st.selectbox("Site ID", ["Select a company first"], disabled=True)
    
# Check if the button was pressed and if so, display the PDF
if st.button('Generate Report'):
    if site_id == "345 Park Avenue":
        pdf_path = '345_Park_Report.pdf'
    elif site_id == "4 Chase Metrotech Center":
        pdf_path = '4_Chase_Report.pdf'
    elif site_id == "Dock 72":
        pdf_path = 'Dock_72_Report.pdf'
    else:
        pdf_path = "This site is not onboarded."
    if os.path.exists(pdf_path):
        show_pdf(pdf_path)
    else:
        st.error("This site is not onboarded.")