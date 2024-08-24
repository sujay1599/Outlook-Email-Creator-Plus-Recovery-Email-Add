import os
import csv

class Config:
    ADD_RECOVERY_EMAIL = True
    RECOVERY_EMAIL = 'INSERT_EMAIL_HERE'
    USE_PROXY = False
    PROXY_USERNAME = 'username'
    PROXY_PASSWORD = 'password'
    PROXY_IP = 'ip'
    PROXY_PORT = 'port'
    NAMES_FILE = 'names.txt'
    WORDS_FILE = 'words5char.txt'
    ACCOUNTS_FILE = 'accounts.txt'

    @staticmethod
    def setup_files():
        # Create accounts.txt if it doesn't exist
        if not os.path.isfile(Config.ACCOUNTS_FILE):
            with open(Config.ACCOUNTS_FILE, 'w') as f:
                f.write('')  # Create an empty file

        # Create created_accounts.csv if it doesn't exist
        csv_file = 'created_accounts.csv'
        if not os.path.isfile(csv_file):
            with open(csv_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=':')
                writer.writerow(['email', 'password', 'date'])  # Write header

# Run the setup when config.py is executed
if __name__ == "__main__":
    Config.setup_files()
    print("Necessary files have been set up.")
