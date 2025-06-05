import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

nazwa_pliku="kontakty.json"

#wqczytywanie danych
def wczytywanie_danych():
    try:
        with open("kontakty.json", "r", encoding="utf-8") as plik:
            return json.load(plik)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


#zapisywanie danych do pliku         
def zapisywanie_danych(dane):
    with open("kontakty.json","w",encoding="utf-8") as plik:
        json.dump(dane,plik)


#dodawanie wpisu (imie,nawisko,telefon,ulica, miasto)
def dodawanie_wpisu(imie, nazwisko, telefon, ulica, miasto, dane):
   # sprawdzanie czy imie i nazwisko powtarzaja sie w danych i w wpisie
    for osoba in dane:
        if osoba["imie"].lower() == imie.lower() and osoba["nazwisko"].lower() == nazwisko.lower():
            print("Te imię i nazwisko już istnieje!")
            return False, dane  #juz te dane istnieja
    
    #dodawanie elemetow do zmiennej dane
    dane.append({"imie": imie, "nazwisko": nazwisko, "telefon": telefon, "ulica": ulica, "miasto": miasto})
    zapisywanie_danych(dane)
    return True, dane #dodanie do zmiennej dane nowych elemetnow


#dodawanie nowej osoby do interfejsu
def dodawanie_osoby():
    imie = tekst_imie.get()
    nazwisko = tekst_nazwisko.get()
    telefon = tekst_telefon.get()
    ulica = tekst_ulica.get()
    miasto = tekst_miasto.get()

    if not (imie and nazwisko and telefon and ulica and miasto):
        komunikat.config(text="Niewprowadzono wszytskich danych.") #jezeli nie wprowadzono wszytkich danych to wyswietla sie komunikat 
        return
    
    if not telefon.isdigit() or len(telefon) != 9:
        komunikat.config(text="Numer telefonu musi zawierać dokładnie 9 cyfr.")
        return

    if not imie.isalpha():
        komunikat.config(text="Imię może zawierać tylko litery.")
        return

    if not nazwisko.isalpha():
        komunikat.config(text="Nazwisko może zawierać tylko litery.")
        return

    if not miasto.isalpha():
        komunikat.config(text="Miasto może zawierać tylko litery.")
        return
    
    dane = wczytywanie_danych()
    sukces, dane = dodawanie_wpisu(imie, nazwisko, telefon, ulica, miasto, dane)

    if sukces:
        komunikat.config(text="Dodano kontakt.")# wyswieltanie komunikat i wprowadzenie nowej osoby
        wyczysc_pola()
        odswiez_tabele(dane)
    else:
        komunikat.config(text="Kontakt już istnieje.")# wyswietlanie komunikat ze juz ten kontakt istnieje


# szukanie kontaktu po wybranym polu
def szukaj_kontaktu():
    tekst = tekst_szukaj.get().lower()# pobieranie tekstu wpisanego przez uzytkowanika
    pole = wybor_pola.get() 
    klucz = pola_z_danymi.get(pole)# pola z danymi kontaktowymi

    dane = wczytywanie_danych()
    wyniki = []

    #przeszukiwanie po danych i dodawnaie do tabeli 
    for osoba in dane:
        if tekst in osoba.get(klucz, "").lower():
            wyniki.append(osoba)
    
    odswiez_tabele(wyniki)

# pokazywanie wszytkich danych
def pokaz_wszystkie():
    dane = wczytywanie_danych()
    odswiez_tabele(dane)
    tekst_szukaj.delete(0, tk.END)


def statystyka_miast():
    dane = wczytywanie_danych()  # wczytanie danych
    miasta = {}  #slownik na miasta 

    for osoba in dane:
        miasto = osoba["miasto"]
        if miasto in miasta:
            miasta[miasto] += 1# jezeli juz miasto sie poajwilo dodawana jest 1
        else:
            miasta[miasto] = 1 # jezeli pierwszy poajwia sie to 1 

    wynik = ""
    for m in miasta:
        linia = m + ": " + str(miasta[m]) + " \n"# 
        wynik += linia

# wyswietlanie jako komunikat ile jest dancyh osob z danego miasta 
    if wynik != "":
        messagebox.showinfo("Statystyka", wynik)
    else:
        messagebox.showinfo("Statystyka", "Brak danych.")


def wyczysc_pola():
    tekst_imie.delete(0, tk.END)
    tekst_nazwisko.delete(0, tk.END)
    tekst_telefon.delete(0, tk.END)
    tekst_ulica.delete(0, tk.END)
    tekst_miasto.delete(0, tk.END)
    tekst_szukaj.delete(0, tk.END)


def odswiez_tabele(dane):
    for a in tabela.get_children():
        tabela.delete(a)# usuwanie całej wypełnionej tablicy
    for osoba in dane:
        tabela.insert("", "end", values=(osoba.get("imie", ""),osoba.get("nazwisko", ""),osoba.get("telefon", ""),osoba.get("ulica", ""),osoba.get("miasto", "")))
        #dodawane są wszystkie elementy z dancyh

#Pole do 
pola_z_danymi = {"Imię": "imie","Nazwisko": "nazwisko","Telefon": "telefon","Ulica": "ulica","Miasto": "miasto"}


# GUI
root = tk.Tk()
root.title("Kontakty")

tk.Label(root, text="Imię").grid(row=0, column=0)
tekst_imie = tk.Entry(root)
tekst_imie.grid(row=0, column=1)

tk.Label(root, text="Nazwisko").grid(row=1, column=0)
tekst_nazwisko = tk.Entry(root)
tekst_nazwisko.grid(row=1, column=1)

tk.Label(root, text="Telefon").grid(row=2, column=0)
tekst_telefon = tk.Entry(root)
tekst_telefon.grid(row=2, column=1)

tk.Label(root, text="Ulica").grid(row=3, column=0)
tekst_ulica = tk.Entry(root)
tekst_ulica.grid(row=3, column=1)

tk.Label(root, text="Miasto").grid(row=4, column=0)
tekst_miasto = tk.Entry(root)
tekst_miasto.grid(row=4, column=1)

tk.Button(root, text="Dodaj", command=dodawanie_osoby,bg="lightblue").grid(row=5, column=0, columnspan=2)

# Szukajka + wybór pola
tk.Label(root, text="Szukaj").grid(row=6, column=0)
tekst_szukaj = tk.Entry(root)
tekst_szukaj.grid(row=6, column=1)

tk.Label(root, text="Szukanie po:").grid(row=7, column=0)
wybor_pola = ttk.Combobox(root, values=list(pola_z_danymi.keys()), state="readonly")# wybieranie z listy pola_z_danymi 
wybor_pola.grid(row=7, column=1)
wybor_pola.current(0)  # domyślnie "Imię"

tk.Button(root, text="Pokaż wszystkie osoby", command=pokaz_wszystkie,bg="lightblue").grid(row=9, column=0, columnspan=2)
tk.Button(root, text="Szukaj", command=szukaj_kontaktu,bg="lightblue").grid(row=8, column=1)

# Statystyka
tk.Button(root, text="Statystyka miast", command=statystyka_miast,bg="lightblue").grid(row=11, column=0, columnspan=2)

# Komunikat
komunikat = tk.Label(root, text="")
komunikat.grid(row=12, column=0, columnspan=2)

# Tabela
tabela = ttk.Treeview(root, columns=("Imię", "Nazwisko", "Telefon", "Ulica", "Miasto"), show="headings")
for col in tabela["columns"]:
    tabela.heading(col, text=col)
tabela.grid(row=13, column=0, columnspan=2)

odswiez_tabele(wczytywanie_danych())

root.mainloop()

