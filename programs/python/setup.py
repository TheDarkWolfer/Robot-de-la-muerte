import os, time

os.system("cls")

try:
    os.system("pip --version")
    os.system("python --version")
except:
    print("Please install python 3.X in order to proceed")
    print("Use 'sudo apt-get install python3'")
    input("\n Press enter to close window")

print(f"Installing keyboard module...")
time.sleep(0.25)
os.system("pip install keyboard")
time.sleep(0.5)

time.sleep(1)
print(f"Installing Opencv2-python module...")
time.sleep(0.25)
os.system("pip install opencv-python")
time.sleep(0.5)

time.sleep(1)
print(f"Installing pandas module...")
time.sleep(0.25)
os.system("pip install pandas")
time.sleep(0.5)

input("Press enter to close window")