x=input("Enter the number to be tested: ")


z=len(x)

a= len(x)

count =0
r=int(x)

for i in range(z):

    p=10**(a-1)
    q=(r//p)
    if (r//p == 4) or(r//p == 7):
        count = (count + 1)
    else:
        pass
    r= r- (q*p)
    a=(a-1)
    i+=1
    

lucky=str(x)

length=len(lucky)
count2=0

for i in range(length):
    if (lucky[i] == '4') or (lucky[i] == '7'):
          count2= count2 + 1
    else:
        print("No,not a nearly Lucky Number!!")
        break
       

if (count2 == 4 or count2 == 7 ):
    print("Yes, this is a nearly Lucky Number!!")
