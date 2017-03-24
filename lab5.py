import sys
import os

# pid,arrival_time,burst_time
# [[4], [0, 0, 12], [1, 2, 4], [2, 3, 1], [3, 4, 2]]

data = []
process_data = []
arrived = []

def get_data():
    file_path = os.getcwd() + "/" + sys.argv[1]
    print("file path is " + file_path)
    try:
        with open(file_path,'rb') as file:
            for line in file:
                d = line.split()
                for w in range(len(d)):
                    d[w] = int(d[w])
                d.append('False')
                data.append(d)
            data.pop(0)
    except IOError as msg:
        msg = "\n'{0}' cannot be read: {1}\n".format(file_path,msg)
        print(msg)
        exit()
    return data

def checkArrive(currentTime):
    for process in data:
        if process[1] <= currentTime and process[3] == 'False':
            process[3] = 'True'
            arrived.append(process)

def sortData(data,index):
    largest = -1
    print("data is ")
    print(data)
    sort_data = []
    for d in range(0,len(data)):
        if data[d][index] > largest:
            largest = data[d][index]
            sort_data.append(data[d])
        else:
            find = False
            for w in range(len(sort_data)):
                if data[d][index] < sort_data[w][index] and find == False:
                    sort_data.insert(w,data[d])
                    find = True
    print(sort_data)
    return sort_data

def toString(outPut, averageWait):
    string = '\nPID  ArrivalTime  StartTime  EndTime  Runningtime  WaitingTime\n'
    for info in outPut:
        for num in info:
            string = string + str(num) + '         '
        string = string + '\n'
    string = string + "Average Waiting Time : %f \n"%(averageWait)
    return string

def FCFS(data):
    # sort based on arrival_time
    process_data = sortData(data,1)
    output_data = []
    startTime = 0
    endTime = 0
    totalWaitTime = 0

    for d in process_data:
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

    return toString(output_data,totalWaitTime/len(data))


'''
s
def RR(data,time_quantum):
    
'''

def SJF(data):
    process_data = sortData(data,1)
    startTime = 0
    endTime = 0
    totalWaitTime = 0.0
    output_data = []
    count = 0
    while(count < len(process_data)):
        checkArrive(startTime)
        tmp_arrived = sortData(arrived, 2)
        tmp_output = []
        endTime = startTime + tmp_arrived[0][2]
        waitingTime = startTime - tmp_arrived[0][1]
        tmp_output.append(tmp_arrived[0][0]) # pid
        tmp_output.append(tmp_arrived[0][1]) # arrivalTime
        tmp_output.append(startTime) 
        tmp_output.append(endTime)
        tmp_output.append(tmp_arrived[0][2]) # burstTime
        tmp_output.append(waitingTime)
        output_data.append(tmp_output)
        startTime = endTime
        pop_arrive(tmp_arrived.pop(0))      
        count = count + 1
        totalWaitTime = totalWaitTime + waitingTime
    return toString(output_data, totalWaitTime/len(data))


def pop_arrive(content):
    index = 0
    for d in range(len(arrived)):
        if arrived[d] == content:
            index = d
    arrived.pop(index)


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
