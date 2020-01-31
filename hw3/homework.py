# -*- coding:utf-8 -*-
import re
import copy


idCreater = 0
"""
问题：目前这语句顺序怎么整

isalways TRUE 怎么办？？？
subsumption
句子去重怎么做
"""
    
class Literal:
    def __init__(self, name, neg, args):
        self.name = name
        self.neg = neg
        self.args = args
        
    def standardize(self, sentence_id):
        for i in range(len(self.args)):
            if self.args[i].islower():
                self.args[i] += ("@" + str(sentence_id))
        return self

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.neg != other.neg:
            return False

        for i in range(len(self.args)):
            # if self.args[i].istitle() and other.args[i].istitle and self.args[i] != other.args[i]:
            #     return False

            if self.args[i].islower() and other.args[i].islower():
                continue
            else:
                return False
            # if self.args[i] != other.args[i]:
            #     return False
        return True

    def changeArgs(self, sub, id):
        for i in range(len(self.args)):
            if self.args[i].islower():
                if self.args[i] in sub:
                    if sub[self.args[i]].islower(): # 还是变量
                        var = sub[self.args[i]]
                        self.args[i] = var[:var.index("@")] + ("@" + str(id))
                    else:
                        self.args[i] = sub[self.args[i]]
                else:
                    var = self.args[i]
                    self.args[i] = var[:var.index("@")] + ("@" + str(id)) # 还是变量

    def opposite(self, other):
        if self.name != other.name:
            return False
        if self.neg == other.neg:
            return False
        for i in range(len(self.args)):
            if self.args[i].istitle() and other.args[i].istitle and self.args[i] != other.args[i]:
                return False
            # if self.args[i] != other.args[i]:
            #     return False
        return True       

    def unification(self, other):
        def unify(arg1, arg2, substitution):
            if substitution == False:
                return False
            if arg1 == arg2:
                return substitution
            if arg1.islower():
                return unifyVar(arg1, arg2, substitution)
            if arg2.islower():
                return unifyVar(arg2, arg1, substitution)
            return False

        def unifyVar(var, x, substitution):
            if var in substitution:
                return unify(substitution[var], x, substitution)
            if x in substitution:
                return unify(var, substitution[x], substitution)
            substitution[var] = x
            return substitution

        # 判断名字和正负
        if other.name != self.name or other.neg + self.neg != 1:
            return False
        
        # 看参数是否可以unify
        sub = {}
        for i in range(len(self.args)):
            sub = unify(self.args[i], other.args[i], sub)
            # print(sub)
            if sub == False:
                return False
        return sub
 
    def unification2(self, other):
        def unify(arg1, arg2, substitution):
            if substitution == False:
                return False
            if arg1 == arg2:
                return substitution
            if arg1.islower():
                return unifyVar(arg1, arg2, substitution)
            if arg2.islower():
                return unifyVar(arg2, arg1, substitution)
            return False

        def unifyVar(var, x, substitution):
            if var in substitution:
                return unify(substitution[var], x, substitution)
            if x in substitution:
                return unify(var, substitution[x], substitution)
            substitution[var] = x
            return substitution

        # 判断名字和正负
        if other.name != self.name or other.neg != self.neg:
            return False
        
        # 看参数是否可以unify
        sub = {}
        for i in range(len(self.args)):
            sub = unify(self.args[i], other.args[i], sub)
            # print(sub)
            if sub == False:
                return False
        return sub

    def __str__(self):
        return (str(self.neg) + " " + self.name + "(" +  ", ".join(self.args) + ")")
    
    def generalStr(self):
        new_args = copy.copy(self.args)
        for i in range(len(new_args)):
            if new_args[i].islower():
                new_args[i] = new_args[i][:new_args.index("@")]
        return (str(self.neg) + " " + self.name + "(" +  ", ".join(new_args) + ")")

    def variableNum(self):
        ans = set()
        for arg in self.args:
            if arg.islower():
                ans.add(arg)
        return len(ans)

    def moreGeneral(self, other):
        if self.name != other.name or self.neg != other.neg or self.variableNum() < other.variableNum():
            return False
        
        for i in range(len(self.args)):
            arg1 = self.args[i]
            arg2 = other.args[i]
            """
                arg1        arg2
                Constant    Variable    NO
                Constant    Constant    YES if equal / NO
                Variable    Constant    YES
                Variable    Variable    YES
            """
            if arg1.istitle() and arg2 != arg1:
                return False
        return True

            



