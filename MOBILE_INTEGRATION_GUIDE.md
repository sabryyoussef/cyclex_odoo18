# Mobile Integration Guide for CycleX 📱

**Date:** October 17, 2025  
**For:** Mobile Development Team (Flutter)  
**Backend:** Odoo 18 REST API  

---

## 🎯 Purpose

This document separates **Odoo backend work** (your responsibility) from **Mobile app development** (Flutter team responsibility). It clearly defines integration points and what you need from the mobile team.

---

## 🔄 Separation of Concerns

### Your Work (Odoo Backend Developer) ✅ COMPLETE
- ✅ REST APIs (22 endpoints)
- ✅ Authentication & authorization
- ✅ Database models & business logic
- ✅ QR code generation (backend)
- ✅ Validation & security
- ✅ Scheduled actions (cron jobs)
- ✅ Admin dashboard & backend UI

### Mobile Team's Work (Flutter Developer) 🔵 SEPARATE
- Flutter mobile apps (iOS & Android)
- QR code scanning (mobile camera)
- Firebase Cloud Messaging (FCM) setup
- Push notification handling
- Photo capture & upload
- GPS location capture
- UI/UX design & implementation

---

## 📋 What You Need FROM Mobile Team

### 1. Firebase Configuration Files 🔴 REQUIRED

**What They'll Provide:**

#### For Android:
```
google-services.json
```
- Location: They'll download from Firebase Console
- Usage: You'll need the **Server Key** from this file
- Found in: Firebase Console → Project Settings → Cloud Messaging → Server Key

#### For iOS:
```
GoogleService-Info.plist
```
- Location: They'll download from Firebase Console
- Usage: You'll need the same **Server Key** (shared between iOS/Android)

**What You'll Do With It (Phase 7):**
```python
# In Odoo system parameters (Phase 7)
'firebase.server_key': 'AAAA...xyz123'  # From their Firebase project
```

---

### 2. Firebase Project Details 🔴 REQUIRED

**What You Need:**
```
Firebase Project ID: ______________ (they create this)
Firebase Server Key: ______________ (you'll use in Phase 7)
```

**When:** Before Phase 7 (External Integrations)

---

### 3. SMS Misr Account (Optional) ⚠️ COORDINATION NEEDED

**Who Creates:** Either you or project manager  
**What Mobile Team Needs:** Nothing (backend handles SMS)  
**What You Need:**
```
SMS Misr Username: ______________
SMS Misr Password: ______________
SMS Misr Sender Name: ______________
```

**When:** Before Phase 7

---

### 4. Testing Devices/Accounts 🔵 NICE TO HAVE

