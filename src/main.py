import enaml
from enamlnative.android.app import AndroidApplication


app = AndroidApplication()

with enaml.imports():
    from view import ContentView
    app.content_view = ContentView()

app.start()
