# This file is part of Active Archives.
# Copyright 2006-2011 the Active Archives contributors (see AUTHORS)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Also add information on how to contact you by electronic and paper mail.

"""
aacore.sniffers
"""

import urllib2
import magic
import re
import subprocess
import RDF

from django.template import Template, Context
from django.template.loader import get_template
from urllib2utils import ResourceOpener

from aacore import RDF_MODEL
from aacore.settings import SNIFFERS
from html5tidy import tidy


sniffers = []


rdfa = RDF.Parser("rdfa")


def extract(d, keys):
    """
    Extracts named keys from a dictionnary.
    """
    return dict((k, d[k]) for k in keys if k in d)


def sniffer(syntax):
    """
    Registers the decorated classes to the list of available sniffers.

    Takes a syntax name to be used to parse the classes index method return value.
    """
    def decorator(cls):
        cls.syntax = syntax
        sniffers.append(cls)
        return cls
    return decorator 


class AAResource(object):
    """
    Represents a web resource.

    Implements an index method that is used to inspect the resource and store
    the information found in the RDF store.
    """
    def __init__(self, url, content=None):
        self.url = url
        self.content = content
        self.dummy_model = self.get_dummy_model()

    def get_sniffers(self):
        """
        Tests the available sniffers and returns the matching ones.
        """
        cls = []
        for sniffer in sniffers:
            if sniffer().test(self.dummy_model):
                cls.append(sniffer)
        return cls

    def get_dummy_model(self):
        """
        Creates and returns an in-memory HashStorage RDF Model.

        It is useful for testing purpose or for temporary storage.
        """
        options = "new='yes', hash-type='memory', contexts='yes'"
        storage = RDF.HashStorage('dummy', options=options)
        return RDF.Model(storage)

    def index_content(self):
        metadata = {}
        mime = magic.from_buffer(tidy(self.content), mime=True)
        metadata['mime_type'] = mime
        print("Detected mime-type: %s" % mime)

        t = get_template("aacore/http.html")
        c = Context({'metadata': metadata, 'url': self.url})

        rdfa.parse_string_into_model(self.dummy_model, t.render(c).encode("utf-8"), self.url)
        #print("indexing content at %s" % self.url)
        #string = tidy(self.content)
        #rdfa.parse_string_into_model(self.dummy_model, string, self.url)

        RDF_MODEL.remove_statements_with_context(RDF.Node(self.url))
        RDF_MODEL.add_statements(self.dummy_model.as_stream(), RDF.Node(self.url))
        RDF_MODEL.sync()


    def index(self):
        """
        Inspects the resource and store the information found in the RDF store.
        """
        # Opens an HTTP request
        try:
            data = ResourceOpener(url=self.url)
            data.get()
        except urllib2.HTTPError, e:
            data.status = e.code

        # Extracts some interesting response fields
        interesting_keys = ['content_type', 'charset', 'content_length', 'last_modified', 'etag', 'status']
        metadata = extract(data.__dict__, interesting_keys)

        # Detects the mime type from content as an alternative to content-type
        mime = magic.from_buffer(data.file.read(1024), mime=True)
        metadata['mime_type'] = mime

        # Maps the HTTP metadata to RDFa and indexes it in a temporary model
        t = get_template("aacore/http.html")
        c = Context({'metadata': metadata, 'url': self.url})
        rdfa.parse_string_into_model(self.dummy_model, t.render(c).encode("utf-8"), self.url)

        # Indexes the content with the appropriate agents (sniffers)
        for sniffer in self.get_sniffers():
            string = sniffer().sniff(self.url)
            if not string:
                break
            if sniffer.syntax == "rdfa":
                string = tidy(string)
            parser = RDF.Parser(name=sniffer.syntax)
            parser.parse_string_into_model(self.dummy_model, string.encode("utf-8"), self.url)

        # Replaces from the RDF model the existing statements with the new ones
        RDF_MODEL.remove_statements_with_context(RDF.Node(self.url))
        RDF_MODEL.add_statements(self.dummy_model.as_stream(), RDF.Node(self.url))
        RDF_MODEL.sync()


map(__import__, SNIFFERS)