class Sentence:
    def __init__(self):
        global idCreater
        idCreater += 1

        self.id = idCreater
        self.literals = []
        self.ancestors = set()
        
    def isEmpty(self):
        return (not self.literals)
    
    def __len__(self):
        return len(self.literals)
        
    def addLiteral(self, literal):
        self.literals.append(literal)

    def whichToResolve(self, other):
        for i in range(len(self.literals)):
            for j in range(len(other.literals)):
                literal1 = self.literals[i]
                literal2 = other.literals[j]
                sub = literal1.unification(literal2)
                if sub != False:
                    return (i, j, sub)
        return (-1, -1, False)

    def resolve(self, other):
        newSentence = Sentence()

        # # 做过resolve的不让他们再占用资源
        # if other.id in self.ancestors or self.id in other.ancestors or len(self.ancestors & other.ancestors) != 0:
        #     return newSentence, False

        idx1, idx2, sub = self.whichToResolve(other)
        
        if sub == False:
            return newSentence, False
        
        if len(self) == 1 and len(other) == 1:
            return newSentence, True # 产生了contradiction
        

        for i in list(range(idx1)) + list(range(idx1+1, len(self.literals))):
            newLiteral = self.getLiteral(i)
            newLiteral.changeArgs(sub, newSentence.id)
            newSentence.addLiteral(newLiteral)
        
        for i in list(range(idx2)) + list(range(idx2+1, len(other.literals))):
            newLiteral = other.getLiteral(i)
            newLiteral.changeArgs(sub, newSentence.id)
            newSentence.addLiteral(newLiteral)  
        # print (newSentence)

        newSentence.factorization()
        
        # 祖先
        # newSentence.ancestors = self.ancestors | other.ancestors
        # newSentence.ancestors.add(self.id)
        # newSentence.ancestors.add(other.id)
        
        return newSentence, False       

    def getLiteral(self, idx):
        l = self.literals[idx]
        return Literal(l.name, l.neg, copy.copy(l.args))
        
    def factorization(self):
        # 内部来个unification
        sub = False
        for i in range(len(self)-1):
            for j in range(i+1, len(self)):
                sub = self.literals[i].unification2(self.literals[j])
                if sub != False:
                    break
            if sub != False:
                break
        
        if sub == False:
            return 

        for literal in self.literals:
            for i in range(len(literal.args)):
                if literal.args[i] in sub:
                    literal.args[i] = sub[literal.args[i]]
        
        dropList = []
        uniqueLiteral = set()
        for i in range(len(self.literals)):
            literal = str(self.literals[i])
            if literal in uniqueLiteral:
                dropList.append(i)
            else:
                uniqueLiteral.add(literal)
        
        for idx in dropList[::-1]:
            del self.literals[idx]


    def convertStringToSentece(self, input_str):
        input_str = "".join(input_str.split())

        if "=>" in input_str:
            input_str = re.split("=>", input_str)
            premise = re.split("&", input_str[0])
            # print (premise)
            for predicate in premise:
                predicate = re.split(r"\s|\(|\)|,", predicate)[:-1]
                predName = predicate[0]
            
                neg = 0
                if predName[0] == "~":
                    neg = 1
                    predName = predName[1:]

                self.addLiteral(Literal(predName, neg, predicate[1:]).standardize(self.id))
                
            conclusion = re.split(r"\s|\(|\)|,", input_str[1])[:-1]
            neg = 1
            if conclusion[0][0] == "~":
                neg = 0
                conclusion[0] = conclusion[0][1:]

            self.addLiteral(Literal(conclusion[0], neg, conclusion[1:]).standardize(self.id))

        else:
            input_str = re.split(r"\s|\(|\)|,", input_str)[:-1]

            neg = 1
            predName = input_str[0]
            if predName[0] == "~":
                neg = 0
                predName = predName[1:]

            self.addLiteral(Literal(predName, neg, input_str[1:]).standardize(self.id))
        return self

    def __str__(self):
        res = "[" + str(self.id) + "]\t"
        for literal in self.literals:
            res += (str(literal) + " | ")
        return res 

    def contains(self, names):
        for literal in self.literals:
            if literal.name in names:
                return True
        return False

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self.literals[i] == other.literals[i]:
                continue
            else:
                return False
        return True

    def alwaysTrue(self):
        for i in range(len(self)-1):
            for j in range(i+1, len(self)):
                if self.literals[i].opposite(self.literals[j]):
                    return True
        return False

    def overlap(self, kb):
        for sentence in kb:
            if self == sentence:
                return True
        return False
    
    def subsumption(self, other):
        # self是不是比other更general
        for literal1 in self.literals:
            flag = False
            for literal2 in other.literals:
                if literal1.moreGeneral(literal2):
                    flag = True
                    break
            if not flag:
                return False
        return True

