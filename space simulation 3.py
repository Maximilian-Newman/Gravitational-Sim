import turtle
import math
import random
import os

import socket
import time
import sys





MaxCloudIP = ["max-cloud.ddns.net", 60001]

app_name = "Space Simulation"

CURRENT_VERSION = "3.0.2"

FILE_PACKET_LENGTH = 200
TIMEOUT_TIME = 5


failCount = 0
authFailCount = 0
apps = []
EOF = "end of " + "file" # '+' in the middle to not interrupt download of this file

stat = turtle.Turtle()
stat.hideturtle()
stat.speed(0)
stat.color("white")
stat.penup()
stat.goto(-550, 250)

loader = turtle.Turtle()
loader.hideturtle()
loader.speed(0)

def init_load(process_name):
    loader.clear()
    loader.penup()
    loader.goto(-250, 175)
    loader.color("white")
    loader.write(process_name, align="left", font=("Arial", 15, "bold"))
    
    loader.color("black")
    loader.pensize(24)
    loader.goto(-222, 150)
    loader.pendown()
    loader.goto(2, 150)
    loader.penup()
    
    loader.color("light gray")
    loader.pensize(18)
    loader.goto(-221, 150)
    loader.pendown()
    loader.goto(1, 150)
    loader.penup()
    loading(0.05)

def loading(progress):
    loader.penup()
    loader.goto(-220, 150)
    loader.pendown()
    loader.pensize(16)
    loader.color("blue")
    progress = int(progress * 220)
    loader.goto(progress - 220, 150)
    if progress == 220:
        loader.clear()
    
def internet_req(msg):
    global failCount
    global authFailCount
    user = ["NO_AUT", "NO_AUTH"]


    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.settimeout(TIMEOUT_TIME)
    try:
        msg = str(msg).encode()
        clientsocket.connect((MaxCloudIP[0], MaxCloudIP[1]))
        
        clientsocket.sendall("MaxCloud API protocol 2\n".encode())
        clientsocket.sendall((user[0] + "\n").encode())
        clientsocket.sendall((user[1] + "\n").encode())
        clientsocket.sendall((app_name + "\n").encode())
        clientsocket.sendall(msg)

        SALT = clientsocket.recv(20).decode()
        packet = clientsocket.recv(200)
        res = b''
        while len(packet) > 0:
            res += packet
            packet = clientsocket.recv(200)
        
        clientsocket.close()
        res = res[:-2]
    
    


        if res == "ERROR: athentification".encode():
            if authFailCount > 2:
                print()
                print()
                print()
                print("Authentication problem.")
                print("Something must have changed with the server, because normally you don't need to be signed in for MaxGraph updates.")
                return None
            else:
                authFailCount += 1
                return internet_req(msg.decode(), binData)

        failCount = 0
        authFailCount = 0
        return res

    except:
        failCount += 1
        if failCount > 1:
            return None
        else:
            time.sleep(3)
            return internet_req(msg.decode()) # try again a few times if failed





def update():
    file_contents = b""
    pnum = 0
    repeat = True
    while repeat:
        response = internet_req("install update\n" + str(pnum) + "\n")

        if response == "ERROR":
            print("\n\nAn unknown error occured.\n\n")
            time.sleep(5)
            return
        
        if response != None:
            if EOF.encode() in response:
                repeat = False
                response = response.replace(EOF.encode(), b"")
                file_contents += response

            elif len(response) == FILE_PACKET_LENGTH:
                file_contents += response
                pnum += 1
                print(".", end="")
        
        else:
            return False # update failed


    file = open(__file__, "wb")
    file.write(file_contents)
    file.close()
    return True






turtle.hideturtle()
turtle.speed(0)
turtle.color("blue")
turtle.penup()
turtle.goto(0, 100)
turtle.write("Space Simulation", align="center", font=("Arial", 50, "bold"))
turtle.color("black")
turtle.goto(0, 50)
turtle.write("Current version: " + CURRENT_VERSION, align="center", font=("Arial", 15, "bold"))
turtle.goto(0, 0)
turtle.write("Checking for software update ...", align="center", font=("Arial", 20, "bold"))


latestVersion = None

latestVersion = internet_req("latest version\n")
    
if latestVersion == None:
    turtle.goto(0, -50)
    turtle.color("red")
    turtle.write("Failed to connect to MaxCloud!", align="center", font=("Arial", 20, "bold"))


