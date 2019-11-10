#-*- coding:UTF-8 -*-
#Filename:nester.py
#Authory by : Lyson

#add level default value
#add indent to control indentation
#handler list
def print_lol(the_list,indent=False,level=0):
    for each_item in the_list:
        if isinstance(each_item,list):
            print_lol(each_item,indent,level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print('\t',end='')
            print(each_item)
