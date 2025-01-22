Test_case=int(input("Enter the no of test cases:"))

for j in range(Test_case):
    NoOfPlayers=int(input("Enter the number of players:"))

    Check_manual=input()
    Players=[]
    count1=0
    count2=0

    if (Check_manual == 'Manual') or (Check_manual == 'manual'):
       
        for i in range(NoOfPlayers):

            x=int(input("Enter the player type:"))
            
            if (count2 <= 1):
                
                if (x==0) or x==1 or x == -1 :
                    Players.append(x)
                    if x==-1:
                        count2 = count2 +1
                        Impostor=i
                else:
                    print('We dont support this player type.')
                    i=i-1
            else:
                print('There can only be one impostor, going to the next test case.')
                j=j+1
            
        while(count1<=(NoOfPlayers + 69)):
                check=input()
                count1 = count1 + 1

                if (check[0] == '?'):
                    fp=int(check[2]) -1
                    sp=int(check[4]) -1

                    if (Players[fp] == Players[sp]):
                        print('yes')
                    elif(Players[fp] ==1 and Players[sp] == 0) or (Players[fp] ==0 and Players[sp] == 1):
                        print('No')
                    elif(Players[fp] ==1 and Players[sp] == -1): print('Yes')
                    elif(Players[fp] ==-1 and Players[sp] == 1):print('No')
                    elif(Players[fp] ==-1 and Players[sp] == 0):print('yes')
                    elif(Players[fp] ==0 and Players[sp] ==-1): print('No') 
                        

                elif(check[0] == '!'):
                    ImpostorGuess=int(check[2]) - 1
                    if ImpostorGuess == Impostor:
                        print('Impostor Found.')
                        break
                    else:
                        print('-1,Wrong Answer')
                        break
                    
                else:print('-1,wrong Answer')



    else: print('Syntax Error!!')
