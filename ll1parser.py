
import pandas as pd
#eliminate immediate left recursion
terminals=[]
change_name={}

def parsing(table,input_string,start_symbol):
    string_pointer=0
    stack=['$',start_symbol]
    input_string=input_string+'$'
    steps={"Stack":[],"String":[],"Action":[]}
    while(len(stack)>0):
        new_stack=[i for i in stack]
        # for i in range(len(stack)):
        #     if(stack[i] in change_name):
        #         new_stack[i]=change_name[stack[i]]
        steps["Stack"].append('    '+' '.join(new_stack))
        steps["String"].append('    '+' '.join(list(input_string[string_pointer:])))
        top=stack[-1]
        stch=input_string[string_pointer]
        # print(stack,input_string[string_pointer:])
        if(top==stch):
            steps["Action"].append("    Pop")
            stack.pop()
            string_pointer+=1
        else:
            key=top,stch
            if(key not in table):
                exit(print("String not valid!"))

            if(table[key]!='^'):
                
                stack.pop()
                temp=list(table[key])[::-1]
                for i in temp:
                    stack.append(i)
                steps["Action"].append(top+"->"+table[key])
            
            else:
                stack.pop()
                steps["Action"].append("Pop")
    print("\nParsing steps\n")
    a=pd.DataFrame(steps)
    print(a)
    print("\nString accepted!")


def eliminate_immediate_left_recursion(c,d,terminals):
    lr=[]
    nlr=[]
    for i in range(len(d[c][1])):
        # append left recursion productions in lr 
        if(d[c][1][i][0]==d[c][0][0]):
            lr.append(d[c][1][i])
        # append left recursion productions in nlr
        else:
            nlr.append(d[c][1][i])
    if(len(lr)!=0):
        nvar=d[c][0][0]+'1'
        for i in range(65,91):
            if(chr(i) not in terminals):
                # print(nvar,"converted to ",chr(i))
                change_name[chr(i)]=nvar
                nvar=chr(i)
                terminals.append(nvar) 
                break       
        d[c][1]=[i+nvar for i in nlr]
        d.append([[nvar],[i[1:]+nvar for i in lr]+['^']])
def eliminate_left_recursion(productions,terminals):
    d=[]
    for term in productions:
        d.append([[term],productions[term]])
    n=len(d)
    eliminate_immediate_left_recursion(0,d,terminals)
    for i in range(1,n):
        for j in range(i):
            #previous production for ith production
            prev=d[j][0][0]
            for k in range(len(d[i][1])):
                #if there is non immediate left recursion
                if(d[i][1][k][0]==prev):
                    x=d[i][1][k][1:]
                    d[i][1].pop(k)
                    d[i][1]+=[l+x for l in d[j][1]]
        eliminate_immediate_left_recursion(i,d,terminals)
    new_prod={}
    for i in range(len(d)):
        new_prod[d[i][0][0]]=d[i][1]
    
    return(new_prod)


# contruction of ll1 parsing table
def table_construction(productions,start_symbol,follow_set):
    table={}
    for key in productions:
        for val in productions[key]:
            if(val!="^"):
                for term in first(val,productions,[]):
                    if (key,term) not in table:
                        table[key,term]=val
                    else:
                        exit(print("Error Not LL(1) grammar"))
            else:
                # for term in follow(key,productions,start_symbol):
                for term in follow_set[key]:
                    if (key,term) not in table:
                        table[key,term]=val
                    else:
                        #print(table)
                        exit(print("Error Not LL(1) grammar"))  
    #print(table)
    new_table = {}
    for pair in table:
        new_table[pair[1]] = {}
    for pair in table:
        new_table[pair[1]][pair[0]] = table[pair]
    print("\n")
    print("\nParsing Table\n")
    print(pd.DataFrame(new_table,index=[key for key in follow_set]).fillna('Error'))
    print("\n")
    return(table) 

#Function to print productions
def print_productions(productions):
    for i in productions:
        print(i+"->"+('/').join(productions[i]))

