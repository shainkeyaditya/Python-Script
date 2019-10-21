
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import uuid
import socket
import getpass
import platform
import netifaces

# joins elements of getnode() after each 2 digits.
import getmac as getmac
import os,sys


scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("habilelabs_credentials.json", scope)

client = gspread.authorize(creds)

sheet = client.open("System-info-sheet").sheet1

data = sheet.get_all_records()

row = sheet.row_values(3)
col = sheet.col_values(3)
cell = sheet.cell(1, 2).value


def getMachine_addr():
    command = ''
    os_type = sys.platform.lower()
    print('ostype', os_type)
    if "win32" == os_type:
        command = "wmic bios get serialnumber"
        print('window serial num')
    elif "linux" == os_type:
        command = "sudo dmidecode -s system-serial-number"
    elif "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    return os.popen(command).read().replace("\n", "").replace("	", "").replace(" ", "")


dupl_serial_number = getMachine_addr()
serial_number = dupl_serial_number[12:]

print(netifaces.interfaces())
list1 = []
mac_address = netifaces.gateways()
print("The MAC address in formatted way is : ", end="")
system_mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff)
                for i in range(0, 8 * 6, 8)][::-1])
host_name = socket.gethostname()
user_name = getpass.getuser()
list1.append(host_name)
username = getpass.getuser()
list1.append(user_name)
machine = platform.machine()

list1.append(machine)
current_wifi_address = getmac.get_mac_address()
list1.append(current_wifi_address)
list1.append(system_mac_address)
processor = platform.processor()
list1.append(processor)
list1.append(serial_number)
sheet.insert_row(list1, 9)