**For Testing Push Notifications:**
- Android device FCM token (they'll provide after app install)
- iOS device FCM token (they'll provide after app install)

**Format:**
```
Android FCM Token: dXYz...abc123 (long string ~150+ chars)
iOS FCM Token: eFgH...def456 (long string ~150+ chars)
```

**When:** During Phase 7 testing

---

## 📱 How Mobile Team Will Implement (Flutter)

> **Note:** This is **their work**, not yours. This section is for your understanding only.

### 1. Flutter Project Setup

**What They'll Do:**
```bash
# Create Flutter project
flutter create cyclex_app

# Add dependencies to pubspec.yaml
dependencies:
  http: ^1.1.0  # For API calls
  firebase_core: ^2.24.0  # Firebase SDK
  firebase_messaging: ^14.7.0  # Push notifications
  qr_code_scanner: ^1.0.1  # QR scanning
  image_picker: ^1.0.5  # Photo capture
  geolocator: ^10.1.0  # GPS location
  shared_preferences: ^2.2.2  # Local storage (auth tokens)
```

**Timeline:** Week 1 of mobile development

---

### 2. Firebase Setup (Mobile Team)

**Step 1: Create Firebase Project**
```
1. Go to console.firebase.google.com
2. Create new project: "CycleX"
3. Enable Cloud Messaging
```

**Step 2: Add Android App**
```
1. Click "Add app" → Android
2. Package name: com.cyclex.app (example)
3. Download google-services.json
4. Place in: android/app/google-services.json
```

**Step 3: Add iOS App**
```
1. Click "Add app" → iOS
2. Bundle ID: com.cyclex.app (example)
3. Download GoogleService-Info.plist
4. Place in: ios/Runner/GoogleService-Info.plist
```

**Step 4: Get Server Key (FOR YOU)**
```
Firebase Console → Project Settings → Cloud Messaging → Server Key
Copy this key → Send to you for Phase 7
```

**What You'll Receive:**
```
Server Key: AAAAxxxxxxx:APAxxxxx... (180+ characters)
```

---

### 3. API Integration (Mobile Team)

**What They'll Do:**

#### A. Create API Service Class
```dart
// lib/services/api_service.dart
class CyclexAPI {
  static const String baseUrl = 'http://your-server:10018';
  
  // Store auth token after login
  String? authToken;
  
  Future<Map<String, dynamic>> login(String phone, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/cyclex/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'jsonrpc': '2.0',
        'params': {
          'phone': phone,
          'password': password,
          'fcm_token': await getFCMToken(),
        }
      }),
    );
    
    final data = jsonDecode(response.body);
    if (data['result']['success']) {
      authToken = data['result']['data']['auth_token'];
      // Save token locally
    }
    return data['result'];
  }
  
  // Similar methods for all 22 endpoints...
}
```

**What You Provide (Already Done):**
- ✅ Complete API documentation (`API_DOCUMENTATION.md`)
- ✅ All 22 endpoints working
- ✅ JSON-RPC format
- ✅ Clear error codes

---

### 4. QR Code Implementation (Mobile Team)

#### A. Display QR Code (Customer App)
```dart
// When customer views their request
Widget buildQRCode(String base64Image) {
  return Image.memory(
    base64Decode(base64Image),
    width: 250,
    height: 250,
  );
}
```

**What You Provide:**
- ✅ QR code image as base64 in API response
- ✅ `/api/cyclex/request/create` returns QR
- ✅ `/api/cyclex/request/details/<id>` returns QR

#### B. Scan QR Code (Collector App)
```dart
// lib/screens/collector/qr_scanner.dart
import 'package:qr_code_scanner/qr_code_scanner.dart';

class QRScanner extends StatelessWidget {
  final QRViewController controller;
  
  void onQRScanned(String qrCode) async {
    // Send UUID to your API
    final result = await api.scanQR(qrCode);
    
    if (result['success']) {
      // Show order details
      showOrderDetails(result['data']);
    } else {
      // Show error
      showError(result['message']);
    }
  }
}
```

**What You Provide:**
- ✅ `/api/cyclex/collector/scan-qr` endpoint
- ✅ Validates QR code UUID
- ✅ Returns order details if valid

---

### 5. Push Notifications (Mobile Team + You in Phase 7)

#### Mobile Team Does:

**A. Initialize Firebase in App**
```dart
// lib/main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  
  // Request permission
  await FirebaseMessaging.instance.requestPermission();
  
  // Get FCM token
  String? fcmToken = await FirebaseMessaging.instance.getToken();
  
  // Send to backend during login/register
  api.login(phone, password, fcmToken: fcmToken);
  
  runApp(CyclexApp());
}
```

**B. Handle Incoming Notifications**
```dart
FirebaseMessaging.onMessage.listen((RemoteMessage message) {
  // Show notification to user
  showNotification(
    title: message.notification?.title,
    body: message.notification?.body,
  );
});

FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
  // Navigate to relevant screen
  navigateToOrder(message.data['order_id']);
});
```

#### You Do (Phase 7):

**A. Install Python Library**
```bash
pip install firebase-admin
```

**B. Create Notification Service**
```python
# models/cyclex_notification.py
import firebase_admin
from firebase_admin import credentials, messaging

class CyclexNotification(models.Model):
    _name = 'cyclex.notification'
    
    def send_push_notification(self, fcm_token, title, body, data=None):
        """Send push notification via Firebase"""
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=fcm_token,
        )
        
        response = messaging.send(message)
        return response
```

**C. Integrate in Business Logic**
```python
# In cyclex_request.py
def action_assign_collector(self):
    # ... existing code ...
    
    # Send notification to collector
    if self.collector_id.fcm_token:
        self.env['cyclex.notification'].send_push_notification(
            fcm_token=self.collector_id.fcm_token,
            title=_('New Order Assigned'),
            body=_('You have been assigned order %s') % self.name,
            data={'order_id': str(self.id), 'type': 'order_assigned'}
        )
```

---

### 6. Photo Upload (Mobile Team)

**What They'll Do:**

```dart
// Capture or pick image
import 'package:image_picker/image_picker.dart';

Future<String> capturePhoto() async {
  final ImagePicker picker = ImagePicker();
  final XFile? image = await picker.pickImage(
    source: ImageSource.camera,  // or ImageSource.gallery
    maxWidth: 1920,
    maxHeight: 1080,
    imageQuality: 85,  // Compress to reduce size
  );
  
  if (image != null) {
    // Convert to base64
    final bytes = await image.readAsBytes();
    String base64Image = base64Encode(bytes);
    
    // Validate size (should be < 5MB)
    if (bytes.length > 5 * 1024 * 1024) {
      throw Exception('Image too large');
    }
    
    return base64Image;
  }
  return '';
}

// Send to API
api.createRequest(
  photo1: await capturePhoto(),
  photo2: await capturePhoto(),
  // ... other params
);
```

**What You Provide:**
- ✅ Image size validation (5MB limit)
- ✅ Accepts base64 encoded images
- ✅ Returns clear error if too large

---

### 7. GPS Location (Mobile Team)

**What They'll Do:**

```dart
import 'package:geolocator/geolocator.dart';

Future<Position> getCurrentLocation() async {
  // Check permission
  LocationPermission permission = await Geolocator.checkPermission();
  if (permission == LocationPermission.denied) {
    permission = await Geolocator.requestPermission();
  }
  
  // Get position
  Position position = await Geolocator.getCurrentPosition(
    desiredAccuracy: LocationAccuracy.high,
  );
  
  return position;
}

// Send to backend
final location = await getCurrentLocation();
api.createRequest(
  gpsLatitude: location.latitude,
  gpsLongitude: location.longitude,
  // ... other params
);
```

**What You Provide:**
- ✅ Accepts `gps_latitude` and `gps_longitude` in APIs
- ✅ Stores in user profile and requests
- ✅ Updates automatically

---

## 📊 Integration Matrix

| Feature | Odoo Backend (You) | Mobile App (Flutter Team) |
|---------|-------------------|---------------------------|
| **Authentication** | ✅ API endpoints | 🔵 Login UI, token storage |
| **QR Code Generation** | ✅ Generate & provide image | 🔵 Display QR code |
| **QR Code Scanning** | ✅ Validate UUID | 🔵 Camera scanner |
| **Push Notifications** | 🔜 Phase 7: Send via FCM | 🔵 Receive & display |
| **Photo Upload** | ✅ Accept & validate | 🔵 Capture & compress |
| **GPS Location** | ✅ Store & use | 🔵 Capture coordinates |
| **SMS Verification** | 🔜 Phase 7: Send SMS | 🔵 Input code UI |
| **API Calls** | ✅ All endpoints ready | 🔵 HTTP client implementation |
| **Data Validation** | ✅ Backend validation | 🔵 Frontend validation (optional) |
| **Error Handling** | ✅ Clear error codes | 🔵 User-friendly messages |

---

## 🎯 What You Need FROM Mobile Team

### 1. Firebase Server Key 🔴 CRITICAL (Phase 7)

**When:** Before starting Phase 7 (External Integrations)  
**Format:**
```
Server Key: AAAAxxxxxxxxxxxxxxx:APAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**How They Get It:**
1. They create Firebase project
2. Firebase Console → Project Settings → Cloud Messaging
3. Copy "Server Key" 
4. Send to you

**What You Do:**
```python
# In Odoo Settings → Technical → Parameters → System Parameters
Key: firebase.server_key
Value: (paste the key they provide)
```

---

### 2. App Package Names 🔴 CRITICAL

**What:**
```
Android Package Name: com.cyclex.app (example)
iOS Bundle ID: com.cyclex.app (example)
```

**Why You Need This:**
- For Firebase FCM targeting
- For notification routing
- For security configuration

**When:** Before Phase 7

---

### 3. Test Device FCM Tokens 🟡 IMPORTANT (Testing)

**What:**
After they install the app on test devices:
```
Android Test Token: dXYz1234abcd... (~150+ characters)
iOS Test Token: eFgH5678wxyz... (~150+ characters)
```

**Why:**
- Test push notifications before production
- Verify FCM integration works
- Debug notification delivery

**How They Get It:**
```dart
String? token = await FirebaseMessaging.instance.getToken();
print('FCM Token: $token');
// They copy and send to you
```

---

### 4. API Server URL Confirmation 🟢 LOW PRIORITY

**What:**
```
Development: http://YOUR_IP:10018
Staging: https://staging.cyclex.app
Production: https://api.cyclex.app
```

**Why:**
- They hardcode this in their app
- Or use environment configuration
- Needs to match your server

---

## 🚀 Mobile Team's Implementation Guide

> **Note:** This is for your understanding of what they'll do. This is NOT your work.

### Flutter App Structure

```
cyclex_app/
├── lib/
│   ├── main.dart                    # App entry point
│   ├── services/
│   │   ├── api_service.dart         # All 22 API endpoints
│   │   ├── auth_service.dart        # Authentication logic
│   │   ├── notification_service.dart # FCM handling
│   │   └── storage_service.dart     # Local data storage
│   ├── models/
│   │   ├── user.dart
│   │   ├── request.dart
│   │   ├── product.dart
│   │   └── category.dart
│   ├── screens/
│   │   ├── auth/
│   │   │   ├── login_screen.dart
│   │   │   ├── register_screen.dart
│   │   │   └── verify_phone_screen.dart
│   │   ├── customer/
│   │   │   ├── home_screen.dart
│   │   │   ├── create_request_screen.dart
│   │   │   ├── my_requests_screen.dart
│   │   │   └── wallet_screen.dart
│   │   └── collector/
│   │       ├── available_orders_screen.dart
│   │       ├── qr_scanner_screen.dart
│   │       ├── my_orders_screen.dart
│   │       └── commission_screen.dart
│   └── widgets/
│       ├── qr_display.dart
│       └── custom_buttons.dart
├── android/
│   └── app/
│       └── google-services.json     # Firebase config (Android)
├── ios/
│   └── Runner/
│       └── GoogleService-Info.plist # Firebase config (iOS)
└── pubspec.yaml                     # Dependencies
```

---

### Authentication Flow (Flutter)

```dart
// lib/services/auth_service.dart
class AuthService {
  final ApiService api = ApiService();
  
  // 1. Login
  Future<bool> login(String phone, String password) async {
    final fcmToken = await FirebaseMessaging.instance.getToken();
    
    final result = await api.post('/api/cyclex/login', {
      'phone': phone,
      'password': password,
      'fcm_token': fcmToken,
    });
    
    if (result['success']) {
      // Save token locally
      await saveAuthToken(result['data']['auth_token']);
      return true;
    }
    return false;
  }
  
  // 2. Register
  Future<Map<String, dynamic>> register({
    required String name,
    required String phone,
    required String password,
    required String confirmPassword,
  }) async {
    final fcmToken = await FirebaseMessaging.instance.getToken();
    
    return await api.post('/api/cyclex/register', {
      'name': name,
      'phone': phone,
      'password': password,
      'confirm_password': confirmPassword,
      'fcm_token': fcmToken,
      'language': 'ar',  // or 'en'
    });
  }
  
  // 3. Verify Phone
  Future<bool> verifyPhone(String phone, String code) async {
    final result = await api.post('/api/cyclex/verify', {
      'phone': phone,
      'verification_code': code,
    });
    
    if (result['success']) {
      await saveAuthToken(result['data']['auth_token']);
      return true;
    }
    return false;
  }
}
```

**Your Part:**
- ✅ All endpoints already implemented
- ✅ Returns proper auth tokens
- ✅ Validates verification codes

---

### Request Creation (Flutter)

```dart
// lib/screens/customer/create_request_screen.dart
class CreateRequestScreen extends StatefulWidget {
  Future<void> createRequest() async {
    // Capture photos
    final photo1 = await ImagePicker().pickImage(source: ImageSource.camera);
    final photo1Base64 = base64Encode(await photo1!.readAsBytes());
    
    // Get GPS location
    final position = await Geolocator.getCurrentPosition();
    
    // Call your API
    final result = await api.post('/api/cyclex/request/create', {
      'category_id': selectedCategory.id,
      'product_id': selectedProduct.id,
      'quantity': quantityController.text,
      'weight': weightController.text,
      'pickup_date': pickupDate.toString(),
      'photo_1': photo1Base64,
      'gps_latitude': position.latitude,
      'gps_longitude': position.longitude,
    });
    
    if (result['success']) {
      // Show success & QR code
      final qrImage = result['data']['qr_code_image'];
      showQRCode(qrImage);
    }
  }
}
```

**Your Part:**
- ✅ Validates all inputs
- ✅ Checks image size (5MB limit)
- ✅ Generates QR code automatically
- ✅ Returns all data including QR image

---

### QR Code Scanner (Flutter)

```dart
// lib/screens/collector/qr_scanner_screen.dart
import 'package:qr_code_scanner/qr_code_scanner.dart';

class QRScannerScreen extends StatefulWidget {
  void onQRViewCreated(QRViewController controller) {
    controller.scannedDataStream.listen((scanData) async {
      // Got QR code UUID
      final uuid = scanData.code;
      
      // Validate with your backend
      final result = await api.post('/api/cyclex/collector/scan-qr', {
        'qr_code': uuid,
      });
      
      if (result['success']) {
        // Valid QR code - show order details
        navigateToOrderDetails(result['data']);
      } else {
        // Invalid QR or not assigned to this collector
        showError(result['message']);
      }
    });
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: QRView(
        key: qrKey,
        onQRViewCreated: onQRViewCreated,
      ),
    );
  }
}
```

**Your Part:**
- ✅ `/api/cyclex/collector/scan-qr` validates UUID
- ✅ Checks collector assignment
- ✅ Returns error codes for invalid scans

---

### Firebase Notification Handling (Flutter)

```dart
// lib/services/notification_service.dart
class NotificationService {
  
  Future<void> initialize() async {
    // Request permission (iOS)
    await FirebaseMessaging.instance.requestPermission(
      alert: true,
      badge: true,
      sound: true,
    );
    
    // Get FCM token
    String? token = await FirebaseMessaging.instance.getToken();
    
    // Send to backend (during login)
    await api.updateProfile(fcm_token: token);
    
    // Handle foreground notifications
    FirebaseMessaging.onMessage.listen((RemoteMessage message) {
      _showLocalNotification(message);
    });
    
    // Handle notification taps
    FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
      _handleNotificationTap(message);
    });
  }
  
  void _handleNotificationTap(RemoteMessage message) {
    // Navigate based on notification type
    switch (message.data['type']) {
      case 'order_assigned':
        navigateToOrder(message.data['order_id']);
        break;
      case 'order_completed':
        navigateToWallet();
        break;
      case 'withdrawal_approved':
        navigateToWithdrawals();
        break;
    }
  }
}
```

**Your Part (Phase 7):**
```python
# Send notification when order is assigned
notification_data = {
    'type': 'order_assigned',
    'order_id': str(self.id),
    'title': 'New Order Assigned',
    'body': f'Order {self.name} has been assigned to you',
}
self.env['cyclex.notification'].send_push_notification(
    fcm_token=self.collector_id.fcm_token,
    **notification_data
)
```

---

## 📋 Integration Checklist

### Before Phase 7 (What You Need)

- [ ] Firebase Server Key from mobile team
- [ ] Android package name confirmed
- [ ] iOS bundle ID confirmed
- [ ] SMS Misr account credentials obtained
- [ ] Test device FCM tokens (for testing)

### Phase 7 Implementation (Your Work)

- [ ] Install `firebase-admin` library
- [ ] Create `cyclex.notification` model
- [ ] Implement `send_push_notification()` method
- [ ] Store Firebase Server Key in system parameters
- [ ] Integrate notifications in business logic:
  - [ ] Order assigned → notify collector
  - [ ] Order completed → notify customer
  - [ ] Withdrawal approved/rejected → notify customer
  - [ ] Collector registration approved → notify collector
- [ ] Install SMS Misr integration
- [ ] Send verification codes via SMS
- [ ] Test with mobile team's devices

### Mobile Team's Timeline

**Week 1-2:**
- Flutter project setup
- Firebase integration
- Basic UI screens

**Week 3-4:**
- API integration (all 22 endpoints)
- Authentication flow
- Request creation flow

**Week 5-6:**
- Collector features
- QR code scanning
- Wallet/commission screens

**Week 7-8:**
- Push notifications (needs Phase 7 complete)
- Polish & testing
- Bug fixes

---

## 🔐 Security Considerations

### Mobile Team Responsibilities

1. **Secure Token Storage**
```dart
// Use secure storage for auth tokens
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final storage = FlutterSecureStorage();
await storage.write(key: 'auth_token', value: token);
```

2. **HTTPS Only**
```dart
// Force HTTPS in production
const String baseUrl = 'https://api.cyclex.app';  // NOT http://
```

3. **Input Validation**
```dart
// Validate before sending to backend
if (!isValidPhone(phone)) {
  return 'Invalid phone number';
}
```

### Your Responsibilities (Backend)

- ✅ Server-side validation (already implemented)
- ✅ SQL injection prevention (Odoo ORM)
- ✅ XSS prevention
- ✅ Rate limiting (future enhancement)
- ✅ Token expiry (future enhancement)

---

## 📞 Communication Protocol

### When Mobile Team Contacts You

**Expected Questions:**
1. ❓ "What's the API endpoint for X?"
   - ✅ Answer: Check `API_DOCUMENTATION.md`

2. ❓ "Why am I getting error code X?"
   - ✅ Answer: Check error code documentation

3. ❓ "Can you test endpoint X with this data?"
   - ✅ Answer: Use Postman or curl to test

4. ❓ "Push notifications not working"
   - ⏳ Answer: "Send me your FCM token, I'll test from backend"

5. ❓ "What's the format for date/time fields?"
   - ✅ Answer: ISO 8601 format (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)

### When You Contact Mobile Team

**What You'll Ask:**
1. 🔴 "Please send me the Firebase Server Key" (Phase 7)
2. 🔴 "Please confirm app package names" (Phase 7)
3. 🟡 "Please send test device FCM tokens" (Phase 7 testing)
4. 🟢 "Please test this new endpoint: /api/..." (Anytime)

---

## 📱 API Usage Examples (For Mobile Team)

### Example 1: Customer Registration & Login

```dart
// 1. Register
final registerResult = await api.register(
  name: 'Ahmed Mohamed',
  phone: '+201234567890',
  password: 'MySecure123',
  confirmPassword: 'MySecure123',
);

