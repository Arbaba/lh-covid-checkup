def byEq(subslist, index, equality):
    a,b = [], []
    for submission in subslist:
        print(submission)
        if submission[index] == equality:
            a.append(submission)
        else:
            b.append(submission)
    return a + b
def sortByEq(subslist, index, equality):
    a,b = [], []
    for submission in subslist:
        print(submission)
        if submission[index] == equality:
            a.append(submission)
        else:
            b.append(submission)
    return a , b
def byContains(subslist, index, value):
    a,b = [], []
    for submission in subslist:
        if value in  submission[index] :
            a.append(submission)
        else:
            b.append(submission)
    return a , b
def byNA(subslist):
    a,b = [], []
    for submission in subslist:
        if len(submission) > 4 :
            a.append(submission)
        else:
            b.append(submission)
    return a , b
def sortByHostStaff(subslist):
    yt, others = byContains(subslist, 3, 'youtube')
    return byEq(yt, 4, 'Yes') + byEq(others,4, 'Yes') 