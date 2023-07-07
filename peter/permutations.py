class Entry:
    def __init__(self, frontArray, backArray) -> None:
        self.frontArray = frontArray
        self.backArray = backArray

    

class Permu:
    def __init__(self, array) -> None:
        self.array = array
        self.bucket = []

    def print_all(self):
        firstEntry = Entry([], self.array.copy())
        self.bucket.append(firstEntry)

        while len(self.bucket) > 0:
            current = self.bucket.pop(0)
            if len(current.backArray) == 0:
                print(current.frontArray)
            else:
                for i in range(len(current.backArray)):
                    newEntry = Entry(current.frontArray.copy(), current.backArray.copy())
                    newEntry.frontArray.append(current.backArray[i])
                    newEntry.backArray.pop(i)
                    self.bucket.append(newEntry)
                    

def basictest1():
    inputString = input("give an array: ")
    inputArray = inputString.split(" ")
    permu = Permu(inputArray)
    permu.print_all()

if __name__ == "__main__":
    basictest1()