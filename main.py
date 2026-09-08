import os
import requests
import webbrowser
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.core.text import LabelBase
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle

# 1. ตั้งค่าการลงทะเบียนฟอนต์ภาษาไทย
FONT_NAME = 'Roboto'

font_paths = [
    'NotoSansThai-Black.ttf',
    'NotoSansThai-VariableFont_wdth,wght.ttf',
    '/storage/emulated/0/Android/data/ru.iiec.pydroid3/files/NotoSansThai-Black.ttf'
]

font_found = False
for path in font_paths:
    if os.path.exists(path):
        LabelBase.register(name='Roboto', fn_regular=path)
        font_found = True
        break

# การ์ดตกแต่งพื้นหลัง
class StyledCard(BoxLayout):
    def __init__(self, bg_color=(0.16, 0.18, 0.23, 1), radius=[15], **kwargs):
        super().__init__(**kwargs)
        self.padding = 10
        with self.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=radius)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

# ปุ่มกดดีไซน์ใหม่
class ModernButton(Button):
    def __init__(self, bg_color=(0.2, 0.6, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.custom_color = bg_color
        
        with self.canvas.before:
            Color(*self.custom_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

# --- หน้าที่ 1: หน้าหลัก (Main Screen) ---
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=15)

        # พื้นหลังหลัก
        with main_layout.canvas.before:
            Color(0.11, 0.12, 0.15, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        main_layout.bind(pos=self.update_bg, size=self.update_bg)

        # 1. แถบด้านบนสุด (Top Bar)
        top_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        
        app_title = Label(
            text="[b]ออโต้หาคีย์[/b]",
            markup=True,
            font_size='60sp',
            color=(1, 0.8, 0.2, 1),
            size_hint=(0.6, 1),
            halign='left',
            valign='middle'
        )
        app_title.bind(size=app_title.setter('text_size'))

        # ปุ่มเกี่ยวกับผู้สร้าง (ขวาบน)
        btn_about = ModernButton(
            bg_color=(0.3, 0.35, 0.45, 1),
            text="เกี่ยวกับผู้สร้าง",
            size_hint=(0.1, 0),
            font_size='12sp'
        )
        btn_about.bind(on_press=self.go_to_about)

        top_bar.add_widget(app_title)
        top_bar.add_widget(btn_about)
        main_layout.add_widget(top_bar)

        # 2. หัวข้อโปรแกรม
        header_card = StyledCard(size_hint=(1, 0.12), orientation='vertical')
        self.sub_label = Label(
            text="(BOT-TOS) ระบบออโต้หาคีย์ข้ามลิงก์",
            font_size='28sp',
            color=(0.7, 0.75, 0.8, 1)
        )
        header_card.add_widget(self.sub_label)
        main_layout.add_widget(header_card)

        # 3. ช่องกรอกลิงก์
        input_card = StyledCard(size_hint=(1, 0.15))
        self.url_input = TextInput(
            hint_text="วางลิงก์ที่ต้องการหาคีย์ที่นี่... (Paste URL here)",
            multiline=False,
            size_hint=(1, 1),
            background_color=(0, 0, 0, 0),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.5, 0.5, 0.6, 1),
            padding_y=[10, 10],
            font_size='25sp'
        )
        input_card.add_widget(self.url_input)
        main_layout.add_widget(input_card)

        # 4. ปุ่มกดทำงาน
        self.btn_bypass = ModernButton(
            bg_color=(0.15, 0.45, 0.9, 1),
            text="เริ่มหาคีย์ (Auto Key)",
            size_hint=(1, 0.13),
            font_size='40sp',
            bold=True
        )
        self.btn_bypass.bind(on_press=self.start_bypass)
        main_layout.add_widget(self.btn_bypass)

        # 5. แสดงผลลัพธ์ (เพิ่ม use_bubble=False และ use_handles=False เพื่อปิดคำว่า Select All)
        result_card = StyledCard(size_hint=(1, 0.25))
        self.result_input = TextInput(
            hint_text="ผลลัพธ์คีย์จะแสดงที่นี่... (Result will appear here)",
            readonly=True,
            use_bubble=False,   # ปิดเมนู Select All / Copy / Cut เมื่อกดค้าง
            use_handles=False,  # ปิดหมุดเลื่อนคลุมข้อความ
            size_hint=(1, 1),
            background_color=(0, 0, 0, 0),
            foreground_color=(0.4, 0.9, 0.5, 1),
            hint_text_color=(0.5, 0.5, 0.6, 1),
            font_size='25sp'
        )
        result_card.add_widget(self.result_input)
        main_layout.add_widget(result_card)

        # 6. ปุ่มคัดลอก
        self.btn_copy = ModernButton(
            bg_color=(0.18, 0.65, 0.35, 1),
            text="(Copy Key) คัดลอกคีย์ผลลัพธ์",
            size_hint=(1, 0.12),
            font_size='35sp',
            bold=True
        )
        self.btn_copy.bind(on_press=self.copy_result)
        main_layout.add_widget(self.btn_copy)

        self.add_widget(main_layout)

    def update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def go_to_about(self, instance):
        self.manager.current = 'about'

    def start_bypass(self, instance):
        target_url = self.url_input.text.strip()
        if not target_url:
            self.result_input.text = "(Please enter URL) กรุณากรอกลิงก์ก่อนครับ"
            return

        self.result_input.text = "(Processing...) กำลังประมวลผลหาคีย์ กรุณารอสักครู่"
        Clock.schedule_once(lambda dt: self.process_url(target_url), 0.1)

    def process_url(self, target_url):
        api_endpoint = "https://baconbypass.xyz/api/bypass"
        headers = {
            "User-Agent": "Mozilla/5.0 (Android; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
            "Content-Type": "application/json"
        }
        payload = {"url": target_url}

        try:
            response = requests.post(api_endpoint, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                res_url = data.get("result") or data.get("bypassed_url") or str(data)
                self.result_input.text = res_url
            else:
                self.result_input.text = f"(Server Error) เกิดข้อผิดพลาด HTTP {response.status_code}"
        except Exception as e:
            self.result_input.text = f"(Connection Failed) การเชื่อมต่อล้มเหลว: {str(e)}"

    def copy_result(self, instance):
        res_text = self.result_input.text.strip()
        if res_text and not res_text.startswith("(") and not res_text.startswith("กรุณา"):
            Clipboard.copy(res_text)
            self.btn_copy.text = "(Copied!) คัดลอกคีย์เรียบร้อยแล้ว"
            Clock.schedule_once(self.reset_copy_btn, 2)
        else:
            self.btn_copy.text = "(No Key) ไม่มีคีย์ให้คัดลอก"
            Clock.schedule_once(self.reset_copy_btn, 2)

    def reset_copy_btn(self, dt):
        self.btn_copy.text = "(Copy Key) คัดลอกคีย์ผลลัพธ์"

# --- หน้าที่ 2: หน้าเกี่ยวกับผู้สร้าง ---
class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        about_layout = BoxLayout(orientation='vertical', padding=[20, 25, 20, 25], spacing=15)

        with about_layout.canvas.before:
            Color(0.11, 0.12, 0.15, 1)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size)
        about_layout.bind(pos=self.update_bg, size=self.update_bg)

        # การ์ดข้อมูลผู้สร้าง
        info_card = StyledCard(size_hint=(1, 0.4), orientation='vertical')
        
        title = Label(
            text="[b]เกี่ยวกับผู้สร้าง (About Creator)[/b]",
            markup=True,
            font_size='20sp',
            color=(1, 0.8, 0.2, 1),
            size_hint=(1, 0.35)
        )
        desc = Label(
            text="ออโต้หาคีย์ (BOT-TOS)\nพัฒนาขึ้นเพื่อความสะดวกในการข้ามลิงก์หาคีย์อัตโนมัติ",
            font_size='14sp',
            color=(0.8, 0.8, 0.8, 1),
            halign='center',
            size_hint=(1, 0.65)
        )
        info_card.add_widget(title)
        info_card.add_widget(desc)
        about_layout.add_widget(info_card)

        # ช่องทางการติดต่อ
        link_title = Label(
            text="ช่องทางการติดต่อผู้สร้าง", 
            font_size='15sp', 
            color=(0.7, 0.75, 0.8, 1), 
            size_hint=(1, 0.08)
        )
        about_layout.add_widget(link_title)

        # ปุ่ม TikTok
        btn_tiktok = ModernButton(
            bg_color=(0.9, 0.15, 0.35, 1),
            text="TikTok: @k_a_e_w.01",
            size_hint=(1, 0.18),
            font_size='16sp',
            bold=True
        )
        btn_tiktok.bind(on_press=self.confirm_open_tiktok)
        about_layout.add_widget(btn_tiktok)

        # ปุ่มย้อนกลับ (ปรับขนาดให้เล็กลง)
        btn_back = ModernButton(
            bg_color=(0.25, 0.3, 0.38, 1),
            text="ย้อนกลับ (Back)",
            size_hint=(1, 0.09),
            font_size='13sp',
            bold=True
        )
        btn_back.bind(on_press=self.go_back)
        about_layout.add_widget(btn_back)

        self.add_widget(about_layout)

    def update_bg(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def confirm_open_tiktok(self, instance):
        content = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        msg = Label(
            text="ต้องการเปิดไปยัง TikTok หรือไม่?",
            font_size='15sp',
            color=(1, 1, 1, 1)
        )
        content.add_widget(msg)

        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.4))
        
        btn_yes = ModernButton(
            bg_color=(0.9, 0.15, 0.35, 1),
            text="เปิดลิงก์",
            font_size='14sp',
            bold=True
        )
        btn_no = ModernButton(
            bg_color=(0.4, 0.4, 0.45, 1),
            text="ยกเลิก",
            font_size='14sp'
        )

        popup = Popup(
            title="ยืนยันการเปิดลิงก์",
            content=content,
            size_hint=(0.85, 0.3),
            auto_dismiss=False
        )

        def open_and_close(inst):
            webbrowser.open("https://www.tiktok.com/@k_a_e_w.01")
            popup.dismiss()

        btn_yes.bind(on_press=open_and_close)
        btn_no.bind(on_press=popup.dismiss)

        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)
        content.add_widget(btn_layout)

        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main'

# --- ตัวจัดการหน้า ---
class AutoKeyApp(App):
    def build(self):
        self.title = "ออโต้หาคีย์"
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(AboutScreen(name='about'))
        return sm

if __name__ == "__main__":
    AutoKeyApp().run()
