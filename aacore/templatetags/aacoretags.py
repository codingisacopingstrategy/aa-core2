import urlparse
import xml.sax.saxutils
import urllib
import os.path
import datetime
from django.template.defaultfilters import stringfilter
from django import template
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from html5tidy import tidy
#from aacore.models import Namespace
import rdfutils



register = template.Library()

####################
## RDF


@register.filter
def browseurl(node):
    """
    Reverses the browse url of a resource or a litteral.
    """
    return reverse('aa-browse') + "?" + urllib.urlencode({'node': node})


@register.filter
def rdfnode (node):
    return rdfutils.rdfnode(node)


@register.filter
def rdfnodedisplay (node):
    if node.is_resource():
        uri = rdfnode(node)
        link = reverse('aacore.views.browse') + "?" + urllib.urlencode({'node': uri})
        return mark_safe('<a href="%s">%s</a>' % (link, compacturl(uri)))

    elif node.is_literal():
        return rdfnode(node)

    elif node.is_blank():
        return "blank" + node.blank_identifier

    else:
        return node


@register.filter
def rdfbrowselink (node):
    """
    filter by aa-resource
    """
    if node.is_resource():
        uri = rdfnode(node)
        return mark_safe('<a href="%s" title="%s">%s</a>' % (browseurl(uri), uri, compacturl(uri)))

    elif node.is_literal():
        literal = rdfnode(node)
        link = reverse('aa-browse') + "?" + urllib.urlencode({'node': literal})
        return mark_safe('<a href="%s">%s</a>' % (link, literal))

    elif node.is_blank():
        link = reverse('aa-browse') + "?" + urllib.urlencode({'node': "blank:" + node.blank_identifier})
        return mark_safe('<a href="%s">%s</a>' % (link, "blank" + node.blank_identifier))

    else:
        return node


@register.filter
def rdfrellink (node):
    """ filter by aa-resource """
    if node.is_resource():
        uri = rdfnode(node)
        link = reverse('aa-browse') + "?" + urllib.urlencode({'node': uri})
        return mark_safe('<a href="%s" title="%s">%s</a>' % (link, uri, compacturl(uri)))

    elif node.is_literal():
        literal = rdfnode(node)
        link = reverse('aa-browse') + "?" + urllib.urlencode({'node': literal})
        return mark_safe('<a href="%s">%s</a>' % (link, literal))

    elif node.is_blank():
        link = reverse('aa-browse') + "?" + urllib.urlencode({'node': "blank:"+node.blank_identifier})
        return mark_safe('<a href="%s">%s</a>' % (link, "blank"+node.blank_identifier))

    else:
        return node


@register.filter
def rdfviewslink (node):
    """ filter used in aacore.views.browse (debug) """
    if node.is_resource():
        uri = rdfnode(node)
        link = reverse('aa-rdf-browse') + "?" + urllib.urlencode({'node': uri})
        return mark_safe('<a href="%s">%s</a>' % (link, compacturl(uri)))

    elif node.is_literal():
        literal = rdfnode(node)
        link = reverse('aa-rdf-browse') + "?" + urllib.urlencode({'node': literal})
        return mark_safe('<a href="%s">%s</a>' % (link, literal))

    elif node.is_blank():
        link = reverse('aa-rdf-browse') + "?" + urllib.urlencode({'node': "blank:" + node.blank_identifier})
        return mark_safe('<a href="%s">%s</a>' % (link, "blank" + node.blank_identifier))

    else:
        return node


#@register.filter
#@stringfilter
#def compacturl (url):
    #url = rdfnode(url)
    #for ns in Namespace.objects.all():
        #if url.startswith(ns.url):
            #return ns.name + ":" + url[len(ns.url):]
    #return url


#@register.filter
#@stringfilter
#def namespace_for_url (url):
    #url = rdfnode(url)
    #for ns in Namespace.objects.all():
        #if url.startswith(ns.url):
            #return ns.name
    #return url


@register.filter
@stringfilter
def url_filename (url):
    parts = urlparse.urlparse(url)
    if parts.path:
        d, p = os.path.split(parts.path.rstrip('/'))
        if p:
            return p
        else:
            return d
    else:
        return url


@register.filter
@stringfilter
def url_hostname (url):
    """
    Returns the hostname of the given URL

    Usage format::

        <dl>
            <dt>Host name</dt>
            <dd property="http:hostname">{{ resource.url|url_hostname }}</dd>
        </dl>
    """
    return urlparse.urlparse(url).netloc


@register.filter
@stringfilter
def html5tidy (src):
    return mark_safe(tidy(src, fragment=True))


@register.filter
@stringfilter
def xmlescape (src):
    return xml.sax.saxutils.escape(src)


@register.filter
def iso8601_date (date):
    """
    Renders the given datetime object to its iso8601 representations
    """
    t = type(date)

    if t == datetime.datetime:
        return date.date().isoformat()
    elif t == datetime.date:
        return date.isoformat()
    else:
        return date

        #literal = unicode(rdfnode(node)).encode('utf-8')
        #literal = rdfnode(node)
        # FIXME: urlencode does not seem to appreciate Arabic:
        #        UnicodeEncodeError at /browse/ with URL <http://www.youtube.com/watch?v=YeoF74Vu180>


@register.filter
def dashify(value):
    """
    Substitues underscores with dashes
    """
    return value.replace ("_", "-")
