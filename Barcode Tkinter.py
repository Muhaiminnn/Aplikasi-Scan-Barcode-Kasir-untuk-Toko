import cv2
import numpy as np
import time
import pygame
import os
import csv

from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from datetime import datetime

pygame.mixer.init()
sound = pygame.mixer.Sound("beep.mp3")
#with open('data.csv') as f:
#    #datalist = f.read().splitlines()
#    datalist = [line.split("-")[0] for line in f]
     
class ScanBarcode:
    def __init__(self, root):
        self.root = root
        self.root.title("Barcode Scanner App")
        self.root.bind("<Escape>", self.close)
        
        self.cap = cv2.VideoCapture(1)
        self.cap.set(3, 720)
        self.cap.set(4, 480)

        self.judul = tk.Label(root, text="Aplikasi Kasir QRcode By. Muhaimin", font=("Times New Roman",24), fg="white", bg="black")
        self.judul.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.panel = tk.Label(self.root, width=500, height=350)
        self.panel.grid(row=1, rowspan=2, column=0, columnspan=2, padx=5, pady=5)

        self.start_scan = tk.Button(root, text="Save Nota", command=self.save_file, width=20, height=3)
        self.start_scan.grid(row=1, column=2, padx=5, pady=5)

        self.kode = tk.Label(root, text="Kode Produk", width=15, height=2)
        self.kode.grid(row=3, column=0, padx=5, pady=5)
        self.kode = tk.Entry(root, width=30)
        self.kode.grid(row=3, column=1, padx=5, pady=5)
        self.nama_produk = tk.Label(root, text="Nama Produk", width=15, height=2)
        self.nama_produk.grid(row=4, column=0, padx=5, pady=5)
        self.nama_produk = tk.Entry(root, width=30)
        self.nama_produk.grid(row=4, column=1, padx=5, pady=5)
        self.harga_produk = tk.Label(root, text="Harga Produk", width=15, height=2)
        self.harga_produk.grid(row=5, column=0, padx=5, pady=5)
        self.harga_produk = tk.Entry(root, width=30)
        self.harga_produk.grid(row=5, column=1, padx=5, pady=5)

        self.daftar_scan = tk.Button(root, text="Daftarkan Produk", command=self.daftar_produk, width=20, height=3)
        self.daftar_scan.grid(row=3, rowspan=6, column=2, padx=5, pady=5)

        with open('nota.txt', 'w') as f:
                f.write(f"                Muhaimin Store\n\n")
                f.write(f"              Jl. St. Alauddin 3\n\n")
                f.write("-------------------- Nota --------------------\n\n")
                f.write("\n\n")
                f.write(f"\n       Total                  Rp. 0,-")
        with open('nota.txt', 'r') as f:
            awal = f.read()
        self.text_label = tk.Label(self.root, text=awal, bg='black', fg='white', font=("Courier New",8), justify='left')
        self.text_label.grid(row=1, rowspan=6, column=3, padx=5, pady=5)

        self.scan()

    def scan(self):
        nota = {}
        with open("data.csv", 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Lewati baris pertama (header)
            datalist = [row[0] for row in reader]

        def clear_nota():
            nota.clear()
            with open('nota.txt', 'w') as f:
                f.write(f"                Muhaimin Store\n\n")
                f.write(f"              Jl. St. Alauddin 3\n\n")
                f.write("-------------------- Nota --------------------\n\n")
                f.write("\n\n")
                f.write(f"\n       Total                  Rp. 0,-")
            self.preview_nota()
            #print("ini maz eee ---> ", nota)
        self.clearNota = tk.Button(root, text="Clear Nota", command=clear_nota, width=20, height=3)
        self.clearNota.grid(row=2, column=2, padx=5, pady=5)
        #while True:
        def update_panel():
            retV, img = self.cap.read()
            #retV, img = self.cap.read()
            #img = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                self.kode.delete(0, 'end')
                self.kode.insert(0, myData)
                self.nama_produk.delete(0, 'end')
                self.harga_produk.delete(0, 'end')
                
                #print(myData)
                if myData in datalist:
                    out = 'Ada'
                else:
                    out = 'Tidak Terdaftar!'
                
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,(0,165,255),5)
                pts2 = barcode.rect
                cv2.putText(img,out,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,(0,255,0),2) 
                
                self.tambah_item(nota, myData)
            
            cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            img_tk = ImageTk.PhotoImage(image=img)
            self.panel.img_tk = img_tk  # Avoid garbage collection
            self.panel.config(image=img_tk)
            self.root.after(10, update_panel)
        update_panel()
            
    def tambah_item(self, nota, myData):
        #nama_item = myData
        #myData = self.scan()
        #print(myData)    

        with open("data.csv", 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Lewati baris pertama (header)
            datalist = [row[0] for row in reader]

        harga_item = {}
        nama_produk = {}
        total = 0
        with open("data.csv", 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)
            lines = list(reader)
            for line in lines:
                kode = line[0]
                itemx = line[1]
                hargax = line[2]
                harga_item[kode] = int(hargax)
                nama_produk[kode] = itemx

        #with open('data.txt', 'r') as f:
        #    for line in f:
        #        itemx, kode, hargax = line.strip().split(',')
        #        harga_item[itemx] = int(hargax)
        if myData in datalist:
            #item = myData.split("-")[1]
            #harga = int(myData.split("-")[2])
            item = myData
            #print(item)
            if item in nota:
                nota[item] += 1
            else:
                nota[item] = 1
            print(nota)
            sound.play()
            time.sleep(1)
            
        else:
            print('Tidak Terdaftar!')
            #sound.play()
            #time.sleep(1)

        with open('nota.txt', 'w') as f:
            f.write(f"                Muhaimin Store\n\n")
            f.write(f"              Jl. St. Alauddin 3\n\n")
            f.write("-------------------- Nota --------------------\n\n")
            for item, harga in nota.items():
                totalx = harga * harga_item[item] 
                itemx = nama_produk[item]
                total += totalx
                f.write(f"{itemx}     {harga} x Rp. {harga_item[item]}     Rp. {totalx},-\n\n")
            f.write(f"\n       Total                  Rp. {total},-")
            
        self.preview_nota()
    
    def close(self, event=None):
        self.cap.release()
        cv2.destroyAllWindows()
        self.root.destroy()

    def preview_nota(self):
        with open('nota.txt', 'r') as f:
            isi_nota = f.read()
        #time.sleep(1) 
        self.text_label.grid_forget()
        self.text_label = tk.Label(self.root, text=isi_nota, bg='black', fg='white', font=("Courier New",8), justify='left')
        self.text_label.grid(row=1, rowspan=6, column=3, padx=5, pady=5)
    
    def save_file(self):
        waktu_sekarang = datetime.now()
        file_name = waktu_sekarang.strftime("%Y%m%d_%H%M%S")
        time_nota = waktu_sekarang.strftime("%Y-%m-%d %H:%M:%S")

        file_path = os.path.join("Nota", f"NOTA {file_name}.txt")

        with open('nota.txt', 'r') as f:
            prnt_nota = f.read()
        
        with open(file_path, "w") as f:
            f.write(f"{time_nota}\n\n")
            f.write(prnt_nota)
        messagebox.showinfo("INFO", f"NOTA {file_name} \nBerhasil disimpan.")   

    def daftar_produk(self):
        kode = self.kode.get()
        nama_produk = self.nama_produk.get()
        harga_produk = self.harga_produk.get()

        with open("data.csv", 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader)  # Lewati baris pertama (header)
            datalist = [row[0] for row in reader]

        #print(kode, nama_produk, harga_produk)
        if kode in datalist:
            messagebox.showwarning("Peringatan!","Kode ini sudah didaftarkan!")
        else:     
            with open("data.csv", 'r', newline='') as f:
                reader = csv.reader(f)
                # Memeriksa setiap baris dalam file CSV
                for row in reader:
                    # Jika kode sudah ada, hentikan dan jangan tambahkan ke file
                    if row and row[0] == kode:
                        messagebox.showwarning("INFO","Sudah didaftarkan!")
                        return
            if kode == "" or nama_produk == "" or harga_produk == "":
                messagebox.showwarning("INFO","Isi Nama & Harga Produk!")
            else:
                with open("data.csv", 'a', newline='') as f:
                    #f.write(f"{kode},{nama_produk},{harga_produk}\n")
                    writer = csv.writer(f)
                    writer.writerow([kode, nama_produk, harga_produk])
                    messagebox.showinfo("INFO","Kode ini berhasil didaftarkan!")  
        

if __name__ == "__main__":
    root = tk.Tk()
    app = ScanBarcode(root)
    root.mainloop()
