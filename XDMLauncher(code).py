import subprocess
import sys

# 自动检测并安装缺失的第三方库
def check_dependencies():
    required = ["customtkinter", "requests"]
    for lib in required:
        try:
            __import__(lib)
        except ImportError:
            print(f"正在安装缺失的依赖: {lib} ...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

check_dependencies()

# 下面正式导入所有需要的库
import customtkinter as ctk
from tkinter import filedialog, messagebox
import json, os, threading, subprocess, shutil, zipfile, tempfile, time
import urllib.request, urllib.error, ssl, hashlib, uuid as uuidlib
import platform
import requests

APP_NAME = "XDMLauncher for Windows"
APP_VER = "V1.0.0R"
BG_COLOR = "#0F2620"
CARD_COLOR = "#1A3B32"
BTN_COLOR = "#245749"
HOVER_COLOR = "#2E6D5C"
TEXT_COLOR = "#E6F3EF"
CONFIG_FILE = "xd_launcher_config.json"
MODRINTH_API = "https://modrinth.cd/v2"
FONT_FAMILY = "Microsoft YaHei"

_OS = {"Windows": "windows", "Darwin": "mac", "Linux": "linux"}.get(platform.system(), "windows")
_ARCH = platform.machine().lower()
_ARCH_API = "x64" if _ARCH in ("amd64", "x86_64") else "aarch64"
_USER_AGENT = "XDMLauncher/1.0"
_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE

LANG = {
    "zh": {
        "tab_launch": "启动", "tab_download": "下载", "tab_settings": "设置", "tab_about": "关于",
        "username": "用户名", "remember_user": "记住用户名", "task_list": "日志",
        "ver_select": "版本选择", "launch_btn": "启动游戏", "ver_settings": "版本设置",
        "dl_game": "游戏", "dl_mod": "模组", "dl_shader": "光影", "dl_modpack": "整合包",
        "mem": "内存分配：", "game_dir": "游戏目录：", "browse": "浏览",
        "lang_text": "语言：", "skin": "皮肤：", "cape": "披风：", "upload": "上传",
        "java": "JAVA：", "auto": "自动", "manual": "手动",
        "win_size": "窗口大小：", "reset": "恢复默认", "save": "保存",
        "check_update": "检查更新", "vanilla": "原版", "forge": "Forge",
        "fabric": "Fabric", "neoforge": "NeoForge",
        "download_start": "开始下载", "no_user_warn": "请填写用户名！",
        "installing": "正在安装...", "launching": "正在启动游戏...",
        "search": "搜索", "search_hint": "输入名称搜索",
        "dl_success": "✅ 完成", "dl_fail": "❌ 失败",
        "search_fail": "搜索失败", "no_result": "没有找到相关资源",
        "mem_invalid": "内存必须是数字，最小1024MB", "size_invalid": "窗口宽高必须为正整数",
        "no_version": "没有已安装版本，请先下载", "working": "任务进行中...",
        "loading_ver": "正在加载版本列表...",
        "ver_type_all": "全部", "ver_type_release": "正式版", "ver_type_snapshot": "快照",
        "ver_type_beta": "Beta", "ver_type_alpha": "Alpha",
        "search_ver_hint": "筛选版本号",
        "select_installer": "选择安装器", "install_now": "安装", "already_installed": "已安装",
        "back_to_ver": "返回", "installing_loader": "正在安装加载器",
        "install_success": "✅ 安装完成！", "install_fail": "❌ 安装失败",
        "no_loader_for_ver": "该版本无此加载器",
        "upload_skin_success": "皮肤已保存", "upload_cape_success": "披风已保存",
        "checking_update": "检查更新中...", "update_latest": "✅ 已是最新版本",
        "update_fail": "检查更新失败", "config_saved": "设置已保存",
        "reset_confirm": "确定恢复默认？", "reset_done": "已恢复默认",
        "skin_not_found": "未找到皮肤", "cape_not_found": "未找到披风",
        "resource_dl_to": "下载到：{path}", "ver_settings_title": "版本设置",
        "open_mods": "打开 mods 文件夹", "open_ver_dir": "打开版本文件夹",
        "export_ver": "导出该版本(zip)", "delete_ver": "删除该版本",
        "export_done": "导出完成", "delete_confirm": "确定删除该版本？",
        "delete_done": "已删除", "mods_empty": "暂无模组",
        "integrity_check": "正在校验文件完整性...", "integrity_ok": "✅ 完整性校验通过",
        "integrity_fail": "⚠ 完整性校验发现问题",
        "top_start": "开始下载：{name}", "top_done": "✅ 安装完成：{name}",
        "top_fail": "❌ 下载失败：{name}", "modpack_installing": "正在安装整合包...",
        "modpack_hint": "输入整合包名称搜索 Modrinth",
        "progress_idle": "就绪", "progress_installing": "安装中...",
        "progress_checking": "校验中...", "mc_ver_filter": "游戏版本",
        "loader_filter": "加载器筛选",
    },
    "en": {
        "tab_launch": "Launch", "tab_download": "Download", "tab_settings": "Settings", "tab_about": "About",
        "username": "Username", "remember_user": "Remember", "task_list": "Log",
        "ver_select": "Version", "launch_btn": "Launch", "ver_settings": "Version Settings",
        "dl_game": "Game", "dl_mod": "Mod", "dl_shader": "Shader", "dl_modpack": "Modpack",
        "mem": "Memory: ", "game_dir": "Game Dir: ", "browse": "Browse",
        "lang_text": "Language: ", "skin": "Skin: ", "cape": "Cape: ", "upload": "Upload",
        "java": "JAVA: ", "auto": "Auto", "manual": "Manual",
        "win_size": "Window: ", "reset": "Reset", "save": "Save",
        "check_update": "Check Update", "vanilla": "Vanilla", "forge": "Forge",
        "fabric": "Fabric", "neoforge": "NeoForge",
        "download_start": "Download", "no_user_warn": "Input username!",
        "installing": "Installing...", "launching": "Launching...",
        "search": "Search", "search_hint": "Search...",
        "dl_success": "✅ Done", "dl_fail": "❌ Failed",
        "search_fail": "Search failed", "no_result": "No results",
        "mem_invalid": "Memory min 1024MB", "size_invalid": "Invalid size",
        "no_version": "No version installed", "working": "Busy...",
        "loading_ver": "Loading versions...",
        "ver_type_all": "All", "ver_type_release": "Release", "ver_type_snapshot": "Snapshot",
        "ver_type_beta": "Beta", "ver_type_alpha": "Alpha",
        "search_ver_hint": "Filter version",
        "select_installer": "Select", "install_now": "Install", "already_installed": "Installed",
        "back_to_ver": "Back", "installing_loader": "Installing loader",
        "install_success": "✅ Installed!", "install_fail": "❌ Install failed",
        "no_loader_for_ver": "Loader unavailable",
        "upload_skin_success": "Skin saved", "upload_cape_success": "Cape saved",
        "checking_update": "Checking...", "update_latest": "✅ Up to date",
        "update_fail": "Check failed", "config_saved": "Saved",
        "reset_confirm": "Reset to default?", "reset_done": "Reset done",
        "skin_not_found": "Skin not found", "cape_not_found": "Cape not found",
        "resource_dl_to": "Downloaded: {path}", "ver_settings_title": "Version Settings",
        "open_mods": "Open mods folder", "open_ver_dir": "Open version folder",
        "export_ver": "Export version (zip)", "delete_ver": "Delete version",
        "export_done": "Exported", "delete_confirm": "Delete this version?",
        "delete_done": "Deleted", "mods_empty": "No mods",
        "integrity_check": "Checking files...", "integrity_ok": "✅ Integrity OK",
        "integrity_fail": "⚠ Integrity issues found",
        "top_start": "Downloading: {name}", "top_done": "✅ Installed: {name}",
        "top_fail": "❌ Failed: {name}", "modpack_installing": "Installing modpack...",
        "modpack_hint": "Search Modrinth modpack",
        "progress_idle": "Ready", "progress_installing": "Installing...",
        "progress_checking": "Checking...", "mc_ver_filter": "MC Version",
        "loader_filter": "Loader filter",
    }
}

class XDMLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} | {APP_VER}")
        self.geometry("1100x650")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")
        self.font_normal = ctk.CTkFont(family=FONT_FAMILY, size=13)
        self.font_bold = ctk.CTkFont(family=FONT_FAMILY, size=14, weight="bold")
        self.font_title = ctk.CTkFont(family=FONT_FAMILY, size=18, weight="bold")
        self.font_small = ctk.CTkFont(family=FONT_FAMILY, size=11)

        self.cfg = self._load_config()
        self.cur_lang = self.cfg.get("lang", "zh")
        self.username_var = ctk.StringVar(value=self.cfg.get("username", ""))
        self.remember_var = ctk.BooleanVar(value=self.cfg.get("remember", False))
        self.mem_var = ctk.StringVar(value=self.cfg.get("memory", "2048"))
        self.gamedir_var = ctk.StringVar(value=self.cfg.get("gamedir", "./minecraft"))
        self.java_mode_var = ctk.StringVar(value=self.cfg.get("java_mode", "auto"))
        self.java_path_var = ctk.StringVar(value=self.cfg.get("java_path", ""))
        self.win_w = ctk.StringVar(value=self.cfg.get("win_w", "854"))
        self.win_h = ctk.StringVar(value=self.cfg.get("win_h", "480"))

        self.current_page = None
        self.current_page_name = "launch"
        self.launch_log_box = None
        self.download_log_box = None
        self.launch_btn = None
        self.version_combobox = None
        self.center_progress_frame = None
        self.center_progress_bar = None
        self.center_progress_label = None
        self.top_banner = None
        self.top_banner_label = None

        self.selected_mc_version = None
        self.dl_category_var = ctk.StringVar(value="game")
        self.dl_view_stage = "version_list"
        self.search_entry = None
        self.loader_select = None
        self.mcver_select = None
        self.result_data_list = []
        self.full_vanilla_version_list = []
        self.is_verlist_loading = False
        self.is_searching = False
        self.is_game_downloading = False
        self.task_lock = threading.Lock()

        self.top_tab = ctk.CTkFrame(self, fg_color=CARD_COLOR)
        self.top_tab.pack(fill="x", padx=10, pady=(8, 4))
        for key, page in [("tab_launch", "launch"), ("tab_download", "download"),
                          ("tab_settings", "settings"), ("tab_about", "about")]:
            ctk.CTkButton(self.top_tab, text=LANG[self.cur_lang][key],
                          command=lambda p=page: self.switch_page(p),
                          fg_color=BTN_COLOR, hover_color=HOVER_COLOR, width=90,
                          font=self.font_normal).pack(side="left", padx=4, pady=4)

        self.top_banner = ctk.CTkFrame(self, fg_color="#1E4D3F", height=34)
        self.top_banner_label = ctk.CTkLabel(self.top_banner, text="", font=self.font_normal)
        self.top_banner_label.pack(pady=6)
        self.top_banner.pack_forget()

        self.main_frame = ctk.CTkFrame(self, fg_color=BG_COLOR)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.switch_page("launch")

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_config(self):
        for k, v in [("lang", self.cur_lang), ("username", self.username_var.get()),
                     ("remember", self.remember_var.get()), ("memory", self.mem_var.get()),
                     ("gamedir", self.gamedir_var.get()), ("java_mode", self.java_mode_var.get()),
                     ("java_path", self.java_path_var.get()), ("win_w", self.win_w.get()),
                     ("win_h", self.win_h.get())]:
            self.cfg[k] = v
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.cfg, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def show_banner(self, text, color="#1E4D3F", auto_hide=4000):
        def _show():
            self.top_banner_label.configure(text=text)
            self.top_banner.configure(fg_color=color)
            self.top_banner.pack(fill="x", padx=10, pady=(0, 4), before=self.main_frame)
            if auto_hide:
                self.after(auto_hide, self.hide_banner)
        self.after(0, _show)

    def hide_banner(self):
        try:
            self.top_banner.pack_forget()
        except Exception:
            pass

    def ui_log_launch(self, text):
        self.after(0, lambda: self._log_launch(text))

    def _log_launch(self, text):
        if self.launch_log_box is not None and self.launch_log_box.winfo_exists():
            self.launch_log_box.insert("end", f"{text}\n")
            self.launch_log_box.see("end")

    def ui_log_download(self, text):
        self.after(0, lambda: self._log_download(text))

    def _log_download(self, text):
        if self.download_log_box is not None and self.download_log_box.winfo_exists():
            self.download_log_box.insert("end", f"{text}\n")
            self.download_log_box.see("end")

    def ui_center_progress(self, val, tip=""):
        def _u():
            if self.center_progress_frame is None or not self.center_progress_frame.winfo_exists():
                return
            self.center_progress_frame.pack(fill="x", padx=8, pady=(0, 4))
            self.center_progress_bar.set(max(0.0, min(1.0, val)))
            self.center_progress_label.configure(text=tip if tip else f"{val*100:.1f}%")
        self.after(0, _u)

    def ui_center_progress_hide(self):
        def _u():
            if self.center_progress_frame and self.center_progress_frame.winfo_exists():
                self.center_progress_frame.pack_forget()
        self.after(0, _u)

    def clear_page(self):
        if self.current_page is not None and self.current_page.winfo_exists():
            self.current_page.destroy()
        self.current_page = None

    def switch_lang(self, lang_code):
        self.cur_lang = lang_code
        self._save_config()
        self.switch_page(self.current_page_name)

    def switch_page(self, page_name):
        self.current_page_name = page_name
        self.clear_page()
        if page_name == "launch":
            self.page_launch()
        elif page_name == "download":
            self.dl_view_stage = "version_list"
            self.selected_mc_version = None
            self.page_download()
        elif page_name == "settings":
            self.page_settings()
        elif page_name == "about":
            self.page_about()

    # ========== 启动页 ==========
    def page_launch(self):
        lang = LANG[self.cur_lang]
        page = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        page.pack(fill="both", expand=True)
        self.current_page = page

        top_frame = ctk.CTkFrame(page, fg_color=CARD_COLOR)
        top_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(top_frame, text="👤", font=ctk.CTkFont(family="Segoe UI Emoji", size=45),
                     width=80, height=80).pack(side="left", padx=10, pady=10)
        user_f = ctk.CTkFrame(top_frame, fg_color=CARD_COLOR)
        user_f.pack(side="left", fill="x", expand=True, padx=10)
        ctk.CTkLabel(user_f, text=lang["username"], font=self.font_bold).pack(anchor="w")
        ctk.CTkEntry(user_f, textvariable=self.username_var, height=34,
                     font=self.font_normal).pack(fill="x", pady=4)
        ctk.CTkCheckBox(user_f, text=lang["remember_user"], variable=self.remember_var,
                        font=self.font_normal).pack(anchor="w")

        task_f = ctk.CTkFrame(page, fg_color=CARD_COLOR)
        task_f.pack(fill="both", expand=True, padx=10, pady=5)
        ctk.CTkLabel(task_f, text=lang["task_list"], font=self.font_bold).pack(anchor="w", padx=8, pady=4)

        self.center_progress_frame = ctk.CTkFrame(task_f, fg_color="#122820", height=40)
        self.center_progress_bar = ctk.CTkProgressBar(self.center_progress_frame, progress_color="#2A9D6F")
        self.center_progress_bar.pack(fill="x", padx=8, pady=(6, 2))
        self.center_progress_bar.set(0)
        self.center_progress_label = ctk.CTkLabel(self.center_progress_frame, text="",
                                                  font=self.font_small)
        self.center_progress_label.pack(pady=(0, 6))
        self.center_progress_frame.pack_forget()

        self.launch_log_box = ctk.CTkTextbox(task_f, fg_color="#0B1A16", font=self.font_normal)
        self.launch_log_box.pack(fill="both", expand=True, padx=8, pady=4)

        bottom_f = ctk.CTkFrame(page, fg_color=CARD_COLOR)
        bottom_f.pack(fill="x", padx=10, pady=10)
        ctk.CTkLabel(bottom_f, text=lang["ver_select"], font=self.font_bold).pack(side="left", padx=10)

        game_dir = os.path.abspath(self.gamedir_var.get())
        ver_list = []
        try:
            base = os.path.join(game_dir, "versions")
            if os.path.isdir(base):
                ver_list = [name for name in os.listdir(base) if self._is_version_installed(game_dir, name)]
                ver_list.sort(reverse=True)
        except Exception:
            ver_list = []

        self.version_combobox = ctk.CTkComboBox(bottom_f, values=ver_list, state="readonly",
                                                font=self.font_normal, width=180)
        if ver_list:
            self.version_combobox.set(ver_list[0])
        self.version_combobox.pack(side="left", padx=6)

        ctk.CTkButton(bottom_f, text=lang["ver_settings"], width=100, font=self.font_normal,
                      fg_color=BTN_COLOR, hover_color=HOVER_COLOR,
                      command=self.open_version_settings).pack(side="left", padx=4)

        self.launch_btn = ctk.CTkButton(bottom_f, text=lang["launch_btn"], fg_color="#2A725F",
                                        hover_color="#348C74", command=self.thread_launch_game,
                                        width=140, font=self.font_bold)
        if not ver_list:
            self.launch_btn.configure(state="disabled")
        self.launch_btn.pack(side="right", padx=10)

    def open_version_settings(self):
        lang = LANG[self.cur_lang]
        vid = self.version_combobox.get() if self.version_combobox else ""
        if not vid:
            messagebox.showwarning("Warning", lang["no_version"])
            return
        game_dir = os.path.abspath(self.gamedir_var.get())
        ver_dir = os.path.join(game_dir, "versions", vid)
        mods_dir = os.path.join(game_dir, "mods")

        win = ctk.CTkToplevel(self)
        win.title(f"{lang['ver_settings_title']} - {vid}")
        win.geometry("520x360")
        win.configure(fg_color=BG_COLOR)

        ctk.CTkLabel(win, text=f"{lang['ver_settings_title']}: {vid}",
                     font=self.font_title).pack(pady=12)

        info = ctk.CTkTextbox(win, height=110, fg_color="#0B1A16", font=self.font_small)
        info.pack(fill="x", padx=16, pady=4)
        mods = []
        if os.path.isdir(mods_dir):
            mods = [f for f in os.listdir(mods_dir) if f.endswith(".jar")]
        info.insert("end", f"Version dir: {ver_dir}\n")
        info.insert("end", f"Mods count: {len(mods)}\n")
        if mods:
            for m in mods[:20]:
                info.insert("end", f"  - {m}\n")
        else:
            info.insert("end", f"  ({lang['mods_empty']})\n")
        info.configure(state="disabled")

        def open_mods():
            os.makedirs(mods_dir, exist_ok=True)
            try:
                os.startfile(mods_dir)
            except Exception:
                subprocess.Popen(["explorer", mods_dir])

        def open_ver():
            try:
                os.startfile(ver_dir)
            except Exception:
                subprocess.Popen(["explorer", ver_dir])

        def export_ver():
            out = filedialog.asksaveasfilename(defaultextension=".zip",
                                               initialfile=f"{vid}.zip",
                                               filetypes=[("ZIP", "*.zip")])
            if not out:
                return
            try:
                with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
                    if os.path.isdir(ver_dir):
                        for root, _, files in os.walk(ver_dir):
                            for fn in files:
                                fp = os.path.join(root, fn)
                                z.write(fp, os.path.relpath(fp, game_dir))
                    if os.path.isdir(mods_dir):
                        for fn in os.listdir(mods_dir):
                            if fn.endswith(".jar"):
                                z.write(os.path.join(mods_dir, fn), os.path.join("mods", fn))
                messagebox.showinfo("OK", lang["export_done"])
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def delete_ver():
            if not messagebox.askyesno("Confirm", lang["delete_confirm"]):
                return
            try:
                if os.path.isdir(ver_dir):
                    shutil.rmtree(ver_dir)
                messagebox.showinfo("OK", lang["delete_done"])
                win.destroy()
                self.switch_page("launch")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        btn_f = ctk.CTkFrame(win, fg_color=CARD_COLOR)
        btn_f.pack(fill="x", padx=16, pady=12)
        ctk.CTkButton(btn_f, text=lang["open_mods"], command=open_mods,
                      font=self.font_normal).pack(side="left", padx=4)
        ctk.CTkButton(btn_f, text=lang["open_ver_dir"], command=open_ver,
                      font=self.font_normal).pack(side="left", padx=4)
        ctk.CTkButton(btn_f, text=lang["export_ver"], command=export_ver,
                      font=self.font_normal).pack(side="left", padx=4)
        ctk.CTkButton(btn_f, text=lang["delete_ver"], command=delete_ver,
                      fg_color="#502828", font=self.font_normal).pack(side="right", padx=4)

    def thread_launch_game(self):
        threading.Thread(target=self.launch_game, daemon=True).start()

    def launch_game(self):
        lang = LANG[self.cur_lang]
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Warning", lang["no_user_warn"])
            return
        version_id = self.version_combobox.get()
        if not version_id:
            messagebox.showerror("Error", lang["no_version"])
            return
        game_dir = os.path.abspath(self.gamedir_var.get())
        try:
            mem = int(self.mem_var.get())
            if mem < 1024:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", lang["mem_invalid"])
            return
        try:
            w, h = int(self.win_w.get()), int(self.win_h.get())
            if w <= 0 or h <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", lang["size_invalid"])
            return

        self.ui_log_launch(f"{lang['launching']} | {version_id} | {username}")
        
        try:
            java_path = self._get_java_path(version_id)
            cmd = self._build_command(game_dir, version_id, username, java_path, mem, w, h)
            subprocess.Popen(cmd, cwd=game_dir)
        except Exception as e:
            self.ui_log_launch(f"启动失败: {str(e)}")

    # ==========================================
    # ======== 原生核心引擎 (完全替代 mclib) ========
    # ==========================================
    
    def _http_get(self, url, timeout=30, retries=3):
        last_err = None
        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
                with urllib.request.urlopen(req, timeout=timeout, context=_ctx) as resp:
                    return resp.read()
            except Exception as e:
                last_err = e
                time.sleep(1 + attempt)
        raise RuntimeError(f"GET {url} failed: {last_err}")

    def _http_get_json(self, url, timeout=30):
        return json.loads(self._http_get(url, timeout=timeout).decode("utf-8"))

    def _download_file(self, url, dest, progress_cb=None, chunk_size=256 * 1024):
        os.makedirs(os.path.dirname(os.path.abspath(dest)), exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
        with urllib.request.urlopen(req, timeout=60, context=_ctx) as resp:
            total = int(resp.headers.get("Content-Length") or 0)
            downloaded = 0
            tmp = dest + ".part"
            with open(tmp, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_cb:
                        progress_cb(downloaded, total)
            os.replace(tmp, dest)
        return dest

    def _version_dir(self, game_dir, version_id):
        return os.path.join(game_dir, "versions", version_id)

    def _is_version_installed(self, game_dir, version_id):
        d = self._version_dir(game_dir, version_id)
        return os.path.exists(os.path.join(d, f"{version_id}.json"))

    def _lib_rules_allow(self, lib):
        rules = lib.get("rules")
        if not rules:
            return True
        allowed = False
        _os_key = {"Windows": "windows", "Darwin": "osx", "Linux": "linux"}.get(platform.system(), "windows")
        _arch_key = "x86_64" if platform.machine().lower() in ("amd64", "x86_64") else "aarch64"
        for rule in rules:
            action = rule.get("action")
            os_rule = rule.get("os")
            if os_rule:
                name = os_rule.get("name")
                if name and name != _os_key:
                    continue
                arch = os_rule.get("arch")
                if arch and arch != _arch_key:
                    continue
            if action == "allow":
                allowed = True
            elif action == "disallow":
                allowed = False
        return allowed

    def _check_sha1(self, path, expected):
        if not expected or not os.path.exists(path):
            return False
        h = hashlib.sha1()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest() == expected

    def _install_vanilla(self, game_dir, version_id, report):
        vdir = self._version_dir(game_dir, version_id)
        os.makedirs(vdir, exist_ok=True)
        manifest = self._http_get_json("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")
        url = next(v["url"] for v in manifest["versions"] if v["id"] == version_id)
        vjson = self._http_get_json(url)
        with open(os.path.join(vdir, f"{version_id}.json"), "w", encoding="utf-8") as f:
            json.dump(vjson, f)
        report("client", 0, 1)
        client_info = vjson.get("downloads", {}).get("client", {})
        jar_path = os.path.join(vdir, f"{version_id}.jar")
        if not self._check_sha1(jar_path, client_info.get("sha1")):
            self._download_file(client_info["url"], jar_path, lambda d, t: report("client", d, t))
        libs = [l for l in vjson.get("libraries", []) if self._lib_rules_allow(l)]
        for i, lib in enumerate(libs):
            report("libraries", i, len(libs))
            art = lib.get("downloads", {}).get("artifact")
            if art:
                path = os.path.join(game_dir, "libraries", art["path"])
                if not self._check_sha1(path, art.get("sha1")):
                    self._download_file(art["url"], path)
        _os_key = {"Windows": "windows", "Darwin": "osx", "Linux": "linux"}.get(platform.system(), "windows")
        natives_dir = os.path.join(vdir, f"{version_id}-natives")
        os.makedirs(natives_dir, exist_ok=True)
        for lib in libs:
            classifiers = lib.get("downloads", {}).get("classifiers", {})
            natives = lib.get("natives", {})
            native_key = natives.get(_os_key, "").replace("${arch}", "64")
            if not native_key or native_key not in classifiers:
                continue
            info = classifiers[native_key]
            dest = os.path.join(game_dir, "libraries", info["path"])
            if not self._check_sha1(dest, info.get("sha1")):
                self._download_file(info["url"], dest)
            try:
                with zipfile.ZipFile(dest) as zf:
                    for name in zf.namelist():
                        if not name.endswith("/"):
                            with zf.open(name) as src, open(os.path.join(natives_dir, os.path.basename(name)), "wb") as out:
                                shutil.copyfileobj(src, out)
            except Exception:
                pass
        report("assets_index", 0, 1)
        assets_root = os.path.join(game_dir, "assets")
        asset_index = vjson.get("assetIndex")
        if asset_index:
            index_id = asset_index["id"]
            index_file = os.path.join(assets_root, "indexes", f"{index_id}.json")
            if not self._check_sha1(index_file, asset_index.get("sha1")):
                self._download_file(asset_index["url"], index_file)
            with open(index_file, "r", encoding="utf-8") as f:
                objects = json.load(f).get("objects", {})
            for i, (name, obj) in enumerate(objects.items()):
                if i % 200 == 0:
                    report("assets", i, len(objects))
                h = obj["hash"]
                obj_path = os.path.join(assets_root, "objects", h[:2], h)
                if not self._check_sha1(obj_path, h):
                    self._download_file(f"https://resources.download.minecraft.net/{h[:2]}/{h}", obj_path)
        report("done", 1, 1)

    def _get_java_path(self, version_id):
        game_dir = os.path.abspath(self.gamedir_var.get())
        java_dir = os.path.join(game_dir, "java")
        if self.java_mode_var.get() == "manual" and os.path.exists(self.java_path_var.get()):
            return self.java_path_var.get()
        sys_java = shutil.which("java")
        if sys_java:
            return sys_java
        bundled = self._find_java_in(java_dir)
        if bundled:
            return bundled
        self.ui_log_download("未找到 Java，正在自动下载 Java 17...")
        url = f"https://api.adoptium.net/v3/binary/latest/17/ga/{_OS}/{_ARCH_API}/jre/hotspot/normal/eclipse"
        os.makedirs(java_dir, exist_ok=True)
        archive = os.path.join(tempfile.gettempdir(), "XDMLauncher-java.zip")
        self._download_file(url, archive, lambda d, t: self.ui_center_progress(d/t if t else 0, "下载 Java..."))
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(java_dir)
        try: os.remove(archive)
        except: pass
        return self._find_java_in(java_dir)

    def _find_java_in(self, path):
        for root, dirs, files in os.walk(path):
            if "java.exe" in files: return os.path.join(root, "java.exe")
            if "java" in files: return os.path.join(root, "java")
        return None

    def _build_command(self, game_dir, version_id, player_name, java_path, memory_mb, width, height):
        vdir = self._version_dir(game_dir, version_id)
        with open(os.path.join(vdir, f"{version_id}.json"), "r", encoding="utf-8") as f:
            vjson = json.load(f)
        entries = []
        for lib in vjson.get("libraries", []):
            if not self._lib_rules_allow(lib): continue
            art = lib.get("downloads", {}).get("artifact")
            if art:
                p = os.path.join(game_dir, "libraries", art["path"])
                if os.path.exists(p): entries.append(p)
        entries.append(os.path.join(vdir, f"{version_id}.jar"))
        classpath = ";".join(entries) if platform.system() == "Windows" else ":".join(entries)
        natives_dir = os.path.join(vdir, f"{version_id}-natives")
        
        digest = hashlib.md5(f"OfflinePlayer:{player_name}".encode("utf-8")).digest()
        b = bytearray(digest); b[6] = (b[6] & 0x0F) | 0x30; b[8] = (b[8] & 0x3F) | 0x80
        mc_uuid = str(uuidlib.UUID(bytes=bytes(b)))
        
        repl = {
            "auth_player_name": player_name, "version_name": version_id,
            "game_directory": game_dir, "assets_root": os.path.join(game_dir, "assets"),
            "assets_index_name": vjson.get("assets", "legacy"), "auth_uuid": mc_uuid,
            "auth_access_token": mc_uuid, "user_type": "legacy", "auth_session": mc_uuid,
            "clientid": "0", "auth_xuid": "0", "resolution_width": str(width),
            "resolution_height": str(height), "natives_directory": natives_dir,
            "launcher_name": "XDMLauncher", "launcher_version": APP_VER, "classpath": classpath,
        }
        
        jvm_args = [f"-Xmx{memory_mb}M", f"-Xms{min(memory_mb, 1024)}M", f"-Djava.library.path={natives_dir}"]
        if "arguments" in vjson:
            for arg in vjson["arguments"].get("jvm", []):
                if isinstance(arg, str):
                    for k, v in repl.items(): arg = arg.replace("${" + k + "}", v)
                    jvm_args.append(arg)
        jvm_args.extend(["-cp", classpath, vjson["mainClass"]])
        
        game_args = []
        if "minecraftArguments" in vjson:
            args = vjson["minecraftArguments"]
            for k, v in repl.items(): args = args.replace("${" + k + "}", v)
            game_args = args.split()
        else:
            for arg in vjson.get("arguments", {}).get("game", []):
                if isinstance(arg, str):
                    for k, v in repl.items(): arg = arg.replace("${" + k + "}", v)
                    game_args.append(arg)
        return [java_path] + jvm_args + game_args

    # ========== 下载页 ==========
    def page_download(self):
        lang = LANG[self.cur_lang]
        page = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        page.pack(fill="both", expand=True)
        self.current_page = page

        top_filter_f = ctk.CTkFrame(page, fg_color=CARD_COLOR)
        top_filter_f.pack(fill="x", padx=10, pady=6)
        for text, val in [(lang["dl_game"], "game"), (lang["dl_mod"], "mod"),
                          (lang["dl_shader"], "shader"), (lang["dl_modpack"], "modpack")]:
            ctk.CTkRadioButton(top_filter_f, text=text, variable=self.dl_category_var,
                               value=val, command=self.refresh_dl_view,
                               font=self.font_normal).pack(side="left", padx=5)

        self.filter_bar = ctk.CTkFrame(page, fg_color=CARD_COLOR)
        self.filter_bar.pack(fill="x", padx=10, pady=4)

        self.list_container = ctk.CTkScrollableFrame(page, fg_color=BG_COLOR)
        self.list_container.pack(fill="both", expand=True, padx=10, pady=4)

        log_f = ctk.CTkFrame(page, fg_color=CARD_COLOR)
        log_f.pack(fill="x", padx=10, pady=4)
        self.download_log_box = ctk.CTkTextbox(log_f, fg_color="#0B1A16", height=90,
                                               font=self.font_small)
        self.download_log_box.pack(fill="both", padx=8, pady=4)

        self.refresh_dl_view()

    def refresh_dl_view(self):
        for w in self.filter_bar.winfo_children():
            w.destroy()
        for w in self.list_container.winfo_children():
            w.destroy()

        cat = self.dl_category_var.get()
        lang = LANG[self.cur_lang]
        if cat == "game":
            self._build_game_filter_bar()
            if self.dl_view_stage == "version_list":
                if len(self.full_vanilla_version_list) == 0 and not self.is_verlist_loading:
                    ctk.CTkLabel(self.list_container, text=lang["loading_ver"],
                                 font=self.font_title).pack(pady=30)
                    threading.Thread(target=self.load_all_vanilla_versions, daemon=True).start()
                else:
                    self.fill_game_card_list()
            else:
                self.fill_installer_list()
        else:
            self._build_mod_filter_bar()

    def _build_game_filter_bar(self):
        lang = LANG[self.cur_lang]
        if self.dl_view_stage == "installer_select":
            ctk.CTkButton(self.filter_bar, text=lang["back_to_ver"], width=100,
                          command=self.back_to_version_list,
                          font=self.font_normal).pack(side="left", padx=6)
            ctk.CTkLabel(self.filter_bar, text=f"  {lang['mc_ver_filter']}: {self.selected_mc_version}",
                         font=self.font_bold).pack(side="left", padx=6)
            return
        if not hasattr(self, 'ver_type_filter_var'):
            self.ver_type_filter_var = ctk.StringVar(value="release")
        for text, val in [(lang["ver_type_release"], "release"), (lang["ver_type_snapshot"], "snapshot"),
                          (lang["ver_type_beta"], "beta"), (lang["ver_type_alpha"], "alpha"),
                          (lang["ver_type_all"], "all")]:
            ctk.CTkRadioButton(self.filter_bar, text=text, variable=self.ver_type_filter_var,
                               value=val, command=self.fill_game_card_list,
                               font=self.font_small).pack(side="left", padx=2)
        ctk.CTkLabel(self.filter_bar, text=" | ").pack(side="left")
        self.ver_search_var = ctk.StringVar()
        ctk.CTkEntry(self.filter_bar, textvariable=self.ver_search_var,
                     placeholder_text=lang["search_ver_hint"], width=180,
                     font=self.font_normal).pack(side="left", padx=4)
        self.ver_search_var.trace_add("write", lambda *a: self.fill_game_card_list())

    def _build_mod_filter_bar(self):
        lang = LANG[self.cur_lang]
        hint = lang["modpack_hint"] if self.dl_category_var.get() == "modpack" else lang["search_hint"]
        
        self.search_entry = ctk.CTkEntry(self.filter_bar, placeholder_text=hint, font=self.font_normal)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=4)
        
        ctk.CTkButton(self.filter_bar, text=lang["search"], command=self.thread_modrinth_search,
                      width=80, font=self.font_normal).pack(side="left", padx=4)
                      
        if self.dl_category_var.get() != "modpack":
            ctk.CTkLabel(self.filter_bar, text=lang["loader_filter"],
                         font=self.font_small).pack(side="left", padx=4)
            
            self.loader_select = ctk.CTkComboBox(self.filter_bar,
                values=["any", "fabric", "forge", "neoforge"], width=110,
                state="readonly", font=self.font_small)
            self.loader_select.set("any")
            self.loader_select.pack(side="left", padx=4)
            
            ctk.CTkLabel(self.filter_bar, text=lang["mc_ver_filter"],
                         font=self.font_small).pack(side="left", padx=4)
                         
            self.mcver_select = ctk.CTkEntry(self.filter_bar, placeholder_text="1.20.1",
                                             width=100, font=self.font_small)
            self.mcver_select.pack(side="left", padx=4)
        else:
            self.loader_select = None
            self.mcver_select = None

    def load_all_vanilla_versions(self):
        self.is_verlist_loading = True
        try:
            manifest = self._http_get_json("https://piston-meta.mojang.com/mc/game/version_manifest_v2.json")
            self.full_vanilla_version_list = manifest.get("versions", [])
            self.after(0, self.fill_game_card_list)
        except Exception as e:
            self.ui_log_download(f"版本加载失败：{e}")
        self.is_verlist_loading = False

    def fill_game_card_list(self):
        if not self.list_container.winfo_exists():
            return
        for w in self.list_container.winfo_children():
            w.destroy()
        lang = LANG[self.cur_lang]
        ft = self.ver_type_filter_var.get()
        st = self.ver_search_var.get().lower().strip()
        
        result = []
        for v in self.full_vanilla_version_list:
            v_id = v.get("id", "")
            v_type = v.get("type", "")
            if ft != "all" and v_type != ft:
                continue
            if st and st not in v_id.lower():
                continue
            result.append(v)
            
        if not result:
            ctk.CTkLabel(self.list_container, text=lang["no_result"],
                         font=self.font_normal).pack(pady=30)
            return
        for v in result[:80]:
            card = ctk.CTkFrame(self.list_container, fg_color=CARD_COLOR)
            card.pack(fill="x", pady=3, padx=2)
            info_f = ctk.CTkFrame(card, fg_color=CARD_COLOR)
            info_f.pack(side="left", fill="x", expand=True, padx=10, pady=6)
            ctk.CTkLabel(info_f, text=v["id"], font=self.font_bold).pack(anchor="w")
            ctk.CTkLabel(info_f, text=f"Type: {v['type']}", font=self.font_small,
                         text_color="#B4C9C3").pack(anchor="w")
            ctk.CTkButton(card, text=lang["select_installer"], width=110,
                          command=lambda vid=v["id"]: self.select_version_for_install(vid),
                          font=self.font_normal).pack(side="right", padx=10)

    def select_version_for_install(self, vid):
        self.selected_mc_version = vid
        self.dl_view_stage = "installer_select"
        self.refresh_dl_view()

    def back_to_version_list(self):
        self.dl_view_stage = "version_list"
        self.selected_mc_version = None
        self.refresh_dl_view()

    def fill_installer_list(self):
        for w in self.list_container.winfo_children():
            w.destroy()
        
        lang = LANG[self.cur_lang]
        ctk.CTkLabel(self.list_container, text="正在检测可用安装器，请稍候...", font=self.font_normal).pack(pady=30)

        # 把网络请求放进子线程，防止界面卡死
        def fetch_installers():
            ver = self.selected_mc_version
            game_dir = os.path.abspath(self.gamedir_var.get())
            
            has_fabric = False
            has_forge = False
            has_neoforge = False

            # 1. 检查 Fabric
            try:
                if self._http_get(f"https://meta.fabricmc.net/v2/versions/loader/{ver}") != b"[]":
                    has_fabric = True
            except Exception:
                pass

            # 2. 检查 Forge
            try:
                forge_xml = self._http_get("https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml").decode("utf-8")
                if f"<version>{ver}-" in forge_xml:
                    has_forge = True
            except Exception:
                pass

            # 3. 检查 NeoForge
            try:
                neo_xml = self._http_get("https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml").decode("utf-8")
                if "<version>" in neo_xml:
                    has_neoforge = True
            except Exception:
                pass

            # 回到主线程渲染界面
            self.after(0, lambda: render_installers(has_fabric, has_forge, has_neoforge))

        def render_installers(has_fabric, has_forge, has_neoforge):
            if not self.list_container.winfo_exists():
                return
            for w in self.list_container.winfo_children():
                w.destroy()
                
            ver = self.selected_mc_version
            game_dir = os.path.abspath(self.gamedir_var.get())
            installed = self._is_version_installed(game_dir, ver)

            # 原版
            self._make_installer_card(lang["vanilla"], "vanilla", ver, installed,
                                      lambda: self.thread_install_vanilla(ver))
            # Fabric
            if has_fabric:
                self._make_installer_card(lang["fabric"], "fabric", ver, False,
                                          lambda: self.thread_install_fabric(ver))
            # Forge
            if has_forge:
                self._make_installer_card(lang["forge"], "forge", ver, False,
                                          lambda: self.thread_install_forge(ver))
            # NeoForge
            if has_neoforge:
                self._make_installer_card(lang["neoforge"], "neoforge", ver, False,
                                          lambda: self.thread_install_neoforge(ver))

        # 启动子线程
        threading.Thread(target=fetch_installers, daemon=True).start()

    def _make_installer_card(self, name, loader_id, mc_ver, is_installed, install_cmd):
        lang = LANG[self.cur_lang]
        card = ctk.CTkFrame(self.list_container, fg_color=CARD_COLOR)
        card.pack(fill="x", pady=4, padx=2)
        info_f = ctk.CTkFrame(card, fg_color=CARD_COLOR)
        info_f.pack(side="left", fill="x", expand=True, padx=10, pady=8)
        ctk.CTkLabel(info_f, text=name, font=self.font_bold).pack(anchor="w")
        ctk.CTkLabel(info_f, text=f"MC {mc_ver}", font=self.font_small,
                     text_color="#B4C9C3").pack(anchor="w")
        if is_installed:
            ctk.CTkLabel(card, text=lang["already_installed"], font=self.font_normal,
                         text_color="#2A9D6F").pack(side="right", padx=10)
        else:
            ctk.CTkButton(card, text=lang["install_now"], width=100, command=install_cmd,
                          font=self.font_normal, fg_color="#2A725F",
                          hover_color="#348C74").pack(side="right", padx=10)

    def _run_install_task(self, task_func, desc, task_name):
        if self.is_game_downloading:
            self.ui_log_download(LANG[self.cur_lang]["working"])
            return
        self.is_game_downloading = True
        lang = LANG[self.cur_lang]
        self.show_banner(lang["top_start"].format(name=task_name), color="#1E4D3F", auto_hide=0)
        self.ui_log_download(desc)
        self.ui_center_progress(0, lang["progress_installing"])

        def wrapper():
            ok = False
            try:
                task_func()
                ok = True
            except Exception as e:
                self.ui_log_download(f"{lang['install_fail']}: {e}")
            finally:
                self.is_game_downloading = False

            if ok:
                self.ui_center_progress(0.95, lang["progress_checking"])
                self.ui_log_download(lang["integrity_check"])
                integ = self.check_integrity(self.selected_mc_version or "")
                if integ:
                    self.ui_log_download(lang["integrity_ok"])
                    self.ui_center_progress(1.0, "100%")
                    self.show_banner(lang["top_done"].format(name=task_name),
                                     color="#1E6B3F", auto_hide=5000)
                    self.after(1200, self.ui_center_progress_hide)
                    self.after(800, self.back_to_version_list)
                else:
                    self.ui_log_download(lang["integrity_fail"])
                    self.show_banner(lang["top_fail"].format(name=task_name),
                                     color="#6B1E1E", auto_hide=5000)
                    self.after(1500, self.ui_center_progress_hide)
            else:
                self.show_banner(lang["top_fail"].format(name=task_name),
                                 color="#6B1E1E", auto_hide=5000)
                self.after(1500, self.ui_center_progress_hide)

        threading.Thread(target=wrapper, daemon=True).start()

    def check_integrity(self, vid):
        if not vid:
            return True
        game_dir = os.path.abspath(self.gamedir_var.get())
        ver_dir = os.path.join(game_dir, "versions", vid)
        json_path = os.path.join(ver_dir, f"{vid}.json")
        return os.path.isdir(ver_dir) and os.path.exists(json_path)
        
    def thread_install_vanilla(self, ver):
        game_dir = os.path.abspath(self.gamedir_var.get())
        def task():
            def report(phase, cur, total):
                if phase == "client":
                    self.ui_center_progress(cur/total if total else 0, "下载客户端文件...")
                elif phase == "libraries":
                    self.ui_center_progress(cur/total if total else 0, f"下载依赖库 {cur}/{total}...")
                elif phase == "assets":
                    self.ui_center_progress(cur/total if total else 0, f"下载资源文件 {cur}/{total}...")
                else:
                    self.ui_center_progress(cur/total if total else 0, "校验中...")
            self._install_vanilla(game_dir, ver, report)
        self._run_install_task(task, f"Vanilla {ver}", f"Vanilla {ver}")

    def thread_install_fabric(self, ver):
        game_dir = os.path.abspath(self.gamedir_var.get())
        def task():
            if not self._is_version_installed(game_dir, ver):
                self.ui_log_download(f"先安装原版 {ver}...")
                self._install_vanilla(game_dir, ver, lambda p, c, t: None)
            
            self.ui_log_download(f"正在获取 Fabric 配置...")
            profile = self._http_get_json(f"https://meta.fabricmc.net/v2/versions/loader/{ver}/latest/profile/json")
            version_id = profile["id"]
            
            vdir = self._version_dir(game_dir, version_id)
            os.makedirs(vdir, exist_ok=True)
            with open(os.path.join(vdir, f"{version_id}.json"), "w", encoding="utf-8") as f:
                json.dump(profile, f)
                
            libs = profile.get("libraries", [])
            for i, lib in enumerate(libs):
                self.ui_center_progress(i/len(libs), "下载 Fabric 库")
                art = lib.get("downloads", {}).get("artifact")
                if art:
                    path = os.path.join(game_dir, "libraries", art["path"])
                    if not self._check_sha1(path, art.get("sha1")):
                        self._download_file(art["url"], path)
            
            src_jar = os.path.join(game_dir, "versions", ver, f"{ver}.jar")
            dst_jar = os.path.join(vdir, f"{version_id}.jar")
            if not os.path.exists(dst_jar) and os.path.exists(src_jar):
                shutil.copy2(src_jar, dst_jar)
                
        self._run_install_task(task, f"Fabric {ver}", f"Fabric {ver}")

    def thread_install_forge(self, ver):
        game_dir = os.path.abspath(self.gamedir_var.get())
        def task():
            if not self._is_version_installed(game_dir, ver):
                self._install_vanilla(game_dir, ver, lambda p, c, t: None)
                
            self.ui_log_download("获取 Forge 版本号...")
            xml = self._http_get("https://maven.minecraftforge.net/net/minecraftforge/forge/maven-metadata.xml").decode()
            import re
            versions = re.findall(rf"<version>({ver}-[^<]+)</version>", xml)
            if not versions: raise Exception("未找到对应的 Forge 版本")
            fv = versions[-1]
            
            url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{fv}/forge-{fv}-installer.jar"
            tmp = os.path.join(tempfile.gettempdir(), "forge-installer.jar")
            self.ui_log_download("下载 Forge 安装器...")
            self._download_file(url, tmp, lambda d, t: self.ui_center_progress(d/t if t else 0, "下载中..."))
            
            self.ui_log_download("运行 Forge 安装器...")
            java_path = self._get_java_path(ver)
            subprocess.run([java_path, "-jar", tmp, "--installClient", game_dir], check=True)
            
        self._run_install_task(task, f"Forge {ver}", f"Forge {ver}")

    def thread_install_neoforge(self, ver):
        game_dir = os.path.abspath(self.gamedir_var.get())
        def task():
            if not self._is_version_installed(game_dir, ver):
                self._install_vanilla(game_dir, ver, lambda p, c, t: None)
                
            self.ui_log_download("获取 NeoForge 版本号...")
            xml = self._http_get("https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml").decode()
            import re
            versions = re.findall(r"<version>([^<]+)</version>", xml)
            prefix = ".".join(ver.split(".")[1:])
            matches = [v for v in versions if v.startswith(prefix)]
            if not matches: raise Exception("未找到对应的 NeoForge 版本")
            nv = matches[-1]
            
            url = f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{nv}/neoforge-{nv}-installer.jar"
            tmp = os.path.join(tempfile.gettempdir(), "neoforge-installer.jar")
            self.ui_log_download("下载 NeoForge 安装器...")
            self._download_file(url, tmp, lambda d, t: self.ui_center_progress(d/t if t else 0, "下载中..."))
            
            self.ui_log_download("运行 NeoForge 安装器...")
            java_path = self._get_java_path(ver)
            subprocess.run([java_path, "-jar", tmp, "--installClient", game_dir], check=True)
            
        self._run_install_task(task, f"NeoForge {ver}", f"NeoForge {ver}")

    def thread_modrinth_search(self):
        if self.is_searching:
            return
        self.is_searching = True
        threading.Thread(target=self.modrinth_search, daemon=True).start()

    def modrinth_search(self):
        lang = LANG[self.cur_lang]
        if not self.search_entry or not self.search_entry.winfo_exists():
            self.is_searching = False
            return
        query = self.search_entry.get().strip()
        cat = self.dl_category_var.get()
        if not query:
            self.is_searching = False
            return
        
        loader = "any"
        if self.loader_select is not None and self.loader_select.winfo_exists():
            loader = self.loader_select.get()
            
        mcver = ""
        if self.mcver_select is not None and self.mcver_select.winfo_exists():
            mcver = self.mcver_select.get().strip()

        try:
            fac = {"mod": "mod", "shader": "shader", "modpack": "modpack"}.get(cat, "mod")
            facet_list = [[f"project_type:{fac}"]]
            if loader != "any":
                facet_list.append([f"categories:{loader}"])
            if mcver:
                facet_list.append([f"versions:{mcver}"])
            
            params = {"query": query, "facets": json.dumps(facet_list), "limit": 20}
            url = "https://modrinth.cd/v2/search"
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            res = resp.json()
        except Exception as e:
            self.ui_log_download(lang["search_fail"] + f" {e}")
            self.is_searching = False
            return
            
        self.result_data_list = res.get("hits", [])

        def render():
            if not self.list_container.winfo_exists():
                self.is_searching = False
                return
            for w in self.list_container.winfo_children():
                w.destroy()
            if not self.result_data_list:
                ctk.CTkLabel(self.list_container, text=lang["no_result"],
                             font=self.font_normal).pack(pady=20)
                self.is_searching = False
                return
            for hit in self.result_data_list:
                pid = hit["project_id"]
                f = ctk.CTkFrame(self.list_container, fg_color=CARD_COLOR)
                f.pack(fill="x", pady=4, padx=2)
                info_f = ctk.CTkFrame(f, fg_color=CARD_COLOR)
                info_f.pack(side="left", fill="x", expand=True, padx=10, pady=8)
                ctk.CTkLabel(info_f, text=hit["title"], font=self.font_bold).pack(anchor="w")
                ctk.CTkLabel(info_f, text=hit.get("description", "")[:100],
                             font=self.font_small, text_color="#B4C9C3").pack(anchor="w")
                ctk.CTkButton(f, text=lang["download_start"], width=90,
                              command=lambda p=pid, t=cat: self.thread_download_modrinth(p, t),
                              font=self.font_normal).pack(side="right", padx=10)
            self.is_searching = False

        self.after(0, render)

    def thread_download_modrinth(self, project_id, res_type):
        threading.Thread(target=self.download_modrinth_file,
                         args=(project_id, res_type), daemon=True).start()

    def download_modrinth_file(self, project_id, res_type):
        lang = LANG[self.cur_lang]
        game_root = os.path.abspath(self.gamedir_var.get())
        name = project_id
        try:
            url = f"https://modrinth.cd/v2/project/{project_id}/version"
            v_list = requests.get(url, timeout=15).json()
            if not v_list:
                self.ui_log_download("无可用版本")
                return
            best = v_list[0]
            name = best.get("name", project_id)
            file_info = best["files"][0]
            dl_url, fn = file_info["url"], file_info["filename"]

            self.show_banner(lang["top_start"].format(name=fn), color="#1E4D3F", auto_hide=0)
            self.ui_center_progress(0, fn[:40])

            if res_type == "mod":
                dest_folder = os.path.join(game_root, "mods")
                save_path = os.path.join(dest_folder, fn)
                os.makedirs(dest_folder, exist_ok=True)
                self._stream_download(dl_url, save_path)
            elif res_type == "shader":
                dest_folder = os.path.join(game_root, "shaderpacks")
                save_path = os.path.join(dest_folder, fn)
                os.makedirs(dest_folder, exist_ok=True)
                self._stream_download(dl_url, save_path)
            else:
                tmp = os.path.join(tempfile.gettempdir(), fn)
                self._stream_download(dl_url, tmp)
                self.ui_log_download(lang["modpack_installing"])
                self._install_modpack(tmp, game_root)

            self.ui_center_progress(1.0, "100%")
            self.ui_log_download(f"{lang['dl_success']} {fn}")
            self.show_banner(lang["top_done"].format(name=name), color="#1E6B3F", auto_hide=5000)
            self.after(1500, self.ui_center_progress_hide)
        except Exception as e:
            import traceback
            err_detail = traceback.format_exc()
            self.ui_log_download(f"{lang['dl_fail']}: {e}")
            self.ui_log_download(err_detail)
            self.show_banner(lang["top_fail"].format(name=name), color="#6B1E1E", auto_hide=5000)
            self.after(1500, self.ui_center_progress_hide)
            messagebox.showerror("下载失败", f"错误信息：{e}\n\n如果是网络问题，请检查网络连接。")

    def _stream_download(self, url, save_path):
        def cb(downloaded, total):
            if total > 0:
                self.ui_center_progress(downloaded / total, os.path.basename(save_path)[:40])
            else:
                self.ui_center_progress(0, f"{downloaded // 1024} KB")
        self._download_file(url, save_path, progress_cb=cb)

    def _install_modpack(self, mrpack_path, game_root):
        tmp_dir = os.path.join(game_root, "_mrpack_tmp")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        with zipfile.ZipFile(mrpack_path, "r") as z:
            z.extractall(tmp_dir)
        idx_path = os.path.join(tmp_dir, "modrinth.index.json")
        if not os.path.exists(idx_path):
            shutil.rmtree(tmp_dir, ignore_errors=True)
            raise RuntimeError("无效的整合包格式")
        with open(idx_path, "r", encoding="utf-8") as f:
            idx = json.load(f)
        deps = idx.get("dependencies", {})
        mc_ver = deps.get("minecraft")
        
        if mc_ver:
            game_dir = os.path.abspath(self.gamedir_var.get())
            try:
                if "fabric-loader" in deps:
                    self.ui_log_download(f"安装 Fabric for {mc_ver}")
                    self.thread_install_fabric(mc_ver)
                elif "forge" in deps:
                    self.ui_log_download(f"安装 Forge for {mc_ver}")
                    self.thread_install_forge(mc_ver)
                elif "neoforge" in deps:
                    self.ui_log_download(f"安装 NeoForge for {mc_ver}")
                    self.thread_install_neoforge(mc_ver)
                else:
                    self.ui_log_download(f"安装原版 {mc_ver}")
                    self._install_vanilla(game_dir, mc_ver, lambda p, c, t: None)
            except Exception as e:
                self.ui_log_download(f"加载器安装失败: {e}")

        file_list = idx.get("files", [])
        total = len(file_list)
        for i, item in enumerate(file_list):
            downloads = item.get("downloads", [])
            if not downloads:
                continue
            path = os.path.join(game_root, item["path"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            try:
                self._stream_download(downloads[0], path)
            except Exception as e:
                self.ui_log_download(f"文件失败 {item['path']}: {e}")
            
            self.ui_center_progress((i + 1) / max(total, 1), f"整合包文件 {i+1}/{total}")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        self.ui_log_download("✅ 整合包安装完成")

    # ========== 设置页 ==========
    def page_settings(self):
        lang = LANG[self.cur_lang]
        page = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        page.pack(fill="both", expand=True)
        self.current_page = page

        def row(label_text):
            r = ctk.CTkFrame(page, fg_color=CARD_COLOR)
            r.pack(fill="x", padx=10, pady=5)
            ctk.CTkLabel(r, text=label_text, font=self.font_bold).pack(side="left", padx=8)
            return r

        r1 = row(lang["mem"])
        ctk.CTkEntry(r1, textvariable=self.mem_var, width=120, font=self.font_normal).pack(side="left")
        ctk.CTkLabel(r1, text=" MB", font=self.font_normal).pack(side="left")

        r2 = row(lang["game_dir"])
        ctk.CTkEntry(r2, textvariable=self.gamedir_var, font=self.font_normal).pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkButton(r2, text=lang["browse"], command=self.select_dir, width=70, font=self.font_normal).pack(side="left")

        r3 = row(lang["lang_text"])
        ctk.CTkButton(r3, text="中文(简体)", command=lambda: self.switch_lang("zh"), width=120, font=self.font_normal).pack(side="left", padx=3)
        ctk.CTkButton(r3, text="English(UK)", command=lambda: self.switch_lang("en"), width=120, font=self.font_normal).pack(side="left", padx=3)

        r4 = row(lang["skin"])
        ctk.CTkButton(r4, text=lang["upload"], command=self.upload_skin, width=80, font=self.font_normal).pack(side="left", padx=3)
        ctk.CTkLabel(r4, text=lang["cape"], font=self.font_bold).pack(side="left", padx=12)
        ctk.CTkButton(r4, text=lang["upload"], command=self.upload_cape, width=80, font=self.font_normal).pack(side="left", padx=3)

        r5 = row(lang["java"])
        ctk.CTkRadioButton(r5, text=lang["auto"], variable=self.java_mode_var, value="auto", font=self.font_normal).pack(side="left")
        ctk.CTkRadioButton(r5, text=lang["manual"], variable=self.java_mode_var, value="manual", font=self.font_normal).pack(side="left", padx=8)
        ctk.CTkButton(r5, text=lang["browse"], command=self.select_java, width=70, font=self.font_normal).pack(side="left")
        if self.java_path_var.get():
            ctk.CTkLabel(r5, text=os.path.basename(self.java_path_var.get()), font=self.font_small, text_color="#B4C9C3").pack(side="left", padx=6)

        r6 = row(lang["win_size"])
        ctk.CTkEntry(r6, textvariable=self.win_w, width=80, font=self.font_normal).pack(side="left")
        ctk.CTkLabel(r6, text=" × ", font=self.font_normal).pack(side="left")
        ctk.CTkEntry(r6, textvariable=self.win_h, width=80, font=self.font_normal).pack(side="left")

        btn_row = ctk.CTkFrame(page, fg_color=BG_COLOR)
        btn_row.pack(fill="x", padx=10, pady=12)
        ctk.CTkButton(btn_row, text=lang["reset"], command=self.reset_cfg, fg_color="#502828", font=self.font_normal).pack(side="left")
        ctk.CTkButton(btn_row, text=lang["save"], command=self._save_config_ui, fg_color="#246B42", font=self.font_normal).pack(side="right")

    def _save_config_ui(self):
        self._save_config()
        messagebox.showinfo("Info", LANG[self.cur_lang]["config_saved"])

    def select_dir(self):
        p = filedialog.askdirectory()
        if p:
            self.gamedir_var.set(p)

    def select_java(self):
        p = filedialog.askopenfilename(title="选择 java.exe", filetypes=[("Java", "java.exe")])
        if p:
            self.java_path_var.set(p)
            self.switch_page("settings")

    def upload_skin(self):
        p = filedialog.askopenfilename(title="选择皮肤", filetypes=[("PNG", "*.png")])
        if p:
            try:
                shutil.copy2(p, "custom_skin.png")
                messagebox.showinfo("Info", LANG[self.cur_lang]["upload_skin_success"])
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", LANG[self.cur_lang]["skin_not_found"])

    def upload_cape(self):
        p = filedialog.askopenfilename(title="选择披风", filetypes=[("PNG", "*.png")])
        if p:
            try:
                shutil.copy2(p, "custom_cape.png")
                messagebox.showinfo("Info", LANG[self.cur_lang]["upload_cape_success"])
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Warning", LANG[self.cur_lang]["cape_not_found"])

    def reset_cfg(self):
        if not messagebox.askyesno("Confirm", LANG[self.cur_lang]["reset_confirm"]):
            return
        self.cur_lang = "zh"
        self.username_var.set("")
        self.remember_var.set(False)
        self.mem_var.set("2048")
        self.gamedir_var.set("./minecraft")
        self.java_mode_var.set("auto")
        self.java_path_var.set("")
        self.win_w.set("854")
        self.win_h.set("480")
        self._save_config()
        self.switch_page("settings")
        messagebox.showinfo("Info", LANG[self.cur_lang]["reset_done"])

    # ========== 关于页（全部靠左） ==========
    def page_about(self):
        lang = LANG[self.cur_lang]
        page = ctk.CTkFrame(self.main_frame, fg_color=BG_COLOR)
        page.pack(fill="both", expand=True)
        self.current_page = page

        left_f = ctk.CTkFrame(page, fg_color=BG_COLOR)
        left_f.pack(side="left", fill="y", anchor="n", padx=20, pady=20)

        ctk.CTkLabel(left_f, text="XDMLauncher for Windows", font=ctk.CTkFont(family=FONT_FAMILY, size=24, weight="bold"), anchor="w", justify="left").pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(left_f, text=APP_VER, font=self.font_title, anchor="w", justify="left").pack(anchor="w", pady=(0, 16))
        ctk.CTkLabel(left_f, text="GitHub:https://github.com/xiaodong0215/XDMLauncher | QQ:3697272702", font=self.font_normal, anchor="w", justify="left").pack(anchor="w", pady=(0, 16))
        ctk.CTkButton(left_f, text=lang["check_update"], command=self.check_update, font=self.font_normal).pack(anchor="w", pady=6)

    def check_update(self):
        lang = LANG[self.cur_lang]
        self.ui_log_download(lang["checking_update"])
        def task():
            self.after(0, lambda: messagebox.showinfo(lang["check_update"], lang["update_latest"].format(ver=APP_VER)))
        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    app = XDMLauncher()
    app.mainloop()
