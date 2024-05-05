import sqlite3
import tkinter as tk
from tkinter import messagebox

class basedata:
    def _init_(self, bd_ad):
        self.conn = sqlite3.connect(bd_ad)
        self.cursor = self.conn.cursor()
    def gemi_s(self, gemi_id):
        self.cursor.execute("DELETE FROM Gemiler WHERE ID=?", (gemi_id,))
        self.conn.commit()
    def tablo_oluştur(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Gemiler (
                                seri_no TEXT PRIMARY KEY,
                                ad TEXT,
                                ağırlık REAL,
                                yapim_yili INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS YolcuGemileri (
                                seri_no TEXT PRIMARY KEY,
                                yolcu_kapasitesi INTEGER,
                                FOREIGN KEY(seri_no) REFERENCES Gemiler(seri_no))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS TankerGemisi (
                                seri_no TEXT PRIMARY KEY,
                                petrol_kapasitesi REAL,
                                FOREIGN KEY(seri_no) REFERENCES Gemiler(seri_no))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS KonteynerGemisi (
                            seri_no TEXT PRIMARY KEY,
                            konteyner_sayisi INTEGER,
                            max_ağırlık REAL,
                            FOREIGN KEY(seri_no) REFERENCES Gemiler(seri_no))''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Seferler (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                yola çıkış tarih DATE,
                                dönüş tarih DATE,
                                liman TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Kaptanlar (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Ad TEXT,
                                Soyad TEXT,
                                Adres TEXT,
                                Vatandaslık TEXT,
                                Lisans Tarihi DATE,
                                Lisans Numarasi TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Murettebat (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Ad TEXT,
                                Soyad TEXT,
                                Adres TEXT,
                                Vatandaslık TEXT,
                                Lisans Tarihi DATE,
                                Lisans Numarasi TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Limanlar (
                                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                Liman Adi TEXT,
                                Ulke TEXT,
                                Liman Ulkesi TEXT,
                                Nufus INTEGER,
                                Pasaport GerekirMi BOOLEAN,
                                Demirleme Ucreti REAL)''')
        self.conn.commit()
    def gemi_ekle(self, data):
        self.cursor.execute('''INSERT INTO Gemiler (Seri Numarasi, Gemi Adi, Gemi Agirligi, Yapim Yili) 
                            VALUES (, , , )''', data)
        self.conn.commit()
    def delete_ship(self, gemi_id):
        try:
            self.cursor.execute("DELETE FROM Gemiler WHERE ID=?", (gemi_id,))
            self.conn.commit()
            print("Gemi silindi.")
        except Exception as x:
            print("Bir hata oluştu:", x)
    def close_connection(self):
        self.conn.close()
class uygulama:
    def _init_(self, master):
        self.master = master
        self.master.title("Giriş")
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        button_texts = ["Gemiler", "Seferler", "Kaptanlar", "Mürettebat", "Limanlar"]
        for text in button_texts:
            button = tk.Button(self.frame, text=text, command=lambda t=text: self.ekran(t))
            button.pack(fill="e", padx=10, pady=5)
        self.center_window()
        self.db_manager = basedata("ship_management.db")
        self.db_manager.tablo_oluştur()
    def center_window(self):
        g = self.master.winfo_reqwidth()
        u = self.master.winfo_reqheight()
        g2 = self.master.winfo_screenwidth()
        u2 = self.master.winfo_screenheight()
        x = (g2 - g) // 2
        y = (u2 - u) // 2
        self.master.geometry("+{}+{}".format(x, y))
    def ekran(self, button_text):
        new_window = tk.Toplevel(self.master)
        new_window.title(button_text)
        if button_text == "Gemiler":
            self.gemi_ekranı(new_window)
        elif button_text == "Seferler":
            self.sefer_ekranı(new_window)
        elif button_text == "Kaptanlar":
            self.kaptan_ekranı(new_window)
        elif button_text == "Mürettebat":
            self.mü_ekranı(new_window)
        elif button_text == "Limanlar":
            self.liman_ekranı(new_window)
    def gemi_ekranı(self, window):
        ship_types = ["Yolcu Gemileri", "Tanker Gemileri", "Konteyner Gemileri"]
        for ship_type in ship_types:
            button = tk.Button(window, text=ship_type, command=lambda t=ship_type: self.sw(window, t))
            button.pack(fill="e", padx=10, pady=5)
    def sefer_ekranı(self, window):
        self.sw(window, "Seferler")
    def kaptan_ekranı(self, window):
        self.sw(window, "Kaptanlar")
    def mü_ekranı(self, window):
        self.sw(window, "Mürettebat")
    def liman_ekranı(self, window):
        self.sw(window, "Limanlar")
    def sw(self, window, giriş):
        self.sil(window)
        l = []
        i = []
        if giriş == "Yolcu Gemileri":
            l = ["Seri Numarası:", "Geminin Adı:", "Gemi Ağırlığı:", "Gemi Yapım Yılı:", "Yolcu Kapasitesi:"]
        elif giriş == "Tanker Gemileri":
            l = ["Seri Numarası:", "Geminin Adı:", "Gemi Ağırlığı:", "Gemi Yapım Yılı:", "Litre Kapasitesi:"]
        elif giriş == "Konteyner Gemileri":
            l = ["Seri Numarası:", "Geminin Adı:", "Gemi Ağırlığı:", "Gemi Yapım Yılı:", "Konteyner Kapasitesi:", "Maksimum Ağırlık:"]
        elif giriş == "Seferler":
            l = ["ID:", "Yola Çıkış Tarihi:", "Dönüş Tarihi:", "Yola Çıkış Limanı:"]
        elif giriş == "Kaptanlar" or giriş == "Mürettebat":
            l = ["ID:", "Ad:", "Soyad:", "Adres:", "Vatandaşlık:", "Lisans Tarihi:", "Lisans Numarası:"]
        elif giriş == "Limanlar":
            l = ["Liman Adı:", "Ülke:", "Liman Ülkesi:", "Nüfus:", "Pasaport Gerekiyor mu:", "Demirleme Ücreti:"]
        for label_text in l:
            label = tk.Label(window, text=label_text)
            label.pack()
            entry = tk.Entry(window)
            entry.pack()
            i.append(entry)
        add_button = tk.Button(window, text="Ekle", command=lambda: self.add_data(giriş, i))
        add_button.pack(fill="e", padx=10, pady=5)
        remove_button = tk.Button(window, text="Çıkar", command=lambda: self.remove_data(giriş, i))
        remove_button.pack(fill="e", padx=10, pady=5)
        back_button = tk.Button(window, text="Ana Ekrana Geri Dön", command=window.destroy)
        back_button.pack(fill="e", padx=10, pady=5)
    def sil(self, window):
        for widget in window.winfo_children():
            widget.destroy()
    def add_data(self, giriş, i):
        data = [entry.get() for entry in i]
        if giriş in ["Yolcu Gemileri", "Tanker Gemileri", "Konteyner Gemileri"]:
            self.db_manager.gemi_ekle(data)
            messagebox.showinfo("Bilgi", "Veri başarıyla eklendi!")
    def remove_data(self, giriş, i):
        if giriş == "Gemiler":
            gemi_id = i[0].get() 
            self.db_manager.gemi_s(gemi_id)       
def main():
    root = tk.Tk()
    app = uygulama(root)
    root.mainloop()
db_file = "gezgin_gemi.db"


connection = sqlite3.connect(db_file)
print()
cursor = connection.cursor()
cursor.execute("SELECT * FROM gemiler")
r = cursor.fetchall()
for row in r:
    print(row)

connection.close()

main()