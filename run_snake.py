import subprocess

output_file = "statistics/hamilton_cycle"
game_path = "/home/ivan/PyCharm/PycharmProjects/RP/Snake_AI/.venv/bin/python"
snake_game_script = "/home/ivan/PyCharm/PycharmProjects/RP/Snake_AI/snake_game.py"

with open(output_file, "w") as f:
    for _ in range(300):
        print(str(_))
        result = subprocess.run([game_path, snake_game_script], capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        last_three = "\n".join(lines[-3:])
        f.write(last_three + "\n\n")
