from pywinauto import Desktop, Application
import pyautogui
from tkinter import messagebox
import time
from pywinauto.keyboard import send_keys
import pyperclip
import datetime

# Ablak keresés/beállítás
def get_window(name):
    """Ablak keresése a megadott név alapján."""
    for win in Desktop(backend="win32").windows():
        if name in win.window_text() and win.window_text() != "":
            return win
    return None

# Többszörös billentyűparancsok kiadása
def send_cmd(n, cmd, delay=0.2):
    """Többszörös billentyűparancsok kiadása."""
    for _ in range(n):
        send_keys(cmd)
        time.sleep(delay)

# Kép megtalálása és rákattintás
def find_and_click(image_path):
    """Kép megtalálása és rákattintás."""
    location = pyautogui.locateOnScreen(image_path, confidence=0.8)
    if location is not None:
        pyautogui.click(pyautogui.center(location))
        print(f'Rákattintott: {image_path}')
    else:
        print(f'{image_path} - GUI elem nem található!')

# Hibakezelés
def check_error():
    """Hiba kezelése."""
    send_keys('{TAB}')
    send_keys('{ENTER}')
    pyperclip.copy("Hibás\n")

def check_missing():
    """Hiányzó elem kezelése."""
    find_and_click('C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\back.png')

# Fő függvény
def run(ertek, outFile, open=False):
    """Fő folyamat végrehajtása."""
    wait_time = 0.1

    # Ablak keresése és fókuszálás
    window = get_window("EMP(1)/102 Bekötés megjelenítése: kezdő kép")
    if window and not open:
        print(f"Célablak megtalálva: {window.window_text()}")
        window.set_focus()
        time.sleep(wait_time)
        send_keys('^f')
        print("Ctrl+F kombináció leütve")
    elif not open:
        print("Célablak nem található")
        return True

    print("Folyamat befejezve")

    window = get_window("EMP(1)/102 Data Finder(adatkereső): Közműbekötés keresése")
    if window:
        print(f"Célablak megtalálva: {window.window_text()}")
        window.set_focus()
        time.sleep(wait_time)

        find_and_click('C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\mas kereso kriteriumok.png')
        time.sleep(1)
        print("'Más kereső kritérium' - ablakra kattint!")

        find_and_click('C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\mer pont megn.png')
        send_keys('{TAB}')
        print("'Mér.pont megn.' - mezőt megtalálva!")

        send_keys('^a')
        pyperclip.copy(ertek)
        send_keys('^v')
        print("'POD-érték' - BEMÁSOLVA!")

        send_keys('{ENTER}')

    time.sleep(0.5)

    window1 = get_window("EMP(1)/102 Bekötés megjelenítése:")
    if window1:
        print(f"Célablak megtalálva: {window1.window_text()}")
        window1.set_focus()
        time.sleep(wait_time)

        send_keys('^a')
        print("'Bekötés' - KIJELÖLVE!")
        time.sleep(wait_time)
        send_keys('^c')
        print("'Bekötés' - KIMÁSOLVA!")

        outFile.write(pyperclip.paste() + "\t")
        time.sleep(wait_time)
        pyautogui.scroll(-4000)

        try:
            find_and_click('C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\idoszeletek.png')
        except Exception as e:
            print(f"Hibás POD: {e}")
            check_error()
            outFile.write("Hibás\n")
            return True
        else:
            print("'Időszeletek' - Gomb lenyomva")
            time.sleep(1)

            try:
                find_and_click('C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\ukszeg.png')
            except Exception as e:
                outFile.write("Hibás\n")
                check_missing()
                return False

            print("'ÜK. szegm.' - Oszlop kiválasztva")
            send_keys('{DOWN}')
            send_keys('^y')
            send_keys('^c')
            outFile.write(pyperclip.paste() + "\n")
            print("'ÜK. szegm.' - Érték sikeresen kimásolva!")

            find_and_click('C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\close.png')
            time.sleep(wait_time)
            print("'Időszeletek' - Felugró ablak bezárva!")

            find_and_click('C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\back.png')
        
        print("Visszalépés megtörtént!")
        time.sleep(wait_time)
        return False

def main():
    start_time = datetime.datetime.now()

    app = Application(backend="win32").start(r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe")
    print("SAP Logon elindult, várunk a keresett ablak megnyitására...")

    target_title = "EMP(1)/102 Bekötés megjelenítése: kezdő kép"
    window = None
    while not window:
        window = get_window(target_title)
        time.sleep(1)

    if window:
        print(f"Célablak megtalálva: {window.window_text()}")
        window.set_focus()
        time.sleep(0.5)
    else:
        print("Célablak nem található.")
        return

    file_path = "C:\\Users\\G3909\\Desktop\\SAPLogon_autorun\\forras.txt"
    with open(file_path, "r") as file, open("output.txt", "a") as output:
        lines = file.readlines()
        error = False

        for line in lines:
            error = run(line.strip(), output, error)
            time.sleep(0.1)

    messagebox.showinfo(
        title="Finished the process",
        message=f"Running time was:\n{datetime.datetime.now() - start_time}"
    )

if __name__ == "__main__":
    main()
