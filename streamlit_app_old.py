"""
CycleX Mobile App Mock - Streamlit Application
Mimics the mobile app for testing API endpoints
"""

import streamlit as st
import requests
import json
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

# Configuration
API_BASE_URL = "http://localhost:8025/api/cyclex"
SESSION_COOKIE = None

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'session_cookies' not in st.session_state:
    st.session_state.session_cookies = {}
if 'language' not in st.session_state:
    st.session_state.language = 'en'

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
        
        return response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text, None
    except Exception as e:
        return None, str(e)

# Page Configuration
st.set_page_config(
    page_title="CycleX Mobile App Mock",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("♻️ CycleX App")
st.sidebar.markdown("---")

# Authentication Status
if st.session_state.authenticated:
    st.sidebar.success(f"✅ Logged in as: {st.session_state.user_data.get('name', 'User')}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.user_data = {}
        st.session_state.session_cookies = {}
        st.rerun()
else:
    st.sidebar.info("🔒 Not authenticated")

# Main Navigation
pages = {
    "🔐 Authentication": ["login", "signup", "verify_otp"],
    "🏠 Home": ["home"],
    "📦 Categories & Products": ["categories", "products"],
    "📋 Orders": ["create_order", "my_orders", "order_tracking"],
    "👤 Profile": ["profile", "update_profile"],
    "💰 Wallet": ["wallet", "transactions"],
    "🚚 Collector": ["collector_home", "collector_orders", "scan_qr"]
}

selected_page = st.sidebar.selectbox("Navigate", list(pages.keys()))

# ==================== AUTHENTICATION PAGES ====================

if selected_page == "🔐 Authentication":
    auth_tab = st.tabs(["Login", "Sign Up", "Verify OTP"])
    
    # Login Tab
    with auth_tab[0]:
        st.header("🔐 Login")
        with st.form("login_form"):
            phone = st.text_input("Phone Number", value="01000000000", help="Enter your phone number")
            password = st.text_input("Password", type="password", value="secret123", help="Enter your password")
            role = st.selectbox("Role", ["customer", "collector"], help="Select user role")
            
            submitted = st.form_submit_button("Login", type="primary")
            
            if submitted:
                with st.spinner("Logging in..."):
                    data = {"phone": phone, "password": password}
                    if role == "collector":
                        data["role"] = "collector"
                    
                    result, error = make_request("POST", "/auth/login", data=data)
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            st.session_state.authenticated = True
                            st.session_state.user_data = result.get("data", {})
                            st.success("✅ Login successful!")
                            st.rerun()
                        else:
                            st.error(f"❌ {result.get('message', 'Login failed')}")
                    else:
                        st.error("No response from server")
    
    # Sign Up Tab
    with auth_tab[1]:
        st.header("📝 Sign Up")
        with st.form("signup_form"):
            name = st.text_input("Full Name", value="Nada Al Sharqawi")
            phone = st.text_input("Phone Number", value="01000000000")
            password = st.text_input("Password", type="password", value="secret123")
            email = st.text_input("Email (Optional)", value="")
            role = st.selectbox("Role", ["customer", "collector"])
            accept_terms = st.checkbox("Accept Terms & Conditions", value=True)
            
            submitted = st.form_submit_button("Sign Up", type="primary")
            
            if submitted:
                if not accept_terms:
                    st.warning("⚠️ Please accept terms and conditions")
                else:
                    with st.spinner("Creating account..."):
                        data = {
                            "name": name,
                            "phone": phone,
                            "password": password,
                            "accept_terms": accept_terms,
                            "role": role
                        }
                        if email:
                            data["email"] = email
                        
                        result, error = make_request("POST", "/auth/register", data=data)
                        
                        if error:
                            st.error(f"Error: {error}")
                        elif result:
                            if result.get("success"):
                                st.success("✅ Account created! Please verify OTP.")
                                st.info(f"User ID: {result.get('data', {}).get('user_id', 'N/A')}")
                            else:
                                st.error(f"❌ {result.get('message', 'Sign up failed')}")
    
    # Verify OTP Tab
    with auth_tab[2]:
        st.header("✅ Verify OTP")
        with st.form("verify_otp_form"):
            phone = st.text_input("Phone Number", value="01000000000")
            otp = st.text_input("OTP Code", value="123456", help="Enter 6-digit OTP")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Verify OTP", type="primary")
            with col2:
                resend = st.form_submit_button("Resend OTP")
            
            if submitted:
                with st.spinner("Verifying OTP..."):
                    data = {"phone": phone, "verification_code": otp}
                    result, error = make_request("POST", "/auth/verify-otp", data=data)
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            st.success("✅ OTP verified! You can now login.")
                        else:
                            st.error(f"❌ {result.get('message', 'Verification failed')}")
            
            if resend:
                with st.spinner("Resending OTP..."):
                    data = {"phone": phone}
                    result, error = make_request("POST", "/auth/resend-otp", data=data)
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            st.success("✅ OTP resent!")
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to resend OTP')}")

# ==================== HOME PAGE ====================

elif selected_page == "🏠 Home":
    st.header("🏠 Home Dashboard")
    
    if not st.session_state.authenticated:
        st.warning("⚠️ Please login first")
    else:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Orders", "0")
        with col2:
            st.metric("Wallet Balance", "0.00 E£")
        with col3:
            st.metric("Total Requests", "0")
        
        st.markdown("---")
        
        # Home Summary
        if st.button("🔄 Refresh Home Data"):
            with st.spinner("Loading home data..."):
                result, error = make_request("GET", "/home/summary")
                if error:
                    st.error(f"Error: {error}")
                elif result:
                    if result.get("success"):
                        data = result.get("data", {})
                        st.json(data)
                    else:
                        st.error(f"❌ {result.get('message', 'Failed to load home data')}")

# ==================== CATEGORIES & PRODUCTS ====================

elif selected_page == "📦 Categories & Products":
    st.header("📦 Categories & Products")
    
    tab1, tab2 = st.tabs(["Categories", "Products"])
    
    with tab1:
        st.subheader("Categories List")
        lang_index = 0 if st.session_state.language == "en" else 1
        language = st.selectbox("Language", ["en", "ar"], index=lang_index, key="cat_lang")
        
        if st.button("🔄 Load Categories"):
            with st.spinner("Loading categories..."):
                result, error = make_request("GET", "/catalog/categories", params={"language": language})
                
                if error:
                    st.error(f"Error: {error}")
                elif result:
                    if result.get("success"):
                        categories = result.get("data", {}).get("categories", [])
                        st.success(f"✅ Found {len(categories)} categories")
                        
                        for cat in categories:
                            with st.expander(f"📁 {cat.get('name', 'Unknown')}"):
                                st.write(f"**ID:** {cat.get('id')}")
                                st.write(f"**Description:** {cat.get('description', 'N/A')}")
                                st.write(f"**Has Children:** {cat.get('has_children', False)}")
                                st.write(f"**Product Count:** {cat.get('product_count', 0)}")
                    else:
                        st.error(f"❌ {result.get('message', 'Failed to load categories')}")
    
    with tab2:
        st.subheader("Products by Category")
        category_name = st.selectbox("Category", ["PLASTIC", "PAPER", "METAL", "GLASS", "ELECTRONICS"])
        lang_index = 0 if st.session_state.language == "en" else 1
        language = st.selectbox("Language", ["en", "ar"], index=lang_index, key="prod_lang")
        
        if st.button("🔄 Load Products"):
            with st.spinner("Loading products..."):
                result, error = make_request("GET", f"/catalog/categories/{category_name}/items", params={"language": language})
                
                if error:
                    st.error(f"Error: {error}")
                elif result:
                    if result.get("success"):
                        products = result.get("data", {}).get("products", [])
                        st.success(f"✅ Found {len(products)} products")
                        
                        for product in products:
                            col1, col2 = st.columns([3, 1])
                            with col1:
                                st.write(f"**{product.get('name', 'Unknown')}**")
                                st.write(product.get('description', 'No description'))
                                st.write(f"Category: {product.get('category_name', 'N/A')}")
                            with col2:
                                st.metric("Price", f"{product.get('price_per_kg', 0)} {product.get('currency_symbol', '$')}/kg")
                    else:
                        st.error(f"❌ {result.get('message', 'Failed to load products')}")

# ==================== ORDERS ====================

elif selected_page == "📋 Orders":
    if not st.session_state.authenticated:
        st.warning("⚠️ Please login first")
    else:
        order_tab = st.tabs(["Create Order", "My Orders", "Order Tracking"])
        
        # Create Order
        with order_tab[0]:
            st.subheader("📝 Create New Order")
            with st.form("create_order_form"):
                category_id = st.number_input("Category ID", min_value=1, value=8)
                product_id = st.number_input("Product ID (0 for custom)", min_value=0, value=0)
                quantity = st.number_input("Quantity", min_value=1, value=1)
                weight = st.number_input("Weight (kg)", min_value=0.0, value=1.5, step=0.1)
                pickup_date = st.date_input("Pickup Date", value=datetime.now().date())
                item_name = st.text_input("Item Name (for custom items)", value="Mixed plastic bottles")
                notes = st.text_area("Notes (Optional)", value="")
                
                # Photo upload
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
        
        # My Orders
        with order_tab[1]:
            st.subheader("📋 My Orders")
            status_filter = st.selectbox("Filter by Status", ["all", "active", "pending", "assigned", "completed"])
            
            if st.button("🔄 Load Orders"):
                with st.spinner("Loading orders..."):
                    params = {} if status_filter == "all" else {"status": status_filter}
                    result, error = make_request("GET", "/orders", params=params)
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            orders = result.get("data", {}).get("requests", [])
                            st.success(f"✅ Found {len(orders)} orders")
                            
                            for order in orders:
                                with st.expander(f"Order #{order.get('id', 'N/A')} - {order.get('status', 'Unknown')}"):
                                    st.write(f"**Status:** {order.get('status', 'N/A')}")
                                    st.write(f"**Total Amount:** {order.get('total_amount', 0)} {order.get('currency_symbol', '$')}")
                                    st.write(f"**Pickup Date:** {order.get('pickup_date', 'N/A')}")
                                    st.write(f"**Created:** {order.get('created_at', 'N/A')}")
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to load orders')}")
        
        # Order Tracking
        with order_tab[2]:
            st.subheader("📍 Order Tracking")
            order_id = st.number_input("Order ID", min_value=1, value=1)
            
            if st.button("🔍 Track Order"):
                with st.spinner("Loading order details..."):
                    result, error = make_request("GET", f"/orders/{order_id}")
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            order = result.get("data", {})
                            st.success("✅ Order details loaded")
                            st.json(order)
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to load order')}")

# ==================== PROFILE ====================

elif selected_page == "👤 Profile":
    if not st.session_state.authenticated:
        st.warning("⚠️ Please login first")
    else:
        profile_tab = st.tabs(["View Profile", "Update Profile"])
        
        # View Profile
        with profile_tab[0]:
            st.subheader("👤 My Profile")
            if st.button("🔄 Load Profile"):
                with st.spinner("Loading profile..."):
                    result, error = make_request("GET", "/user/profile")
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            profile = result.get("data", {})
                            st.success("✅ Profile loaded")
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Name:** {profile.get('name', 'N/A')}")
                                st.write(f"**Phone:** {profile.get('phone', 'N/A')}")
                                st.write(f"**Email:** {profile.get('email', 'N/A')}")
                            with col2:
                                st.write(f"**User Type:** {profile.get('user_type', 'N/A')}")
                                st.write(f"**Language:** {profile.get('language', 'N/A')}")
                                st.write(f"**Status:** {profile.get('account_status', 'N/A')}")
                            
                            st.json(profile)
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to load profile')}")
        
        # Update Profile
        with profile_tab[1]:
            st.subheader("✏️ Update Profile")
            with st.form("update_profile_form"):
                name = st.text_input("Name", value=st.session_state.user_data.get('name', ''))
                phone = st.text_input("Phone", value=st.session_state.user_data.get('phone', ''))
                email = st.text_input("Email", value=st.session_state.user_data.get('email', ''))
                lang_index = 0 if st.session_state.language == "en" else 1
                language = st.selectbox("Language", ["en", "ar"], index=lang_index)
                
                submitted = st.form_submit_button("Update Profile", type="primary")
                
                if submitted:
                    with st.spinner("Updating profile..."):
                        data = {
                            "name": name,
                            "phone": phone,
                            "email": email,
                            "language": language
                        }
                        
                        result, error = make_request("PUT", "/user/profile", data=data)
                        
                        if error:
                            st.error(f"Error: {error}")
                        elif result:
                            if result.get("success"):
                                st.success("✅ Profile updated successfully!")
                                st.session_state.user_data.update(data)
                            else:
                                st.error(f"❌ {result.get('message', 'Failed to update profile')}")

# ==================== WALLET ====================

elif selected_page == "💰 Wallet":
    if not st.session_state.authenticated:
        st.warning("⚠️ Please login first")
    else:
        wallet_tab = st.tabs(["Balance", "Transactions"])
        
        # Wallet Balance
        with wallet_tab[0]:
            st.subheader("💰 Wallet Balance")
            if st.button("🔄 Load Balance"):
                with st.spinner("Loading wallet balance..."):
                    result, error = make_request("GET", "/wallet")
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            wallet = result.get("data", {})
                            st.success("✅ Wallet data loaded")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Balance", f"{wallet.get('balance', 0)} E£")
                            with col2:
                                st.metric("Total Earned", f"{wallet.get('total_earned', 0)} E£")
                            with col3:
                                st.metric("Total Withdrawn", f"{wallet.get('total_withdrawn', 0)} E£")
                            
                            st.json(wallet)
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to load wallet')}")
        
        # Transactions
        with wallet_tab[1]:
            st.subheader("📊 Transactions")
            if st.button("🔄 Load Transactions"):
                with st.spinner("Loading transactions..."):
                    result, error = make_request("GET", "/wallet/transactions")
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            transactions = result.get("data", {}).get("transactions", [])
                            st.success(f"✅ Found {len(transactions)} transactions")
                            
                            for txn in transactions:
                                with st.expander(f"{txn.get('type', 'Unknown')} - {txn.get('amount', 0)} E£"):
                                    st.write(f"**Date:** {txn.get('date', 'N/A')}")
                                    st.write(f"**Type:** {txn.get('type', 'N/A')}")
                                    st.write(f"**Amount:** {txn.get('amount', 0)} E£")
                                    st.write(f"**Description:** {txn.get('description', 'N/A')}")
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to load transactions')}")

# ==================== COLLECTOR ====================

elif selected_page == "🚚 Collector":
    if not st.session_state.authenticated:
        st.warning("⚠️ Please login first")
    else:
        collector_tab = st.tabs(["Home", "Available Orders", "Scan QR"])
        
        # Collector Home
        with collector_tab[0]:
            st.subheader("🚚 Collector Dashboard")
            if st.button("🔄 Load Dashboard"):
                with st.spinner("Loading dashboard..."):
                    result, error = make_request("GET", "/collector/home")
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            dashboard = result.get("data", {})
                            st.success("✅ Dashboard loaded")
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Available Orders", dashboard.get('available_orders_count', 0))
                            with col2:
                                st.metric("Assigned Orders", dashboard.get('assigned_orders_count', 0))
                            with col3:
                                st.metric("Total Earnings", f"{dashboard.get('total_earnings', 0)} E£")
                            
                            st.json(dashboard)
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to load dashboard')}")
        
        # Available Orders
        with collector_tab[1]:
            st.subheader("📦 Available Orders")
            if st.button("🔄 Load Available Orders"):
                with st.spinner("Loading available orders..."):
                    result, error = make_request("GET", "/collector/orders")
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            orders = result.get("data", {}).get("orders", [])
                            st.success(f"✅ Found {len(orders)} available orders")
                            
                            for order in orders:
                                col1, col2, col3 = st.columns([3, 1, 1])
                                with col1:
                                    st.write(f"**Order #{order.get('id', 'N/A')}**")
                                    st.write(f"Distance: {order.get('distance', 'N/A')} km")
                                    st.write(f"Amount: {order.get('total_amount', 0)} E£")
                                with col2:
                                    if st.button(f"Accept", key=f"accept_{order.get('id')}"):
                                        with st.spinner("Accepting order..."):
                                            result2, error2 = make_request("POST", f"/collector/orders/{order.get('id')}/accept")
                                            if result2 and result2.get("success"):
                                                st.success("✅ Order accepted!")
                                                st.rerun()
                                with col3:
                                    if st.button(f"Reject", key=f"reject_{order.get('id')}"):
                                        with st.spinner("Rejecting order..."):
                                            result2, error2 = make_request("POST", f"/collector/orders/{order.get('id')}/reject", data={"reason": "Not available"})
                                            if result2 and result2.get("success"):
                                                st.success("✅ Order rejected!")
                                                st.rerun()
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to load orders')}")
        
        # Scan QR
        with collector_tab[2]:
            st.subheader("📷 Scan QR Code")
            qr_code = st.text_input("QR Code", value="ORDER_12345_ABC", help="Enter or scan QR code")
            
            if st.button("🔍 Process QR Code"):
                with st.spinner("Processing QR code..."):
                    data = {"qr_code": qr_code}
                    result, error = make_request("POST", "/collector/orders/scan-qr", data=data)
                    
                    if error:
                        st.error(f"Error: {error}")
                    elif result:
                        if result.get("success"):
                            st.success("✅ QR code processed!")
                            st.json(result.get("data", {}))
                        else:
                            st.error(f"❌ {result.get('message', 'Failed to process QR code')}")

# Footer
st.markdown("---")
st.markdown("**CycleX Mobile App Mock** - Testing Interface")
st.caption(f"API Base URL: {API_BASE_URL}")

