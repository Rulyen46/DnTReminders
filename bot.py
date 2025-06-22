import requests
import time
import random
import datetime
import schedule
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = os.getenv('CHANNEL_ID')
VARIANCE_MINUTES = 2.5  # ±2.5 minutes variance

# Headers for Discord API requests
headers = {
    'Authorization': TOKEN,
    'Content-Type': 'application/json',
}

# Message variations for each scheduled announcement
message_variations = {
    "guildBank": [
        "Did you know we have a Guild Bank with tons of items available to request? Alts welcome! Check Discord for instructions.",
        "Our Guild Bank has plenty of items for all members! Alts are welcome too. See Discord for how to access.",
        "Need items? Check out our Guild Bank! We welcome requests from mains and alts. Instructions on Discord.",
        "Don't forget about our Guild Bank - loaded with items for everyone including alts! Details on Discord.",
        "Guild Bank reminder: we have TONS of items available for you and your alts! See Discord for request instructions."
    ],
    "bankLocations": [
        "Send items to: DNTBank (Time Loot), DNTSpells (60+ Any), DNTEpics (Epic Items), DNTCraft (EP Mold: PLATE ONLY, Ornate BP/Legs/Gloves only) and high-end crafting mats.",
        "Guild Bank locations: DNTBank for Time Loot, DNTSpells for 60+ spells, DNTEpics for Epic Items, and DNTCraft for EP Mold (PLATE ONLY) & Ornate BP/Legs/Gloves.",
        "Our bank characters: DNTBank (Time Loot), DNTSpells (Lvl 60+ spells), DNTEpics (Epic Items), DNTCraft (Plate EP Molds & Ornate BP/Legs/Gloves, high-end mats).",
        "Bank alts for your donations: DNTBank, DNTSpells, DNTEpics, and DNTCraft. See Discord for what goes where!",
        "Remember our bank alts: DNTBank, DNTSpells, DNTEpics, and DNTCraft. Check Discord for specific deposit guidelines."
    ],
    "website": [
        "Our Guild Bank website is updated daily with tons of new stuff constantly being added: https://thj-dnt.web.app/bank",
        "Check out our Guild Bank website - updated DAILY with new items: https://thj-dnt.web.app/bank",
        "Browse our Guild Bank inventory at https://thj-dnt.web.app/bank - we add new items every day!",
        "Visit our Guild Bank website for the latest inventory: https://thj-dnt.web.app/bank (updated daily)",
        "Need something? Our Guild Bank website shows all available items and is refreshed daily: https://thj-dnt.web.app/bank"
    ],
    "requestProcess": [
        "To request items, make a post in Discord under Requests. Don't be shy - we have tons of stuff, get greedy!",
        "Want something from the Guild Bank? Post in the Discord Requests channel. We have plenty, so don't hold back!",
        "Item requests go in the Discord Requests channel. We have an abundance of items, so feel free to ask for what you need!",
        "Need something? Post in Discord Requests! We have loads of items and want to help gear you up!",
        "For Guild Bank requests, post in our Discord Requests channel. We encourage you to ask - we have TONS of items!"
    ],
    "guildNeeds": [
        "Check Discord Announcements and Getting Started for info (channel Guild-Wanted) to see what we might need.",
        "Want to contribute? Check the Guild-Wanted channel in Discord to see our current needs.",
        "See what the guild is looking for in our Discord's Guild-Wanted channel (under Announcements and Getting Started).",
        "Help the guild grow! Check Discord Announcements and Getting Started sections for our Guild-Wanted list.",
        "Looking to donate? The Guild-Wanted channel in Discord shows what items we're currently seeking."
    ],
    "guildPerks": [
        "New member benefits: 5k plat advance, free 30-slot bag, stat food/drink clicks (ask officers!), build guides on Discord, and PL/flag help!",
        "Guild perks alert: Starter platinum, weight-reduction bag, free stat food (officers have clickies!), build advice, and group help - just ask!",
        "Remember: We offer new members 5k plat, giant bag, stat boost food (ask online officers!), Discord guides, and PL/flag assistance!",
        "Pro tip: Claim your 5000p advance, free bag , consumables (check with officers!), build resources, and group help!",
        "Member benefits: Instant 5k plat, 30-slot bag, food/drink clicks (officers carry them!), Discord guides, and progression help!"
    ]
}

