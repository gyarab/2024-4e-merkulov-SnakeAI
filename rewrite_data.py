import re

def multiply_time_by_4(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    total_seconds = (minutes * 60 + seconds) * 2
    new_minutes = total_seconds // 60
    new_seconds = total_seconds % 60
    return f"{new_minutes:02}:{new_seconds:02}"

input_file = "statistics/a_star"
output_file = "statistics/a_star_processed.csv"

with open(input_file, "r") as f, open(output_file, "w") as out_f:
    out_f.write("Time,Score,Moves\n")  # Add headers for Google Sheets
    lines = [line.strip() for line in f if line.strip()]  # Remove empty lines

    if len(lines) % 3 != 0:
        print("Warning: Data might be incomplete. Check the input file format.")

    for i in range(0, len(lines), 3):
        try:
            time_line = lines[i]
            score_line = lines[i+1]
            moves_line = lines[i+2]

            if re.match(r'\d{2}:\d{2}', time_line):
                time_line = multiply_time_by_4(time_line)

            out_f.write(f"{time_line},{score_line},{moves_line}\n")
        except IndexError:
            print(f"Skipping incomplete data at the end of file: {lines[i:]}")

print("Processing complete. Output saved in", output_file)
