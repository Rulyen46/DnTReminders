import os
import random
import time
import datetime
import requests

# Configuration from Lambda environment variables
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
VARIANCE_SECONDS = 300  # �5 minutes (300 seconds) total variance

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

# Updated hourly rotation schedule
hourly_categories = [
    ['guildBank', 'bankLocations', 'guildPerks'],   # 00,05,10,15,20
    ['website', 'requestProcess'],                  # 01,06,11,16,21
    ['guildNeeds', 'guildBank'],                    # 02,07,12,17,22
    ['bankLocations', 'website'],                   # 03,08,13,18,23
    ['requestProcess', 'guildNeeds', 'guildPerks']  # 04,09,14,19
]

def get_random_message(category):
    return random.choice(message_variations[category])

def simulate_typing():
    """Simulate typing indicator with error handling"""
    try:
        requests.post(
            f"https://discord.com/api/v10/channels/{CHANNEL_ID}/typing",
            headers={'Authorization': TOKEN},
            timeout=2
        )
    except Exception as e:
        print(f"Typing simulation failed: {str(e)}")
    time.sleep(2)  # Shortened for Lambda constraints

def send_message(content):
    """Send message to Discord with Lambda-optimized timeouts"""
    try:
        response = requests.post(
            f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages",
            headers={
                'Authorization': TOKEN,
                'Content-Type': 'application/json'
            },
            json={'content': content},
            timeout=5  # Important for Lambda timeout handling
        )
        if not response.ok:
            print(f"Message failed: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Message send error: {str(e)}")

def process_messages():
    """Main message handling logic"""
    try:
        now = datetime.datetime.utcnow()  # Using UTC for cloud consistency
        current_hour = now.hour % 24
        hour_group = current_hour % 5
        categories = hourly_categories[hour_group]
        
        print(f"Processing hour {current_hour} (group {hour_group}): {categories}")
        
        for category in categories:
            message = get_random_message(category)
            simulate_typing()
            send_message(message)
            time.sleep(random.uniform(0.5, 1.5))  # Natural interval
            
    except Exception as e:
        print(f"Processing failed: {str(e)}")
        raise

def lambda_handler(event, context):
    """AWS Lambda entry point"""
    try:
        # Apply random variance
        delay = random.randint(0, VARIANCE_SECONDS)
        print(f"Applying variance delay: {delay}s")
        time.sleep(delay)
        
        process_messages()
        return {
            'statusCode': 200,
            'body': 'Messages processed successfully'
        }
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
        return {
            'statusCode': 500,
            'body': 'Failed to process messages'
        }