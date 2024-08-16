from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window

Window.size = (300, 200)

labels_path = "./labels.txt"

with open(labels_path) as file:
    labels = [line.rstrip() for line in file]

class MainWindow(BoxLayout):
    def __init__(self):
        super().__init__()

        main_layout = GridLayout(cols=2)
        button_layout = GridLayout(cols=1, size_hint_x=None, width=100)
        for label in labels:
            button_layout.add_widget(Button(text=label))
        main_layout.add_widget(button_layout)
        wimg = Image(source='test.jpg')
        main_layout.add_widget(wimg)

        self.add_widget(main_layout)

    def handle_button_clicked(self, event):
        self.button.text = "Hello, World!"


class MyApp(App):
    def build(self):
        self.title = "Hello, World!"
        return MainWindow()



app = MyApp()
app.run()