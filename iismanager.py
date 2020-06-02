import requests
import sys


class IisManager:
    uri = ""
    user = ""
    pwd = ""
    token = ""
    stopped = {"status": "stopped"}
    started = {"status": "started"}
    recycling = {"status": "recycling"}

    def __init__(self, uri, user, pwd):
        self.uri = uri
        self.user = user
        self.pwd = pwd

    def getHeaders(self):
        return {'Content-Type': 'application/json', 'Accept': 'application/hal+json', 'Access-Token': 'Bearer '+self.token}

    def getUrl(self, part):
        return self.uri + part

    def getServices(self):
        return requests.get(self.getUrl("api/webserver/websites"), , headers=self.getHeaders(), verify=False).json()

    def getServiceId(self, name):
        services = self.getServices()
        for s in services:
            if s['name'] == name:
                return s['id']

    def stopService(self, name):
        id = self.getServiceId(name)
        requests.patch(self.getUrl(
            "api/webserver/websites/"+id), json=self.stopped, headers=self.getHeaders(), verify=False)

    def startService(self, name):
        id = self.getServiceId(name)
        requests.patch(self.getUrl(
            "api/webserver/websites/"+id), json=self.started, headers=self.getHeaders(), verify=False)

    def getAppPools(self):
        return requests.get(self.getUrl("api/webserver/application-pools"), headers=self.getHeaders(), verify=False).json()

    def stopAppPool(self, name):
        id = self.getAppPools()
        requests.patch(self.getUrl(
            "api/webserver/application-pools/"+id), json=self.stopped, headers=self.getHeaders(), verify=False)

    def startAppPool(self, name):
        id = self.getAppPools()
        requests.patch(self.getUrl(
            "api/webserver/application-pools/"+id), json=self.started, headers=self.getHeaders(), verify=False)


def main(argv):
    if len(argv) <= 5:
        print("Args")
        exit(1)
    uri = argv[0]
    user = argv[1]
    pwd = argv[2]
    token = argv[3]
    name = argv[4]
    manager = IisManager(uri, user, pwd)

    for action in argv[5:]:
        func = getattr(manager, action)
        func(name)


if __name__ == "__main__":
    main(sys.argv[1:])
