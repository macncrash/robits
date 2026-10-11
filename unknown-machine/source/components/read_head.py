"""Encoder read head on the end bell, facing the code disk rim."""
from steve import Component
from shapes import box

read_head = Component("read_head", name="Encoder read head")
read_head.add("head", box(-6, 23, -58, 6, 31, -48), name="Read head")
read_head.material("pc", color="#2a7d4f")
