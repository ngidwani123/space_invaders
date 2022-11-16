"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Avery Avila - aha68
# Neil Gidwani - nsg67
# 12/7/21
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute _vsteps: the amount of vertical steps taken
    # Invarient: _vsteps is an int >= 0

    # Attribute _rate: the current number of steps the alien should take
    #                  before its next bolt
    # Invariant: _rate is an int between 1 and BOLT_RATE

    # Attribute _rate_time: the amount of time since the alien bolt was fired
    # Invariant: _rate_time is an int >= 0

    # Attribute _ship_destroyed: determines if a ship has been destroyed or not
    # Invariant: _ship_destroyed is a bool

    # Attribute _animator: A coroutine for performing an animation
    # Invariant: _animator is a generator-based coroutine (or None)
    # ^ (above was taken from coroutine.py)

    # Attribute _old_ship: The ship object before it is destroyed
    # Invariant: _old_ship is a ship object or None

    # Attribute _curr_alien_speed: The current speed of the aliens
    # Invariant: _curr_alien_speed is an int >= 0

    # Attribute _hearts: shows the hearts (lives) the player has
    # Invariant: _hearts is a list of heart objects (the list can be empty)

    # Attribute _heart_time: the times between each full heart animation (frame
    #                        7 to next frame 0)
    # Invariant: _heart_time is an int >= 0

    # Attribute _heart_animator: A coroutine for performing a heart animation
    # Invariant: _heart_animator is a generator-based coroutine (or None)

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the wave subcontroller

        Note that this is a proper initializer, because
        Animation is NOT a subclass of GameApp (we only
        want one Window)
        """
        self._create_aliens()
        self._create_ship()
        self._time = 0
        self._vstep = 0
        self._bolts = []
        self._rate = random.randint(1, BOLT_RATE)
        self._rate_time = 0
        self._ship_destroyed = False
        self._animator = None
        self._lives = SHIP_LIVES
        self._old_ship = None
        self._curr_alien_speed = ALIEN_SPEED
        self._create_hearts()
        self._heart_time = 0
        self._heart_animator = None

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self,input, dt):
        """
        Animates the wave

        Attribute input : the input (inherited from GameApp)
        Invariant: input is an instance of GInput

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        if self._lives > 0 and self._ship is None:
            self._revive_ship()
        if self._animator is not None:    # We have something to animate
            try:
                self._animator.send(dt)       # Tell it how far to animate
            except:
                self._animator = None
        elif self._ship_destroyed:
            self._animator = self._animate_destroy_ship()
            next(self._animator)
        else:
            self._update_ship_bolt(input, dt)
        self._time += dt
        self._heart_time += dt
        if self._time > self._curr_alien_speed and self._time != 0:
                self._update_aliens(dt)
        self._update_bolts()
        self._update_hearts(dt)

    def is_ship_dead(self):
        """
        Returns if the ship is currently dead

        A ship is dead if it is type None
        """
        if self._ship is None:
            return True
        return False

    def is_game_over(self):
        """
        Returns if the game is over

        A game is over if _lives < 0 or all aliens are dead
        """
        alien_dead = True
        if self._lives <= 0:
            return True
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien_dead = False
        return alien_dead

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ship, aliens, defensive line, and bolts

        Attribute view: the game view, used in drawing
        Invariant: view is an instance of GView (inherited from GameApp)
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.draw(view)
        if self._ship is not None:
            self._ship.draw(view)
        def_line = GPath(linewidth = 5,
                        points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                        linecolor = 'grey')
        def_line.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)
        for heart in self._hearts:
            heart.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def _ship_contact(self,bolt):
        """
        Determines if there has been a collision between a ship and a bolt

        If there has been contact, the ship gets set to None

        Parameter bolt: The bolt object to check if it collides with an alien
        Precondition: bolt is a Bolt object
        """

        if self._ship is not None and self._ship.collides(bolt):
            self._ship_destroyed = True
            self._hearts.pop(-1)
            return True

    def _alien_contact(self, bolt):
        """
        Determines if there has been a collision between a alien and a bolt

        If there has been contact, the alien gets set to none

        Parameter bolt: The bolt object to check if it collides with an alien
        Precondition: bolt is a Bolt object
        """
        bolt = bolt
        for i in range(len(self._aliens)):
            for j in range(len(self._aliens[i])):
                if self._aliens[i][j] is not None:
                    if self._aliens[i][j].collides(bolt):
                        self._aliens[i][j] = None
                        self._curr_alien_speed *= .97
                        return True

    def _update_ship_bolt(self, input, dt):
        """
        A helper method for updates the ship and bolts

        This method moves the ship, creates bolts for the ship, and
        determines if alien bolts should be created

        Attribute input : the input (inherited from GameApp)
        Invariant: input is an instance of GInput

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        self._update_ship(input)
        if input.is_key_down('up') or input.is_key_down('spacebar'):
            if self._ship is not None:
                self._create_ship_bolt()
        if self._rate_time > self._rate:
            self._create_alien_bolt()
            self._rate_time = 0
            self._rate = random.randint(1, BOLT_RATE)

    def _update_ship(self, input):
        """
        Updates the ships position

        The ship can only more horizontally and is determined by
        a key input. Also makes sure the ship does not travel too far
        to the left or right.

        Attribute input : the input (inherited from GameApp)
        Invariant: input is an instance of GInput
        """
        #i took this from arrows.py in samples
        da = 0
        if input.is_key_down('left') or input.is_key_down('a'):
            da -= SHIP_MOVEMENT
        if input.is_key_down('right') or input.is_key_down('d'):
            da += SHIP_MOVEMENT

        temp = self._ship.x + da
        max_dist = GAME_WIDTH - SHIP_WIDTH//2
        min_dist = SHIP_WIDTH//2
        if temp > max_dist:
            self._ship.x = max_dist
        elif temp < min_dist:
            self._ship.x = min_dist
        else:
            self._ship.x = temp

    def _update_bolts(self):
        """
        Updates the bolt

        The bolt needs to have its position updates and it needs to be
        checked if it must be deleted or hits an alien or ship.
        """
        #i took the bottom section from pyro.py in samples
        for bolt in self._bolts:
            bolt.update_pos()

        i = 0
        while i < len(self._bolts):
            if self._bolts[i].is_gone():
                del self._bolts[i]
            elif self._alien_contact(self._bolts[i]):
                del self._bolts[i]
            elif self._ship_contact(self._bolts[i]):
                del self._bolts[i]
            else:
                i += 1

    def _update_aliens(self,dt):
        """
        Updates all aliens

        Aliens need to either move left, right, or down depending on depending
        on their _vstep and leftmost and rightmost position. Also resets _time.
        Also checks to see if aliens are below the defence line.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        if self._vstep % 2 == 0:
            right = self._rightmost() + ALIEN_H_SEP
            if right < GAME_WIDTH:
                self._move_aliens_right()
            elif right >= GAME_WIDTH:
                self._move_down()
            self._rate_time += 1
        elif self._vstep % 2 == 1:
            left = self._leftmost() - ALIEN_H_SEP
            if left > 0:
                self._move_aliens_left()
            elif left <= 0:
                self._move_down()
            self._rate_time += 1
        if self._below_defense_line():
            self._ship = None
            self._lives = 0
        self._time = dt

    def _update_hearts(self, dt):
        """
        Updates all hearts

        Hearts only get animated if _heart_time >= HEART_TIME

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """

        if self._heart_animator is not None:
            try:
                self._heart_animator.send(dt)
            except:
                self._heart_animator = None
                self._heart_time = dt
        elif self._heart_time >= HEART_TIME:
            self._heart_animator = self._animate_hearts(dt)
            next(self._heart_animator)

    def _move_aliens_right(self):
        """
        Moves all aliens to the right by ALIEN_H_WALK
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x += ALIEN_H_WALK

    def _move_aliens_left(self):
        """
        Moves all aliens to the left by ALIEN_H_WALK
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.x -= ALIEN_H_WALK

    def _rightmost(self):
        """
        Returns the x coordinate of the rightmost alien

        This method loops through the right most alien in each row
        """
        furthest = 0
        for row in self._aliens:
            alien = row[-1]
            i = -2
            while alien is None and i >= -len(row):
                alien = row[i]
                i -= 1
            if alien is not None:
                curr_x = alien.x + ALIEN_WIDTH//2
                if curr_x > furthest:
                    furthest = curr_x
        return furthest

    def _leftmost(self):
        """
        Returns the x coordinate of the leftmost alien

        This methods loops through the left most alien in each row
        """
        furthest = GAME_WIDTH
        for row in self._aliens:
            alien = row[0]
            i = 1
            while alien is None and i < len(row):
                alien = row[i]
                i += 1
            if alien is not None:
                curr_x = alien.x - ALIEN_WIDTH//2
                if curr_x < furthest:
                    furthest = curr_x
        return furthest

    def _move_down(self):
        """
        Moves all aliens down by ALIEN_V_WALK

        Also increments _vstep by 1
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.y -= ALIEN_V_WALK
        self._vstep += 1

    def _create_ship_bolt(self):
        """
        Creates a bolt object directed upwards and adds it to _bolts

        The bolt object is created above the nose of the ship, and
        is directed upwards. The bolt is only created if there is no
        other player bolts active
        """
        for bolt in self._bolts:
            if bolt.is_player_bolt():
                return None
        real_y = self._ship.y + SHIP_HEIGHT//2 + BOLT_HEIGHT//2
        self._bolts.append(Bolt(self._ship.x, real_y, 'up'))

    def _create_alien_bolt(self):
        """
        Creates a bolt object directed downwards and adds it to _bolts

        The bolt object is created just below the alien. The alien column
        is selected at random and will always find an alien to fire
        unless all aliens are None.
        """
        fire = None
        while fire is None:
            i = 1
            fire = random.randint(0,ALIENS_IN_ROW -1)
            alien = self._aliens[0][fire]
            while alien is None and i < ALIEN_ROWS:
                alien = self._aliens[i][fire]
                i+=1
            if alien is not None:
                real_y = alien.y - ALIEN_HEIGHT//2 - BOLT_HEIGHT//2
                self._bolts.append(Bolt(alien.x, real_y, 'down'))
            else:
                fire = None

    def _animate_destroy_ship(self):
        """
        Animates a vertical up or down of the image over
        ANIMATION_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        #taken from _animate_slide in coroutine.py
        self._old_ship = self._ship
        steps = 8/DEATH_SPEED
        animating = True
        total = 0
        while animating:
            dt = (yield)
            amount = steps * dt
            total += amount

            if total >= 8:
                animating = False
            else:
                self._ship.frame = int(total)
        self._ship.frame = 7
        self._ship = None
        self._lives -= 1

    def _animate_hearts(self,dt):
        """
        Aminates the hearts the player has.

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.
        """
        #taken from _animate_slide in coroutine.py
        steps = 8/HEART_SPEED
        animating = True
        total = 0
        while animating:
            dt = (yield)
            amount = steps*dt
            total += amount

            if total >= 8:
                animating = False
            else:
                for heart in self._hearts:
                    if heart is not None:
                        heart.frame = int(total)
        for heart in self._hearts:
            if heart is not None:
                heart.frame = 0

    def _revive_ship(self):
        """
        Brings the ship back to life

        This method sets the ship back to its old state before it
        was destroyed. This includes position and frame.
        """
        self._ship = self._old_ship
        self._ship.frame = 0
        self._ship_destroyed = False

    def _below_defense_line(self):
        """
        Determines if any alien is below the defense line

        Returns True if an any alien is below the defense line
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    real_y = alien.y - ALIEN_HEIGHT//2
                    if real_y - DEFENSE_LINE <= 0:
                        return True
        return False

    def _create_aliens(self):
        """
        Creates a 2d list of Alien objects

        Creates aliens from the bottom-up and starts in the bottom-left corner
        and creates from left to right. Each alien image is repeated for two
        rows and then changed to the next ALIEN_IMAGES in consts.
        """
        self._aliens = []
        real_h_sep = ALIEN_H_SEP + ALIEN_WIDTH
        real_v_sep = ALIEN_V_SEP + ALIEN_HEIGHT
        #need to start from bottom
        curr_x = ALIEN_H_SEP + ALIEN_WIDTH//2
        top_h = GAME_HEIGHT - (ALIEN_CEILING + ALIEN_HEIGHT//2)
        curr_y = top_h - (real_v_sep * (ALIEN_ROWS-1))
        index= 0
        flip = []
        for a in ALIEN_IMAGES:
            flip.insert(0,a)

        for i in range(ALIEN_ROWS):
            self._aliens.append([])
            for j in range(ALIENS_IN_ROW):
                image = ALIEN_IMAGES[((index%ALIEN_ROWS)//2)%3]
                self._aliens[i].append(Alien(curr_x,curr_y,image))
                curr_x += real_h_sep
            curr_x = ALIEN_H_SEP + ALIEN_WIDTH//2
            curr_y += real_v_sep
            index += 1

    def _create_ship(self):
        """
        Creates a ship object

        The ship is centered horizontally and located at SHIP_BOTTOM. The
        ship also uses SHIP_IMAGE in consts
        """
        self._ship = Ship(GAME_WIDTH//2, SHIP_BOTTOM)

    def _create_hearts(self):
        """
        Creates a heart object

        The hearts are located in the top right corner with the first heart
        the rightmost one
        """
        self._hearts = []
        curr_x = GAME_WIDTH - HEART_WIDTH//2
        curr_y = GAME_HEIGHT - HEART_HEIGHT//2
        for heart in range(self._lives):
            self._hearts.append(Heart(curr_x, curr_y))
            curr_x -= HEART_WIDTH
