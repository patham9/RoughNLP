from subprocess import Popen, PIPE, STDOUT
import thread
import subprocess
import re,os
import socket
import sys
import time
import itertools
from MOM_def import *
proc = None

#ok form conjunctions thereof:
#Support for implication (AFTER):
indices = ["{"+str(i)+"}" for i in range(50)]
Forms2=[]
for a in BasicForms:
    for b in BasicForms:
        NewB = [x for x in b]
        #1. get the maximum of a
        k=-1
        h=0
        for ind in indices:
            #print ind, a[1]
            if ind in a[1]:
                k=h
            h+=1
        #2. add the maximum+2 to the indices
        #print NewB[1],k,len(indices),len(indices)-1-1-k
        for i in range(len(indices)-10-k,0-1,-1):
            NewB[1]=NewB[1].replace(indices[i],indices[i+k+2])
        #print NewB[1]
        NewB[0] = a[0] + " AND " + b[0]
        NewB[1] = "(&&," + a[1] + "," + NewB[1] + ")" 
        Forms2.append(NewB)
        #print NewB

for F in ExtraForms:
    Forms2.insert(0,F)

#Support for OR:
Forms3=[]
for F in Forms2:
    Forms3.append(F)
    F=[x for x in F]
    F[0]=F[0].replace("AND","OR")
    F[1]=F[1].replace("&&","||")
    Forms3.append(F)

#debug:
#Forms3=[['N N N AND N', '<(*,{0},(&,{2},{4})) --> {1}>', 'sam likes tim and tom'],
#['N IS N', '<{0} --> {2}>', 'house is old']]

for F in BasicForms:
    Forms3.insert(0,F)

#Support for implication (AFTER):
indices = ["{"+str(i)+"}" for i in range(50)]
Rules=[]
for a in Forms3:
    Rules.append(a)
    for b in Forms3:
        NewB = [x for x in b]
        #1. get the maximum of a
        k=-1
        h=0
        for ind in indices:
            #print ind, a[1]
            if ind in a[1]:
                k=h
            h+=1
        #2. add the maximum+2 to the indices
        #print NewB[1],k,len(indices),len(indices)-1-1-k
        for i in range(len(indices)-10-k,0-1,-1):
            NewB[1]=NewB[1].replace(indices[i],indices[i+k+2])
        #print NewB[1]
        NewB[0] = a[0] + " AFTER " + b[0]
        NewB[1] = "<" + NewB[1] + " ==> " + a[1] + ">" 
        Rules.append(NewB)
        #if NewB[0] == "N N N AFTER N N N":
        #    print NewB[0]
        #print NewB

print len(Rules)
#devug:
for z in Rules:
    if z[0] == "N N N AFTER N N N":
       print z

ReplaceRequest(lambda s,arg: [d.split("=")[1].replace(",","") for d in eval(PrettyTell(s)) if "=" in d and d.split("=")[0]==arg])
regexp_tag=lambda w: (j[1] for j in Types if re.match(j[0],w)!=None).next()
print "I'm a basic NARS NLP interface! If you want me to output all user-provided knowledge, write KNOWLEDGE, if you want to save it write SAVE, IRC if you want me to connect to IRC.\n"
Knowledge=[]; BackgroundKnowledge="""
"""

def SplitAndCombineMeaning(syntax,s,Offset):
	r2,r1,b1,c=(((("A"+Tell(s.split(c)[0],Recursion=True,Offset=Offset))).split("A"),("A"+Tell(c.join(s.split(c)[1:]),Recursion=True,Offset=Offset+len(
	[j for j in s.split(c)[0].split(" ") if j!=""])+1)).split("A"),b[1],c) for b in [] for c in b[0] if c in s).next()
	return r2[len(r2)-1].replace("T0","T0")+" "+b1.replace(",",". " if ":-" in r1[len(r1)-1] else ",")+" "+r1[len(r1)-1]

def AssumeReferences(syntax,words):  #if something like it or he or she is used, use the last noun we talked about (maybe better strategies one day)
	global lastNoun
	for u in range(len(syntax)):
		if u in range(len(syntax)) and syntax[u]=="N" and (u-1<0 or (syntax[u-1]!="IS" and syntax[u-1]!="N")): lastNoun=words[u]
		if syntax[u]=="REF": words[u],syntax[u]=lastNoun,"N"
	return " ".join(syntax),words

def AddSynonym(syntax,a,means): #add a synonymous sentence (much todo here) example: patrick is a cat = a cat patrick is
	global Rules
	try:#search for the equivalent words in the new sentence and update the indices in the meaning expression
		li=[ind.split("}")[0] for ind in means.split("{") if "}" in ind] 	     #old indices
		li2=[str(synonymli.index(a[int(li[i])])) for i in range(len(li))]        #new indices
		Rules+=[[lastSyntax,"".join([h.split("{")[0]+("{"+li2[i]+"}" if i<len(li2) else "") for i,h in enumerate(means.split("}")) if h!=""])]] #index replaced, pattern add
	except: print "(I don't understand the synonymity)"

