server = "irc.freenode.net"
channel = "#nars"
botnick = "mr_nars"

def ReplaceRequest(R): exec 'def Request(s,arg=\"N0\"): return R(s,arg)' in locals(),globals()
#Operator word
OperatorWord="invokes" #nars brings the newspaper whenever the sun is shining and nars invokes op1
InternalOp="say" #some really registered operator
Selfworld="nars"
#simple replacements
Replacements=[('that','and'),('but','and')]
#Representations (type,transform), as what should words of type get transformed to? to variables, words?
Repres=[('IRRELEVANTFORNOW', ' '), ('SOMETHING', ' $1 '), ('VARX', ' $X '), ('VARY', ' $Y '), ('VARZ', ' $Z '), ('WHAT', ' ?1 '), ('IS', ' is '), ('HAS', 'has')]
# Word Types (word_regex,Type) #todo use a tagger for adjectives and verbs!!
Types=[
('(was|be|gets|is|are)$', 'IS'),
('(have)$', 'HAS'), #everything that reduced to has, already including has
('(and)$', 'AND'),
('(or)$', 'OR'),
('(in|at|on)$', 'PREP'),
('(of|to|about)$', 'PREP'),
('(after|if|when|whenever)$', 'AFTER'),
#('(it|itself|he|she|they)$', 'REF'),
('(much|many|would|actually|immediately|that|the|a|an|inside|onto|can)$', 'IRRELEVANTFORNOW'),
('(not|doesn\'t)$', 'ZOT'), #not..
('(something|someone|somewhere|it|itself|he|she|they)$', 'SOMETHING'),
('(X)$', 'VARX'),
('(Z)$', 'VARY'),
('(Y)$', 'VARZ'),
('(what|who|where|which|why)$', 'WHAT'),
('.*', 'N')]

#Sentence Structures [WordTypes,Meaning,Description]
BasicForms=[ #todo improve with tagging results
#['N N', '<{0} --> [{1}]>', 'shark kill'],
['N IS N', '<{0} --> {2}>', 'house is old'],
['N N N', '<(*,{0},{2}) --> {1}>', 'shark kill human'], 
['N N N N', '<(*,{0},(&,{2},{3})) --> {1}>', 'sam eats good pizza'],
['N N N N N', '<(*,(&,{0},{1}),(&,{3},{4})) --> {2}>', 'old sam eats good pizza'],
['N N IS N N', '<(&,{0},{1}) --> (&,{3},{4})>', 'old sam is good human'],
['N IS N N', '<{0} --> (&,{2},{3})>', 'tom is good human'],
['N IS N N PREP N', '<(*,(*,{0},{5}),{3}) --> {2}_{4}>', 'the bottle is reminding people of beer'],
['N IS N N PREP N N', '<(*,(*,{0},(&,{5},{6}))),{3}) --> {2}_{4}>', 'the bottle is reminding people of beer'],
['N N IS N N PREP N', '<(*,(*,(&,{0},{1}),{6}),{4}) --> {3}_{5}>', 'the bottle is reminding people of beer'],
['N N IS N N PREP N N', '<(*,(*,(&,{0},{1}),(&,{6},{7}))),{4}) --> {3}_{5}>', 'the bottle is reminding people of beer'],
['N IS N PREP N','(&&,<(*,{0},{4}) --> {3}>,<{0} --> {2}>)','cat is sitting on table'],
['N IS PREP N','<(*,{0},{3}) --> {2}>','cat is on table'],
['N IS PREP N N','<(*,{0},(&,{3},{4})) --> {2}>','cat is on good table'],
['N N IS N PREP N','(&&,<(*,(&,{0},{1}),{5}) --> {4}>,<(&,{0},{1}) --> {3}>)','good cat is sitting on table'],
['N N IS PREP N','<(*,(&,{0},{1}),{4}) --> {3}>','good cat is on table'],
['N N IS N PREP N N','(&&,<(*,(&,{0},{1}),(&,{5},{6}))) --> {4}>,<(&,{0},{1}) --> {3}>)','good cat is sitting on table'],
['N N IS PREP N N','<(*,(&,{0},{1}),(&,{4},{5})) --> {3}>','good cat is on table'],
['N IS N PREP N N','(&&,<(*,{0},(&,{4},{5}))) --> {3}>,<{0} --> {2}>)','cat is sitting on table'],
['N IS PREP N N','<(*,{0},(&,{3},{4})) --> {2}>','cat is on table'],
['N IS N N PREP N','(&&,<(*,{0},{5}) --> {4}>,<{0} --> (*,{2},{3})>)','cat is putting stuff on table'],
['N IS N N PREP N N','(&&,<(*,{0},(&,{5},{6})) --> {4}>,<{0} --> (*,{2},{3})>)','cat is putting stuff on old table'],
['N N IS N N PREP N N','(&&,<(*,(&,{0},{1}),(&,{6},{7})) --> {5}>,<(&,{0},{1}) --> (*,{3},{4})>)','old cat is putting stuff on old table'],
['N N IS N N PREP N','(&&,<(*,(&,{0},{1}),{6}) --> {5}>,<(&,{0},{1}) --> (*,{3},{4})>)','old cat is putting stuff on table']
]

