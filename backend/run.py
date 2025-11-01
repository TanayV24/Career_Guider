from app import create_app
import os

# Import keep-alive service
try:
    from app.keep_alive import start_keep_alive
    KEEP_ALIVE_AVAILABLE = True
except ImportError:
    KEEP_ALIVE_AVAILABLE = False
    print("⚠️ Keep-alive service not available")

app = create_app()

if __name__ == '__main__':
    # Start keep-alive service only in production (Render)
    if os.getenv('RENDER_EXTERNAL_URL') and KEEP_ALIVE_AVAILABLE:
        print("🌐 Production environment detected (Render)")
        start_keep_alive()
    else:
        print("💻 Local development environment")
    
    # Get port from environment (Render provides this)
    port = int(os.environ.get('PORT', 5050))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
