from gui.todo_app.views.todo_view import TodoView


class MainView:
    def __init__(self, controller):
        self.controller = controller
        self.todo_view = TodoView(controller)

    def show(self):
        pass
