import webapp2
import passwords
import MySQLdb
import cgi
import random

conn = MySQLdb.connect(unix_socket = "/cloudsql/fast-flight-258317:us-central1:lab7gae",
                       user = passwords.SQL_USER,
                       passwd = passwords.SQL_PASSWD,
                       db = "lab7")
cursor = conn.cursor()
form = cgi.FieldStorage()
value = 0

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers["Content-Type"] = "text/html"
        self.response.write("Hello world")
        cookie = self.request.cookies.get("cookie_name")
        if (cookie):
            cursor.execute("SELECT user FROM sessions WHERE ID = ?", cookie)
            user = cursor.fetchall()
            if (user == "NULL"):
                user(self,cookie)

        else:
            id = "%032x" % random.getrandbits(128)
            query = "INSERT INTO sessions (ID) VALUES (" + id + ");"
            cursor.execute(query)
            self.response.set_cookie("cookie_name",id, max_age=1800)
            user(self,id)

def val(self,user):
    value = cursor.execute("SELECT num FROM value WHERE username = ?", user)
    self.response.write("""
                    <form action="/gae method="get">
                      <input type="submit", name="increment", value={}>
                    </form>""").format(value)
    if "increment" in form:
        val = value + 1
        cursor.execute("UPDATE value SET val = ? WHERE username = ?", (val, user))

def user(self,cookie):
    self.response.write("""
                    <form action="/gae method="get">
                      <input type="text" value="username">
                      <input type="submit">
                    </form>""")
    if "username" in form:
        val = form["username"].value
        cursor.execute("UPDATE sessions SET username = ? WHERE ID = ?", (val, cookie))
        val(self,val)

app = webapp2.WSGIApplication([
     ("/", MainPage),
], debug=True)
