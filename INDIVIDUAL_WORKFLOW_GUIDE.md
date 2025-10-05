# 🎯 Individual Workflow Execution Guide

## 🚨 **Problem Solved: Workflows Now Run Individually**

All workflows are now **manual-only** to prevent simultaneous execution and billing issues.

## 🛠️ **How to Run Workflows Individually:**

### **Step 1: Go to GitHub Actions**
1. Visit: https://github.com/aarondhurst2016-ship-it/accessmate/actions
2. You'll see all available workflows

### **Step 2: Choose Your Workflow**

#### **🆓 For Testing (Minimal Resources):**
- **🆓 Free Tier Build - Essential Only** 
  - **Use:** When billing is fixed, want to save minutes
  - **Builds:** Single platform (Windows OR Linux)
  - **Time:** ~10 minutes
  - **Resources:** Minimal

#### **🚀 For Full Builds:**
- **Build All Platforms - Store Ready**
  - **Use:** Complete store-ready builds
  - **Builds:** Windows, Android, iOS, Linux, macOS
  - **Time:** ~50 minutes
  - **Resources:** High

- **🚀 Build All Platforms - Store Ready** (Different version)
  - **Use:** Alternative full build with different settings
  - **Builds:** All platforms
  - **Time:** ~60 minutes
  - **Resources:** High

- **Build ALL Versions - Manual Hard Installs + App Store Packages + GitHub Releases**
  - **Use:** Complete distribution package
  - **Builds:** All platforms + GitHub releases
  - **Time:** ~75 minutes
  - **Resources:** Maximum

- **Build Android APK**
  - **Use:** Android-only builds
  - **Builds:** Just Android
  - **Time:** ~8 minutes
  - **Resources:** Low

### **Step 3: Run Individual Workflow**
1. **Click** on the workflow you want
2. **Click** "Run workflow" button (top right)
3. **Select** branch (usually `main`)
4. **Add** optional reason/notes
5. **Click** "Run workflow" green button

## 💡 **Recommended Strategy:**

### **When Billing is Fixed:**
1. **Start with:** 🆓 Free Tier Build (test the waters)
2. **Then try:** Build Android APK (single platform)
3. **Finally:** Full platform builds when confident

### **Resource Management:**
- **Test builds:** Use Free Tier workflow
- **Single platform:** Use Android-only or Windows-only
- **Full release:** Use complete build workflows
- **Emergency:** Use local build script (`python build_local.py`)

## 🔧 **Local Alternative (Always Available):**
```bash
# No GitHub needed - works immediately
python build_local.py
```

## 📊 **Workflow Comparison:**

| Workflow | Platforms | Time | Minutes Used | Best For |
|----------|-----------|------|--------------|----------|
| 🆓 Free Tier | 1 | ~10 min | 10 | Testing |
| Android APK | 1 | ~8 min | 8 | Android only |
| Store Ready | 5 | ~50 min | 250 | Full release |
| ALL Versions | 5+ | ~75 min | 375 | Complete package |
| Local Build | 1 | ~5 min | 0 | Immediate |

---

**✅ Now you can run workflows one at a time instead of all simultaneously!**