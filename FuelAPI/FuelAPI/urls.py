from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
                       url(r'^docs/', include('rest_framework_swagger.urls', namespace='swagger')),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^v0\.1/', include('v0_1.urls', namespace='v0.1'))
                       )

