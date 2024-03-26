import pyxel
import random
import math
import Quadtree as qt

AMT_OF_COUNTRIES = 600

class target:
    def __init__(self):
        self.y = pyxel.mouse_y
        self.x = pyxel.mouse_x

    def getCoords(self):
        return self.x, self.y
    
    def setCoords(self, x, y):
        self.x = x
        self.y = y

class country:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = [0, 0]
        self.maxSpeed = 3

    def setCoords(self, x, y):
        self.x = x
        self.y = y
    
    def getCoords(self):
        return self.x, self.y
    
    def getDir(self):
        return self.direction

    def setDir(self, dir):
        self.direction = dir

    def align(self, boids):
        radius = 30
        steering = [0, 0]
        total = 0
        for other in boids:
            d = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
            if other != self and d < radius:
                steering[0] += other.getDir()[0]
                steering[1] += other.getDir()[1]
                total += 1
        if total > 0:
            steering[0] /= total
            steering[1] /= total

            magnitude = math.sqrt(math.pow(steering[0], 2) + math.pow(steering[1], 2))
            
            if magnitude != 0:
                steering[0] /= magnitude
                steering[1] /= magnitude

        return steering
 
    def cohesion(self, boids):
        radius = 30
        steering = [0, 0]
        total = 0
        for other in boids:
            d = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
            if other != self and d < radius:
                x, y = other.getCoords()
                steering[0] += x
                steering[1] += y
                total += 1
        if total > 0:
            steering[0] /= total
            steering[1] /= total

            x, y = self.getCoords()
            steering[0] -= x
            steering[1] -= y

            magnitude = math.sqrt(math.pow(steering[0], 2) + math.pow(steering[1], 2))
            
            if magnitude != 0:
                steering[0] /= magnitude
                steering[1] /= magnitude

        return steering

    def separation(self, boids):
        radius = 30
        steering = [0, 0]
        total = 0
        for other in boids:
            d = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
            if other != self and d < radius:
                x, y = self.getCoords()
                x2,y2 = other.getCoords()
                x -= x2
                y -= y2
                if d!=0:
                    x /= d
                    y /= d
                steering[0] += x
                steering[1] += y
                total += 1
        if total > 0:
            steering[0] /= total
            steering[1] /= total

            magnitude = math.sqrt(math.pow(steering[0], 2) + math.pow(steering[1], 2))
            
            if magnitude != 0:
                steering[0] /= magnitude
                steering[1] /= magnitude

        return steering

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        
        # Update the direction based on alignment and cohesion
        self.direction[0] += alignment[0] + cohesion[0] + separation[0]
        self.direction[1] += alignment[1] + cohesion[1] + separation[1]

        # Scale the direction vector to the maximum speed
        magnitude = math.sqrt(math.pow(self.direction[0], 2) + math.pow(self.direction[1], 2))
        if magnitude != 0:
            self.direction[0] = self.direction[0] / magnitude * self.maxSpeed
            self.direction[1] = self.direction[1] / magnitude * self.maxSpeed

def initCountries(amt_countries, width, height):
    countries = []
    for _ in range(amt_countries):
        x = random.randint(0, width)
        y = random.randint(0, height)
        c = country()
        c.setCoords(x, y)
        countries.append(c)
    return countries

def inittarget():
    x = pyxel.mouse_x
    y = pyxel.mouse_y
    p = target()
    p.setCoords(x, y)
    return p

class App:
    def __init__(self):
        pyxel.init(800, 800)
        self.countries = initCountries(AMT_OF_COUNTRIES, 800, 800)
        self.target = inittarget()

        # Create a quadtree and insert countries into it
        self.quadtree = qt.QuadTree(qt.Square(0, 0, 800, 800), 2)
        for country in self.countries:
            self.quadtree.insert(country)
        
        pyxel.run(self.update, self.draw)

    def update(self):
        self.target.setCoords(pyxel.mouse_x, pyxel.mouse_y)
        
        for country in self.countries:
            direction = country.getDir()
            x, y = country.getCoords()
            
            # Update the position based on the assigned direction
            new_x = x + direction[0] 
            new_y = y + direction[1]
            
            # Wrap around the screen if the new position goes out of bounds
            new_x %= 800
            new_y %= 800
            
            country.setCoords(new_x, new_y)
            
            # Retrieve neighboring countries from the quadtree
            neighbors = self.quadtree.query_range(country.getCoords(), 30)
            
            # Apply alignment, cohesion, and separation behaviors
            country.flock(neighbors)

    def draw(self):
        pyxel.cls(0)
        
        for country in self.countries:
            x, y = country.getCoords()
            pyxel.circ(x, y, 4, 10)
        
        x, y = self.target.getCoords()
        pyxel.circ(x, y, 2, 8)

App()