# What Odoo Developer Needs FROM Mobile Team 🔴

**For:** Odoo Backend Developer  
**From:** Flutter Mobile Development Team  
**Purpose:** Integration requirements for Phase 7

---

## 🎯 Summary

As the Odoo developer, you **don't do any mobile development work**. However, you **need specific information** from the mobile team to complete Phase 7 (External Integrations).

---

## 🔴 Critical Requirements (Before Phase 7)

### 1. Firebase Server Key 🔴 MOST IMPORTANT

**What It Is:**
```
Format: AAAAxxxxxxxxxxxxxxx:APAxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Length: ~180 characters
Example: AAAA1234567:APA91bF...xyz
```

**Where They Get It:**
1. Mobile team creates Firebase project at console.firebase.google.com
2. They go to: **Project Settings → Cloud Messaging → Server Key**
3. They copy the key and send to you

**What You'll Do With It:**
```python
# In Odoo: Settings → Technical → Parameters → System Parameters
# Add new parameter:
Key: firebase.server_key
Value: (paste the Server Key they provide)
```

**When You Need It:**
- ⏰ Before starting Phase 7, Checkpoint 7.2
- 📍 Absolutely required to send push notifications from Odoo

**Without This:**
- ❌ You cannot send push notifications
- ❌ No mobile alerts for orders/wallet updates
- ⚠️ App will work but without notifications

---

### 2. App Package Names 🔴 REQUIRED

**What They Are:**

#### Android Package Name:
```
Format: com.company.appname
Example: com.cyclex.app
```

#### iOS Bundle ID:
```
Format: com.company.appname
Example: com.cyclex.app
```

**Where They Get It:**
- Android: From `android/app/build.gradle` → `applicationId`
- iOS: From Xcode → Target → Bundle Identifier

**What You'll Do With It:**
- Store in Odoo configuration
- Use for Firebase FCM targeting
- Use for notification routing

**When You Need It:**
- ⏰ Before Phase 7, Checkpoint 7.2
- 📍 When setting up Firebase integration

---

## 🟡 Important (For Testing)

### 3. Test Device FCM Tokens 🟡 FOR TESTING

**What They Are:**
```
Format: Long string (~150-200 characters)
Example: dXYzABC123def...uvwxyz789
```

**Where They Get Them:**

Mobile team adds this code to their Flutter app:
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  
  String? token = await FirebaseMessaging.instance.getToken();
  print('FCM Token: $token');  // They copy this from console
}
```

**What You'll Do With Them:**
- Test push notifications from Odoo
- Verify Firebase integration works
- Debug notification issues

**When You Need Them:**
- ⏰ During Phase 7 testing
- 📍 After you've implemented Firebase FCM integration
- 🧪 For end-to-end testing

**How Many:**
- 1 Android device token
- 1 iOS device token (optional but recommended)

---

## 🟢 Nice to Have (For Coordination)

### 4. API Server URL Confirmation 🟢 COORDINATION

**What:**
```
Development: http://YOUR_IP:10018
Staging: https://staging.cyclex.app (if applicable)
Production: https://api.cyclex.app (future)
```

**Why:**
- They need to know where to point their API calls
- You need to confirm your server is accessible

**When:**
- ⏰ When they start development (Phase 8)
- 📍 Can change between dev/staging/production

---

### 5. Test Accounts 🟢 OPTIONAL

**What:**
```
Test Customer:
  Phone: +201111111111
  Password: TestPass123
  
Test Collector:
  Phone: +201222222222
  Password: TestPass123
```

**Why:**
- They can test without creating new accounts
- Faster testing
- Pre-configured with sample data

**When:**
- ⏰ When they start API integration
- 📍 You can create these anytime

---

## 📋 Request Template for Mobile Team

Send this to the mobile team:

```
Subject: Firebase Configuration Needed for CycleX Backend

Hi Mobile Team,

I've completed the Odoo backend (Phase 1-5) and all APIs are ready for integration.

To complete Phase 7 (Push Notifications), I need the following from you:

🔴 CRITICAL (Please provide before [DATE]):

1. Firebase Server Key
   - Location: Firebase Console → Project Settings → Cloud Messaging → Server Key
   - Format: Long string starting with "AAAA..."
   - Purpose: Allows Odoo to send push notifications

2. App Package Names
   - Android package name (from build.gradle)
   - iOS bundle ID (from Xcode)

🟡 FOR TESTING (When ready):

3. Test Device FCM Tokens
   - One Android device token
   - One iOS device token
   - You can get this by printing the token in your app after Firebase.initializeApp()

📚 DOCUMENTATION PROVIDED:

I've attached:
- API_DOCUMENTATION.md (All 22 API endpoints)
- MOBILE_INTEGRATION_GUIDE.md (Complete integration guide)
- API Server URL: http://[YOUR_IP]:10018

You can start mobile development immediately. The backend is ready!

Please let me know if you have any questions.

Best regards,
Odoo Developer
```

---

## 🔄 When You'll Use Each Item

### Timeline:

```
NOW (Phase 5 Complete):
├─ YOU: Provide API_DOCUMENTATION.md to mobile team ✅
├─ YOU: Provide MOBILE_INTEGRATION_GUIDE.md to mobile team ✅
└─ YOU: Provide API server URL ✅

Week 1-2 (Mobile Team Starts):
├─ THEM: Create Firebase project
├─ THEM: Start Flutter development
└─ THEM: Begin API integration

