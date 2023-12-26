"""
depth: z
volume: V
pressure: p
"""
import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd

from streamlit_vertical_slider import vertical_slider
from scripts.utils.utils_divephysfun import get_p_from_z, get_z_from_p

# Variables for plotting profiles
Z_MIN = -100
Z_MAX = 0
PLOT_SCALE_FACTOR = 20

# instantiate variables
z_slid = 0 # 0 meters
V0 = 1 # 1 liter

def law_boyle_V1(V0, p0, p1):

    """
    Boyle's law: PV = constant k
    """
    V1 = V0*p0 / p1

    return V1

def get_disk_from_V(V: float) -> float:

    """
    Parameters:
        V: volume
    Returns:
        disk: cross-sectional area or corresponding disk with the corresponding radius r
    """
    r = (3 * V / (4 * math.pi))**(1/3)
    disk = 2 * math.pi * (r**2)

    return disk

def header():
    st.header("Boyle's Law")
    st.markdown("""
    Boyle's Law states that the volume and the absolute pressure of a gas are inversely proportional when temperature and the amount of gas remain constant. 
                This is relevant for diving because it means that as the pressure exerted on a gas increases, its volume decreases, and vice versa.
    """ )

def interactive_depth_slider():
    st.subheader("Interactive Slider")
    st.markdown("""
                Assume you start with a volume $V_1$ of 1 liter (L) at the surface, i.e. a depth of 0 meter with absolute pressure $p_1$ of 1 bar.
    Use the vertical slider below to pick a new depth. As you move the slider up or down, observe how the corresponding volume of the gas changes, demonstrating the relationship described by Boyle's Law.
                
    Tip: hover over the tooltip to see the corresponding change in volume.
    """)

    ## Layout
    col1, col2 = st.columns(2)

    with col1:

        slid_out = vertical_slider(
            label = "Depth [meters]",
            key = "vert_01" ,
            height = 300, 
            min_value= Z_MIN,
            max_value= Z_MAX,
            step = 0.5,
            track_color = "#29B5E8",
            slider_color = ("#09A9C8", "#001F3D"),
            thumb_color= "orange",
            thumb_shape = "square",
            value_always_visible = True,
        )
        
        if slid_out is not None:
            z_slid = slid_out


    with col2:
        # Define the range for the depth slider
        depth_range = (0, 100)
        volume_range = (0, 100)

        # Calculate the pressure based on the depth
        p0 = get_p_from_z(0)
        p1 = get_p_from_z(-z_slid)
        V1 = law_boyle_V1(V0, p0, p1)
        A1 = get_disk_from_V(V1)

        # Create a plot to visualize the pressure-depth relationship
        z_array = np.linspace(depth_range[0], depth_range[1], 100)
        p_array = get_p_from_z(z_array)
        V_array = law_boyle_V1(V0, p0, p_array)
        A_array = get_disk_from_V(V_array)

        dict_out = {'z': [z_slid], 
                    'x': [0], 
                    'V': [V1],
                    'A': [A1]}
        source = pd.DataFrame(data = dict_out, columns = ['z', 'x', 'V', 'A'])

        chart = alt.Chart(source).transform_calculate(
            size=f"{PLOT_SCALE_FACTOR} * datum.A"  # Compute the size as 10 times A
            ).mark_circle(color="#09A9C8").encode( # mark circle with color is how to enforce the color as it's not a variable
                x=alt.X('x', title=None),
                y=alt.Y('z', title="Depth [meters]", scale=alt.Scale(domain=[Z_MIN - 1, Z_MAX + 8])),
                size=alt.Size(
                    'size:Q', 
                    scale=alt.Scale(
                        domain=[PLOT_SCALE_FACTOR * A_array[-1], PLOT_SCALE_FACTOR * A_array[0]],
                        range=[PLOT_SCALE_FACTOR, PLOT_SCALE_FACTOR*100]
                        ), 
                    legend=None
                    ),
                # Add tooltip for V values
                tooltip=[alt.Tooltip('V:Q', title='V in liters')]  
                ).configure_axisX(grid=False, ticks=False, labels=False).properties(width=300, height=350).interactive()

        # Use the Streamlit theme by default.
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

def calculator():
    st.subheader("Calculator")

    with st.container():

        st.markdown("Enter the initial values for pressure $p_1$ and volume $V_1$:")

        col1, col2 = st.columns(2)

        p1 = col1.number_input("Initial pressure $p_1$", value=1.0)
        V1 = col2.number_input("Initial volume $V_1$ in liters:", value=1.0)

    
    with st.container():

        st.markdown("Enter the new value for either pressure $p_2$ or volume $V_2$:")

        col1, col2 = st.columns(2)
        p2 = col1.number_input("Final pressure $p_2$", value=None)
        V2 = col2.number_input("Final volume $V_2$ in liters (optional):", value=None)

        if not p2 and not V2:
            st.error("Enter a value for the final pressure or volume.")

        elif p2 and not V2:
            if st.button("Calculate $V_2$"):
                V2 = (p1 * V1)/ p2
                st.write(f"The final volume is $V_2 = {V2}$ liters.")
        
        elif V2 and not p2:
            if st.button("Calculate $p_2$"):
                p2 = (p1 * V1)/ V2
                st.write(f"The corresponding pressure is $p_2 = {p2}$ bars.")
                z2 = get_z_from_p(p2)
                st.write(f"The corresponding depth is {-z2} meters.")

        elif p2*V2 != p1*V1:
            st.error("There is an error with either $p_2$ or $V_2$.")


def main():

    # Title and definition
    header()
    # Depth slider to calculate volume change
    with st.container():
        interactive_depth_slider()
    # Calculator for calculate pressure, volume
    with st.container():
        calculator()

if __name__ == '__main__':
    main()