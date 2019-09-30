import urllib2
import os
import csv

# Created by Nicholas Venis 09/09/19


url = "https://www.dan.me.uk/torlist/"
hdr = {
    "User-Agent": "'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
filename = "tor_nodes.csv"

req = urllib2.Request(url, headers=hdr)


def check():
    if os.path.isfile(filename) is True:
        mode = "a"
    else:
        mode = "w"

    pull(mode)


def pull(mode):
    inp = ""

    try:
        page = urllib2.urlopen(req)
        inp = page.read()

        inp = inp.split("\n")

    except urllib2.HTTPError as e:
        print(e)
    except Exception as e:
        print("ERROR: " + str(e))

    if inp != "":
        with open(filename, mode) as out:
            writer = csv.writer(out, delimiter="\n")
            writer.writerow(inp)
            out.close()


if __name__ == '__main__':
    check()