// Response: { success: true, data: { user_id: 123 } }

// 2. Verify (after SMS received)
final verifyResult = await api.verifyPhone(
  phone: '+201234567890',
  code: '123456',  // Code from SMS
);

// Response: { success: true, data: { auth_token: 'abc...' } }

// 3. Save token and use for future requests
await storage.write(key: 'auth_token', value: verifyResult['data']['auth_token']);
```

### Example 2: Create Recycling Request

```dart
// With authentication token in headers
final result = await api.createRequest(
  categoryId: 2,  // Plastic
  productId: 5,   // Plastic Bottles
  quantity: 10,
  weight: 5.5,
  pickupDate: '2025-10-20',
  photo1: base64Photo1,
  photo2: base64Photo2,
  gpsLatitude: 30.0444,
  gpsLongitude: 31.2357,
);

// Response includes QR code
if (result['success']) {
  final qrCode = result['data']['qr_code'];
  final qrImage = result['data']['qr_code_image'];
  // Display QR code for customer
}
```

### Example 3: Collector Scans QR

```dart
// After scanning QR code with camera
final scannedUUID = '550e8400-e29b-41d4-a716-446655440000';

final result = await api.scanQR(qrCode: scannedUUID);

if (result['success']) {
  // Valid QR - show order details
  final orderDetails = result['data'];
  showDialog(
    context: context,
    builder: (context) => OrderDetailsDialog(
      requestNumber: orderDetails['request_number'],
      customerName: orderDetails['customer_name'],
      productName: orderDetails['product_name'],
      price: orderDetails['calculated_price'],
    ),
  );
} else {
  // Invalid QR or not assigned to this collector
  showError(result['message']);
}
```

---

## 🧪 Testing Workflow

### Phase 1: API Testing (Current - You)
- ✅ Use Postman to test all endpoints
- ✅ Verify responses match documentation
- ✅ Test error scenarios

### Phase 2: Mobile Integration (Mobile Team)
- 🔵 Implement API client in Flutter
- 🔵 Test each endpoint from mobile app
- 🔵 Handle all error codes
- 🔵 Report any API issues to you

### Phase 3: End-to-End Testing (Both)
- 🔵 Mobile team creates test users
- ✅ You monitor backend logs
- 🔵 Mobile team tests complete workflows
- ✅ You fix any backend issues
- 🔵 Mobile team fixes any UI issues

### Phase 4: Firebase Testing (After Phase 7)
- 🔵 Mobile team provides test FCM tokens
- ✅ You send test push notifications
- 🔵 Mobile team confirms receipt
- ✅ You integrate into business logic
- 🔵 Mobile team tests auto-notifications

---

## 📊 Dependency Timeline

```
Week 1-2: ✅ Odoo Backend (Phase 1-5) COMPLETE
          ↓
