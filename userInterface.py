import streamlit as st

# some variables
total_fix_app=None
total_wsfu=None
flow_rate=None
pipe_diameter=None

main_container = st.empty()
with main_container.container():
    if 'drain' not in st.session_state:
        st.session_state.drain = False
    if 'supply' not in st.session_state:
        st.session_state.supply = False

    def drain():
        st.session_state.drain = True

    def supply():
        st.session_state.supply = True

    st.button('Drainage', on_click=drain)
    st.button('Water Supply', on_click=supply)

if st.session_state.drain or st.session_state.supply:
    main_container.empty()
    load_requirement = main_container.columns(2)
    with load_requirement[0]:
        st.radio("State Type", ["Private", "Public"], key="space_type", label_visibility="collapsed", disabled=False,
                 horizontal=True)
    with load_requirement[1]:
        st.text_input("Section/Floor", key="section_floor")
        st.text_input("Pipe Number", key="pipe_number")

    # TABS
    uitabs = st.tabs(
        ["Pipe Sizing", "Pipe Length", "Head Loss", "Results Summary", "Waste Pipe", "Waste Result Summary"])
    # Pipe Sizing
    with uitabs[0]:
        Pipe_sizing_tab=st.container(border=True)
        Pipe_sizing_tab.subheader("Loading Requirement")

        Pipe_sizing_tab.markdown("##### Fixture & Appliance")
        Pipe_sizing_tab.write("Enter The Number of Fixture & Appliance:")
        Pipe_sizing_tab.container(border=True)
        fixture_appliance_results=Pipe_sizing_tab.columns(3)
        fixture_appliance=fixture_appliance_results[:2]
        pipe_sizing_results = fixture_appliance_results[2]

        with fixture_appliance[0]:
            st.text_input("Water Closet", key="water_closet")
            st.text_input("Wash Hand Basin", key="wash_hand_basin")
            st.text_input("Kitchen Sink", key="kitchen_sink")
            st.text_input("Bathhub Faucet", key="bathhub_faucet")
        with fixture_appliance[1]:
            st.text_input("Shower Head", key="shower_head")
            st.text_input("Urinal Flush Valve", key="urinal_flush_valve")
            st.text_input("Laundry Tube/Tray", key="laundry_tub")
            st.text_input("Tap Diameter", key="tap_diameter")
            st.text_input("The Maximum Velocity of Required Pipe (in/sec)", key="max_velocity_pipe")
        with pipe_sizing_results:
            st.text_area("Total Fixture & Appliances",total_fix_app, key="total_fix_app")
            st.text_area("Total WSFU (Unit Load)", total_wsfu, key="total_wsfu")
            st.text_area("Flow Rate (L/sec)", flow_rate, key="flow_rate")
            st.text_area("Pipe Diameter (mm)", total_wsfu, key="pipe_diameter")

    # Pipe Length
    # variables
    pipelength_nocomp=None
    pipelength_flowrate=None
    pipelength_eqv=None
    pipelength_eff=None
    with uitabs[1]:
        component_result = st.columns(2)

        bendandvalves = st.container(border=True)
        with bendandvalves:
            st.markdown("#### Bend and Valves")
            bendandvalves_col = st.columns(5)
            bav_vals=[('Bend','piplength_bend'),('Stop Valve', 'piplength_stopvalve'),('Globe Valve','piplength_globevalve'),
                        ('Check Valve','piplength_checkvalve'),('Service Valve','piplength_servicevalve')]
            for c,v in zip(bendandvalves_col,bav_vals):
                c.checkbox(v[0],key=v[1])

        with component_result[0].container(border=True):
            st.markdown("##### Components")
            st.markdown('**Please Enter the Types and Number of Fixtures Here**')
            pipelengthcomp=st.columns(3)
            with pipelengthcomp[0]:
                st.write('Elbow')
                st.write('Tees')
                st.write('Taps')
            with pipelengthcomp[1]:
                st.selectbox(label_visibility='hidden')
                st.selectbox(label_visibility='hidden')
                st.selectbox(label_visibility='hidden')
            with pipelengthcomp[2]:
                st.selectbox(label_visibility='hidden')
                st.selectbox(label_visibility='hidden')
                st.selectbox(label_visibility='hidden')
        with component_result[1].container(border=True):
            st.markdown("#### Results")
            st.text_area("Total Number of Components",pipelength_nocomp,key='pipelength_nocomp')
            st.text_area("Flow Rate (L/Sec)", pipelength_flowrate, key='pipelength_flowrate')
            st.text_area("Equivalent Pipe Length (meters)", pipelength_eqv, key='pipelength_eqv')
            st.text_area("Effective Pipe Length (meters)", pipelength_eff, key='pipelength_eff')

    # headloss
    # variables
    headloss=None
    headloss_permissible=None
    headloss_consumed=None
    headloss_progressive=None
    with uitabs[2]:
        watersource=st.radio('Water Source',['Storage Tank','Water Service Mains'])
        headloss_input_result=st.columns(2)
        with headloss_input_result[0].container(border=True):
            st.markdown("#### Data Input")
            st.markdown("##### **Enter The Head Available**")
            st.text_input("Velocity (m/sec)", key='headloss_velocity')
            st.text_input("Diameter(mm)", key='headloss_diameter')
            st.text_input("Effective Pipe Length(meter)", key='headloss_eff')
            st.selectbox("Head Available (meter)", key='headloss_head')
        with headloss_input_result[1].container(border=True):
            st.markdown("#### Results")
            st.text_area("Head Loss (m/m run)",headloss,key='headloss')
            st.text_area("Head Permissible (m/m run)", headloss_permissible, key='headloss_permissible')
            st.text_area("Head Consumes (meters)", headloss_consumed, key='headloss_consumed')
            st.text_area("Progressive Head (meters)", headloss_progressive, key='headloss_progressive')

    with uitabs[3]:
        st.table(columns=('Pipe Number','Loading Units','Flow Rate','Head Available','Pipe Diameter','Flow Velocity',
                          'Equivalent Pipe','Measured Pipe','Effective Pipe','Progressive Head','Head Consumed'))

    # Wastepipe
    # variables
    wastepipe_totalfix=None
    wastepipe_horizontalfix=None
    wastepipe_discharge=None
    wastepipe_horizontalpipe=None
    wastepipe_stackpipe=None
    wastepipe_ventpipe=None
    with uitabs[4]:
        wastepipe_col=st.columns[2]

        with wastepipe_col[0].container(border=True):
            st.markdown("#### Fixture And Appliance")
            st.markdown("##### **Enter The Number of Fixtures And Appliances**")
            st.text_input("Water Closet",key='wastepipe_watercloset')
            st.text_input("Wash Hand Basin", key='wastepipe_handbasin')
            st.text_input("Kitchen Sink", key='wastepipe_kitchensink')
            st.text_input("Bathtub", key='wastepipe_bathtub')
            st.text_input("Shower Head", key='wastepipe_showerhead')
            st.text_input("Urinal Flush", key='wastepipe_urinalflush')
            st.text_input("Laundry Tub/Tray", key='wastepipe_laundrytub')
            st.selectbox("Flow Drains", key='wastepipe_flowdrains') #add options
        with wastepipe_col[1].container(border=True):
            st.markdown("#### Results")
            st.text_area("Total Fixture and Appliances",wastepipe_totalfix,key='wastepipe_totalfix')
            st.text_area("Horizontal Fixture Branch", wastepipe_horizontalfix, key='wastepipe_horizontalfix')
            st.text_area("Discharge Flow Rate", wastepipe_discharge, key='wastepipe_discharge')
            st.text_area("Horizontal Pipe Diameter (mm)", wastepipe_horizontalpipe, key='wastepipe_horizontalpipe')
            st.text_area("Stack Pipe Diameter (mm)", wastepipe_stackpipe, key='wastepipe_stackpipe')
            st.text_area("Vent Pipe Diameter (mm)", wastepipe_ventpipe, key='wastepipe_ventpipe')

    with uitabs[5]:
        st.table(columns=("Pipe Number", "Fixture Unit FU", "Accumulated FU","Pipe Size Branch","Pipe Size Stack","Pipe size Vent"))
