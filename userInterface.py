import streamlit as st
from streamlit.runtime.state.session_state import WStates

from designCalculations import get_LU_flow, get_DU_flow
from designCalculations import LU_Fixtures, DU_Fixtures, LU_flow, DU_constant, Pipe_types_length

# '''Add a data store given tabs calculate for a single section per time'''

# some variables
total_fix_app=0
total_wsfu=0
flow_rate=0
pipe_diameter=0

main_container = st.empty()
with main_container.container():
    if 'drain' not in st.session_state:
        st.session_state.drain = False
    if 'supply' not in st.session_state:
        st.session_state.supply = False

    def supply():
        st.session_state.supply = True

    def drain():
        st.session_state.drain = True

    st.button('Water Supply', on_click=supply)
    st.button('Drainage', on_click=drain)

if st.session_state.supply:
    main_container.empty()
    load_requirement = main_container.columns(2)
    with load_requirement[0]:
        st.radio("State Type", ["Private", "Public"], key="supply_space_type", label_visibility="collapsed", disabled=False,
                 horizontal=True)
    with load_requirement[1]:
        st.text_input("Section/Floor", key="supply_section_floor")
        st.text_input("Pipe Number", key="supply_pipe_number")

    # TABS
    supplyuitabs = st.tabs(["Pipe Sizing", "Pipe Length", "Head Loss", "Results Summary"])
    # Pipe Sizing
    with supplyuitabs[0]:
        Pipe_sizing_tab=st.container(border=True)
        Pipe_sizing_tab.subheader("Loading Requirement")

        Pipe_sizing_tab.markdown("##### Fixture & Appliance")
        Pipe_sizing_tab.write("Enter The Number of Fixture & Appliance:")
        Pipe_sizing_tab.container(border=True)
        fixture_appliance_results=Pipe_sizing_tab.columns(3)
        fixture_appliance=fixture_appliance_results[:2]
        pipe_sizing_results = fixture_appliance_results[2]

        with fixture_appliance[0]:
            fix_app_water_closet=st.text_input("Water Closet", key="water_closet")
            fix_app_wash_basin=st.text_input("Wash Hand Basin", key="wash_hand_basin")
            fix_app_kitchen_sink=st.text_input("Kitchen Sink", key="kitchen_sink")
            fix_app_shower_head = st.text_input("Shower Head", key="shower_head")
        with fixture_appliance[1]:
            fix_app_urinal_flush=st.text_input("Urinal Flush Valve", key="urinal_flush_valve")
            fix_app_bathtub_faucet = st.text_input("Bathhub Faucet", key="bathtub_faucet")
            fix_app_laundry_tub=st.text_input("Laundry Tube/Tray", key="laundry_tub")
            fix_app_tap_dia=st.text_input("Tap Diameter", key="tap_diameter")
            fix_app_max_velocity=st.text_input("The Maximum Velocity of Required Pipe (in/sec)", key="max_velocity_pipe")
        with pipe_sizing_results:
            # addition of fixture_appliance
            fix_app=[
                fix_app_water_closet,fix_app_wash_basin,fix_app_kitchen_sink,fix_app_shower_head,fix_app_urinal_flush,
                fix_app_bathtub_faucet,fix_app_laundry_tub
            ]
            fix_app = [int(f) if f.isdigit() else 0 for f in fix_app]
            total_fix_app = sum(fix_app)
            st.text_area("Total Fixture & Appliances", value=total_fix_app, key="total_fix_app")
            # sum of LU multiplied by single fixtures
            total_wsfu = sum([fix_app[n]*LU for n,LU in enumerate(LU_Fixtures.values())])
            st.text_area("Total WSFU (Unit Load)", value=total_wsfu, key="total_wsfu")
            # flow rate
            flow_rate=get_LU_flow(LU_flow,LU=total_wsfu)
            st.text_area("Flow Rate (L/sec)", value=flow_rate, key="flow_rate")
            # diameter when velocity is 1m/s2
            if flow_rate:
                pipe_diameter = (1.273 * (flow_rate/1000)) ** 0.5
            st.text_area("Pipe Diameter (mm)", value=pipe_diameter, key="pipe_diameter")

    # Pipe Length
    # variables
    pipelength_nocomp=0
    pipelength_flowrate=0
    pipelength_eqv=0
    pipelength_eff=0
    with supplyuitabs[1]:
        bendandvalves = st.container(border=True)
        with bendandvalves:
            st.markdown("#### Bend and Valves")
            bendandvalves_col = st.columns(5)
            bav_vals=[('Bend','piplength_bend'),('Stop Valve', 'piplength_stopvalve'),('Globe Valve','piplength_globevalve'),
                        ('Check Valve','piplength_checkvalve'),('Service Valve','piplength_servicevalve')]
            for c,v in zip(bendandvalves_col,bav_vals):
                c.checkbox(v[0],key=v[1])

        component_result = st.columns(2)
        with component_result[0].container(border=True):
            st.markdown("##### Components")
            st.markdown('**Please Enter the Types and Number of Fixtures Here**')
            # st.text_input('Elbow', key='pipelength_elbow')
            # st.text_input('Tees', key='pipelength_tees')
            # st.text_input('Taps', key='pipelength_taps')
            pipelengthcomp=st.columns(2)
            with pipelengthcomp[0]:
                st.markdown('##### Fixture Types')
                st.text_input('Elbows 90', key='pipelength_elbow90')
                st.text_input('Elbows 45', key='pipelength_elbow45')
                st.text_input('Tees', key='pipelength_tees')
                st.text_input('Taps', key='pipelength_taps')
                st.text_input('Actual Measured Pipe Run', key='pipelength_actualmeasuredrun')
            with pipelengthcomp[1]:
                st.markdown('##### Pipe Diameter')
                st.selectbox('Pipe Diameter (mm)',options=Pipe_types_length['Pipe Diameter'],label_visibility='hidden', key='elbow90')
                st.selectbox('Pipe Diameter (mm)',options=Pipe_types_length['Pipe Diameter'],label_visibility='hidden', key='elbow45')
                st.selectbox('Pipe Diameter (mm)',options=Pipe_types_length['Pipe Diameter'],label_visibility='hidden', key='tees')
                st.selectbox('Pipe Diameter (mm)', options=Pipe_types_length['Pipe Diameter'], label_visibility='hidden', key='taps')
            # with pipelengthcomp[2]:
            #     st.selectbox(label_visibility='hidden')
            #     st.selectbox(label_visibility='hidden')
            #     st.selectbox(label_visibility='hidden')
        with component_result[1].container(border=True):
            st.markdown("#### Results")
            # addition of components
            st.text_area("Total Number of Components",value=pipelength_nocomp,key='pipelength_nocomp')
            # move to top of tab
            st.text_area("Flow Rate (L/Sec)", value=pipelength_flowrate, key='pipelength_flowrate')
            # ??
            st.text_area("Equivalent Pipe Length (meters)", value=pipelength_eqv, key='pipelength_eqv')
            # sum of equivalent pipe length and actual measured run
            st.text_area("Effective Pipe Length (meters)", value=pipelength_eff, key='pipelength_eff')

    # headloss
    # variables
    headloss=0
    headloss_permissible=0
    headloss_consumed=0
    headloss_progressive=0
    with supplyuitabs[2]:
        watersource=st.radio('Water Source',['Storage Tank','Water Service Mains'])
        headloss_input_result=st.columns(2)
        with headloss_input_result[0].container(border=True):
            st.markdown("#### Data Input")
            st.markdown("##### **Enter The Head Available**")
            headloss_velocity=st.text_input("Velocity (m/sec)", key='headloss_velocity')
            headloss_diameter=st.text_input("Diameter(mm)", key='headloss_diameter')
            headloss_eff=st.text_input("Effective Pipe Length(meter)", key='headloss_eff')
            headloss_head=st.text_input("Head Available (meter)", key='headloss_head')
        with headloss_input_result[1].container(border=True):
            st.markdown("#### Results")
            # calculation in excel file
            if headloss_diameter:
                headloss_diameter = int(headloss_diameter)
                headloss = (0.9/(0.5545*headloss_diameter)**0.6935)**(1/0.5645)
            st.text_area("Head Loss (m/m run)",headloss,key='headloss')
            # Head Available/Effective Pipe Length
            if headloss_head and headloss_eff:
                headloss_head = int(headloss_head)
                headloss_eff = int(headloss_eff)
                headloss_permissible=headloss_head/headloss_eff
            st.text_area("Head Permissible (m/m run)", headloss_permissible, key='headloss_permissible')
            # Head Loss * Effective Pipe Length
            headloss_consumed=headloss * headloss_eff
            st.text_area("Head Consumed (meters)", headloss_consumed, key='headloss_consumed')
            # Cummulative Head Consumed (Head Consumed so far for different floors/sections)
            st.text_area("Progressive Head (meters)", headloss_progressive, key='headloss_progressive')


    # Water Supply
    with supplyuitabs[3]:
        st.table(columns=('Pipe Number','Loading Units','Flow Rate','Head Available','Pipe Diameter','Flow Velocity',
                          'Equivalent Pipe','Measured Pipe','Effective Pipe','Progressive Head','Head Consumed'))

