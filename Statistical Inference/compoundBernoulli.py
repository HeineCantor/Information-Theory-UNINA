from numpy.random import binomial
from asyncio import sleep
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation

SIMULATION_STARTING = 1
SIMULATION_STEP = 1
SIMULATION_UPDATE = 100

numberOfObservations = SIMULATION_STARTING
axisX, axisYMMSE, axisYMAP = [], [], []

betaParameter = 0.2

figure = pyplot.figure("Bernoulli process estimator")
pyplot.title(f"Estimation of a conditional Bernoulli process (β={betaParameter})")
pyplot.ylabel("Estimate")
pyplot.xlabel("# Samples")

lineMMSE, = pyplot.plot(axisX, axisYMMSE, '-', label='MMSE estimator')
lineMAP, = pyplot.plot(axisX, axisYMAP, '-', label='MAP estimator')

def update(frame):
    global numberOfObservations
    
    hammingWeight = binomial(numberOfObservations, betaParameter)
    estimateMMSE = EstimatorMMSE(hammingWeight, numberOfObservations)
    estimateMAP = EstimatorMAP(hammingWeight, numberOfObservations)

    axisX.append(numberOfObservations)
    axisYMMSE.append(estimateMMSE)
    axisYMAP.append(estimateMAP)
    numberOfObservations+=SIMULATION_STEP
    lineMMSE.set_data(axisX, axisYMMSE)
    lineMAP.set_data(axisX, axisYMAP)
    figure.gca().relim()
    figure.gca().autoscale_view()

    printErrors()

    return [lineMMSE, lineMAP]

def printErrors():
    global betaParameter

    systematicMMSE = round(abs(sum(axisYMMSE)/len(axisYMMSE) - betaParameter), 5)
    systematicMAP = round(abs(sum(axisYMAP)/len(axisYMAP) - betaParameter), 5)

    casualMMSE = round(abs(sum(axisYMMSE)/len(axisYMMSE) - betaParameter)**2, 5)
    casualMAP = round(abs(sum(axisYMAP)/len(axisYMAP) - betaParameter)**2, 5)

    print(f"SYSTEMATIC: e(MMSE)={systematicMMSE} | e(MAP)={systematicMAP} ||| MSE: e^2(MMSE)={casualMMSE} | e^2(MAP)={casualMAP} ")

def EstimatorMMSE(hammingWeight, n):
    return (hammingWeight+1)/(n+2)

def EstimatorMAP(hammingWeight, n):
    return hammingWeight/n

animation = FuncAnimation(figure, update, interval=SIMULATION_UPDATE)
pyplot.axhline(y=betaParameter, color='g', linestyle='-')
pyplot.legend()
pyplot.show()