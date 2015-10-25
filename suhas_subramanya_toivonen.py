__author__ = 'suhas subramanya'
import sys
import random
import itertools

def toivonenMain():
    filename=sys.argv[1]
    fil = open(filename, 'r')
    support=int(sys.argv[2])
    randomsamplerate=50
    linecount=0
    contentlist=[]
    for line in fil:
        linecount=linecount+1
        contentlist.append(line)
    fil.seek(0,0)
    randomContent=randomimputsample(contentlist,linecount,randomsamplerate)
    finallist=[]
    finallist=findfrequentitems(filename,randomContent,support,randomsamplerate,linecount,contentlist,finallist)
    print finallist[1]
    print randomsamplerate/100.0
    for each in finallist[0]:
        print each
        print ""

def findcandidateitemsetsforpairsandmore(randomcontentList,candidateitemset,k):
    tempcandidateitemset={}
    for eachcandidate in candidateitemset:
        for eachline in randomcontentList:
            lst=[]
            splittransaction=sorted(eachline.split(","))
            for each in splittransaction:
                each=each.rstrip("\n")
                lst.append(each)
            itemset=generateitemsets(lst,k)
            itemset.sort()
            for each in itemset:
                if cmp(list(eachcandidate),each)==0:
                    v=tuple(eachcandidate)
                    if tempcandidateitemset.__contains__(v):
                        value=tempcandidateitemset.get(v)
                        value=value+1
                        tempcandidateitemset[v]=value
                    else:
                        tempcandidateitemset[v]=1
                        break;
    return tempcandidateitemset


def findfrequentitems(filename,randomcontentList,support,randomsamplerate,linecount,contentlist,finallist):
    k=1
    truelyfrequentitemset=[]
    loopcount=1
    while True:
        if k==1:
            reducedsupport=support*0.9*(randomsamplerate/100.0)
            candidateitemset=findcandidateitemsets(randomcontentList,k)
        else:
            candidateitemset=findcandidateitemsetsforpairsandmore(randomcontentList,candidateitemset,k)
        candidatefrequentitemset=findcandidatefrequentitemsets(candidateitemset,reducedsupport,k)
        tempcandidateset=candidateitemset
        sorted(tempcandidateset)
        candidateitemset=[]
        flag=0
        for each in tempcandidateset:
            flag=0
            for eachitem in candidateitemset:
                if frozenset(eachitem)==each:
                    flag=1
                    break
            if flag!=1:
                candidateitemset.append(sorted(list(each)))
            candidateitemset.sort()
            sorted(candidateitemset)
        if k!=1:
            negativeborderlist=findnegativeBorder(candidatefrequentitemset,candidateitemset,truelyfrequentitemset,k-1)

        else:
            candidatefrequentitemset=candidatefrequentitemset
            negativeborderlist=[]

            for eachitem in candidateitemset:
                flag=0
                for each in candidatefrequentitemset:
                    if(cmp(each,eachitem)==0):
                        flag=1
                        break
                if flag==0:
                    negativeborderlist.append(eachitem)
        truelyfrequentitemset=findtruefrequentitemset(filename,candidatefrequentitemset,negativeborderlist,k,support)
        if truelyfrequentitemset[0]==True:
            k=k+1
            if truelyfrequentitemset[1].__len__()==0:
                break
            '''print truelyfrequentitemset[1]'''
            finallist.append(truelyfrequentitemset[1])
            candidateitemset=generatefrequentitemsetfromcandidate(truelyfrequentitemset[1],k)
        else:
            k=1
            loopcount+=1
            for each in finallist:
                finallist.remove(each)
            randomcontentList=randomimputsample(contentlist,linecount,randomsamplerate)
    return finallist,loopcount

def findnegativeBorder(candidatefrequentitemset,candidateitemset,truelyfrequentitemset,k):
    negativeborderlist=[]
    for eachitem in candidateitemset:
        flag=0
        for each in candidatefrequentitemset:
            if(cmp(each,eachitem)==0):
                flag=1
                break
        if flag==0:
            negativeborderlist.append(eachitem)
    truenegativeborder=[]
    for each in negativeborderlist:
        itemset=generateitemsets(each,k)
        count=0
        itemcount=len(itemset)
        for eachfrequent in itemset:

            for eachtrue in truelyfrequentitemset[1]:
                if cmp(eachfrequent,eachtrue)==0:
                    count+=1
        if itemcount==count:
            truenegativeborder.append(each)
    return truenegativeborder



