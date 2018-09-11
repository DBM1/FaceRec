from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.animation import Animation

Builder.load_string('''
<Node>:
    canvas:
        Color:
            rgba: 1, 1, 1, 0.3 * root.alpha
            # rgba: .1, .1, 0.8, 0.3 * root.alpha
        Line:
            circle: (root.x, root.y,self.size1 / 2 )
            width: self.size1 / 33
        Color:
            rgba: 1, 1, 1, 0.3 * root.alpha
            # rgba: .01, .01, 0.8, 0.5 * root.alpha
        Line:
            circle: (root.x, root.y ,self.size1 / 10)
            width: 20
            
<Line>:
    canvas:
        Color:
            rgba: .1, .1, 0.8, 0.3 
        Line:
            points:root.point
            width:3
''')


class Node(Widget):
    def __init__(self):
        self.alpha = 1
        self.size1 = 150
        self.x = 150
        self.y = 150
        anim = Animation(x=200, y=200, size1=100, t="in_out_back", duration=4) + Animation(x=150, y=250,
                                                                                           t="in_out_back",
                                                                                           size1=170,
                                                                                           duration=4) + Animation(
            x=150,
            y=150,
            t="in_out_back",
            size1=150,
            duration=4)
        anim.repeat = True
        anim.start(self)
        super(Node, self).__init__()


class Line(Widget):
    def __init__(self):
        self.point = [150, 150, 800, 800]
        anim = Animation(point = [200,200,800,800], t="in_out_back", duration=4) + Animation(point = [150,250,800,800],
                                                                                           t="in_out_back",
                                                                                           duration=4) + Animation(
            point = [150, 150, 800, 800],
            t="in_out_back",
            duration=4)
        anim.repeat = True
        anim.start(self)
        super(Line, self).__init__()


class LineExtendedApp(App):

    def build(self):
        root = GridLayout(cols=2, padding=50, spacing=50)
        node = Node()
        line = Line()
        root.add_widget(node)
        root.add_widget(line)
        return root


if __name__ == '__main__':
    LineExtendedApp().run()
