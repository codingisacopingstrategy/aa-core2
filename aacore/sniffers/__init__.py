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


import html5lib
import RDF
import requests


from aacore import RDF_MODEL
from aacore.settings import SNIFFERS


sniffers = []


def tidy(method):
    """
    Tidies the ouput of the given Sniffer sniff method.
    """
    def decorator(self):
        string = method(self)

        if not string:
            return string

        if self.syntax == "rdfa":
            parser = html5lib.HTMLParser(tree=html5lib.treebuilders.getTreeBuilder("dom"))
            dom = parser.parse(string, encoding='utf-8')
            string = dom.toxml()

        return string
    return decorator


def sniffer(syntax):
    """
    Registers the decorated classes to the list of available sniffers.

    Takes a syntax name to be used to parse the classes index method return value.
    """
    def decorator(cls):
        cls.syntax = syntax
        cls.sniff = tidy(cls.sniff)
        sniffers.append(cls)
        return cls
    return decorator 


class AAResource(object):
    """
    Represents a web resource.

    Implements an index method that is used to inspect the resource and store
    the information found in the RDF store.
    """
    def __init__(self, url):
        self.url = url
        self.dummy_model = self.get_dummy_model()

    def get_dummy_model(self):
        """
        Creates and returns an in-memory HashStorage RDF Model.

        It is useful for testing purpose or for temporary storage.
        """
        options = "new='yes', hash-type='memory', contexts='yes'"
        storage = RDF.HashStorage('dummy', options=options)
        return RDF.Model(storage)

    def index(self):
        """
        Inspects the resource and store the information found in the RDF store.
        """
        request = requests.get(self.url, prefetch=False)

        # Indexes the content with the appropriate agents (sniffers)
        for sniffer in sniffers:
            sniffer = sniffer(request=request, model=self.dummy_model)
            string = sniffer.sniff() if sniffer.test() else None

            if not string:
                break

            parser = RDF.Parser(name=sniffer.syntax)
            #parser.parse_string_into_model(self.dummy_model, string.encode("utf-8"), self.url)
            parser.parse_string_into_model(self.dummy_model, string, self.url)

        # Replaces from the RDF model the existing statements with the new ones
        RDF_MODEL.remove_statements_with_context(RDF.Node(self.url))
        RDF_MODEL.add_statements(self.dummy_model.as_stream(), RDF.Node(self.url))
        RDF_MODEL.sync()


map(__import__, SNIFFERS)
