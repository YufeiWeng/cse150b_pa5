from __future__ import print_function
from queue import Empty
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 
        
        sigma = {}
        delta = []
        sigma[(-1,-1)] = 0
        # TODO: implement backtracking search. 
        while True:
            sigma, domains = self.propagate(sigma, domains)
            if sigma[(-1, -1)] != -1:
                if len(sigma.keys()) >= 82:
                    ##for spot in domains.keys():
                        ##domains[spot] = [domains[spot]]
                    return domains
                else:
                    sigma, x = self.makeDecision(sigma, domains)
                    delta.append((copy.deepcopy(sigma), x, copy.deepcopy(domains)))
                    #domains[x] = [sigma[x]]
            else:
                if len(delta) == 0:
                    return "no solution"
                else:
                    sigma, domains = self.backTrack(delta)       


        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 
        #for spot in sd_spots:
        #    domains[spot] = [1]
        #return domains
        # <- TODO: delete this block
        
    # TODO: add any supporting function you need
    
    
    def propagate(self, sigma, domains):
        
        sigma[(-1,-1)] = 0
        while True:
            for x in domains.keys():
                if x not in sigma.keys() and len(domains[x]) == 1:
                    sigma[x] = domains[x][0]
            for x in sigma.keys():
                ## (-1, -1) not in domains
                if x in domains.keys() and len(domains[x]) > 1:
                    domains[x] = [sigma[x]]
            for x in domains.keys():
                ## bug: if len(domains[x]) == 0:
                ##      TypeError: object of type 'int' has no len() 
                ## if not isinstance(domains[x], list)
                if len(domains[x]) == 0:
                    sigma[(-1, -1)] = -1
                    return sigma, domains
            ##check for rows, cols, then blocks
            for spot in domains.keys():
                peers = sd_peers[spot]
                for peer in peers:
                    if len(domains[peer]) == 1 and domains[peer][0] in domains[spot]:
                        domains[spot].remove(domains[peer][0])  
            return sigma, domains    
        return None
    
    """""
    def propagate(self, assignment, D):
        domain_key = D.keys()
        N_s = [0,1,2,3,4,5,6,7,8]
        assignment["Conflict"] = 0
        while True:
            for key in domain_key:
                if len(D[key]) == 1 and key not in assignment.keys():
                    assignment[key]=D[key][0]
            for a in assignment.keys():
                if(a != "Conflict"):
                    D[a] = [assignment[a]]
            for key in domain_key:
                if len(D[key]) == 0:
                    assignment["Conflict"] = 1
                    return assignment, D
            #If does not meet the constraint
            #Check Row
            #Check Column
            #Check Box
            check = True
            for key in domain_key:
                for n in N_s:
                    if (key[0],n) != key and len(D[(key[0],n)]) == 1:
                        if D[(key[0],n)][0] in D[key]:
                            D[key].remove(D[(key[0],n)][0])
                            check = False
                for n in N_s:
                    if (n,key[1]) != key and len(D[(n,key[1])]) == 1:
                        if D[(n,key[1])][0] in D[key]:
                            D[key].remove(D[(n,key[1])][0])
                            check = False
                i = int(key[0]/3)
                j = int(key[1]/3)
                for x in range(3):
                    for y in range(3):
                        if( (i*3)+x , (j*3)+y ) != key and len(D[( (i*3)+x , (j*3)+y ) ]) == 1:
                            if D[( (i*3)+x , (j*3)+y ) ][0] in D[key]:
                                D[key].remove(D[( (i*3)+x , (j*3)+y ) ][0])
                                check = False
            if check:
                return assignment, D
        return assignment, D
        """""
    
    def makeDecision(self, sigma, domains):
        """""
        numOfGuesses = float('inf')
        spotWeGuess = (0, 0)
        ###super wired design bug: a cant be None
        a = 88888888
        for x in domains.keys():
            if x not in sigma.keys() and len(domains[x]) > 1:
                if len(domains[x]) < numOfGuesses:
                   a = domains[x][0]
                   spotWeGuess = x
        sigma[spotWeGuess] = a
        return sigma, spotWeGuess
        """""
        
        for x in domains.keys():
            if x not in sigma.keys():
                #if len(domains[x]) == 0:
                #    sigma[x] = 0
                #    return sigma, x
                #else:
                    sigma[x] = domains[x][0]
                    return sigma, x

        
        """""
        keys = domains.keys()
        a = sigma.keys()
        min_choices = 9
        choice_key = 0
        for key in keys:
            if len(domains[key]) < min_choices and key not in a and len(domains[key]) > 1:
                min_choices = len(domains[key])
                choice_key = key

        sigma[choice_key] = random.choice(domains[choice_key])
        return sigma, choice_key
        """""

    def backTrack(self, delta):
        sigma, x, domains = delta.pop()
        a = sigma.pop(x)
        domains[x].remove(a)
        return sigma, domains
        
    #### The following templates are only useful for the EC part #####
    
    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
