import os
import flask
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import arrow
import acp_times
#import config
import logging
#from flask_restful import Resource, Api

# http://127.0.0.1:5000
# Run using...
# docker-compose build
# docker-compose up

app = Flask(__name__)

client = MongoClient('db', 27017)
db = client.tododb # gets database

db.tododb.delete_many({})

@app.route("/")
@app.route("/index")
def index():
    #app.logger.debug("Main page entry")
    return flask.render_template('calc.html') # renders main page


@app.errorhandler(404) # error handler
def page_not_found(error):
    app.logger.debug("Page not found")
    #flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    #app.logger.debug("Got a JSON request")
    
    # gets all arguments needed to calculating opening and closing times
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brev_dis', 999, type=int)
    start_time = request.args.get('start_t', 999, type=str)
    start_date = request.args.get('start_d', 999, type=str)
    
    # debug statements
    #app.logger.debug("start time={}".format(start_time))
    #app.logger.debug("start date={}".format(start_date))
    #app.logger.debug("km={}".format(km))
    #app.logger.debug("request.args: {}".format(request.args))
    
    # reformats times to correct iso string format
    time_str = "{}T{}".format(start_date, start_time)
    time = arrow.get(time_str)
    time = time.isoformat() 
    
    # calculates new opening and closing times for control
    opening = acp_times.open_time(km, brevet_dist, time)
    closing = acp_times.close_time(km, brevet_dist, time)

    result = {"open": opening, "close": closing}

    return flask.jsonify(result=result) # sends back result!


@app.route('/display', methods=['POST'])
def display():
    _items = db.tododb.find() # finds specified data base collection?
    items = [item for item in _items] 	
    # contents of text box are kept track of in items (saved)
    # and then displayed below

    return render_template('times.html',items=items) # updates displayed items
    # todo.html has two blank text boxes and a submit button
    # entering text in the left box and hitting submit will
    # display it below in large bold while data entered in
    # right box displays it below in smaller unbolded letters
    # left box contents are displayed before right box contents

@app.route('/empty')
def empty():
	return render_template('empty.html')

@app.route('/new', methods=['POST'])
def new():
    open_data = request.form.getlist("open")
    close_data = request.form.getlist("close")

    open_list = []
    close_list = []

    for item in open_data:
	    if str(item) != '':
		    open_list.append(str(item))
	
    for item in close_data:
        if str(item) != '':
            close_list.append(str(item))
		
    #app.logger.debug("OPEN " + str(open_list))
    #app.logger.debug("CLOSE " + str(close_list))

    for x in range(len(open_list)):	    
        item_doc = {
             'open_times': open_list[x],
		     'close_times': close_list[x]
        }
        db.tododb.insert_one(item_doc)

    _items = db.tododb.find() # finds specified data base collection
    items = [item for item in _items]
    app.logger.debug("Contents of db: " + str(items))

    if items == []:
	    return redirect(url_for('empty'))
    else:
        return redirect(url_for('index')) # calls todo method again

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)