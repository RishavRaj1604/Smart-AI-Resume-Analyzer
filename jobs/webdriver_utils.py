"""
Utility functions for webdriver setup and management
Mac-safe, Windows-safe, Python 3.11 compatible
"""

import os
import platform
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Try webdriver-manager
try:
    from webdriver_manager.chrome import ChromeDriverManager
    webdriver_manager_available = True
except ImportError:
    webdriver_manager_available = False


def get_chromedriver_path():
    """Return chromedriver path if already installed"""
    home = os.path.expanduser("~")
    possible_paths = [
        os.path.join(home, ".chromedriver", "chromedriver"),
        "/usr/local/bin/chromedriver",
        "/opt/homebrew/bin/chromedriver",
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path
    return None


def setup_webdriver():
    """
    Setup Chrome webdriver with safe fallbacks.
    Works on Mac (M1), Linux, Windows.
    """

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # Method 1 — Use existing chromedriver if available
    chromedriver_path = get_chromedriver_path()
    if chromedriver_path:
        try:
            service = Service(chromedriver_path)
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception:
            pass

    # Method 2 — Use webdriver-manager (recommended)
    if webdriver_manager_available:
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except Exception:
            pass

    # Method 3 — Try system Chrome directly
    try:
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        st.error("Failed to start Chrome WebDriver.")
        st.error(str(e))

    return None
