class NotFoundHackaton(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)

class NotFoundHackatonUser(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)

class NotFoundTeam(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)

class NotFoundUserTeam(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)

class NotFoundInvite(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)

class TeamIsFull(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)