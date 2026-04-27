# Something just for testing and playing

import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1500, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
CYAN = (80, 220, 220)
DARK_BLUE = (25, 25, 112)

FONT = pygame.font.SysFont("console", 16)

class Planet:
  AU = 149.6e6 * 1000   # Astronomical Units - The distance between the Earth to the Sun
  G = 6.67428e-11       # Constant defining gravitational behaviour / not the acceleration provoked by the gravitational atraction of Earth
  SCALE = 20 / AU      # 1 AU = 100 px
  TIMESTEP = 3600 * 24

  def __init__(self, x, y, radius, color, mass, name):
    self.x = x
    self.y = y
    self.radius = radius / 10
    self.color = color
    self.mass = mass
    self.name = name

    self.orbit = []
    self.sun = False
    self.distance_to_sun = 0

    self.x_vel = 0
    self.y_vel = 0

  def draw(self, win):
    x = self.x * self.SCALE + WIDTH / 2
    y = self.y * self.SCALE + HEIGHT / 2

    if len(self.orbit) >= 2:
      updated_points = []
      for point in self.orbit:
        x, y = point
        x = x * self.SCALE + WIDTH / 2
        y = y * self.SCALE + HEIGHT / 2

        updated_points.append((x, y))

      pygame.draw.lines(win, self.color, False, updated_points)

    if not self.sun:
      distance_text = FONT.render(f"{self.name} at {round(self.distance_to_sun/self.AU, 1)}AU", 1, WHITE)
      win.blit(distance_text, (x + self.radius, y))

    pygame.draw.circle(win, self.color, (x, y), self.radius)

  def attraction(self, other):
    other_x, other_y = other.x, other.y
    distance_x = other_x - self.x
    distance_y = other_y - self.y
    distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

    if other.sun:  # Case in wich the influence is being calculated against the sun and not against other planetary objects
      self.distance_to_sun = distance

    force = self.G * self.mass * other.mass / distance ** 2

    theta = math.atan2(distance_y, distance_x)

    force_x = math.cos(theta) * force
    force_y = math.sin(theta) * force

    return force_x, force_y
  
  def update_position(self, planets):
    total_fx = total_fy = 0

    for planet in planets:
      if self == planet:
        continue

      fx, fy = self.attraction(planet)

      total_fx += fx
      total_fy += fy

    self.x_vel += total_fx / self.mass * self.TIMESTEP
    self.y_vel += total_fy / self.mass * self.TIMESTEP

    self.x += self.x_vel * self.TIMESTEP
    self.y += self.y_vel * self.TIMESTEP

    self.orbit.append((self.x, self.y))
    ...

def main ():
  run = True

  clock = pygame.time.Clock()

  sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, "sun")
  sun.sun = True

  earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, "earth")
  earth.y_vel = 29.783 * 1000

  mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, "mars")
  mars.y_vel = 24.077 * 1000

  mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10**23, "mercury")
  mercury.y_vel = -47.4 * 1000

  venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, "venus")
  venus.y_vel = -35.02 * 1000

  jupiter = Planet(5.203 * Planet.AU, 0, 28, ORANGE, 1.898 * 10**27, "jupiter")
  jupiter.y_vel = -13.07 * 1000

  saturn = Planet(9.537 * Planet.AU, 0, 24, BROWN, 5.683 * 10**26, "saturn")
  saturn.y_vel = -9.69 * 1000

  uranus = Planet(19.191 * Planet.AU, 0, 20, CYAN, 8.681 * 10**25, "uranus")
  uranus.y_vel = -6.81 * 1000

  neptune = Planet(30.07 * Planet.AU, 0, 20, DARK_BLUE, 1.024 * 10**26, "neptune")
  neptune.y_vel = -5.43 * 1000

  planets = [
      sun,
      mercury,
      venus,
      earth,
      mars,
      jupiter,
      saturn,
      uranus,
      neptune
  ]

  while run:
    clock.tick(60)
    WIN.fill((0, 0, 0))
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False

    for planet in planets:
      planet.update_position(planets)
      planet.draw(WIN)

    pygame.display.update()

  pygame.quit()

main()
