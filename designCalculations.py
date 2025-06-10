LU_flow = [[1.5,3,5,10,20,30,40,50,70,100,200,400,800,1000,1500,3000,5000,8000],
           [0.1,0.15,0.2,0.3,0.45,0.58,0.7,0.8,0.98,1.3,2.2,3.5,5.8,7,9,15,20,30]
           ]

Diameters = [0.16,0.11,0.09,0.075,0.063,0.05,0.04,0.032,0.025,0.02,0.016]

LU_Fixtures = {'Wash Hand Basin':2, 'Water Closet':2, 'Kitchen Sink':5, 'Shower Head':3, 'Urinal Flush Valve':1}

DU_Fixtures = {'Wash Hand Basin':0.3, 'Water Closet':1.7, 'Kitchen Sink':1.3, 'Urinal Flush Valve':0.4}

DU_constant = {'Public':0.7, 'Private':0.5}

DUdiameter_flow = [[0.075, 0.1, 0.15], [2.6, 5.2, 12.4]]

Pipe_types_length = {'Pipe Diameter': [10, 12, 16, 20, 25, 32, 40, 50, 63, 75, 90, 100],
                     'Elbows 90': [0.7, 0.9, 1.1, 1.3, 1.6, 2.0, 2.3, 2.6, 2.8, 3.4, 3.7, 4.0],
                     'Elbows 45': [0.1, 0.2, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.2, 1,6, 1.7],
                     'Bend': [0.9, 0.9, 1.1, 1.3, 1.6, 2.0, 2.3, 2.6, 2.8, 3.4, 3.7, 4.0],
                     'Tee Line Flow': [0.2, 0.4, 0.5, 0.7, 1.0, 1.4, 1.7, 2.3, 2.8, 3.7, 4.5, 5.2],
                     'Tee Branch': [0.7, 1.1, 1.3, 1.6, 2.0, 2.7, 3.0, 3.7, 4.0, 5.2, 5.8, 6.4],
                     'Globe Valve': [6.4, 6.7, 6.7, 7.3, 8.8, 11.3, 12.8, 16.5, 18.9, 24.1, 31.5, 33.6],
                     'Gate Valve': [0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.4, 0.5, 0.5, 0.6, 0.7, 0.8],
                     'Check Valve': [2.2, 2.2, 2.4, 2.7, 3.4, 4.0, 4.6, 5.8, 6.7, 8.2, 9.9, 11.6],
                     'Stop Valve': [3.9, 4.6, 4.6, 4.6, 5.2, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5, 5.5],
                     'Draw Off Taps': [0.9, 1.6, 2.6, 3.6, 4.6, 0, 0, 0, 0, 0, 0, 0]}


# get total loading units from all the fixtures
# system parameter takes dictionary argument fixtures and respective loading unit for specific water system being calculated
def cal_total_load(system, fixtures):
    t=0
    for f,n in fixtures.items():
        t+=system[f]*n
    return t


'''Water Supply'''
# find corresponding value when either Loading Unit or flow_rate is given
def get_LU_flow(tab,LU=None,flow_rate=None):
    lu_list=tab[0]
    fr_list=tab[1]
    # get flow_rate from loading unit
    if LU:
        try:
            # loading unit value is on table
            ludx=lu_list.index(LU)
            flow_rate=tab[1][ludx]
        except:
            # loading unit value is not on table, use interpolation
            for n in range(len(lu_list)-1):
                if LU>lu_list[n] and LU<lu_list[n+1]:
                    flow_rate=fr_list[n+1]-(((lu_list[n + 1] - LU)*(fr_list[n+1]-fr_list[n]))/(lu_list[n+1]-lu_list[n]))
        return flow_rate
    # get loading unit from flow_rate
    if flow_rate:
        try:
            # flow rate value is on table
            fdx=tab[1].index(flow_rate)
            LU=tab[0][fdx]
        except:
            # flow rate value is not on table, use interpolation
            for n in range(len(fr_list)-1):
                if flow_rate>fr_list[n] and flow_rate<fr_list[n+1]:
                    LU=lu_list[n+1]-(((fr_list[n + 1] - flow_rate)*(lu_list[n+1]-lu_list[n]))/(fr_list[n+1]-fr_list[n]))
        return LU

def get_poss_vel(flow_rate):
    vels=[]
    for d in Diameters:
        vel=(1.273*(flow_rate/1000))/(d**2) #
        # if vel >= 1 and vel <= 1.5:
        vels+=[vel]
    return vels

def get_poss_slope(flow_rate):
    slopes=[]
    for d in Diameters:
        slope = ((3.04935 * (flow_rate/1000))/(0.849*150*(d**2.63)))**1.852
        # slope=(((0.849*(flow_rate/1000))*(d**2.63))/0.3279)**1.852
        # if vel >= 1 and vel <= 1.5:
        slopes+=[slope]
    return slopes

def watersupplyresult(fixtures):
    LU = cal_total_load(LU_Fixtures,fixtures)
    flow_rate = get_LU_flow(LU_flow,LU)
    # assuming velocity of water is 1, using the volumetric flow rate formula
    d = (1.273 * (flow_rate / 1000)) ** 0.5
    return d


'''Drainage'''
# find flow rate from Drainage Unit
def get_DU_flow(usage, fixtures):
    DU=cal_total_load(DU_Fixtures, fixtures)
    flow_rate=DU_constant[usage]*(DU**0.5)
    return flow_rate

# get diameter of piping for septic tank
def drainageresult(usage, fixtures):
    flow_rate = get_DU_flow(usage, fixtures)
    for n,f in enumerate(DUdiameter_flow[1]):
        if flow_rate <= f:
            d = DUdiameter_flow[0][n]
            break
    return d

def horizontalpipediameter(df):
    primary_stack_vent=[[75,100,150],[2.6,5.2,12.4]]

    for n,d in enumerate(primary_stack_vent[1]):
        if df <= d:
            return primary_stack_vent[0][n]
        if n==2 and df > d:
            return primary_stack_vent[0][n]


if __name__=="__main__":
    # flow_rate=5.8
    # LU=158
    LU = get_LU_flow(LU_flow,flow_rate=10)
    print('Loading Unit',LU)
    flow_rate = get_LU_flow(LU_flow,LU=158)
    print('Flow Rate',flow_rate)
    d=(1.273 * (flow_rate/1000)) ** 0.5
    print('diameter',d)

    vels = get_poss_vel(flow_rate)
    print('possible velocities', vels)

    slopes = get_poss_slope(flow_rate)
    print('possible slopes', slopes)

    fix = {'Wash Hand Basin': 3, 'Water Closet': 7, 'Kitchen Sink': 1, 'Urinary': 4}
    print('total units',cal_total_load(LU_Fixtures,fix))
