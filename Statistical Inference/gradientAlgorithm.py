import numpy as np
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

'''
Ipotesi:


E[X] = 0
M: r_ij = (-0.80)^|i-j| 

'''

# Initializing test vector
X = np.asarray([4, 2])

# Correlation matrix method
def getCorrelation(iStep, jStep):
    return (-0.8)**abs(iStep - jStep)

# Building correlation matrix
observationCorrelation = [[0 for _ in range(len(X))] for _ in range(len(X))]

for i in range(len(X)):
    for j in range(len(X)):
        observationCorrelation[i][j] = getCorrelation(i, j)

observationCorrelation = np.asarray(observationCorrelation)

# Inverse of correlation matrix
mInverse = np.linalg.inv(observationCorrelation)

# Cross correlation vector
s = np.asarray([[getCorrelation(0, 2), getCorrelation(1, 2)]])

# Optimum value for a*, solving the problem exactly
aOptimum = np.inner(mInverse, s)

print("======== AUTO-CORRELATION MATRIX =======")
print(observationCorrelation)
print("======== CROSS-CORRELATION VECTOR =======")
print(s)

print("\n=========== COMPUTED a* VALUE ============")
print(aOptimum)
print("==============================")

# X_3_estimate = np.dot(aOptimum.T, X)
# print(X_3_estimate)

# Gradient Algorithm Parameters

INIT_A_VALUE = [1, 1]

a_previous = np.asarray([INIT_A_VALUE])

GAMMA = 0.1

# ========================================

xAxis, yAxis = [], []

figure = pyplot.figure("LMMSE estimator (Gradient Algorithm)")
pyplot.title(f"Gradient algorithm for subject process")
pyplot.ylabel("Estimate")
pyplot.xlabel("Iteration")

lineMMSE, = pyplot.plot(xAxis, yAxis, '-', label='LMMSE gradient algorithm')

def gradientStep(a_previous, M, s):
    a_next = a_previous - GAMMA*(np.inner(M, a_previous).T - s)

    return a_next

iteration = 1

def update(frame):
    global a_previous, observationCorrelation, s, aOptimum, iteration

    a_next = gradientStep(a_previous, observationCorrelation, s)
    a_previous = a_next

    xAxis.append(iteration)
    yAxis.append(np.linalg.norm(a_next.T - aOptimum)**2)

    iteration+=1

    lineMMSE.set_data(xAxis, yAxis)
    figure.gca().relim()
    figure.gca().autoscale_view()

    return lineMMSE

a_0 = np.asarray([[1, 1]])
a_previous = a_0
a_next = a_0


diagonalMatrix = np.eye(len(X)) - GAMMA*observationCorrelation
eigenValues = np.linalg.eigvals(observationCorrelation)

print(f"\nMAXIMAL VALUE FOR γ: {2/eigenValues.max()}")

animation = FuncAnimation(figure, update, interval=100, cache_frame_data=False)
pyplot.axhline(y=0, color='g', linestyle='-')
pyplot.legend()
pyplot.show()

print(a_previous)