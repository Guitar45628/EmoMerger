import tkinter as tk
from tkinterdnd2 import *
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd

file_paths = []  # รายการ (list) เพื่อเก็บ path ของไฟล์ CSV

# รายการของส่วนท้ายของไฟล์ที่ยอมรับ
accepted_endings = ["AK", "AX", "AY", "AZ", "B_", "BI", "BV", "EA", "EL", "EM", "GX", "GY", "GZ", "HR", "MX", "MY", "MZ", "PG", "PI", "PR", "RD", "SA", "SF", "SR", "T1", "TH", "TL"]

def handle_drop(event):
    allow_endings = [ending for ending, var in ending_vars.items() if var.get() == 1]
    for file_path in event.data.split():
        file_name = os.path.basename(file_path)
        if file_name.lower().endswith(tuple("_{}.csv".format(ending.lower()) for ending in allow_endings)):
            file_paths.append(file_path)  # เพิ่ม path ของไฟล์ CSV ลงในรายการ
    update_file_list()

def update_file_list():
    for i in tree.get_children():
        tree.delete(i)
    for index, file_name in enumerate(file_paths, start=1):
        tree.insert("", "end", values=(index, file_name))

def delete_selected_files():
    selected_items = tree.selection()
    for item in selected_items:
        file_name = tree.item(item, "values")[1]
        file_paths.remove(file_name)
        tree.delete(item)

def merge_columns(output_file_name):
    # สร้างรายการสำหรับเก็บข้อมูลจากไฟล์ที่ถูกเลือก
    data_list = []
    
    # วนลูปผ่าน path ของไฟล์ที่ถูกเลือกในรายการ
    for file_path in file_paths:
        try:
            # ใช้ pandas ในการอ่านไฟล์ CSV จาก path นี้
            df = pd.read_csv(file_path)
            
            # กรองข้อมูลเฉพาะคอลัมน์ 'LocalTimestamp' และคอลัมน์ที่มี tag เท่ากับ EA, EL, HR (หรือคอลัมน์ที่คุณต้องการ)
            selected_columns = ['LocalTimestamp'] + [col for col in df.columns if col in accepted_endings]
            df = df[selected_columns]
            
            # รวมข้อมูลทั้งหมดเข้าไปใน data_list
            data_list.append(df)
                
        except Exception as e:
            messagebox.showerror("Error", f"เกิดข้อผิดพลาดในการอ่านไฟล์ {file_path}: {str(e)}")
    
    if data_list:
        # รวมข้อมูลทั้งหมดจาก data_list โดยรวมตามคอลัมน์ 'LocalTimestamp'
        merged_data = pd.concat(data_list, axis=0, ignore_index=True, sort=False)
        
        # รวมข้อมูลที่มี LocalTimestamp เท่ากันในแถวเดียวกัน
        merged_data = merged_data.groupby('LocalTimestamp', as_index=False).agg('sum')
        merged_data = merged_data.fillna('')

        
        # บันทึกข้อมูลที่รวมเข้าไฟล์ CSV
        merged_file_name = output_file_name  # ใช้ชื่อไฟล์เป็น Label
        # if not location:
        #     messagebox.showerror("Error", "กรุณาเลือก Location ให้ครบทุกช่อง")
        #     return
        merged_file_path = os.path.join(merged_file_name)
        merged_data.to_csv(merged_file_path, index=False)
        messagebox.showinfo("Success", f"รวมข้อมูลเสร็จสิ้น ไฟล์ถูกบันทึกที่ {merged_file_path}")


def merge_files():
    # ให้ผู้ใช้ป้อนชื่อไฟล์ผลลัพธ์
    output_file_name = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    
    if not output_file_name:
        messagebox.showerror("Error", "กรุณาเลือกชื่อไฟล์ที่ต้องการบันทึก")
        return

    # เรียกใช้ฟังก์ชันสำหรับรวมคอลัมน์
    merge_columns(output_file_name)

root = TkinterDnD.Tk()
root.title("Drag and Drop CSV Files")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

label = tk.Label(frame, text="ลากและวางไฟล์ CSV ที่นี่:")
label.pack()

entry = tk.Entry(frame, width=100)
entry.pack(fill=tk.X)

entry.drop_target_register(DND_FILES)
entry.dnd_bind('<<Drop>>', handle_drop)

tree_frame = ttk.Frame(frame)
tree_frame.pack(fill=tk.BOTH, expand=True)

columns = ("No.", "ชื่อไฟล์")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
tree.pack(fill=tk.BOTH, expand=True)

tree.heading("No.", text="No.")
tree.heading("ชื่อไฟล์", text="ชื่อไฟล์")

tree.column("No.", width=20)  # กำหนดความกว้างเป็น 20px
tree.column("ชื่อไฟล์", width=400)

# สร้างเฟรมเพิ่มเติมสำหรับการใช้ grid geometry manager
checkbutton_frame = tk.Frame(frame)
checkbutton_frame.pack()

# สร้าง Checkbutton สำหรับการเลือกส่วนท้ายของไฟล์
ending_vars = {}
row = 1
col = 0
for ending in accepted_endings:
    var = tk.IntVar()
    ending_vars[ending] = var
    cb = tk.Checkbutton(checkbutton_frame, text=ending, variable=var)
    cb.grid(row=row, column=col, sticky='w')
    col += 1
    if col >= 10:
        col = 0
        row += 1

# สร้างเฟรมสำหรับ Location
label_location_frame = tk.Frame(frame)
label_location_frame.pack()

# location_label = tk.Label(label_location_frame, text="Location:")
# location_label.pack(side=tk.LEFT)
# location_entry = tk.Entry(label_location_frame, width=50)
# location_entry.pack(side=tk.LEFT)

# location_button = tk.Button(label_location_frame, text="เลือก Location", command=get_save_location)
# location_button.pack(side=tk.LEFT)

add_button = tk.Button(frame, text="ลบรายการที่เลือก", command=delete_selected_files)
add_button.pack()

merge_button = tk.Button(frame, text="รวมไฟล์", command=merge_files)
merge_button.pack()

update_file_list()

root.mainloop()
