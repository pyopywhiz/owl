from gui.todo_app.views.todo_form import TodoForm
from gui.todo_app.views.todo_list_view import TodoListView


class TodoView:
    def __init__(self, controller):
        self.controller = controller
        self.form = TodoForm(controller)
        self.list_view = TodoListView(controller)

    def show(self):
        pass
