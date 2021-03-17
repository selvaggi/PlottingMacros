import itertools

# Python code to create pair of element  
# from two list such that element  
# in pairs are not equal. 
  
# List initialization 
l =[1, 2, 3, 4] 


pairs = []
for leg1, leg2 in itertools.combinations(l,2):
     pairs.append( (leg1,leg2) )


pairs_of_pairs = []

for p in pairs:
    p1=p[0]
    p2=p[1]

    print p1,p2

    for m in pairs:
        m1=m[0]
        m2=m[1]
        
        if m1 == p1 or m1 == p2 or m2 == p1 or m2 == p2:
            continue
            
        print '     ',   m1,m2
        
        pair1 = (p1,p2)
        pair2 = (m1,m2)

        fillpair = True

        for pp in pairs_of_pairs:

           if pair1 in pp and pair2 in pp:
               fillpair = False
               #fillpair = True

        if fillpair:
            pairs_of_pairs.append( (pair1 , pair2) )

# printing output 
print(pairs_of_pairs) 
print len(pairs_of_pairs) 
