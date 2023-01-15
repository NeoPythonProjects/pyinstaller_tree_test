from kivy.app import App
# from kivy.uix.image import Image
# from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.properties import StringProperty
import os, sys
# for pyinstaller
from kivy.resources import resource_add_path


class TestApp(App):
    def build(self):
        self.title = 'Testing folder levels for Kivy spec file'
        return Builder.load_file(self.resource_path('gui.kv'))

    # === Add to create executable with PyInstaller ======
    # we need a function to makes our script look in the correct folder for files
    # when pyinstaller has created the MEIPASS directory then we need to look there
    # this doesn't assume all our files (.py, .kv, .jpeg, .png, ... everything) are copied
    # into a new folder for pyinstaller to look in
    # in the .spec file we'll then need to to some extra work to make this work
    # if MEIPASS isn't there, then we want the relative path as per the code
    # we do this by creating the absolute path to the current directory, represented by a dot '.'
    # we then need to use this function everywhere we refer to a file, including file references
    # in the kv file. that's why i stuck that function in the App class, so I can refer to it
    # in kv file via app
    @staticmethod
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)


class MyScreenManager(ScreenManager):
    def __init(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def load_picture_screen(self, img_source: str):
        # pass img_source as kwarg
        self.switch_to(PictureScreen(img_source=img_source))
        # picture_screen = self.add_widget(PictureScreen(name='picture screen', img_source=img_source))
        # print(picture_screen) - None
        # self.current = picture_screen
        # print(self.current) - None


class WelcomeScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    text_file = StringProperty('')

    # use os.path.join
    path_str = TestApp.resource_path(os.path.join('level1', 'level2', 'sometext.txt'))
    with open(path_str, 'r') as f:
        text_file = f.read()


class PictureScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # img_source is passed through kwargs
    # but for kivy need to define it as a stringproperty
    # kv file can then use root.img_source to pull through
    # the value of img_source into kv file
    img_source = StringProperty('')

    def switch_back(self):
        app = App.get_running_app()
        sm = app.root.ids.sm
        # WelcomeScreen is a class
        # WelcomeScreen() is the instance of the class
        # WelcomeScreen is a screen widget
        sm.switch_to(WelcomeScreen())


class MyButton(Button):

    def action(self, img_path: str):
        # os.path.join() -> str
        app = App.get_running_app()
        sm = app.root.ids.sm
        sm.load_picture_screen(img_path)
        # sm.current = 'picture_screen'
        # print(sm.screens)
        # sm.screens.picture_screen.ids.img_screen.source = img_path





if __name__ == '__main__':
    # === Add to create executable with PyInstaller ======
    if hasattr(sys, '_MEIPASS'):
        resource_add_path((os.path.join(sys._MEIPASS)))
    # ==== end ===========================================
    TestApp().run()
