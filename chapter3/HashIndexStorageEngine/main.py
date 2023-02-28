import argparse
from CityLog import CityLog

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Append-only log of city information")
    parser.add_argument("command", nargs="?", choices=["add", "get", "start"], help="command to run")
    parser.add_argument("--file", default="city_log.bin", help="log file name")
    args = parser.parse_args()

    log = CityLog(args.file)

    if args.command == "start":
        log.start()
        log.start_repl()
        log.stop()
    elif args.command == "add":
        city_name = input("Enter city name: ")
        population = int(input("Enter population: "))
        land_area = float(input("Enter land area: "))
        log.add_entry(city_name, population, land_area)
        print(f"Added entry for {city_name}")
    elif args.command == "get":
        city_name = input("Enter city name: ")
        log_entry = log.get_entry(city_name)
        if log_entry:
            print(f"Population of {log_entry.city_name}: {log_entry.city_info.population}")
        else:
            print(f"No entry found for {city_name}")