ExtraForms=[ #will not be combined like basic forms, yet OR versions will be produced
['N IS N AND N', '(&&,<{0} --> {2}>,<{0} --> {4}>)', 'house is old and damaged'],
#['N N N N AND N', '(&&,<(*,{0},(&,{2},{3})) --> {1}>,<(*,{0},{5}) --> {1}>)', 'sam likes good pizza and beer'],
['N IS N N AND N', '(&&,<{0} --> (&,{2},{3})>,<{0} --> {5}>)', 'calzone is good pizza and food'],
['N N IS N N AND N', '(&&,<(&,{0},{1}) --> (&,{3},{4})>,<(&,{0},{1}) --> {6}>)', 'fresh calzone is good pizza and food'], #
#['N N N N N AND N', '(&&,<(*,(&,{0},{1}),(&,{3},{4})) --> {2}>,<(*,(&,{0},{1}),{6}) --> {2}>)', 'old sam likes good pizza and beer'],
['N N N AND N', '(&&,<(*,{0},{2}) --> {1}>,<(*,{0},{4}) --> {1}>)', 'sam likes tim and tom'],
['N N IS N AND N', '(&&,<(&,{0},{1}) --> {3}>,<(&,{0},{1}) --> {5})', 'tasty calzone is good pizza and food'],
['N N N AND IS N', '(&&,<(*,{0},{2}) --> {1}>,<{0} --> {5}>)', 'sam likes tim and is human'],
#N N at the end:
['N IS N AND N N', '(&&,<{0} --> {2}>,<{0} --> (&,{4},{5})>)', 'house is old and damaged garbage'],
#['N N N N AND N N', '(&&,<(*,{0},(&,{2},{4})) --> {1}>,<(*,{0},(&,{5},{6})) --> {1}>)', 'sam likes good pizza and cold beer'],
['N IS N N AND N N', '(&&,<{0} --> (&,{2},{2})>,<{0} --> (&,{5},{6})>)', 'calzone is good pizza and healthy food'], #
['N N IS N N AND N N', '(&&,<(&,{0},{1}) --> (&,{3},{4})>,<(&,{0},{1}) --> (&,{6},{7})>)', 'old sam likes tasty pizza and good beer'], #
#['N N N N N AND N N', '(&&,<(*,(&,{0},{1}),(&,{3},{4})) --> {2}>,<(*,(&,{0},{1}),(&,{6},{7})) --> {2}>)', 'old sam likes tasty pizza and good beer'],
['N N N AND N N', '(&&,<(*,{0},{2}) --> {1}>,<(*,{0},(&,{4},{5})) --> {1}>)', 'sam likes tim and old tom'],
['N N IS N AND N N', '(&&,<(&,{0},{1}) --> {3}>,<(&,{0},{1}) --> (&,{5},{6}))', 'tasty calzone is good pizza and food'],
['N N N AND IS N N', '(&&,<(*,{0},{2}) --> {1}>,<{0} --> (&,{5},{6})>)', 'sam likes tim and is good boy']]

#Default knowledge in Narsese
DefaultKnowledge=""""""
#Language Knowledge
Sentences=[]