def TrainTagger(bQuestion,Rs):
    global Types,Repres
    if len(Rs)==2 and not bQuestion:                                          #simple not grammatic dependent word learning 
        if Rs[0].isupper(): Repres+=[(Rs[0]," "+Rs[1]+" ")]; return True      #bicycle CYCLE; fahhrad CYCLE; CYCLE cycle => cycle=bicycle=fahrrad
        if Rs[1].isupper(): Types=[("("+Rs[0]+")$",Rs[1])]+Types; return True #word CATEGORY, CATEGORY word, example^

def AddKnowledge(ret, bQuestion,bGoal,bEvent,bPlan):
    global Knowledge, proc
    EventPostfix=" :|:" if bGoal or bEvent else ""
    newknol = ret.replace("T0","T0" if ":-" in ret else "0")
    if bPlan:
        print "WTF"
        newknol=newknol.replace("&&","&/").replace(") ==>",",+5) =/>").replace(",<(*,{SELF}",",+5,<(*,{SELF}")
    punctuation = "?" if bQuestion else ("!" if bGoal else ".")
    if proc!=None:
        print "Natural language input translated to Narsese: "+newknol+punctuation+EventPostfix
        proc.stdin.write(newknol+punctuation+EventPostfix+"\n")
    Knowledge+=sum([[kn+punctuation+EventPostfix for kn in newknol.split(", ") if kn!=""] if ":-" not in newknol else [newknol+"."]],[])
    with open("MOM_pl.pl", "w") as text_file: text_file.write(BackgroundKnowledge+"\n"+DefaultKnowledge+"\n"+"\n".join(Knowledge))

def GetMeaning(syntax,s,Offset):
    try: 
        ret2=[b[1] for b in Rules if len(syntax.split(" "))==len(b[0].split(" ")) and not False in [x in y for x,y in zip(syntax.split(" "),b[0].split(" "))]][0]
        for i,h in enumerate(re.finditer(r'\{([0-9]*)\}',ret2)): ret2=ret2.replace(h.group(0),"{"+str(int(h.group(0).replace("{","").replace("}",""))+Offset)+"}")
    except: ret2=str(SplitAndCombineMeaning(syntax,s,Offset))
    return ret2

def Do_Replacements(s):
    for a in Replacements:
        s=s.replace(a[0],a[1])
    return s

synonymadd=False; synonymli=[]; lastSyntax=""; SInput=[]; lastNoun=""
def Tell(s,ret="",Recursion=False,AddToSentences=True,Offset=0): 
    global Knowledge,synonymadd,synonymli,lastSyntax,SInput
    s=Do_Replacements(s)
    print s
    bGoal="!" in s
    bEvent="..." in s
    bPlan=OperatorWord in s
    s=s.replace("...","").replace("!","").replace(OperatorWord,"^"+InternalOp).replace(Selfworld,"{SELF}")
    bQuestion,Rs="?" in s,s.split(" ")
    if TrainTagger(bQuestion,Rs): print "Thank you for correcting me and training my tagger."; return ""
    if not Recursion and not bQuestion and AddToSentences: SInput+=[s]
    s=s.replace("?"," ").replace("."," ").replace(" ","  ") #which words of which type are in s:
    x_wd_in_s=lambda tp:["\s"+w+"\s" for w in [re.sub(r'(\$|\(|\))','',h) for h in sum([(g[0]+"|").split("|") for g in Types if g[1]==tp],[])] if " "+w+" " in " "+s+" " and w!='']
    for wordtype,replacement in Repres: #create boolean variables and rewrite word types instances according to the Repres rules
		exec wordtype+"=x_wd_in_s('"+wordtype+"');\nb"+wordtype+"="+wordtype+"!=[] if not Recursion else b"+wordtype in locals(),globals()
		s=eval("re.sub(r'('+'|'.join("+wordtype+")+')','"+replacement+"',' '+s+' ')  if "+wordtype+"!=[] else s")
    words=[z for z in s.split(" ") if z!=""]; syntax=map(regexp_tag,words)
    syntax,words=AssumeReferences(syntax,[d[1]+str(d[0]) if len(d[1])==1 and d[1].isupper() else d[1] for d in enumerate(words)]) #also replace N V and such with enumerated vars
    print syntax,x_wd_in_s
    try:
		ret2=GetMeaning(syntax,s,Offset)
		ret2,command=ret2.split("$") if "$" in ret2 else (ret2,"")
		ret=ret2.format(*words) if not Recursion else ret2
		if bQuestion and not "None" in ret and not Recursion:
			if not Recursion: AddKnowledge(ret, True,bGoal,bEvent,bPlan)
		elif not Recursion: AddKnowledge(ret, False,bGoal,bEvent,bPlan)
		exec (command.format(*words) if not Recursion else "") in locals(),globals()
		synonymadd=(AddSynonym(syntax,words,ret2) and False) if synonymadd and not Recursion else synonymadd
		return ret
    except:
		synonymli,synonymadd,lastSyntax=words,True,syntax
		print "I don't understand the form "+syntax+", tell me something synonymous or add a rule."

