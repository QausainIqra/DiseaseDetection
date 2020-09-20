from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import OneLineAvatarListItem
from kivy.properties import StringProperty
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from tkinter import *
from kivy.properties import ObjectProperty
from kivymd.uix.floatlayout import FloatLayout
from functools import partial
from kivy.core.window import Window
import cv2
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
from kivy.uix.button import Button


Window.size = (360, 600)


screen_manager = '''
<LoadDialog>:
    BoxLayout:
        size: root.size
        pos: root.pos
        orientation: "vertical"
        FileChooserListView:
            id: filechooser
            path: '/'
        BoxLayout:
            size_hint_y: None
            height: 30
            Button:
                text: "Cancel"
                on_release: root.cancel()
            Button:
                text: "Load"
                on_press: root.load(filechooser.path, filechooser.selection)
<Item>
    ImageLeftWidget:
        source: root.source

              
ScreenManager:
    MenuScreen:
    LastScreen:
       
<MenuScreen>:
    name: 'menu'
    Screen:
    NavigationLayout:
        ScreenManager:
            Screen:
                BoxLayout:
                    orientation: 'vertical'
                    spacing: '4dp'
                    
                    MDToolbar:
                        title: 'Skin Disease Detection'
                        left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
                        right_action_items: [['camera', lambda x: app.camera_option()]]
                        elevation: 9
                    MDLabel:
                        text: 'Start recognizing your diseases here! Just take a picture of the affected area of your skin and click on the submit button to identify the disease.'
                        halign: 'center'
                        # bold: True
                       
                    MDRectangleFlatButton:
                        text: 'Gallery'
                        pos_hint:{'center_x':0.5, 'center_y':0.3}
                        on_release: root.show_load_list()
                        
                    MDLabel:
                        id: image_loaded_label
                        text: 'Your Image has been Loaded! Click on see Results'
                        bold: True
                        halign: 'center'
                        opacity: 0
                        disabled:True
                    
                    MDRectangleFlatButton:
                        id: result_btn
                        text: 'See Results'
                        pos_hint:{'center_x':0.5, 'center_y':0.3}
                        opacity: 0
                        disabled:True
                        on_release: root.manager.current = 'last'
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
                            text: 'help'
                            IconLeftWidget:
                                icon: 'help'
                                
<LastScreen>:
    name: 'last'
    BoxLayout:
        orientation: 'vertical'
        spacing: '0dp'
        
        MDToolbar:
            title: 'Skin Disease Detection'
            left_action_items: [['menu', lambda x: nav_drawer.toggle_nav_drawer()]]
            right_action_items: [['camera', lambda x: app.camera_option()]]
            elevation: 9
        MDLabel:
            id: disease_name
            halign: 'center'
            opacity: 0
            disabled: True
            bold: True
        MDLabel:
            id: disease_info
            halign: 'center'
            opacity: 0
            disabled: True
            
            
    
'''


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)




class MenuScreen(Screen):


    load = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def show_load_list(self):
        content = LoadDialog(load=self.load_list, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load a file list", content=content, size_hint=(1, 1))
        self._popup.open()

    def check(self,path):
        # prediction
        model = load_model('diseaseClassification1.h5')

        img_rows, img_cols = 224, 224

        class_labels = [
            'eczema',
            'normal',
            'psoriasis'
        ]
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = x.astype('float32') / 255
        pred = np.argmax(model.predict(x))

        if class_labels[pred] == 'psoriasis':
            global text
            text = "It's a psoriasis"
            # print('Its a psoriasis')

        else:
            if class_labels[pred] == 'eczema':
                text = "It's an eczema"
                # print('Its a eczema')
            else:
                text = "The skin is neither affected by eczema nor psoriasis"
                # print('The skin is neither affected by eczema nor psoriasis')

        print("It's a {}.".format(class_labels[pred]))

        self.ids.image_loaded_label.opacity= 1
        self.ids.image_loaded_label.disabled= False
        self.ids.result_btn.opacity = 1
        self.ids.result_btn.disabled = False
        print(self.ids.result_btn.text)
        LastScreen.set_text(LastScreen,text)


    def load_list(self, path, filename):
        text = filename[0]
        print(path)
        print(filename[0])
        self._popup.dismiss()
        self.check(text)

    def dismiss_popup(self):
        self._popup.dismiss()

    pass


class LastScreen(Screen):
    def set_text(self, lab):
        global result
        result = str(lab)
        print(result)
        global info
        if result == "It's a psoriasis":
            info = '  Here are the prcautionary measures: \n   1. Take dietary supplements \n   2. Avoid fragrances \n   3. Prevent dry skin \n   4. Eat healthfully \n   5. Soak your body \n   6. Get some rays \n   7. Reduce stress \n   8. Avoid alcohol \n   9. Try turmeric \n   10. Stop smoking'

        else:
            if result == "It's an eczema":
                info = "  Here are the precautionary measures: \n   1. Moisturize your skin at least twice a day \n   2. Apply an anti-itch cream to the affected area.\n   3. Take an oral allergy or anti-itch medication. \n   4. Don't scratch. \n   5. Apply bandages. \n   6. Take a warm bath. \n   7. Choose mild soaps without dyes or perfumes. \n   8. Use a humidifier. \n   9. Wear cool, smooth-textured clothing. \n   10. Treat stress and anxiety."

            else:
                info = 'No disease'
        print(info)

    def on_pre_enter(self, *args):
        self.ids.disease_name.text = result
        self.ids.disease_name.opacity = 1
        self.ids.disease_name.disabled= False
        self.ids.disease_info.text = info
        self.ids.disease_info.opacity = 1
        self.ids.disease_info.disabled = False



class Item(OneLineAvatarListItem):
    divider = None
    source = StringProperty()


sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(LastScreen(name='last'))



class skinDiseaseDetection(MDApp):
    dialog = None


    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = 'A700'

        screen = Builder.load_string(screen_manager)
        return screen



    def camera_option(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Select Image",
                type="simple",
                size_hint=(0.7, 1),
                items=[
                    Item(text="Take Picture", source="camera.jpg", on_release=self.open_camera),
                    Item(text="Cancel", source="cancel.jpg", on_release=self.close_dialogue),
                ],

            )

        self.dialog.open()

    def close_dialogue(self, obj):
        self.dialog.dismiss()


    def open_camera(self, obj):
        self.dialog.dismiss()

        cam = cv2.VideoCapture(0)

        cv2.namedWindow("test")

        img_counter = 0

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("test", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = "opencv_frame_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                print("{} written!".format(img_name))
                img_counter += 1

        cam.release()

        cv2.destroyAllWindows()



app = skinDiseaseDetection()
app.run()