class KB:
    def __init__(self):
        self.sentences = []
        self.queries = []

    def addSentence(self, sentence):
        self.sentences.append(sentence)
    
    def addQuery(self, sentence):
        self.queries.append(sentence)

    def build(self, filename):
        file = open(filename)
        

        n_query = int(file.readline())
        for _ in range(n_query):
            input_str = file.readline()
            self.addQuery(Sentence().convertStringToSentece(input_str))

        n_kb = int(file.readline())
        for _ in range(n_kb):
            input_str = file.readline()
            newSentence = Sentence().convertStringToSentece(input_str)
            self.addSentence(newSentence)
            # if not newSentence.alwaysTrue():
            #     self.addSentence(newSentence)
            # else:
            #     print ("always true")
            #     print (newSentence)

    def __str__(self):
        res = ""
        # for query in self.queries:
        #     res += (str(query) + "\n")            
        
        for sentence in self.sentences:
            res += (str(sentence) + "\n")
        return res

    # def ASK(self, query):
    def getSentence(self, idx):
        return self.sentences[idx]
    
    def subsumption(self, newSentence, kb):
        for sentence in kb:
            if sentence.subsumption(newSentence):
                return True
        return False

    def run(self, filename = "output.txt"):
        fout = open(filename, "w")

        # 原始kb内部做resolution
        # new_sentences = []
        # for i in range(len(self.sentences)-1):
        #     # print (i, len(new_sentences))
        #     for j in range(i+1, len(self.sentences)):
        #         sentence1 = self.sentences[i]
        #         sentence2 = self.sentences[j]
        #         newSentence, contradiction = sentence1.resolve(sentence2)
                
        #         if contradiction: # 产生矛盾
        #             for _ in range(len(self.queries)):
        #                 fout.write("TRUE\n")
        #             fout.close()
        #             return
                
                # if not newSentence.isEmpty(): # 不能resolution
                #     new_sentences.append(newSentence)
        
        # print (len(self.sentences))
        # print (self)
        
        for query in self.queries:
            subKB = self.kbRelatedToQuery(query)
            # subKB.sentences = sorted(subKB.sentences, key=lambda x: len(x))
            # print ("===========")
            # print (query)
            # print (subKB)
            ans = self.ASK(query, subKB)
            if ans:
                fout.write("TRUE\n") # str(query) + 
            else:
                fout.write("FALSE\n") # str(query) + 
        fout.close()

    def ASK(self, query, kb): 
        def comp(x, y):
            if len(x) < len(y):
                return -1
            if len(x) == len(y):
                return 0
            else:
                return 1

        query.literals[0].neg = 1 - query.literals[0].neg # 取反
        new_sentences = [query]
        # kb.addSentence(query)
        
        for i in range(100):

            # print (i)
            new_new_sentences = []

            # kb 内部做resoluton
            # for i in range(len(kb.sentences)-1):
            #     for j in range(i+1, len(kb.sentences)):
            #         sentence1 = kb.sentences[i]
            #         sentence2 = kb.sentences[j]
            #         newSentence, contradiction = sentence1.resolve(sentence2)
            #         if contradiction: # 产生矛盾
            #             # print ("产生矛盾：")
            #             # print (sentence1)
            #             # print (sentence2)
            #             return True
            #         if not newSentence.isEmpty() and not newSentence.alwaysTrue() and not newSentence.overlap(new_new_sentences) and not newSentence.overlap(kb.sentences): # and not newSentence.overlap(new_sentences): # 不能resolution
            #             # print (newSentence, newSentence.overlap(new_new_sentences))
            #             new_new_sentences.append(newSentence)

            # kb和句子池 resolution
            for sentence1 in kb.sentences:
                for sentence2 in new_sentences:
                    # print ("kb-sentence: ", sentence1)
                    # print ("new-sentence: ", sentence2)
                    newSentence, contradiction = sentence1.resolve(sentence2)
                    # print ("resolve: ", newSentence, contradiction)
                    # print (str(sentence1.id) + "+" + str(sentence2.id) + "=>" + str(newSentence))

                    if contradiction: # 产生矛盾
                        # print ("contradiction!!!!: " + str(sentence1) + str(sentence2))
                        return True

                    # if newSentence.alwaysTrue():
                    #     print ("====== always true new sentence ======")
                    #     print (sentence1)
                    #     print (sentence2)
                    #     print (newSentence)
                    
                    # if newSentence.overlap
                    if not newSentence.isEmpty() and not self.subsumption(newSentence, kb.sentences) and \
                        not self.subsumption(newSentence, new_sentences) and \
                        not self.subsumption(newSentence, new_new_sentences):
                        # #not newSentence.alwaysTrue() and \not newSentence.overlap(new_new_sentences) and not newSentence.overlap(kb.sentences) and not newSentence.overlap(new_sentences): # 不能resolution
                        #print (newSentence)
                        # print ("========= new sentence ====== ")
                        # print (sentence1)
                        # print (sentence2)
                        # print (newSentence)
                        new_new_sentences.append(newSentence)

            # 句子池内部 resolution
            for i in range(len(new_sentences)-1):
                for j in range(i+1, len(new_sentences)):
                    sentence1 = new_sentences[i]
                    sentence2 = new_sentences[j]
                    newSentence, contradiction = sentence1.resolve(sentence2)
                    # print (str(sentence1.id) + "+" + str(sentence2.id) + "=>" + newSentence)
                    if contradiction: # 产生矛盾
                        # print ("contradiction!!!!: " + sentence1 + sentence2)
                        return True

                    # if newSentence.alwaysTrue():
                    #     print ("====== always true new sentence ======")
                    #     print (sentence1)
                    #     print (sentence2)
                    #     print (newSentence)

                    if not newSentence.isEmpty() and not self.subsumption(newSentence, kb.sentences) and \
                        not self.subsumption(newSentence, new_sentences) and \
                        not self.subsumption(newSentence, new_new_sentences):
                     #and not newSentence.overlap(new_new_sentences) and not newSentence.overlap(kb.sentences) and not newSentence.overlap(new_sentences): # 不能resolution
                        #print (newSentence)
                        # print ("========= new sentence ====== ")
                        # print (sentence1)
                        # print (sentence2)
                        # print (newSentence)
                        new_new_sentences.append(newSentence)
            
            # print ("new senctences")
            # for sentence in new_sentences:
            #     print (sentence)

            # print ("new new senctences")
            # for sentence in new_new_sentences:
            #     print (sentence)

            if not new_new_sentences: # 不能再产生新句子了
                # print ("no new sentence")
                # print (kb)
                return False
            
            # 句子池里的东西加到kb
            for sentence in new_sentences:
                kb.addSentence(sentence)
            #     kb.sentences = sorted(kb.sentences, key=lambda x: len(x))
            

            # # 新句子池变成句子池
            new_sentences = new_new_sentences
            # new_sentences = sorted(new_sentences, key=lambda x: len(x))
            # for sentence in new_new_sentences:
            #     kb.addSentence(sentence)

            # kb.sentences = sorted(kb.sentences, key=lambda x: len(x))
            
            # print ("=======")
            # for sentence in kb.sentences:
            #     print (sentence)
            # print ("\n")
            # for sentence in new_sentences:
            #     print (sentence)
        print ("iteration ended!!!!")
        return False     

    def copy(self):
        copykb = KB()
        for sentence in self.sentences:
            copykb.addSentence(sentence)
        return copykb
    
    def kbRelatedToQuery(self, query):
        """
        找到和当前query有关的语句
        """
        subKB = KB()
        names = set()
        names.add(query.literals[0].name)
        flag = True
        visited = set()
        while flag:
            #  (cnt)print
            # cnt += 1
            flag = False
            for sentence in self.sentences:
                if sentence.id not in visited and sentence.contains(names):
                    subKB.addSentence(sentence)
                    visited.add(sentence.id)
                    for literal in sentence.literals:
                        names.add(literal.name)
                    flag = True
        return subKB
                    
                

