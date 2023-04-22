from game_model import GameData
stats = ["402:69", "John", 1, 1234, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2,
         3, 5, 7,
         1, 2, 3,
         2, 2, 2, 2, 2, 2, "some comments"]
game_data = GameData(stats)
game_data.add_to_db()
