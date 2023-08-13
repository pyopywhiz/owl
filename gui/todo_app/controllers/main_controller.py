from gui.todo_app.controllers.todo_controller import TodoController
from gui.todo_app.controllers.todo_table_controller import TodoTableController
from gui.todo_app.views.main_view import MainView
from gui.todo_app.views.todo_table_view import TodoTableView
from gui.todo_app.views.todo_view import TodoView


class MainController:
    def __init__(self):
        todo_view = TodoView()
        todo_table_view = TodoTableView()

        self.view = MainView()
        self.view.add_view(todo_view)
        self.view.add_view(todo_table_view)

        self.todo_controller = TodoController(todo_view, todo_table_view)
        self.todo_table_controller = TodoTableController(todo_table_view)

        todo_view.register_todo_controller(self.todo_controller)
        todo_table_view.register_todo_table_controller(self.todo_table_controller)

    def show(self):
        self.view.show()
        self.todo_table_controller.load_todos()
