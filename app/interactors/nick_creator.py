from random import randint

from app.db_interactors.user_db_inter import UserDbInter


class NickCreator:

    def create_temp_nick(self, email):
        split_email = email.split('@')
        temp_nick = split_email[0]
        if len(temp_nick) > 12:
            temp_nick = split_email[0][0: 9]
        elif len(temp_nick) < 5:
            temp_nick = temp_nick + str(randint(100, 999))
        temp_nick = NickCreator().check_temp_nick(temp_nick)
        return temp_nick

    def check_temp_nick(self, temp_nick):
        user = UserDbInter().user_by_nick(temp_nick)
        if not user:
            return temp_nick
        else:
            while user is not None:
                del_last_signs = temp_nick[:-3]
                temp_nick = del_last_signs + str(randint(100, 999))
                user = UserDbInter().user_by_nick(nick=temp_nick)
            return temp_nick