elif latestVersion != CURRENT_VERSION.encode():
    turtle.goto(0, -50)
    turtle.write("New update available: " + latestVersion.decode(), align="center", font=("Arial", 20, "bold"))

    if turtle.numinput("Max Graph Software Update", "A new update is available\n\nCurrent version: {}\nNew version: {}\n\nDo you want to install this update?\n 1. Yes\n 2. No".format(CURRENT_VERSION, latestVersion.decode()), minval=1, maxval=2, default="Enter a number here") == 1:
        
        turtle.goto(0, -80)
        turtle.write("Installing update ...", align="center", font=("Arial", 20, "bold"))
        
        if update() == True:
        
            turtle.goto(0, -100)
            turtle.write("Update installed, please restart the app.", align="center", font=("Arial", 20, "bold"))
            time.sleep(5)
            sys.exit()

        else:
            turtle.goto(0, -100)
            turtle.color("red")
            turtle.write("Update Failed!", align="center", font=("Arial", 20, "bold"))

    else:
        turtle.goto(0, -80)
        turtle.color("red")
        turtle.write("Update Canceled", align="center", font=("Arial", 20, "bold"))
else:
    turtle.goto(0, -50)
    turtle.write("No update available", align="center", font=("Arial", 20, "bold"))









time.sleep(2)
turtle.clear()





# Start of Simulation Software




def downloadFile(f_name, save_name):
    
    location = os.path.dirname(__file__) + "/saved simulations/" + save_name

    init_load("downloading: " + os.path.basename(location))

    file_contents = b""
    try:
        totalPackets = int(internet_req("download\n" + f_name + "\nlength?\n").decode()) +1
    except:
        loading(1)
        return
        
    pnum = 0
    lenProbCount = 0
    repeat = True
    while repeat:
        response = internet_req("download\n" + f_name + "\n" + str(pnum) + "\n")
        loading(pnum/totalPackets)
        if response == "ERROR":
            return

        
        if response != None:
            
            if EOF.encode() in response:
                repeat = False
                response = response.replace(EOF.encode(), b"")
                file_contents += response
                lenProbCount = 0

            elif len(response) == FILE_PACKET_LENGTH:
                file_contents += response
                pnum += 1
                lenProbCount = 0

            else: # wrong packet length, likely corrupted
                lenProbCount += 1
                if lenProbCount > 5:
                    time.sleep(5)
                    return
                else:
                    time.sleep(1) # try again a few times if failed
        
        else:
            # Internet disconnected
            return

    

    if file_contents != b"ERROR":

        file = open(location, "wb")
        file.write(file_contents)
        file.close()

        loading(1)

    else:
        loading(1) # failed
    





GRAVITATIONAL_CONSTANT = 1
SPEED = 1
PLANETS = []
REMOVED = []
START_POSITIONS = ""
highestID = 0
frameNumber = 0
initialEnergy = 0
thermalEnergy = 0
optimizationEnergy = 0
MIN_BRIGHTNESS = 50.0

class Vector():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def magnitude(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2) + (self.z ** 2))

    def cos_direction_from(self, vect):
        product = self.x * vect.x + self.y * vect.y + self.z * vect.z
        return product / (self.magnitude() * vect.magnitude())

    def add(self, vect):
        self.x += vect.x
        self.y += vect.y
        self.z += vect.z

    def multiply(self, num):
        vect = self.copy()
        vect.x *= num
        vect.y *= num
        vect.z *= num
        return vect

    def copy(self):
        return Vector(self.x, self.y, self.z)

X_AXIS = Vector(1, 0, 0)
Y_AXIS = Vector(0, 1, 0)
Z_AXIS = Vector(0, 0, 1)

