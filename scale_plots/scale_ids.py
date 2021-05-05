# Dictionary of nuclide ids and names
# Found in Table 10.1.1 of the Scale documentation
mat_ids = {1001:'h', 1001001:'h-liquid_ch4', 2001001:'h-solid_ch4', 4001001:'h-cryo_ortho', 5001001:'h-cryo_para',
           6001001:'h-benzene', 7001001:'h-zrh2', 8001001:'hfreegas', 9001001:'h-poly', 1002:'d', 4001002:'d-cryo_ortho',
           5001002:'d-cryo_para', 8001002:'dfreegas', 1003:'h-3', 2003:'he-3', 2004:'he-4', 3006:'li-6', 3007:'li-7', 4007:'be-7', 4009:'be-9',
           3004009:'bebound', 5004009:'be-beo', 5010:'b-10', 5011:'b-11', 6000:'c', 3006000:'graphite', 5006000:'h-benzene', 7014:'n-14',
           7015:'n-15', 8016:'o-16', 5008016:'o-beo', 8017:'o-17', 9019:'f-19', 11022:'na-22', 11023:'na-23', 12024:'mg-24',
           12025:'mg-25', 12026:'mg-26', 13027:'al-27', 1013027:'albound', 14028:'si-28', 14029:'si-29', 14030:'si-30',
           1014028:'sibound', 1014029:'sibound', 1014030:'sibound', 15031:'p-31', 16032:'s-32', 16033:'s-33', 16034:'s-34', 16036:'s-36',
           17035:'cl-35', 17037:'cl-37', 18036:'ar-36', 18038:'ar-38', 18040:'ar-40', 19039:'k-39', 19040:'k-40', 19041:'k-41',
           20040:'ca-40', 20042:'ca-42', 20043:'ca-43', 20044:'ca-44', 20046:'ca-46', 20048:'ca-48', 21045:'sc-45', 22046:'ti-46',
           22047:'ti-47', 22048:'ti-48', 22049:'ti-49', 22050:'ti-50', 23000:'v', 23050:'v-50', 23051:'v-51', 24050:'cr-50',
           24052:'cr-52', 24053:'cr-53', 24054:'cr-54', 25055:'mn-55', 26054:'fe-54', 26056:'fe-56', 26057:'fe-57', 26058:'fe-58',
           1026000:'febound', 27058:'co-58', 1027058:'co-58m', 27059:'co-59', 28058:'ni-58', 28059:'ni-59', 28060:'ni-60', 28061:'ni-61',
           28062:'ni-62', 28064:'ni-64', 29063:'cu-63', 29065:'cu-65', 30000:'zn', 30064:'zn-64', 30065:'zn-65', 30066:'zn-66',
           30067:'zn-67', 30068:'zn-68', 30070:'zn-70', 31069:'ga-69', 31071:'ga-71', 32070:'ge-70', 32072:'ge-72', 32073:'ge-73',
           32074:'ge-74', 32076:'ge-76', 33074:'as-74', 33075:'as-75', 34074:'se-74', 34076:'se-76', 34077:'se-77', 34078:'se-78',
           34079:'se-79', 34080:'se-80', 34082:'se-82', 35079:'br-79', 35081:'br-81', 36078:'kr-78', 36080:'kr-80', 36082:'kr-82',
           36083:'kr-83', 36084:'kr-84', 36085:'kr-85', 36086:'kr-86', 37085:'rb-85', 37086:'rb-86', 37087:'rb-87', 38084:'sr-84',
           38086:'sr-86', 38087:'sr-87', 38088:'sr-88', 38089:'sr-89', 38090:'sr-90', 39089:'y-89', 39090:'y-90', 39091:'y-91',
           40090:'zr-90', 1040090:'zr90-zr5h8', 40091:'zr-91', 1040091:'zr91-zr5h8', 40092:'zr-92', 1040092:'zr92-zr5h8',
           40093:'zr-93', 1040093:'zr93-zr5h8', 40094:'zr-94', 1040094:'zr94-zr5h8', 40095:'zr-95', 1040095:'zr95-zr5h8',
           40096:'zr-96', 1040096:'zr96-zr5h8', 41093:'nb-93', 41094:'nb-94', 41095:'nb-95', 42092:'mo-92', 42094:'mo-94',
           42095:'mo-95', 42096:'mo-96', 42097:'mo-97', 42098:'mo-98', 42099:'mo-99', 42100:'mo-100', 43099:'tc-99', 44096:'ru-96',
           44098:'ru-98', 44099:'ru-99', 44100:'ru-100', 44101:'ru-101', 44102:'ru-102', 44103:'ru-103', 44104:'ru-104',
           44105:'ru-105', 44106:'ru-106', 45103:'rh-103', 45105:'rh-105', 46102:'pd-102', 46104:'pd-104', 46105:'pd-105',
           46106:'pd-106', 46107:'pd-107', 46108:'pd-108', 46110:'pd-110', 47107:'ag-107', 47109:'ag-109', 1047110:'ag-110m',
           47111:'ag-111', 48106:'cd-106', 48108:'cd-108', 48110:'cd-110', 48111:'cd-111', 48112:'cd-112', 48113:'cd-113',
           48114:'cd-114', 1048115:'cd-115m', 48116:'cd-116', 49113:'in-113', 49115:'in-115', 50112:'sn-112', 50113:'sn-113',
           50114:'sn-114', 50115:'sn-115', 50116:'sn-116', 50117:'sn-117', 50118:'sn-118', 50119:'sn-119', 50120:'sn-120',
           50122:'sn-122', 50123:'sn-123', 50124:'sn-124', 50125:'sn-125', 50126:'sn-126', 51121:'sb-121', 51123:'sb-123',
           51124:'sb-124', 51125:'sb-125', 51126:'sb-126', 52120:'te-120', 52122:'te-122', 52123:'te-123', 52124:'te-124',
           52125:'te-125', 52126:'te-126', 1052127:'te-127m', 52128:'te-128', 1052129:'te-129m', 52130:'te-130', 52132:'te-132',
           53127:'i-127', 53129:'i-129', 53130:'i-130', 53131:'i-131', 53135:'i-135', 54123:'xe-123', 54124:'xe-124', 54126:'xe-126',
           54128:'xe-128', 54129:'xe-129', 54130:'xe-130', 54131:'xe-131', 54132:'xe-132', 54133:'xe-133', 54134:'xe-134',
           54135:'xe-135', 54136:'xe-136', 55133:'cs-133', 55134:'cs-134', 55135:'cs-135', 55136:'cs-136', 55137:'cs-137',
           56130:'ba-130', 56132:'ba-132', 56133:'ba-133', 56134:'ba-134', 56135:'ba-135', 56136:'ba-136', 56137:'ba-137',
           56138:'ba-138', 56140:'ba-140', 57138:'la-138', 57139:'la-139', 57140:'la-140', 58136:'ce-136', 58138:'ce-138',
           58139:'ce-139', 58140:'ce-140', 58141:'ce-141', 58142:'ce-142', 58143:'ce-143', 58144:'ce-144', 59141:'pr-141',
           59142:'pr-142', 59143:'pr-143', 60142:'nd-142', 60143:'nd-143', 60144:'nd-144', 60145:'nd-145', 60146:'nd-146',
           60147:'nd-147', 60148:'nd-148', 60150:'nd-150', 61147:'pm-147', 61148:'pm-148', 1061148:'pm-148m', 61149:'pm-149',
           61151:'pm-151', 62144:'sm-144', 62147:'sm-147', 62148:'sm-148', 62149:'sm-149', 62150:'sm-150', 62151:'sm-151',
           62152:'sm-152', 62153:'sm-153', 62154:'sm-154', 63151:'eu-151', 63152:'eu-152', 63153:'eu-153', 63154:'eu-154',
           63155:'eu-155', 63156:'eu-156', 63157:'eu-157', 64152:'gd-152', 64153:'gd-153', 64154:'gd-154', 64155:'gd-155',
           64156:'gd-156', 64157:'gd-157', 64158:'gd-158', 64160:'gd-160', 65159:'tb-159', 65160:'tb-160', 66156:'dy-156',
           66158:'dy-158', 66160:'dy-160', 66161:'dy-161', 66162:'dy-162', 66163:'dy-163', 66164:'dy-164', 67165:'ho-165',
           1067166:'ho-166m', 68162:'er-162', 68164:'er-164', 68166:'er-166', 68167:'er-167', 68168:'er-168', 68170:'er-170',
           69168:'tm-168', 69169:'tm-169', 69170:'tm-170', 71175:'lu-175', 71176:'lu-176', 72174:'hf-174', 72176:'hf-176',
           72177:'hf-177', 72178:'hf-178', 72179:'hf-179', 72180:'hf-180', 73180:'ta-180', 73181:'ta-181', 73182:'ta-182',
           74180:'w-180', 74182:'w-182', 74183:'w-183', 74184:'w-184', 74186:'w-186', 75185:'re-185', 75187:'re-187', 77191:'ir-191',
           77193:'ir-193', 79197:'au-197', 80196:'hg-196', 80198:'hg-198', 80199:'hg-199', 80200:'hg-200', 80201:'hg-201',
           80202:'hg-202', 80204:'hg-204', 81203:'tl-203', 81205:'tl-205', 82204:'pb-204', 82206:'pb-206', 82207:'pb-207',
           82208:'pb-208', 83209:'bi-209', 88223:'ra-223', 88224:'ra-224', 88225:'ra-225', 88226:'ra-226', 89225:'ac-225',
           89226:'ac-226', 89227:'ac-227', 90227:'th-227', 90228:'th-228', 90229:'th-229', 90230:'th-230', 90231:'th-231',
           90232:'th-232', 90233:'th-233', 90234:'th-234', 91229:'pa-229', 91230:'pa-230', 91231:'pa-231', 91232:'pa-232',
           91233:'pa-233', 92230:'u-230', 92231:'u-231', 92232:'u-232', 92233:'u-233', 92234:'u-234', 92235:'u-235', 92236:'u-236',
           92237:'u-237', 92238:'u-238', 92239:'u-239', 92240:'u-240', 92241:'u-241', 93234:'np-234', 93235:'np-235', 93236:'np-236',
           93237:'np-237', 93238:'np-238', 93239:'np-239', 94236:'pu-236', 94237:'pu-237', 94238:'pu-238', 94239:'pu-239',
           94240:'pu-240', 94241:'pu-241', 94242:'pu-242', 94243:'pu-243', 94244:'pu-244', 94246:'pu-246', 95240:'am-240',
           95241:'am-241', 95242:'am-242', 1095242:'am-242m', 95243:'am-243', 95244:'am-244', 1095244:'am-244m', 96240:'cm-240',
           96241:'cm-241', 96242:'cm-242', 96243:'cm-243', 96244:'cm-244', 96245:'cm-245', 96246:'cm-246', 96247:'cm-247',
           96248:'cm-248', 96249:'cm-249', 96250:'cm-250', 97245:'bk-245', 97246:'bk-246', 97247:'bk-247', 97248:'bk-248',
           97249:'bk-249', 97250:'bk-250', 98246:'cf-246', 98248:'cf-248', 98249:'cf-249', 98250:'cf-250', 98251:'cf-251',
           98252:'cf-252', 98253:'cf-253', 98254:'cf-254', 99251:'es-251', 99252:'es-252', 99253:'es-253', 99254:'es-254',
           1099254:'es-254m', 99255:'es-255', 100255:'fm-255'}

