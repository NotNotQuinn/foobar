def solution(l):
  # l is an array of strings
  # each string follows one of these formats:
  #    "N" "N.N" "N.N.N"
  # where N is a number, it is unknown if multi-digit.
  
  l = map(lambda x: map(lambda y: int(y), x.split('.')), l)
  
  l.sort(key=sort_by_index(2))
  l.sort(key=sort_by_index(1))
  l.sort(key=sort_by_index(0))
	
  l_sorted = map(format_semver, l)
  # print l_sorted
  return l_sorted

# Returns a function that returns the Nth index of a list
# If the list is too short, -1 is returned
def sort_by_index(index):
  def key(l):
    try:
    	return l[index]
    except IndexError:
      return -1
  return key
  
def format_semver(semver):
  if len(semver) == 1:
    return str(semver[0])
  elif len(semver) == 2:
    return str(semver[0])+"."+str(semver[1])
  elif len(semver) == 3:
    return str(semver[0])+"."+str(semver[1])+"."+str(semver[2])
