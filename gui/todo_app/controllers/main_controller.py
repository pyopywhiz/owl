from gui.todo_app.controllers.todo_controller import TodoController
from gui.todo_app.controllers.todo_list_controller import TodoListController
from gui.todo_app.views.main_view import MainView
from gui.todo_app.views.todo_list_view import TodoListView
from gui.todo_app.views.todo_view import TodoView


class MainController:
    def __init__(self):
        todo_view = TodoView()
        todo_list_view = TodoListView()

        self.view = MainView()
        self.view.add_view(todo_view)
        self.view.add_view(todo_list_view)

        self.todo_controller = TodoController(todo_view, todo_list_view)
        self.todo_list_controller = TodoListController(todo_list_view)

        todo_view.register_controller(self.todo_controller)
        todo_list_view.register_controller(self.todo_list_controller)

    def show(self):
        self.view.show()
        self.todo_list_controller.load_todos()
