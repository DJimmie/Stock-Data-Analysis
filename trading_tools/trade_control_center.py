"""TRADE MONITORING & DECISION TOOL"""


from dependencies import *

# Create utility folder and logging file
ini_file,log_file=the_program_folder(os.path.basename(__file__))
logging.info('Start')

a=get_config_values(ini_file=ini_file,section='database server',option='sqlite_server')



class UserInterface():
    """Parent class for the UI. Instantiates the composite Window.
    User Interface with fields for entering data to the database."""

    logging.info('UserInterface()')

    def __init__(self):
        """Interface build."""
        UI(None,title='MY TRADING TOOL',
        banner='MY TRADING TOOL',
        win_color='#6334D0',
        fg='black',
        window_height=500)

       

        mainloop()

    


    


UserInterface()