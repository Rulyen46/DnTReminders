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
        "Did you know our Guild Bank is bursting with loot? Alts welcome! Check Discord for details—and send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs!"
        "Got extras? Share the wealth! Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs—and check Discord to request some too!"
        "Our Guild Bank is stacked—and open to all! Alts welcome. Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Check Discord for the loot guide!"
        "Feeling generous? Help keep the Guild Bank strong—send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Don’t forget to request some for your alts too—check Discord!"
        "Join the loot cycle of life: send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs—and claim what you need via Discord. Alts love free gear!"
        "From epics to augs, we’ve got you covered! Guild Bank is fully stocked. Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Request gear via Discord!"
        "Keep the treasure flowing—send your extras to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Need something? Instructions are in Discord!"
        "The Guild Bank gods smile upon those who send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Check Discord to request your divine loot!"
        "No alt left behind! Help us gear up the squad—send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Instructions in Discord for loot requests!"
        "Our Guild Bank is your loot buffet. Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs—and check Discord for how to feast!"
        "See a noob in need? Be the hero—send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Then hop into Discord and grab gear for yourself!"
        "Don’t vendor that shiny drop! Send it to DNTBank, DNTSpells, DNTEpics, DNTCraft, or DNTAugs. Then check Discord to see what you can score in return!"
        "Whether it’s spells or crafting loot, the Guild Bank needs YOU. Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Details in Discord!"
        "Turn your clutter into community power! Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Loot instructions await in Discord!"
        "Helping your guild is just a parcel away—send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Want free gear? Check Discord!"
        "Your junk is another alt's upgrade. Contribute to the Guild Bank by sending items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Check Discord for requests!"
        "DNTBank and friends are hungry! Feed them loot—send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Then check Discord and get fed yourself!"
        "EverQuest karma: send your spares to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Then check Discord and get some gear love in return!"
        "DNTBank wants your dusty drops! Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Discord holds the secrets to claiming your own!"
        "Stock the Guild Bank, gear the guild! Send items to DNTBank, DNTSpells, DNTEpics, DNTCraft, and DNTAugs. Then hit up Discord for the loot lottery!"
    ],
    "bankLocations": [
        // redundant combined with guild bank message remove banklocations
    ],
    "website": [
        // redundant combined with guild bank request message remove website
    ],
    "requestProcess": [
        "Lost in lootless limbo? Fear not! Check the Guild Bank at https://thj-dnt.web.app/bank. Tons of gear awaits—don’t be shy, dive in! Post your request in Discord’s Bank-Requests channel."
        "Running light on loot? The Guild Bank is loaded! Visit https://thj-dnt.web.app/bank and post in Discord’s Bank-Requests. Don’t be shy—we seriously have plenty to go around!"
        "The treasure hoard is real. Check out our Guild Bank at https://thj-dnt.web.app/bank and post in Bank-Requests on Discord. Don’t hesitate—we’ve got more than enough for all!"
        "Need gear? We’ve got gear. Check the Guild Bank at https://thj-dnt.web.app/bank. Don't be bashful—post in Bank-Requests on Discord. We love giving stuff away!"
        "Think your alt is undergeared? We know they are. Check https://thj-dnt.web.app/bank and post in Bank-Requests on Discord. Do not be shy—we're bursting with loot!"
        "Your next upgrade might already be waiting. Hit https://thj-dnt.web.app/bank, then post in Discord’s Bank-Requests. Seriously—don’t be shy. We’re overflowing."
        "If you haven’t checked the Guild Bank yet, you're missing out! Go to https://thj-dnt.web.app/bank. Do not be shy—ask in Bank-Requests. There's so much loot!"
        "The Guild Bank is not a myth. It's real. It's glorious. Visit https://thj-dnt.web.app/bank and request in Discord. Don’t be shy—we promise, we have TONS."
        "Alts, mains, returning heroes—all welcome! Browse https://thj-dnt.web.app/bank and post in Discord’s Bank-Requests. Don’t hold back—we’ve got plenty!"
        "Stop hoarding those bronze boots and upgrade already! Check https://thj-dnt.web.app/bank. Ask in Discord’s Bank-Requests. No shame—we have enough for an army."
        "If you need something, we probably have three of it. Go to https://thj-dnt.web.app/bank and make a request in Discord. Don’t be shy—we want you to ask!"
        "That missing spell or epic drop? It might be waiting. See https://thj-dnt.web.app/bank. Don’t hesitate—ask in Bank-Requests on Discord. There’s plenty."
        "Don’t quest in rags. The Guild Bank is full of riches! Check https://thj-dnt.web.app/bank and ask in Bank-Requests. We’re literally begging you to take it."
        "There’s no such thing as 'asking for too much'—check https://thj-dnt.web.app/bank and request in Discord. Don’t be shy—we've got stacks on stacks!"
        "Your inventory deserves better. Check the Guild Bank: https://thj-dnt.web.app/bank. Do not be shy—post your wishlist in Discord. We will make it happen."
        "The loot fairy lives at https://thj-dnt.web.app/bank. Visit her and make a wish in Discord’s Bank-Requests channel. We’re stocked—so don’t be shy!"
        "Before you farm it, check the Guild Bank first: https://thj-dnt.web.app/bank. Don’t be shy—we might just have what you need waiting!"
        "You like loot? We love giving it away! Visit https://thj-dnt.web.app/bank and ask in Discord. Do not be shy—seriously, we’re drowning in items."
        "That aug you've been searching for? It’s probably already in the bank. Check https://thj-dnt.web.app/bank and request in Discord. Don’t be shy—we have tons."
        "This is your sign to gear up! Go to https://thj-dnt.web.app/bank and post in Discord’s Bank-Requests. Do not be shy—we’re way more stocked than you think."
    ],
    "guildNeeds": [
        "Support the guild dream—donate level 61+ spells, augs, help fund Stimilus donations, high demand crafting materials, hard to obtain epic items, and end game loot!"
        "Got extras? We’ll take end game loot, high demand crafting donations, augs, level 61+ spells, help fund Stimilus donations, and epic item pieces!"
        "Your guild needs you! Send in help fund Stimilus donations, hard to obtain epic items, crafting donations, augs, end game loot, and 61+ spells!"
        "Clean your bags for a cause—donate crafting mats, end game loot, hard to obtain epic items, help fund Stimilus donations, level 61+ spells, and augs!"
        "Make a difference! We need high demand crafting donations, 61+ spells, help fund Stimilus donations, end game loot, hard to obtain epic items, and augs!"
        "The vaults are hungry—feed them with augs, 61+ spells, end game loot, high demand crafting donations, hard to obtain epic items, and Stimilus support!"
        "Got loot collecting dust? We’re looking for hard to obtain epic items, help fund Stimilus donations, augs, end game loot, level 61+ spells, and crafting donations!"
        "Help the guild thrive! Donate end game loot, 61+ spells, crafting materials, help fund Stimilus donations, hard to obtain epic items, and augs!"
        "Be a guild hero—donate augs, high demand crafting goods, end game loot, help fund Stimilus donations, 61+ spells, and those hard to find epic pieces!"
        "We’re always in need of donations! Bring us level 61+ spells, augs, crafting donations, end game loot, hard to obtain epic items, and support for Stimilus!"
        "Stash to spare? Send end game loot, 61+ spells, help fund Stimilus donations, crafting goods, augs, and hard to obtain epic items!"
        "Don't let your loot rot—donate augs, epic items, crafting mats, 61+ spells, help fund Stimilus donations, and end game loot!"
        "Your spare stuff powers us all—donate high demand crafting materials, level 61+ spells, augs, end game loot, hard to obtain epic items, and support Stimilus!"
        "Time to give back! We need help funding Stimilus, end game loot, 61+ spells, hard to obtain epic items, augs, and top-tier crafting donations!"
        "Help the cause—donate augs, help fund Stimilus donations, end game loot, crafting supplies, 61+ spells, and rare epic items!"
        "Be legendary—donate rare epic items, help fund Stimilus donations, high demand crafting materials, augs, level 61+ spells, and end game loot!"
        "Stock the vaults with your loot—donate end game loot, level 61+ spells, crafting mats, hard to obtain epic items, augs, and help fund Stimilus!"
        "Support your guildmates! We're after hard to obtain epic items, high demand crafting donations, augs, 61+ spells, help fund Stimilus donations, and end game loot!"
        "Join the supply squad—donate 61+ spells, hard to obtain epic items, crafting donations, augs, end game loot, and help fund Stimilus!"
        "We rise together—help fund Stimilus donations, drop off end game loot, share 61+ spells, hand in epic items, donate augs, and contribute crafting goods!"
    ],
    "guildPerks": [
        "New here? Grab a free 30-slot bag, PL/flag help, 5k plat advance, build guides on Discord, and stat food/drink clicks (ask officers!)"
        "Join the squad and enjoy build guides on Discord, stat food/drink clicks (ask officers!), a 30-slot bag, PL/flag help, and a sweet 5k plat advance!"
        "We hook you up fast: PL/flag help, a free 30-slot bag, 5k plat advance, build guides on Discord, and clickable stat food/drinks!"
        "Fresh recruits get spoiled—get stat food/drink clicks (ask officers!), a 5k plat advance, PL/flag help, build guides on Discord, and a 30-slot bag!"
        "Welcome package includes: build guides on Discord, a 5k plat advance, stat food/drink clicks (ask officers!), PL/flag help, and a shiny 30-slot bag!"
        "Don’t level alone! Get PL/flag help, a 30-slot bag, build guides on Discord, stat food/drink clicks (ask officers!), and 5k plat to start!"
        "Your starter kit: 30-slot bag, 5k plat advance, PL/flag help, build guides on Discord, and tasty stat food/drinks (ask officers!)"
        "Join today and get rich—5k plat advance, stat food/drink clicks (ask officers!), PL/flag help, build guides on Discord, and a 30-slot bag!"
        "We’ll get you rolling with PL/flag help, stat food/drinks, a free 30-slot bag, 5k plat advance, and expert build guides on Discord!"
        "Start strong with a 5k plat advance, stat food/drink clicks (ask officers!), a 30-slot bag, build guides on Discord, and full PL/flag support!"
        "We give more than loot: PL/flag help, a 30-slot bag, 5k plat advance, clickable stat food/drinks, and build guides on Discord!"
        "New members rejoice: claim your 5k plat advance, get a 30-slot bag, enjoy stat food/drink clicks (ask officers!), build guides on Discord, and PL/flag help!"
        "We make alts and newbies feel right at home—stat food/drink clicks (ask officers!), 30-slot bag, PL/flag help, 5k plat, and guides on Discord!"
        "Power up with build guides on Discord, a 30-slot bag, stat food/drinks, PL/flag help, and a generous 5k plat advance!"
        "Why struggle when you can have a 30-slot bag, stat food/drinks, PL/flag help, a 5k plat advance, and build guides on Discord?"
        "New blood gets all the perks—build guides on Discord, PL/flag help, stat food/drinks, 5k plat, and a giant 30-slot bag!"
        "We don’t just welcome—we equip! Get 5k plat, PL/flag help, build guides on Discord, stat food/drink clicks, and a 30-slot bag!"
        "New to the guild? Receive PL/flag help, a free 30-slot bag, build guides on Discord, a 5k plat advance, and clickable stat food/drinks!"
        "Kick off your journey with a 30-slot bag, PL/flag help, build guides on Discord, 5k plat, and stat food/drink clicks (ask officers!)"
        "Loot? Yup. Help? Always. You get build guides on Discord, a 5k plat advance, PL/flag help, stat food/drink clicks, and a 30-slot bag!"
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
