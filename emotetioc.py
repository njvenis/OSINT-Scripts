import json
import os
import re
from time import gmtime, strftime

import requests
from bs4 import BeautifulSoup

filename = "emotetIocs.csv"
mode = ""
loggedIn = False
re_ip = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
re_domain = re.compile(r"(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}")
re_sha = re.compile(r"[A-Fa-f0-9]{64}")


def check():
    if os.path.isfile(filename) is True:
        mode = "a"
    else:
        mode = "w"
    list(mode)


def list(mode):
    url = "https://pastebin.com/u/jroosen"
    rex = re.compile(r'^[/][a-zA-Z0-9]{8}$')

    try:

        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        elems = soup.find_all(href=rex)
        links = []
        postTitles = []
        postURLs = []

        for elem in elems:
            if elem.find(text=re.compile(r"Emotet|emotet")):
                links.append(elem)

        for i in range(len(links)):
            postTitles.append(links[i].getText())
            postURLs.append('https://pastebin.com/raw{}'.format(links[i].attrs['href']))

        zipObj = zip(postTitles, postURLs)
        pastesDict = dict(zipObj)

        diffTitles = []

        if os.path.isfile("pastes.log"):
            temp = ""
            urls = []
            with open("pastes.log", "r") as inp:
                temp = inp.read()
                temp = temp.split("\n")

            diff = set(postTitles) - set(temp)

            if len(diff) == 0:
                exit()
            else:
                for item in diff:
                    for key, value in pastesDict.items():
                        if item in key:
                            urls.append(value)
                            diffTitles.append(key)
                index = 0
                for url in urls:

                    response = requests.get(url)
                    response.raise_for_status()
                    page = response.text
                    ips = re.findall(re_ip, page)
                    domains = re.findall(re_domain, page)

                    print(domains)

                    try:
                        domains.remove("pastebin.com")
                    except ValueError:
                        pass
                    try:
                        domains.remove("github.com")
                    except ValueError:
                        pass
                    try:
                        domains.remove("otx.alienvault.com")
                    except ValueError:
                        pass
                    try:
                        domains.remove("urlhaus.abuse.ch")
                    except ValueError:
                        pass
                    try:
                        domains.remove("host.tld")
                    except ValueError:
                        pass
                    try:
                        domains.remove("aus.ch")
                    except ValueError:
                        pass
                    try:
                        domains.remove("cape.contextis.com")
                    except ValueError:
                        pass
                    try:
                        domains.remove("twitter.com")
                    except ValueError:
                        pass
                    try:
                        domains.remove("URLHaus.ch")
                    except ValueError:
                        pass
                    try:
                        domains.remove("app.any.run")
                    except ValueError:
                        pass

                    domains = [x for x in domains if not re_ip.match(x)]

                    shas = re.findall(re_sha, page)

                    outDict = {}

                    outDict["Time"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    outDict["C2's"] = ips
                    outDict["Domains"] = domains
                    outDict["sha-256 Hashes"] = shas

                    out = json.dumps(outDict)

                    filename = diffTitles[index]
                    filename = filename.replace(" ", "_")
                    filename = filename.replace("/", "-") + ".json"

                    with open(filename, "w") as outfile:
                        json.dump(out, outfile, sort_keys=True, indent=4)
                        outfile.close()

                    index += 1

                with open("pastes.logs") as out:
                    out.write("\n".join(postTitles))
                    out.close()



        elif len(links) != 0:
            index = 0
            for url in postURLs:
                response = requests.get(url)
                response.raise_for_status()
                page = response.text
                ips = re.findall(re_ip, page)
                domains = re.findall(re_domain, page)

                try:
                    domains.remove("pastebin.com")
                except ValueError:
                    pass
                try:
                    domains.remove("github.com")
                except ValueError:
                    pass
                try:
                    domains.remove("otx.alienvault.com")
                except ValueError:
                    pass
                try:
                    domains.remove("urlhaus.abuse.ch")
                except ValueError:
                    pass
                try:
                    domains.remove("host.tld")
                except ValueError:
                    pass
                try:
                    domains.remove("aus.ch")
                except ValueError:
                    pass
                try:
                    domains.remove("cape.contextis.com")
                except ValueError:
                    pass
                try:
                    domains.remove("URLHaus.ch")
                except ValueError:
                    pass
                try:
                    domains.remove("app.any.run")
                except ValueError:
                    pass


                domains = [x for x in domains if not re_ip.match(x)]

                shas = re.findall(re_sha, page)

                outDict = {}

                outDict["Time"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                outDict["C2's"] = ips
                outDict["Domains"] = domains
                outDict["sha-256 Hashes"] = shas

                out = json.dumps(outDict)

                filename = postTitles[index]
                filename = filename.replace(" ", "_")
                filename = filename.replace("/", "-") + ".json"

                with open(filename, "w") as outfile:
                    json.dump(out, outfile, sort_keys=True, indent=4)
                    outfile.close()

                index += 1
            with open("pastes.logs", "a") as out:
                out.write("\n".join(postTitles))
                out.close()
        else:
            exit()

    except requests.HTTPError as e:
        print(e)


if __name__ == '__main__':
    check()
