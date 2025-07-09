"""
Simple Gun Control Keywords Twitter Analysis Script with Replies
"""

import os
import sys
import time
import json
import csv
from datetime import datetime
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.common.exceptions import NoSuchElementException

# Load environment variables
load_dotenv()

# Get credentials from .env
TWITTER_MAIL = "dominiclim@ucsb.edu"
TWITTER_USERNAME = "ilychiikawa"
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
HEADLESS = os.getenv('HEADLESS', 'no')


# print(TWITTER_USERNAME)
print(f"📧 Using credentials for: {TWITTER_USERNAME}")
print(f"🖥️  Headless mode: {HEADLESS}")

# Import the existing scraper
sys.path.append('./scraper')
from twitter_scraper import Twitter_Scraper

# Gun Control Keywords
keywords = [
   "gun control",
   "2nd amendment", 
   "second amendment",
   "NRA",
   "AR-15",
   "assault weapon",
   "gun rights",
   "gun reform",
   "school shooting",
   "background checks"
]

# def scrape_replies(tweet_url, max_replies=100):
#    """Simple reply scraper"""
#    browser_option = FirefoxOptions()
#    browser_option.add_argument("--no-sandbox")
#    if HEADLESS.lower() == 'yes':
#        browser_option.add_argument("--headless")
   
#    driver = webdriver.Firefox(options=browser_option)
#    replies = []
   
#    try:
#        # Quick login
#        driver.get("https://twitter.com/i/flow/login")
#        time.sleep(3)
       
#        # Username
#        username_field = driver.find_element("xpath", "//input[@autocomplete='username']")
#        username_field.send_keys(TWITTER_USERNAME)
#        username_field.send_keys("\n")
#        time.sleep(3)
       
#        # Handle verification
#        try:
#            verification_field = driver.find_element("xpath", "//input[@data-testid='ocfEnterTextTextInput']")
#            verification_field.send_keys(TWITTER_USERNAME.replace('@', ''))
#            verification_field.send_keys("\n")
#            time.sleep(3)
#        except:
#            pass
       
#        # Password
#        password_field = driver.find_element("xpath", "//input[@autocomplete='current-password']")
#        password_field.send_keys(TWITTER_PASSWORD)
#        password_field.send_keys("\n")
#        time.sleep(5)
       
#        # Go to tweet
#        driver.get(tweet_url)
#        time.sleep(5)
       
#        # Scroll and collect replies
#        for _ in range(10):  # 10 scrolls max
#            reply_elements = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')[1:]  # Skip main tweet
           
#            for element in reply_elements:
#                try:
#                    # Get reply text
#                    content_element = element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
#                    content = content_element.text
                   
#                    # Get user
#                    user_element = element.find_element(By.CSS_SELECTOR, '[data-testid="User-Name"] span')
#                    user = user_element.text
                   
#                    reply_data = {
#                        'user': user,
#                        'content': content,
#                        'parent_tweet_url': tweet_url
#                    }
                   
#                    if reply_data not in replies and content:
#                        replies.append(reply_data)
#                        if len(replies) >= max_replies:
#                            break
                           
#                except:
#                    continue
           
#            if len(replies) >= max_replies:
#                break
               
#            # Scroll down
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#            time.sleep(2)
   
#    except Exception as e:
#        print(f"Reply scraping error: {e}")
   
#    finally:
#        driver.quit()
   
#    return replies

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Scrape each keyword
for keyword in keywords:
   print(f"\n🔍 Scraping: {keyword}")
   
   scraper = Twitter_Scraper(
       mail=TWITTER_MAIL,
       username=TWITTER_USERNAME,
       password=TWITTER_PASSWORD,
       headlessState=HEADLESS
   )
   
   scraper.login()
   scraper.scrape_tweets(
       max_tweets=1000,
       scrape_query=f'"{keyword}"',
    #    scrape_poster_details=True
   )
   
   keyword_safe = keyword.replace(" ", "_").replace('"', '')
   tweets = scraper.get_tweets()
   
   if tweets:
       # Save tweets
       scraper.save_to_csv()
       
    #    # Rename tweet file
    #    import glob
    #    latest_file = max(glob.glob("./tweets/*.csv"), key=os.path.getctime)
    #    new_name = f"./tweets/{keyword_safe}_{timestamp}_{len(tweets)}_tweets.csv"
    #    os.rename(latest_file, new_name)
    #    print(f"✅ Saved {len(tweets)} tweets to {new_name}")
       
    #    # Get replies from top 10 most liked tweets
    #    all_replies = []
    #    top_tweets = sorted(tweets, key=lambda x: x[7] if x[7] else 0, reverse=True)[:10]  # Sort by likes
       
    #    for i, tweet in enumerate(top_tweets):
    #        tweet_url = tweet[13]  # Tweet link is at index 13
    #        if tweet_url:
    #            print(f"💬 Getting replies for tweet {i+1}/10...")
    #         #    replies = scrape_replies(tweet_url, max_replies=50)
    #         #    all_replies.extend(replies)
    #            time.sleep(3)
       
    #    # Save replies
    #    if all_replies:
    #        replies_file = f"./tweets/{keyword_safe}_{timestamp}_{len(all_replies)}_replies.csv"
    #        with open(replies_file, 'w', newline='', encoding='utf-8') as f:
    #            writer = csv.DictWriter(f, fieldnames=['user', 'content', 'parent_tweet_url'])
    #            writer.writeheader()
    #            writer.writerows(all_replies)
    #        print(f"✅ Saved {len(all_replies)} replies to {replies_file}")
   
   scraper.driver.quit()
   time.sleep(5)

print("\n🎯 All keywords scraped with replies!")