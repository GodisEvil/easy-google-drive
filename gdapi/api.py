#!python
#-*- coding: utf-8 -*-
'''
    google drive api
'''

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError
import logging
import os


logger = logging.getLogger(__name__)


class MyDriver():
    def __init__(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("credentials.txt")
        if gauth.credentials is None:
            print(gauth.GetAuthUrl())
            gauth.CommandLineAuth()
        elif gauth.access_token_expired:
            logger.info('refresh token')
            gauth.Refresh()
        else:
            logger.info('authorized')
            gauth.Authorize()
        gauth.SaveCredentialsFile("credentials.txt")
        self._gauth = gauth
        self._drive = GoogleDrive(self._gauth)

    @property
    def drive(self):
        return self._drive

    def getAuthUri(self):
        '''
        auth to get token
        :return:
        '''
        return self.drive.auth.GetAuthUrl()

    def auth(self, code):
        '''
        填写了code之后，调用该接口通过认证；通过之后保存到认证文件
        :param code:
        :return:
        '''
        ret = self.drive.auth.Auth(code)
        self._gauth.SaveCredentialsFile("credentials.txt")
        return ret

    def uploadFile(self, localPath, parentId, remoteName=''):
        '''
        upload
        :param localPath:   local file path
        :param remoteName:  remote file name
        :return:
        '''
        ## if donot have remote file name, use local file name
        if not remoteName:
            remoteName = os.path.basename(localPath)
        http = self.drive.auth.Get_Http_Object()
        fileObj = self.drive.CreateFile()
        fileObj.SetContentFile(localPath)
        fileObj['title'] = remoteName
        fileObj['shared'] = True
        # fileObj['writersCanShare'] = True
        fileObj['parents'] = [{'id': parentId}]
        # fileObj['properties'] = {'shared': True}
        # fileObj['viewersCanCopyContent'] = True
        try:
            ret = fileObj.Upload(param={'http': http})
        except ApiRequestError, e:
            logger.info('upload %s to %s failed: %s' % (localPath, remoteName, str(e)))
            return False
        # print('Created file %s with mimeType %s' % (fileObj['title'], fileObj['mimeType']))
        # logger.info(fileObj)
        return fileObj.get('id')


    def mkDir(self, dname, parents):
        '''

        :param dname:
        :return:
        '''
        fileObj = self.drive.CreateFile({'title': dname, 'parents': [{'id': parents}],
                               "mimeType": "application/vnd.google-apps.folder", 'shared': True})
        http = self.drive.auth.Get_Http_Object()
        try:
            ret = fileObj.Upload(param={'http': http})
        except ApiRequestError, e:
            logger.info('create dir failed: %s, %s' % (dname, parents))
            return False
        # print('Created file %s with mimeType %s' % (fileObj['title'], fileObj['mimeType']))
        # logger.info(fileObj)
        return fileObj.get('id')

    def listDir(self, dname):
        q = "'%s' in parents and trashed=false" % dname
        flist = self.drive.ListFile({'q': q}).GetList()
        return flist


    def about(self):
        if self.drive.auth.access_token_expired:
            logger.info('token is expired')
            raise AuthError, 'token is expired'
        return self.drive.GetAbout()


    def infoFile(self, fid):
        '''
        get file info by id
        :param fid: 
        :return: 
        '''
        fileobj = self.drive.CreateFile({'id': fid})
        try:
            fileobj.Upload()
        except ApiRequestError, e:
            logger.info('get file info failed: ' + fid)
            return {}
        return fileobj


class AuthError(Exception):
    pass

driver = MyDriver()


if __name__ == '__main__':
    import sys
    logger = logging.getLogger('test')
    logger.setLevel(logging.DEBUG)
    hdr = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
    hdr.setFormatter(formatter)
    logger.addHandler(hdr)

    if len(sys.argv) < 3:
        print('Usage: %s functionName parameters' % sys.argv[0])
        sys.exit(1)
    if sys.argv[1] == 'uploadFile':
        print(driver.uploadFile(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else ''))
    elif sys.argv[1] == 'createDir':
        print(driver.mkDir(sys.argv[2], sys.argv[3]))
    elif sys.argv[1] == 'infoFile':
        print(driver.infoFile(sys.argv[2]))
    else:
        print('unsupported operation')
