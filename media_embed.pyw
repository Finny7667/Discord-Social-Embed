import pyperclip
import re
import time
import sys
import logging
from threading import Thread

# Constants
CLIPBOARD_CHECK_INTERVAL = 0.5  # Seconds
ERROR_RETRY_INTERVAL = 5  # Seconds
LOG_FILE = 'url_transformer_error.log'

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, 
                    format='%(asctime)s: %(message)s')

# URL replacement patterns
URL_PATTERNS = [
    # Pixiv daily ranking with date (both daily and daily_r18)
    (r'https://www\.pixiv\.net/ranking\.php\?date=\d+&mode=daily(?:_r18)?#ppixiv\?(?:view=illust&)?illust_id=(\d+)&(?:view=illust&)?page=(\d+)',
     r'https://www.phixiv.net/en/artworks/\1/\2'),
    # Pixiv daily ranking without date (both daily and daily_r18)
    (r'https://www\.pixiv\.net/ranking\.php\?mode=daily(?:_r18)?#ppixiv\?(?:view=illust&)?illust_id=(\d+)&(?:view=illust&)?page=(\d+)',
     r'https://www.phixiv.net/en/artworks/\1/\2'),
    # General Pixiv to Phixiv replacement
    (r'https://www\.pixiv\.net/([^\s]+)', r'https://www.phixiv.net/\1'),
    # Twitter/X to fxtwitter
    (r'https://x\.com/([^/]+)/status/(\d+)', r'https://fixupx.com/\1/status/\2'),
    # Reddit to rxddit
    (r'https://www\.reddit\.com/([^\s]+)', r'https://www.rxddit.com/\1'),
    # Bluesky to bskyx
    (r'https://bsky\.app/([^\s]+)', r'https://bskyx.app/\1')
]

def replace_urls(text):
    """Replace URLs in the given text based on predefined patterns."""
    for pattern, replacement in URL_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text

def monitor_clipboard():
    """Monitor the clipboard for changes and replace URLs as needed."""
    last_content = ''
    while True:
        try:
            current_content = pyperclip.paste()
            if current_content != last_content:
                new_content = replace_urls(current_content)
                if new_content != current_content:
                    pyperclip.copy(new_content)
                last_content = new_content
            time.sleep(CLIPBOARD_CHECK_INTERVAL)
        except Exception as e:
            logging.error(f"An error occurred: {e}", exc_info=True)
            time.sleep(ERROR_RETRY_INTERVAL)

def main():
    """Start the clipboard monitoring thread and keep the program running."""
    clipboard_thread = Thread(target=monitor_clipboard, daemon=True)
    clipboard_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
