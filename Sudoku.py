import tkinter as tk
from tkinter import messagebox
import random
import time


# Hàm sinh bảng Sudoku đầy đủ bằng thuật toán backtracking
def sinh_bang_day_du():
    bang = [[0] * 9 for _ in range(9)]

    def la_hop_le(so, hang, cot):
        for i in range(9):
            if bang[hang][i] == so or bang[i][cot] == so:
                return False
        sub_hang, sub_cot = 3 * (hang // 3), 3 * (cot // 3)
        for i in range(sub_hang, sub_hang + 3):
            for j in range(sub_cot, sub_cot + 3):
                if bang[i][j] == so:
                    return False
        return True

    def giai():
        for i in range(9):
            for j in range(9):
                if bang[i][j] == 0:
                    so_ngau_nhien = list(range(1, 10))
                    random.shuffle(so_ngau_nhien)
                    for so in so_ngau_nhien:
                        if la_hop_le(so, i, j):
                            bang[i][j] = so
                            if giai():
                                return True
                            bang[i][j] = 0
                    return False
        return True

    giai()
    return bang

# Hàm xóa số ngẫu nhiên để tạo đề bài
def xoa_so(bang_day_du, muc_do):
    bang = [row[:] for row in bang_day_du]
    so_can_xoa = {"Dễ": 30, "Trung bình": 40, "Khó": 50}[muc_do]
    dem = 0
    while dem < so_can_xoa:
        hang, cot = random.randint(0, 8), random.randint(0, 8)
        if bang[hang][cot] != 0:
            bang[hang][cot] = 0
            dem += 1
    return bang

# Hàm đặt lại bảng với mức độ khó
def dat_lai_bang():
    global bang, bang_goc, start_time
    muc_do = difficulty.get()
    bang_day_du = sinh_bang_day_du()
    bang = xoa_so(bang_day_du, muc_do)
    bang_goc = [row[:] for row in bang]
    start_time = time.time()

    for i in range(9):
        for j in range(9):
            o_nhap[i][j].delete(0, tk.END)
            if bang[i][j] != 0:
                o_nhap[i][j].insert(0, str(bang[i][j]))
                o_nhap[i][j].config(fg="black", bg="white")
            else:
                o_nhap[i][j].config(fg="blue", bg="white")

# Hàm cập nhật dữ liệu từ các ô nhập liệu vào bảng `bang`
def cap_nhat_bang():
    for i in range(9):
        for j in range(9):
            try:
                gia_tri = int(o_nhap[i][j].get())
                bang[i][j] = gia_tri
            except ValueError:
                bang[i][j] = 0

# Hàm kiểm tra đúng/sai
def kiem_tra_dap_an():
    cap_nhat_bang()
    dung = True
    for i in range(9):
        for j in range(9):
            if bang[i][j] != 0:
                hang_hop_le = bang[i].count(bang[i][j]) == 1
                cot_hop_le = [bang[x][j] for x in range(9)].count(bang[i][j]) == 1
                sub_hang, sub_cot = i // 3 * 3, j // 3 * 3
                luoi_con = [bang[x][y] for x in range(sub_hang, sub_hang + 3) for y in range(sub_cot, sub_cot + 3)]
                luoi_hop_le = luoi_con.count(bang[i][j]) == 1

                if hang_hop_le and cot_hop_le and luoi_hop_le:
                    o_nhap[i][j].config(bg="lightgreen")
                else:
                    o_nhap[i][j].config(bg="red")
                    dung = False

# Sự kiện tô sáng hàng, cột và lưới con khi nhấn vào ô
def to_sang_lien_quan(event):
    cap_nhat_bang()
    for i in range(9):
        for j in range(9):
            o_nhap[i][j].config(bg="white")
    widget = event.widget
    index = None
    for i, row in enumerate(o_nhap):
        if widget in row:
            index = (i, row.index(widget))
            break
    if index:
        hang, cot = index
        for i in range(9):
            o_nhap[hang][i].config(bg="lightyellow")
            o_nhap[i][cot].config(bg="lightyellow")

# Giao diện chính
root = tk.Tk()
root.title("Thuật giải game Sudoku")
root.geometry("700x800")
root.configure(bg="lightgray")



# Biến toàn cục
start_time = None
difficulty = tk.StringVar(value="Trung bình")  # Mặc định mức độ là "Trung bình"

# Tiêu đề
tieu_de = tk.Label(root, text="Sudoku", font=("Arial", 16), bg="lightgray")
tieu_de.pack(pady=10)

# Tiêu đề thời gian
time_label = tk.Label(root, text="Thời gian: 00:00", font=("Arial", 14), bg="lightgray")
time_label.pack(pady=5)

# Hàm cập nhật thời gian
def cap_nhat_thoi_gian():
    if start_time:
        elapsed_time = int(time.time() - start_time)    
        phut, giay = divmod(elapsed_time, 60)
        time_label.config(text=f"Thời gian: {phut:02}:{giay:02}")
        time_label.after(1000, cap_nhat_thoi_gian)

# Tạo bảng Sudoku
khung = tk.Frame(root, bg="lightgray")
khung.pack(pady=20)
o_nhap = []
for sub_hang in range(3):  # Lưới con theo hàng
    for sub_cot in range(3):  # Lưới con theo cột
        khung_con = tk.Frame(khung, relief="ridge", bd=1, bg="black")  # Viền mỏng hơn
        khung_con.grid(row=sub_hang, column=sub_cot, padx=3, pady=3)
        for i in range(3):  # Ô trong lưới con
            for j in range(3):
                hang_chinh = sub_hang * 3 + i
                cot_chinh = sub_cot * 3 + j
                o = tk.Entry(khung_con, width=3, font=("Arial", 18), justify="center", relief="flat", bd=1)  # Viền mỏng
                o.grid(row=i, column=j, padx=1, pady=1, ipady=5)
                if len(o_nhap) <= hang_chinh:
                    o_nhap.append([])
                o_nhap[hang_chinh].append(o)
                o.bind("<FocusIn>", to_sang_lien_quan)

# Nút chức năng và chọn mức độ
khung_nut = tk.Frame(root, bg="lightgray")
khung_nut.pack(pady=10)

nut_kiem_tra = tk.Button(khung_nut, text="Kiểm tra", command=kiem_tra_dap_an, bg="lightblue", font=("Arial", 14))
nut_kiem_tra.grid(row=0, column=0, padx=10)

nut_dat_lai = tk.Button(khung_nut, text="Làm mới", command=dat_lai_bang, bg="lightgreen", font=("Arial", 14))
nut_dat_lai.grid(row=0, column=1, padx=10)

nut_thoat = tk.Button(khung_nut, text="Thoát", command=root.quit, bg="red", font=("Arial", 14), fg="white")
nut_thoat.grid(row=0, column=2, padx=10)

# Dropdown menu chọn mức độ
menu_chon_muc_do = tk.OptionMenu(khung_nut, difficulty, "Dễ", "Trung bình", "Khó")
menu_chon_muc_do.config(bg="orange", font=("Arial", 14))
menu_chon_muc_do.grid(row=0, column=3, padx=10)

# Khởi tạo bảng đầu tiên
dat_lai_bang()
cap_nhat_thoi_gian()
root.mainloop()
