#To front-end collaborators
##Adding html files
* Place the html file in directory ```/InfoRobot/templates```.
* Add a function in the routing rules file ```/InfoRobot/routes/views.py``` . Specify the html file name and the url to access it. 
Sample:
```
@app.route('/hello')
def index():
	return render_template('hello.html')
```
The file path of ```hello.html``` should be ```InfoRobot/templates/hello.html```
Now you can view the ```hello.html``` page by accessing http://127.0.0.1:5000/hello
* Note: the new function name depends on the page role. Another sample:
```
@app.route('/register')
def register_page():
	return render_template('register.html')
```

##Adding Static Files 
* Although html files are placed in ```InfoRobot/templates``` directory, you should place JS/CSS/images files in ```InfoRobot/static``` directory, because those files CANNOT be rendered as templates.
* By placing static files in the correct directory, you can access them by url ```http://127.0.0.1:5000/static/{{file_path}}```
Sample:
Route: ```http://127.0.0.1:5000/static/js/hello.js```
File Path: ```InfoRobot/static/js/hello.js```
