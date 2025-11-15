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
from demo_data import (
    DEMO_CATEGORIES, DEMO_PRODUCTS, DEMO_ORDERS, DEMO_WALLET,
    DEMO_TRANSACTIONS, DEMO_PROFILE, DEMO_COLLECTOR_ORDERS,
    DEMO_HOME_SUMMARY, DEMO_COLLECTOR_HOME
)

# Configuration
API_BASE_URL = "http://localhost:8025/api/cyclex"
SCREENSHOTS_DIR = "/home/sabry3/edu_demo/custom_addons/cyclex/postman/screenshots"
USE_DEMO_DATA = False  # Set to False to use real API only

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
                # Return dict if it's a dict, otherwise return as-is
                if isinstance(result, dict):
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
            st.image(img, caption=screenshot_name.replace('.png', '').replace('_', ' ').title(), width="stretch")
        except:
            pass

# Page Configuration - Mobile-like compact design
st.set_page_config(
    page_title="CycleX Mobile App",
    page_icon="♻️",
    layout="centered",  # Changed from "wide" to "centered" for mobile-like
    initial_sidebar_state="collapsed"
)

# Hide default Streamlit UI elements and make compact
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 500px;
    }
    h1 {
        font-size: 1.8rem;
    }
    h2 {
        font-size: 1.4rem;
    }
    h3 {
        font-size: 1.2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
    }
    .stSelectbox>div>div>select {
        border-radius: 8px;
    }
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
            if st.button("Get Started", type="primary", width="stretch"):
                st.session_state.current_screen = 'login'
                st.rerun()
        
        # Show screenshot
        show_screenshot("splash.png")
    
    # ==================== LOGIN SCREEN ====================
    elif st.session_state.current_screen == 'login':
        st.markdown("### 🔐 Login")
        
        # Demo mode info
        if USE_DEMO_DATA:
            with st.expander("📱 Demo Mode - Quick Login", expanded=True):
                st.info("**Demo users available:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Customer:**")
                    st.code("Phone: 01000000000\nPassword: demo123")
                    if st.button("👤 Login as Customer", width="stretch", key="demo_customer"):
                        st.session_state.authenticated = True
                        st.session_state.user_data = {
                            'name': 'Demo Customer',
                            'phone': '01000000000',
                            'user_type': 'customer',
                            'account_status': 'active',
                            'verified': True
                        }
                        st.session_state.current_screen = 'home'
                        st.rerun()
                with col2:
                    st.markdown("**Collector:**")
                    st.code("Phone: 01000000001\nPassword: demo123")
                    if st.button("🚚 Login as Collector", width="stretch", key="demo_collector"):
                        st.session_state.authenticated = True
                        st.session_state.user_data = {
                            'name': 'Demo Collector',
                            'phone': '01000000001',
                            'user_type': 'collector',
                            'account_status': 'active',
                            'verified': True
                        }
                        st.session_state.current_screen = 'collector_home'
                        st.rerun()
                st.markdown("---")
                st.caption("💡 Or use the form below to test real API login")
        
        with st.form("login_form", clear_on_submit=False):
            phone = st.text_input("📱 Phone Number", placeholder="01000000000", value="01000000000" if USE_DEMO_DATA else "")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password", value="demo123" if USE_DEMO_DATA else "")
            
            submitted = st.form_submit_button("Login", type="primary", width="stretch")
            
            if submitted:
                if not phone or not password:
                    st.error("⚠️ Please enter phone number and password")
                else:
                    # Demo mode: Allow login with demo credentials
                    if USE_DEMO_DATA and phone in ["01000000000", "01000000001"] and password == "demo123":
                        st.session_state.authenticated = True
                        if phone == "01000000000":
                            st.session_state.user_data = {
                                'name': 'Demo Customer',
                                'phone': '01000000000',
                                'user_type': 'customer',
                                'account_status': 'active',
                                'verified': True,
                                'total_requests': 15,
                                'total_earnings': 450.75
                            }
                            st.session_state.current_screen = 'home'
                        else:
                            st.session_state.user_data = {
                                'name': 'Demo Collector',
                                'phone': '01000000001',
                                'user_type': 'collector',
                                'account_status': 'active',
                                'verified': True,
                                'total_orders_completed': 45,
                                'total_earnings': 1250.50
                            }
                            st.session_state.current_screen = 'collector_home'
                        st.success("✅ Demo login successful!")
                        st.rerun()
                    else:
                        # Real API login
                        with st.spinner("Logging in..."):
                            data = {"phone": phone, "password": password}
                            result, error = make_request("POST", "/auth/login", data=data)
                            
                            if error:
                                st.error(f"❌ Error: {error}")
                            elif result and isinstance(result, dict):
                                if result.get("success"):
                                    st.session_state.authenticated = True
                                    st.session_state.user_data = result.get("data", {})
                                    user_type = st.session_state.user_data.get('user_type', 'customer')
                                    st.session_state.current_screen = 'home' if user_type == 'customer' else 'collector_home'
                                    st.success("✅ Login successful!")
                                    st.rerun()
                                else:
                                    error_msg = result.get('message', 'Login failed')
                                    st.error(f"❌ {error_msg}")
                                    
                                    # Handle phone not verified
                                    if result.get('error_code') == 'PHONE_NOT_VERIFIED':
                                        st.session_state.phone_not_verified = True
                                        st.session_state.phone_to_verify = phone
                            else:
                                st.error("❌ No response from server")
        
        # Handle phone not verified - show button outside form
        if st.session_state.get('phone_not_verified', False):
            st.warning("⚠️ Phone number not verified")
            if st.button("Go to Verify OTP", width="stretch"):
                st.session_state.current_screen = 'verify_otp'
                st.session_state.phone_not_verified = False
                st.rerun()
        
        st.markdown("---")
        if st.button("📝 Don't have an account? Sign Up", width="stretch"):
            st.session_state.current_screen = 'signup'
            st.rerun()
    
    # ==================== SIGN UP SCREEN ====================
    elif st.session_state.current_screen == 'signup':
        st.markdown("### 📝 Sign Up")
        
        with st.form("signup_form", clear_on_submit=False):
            name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            phone = st.text_input("📱 Phone Number", placeholder="01000000000")
            password = st.text_input("🔒 Password", type="password", placeholder="Create password")
            confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm password")
            email = st.text_input("📧 Email (Optional)", placeholder="email@example.com")
            
            role = st.radio("Account Type", ["Customer", "Collector"], horizontal=True, index=0)
            accept_terms = st.checkbox("I accept the Terms & Conditions", value=False)
            
            submitted = st.form_submit_button("Sign Up", type="primary", width="stretch")
            
            if submitted:
                # Strip whitespace and validate
                name = name.strip() if name else ""
                phone = phone.strip() if phone else ""
                password = password.strip() if password else ""
                confirm_password = confirm_password.strip() if confirm_password else ""
                email = email.strip() if email else ""
                
                if not name or not phone or not password or not confirm_password:
                    st.error("⚠️ Name, phone, password, and confirm password are required")
                elif password != confirm_password:
                    st.error("⚠️ Passwords do not match")
                elif not accept_terms:
                    st.warning("⚠️ Please accept terms and conditions")
                elif len(password) < 8:
                    st.error("⚠️ Password must be at least 8 characters")
                elif not any(c.isupper() for c in password):
                    st.error("⚠️ Password must contain at least one uppercase letter")
                elif not any(c.islower() for c in password):
                    st.error("⚠️ Password must contain at least one lowercase letter")
                elif not any(c.isdigit() for c in password):
                    st.error("⚠️ Password must contain at least one number")
                elif len(phone) < 10:
                    st.error("⚠️ Phone number must be at least 10 digits")
                else:
                    with st.spinner("Creating account..."):
                        role_value = role.lower() if role and isinstance(role, str) else "customer"
                        data = {
                            "name": name,
                            "phone": phone,
                            "password": password,
                            "confirm_password": confirm_password,  # API requires this
                            "user_type": role_value,  # API expects user_type, not role
                            "accept_terms": True
                        }
                        if email:
                            data["email"] = email
                        
                        result, error = make_request("POST", "/auth/register", data=data)
                        
                        if error:
                            st.error(f"❌ Error: {error}")
                        elif result:
                            if result.get("success"):
                                verification_code = None
                                data_payload = result.get("data")
                                if isinstance(data_payload, dict):
                                    verification_code = data_payload.get("verification_code")

                                st.success("✅ Account created! Please verify OTP.")
                                st.session_state.current_screen = 'verify_otp'
                                st.session_state.phone_to_verify = phone
                                if verification_code:
                                    st.session_state.last_verification_code = verification_code
                                st.rerun()
                            else:
                                st.error(f"❌ {result.get('message', 'Sign up failed')}")
        
        st.markdown("---")
        if st.button("← Back to Login", width="stretch"):
            st.session_state.current_screen = 'login'
            st.rerun()
    
    # ==================== VERIFY OTP SCREEN ====================
    elif st.session_state.current_screen == 'verify_otp':
        st.markdown("### ✅ Verify OTP")
        
        phone = st.session_state.get('phone_to_verify', '')
        if phone:
            st.info(f"📱 OTP sent to: {phone}")

        test_otp = st.session_state.get('last_verification_code')
        if test_otp:
            st.warning(f"🧪 Test OTP Code: {test_otp} (local testing only)")
        
        with st.form("verify_otp_form", clear_on_submit=False):
            otp = st.text_input("🔢 OTP Code", placeholder="123456", help="Enter 6-digit OTP code")
            
            submitted = st.form_submit_button("Verify", type="primary", width="stretch")
            
            st.markdown("---")
            resend = st.form_submit_button("🔄 Resend OTP", width="stretch")
            
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
        
        st.markdown("---")
        if st.button("🔄 Resend OTP", width="stretch"):
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
    
    # Initialize screen if not set
    user_type = st.session_state.user_data.get('user_type', 'customer')
    if 'current_screen' not in st.session_state or st.session_state.current_screen not in ['home', 'categories', 'create_order', 'my_orders', 'profile', 'wallet', 'collector_home', 'available_orders', 'collector_orders', 'scan_qr', 'collector_profile']:
        st.session_state.current_screen = 'home' if user_type == 'customer' else 'collector_home'
    
    # Sidebar for user info and logout
    with st.sidebar:
        st.markdown(f"**{st.session_state.user_data.get('name', 'User')}**")
        st.markdown(f"📱 {st.session_state.user_data.get('phone', 'N/A')}")
        st.markdown(f"👤 {st.session_state.user_data.get('user_type', 'customer').title()}")
        st.markdown("---")
        if st.button("🚪 Logout", type="secondary", width="stretch"):
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
            elif result and isinstance(result, dict) and result.get("success"):
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
        st.markdown("### 📦 Categories")
        
        # Initialize categories in session state if not exists
        if 'loaded_categories' not in st.session_state:
            st.session_state.loaded_categories = []
        
        # Load categories
        if USE_DEMO_DATA:
            st.session_state.loaded_categories = DEMO_CATEGORIES
            st.info("📱 Demo Data")
        else:
            lang_index = 0 if st.session_state.language == "en" else 1
            language = st.selectbox("Language", ["en", "ar"], index=lang_index, key="cat_lang")
            
            if st.button("🔄 Load", type="primary"):
                with st.spinner("Loading..."):
                    # Get root categories first
                    result, error = make_request("GET", "/catalog/categories", params={"language": language})
                    st.write("DEBUG - Root result:", result)
                    st.write("DEBUG - Error:", error)
                    if not error and result and isinstance(result, dict) and result.get("success"):
                        root_categories = result.get("data", {}).get("categories", [])
                        st.write(f"DEBUG - Root categories count: {len(root_categories)}")
                        # If we have a root "Recyclable Materials" category, fetch its children
                        if root_categories and root_categories[0].get("has_children"):
                            parent_id = root_categories[0].get("id")
                            st.write(f"DEBUG - Fetching children of parent_id: {parent_id}")
                            result, error = make_request("GET", "/catalog/categories", params={"language": language, "parent_id": parent_id})
                            st.write("DEBUG - Children result:", result)
                            if not error and result and isinstance(result, dict) and result.get("success"):
                                st.session_state.loaded_categories = result.get("data", {}).get("categories", [])
                                st.write(f"DEBUG - Loaded {len(st.session_state.loaded_categories)} child categories")
                        else:
                            st.session_state.loaded_categories = root_categories
                            st.write(f"DEBUG - No children, loaded {len(st.session_state.loaded_categories)} root categories")
                    else:
                        st.error(f"Failed to load categories. Error: {error}")
        
        if st.session_state.loaded_categories:
            # Compact card-like display
            for cat in st.session_state.loaded_categories:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**{cat.get('name', 'Unknown')}**")
                        st.caption(cat.get('description', 'No description'))
                    with col2:
                        st.metric("", f"{cat.get('product_count', 0)}")
                    
                    if st.button(f"View Products →", key=f"cat_{cat.get('id')}", width="stretch"):
                        st.session_state.selected_category = cat.get('id')
                        st.session_state.current_screen = 'category_products'
                        st.rerun()
                    st.divider()
        else:
            st.info("Click 'Load' to fetch categories")
    
    # ==================== CREATE ORDER SCREEN ====================
    elif st.session_state.current_screen == 'create_order':
        st.markdown("### ➕ Create Order")
        
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
                    elif result and isinstance(result, dict):
                        if result.get("success"):
                            st.success("✅ Order created successfully!")
                            st.json(result.get("data", {}))
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to create order')}")
    
    # ==================== MY ORDERS SCREEN ====================
    elif st.session_state.current_screen == 'my_orders':
        st.markdown("### 📋 My Orders")
        
        status_filter = st.selectbox("Filter", ["all", "active", "pending", "assigned", "completed"], index=0)
        
        # Load orders
        orders = []
        if USE_DEMO_DATA:
            orders = DEMO_ORDERS
            st.info("📱 Demo Data")
        else:
            if st.button("🔄 Load", type="primary"):
                with st.spinner("Loading..."):
                    params = {} if status_filter == "all" else {"status": status_filter}
                    result, error = make_request("GET", "/orders", params=params)
                    if not error and result and isinstance(result, dict) and result.get("success"):
                        orders = result.get("data", {}).get("requests", [])
        
        if orders:
            for order in orders:
                with st.container():
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Order #{order.get('id', 'N/A')}**")
                        st.caption(f"Status: {order.get('status', 'Unknown')} | {order.get('pickup_date', 'N/A')}")
                    with col2:
                        st.metric("", f"{order.get('total_amount', 0)} {order.get('currency_symbol', 'E£')}")
                    
                    if st.button(f"Track →", key=f"track_{order.get('id')}", width="stretch"):
                        st.session_state.selected_order_id = order.get('id')
                        st.session_state.current_screen = 'order_tracking'
                        st.rerun()
                    st.divider()
        else:
            st.info("No orders found")
    
    # ==================== PROFILE SCREEN ====================
    elif st.session_state.current_screen == 'profile':
        st.markdown("### 👤 Profile")
        
        # Load profile
        profile = None
        if USE_DEMO_DATA:
            profile = DEMO_PROFILE
            st.info("📱 Demo Data")
        else:
            if st.button("🔄 Load", type="primary"):
                with st.spinner("Loading..."):
                    result, error = make_request("GET", "/user/profile")
                    if not error and result and isinstance(result, dict) and result.get("success"):
                        profile = result.get("data", {})
        
        if profile:
            st.markdown("**Personal Info**")
            st.write(f"👤 {profile.get('name', 'N/A')}")
            st.write(f"📱 {profile.get('phone', 'N/A')}")
            st.write(f"📧 {profile.get('email', 'N/A')}")
            st.divider()
            
            st.markdown("**Account Info**")
            st.write(f"Type: {profile.get('user_type', 'N/A')}")
            st.write(f"Language: {profile.get('language', 'N/A')}")
            st.write(f"Status: {profile.get('account_status', 'N/A')}")
            st.write(f"Verified: {'✅' if profile.get('verified') else '❌'}")
            st.divider()
            
            if profile.get('user_type') == 'customer':
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Requests", profile.get('total_requests', 0))
                with col2:
                    st.metric("Total Earnings", f"{profile.get('total_earnings', 0)} E£")
            
            if st.button("✏️ Edit Profile", width="stretch"):
                st.session_state.current_screen = 'edit_profile'
                st.rerun()
    
    # ==================== WALLET SCREEN ====================
    elif st.session_state.current_screen == 'wallet':
        st.markdown("### 💰 Wallet")
        
        # Load wallet
        wallet = None
        if USE_DEMO_DATA:
            wallet = DEMO_WALLET
            st.info("📱 Demo Data")
        else:
            if st.button("🔄 Load", type="primary"):
                with st.spinner("Loading..."):
                    result, error = make_request("GET", "/wallet")
                    if not error and result and isinstance(result, dict) and result.get("success"):
                        wallet = result.get("data", {})
        
        if wallet:
            st.metric("Balance", f"{wallet.get('balance', 0)} {wallet.get('currency_symbol', 'E£')}", delta=None)
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Earned", f"{wallet.get('total_earned', 0)} {wallet.get('currency_symbol', 'E£')}")
            with col2:
                st.metric("Total Withdrawn", f"{wallet.get('total_withdrawn', 0)} {wallet.get('currency_symbol', 'E£')}")
            
            if st.button("📊 View Transactions", width="stretch"):
                st.session_state.current_screen = 'transactions'
                st.rerun()
    
    # ==================== COLLECTOR SCREENS ====================
    if st.session_state.current_screen == 'collector_home':
        st.markdown("### 🚚 Collector Dashboard")
        
        # Load dashboard
        dashboard = None
        if USE_DEMO_DATA:
            dashboard = DEMO_COLLECTOR_HOME
            st.info("📱 Demo Data")
        else:
            if st.button("🔄 Load", type="primary"):
                with st.spinner("Loading..."):
                    result, error = make_request("GET", "/collector/home")
                    if not error and result and isinstance(result, dict) and result.get("success"):
                        dashboard = result.get("data", {})
        
        if dashboard:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Available", dashboard.get('available_orders_count', 0))
                st.metric("Assigned", dashboard.get('assigned_orders_count', 0))
            with col2:
                st.metric("Completed", dashboard.get('total_orders_completed', 0))
                st.metric("Earnings", f"{dashboard.get('total_earnings', 0)} {dashboard.get('currency_symbol', 'E£')}")
            st.metric("Rating", f"{dashboard.get('average_rating', 0)} ⭐")
    
    elif st.session_state.current_screen == 'available_orders':
        st.title("📦 Available Orders")
        show_screenshot("active orders.png")
        
        if st.button("🔄 Load Orders", type="primary"):
            with st.spinner("Loading..."):
                result, error = make_request("GET", "/collector/orders")
                if result and isinstance(result, dict) and result.get("success"):
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

    # ==================== BOTTOM NAVIGATION BAR ====================
    st.markdown("---")
    st.markdown("### 📱 Navigation")
    
    if user_type == 'customer':
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🏠\nHome", width="stretch", key="nav_home", 
                        type="primary" if st.session_state.current_screen == 'home' else "secondary"):
                st.session_state.current_screen = 'home'
                st.rerun()
        
        with col2:
            if st.button("📦\nCategories", width="stretch", key="nav_categories",
                        type="primary" if st.session_state.current_screen == 'categories' else "secondary"):
                st.session_state.current_screen = 'categories'
                st.rerun()
        
        with col3:
            if st.button("➕\nCreate", width="stretch", key="nav_create",
                        type="primary" if st.session_state.current_screen == 'create_order' else "secondary"):
                st.session_state.current_screen = 'create_order'
                st.rerun()
        
        with col4:
            if st.button("📋\nOrders", width="stretch", key="nav_orders",
                        type="primary" if st.session_state.current_screen == 'my_orders' else "secondary"):
                st.session_state.current_screen = 'my_orders'
                st.rerun()
        
        with col5:
            if st.button("👤\nProfile", width="stretch", key="nav_profile",
                        type="primary" if st.session_state.current_screen == 'profile' else "secondary"):
                st.session_state.current_screen = 'profile'
                st.rerun()
    
    else:  # collector
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            if st.button("🏠\nHome", width="stretch", key="nav_coll_home",
                        type="primary" if st.session_state.current_screen == 'collector_home' else "secondary"):
                st.session_state.current_screen = 'collector_home'
                st.rerun()
        
        with col2:
            if st.button("📦\nAvailable", width="stretch", key="nav_coll_available",
                        type="primary" if st.session_state.current_screen == 'available_orders' else "secondary"):
                st.session_state.current_screen = 'available_orders'
                st.rerun()
        
        with col3:
            if st.button("📋\nMy Orders", width="stretch", key="nav_coll_orders",
                        type="primary" if st.session_state.current_screen == 'collector_orders' else "secondary"):
                st.session_state.current_screen = 'collector_orders'
                st.rerun()
        
        with col4:
            if st.button("📷\nScan QR", width="stretch", key="nav_coll_scan",
                        type="primary" if st.session_state.current_screen == 'scan_qr' else "secondary"):
                st.session_state.current_screen = 'scan_qr'
                st.rerun()
        
        with col5:
            if st.button("👤\nProfile", width="stretch", key="nav_coll_profile",
                        type="primary" if st.session_state.current_screen == 'collector_profile' else "secondary"):
                st.session_state.current_screen = 'collector_profile'
                st.rerun()

# Footer
st.markdown("---")
st.caption(f"API: {API_BASE_URL} | Status: {'✅ Authenticated' if st.session_state.authenticated else '🔒 Not Authenticated'}")

