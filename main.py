import folium
import os

# Function to plot locations on a map
def plot_locations():
    # Create a map centered around San Francisco
    map_sf = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

    # Loop over each folder in the data directory
    for folder_name in os.listdir("data"):
        folder_path = os.path.join("data", folder_name)

        # Read the location information from the loc.txt file
        loc_file = os.path.join(folder_path, "loc.txt")
        with open(loc_file, "r") as f:
            lines = f.readlines()
            latitude = float(lines[0].split(":")[1].strip())
            longitude = float(lines[1].split(":")[1].strip())

        # Add a marker for the location to the map
        folium.Marker([latitude, longitude], popup=folder_name).add_to(map_sf)

    # Save the map as an HTML file
    map_sf.save("map_sf.html")

# Call the function to plot locations on the map


from get_images import download_images


def main():
    # Use a breakpoint in the code line below to debug your script.
    download_images()
    plot_locations()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