# Define which categories to use each hour (rotating pattern)
hourly_categories = [
    # 00:00, 05:00, 10:00, 15:00, 20:00
    ['guildBank', 'requestProcess'],  
    # 01:00, 06:00, 11:00, 16:00, 21:00 
    ['guildNeeds', 'guildPerks'],                 
    # 02:00, 07:00, 12:00, 17:00, 22:00
    ['guildNeeds', 'guildBank'],                   
    # 03:00, 08:00, 13:00, 18:00, 23:00
    ['guildBank', 'guildPerks'],                  
    # 04:00, 09:00, 14:00, 19:00
    ['requestProcess', 'guildNeeds', 'guildPerks'] 
]

def get_random_message(category):
    """Get a random message from the specified category."""
    return random.choice(message_variations[category])

def simulate_typing(channel_id, duration=3):
    """Simulate typing in the channel with timeout."""
    typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
    try:
        response = requests.post(typing_url, headers=headers, timeout=5)
        if response.status_code != 204:
            print(f"Error simulating typing: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Typing simulation error: {e}")
    time.sleep(duration)

def send_message(channel_id, content):
    """Send a message to the specified channel with timeout."""
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    data = {'content': content}
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            print(f"Message sent: {content[:30]}...")
        else:
            print(f"Error sending message: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error sending message: {e}")

def send_scheduled_messages():
    """Send the scheduled messages with typing simulation."""
    try:
        current_hour = datetime.datetime.now().hour
        hour_index = current_hour % 5
        categories = hourly_categories[hour_index]
        
        print(f"\n--- Sending messages from categories: {categories} ---")
        
        for i, category in enumerate(categories):
            message = get_random_message(category)
            
            # Simulate typing before sending
            typing_duration = min(len(message) * 0.05, 5)
            simulate_typing(CHANNEL_ID, typing_duration)
            
            send_message(CHANNEL_ID, message)
            
            if i < len(categories) - 1:
                time.sleep(1 + random.random())
                
    except Exception as e:
        print(f"Error in scheduled task: {e}")

def schedule_next_run():
    """Schedule next message at exactly 1 hour ± variance from NOW."""
    schedule.clear()
    variance_seconds = random.randint(-int(VARIANCE_MINUTES * 60), int(VARIANCE_MINUTES * 60))
    next_run = datetime.datetime.now() + datetime.timedelta(seconds=3600 + variance_seconds)
    schedule.every().day.at(next_run.strftime("%H:%M:%S")).do(job_wrapper)
    print(f"Next message at: {next_run.strftime('%H:%M:%S %Z')}")

def job_wrapper():
    """Handle message sending and reschedule."""
    try:
        send_scheduled_messages()
    finally:
        schedule_next_run()

def validate_token():
    """Validate Discord token."""
    url = "https://discord.com/api/v10/users/@me"
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            user_data = response.json()
            print(f"Authenticated as: {user_data['username']}#{user_data['discriminator']}")
            return True
        print(f"Authentication failed: {response.status_code}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Token validation error: {e}")
        return False

if __name__ == "__main__":
    if not TOKEN or not CHANNEL_ID:
        print("Missing environment variables. Check .env file.")
        exit(1)
    
    if not validate_token():
        exit(1)
    
    print("\n=== Discord message scheduler started ===")
    
    # Initial schedule (first run within 10 minutes)
    initial_delay = random.randint(0, 600)
    first_run = datetime.datetime.now() + datetime.timedelta(seconds=initial_delay)
    schedule.every().day.at(first_run.strftime("%H:%M:%S")).do(job_wrapper)
    
    print(f"\nFirst message scheduled for: {first_run.strftime('%H:%M:%S %Z')} "
          f"(in {initial_delay//60} minutes)")
    
    while True:
        schedule.run_pending()
        time.sleep(1)
