import time
import requests
import statistics
import math
import random

class LatencyBenchmark:

    def __init__(self):

        self.BASE_URL = "http://127.0.0.1:5000/api/"

        self.N_REQUESTS = 100
        self.TEAMS = [
            "Paper Rex", "Bilibili Gaming", "Team Liquid", "Sentinels",
            "Wolves Esports", "Gen.G", "MIBR", "G2 Esports", "Team Heretics",
            "Xi Lai Gaming", "Rex Regum Qeon", "FNATIC", "Team Vitality",
            "GIANTX", "BBL Esports", "Karmine Corp", "Apeks",
            "FUT Esports", "KOI", "Natus Vincere", "Gentle Mates",
            "DetonatioN FocusMe", "Global Esports", "T1", "ZETA DIVISION",
            "DRX", "TALON", "Team Secret", "BOOM Esports",
            "Nongshim RedForce", "Trace Esports", "All Gamers",
            "Dragon Ranger", "NOVA Esports", "TYLOO", "Edward Gaming",
            "JD Gaming", "FunPlus Phoenix", "Titan Esports Club",
            "NRG", "KRÜ Esports", "LOUD", "FURIA", "LEVIATÁN",
            "ZETA Game Esports", "Evil Geniuses"
        ]


    def makeRequests(self, endpoint):
        latencies = []
        URL = self.BASE_URL + endpoint

        for i in range(self.N_REQUESTS):
            start = time.perf_counter()
            r = requests.get(URL)
            r.raise_for_status()
            latencies.append(time.perf_counter() - start)

        latencies.sort()

        return latencies
    
    def percentile(self, data, p):
        idx = int(len(data) * p)
        return data[min(idx, len(data) - 1)]
    
    def printResults(self, data):
        print(f"avg: {statistics.mean(data) * 1000:.2f} ms")
        print(f"p50: {self.percentile(data, 0.50) * 1000:.2f} ms")
        print(f"p95: {self.percentile(data, 0.95) * 1000:.2f} ms")
        print(f"p99: {self.percentile(data, 0.99) * 1000:.2f} ms")

    def benchmarkGetTeamRequest(self):
        t1 = random.choice(self.TEAMS)
        latencies = self.makeRequests(f"team/{t1}")
        self.printResults(latencies)

    def benchmarkGetTeamsData(self):
        t1 = random.choice(self.TEAMS)
        t2 = random.choice(self.TEAMS)
        latencies = self.makeRequests(f"team/matchup_data/{t1}/{t2}")
        self.printResults(latencies)

    def benchmarkPredict(self):
        t1 = random.choice(self.TEAMS)
        t2 = random.choice(self.TEAMS)
        latencies = self.makeRequests(f"team/predict/{t1}/{t2}")
        self.printResults(latencies)


