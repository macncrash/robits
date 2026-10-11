"""Rear motor bearing, 6001 (12 x 28 x 8), in the end bell."""
from steve import Component
from shapes import ball_bearing

rear_bearing = Component("rear_bearing", name="Rear bearing 6001")
outer, inner, balls = ball_bearing(6, 14, 8, -46)
rear_bearing.add("outer", outer, name="Outer race")
rear_bearing.add("inner", inner, op="new", name="Inner race")
rear_bearing.add("balls", balls, op="new", name="Balls")
rear_bearing.material("steel-1c60", finish="polished")
