#Collatz
class Expr :
    def __init__(self,odd=None) :
        if odd is None:
            odd = (self.eval(env)%2 != 0)
        self.odd = odd

class Operation (Expr):
    def __init__(self,l,r,odd=None) :
        self.l = l
        self.r = r
        super().__init__(odd)
    def __str__(self) :
        return "(" + str(self.l) + self.symbol + str(self.r) + ")"
    def eval(self, env) :
        return eval(str(self.l.eval(env)) + self.symbol + str(self.r.eval(env)))
class Times (Operation) :
    def __init__(self, l, r,odd=None):
        self.symbol = "*"
        super().__init__(l,r,odd)

class Divide (Operation) :
    def __init__(self, l, r,odd=None):
        self.symbol = "/"
        super().__init__(l,r,odd)
    
class Plus (Operation) :
    def __init__(self, l, r,odd=None):
        self.symbol = "+"
        super().__init__(l,r,odd)

class Const (Expr) :
    def __init__(self,val,odd=None) :
        self.val = val
        super().__init__(odd)
    def __str__(self) :
        return str(self.val)
    def eval(self,env) :
        return self.val
    
class Var (Expr) :
    def __init__(self,name,odd=None) :
        self.name = name
        super().__init__(odd)
    def __str__(self) :
        return self.name
    def eval(self, env) :
        return env[self.name]
    
def collatz_step(exp,odd) :
    if exp.odd :
        #env["n"+str(step)] = Plus(Times(Const(2),env["n"+str(step-1)]),Const(1),odd=True)
        return Plus(Times(Const(3),exp),Const(1),odd=odd)
    else :
        return Divide(exp,Const(2),odd=odd)
    
def collatz_loop(exp,length) :
    for i in range(length) :
        exp = collatz_step(exp,None)
    return exp

def solve_equation(eq, steps) :
    from sympy.solvers import solve
    solutions = solve("Eq(" + str(eq) + ",n)","n")
    int_sols = [sol for sol in solutions if (sol%1==0) & (sol > 0)]
    if len(int_sols) > 0 :
        int_sols = [sol for sol in solutions if collatz_loop(Const(sol),steps).eval({"n" : sol}) == sol]
    return int_sols

def check_solution(eq,steps) :
    solutions = solve_equation(eq, steps)
    if len(solutions) > 0 :
        print("Equation:" + str(eq))
        #print(steps)
        print("Solutions:" + str(solutions))
        return True
    else:
        return False

def continuous_search(env) :
    #eqs = []
    #steps = []
    equation = Var("n",odd=True)
    stepsize = 0
    prev_size_eqs = [equation]
    found = False
    
    while not(found) :
        this_size_eqs = []
        for eq in prev_size_eqs :
            if prev_size_eqs.index(eq)%2==0 :
                found = check_solution(eq,stepsize)
            this_size_eqs.append(collatz_step(eq,odd=True))
            #steps.append(stepsize+1)
            this_size_eqs.append(collatz_step(eq,odd=False))
            #steps.append(stepsize+1)
        stepsize +=1
        #eqs.append(this_size_eqs)
        prev_size_eqs = this_size_eqs
env = { "n" : 1 }

def check_tree(length, eq = Var("n",odd=True), branch=0) :
    if branch == length :
        return check_solution(eq,length)
    found = check_tree(length, collatz_step(eq,odd=False), branch + 1)
    if not(found | eq.odd) :
        check_tree(length, collatz_step(eq,odd=True), branch + 1)
    return False
check_tree(length = 3)
