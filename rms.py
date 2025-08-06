# rms.py
import streamlit as st
import time
import pandas as pd
import os
from datetime import datetime
from style import center_title, section_header, center_button

# Preparation time
prep_time = {'burger': 2, 'fries': 1, 'coke': 1, 'wrap': 2}

class SurajError(Exception):
    pass

class RMS:
    def __init__(self, rest_name, rest_menu, csv_file):
        self.rest_name = rest_name
        self.rest_menu = rest_menu
        self.csv_file = csv_file

    def welcome_user(self):
        center_title(f"Welcome to {self.rest_name}")
        st.markdown("<hr>", unsafe_allow_html=True)
        print("Welcome to the Foodiess")

    def take_order_directly(self):
        section_header("Menu")
        st.session_state.user_cart = {}
        cols = st.columns(2)
        i = 0
        for item, price in self.rest_menu.items():
            with cols[i % 2]:
                qty = st.number_input(
                    f"{item.title()} (₹{price})", min_value=0, step=1, key=f"qty_{item}"
                )
                if qty > 0:
                    st.session_state.user_cart[item] = qty
            i += 1
        if center_button("Confirm Order", "confirm_order"):
            if st.session_state.user_cart:
                st.session_state.order_confirmed = True
                st.rerun()
            else:
                st.warning("Please select at least one item.")
        print("Order confirmed:", st.session_state.order_confirmed)

    def display_cart(self):
        if st.session_state.user_cart:
            section_header("Order Summary")
            cart_data = []
            for item, qty in st.session_state.user_cart.items():
                cart_data.append([f"{item.title()} x{qty}", f"₹{self.rest_menu[item] * qty}"])
            st.table(cart_data)

    def verify_bill(self):
        st.session_state.total_bill = sum(
            self.rest_menu[item] * qty for item, qty in st.session_state.user_cart.items()
        )
        section_header(f"Total Bill: ₹{st.session_state.total_bill}")
        user_pay = st.number_input("Enter payment amount:", min_value=0.0, format="%.2f")
        if center_button("Pay Now", "pay_now"):
            try:
                if user_pay >= st.session_state.total_bill:
                    change = user_pay - st.session_state.total_bill
                    st.session_state.payment_message = (
                        f"Payment Successful! Change: ₹{change:.2f}"
                        if change > 0 else "Payment Successful! Exact amount received."
                    )
                    st.session_state.payment_done = True
                    self.save_order()
                    st.rerun()
                else:
                    raise SurajError("Payment Failed! Please pay full amount!")
            except SurajError as e:
                st.error(str(e))
        print('current cart: ', st.session_state.user_cart)

    def preparing_order(self):
        total_time = sum(prep_time[item] * qty for item, qty in st.session_state.user_cart.items())
        if st.session_state.final_screen_start_time is None:
            st.session_state.final_screen_start_time = time.time()
        elapsed_time = time.time() - st.session_state.final_screen_start_time
        remaining_time = max(0, 10 - elapsed_time)
        section_header("Payment Successful!")
        st.success(st.session_state.payment_message)
        section_header("Preparing Your Order")
        st.info(f"Estimated preparation time: {total_time} minutes")
        if remaining_time > 0:
            st.write(f"Processing... {int(remaining_time)} seconds remaining")
            time.sleep(1)
            st.rerun()
        else:
            st.session_state.show_final_screen = True
            st.rerun()

    def final_screen_with_timer(self):
        center_title(f"Welcome to {self.rest_name}")
        if center_button("🍽️ Start New Order", "start_new_order"):
            self.reset_session()
            st.rerun()

    def reset_session(self):
        st.session_state.order_confirmed = False
        st.session_state.payment_done = False
        st.session_state.order_prepared = False
        st.session_state.user_cart = {}
        st.session_state.total_bill = 0.0
        st.session_state.payment_message = ""
        st.session_state.show_final_screen = False
        st.session_state.final_screen_start_time = None

    def save_order(self):
        order_data = {
            "items": {item: qty for item, qty in st.session_state.user_cart.items()},
            "total": st.session_state.total_bill,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        order_row = {
            "Time": order_data["time"],
            "Total_Bill": order_data["total"]
        }
        for item in self.rest_menu.keys():
            order_row[item] = order_data["items"].get(item, 0)
        if not os.path.exists(self.csv_file):
            pd.DataFrame([order_row]).to_csv(self.csv_file, index=False)
        else:
            df = pd.read_csv(self.csv_file)
            df = pd.concat([df, pd.DataFrame([order_row])], ignore_index=True)
            df.to_csv(self.csv_file, index=False)
        print('total bill:', st.session_state.total_bill)

    # ✅ The function you missed earlier
    def order_process(self):
        if not st.session_state.order_confirmed:
            self.welcome_user()
            self.take_order_directly()
        elif st.session_state.order_confirmed and not st.session_state.payment_done:
            self.display_cart()
            self.verify_bill()
        elif st.session_state.payment_done and not st.session_state.show_final_screen:
            self.preparing_order()
        elif st.session_state.show_final_screen:
            self.final_screen_with_timer()
