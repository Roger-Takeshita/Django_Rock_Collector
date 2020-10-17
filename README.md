<h1 id='contents'>Table of Contents</h1>

- [DJANGO ROCK COLLECTOR](#django-rock-collector)
  - [Components of a Django Project](#components-of-a-django-project)
  - [Database](#database)
    - [Create a PostgreSQL Database](#create-a-postgresql-database)
  - [Start a New Project](#start-a-new-project)
    - [Folder and Files](#folder-and-files)
    - [Configure App](#configure-app)
      - [Connecting to PostgreSQL](#connecting-to-postgresql)
    - [Start Server](#start-server)
    - [Migrate](#migrate)
    - [Make Migrations](#make-migrations)
    - [Superuser](#superuser)
    - [URLs (Routes)](#urls-routes)
      - [One-time URL Setup](#one-time-url-setup)
      - [Defining Routes](#defining-routes)
    - [View Functions (Controllers)](#view-functions-controllers)
    - [Templates](#templates)
      - [Template Inheritance (Partials)](#template-inheritance-partials)
        - [BASE TEMPLATE](#base-template)
    - [Template Tags](#template-tags)
    - [Static Files](#static-files)
    - [Render Data in a Template](#render-data-in-a-template)

# DJANGO ROCK COLLECTOR

[Go Back to Contents](#contents)

## Components of a Django Project

[Go Back to Contents](#contents)

- Django is a much higher-level framework that provides lots of functionalities out of the box.

  - A powerful **Object-Relational-Mapper** (ORM) for working with relational database using Python
  - A built-in admin app for browsing and manipulating data in the database
  - Built-in user management and authentication

    ![](https://i.imgur.com/1fFg7lz.png)

## Database

[Go Back to Contents](#contents)

- By default, Django uses a lightweight database called **SQLite**. However, it's not supported by most hosting services (Heroku, etc.).
- To use PostgreSQL, we need to do a one-time install of the psycopg2 Python package:

  ```Bash
    pip3 install psycopg2-binary
  ```

  - **psycopg2** is a popular library that enables Python applications to interface with PostgreSQL.

- You can find more SQL commands [here](https://github.com/Roger-Takeshita/SQL)

### Create a PostgreSQL Database

[Go Back to Contents](#contents)

- On `Terminal`

  ```Bash
    psql
    CREATE DATABASE rock_collector;
    \l # to view all database
  ```

  ![](https://i.imgur.com/pzIoPbA.png)

## Start a New Project

[Go Back to Contents](#contents)

- To start a new project run the command in your project's folder

  ```Bash
    django-admin startproject rock_collector .
  ```

<!-- ~~~> Folder and Files -->

### Folder and Files

[Go Back to Contents](#contents)

- Create our app in a different folder.
- Using my custom [touch command](https://github.com/Roger-Takeshita/Shell-Script/blob/master/touch-open.sh)

  ```Bash
    touch main_app + urls.py + views.py + templates/about.html + base.html + rocks/index.html main_app/static/css/style.css
  ```

- Final structure

  ```Bash
    .
    ├── rock_collector
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── main_app
    ├── .gitignore
    ├── manage.py
    └── README.md
  ```

### Configure App

[Go Back to Contents](#contents)

- Add the **main_app** to the list of installed apps
- In `rock_collector/settings.py`

  ```Bash
    # Application definition

    INSTALLED_APPS = [
        'main_app',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]
  ```

#### Connecting to PostgreSQL

[Go Back to Contents](#contents)

- In `DATABASES`

- Change the default database (**sqlite3**) to **postgreSQL**

  ```Python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
  ```

  ```Python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'rock_collector',
        }
    }
  ```

### Start Server

[Go Back to Contents](#contents)

- To start the server run:

  ```Bash
      python3 manage.py runserver
  ```

  ![](https://i.imgur.com/NbIR02l.png)

  - Notice that we have a warning:
    > You have 17 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
    > Run 'python manage.py migrate' to apply them.

### Migrate

[Go Back to Contents](#contents)

- Migrations are Django’s way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema.

  ```Bash
    python3 manage.py migrate
  ```

  ![](https://i.imgur.com/cEPoF0r.png)

### Make Migrations

### Superuser

[Go Back to Contents](#contents)

- On `Terminal` create an admin user

  ```Bash
    python3 manage.py createsuperuser
  ```

  - after creating the superuser, you can login [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

### URLs (Routes)

#### One-time URL Setup

[Go Back to Contents](#contents)

- Django uses just the **URL** when defining a route, **ignoring the HTTP verb**.
- This means is that, for the **home page** functionality, we simply want to define a URL for the root route (**localhost:8000**).

- In `rock_collector/urls.py`

  - Routes are defined within URLconf modules named `urls.py`.
  - Import **include** from `django.urls`

  ```Python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('main_app.urls')),
    ]
  ```

  - **NOTE** that similar to how `Express` appends paths defined in a router module to the path in `app.use`, the paths defined in **main_app.urls** will be appended to the path specified in the `include` function.

#### Defining Routes

[Go Back to Contents](#contents)

- In `main_app/urls.py`

  - We define all the routes of our app
  - We've imported the **path** function that will be used to define each route.
  - We've also created at **urlpatterns** list that will hold each route we define for main_app.

  ```Python
    from django.urls import path
    from . import views

    urlpatterns = [
      path('', views.home, name='home'),
      path('about', views.about, name='about'),
    ]
  ```

  - a root path using an **empty string** and maps it to the **view.home** view function that does not exist yet - making the server unhappy.
  - The `name='home'` kwarg is optional but **will us referencing the URL** in other parts of the app, **especially from within templates**.

### View Functions (Controllers)

[Go Back to Contents](#contents)

- Views are equivalent to our **Controllers**
- In the `main_app/urls.py` for the home page we referenced a view function named **home**
- Let's create this function
- In `main_app/views.py`

  - Import the **render** method from `django.shortcuts`
  - Import the **HttpResponse** method from `django.http`
    - **HttpResponse** is the simplest way to send something back in response to a request. It's like `res.send()` was in Express.

  ```Python
    from django.shortcuts import render
    from django.http import HttpResponse

    def home(request):
        return HttpResponse('<h1>Hello World</h1>')

    def about(request):
        return HttpResponse('<h1>About Page</h1>')
  ```

  ![](https://i.imgur.com/6y42A5N.png)

### Templates

[Go Back to Contents](#contents)

- Django has two templating engines built-in:
  - Its own Django Template Language (DTL), and
  - [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/), a Python template engine, inspired by Django's.
- In `main_app/templates/about.html`

  - Let's create our about template

  ```HTML
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        <title>Rock Collector</title>
    </head>

    <body>
        <h1>About the Rock Collector</h1>
        <hr />
        <p>Hire a Rock Collector!</p>
        <footer>All Rights Reserved, &copy; 2020 Roger Takeshita</footer>
    </body>

    </html>
  ```

#### Template Inheritance (Partials)

[Go Back to Contents](#contents)

- Django has a [template inheritance](https://docs.djangoproject.com/en/3.1/ref/templates/language/#template-inheritance) feature built-in.
- Template inheritance is like using partials in EJS with Express, except they're more flexible.
  - You can declare that a template extends another template.
  - Extending another template results in defined blocks overriding (replacing) blocks defined in the template being extended.

##### BASE TEMPLATE

[Go Back to Contents](#contents)

- In `main_app/templates/base.html`

  ```HTML
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rock Collector</title>
    </head>

    <body>
        <header class="navbar-fixed">
            <nav>
                <div class="nav-wrapper">
                    <ul>
                        <li><a href="/" class="left brand-log">&nbsp;&nbsp;RockCollector</a></li>
                    </ul>
                    <ul class="right">
                        <li><a href="/about">About</a></li>
                        <li><a href="/rocks">Rocks</a></li>
                    </ul>
                </div>
            </nav>
        </header>
        <main class="container">
            {% block content %}
            {% endblock %}
        </main>
        <footer class="page-footer">
            <div class="right">All Rights Reserved, &copy; 2020 Roger Takeshita</div>
        </footer>
    </body>

    </html>
  ```

  - **Note** that we are using the **Materialize CSS Framework** for quick styling.

### Template Tags

[Go Back to Contents](#contents)

- [Template Tags](https://docs.djangoproject.com/en/3.1/ref/templates/builtins/#ref-templates-builtins-tags)
- In `main_app/templates/base.html`

  - We are using:

    ```HTML
      {% block content %}
      {% endblock %}
    ```

  - DTL template tags, `block` & `endblock`, enclosed within the template tag delimiters {% %}.
  - Django template tags control logic within a template. Depending upon the tag, they may, or may not, result in content being embedded in the page.

- In `main_app/views.py`

  - Update our about route to render the `about.html`

    ```Python
      from django.shortcuts import render
      from django.http import HttpResponse

      def home(request):
          return HttpResponse('<h1>Hello World</h1>')

      def about(request):
          return render(request, 'about.html')
    ```

- In `main_app/templates/about.html`

  - Update our html to use template tags

    ```HTML
      {% extends 'base.html' %}
      {% block content %}
      <h1>About the Rock Collector</h1>
      <hr />
      <p>Hire the Rock Collector!</p>
      {% endblock %}
    ```

### Static Files

[Go Back to Contents](#contents)

- Including static files in a template
- Django projects are pre-configured with a **django.contrib.staticfiles** app installed for the purpose of serving static files.
- To use the static folder, we need to tell Django to use the right path
- In `rock_collector/settings.py`

  - At the bottom, there is a `STATIC_URL = '/static/'` variable that declares what folder within the app to look for static files in.

- In `main_app/static/css/style.css`

  ```CSS
    body {
      display: flex;
      min-height: 100vh;
      flex-direction: column;
    }

    main {
      flex: 1 0 auto;
    }

    footer {
      padding-top: 0;
      text-align: right;
    }
  ```

- In `main_app/templates/base.html`

  - Add the `{% load static %}` DTL to import static files to our base template

  ```HTML
    {% load static %}

    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        <link rel="stylesheet" type="text/css" href="{% static 'css/style.css' %}">
        <title>Rock Collector</title>
    </head>

    ...
  ```

### Render Data in a Template

[Go Back to Contents](#contents)

- In `main_app/urls.py` (routes)

  - Update our routes to handle this new route

  ```Python
    from django.urls import path
    from . import views

    urlpatterns = [
      path('', views.home, name='home'),
      path('about', views.about, name='about'),
      path('rocks', views.rocks_index, name='index'),
    ]
  ```

- In `main_app/views.py` (controllers)

  - Create a new **Class** name **Rock** just to send some data to our `rocks_index`

  ```Python
    from django.shortcuts import render
    from django.http import HttpResponse

    class Rock:
        def __init__(self, name, type, description, age):
            self.name = name
            self.type = type
            self.description = description
            self.age = age

    rocks = [
        Rock('Rock 1', 'Rock 1 Name', 'Rock 1 Description', 3),
        Rock('Rock 2', 'Rock 2 Name', 'Rock 1 Description', 0),
        Rock('Rock 3', 'Rock 3 Name', 'Rock 1 Description', 4)
    ]

    def home(request):
        return HttpResponse('<h1>Hello World</h1>')

    def about(request):
        return render(request, 'about.html')

    def rocks_index(request):
        return render(request, 'rocks/index.html', { 'rocks': rocks })
  ```

- In `main_app/templates/rocks/index.html`

  ```HTML
    {% extends 'base.html' %}
    {% block content %}

    <h1>Rock List</h1>

    {% for rock in rocks %}
    <div class="card">
        <div class="card-content">
            <span class="card-title">{{ rock.name }}</span>
            <p>type: {{ rock.type }}</p>
            <p>Description: {{ rock.description }}</p>
            {% if rock.age > 0 %}
            <p>Age: {{ rock.age }}</p>
            {% else %}
            <p>Age: Rock</p>
            {% endif %}
        </div>
    </div>
    {% endfor %}

    {% endblock %}
  ```