class Planet():

    def __init__(self, x, y, z, p_x, p_y, p_z, mass, size=0):
        global highestID
        
        self.position = Vector(x, y, z)
        self.momentum = Vector(p_x, p_y, p_z)
        self.mass = mass

        self.turt = turtle.Turtle()
        self.turt.speed(0)
        self.turt.penup()
        self.turt.shape("circle")
        self.turt.goto(x, y)
        self.color = [random.randint(MIN_BRIGHTNESS, 255), random.randint(MIN_BRIGHTNESS, 255), random.randint(MIN_BRIGHTNESS, 255)]
        self.turt.color(self.color)
        self.ID = highestID
        highestID += 1

        
        if showLines:
            self.turt.pendown()

        size = size/21
        
        if size == 0:
            size = (mass ** (1/2.1) ) / 3
        if size < 0.2:
            size = 0.2
        self.turt.turtlesize(size, size, size)
        self.size = size * 21 # multiply by 21 for diameter in pixels

        PLANETS.append(self)

    def get_color(self, depth):
        depth /=2
        
        colors = self.color.copy()
        while colors[0] + colors[1] + colors[2] < 255 * 3 / 2 + depth and colors != [255, 255, 255]:
            if colors[0] < 255:
                colors[0] += 1
            if colors[1] < 255:
                colors[1] += 1
            if colors[2] < 255:
                colors[2] += 1
        
        while colors[0] + colors[1] + colors[2] > 255 * 3 / 2 + depth and colors != [MIN_BRIGHTNESS, MIN_BRIGHTNESS, MIN_BRIGHTNESS]:
            if colors[0] > MIN_BRIGHTNESS:
                colors[0] -= 1
            if colors[1] > MIN_BRIGHTNESS:
                colors[1] -= 1
            if colors[2] > MIN_BRIGHTNESS:
                colors[2] -= 1
        
        color = 256*256*int(colors[0]) + 256*int(colors[1]) + int(colors[2])
        color = str(hex(color))[2:].upper()
        while len(color) < 6:
            color = "0" + color
        return color


    def text_data(self):
        return "{},{},{},{},{},{},{},{}\n".format(self.position.x, self.position.y, self.position.z, self.momentum.x, self.momentum.y, self.momentum.z, self.mass, self.size)

    def kill(self):
        self.turt.clear()
        self.turt.hideturtle()
        try:
            PLANETS.remove(self)
        except:
            REMOVED.remove(self)

    def remove(self):
        self.turt.hideturtle()
        PLANETS.remove(self)
        REMOVED.append(self)

    def get_gravitational_energy(self):
        energy = 0
        for planet in PLANETS:
            if planet.ID != self.ID:
                energy += get_potential_energy(self, planet)
        return energy

    def get_kinetic_energy(self):
        v = self.momentum.magnitude() / self.mass
        return 0.5 * self.mass * v**2
        #return ( (self.momentum.x/self.mass) ** 2 + (self.momentum.y/self.mass) ** 2 + (self.momentum.z/self.mass) ** 2) / (2*self.mass)


def distance(planet1, planet2):
    dx = planet2.position.x - planet1.position.x
    dy = planet2.position.y - planet1.position.y
    dz = planet2.position.z - planet1.position.z
    return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

def get_force_components(planet1, planet2, force):
    dx = planet2.position.x - planet1.position.x
    dy = planet2.position.y - planet1.position.y
    dz = planet2.position.z - planet1.position.z


    diff = Vector(dx, dy, dz)
    f = Vector(0, 0, 0)
    f.x = force * diff.cos_direction_from(X_AXIS)
    f.y = force * diff.cos_direction_from(Y_AXIS)
    f.z = force * diff.cos_direction_from(Z_AXIS)

    return f

def get_potential_energy(planet1, planet2):
    return -GRAVITATIONAL_CONSTANT * planet1.mass * planet2.mass / distance(planet1, planet2)

def get_total_energy():
    try:
        energy = thermalEnergy + optimizationEnergy
        for planet1 in PLANETS:
            energy += planet1.get_kinetic_energy()
            for planet2 in PLANETS:
                if planet1.ID < planet2.ID:
                    energy += get_potential_energy(planet1, planet2)
        return energy
    except:
        return 0

def total_mass():
    mass = 0
    for planet in PLANETS:
        mass += planet.mass
    return mass

def total_momentum():
    momentum = Vector(0, 0, 0)
    for planet in PLANETS:
        momentum.add(planet.momentum)
    return momentum