if __name__ == "__main__":
    # import os
    # path = "./testcase"
    # files= os.listdir(path) 
    # print (files)

    # for filename in files:
    #     if filename[:5] != "input":
    #         continue
    #     print ("======================================")
    #     print ("filename:" + filename)
    #     fin = path + "/" + filename
    #     fout = "output/output" + filename[5:]
    #     print (fout)

    #     kb = KB()
    #     kb.build(fin)
    #     kb.run(fout)
    fin = "input49.txt"
    fout = "output49.txt"
    kb = KB()
    kb.build(fin)
    kb.run(fout)
    # print (idCreater)
    
    # s1 = Sentence()
    # s1.addLiteral(Literal('P', 1, ['A','x@1']))
    # s1.addLiteral(Literal('Q', 1, ['B', 'C']))
    # s2 = Sentence()
    # s2.addLiteral(Literal('P', 1, ['A', 'y@1']))
    # s2.addLiteral(Literal('Q', 1, ['B', 'A']))
    # s2.addLiteral(Literal('M', 1, ['B', 'A']))
    # print (s1.subsumption(s2))

    # s1.addLiteral(Literal('Ancestor2', 1, ['Liz', 'Joe']))
    
    # # # s1.addLiteral(Literal('B210', 1, ['x@200']))
    # # # s1.addLiteral(Literal('P210', 1, ['x@200']))
    # # print (Literal('A210', 0, ['x@200']) == Literal('A210', 0, ['x@200']))
    # s2 = Sentence()
    # s2.addLiteral(Literal('Ancestor2', 0, ['x', 'y']))
    # s2.addLiteral(Literal('Parent2', 1, ['x', 'y']))
    # # s2.addLiteral(Literal('A210', 0, ['Alice']))

    # # print (s1 == s2)
    # #print (s1.alwaysTrue())
    # # # s2.addLiteral(Literal('B210', 0, ['x@201']))
    # # print (s1.overlap([s2]))
    # print (s1)
    # print (s2)

    # s3, res = s1.resolve(s2)
    # print (s3, res)
    


    
        
        

    

    

    

     
    