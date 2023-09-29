from flask import Flask

# we need to import the file that contains the status codes
from src import status

app = Flask(__name__)

COUNTERS = {}

# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".


@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS
    # line added from example
    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT
    COUNTERS[name] = 0
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


# create a route for method PUT

@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    # increment the counter by 1
    COUNTERS[name] = COUNTERS[name] + 1
    # return the new counter and a 200_ok return code
    return {name: COUNTERS[name]}, status.HTTP_200_OK


# create a route for method GET

@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    # check to see if the name does not exist and return 404 if not
    if name not in COUNTERS:
        return {"Message": f"Counter {name} does not exists"}, status.HTTP_404_NOT_FOUND
    # if the name is in the counters list then return a status code okay
    return {name: COUNTERS[name]}, status.HTTP_200_OK


# create a route for method delete similar to assignment before
@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    # check if name exist within the list of counters
    if name not in COUNTERS:
        # if name does not exist return 404
        return {"Message": f"Counter {name} does not exists"}, status.HTTP_404_NOT_FOUND
    # if it does, we need to delete it before returning a 204 status
    del COUNTERS[name]
    # now return success code
    return {name: COUNTERS[name]}, status.HTTP_204_NO_CONTENT