def frame():
    global frameNumber
    global initialEnergy
    global thermalEnergy
    global optimizationEnergy
    pNum = 0
    
    while pNum < len(PLANETS):
        planet = PLANETS[pNum]
        cNum = 0
        while cNum < len(PLANETS):
            compare = PLANETS[cNum]
            if planet.ID != compare.ID:
                if distance(planet, compare) < (planet.size + compare.size) /2: # collision
                    newMass = planet.mass + compare.mass
                    newMomentumX = planet.momentum.x + compare.momentum.x
                    newMomentumY = planet.momentum.y + compare.momentum.y
                    newMomentumZ = planet.momentum.z + compare.momentum.z
                    newX = (planet.position.x * planet.mass + compare.position.x * compare.mass) / (planet.mass + compare.mass)
                    newY = (planet.position.y * planet.mass + compare.position.y * compare.mass) / (planet.mass + compare.mass)
                    newZ = (planet.position.z * planet.mass + compare.position.z * compare.mass) / (planet.mass + compare.mass)

                    energyBefore = get_total_energy()
                    
                    new = Planet(newX, newY, newZ, newMomentumX, newMomentumY, newMomentumZ, newMass)

                    planet.remove()
                    compare.remove()
                    
                    thermalEnergy += energyBefore - get_total_energy()

                    cNum = len(PLANETS)
                    pNum -= 1
                    

                else: # gravitational interaction
                    force = get_force_components(planet, compare, GRAVITATIONAL_CONSTANT * ((planet.mass * compare.mass) / (distance(planet, compare) ** 2) ))

                    planet.momentum.x += force.x * SPEED
                    planet.momentum.y += force.y * SPEED
                    planet.momentum.z += force.z * SPEED

            cNum += 1
        pNum += 1

            
    energyBefore = get_total_energy()
    for planet in PLANETS:
        if planet.position.magnitude() > 4000:
            planet.remove()
            reset_momentums()
    
    
    optimizationEnergy += energyBefore - get_total_energy()
    
    for planet in PLANETS:
        planet.position.x += planet.momentum.x * SPEED / planet.mass
        planet.position.y += planet.momentum.y * SPEED / planet.mass
        planet.position.z += planet.momentum.z * SPEED / planet.mass

        planet.turt.goto(planet.position.x, planet.position.y)
        planet.turt.color("#" + planet.get_color(planet.position.z))


    try:
        totalGPE = 0
        totalKE = 0
        for planet1 in PLANETS:
            totalKE += planet1.get_kinetic_energy()
            for planet2 in PLANETS:
                if planet1.ID < planet2.ID:
                    totalGPE += get_potential_energy(planet1, planet2)
        
        if frameNumber == 0:
            initialEnergy = totalKE + totalGPE
            thermalEnergy = 0
            optimizationEnergy = 0

        
        stat.clear()
        stat.write("""Press 'M' to access menu
Brightness indicates Z-axis

Frame Number: {}
Number of Particles: {}
Kinetic Energy: {}
Gravitational Potential Energy: {}
Thermal Energy (collisions): {}
Optimisation Energy (particles removed from system): {}
Total Energy: {}
Energy Deviation (simulation error): {} %""".format(frameNumber+1, len(PLANETS), totalKE, totalGPE, thermalEnergy, optimizationEnergy, totalKE + totalGPE + thermalEnergy + optimizationEnergy, (initialEnergy - (totalKE + totalGPE + thermalEnergy + optimizationEnergy) )*100/initialEnergy))
    except:
        stat.write("Press 'M' to access menu")

    frameNumber += 1


running = True
showLines = True


def load_from_text(text):
    global highestID
    global PLANETS
    global REMOVED
    global showLines
    global frameNumber
    frameNumber = 0
    
    while len(PLANETS) > 0:
        PLANETS[0].kill()
    while len(REMOVED) > 0:
        REMOVED[0].kill()

    text = text.split("\n")
    for planet in text:
        planet = planet.split(",")

        Planet(float(planet[0]), float(planet[1]), float(planet[2]), float(planet[3]), float(planet[4]), float(planet[5]), float(planet[6]), float(planet[7]))

    reset_momentums()


def reset_momentums():
    # makes sure total momentum of system is 0
    # otherwise everything drifts off the screen
    momentum = total_momentum()
    momentum = momentum.multiply(-1 / total_mass())
    for planet in PLANETS:
        planet.momentum.add(momentum.multiply(planet.mass))


def load_from_file(path):
    global highestID
    global PLANETS
    global REMOVED
    global START_POSITIONS
    global GRAVITATIONAL_CONSTANT
    global showLines
    global frameNumber
    frameNumber = 0
    showLines = True
    
    try:
        file = open(path, "r")
        data = file.read()
        file.close()

        data = data.split(";")
        GRAVITATIONAL_CONSTANT = float(data[0])

        if path.endswith(".ss2"):
            data[1] = data[1].split("\n")
            for i in range(0, len(data[1])):
                data[1][i] = data[1][i].split(",")
                data[1][i] = [data[1][i][0], data[1][i][1], "0", data[1][i][2], data[1][i][3], "0", data[1][i][4], "0"]
                data[1][i] = ",".join(data[1][i])
            data[1] = "\n".join(data[1])
        
        load_from_text(data[1])

        START_POSITIONS = data[1]
        
    except:
        print()
        print()
        print()
        print("An error occured loading your file")



def load_random_nebula():
    global highestID
    global PLANETS
    global showLines
    global GRAVITATIONAL_CONSTANT
    global START_POSITIONS
    global frameNumber
    frameNumber = 0

    showLines = False
    GRAVITATIONAL_CONSTANT = 30 # was 30
    
    START_POSITIONS = ""
    
    for i in range(400):
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        z = random.randint(-200, 200)
        
        START_POSITIONS += "{},{},{},{},{},{},{},{}\n".format(x, y, z, y / 50, -x / 50, z / 50, 1, 0)
    START_POSITIONS = START_POSITIONS[0:-1]
    load_from_text(START_POSITIONS)
    
