#-----------------------------------------------------------------------------#
# Name: visiblelines.py
# Desc: Implementation for Visible Lines Project in CS 325
# Auth: Cezary Wojcik
# Note: Input is assumed to be sorted by slope.
#       All slopes are assumed to be unique.
#       Running produces a benchmark file.
# Opts: -i, --inputfile     : specify input file (defaults to "test.txt")
#       -o, --outputfile    : specify output file for results
#       -b, --benchmarkfile : specify output file for benchmark results
#       -d, --debug           : show debug messages
#       -g, --generate        : use generated data instead of input file
#-----------------------------------------------------------------------------#

# ---- [ imports ] ------------------------------------------------------------

import getopt, numpy, random, sys
from timeit import default_timer as timer

# ---- [ globals ] ------------------------------------------------------------

debug = False
outputfile = "proj2_grp3.txt"
benchmarkfile = "benchmarks.csv"

# ---- [ classes ] ------------------------------------------------------------

class LineEquation():
  def __init__(self, slope, intercept):
    self.slope = slope
    self.intercept = intercept
    self.visible = False

  def __repr__(self):
    return "y = {0}x + {1}".format(self.slope, self.intercept)

  def value(self, x):
    return float(self.slope * x + self.intercept)

# ---- [ utility functions ] --------------------------------------------------

def handle_error(message):
  print "Error: {0}".format(message)
  sys.exit(2)

def debug_message(message):
  global debug
  if debug:
    print message

def test_case(string):
  try:
    # get float array of slopes
    start = string.index("[") + 1
    end = string.index("]")
    slopes = map(float, string[start:end].replace(" ", "").split(","))

    # get float array of intercepts
    start = string.index("[", end) + 1
    end = string.index("]", end + 1)
    intercepts = map(float, string[start:end].replace(" ", "").split(","))

    # ensure matching number of slopes and intercepts
    if len(slopes) != len(intercepts):
      raise ValueError

    # construct LineEquation objects
    equations = []
    for i in range(0, len(slopes)):
      equations.append(LineEquation(slopes[i], intercepts[i]))

    # run algorithm 1
    debug_message("Beginning Algorithm 1.")
    tstart = timer()
    #alg1(equations)
    tend = timer()
    alg1_duration = tend - tstart
    debug_message("Algorithm 1 Finished. Duration: {0} seconds."
      .format(alg1_duration))

    # run algorithm 2
    debug_message("Beginning Algorithm 2.")
    tstart = timer()
    #alg2(equations)
    tend = timer()
    alg2_duration = tend - tstart
    debug_message("Algorithm 2 Finished. Duration: {0} seconds."
      .format(alg2_duration))

    # run algorithm 3
    debug_message("Beginning Algorithm 3.")
    tstart = timer()
    #alg3(equations)
    tend = timer()
    alg3_duration = tend - tstart
    debug_message("Algorithm 3 Finished. Duration: {0} seconds."
      .format(alg3_duration))

    # run algorithm 4
    debug_message("Beginning Algorithm 4.")
    tstart = timer()
    alg4(equations)
    tend = timer()
    alg4_duration = tend - tstart
    debug_message("Algorithm 4 Finished. Duration: {0} seconds."
      .format(alg4_duration))

    # write benchmarking results
    f = open(benchmarkfile, "a")
    f.write("{0},{1},{2},{3},{4}\n".format(len(equations), alg1_duration,
      alg2_duration, alg3_duration, alg4_duration))
    f.close()

    # write actual results
    f = open(outputfile, "a")
    first = True
    for e in equations:
      if first:
        first = False
      else:
        f.write(", ")
      f.write(str(e.visible))
    f.write("\n")

  except ValueError:
    handle_error("the string '{0}' cannot be read into a test case."
      .format(string))
  except IOError:
    handle_error("failed to write to results file, '{0}'."
      .format(benchmarkfile))

# y = mx + b => -mx + 1y = b
# returns tuple (x, y) of intersection point
def intersection(line1, line2):
  a = numpy.array([[-1 * line1.slope, 1], [-1 * line2.slope, 1]])
  b = numpy.array([line1.intercept, line2.intercept])
  x, y = numpy.linalg.solve(a, b)
  return x, y

def generate_input(num):
  result = "["

  # generate slopes
  slope = -1 * num / 2
  for i in range(0, num):
    result += str(slope)
    if i != num - 1:
      result += ","
    slope += 1
  result += "],["

  # generate intercepts
  for i in range(0, num):
    result += str(random.uniform(-999999.0, 999999.0))
    if i != num - 1:
      result += ","
  result += "]"

  debug_message("Generated input of size {0}.".format(num))
  return result

# ---- [ algorithms ] ---------------------------------------------------------

# algorithm 1
def alg1(equations):
  # mark each line as visible
  for e in equations:
    e.visible = True

  # loop over each possible j < i < k (distance = k - j)
  for distance in range(2, len(equations)):
    # print
    for j in range(0, len(equations) - distance):
      k = j + distance
      for i in range(j + 1, k):
        # get intersection of lines j and k
        xjk, yjk = intersection(equations[j], equations[k])
        # if line j at xjk > line i at xjk, mark line i as not visible
        if equations[j].value(xjk) > equations[i].value(xjk):
          equations[i].visible = False

# algorithm 2
def alg2(equations):
  # mark each line as visible
  for e in equations:
    e.visible = True

  # loop over each possible j < i < k (distance = k - j)
  for distance in range(2, len(equations)):
    for j in range(0, len(equations) - distance):
      k = j + distance
      for i in range(j + 1, k):
        # skip if already marked as not visible
        if not equations[i].visible:
          continue
        # get intersection of lines j and k
        xjk, yjk = intersection(equations[j], equations[k])
        # if line j at xjk > line i at xjk, mark line i as not visible
        if equations[j].value(xjk) > equations[i].value(xjk):
          equations[i].visible = False