def generatefrequentitemsetfromcandidate(truelyfrequentitemset,k):
    candidateitemdictionary={}
    for each in truelyfrequentitemset:
        for eachitem in generateitemsets(each,1):
            if not candidateitemdictionary.__contains__(eachitem[0]):
                candidateitemdictionary[eachitem[0]]=1
    candidateitemset=[]
    for key,value in candidateitemdictionary.iteritems():
        candidateitemset.append(key)
    candidateitemset.sort()
    candidateitemset=generateitemsets(candidateitemset,k)
    return  candidateitemset


def findtruefrequentitemset(filename,candidatefrequentitemset,negativeborderlist,k,support):
    fil = open(filename, 'r')
    tuplelist=[]
    tuplelistwithcount=[]
    actualtuplelist=[]
    for line in fil:
        lst=[]
        splittransaction=sorted(line.split(","))
        for each in splittransaction:
            each=each.rstrip("\n")
            lst.append(each)
        itemset=generateitemsets(lst,k)
        for each in itemset:
            if k==1:
                tuplelist.append(sorted(each[0]))
            else:
                tuplelist.append(sorted(each))
    sorted(tuplelist)
    tuplelist.sort()
    truelyfrequentlist=[]
    for eacgnegative in negativeborderlist:
        for each in tuplelist:
            if(cmp(each,eacgnegative)==0):
                tuplelistwithcount.append(eacgnegative)
                break

    for eachnegative in tuplelistwithcount:
        count=0
        for each in tuplelist:
            if cmp(each,eachnegative)==0:
                count+=1
                if count>=support:
                    return False,truelyfrequentlist

    tuplelistwithcount=[]

    for eachfrequent in candidatefrequentitemset:
        for each in tuplelist:
            if(cmp(each,eachfrequent)==0):
                tuplelistwithcount.append(eachfrequent)
                break

    for eachfrequent in tuplelistwithcount:
        count=0
        for each in tuplelist:
            if cmp(each,eachfrequent)==0:
                count+=1
                if count>=support:
                    truelyfrequentlist.append(eachfrequent)
    intermediate=truelyfrequentlist
    truelyfrequentlist=[]

    for eachitem in intermediate:
        flag=0
        for each in truelyfrequentlist:
            if(cmp(each,eachitem)==0):
                flag=1
                break
        if flag==0:
            truelyfrequentlist.append(eachitem)

    return True,truelyfrequentlist


def generatetuples(filename,k):
    fil = open(filename, 'r')
    tuplelist=[]
    for line in fil:
        lst=[]
        splittransaction=sorted(line.split(","))
        for each in splittransaction:
            each=each.rstrip("\n")
            lst.append(each)
        itemset=generateitemsets(lst,k)
        for each in itemset:
            tuplelist.append(sorted(each))
    tuplelist.sort()
    return tuplelist







def findcandidatefrequentitemsets(candidateitemset,reducedsupport,k):
    candidatefrquentitemset=[]
    intermediatecandidatefrequentitemset=[]
    finalfrequentitemset=[]
    for key,value in candidateitemset.iteritems():
        if value>=reducedsupport:
            intermediatecandidatefrequentitemset.append(list(key))

    intermediatecandidatefrequentitemset.sort()
    list(intermediatecandidatefrequentitemset)
    sorted(intermediatecandidatefrequentitemset)
    for eachtuple in intermediatecandidatefrequentitemset:
        flag=0
        for each in finalfrequentitemset:
            if eachtuple==each:
                flag=1
                break
        if flag!=1:
            finalfrequentitemset.append(eachtuple)
    return finalfrequentitemset

def findcandidateitemsets(randomcontentlist,k):
    tuplelist={}
    for eachline in randomcontentlist:
        lst=[]
        splittransaction=sorted(eachline.split(","))
        for each in splittransaction:
            each=each.rstrip("\n")
            lst.append(each)
        itemset=generateitemsets(lst,k)
        itemset.sort()
        for each in itemset:
            v=frozenset(each)
            if tuplelist.__contains__(v):
                value=tuplelist.get(v)
                value=value+1
                tuplelist[v]=value
            else:
                tuplelist[v]=1
    sorted(tuplelist)
    return tuplelist


def generateitemsets(lists,k):
    lst=[list(x) for x in itertools.combinations(lists, k)]
    return lst



def randomimputsample(contentList,linecount,randomsamplerate):
    samplecount=linecount*(randomsamplerate/100.0)
    samplecount=int(samplecount)
    randomlinenumers={}
    randomContent=[]
    while(samplecount>0):
        randomnum=random.randint(0,linecount-1)

        if randomlinenumers.__contains__(randomnum):
            continue
        else:
            samplecount=samplecount-1
            randomContent.append(contentList[randomnum])
            randomlinenumers[randomnum]=1
    return randomContent


toivonenMain()







