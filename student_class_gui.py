import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import json

# 课节时间段
PERIODS = [
    ("8:30-10:15", ["8:30", "9:20", "9:25", "10:15"]),  # 大课1（8:30-9:20, 9:25-10:15）
    ("10:25-12:10", ["10:25", "11:15", "11:20", "12:10"]), # 大课2（10:25-11:15, 11:20-12:10）
    ("14:00-15:45", ["14:00", "14:50", "14:55", "15:45"]), # 大课3（14:00-14:50, 14:55-15:45）
    ("16:00-17:45", ["16:00", "16:50", "16:55", "17:45"]), # 大课4（16:00-16:50, 16:55-17:45）
    ("18:45-19:35", ["18:45", "19:35"]), # 晚上小课1
    ("19:40-20:30", ["19:40", "20:30"]), # 晚上小课2
    ("20:35-21:25", ["20:35", "21:25"])  # 晚上小课3
]
WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

# 区域分割索引
def get_section_label(i):
    if i == 0:
        return "上午"
    elif i == 2:
        return "下午"
    elif i == 4:
        return "晚上"
    else:
        return None

class ScheduleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("学生课表生成器")
        self.busy = set()  # (row, col) 记录有课
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        # 姓名、学号输入
        tk.Label(self.root, text="姓名:").grid(row=0, column=0, sticky='e')
        self.name_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.name_var, width=10).grid(row=0, column=1)
        tk.Label(self.root, text="学号:").grid(row=0, column=2, sticky='e')
        self.id_var = tk.StringVar()
        tk.Entry(self.root, textvariable=self.id_var, width=15).grid(row=0, column=3)
        tk.Button(self.root, text="导出课表JSON", command=self.export_json).grid(row=0, column=4, padx=10)

        # 课表表头
        tk.Label(self.root, text="时间/星期").grid(row=1, column=0)
        for j, wd in enumerate(WEEKDAYS):
            tk.Label(self.root, text=wd).grid(row=1, column=j+1)
        # 课表格子
        row_offset = 2
        for i, (label, times) in enumerate(PERIODS):
            section = get_section_label(i)
            if section:
                # 区域标签，跨8列
                tk.Label(self.root, text=section, bg='#e0e0e0', fg='#333', font=('Arial', 10, 'bold')).grid(row=row_offset, column=0, columnspan=8, sticky='we', pady=(8,0))
                row_offset += 1
            tk.Label(self.root, text=label).grid(row=row_offset, column=0)
            for j in range(7):
                btn = tk.Button(self.root, width=10, height=1, relief='raised',
                                command=lambda x=i, y=j: self.toggle(x, y))
                btn.grid(row=row_offset, column=j+1, padx=1, pady=1)
                self.entries[(i, j)] = btn
            row_offset += 1

    def toggle(self, i, j):
        key = (i, j)
        btn = self.entries[key]
        if key in self.busy:
            self.busy.remove(key)
            btn.config(bg='SystemButtonFace')
        else:
            self.busy.add(key)
            btn.config(bg='#ffb3b3')

    def export_json(self):
        name = self.name_var.get().strip()
        student_id = self.id_var.get().strip()
        if not name or not student_id:
            messagebox.showerror("错误", "请填写姓名和学号！")
            return
        busy = []
        for (i, j) in self.busy:
            label, times = PERIODS[i]
            # 大课（前4行）按两节小课分别写入
            if i < 4:
                busy.append({"day": WEEKDAYS[j], "start": times[0], "end": times[1]})
                busy.append({"day": WEEKDAYS[j], "start": times[2], "end": times[3]})
            else:
                busy.append({"day": WEEKDAYS[j], "start": times[0], "end": times[1]})
        data = {
            "name": name,
            "student_id": student_id,
            "busy": busy
        }
        file_path = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON files', '*.json')],
            initialfile=f'{student_id}.json',
            title='保存课表JSON文件')
        if file_path:
            # 自定义JSON格式化：确保数组项目在单行中
            with open(file_path, 'w', encoding='utf-8') as f:
                # 开始写入JSON
                f.write('{\n')
                f.write(f'  "name": "{name}",\n')
                f.write(f'  "student_id": "{student_id}",\n')
                f.write('  "busy": [\n')
                
                # 写入busy数组，每个项目一行
                for i, item in enumerate(busy):
                    line = f'    {{"day": "{item["day"]}", "start": "{item["start"]}", "end": "{item["end"]}"}}' 
                    if i < len(busy) - 1:
                        line += ','
                    f.write(line + '\n')
                
                # 结束JSON
                f.write('  ]\n')
                f.write('}\n')
            
            messagebox.showinfo("成功", f"课表已保存到 {file_path}")

if __name__ == '__main__':
    root = tk.Tk()
    app = ScheduleGUI(root)
    root.mainloop() 