import streamlit as st
from rms import RMS
from admin_dashboard import admin_login, sales_dashboard
from style import apply_fullscreen_css

# ---------------- BASIC CONFIG ----------------
restaurant_name = "Foodiees"
restaurant_menu = {
    "burger": 200,
    "fries": 180,
    "coke": 140,
    "wrap": 130
}
CSV_FILE = "orders_data.csv"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "foodiees2025"

# ---------------- SESSION STATES ----------------
if "order_confirmed" not in st.session_state:
    st.session_state.order_confirmed = False
if "payment_done" not in st.session_state:
    st.session_state.payment_done = False
if "order_prepared" not in st.session_state:
    st.session_state.order_prepared = False
if "user_cart" not in st.session_state:
    st.session_state.user_cart = {}
if "total_bill" not in st.session_state:
    st.session_state.total_bill = 0.0
if "payment_message" not in st.session_state:
    st.session_state.payment_message = ""
if "show_final_screen" not in st.session_state:
    st.session_state.show_final_screen = False
if "final_screen_start_time" not in st.session_state:
    st.session_state.final_screen_start_time = None
if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = "menu"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "show_admin_option" not in st.session_state:
    st.session_state.show_admin_option = False

# ---------------- MAIN APP ----------------
apply_fullscreen_css()

# Admin trigger (hidden button)
if st.button("🔐", help="Admin Access", key="hidden_admin_trigger"):
    st.session_state.show_admin_option = True

if st.session_state.show_admin_option and not st.session_state.admin_authenticated:
    admin_login(ADMIN_USERNAME, ADMIN_PASSWORD)
elif st.session_state.admin_authenticated:
    sales_dashboard(restaurant_menu, CSV_FILE)
else:
    rms_app = RMS(restaurant_name, restaurant_menu, CSV_FILE)
    rms_app.order_process()
