import os

from datetime import datetime,timedelta, date
import wget


class DownloadClass(object):
    """Class that downloads the file from url to destination"""
    def download_file(self, url, destination):
        if os.path.exists(destination):
            mtime = date.fromtimestamp(os.path.getmtime(destination))
            cur_time = date.today() - timedelta(days = 1)
            if(mtime < cur_time ):
                os.remove(destination)
                wget.download(url, destination)
        else:    
            wget.download(url, destination)

