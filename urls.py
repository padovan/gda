from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
from caco.sad import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Example:
                           # (r'^caco/', include('caco.foo.urls')),
                       
                       # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
                       # to INSTALLED_APPS to enable admin documentation:
                           # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
                       
                       # Uncomment the next line to enable the admin:
                       (r'^admin/(.*)', admin.site.root),

					   (r'^$', views.home),	   
					   (r'^auth/$', views.login_auth),	   
					   (r'^logout/$', views.logout),	   
                       (r'^[Ii][Cc]/$', views.show_all_semesters),
                       (r'^[Ii][Cc]/(?P<ano>\d+)[sS](?P<semestre>\d)/$', views.show_all_courses),
                       (r'^[Ii][Cc]/(?P<ano>\d+)[sS](?P<semestre>\d)/(?P<disciplina>[A-Z][A-Z]\d+)(?P<turma>[A-Z1-9#])/$', views.show_all_answers),
                       (r'^[Ii][Cc]/(?P<ano>\d+)[sS](?P<semestre>\d)/answer/$', views.all_to_answer),
                       (r'^[Ii][Cc]/(?P<ano>\d+)[sS](?P<semestre>\d)/(?P<disciplina>[A-Z][A-Z]\d+)(?P<turma>[A-Z1-9#])/answer/$', views.answer_course),
                       (r'^[Ii][Cc]/(?P<ano>\d+)[sS](?P<semestre>\d)/(?P<disciplina>[A-Z][A-Z]\d+)(?P<turma>[A-Z1-9#])/commit/$', views.commit_answer_course),
                       (r'^(?P<path>.*\.css)$', 'django.views.static.serve', {'document_root': 'templates/css/' }),
                       (r'^(?P<path>.*\.(jpg|png|gif))$', 'django.views.static.serve', {'document_root': 'templates/img/' }),
                       )

