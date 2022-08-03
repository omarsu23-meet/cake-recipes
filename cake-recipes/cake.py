from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyB_bp5nrsoZAIMXpx1oHU2BZmwDsdbmpdY",
  "authDomain": "cake-recipes-2be9b.firebaseapp.com",
  "projectId": "cake-recipes-2be9b",
  "storageBucket": "cake-recipes-2be9b.appspot.com",
  "messagingSenderId": "298467564118",
  "appId": "1:298467564118:web:f831de7c607cead6a8b9f7",
  "measurementId": "G-16S2NQ3VYR",
  "databaseURL": "https://cake-recipes-2be9b-default-rtdb.europe-west1.firebasedatabase.app"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
cheesecake = {"name": "Cheesecake", "ingredients": "For the cheesecake ingredients: <br/> <br/> Butter, for coating the pan <br/> 2 pounds full-fat cream cheese <br/> 1 cup granulated sugar <br/> 1 tablespoon cornstarch, or 2 tablespoons all-purpose flour (optional) <br/> 1/8 teaspoon salt <br/> 1/2 cup sour cream <br/> 2 teaspoons freshly squeezed lemon juice (optional) <br/> 1 teaspoon vanilla extract <br/> 3 large eggs <br/> 1 large egg yolk <br/> For the crust: <br/> 12 whole graham cracker rectangles (6 ounces) <br/> 5 tablespoons unsalted butter",
"method": ["Heat the oven and soften the cream cheese. Arrange a rack in the lower-middle position of the oven and heat the oven to 350°F. Take the blocks of cream cheese out of their boxes and let them come to room temperature on the counter while you prepare the crust, about 30 minutes", "Coat the pan with butter. Use your fingers to coat a small pat of butter all over the bottom and sides of a 9-inch or 10-inch springform pan", "Wrap the pan in foil. Cut 2 large pieces of foil and place them on your work surface on top of each other in a cross. Set the springform pan in the middle and fold the edges of the foil up and around the sides of the pan. The foil gives you extra protection against water getting into the pan during the water bath step", "Prepare the crust. Crush the graham crackers in a food processor (or in a bag using a rolling pin) until they form fine crumbs — you should have 1 1/2 to 2 cups. Melt the butter in the microwave or on the stovetop and mix this into the graham cracker crumbs. The mixture should look like wet sand and hold together in a clump when you press it in your fist. If not, add extra tablespoons of water (one a time) until the mixture holds together. Transfer it into the springform pan and use the bottom of a glass to press it evenly into the bottom", "Bake the crust. Place the crust in the oven (be careful not to tear the foil). Bake until the crust is fragrant and just starting to brown around the edges, 8 to 10 minutes. Let the crust cool on a cooling rack while you prepare the filling", "Mix the cream cheese, sugar, cornstarch, and salt. Place the cream cheese, sugar, cornstarch, and salt in the bowl of a stand mixer fitted with a paddle attachment. (Alternatively, use an electric handheld mixer and large bowl.) Mix on medium-low speed until the mixture is creamy, like thick frosting, and no lumps of cream cheese remain. Scrape down the beater and the sides of the bowl with a spatula", "Mix in the sour cream, lemon juice, and vanilla. Add the sour cream, lemon juice, and vanilla and beat on medium-low speed until combined and creamy. Scrape down the beater and sides of the bowl with a spatula", "Mix in the eggs and yolk one at a time. With the mixer on medium-low speed, beat in the eggs and the yolk one at a time. Wait until the previous egg is just barely mixed into the batter before adding the next one. At first, the mixture will look clumpy and broken, but it will come together as the eggs are worked in", "Stir a few times by hand. Scrape down the beater and sides of the bowl with a spatula. Stir the whole batter a few times by hand, being sure to scrape the bottom of the bowl, to make sure everything is incorporated. The finished batter should be thick, creamy, and silky. Don't worry if you see a few specks of un-mixed cream cheese here and there; they will melt into the batter during baking and won't affect the finished cheesecake", "Pour the batter over the cooled crust. Check to make sure the crust and the sides of the pan are cool — if they're cool enough to comfortably touch, you can go on. Pour the batter over the cooled crust and spread it into an even layer", "Transfer the pan to the water bath. Transfer the pan to a roasting pan or other baking dish big enough to hold it. Bring a few cups of water to a boil and pour the water into the roasting pan, being careful not to splash any water onto the cheesecake. Fill the pan to about an inch, or just below the lowest edge of foil", "Bake the cheesecake. Bake the cheesecake for 50 to 60 minutes. Cakes baked in a 10-inch pan will usually cook in 50 to 55 minutes; cakes in a 9-inch pan will cook in 55 to 60 minutes. The cheesecake is done when the outer two to three inches look slightly puffed and set, but the inner circle still jiggles (like Jell-O) when you gently shake the pan. Some spots of toasted golden color are fine, but if you see any cracks starting to form, move on to the next step right away", "Cool the cheesecake in the oven. Leave the cheesecake in the oven. Turn off the oven and crack the door open or prop it open with a wooden spoon. Let the cheesecake cool slowly for 1 hour", "Run a knife around the edge of the cake and cool the cake completely. Remove the cheesecake from the oven and from the water bath, unwrap the foil, and transfer it to a cooling rack. Run a thin-bladed knife around the edge of the cake to make sure it's not sticking to the sides (which can cause cracks as it cools). Let the cheesecake cool completely on the rack", "Chill the cheesecake for 4 hours in the refrigerator. Chill the cheesecake, uncovered, for at least 4 hours or up to 3 days in the refrigerator. This step is crucial for letting the cheesecake set and achieving perfect cheesecake texture — don't rush it", "Top the cheesecake and serve. Take the cheesecake out of the refrigerator about 30 minutes before you plan to serve. Unmold the cake and top the cheesecake just before serving. You can serve the cake right from the bottom of the springform pan, or use a large off-set spatula to gently unstick the crust from the pan and transfer it to a serving platter"]}
lazy_cake = {"name1": "Lazy-cake ingredients:-", "ingredients": "Butter: You can use either hot, melted butter or butter softened at room temperature <br/> Sugar: You can use granulated sugar or powdered (icing) sugar <br/> Cocoa powder: Use unsweetened cocoa powder as the recipe contains sugar <br/> 1 cup of milk <br/> Tea biscuits <br/> Flavorings: A little bit of salt, to enhance the flavors. But you can really have as much fun as you’d like with the flavorings! Add orange zest, vanilla extract", 
"method1": ["Place the butter in a large bowl (microwavable). Heat in the microwave in 20 second increments until fully melted. You can heat the butter in a pan on the stove if you prefer. Using softened butter: If you don’t want to melt the butter at all, you can simply let it sit at room temperature until softened. Use powdered (icing) sugar in this case instead of granulated sugar", "Pour the sugar over the hot melted butter and whisk until combined", "Whisk in the cocoa powder and salt. You don’t need to sift the cocoa powder but whisk well to get rid of any cocoa lumps", "Pour the milk over the mixture and whisk until completely smooth and shiny. If desired, taste the chocolate mixture at this point to see if you are happy with the chocolate flavor and sweetness. Add more cocoa powder if you want a stronger chocolate flavor or less sweetness. Add more sugar if you want it sweeter", "Crush the biscuits with your hands over the chocolate mixture. The pieces shouldn’t be too small. I crush each biscuit into about 6-8 pieces", "Mix the biscuits with the chocolate using a large spoon until completely coated"]} 

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)

            return redirect(url_for('about_us'))
        except:
           error = "Authentication failed"
           return error
    else: 
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['name']
        username = request.form['user']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"name": full_name, "email": email}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('about_us'))
        except:
            error = "signing up failed"
            return error
    else:
        return render_template("signup.html")

@app.route('/share', methods=['GET', 'POST'])
def share():
    user = db.child("Users").child(login_session['user']['localId']).get().val()
    name = user['name']
    if request.method == 'POST':
        try:
            cake = {
            "name": request.form['name'], 
            "ingredients": request.form['ingredients'], 
            "method": request.form['method']}
            db.child("Cakes").push(cake)
            ## Firas has changed this line, 
            return redirect(url_for('recipes'))
        except:
            error = "Authentication failed"
            return error
    return render_template("share.html", name=name)

@app.route('/about_us', methods=['GET', 'POST'])
def about_us():
    user = db.child("Users").child(login_session['user']['localId']).get().val()
    name = user['name']
    return render_template("home.html", name=name)

@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    user = db.child("Users").child(login_session['user']['localId']).get().val()
    name = user['name']
    cakes = db.child("Cakes").get().val()
    return render_template("recipes.html", name=name, cheesecake=cheesecake, lazy_cake=lazy_cake, cakes=cakes)

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)