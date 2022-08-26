def solution(data, n):
    # Holds counts for each id
    counts = {}

    for num in data:
        try:
            counts[str(num)] += 1
        except KeyError:
            counts[str(num)] = 1
    
    # print "Counts: " + str(counts)
    
    # Ids that should be kept
    keep_these = []
    for key in counts:
        v = counts[key]
        if v <= n:
            keep_these.append(int(key))
    
    # print "Keeping: " + str(keep_these)
    
    data_out = []
    
    for num in data:
        for keep in keep_these: 
            # print (keep, num);
            if num == keep:
               data_out.append(num)
    return data_out
