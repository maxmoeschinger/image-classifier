from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
import os

# Window.size = (300, 200)

labels_path = "/home/max/projects/momentech/potatosorter/raw_datasets/v2/labels.txt"
images_folder = "/home/max/projects/momentech/potatosorter/raw_datasets/v2/bad_1"

def get_label_file_name(image_file_path):
    return f"{image_file_path.replace('.jpg', '')}_class.txt"

with open(labels_path) as file:
    labels = [line.rstrip() for line in file]

image_files = sorted([os.path.join(images_folder, f) for f in os.listdir(images_folder) if
               os.path.isfile(os.path.join(images_folder, f)) and f.endswith('.jpg')])

image_and_label_files = []
for image_file in image_files:
    label_file = get_label_file_name(image_file)

    if os.path.isfile(label_file):
        image_and_label_files.append((image_file, label_file))
    else:
        image_and_label_files.append((image_file, None))


class MainWindow(BoxLayout):
    def __init__(self):
        super().__init__()
        self.hide_labeled = True
        self.files = image_and_label_files
        self.current_image_index = self.get_next_image_index(None)

        main_layout = GridLayout(cols=2)
        button_layout = GridLayout(cols=1, size_hint_x=None, width=100)

        for label in labels:
            button = Button(text=label)
            button.bind(on_press=lambda a, _label=label: self.handle_button_clicked(_label))
            button_layout.add_widget(button)

        main_layout.add_widget(button_layout)
        self.layout_image = Image(source=self.files[self.current_image_index][0])
        main_layout.add_widget(self.layout_image)

        self.add_widget(main_layout)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.index_history = []

    def get_next_image_index(self, current_index):
        new_index = current_index + 1 if current_index is not None else 0
        if new_index >= len(self.files):
            return None

        if self.hide_labeled:
            if self.files[new_index][1] is None:
                return new_index
            else:
                return self.get_next_image_index(new_index)
        else:
            return new_index

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1].isdigit():
            input_number = int(keycode[1])

            if 0 < input_number <= len(labels):
                self.handle_button_clicked(labels[input_number - 1])

        if keycode[1] == 'd':
            os.remove(self.files[self.current_image_index][0])
            label_file = get_label_file_name(self.files[self.current_image_index][0])
            if os.path.isfile(label_file):
                os.remove(label_file)

            self.files.pop(self.current_image_index)

            self.set_new_current_index(self.get_next_image_index(self.current_image_index - 1))
            self.update_image()

        if keycode[1] == 'p' and len(self.index_history) > 0:
            self.set_new_current_index(self.index_history.pop(), False)
            self.update_image()

        return True

    def handle_button_clicked(self, label):
        label_file = get_label_file_name(self.files[self.current_image_index][0])
        with open(label_file, 'w') as file:
            file.write(label + '\n')

        self.set_new_current_index(self.get_next_image_index(self.current_image_index))
        self.update_image()

    def set_new_current_index(self, new_index, add_to_history=True):
        if add_to_history:
            self.index_history.append(self.current_image_index)
        self.current_image_index = new_index
        self.update_image()

    def update_image(self):
        self.layout_image.source = self.files[self.current_image_index][0]


class MyApp(App):
    def build(self):
        self.title = "Classifier!"
        return MainWindow()


app = MyApp()
app.run()
