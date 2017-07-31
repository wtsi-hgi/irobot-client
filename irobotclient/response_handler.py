from irobotclient.request_handler import Requester

# iRobot response status codes.
DATA_RETURNED = 200
FETCHING_DATA = 202
DATA_MATCHED_CLIENT = 304

def process_response(request_handler: Requester):
    print("Process the responses.")

    # TODO - process the responses and output the status and progress to the standard out
    # Handle the different responses
        # Handle the wait response by calling the handle request method again?
        # Handle failed authorisation by checking the headers in the response.
    # If the HEAD request comes back good, then set it to a GET request
    # Output the various stages to standard out such as:
        # fetching and the delay amount
        # printing when the 200 has been successful and the status of the download?
