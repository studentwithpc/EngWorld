import pandas as pd
import random as rm
import numpy as np
debug=False

def read_file(path):
    df=pd.read_csv(path,  usecols=["eng_word","rus_word", "status"])
    return df

def count_knowledge(frame, key="done"):
    kn=np.count_nonzero(frame.status==key)
    return kn

def learn_mode(frame):

    num=rm.randint(0,len(frame)-1)
    if frame.status[num]=="done":
        learn_mode(frame)
    else:
        print("New word :\n\n")
        print(frame.eng_word[num])#, " - ", frame.rus_word[num])
        ans = input("\n\nDo you know this word? y/n\n")
        if ans == "y":
            print("\n\n - ", frame.rus_word[num])
            ans=input("\n\nAre you sure?\n")
            if ans=="y":
                frame.status[num] = "done"
            else:
                frame.status[num] = "learning"
        else:
            print("\n\n - ",frame.eng_word[num]," - ", frame.rus_word[num],"\n\n")
            frame.status[num] = "learning"


def start(path):
    frame = read_file(path)

    learn_mode(frame)
    frame.to_csv(path, index=False)
    return (count_knowledge(frame), count_knowledge(frame,"learning"))

if __name__== "__main__":
    path="./words/res_merge.csv"
    count= 0
    kn, pr=0,0
    if not(debug):
        ans = input("Do you want to start  learning? y/n\n")
    else:
        ans = "y"
    while True:

        #TODO: base of answers
        if ans=="n":
            break
        elif ans=="y":
            kn,pr=start(path)
            count+=1
            print(" In this session you learn {} words".format(count))

        else:
            print("I'm sorry. I don't understand.")
        ans = input("Do you want to continue? y/n\n")

    print("Your status:\n You know {} words.\n In process {} words".format(kn,pr))
    print("You know {} % printing words".format(round(kn/(kn+pr)*100)))
    if count >5:
        print("Good work! See you leter!")
    else:
        print ("You are so lasy today! Goodbye!")
