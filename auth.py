import asyncio
import csv
import random
from time import sleep
from playwright.async_api import async_playwright
from config import Config

async def get_last_created_account():
    with open('created_accounts.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=':')
        last_row = None
        for row in reader:
            last_row = row
        if last_row:
            email, password, _ = last_row
            return email, password
        return None, None

async def add_recovery_email(email, password):
    async with async_playwright() as p:
        # Launch the browser in incognito mode (non-headless for debugging)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Open a new page in incognito mode
        page = await context.new_page()

        # Log in to the account
        await page.goto("https://login.live.com/")
        await page.fill('input[name="loginfmt"]', email)
        await page.press('input[name="loginfmt"]', "Enter")

        await page.wait_for_selector('input[name="passwd"]')
        await page.fill('input[name="passwd"]', password)
        await page.press('input[name="passwd"]', "Enter")

        # Add a random wait between 10-15 seconds
        sleep(random.uniform(10, 15))

        # Wait for the page to load and press the specified button
        try:
            await page.wait_for_selector('xpath=/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/form/div[3]/div[2]/div/div[1]/button', timeout=10000)
            await page.click('xpath=/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/form/div[3]/div[2]/div/div[1]/button')
            print("Button pressed successfully.")
        except Exception as e:
            print("Button could not be pressed. Proceeding with recovery email setup.")

        # Add a random wait between 10-15 seconds
        sleep(random.uniform(10, 15))

        # Go to the account recovery page
        await page.goto("https://account.live.com/proofs/Manage")
        
        # Increase timeout and try to locate the specific element to interact with
        try:
            await page.wait_for_selector('#idDiv_SAOTCS_Proofs > div > div > div > div.table-cell.text-left.content', timeout=60000)  # Increased timeout to 60 seconds
            print("Recovery email element found.")
            
            # Click the element containing the recovery email
            await page.click('#idDiv_SAOTCS_Proofs > div > div > div > div.table-cell.text-left.content')
            print("Recovery email element clicked successfully.")
            
            # Wait for the user to manually input the code and press Enter
            input("Please check your recovery email for the code, enter it manually in the browser, and press Enter here to continue...")
            
            # Resume script after the user has pressed Enter
            await page.wait_for_selector(SELECTORS['EMAIL_CODE_INPUT'], timeout=60000)
            await page.press(SELECTORS['EMAIL_CODE_INPUT'], "Enter")
            await page.wait_for_selector(SELECTORS['AFTER_CODE'])
            print("Recovery email process completed successfully.")
        
        except Exception as e:
            print(f"Failed to find or interact with the recovery email element: {str(e)}")

        # Do not close the browser; keep it open for further interactions
        print("Process completed. The browser will remain open.")

SELECTORS = {
    'RECOVERY_EMAIL_INPUT': '#EmailAddress',
    'EMAIL_CODE_INPUT': '#iOttText',
    'AFTER_CODE': '#idA_SAOTCS_LostProofs'
}

if __name__ == "__main__":
    email, password = asyncio.run(get_last_created_account())
    if email and password:
        asyncio.run(add_recovery_email(email, password))
    else:
        print("No account found in the CSV file.")
