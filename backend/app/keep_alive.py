"""
Keep Render instance awake by pinging it every 14 minutes
Prevents the 50-second cold start delay
"""
import requests
import os
from threading import Thread
from datetime import datetime
import time

def keep_alive():
    """Ping API every 14 minutes to prevent spin down"""
    # Get the API URL from environment variable
    api_url = os.getenv('RENDER_EXTERNAL_URL', 'http://localhost:5050') + '/api/test'
    
    print(f"✅ Keep-alive service started for: {api_url}")
    
    while True:
        try:
            # Sleep 14 minutes (840 seconds)
            # Render spins down after 15 min, so we ping before that
            time.sleep(14 * 60)
            
            # Ping the API
            response = requests.get(api_url, timeout=30)
            
            if response.status_code == 200:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Keep-alive ping successful")
            else:
                print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ⚠️ Keep-alive ping returned: {response.status_code}")
                
        except Exception as e:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Keep-alive ping failed: {e}")

def start_keep_alive():
    """Start keep-alive in background thread"""
    thread = Thread(target=keep_alive, daemon=True)
    thread.start()
    print("🚀 Keep-alive background service initialized!")
