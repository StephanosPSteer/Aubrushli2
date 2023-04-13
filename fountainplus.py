"""
fountainplus.py
extended version of fountain.py by Stephanos Steer - stephanos_steer@yahoo.co.uk
Original Python code at https://gist.github.com/ColtonProvias/8232624
Based on Fountain by Nima Yousefi & John August
Original code for Objective-C at https://github.com/nyousefi/Fountain
Further Edited by Manuel Senfft
"""


COMMON_TRANSITIONS = {'FADE OUT.', 'CUT TO BLACK.', 'FADE TO BLACK.'}
UPPER_ALPHABETS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ ÄÖÜ'


class FountainElement:
    def __init__(
        self,
        element_type,
        element_text='',
        section_depth=0,
        scene_number='',
        is_centered=False,
        is_dual_dialogue=False,
        original_line=0,
        scene_abbreviation='.',
        original_content='',
	    curr_scene_no=0
    ):
        self.element_type = element_type
        self.element_text = element_text
        self.section_depth = section_depth
        self.scene_number = scene_number
        self.scene_abbreviation = scene_abbreviation
        self.is_centered = is_centered
        self.is_dual_dialogue = is_dual_dialogue
        self.original_line = original_line
        self.original_content = original_content
        

    def __repr__(self):
        return self.element_type + ': ' + self.element_text


