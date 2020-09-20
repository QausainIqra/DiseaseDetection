from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.core.window import Window
Window.size = (360, 600)
result_screen = '''
Screen:
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    padding: '100'
                    spacing: '100'
                    MDToolbar:
                        title: 'Skin Disease Detection'
                        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                        right_action_items: [['camera', lambda x: app.camera_option()]]
                        elevation: 9
                    MDLabel:
                        text: app.pass_result()
                        halign: 'center'
                        bold: True 
                    MDLabel:
                        text: app.info_disease()
                        halign: 'center'
                    MDRectangleFlatButton:
                        text: 'View Recomendations'
                        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
                    Widget:

        MDNavigationDrawer:
            id: nav_drawer
            BoxLayout:
                orientation: 'vertical'
                spacing: '8dp'
                padding: '8dp'
                ScrollView:
                    MDList:
                        OneLineAvatarListItem:
                            text: 'About Us'
                            ImageLeftWidget:
                                source: 'about.jpg'
                        OneLineIconListItem:
                            on_release: app.camera_option()
                            text: 'Upload an Image'
                            IconLeftWidget:
                                icon: 'file-upload'
                        OneLineIconListItem:
                            on_release: app.login()
                            text: 'Login'
                            IconLeftWidget:
                                icon: 'profile'
                        OneLineIconListItem:
                            text: 'help'
                            IconLeftWidget:
                                icon: 'help'


'''


class ResultScreen(MDApp):
    # global result
    # result = 'hi'
    def build(self):
        screen = Builder.load_string(result_screen)
        return screen

    def display_result(self, text):

        global result
        result = str(text)
        print('display result ' + result)
        print('display ' + str(text))

    def pass_result(self):
        print('pass' + result)
        return result

    def info_disease(self):
        if result == "It's a psoriasis":
            info = '  Here are the prcautionary measures: \n   1. Take dietary supplements \n   2. Avoid fragrances \n   3. Prevent dry skin \n   4. Eat healthfully \n   5. Soak your body \n   6. Get some rays \n   7. Reduce stress \n   8. Avoid alcohol \n   9. Try turmeric \n   10. Stop smoking'
            return info
        else:
            if result == "It's an eczema":
                info = "  Here are the precautionary measures: \n   1. Moisturize your skin at least twice a day \n   2. Apply an anti-itch cream to the affected area.\n   3. Take an oral allergy or anti-itch medication. \n   4. Don't scratch. \n   5. Apply bandages. \n   6. Take a warm bath. \n   7. Choose mild soaps without dyes or perfumes. \n   8. Use a humidifier. \n   9. Wear cool, smooth-textured clothing. \n   10. Treat stress and anxiety."
                return info
            else:
                info = 'No disease'
                return info

    def view_recomendations(self):
        return

# ResultScreen().run()