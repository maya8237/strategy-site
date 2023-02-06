from db import get_db

# RESEARCH ON SECURITY ON CLASS VARS
class Game:
    def __init__(self, game_num, game_type, team_num,
                 scouter_name):
        db = get_db()
        db.execute(
            """INSERT INTO games (team_num, game_num, game_type,
                 scouter_name) """
            "VALUES (?, ?, ?, ?)",
            (team_num, game_num, game_type,
             scouter_name),
        )
        db.commit()
        # self.id = id_
        # self.game_num = game_num
        # self.game_type = game_type
        # self.team_num = team_num
        # self.form_filler = form_filler
        # self.auto_climb_lvl = auto_climb_lvl
        # self.auto_balls_amt = auto_balls_amt
        # self.create()

    #@staticmethod
    #def get(game_type, game_num):
    #    db = get_db()
        # user = db.execute(
        #     "SELECT * FROM user WHERE id = ?", (user_id,)
        # ).fetchone()
        # if not user:
        #     return None
        #
        # user = User(
        #     id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
        # )
        # return user

    # def create(self):
    #     db = get_db()
    #     db.execute(
    #         """INSERT INTO games (id, team_num, game_num, game_type,
    #              form_filler, auto_climb_lvl, auto_balls_amt) """
    #         "VALUES (?, ?, ?, ?, ?, ?, ?)",
    #         (self.id, self.team_num, self.game_num, self.game_type,
    #          self.form_filler, self.auto_climb_lvl, self.auto_balls_amt),
    #     )
    #     db.commit()
