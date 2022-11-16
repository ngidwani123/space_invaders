"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Avery Avila - aha68
# Neil Gidwani - nsg67
# 12/7/21
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, completed, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)
    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # Attribute lastkeys: the number of keys pressed last frame
    # Invariant: laskeys is an int >= 0

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self.lastkeys = 0

        if self._state is STATE_INACTIVE:
            label_width = self.width//2
            label_height = self.height//2
            self._text = GLabel(
                text= "Press 'S' To Start",
                font_size = 30,
                font_name = 'RetroGame.ttf'
            )
            self._text.x = label_width
            self._text.y = label_height

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._determineChange()
        elif self._state == STATE_NEWWAVE:
            self._wave = Wave()
            self._state = STATE_ACTIVE
        elif self._state == STATE_ACTIVE:
            self._text = None
            self._wave.update(self.input, dt)
            if self._wave.is_ship_dead():
                self._state = STATE_PAUSED
            if self._wave.is_game_over():
                self._state = STATE_COMPLETE
        elif self._state == STATE_PAUSED:
            self._text = GLabel(
                x = self.width//2, y = self.height//2,
                text= "Press 'S' To Continue", font_size = 30,
                font_name = 'RetroGame.ttf')
            self._determineChange()
        elif self._state == STATE_CONTINUE:
            self._text = None
            self._wave.update(self.input, dt)
            self._state = STATE_ACTIVE
        elif self._state == STATE_COMPLETE:
            if self._wave.is_ship_dead():
                self._game_loss()
            else:
                self._game_win()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        # IMPLEMENT ME
        if self._text is not None:
            self._text.draw(self.view)
        else:
            self._wave.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _determineChange(self):
        """
        Determines the current state and assigns it to
        self._state

        This method checks for a key press, and if there is
        one, changes the state to the next value.  A key
        press is when a key is pressed for the FIRST TIME.
        We do not want the state to continue to change as
        we hold down the key. The user must release the
        key and press it again to change the state.
        """
        #i took this from state.py in samples
        curr_keys = self.input.key_count
        change = curr_keys > 0 and self.lastkeys == 0
        if change:
            change = self.input.is_key_down('s')
        if change:
            # Click happened.  Change the state
            if self._state == STATE_INACTIVE:
                self._state = STATE_NEWWAVE
            elif self._state == STATE_PAUSED:
                self._state = STATE_CONTINUE
        self.lastkeys= curr_keys

    def _game_loss(self):
        """
        A helper method for STATE_COMPLETE if a player loses the game
        """
        self._text = GLabel(
            x = self.width//2, y = self.height//2,
            text= "Game Over - You Lose :(", font_size = 30,
            font_name = 'RetroGame.ttf')

    def _game_win(self):
        """
        A helper method for STATE_COMPLETE if a player wins the game
        """
        self._text = GLabel(
            x = self.width//2, y = self.height//2,
            text= "You Win!", font_size = 30,
            font_name = 'RetroGame.ttf')
