import solara
from tax import Income


income = Income()

@solara.component
def Page():
    income.consol()

# The following line is required only when running the code in a Jupyter notebook:
Page()
