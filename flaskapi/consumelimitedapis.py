import requests

url = "http://0.0.0.0:2224/fast"

def main():
    counter = 0
    while True:
        resp = requests.get(url)

        #got_dj = resp.json()

        print(resp.status_code)

        counter += 1

        if counter > 201:
            break

if __name__ == "__main__":
    main()
