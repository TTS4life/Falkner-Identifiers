class RNG:
    def __init__(self, seed, mrateModifier = 0):
        self.seed = seed
        self.val = seed
        self.frame = 0
        self.mrateModifier = mrateModifier
        self.cache = {}

    def advance(self, n=1):
        #print(f"n is {n}, target is {self.frame+n}")
        target = self.frame + n
        if target in self.cache:
            self.frame = target
            self.val = self.cache[self.frame]
            return self
        else:
            #print("Not found in cache, advancing...")
            for x in range(0,n):
                #print(f"executing, current frame: {self.frame}")
                target = self.frame + 1
                if target in self.cache:
                    self.frame = target
                    self.val = self.cache[self.frame]
                    continue
                else:
                    self.val = ((self.val * 0x41C64E6D) + 0x6073) % (2**32)
                    self.frame += 1
                    self.cache[self.frame] = self.val
            return self
    
    def getRand(self):
        return self.val >> 16
    
    def jump(self, n):
        if n in self.cache:
            self.val = self.cache[n]
            self.frame = n
        else:
            self.val = self.seed
            self.frame = 0
            self.advance(n)