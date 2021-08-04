# This is the code for the Zendesk Ticket Viewer

# Import packages
import requests 

# Read in credentials from separate file
keyFile = open("keyFile.txt")
lines = keyFile.readlines()
username = lines[0].rstrip()
password = lines[1].rstrip()

# Define global variables
url = "https://zccoevcoding.zendesk.com/api/v2/tickets.json"
credentials = username, password
session =  requests.Session()
session.auth = credentials
TOTAL_PAGE = 25
MAX_PAGE = 25
MAX_LINE = 40


# Startup welcome message   
print("\nWELCOME TO THE ZENDESK TICKET VIEWER!\n")
print("CHOOSE ONE OF THE FOLLOWING OPTIONS\n")
print("Type 'tickets' and press enter tot view all tickets")
print("Type 'select' and press enter to select a specific ticket")
print("Type 'exit' and press enter to quit the viewer\n")


# Check formatting of input
def check_input(user_input):
    try:
        user_choice = input(user_input)
    except NameError:
        print("\nThat doesn't appear to be correctly formatted")
        user_choice = check_input(user_input)
    
    return str(user_choice)

# Check connection
def check_status(response):
    if response.status_code != requests.codes.ok:
        try:
            response.json()["error"]
            error = response.json()["error"]
        except KeyError:
            error = "Connection failed"       
        
        print("\nThe following error occurred:")
        print("\n\t - "+error+" -\n")
        print("Contact your administrator or try again")
        print_options()

        return False
    return True

# Exit the viewer
def system_exit():
    print("\nThanks for using Zendesk ticket viewer!\n")
    raise SystemExit

# Print out selected ticket details
def print_ticket(ticket):

    formats = [('\nCREATED:', "created_at"), ("SUBJECT:","subject"),
               ("\nDESCRIPTION:", "description"), ("\nTICKET ID:", "brand_id"),
               ("REQUESTED BY:", "requester_id"),
               ("ASSIGNED TO:", "assignee_id"),("OPEN/CLOSED:", "status")]
    
    
    try:
        print('-'*10,"Ticket number:",ticket["id"],'-'*10)
    except KeyError:
        print('-'*10,"Ticket number: unavailable",'-'*10)
        
    for pair in formats:
        print(pair[0], end = ' ')
        try:
    # Formatting so that lines don't go off page
            if len(str(ticket[pair[1]])) > MAX_LINE - len(pair[0]):
                start = 0
                end = MAX_LINE - len(pair[0])
                while end < len(ticket[pair[1]]):
                    print(ticket[pair[1]][start:end])
                    start = end
                    end+=MAX_LINE
            else:
                print(ticket[pair[1]])
        except KeyError:
            print("unavailable")
    
    return
    
# Print all tickets contained in page
def print_tickets(page, count, total):
    
    start = total*TOTAL_PAGE - 24

    print("\t"+"-"*8 + "Total entries: "+str(count) + "-"*8 +"\t")
    if count == 0:
        print("\nNo tickets to tickets to display.")
        return

    print("Displaying "+ str(start)+" to " + str(start +len(page) - 1))
    print("Ticket no. | \t\t\tTicket details")
    for entry in page:
        print(5*' '+ str(start) + (6-len(str(start)))*' '+"|",end = " ")
        print("'"+entry["subject"] + "'  SUBMITTED BY", end = "  '")
        print(str(entry["submitter_id"]) + "' ON", end = "  '")
        print(entry["created_at"], end = "'\n")
        start+=1
    return

# Print all command options
def print_options():
    print("\nType one of the following then press enter:")
    print("\t'tickets' - View all available tickets")
    print("\t'select' - View a specific ticket")
    print("\t'exit' - Quit the viewer")
    return

# GET all tickets
def all_tickets():
    params = {"per_page":TOTAL_PAGE, "page": 1}
    while True:

        # Get page
        response = session.get(url = url)
        if check_status(response):
            data = response.json()
        else:
            break
        
        try:
            page = data["tickets"]
        except KeyError:
            print("No tickets appear to have been returned,", end=' ')
            print("maybe try again later, good bye.")
        
        next_page = data["next_page"]
        prev_page = data["previous_page"]

        # Show options
        print_tickets(page, data["count"], params["page"])
        print("\nYou may type the following and press enter to continue:")
        print("\t'tickets' - View all available tickets")
        print("\t'next' or 'last' to and press enter to navigate pages")
        print("\t'select' - View a specific ticket")
        print("\t'exit' - Quit the viewer.")

        user_choice = check_input("\nCHOOSE YOUR OPTION: ")

        if user_choice == "exit":
            system_exit()
            break
        
        elif user_choice == "next":
            if next_page == None:
                print("\nThere is no next page, try another option")
                print("Here's that page again in case you need it\n")
            else:
                print()
                params["page"]+=1
                
        elif user_choice == "previous":
            if prev_page == None:
                print("\nThere is no previous page, try another option")
                print("Here's that page again in case you need it\n")
            else:
                params["page"]-=1
                
        elif user_choice == "select":
            get_ticket()
            break

        else:
            print("That wasn't one of my suggestions, try again :)")
            print("Here's that page again in case you need it\n")
              
    return

# Function when choosing a specific ticket
def get_ticket():
    ticket = int(check_input("\nPlease type the ticket number and press enter: "))
    params = {"per_page": MAX_PAGE, "page": ticket//MAX_PAGE + 1}
    
    print ("Retrieving ticket number "+str(ticket)+" one moment please.\n")

    # Get page containing ticket, check for errors         
    response = requests.get(url = url, params = params, auth = credentials)
    if check_status(response):
        data = response.json()
    else:
        return
    
    try:
        page = data["tickets"]
    except KeyError:
        print("No tickets appear to have been returned,", end=' ')
        print("maybe try again later, good bye.")

    try:
        retrieved = page[ticket%MAX_PAGE - 1]
    except IndexError:
        print("\nThat ticket doesn't appear to be available.")
        print("I'm now returning to the options menu")
        print_options()
        return

    # Print ticket content
    print_ticket(retrieved)

    # Options refresher
    while True:
        print("\nYou may type the following and press enter to continue:\n")
        print("\t'tickets' - View all available tickets")
        print("\t'select' - View a specific ticket")
        print("\t'exit' - Quit the viewer")

        user_choice = check_input("\nSelection: ")

        if user_choice == "exit":
            system_exit()
            return

        elif option == "tickets":
            all_tickets()

        elif option == "select":
            get_ticket()

        else:
            print("That wasn't one of my suggestions, try again :)")
        
    return

#body and decision maker, uses linguistic input to determine what the user
#is requesting 
while True:
    option = check_input("\nSelection: ")
    
    if len(option.split() )> 1:
        print("I'm sorry I can't understand sentences with more than one")
        print("word, please try again")
        
    elif option == "exit":
        system_exit()
        break
    
    elif option == "options":
        print_options()

    elif option == "tickets":
        all_tickets()

    elif option == "select":
        get_ticket()
        
    else:
        print("That wasn't one of my suggestions, here they are again")
        print_options()

