# Description: Intersections
import bpy

from math import pi, ceil, sqrt, tan, acos, asin, sin, cos, degrees

def multiply(p, scalar):
  p_result = {"x": p["x"] * scalar, "y": p["y"] * scalar}
  return p_result

def add(p1, p2):
  p_result = {"x": p1["x"] + p2["x"], "y": p1["y"] + p2["y"]}
  return p_result

def dot(p1, p2):
  return p1["x"]*p2["x"] + p1["y"]*p2["y"]

def lerp(p1, p2, t):
  p_result = {"x": p1["x"] + (p2["x"] - p1["x"]) * t, "y": p1["y"] + (p2["y"] - p1["y"]) * t}
  return p_result

def min_point(a1, a2):
  a = {"x": min(a1["x"], a2["x"]), "y": min(a1["y"], a2["y"])}
  return a

def max_point(a1, a2):
  a = {"x": max(a1["x"], a2["x"]), "y": max(a1["y"], a2["y"])}
  return a