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


from django.conf import settings
import os


RDF_STORAGE_NAME = getattr(settings, 'AA_RDF_STORAGE_NAME', "aa")
# Must be an absolute path
RDF_STORAGE_DIR = getattr(settings, 'AA_RDF_STORAGE_DIR', os.path.dirname(os.path.normpath(os.sys.modules[settings.SETTINGS_MODULE].__file__)))

SNIFFERS = getattr(settings, 'AA_SNIFFERS', ["aacore.sniffers.image", "aacore.sniffers.youtube", "aacore.sniffers.ogg", "aacore.sniffers.html"])
