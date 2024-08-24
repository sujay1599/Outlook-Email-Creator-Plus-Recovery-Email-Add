# Microsoft Account Creator Automation

This project automates the process of creating Microsoft Outlook accounts and adding recovery emails. It leverages the Playwright library to interact with the web interface of the Outlook account creation page and login page. The program includes several scripts that work together to create accounts, manage recovery emails, and handle CAPTCHA challenges manually.

## Features

- **Account Creation**: Automatically fills out the Outlook signup form with randomly generated personal information and a secure password.
- **CAPTCHA Handling**: Prompts the user to manually solve CAPTCHAs.
- **Recovery Email Setup**: Adds a recovery email to newly created accounts.
- **Credential Storage**: Saves the credentials of created accounts to a CSV file for later use.

## Prerequisites

- Python 3.8 or higher
- Playwright Python library
- CSV file management
- Basic understanding of Python and web automation

## Setup

1. **Install Required Libraries**:
   Ensure you have Playwright and other dependencies installed:
   ```bash
   pip install playwright
   playwright install
   ```

2. **Run Config Script**:
   Before running the main scripts, execute `config.py` to set up the necessary files:
   ```bash
   python config.py
   ```
   This will create `accounts.txt` and `created_accounts.csv` if they don't already exist.

3. **Configure the Settings**:
   Edit `config.py` to customize settings, such as proxy usage and the recovery email:
   ```python
   class Config:
       ADD_RECOVERY_EMAIL = True
       RECOVERY_EMAIL = 'INSERT_EMAIL_HERE'
       # other settings...
   ```

## Usage

### 1. Account Creation

To create a new Microsoft Outlook account:

- Run `main.py`:
  ```bash
  python main.py
  ```
  - This script will open an incognito browser, fill out the account creation form, and save the credentials to `created_accounts.csv`.
  - You will need to manually solve any CAPTCHA challenges and press Enter to continue.

### 2. Adding Recovery Email

To log into the newly created account and add a recovery email:

- Run `auth.py`:
  ```bash
  python auth.py
  ```
  - This script will log into the most recently created account using the credentials stored in `created_accounts.csv`.
  - The script will then navigate to the account recovery page, where it will prompt you to manually enter the recovery code received by email.

### 3. Manually Navigating the Browser

- Both `main.py` and `auth.py` scripts will leave the browser open after completing their tasks. This allows you to manually perform any additional steps or verify the actions taken by the scripts.

## File Descriptions

- **`config.py`**: Contains configuration settings and a setup function to initialize necessary files.
- **`main.py`**: Automates the account creation process.
- **`auth.py`**: Logs into the created account and adds a recovery email.

## Additional Notes

- **Manual Intervention**: The script pauses at certain points (like CAPTCHA challenges) to allow manual intervention.
- **Browser Interaction**: The scripts are designed to run in a non-headless browser for easier debugging and manual intervention.
- **Security**: Ensure that the recovery email is set up properly to secure your new accounts.

## Troubleshooting

- **Issues with Selectors**: If the script fails to find or interact with certain elements, verify that the selectors used in the scripts match those on the web page.
- **CAPTCHA Challenges**: The script cannot solve CAPTCHAs; you will need to do this manually.

## Future Improvements

- **Automated CAPTCHA Solving**: Integrate third-party services to automate CAPTCHA solving.
- **Enhanced Error Handling**: Improve error handling and logging for better debugging.

