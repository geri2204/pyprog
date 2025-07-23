Fájlmásoló lista alapján [program] – Dokumentáció és Használati útmutató

#################[Adatok és Kapcsolat]#################

Program neve: Fájlmásoló lista alapján
Verzió: 1.0
Készítette: Hafner Gergő László
Elérhetőség: hafner.gergo.laszlo@mvm.hu

#################[A program célja]#################

Ez a Python-alapú, grafikus felületű (GUI) alkalmazás lehetővé teszi, 
hogy egy szöveges fájlban megadott fájlnevek alapján fájlokat másoljunk át egy forrásmappából egy célmappába.

#################[Rendszerkövetelmények]#################

A program egyszerűen futtatható '.exe' állományba lett tömörítve, így nem igényel Python IDE-t.
Speciális igények: Nem igényel külső csomagokat (csak beépített Python modulokat használ)
Platform: Windows, Linux

#################[Használati eset]#################

Ha van egy listád (pl. lista.txt), amely tartalmaz fájlneveket ilyen formában:
"
fajl1.xml
fajl2.xml
dokumentum123.xml
"

És ezek a fájlok egy mappában találhatók (pl. C:\Forras), 
akkor a program segítségével könnyedén átmásolhatod ezeket egy másik mappába (pl. C:\Cel), 
anélkül, hogy egyesével kellene keresni őket.

#################[Program indítása]#################

Windows: A program mappájában keresse meg a 'dist' nevű mappát,
majd a benne található 'file_move' mappában található a 'file_move.exe' alkalmazás futtatható állománya.

Linux: Konzolon/Terminálba kiadva a következő parancsot, egyszerűen futtatható:
python3 file_move.py

#################[A program kezelése – GUI elemek]#################

# Forrás mappa:
Tallózd be azt a mappát, ahol a listában szereplő fájlok fizikailag találhatók.

# Cél mappa:
Add meg, hová szeretnéd másolni a fájlokat.

# Lista fájl (.txt):
Tallózd be azt a .txt fájlt, amely soronként tartalmazza a fájlneveket (pl. valami.xml formátumban).

# Másolás indítása:
Ha minden mezőt kitöltöttél, kattints erre a gombra. A program elindítja a másolást, és tájékoztat, hogy:

A) hány fájlt sikerült másolni,
B) hány fájl hiányzik (pl. nincs meg a forrásmappában).

#################[A lista fájl formátuma]#################

A fájlnév minden sorban külön szerepeljen.

Nem tartalmazhat elérési utat, csak magát a fájlnevet.

Példa:
"
dokumentum1.xml
dokumentum2.xml
alapadatok.xml
"

#################[!!! FIGYELEM: Fontos megjegyzések]#################

@ A program nem módosítja az eredeti fájlokat – csak másolást végez.
@ Ha a célmappában már létezik az adott fájl, felülírja azt.
@ A program csak azokat a fájlokat másolja, amelyek szerepelnek a listában ÉS megtalálhatók a forrásmappában.
@ A hibás vagy hiányzó fájlokról a végén a felhasználó jelentést kap.

#################[Technikai részletek]#################

A program Python nyelven készült, és a következő beépített modulokat használja:

- tkinter – a grafikus felülethez
- os – fájlrendszer-kezeléshez
- shutil – másolási művelethez

A másolást a shutil.copy2() függvény végzi, amely megőrzi az eredeti fájl módosítási dátumát is.

A program mappahierarchiája:

file_move
	|- build
	|- dist
		|- file_move
			|- _internal
			|- file_move.exe
	|- file_move.py
	|- file_move.pyw
	|- file_move.spec

Érdemes a 'dist' mappán belül a 'file_move' mappában található 'file_move.exe' fájlt az asztalra parancsikonként elhelyezni.
Ennek egy tetszőleges módja a következő:
	1) Jobbklikk a futtatható állományon
	2) (Windows 11 alatt:) További lehetőségek megjelenítése
	3) Küldés > Aszatl (parancsikon létrehozása)

-----------------[Teljesítmény és hatékonyság]-----------------

Műveleti lépések:
A program futása során a következő lépéseket hajtja végre, sorrendben:

1.) Beolvassa a .txt fájlt, soronként.
2.) Minden fájlnévhez:
	- Összeállítja a teljes elérési útvonalat a forrásmappában.
	- Ellenőrzi, hogy a fájl létezik-e.
	- Ha igen, átmásolja a célmappába.
	- Ha nem, jegyzi, hogy hiányzik.

3.) A futás végén összesítést ad: sikeres és hiányzó fájlok száma.

-----------------[Futási idő]-----------------

# A program futási ideje lineáris a lista méretéhez képest:
  O(n), ahol n a listában szereplő fájlnevek száma.

# Példák (becsült értékek SSD-t és helyi fájlrendszert feltételezve):
	- 10 fájl: ~0,1–0,2 másodperc (a fájlok méretétől függően)
	- 100 fájl: ~1–2 másodperc (a fájlok méretétől függően)
	- 1000 fájl: ~5–10 másodperc (a fájlok méretétől függően)
	- 10 000 fájl: akár ~1 perc (a fájlok méretétől függően)

# A tényleges időt több tényező befolyásolja:
	- fájlok mérete (pl. néhány kB vagy több MB)
	- háttértár sebessége (HDD vs SSD)
	- CPU és RAM
	- másolás közbeni rendszerterhelés

-----------------[Memóriahasználat]-----------------

A memóriaigény minimális, mivel a lista fájlt egyszer beolvassa, és azután soronként dolgozza fel a fájlokat. Nincs nagy adathalmaz betöltve a memóriába.

-----------------[Optimalizáció]-----------------

@ A program csak azokat a fájlokat vizsgálja, amelyek szerepelnek a listában → nincs teljes könyvtár-bejárás.
@ Nem használ párhuzamosítást, de kis és közepes listáknál ez nem szükséges.
@ A shutil.copy2 használata biztosítja, hogy a fájl metaadatai (pl. módosítási idő) is megmaradjanak, miközben hatékonyan másol.

#################[Tippek]#################

@ Ha sok fájlt kell másolnod, ellenőrizd, hogy a lista .txt fájl nem tartalmaz üres sorokat vagy elírásokat.
@ Célszerű előbb a lista alapján ellenőrizni a fájlneveket egy szövegszerkesztővel (pl. Notepad++).

#################[Kapcsolat / Támogatás]#################

Ha hibát találsz a program működésében vagy kérdésed van, fordulj a fejlesztőhöz:
hafner.gergo.laszlo@mvm.hu

#################[Vége]#################

Köszönöm, hogy használod a programot!
Egyszerű, gyors, megbízható megoldás fájlok másolására listák alapján.