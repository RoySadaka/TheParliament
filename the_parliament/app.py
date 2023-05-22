from the_parliament.metadata import Metadata

class App:
    metadata: Metadata = None

global app
app = App()
app.metadata = Metadata()