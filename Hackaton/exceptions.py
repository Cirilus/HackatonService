class NotFoundHackaton(Exception):
    def __init__(self, text):
        self.txt = text

class NotFoundHackatonUser(Exception):
    def __init__(self, text):
        self.txt = text

class NotFoundTeam(Exception):
    def __init__(self, text):
        self.txt = text

class NotFoundUserTeam(Exception):
    def __init__(self, text):
        self.txt = text

class NotFoundInvite(Exception):
    def __init__(self, text):
        self.txt = text

class TeamIsFull(Exception):
    def __init__(self, text):
        self.txt = text