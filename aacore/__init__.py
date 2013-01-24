import RDF
import settings


options = "hash-type='bdb', contexts='yes', dir='%s'" % settings.RDF_STORAGE_DIR
storage = RDF.HashStorage(settings.RDF_STORAGE_NAME, options=options)


RDF_MODEL = RDF.Model(storage)
