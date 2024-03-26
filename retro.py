import pyxel
import random
import math
import Quadtree as qt

AMT_OF_birdies = 300
AMT_OF_PREDATORS = 10

class target:
    def __init__(self):
        self.y = pyxel.mouse_y
        self.x = pyxel.mouse_x

    def getCoords(self):
        return self.x, self.y
    
    def setCoords(self, x, y):
        self.x = x
        self.y = y
        

class predator:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = [0, 0]
        self.maxSpeed = 2
        self.size = 10
        self.health = 100

    def getCoords(self):
        return self.x, self.y
    
    def setCoords(self, x, y):
        self.x = x
        self.y = y
    
    def getDir(self):
        return self.direction

    def setDir(self, dir):
        self.direction = dir

    def attack(self, boids):
        radius = 50  # Adjust the predator's attack radius as desired
        closest_boid = None
        closest_distance = float("inf")

        x, y = self.getCoords()
        for other in boids:
            x2, y2 = other.getCoords()
            distance = math.sqrt(math.pow(x - x2, 2) + math.pow(y - y2, 2))
            if other != self and distance < radius and distance < closest_distance:
                closest_boid = other
                closest_distance = distance

        steering = [0, 0]
        if closest_boid is not None:
            x2, y2 = closest_boid.getCoords()
            steering[0] = x2 - x
            steering[1] = y2 - y
            
            magnitude = math.sqrt(math.pow(steering[0], 2) + math.pow(steering[1], 2))
            if magnitude != 0:
                steering[0] /= magnitude
                steering[1] /= magnitude
        
        return steering

    def separation(self, predators):
        steering = [0, 0]
        total = 0
        for other in predators:
            radius = other.size + 80
            d = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
            if other != self and d < radius:
                x, y = self.getCoords()
                x2,y2 = other.getCoords()
                x -= x2
                y -= y2
                if d > 0:
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

    def move(self, boids,predators):
        attacking = self.attack(boids)
        separation = self.separation(predators)

        
        self.direction[0] += attacking[0] + separation[0]
        self.direction[1] += attacking[1] + separation[1]

        # Scale the direction vector to the maximum speed
        magnitude = math.sqrt(math.pow(self.direction[0], 2) + math.pow(self.direction[1], 2))
        if magnitude != 0:
            self.direction[0] = self.direction[0] / magnitude * self.maxSpeed
            self.direction[1] = self.direction[1] / magnitude * self.maxSpeed

    def bigger(self, boids):
        for other in boids:
            d = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
            if other != self and d < self.size:
                self.size += 1
                self.health += 5
                return self.size, self.health
            
        return self.size, self.health

    def die(self):
        if self.health <= 0:
                return True
            
        return False

class birdy:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = [0, 0]
        self.maxSpeed = 3
        self.color = random.randint(1,10)

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
        radius = 50
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
        radius = 50
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
        radius = 35
        steering = [0, 0]
        total = 0
        for other in boids:
            d = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
            if other != self and d < radius:
                x, y = self.getCoords()
                x2,y2 = other.getCoords()
                x -= x2
                y -= y2
                if d > 0:
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

    def attract(self, target, attraction_radius):
        steering = [0, 0]
        x, y = self.getCoords()
        target_x, target_y = target.getCoords()
        
        distance = math.sqrt(math.pow(target_x - x, 2) + math.pow(target_y - y, 2))
        if distance <= attraction_radius:
            # Calculate the direction towards the target
            steering[0] = target_x - x
            steering[1] = target_y - y
            
            magnitude = math.sqrt(math.pow(steering[0], 2) + math.pow(steering[1], 2))
            if magnitude != 0:
                # Normalize the attraction vector
                steering[0] /= magnitude
                steering[1] /= magnitude
        
        return steering
    
    def evade(self, predators):
        steering = [0, 0]
        total = 0
        for predator in predators:
            radius = predator.size + 80
            d = math.sqrt(math.pow(self.x - predator.x, 2) + math.pow(self.y - predator.y, 2))
            if predator != self and d < radius:
                x, y = self.getCoords()
                x2,y2 = predator.getCoords()
                x -= x2
                y -= y2
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
    
    def colorChange(self, boids):
        radius = 50
        self.color = random.randint(1,10)  # Reset the color to the default value

        for other in boids:
            if other != self:
                d = math.sqrt(math.pow(self.x - other.x, 2) + math.pow(self.y - other.y, 2))
                if d < radius:
                    self.color = other.color  # Set the color to a unique value
                    break

        return self.color

    def flock(self, boids, target, attraction_radius, predators):
        alignment = self.align(boids)
        cohesion = self.cohesion(boids)
        separation = self.separation(boids)
        attraction = self.attract(target, attraction_radius)
        evasion = self.evade(predators)
        
        # Update the direction based on alignment, cohesion, separation, and attraction
        self.direction[0] += separation[0] + cohesion[0] + alignment[0] + attraction[0] + evasion[0]
        self.direction[1] += separation[1] + cohesion[1] + alignment[1] + attraction[1] + evasion[1]

        # Scale the direction vector to the maximum speed
        magnitude = math.sqrt(math.pow(self.direction[0], 2) + math.pow(self.direction[1], 2))
        if magnitude != 0:
            self.direction[0] = (self.direction[0] / magnitude) * self.maxSpeed
            self.direction[1] = (self.direction[1] / magnitude) * self.maxSpeed
    
    def die(self, predators):
        for predator in predators:
            d = math.sqrt(math.pow(self.x - predator.x, 2) + math.pow(self.y - predator.y, 2))
            if predator != self and d < 10:
                return True
            
        return False

