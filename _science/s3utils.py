'''
Created on 2013-08-30

@author: Ian
'''
from storages.backends.s3boto import S3BotoStorage

StaticRootS3BotoStorage = lambda: S3BotoStorageAdminFix(location='static')
MediaRootS3BotoStorage  = lambda: S3BotoStorageAdminFix(location='media')

class S3BotoStorageAdminFix(S3BotoStorage):
    
    def url(self, name):
        url = super(S3BotoStorageAdminFix, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url
