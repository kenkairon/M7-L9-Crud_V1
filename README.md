# M7-L9-Crud_V1
Educativo y de Aprendizaje Personal
---
## Tabla de Contenidos
- [Tecnologías](#Tecnologías)
- [Configuración Inicial](#configuración-Inicial)
- [Creación del Modelo](#creación-del-modelo)
---
# Tecnologías
- Django: Framework web en Python.
- SQLite:
--- 
# Configuración Inicial 
1. Entorno virtual 
    ```bash 
    python -m venv venv

2. Activar el entorno virtual
    ```bash 
    venv\Scripts\activate

3. Instalar Django
    ```bash 
    pip install django 
        
4. Actualizamos el pip 
    ```bash
    python.exe -m pip install --upgrade pip

5. Crear el proyecto de django  linkdump
    ```bash 
    django-admin startproject linkdump

6. Guardamos dependencias
    ```bash
    pip freeze > requirements.txt

7. Ingresamos al linkdump
    ```bash 
    cd linkdump

9. Creamos la aplicacion llamada app
    ```bash     
    python manage.py startapp app


10. Configuración de /settings.py 
    ```bash 
        INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'app',
    ]

# Creación del Modelo 

11. app/models.py
    ```bash
    from django.db import models

    class Link(models.Model):
        url = models.URLField(max_length=200)
        description = models.TextField()

        def __str__(self):
            return self.url

12. Creamos el .form en app
    ```bash
    from django import forms
    from .models import Link

    class LinkForm(forms.ModelForm):
        class Meta:
            model = Link
            fields = ['url', 'description']

13. Creamos las migraciones
    ```bash
    python manage.py migrate
    python manage.py makemigrations
    python manage.py migrate

14. en app/views.py creamos las vistas
    ```bash
    from django.shortcuts import render, get_object_or_404, redirect
    from .models import Link
    from .forms import LinkForm

    def link_list(request):
        links = Link.objects.all()
        return render(request, 'app/link_list.html', {'links': links})

    def link_create(request):
        if request.method == "POST":
            form = LinkForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('link_list')
        else:
            form = LinkForm()
        return render(request, 'app/link_form.html', {'form': form})

    def link_update(request, pk):
        link = get_object_or_404(Link, pk=pk)
        if request.method == "POST":
            form = LinkForm(request.POST, instance=link)
            if form.is_valid():
                form.save()
                return redirect('link_list')
        else:
            form = LinkForm(instance=link)
        return render(request, 'app/link_form.html', {'form': form})

    def link_delete(request, pk):
        link = get_object_or_404(Link, pk=pk)
        if request.method == "POST":
            link.delete()
            return redirect('link_list')
        return render(request, 'app/link_confirm_delete.html', {'link': link})
        
15. Creamos los templates/app/link_list.html
    ```bash
    <h2>Links</h2>
    <a href="{% url 'link_create' %}">Add New Link</a>
    <ul>
        {% for link in links %}
        <li>
            <a href="{{ link.url }}" target="_blank">{{ link.url }}</a> - {{ link.description }}
            <a href="{% url 'link_update' link.pk %}">Edit</a>
            <a href="{% url 'link_delete' link.pk %}">Delete</a>
        </li>
        {% endfor %}
    </ul>
16. Creamos los templates/app/link_form.html
    ```bash
    <h2>{% if form.instance.pk %}Edit{% else %}New{% endif %} Link</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
    <a href="{% url 'link_list' %}">Cancel</a>

17. Genero los templates/app/link_confirm_delete.html
    ```bash
    <h2>Delete Link</h2>
    <p>Are you sure you want to delete "{{ link.url }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Confirm</button>
    </form>
    <a href="{% url 'link_list' %}">Cancel</a>

18. Creamos los urls en app/urls.py
    ```bash
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.link_list, name='link_list'),
        path('link/new/', views.link_create, name='link_create'),
        path('link/<int:pk>/edit/', views.link_update, name='link_update'),
        path('link/<int:pk>/delete/', views.link_delete, name='link_delete'),
    ]

19. Agregamos la urls en linkdunp/urls.py
    ```bash
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('app.urls')),
    ]
20. Se corre el servidor y se revisa las urls http://127.0.0.1:8000/
    ```bash
    python manage.py runserver