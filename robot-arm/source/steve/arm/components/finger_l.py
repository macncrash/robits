from steve import Component
from params import w2_x, w_y, a6_z
from shapes import finger

finger_l = Component("finger_l", name="Claw finger (left)")
body, pad, pin = finger(-1, w2_x, w_y, a6_z - 42.5 - 68)
finger_l.add("body", body, name="Finger")
finger_l.add("pad", pad, op="new", name="Grip pad")
finger_l.add("pin", pin, op="new", name="Knuckle pin")

finger_l.material("aluminum-7075-t6", finish="anodized", color="#2a2e35")
finger_l.material("tpu-60a", bodies=["pad"], color="#2f6fd6")
finger_l.material("stainless-304", bodies=["pin"], finish="polished")
