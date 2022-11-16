"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Avery Avila - aha68
# Neil Gidwani - nsg67
# 12/7/21
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GSprite):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP

    def __init__(self,curr_x,curr_y):
        """
        Initializes a Ship at the given location

        Parameter curr_x: the starting x coordinate
        Precondition: x is a number (int or float)

        Parameter curr_y: the starting y coordinate
        Precondition: y is a number (int or float)

        Parameter source: the .png image of the ship
        Precondition: source is a string that references a .png file
        inside of invaders
        """
        super().__init__(x = curr_x,y = curr_y, width = SHIP_WIDTH,
                        height = SHIP_HEIGHT, source = SHIP_IMAGE,
                        format = (2,4))

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this ship

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        #i took this from the assignment instructions
        if not isinstance(bolt, Bolt):
            return False
        #corners goes ((top left),(top right), (bottom left), (bottom right))
        corners =  ((bolt.x - BOLT_WIDTH//2, bolt.y + BOLT_HEIGHT//2),
                    (bolt.x + BOLT_WIDTH//2, bolt.y + BOLT_HEIGHT//2),
                    (bolt.x + BOLT_WIDTH//2, bolt.y - BOLT_HEIGHT//2),
                    (bolt.x - BOLT_WIDTH//2, bolt.y - BOLT_HEIGHT//2))
        contain = False
        for point in corners:
            if self.contains(point):
                contain = True
        return contain

    # COROUTINE METHOD TO ANIMATE THE SHIP

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,curr_x,curr_y,source):
        """
        Initializes a Alien at the given location

        Parameter curr_x: the starting x coordinate
        Precondition: x is a number (int or float)

        Parameter curr_y: the starting y coordinate
        Precondition: y is a number (int or float)

        Parameter source: the .png image of the alien
        Precondition: source is a string that references a .png file
        inside of invaders
        """
        super().__init__(x = curr_x,y = curr_y, width = ALIEN_WIDTH,
                        height = ALIEN_HEIGHT, source = source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this ship

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        #i took this from the assignment instructions
        if not isinstance(bolt, Bolt):
            return False
        #corners goes ((top left),(top right), (bottom left), (bottom right))
        corners =  ((bolt.x - BOLT_WIDTH//2, bolt.y + BOLT_HEIGHT//2),
                    (bolt.x + BOLT_WIDTH//2, bolt.y + BOLT_HEIGHT//2),
                    (bolt.x + BOLT_WIDTH//2, bolt.y - BOLT_HEIGHT//2),
                    (bolt.x - BOLT_WIDTH//2, bolt.y - BOLT_HEIGHT//2))
        contain = False
        for point in corners:
            if self.contains(point):
                contain = True
        return contain

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # Attribute _player_bolt: describes if the bolt was fired by a player
    # Invariant: _player_bolt is a bool

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setVelocity(self,direction):
        """
        Sets _velocity of the bolt

        Note that velocity will only be set to a value if direction
        is up or down

        Parameter direction: the direction of the bolt
        Precondition: direction is a string
        """
        if direction == 'up':
            self._velocity = BOLT_SPEED
            self._player_bolt = True
        elif direction == 'down':
            self._velocity = 0 - BOLT_SPEED
            self._player_bolt = False

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, curr_x, curr_y, direction):
        """
        Initializes a bolt at the given location

        Parameter curr_x: the starting x coordinate
        Precondition: x is a number (int or float)

        Parameter curr_y: the starting y coordinate
        Precondition: y is a number (int or float)

        Parameter direction: the direction of the bolt
        Precondition: direction is a string
        """
        super().__init__(x = curr_x, y = curr_y, width = BOLT_WIDTH,
                        height = BOLT_HEIGHT, linecolor = 'black',
                        fillcolor = 'magenta')
        self.setVelocity(direction)

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def is_player_bolt(self):
        """
        Returns True if the bolt was created by a player's ship

        Returns False if the bolt was created any other way
        """
        #i took this from the assignment instructions
        return self._player_bolt

    def update_pos(self):
        """
        Updates the position of the bolt

        This method only updates the y position of the bolt by _velocity
        """
        self.y += self._velocity

    def is_gone(self):
        """
        Returns True if the bolt goes beyond the boundary of the game

        The bolt needs to be between the GAME_HEIGHT and 0
        """
        #i took this from pyro.py in samples
        high = (self.y + BOLT_HEIGHT//2)
        low = (self.y - BOLT_HEIGHT//2)
        if high > GAME_HEIGHT or low < 0:
            return True
        return False


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Heart(GSprite):
    """
    A class to represent a heart that represents one life

    Hearts are a sprite
    """

    def __init__(self,curr_x,curr_y):
        """
        Initializes a Ship at the given location

        Parameter curr_x: the starting x coordinate
        Precondition: x is a number (int or float)

        Parameter curr_y: the starting y coordinate
        Precondition: y is a number (int or float)

        Parameter source: the .png image of the ship
        Precondition: source is a string that references a .png file
        inside of invaders
        """
        # THE SPRITE FOR THE HEART WAS TAKEN FROM LAB 23
        super().__init__(x = curr_x,y = curr_y, width = HEART_WIDTH,
                        height = HEART_HEIGHT, source = 'heart-sprite.png' ,
                        format = (2,4))