# algorithm 3
def alg3(equations):
  # mark each line as visible
  for e in equations:
    e.visible = True

  # visible subset starts with Y1 and Y2 ONLY for algorithm
  visible_lines = []
  for line in range(0,2):
    if equations[line].visible == True:
      visible_lines.append(equations[line])

  # range(2, len(equations-1)) gives proper indexing for elements
  # 3->end of equations
  for i in range(2, len(equations)):
    count = 1
    debug_message("i = {0}".format(i))
    visible_lines.append(equations[i])
    for k in reversed(range(1, len(visible_lines))):
      # assign largest visible k to variable
      # continue loop and find next largest visible k, assign to variable
      # break from loop
      debug_message("len of visible_lines: {0}".format(len(visible_lines)))
      if k == 1:
        break
      xkK, ykK = intersection(visible_lines[k-1], visible_lines[k-2])
      debug_message("ykK: {0}, equations[i].value(xkK): {1} xkK: {2}"
        .format(ykK, equations[i].value(xkK), xkK))
      if ykK < equations[i].value(xkK):
        equations[i-count].visible = False
        count += 1
        # remove visible line k from visible array
        del visible_lines[k-1]
      if ykK >= equations[i].value(xkK):
        break

# algorithm 4
def alg4(equations):
  def merge_visible(equations1, equations2):
    intersect_array1 = []
    intersect_array2 = []
    temp_x = 0
    temp_y = 0

    # add intersect points to the arrays
    if len(equations1) != 1:
      for i in range(0, len(equations1)):
        if ((i + 1) < len(equations1)):
          temp_x, temp_y = intersection(equations1[i], equations1[i+1])
          intersect_array1.append((temp_x, temp_y))
    if len(equations2) != 1:
      for i in range(0, len(equations2)):
        if ((i + 1) < len(equations2)):
          temp_x, temp_y = intersection(equations2[i], equations2[i+1])
          intersect_array2.append((temp_x, temp_y))
    if len(equations1) == 1 and len(equations2) == 1:
      return

    if len(equations1) + len(equations2) >= 4:
      # boolean to check to see if the left is bigger than the right
      bigger_y = False
      bigger_y = (intersect_array1[0][1] > intersect_array2[0][1])

      length1 = len(intersect_array1)
      length2 = len(intersect_array2)
      i = 0
      j = 0
      while bigger_y:
        if i == length1 or j == length2:
          break
        bigger_y = (intersect_array1[i][1] > intersect_array2[j][1])
        if intersect_array1[i][0] > intersect_array2[j][0]:
          j += 1
        else:
          i += 1
      for k in range(0, len(equations1)):
        if k > i:
          equations[k].visible = False
      for k in range(0, len(equations2)):
        if k < j:
          equations[k].visible = False
    elif len(equations1) == 2 and len(equations2) == 1:
      if intersect_array1[0][1] < equations2[0].value(intersect_array1[0][0]):
        equations1[1].visible = False
    elif len(equations2) == 2 and len(equations1) == 1:
      if intersect_array2[0][1] < equations2[0].value(intersect_array2[0][0]):
        equations2[0].visible = False

  # base case for recursive call
  if len(equations) <= 2:
    for e in equations:
      e.visible = True
    return equations
  # this breaks each subsection into 2 parts, recursively 
  else:
    debug_message("equations: {0}".format(equations))
    debug_message("left: {0} right: {1}".format(equations[:len(equations)/2],
      equations[len(equations)/2 + 1:]))
    equations_left = alg4(equations[:len(equations)/2])
    equations_right = alg4(equations[len(equations)/2 + 1:])
    debug_message("left: {0} right: {1}".format(equations_left, equations_right))
    return merge_visible(equations_left, equations_right)


# ---- [ main ] ---------------------------------------------------------------

def main(argv):
  global debug, outputfile, benchmarkfile

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:o:b:dg',
      ['inputfile=', 'outputfile=', 'benchmarkfile=', 'debug', 'generate'])
  except getopt.GetoptError as err:
    handle_error(str(err))

  inputfile = "test.txt"
  generate = False

  for o, a in opts:
    if o in ['-i', '--inputfile']:
      inputfile = a
    elif o in ['-o', '--outputfile']:
      outputfile = a
    elif o in ['-b', '--benchmarkfile']:
      benchmarkfile = a
    elif o in ['-d', '--debug']:
      debug = True
    elif o in ['-g', '--generate']:
      generate = True
    else:
      handle_error("unhandled option '{0}' detected".format(o))

  # create benchmark and results output files
  try:
    f = open(benchmarkfile, "w+")
    f.write("Number Of Equations,Algorithm 1 Duration,Algorithm 2 Duration," +
      "Algorithm 3 Duration, Algorithm 4 Duration\n")
    f.close()
    f = open(outputfile, "w+")
    f.close()
  except IOError:
    handle_error("failed to write to file, '{0}'."
      .format(benchmarkfile))

  if generate:
    debug_message("Generation Enabled.")
    gen_sizes = range(100, 901, 100) + range(1000, 9001, 1000)
    for size in gen_sizes:
      test_case(generate_input(size))
  else:
    try:
      with open(inputfile) as f:
        for line in f:
          test_case(line)
    except IOError:
      handle_error("{0} does not appear to exist.".format(inputfile))

if __name__ == "__main__":
    main(sys.argv[1:])
