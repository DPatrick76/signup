form="""
<html>
    <head>
        <style>
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="%(username)s">
                        <span class="error">%(usernameError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password"">
                        <span class="error">%(passwordError)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password">
                        <span class="error">%(matcherror)s</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email</label></td>
                    <td>
                        <input name="email" type="email" value="%(email)s">
                        <span class="error">%(emailerror)s</span>
                    </td>
                </tr>
            </table>
            <input type="submit">
        </form>
    </body>
</html>
"""
import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def validUsername(username):
    return USER_RE.match(username)

def validPassword(password):
    return PASS_RE.match(password)

def validEmail(email):
    return EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="",email="", usernameError="", passwordError="", matcherror="", emailerror=""):
        self.response.out.write(form % {"username": username,
                                        "email": email,
                                        "usernameError": usernameError,
                                        "passwordError": passwordError,
                                        "matcherror": matcherror,
                                        "emailerror": emailerror})

    def get(self):
        self.write_form()

    def post(self):
        process_username = self.request.get('username')
        process_password = self.request.get('password')
        verify_password = self.request.get('verify')
        process_email = self.request.get('email')

        username= process_username
        email = process_email
        password = process_password
        verify = verify_password

        usernameVal = validUsername(process_username)
        passwordVal = validPassword(process_password)
        emailVal = validEmail(process_email)

        matchVal = True
        if process_password != verify_password:
            matchVal = False

        if not usernameVal:
            usernameError = "Please enter a valid username"
        else: usernameError = ""

        if not passwordVal:
            passwordError = "Please enter a valid password"
        else: passwordError = ""

        if not matchVal:
            matchError = "Passwords do not match"
        else: matchError = ""

        if not email:
            emailError = ""
            emailVal = True
        elif not emailVal:
            emailError = "Please enter a valid email address"
        else: emailError = ""

        if not (usernameVal and passwordVal and emailVal and matchVal):
            self.write_form(process_username, process_email,usernameError,passwordError,matchError, emailError)
        else:
            self.redirect('/welcome?username=%s' % username)
class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        print "The string username = ", username
        welcomeMessage = "Welcome, %s!"
        self.response.out.write(welcomeMessage % username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)], debug=True)
