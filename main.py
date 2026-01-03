import requests
import time
import json
import os
from datetime import datetime

# ==========================================
# ការកំណត់ (CONFIGURATION)
# ==========================================
# Token និង ID របស់អ្នក (ដែលបានផ្តល់អោយ)
BOT_TOKEN = "8404578268:AAFtvrCNLvuURNV1E5ZogK2U_WwWm7dQ52w"
CHAT_ID = "7322712989"
DATA_FILE = "accounts.json"

# ==========================================
# មុខងារ (FUNCTIONS)
# ==========================================

def load_accounts():
    """អានទិន្នន័យពី file json មកប្រើ"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_account(username, password):
    """រក្សាទុក account ចូលក្នុង stock (json file)"""
    accounts = load_accounts()
    # បន្ថែម account ថ្មី
    accounts.append({
        "username": username,
        "password": password,
        "date_added": str(datetime.now())
    })
    # សរសេរចូល file វិញ
    with open(DATA_FILE, "w") as f:
        json.dump(accounts, f, indent=4)
    print(f"✅ បានរក្សាទុក {username} ជោគជ័យ!")

def send_to_telegram():
    """ផ្ញើទិន្នន័យទាំងអស់ទៅ Telegram Bot"""
    accounts = load_accounts()
    
    if not accounts:
        print("❌ គ្មាន Account នៅក្នុង Stock ទេ!")
        return

    # រៀបចំសារដែលត្រូវផ្ញើ
    message = "📦 REPORT: ROBLOX ACCOUNTS STOCK 📦\n\n"
    for idx, acc in enumerate(accounts, 1):
        message += f"👤 **Account {idx}:**\n"
        message += f"🆔 User: `{acc['username']}`\n"
        message += f"🔑 Pass: `{acc['password']}`\n"
        message += "--------------------------\n"

    # URL សម្រាប់ផ្ញើទៅ API Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("🚀 បានផ្ញើទៅ Telegram ជោគជ័យ!")
        else:
            print(f"⚠️ មានបញ្ហា: {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")

def schedule_sender():
    """កំណត់ម៉ោងផ្ញើ"""
    print("\n⏰ --- កំណត់ម៉ោងផ្ញើ ---")
    target_time = input("បញ្ចូលម៉ោងចង់ផ្ញើ (ទម្រង់ 24h ឧ. 14:30): ")
    
    print(f"⏳ កំពុងរង់ចាំដល់ម៉ោង {target_time} ដើម្បីផ្ញើ...")
    
    while True:
        # យកម៉ោងបច្ចុប្បន្ន (HH:MM)
        current_time = datetime.now().strftime("%H:%M")
        
        if current_time == target_time:
            print("\n🔔 ដល់ម៉ោងហើយ! កំពុងផ្ញើ...")
            send_to_telegram()
            break # ឈប់ដំណើរការបន្ទាប់ពីផ្ញើរួច
        
        time.sleep(30) # សម្រាក 30 វិនាទីសិន ចាំ check ម្តងទៀត

# ==========================================
# ដំណើរការកម្មវិធី (MAIN LOOP)
# ==========================================
def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("""
    🤖 ROBLOX ACCOUNT MANAGER & SENDER 🤖
    1. ➕ បញ្ចូល Account ថ្មី (Stock)
    2. 📋 មើលចំនួន Account ក្នុង Stock
    3. 🚀 ផ្ញើទៅ Telegram ភ្លាមៗ
    4. ⏰ កំណត់ម៉ោងផ្ញើ (Schedule)
    5. ❌ ចាកចេញ
        """)
        choice = input("👉 ជ្រើសរើស (1-5): ")

        if choice == '1':
            u = input("Username: ")
            p = input("Password: ")
            save_account(u, p)
            input("\nចុច Enter ដើម្បីបន្ត...")
        elif choice == '2':
            accs = load_accounts()
            print(f"\n📦 មាន {len(accs)} accounts នៅក្នុង stock.")
            input("\nចុច Enter ដើម្បីបន្ត...")
        elif choice == '3':
            send_to_telegram()
            input("\nចុច Enter ដើម្បីបន្ត...")
        elif choice == '4':
            schedule_sender()
            input("\nចុច Enter ដើម្បីបន្ត...")
        elif choice == '5':
            print("👋 លាហើយ!")
            break
        else:
            print("❌ សូមជ្រើសរើសអោយត្រឹមត្រូវ!")
            time.sleep(1)

if name == "__main__":
    main()