class Fountain:
    def __init__(self, string=None, path=None):
        self.metadata = dict()
        self.elements = list()
        self.curr_scene_no = 0
        #02/09/22 be nice in the future to import cats from e.g. csv as an option. quite like the idea of adding 
        # colours or colour codes to csvs too
        self.breakcats = ['CAST:', 'EXTRAS SILENT:', 'EXTRAS ATMOSPHERE:', 'PROPS:', 'WARDROBE:', 'SPECIAL EQUIPMENT:',
        'COSTUMES:','MAKEUP & HAIR:','VEHICLES:','STUNTS:', 'SOUND FX & MUSIC:', 'PRODUCTION NOTES:', 'GREENS:',
        'SPFX:', 'LIVESTOCK:', 'WRANGLER:', 'VFX:', 'SET DRESSING:', 'WEAPONS:','SHOTSTART', 'SHOTEND']
        self.csvrow =[]
        self.shotrow =[]
        #02/09/22 like with cats maybe offer to change headers but really only header names would be possible 
        # without potentially tonnes of work
        self.csvheader =['Scene Number',  'Scene Name','TAG','Tagged Resource Required','Surrounding Text', 
        'Start Line Index', 'Start Char Index', 'End Char Index']
        
        self.shotheader =['Shot Number', 'Scene Number', 'Scene Name',  'Shot Size','Shot Type','AngleOrigin','MoveMent', 
        'lens', 'Sound', 'Description', 'Start Line Index', 'Start Char Index', 'End Char Index', 'End Line Index', 'Surrounding Text']
        self.alllines =[]
        self.characters=[]
        self.curr_scene_name = ''
        if path:
            with open(path) as fp:
                self.contents = fp.read()
        else:
            self.contents = string
        if self.contents != '':
            self.parse()
        

    def parse(self):
        contents = self.contents.strip().replace('\r', '')

        contents_has_metadata = ':' in contents.splitlines()[0]
        contents_has_body = '\n\n' in contents

        if contents_has_metadata and contents_has_body:
            script_head, script_body = contents.split('\n\n', 1)
            self._parse_head(script_head.splitlines())
            self._parse_body(script_body.splitlines())
        elif contents_has_metadata and not contents_has_body:
            self._parse_head(contents.splitlines())
        else:
            self._parse_body(contents.splitlines())


    def BoneBreak(self,theline, index=None, curr_scene=0):
            if ('/*' and '*/') in theline :
                for breaker in self.breakcats:
                    
                    mystart = theline.find('/*')
                    
                    while theline.count('/*',mystart) !=0 :
                        mystart = theline.find('/*',mystart)
                        myend = theline.find('*/',mystart)
                        #print("all of them " + theline)
                        
                        if (breaker != 'SHOTSTART' and breaker != 'SHOTEND') and breaker in theline[mystart:myend+2]:
                        

                            self.csvrow.append([curr_scene,  self.curr_scene_name, breaker, theline[mystart:myend+2],theline, index, mystart, myend])
                    
                        elif (breaker == 'SHOTSTART') and breaker in theline[mystart:myend+2]:
                            #print("SHOTSTART " + theline)
                            colonindex = theline.find(':')
                            shotnostartindex = theline.find('SHOTSTART ') +10
                            
                            shotno = theline[shotnostartindex:colonindex]
                            shotinfostr = theline[colonindex+1:myend]
                            shotinfolist = shotinfostr.split(",")
                            scenedef = curr_scene
                            if curr_scene ==0:
                                scenedef = shotinfolist[0]


                            self.shotrow.append([shotno, scenedef,  self.curr_scene_name, shotinfolist[1], shotinfolist[2],
                            shotinfolist[3], shotinfolist[4], shotinfolist[5], shotinfolist[6], shotinfolist[7], index, mystart, myend])
                        

                        elif (breaker == 'SHOTEND') and breaker in theline[mystart:myend+2]:
                            #print("SHOTEND " + theline)
                            colonindex = theline.find(':')
                            shotnostartindex = theline.find('SHOTEND ')+8
                            
                            shotno = theline[shotnostartindex:colonindex]
                            
                            for l in self.shotrow:
                                if l != []:
                                    
                                    if l[0] == shotno:
                                        l.insert(14,index)
                                        l.insert(15,self.alllines[l[10]:index+1])
                                        
                        mystart = myend +2

    def _parse_head(self, script_head):
        open_key = None
        for line in script_head:
            line = line.rstrip()
            if line[0].isspace():
                self.metadata[open_key].append(line.strip())
            elif line[-1] == ':':
                open_key = line[0:-1].lower()
                self.metadata[open_key] = list()
            else:
                key, value = line.split(':', 1)
                self.metadata[key.strip().lower()] = [value.strip()]

    def _parse_body(self, script_body):
        is_comment_block = False
        is_inside_dialogue_block = False
        newlines_before = 0
        index = -1
        comment_text = list()
        curr_scene_no =0
        

        for linenum, line in enumerate(script_body):
            assert type(line) is str
            index += 1
            line = line.lstrip()
            full_strip = line.strip()
            self.alllines.append(full_strip)

            if (not line or line.isspace()) and not is_comment_block:
                self.elements.append(FountainElement('Empty Line'))
                is_inside_dialogue_block = False
                newlines_before += 1
                continue
            #print(line)
            scriptbreak =  any(breaker in line for breaker in self.breakcats)
            
            if (line.startswith('/*') and not scriptbreak):
                #print('startswith')
               
                line = line.rstrip()
                if line.endswith('*/'):
                    text = line.replace('/*', '').replace('*/', '')
                    self.elements.append(
                        FountainElement(
                            'Boneyard',
                            text,
                            original_line=linenum,
                            original_content=line
                        )
                    )
                    is_comment_block = False
                    newlines_before = 0
                else:
                    is_comment_block = True
                    comment_text.append('')
                continue

            if (line.rstrip().endswith('*/') and not scriptbreak):
                #print(line)
                #y = line not in breakcats
                #print (y)
                text = line.replace('*/', '')
                comment_text.append(text.strip())
                self.elements.append(
                    FountainElement(
                        'Boneyard',
                        '\n'.join(comment_text),
                        original_line=linenum,
                        original_content=line
                    )
                )
                is_comment_block = False
                comment_text = list()
                newlines_before = 0
                continue

            if is_comment_block:
                comment_text.append(line)
                continue

            if line.startswith('==='):
                self.elements.append(
                    FountainElement(
                        'Page Break',
                        line,
                        original_line=linenum,
                        original_content=line
                    )
                )
                newlines_before = 0
                continue

            if len(full_strip) > 0 and full_strip[0] == '=':
                self.elements.append(
                    FountainElement(
                        'Synopsis',
                        full_strip[1:].strip(),
                        original_line=linenum,
                        original_content=line
                    )
                )
                continue

            if (
                newlines_before > 0
                and full_strip.startswith('[[')
                and full_strip.endswith(']]')
            ):
                self.elements.append(
                    FountainElement(
                        'Comment',
                        full_strip.strip('[] \t'),
                        original_line=linenum,
                        original_content=line
                    )
                )
                continue

            if len(full_strip) > 0 and full_strip[0] == '#':
                newlines_before = 0
                depth = full_strip.split()[0].count('#')
                self.elements.append(
                    FountainElement(
                        'Section Heading',
                        full_strip[depth:].strip(),
                        section_depth=depth,
                        original_line=linenum,
                        original_content=line
                    )
                )
                continue

            if len(line) > 1 and line[0] == '.' and line[1] != '.':
                newlines_before = 0
                if full_strip[-1] == '#' and full_strip.count('#') > 1:
                    scene_number_start = len(full_strip) - \
                        full_strip[::-1].find('#', 1) - 1
                    self.elements.append(
                        FountainElement(
                            'Scene Heading',
                            full_strip[1:scene_number_start].strip(),
                            scene_number=full_strip[
                                scene_number_start:
                            ].strip('#').strip(),
                            original_line=linenum,
                            original_content=line
                        )
                    )
                    curr_scene_no=full_strip[
                                scene_number_start:
                            ].strip('#').strip()
                    self.curr_scene_name = line #scene_name_start#full_strip[1:scene_number_start].strip()
                    
                else:
                    self.elements.append(
                        FountainElement(
                            'Scene Heading',
                            full_strip[1:].strip(),
                            original_line=linenum,
                            original_content=line
                        )
                    )
                    curr_scene_no = curr_scene_no +1
                    self.curr_scene_name =line#scene_name_start#full_strip[1:].strip()
                continue

            if (
                line[0:4].upper() in
                ['INT ', 'INT.', 'EXT ', 'EXT.', 'EST ', 'EST.', 'I/E ', 'I/E.']
                or line[0:8].upper() in ['INT/EXT ', 'INT/EXT.']
                or line[0:9].upper() in ['INT./EXT ', 'INT./EXT.']
            ):
                newlines_before = 0
                scene_name_start = line.find(line.split()[1])
                if full_strip[-1] == '#' and full_strip.count('#') > 1:
                    scene_number_start = len(full_strip) - \
                        full_strip[::-1].find('#', 1) - 1
                    self.elements.append(
                        FountainElement(
                            'Scene Heading',
                            full_strip[
                                scene_name_start:scene_number_start
                            ].strip(),
                            scene_number=full_strip[
                                scene_number_start:
                            ].strip('#').strip(),
                            original_line=linenum,
                            scene_abbreviation=line.split()[0],
                            original_content=line
                        )
                    )
                    full_strip[
                                scene_name_start:scene_number_start
                            ].strip()
                    curr_scene_no = full_strip[
                                scene_number_start:
                            ].strip('#').strip()
                    self.curr_scene_name = line#scene_name_start #full_strip[scene_name_start:scene_number_start].strip()
                    
                else:
                    self.elements.append(
                        FountainElement(
                            'Scene Heading',
                            full_strip[scene_name_start:].strip(),
                            original_line=linenum,
                            scene_abbreviation=line.split()[0],
                            original_content=line
                        )
                    )
                    curr_scene_no = curr_scene_no +1
                    self.curr_scene_name =line #scene_name_start#full_strip[scene_name_start:].strip()
                    
                    
                continue

            if full_strip.endswith(' TO:'):
                newlines_before = 0
                self.elements.append(
                    FountainElement(
                        'Transition',
                        full_strip,
                        original_line=linenum,
                        original_content=line
                    )
                )
                continue

            if full_strip in COMMON_TRANSITIONS:
                newlines_before = 0
                self.elements.append(
                    FountainElement(
                        'Transition',
                        full_strip,
                        original_line=linenum,
                        original_content=line
                    )
                )
                continue

            if full_strip[0] == '>':
                newlines_before = 0
                if len(full_strip) > 1 and full_strip[-1] == '<':
                    
                    self.elements.append(
                        FountainElement(
                            'Action',
                            full_strip[1:-1].strip(),
                            is_centered=True,
                            original_line=linenum,
                            original_content=line
                        )
                    )
                    self.BoneBreak(full_strip,index, curr_scene_no)
                else:
                    
                    self.elements.append(
                        FountainElement(
                            'Transition',
                            full_strip[1:].strip(),
                            original_line=linenum,
                            original_content=line
                        )
                    )
                    self.BoneBreak(full_strip, index, curr_scene_no)
                continue

            if (
                newlines_before > 0
                and index + 1 < len(script_body)
                and script_body[index + 1]
                and not line[0] in ['[', ']', ',', '(', ')']
                and (all([(c in UPPER_ALPHABETS) for c in full_strip])
                     or full_strip[0] == '@')
            ):
                newlines_before = 0
                if full_strip[-1] == '^':
                    for element in reversed(self.elements):
                        if element.element_type == 'Character':
                            element.is_dual_dialogue = True
                            break
                    self.BoneBreak(full_strip, index, curr_scene_no)
                    self.elements.append(
                        FountainElement(
                            'Character',
                            full_strip.lstrip('@').rstrip('^').strip(),
                            is_dual_dialogue=True,
                            original_line=linenum,
                            original_content=line
                        )
                        
                    )
                    self.characters.append(full_strip.lstrip('@').rstrip('^').strip())
                    is_inside_dialogue_block = True
                else:
                    
                    self.elements.append(
                        FountainElement(
                            'Character',
                            full_strip.lstrip('@'),
                            original_line=linenum,
                            original_content=line
                        )
                    )
                    self.characters.append(full_strip.lstrip('@'))
                    self.BoneBreak(full_strip, index, curr_scene_no)
                    is_inside_dialogue_block = True
                continue

            if is_inside_dialogue_block:
                if newlines_before == 0 and full_strip[0] == '(':
                    self.BoneBreak(full_strip, index, curr_scene_no)
                    self.elements.append(
                        FountainElement(
                            'Parenthetical',
                            full_strip,
                            original_line=linenum,
                            original_content=line
                        )
                    )
                else:
                    if self.elements[-1].element_type == 'Dialogue':
                        self.elements[-1].element_text = '\n'.join(
                            [self.elements[-1].element_text, full_strip]
                        )
                    else:
                        #self.BoneBreak(full_strip)
                        self.elements.append(
                            FountainElement(
                                'Dialogue',
                                full_strip,
                                original_line=linenum,
                                original_content=line
                            )
                        )
                        self.BoneBreak(full_strip, index, curr_scene_no)
                continue

            if newlines_before == 0 and len(self.elements) > 0:
                self.elements[-1].element_text = '\n'.join(
                    [self.elements[-1].element_text, full_strip])
                newlines_before = 0
            else:
                self.BoneBreak(full_strip, index, curr_scene_no)
                self.elements.append(
                    FountainElement(
                        'Action',
                        full_strip,
                        original_line=linenum,
                        original_content=line
                    )
                )
                newlines_before = 0