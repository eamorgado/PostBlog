# PostBlog
A post blog using python and flask.
This was made for learning purposes only. To introduce the basic concepts and procedures to develop a python-flask website.

With this website you will be able to create and delete posts as well as accounts. The DBMS is sqllite, I will try to change that and use MySQL.

Note that to execute this you must have python installed and flask (as well as all the flask extensions that are imported in the files), after you meet all the requirements you will also need to set environment variables before execution, those are FLASK_APP, FLASK_DEBUG, EMAIL_USER, EMAIL_PASS, SECRET_KEY and SQLALCHEMY_DATABASE_URI.

Using powershell you can simply do:
    $env:FLASK_APP = "run.py"
    
    $env:FLASK_DEBUG = 1 [that is if you want to run it in debug mode]
    
    $env:EMAIL_USER = "example_email@gmail.com" [it can be whatever email you want, it's to send messages to the users]
    
    $env:EMAIL_PASS = "example_email_pass" [the password for the email you chose]
    
    $env:SECRET_KEY = "91ac98766d37ae4df360c0961c6b157a" [it's a random key]
    
    $env:SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
  
  
After you have all this, simply run <b>flask run</b> and you can test the site in localhost
