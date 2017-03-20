import sys
import os

# pid,arrival_time,burst_time

def get_data():
    file_path = os.getcwd() + "/" + sys.argv[1]
    print("file path is " + file_path)
    data = []
    try:
        with open(file_path,'rb') as file:
            for line in file:
                d = line.split()
                for w in range(len(d)):
                    d[w] = int(d[w])
                data.append(d)
    except IOError as msg:
        msg = "\n'{0}' cannot be read: {1}\n".format(file_path,msg)
        print(msg)
    return data

'''
def FCFS(data):

s
def RR(data,time_quantum):


def SJF(data):

'''


def runner():
    print(sys.argv)

    if len(sys.argv) == 3:
        if sys.argv[2] == 'FCFS':
            

        elif sys.argv[2] == 'SJF':


        else:
            print("Unknow algorithm name")

    elif len(sys.argv) == 4 and sys.argv[2] == 'RR':


    else:
        print("wrong input argument!")




get_data()
