"""
CycleX Mobile App Mock - Streamlit Application v2
Based on actual mobile app screenshots
"""

import streamlit as st
import requests
import json
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import os

# Configuration
API_BASE_URL = "http://localhost:8025/api/cyclex"
SCREENSHOTS_DIR = "/home/sabry3/edu_demo/custom_addons/cyclex/postman/screenshots"

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'session_cookies' not in st.session_state:
    st.session_state.session_cookies = {}
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'splash'

def make_request(method, endpoint, data=None, files=None, params=None):
    """Make API request with session handling"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    
    try:
        if method == "GET":
            response = requests.get(url, params=params, cookies=st.session_state.session_cookies)
        elif method == "POST":
            if files:
                headers = {}  # Let requests set Content-Type for multipart
                response = requests.post(url, data=data, files=files, cookies=st.session_state.session_cookies)
            else:
                response = requests.post(url, json=data, headers=headers, cookies=st.session_state.session_cookies)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, cookies=st.session_state.session_cookies)
        else:
            return None, "Unsupported method"
        
        # Save cookies for session management
        if response.cookies:
            st.session_state.session_cookies.update(response.cookies.get_dict())
        
        # Handle JSON-RPC 2.0 format
        if response.headers.get('content-type', '').startswith('application/json'):
            try:
                result = response.json()
                # Check if it's JSON-RPC format
                if isinstance(result, dict) and 'result' in result:
                    return result.get('result'), None
                # Check if it's already the result format
                if isinstance(result, dict) and 'success' in result:
                    return result, None
                return result, None
            except:
                return response.text, None
        return response.text, None
    except Exception as e:
        return None, str(e)

def show_screenshot(screenshot_name):
    """Display screenshot if available"""
    screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
    if os.path.exists(screenshot_path):
        try:
            img = Image.open(screenshot_path)
            st.image(img, caption=screenshot_name.replace('.png', '').replace('_', ' ').title(), use_container_width=True)
        except:
            pass

# Page Configuration
st.set_page_config(
    page_title="CycleX Mobile App",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit UI elements
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Main App Flow
if not st.session_state.authenticated:
    # ==================== SPLASH SCREEN ====================
    if st.session_state.current_screen == 'splash':
        st.title("♻️ CycleX")
        st.markdown("### Recycling Made Easy")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("---")
            if st.button("Get Started", type="primary", use_container_width=True):
                st.session_state.current_screen = 'login'
                st.rerun()
        
        # Show screenshot
        show_screenshot("splash.png")
    
    # ==================== LOGIN SCREEN ====================
    elif st.session_state.current_screen == 'login':
        st.title("🔐 Login")
        
        # Show screenshot reference
        show_screenshot("login.png")
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### Welcome Back")
            phone = st.text_input("Phone Number", placeholder="01000000000", help="Enter your phone number")
            password = st.text_input("Password", type="password", placeholder="Enter password", help="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
            with col2:
                if st.form_submit_button("Sign Up", use_container_width=True):
                    st.session_state.current_screen = 'signup'
                    st.rerun()
            
            if submitted:
                if not phone or not password:
                    st.error("⚠️ Please enter phone number and password")
                else:
                    with st.spinner("Logging in..."):
                        data = {"phone": phone, "password": password}
                        result, error = make_request("POST", "/auth/login", data=data)
                        
                        if error:
                            st.error(f"❌ Error: {error}")
                        elif result:
                            if result.get("success"):
                                st.session_state.authenticated = True
                                st.session_state.user_data = result.get("data", {})
                                st.session_state.current_screen = 'home'
                                st.success("✅ Login successful!")
                                st.rerun()
                            else:
                                error_msg = result.get('message', 'Login failed')
                                st.error(f"❌ {error_msg}")
                                
                                # Handle phone not verified
                                if result.get('error_code') == 'PHONE_NOT_VERIFIED':
                                    if st.button("Go to Verify OTP"):
                                        st.session_state.current_screen = 'verify_otp'
                                        st.session_state.phone_to_verify = phone
                                        st.rerun()
                        else:
                            st.error("❌ No response from server")
    
    # ==================== SIGN UP SCREEN ====================
    elif st.session_state.current_screen == 'signup':
        st.title("📝 Sign Up")
        
        # Show screenshot reference
        show_screenshot("sign up.png")
        
        with st.form("signup_form", clear_on_submit=False):
            st.markdown("### Create Account")
            name = st.text_input("Full Name", placeholder="Enter your full name")
            phone = st.text_input("Phone Number", placeholder="01000000000")
            password = st.text_input("Password", type="password", placeholder="Create password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
            email = st.text_input("Email (Optional)", placeholder="email@example.com")
            
            role = st.radio("Account Type", ["Customer", "Collector"], horizontal=True)
            accept_terms = st.checkbox("I accept the Terms & Conditions", value=False)
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Sign Up", type="primary", use_container_width=True)
            with col2:
                if st.form_submit_button("Back to Login", use_container_width=True):
                    st.session_state.current_screen = 'login'
                    st.rerun()
            
            if submitted:
                if not all([name, phone, password, confirm_password]):
                    st.error("⚠️ Please fill all required fields")
                elif password != confirm_password:
                    st.error("⚠️ Passwords do not match")
                elif not accept_terms:
                    st.warning("⚠️ Please accept terms and conditions")
                else:
                    with st.spinner("Creating account..."):
                        data = {
                            "name": name,
                            "phone": phone,
                            "password": password,
                            "accept_terms": True,
                            "role": role.lower()
                        }
                        if email:
                            data["email"] = email
                        
                        result, error = make_request("POST", "/auth/register", data=data)
                        
                        if error:
                            st.error(f"❌ Error: {error}")
                        elif result:
                            if result.get("success"):
                                st.success("✅ Account created! Please verify OTP.")
                                st.session_state.current_screen = 'verify_otp'
                                st.session_state.phone_to_verify = phone
                                st.rerun()
                            else:
                                st.error(f"❌ {result.get('message', 'Sign up failed')}")
    
    # ==================== VERIFY OTP SCREEN ====================
    elif st.session_state.current_screen == 'verify_otp':
        st.title("✅ Verify OTP")
        
        # Show screenshot reference
        show_screenshot("verify.png")
        
        phone = st.session_state.get('phone_to_verify', '')
        if phone:
            st.info(f"📱 OTP sent to: {phone}")
        
        with st.form("verify_otp_form", clear_on_submit=False):
            st.markdown("### Enter Verification Code")
            otp = st.text_input("OTP Code", placeholder="123456", help="Enter 6-digit OTP code")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Verify", type="primary", use_container_width=True)
            with col2:
                resend = st.form_submit_button("Resend OTP", use_container_width=True)
            
            if submitted:
                if not otp:
                    st.error("⚠️ Please enter OTP code")
                else:
                    with st.spinner("Verifying OTP..."):
                        data = {"phone": phone, "verification_code": otp}
                        result, error = make_request("POST", "/auth/verify-otp", data=data)
                        
                        if error:
                            st.error(f"❌ Error: {error}")
                        elif result:
                            if result.get("success"):
                                st.success("✅ OTP verified! You can now login.")
                                st.session_state.current_screen = 'login'
                                st.rerun()
                            else:
                                st.error(f"❌ {result.get('message', 'Verification failed')}")
            
            if resend:
                with st.spinner("Resending OTP..."):
                    data = {"phone": phone}
                    result, error = make_request("POST", "/auth/resend-otp", data=data)
                    
                    if error:
                        st.error(f"❌ Error: {error}")
                    elif result:
                        if result.get("success"):
                            st.success("✅ OTP resent!")
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to resend OTP')}")

else:
    # ==================== AUTHENTICATED USER SCREENS ====================
    
    # Sidebar Navigation
    with st.sidebar:
        st.title("♻️ CycleX")
        st.markdown(f"**Welcome, {st.session_state.user_data.get('name', 'User')}**")
        st.markdown("---")
        
        user_type = st.session_state.user_data.get('user_type', 'customer')
        
        if user_type == 'customer':
            screens = {
                "🏠 Home": "home",
                "📦 Categories": "categories",
                "📋 My Orders": "my_orders",
                "➕ Create Order": "create_order",
                "👤 Profile": "profile",
                "💰 Wallet": "wallet"
            }
        else:  # collector
            screens = {
                "🏠 Home": "collector_home",
                "📦 Available Orders": "available_orders",
                "📋 My Orders": "collector_orders",
                "📷 Scan QR": "scan_qr",
                "👤 Profile": "collector_profile"
            }
        
        selected_screen = st.radio("Navigate", list(screens.keys()))
        st.session_state.current_screen = screens[selected_screen]
        
        st.markdown("---")
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.session_state.user_data = {}
            st.session_state.session_cookies = {}
            st.session_state.current_screen = 'login'
            st.rerun()
    
    # ==================== HOME SCREEN ====================
    if st.session_state.current_screen == 'home':
        st.title("🏠 Home")
        show_screenshot("Home.png")
        
        # Load home summary
        with st.spinner("Loading..."):
            result, error = make_request("GET", "/home/summary")
            if error:
                st.error(f"Error: {error}")
            elif result and result.get("success"):
                data = result.get("data", {})
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Balance", f"{data.get('balance', 0)} E£")
                with col2:
                    st.metric("Active Orders", data.get('active_orders_count', 0))
                with col3:
                    st.metric("Total Requests", data.get('total_requests', 0))
                with col4:
                    st.metric("Total Earnings", f"{data.get('total_earnings', 0)} E£")
            else:
                # Fallback display
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Active Orders", "0")
                with col2:
                    st.metric("Wallet Balance", "0.00 E£")
                with col3:
                    st.metric("Total Requests", "0")
    
    # ==================== CATEGORIES SCREEN ====================
    elif st.session_state.current_screen == 'categories':
        st.title("📦 Categories")
        show_screenshot("categories.png")
        
        lang_index = 0 if st.session_state.language == "en" else 1
        language = st.selectbox("Language", ["en", "ar"], index=lang_index, key="cat_lang")
        
        if st.button("🔄 Load Categories", type="primary"):
            with st.spinner("Loading categories..."):
                result, error = make_request("GET", "/catalog/categories", params={"language": language})
                
                if error:
                    st.error(f"Error: {error}")
                elif result and result.get("success"):
                    categories = result.get("data", {}).get("categories", [])
                    st.success(f"✅ Found {len(categories)} categories")
                    
                    # Display in grid
                    cols = st.columns(2)
                    for idx, cat in enumerate(categories):
                        with cols[idx % 2]:
                            with st.container():
                                st.markdown(f"### {cat.get('name', 'Unknown')}")
                                st.write(cat.get('description', 'No description'))
                                st.write(f"**Products:** {cat.get('product_count', 0)}")
                                if st.button(f"View Products", key=f"cat_{cat.get('id')}"):
                                    st.session_state.selected_category = cat.get('id')
                                    st.session_state.current_screen = 'category_products'
                                    st.rerun()
    
    # ==================== CREATE ORDER SCREEN ====================
    elif st.session_state.current_screen == 'create_order':
        st.title("➕ Create Order")
        show_screenshot("add new item.png")
        
        with st.form("create_order_form"):
            st.markdown("### Add New Item")
            category_id = st.number_input("Category ID", min_value=1, value=8)
            product_id = st.number_input("Product ID (0 for custom)", min_value=0, value=0)
            quantity = st.number_input("Quantity", min_value=1, value=1)
            weight = st.number_input("Weight (kg)", min_value=0.0, value=1.5, step=0.1)
            pickup_date = st.date_input("Pickup Date", value=datetime.now().date())
            item_name = st.text_input("Item Name (for custom items)", value="Mixed plastic bottles")
            notes = st.text_area("Notes (Optional)", value="")
            
            uploaded_file = st.file_uploader("Upload Photo", type=['png', 'jpg', 'jpeg'])
            
            submitted = st.form_submit_button("Create Order", type="primary")
            
            if submitted:
                with st.spinner("Creating order..."):
                    data = {
                        "category_id": category_id,
                        "quantity": quantity,
                        "weight": weight,
                        "pickup_date": pickup_date.strftime("%Y-%m-%d"),
                        "notes": notes
                    }
                    
                    if product_id > 0:
                        data["product_id"] = product_id
                    else:
                        data["item_name"] = item_name
                    
                    files = None
                    if uploaded_file:
                        files = {"photo": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    
                    result, error = make_request("POST", "/request/create", data=data, files=files)
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            st.success("✅ Order created successfully!")
                            st.json(result.get("data", {}))
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to create order')}")
    
    # ==================== MY ORDERS SCREEN ====================
    elif st.session_state.current_screen == 'my_orders':
        st.title("📋 My Orders")
        show_screenshot("my orders.png")
        
        status_filter = st.selectbox("Filter by Status", ["all", "active", "pending", "assigned", "completed"])
        
        if st.button("🔄 Load Orders", type="primary"):
            with st.spinner("Loading orders..."):
                params = {} if status_filter == "all" else {"status": status_filter}
                result, error = make_request("GET", "/orders", params=params)
                
                if error:
                    st.error(f"Error: {error}")
                elif result and result.get("success"):
                    orders = result.get("data", {}).get("requests", [])
                    st.success(f"✅ Found {len(orders)} orders")
                    
                    for order in orders:
                        with st.expander(f"Order #{order.get('id', 'N/A')} - {order.get('status', 'Unknown')}"):
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Status:** {order.get('status', 'N/A')}")
                                st.write(f"**Total:** {order.get('total_amount', 0)} {order.get('currency_symbol', '$')}")
                            with col2:
                                st.write(f"**Pickup Date:** {order.get('pickup_date', 'N/A')}")
                                st.write(f"**Created:** {order.get('created_at', 'N/A')}")
                            
                            if st.button(f"Track Order", key=f"track_{order.get('id')}"):
                                st.session_state.selected_order_id = order.get('id')
                                st.session_state.current_screen = 'order_tracking'
                                st.rerun()
                else:
                    st.error(f"❌ {result.get('message', 'Failed to load orders') if result else 'No response'}")
    
    # ==================== PROFILE SCREEN ====================
    elif st.session_state.current_screen == 'profile':
        st.title("👤 Profile")
        show_screenshot("profile.png")
        
        if st.button("🔄 Load Profile", type="primary"):
            with st.spinner("Loading profile..."):
                result, error = make_request("GET", "/user/profile")
                
                if error:
                    st.error(f"Error: {error}")
                elif result and result.get("success"):
                    profile = result.get("data", {})
                    st.success("✅ Profile loaded")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("### Personal Info")
                        st.write(f"**Name:** {profile.get('name', 'N/A')}")
                        st.write(f"**Phone:** {profile.get('phone', 'N/A')}")
                        st.write(f"**Email:** {profile.get('email', 'N/A')}")
                    with col2:
                        st.markdown("### Account Info")
                        st.write(f"**User Type:** {profile.get('user_type', 'N/A')}")
                        st.write(f"**Language:** {profile.get('language', 'N/A')}")
                        st.write(f"**Status:** {profile.get('account_status', 'N/A')}")
                    
                    if st.button("Edit Profile"):
                        st.session_state.current_screen = 'edit_profile'
                        st.rerun()
    
    # ==================== WALLET SCREEN ====================
    elif st.session_state.current_screen == 'wallet':
        st.title("💰 Wallet")
        show_screenshot("profile-wallet.png")
        
        if st.button("🔄 Load Wallet", type="primary"):
            with st.spinner("Loading wallet..."):
                result, error = make_request("GET", "/wallet")
                
                if error:
                    st.error(f"Error: {error}")
                elif result and result.get("success"):
                    wallet = result.get("data", {})
                    st.success("✅ Wallet loaded")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Balance", f"{wallet.get('balance', 0)} E£")
                    with col2:
                        st.metric("Total Earned", f"{wallet.get('total_earned', 0)} E£")
                    with col3:
                        st.metric("Total Withdrawn", f"{wallet.get('total_withdrawn', 0)} E£")
                    
                    if st.button("View Transactions"):
                        st.session_state.current_screen = 'transactions'
                        st.rerun()
    
    # ==================== COLLECTOR SCREENS ====================
    elif st.session_state.current_screen == 'collector_home':
        st.title("🚚 Collector Dashboard")
        show_screenshot("home - coolector.png")
        
        if st.button("🔄 Load Dashboard", type="primary"):
            with st.spinner("Loading..."):
                result, error = make_request("GET", "/collector/home")
                if result and result.get("success"):
                    dashboard = result.get("data", {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Available Orders", dashboard.get('available_orders_count', 0))
                    with col2:
                        st.metric("Assigned Orders", dashboard.get('assigned_orders_count', 0))
                    with col3:
                        st.metric("Total Earnings", f"{dashboard.get('total_earnings', 0)} E£")
    
    elif st.session_state.current_screen == 'available_orders':
        st.title("📦 Available Orders")
        show_screenshot("active orders.png")
        
        if st.button("🔄 Load Orders", type="primary"):
            with st.spinner("Loading..."):
                result, error = make_request("GET", "/collector/orders")
                if result and result.get("success"):
                    orders = result.get("data", {}).get("orders", [])
                    for order in orders:
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**Order #{order.get('id')}** - {order.get('distance', 'N/A')} km")
                        with col2:
                            if st.button(f"Accept", key=f"accept_{order.get('id')}"):
                                result2, _ = make_request("POST", f"/collector/orders/{order.get('id')}/accept")
                                if result2 and result2.get("success"):
                                    st.success("✅ Accepted!")
                                    st.rerun()
                        with col3:
                            if st.button(f"Reject", key=f"reject_{order.get('id')}"):
                                result2, _ = make_request("POST", f"/collector/orders/{order.get('id')}/reject", data={"reason": "Not available"})
                                if result2 and result2.get("success"):
                                    st.success("✅ Rejected!")
                                    st.rerun()

# Footer
st.markdown("---")
st.caption(f"API: {API_BASE_URL} | Status: {'✅ Authenticated' if st.session_state.authenticated else '🔒 Not Authenticated'}")

