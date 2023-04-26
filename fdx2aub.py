import xml.etree.ElementTree as ET
# tree = ET.parse(r'D:\pythonEnvs\stable_LLM\Big_Fish.fdx')
# root = tree.getroot()

# for child in root:
#     print(child.tag, child.attrib)

import sys
import sqlite3
import pandas as pd
from Aubrushli import Aubrushli
import os


class fdx2aub:


    def createbigcsv(self, csvpath, screenplayid):

        current_dir = os.path.dirname(os.path.abspath(__file__))

        connection = sqlite3.connect(current_dir + "/aubrushli.db")
        connection.execute('PRAGMA synchronous = NORMAL')
        connection.execute('PRAGMA journal_mode = WAL')
        connection.execute('PRAGMA cache_size = -8192')
        connection.commit()

        sql = "SELECT linenumber,  line, linetype, scenenum, length, pagenum, charsinscene FROM fdxlines where screenplayid = ?  order by linenumber"
        castcsvdf = pd.read_sql(sql, connection, params=(screenplayid,))
        #print(castcsvdf)
            #connection.commit()
        castcsvdf.to_csv(csvpath, index=False)


    def writelinetodb(self, connection, screenplayID, line, linenum, linetype, scenenum, scenetypenum, officialnum='', length='', pagenum='', chars=0 ):
        #print(connection, screenplayID, line, linenum, linetype, scenenum, scenetypenum, officialnum, length, pagenum, chars )
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO fdxlines (screenplayID, line, linenumber, linetype, scenenum, scenetypenum, officialnum, length, pagenum, charsinscene) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (screenplayID, line, linenum, linetype, scenenum, scenetypenum, officialnum, length, pagenum, chars))
        connection.commit()
        # # last_id = cursor.lastrowid


    def create_cast_list(self,castlistpath, screenplayid):
        #print(screenplayid)

        current_dir = os.path.dirname(os.path.abspath(__file__))

        connection = sqlite3.connect(current_dir + "/aubrushli.db")
        connection.execute('PRAGMA synchronous = NORMAL')
        connection.execute('PRAGMA journal_mode = WAL')
        connection.execute('PRAGMA cache_size = -8192')
        connection.commit()

        sql = "select line as character, count(line) as lines from fdxlines where linetype = 'character' and screenplayid = ? group by line order by lines desc"
        castcsvdf = pd.read_sql(sql, connection, params=(screenplayid,))
        #print(castcsvdf)
            #connection.commit()
        castcsvdf.to_csv(castlistpath, index=False)
            
    def fdx2dbaub(self, input_file_name, shotsdef, outpath):
    
        current_dir = os.path.dirname(os.path.abspath(__file__))

        connection = sqlite3.connect(current_dir + "/aubrushli.db")
        connection.execute('PRAGMA synchronous = NORMAL')
        connection.execute('PRAGMA journal_mode = WAL')
        connection.execute('PRAGMA cache_size = -8192')
        connection.commit()
            
                        



            
        #output_file_name = r"D:\pythonEnvs\stable_LLM\test.txt"
        #input_file_name = r'G:\Aubrushli_images_current\Big_Fish.fdx'
        #shotsdef = r'G:\Aubrushli_images_current\shot_vals.csv'
        #outpath = 'G:/Aubrushli_images_current/fdxshotlists/'
        #file = open(output_file_name,"w")



        cursor = connection.cursor()
        cursor.execute('''INSERT INTO screenplay_document (Title,'Path') VALUES (?, ?)''', ('Big_Fish', input_file_name ))
        connection.commit()
        screenplayID = cursor.lastrowid
        #print(screenplayID)


        tree = ET.parse(input_file_name)
        # line, linenumber, linetype, linelength, numwords, firstwordpos, firstword, lastwordpos, lastword
        # you do not need all the above as already parsed by definition so just line, linenumber and linetype 
        # need to get line number which would be if its action, character, dialogue, para, scene, note not empty lines 
        # so you can create if you ever convert into pdf for example.


        linenum =0
        scenenum=0
        #typenum=0
        scenetypenum=0
        charsinscene=0    
        root = tree.getroot()
        for paragraph in root.iterfind('Content/Paragraph'):
                #print(paragraph)
                if paragraph.attrib['Type'] == "Action":
                    #print("action")
                    if hasattr(paragraph.find('Text'), 'text'):
                        for index, text_element in enumerate(paragraph.findall('Text')):
                            if (text_element.text is not None):
                                linenum = linenum + 1
                                scenetypenum= scenetypenum + 1
                                self.writelinetodb(connection, screenplayID, text_element.text , linenum, 'action', scenenum, scenetypenum )
                                #print(text_element.text)

                elif paragraph.attrib['Type'] == "General":

                    if hasattr(paragraph.find('Text'), 'text'):
                        for index, text_element in enumerate(paragraph.findall('Text')):
                            if (text_element.text is not None):
                                linenum = linenum + 1
                        
                                scenetypenum= scenetypenum + 1
                                self.writelinetodb(connection, screenplayID, text_element.text, linenum, 'label', scenenum, scenetypenum )

                elif paragraph.attrib['Type'] == "Transition":

                    if hasattr(paragraph.find('Text'), 'text'):
                        for index, text_element in enumerate(paragraph.findall('Text')):
                            if (text_element.text is not None):

                                linenum = linenum + 1
                                #scenenum = scenenum + 1
                        #typenum = typenum +1
                                scenetypenum= scenetypenum =0
                                self.writelinetodb(connection, screenplayID, text_element.text.upper(), linenum, 'transition', scenenum, scenetypenum )
        
                        
                elif paragraph.attrib['Type'] == "Character":
                    if hasattr(paragraph.find('Text'), 'text'):
                        for index, text_element in enumerate(paragraph.findall('Text')):
                            if (text_element.text is not None):
                                linetype =''
                                if "(" in text_element.text or ")" in text_element.text or "cont’d" in text_element.text:
                                    #charsinscene= charsinscene +1
                                    linetype = 'parenthetical'
                                else:
                                    #print(text_element.text, linenum)
                                    charsinscene= charsinscene +1
                                    linetype = 'character'
                                linenum = linenum + 1
                    # typenum = typenum +1
                                scenetypenum= scenetypenum + 1
                                self.writelinetodb(connection, screenplayID, text_element.text.upper().strip(), linenum, linetype, scenenum, scenetypenum, chars=charsinscene )

                elif paragraph.attrib['Type'] == "Parenthetical":
                    if hasattr(paragraph.find('Text'), 'text'):
                        for index, text_element in enumerate(paragraph.findall('Text')):
                            if (text_element.text is not None):

                                linenum = linenum + 1
                    # typenum = typenum +1
                                scenetypenum= scenetypenum + 1
                                self.writelinetodb(connection, screenplayID, text_element.text.upper(), linenum, 'parenthetical', scenenum, scenetypenum )
                    
                elif paragraph.attrib['Type'] == "Dialogue":
                    if hasattr(paragraph.find('Text'), 'text'):
                        for index, text_element in enumerate(paragraph.findall('Text')):
                            if (text_element.text is not None):
                                linenum = linenum + 1
                    # typenum = typenum +1
                                scenetypenum= scenetypenum + 1
                                self.writelinetodb(connection, screenplayID, text_element.text, linenum, 'dialogue', scenenum, scenetypenum )
                elif paragraph.attrib['Type'] == "Scene Heading":
                    off= paragraph.get('Number')
                    scene_properties = paragraph.find('SceneProperties').attrib
                    
                    # Access the values of the SceneProperties attributes
                    length = scene_properties['Length']
                    page = scene_properties['Page']
                
                    #print(child.attrib)
                    if hasattr(paragraph.find('Text'), 'text'):
                        thetext = ''
                        for index, text_element in enumerate(paragraph.findall('Text')):
                            if (text_element.text is not None):
                                thetext = thetext + ' ' + text_element.text.upper()
                        charsinscene=0 
                        linenum = linenum + 1
                    # typenum = typenum +1
                        scenenum = scenenum + 1
                        scenetypenum=0
                        self.writelinetodb(connection, screenplayID, thetext , linenum, 'scene', scenenum, scenetypenum, off, length, page, chars=charsinscene)

        #*************************steph need a characters in scene update here to distinct characters*************************************
        cursor = connection.cursor()
        sql = "CREATE TEMP TABLE distchars as select distinct line, scenenum from fdxlines where linetype = 'character' group by scenenum, line order by scenenum" 
        sql1 ="create temp table finchars as select count(line) thechars, scenenum from distchars group by scenenum"
        sql2 = "update fdxlines set charsinscene = f.thechars from (select thechars, scenenum from finchars) as f where f.scenenum = fdxlines.scenenum"
        sql3 = "INSERT INTO characters (screenplayID, charactername) select distinct screenplayid, trim(line) from fdxlines where linetype = 'character'"
        cursor.execute(sql)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        connection.commit()
        cursor = connection.cursor()
        sql4 = "SELECT characterID, screenplayID, charactername FROM characters where screenplayid =? "
        params = (screenplayID,)  # create a tuple of parameters
        cursor.execute(sql4, params)  # pass the tuple to cursor.execute()
        for row in cursor:
            print(row[1], row[2])
            cursor1 = connection.cursor()
            sql5= "INSERT INTO characteractions (characterID, actionID, charactername, theline) select ? , fdxlineID , ? , line from fdxlines where screenplayid =? and linetype = 'action' and (line like '% ' || ? || '%' or line like ? || '%')  "
            params1 = (row[0], row[2], screenplayID, row[2], row[2])
            cursor1.execute(sql5, params1) 
            #for newrow in cursor1:
            #    print(newrow)
            #b= row  
        cursor = connection.cursor()
        sql6= "update fdxlines set actchars = c.actchars from (select count(actionid) as actchars, actionid FROM characteractions group by actionid, theline) as c where c.actionid = fdxlines.fdxlineid"
        cursor.execute(sql6)
        connection.commit()



        # need to loop round each scene in db for shots call aubrushli.py




        # need a complete DF of the fdxlines table in the same format as fountain
        # need to put an id in fdxlines to match to the screenplay you need.
        sql = 'SELECT line, linetype, linenumber, scenenum, case when actchars is null then charsinscene else actchars end as charsinscene from fdxlines where screenplayID=?'
        df = pd.read_sql(sql, connection, params=(screenplayID,))

        df = df.rename(columns={'line': 'element_text', 'linetype': 'element_type', 'linenumber': 'original_line'})
        #print(df.columns)

        # need a shot vals df - taken from csv
        shot_vals_df = pd.read_csv(shotsdef)

        # need an actions in the current scene df in the same format as fountain
        scenes =[]
        cursor = connection.cursor()
        sql = 'SELECT distinct scenenum from fdxlines where screenplayID=?'
        params = (screenplayID,)  # create a tuple of parameters
        cursor.execute(sql, params)  # pass the tuple to cursor.execute()
        scenes = cursor.fetchall()  # fetch the results
        connection.commit()

        for scene in scenes:
            scenedf = df[(df['scenenum'] == scene[0])]
            scenedf = scenedf.reset_index(drop=True)
            currscenenamedf = scenedf[(scenedf['element_type']== 'scene')]
            currscenenamedf = currscenenamedf.reset_index(drop=True)
            #print(currscenenamedf)
            if len(currscenenamedf) >0:
                curscenename = currscenenamedf['element_text'][0]
                #print(curscenename)
                charsinscene = scenedf['charsinscene'][0]
                currsceneno = scenedf['scenenum'][0]
            
                actionsdf = scenedf[(scenedf['element_type'] == 'action')]

                # get the minimum value in column A
                startline = scenedf['original_line'].min()

                # get the maximum value in column A
                endline = scenedf['original_line'].max()
                combined=[]

                # #print(scene[0])
                # print(scenedf)
                # print(actionsdf)
                # print(startline)
                # print(endline)
                # print(charsinscene)

                aubshot = Aubrushli()
                aubshot.createshotlist( charsinscene, outpath, actionsdf, df, shot_vals_df, 2, startline, endline, currsceneno, curscenename, combined, 'Big_FDX_Fish')

                #createshotlist( numcharacters, outpath, action_df, df, shot_vals_df, sending_format=1, startline=f_start_scene_line, endline=f_next_scene_line, currscene=currscneno, currscenename=f_scene_name, combined=combine_chars):





        # also need a start and end line for the scene
        # use the sending format param to allow extra

        connection.close()

