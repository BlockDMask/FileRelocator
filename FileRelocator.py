# 2023.12.21. blockdmask@gmail.com

import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import webbrowser
import shutil
import os

# 프로그램 버전.
version = "0.0.1" 
row_index = 0

def choose_folder(entry_var):
    folder_path = filedialog.askdirectory()
    entry_var.set(folder_path)  # StringVar 객체를 업데이트

def update_status(text):
    status_text.config(state='normal')
    status_text.insert(tk.END, text + "\n")
    status_text.config(state='disabled')
    status_text.yview(tk.END)

def create_unique_filename(dst, filename):
    """대상 경로에 동일한 파일명이 있을 경우, 고유한 파일명 생성"""
    counter = 1
    name, extension = os.path.splitext(filename)
    new_filename = filename
    while os.path.exists(os.path.join(dst, new_filename)):
        new_filename = f"{name}_{counter}{extension}"
        counter += 1
    return new_filename

def move_files(src, dst):
    files_moved = 0
    try:
        # 소스 폴더 내의 모든 하위 폴더 및 파일 순회
        for root, dirs, files in os.walk(src):
            for file in files:
                src_path = os.path.join(root, file)

                if os.path.isfile(src_path):
                    unique_filename = create_unique_filename(dst, file)
                    dst_path = os.path.join(dst, unique_filename)
                    shutil.move(src_path, dst_path)
                    update_status(f"{src_path} 에서 {dst_path} 로 이동 완료.")
                    files_moved += 1
                    
        update_status(f"모든 파일 이동 완료. 총 {files_moved}개의 파일을 이동했습니다.")
    except Exception as e:
        update_status(f"오류 발생: {e}")
    finally:
        move_button['state'] = tk.NORMAL  # 작업 완료 후 버튼 활성화

def move_files_thread():
    move_button['state'] = tk.DISABLED  # 작업 중 버튼 비활성화
    src = source_var.get()
    dst = destination_var.get()
    thread = threading.Thread(target=move_files, args=(src, dst))
    thread.start()
    root.after(100, check_thread, thread)

def check_thread(thread):
    if thread.is_alive():
        root.after(100, check_thread, thread)
    else:
        update_status("모든 작업이 완료되었습니다.")

def update_move_button_state(*args):
    src = source_var.get()
    dst = destination_var.get()
    move_button['state'] = tk.NORMAL if src and dst else tk.DISABLED
    
def open_blog():
    webbrowser.open('https://blockdmask.tistory.com/')

# GUI 초기화
root = tk.Tk()
root.geometry("720x425")
root.title("FileRelocator")
root.resizable(False, False)  # 창 크기 조절 비활성화
root.attributes("-toolwindow", True)  # 최대화 버튼 비활성화

# StringVar 객체 생성
source_var = tk.StringVar()
destination_var = tk.StringVar()

# 폴더 경로 레이블과 입력창
source_label = tk.Label(root, text="Source Folder:")
source_entry = tk.Entry(root, textvariable=source_var, width=50, state='readonly')
source_label.grid(row=0, column=0, padx=10, pady=10)
source_entry.grid(row=0, column=1, padx=10, pady=10)

destination_label = tk.Label(root, text="Destination Folder:")
destination_entry = tk.Entry(root, textvariable=destination_var, width=50, state='readonly')
destination_label.grid(row=1, column=0, padx=10, pady=10)
destination_entry.grid(row=1, column=1, padx=10, pady=10)

# 폴더 선택 버튼
choose_source_button = tk.Button(root, text="Choose Source", command=lambda: choose_folder(source_var))
choose_destination_button = tk.Button(root, text="Choose Destination", command=lambda: choose_folder(destination_var))
move_button = tk.Button(root, text="Move Files", command=move_files_thread, state=tk.DISABLED)
choose_source_button.grid(row=0, column=2, padx=10, pady=10)
choose_destination_button.grid(row=1, column=2, padx=10, pady=10)
move_button.grid(row=2, column=1, padx=10, pady=10)

# 상태 표시 텍스트 창
status_text = scrolledtext.ScrolledText(root, height=14, state='disabled')
status_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="we")

# StringVar 객체의 변경을 감지하여 move_button의 상태를 업데이트
source_var.trace_add("write", update_move_button_state)
destination_var.trace_add("write", update_move_button_state)

# 기타 GUI 구성등
# 개발자 블로그로 이동하는 버튼
blog_button = tk.Button(root, text="Visit Developer Blog", command=open_blog)
blog_button.grid(row=4, column=0, padx=10, pady=10)

# 개발자 이메일 주소 표시
email_label = tk.Label(root, text="Contact: blockdmask@gmail.com")
email_label.grid(row=4, column=2, padx=10, pady=10, sticky="e")

# 버전 정보 표시
version_label = tk.Label(root, text=f"Version: {version}")
version_label.grid(row=5, column=2, padx=10, pady=10, sticky="e")

# GUI 실행 시 초기 상태 메시지
update_status("프로그램을 시작합니다. 소스 폴더와 대상 폴더를 선택하세요.")

# GUI 실행
root.mainloop()
