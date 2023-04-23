import os
#from sqlboiler import sqlboiler

class pathboiler:

    def getkeypaths(self):
        #no sql as causes circular path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(current_dir, 'aubrushli.db')
        return current_dir, db_path

    # def getstylepaths(self):
    #     current_dir, db_path = self.getkeypaths()
    #     stylesfolder = current_dir + "/styles/"
    #     sb = sqlboiler()
    #     currstyle = sb.getstyle()
    #     style_path = os.path.join(stylesfolder, currstyle)
    #     return stylesfolder, currstyle, style_path