"""Hub gearbox housing. Envelope of a second 5:1 planetary, the same tooth numbers as the
unknown-machine actuator (sun 18, planet 27, ring 72, module 1). The cut gears are not in this
housing: the actuator already has that stage, and this part is the housing and the output pilot.
"""
from steve import Component
from params import hub_y0, hub_y1

hub = Component("hub", name="Hub gearbox")
hub.cylinder("tube", 58, hub_y1 - hub_y0, at=(0, hub_y0, 0), direction=(0, 1, 0))
hub.cylinder("bore", 34, hub_y1 - hub_y0 + 8, at=(0, hub_y0 - 4, 0), direction=(0, 1, 0), op="cut")
# Pilot meets the upright's stub. It stays inside the bore radius.
hub.cylinder("pilot", 28, 4, at=(0, hub_y1, 0), direction=(0, 1, 0), op="join")
hub.material("aluminum-6061-t6", finish="anodized", color="#2a3038")
