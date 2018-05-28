#by month from 2013-2018 ,injured+killed
import csv
import numpy as np
import matplotlib.pyplot as plt


#by month ,line
gundict={}
#by state, pie
statedict={}
def linegraph(setdict):
    x=[1,2,3,4,5,6,7,8,9,10,11,12]
    a=[setdict[2018][0],setdict[2018][1],setdict[2018][2]]
    plt.figure(figsize=(8,4))
    plt.plot(x,setdict[2013],color='green',label='2013')
    plt.plot(x,setdict[2014],color='black',label='2014')
    plt.plot(x, setdict[2015], color='red', label='2015')
    plt.plot(x, setdict[2016], color='blue', label='2016')
    plt.plot(x, setdict[2017], color='skyblue', label='2017')
    plt.plot([1,2,3], a, color='yellow', label='2018')
    plt.legend()

    plt.xlabel("month from Jan. to Dec.")
    plt.ylabel("the number of injured and killed people")
    #plt.show()
    plt.savefig("bymonth.png")
    plt.show()

def piegraph(ll):
    labels=[]
    sizes=[]
    colors=['red','yellow','blue','green','skyblue']
    for x in ll:
        labels.append(x[0])
        sizes.append(x[1])

    explode=(0.1,0.05,0,0,0)
    plt.axes(aspect=1)
    plt.pie(sizes, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=True, labeldistance=1.1, startangle=90, pctdistance=0.6
            )
    plt.legend(loc=[0.9,0.6])
    plt.title("top 5 states and their property")
    plt.savefig("bystate.png")
    plt.show()

def bargraph():
    pass



def search_by_month():
    global gundict
    incidentamount={}
    gun_filename = 'gun-violence-data_01-2013_03-2018.csv'
    path_name = '/Users/xilanyuan/Desktop/9321 ass3/'
    csvfile= open(path_name+gun_filename,"r")
    reader=csv.reader(csvfile)
    for item in reader:
        if reader.line_num==1:
            continue
        #print(item[1],item[5],item[6])
        if item[1] not in gundict.keys():
            gundict[item[1]]=[int(item[5]),int(item[6])]
            #print(item[1],gundict[item[1]])
        else:
            a = int(item[5])
            b = int(item[6])
            gundict[item[1]][0]+=a
            gundict[item[1]][1]+=b
        m=item[1][:7]
        if m not in incidentamount.keys():
            incidentamount[m] = 1
        else:
            incidentamount[m] += 1

            #print('aaaaaaa',item[1],gundict[item[1]])
        # if reader.line_num==20:
        #     break
    #print(gundict)
    print(incidentamount)
    bymonth={}
    for x in gundict.keys():
        c=x[:7]
        #print('c',c)
        if c not in bymonth.keys():
            bymonth[c]=gundict[x]
            #incidentamount[c]=1
        else:
            bymonth[c][0]+=gundict[x][0]
            bymonth[c][1] += gundict[x][1]
            #incidentamount[c]+=1
        #print(c,bymonth[c])
    print(bymonth)
    #print(incidentamount)
    year=[2013,2014,2015,2016,2017,2018]
    month = ['01', '02', '03', '04','05', '06', '07', '08','09', '10', '11', '12']
    ymdict={}
    inciym={}

    for element in year:
        ll=[]
        nn=[]
        print('111111111111')
        for e in range(12):
            for y in bymonth.keys():
                #print('keys:',y)
                if y[0:4]==str(element) and y[5:7]==month[e] :
                    d=bymonth[y][0]+bymonth[y][1]
                    #print(d)
                    ll.append(d)
            for n in incidentamount.keys():
                #print('keys:',n)
                if n[0:4] == str(element) and n[5:7] == month[e]:
                    #print(incidentamount[n])
                    nn.append(incidentamount[n])
                    print(nn)

        inciym[element]=nn
        #print('ll:',ll)
        ymdict[element]=ll
    print(inciym)
    print(ymdict)
    linegraph(inciym)

def state():
    global statedict
    gun_filename = 'gun-violence-data_01-2013_03-2018.csv'
    path_name = '/Users/xilanyuan/Desktop/9321 ass3/'
    csvfile = open(path_name + gun_filename, "r")
    reader = csv.reader(csvfile)
    for item in reader:
        #print(item)
        if reader.line_num==1:
            continue
        if item[2] not in statedict.keys():
            statedict[item[2]]=int(item[5])+int(item[6])
        else:
            statedict[item[2]]+=int(item[5])+int(item[6])
    #print(statedict)
    statedict=sorted(statedict.items(),key=lambda item:item[1])
    #print(statedict)
    num=0
    for x in statedict:
        num+=x[1]
    #print('sum:',num)
    top5=[statedict[-1],statedict[-2],statedict[-3],statedict[-4],statedict[-5]]
    print(top5)
    part_num=0
    for y in top5:
        part_num+=y[1]
    toprate=[]
    for y in top5:
        z=y[1]/part_num*100
        toprate.append([y[0],z])
    print(toprate)
    #piegraph(toprate)

def gender():
    year=[[17,2017],[16,2016],[15,2015],[14,2014],[13,2013]]
    gt=[['M','Male'],['F','Female'],['Unknown']]
    gendercount={}
    genderamount={}
    gun_filename = 'Mass Shootings Dataset Ver 5.csv'
    path_name = '/Users/xilanyuan/Desktop/9321 ass3/'
    #with open(path_name ,'rb') as f:
     #   read=csv.reader(f)
    csvfile = open(path_name + gun_filename, 'rt',encoding="ISO-8859-1")
    reader = csv.reader(csvfile)
    # print("11111111")
    for item in reader:
        #print('2222222')
        #print(item)
        if reader.line_num==1:
            continue
        #print(item[3])
        a=item[3].split('/')
        #print(a)
        for y in year:
            if int(a[2]) in y:
                if int(a[2]) not in gendercount.keys():
                    gendercount[int(a[2])]=[0,0,0]
                #print(item[18])
                flag=0
                for i in range(3):
                    if item[18] in gt[i]:
                        gendercount[int(a[2])][i]+=1
                        #print('1111111',a[2],i,gendercount[int(a[2])])
                        flag=1
                        break
                if flag==0:
                    gendercount[int(a[2])][0] += 1
                    gendercount[int(a[2])][1] += 1
                    #print('22222222', a[2], gendercount[int(a[2])])


    #print(gendercount)
    genderamount={2017:[0,0,0],2016:[0,0,0],2015:[0,0,0],2014:[0,0,0],2013:[0,0,0]}
    for j in gendercount.keys():
        for m in year:
            if j in m:
                genderamount[m[1]][0]+=gendercount[j][0]
                genderamount[m[1]][1] += gendercount[j][1]
                genderamount[m[1]][2] += gendercount[j][2]
    print(genderamount)



if __name__ == '__main__':

    search_by_month()
    #state()
#gender()

