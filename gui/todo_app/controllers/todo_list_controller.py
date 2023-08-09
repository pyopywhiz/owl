from gui.todo_app.views.todo_list_view import TodoListView


class TodoListController:
    def __init__(self):
        self.todo_list_view = TodoListView(self)

    def on_data_changed(self) -> None:
        print("on data changed")
