import warnings
import contextlib


class PrintMessageOnWarningOrExcept(contextlib.ContextDecorator):
    """Used to print the filename of any file that raises a warning or exception."""

    def __init__(self, msg):
        self.msg = msg
        print(f"Initializing with {msg}")
        super().__init__()

    def __enter__(self):
        # Use a custom warning catcher
        self.warnings = []
        print(f"Entering with {self.msg}")
        warnings.simplefilter("always")
        self.catcher = warnings.catch_warnings(record=True)
        self.log = self.catcher.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"Exiting with {self.msg}")
        self.catcher.__exit__(exc_type, exc_value, traceback)
        if self.log or exc_type is not None:
            print(self.msg)

        for w in self.log:
            breakpoint()
            warnings.showwarning(w.message, w.category, w.filename, w.lineno)

        if exc_type is not None:
            raise exc_value