Week 3-4: 🔵 Mobile team can start (Phase 8 in parallel)
          ↓
Week 5-6: 📋 Phase 6: Testing & Documentation (You)
          🔵 Mobile team continues (APIs working)
          ↓
Week 7-8: 🔌 Phase 7: Firebase + SMS integration (You)
          🔵 Mobile team integrates push notifications
          ↓
Week 9: 🧪 Integration testing (Both teams)
        ↓
Week 10: 🚀 Deployment & Launch
```

---

## 🎯 Current Status

### What's Ready NOW for Mobile Team ✅

1. ✅ **All 22 REST API endpoints** working
2. ✅ **Complete API documentation** (`API_DOCUMENTATION.md`)
3. ✅ **QR code generation** (backend provides image)
4. ✅ **Authentication system** (login, register, verify)
5. ✅ **Business logic** (wallets, commissions, orders)
6. ✅ **Validation** (phone, password, images)
7. ✅ **Sample data** (categories, products)
8. ✅ **Backend running** on http://localhost:10018

### What's NOT Ready (Phase 7) ⏳

1. ⏳ **Firebase FCM integration** (needs Firebase project from mobile team)
2. ⏳ **SMS Misr integration** (needs SMS account credentials)
3. ⏳ **Push notifications** (depends on Firebase setup)
4. ⏳ **SMS verification** (depends on SMS Misr setup)

**But:** Mobile team can start without these! They can:
- Use mock notifications
- Use manual verification codes (you can set in backend)
- Build entire app except push notifications

---

## 📝 Handoff Document for Mobile Team

### What to Send Them

**Files:**
1. ✅ `API_DOCUMENTATION.md` - Complete API reference
2. ✅ `MOBILE_INTEGRATION_GUIDE.md` - This document
3. ✅ Server URL: `http://YOUR_IP:10018` or staging URL
4. ✅ Test credentials: 
   - Admin: `admin` / `admin`
   - Test customer: (create via API)