Week 3-4 (Before Your Phase 7):
├─ THEM: Send you Firebase Server Key 🔴
├─ THEM: Send you package names 🔴
└─ YOU: Can start Phase 7 implementation

Week 5-6 (Phase 7 - You):
├─ YOU: Implement Firebase FCM in Odoo
├─ YOU: Implement SMS Misr integration
└─ THEM: Provide test FCM tokens for testing 🟡

Week 7-8 (Testing):
├─ YOU: Send test notifications
├─ THEM: Confirm notifications received
├─ YOU: Fix any backend issues
└─ THEM: Fix any mobile issues
```

---

## ❌ What You DON'T Need From Them

### These Stay in Mobile App (NOT Odoo):

1. ❌ **google-services.json** - Stays in Android app
2. ❌ **GoogleService-Info.plist** - Stays in iOS app
3. ❌ Flutter code or mobile app files
4. ❌ Mobile UI designs or mockups
5. ❌ App Store / Play Store credentials
6. ❌ Mobile build configurations

### You Only Need:

1. ✅ Firebase **Server Key** (just the key string)
2. ✅ Package names (just the text strings)
3. ✅ FCM tokens (for testing)

---

## 🎯 Quick Reference Card

### Phase 7 Blocker Items (Must Have):

| Item | Who Provides | When Needed | Format |
|------|-------------|-------------|---------|
| **Firebase Server Key** | Mobile Team | Before Phase 7 | String ~180 chars |
| **Android Package Name** | Mobile Team | Before Phase 7 | com.example.app |
| **iOS Bundle ID** | Mobile Team | Before Phase 7 | com.example.app |
| **Test FCM Tokens** | Mobile Team | Phase 7 Testing | String ~150 chars |

### What You Provide to Them:

| Item | When | Location |
|------|------|----------|
| **API Documentation** | NOW | `API_DOCUMENTATION.md` |
| **Integration Guide** | NOW | `MOBILE_INTEGRATION_GUIDE.md` |
| **Server URL** | NOW | `http://YOUR_IP:10018` |
| **Test Accounts** | When requested | Create in Odoo |

---

## 📞 Communication Checklist

### Initial Handoff (NOW):
- [ ] Send `API_DOCUMENTATION.md` to mobile team
- [ ] Send `MOBILE_INTEGRATION_GUIDE.md` to mobile team
- [ ] Provide API server URL and test credentials
- [ ] Confirm they can start development immediately

### Before Phase 7 (Week 3-4):
- [ ] Request Firebase Server Key from mobile team
- [ ] Request package names from mobile team
- [ ] Confirm they understand what you need

### During Phase 7 (Week 5-6):
- [ ] Implement Firebase FCM with their Server Key
- [ ] Request test device FCM tokens
- [ ] Test notifications end-to-end

### After Phase 7 (Week 7-8):
- [ ] Mobile team tests notifications
- [ ] Fix any integration issues together
- [ ] Finalize for production

---

## 🚀 Next Steps

### What You Do Next:

1. **Immediate:**
   - ✅ Send documentation to mobile team
   - ✅ Phase 5 complete, all changes pushed

2. **Optional: Phase 6 (Testing & Documentation)**
   - Create Postman collection
   - Test all APIs
   - Document backend workflows

3. **Waiting Period:**
   - ⏳ Wait for Firebase Server Key from mobile team
   - ⏳ Wait for package names from mobile team
   - 📱 Mobile team builds app in parallel

4. **Phase 7: External Integrations**
   - 🔜 Use Firebase Server Key to send notifications
   - 🔜 Integrate SMS Misr for OTP
   - 🔜 Test with mobile team's devices

---

## 📝 Sample Responses to Mobile Team Questions

**Q: "Where do we get the API documentation?"**
- A: "Check `API_DOCUMENTATION.md` - all 22 endpoints documented"

**Q: "How do we authenticate API calls?"**
- A: "After login, use the auth_token in session cookies. See `MOBILE_INTEGRATION_GUIDE.md` section 'Authentication Flow'"

**Q: "What format should images be?"**
- A: "Base64 encoded, max 5MB per image. See endpoint `/api/cyclex/request/create`"

**Q: "How do we display the QR code?"**
- A: "I return it as base64 PNG in `qr_code_image` field. Just decode and display. Example in MOBILE_INTEGRATION_GUIDE.md"

**Q: "Where should we send the Firebase Server Key?"**
- A: "Email it to me or add to shared documentation. I need it before Phase 7"

**Q: "When will push notifications work?"**
- A: "After Phase 7 is complete (about 2-3 weeks). You can build the app now without notifications"

**Q: "Can we start development now?"**
- A: "YES! All APIs are ready. You don't need to wait for Phase 7. Build the app, notifications will be added later"

---

## ✅ TL;DR (Too Long; Didn't Read)

### What You Need:

**From Mobile Team (Critical):**
1. 🔴 Firebase Server Key (~180 char string)
2. 🔴 Android package name (com.example.app)
3. 🔴 iOS bundle ID (com.example.app)
4. 🟡 Test FCM tokens (for testing)

**What You Provide:**
1. ✅ API_DOCUMENTATION.md
2. ✅ MOBILE_INTEGRATION_GUIDE.md
3. ✅ API server URL

**What You Don't Need:**
- ❌ Any Firebase config files (they keep those)
- ❌ Any mobile code or Flutter files
- ❌ Any mobile app build files

**Your Phase 7 Work:**
- 🔜 Use their Server Key to send notifications FROM Odoo
- 🔜 Implement SMS sending for verification

---

**That's it! Simple and clear. 🎯**

