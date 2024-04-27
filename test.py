from packages.api_calls import *

data = get_champion_counters("orianna")

print(data["data"]["championMatchupSpecificData"])
print(data["data"]["championRoleData"])

