# labton
A package for labeling sentances and words made in flask.
Clean minimal tekst-annotation - with buildt in control of Inter-Annotator Agreement.

To test if the package is useable to Your annotation project simply:

pip install labton


and the run the following in a python shell:
from labton.annotation_app import App

app = App()

app.run()

or simply run the following from a terminal:

python -m labton