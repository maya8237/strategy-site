from sqlalchemy import Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, Session

# Define the GameData class
Base = declarative_base()


class GameData(Base):
    __tablename__ = 'game_data'
    # Define the columns of the table
    id = Column(Integer, primary_key=True, unique=True)
    timestamp = Column(String, nullable=False)
    scouter_name = Column(String, nullable=False)
    game_num = Column(Integer, nullable=False)
    team_num = Column(Integer, nullable=False)
    __table_args__ = (
        UniqueConstraint('game_num', 'team_num'),
    )
    played = Column(Integer, nullable=False)
    starting_location = Column(Integer, nullable=False)
    piece_1 = Column(Integer, nullable=False)
    piece_1_height = Column(Integer, nullable=True) # MAKE IT NOT NULLABLE WITH CHECKS
    piece_2 = Column(Integer, nullable=True)
    piece_2_height = Column(Integer, nullable=True)
    piece_3 = Column(Integer, nullable=True)
    piece_3_height = Column(Integer, nullable=True)
    auto_seesaw = Column(Integer, nullable=False)
    mobility = Column(Integer, nullable=False)
    cones_h = Column(Integer, nullable=False)
    cones_m = Column(Integer, nullable=False)
    cones_l = Column(Integer, nullable=False)
    floats_h = Column(Integer, nullable=False)
    floats_m = Column(Integer, nullable=False)
    floats_l = Column(Integer, nullable=False)
    cones_shoot = Column(Integer, nullable=False)
    floats_shoot = Column(Integer, nullable=False)
    defended = Column(Integer, nullable=False)
    defence_receive = Column(Integer, nullable=False)
    malfunction = Column(Integer, nullable=False)
    flip_over = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)

    def __init__(self, stats):
        self.timestamp = stats[0]
        self.scouter_name = stats[1]
        self.game_num = stats[2]
        self.team_num = stats[3]
        self.played = stats[4]
        self.starting_location = stats[5]
        self.piece_1 = stats[6]
        self.piece_1_height = stats[7]
        self.piece_2 = stats[8]
        self.piece_2_height = stats[9]
        self.piece_3 = stats[10]
        self.piece_3_height = stats[11]
        self.auto_seesaw = stats[12]
        self.mobility = stats[13]
        self.cones_h = stats[14]
        self.cones_m = stats[15]
        self.cones_l = stats[16]
        self.floats_h = stats[17]
        self.floats_m = stats[18]
        self.floats_l = stats[19]
        self.cones_shoot = stats[20]
        self.floats_shoot = stats[21]
        self.defended = stats[22]
        self.defence_receive = stats[23]
        self.malfunction = stats[24]
        self.flip_over = stats[25]
        self.comments = stats[26]

    def add_to_game_db(self, session):
        session.add(self)
        session.commit()

