# https://developers.google.com/maps/documentation/pollen/forecast?hl=en

import subprocess

# Run the curl command and capture the output
output = subprocess.run(['curl', '-X', 'GET', 'https://pollen.googleapis.com/v1/forecast:lookup?key=AIzaSyBdCar99kGIVNgU-OCNno_jgwsaE7HP2OY&location.longitude=35.32&location.latitude=32.32&days=1'], capture_output=True, text=True)

# Write the output to a text file
with open('data/pollen_forecast.txt', 'w') as file:
    file.write(output.stdout)

print("Output saved to data/pollen_forecast.txt")