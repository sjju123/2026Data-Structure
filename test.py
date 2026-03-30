
def contain(bag,e):
    return e in bag

def insert(bag,e):
    bag.append(e)

def remove(bag,e):
    bag.remove(e)

def count(bag):
    return len(bag) 

myBag=["필기구","지갑"]
print("내가방속의물건:",myBag)
insert(myBag,"휴대폰")
insert(myBag,"교재")
insert(myBag,"노트북")
print("내가방속의물건:",myBag)
print("가방속 유무:",contain(myBag,"모자"))
insert(myBag,"모자")
print("내가방속의물건:",myBag)
remove(myBag,"모자")
print("가방속 유무:",contain(myBag,"모자"))
insert(myBag,"교재")
insert(myBag,"교재")
print("내가방속의물건:",myBag)
print("가방속 물건의 개수:",count(myBag))

def numOf(bag,e):
    count = 0
    for i in range(len(bag)):
        if bag[i] == e :
            count = count + 1
    return count

print("가방속 교재의 개수 : ",numOf(myBag,"교재")) 