def init_proc():
    global proc
    proc = subprocess.Popen(["/home/tc/Dateien/jdk-10.0.2/bin/java","-cp","/home/tc/Dateien/NARSMOM/opennars-lab-3.0.1-SNAPSHOT.jar","org.opennars.main.Shell"], stdin=subprocess.PIPE, stdout=subprocess.PIPE) 

Narsese_Filter=["EXE: ","Answer:"]
Max_Outputs_Before_Reset=30
cnt=0

try:
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    irc.connect((server, 6667))
    irc.send("USER "+ botnick +" " + botnick +" "+ botnick +" :Hallo!\r\n")
    irc.send("NICK "+ botnick +"\r\n")
    irc.send("PRIVMSG nickserv :iNOOPE\r\n")
    irc.send("JOIN "+ channel +"\r\n") #fails on euirc, works in all others, euirc is not completely RFC 2810 compatible maybe?
    print "connected"
    init_proc()
    print "NARS instance created"
    proc.stdin.write("*volume=0\n");
    print "NARS is set to shut up: "+proc.stdout.readline()
    print "Narsese Filter applied: '"+str(Narsese_Filter)+"'"
    print "Max Outputs before Reset: "+str(Max_Outputs_Before_Reset)
    proc.stdin.write(DefaultKnowledge)
    print "Knowledge put in"
except:
    print "Starting without IRC functionality"
    None


def receive_thread(a):
    global cnt
    while True:
       msg=proc.stdout.readline()
       if "% {" in msg:
           msg=msg.split("% {")[0]+"%"
       if msg!=None and msg!="" and True in [u in msg for u in Narsese_Filter]: #we received an execution
          cnt+=1
          print "NAR output: "+msg
          bReset= cnt>=Max_Outputs_Before_Reset
          irc.send("PRIVMSG "+ channel +" : "+msg+"\r\n")
          if bReset:
              irc.send("PRIVMSG "+ channel +" : NAR RESET happened (max. amount of output happened)\r\n")
              cnt=0
              #proc.close()
              #init_proc();
              proc.stdin.write("*****\n")
              proc.stdin.write(knowledge)
              print "Knowledge put in"

if proc != None:
    thread.start_new_thread(receive_thread,(1,))

if os.path.exists("MOM_pl.pl"): os.remove("MOM_pl.pl")
[PrettyTell(Sentence) for Sentence in Sentences]
while 1!=0:
	txt=raw_input("you: ")
	if txt=="IRC":
		break;
	if txt=="KNOWLEDGE" or txt=="SAVE":
		toWrite=("def ReplaceRequest(R): exec 'def Request(s,arg=\"N0\"): return R(s,arg)' in locals(),globals()\n#Representations (type,transform), as what should words of type get transformed to? to variables, words?\nRepres="+str(Repres)+
		"\n# Logic Operators (words,syntax,type)\n")+("\n# Word Types (word_regex,Type)\nTypes="+str(Types)+
		"\n#Sentence Structures [WordTypes,"+
		"Meaning,Description]\n"+"#in sentences the left part of A in Meaning is for assumptions, else its just a &, and the part after $ is a python cmd(T0 for now(time)):\nRules="+str(Rules)+
		"\n#Knowledge the system doesn't include \nKnowledge=\"\"\""+Knowledge+"\"\"\"\n#Procedural Knowledge\nexec CustomCode\n#Language Knowledge\nSentences="+str(SInput).replace(", '",",\n'")).replace(", (",",\n(").replace(", [",",\n[")
		if txt=="SAVE":
			with open("MOM_def.py", "w") as def_file: def_file.write(toWrite)
		else: print toWrite
	else:
		print str(Tell(txt))
        
while True:
    try:
        text=irc.recv(2040)
        if "PING" in text:
            print "ping"
            STR='PONG :' + text.split("PING :")[1].split("\n")[0] + '\r\n';
            irc.send(STR)
        else:
            if "VERSION" in text:
                print "version"
                irc.send("JOIN "+ channel +"\r\n") #join when version private message comes :D
            else:
                if "system" in text.lower() or "from os" in text.lower() or "import os" in text.lower():
                    print "skipped"
                    continue
                SPL=text.split(":")
                TEXT=":".join(SPL[2:len(SPL)])
                if TEXT.replace(" ","").replace("\n","").replace("\r","")=="":
					continue
                print TEXT
                if TEXT.startswith("**"):
                    proc.stdin.write("*****\n")
                    proc.stdin.write(knowledge)
                    print "Knowledge put in"
                #if TEXT.startswith("<") or TEXT.startswith("("): #narsese backdoor
                #    print "NAR input: "+TEXT
                #    try:
                #        proc.stdin.write(TEXT)
                #    except:
                #        print "err"
                #        None
                else:
                    print "NAR input: "+TEXT
                    try:
                        Tell(TEXT.strip()) #was: proc.stdin.write
                    except:
                        print "err"
                        None
    except:
        print "exception"
None

