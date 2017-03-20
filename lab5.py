import sys
import os

# pid,arrival_time,burst_time
# [[4], [0, 0, 12], [1, 2, 4], [2, 3, 1], [3, 4, 2]]

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
        exit()
    return data

def sortData(data,index):
    tmp_data = []
    largest = -1
    for d in range(1,data[0][0]+1):

        if data[d][index] > largest:
            largest = data[d][index]
            tmp_data.append(data[d])
        else:
            find = False
            for w in range(len(tmp_data)):
                if data[d][index] < tmp_data[w][index] and find == False:
                    tmp_data.insert(w,data[d])
                    find = True
    print(tmp_data)
    return tmp_data

def toString(outPut, averageWait):
    string = '\nPID  ArrivalTime  StartTime  EndTime  Runningtime  WaitingTime\n'
    for info in outPut:
        for num in info:
            string = string + str(num) + '         '
        string = string + '\n'
    string = string + "Average Waiting Time : %d \n"%(averageWait)
    return string

def FCFS(data):
    # sort based on arrival_time
    tmp_data = sortData(data,1)

    output_data = []
    startTime = 0
    endTime = 0
    totalWaitTime = 0

    for d in tmp_data:
        tmp_output = []
        endTime = startTime + d[2] # end = start + burst_Time
        waitingTime = startTime - d[1] # wait_time = start - arrival_Time
        tmp_output.append(d[0])
        tmp_output.append(d[1])
        tmp_output.append(startTime)
        tmp_output.append(endTime)
        tmp_output.append(d[2])
        tmp_output.append(waitingTime)  
        output_data.append(tmp_output)
        totalWaitTime = totalWaitTime + waitingTime # record total wait time
        startTime = endTime # update start time to end time   

    return toString(output_data,totalWaitTime/data[0][0])


'''
s
def RR(data,time_quantum):
    
'''

def SJF(data):

    tmp_data = sortData(data,2)




def runner():

    if len(sys.argv) == 3:
        if sys.argv[2] == 'FCFS':
            data = get_data()
            outPut = FCFS(data)            
            print(outPut)

        elif sys.argv[2] == 'SJF':
            data = get_data()
            outPut = SJF(data)            
            print(outPut)

        else:
            print("Unknow algorithm name")

    elif len(sys.argv) == 4 and sys.argv[2] == 'RR':
        print("")

    else:
        print("wrong input argument!")


if __name__ == '__main__':
    runner()
