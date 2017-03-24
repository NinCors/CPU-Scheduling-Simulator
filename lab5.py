import sys
import os

# pid,arrival_time,burst_time
# [[4], [0, 0, 12], [1, 2, 4], [2, 3, 1], [3, 4, 2]]

data = []
process_data = []
arrived = []
s1 = '\nPID  ArrivalTime  StartTime  EndTime  Runningtime  WaitingTime\n'
s2 = '\nPID  StartTIme  EndTime  RunningTime\n'
s3 = '\nPID  ArrivalTime  RunningTime  EndTime  WaitingTime\n '


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

def checkArrive(data, currentTime):
    print("current data is")
    print(data)
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

def toString(outPut, averageWait,string):
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

    return toString(output_data,totalWaitTime/len(data),s1)



def RR(data):
    quantum = int(sys.argv[3])
    
    startTime = 0
    endTime = 0
    
    output1 = []# pid startT endT runningT
    output2 = sortData(data,1)# pid arrivalT runningT EndT WaitT

    tmp_d = []
    count = len(data)
    print("\nBEGIN!!\n")
    while(count > 0):
        tmp_output = []
        checkArrive(data, startTime)
        # if the last one is not finished, then append it in the end
        if len(tmp_d) != 0:
            arrived.append(tmp_d)
      
        print("Arrival is ")
        print(arrived)
        # if burst time - start time bigger than quantum, then endtime = start + quantum
        # runningtime = end - start
        tmp_output.append(arrived[0][0])# pid
        tmp_output.append(startTime)
        if arrived[0][2] > quantum:
            endTime = startTime + quantum
            arrived[0][2] = arrived[0][2] - quantum # update the left running time
            # Not finished for this one, move to the end of query
            tmp_d = []
            for w in arrived[0]:
                tmp_d.append(w)
            arrived.pop(0)

        else:
            endTime = arrived[0][2] + startTime
            insertValue(arrived[0][0],endTime,output2)
            count = count - 1
            tmp_d = []
            arrived.pop(0)
        runningTime = endTime - startTime
        print("In this round %d, start is %d, end is %d, quanTum is %d\n"%(count,startTime,endTime,quantum))
        tmp_output.append(endTime)
        tmp_output.append(runningTime)
        output1.append(tmp_output)
        startTime = endTime

    totalWait = 0.0
    for d in output2:
        totalWait = totalWait + d[4]
    averageW = totalWait/len(output2)

    return toString(output1,-1,s2),toString(output2,averageW,s3)

def insertValue(pid,endTime,output):
    for d in output:
        if d[0] == pid:
            d.pop()
            d.append(endTime)
            waitingTime = endTime - d[2] - d[1]
            d.append(waitingTime)

def SJF(data):
    process_data = sortData(data,1)
    startTime = 0
    endTime = 0
    totalWaitTime = 0.0
    output_data = []
    count = 0
    while(count < len(process_data)):
        checkArrive(data, startTime)
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
    return toString(output_data, totalWaitTime/len(data),s1)


def pop_arrive(content):
    index = 0
    for d in range(len(arrived)):
        if arrived[d] == content:
            index = d
    arrived.pop(index)


def runner():
    print(sys.argv)
    if len(sys.argv) == 3:
        if sys.argv[2] == 'FCFS':
            data1 = get_data()
            data = sortData(data1,1)
            outPut = FCFS(data)            
            print(outPut)

        elif sys.argv[2] == 'SJF':
            data1 = get_data()
            data = sortData(data1,1)           
            outPut = SJF(data)            
            print(outPut)

        else:
            print("Unknow algorithm name")

    elif len(sys.argv) == 4 and sys.argv[2] == 'RR':
        data1 = get_data()
        data = sortData(data1,1)
        outPut = RR(data)
        print(outPut)

    else:
        print("wrong input argument!")


if __name__ == '__main__':
    runner()
