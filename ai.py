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
                if len(sigma.keys()) == 81:
                    ##for spot in domains.keys():
                        ##domains[spot] = [domains[spot]]
                    return domains
                else:
                    sigma, x = self.makeDecision(sigma, domains)
                    delta.append((copy.deepcopy(sigma), x, copy.deepcopy(domains)))
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
    
    def makeDecision(self, sigma, domains):
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
