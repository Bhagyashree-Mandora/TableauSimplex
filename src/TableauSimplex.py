import numpy as np


class TableauSimplex:
    def __init__(self, T, B_idx):
        self.T = T
        self.B_idx = B_idx

    def is_optimal(self, z):
        for x in np.nditer(z):
            if x < 0:
                return False
        return True

    def compute_entering_variable(self, z):
        min_ev = 999999999
        min_index = -1
        idx = 0
        for x in np.nditer(z):
            if x < min_ev:
                min_ev = x
                min_index = idx
            idx += 1
        if min_index is not -1:
            return min_index

    def min_ratio_test(self, b, ev):
        min_ratio = 999999999
        min_index = -1
        idx = 0
        for x, y in np.nditer([b, ev]):
            if y <= 0:
                idx += 1
                continue
            ratio = x / y
            # if 0 < ratio < min:
            if ratio < min_ratio:
                min_ratio = ratio
                min_index = idx
            idx += 1
        if min_index is not -1:
            return min_index

    def pivot(self, T, ev_idx, dv_idx):
        pivot_val = T[dv_idx][ev_idx]
        T[dv_idx] = [(x / pivot_val) for x in T[dv_idx]]
        for i in range(T.shape[0]):
            if i != dv_idx:
                multiple = T[i][ev_idx]
                T[i] = [(x - multiple*y) for x, y in zip(T[i], T[dv_idx])]
        return T

    def is_unbounded(self, ev):
        for x in np.nditer(ev):
            if x > 0:
                return False
        return True

    def get_b(self, T):
        b = []
        for i in range(1, T.shape[0]):
            b.append(T[i][-1])
        return b

    def get_ev(self, T, ev_idx):
        ev = []
        for i in range(1, T.shape[0]):
            ev.append(T[i][ev_idx])
        return ev

    def update_B_idx(self, B_idx, ev_idx, dv_idx):
        B_idx[dv_idx] = ev_idx
        return B_idx

    def do_simplex(self):
        while True:
            z = self.T[0][:-1]
            b = self.get_b(self.T)

            if self.is_optimal(z):
                print "\nOptimal solution found.."
                b = ['z', [('x' + str(x)) for x in self.B_idx]]
                print "Row names:"
                print b
                print self.T
                return self.T

            ev_idx = self.compute_entering_variable(z)
            ev = self.get_ev(self.T, ev_idx)

            if self.is_unbounded(ev):
                raise Exception("\nSolution is unbounded!")

            dv_idx = self.min_ratio_test(b, ev) + 1  # +1 to min ratio index to account for row R0 i.e. z in tableau
            # dv = self.T[dv_idx][:-1]

            self.B_idx = self.update_B_idx(self.B_idx, ev_idx, (dv_idx-1)) # -1 in dv_idx to get the index from B_idx

            self.T = self.pivot(self.T, ev_idx, dv_idx)




print "\nProblem 2:"

print "\nLet x0 be total acres of crop A, x1 be total acres of crop B"

T = np.array([
    [-170, -190, 0, 0, 0, 0],
    [1, 2, 1, 0, 0, 3000],
    [90, 60, 0, 1, 0, 150000],
    [1, 1, 0, 0, 1, 2000]],
    dtype=np.float64)

tableau_simplex = TableauSimplex(T, [2, 3, 4])
tableau_simplex.do_simplex()

print "\nFrom the tableau, optimal value of z (profit) is 360,000."
print "The areas under crop A and B are 1000 acres each."
print "..................................................."

print "\nProblem 2.1: Increasing total person-days by 100"
print "The tableau now becomes:"

T = np.array([
    [-170, -190, 0, 0, 0, 0],
    [1, 2, 1, 0, 0, 3100],
    [90, 60, 0, 1, 0, 150000],
    [1, 1, 0, 0, 1, 2000]],
    dtype=np.float64)

tableau_simplex = TableauSimplex(T, [2, 3, 4])
tableau_simplex.do_simplex()

print "\nz (profit) is now 362,000. Thus, increase in revenue is $2000."
print "..................................................."

print "\nProblem 2.2: Increasing total capital by 100"
print "The tableau now becomes:"

T = np.array([
    [-170, -190, 0, 0, 0, 0],
    [1, 2, 1, 0, 0, 3000],
    [90, 60, 0, 1, 0, 150100],
    [1, 1, 0, 0, 1, 2000]],
    dtype=np.float64)

tableau_simplex = TableauSimplex(T, [2, 3, 4])
tableau_simplex.do_simplex()

print "\nz (profit) is now 360,000. Thus, there is no change in revenue."
print "..................................................."

print "\nProblem 2.3: What is more valuable? Person-days or capital?"
print "From 2.1 and 2.2, we see person-days are more valuable since an increase in it causes increase in the revenue."
print "-----------------------------------------------------------------------------------"


print "\n\nProblem 3:"

print "\nLet x0 be total number of large muffins, x1 be total number of small muffins"

T = np.array([
    [-0.25, -0.1, 0, 0, 0],
    [4, 1, 1, 0, 300],
    [2, 1, 0, 1, 310]],
    dtype=np.float64)

tableau_simplex = TableauSimplex(T, [2, 3])
tableau_simplex.do_simplex()

print "\nFrom the tableau, optimal value of z (profit) is $19.5"
print "Make x0 = 70 (large muffins) and x1 = 20 (small muffins)"
print "..................................................."

print "\nProblem 3.1: If dough is increased, at what point does profit stops rising?"
print "The profit keeps increasing till dough is 320, revenue is 20."
print "..................................................."

print "\nProblem 3.2: If bran is increased, at what point does profit stops rising?"
print "The profit keeps increasing till bran is 300, revenue is 30."
print "-----------------------------------------------------------------------------------"


print "\n\nProblem 4:"

print "\nConverting the minimization problem into its maximization dual (see attachment), we get the following tableau:"

T = np.array([
    [0, 0, 0, -250, -500, -9, 0],
    [1, 0, 0, 10, 10, 0.3, 60],
    [0, 1, 0, 40, 20, 0.2, 50],
    [0, 0, 1, 60, 30, 0.6, 90]],
    dtype=np.float64)

tableau_simplex = TableauSimplex(T, [0, 1, 2])
tableau_simplex.do_simplex()

print "\n z = [[  0.00000000e+00   5.00000000e+00   1.33333333e+01   " \
      "7.50000000e+02  0.00000000e+00   0.00000000e+00   1.45000000e+03]"
print "Thus, Ann should eat x0 = 0 (apples), x1 = 5 (oranges), x2 = 13.33 (bananas) for z= 1450 (calories), "
