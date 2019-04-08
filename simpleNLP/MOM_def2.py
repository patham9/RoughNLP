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
Repres=[('IRRELEVANTFORNOW', ' '), ('SOMETHING', ' $1 '), ('VARX', ' $X '), ('VARY', ' $Y '), ('VARZ', ' $Z '), ('WHAT', ' ?1 '), ('IS', ' is '), ('MADE', ' made '), ('PART', ' part '), ('HAS', 'has')]
# Word Types (word_regex,Type) #todo use a tagger for adjectives and verbs!!
Types=[
('(was|be|gets|is|are)$', 'IS'),
('(have)$', 'HAS'), #everything that reduced to has, already including has
('(and)$', 'AND'),
('(made)$', 'MADE'), #made
('(part)$', 'PART'), #plastic
('(or)$', 'OR'),
('(after|if|when|whenever)$', 'AFTER'),
#('(it|itself|he|she|they)$', 'REF'),
('(much|many|would|actually|immediately|that|the|a|an|inside|onto|can)$', 'IRRELEVANTFORNOW'),
('(in|of|on|to)', 'PREP'),
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
['N N N', '<(*,{0},{2}) --> {1}>', 'shark kill human'], 
['N IS MADE PREP N', '<(*,{0},{4}) --> MadeOf>', 'cat is made of fur'],
['N IS PART PREP N', '<(*,{0},{4}) --> PartOf>', 'cat is made of fur']]

ExtraForms=[]

#Default knowledge in Narsese
DefaultKnowledge=""""""
#Language Knowledge
Sentences=[]
