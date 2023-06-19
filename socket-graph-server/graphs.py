from sqlalchemy import func
import matplotlib.pyplot as plt
import matplotlib
from sqlalchemy import create_engine, text, exists
from sqlalchemy.orm import sessionmaker
import os
import threading
from queue import Queue
from models import GameData

import time
import datetime

matplotlib.use('Agg')

# Define database URI
DB_URI = 'sqlite:///instance/games.db'
# Create SQLAlchemy engine and session
engine = create_engine(DB_URI)


# ALL TEAM AVERAGE CONES
def get_all_teams_average_cones(session):
    # Use the GameData model to obtain the average cone count per team
    query = (
        session
        .query(GameData.team_num,
               func.avg(GameData.cones_h + GameData.cones_m + GameData.cones_l).label('average_cone_count'))
        .group_by(GameData.team_num)
        .order_by(GameData.team_num)
    )
    result = query.all()

    # Extract team numbers and average cone counts into separate lists
    team_nums = []
    avg_cones = []
    for row in result:
        team_nums.append(str(row.team_num))
        avg_cones.append(float(row.average_cone_count))

    count = 0
    # Print the average cone counts per team
    for team_num in team_nums:
        print(f"Team {team_num}: Average Cone Count = {avg_cones[count]}")
        count += 1

    return team_nums, avg_cones


# PLOT ALL TEAM AVERAGE CONES
def plot_all_teams_average_cones(session, filename):
    team_nums, avg_cones = get_all_teams_average_cones(session)

    # Plot and display the graph
    plt.figure(figsize=(10, 5))
    plt.bar(team_nums, avg_cones)
    plt.xlabel('Team Number')
    plt.ylabel('Average Cones Per Game')
    plt.title('Average Cones Per Game for All Teams')
    plt.xticks(rotation=90)
    plt.savefig("images/" + filename)
    plt.clf()


# ALL TEAM AVERAGE FLOATS
def get_all_teams_average_floats(session):
    # Use the GameData model to obtain the average float count per team
    query = (
        session
        .query(GameData.team_num,
               func.avg(GameData.floats_h + GameData.floats_m + GameData.floats_l).label('average_float_count'))
        .group_by(GameData.team_num)
        .order_by(GameData.team_num)
    )
    result = query.all()

    # Extract team numbers and average float counts into separate lists
    team_nums = []
    avg_floats = []
    for row in result:
        team_nums.append(str(row.team_num))
        avg_floats.append(float(row.average_float_count))

    count = 0
    # Print the average float counts per team
    for team_num in team_nums:
        print(f"Team {team_num}: Average Float Count = {avg_floats[count]}")
        count += 1

    return team_nums, avg_floats


# PLOT ALL TEAM AVERAGE FLOATS
def plot_all_teams_average_floats(session, filename):
    team_nums, avg_floats = get_all_teams_average_floats(session)

    # Plot and display the graph
    plt.figure(figsize=(10, 5))
    plt.bar(team_nums, avg_floats)
    plt.xlabel('Team Number')
    plt.ylabel('Average Floats Per Game')
    plt.title('Average Floats Per Game for All Teams')
    plt.xticks(rotation=90)
    plt.savefig("images/" + filename)
    plt.clf()


# TEAM TOTAL FLOATS PER GAME
def get_total_floats_per_game(session, team_num):
    query = (
        session
        .query(GameData.game_num,
               func.sum(GameData.floats_h + GameData.floats_m + GameData.floats_l).label('total_floats'))
        .filter(GameData.team_num == team_num)
        .group_by(GameData.game_num)
        .order_by(GameData.game_num)
    )
    result = query.all()

    # Extract game_nums and total_floats_per_games into separate lists
    game_nums = []
    total_floats_per_games = []
    for row in result:
        game_nums.append(str(row.game_num))
        total_floats_per_games.append(float(row.total_floats))

    return game_nums, total_floats_per_games


# PLOT TEAM TOTAL FLOATS PER GAME
def plot_total_floats_per_team(session, team_num, filename):
    game_nums, total_floats_per_games = get_total_floats_per_game(session, team_num)

    # Calculate the average total cones
    average_cones = sum(total_floats_per_games) / len(total_floats_per_games)

    # Plot and display the graph
    plt.bar(game_nums, total_floats_per_games)
    plt.xlabel('Game Number')
    plt.ylabel('Total Floats')
    plt.title('Total Floats Per Games for Team #' + str(team_num))
    plt.axhline(y=average_cones, color='r', linestyle='--', label='Average')
    plt.legend()

    plt.savefig("images/" + filename)
    plt.clf()


# TEAM TOTAL CONES PER GAME
def get_total_cones_per_game(session, team_num):
    query = (
        session
        .query(GameData.game_num,
               func.sum(GameData.cones_h + GameData.cones_m + GameData.cones_l).label('total_cones'))
        .filter(GameData.team_num == team_num)
        .group_by(GameData.game_num)
        .order_by(GameData.game_num)
    )
    result = query.all()

    # Extract game_nums and total_cones_per_games into separate lists
    game_nums = []
    total_cones_per_games = []
    for row in result:
        game_nums.append(str(row.game_num))
        total_cones_per_games.append(float(row.total_cones))

    return game_nums, total_cones_per_games


# PLOT TEAM TOTAL CONES PER GAME
def plot_total_cones_per_team(session, team_num, filename):
    game_nums, total_cones_per_games = get_total_cones_per_game(session, team_num)

    # Calculate the average total cones
    average_cones = sum(total_cones_per_games) / len(total_cones_per_games)

    # Plot and display the graph
    plt.bar(game_nums, total_cones_per_games)
    plt.xlabel('Game Number')
    plt.ylabel('Total Cones')
    plt.title('Total Cones Per Games for Team #'+str(team_num))
    plt.axhline(y=average_cones, color='r', linestyle='--', label='Average')
    plt.legend()

    plt.savefig("images/" + filename)
    plt.clf()


# Create a lock to synchronize access to shared resources
lock = threading.Lock()


def create_graph(filename, team_num, query):
    # Create a session object for the database
    Session = sessionmaker(bind=engine)
    session = Session()

    POSSIBLE_QUERIES = ["CONES_ALL", "CONES_PER", "FLOATS_ALL", "FLOATS_PER"]

    # Check if team_num exists in the database
    team_num_exists = session.query(exists().where(GameData.team_num == team_num)).scalar()
    if not team_num_exists and "PER" in query:
        session.close()
        return None

    if query not in POSSIBLE_QUERIES:
        return None

    # Acquire the lock before accessing shared resources
    lock.acquire()

    try:
        if query == "CONES_ALL":
            plot_all_teams_average_cones(session, filename)

        elif query == "CONES_PER":
            plot_total_cones_per_team(session, team_num, filename)

        elif query == "FLOATS_ALL":
            plot_all_teams_average_floats(session, filename)

        elif query == "FLOATS_PER":
            plot_total_floats_per_team(session, team_num, filename)
    finally:
        # Release the lock after accessing shared resources
        lock.release()
        session.close()
        return "CREATED"


def generate_filename(team_num, query):
    unix_timestamp = int(time.time())
    return str(team_num) + query + str(unix_timestamp)


if __name__ == '__main__':
    create_graph("cp", engine, 3075, "CONES_PER")
    create_graph("ca", engine, 3075, "CONES_ALL")
    create_graph("fp", engine, 3075, "FLOATS_PER")
    create_graph("fa", engine, 3075, "FLOATS_ALL")
