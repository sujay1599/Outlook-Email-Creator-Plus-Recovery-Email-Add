from playwright.async_api import async_playwright
import asyncio
import random
import csv
from datetime import datetime
from config import Config

async def generate_personal_info():
    names = []
    with open(Config.NAMES_FILE, "r") as f:
        names = f.read().splitlines()

    random_first_name = names[random.randint(0, len(names) - 1)].strip()
    random_last_name = names[random.randint(0, len(names) - 1)].strip()
    username = f"{random_first_name}{random_last_name}{random.randint(0, 9999)}"
    birth_day = str(random.randint(1, 28))
    birth_month = str(random.randint(1, 12))
    birth_year = str(random.randint(1990, 1999))

    return {
        "username": username,
        "randomFirstName": random_first_name,
        "randomLastName": random_last_name,
        "birthDay": birth_day,
        "birthMonth": birth_month,
        "birthYear": birth_year
    }

async def generate_password():
    words = []
    with open(Config.WORDS_FILE, "r") as f:
        words = f.read().splitlines()

    first_word = words[random.randint(0, len(words) - 1)].strip()
    second_word = words[random.randint(0, len(words) - 1)].strip()
    return f"{first_word}{second_word}{random.randint(0, 9999)}!"

async def delay(time_ms):
    await asyncio.sleep(time_ms / 1000)

async def write_credentials(email, password):
    account = f"{email}:{password}"
    print(account)
    
    # Save to a text file
    with open(Config.ACCOUNTS_FILE, 'a') as f:
        f.write(f"\n{account}")
    
    # Save to a CSV file with date
    csv_file = 'created_accounts.csv'
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=':')
        writer.writerow([email, password, datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

async def start():
    async with async_playwright() as p:
        # Launch browser in incognito mode (private context)
        browser = await p.chromium.launch(headless=False)
        
        # Create a new incognito context (similar to guest mode)
        context = await browser.new_context()

        # Open a new page within the incognito context
        page = await context.new_page()
        
        await create_account(page)
        
        # Do not close the browser; keep it open for further interactions
        print("Account creation flow completed. Browser will remain open for further actions.")

async def create_account(page):
    await page.goto("https://outlook.live.com/owa/?nlp=1&signup=1")
    await page.wait_for_selector(SELECTORS['USERNAME_INPUT'])

    personal_info = await generate_personal_info()

    await page.fill(SELECTORS['USERNAME_INPUT'], personal_info['username'])
    await page.press(SELECTORS['USERNAME_INPUT'], "Enter")

    password = await generate_password()
    await page.wait_for_selector(SELECTORS['PASSWORD_INPUT'])
    await page.fill(SELECTORS['PASSWORD_INPUT'], password)
    await page.press(SELECTORS['PASSWORD_INPUT'], "Enter")

    await page.wait_for_selector(SELECTORS['FIRST_NAME_INPUT'])
    await page.fill(SELECTORS['FIRST_NAME_INPUT'], personal_info['randomFirstName'])
    await page.fill(SELECTORS['LAST_NAME_INPUT'], personal_info['randomLastName'])
    await page.press(SELECTORS['LAST_NAME_INPUT'], "Enter")

    await page.wait_for_selector(SELECTORS['BIRTH_DAY_INPUT'])
    await delay(1000)
    await page.select_option(SELECTORS['BIRTH_DAY_INPUT'], personal_info['birthDay'])
    await page.select_option(SELECTORS['BIRTH_MONTH_INPUT'], personal_info['birthMonth'])
    await page.fill(SELECTORS['BIRTH_YEAR_INPUT'], personal_info['birthYear'])
    await page.press(SELECTORS['BIRTH_YEAR_INPUT'], "Enter")
    email = await page.text_content(SELECTORS['EMAIL_DISPLAY'])

    # Save credentials immediately after account creation
    await write_credentials(email, password)

    print("Account created and details saved. Proceeding to CAPTCHA...")

    print("Doing Captcha...")

    # Wait for the user to solve the CAPTCHA manually
    input("Please solve the CAPTCHA and press Enter to continue...")

    # Try to find the decline button, if it exists
    try:
        await page.wait_for_selector(SELECTORS['DECLINE_BUTTON'], timeout=5000)
        await page.click(SELECTORS['DECLINE_BUTTON'])
    except Exception as e:
        print("Decline button not found, proceeding to the next step.")

    # Move on to the next step regardless of whether the decline button was clicked or not
    try:
        await page.wait_for_selector(SELECTORS['OUTLOOK_PAGE'], timeout=30000)
    except Exception as e:
        print("Main page not loaded, proceeding anyway.")

    # After CAPTCHA, press the specified button using the provided XPath
    try:
        await page.wait_for_selector('xpath=/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/form/div[3]/div[2]/div/div[1]/button', timeout=30000)
        await page.click('xpath=/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/form/div[3]/div[2]/div/div[1]/button')
        print("Button pressed successfully.")
    except Exception as e:
        print("Button could not be pressed, please check manually.")

    if Config.ADD_RECOVERY_EMAIL:
        await page.goto("https://account.live.com/proofs/Manage")
        await page.wait_for_selector(SELECTORS['RECOVERY_EMAIL_INPUT'])
        await page.fill(SELECTORS['RECOVERY_EMAIL_INPUT'], Config.RECOVERY_EMAIL)
        await page.press(SELECTORS['RECOVERY_EMAIL_INPUT'], "Enter")

        await page.wait_for_selector(SELECTORS['EMAIL_CODE_INPUT'])
        # Simulate manual input of the recovery email code
        input("Please check your recovery email for the code, enter it manually in the browser, and press Enter here to continue...")
        await page.press(SELECTORS['EMAIL_CODE_INPUT'], "Enter")
        await page.wait_for_selector(SELECTORS['AFTER_CODE'])

    print("Account creation complete. Please manually navigate and perform the necessary actions.")

SELECTORS = {
    'USERNAME_INPUT': '#usernameInput',
    'PASSWORD_INPUT': '#Password',
    'FIRST_NAME_INPUT': '#firstNameInput',
    'LAST_NAME_INPUT': '#lastNameInput',
    'BIRTH_DAY_INPUT': '#BirthDay',
    'BIRTH_MONTH_INPUT': '#BirthMonth',
    'BIRTH_YEAR_INPUT': '#BirthYear',
    'EMAIL_DISPLAY': '#userDisplayName',
    'DECLINE_BUTTON': '#declineButton',
    'OUTLOOK_PAGE': '#mainApp',
    'RECOVERY_EMAIL_INPUT': '#EmailAddress',
    'EMAIL_CODE_INPUT': '#iOttText',
    'AFTER_CODE': '#idA_SAOTCS_LostProofs'
}

if __name__ == "__main__":
    # Ensure necessary files are set up before starting
    Config.setup_files()
    
    # Run the main process
    asyncio.run(start())
