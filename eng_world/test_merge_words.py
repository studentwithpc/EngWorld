# file for delete duplicates in english words, and merge russian words
import pandas as pd


def read_file(path):
    df=pd.read_csv(path,  usecols=["eng_word","rus_word", "status"])
    return df

def merge_word(frame):
    mark_dup=frame.duplicated(subset="eng_word").tolist()
    last_rus=" "
    for word,rus_word,mark in zip(frame['eng_word'],frame['rus_word'],mark_dup):
        if mark:
            frame.loc[frame.rus_word==last_rus, 'rus_word']=last_rus+": "+rus_word
            rus_word=last_rus+rus_word
        last_rus=rus_word
    frame=frame.drop_duplicates(subset="eng_word")
    return frame


if __name__== "__main__":
    path="./words/2000.csv"
    path_res="./words/res_merge.csv"
    frame=read_file(path)
    frame= merge_word(frame)
    frame.to_csv(path_res,index=False)
