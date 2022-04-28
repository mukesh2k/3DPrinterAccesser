from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.stencilview import StencilView
from kivy.graphics import Color, Ellipse, Line, Rectangle


class MyPaintWidget(StencilView):

    def on_touch_down(self, touch):
        color = (1, 1, 1)
        with self.canvas:
            Color(*color, mode='hsv')
            d = 10
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=(d))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):
    def build(self):
        parent = Widget()
        self.painter = MyPaintWidget(size=[i/2.0 for i in Window.size])
        with self.painter.canvas:
            Color(1, 0, 0, 0.3)
            Rectangle(pos=self.painter.pos, size=self.painter.size)
        ssbtn = Button(text='Save')
        ssbtn.bind(on_release=self.save_screenshot)
        parent.add_widget(self.painter)
        parent.add_widget(ssbtn)
        return parent

    def save_screenshot(self, obj):
        self.painter.export_to_png("screenshot.png")


MyPaintApp().run()
