# vDate - Virtual Dating
>&copy;2015, Raghav Khandelwal, LIT2015002, [TeraFlik](http://www.teraflik.com)

##Installation
- You must have python installed and in your system path to run webserver.  
```
    pip install --upgrade pip  
    pip install django  
    python manage.py makemigrations vDate  
    python manage.py migrate vDate  
    python manage.py runserver  
```   
- Then open your browser and go to http://127.0.0.1:8000/  
- Make sure to add the address to list of proxy exceptions.

##Description
This is the PPL Assignment made by Raghav Khandelwal on Django. See the [Documentation](https://ppl-iiita.github.io/ppl-assignment-TeraFlik/).   
Django is a free and open-source web framework, written in Python, which follows the model-view-template architectural pattern.

1. Fully functional Web App, on sqlite3, a simple database management system.
2. Forms, if user wants to enter custom attributes of various models.
3. Random entries generator, to create multiple instances at the click of a single button.
4. All form requests through POST, ensuring security.
5. Easily extensible for future updates.

##Tools
1. [Sphinx v1.5.3](http://www.sphinx-doc.org/en/stable/) used for generating documentation.
2. [django](https://www.djangoproject.com/) framework to create the application.