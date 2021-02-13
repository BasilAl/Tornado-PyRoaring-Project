import random
import pyroaring




def generate_User_stats(ulist,verbose=0):
    '''Generates a list of how many users have each tag.'''
    user_stats=[]
    for i in range(1,11):
        s=0
        for user in ulist:
            if user[1].contains_range(i,i+1):
                s+=1
        user_stats.append(["tag{:02d}".format(i),s])

        if verbose:
            print("tag{:02d}: {}".format(i,s))
    return user_stats

def check_uid_for_tag(ulist,tag,verbose=0):
    '''Returns a list of IDs of users in ulist that have a given tag and how many have the given tag in the format ([users],amount)'''
    users=[]
    s=0
    for user in ulist:
        if user[1].contains_range(tag,tag+1):
            users.append(user[0])
            s+=1

    if verbose:
        print("{} users have tag{:02d}. These are: ".format(s,tag))
        for i in range(len(users)):
            if i%8==0:
                print(users[i])
            else:
                print(users[i],end=", ")
        print("\n{}".format(s))
    return (users,s)

def generate_users_file(filename="users.txt",verbose=0):
    '''Creates a file with a list of mock users and their tags'''
    import os
    amount=1500
    try:
        os.remove(filename)
        print("Cleared file")
    except:
        pass
    finally:
        f=open(filename,"x")
        f.close()
        users=generate_mock_users(amount)
        f=open(filename,"a")
        for user in users:
            f.write(user[0]+" "+ str(user[1])+"\n")
        f.close()
        print("File {} created.".format(filename))

def read_users_from_file(filename="users.txt",verbose=0):
    '''Reads a text file of users and their BitMap codes and returns a list [user,[codes]] where [codes] is a BitMap list'''
    f=open(filename,"r")
    raw_users=f.readlines()
    f.close()
    for i in range(len(raw_users)):
        raw_users[i]=raw_users[i].split(" ",1)
        raw_users[i][1]=raw_users[i][1].removeprefix("BitMap([")
        raw_users[i][1]=raw_users[i][1].removesuffix("])\n").replace(" ","").split(",")
        tmplist=raw_users[i][1]
        bmp=pyroaring.BitMap()
        for item in tmplist:
            try:
                bmp.add(int(item))
            except:
                pass
        raw_users[i][1]=bmp
    return raw_users

def generate_mock_users(amount=1500):
    '''Generates [amount] number of users.Users are tuples with a username and a list of tags attached. Returns a list: [(username,[tags])]'''
    ulist=[]
    for i in range(amount):
        tags=pyroaring.BitMap()
        user=("user{:04d}".format(i),tags)
        for i in range(random.randint(0,10)):
            user[1].add(random.randint(1,10))
            # user[1].add(1)
            # user[1].contains_range()
        ulist.append(user)
    return ulist






if __name__=="__main__":
    '''If executed generates a mock list of users with each user being a tuple (user,[tags]) '''
    users_list=generate_mock_users()
    
    users_list[1][1]
    # for i in range(5):
        # print(users_list[i])
    # lista=generate_User_stats(users_list,1)
    print()
    # check_uid_for_tag(users_list,3,1)
    generate_users_file()
    # read_users_from_file()