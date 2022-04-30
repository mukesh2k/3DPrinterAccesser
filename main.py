from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stencilview import StencilView
from kivy.graphics import Color, Ellipse, Line, Rectangle
import test


class Float_layout(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.painter = MyPaintWidget(size_hint=(
            0.7, 0.5), pos_hint={"x": 0, "y": 0.5})
        with self.painter.canvas:
            Color(0, 0, 0)
            Rectangle(pos=self.painter.pos, size=self.painter.size)
        self.infotext = "hey"
        self.ssbtn = Button(text='Save', size_hint=(
            0.1, 0.05), pos_hint={"x": 0, "y": 0.1})
        self.clearbtn = Button(text='Clear', size_hint=(
            0.2, 0.05), pos_hint={"x": 0.1, "y": 0.1})
        # self.la = Label(text=self.infotext, font_size='20sp',
        #                 color=[0.41, 0.42, 0.74, 1], ids="fun")
        self.ssbtn.bind(on_release=self.save_screenshot)
        self.clearbtn.bind(on_release=self.clear_screen)
        # self.add_widget(self.la)
        self.add_widget(self.painter)
        self.add_widget(self.ssbtn)
        self.add_widget(self.clearbtn)

    def save_screenshot(self, obj):
        self.painter.export_to_png("screenshot.png")
        test.run()

    def clear_screen(self, obj):
        self.painter.canvas.clear()
        self.infotext += "hey"
        self.ids.fun.text = self.infotext


class MyPaintWidget(StencilView):
   # StencilView.canvas(Color((1, 0.5, 0.5)))
    with StencilView().canvas.after:
        Color(0, 0, 1)
        #Rectangle(pos=self.painter.pos, size=self.painter.size)

    def on_touch_down(self, touch):
        color = (1, 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 5
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=(d))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):
    def build(self):
        self.root = root = Float_layout()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
           # Color(0, 1, 0, 1)  # green; colors range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


MyPaintApp().run()
