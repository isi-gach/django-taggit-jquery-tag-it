from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson

from taggit.models import Tag


def list_tags(request):
    """List all tags that start with the given query"""

    query = request.GET.get('q', None)
    if request.method != 'GET' or not query:
        return HttpResponseBadRequest()

    filters = getattr(settings, 'TAGGIT_AUTOCOMPLETE_FILTERS', {})
    try:
        tags = Tag.objects.filter(
            name__istartswith=query, **filters).values_list('name', flat=True)
    except:  # Naked except, we may not have access to hvad
        tags = Tag.objects.language().filter(
            name__istartswith=query, **filters).values_list('name', flat=True)

    tags = list(tags)
    return HttpResponse(simplejson.dumps(tags), mimetype='text/javascript')
