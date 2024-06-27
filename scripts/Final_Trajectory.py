import csv
import numpy as np
import matplotlib.pyplot as plt

# Step 1: Convert the TXT file to CSV
input_txt_file = "data.txt"
output_csv_file = "data.csv"

# Define the header for the CSV file
header = [
    "DateTime", "StepIndex", "StepHeading", "StepDistanceX", "StepDistanceY", "StepDistance",
    "StepTime", "StepAmplitude", "StepDutyCycle", "StepRatio", "Altitude", "Confidence",
    "AltitudeOffset", "BatteryLevel", "RawGyroX", "RawGyroY", "RawGyroZ", "RawAccelX",
    "RawAccelY", "RawAccelZ", "RawCompassX", "RawCompassY", "RawCompassZ",
    "CorrectedGyroX", "CorrectedGyroY", "CorrectedGyroZ", "CorrectedAccelX",
    "CorrectedAccelY", "CorrectedAccelZ", "CorrectedCompassX", "CorrectedCompassY",
    "CorrectedCompassZ", "LinearAccelX", "LinearAccelY", "LinearAccelZ"
]

# Open the input and output files
with open(input_txt_file, "r") as f_in, open(output_csv_file, "w", newline="") as f_out:
    # Create a CSV writer object
    writer = csv.writer(f_out)
    
    # Write the header row
    writer.writerow(header)
    
    # Read each line from the input file
    for line in f_in:
        # Split the line by spaces
        parts = line.strip().split()
        
        # Extract date and time
        date_parts = parts[0].split("/")
        time_parts = parts[1].split(":")
        
        # Ensure date and time parts are valid
        if len(date_parts) == 3 and len(time_parts) == 3:
            # Combine date and time into proper format
            date_time = f"{date_parts[0]}/{date_parts[1]}/{date_parts[2]} {time_parts[0]}:{time_parts[1]}:{time_parts[2]}"
            
            # Extract the rest of the data
            data = parts[2:]
            
            # Split the data separated by commas into separate columns
            new_data = []
            for item in data:
                new_data.extend(item.split(","))
            
            # Combine date, time, and remaining data into a single row
            row = [date_time] + new_data
            
            # Write the row to the CSV file
            writer.writerow(row)
        else:
            print("Skipping invalid line:", line)

print("CSV conversion completed.")

# Step 2: Read the CSV file and process the trajectory data
input_csv_file = "data.csv"

# Create lists to store trajectory points
trajectory_x = [0]
trajectory_y = [0]

# Initialize position variables
x_position = 0
y_position = 0
total_distance = 0

# Open the CSV file and read data
with open(input_csv_file, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Extract parameters from each row
        step_heading = float(row['StepHeading'])
        step_distance_x = float(row['StepDistanceX'])
        step_distance_y = float(row['StepDistanceY'])
        step_distance = float(row['StepDistance'])

        # Calculate displacement components along X and Y axes
        displacement_x = step_distance_x * step_distance
        displacement_y = step_distance_y * step_distance
        
        # Update position
        x_position += displacement_x
        y_position += displacement_y
        
        # Add new position to trajectory
        trajectory_x.append(x_position)
        trajectory_y.append(y_position)
        
        # Update total distance walked
        total_distance += step_distance

# Reflect points across X-axis
reference_y = 2 * max(trajectory_y)  # Reference value
trajectory_y_reflected = [reference_y - y for y in trajectory_y]

# Plot trajectory
s=1000
plt.plot(trajectory_x[:s], trajectory_y_reflected[:s], marker='o', label='Trajectory')
#plt.plot(trajectory_x[:s], label='Trajectory_x')
#plt.plot(trajectory_y_reflected[:s], label='Trajectory_y')
# Display total distance on plot
plt.text(0, reference_y * 1.05, f'Total Distance: {total_distance:.2f} meters', fontsize=10, ha='center')

plt.title('Walk Trajectory')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.grid(True)
plt.legend()
plt.show()
