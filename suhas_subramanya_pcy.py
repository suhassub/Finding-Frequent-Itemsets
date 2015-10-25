__author__ = 'suhas subramanya'
import sys
import itertools

def pcyMain():
    filename=sys.argv[1]
    fil = open(filename, 'r')
    support=int(sys.argv[2])
    bucket=int(sys.argv[3])
    dictionaryofitems={}
    splittransaction=''
    itemArray={}
    finalfrequentitemset=[]
    position=0
    for line in fil:
        splittransaction=line.split(",")
        for each in splittransaction:
            each=each.rstrip("\n")
            if not dictionaryofitems.__contains__(each):
                position+=1
                dictionaryofitems[each]=position
            if itemArray.__contains__(each):
                count=itemArray.get(each)
                count+=1
                itemArray[each]=count
            else:
                itemArray[each]=1
    for key,value in itemArray.iteritems():
        if value>=support:
            finalfrequentitemset.append([key,value])
    finalfrequentitemset.sort()
    printablefrequent=[]
    for each in finalfrequentitemset:
        printablefrequent.append(each[0])
    print printablefrequent
    findcandidateitemsets(filename,finalfrequentitemset,dictionaryofitems,support,bucket)



def findcandidateitemsets(filename,frequentItemSet,dictionaryofitems,support,bucket):
    k=2
    while True:
        print ""
        print ""

        tuplelist=generatetuples(filename,k)

        hashbucketmapping={}
        hashbucketcount={}
        tuplelist.sort()
        for each in tuplelist:
            sums=0
            for eachitem in each:
                sums+=dictionaryofitems[eachitem]
            value=sums%bucket
            if hashbucketmapping.__contains__(value):
                lst=hashbucketmapping[value]
                lst.append(each)
                hashbucketmapping[value]=lst
            else:
                hashbucketmapping[value]=[each]
            if hashbucketcount.__contains__(sums%bucket):
                count=hashbucketcount[(sums%bucket)]
                hashbucketcount[(sums%bucket)]=count+1
            else:
                hashbucketcount[(sums%bucket)]=1
        bitmap=generatebitMaps(bucket,support,hashbucketcount)


        candidateitemsets=[]
        for each in tuplelist:
            reduceditemsets=generateitemsets(each,k-1)

            flag=0
            for eachitem in reduceditemsets:
                if k==2:
                    eachitem=eachitem[0]
                flag2=0
                for eachfrequent in frequentItemSet:
                    if k==2:
                        if eachfrequent[0].__contains__(eachitem):
                            flag2=1
                            break
                    else:
                        listtotuplereduced=list(eachitem)
                        if cmp(eachfrequent[0],listtotuplereduced)==0:
                            flag2=1
                            break
                if flag2==0:
                    break
                else:
                    flag=1
            if flag==1 and flag2==1:
                for key,value in hashbucketmapping.iteritems():
                    if value.__contains__(each):
                        sums=key
                        break
                if bitmap[sums]==1:
                    candidateitemsets.append(each)

        candidateitemsets.sort()
        frequentItemSet=[]
        frequentitemscount=[]

        for each in tuplelist:
            if candidateitemsets.__contains__(each):
                flag=0
                for eachfrequent in frequentItemSet:
                    if cmp(eachfrequent[0],each)==0:
                        count=eachfrequent[1]
                        eachfrequent[1]=count+1
                        flag=1
                        break;
                if flag==0:
                    frequentItemSet.append([each,1])
        tempfreqitemset=frequentItemSet
        frequentItemSet=[]
        for each in tempfreqitemset:
            if each[1]>=support:
                frequentItemSet.append(each)

        k+=1
        if frequentItemSet.__len__()==0:
            break
        print hashbucketcount
        printablefrequent=[]
        for each in frequentItemSet:
            printablefrequent.append(each[0])
        print printablefrequent



def generatebitMaps(bucket,support,hashbucketcount):
    bitmap=[]
    for i in range(0,bucket):
        bitmap.append(0)
    for key,value in hashbucketcount.iteritems():
        if value>=support:
            bitmap[key]=1
    return bitmap


def generateitemsets(lists,k):
    lst=[list(x) for x in itertools.combinations(lists, k)]
    return lst


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


pcyMain()