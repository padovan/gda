from django.conf.urls.defaults import *
from caco.sad.views import *
from settings import TEMPLATE_DIRS

urlpatterns = patterns('',
    # Example:
    # (r'^caco/', include('caco.foo.urls')),

    # Uncomment this for admin:
     (r'^admin/', include('django.contrib.admin.urls')),
     (r'^$', selecionaDisciplina),
     (r'^preenche/(?P<req_sigla>\w{5})/$', preencheDisciplina),
     (r'^salva/(?P<req_sigla>\w{5})/', salvaDisciplina),
     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
         'document_root': TEMPLATE_DIRS[1]
         })
)