def initbirdies(amt_birdies, width, height):
    birdies = []
    for _ in range(amt_birdies):
        x = random.randint(0, width)
        y = random.randint(0, height)
        c = birdy()
        c.setCoords(x, y)
        birdies.append(c)
    return birdies

def initPredator(amt_predators, width, height):
    predators = []
    for _ in range(amt_predators):
        x = random.randint(0, width)
        y = random.randint(0, height)
        p = predator()
        p.setCoords(x, y)
        predators.append(p)
    return predators

def inittarget():
    x = pyxel.mouse_x
    y = pyxel.mouse_y
    p = target()
    p.setCoords(x, y)
    return p

class App:
    def __init__(self):
        pyxel.init(800, 800)
        self.birdies = initbirdies(AMT_OF_birdies, 800, 800)
        self.target = inittarget()
        self.predators = initPredator(AMT_OF_PREDATORS, 800, 800)

        # Create a quadtree and insert birdies into it
        self.quadtree = qt.QuadTree(qt.Square(0, 0, 800, 800), 2)
        for birdy in self.birdies:
            self.quadtree.insert(birdy)
        
        pyxel.run(self.update, self.draw)


    def update(self):
        #if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        #    new_birdy = self.birdy()
        #    new_birdy.setCoords(pyxel.mouse_x, pyxel.mouse_y)
        #    self.birdies.append(new_birdy)
        #    self.quadtree.insert(new_birdy)

        self.target.setCoords(pyxel.mouse_x, pyxel.mouse_y)
        
        for birdy in self.birdies:
            direction = birdy.getDir()
            x, y = birdy.getCoords()
            
            # Update the position based on the assigned direction
            new_x = x + direction[0] 
            new_y = y + direction[1]
            
            # Wrap around the screen if the new position goes out of bounds
            new_x %= 800
            new_y %= 800
            
            birdy.setCoords(new_x, new_y)
            
            # Retrieve neighboring birdies from the quadtree
            neighbors = self.quadtree.query_range(birdy.getCoords(), 30)
            
            # Apply alignment, cohesion, and separation behaviors
            birdy.flock(neighbors, self.target, 100, self.predators)
            
            
            if birdy.die(self.predators):
                self.birdies.remove(birdy)
            
        if pyxel.frame_count % 30 == 0:
            for predator in self.predators:
                predator.health -= 2

        for predator in self.predators:
            direction = predator.getDir()
            x, y = predator.getCoords()
            
            # Update the position based on the assigned direction
            new_x = x + direction[0] 
            new_y = y + direction[1]
            
            # Wrap around the screen if the new position goes out of bounds
            new_x %= 800
            new_y %= 800
            
            predator.setCoords(new_x, new_y)
            predator.move(self.birdies,self.predators)
            if predator.die():
                self.predators.remove(predator)


    def draw(self):
        pyxel.cls(0)
        
        for birdy in self.birdies:
            x, y = birdy.getCoords()
            color = birdy.colorChange(self.birdies)
            pyxel.circ(x, y, 4, int(color))
                    
        for predator in self.predators:
            x, y = predator.getCoords()
            if predator.size < 30:
                size,health = predator.bigger(self.birdies)
            else:
                size = predator.size
                health = predator.health
            pyxel.circ(x, y, size, 12)
            pyxel.text(x - (size * 2),y - (size * 3),"health: " + str(health),7)
            pyxel.rectb(x - (size*1.5),y - (size*2),size*3,size/2,7)
            pyxel.rect(x - (size*1.5),y - (size*2),health/3,size/2,8)

        x, y = self.target.getCoords()
        pyxel.circ(x, y, 2, 7)


        p = f"POPULATION {str(len(self.birdies)):}"
        pr = f"PREDATORS {str(len(self.predators)):}"
        pyxel.text(5, 4, p, 7)
        pyxel.text(5, 12, pr, 7)

App() 

    # could TODO 
        #change speeds based on cluster
        #genetic algorithm 
        #quad tree implementation
        #actual game mechanics
        #hunter


    #should TODO

        #ok no more stuff to implement other than the quadtree integration