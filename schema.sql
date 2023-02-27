CREATE TABLE user (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  profile_pic TEXT NOT NULL
);

CREATE TABLE games (
  team_num TEXT NOT NULL,
  game_num TEXT NOT NULL,
  game_type TEXT NOT NULL,
  scouter_name TEXT NOT NULL
);