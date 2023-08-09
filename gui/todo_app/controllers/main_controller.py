from gui.todo_app.controllers.todo_controller import TodoController
from gui.todo_app.controllers.todo_list_controller import TodoListController
from gui.todo_app.views.main_view import MainView


class MainController:
    def __init__(self):
        self.todo_controller = TodoController()
        self.todo_list_controller = TodoListController()
        self.view = MainView(self)

    def show(self):
        self.view.show()