**Information:**
1. ✅ All endpoints use JSON-RPC 2.0 format
2. ✅ Authentication via session cookies or tokens
3. ✅ Error codes are consistent across all endpoints
4. ✅ Images must be base64 encoded, max 5MB
5. ✅ Phone numbers must be Egyptian format (+20 or 01)
6. ✅ Passwords require: 8+ chars, uppercase, lowercase, number

**What to Ask From Them:**
1. 🔴 Firebase Server Key (before Phase 7)
2. 🔴 App package names (Android + iOS)
3. 🟡 Test device FCM tokens (for testing)
4. 🟢 Feedback on API usability

---

## 🔌 Phase 7 Preview (Your Future Work)

### Firebase Integration (You)

```python
# 1. Install library
pip install firebase-admin

# 2. Initialize Firebase
import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "cyclex-app",
    # ... (or use Server Key)
})
firebase_admin.initialize_app(cred)

# 3. Send notification
def send_notification(fcm_token, title, body, data):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data,
        token=fcm_token,
    )
    return messaging.send(message)
```

### SMS Integration (You)

```python
# 1. Install requests library (already installed)
import requests

# 2. Send SMS via SMS Misr
def send_sms(phone, message):
    url = 'https://smsmisr.com/api/v2/'
    payload = {
        'username': 'your_username',
        'password': 'your_password',
        'sender': 'CycleX',
        'message': message,
        'mobile': phone,
    }
    response = requests.post(url, data=payload)
    return response.json()

# 3. Use in verification
verification_code = ''.join(random.choices('0123456789', k=6))
message = f'Your CycleX verification code is: {verification_code}'
send_sms(partner.phone, message)
```

---

## ✅ Summary

### Your Work (Odoo Developer)

**Phase 1-5:** ✅ COMPLETE
- Backend, APIs, QR codes, business logic, validations

**Phase 6:** Testing & Documentation

**Phase 7:** External Integrations
- Firebase FCM (needs Server Key from mobile team)
- SMS Misr (needs account credentials)

### Mobile Team's Work (Separate)

**Phase 8:** Flutter App Development
- Can start NOW
- Needs your API documentation
- Will provide Firebase Server Key to you
- Parallel development (independent)

### Integration Points

**What You Provide:**
- ✅ REST APIs
- ✅ QR code images
- ✅ Validation logic
- 🔜 Push notifications (Phase 7)
- 🔜 SMS verification (Phase 7)

**What They Provide:**
- 🔵 Mobile UI/UX
- 🔵 Photo capture
- 🔵 GPS capture
- 🔵 QR scanning
- 🔴 Firebase Server Key (Phase 7)
- 🔵 FCM token handling

---

**Mobile development is completely separate from your Odoo work!** 🎉  
**They can start building the app NOW while you continue with Phase 6-7!**

