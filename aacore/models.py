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
Active Archives aacore models
"""


from django.db import models


class Namespace (models.Model):
    """
    Defines RDF namespaces and assigns them HTML colors.
    
    Colors are used to generate stylesheets. 
    """
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    color = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name