import pandas as pd
import random as rm
import numpy as np

debug=False
users_path = "./user_info/users.csv"
last_user_path="./user_info/last.csv"
class AdventureDone(Exception): pass

def read_file(path):
    df=pd.read_csv(path)
    return df

def count_knowledge(frame, key="done"):
    kn=np.count_nonzero(frame.status==key)
    return kn

def first_test_mode(frame):

    num=rm.randint(0,len(frame)-1)
    while frame.status[num]=="done" or frame.status[num]=="learning":
         print("repeat", num)
         num=rm.randint(0,len(frame)-1)

    print("New word :\n\n")
    print(frame.eng_word[num])  # , " - ", frame.rus_word[num])
    ans = input("\n\nDo you know this word? y/n\n")
    if ans == "y":
        print("\n\n - ", frame.rus_word[num])
        ans = input("\n\nAre you sure?\n")
        if ans == "y":
            frame.status[num] = "done"
        else:
            frame.status[num] = "learning"
    else:
        print("\n\n - ", frame.eng_word[num], " - ", frame.rus_word[num], "\n\n")
        frame.status[num] = "learning"


def start(path):
    frame = read_file(path)

    first_test_mode(frame)
    frame.to_csv(path, index=False)
    return (count_knowledge(frame), count_knowledge(frame,"learning"),len(frame)-1)

def standart_question(info, mode=0):
    ans = input(info + " y/n\n")
    if ans == "n":
        # TODO: base of answers
        if mode==0:
            raise AdventureDone
        else:
            return False
    elif ans=="y":
        return True
    else:
        if mode == 0:
            print("I'm sorry. I don't understand.")
        return False

def update_users_info(users_path,last_user_id):

    users = read_file(users_path)
    id_list = users["id"].tolist()
    name_list = users["name"].tolist()
    user = users.loc[users["id"] == int(last_user_id)]
    name = user["name"].item()
    path = ("./words/" + user["words_file"].item())
    return (users,id_list,name_list,name,path)


def add_new_user(users):
    new_name =choose_user(name_list)
    new_id = id_list[-1] + 1

    path = "./words/res.csv"
    df = read_file(path)
    path = path[:-4] + str(new_id) + path[-4:]
    df.to_csv(path, index=False)
    new_path = path[8:]
    new_user = pd.DataFrame([[new_id, new_name, new_path]], columns=["id", "name", "words_file"])
    users=users.append(new_user)
    print(users)
    users.to_csv(users_path, index=False)
    f = open(last_user_path, "w")
    f.write(str(new_id))
    f.close()
    return new_id

def choose_user(name_list,mode=0):
    while True:
        old_name = input("Enter username: \n")
        flag = False
        for name in name_list:
            if old_name == name:
                flag = True
                break
        if mode == 0:
            if flag:
                print("This name is already used!!!")
            else:
                break
        else:
            if not (flag):
                print("Name not found!!!")
            else:
                break
    return old_name

if __name__== "__main__":

    f = open(last_user_path, "r")
    last_user_id = f.read()
    f.close()


    users,id_list,name_list,name,path=update_users_info(users_path,last_user_id)

    # path="./words/res_merge.csv"
    count= 0
    kn, pr=1,0
    all=-99
    if not(debug):
        ans=standart_question( "Do you want to continue last game as {}?".format(name) ,1)
        if not(ans):
            ans = standart_question("Create new user?", 1)
            if ans:
                last_user_id=add_new_user(users)
                users, id_list, name_list, name, path = update_users_info(users_path,last_user_id)
            else:
               print("Save users: {}".format(name_list))
               name = choose_user(name_list,1)
               user = users.loc[users["name"] == name]
               new_id=user["id"].item()
               f = open(last_user_path, "w")
               f.write(str(new_id))
               f.close()
               users, id_list, name_list, name, path= update_users_info(users_path, new_id)



    try:
        while True:

            ans=standart_question( "Do you want to continue {}?".format(name) )
            if ans:
                kn, pr, all = start(path)
                count += 1
                print(" In this session you learn {} words".format(count))
    except AdventureDone:
        pass
    print("Your status:\n You know {} words.\n In process {} words".format(kn,pr))
    print("You know {} % printing words".format(round(kn/(kn+pr)*100)))
    print("Here {} words. i see {} words".format(all, kn+pr))
    if count >5:
        print("Good work! See you leter!")
    else:
        print ("You are so lasy today! Goodbye!")
