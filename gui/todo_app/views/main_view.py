from gui.todo_app.views.todo_list_view import TodoListView
from gui.todo_app.views.todo_view import TodoView


class MainView:
    def __init__(self, controllers ):
        self.setWindowTitle("Todo List App")
        self.resize(600, 600)

        qr_value = self.frameGeometry()
        cp_value = QDesktopWidget().availableGeometry().center()
        qr_value.moveCenter(cp_value)
        self.move(qr_value.topLeft())

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout: Any = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.todo_view = TodoView()
        self.todo_list_view = TodoListView()

    def show(self):
        self.todo_view.show()
