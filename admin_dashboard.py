import streamlit as st
import pandas as pd
import os
import time
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- ADMIN LOGIN ----------------
def admin_login(admin_user, admin_pass):
    """Admin login screen"""
    st.markdown('<h2 style="color:#FF9913;text-align:center;">Admin Login</h2>', unsafe_allow_html=True)
    
    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if username.strip() == admin_user and password.strip() == admin_pass:
            st.session_state.admin_authenticated = True
            st.success("✅ Login successful!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Invalid username or password!")

    # Back to guest mode button
    if st.button("← Back to Guest Mode"):
        st.session_state.show_admin_option = False
        st.rerun()

# ---------------- ADMIN LOGOUT ----------------
def admin_logout():
    st.session_state.admin_authenticated = False
    st.session_state.dashboard_view = "menu"
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()

# ---------------- SALES DASHBOARD ----------------
def sales_dashboard(restaurant_menu, csv_file):
    st.markdown('<h1 style="color:#FF9913;text-align:center;">Sales Dashboard</h1>', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🚪 Logout", key="admin_logout"):
            admin_logout()

    st.markdown('<hr style="border:2px solid #FF9913; margin: 1rem 0;">', unsafe_allow_html=True)

    if not os.path.exists(csv_file):
        st.info("No sales records yet.")
        return

    df = pd.read_csv(csv_file)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("All Sales Records"):
            st.session_state.dashboard_view = "records"
    with col2:
        if st.button("Basic Insights"):
            st.session_state.dashboard_view = "insights"
    with col3:
        if st.button("Top Selling Items"):
            st.session_state.dashboard_view = "top_items"
    with col4:
        if st.button("Sales Visualization"):
            st.session_state.dashboard_view = "visualization"

    if st.session_state.dashboard_view == "records":
        show_all_records(df)
    elif st.session_state.dashboard_view == "insights":
        show_basic_insights(df)
    elif st.session_state.dashboard_view == "top_items":
        show_top_selling_items(df, restaurant_menu)
    elif st.session_state.dashboard_view == "visualization":
        show_sales_visualization(df, restaurant_menu)
    else:
        st.info("Select a view from the buttons above.")

# ---------------- ALL SALES VIEWS ----------------
def show_all_records(df):
    st.subheader("All Sales Records")
    st.dataframe(df, use_container_width=True)

def show_basic_insights(df):
    st.subheader("Basic Insights")
    total_revenue = df["Total_Bill"].sum()
    total_orders = len(df)
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"₹{total_revenue:.2f}")
    c2.metric("Total Orders", total_orders)
    c3.metric("Average Order Value", f"₹{avg_order_value:.2f}")

    st.subheader("Recent Orders")
    st.dataframe(df.tail(5)[['Time', 'Total_Bill']], use_container_width=True)

def show_top_selling_items(df, restaurant_menu):
    st.subheader("Top Selling Items")
    item_totals = {item: int(df[item].sum()) for item in restaurant_menu.keys()}
    sorted_items = sorted(item_totals.items(), key=lambda x: x[1], reverse=True)
    table_data = []
    for rank, (item, qty) in enumerate(sorted_items, 1):
        revenue = qty * restaurant_menu[item]
        table_data.append({
            "Rank": rank,
            "Item": item.title(),
            "Quantity Sold": qty,
            "Unit Price": f"₹{restaurant_menu[item]}",
            "Total Revenue": f"₹{revenue}"
        })
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

def show_sales_visualization(df, restaurant_menu):
    st.subheader("📊 Sales Visualization")

    # -------- ITEM TOTALS --------
    item_totals = {item: int(df[item].sum()) for item in restaurant_menu.keys()}

    # -------- BAR CHARTS (Brand Color) --------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    # Total Items Sold
    sns.barplot(
        x=list(item_totals.keys()),
        y=list(item_totals.values()),
        ax=ax1,
        color="#FF9913"  # ✅ brand color
    )
    ax1.set_title("Total Items Sold", fontsize=12, color="#333333")
    ax1.set_ylabel("Quantity Sold", fontsize=10)
    ax1.tick_params(axis='x', rotation=45)

    # Revenue by Item
    item_revenues = {item: qty * restaurant_menu[item] for item, qty in item_totals.items()}
    sns.barplot(
        x=list(item_revenues.keys()),
        y=list(item_revenues.values()),
        ax=ax2,
        color="#FF9913"  # ✅ brand color
    )
    ax2.set_title("Revenue by Item (₹)", fontsize=12, color="#333333")
    ax2.set_ylabel("Revenue (₹)", fontsize=10)
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    st.pyplot(fig)

    # -------- SALES TREND LINE CHART (Brand Color) --------
    if len(df) > 1:
        st.subheader("📈 Sales Trend Over Time")
        df['Time'] = pd.to_datetime(df['Time'])
        df_sorted = df.sort_values('Time')

        fig2, ax3 = plt.subplots(figsize=(10, 3))
        ax3.plot(
            df_sorted['Time'],
            df_sorted['Total_Bill'],
            marker='o',
            linewidth=2,
            color="#FF9913"  # ✅ brand color line
        )
        ax3.set_ylabel("Order Value (₹)", fontsize=10)
        ax3.set_title("Sales Trend Over Time", fontsize=12, color="#333333")
        ax3.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        st.pyplot(fig2)