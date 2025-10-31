from supabase import create_client, Client
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_ANON_KEY = os.getenv('SUPABASE_ANON_KEY')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

# Debug: Print to verify (remove in production)
print(f"Supabase URL loaded: {SUPABASE_URL is not None}")
print(f"Anon Key loaded: {SUPABASE_ANON_KEY is not None}")

# Check if environment variables are loaded
if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError(
        "Supabase credentials not found! Make sure:\n"
        "1. backend/.env file exists\n"
        "2. SUPABASE_URL is set\n"
        "3. SUPABASE_ANON_KEY is set"
    )

# Create Supabase clients
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY) if SUPABASE_SERVICE_KEY else None
except Exception as e:
    print(f"Error creating Supabase client: {e}")
    raise

def get_supabase():
    """Get Supabase client for normal operations"""
    return supabase

def get_supabase_admin():
    """Get Supabase admin client for privileged operations"""
    if not supabase_admin:
        raise ValueError("Service key not configured")
    return supabase_admin
