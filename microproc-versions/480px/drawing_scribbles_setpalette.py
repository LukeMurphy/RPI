import random
def setPalette(arg, penMark):
    # arg = 1
    penMark.pointsPerLoop = 9
    penMark.linesDrawn = 0

    penMark.changeMarkWidthProb = 0.03
    penMark.incrementFactor = 0.7

    penMark.noiseX = 2
    penMark.noiseY = 4
    penMark.xRadiusDelta = 2
    penMark.yRadiusDelta = 2
    penMark.deltaRadiusXChangeProb = 0.02
    penMark.deltaRadiusYChangeProb = 0.02

    penMark.xCenter = 0
    penMark.yCenter = 0
    penMark.xOffset = 120
    penMark.yOffset = 132
    penMark.centerXDelta = 3
    penMark.centerYDelta = 4
    penMark.deltaRadiusXCenterChangeProb = 0.1
    penMark.deltaRadiusYCenterChangeProb = 0.1

    global bgColorSets, bgBoxColorSets, penColorSets
    _brt = 1.0
    if random.random() < penMark.probDarkBG:
        _brt = 0.05
    # print(f"setPalette to {arg} {_brt}")
    penMark.num = arg
    if arg == 0:
        # MATISSE 3 NUDES WITH TURTLE
        penMark.bgColorSets = [(159 / 360, 190 / 360, 0.70, 0.92, 0.45 * _brt, 0.7 * _brt), (159 / 360, 190 / 360, 0.80, 0.92, 0.45 * _brt, 0.7 * _brt)]
        penMark.bgBoxColorSets = [
            (5 / 360, 27 / 360, 0.77, 0.97, 0.1 * _brt, 0.77 * _brt),
            (215 / 360, 218 / 360, 0.77, 0.97, 0.35 * _brt, 0.87 * _brt),
            (159 / 360, 190 / 360, 0.70, 0.92, 0.45 * _brt, 0.7 * _brt),
            (159 / 360, 190 / 360, 0.80, 0.92, 0.45 * _brt, 0.7 * _brt),
        ]
        penMark.penColorSets = [
            (28 / 360, 30 / 360, 0.5, 0.99, 0.95, 0.99, 0, 0),
            (18 / 360, 20 / 360, 0.65, 0.650, 0.93, 0.99, 0, 0),
            (10 / 360, 18 / 360, 0.5, 0.50, 0.95, 0.99, 0, 0),
            (10 / 360, 18 / 360, 0.25, 0.350, 0.95, 0.99, 0, 0),
            (10 / 360, 20 / 360, 0.5, 0.750, 0.25, 0.49, 0, 0),
        ]
        penMark.linesToDrawMin = 1
        penMark.linesToDrawMax = 5
        penMark.timeDelayBeforeDrawingAgain = 7
        penMark.loopsMin = 1
        penMark.loopsMax = 5
        penMark.penSpeedMinVal = 1
        penMark.penSpeedMaxVal = 9
        penMark.radiusXMin = 15
        penMark.radiusXMax = 82
        penMark.radiusYMin = 15
        penMark.radiusYMax = 84
        penMark.height = 10
        penMark.radiusX = 124
        penMark.radiusY = 127
        penMark.minMarkWidth = 1
        penMark.maxMarkWidth = 15
        penMark.outlineProb = 0.2
    if arg == 1:
        # LAST TWOMBLY
        penMark.bgColorSets = [[40 / 360, 45 / 360, 0.3, 0.40, 0.8 * _brt, 0.80 * _brt]]
        penMark.bgBoxColorSets = [
            [40 / 360, 45 / 360, 0.3, 0.40, 0.8 * _brt, 0.80 * _brt],
            [40 / 360, 180 / 360, 0.1, 0.4, 0.5 * _brt, 1.0 * _brt],
        ]
        penMark.penColorSets = [[350 / 360, 5 / 360, 0.9, 1.0, 0.1, 0.4], [356 / 360, 5 / 360, 0.99, 1.0, 0.1, 0.4]]
        penMark.linesToDrawMin = 2
        penMark.linesToDrawMax = 5
        penMark.timeDelayBeforeDrawingAgain = 1
        penMark.loopsMax = 4
        penMark.loopsMin = 1
        penMark.penSpeedMinVal = 1
        penMark.penSpeedMaxVal = 5
        penMark.radiusXMin = 5
        penMark.radiusXMax = 180
        penMark.radiusYMin = 5
        penMark.radiusYMax = 180
        penMark.height = 10
        penMark.radiusX = 240
        penMark.radiusY = 260
        penMark.minMarkWidth = 1
        penMark.maxMarkWidth = 5
        penMark.outlineProb = 0.1
        
        penMark.noiseX = 2
        penMark.noiseY = 4
        penMark.xRadiusDelta = 1
        penMark.yRadiusDelta = 1
        penMark.deltaRadiusXChangeProb = 0.02
        penMark.deltaRadiusYChangeProb = 0.02

        penMark.xCenter = 0
        penMark.yCenter = 0
        penMark.xOffset = 320
        penMark.yOffset = 480
        penMark.centerXDelta = 3
        penMark.centerYDelta = 4
        penMark.deltaRadiusXCenterChangeProb = 0.1
        penMark.deltaRadiusYCenterChangeProb = 0.1
    if arg == 2:
        # PINK ON PINK
        _brt = 0.1
        penMark.bgColorSets = [[335 / 360, 345 / 360, 0.7, 1.0, 0.7 * _brt, 0.9 * _brt]]
        penMark.bgBoxColorSets = [[335 / 360, 345 / 360, 0.7, 1.0, 0.7 * _brt, 0.9 * _brt], [335 / 360, 350 / 360, 0.9, 1.0, 0.7 * _brt, 0.9 * _brt]]
        penMark.penColorSets = [[330 / 360, 355 / 360, 0.60, 1.0, 0.30, 1.0], [340 / 360, 40 / 360, 0.9, 1.0, 0.3, 0.950]]
        penMark.linesToDrawMin = 1
        penMark.linesToDrawMax = 3
        penMark.timeDelayBeforeDrawingAgain = 1
        penMark.loopsMin = 1
        penMark.loopsMax = 4
        penMark.penSpeedMinVal = 1
        penMark.penSpeedMaxVal = 5
        penMark.radiusXMin = 5
        penMark.radiusXMax = 18
        penMark.radiusYMin = 5
        penMark.radiusYMax = 18
        penMark.height = 10
        penMark.radiusX = 24
        penMark.radiusY = 26
        penMark.minMarkWidth = 0.5
        penMark.maxMarkWidth = 7
        penMark.outlineProb = 0.1
    if arg == 3:
        # NOIR
        _brt = 0.1
        penMark.bgColorSets = [[335 / 360, 345 / 360, 0.1, 0.10, 0.2 * _brt, 0.9 * _brt]]
        penMark.bgBoxColorSets = [[335 / 360, 345 / 360, 0.1, 0.10, 0.2 * _brt, 0.9 * _brt], [335 / 360, 345 / 360, 0.1, 0.10, 0.2 * _brt, 0.9 * _brt]]
        penMark.penColorSets = [[330 / 360, 355 / 360, 0.01, 0.1, 0.10, 1.0], [330 / 360, 355 / 360, 0.01, 0.1, 0.10, 1.0]]
        penMark.linesToDrawMax = 5
        penMark.linesToDrawMin = 1
        penMark.timeDelayBeforeDrawingAgain = 5
        penMark.loopsMin = 1
        penMark.loopsMax = 4
        penMark.penSpeedMinVal = 1
        penMark.penSpeedMaxVal = 3
        penMark.radiusXMin = 5
        penMark.radiusXMax = 18
        penMark.radiusYMin = 5
        penMark.radiusYMax = 18
        penMark.height = 10
        penMark.radiusX = 24
        penMark.radiusY = 26
        penMark.minMarkWidth = 0.75
        penMark.maxMarkWidth = 5
        penMark.outlineProb = 0.99
    if arg == 4:
        # WHITEBOARDS
        _brt = 0.5
        penMark.bgColorSets = [[335 / 360, 345 / 360, 0.1, 0.10, 0.72 * _brt, 0.9 * _brt]]
        penMark.bgBoxColorSets = [[335 / 360, 345 / 360, 0.1, 0.10, 0.72 * _brt, 0.9 * _brt], [335 / 360, 345 / 360, 0.1, 0.10, 0.72 * _brt, 0.9 * _brt]]
        penMark.penColorSets = [
            [0 / 230, 5 / 360, 0.0, 0.0, 0.0, 0.0030],
            [50 / 360, 60 / 360, 1.0, 1.0, 0.60, 0.90],
            [50 / 360, 60 / 360, 1.0, 1.0, 0.60, 0.90],
            [90 / 360, 140 / 360, 1.0, 1.0, 0.60, 0.90],
            [170 / 360, 180 / 360, 1.0, 1.0, 0.60, 0.90],
            [220 / 360, 230 / 360, 1.0, 1.0, 0.60, 0.90],
            [330 / 360, 5 / 360, 1.0, 1.0, 0.60, 0.90],
            [220 / 360, 230 / 360, 1.0, 1.0, 0.60, 0.90],
            [0 / 230, 5 / 360, 0.50, 0.60, 0.10, 0.30],
            [0 / 230, 5 / 360, 0.0, 0.0, 0.0, 0.0030],
        ]
        penMark.linesToDrawMax = 7
        penMark.linesToDrawMin = 3
        penMark.timeDelayBeforeDrawingAgain = 0.1
        penMark.loopsMin = 2
        penMark.loopsMax = 4
        penMark.penSpeedMinVal = 1
        penMark.penSpeedMaxVal = 3
        penMark.radiusXMin = 1
        penMark.radiusXMax = 8
        penMark.radiusYMin = 5
        penMark.radiusYMax = 8
        penMark.height = 10
        penMark.radiusX = 5
        penMark.radiusY = 21
        penMark.minMarkWidth = 0.75
        penMark.maxMarkWidth = 5
        penMark.outlineProb = 0.99
    if arg == 5:
        # Gyres, spirals, helix, cords, powerlines, Caduceus
        _brt = 0.75
        penMark.bgColorSets = [[35 / 360, 45 / 360, 0.1, 0.30, 0.72 * _brt, 0.9 * _brt]]
        penMark.bgBoxColorSets = [
            [35 / 360, 55 / 360, 0.1, 0.30, 0.72 * _brt, 0.9 * _brt],
            [35 / 360, 55 / 360, 0.1, 0.30, 0.72 * _brt, 0.9 * _brt],
            [35 / 360, 55 / 360, 0.3, 0.40, 0.8 * _brt, 0.80 * _brt],
            [40 / 360, 180 / 360, 0.1, 0.4, 0.5 * _brt, 1.0 * _brt],
        ]
        penMark.penColorSets = [
            [0 / 360, 5 / 360, 0.95, 1.0, 0.50, 0.530],
            [0 / 360, 5 / 360, 0.95, 1.0, 0.50, 0.530],
            [50 / 360, 60 / 360, 1.0, 1.0, 0.60, 0.90],
            [50 / 360, 120 / 360, 1.0, 1.0, 0.40, 0.50],
            [120 / 360, 180 / 360, 1.0, 1.0, 0.20, 0.50],
            [220 / 360, 230 / 360, 1.0, 1.0, 0.60, 0.90],
        ]
        penMark.linesToDrawMax = 7
        penMark.linesToDrawMin = 1
        probLineChangesColor = 0.01
        penMark.timeDelayBeforeDrawingAgain = 10.0
        penMark.loopsMin = 3
        penMark.loopsMax = 3
        penMark.penSpeedMinVal = 3
        penMark.penSpeedMaxVal = 3
        penMark.radiusXMin = 40
        penMark.radiusXMax = 90
        penMark.radiusYMin = 10
        penMark.radiusYMax = 10
        penMark.height = 64
        penMark.radiusX = 150
        penMark.radiusY = 0
        penMark.minMarkWidth = 0.75
        penMark.maxMarkWidth = 4
        penMark.outlineProb = 0.85

        penMark.xCenter = 0
        penMark.yCenter = 0
        penMark.xOffset = 32
        penMark.yOffset = 64
        penMark.centerXDelta = 0.1
        penMark.centerYDelta = 0
        penMark.deltaRadiusXCenterChangeProb = 0.01
        penMark.deltaRadiusYCenterChangeProb = 0.0

        penMark.noiseX = 1
        penMark.noiseY = 2.5
        penMark.xRadiusDelta = 1
        penMark.yRadiusDelta = 0
        penMark.deltaRadiusXChangeProb = 0.02
        penMark.deltaRadiusYChangeProb = 0.0

        #print("reset")
