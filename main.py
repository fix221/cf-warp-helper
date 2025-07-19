import subprocess
import csv
import os
import tkinter
import ctypes
import threading
import time
import sys
from tkinter import scrolledtext, messagebox

def is_admin():
    """检查当前脚本是否以管理员权限运行"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(command, args=None):
    """以管理员权限重新运行脚本"""
    try:
        if args is None:
            args = []
        ps_args = f'"{command}" ' + ' '.join([f'"{arg}"' for arg in args])
        ps_command = f'Start-Process -Verb RunAs -FilePath {ps_args} -Wait'
        
        subprocess.run(
            ['powershell', '-Command', ps_command],
            check=True,
            text=True
        )
        sys.exit(0)  # 确保原脚本退出
    except subprocess.CalledProcessError as e:
        print(f"执行失败: {e}")
        messagebox.showerror("错误", f"执行失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"发生错误: {e}")
        messagebox.showerror("错误", f"发生错误: {e}")
        sys.exit(1)

class CFWarpGUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("CF-Warp-GUI")
        self.root.geometry("600x800")
        self.root.resizable(0, 0)
        self.ip_ports = []
        self.i = 0
        self.ip_port = ""
        self.connect_status = False

        # 存储wg info输出的变量
        self.wg_info_text = tkinter.StringVar()
        self.wg_info_text.set("正在获取WireGuard信息...")

        # 控制刷新的标志
        self.is_refreshing = True
        if sys.platform.startswith('win'):
            self.default_font = ('Microsoft YaHei UI', 10)
        elif sys.platform.startswith('darwin'):
            self.default_font = ('Heiti TC', 10)
        else:
            self.default_font = ('SimHei', 10)
        self.create_widgets()
        # 启动刷新线程
        self.refresh_thread = threading.Thread(target=self.refresh_wg_show)
        self.refresh_thread.start()
        self.root.mainloop()

    def create_widgets(self):
        # 开始转换
        self.label2 = tkinter.Button(self.root, text="开始解析")
        self.label2.pack(padx=10, pady=10)
        self.label2.bind("<Button-1>", self.convert)

        # 显示ip 端口 丢包 延迟
        self.label4 = tkinter.Label(self.root, text="ip 端口 丢包 延迟")
        self.label4.pack(padx=10, pady=10)

        self.label5 = tkinter.Label(self.root, text=None)
        self.label5.pack(padx=10, pady=10)

        self.btn = tkinter.Button(self.root, text="下一个ip")
        self.btn.pack(padx=10, pady=10)
        self.btn.bind("<Button-1>", self.convert_next)

        self.label6 = tkinter.Button(self.root, text="生成wg节点配置")
        self.label6.pack(padx=10, pady=10)
        self.label6.bind("<Button-1>", self.wg_node)

        self.label7 = tkinter.Button(self.root, text="直接挂节点")
        self.label7.pack(padx=10, pady=10)
        self.label7.bind("<Button-1>", self.wg_direct)

        self.disconnect_btn = tkinter.Button(self.root, text="断开节点", command=self.disconnect_wg, font=self.default_font)

        # 创建滚动文本区域显示wg info输出
        self.info_text = scrolledtext.ScrolledText(self.root, wrap=tkinter.WORD, font=self.default_font)
        self.info_text.pack(expand=True, padx=10, pady=10)

        # 创建状态标签
        self.status_var = tkinter.StringVar()
        self.status_var.set("最后更新: 从未")
        status_label = tkinter.Label(self.root, textvariable=self.status_var, font=self.default_font)
        status_label.pack(side=tkinter.LEFT, padx=10, pady=5)

        # 创建刷新按钮
        self.refresh_button = tkinter.Button(self.root, text="刷新", command=self.manual_refresh, font=self.default_font)
        self.refresh_button.pack(side=tkinter.RIGHT, padx=10, pady=5)

    def convert(self, event):
        subprocess.run(dir_path + "\\warp-test.bat", check=True)
        self.label5.config(text="")
        # 获得输入参数
        filename = dir_path + "\\result.csv"
        with open(filename, 'r') as csvfile:
            # 调用转换程序
            reader = csv.reader(csvfile)
            rows = list(reader)  # 将迭代器转换为列表
            for row in rows:
                self.ip_ports.append(row)

            self.ip_port = self.ip_ports[1][0]
            # self.label5.config(text=ip_port)
            for i in self.ip_ports[1]:
                print(i)
                self.label5.config(text=self.label5.cget("text") + "    " + i)

        # 提示完成
        # tkinter.messagebox.showinfo(title="提示", message="转换完成！")
        print("转换完成！")

    def convert_next(self, event):
        if self.i < len(self.ip_ports) - 1:
            self.label5.config(text="")
            self.i += 1
            self.ip_port = self.ip_ports[self.i][0]
            for i in self.ip_ports[self.i + 1]:
                print(i)
                self.label5.config(text=self.label5.cget("text") + "    " + i)

    def wg_node(self, event):
        # 生成wg节点配置
        with open("wg-sample.conf") as f:
            content = f.read()
            content = content.replace("REPLACE_IP_PORT", self.ip_port)
            with open("wg-node.conf", "w") as f:
                f.write(content)
                f.close()
        # 提示完成
        # tkinter.messagebox.showinfo(title="提示", message="生成wg节点配置完成！")
        print("生成wg节点配置完成！")

    def wg_direct(self, event):
        if not self.ip_port:
            self.convert_next(event)
            self.wg_node(event)
        # 直接挂节点 run as admin
        # subprocess.Popen(["wireguard","/installtunnelservice","wg-node.conf"])
        # subprocess
        if is_admin():
            if self.i:
                subprocess.run(["wireguard", "/uninstalltunnelservice", "wg-node"])
            subprocess.run(["wireguard", "/installtunnelservice", dir_path + "\\wg-node.conf"])
        else:
            if self.i:
                run_as_admin("wireguard", ["/uninstalltunnelservice", "wg-node"])
            run_as_admin(sys.executable, [script_path])
        # tkinter.messagebox.showinfo(title="提示", message="挂载wg节点完成！")
        print("挂wg节点完成！")
        self.connect_status = True

    def disconnect_wg(self):
        if is_admin():
            subprocess.run(["wireguard", "/uninstalltunnelservice", "wg-node"])
        else:
            run_as_admin("wireguard", ["/uninstalltunnelservice", "wg-node"])

    def get_wg_show(self):
        cmd = "wg show"
        """执行wg show命令并返回输出"""
        """以管理员权限执行命令并返回输出"""
        temp_file = os.path.join(os.environ["TEMP"], f"wg_{int(time.time())}.txt")
        try:
            # 最简化的PowerShell命令：直接启动管理员PowerShell执行命令并写文件
            ps_cmd = f'''
            Start-Process powershell -ArgumentList "
                -Command & {{
                    {cmd} 2>&1 | Out-File '{temp_file}' -Encoding utf8;
                    exit $LASTEXITCODE
                }}
            " -Wait -WindowStyle Hidden
            '''
            # 执行PowerShell（会弹出UAC）
            subprocess.run(
                ["powershell", "-Command", ps_cmd],
                timeout=10,
                check=True
            )
            # 读取结果
            if os.path.exists(temp_file):
                with open(temp_file, 'r', encoding='utf8', errors='replace') as f:
                    return f.read()
            return "命令执行成功，但未生成输出文件"
        except Exception as e:
            return f"执行失败: {str(e)}\n临时文件: {temp_file}"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

    def refresh_wg_show(self):
        # print(1)
        """每秒刷新一次wg show信息的线程函数"""
        while self.is_refreshing:
            # 获取wg info输出
            wg_output = self.get_wg_show()
            if wg_output and self.info_text.get(1.0, tkinter.END) == "":
                self.connect_status = True
            elif wg_output:
                self.info_text.delete(1.0, tkinter.END)
                self.info_text.insert(tkinter.END, wg_output)
                self.status_var.set("最后刷新时间：" + time.strftime("%Y-%m-%d %H:%M:%S"))
                self.connect_status = True
            if self.connect_status:
                self.disconnect_btn.pack()
            else:
                self.disconnect_btn.pack_forget()
            # 更新UI（需要使用root.after在主线程中执行）
            self.root.after(0, self.update_ui, wg_output)

            # 等待1秒
            time.sleep(5)

    def update_ui(self, wg_output):
        """更新UI显示"""
        self.info_text.delete(1.0, tkinter.END)
        print(wg_output)
        if wg_output == "":
            wg_output = "未连接节点/出现错误"
        # 插入新的wg show输出
        self.info_text.insert(tkinter.END, wg_output)

        # 更新状态标签
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.status_var.set(f"最后更新: {current_time}")

    def manual_refresh(self):
        """手动刷新按钮的回调函数"""
        # 获取wg info输出
        wg_output = self.get_wg_show()
        self.info_text.delete(1.0, tkinter.END)
        # 更新UI
        self.update_ui(wg_output)

if __name__ == '__main__':
    script_path = os.path.abspath(__file__)
    dir_path = os.path.dirname(script_path)
    
    if is_admin():
        cf_gui = CFWarpGUI()
    else:
        # 弹窗提示需要管理员权限
        messagebox.showwarning("权限不足", "将以管理员权限重新运行此脚本。")
        run_as_admin(sys.executable, [script_path])
