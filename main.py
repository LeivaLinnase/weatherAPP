import subprocess


def main():
    # Run main.py
    print("Updating weather data...")
    subprocess.run(["python", "get_data.py"], check=True)

    # Run visualize.py
    print("Creating visualization...")
    subprocess.run(["python", "visualize.py"], check=True)


if __name__ == "__main__":
    main()
