
def contain(bag,e):
    return e in bag

def insert(bag,e):
    bag.append(e)

def remove(bag,e):
    bag.remove(e)

def count(bag):
    return len(bag) 

myBag=[]
insert(myBag,"휴대폰",:)
print("내가방속의물건:",myBag)