def choose_simulation():
    global highestID
    global PLANETS
    global REMOVED
    global START_POSITIONS
    global GRAVITATIONAL_CONSTANT
    global showLines
    
    directory = os.listdir(os.path.dirname(__file__) + "/saved simulations")
    files = []

    for file in directory:
        if file.endswith(".ss2") or file.endswith(".ss3"):
            files.append(file)


    prompt = """Please choose a simulation to run:

  1 - Generate random nebula

"""

    for i in range(2, len(files) + 2):
        prompt += "  " + str(i) + " - " + files[i-2] + "\n"

    fNum = turtle.numinput("Space Simulation 2", prompt, default = "Enter the corresponding number here", minval=1, maxval=len(files)+1)
    screen.listen()
    
    if fNum == 1:
        load_random_nebula()

    elif fNum != None:
        load_from_file(os.path.dirname(__file__) + "/saved simulations/" + files[int(fNum) - 2])

    screen.listen()
    
    




def save_frame():
    global GRAVITATIONAL_CONSTANT
    
    title = turtle.textinput("Space simulation 3", "Please enter a name for your saved file:")

    while title != None:
        title += ".ss3"

        try:
            file = open(os.path.dirname(__file__) + "/saved simulations/" + title, "r")# check if file already exists
            file.close()
            
            title = turtle.textinput("Space simulation 3", "This file already exists.\nPlease enter a name for your saved file:")
            
        except:
            save = str(GRAVITATIONAL_CONSTANT) + ";"
            for planet in PLANETS:
                save += planet.text_data()
            save = save[:-1]

            file = open(os.path.dirname(__file__) + "/saved simulations/" + title, "w")
            file.write(save)
            file.close()
            title = None

    screen.listen()

def download_new():
    options = ""
    index = 0
    while not options.endswith(EOF):
        options += internet_req("index\n" + str(index) + "\n").decode()
        index += 1
    options = options.replace(EOF, "").split("\n")
    prompt = "choose a simulation from the list by entering a number:\n\n"
    for i in range(0, len(options)):
        prompt += " " + str(i+1) + ". " + options[i] + "\n"
    
    num = turtle.numinput("Download simulations", prompt)
    screen.listen()
    if num != None:
        downloadFile(str(int(num)) + ".ssm", options[int(num)-1])

    pause()




    

def Quit():
    global running
    running = False



def show_hide_lines():
    global showLines
    if showLines:
        showLines = False
        for planet in PLANETS:
            planet.turt.penup()
    else:
        showLines = True
        for planet in PLANETS:
            planet.turt.pendown()


def clear_lines():
    for planet in PLANETS:
        planet.turt.clear()
    
    while len(REMOVED) > 0:
        REMOVED[0].kill()


def restart():
    load_from_text(START_POSITIONS)


def pause():
    prompt = """
Simulation Paused

Options:
 1. Resume
 2. Show/hide trace lines
 3. Clear trace lines
 4. Change speed
 5. Restart
 6. Save current frame
 7. Start new simulation
 8. Download new simulations
 9. Quit

You can press 'M' at any time to show this menu
"""
    option = turtle.numinput("Space Sumulation", prompt, minval=1, maxval=9, default=1)
    if option == 2:
        show_hide_lines()
    if option == 3:
        clear_lines()
    if option == 4:
        global SPEED
        n = turtle.numinput("MaxCloud Space Simulation", "Enter a new speed\nA higher speed will lead to lower accuracy", minval=0.01, default=SPEED)
        if n != None:
            SPEED = n
    if option == 5:
        restart()
    if option == 6:
        save_frame()
    if option == 7:
        choose_simulation()
    if option == 8:
        download_new()
    if option == 9:
        Quit()
    screen.listen()

menuBtnPressed = False

def menu_button():
    global menuBtnPressed
    menuBtnPressed = True

turtle.hideturtle()
turtle.colormode(255)


screen = turtle.Screen()
screen.tracer(False)
screen.title("MaxCloud Space Simulation")
screen.bgcolor("black")
screen.listen()
screen.setup(1200, 800)
screen.screensize(5000, 5000)

screen.onkey(menu_button, "m")
screen.onkey(menu_button, "M")






try:
    os.mkdir(os.path.dirname(__file__) + "/saved simulations")
except:
    pass




pause()

try:
    while running:
        if menuBtnPressed:
            menuBtnPressed = False
            pause()
        screen.update()
        frame()
    turtle.bye()

except: # closing window causes error
    pass