# Dictionary of reaction ids and names
# Found in Table 10.1.A.1 of the Scale documentation.
# Uses the shorthand when one was given. If a description
# does not make sense, longer descriptions are given in the table.
mt_ids = {1:'n,total', 2:'z,z0', 3:'z,nonelastic', 4:'z,n', 5:'z,anything', 10:'z,continuum', 11:'z,2nd', 16:'z,2n',
          17:'z,3n', 18:'z,fission', 19:'n,f', 20:'n,nf', 21:'n,2nf', 22:'z,n\u03b1', 23:'n,n3\u03b1', 24:'z,2n\u03b1',
          25:'z,3n\u03b1', 27:'n,abs', 28:'z,np', 29:'z,n2\u03b1', 30:'z,2n2\u03b1', 32:'z,nd', 33:'z,nt', 34:'z,n3He',
          35:'z,nd2\u03b1', 36:'z,nt2\u03b1', 37:'z,4n', 38:'n,3nf', 41:'z,2np', 42:'z,3np', 44:'z,n2p', 45:'z,np\u03b1', 50:'y,n0',
          51:'z,n1', 52:'z,n2', 90:'z,n40', 91:'z,nc', 101:'n,disap', 102:'z,\u03b3', 103:'z,p', 104:'z,d', 105:'z,t',
          106:'z,3He', 107:'z,\u03b1', 108:'z,2\u03b1', 109:'z,3\u03b1', 111:'z,2p', 112:'z,p\u03b1', 113:'z,t2\u03b1',
          114:'z,d2\u03b1', 115:'z,pd', 116:'z,pt', 117:'z,d\u03b1', 151:'n,RES', 201:'z,\u03a7n', 202:'z,\u03a7\u03b3',
          203:'z,\u03a7p', 204:'z,\u03a7d', 205:'z,\u03a7t', 206:'z,\u03a73He', 207:'z,\u03a7\u03b1', 208:'z,\u03a7\u03c0+',
          209:'z,\u03a7\u03c00', 210:'z,\u03a7\u03c0-', 211:'z,\u03a7\u03bc+', 212:'z,\u03a7\u03bc-', 213:'z,\u03a7\u03ba+',
          214:'z,\u03a7\u03ba0long', 215:'z,\u03a7\u03ba0short', 216:'z,\u03a7\u03ba-', 217:'z,\u03a7p', 218:'z,\u03a7n', 251:'n,\u03bcL',
          252:'n,\u03be', 253:'n,\u03b6', 301:'n,total kerma', 302:'z,z0 kerma', 303:'z,nonelastic kerma', 304:'z,n kerma',
          305:'z,anything kerma', 310:'z,continuum kerma', 311:'z,2nd kerma', 316:'z,2n kerma', 317:'z,3n kerma', 318:'z,fission kerma',
          319:'n,f kerma', 320:'n,nf kerma', 321:'n,2nf kerma', 322:'z,n\u03b1 kerma', 323:'n,n3\u03b1 kerma', 324:'z,2n\u03b1 kerma',
          325:'z,3n\u03b1 kerma', 327:'n,abs kerma', 328:'z,np kerma', 329:'z,n2\u03b1 kerma', 330:'z,2n2\u03b1 kerma', 332:'z,nd kerma',
          333:'z,nt kerma', 334:'z,n3He kerma', 335:'z,nd2\u03b1 kerma', 336:'z,nt2\u03b1 kerma', 337:'z,4n kerma', 338:'n,3nf kerma',
          341:'z,2np kerma', 342:'z,3np kerma', 344:'z,n2p kerma', 345:'z,np\u03b1 kerma', 350:'y,n0 kerma', 452:'z,\u03bdT',
          454:'z,Independent fission product yield data', 455:'z,\u03bdd', 456:'z,\u03bdp', 457:'z,Radioactive decay data',
          458:'n,Energy release in fission for incident neutrons', 459:'z,Cumulative fission product yield data', 500:'Total charged-particle stopping power',
          501:'Total photon interaction', 502:'Photon coherent scattering', 504:'Photon incoherent scattering', 505:'Imaginary scattering factor',
          506:'Real scattering factor', 515:'Pair production, electron field', 516:'Pair production; electron + nuclear field',
          517:'Pair production, nuclear field', 522:'Photoelectric absorption', 523:'Photo-excitation cross section', 526:'Electro-atomic scattering',
          527:'Electro-atomic bremsstrahlung', 528:'Electro-atomic excitation cross section', 533:'Atomic relaxation data', 534:'K', 535:'L1', 536:'L2',
          537:'L3', 538:'M1', 539:'M2', 540:'M3', 541:'M4', 542:'M5', 543:'N1', 544:'N2', 545:'N3', 546:'N4', 547:'N5',
          548:'N6', 549:'N7', 550:'O1', 551:'O2', 552:'O3', 553:'O4', 554:'O5', 555:'O6', 556:'O7', 557:'O8', 558:'O9',
          559:'P1', 560:'P2', 561:'P3', 562:'P4', 563:'P5', 564:'P6', 565:'P7', 566:'P8', 567:'P9', 568:'P10', 569:'P11',
          570:'Q1', 571:'Q2', 572:'Q3', 600:'z,p0', 601:'z,p1', 602:'z,p2', 603:'z,p3', 604:'z,p4', 649:'z,pc', 650:'z,d0',
          651:'z,d1', 652:'z,d2', 699:'z,dc', 700:'z,t0', 701:'z,t1', 702:'z,t2', 749:'z,tc', 750:'n,3He0', 751:'n,3He1',
          799:'n,3Hec', 800:'z,\u03b10', 801:'z,\u03b11', 849:'z,\u03b1c', 875:'z,2n0', 876:'z,2n1', 891:'z,2nc',
          1000:'Transport cross section based on the outscatter approximation', 1001:'Transport cross section based on the inscatter approximation', 1007:'Thermal scattering matrix',
          1008:'Elastic part of thermal scattering matrix', 1018:'Fission spectrum', 1019:'First chance fission spectrum', 1020:'Second chance fission spectrum',
          1021:'Third chance fission spectrum', 1038:'Fourth chance fission spectrum', 1099:'Group integral of the weight function',
          1111:'Flux moment (P1) weighted total cross section', 1112:'Flux moment (P2) weighted total cross section', 1113:'Flux moment (P3) weighted total cross section',
          1114:'Flux moment (P4) weighted total cross section', 1115:'Flux moment (P5) weighted total cross section', 1116:'Flux moment (P6) weighted total cross section',
          1117:'Flux moment (P7) weighted total cross section', 1118:'Flux moment (P8) weighted total cross section', 1119:'Flux amount (P9) weighted total cross section',
          1452:'Product of \u03bdT times the fission cross section', 1456:'Product of \u03bdp times the fission cross section',
          1455:'Product of \u03bdd times the fission cross section', 1500:'Transport cross section based on the outscatter approximation for gamma-ray cross sections',
          1501:'Transport cross section based on the inscatter approximation for gamma-ray cross sections', 1527:'Gamma-ray energy absorption coefficient factors',
          2006:'Non-absorption collision probability', 2016:'Probability of emitting two neutrons', 2017:'Probability of emitting three neutrons', 2018:'Fission probability',
          2022:'Within-group scattering cross section', 2027:'Absorption probability', 4561:'\u03bdp for first chance fissions',
          4562:'\u03bdp for second chance fissions', 4563:'\u03bdp for third chance fissions', 4564:'\u03bdp for fourth chance fissions'}

