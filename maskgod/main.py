import sys
import time
import pyshorteners
from urllib.parse import urlparse
import re
import qrcode
import json
import os

# Colors for terminal
R = '\033[31m'  # Red
G = '\033[32m'  # Green
C = '\033[36m'  # Cyan
Y = '\033[33m'  # Yellow
W = '\033[0m'   # Reset

TOOL_NAME = "MaskGod"
VERSION = "v1.0"
AUTHOR = "Created by Nishkarsh"

BANNER = rf'''
{C}
 ███╗   ███╗ █████╗ ███████╗██╗  ██╗ ██████╗  ██████╗  ██████╗ ██████╗ 
 ████╗ ████║██╔══██╗██╔════╝██║  ██║██╔═══██╗██╔════╝ ██╔════╝██╔═══██╗
 ██╔████╔██║███████║███████╗███████║██║   ██║██║  ███╗██║     ██║   ██║
 ██║╚██╔╝██║██╔══██║╚════██║██╔══██║██║   ██║██║   ██║██║     ██║   ██║
 ██║ ╚═╝ ██║██║  ██║███████║██║  ██║╚██████╔╝╚██████╔╝╚██████╗╚██████╔╝
 ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚═════╝  
         {W}The Final Boss of URL Masking
         {Y}{TOOL_NAME} {W}- {VERSION}
         {G}{AUTHOR}{W}
'''

def print_banner():
    print(BANNER)

def loading_animation():
    spinner = ["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"]
    for _ in range(2):
        for symbol in spinner:
            sys.stdout.write(f"\r{C}Masking in progress... {symbol}{W}")
            sys.stdout.flush()
            time.sleep(0.1)
    print("\r\033[K", end='')

def mask_url(domain: str, keyword: str, target_url: str) -> str:
    parsed = urlparse(target_url)
    return f"{parsed.scheme}://{domain}-{keyword}@{parsed.netloc}{parsed.path}"

def generate_qr_code(link: str, filename="maskgod_qr.png"):
    qrcode.make(link).save(filename)
    print(f"{G}✓ QR code saved as {filename}{W}")

def save_to_file(data, filename="masked_links.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"{Y}✓ Links saved to {filename}{W}")

def validate_url(url: str) -> bool:
    """Validates the given URL to ensure it starts with http:// or https://"""
    return bool(re.match(r'^(https?://)[^\s]+$', url))

def validate_domain(domain: str) -> bool:
    """Validates the given domain format to ensure it follows a proper structure"""
    return bool(re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain))

def validate_keyword(keyword: str) -> bool:
    """Validates the keyword to ensure it does not contain spaces and is not too long"""
    return " " not in keyword and 0 < len(keyword) <= 20

def main():
    print_banner()
    print(f"{C}Welcome to {TOOL_NAME} - The Final Boss of URL Masking!{W}\n")
    print(f"{Y}Note: This tool is for educational purposes only. Use responsibly.{W}\n")
    while True:
        original_url = input(f"{G}Enter target URL (e.g., https://example.com): {W}")
        if validate_url(original_url):
            break
        print(f"{R}✗ Invalid URL. Try again.{W}")

    while True:
        domain = input(f"{Y}Enter a legit-looking domain (e.g., google.com): {W}")
        if validate_domain(domain):
            break
        print(f"{R}✗ Invalid domain format. Try again.{W}")

    while True:
        keyword = input(f"{C}Enter a keyword (e.g., login, account): {W}")
        if validate_keyword(keyword):
            break
        print(f"{R}✗ Keyword too long or contains spaces.{W}")

    
    loading_animation()
    shorteners = [
        ("TinyURL", pyshorteners.Shortener().tinyurl),
        ("Dagd", pyshorteners.Shortener().dagd),
        ("Clck.ru", pyshorteners.Shortener().clckru),
        ("Osdb", pyshorteners.Shortener().osdb),
        # These are the free ones f you want to add more: like bitly or t2m, you need to get an API key and add it here.
    ]

    results = []  

    print(f"\n{C}Original URL: {W}{original_url}\n")

  
    for name, shortener in shorteners:
        try:
            short_url = shortener.short(original_url)
            masked = mask_url(domain, keyword, short_url)
            print(f"{G}✓ {name}: {masked}{W}")
            results.append({"shortener": name, "short_url": short_url, "masked_url": masked})
        except Exception as e:
            print(f"{R}✗ Failed using {name}: {e}{W}")

   
    if results:
        generate_qr_code(results[0]["masked_url"]) 
        save_to_file(results)  

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{R}Exited by user.{W}")
    except Exception as err:
        print(f"{R}Error: {err}{W}")
