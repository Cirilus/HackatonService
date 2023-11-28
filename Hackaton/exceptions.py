class BaseException(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)


class NotFoundHackaton(BaseException):
    pass


class NotFoundHackatonUser(BaseException):
    pass


class NotFoundTeam(BaseException):
    pass


class NotFoundUserTeam(BaseException):
    pass


class NotFoundInvite(BaseException):
    pass


class TeamIsFull(BaseException):
    pass


class NotFoundJoinRequest(BaseException):
    pass