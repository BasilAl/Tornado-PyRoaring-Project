import json
import generateMockUsers as users 
import tornado.web
import tornado.ioloop
from tornado import httpclient, gen
from tornado.gen import multi
from datetime import date

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello world, this is executed from get")
        self.render("index.html")

# class listRequestHandler(tornado.web.RequestHandler):
#     def get(self,tag):
#         pass
#     def post(self):
#         tag = self.get_argument("tag")
#         usersList=users.generate_User_stats(users.read_users_from_file("users.txt"))
#         if tag=="All":
#             returnItem=json.dumps(usersList)
#         elif tag.isdigit():
#             returnItem=json.dumps(usersList[int(tag)-1])
#         else:
#             self.write(json.dumps({"message":"No Such Tag"}))
#         print(returnItem)
#         print(type(returnItem))
#         self.write(returnItem+" users")

class tagStatsRequestHandler(tornado.web.RequestHandler):
    def get(self,tag):
        tag=int(tag)
        tagsList=users.generate_User_stats(users.read_users_from_file("users.txt"))
        usersList=users.check_uid_for_tag(users.read_users_from_file("users.txt"), tag)
        for i in range(len(tagsList)):
            tagsList[i][0]="<a href='/tagStats/{}'>".format(i+1)+tagsList[i][0]+"</a>"
        self.write("<a href='/'>Back to index</a><br>")
        self.write("Tag Statistics (amount of users for each tag): <br>")
        if tag==0:
            self.write(json.dumps(tagsList))
        elif tag<=10:
            self.write(json.dumps(tagsList[tag-1]))
            self.write("<br>Users with tag{:02d} :<br>".format(tag))
            for i in range(len(usersList[0])):
                usersList[0][i]="<a href='/users/"+str(usersList[0][i]).removeprefix("user")+"'>"+usersList[0][i]+"</a>"
            self.write(json.dumps(usersList))
            self.write("<br><a href='/tagStats/0'>Back to statistics</a><br>")
        else:
            self.write("No such tag.")
            self.write("<br><a href='/tagStats/0'>Back to statistics</a><br>")


class sessionRequestHandler(tornado.web.RequestHandler):
    def get(self):
        curDate=date.today()
        long_unlogged_users=[]
        for i in range(len(USERS)):
            dayDif=curDate-USERS[i][2]
            if dayDif.days>7:
                long_unlogged_users.append(USERS[i][0]+" : "+str(USERS[i][2]))
            else:
                pass
        # long_unlogged_users.append(len(long_unlogged_users))
        self.write("<a href='/'>Back to index</a><br>")
        self.write("<br> Number of users that haven't logged for 7 days: "+str(len(long_unlogged_users)))
        self.write("<br>Usernames and last login of said users: <br>")
        self.write(json.dumps(long_unlogged_users))

class userRequestHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self,usr):
        self.write("<a href='/'>Back to index</a><br>")
        usr=int(usr)
        usrs=users.read_users_from_file()
        if usr>len(usrs):
            self.write("No such user")
            return
        for i in range(len(usrs)):
            usrs[i][1]=usrs[i][1].to_array().tolist()
        self.write("Tags of user{:04d}: <br>".format(usr))
        self.write(str(usrs[usr][1]))
        # usrs=json.dumps(usrs)

class GenAsyncHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        urls=[]
        for i in range(10):
            urls.append("http://localhost:8882/users/{:04d}".format(i))
        response = yield multi([http_client.fetch(url) for url in urls])
        response=str(response)
        self.write("Still haven't figured how to modify the request handler to use these properly<br><br>")
        self.write(response)

if __name__ == "__main__":
    import random
    USERS = users.read_users_from_file()
    for i in range(len(USERS)):
        USERS[i].append(date(2021,random.randint(1,2),random.randint(1,date.today().day)))
    app = tornado.web.Application([
        (r"/", basicRequestHandler),
        (r"/sessionmanagement", sessionRequestHandler),
        (r"/tagStats/([0-9]{1,2})", tagStatsRequestHandler),
        (r"/users/([0-9]{4})",userRequestHandler),
        (r"/async",GenAsyncHandler)
    ])

    port = 8882
    http_client = httpclient.HTTPClient()
    
    app.listen(port)
    print(f"Listening on port {port}")
    tornado.ioloop.IOLoop.current().start()

    # async def parallel_fetch_many(urls):
    #     responses = await multi ([http_client.fetch(url) for url in urls])
    #     return responses


      
    
    