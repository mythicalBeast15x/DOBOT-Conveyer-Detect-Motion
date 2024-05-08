import DobotDllType as dType

api = dType.load()

#Connect Dobot
state = dType.ConnectDobot(api, "COM5", 115200)[0]

print('Dobot Connected...')
suction_cup = 1
enable_pump = 1
ctrl_mode = 1
pos = dType.GetPose(api)
x = pos[0]
y = pos [1]
z = pos[2]
rHead = pos[3]

print(x, y, z, rHead)


# SETUP------
dType.SetHOMEParams(api, x,  y,  z,  rHead)
dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200)
dType.SetPTPCommonParams(api, 100, 100)

isEnable = 1

infraredPort = 2 # plug IR sensor into GP4 (port 2)

dType.SetInfraredSensor(api, isEnable, infraredPort, version = 0)
counter = 0
while counter < 10:
    # Get the current status of the photocell sensor
    IRSensor = dType.GetInfraredSensor(api,infraredPort)
    # Print the current status of the IR sensor
    if IRSensor[0] == 0:
        print("The IR sensor is OFF") # no object
        dType.SetEMotor(api, 0, 1, 4000)
    else:
        print("The IR sensor is ON") # detects an object
        dType.SetEMotor(api, 0, 0, 0)

        dType.SetPTPCmd(api, 2, 197.388916015625, 57.74249267578125, 9.368743896484375, 14.711947441101074, 0)

        enable_pump = 1
        dType.SetEndEffectorSuctionCup(api, suction_cup, enable_pump, ctrl_mode)
        dType.dSleep(2000)

        dType.SetPTPCmd(api, 0, 99.04, -133.19, 85.58, -53.36, 0)

        enable_pump = 0
        dType.SetEndEffectorSuctionCup(api, suction_cup, enable_pump, ctrl_mode)

        dType.SetPTPCmd(api, 2, x, y, z, rHead, 0)
        counter+= 1
        print("counter ",counter)
        dType.dSleep(2000)