#Function to generate first set
def first(val,productions,visited):
    first_set=set()
    #print(val,productions)
    # if(val in visited):
    #     return first_set
    if(not(val[0].isupper())):
        first_set=first_set.union(val[0])
    else:
        
        for prod in productions[val[0]]:
            if(prod == "^"):
                first_set = first_set.union(prod)
            else:
                if(prod[0].isupper()):
                    if(prod[0] in visited):
                        continue
                    NT_first_set = first(prod[0],productions,visited+[prod[0]])
                    if("^" in NT_first_set):
                        if(len(prod) > 1):
                            NT_first_set_again = first(prod[1:],productions,visited+[prod[0]])
                            #When "^" is in first of a NT 
                            #Then production is checked further and its set is unioned with first_set(final result)
                            first_set = first_set.union(NT_first_set_again)
                    first_set = first_set.union(NT_first_set)
                else:
                    
                    first_set = first_set.union(prod[0])
                    
    return(first_set)

#Function to generate first set
def follow(val,productions,start_symbol,visited_NT):
    follow_set = set()
    if(start_symbol == val):
        follow_set = set('$')
    # if(val in visited_NT):
    #     return follow_set

    for key,prod in productions.items():
        flag=1
        for strings in prod:
            for char_idx in range(len(strings)):
                if(strings[char_idx] == val):
                    if(char_idx == len(strings)-1):
                        if(key in visited_NT):
                            flag=0
                            break
                        
                        
                        NT_follow_set = follow(key,productions,start_symbol,visited_NT+[key])
                        follow_set = follow_set.union(NT_follow_set)
                    else:
                        NT_first_set = first(strings[char_idx+1:],productions,[])
                        
                        for element in NT_first_set:
                            if(element=="^"):
                                #print(key,element)
                                if(key in visited_NT):
                                    flag=0
                                    break
                                NT_follow_set_again = follow(key,productions,start_symbol,visited_NT+[key])
                                follow_set = follow_set.union(NT_follow_set_again)
                            
                            else:
                                follow_set = follow_set.union(element)
                else:
                    #do nothing

                    pass
            if flag==0:
                break

    return follow_set

        


if __name__=="__main__":
    productions={}
    first_set={}
    follow_set={}
    terminals=[]
    grmr_file=open("grammar.txt","r")
    
    start_symbol=""
    flag=1
    for i in grmr_file:
        k=i.rstrip().split('->')
        #print(grmr_file)
        if(flag==1):
            flag=0
            start_symbol=k[0]
        if(k[0].strip() not in productions):
            productions[(k[0]).strip()]=[]   
        # productions[(k[0]).strip()]+=(''.join(j.strip().split()) for j in k[1].split('|'))
        productions[(k[0]).strip()]+=(j.strip() for j in k[1].split('|'))
        #x=(str(j.strip()) for j in k[1].split('|'))
        
    terminals=[i for i in productions]
    print("\nProductions : ")
    print_productions(productions)
    pr1=productions
    productions=eliminate_left_recursion(productions,terminals)
    if(pr1==productions):
        print("\nNo left recursion.")
    else:
        print("\nProductions after left recursion elimination: ")
        print_productions(productions)

    flag = 1
    for key in productions:
        if(flag == 1):
            start_symbol = key
            flag = 0
            
        follow_set[key] = follow(key,productions,start_symbol,[])
        first_set[key] = first(key,productions,[])
        
    
    print("-----------------------------")
    for key in first_set:
        print("First("+key+")"+' -> { '+ ', '.join(list(first_set[key]))+' }')
    print("\n\n----------------------------")
    for key in follow_set:
        print("Follow("+key+")"+' -> { '+ ', '.join(list(follow_set[key]))+' }')
        
    
    table=table_construction(productions,start_symbol,follow_set)
    input_string = input("Input String: ")
    parsing(table,input_string,start_symbol)
    # print(table)
