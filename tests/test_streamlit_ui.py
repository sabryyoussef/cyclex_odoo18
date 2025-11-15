"""
Playwright UI Tests for CycleX Streamlit App
Tests the Streamlit application UI and user flows
"""

import pytest
from playwright.sync_api import Page, expect
import time

# Base URL for Streamlit app
STREAMLIT_URL = "http://localhost:8501"
TIMEOUT = 10000  # 10 seconds


class TestStreamlitUI:
    """Test suite for Streamlit UI"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup before each test"""
        page.set_default_timeout(TIMEOUT)
        page.goto(STREAMLIT_URL)
        time.sleep(2)  # Wait for Streamlit to load
    
    def test_splash_screen_loads(self, page: Page):
        """Test that splash screen loads correctly"""
        # Check for CycleX title
        expect(page.locator("text=CycleX")).to_be_visible()
        expect(page.locator("text=Recycling Made Easy")).to_be_visible()
        
        # Check for Get Started button
        get_started = page.locator("button:has-text('Get Started')")
        expect(get_started).to_be_visible()
    
    def test_navigate_to_login(self, page: Page):
        """Test navigation from splash to login"""
        # Click Get Started
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        # Should be on login screen
        expect(page.locator("text=Login")).to_be_visible()
        expect(page.locator("input[placeholder*='Phone']")).to_be_visible()
        expect(page.locator("input[type='password']")).to_be_visible()
    
    def test_demo_login_customer(self, page: Page):
        """Test quick demo login as customer"""
        # Navigate to login
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        # Expand demo login section
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
        
        # Click Login as Customer
        customer_btn = page.locator("button:has-text('Login as Customer')")
        if customer_btn.is_visible():
            customer_btn.click()
            time.sleep(2)
            
            # Should be logged in and on home screen
            expect(page.locator("text=Home")).to_be_visible(timeout=5000)
    
    def test_demo_login_collector(self, page: Page):
        """Test quick demo login as collector"""
        # Navigate to login
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        # Expand demo login section
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
        
        # Click Login as Collector
        collector_btn = page.locator("button:has-text('Login as Collector')")
        if collector_btn.is_visible():
            collector_btn.click()
            time.sleep(2)
            
            # Should be logged in
            expect(page.locator("text=Collector")).to_be_visible(timeout=5000)
    
    def test_form_login(self, page: Page):
        """Test login using form with demo credentials"""
        # Navigate to login
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        # Fill login form
        phone_input = page.locator("input[placeholder*='Phone']")
        password_input = page.locator("input[type='password']")
        
        phone_input.fill("01000000000")
        password_input.fill("demo123")
        
        # Submit form
        page.click("button:has-text('Login')")
        time.sleep(2)
        
        # Should be logged in
        expect(page.locator("text=Home")).to_be_visible(timeout=5000)
    
    def test_navigation_tabs_customer(self, page: Page):
        """Test tab navigation for customer"""
        # Login first
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
            page.click("button:has-text('Login as Customer')")
            time.sleep(2)
        
        # Test tab navigation
        tabs = ["🏠", "📦", "➕", "📋", "👤"]
        for tab in tabs:
            page.click(f"button[aria-label*='{tab}']")
            time.sleep(1)
            # Verify tab is active (basic check)
            expect(page.locator(f"button[aria-label*='{tab}']")).to_be_visible()
    
    def test_categories_screen(self, page: Page):
        """Test categories screen loads"""
        # Login as customer
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
            page.click("button:has-text('Login as Customer')")
            time.sleep(2)
        
        # Navigate to categories
        page.click("button[aria-label*='📦']")
        time.sleep(1)
        
        # Should see categories
        expect(page.locator("text=Categories")).to_be_visible()
        # Check for demo data indicator or categories
        expect(page.locator("text=Demo Data").or_(page.locator("text=Plastic"))).to_be_visible(timeout=5000)
    
    def test_create_order_screen(self, page: Page):
        """Test create order screen"""
        # Login as customer
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
            page.click("button:has-text('Login as Customer')")
            time.sleep(2)
        
        # Navigate to create order
        page.click("button[aria-label*='➕']")
        time.sleep(1)
        
        # Should see create order form
        expect(page.locator("text=Create Order")).to_be_visible()
        expect(page.locator("input[type='number']").first()).to_be_visible()
    
    def test_my_orders_screen(self, page: Page):
        """Test my orders screen"""
        # Login as customer
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
            page.click("button:has-text('Login as Customer')")
            time.sleep(2)
        
        # Navigate to orders
        page.click("button[aria-label*='📋']")
        time.sleep(1)
        
        # Should see orders screen
        expect(page.locator("text=My Orders").or_(page.locator("text=Orders"))).to_be_visible()
    
    def test_profile_screen(self, page: Page):
        """Test profile screen"""
        # Login as customer
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
            page.click("button:has-text('Login as Customer')")
            time.sleep(2)
        
        # Navigate to profile
        page.click("button[aria-label*='👤']")
        time.sleep(1)
        
        # Should see profile
        expect(page.locator("text=Profile")).to_be_visible()
    
    def test_logout(self, page: Page):
        """Test logout functionality"""
        # Login first
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
            page.click("button:has-text('Login as Customer')")
            time.sleep(2)
        
        # Open sidebar (if needed) and click logout
        logout_btn = page.locator("button:has-text('Logout')")
        if logout_btn.is_visible():
            logout_btn.click()
            time.sleep(1)
            
            # Should be back at login
            expect(page.locator("text=Login")).to_be_visible()
    
    def test_signup_navigation(self, page: Page):
        """Test navigation to signup screen"""
        # Navigate to login
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        # Click sign up button
        signup_btn = page.locator("button:has-text('Sign Up')")
        if signup_btn.is_visible():
            signup_btn.click()
            time.sleep(1)
            
            # Should be on signup screen
            expect(page.locator("text=Sign Up")).to_be_visible()
            expect(page.locator("input[placeholder*='Full Name']")).to_be_visible()
    
    def test_wallet_access(self, page: Page):
        """Test wallet access from sidebar"""
        # Login as customer
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        demo_expander = page.locator("text=Demo Mode - Quick Login")
        if demo_expander.is_visible():
            demo_expander.click()
            time.sleep(0.5)
            page.click("button:has-text('Login as Customer')")
            time.sleep(2)
        
        # Click wallet button (in sidebar)
        wallet_btn = page.locator("button:has-text('Wallet')")
        if wallet_btn.is_visible():
            wallet_btn.click()
            time.sleep(1)
            
            # Should see wallet screen
            expect(page.locator("text=Wallet")).to_be_visible()


class TestStreamlitAPI:
    """Test API integration when USE_DEMO_DATA = False"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup before each test"""
        page.set_default_timeout(TIMEOUT)
        # Note: These tests require USE_DEMO_DATA = False
        page.goto(STREAMLIT_URL)
        time.sleep(2)
    
    @pytest.mark.skip(reason="Requires USE_DEMO_DATA = False and valid Odoo user")
    def test_real_api_login(self, page: Page):
        """Test login with real Odoo API"""
        page.click("button:has-text('Get Started')")
        time.sleep(1)
        
        # Fill with real credentials
        phone_input = page.locator("input[placeholder*='Phone']")
        password_input = page.locator("input[type='password']")
        
        phone_input.fill("01012345678")  # Real user phone
        password_input.fill("realpassword")  # Real password
        
        page.click("button:has-text('Login')")
        time.sleep(3)
        
        # Should login successfully
        expect(page.locator("text=Home")).to_be_visible(timeout=10000)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--headed"])

