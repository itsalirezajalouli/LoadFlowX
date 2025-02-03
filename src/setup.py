from cx_Freeze import setup, Executable

setup(
    name='PSALoadFlowGUI',
    version='1.0',
    description='PSA Load Flow Simulation GUI',
    executables=[Executable('main.py')]
)

