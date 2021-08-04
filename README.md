# Welcome to my Zendesk Ticket Viewer!

This CLI based application written in Python connects to the Zendesk API and allows the user to view support tickets in their account.

# Getting Started

To run this program, Python and pip is required to run Python3 and install the "requirements.txt" document tnecessary to run the viewer. <br>
For Mac, the following command can be run in the terminal to get pip: curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py. <br>

For Windows, download get-pip.py to a folder on your computer. Open a command prompt and navigate to the folder containing the get-pip.py installer. Run the following command: python get-pip.py <br>

Once pip is installed, run the command "pip install -r requirements.txt" in a command window/ terminal <br>

# Running the application
This version of the application pulls credentials from an external file called keyFile.txt An example file has been added to this repository.
The first line of the text file should be your username/email whereas the second line should be your password
Type python3 ticket_viewer.py to run the application in the CLI. This brings up the welcome message that presents 3 user input options the user can type in. <br>
'tickets' - option to view all available tickets <br>
'select' - option to select a specific ticket <br>
'exit' - option to exit the application <br>
If the user chooses 'tickets' there are additional options that can be typed in to navigate pages: 'next' and 'last'. <br>
If the user chooses 'select', the information for the ticket will appear and the user will return to the options available. <br>
If the user chooses 'exit' then the user exits the application. <br>
Thanks for using the Zendesk ticket viewer!


