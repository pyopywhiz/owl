from gui.todo_app.views.main_view import MainView


class MainController:
    def __init__(self):
        self.view = MainView()

    def show(self):
        self.view.show()
