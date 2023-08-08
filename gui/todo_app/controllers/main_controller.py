from gui.todo_app.views.main_view import MainView


class MainController:
    def __init__(self):
        self.view = MainView(self)

    def show(self):
        self.view.show()
