import fountainplus
import pandas as pd
import argparse
from collections import Counter
import os
import csv

class Aubrushli:

    f_start_scene_line=0
    f_scene_name=''
    real_first_scene_line=0
    f_next_scene_line = 0
    curr_chars_in_scene =[]
    curr_act_chars_in_scene =[]
    combine_chars = []
    shotlist =[]
    outfolder = 'G:/Aubrushli_images_current/shotlists/'
    productionName = "bigfish"
    currdesc = ''
    currscneno = 0
    infile = "G:/Aubrushli_images_current/bigfish.fountain"
    shotsdef = 'G:/Aubrushli_images_current/shot_vals.csv'
    initialCSV = 'G:/Aubrushli_images_current/bigfish.csv'
    # need to insert at real lines not fountain lines so remember to add the difference on to the fountain line
    # to get the actual insert line

    def createbigcsv(self, fountainpath, csvpath):
        d = open(fountainpath, 'r')
        fountaintext = d.read()
        d.close()

        F = fountainplus.Fountain(fountaintext)

        #the main dataframe
        df = pd.DataFrame([{'element': element, 'original_line': element.original_line, 'scene_abbreviation': element.scene_abbreviation,
                            'original_content': element.original_content, 'element_type': element.element_type, 
                            'element_text': element.element_text, 'section_depth': element.section_depth, 
                            'scene_number': element.scene_number, 'is_centered': element.is_centered,
                            'is_dual_dialogue': element.is_dual_dialogue}
                        for element in F.elements])

        df.to_csv(csvpath, index=False)


    def create_cast_list(self, fountainpath, castlistpath):

        # Load the fountain file
        with open(fountainpath, 'r') as f:
            fountain_text = f.read()

        # Create a fountain object
        F = fountainplus.Fountain(fountain_text)

        # Get the cast list
        cast_list = list(Counter(F.characters).items())

        # Create a header for the cast list
        header = ['Cast Name', 'Dialogue Frequency']

        if castlistpath:
        # Create a CSV file for the cast list
            with open(castlistpath, 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(cast_list)


        

    def find_line_number(self, file_path, search_text):
        line_number = 0
        with open(file_path, 'r') as f:
            for line in f:
        
                line_number += 1
                if search_text in line:
                    return line_number -2
        return -1

    def createshotlist(self, numcharacters, outpath, action_df, df, shot_vals_df):

        print(self.f_start_scene_line)
        print(self.f_next_scene_line)
        print(numcharacters)
        print(outpath)


        # What are the actions in our scene
        filact_df = action_df[ 
                        (action_df['original_line'].astype(int) >= self.f_start_scene_line) & 
                        (action_df['original_line'].astype(int) <= self.f_next_scene_line)]
        
        filreact_df = filact_df.reset_index(drop=True)
        # shot number you create depending on shots 

        #the headers for the shotlist

        keys=['Shot Number', 'Scene Number', 'Scene Name', 'Shot Size', 'Shot Type', 'AngleOrigin', 'MoveMent', \
                                            'lens', 'Sound', 'Description', 'debug_chars', 'chars_in_scene']
    

        # loop through every row in the df in our current scene
        #you only care about actions that are adjacent to dialog/character
        # in which case store their original_line and match later
        
        matching_lines =[0]
        current_type = ''
        previousval = 0

        thisscene_df = df[(df['original_line'].astype(int) >= self.f_start_scene_line) & 
                        (df['original_line'].astype(int) <= self.f_next_scene_line)]
        
        for scenerowindex, thisscenerow in thisscene_df.iterrows():
            #print('element: ' + thisscenerow['element_type'])
            #print('current type' + current_type)
        
            
            # this horrible code is all about dialog and if it follows or precedes an action
            #if it does then I allow OTS shots as it implies we are in a conversation.
            #REMEMBER actions are the only thing I am sending to SD as dialog is heard not seen.
            # there is probably a much better way to do this.
            if current_type == '':
                current_type = thisscenerow['element_type']
            # now start checking element type
            if thisscenerow['element_type'] == 'Action' or thisscenerow['element_type'] == 'Dialogue' or thisscenerow['element_type'] == 'Character' or thisscenerow['element_type'] == 'Parenthetical':
                if thisscenerow['original_line'] == 24:
                    print(thisscenerow['element_type'])
                    # this element is an action was the previous dialoguey
                if thisscenerow['element_type'] == 'Action' and (current_type == 'Dialogue' or current_type == 'Character' or current_type == 'Parenthetical'):
                    matching_lines.append(thisscenerow['original_line'])
                    # this element is dialoguey was the previous an action
                elif (thisscenerow['element_type'] == 'Dialogue' or thisscenerow['element_type'] == 'Character' or thisscenerow['element_type'] == 'Parenthetical') and current_type == 'Action':
                    matching_lines.append(previousval)
                    #neither
            previousval = thisscenerow['original_line']
            current_type = thisscenerow['element_type']


    #not sure about this anymore as I need more than just checking if dialog exists now
        currdialog_df = df[(df['element_type'] =='Dialogue') &
                        (df['original_line'].astype(int) >= self.f_start_scene_line) & 
                        (df['original_line'].astype(int) <= self.f_next_scene_line)]

        finshot ={}
        # do I want drones and extreme wides, probably not indoors
        dronesetc = 0
        if 'EXT.' in self.f_scene_name or self.f_scene_name.startswith("."):
            dronesetc=1 #thetext in row['element_text']:
        # choose shots depending on characters in scene
        #print(f_scene_name)
        #print(dronesetc)
        # this check is all about what shots are needed as per number of characters
        filshot_df = shot_vals_df[(shot_vals_df['min_chars'] <=numcharacters) & (shot_vals_df['dronesetc'] <= dronesetc) &  (shot_vals_df['dialog'] <= len(currdialog_df))]
        finshot_df = filshot_df.reset_index(drop=True)
        finshot_df = finshot_df.drop_duplicates()
            
            #elif current_type == 'Action':
            #if current_type == '':
                #print(thisscenerow)
        
        
        #*********steph here 11/04/23 need to work out who the primary actor in the scene is. and create a column called primary actor
    # also the sentiment model is pretty good lets try it.
        


        mycounter=0
            # for ALL the actions in the scene
        for thisindex, theaction in filreact_df.iterrows():
            #print(theaction) # description 
            mydesc = theaction['element_text']
            eddesc = mydesc
            if '(V.O'.lower() in mydesc:
                #print(theaction['original_content'])
                eddesc =   mydesc.replace(theaction['original_content'].lower(), '') 
                #print(mydesc)
                #print(eddesc) 
                #THESE ARE THE SHOTS
            for index, shotrow in finshot_df.iterrows():
                    #otsok = 0
                    #values = index + 1, currscneno, f_scene_name, shotrow['shot_size'], shotrow['shot_type'], shotrow['AngleOrigin'], 'STATIC or PAN', shotrow['lens'] \
                    #            ,'SYNC', currdesc, numcharacters, combine_chars
                    
                    # if I have dialog is this actual action line before/after dialog in which case ots. 
                    # this may not make sense but testing for now
                    if (shotrow['shot_size'] == 'OTS' or shotrow['shot_size'] == 'OTS opposite'):
                        for line in matching_lines:
                            if theaction['original_line'] == line:
                                #otsok = 1
                                values = mycounter + 1, self.currscneno, self.f_scene_name, shotrow['shot_size'], shotrow['shot_type'], shotrow['AngleOrigin'], 'STATIC or PAN', shotrow['lens'] \
                                ,'SYNC', eddesc, numcharacters, self.combine_chars
                    
                                finshot[mycounter] = dict(zip(keys, values))
                                mycounter = mycounter +1
                                matching_lines.remove(line)
                    else:
                        values = mycounter + 1, self.currscneno, self.f_scene_name, shotrow['shot_size'], shotrow['shot_type'], shotrow['AngleOrigin'], 'STATIC or PAN', shotrow['lens'] \
                                ,'SYNC', eddesc, numcharacters, self.combine_chars
                    
                        finshot[mycounter] = dict(zip(keys, values))
                        mycounter = mycounter +1
            #mycounter = mycounter +1
            #df.loc[i] = [Shot_Number , Scene_Number, Scene_Name, Shot_Size, Shot_Type, AngleOrigin, MoveMent, lens, Sound, Description]
        shotlist_df = pd.DataFrame.from_dict(finshot, orient='index') # shotlist_df.append(row, ignore_index=True)
        nodots = self.f_scene_name.replace(".","")
        noslashes = nodots.replace("/","")
        nosbacklashes = noslashes.replace("\\","")
        nospaces = nosbacklashes.replace(" ","_")
        csvpath = outpath + '/' + str(self.currscneno) + self.productionName + '_' + nospaces + '.csv'
            # Write the dataframe to a CSV file
        shotlist_df.to_csv(csvpath, index=False)

    def generateallshotlists(self, fountainfile, shotvalsfile, outpath):
        
        d = open(fountainfile, 'r')
        fountain_text = d.read()
        d.close()

        ### got text into lines ready top be inserted if you need to modify original
        #lines = work_with_me.splitlines()

            # make it a fountain object to get all the elements.
        F = fountainplus.Fountain(fountain_text)


        # this will probably go in the datbase eventually
        shot_vals_df = pd.read_csv(shotvalsfile)

        #the main dataframe
        df = pd.DataFrame([{'element': element, 'original_line': element.original_line, 'scene_abbreviation': element.scene_abbreviation,
                            'original_content': element.original_content, 'element_type': element.element_type, 
                            'element_text': element.element_text, 'section_depth': element.section_depth, 
                            'scene_number': element.scene_number, 'is_centered': element.is_centered,
                            'is_dual_dialogue': element.is_dual_dialogue}
                        for element in F.elements])


 

        #scenes df
        # if i can get llama, alpaca or vicuna or whatever on commandline or better yet python then maybe I can throw the scene
        #at them and get sentiment and maybe main action also to possibly override wrong logic. UPDATE tried it right now vicuna
        #worked a bit but spout out mad stuff which makes it no use for automation. Keep an eye though as things move fast.
        scene_df = df.loc[df['element_type'] =='Scene Heading']

        # we need that index back to 0
        filtered_scene_df = scene_df.reset_index(drop=True)

        # characters df
        character_df = df.loc[(df['element_type'] =='Character')]

            #character_df['element_text'] = character_df['element_text'].str.lower()
        # for matching set to 0
        character_df.loc[:, 'element_text'] = character_df['element_text'].str.lower()

        #actions df
        action_df = df[(df['element_type'] =='Action')]

        # Convert all strings to lowercase

        #for matching
        action_df.loc[:, 'element_text'] = action_df['element_text'].str.lower()

        #get chars in actionlines 
        # but have to exclude voice over (V.O.), Off screen (O.S.)
            # done exclusions
        my_list = []

        for index,row in action_df.iterrows():
            for thetext in character_df['element_text'].unique():
                #does the character exist in the action text
                if thetext in row['element_text']:
                    #If they do find the index of that text
                    start_index = row['element_text'].find(thetext)
                    # If the text starts at the beginning, or it is later on in which case does it have a space?
                    if start_index == 0 or (start_index > 0 and row['element_text'][start_index - 1] == ' '):
                        if ("(V.O" or "(O.S") not in row['original_content']:
                        
                            my_list.append((thetext, row['original_line']))
                    




        # the big loop of where we are scene by scene
        for index, scenerow in filtered_scene_df.iterrows():
            self.curr_chars_in_scene=[]
            self.curr_act_chars_in_scene=[]
            self.shotlist =[]
            self.combine_chars = []

            self.f_start_scene_line = scenerow['original_line'] #scene_df.iloc[index][1]
            self.f_scene_name = scenerow['original_content']

            # dealing with out of bounds errors no looking at end of main df not scene df
            endindex = index + 1
            if endindex == len(filtered_scene_df):
                self.f_next_scene_line = df.iloc[-1][1]
            else:
                self.f_next_scene_line = filtered_scene_df.iloc[endindex][1] -1

            # this is if I alter/ make a copy of original doc
            if index == 0:
                self.real_first_scene_line= self.find_line_number(fountainfile, self.f_scene_name)
        
            self.currscneno = index
            # Convert the f_first_scene_line and f_next_scene_line variables to integers
            self.f_start_scene_line = int(self.f_start_scene_line)
            self.f_next_scene_line = int(self.f_next_scene_line)



            filcharacter_df = character_df[ 
                            (character_df['original_line'].astype(int) >= self.f_start_scene_line) & 
                            (character_df['original_line'].astype(int) <= self.f_next_scene_line)]

            # #print(filcharacter_df['element_text'])

            for indexfil, row in filcharacter_df.iterrows():
                self.curr_chars_in_scene.append(row['element_text'])

            # so for every line number in my current scene check if I have characters in actions if I do
            for myline in range(self.f_start_scene_line, self.f_next_scene_line):
                for thetext, original_line in my_list:
                    if int(myline) == int(original_line):
                
                        self.curr_act_chars_in_scene.append(thetext)
                
            #print(curr_act_chars_in_scene)

            # Combine the two lists and get unique items using set()
            combine_chars = self.curr_chars_in_scene + self.curr_act_chars_in_scene
            combine_charsdf = pd.DataFrame({'items': combine_chars})
        # Count the items in the third list
            character_count = len(combine_charsdf['items'].unique())
            #print(count)
            #self.createshotlist(character_count) 
            self.createshotlist(character_count, outpath, action_df, df, shot_vals_df)


    def create_breakdown_summary(self, fountainfile, csvfile):
                # Get the input file name
        # Load the fountain file
        with open(fountainfile, 'r') as f:
            fountain_text = f.read()

        # Create a fountain object
        F = fountainplus.Fountain(fountain_text)

        # Get the breakdown summary
        breakdown_summary = F.csvheader
        data = F.csvrow

        # Sort the data by scene number, shot number, and action
        data.sort(key=lambda x: (x[5], x[6], x[7]))

        # Create a CSV file for the breakdown summary
        with open(csvfile, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(breakdown_summary)
            writer.writerows(data)
            f.close

    def create_legacy_shotlist(self, fountainfile, csvfile):
                # Get the input file name
        # Load the fountain file
        with open(fountainfile, 'r') as f:
            fountain_text = f.read()

        # Create a fountain object
        F = fountainplus.Fountain(fountain_text)

        # Get the breakdown summary
        header = F.shotheader
        data = F.shotrow

        # Create a CSV file for the breakdown summary
        with open(csvfile, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(data)
            f.close
