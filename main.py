import sys
import io
import builtins
import threading
import traceback
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.core.window import Window

# ตรวจสอบการติดตั้ง Google GenAI SDK
try:
    from google import genai
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class PythonMobileIDE(App):
    def build(self):
        self.title = "Python 3 Mobile IDE & Smart AI Agent"
        Window.clearcolor = (0.1, 0.1, 0.1, 1)

        # state สำหรับกันเรียกซ้ำ / กัน popup ซ้อน
        self._running_code = False
        self._running_ai = False
        self.popup = None

        tb_panel = TabbedPanel(do_default_tab=False)

        # ==========================================================
        # TAB 1: 💻 โค้ด & รัน
        # ==========================================================
        editor_tab = TabbedPanelItem(text='💻 โค้ด & รัน')
        editor_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.code_input = TextInput(
            text='# พิมพ์โค้ด Python ของคุณที่นี่...\nprint("ยินดีต้อนรับสู่ Python Mobile IDE!")\n\nfor i in range(3):\n    print("กำลังรันรอบที่:", i + 1)',
            font_size=15,
            font_name='Roboto',
            background_color=(0.15, 0.15, 0.15, 1),
            foreground_color=(0.8, 1.0, 0.8, 1),
            multiline=True,
            size_hint_y=0.4
        )
        editor_layout.add_widget(self.code_input)

        # แถวที่ 1
        btn_row1 = BoxLayout(size_hint_y=None, height=45, spacing=10)
        self.run_btn = Button(text='▶️ รันโค้ด', background_color=(0.1, 0.6, 0.3, 1), font_size=15)
        self.run_btn.bind(on_press=self.run_code)
        btn_row1.add_widget(self.run_btn)

        self.save_btn = Button(text='💾 บันทึกไฟล์', background_color=(0.2, 0.4, 0.8, 1), font_size=15)
        self.save_btn.bind(on_press=self.show_save_popup)
        btn_row1.add_widget(self.save_btn)
        editor_layout.add_widget(btn_row1)

        # แถวที่ 2
        btn_row2 = BoxLayout(size_hint_y=None, height=45, spacing=10)
        self.clear_out_btn = Button(text='🧹 ล้างผลลัพธ์', background_color=(0.7, 0.5, 0.1, 1), font_size=15)
        self.clear_out_btn.bind(on_press=self.clear_output)
        btn_row2.add_widget(self.clear_out_btn)

        self.clear_code_btn = Button(text='🗑️ ล้างโค้ด', background_color=(0.8, 0.2, 0.2, 1), font_size=15)
        self.clear_code_btn.bind(on_press=self.clear_code)
        btn_row2.add_widget(self.clear_code_btn)
        editor_layout.add_widget(btn_row2)

        # พื้นที่แสดงผล
        self.output_label = Label(
            text='[ผลลัพธ์การรันจะแสดงที่นี่]',
            font_size=14,
            halign='left',
            valign='top',
            size_hint_y=None,
            color=(1, 1, 1, 1)
        )
        self.output_label.bind(width=lambda *x: setattr(self.output_label, 'text_size', (self.output_label.width, None)))
        self.output_label.bind(texture_size=lambda *x: setattr(self.output_label, 'height', self.output_label.texture_size[1]))

        scroll_out = ScrollView(size_hint_y=0.4)
        scroll_out.add_widget(self.output_label)
        editor_layout.add_widget(scroll_out)

        editor_tab.add_widget(editor_layout)
        tb_panel.add_widget(editor_tab)

        # ==========================================================
        # TAB 2: 🤖 AI ค้นหาข้อมูล
        # ==========================================================
        ai_tab = TabbedPanelItem(text='🤖 AI ค้นหาข้อมูล')
        ai_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # ช่อง API Key + ปุ่ม show/hide
        key_layout = BoxLayout(size_hint_y=None, height=40, spacing=5)
        key_layout.add_widget(Label(text='API Key:', size_hint_x=None, width=70, font_size=14))
        self.api_key_input = TextInput(
            text='',
            hint_text='ใส่ Gemini API Key ที่นี่',
            multiline=False,
            password=True,
            font_size=14
        )
        key_layout.add_widget(self.api_key_input)

        self.toggle_key_btn = Button(
            text='👁️',
            size_hint_x=None,
            width=50,
            background_color=(0.4, 0.4, 0.4, 1),
            font_size=16
        )
        self.toggle_key_btn.bind(on_press=self.toggle_api_key_visibility)
        key_layout.add_widget(self.toggle_key_btn)
        ai_layout.add_widget(key_layout)

        # พื้นที่ผลลัพธ์ AI
        self.ai_chat_label = Label(
            text='[ยินดีต้อนรับ! กรอก API Key ด้านบน แล้วพิมพ์หัวข้อที่ต้องการให้ AI ค้นหาข้อมูลเชิงลึกได้เลย]',
            font_size=14,
            halign='left',
            valign='top',
            size_hint_y=None,
            color=(0.9, 0.9, 1.0, 1)
        )
        self.ai_chat_label.bind(width=lambda *x: setattr(self.ai_chat_label, 'text_size', (self.ai_chat_label.width, None)))
        self.ai_chat_label.bind(texture_size=lambda *x: setattr(self.ai_chat_label, 'height', self.ai_chat_label.texture_size[1]))

        scroll_ai = ScrollView(size_hint_y=0.7)
        scroll_ai.add_widget(self.ai_chat_label)
        ai_layout.add_widget(scroll_ai)

        # แถบพิมพ์หัวข้อ + ปุ่มสืบค้น
        prompt_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.ai_prompt_input = TextInput(
            text='',
            hint_text='พิมพ์หัวข้อที่อยากให้ AI ค้นหาข้อมูล...',
            multiline=False,
            font_size=14,
            size_hint_x=0.75
        )
        self.research_btn = Button(
            text='🔍 สืบค้นข้อมูล',
            background_color=(0.2, 0.5, 0.8, 1),
            font_size=14,
            size_hint_x=0.25
        )
        self.research_btn.bind(on_press=self.run_ai_researcher)

        prompt_layout.add_widget(self.ai_prompt_input)
        prompt_layout.add_widget(self.research_btn)
        ai_layout.add_widget(prompt_layout)

        ai_tab.add_widget(ai_layout)
        tb_panel.add_widget(ai_tab)

        return tb_panel

    # ==========================================================
    # helper: อัปเดต UI จาก thread อื่นอย่างปลอดภัย
    # ==========================================================
    def _set_output(self, text):
        Clock.schedule_once(lambda dt: setattr(self.output_label, 'text', text))

    def _set_ai_text(self, text):
        Clock.schedule_once(lambda dt: setattr(self.ai_chat_label, 'text', text))

    def _set_btn_enabled(self, btn, enabled):
        def _apply(dt):
            btn.disabled = not enabled
        Clock.schedule_once(_apply)

    # ==========================================================
    # ฟังก์ชันฝั่ง IDE
    # ==========================================================
    def run_code(self, instance):
        if self._running_code:
            return
        code = self.code_input.text
        if not code.strip():
            self.output_label.text = "❌ ไม่มีโค้ดให้รัน"
            return

        self._running_code = True
        self._set_btn_enabled(self.run_btn, False)
        self.output_label.text = "⏳ กำลังรัน..."

        def worker():
            buf = io.StringIO()
            try:
                # ใช้ builtins module ตรง ๆ เพื่อความแน่นอน
                exec_globals = {'__builtins__': builtins}
                # redirect stdout เฉพาะ thread นี้
                with _redirect_stdout(buf):
                    exec(code, exec_globals)
                output = buf.getvalue()
                result = output if output else "✅ รันสำเร็จ (ไม่มี Output)"
            except SystemExit:
                result = "⚠️ โค้ดเรียก sys.exit() — หยุดการทำงาน"
            except BaseException:
                result = f"❌ เกิดข้อผิดพลาด:\n{traceback.format_exc()}"
            finally:
                self._running_code = False
                self._set_btn_enabled(self.run_btn, True)
                self._set_output(result)

        threading.Thread(target=worker, daemon=True).start()

    def clear_output(self, instance):
        self.output_label.text = "[ผลลัพธ์ถูกเคลียร์แล้ว]"

    def clear_code(self, instance):
        self.code_input.text = ""
        self.output_label.text = "🗑️ ช่องพิมพ์โค้ดว่างเปล่าแล้ว"

    # ==========================================================
    # ฟังก์ชันฝั่ง AI
    # ==========================================================
    def toggle_api_key_visibility(self, instance):
        self.api_key_input.password = not self.api_key_input.password
        self.toggle_key_btn.text = '🙈' if self.api_key_input.password else '👁️'

    def run_ai_researcher(self, instance):
        if not AI_AVAILABLE:
            self.ai_chat_label.text = (
                "❌ ไม่พบไลบรารี google-genai\n"
                "กรุณาติดตั้งด้วยคำสั่ง: pip install google-genai"
            )
            return

        if self._running_ai:
            return

        api_key = self.api_key_input.text.strip()
        topic = self.ai_prompt_input.text.strip()

        if not api_key:
            self.ai_chat_label.text = "⚠️ กรุณาใส่ Gemini API Key ที่ช่องด้านบนก่อนใช้งาน"
            return
        if not topic:
            self.ai_chat_label.text = "⚠️ กรุณาพิมพ์หัวข้อที่ต้องการค้นหาก่อน"
            return

        self._running_ai = True
        self._set_btn_enabled(self.research_btn, False)
        self.ai_chat_label.text = f"⏳ กำลังให้ AI ค้นหาและวิเคราะห์ข้อมูลเรื่อง: '{topic}'..."

        def worker():
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=(
                        "คุณคือ AI นักวิจัยผู้เชี่ยวชาญ ค้นหา วิเคราะห์ "
                        f"และสรุปข้อมูลเชิงลึกที่แม่นยำที่สุดเกี่ยวกับหัวข้อนี้: {topic}"
                    ),
                )
                text = f"📌 หัวข้อ: {topic}\n\n--------------------\n🤖 รายงานข้อมูลจาก AI:\n{response.text}"
                self._set_ai_text(text)
                Clock.schedule_once(lambda dt: setattr(self.ai_prompt_input, 'text', ''))
            except Exception as e:
                self._set_ai_text(f"❌ เกิดข้อผิดพลาดในการเชื่อมต่อ:\n{str(e)}")
            finally:
                self._running_ai = False
                self._set_btn_enabled(self.research_btn, True)

        threading.Thread(target=worker, daemon=True).start()

    # ==========================================================
    # Save popup
    # ==========================================================
    def show_save_popup(self, instance):
        # กัน popup ซ้อน
        if self.popup is not None and self.popup._window is not None:
            return

        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.filename_input = TextInput(
            text='my_script.py',
            multiline=False,
            size_hint_y=None,
            height=40,
            font_size=16
        )
        content.add_widget(Label(text="ตั้งชื่อไฟล์ (ต้องลงท้ายด้วย .py):", size_hint_y=None, height=30))
        content.add_widget(self.filename_input)

        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        save_confirm_btn = Button(text="บันทึก", background_color=(0.1, 0.6, 0.3, 1))
        cancel_btn = Button(text="ยกเลิก", background_color=(0.8, 0.2, 0.2, 1))

        btn_layout.add_widget(save_confirm_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)

        self.popup = Popup(title='บันทึกโค้ด', content=content, size_hint=(0.9, 0.4))
        save_confirm_btn.bind(on_press=self.save_file)
        cancel_btn.bind(on_press=self.popup.dismiss)
        self.popup.bind(on_dismiss=self._on_popup_dismiss)
        self.popup.open()

    def _on_popup_dismiss(self, *args):
        self.popup = None

    def save_file(self, instance):
        filename = self.filename_input.text.strip()
        if not filename:
            self.output_label.text = "❌ กรุณาตั้งชื่อไฟล์"
            return
        if not filename.endswith('.py'):
            filename += '.py'
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.code_input.text)
            self.output_label.text = f"💾 บันทึกไฟล์ '{filename}' สำเร็จ!"
            if self.popup:
                self.popup.dismiss()
        except Exception as e:
            self.output_label.text = f"❌ บันทึกไม่สำเร็จ: {str(e)}"
            if self.popup:
                self.popup.dismiss()


# ==========================================================
# context manager: redirect stdout แบบ thread-local
# ==========================================================
import contextlib

class _redirect_stdout:
    """
    ใช้ contextlib.redirect_stdout ภายใน แต่ sys.stdout เป็น global
    ถ้าหลาย thread รันพร้อมกันจะชนกัน — แต่ในแอปนี้เรารันทีละครั้ง
    (มี _running_code guard) จึงปลอดภัยพอ
    """
    def __init__(self, new_target):
        self._cm = contextlib.redirect_stdout(new_target)

    def __enter__(self):
        return self._cm.__enter__()

    def __exit__(self, *exc):
        return self._cm.__exit__(*exc)


if __name__ == '__main__':
    PythonMobileIDE().run()
