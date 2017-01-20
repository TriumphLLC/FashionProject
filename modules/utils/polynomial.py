# Description: Intersections
import bpy

from math import log, log10, pi, ceil, sqrt, asinh, acosh, sinh, cosh, atan2, tan, acos, asin, sin, cos, radians, degrees, exp


def get_roots(coefs):
  new_coefs = simplify(init(coefs))
  if get_degree(new_coefs) == 0:
    result = []
  elif get_degree(new_coefs) == 1:
    result = get_linear_root(new_coefs)
  elif get_degree(new_coefs) == 2:
    result = get_quadratic_roots(new_coefs)
  elif get_degree(new_coefs) == 3:
    result = get_cubic_roots(new_coefs)
  else:
    result = []
  return result


def sing(r):
  if r < 0: return -1
  elif r > 0: return 1
  else: return 0


def init(coefs):
  new_coefs = []
  i = len(coefs) - 1
  while i >= 0:
    new_coefs.append(coefs[i])
    i -= 1
  return new_coefs

def get_linear_root(coefs):
  result = []
  a = coefs[1]

  if a != 0:
    result.append( -coefs[0] / a)

  return result


def get_quadratic_roots(coefs):
  result = []

  a = coefs[2]
  b = coefs[1]/a
  c = coefs[0]/a
  d = b*b - 4*a*c

  if d > 0:
    e = sqrt(d)
    result.append( 0.5 * (-b + e))
    result.append( 0.5 * (-b - e))
  elif d == 0:
    result.append( 0.5 * -b)

  return result


def get_cubic_roots(coefs):
  results = []

  c3 = coefs[3]
  c2 = coefs[2] / c3
  c1 = coefs[1] / c3
  c0 = coefs[0] / c3

  a = (3*c1 - c2*c2) / 3
  b = (2*c2*c2*c2 - 9*c1*c2 + 27*c0) / 27
  offset = c2 / 3
  discrim = b*b/4 + a*a*a/27
  halfB = b / 2

  if abs(discrim) <= exp(-6):
    disrim = 0;
        
  if discrim > 0:
    e = sqrt(discrim)

    tmp = -halfB + e
    if tmp >= 0:
        root = pow(tmp, 1/3)
    else:
        root = -pow(-tmp, 1/3)

    tmp = -halfB - e
    if tmp >= 0:
        root += pow(tmp, 1/3)
    else:
        root -= pow(-tmp, 1/3)

    results.append( root - offset )
  elif discrim < 0:
    distance = sqrt(-a/3)
    angle = atan2( sqrt(abs(discrim)), -halfB) / 3
    cos_angle = cos(angle)
    sin_angle = sin(angle)
    sqrt3 = sqrt(3)

    results.append( 2*distance*cos_angle - offset )
    results.append( -distance * (cos_angle + sqrt3 * sin_angle) - offset)
    results.append( -distance * (cos_angle - sqrt3 * sin_angle) - offset)
  else:
    if halfB >= 0:
        tmp = -pow(halfB, 1/3)
    else:
        tmp = pow(-halfB, 1/3)

    results.append( 2*tmp - offset )
    results.append( -tmp - offset )

  return results

  # result = []
  # d = coefs[3]
  # a = coefs[2]/d
  # b = coefs[1]/d
  # c = coefs[0]/d

  # Q = (a*a - 3*b) / 9
  # R = (2*a*a*a - 9*a*b + 27*c)/54
  # S = Q*Q*Q - R*R

  # if S > 0:
  #       angle = 1/3 * acos(R/sqrt(Q*Q*Q))
  #       result.append(-2 * sqrt(Q) * cos(angle) - a/3)
  #       result.append(-2 * sqrt(Q) * cos(angle + 2/3*pi) - a/3)
  #       result.append(-2 * sqrt(Q) * cos(angle - 2/3*pi) - a/3)
  # elif S < 0:
  #   if Q < 0:
  #     angle = 1/3 * asinh(abs(R)/sqrt(abs(Q*Q*Q)))
  #     result.append(-2 * sing(R) * sqrt(abs(Q)) * sinh(angle) - a/3)
  #   elif Q > 0:
  #     angle = 1/3 * acosh(abs(R)/sqrt(Q*Q*Q))
  #     result.append(-2 * sing(R) * sqrt(Q) * cosh(angle) - a/3)
  # else: 
  #   result.append(-2 * sing(R) * sqrt(Q) - a/3)
  #   result.append(sing(R) * sqrt(Q) - a/3)

  # return result


def simplify(coefs):
  coefs_result = [
    co for co in coefs if abs(co) > exp(-6)
  ]
  return coefs_result


def get_degree(coefs):
  return len(coefs) - 1


def get_roots_in_interval(coefs, min_value, max_value):
  results = []
  new_coefs = init(coefs)
  if get_degree(new_coefs) == 1:
    root = bisection(new_coefs, min_value, max_value)
    if not root == 0:
      results.append(root)
  else:
    deriv = get_derivative(new_coefs)
    droots = get_roots_in_interval(deriv, min_value, max_value)

    if len(droots) > 0:
      root = bisection(new_coefs, min_value, droots[0])
      if not root == 0:
        results.append(root)

      i = 0
      while i <= len(droots) - 2:
        root = bisection(new_coefs, droots[i], droots[i+1])
        i += 1
        if not root == 0:
          results.append(root)

      root = bisection(new_coefs, droots[len(droots)-1], max_value)
      if not root == 0:
        results.append(root)
    else:
      root = bisection(new_coefs, min_value, max_value)
      if not root == 0:
        results.append(root)

  return results


def bisection(coefs, value_min, value_max):
  min_value = evl(coefs, value_min)
  max_value = evl(coefs, value_max)
  result = 0
  if abs(min_value) <= exp(-6):
    result = value_min
  elif abs(max_value) <= exp(-6):
    result = value_max
  elif min_value*max_value <= 0:
    tmp1 = log(value_max - value_min)
    tmp2 = log(10) * 6
    iters = ceil((tmp1+tmp2) / log(2))

    i = 0
    while i < iters:
      result = 0.5 * (value_min+value_max)
      value = evl(coefs, result)
      i += 1

      if abs(value) <= exp(-6):
        break

      if value*min_value < 0:
        value_max = result
        max_value = value
      else:
        value_min = result
        min_value = value

  return result


def get_derivative(coefs):
  derivative = []

  i = 1
  while i < len(coefs):
    derivative.append(i*coefs[i])
    i += 1

  new_derivative = init(derivative)
    
  return new_derivative


def evl(coefs, x):
  result = 0
  i = len(coefs) - 1
  while i >= 0:
    result = result*x + coefs[i]
    i -= 1
  return result
    