# Elements and their atomic numbers
elements = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10,
            'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20,
            'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30,
            'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40,
            'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50,
            'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60,
            'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70,
            'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80,
            'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90,
            'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100,
            'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109,
            'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118}

specials = {'D': 1002, 'H-liquid_CH4': 1001001, 'Albound': 1013027, 'Zr90-Zr5H8': 1040090, 'Zr91-Zr5H8': 1040091,
            'Zr92-Zr5H8': 1040092, 'Zr93-Zr5H8': 1040093, 'Zr94-Zr5H8': 1040094, 'Zr95-Zr5H8': 1040095,
            'Zr96-Zr5H8': 1040096, 'H-solid_CH4': 2001001, 'Bebound': 3004009, 'H-cryo_ortho': 4001001,
            'D-cryo_ortho': 4001002, 'H-cryo_para': 5001001, 'D-cryo_para': 5001002, 'Be-BeO': 5004009,
            'O-BeO': 5008016, 'H-benzene': 6001001, 'H-ZrH2': 7001001, 'Hfreegas': 8001001, 'Dfreegas': 8001002,
            'H-poly': 9001001, 'page': 1597}

def get_name(key):
    '''Translates the numbered names into string names'''
    name = ''
    E = {v: k for k, v in elements.items()}
    # Extract the mass number
    A = '-' + str(key % 1000)
    # Find the correct name from the atomic number
    special_num = key // 1000000
    special_str = ''
    if special_num == 0:
        Z = E[key // 1000]
    else:
        
        

    # Add full name to the list
    name = Z + A + special_str
    return name

for key in mat_ids.keys():
    print(get_name(key))