if st.session_state.drain:
    main_container.empty()
    drain_requirement = main_container.columns(2)
    with drain_requirement[0]:
        st.radio("State Type", ["Private", "Public"], key="drain_space_type", label_visibility="collapsed",
                 disabled=False,
                 horizontal=True)
    with drain_requirement[1]:
        st.text_input("Section/Floor", key="drain_section_floor")
        st.text_input("Pipe Number", key="drain_pipe_number")

    # TABS
    drainuitabs=st.tabs(["Waste Pipe", "Septic Tank Volume", "Soaking Size", "Waste Result Summary"])
    # Wastepipe
    # variables
    wastepipe_totalfix=0
    wastepipe_horizontalfix=0
    wastepipe_discharge=0
    wastepipe_horizontalpipe=0
    wastepipe_stackpipe=0
    wastepipe_ventpipe=0
    with drainuitabs[0]:
        wastepipe_col=st.columns(2)

        with wastepipe_col[0].container(border=True):
            st.markdown("#### Fixture And Appliance")
            st.markdown("##### **Enter The Number of Fixtures And Appliances**")
            wastepipe_handbasin=st.text_input("Wash Hand Basin", key='wastepipe_handbasin')
            wastepipe_watercloset=st.text_input("Water Closet",key='wastepipe_watercloset')
            wastepipe_urinalflush=st.text_input("Urinal Flush Valve", key='wastepipe_urinalflush')
            wastepipe_kitchensink=st.text_input("Kitchen Sink", key='wastepipe_kitchensink')
            wastepipe_bathtub=st.text_input("Bathtub", key='wastepipe_bathtub')
            wastepipe_showerhead=st.text_input("Shower Head", key='wastepipe_showerhead')
            wastepipe_laundrytub=st.text_input("Laundry Tub/Tray", key='wastepipe_laundrytub')
            wastepipe_flowdrains=st.text_input("Flow Drains", key='wastepipe_flowdrains')
        with wastepipe_col[1].container(border=True):
            st.markdown("#### Results")
            # Sum of total fixtures and appliance
            wastefix=[wastepipe_handbasin,wastepipe_watercloset,wastepipe_kitchensink,wastepipe_urinalflush,wastepipe_bathtub,
                      wastepipe_showerhead,wastepipe_laundrytub,wastepipe_flowdrains]
            wastefix=[int(f) if f.isdigit() else 0 for f in wastefix]
            wastepipe_totalfix=sum(wastefix)
            st.text_area("Total Fixture and Appliances",wastepipe_totalfix,key='wastepipe_totalfix')
            # equivalent of total loading unit
            wastepipe_horizontalfix=sum([wastefix[n] * DU for n, DU in enumerate(DU_Fixtures.values())])
            st.text_area("Horizontal Fixture Branch", wastepipe_horizontalfix, key='wastepipe_horizontalfix')
            # k * horizontal fixture branch (k is different for private and public)
            k=DU_constant[st.session_state.drain_space_type]
            wastepipe_discharge=wastepipe_horizontalfix*k
            st.text_area("Discharge Flow Rate", wastepipe_discharge, key='wastepipe_discharge')
            # use corresponding diameter from rounding up DF in Primary discharge stacks table
            st.text_area("Horizontal Pipe Diameter (mm)", wastepipe_horizontalpipe, key='wastepipe_horizontalpipe')
            # ((DF/K)**3)**1/8
            wastepipe_stackpipe=((wastepipe_discharge/(32*(10**-6)))**3)**0.125
            st.text_area("Stack Pipe Diameter (mm)", wastepipe_stackpipe, key='wastepipe_stackpipe')
            # 50mm
            wastepipe_ventpipe=50
            st.text_area("Vent Pipe Diameter (mm)", wastepipe_ventpipe, key='wastepipe_ventpipe')

    # Septic Tank Volume
    septictankvolume=0
    with (drainuitabs[1]):
        septictank_col=st.columns(2)
        with septictank_col[0].container(border=True):
            septictank_wastewater = st.text_input("Waste Water Flow Rate (L/sec)", key='septictank_wastewater')
            septictank_removaleff = st.text_input("Removal Efficiency", key='septictank_removaleff')
            septictank_returntime = st.text_input("Retention Time (sec)", key='septictank_returntime')
        with septictank_col[1].container(border=True):
            st.markdown("#### Results")
            if septictank_wastewater and septictank_removaleff and septictank_returntime:
                septictank_wastewater=int(septictank_wastewater)
                septictank_removaleff=int(septictank_removaleff)
                septictank_returntime=int(septictank_returntime)
                septictankvolume=(septictank_wastewater*septictank_returntime*3.78541)/(86400*septictank_removaleff)
            st.text_area("Septic Tank Volume (Litre)", value=septictankvolume, key='septictankvolume')

    # Soakaway Size
    soakawaysize=0
    with (((drainuitabs[2]))):
        soakaway_col = st.columns(2)
        with soakaway_col[0].container(border=True):
            soakaway_wastewater=st.text_input("Waste Water Flow Rate (L/sec)", key='soakaway_wastewater')
            soakaway_infiltration=st.text_input("Infiltration Rate (L/sec/mm2)", key='soakaway_infiltration')
            soakaway_retention=st.text_input("Retention Time (sec)", key='soakaway_retention')
            soakaway_safetyfactor=st.text_input("Safety Factor", key='soakaway_safetyfactor')
        with soakaway_col[1].container(border=True):
            st.markdown("#### Results")
            if soakaway_wastewater and soakaway_infiltration and soakaway_retention and soakaway_safetyfactor:
                soakaway_wastewater=int(soakaway_wastewater)
                soakaway_infiltration=int(soakaway_infiltration)
                soakaway_retention=int(soakaway_retention)
                soakaway_safetyfactor=int(soakaway_safetyfactor)
                soakawaysize=(soakaway_wastewater*soakaway_retention)/(soakaway_infiltration*soakaway_safetyfactor)
            st.text_area("Soakaway Size", value=soakawaysize, key='soakawaysize')

    # Water Result
    with drainuitabs[3]:
        st.table(columns=("Pipe Number", "Fixture Unit FU", "Accumulated FU","Pipe Size Branch","Pipe Size Stack","Pipe size Vent"))
