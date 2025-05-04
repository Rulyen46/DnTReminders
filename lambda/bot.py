import os
import random
import time
import datetime
import requests

# Configuration from Lambda environment variables
TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']
VARIANCE_SECONDS = 300  # ±5 minutes (300 seconds) total variance

# Keep your existing message variations and categories
message_variations = { ... }  # Your existing message variations
hourly_categories = [ ... ]   # Your existing category rotation

def get_random_message(category):
    """Get a random message from the specified category."""
    return random.choice(message_variations[category])

def simulate_typing(channel_id, duration=3):
    """Simulate typing in the channel with timeout."""
    typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
    try:
        response = requests.post(typing_url, headers={'Authorization': TOKEN}, timeout=2)
        if response.status_code != 204:
            print(f"Typing simulation warning: {response.status_code}")
    except Exception as e:
        print(f"Typing simulation error: {e}")
    time.sleep(duration)

def send_message(content):
    """Send message to Discord channel."""
    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    try:
        response = requests.post(
            url,
            headers={'Authorization': TOKEN, 'Content-Type': 'application/json'},
            json={'content': content},
            timeout=5
        )
        if response.status_code == 200:
            print(f"Message sent: {content[:50]}...")
        else:
            print(f"Message send error: {response.status_code}")
    except Exception as e:
        print(f"Message send failed: {e}")

def send_scheduled_messages():
    """Main message sending logic."""
    try:
        # Get current hour in UTC (adjust if needed)
        now = datetime.datetime.now()
        current_hour = now.hour
        
        # For non-UTC timezones, adjust with:
        # current_hour = (now.hour + TIMEZONE_OFFSET) % 24
        
        hour_index = current_hour % 5
        categories = hourly_categories[hour_index]
        
        print(f"Processing hour {current_hour} (index {hour_index}) with categories: {categories}")
        
        for category in categories:
            message = get_random_message(category)
            simulate_typing(CHANNEL_ID, duration=2)
            send_message(message)
            time.sleep(random.uniform(0.5, 1.5))
            
    except Exception as e:
        print(f"Error in message sending: {e}")
        raise

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    try:
        # Add random delay for variance
        delay = random.randint(0, VARIANCE_SECONDS)
        print(f"Applying variance delay: {delay} seconds")
        time.sleep(delay)
        
        send_scheduled_messages()
        return {'statusCode': 200, 'body': 'Messages sent successfully'}
        
    except Exception as e:
        print(f"Lambda handler error: {e}")
        return {'statusCode': 500, 'body': 'Error processing messages'}