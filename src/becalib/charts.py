import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from becalib.translator import get_translator



def plot_sinusoidal_wave(            
    decrement_factor: float, 
    time_shift: float,
    time_period:float =24,
    max_temp:float = 35, 
    min_temp:float = 28, 
    language:str="en"
     )-> plt:
    """sinusoidal_wave matplotlib pyplot object of time_shift and decrement_factor 

    Args:
        decrement_factor (float): in [-]
        time_shift (float): in [h]
        time_period (float, optional): in [h]. Defaults to 24h.
        max_temp (float, optional): in °C. Defaults to 35°C.
        min_temp (float, optional): in °C. Defaults to 28°C.
        language (str, optional): Defaults "en", ["fr","en","it"]

    Raises:
        TypeError: all parameters cannot be None

    Returns:
        plt: matplotlib pyplot object
    """

    _=get_translator(language)

    # Do not accept None
    for k,v in locals().items():
        if v is None:
            raise TypeError(f"{k} cannot be None") 

    temp_average = (max_temp+min_temp)/2

    amplitude_ext=max_temp-temp_average
    b=2*np.pi/time_period 
    c=0

    x = np.arange(0,2*time_period,0.1) 
    y = amplitude_ext* np.sin(b*x+c) + temp_average

    amplitude_int=amplitude_ext*decrement_factor
    
    z = amplitude_int* np.sin(b*x+time_shift)+ temp_average

    plt.plot(x,y, x,z)
    
    # Settng title for the plot in blue color

    time_shift_str=_('Time shift')
    decrement_factor_str=_("Decrement factor")

    title_str=\
f"""{time_shift_str}:  {time_shift:.1f} [h]
    {decrement_factor_str}: {decrement_factor:.2f} [-]
    """
    
    # plt.title(_('Time shift'),  fontsize=12, color='black')
    plt.title(title_str,  fontsize=10, color='black')

    # Setting x axis label for the plot
    plt.xlabel(_('Time [h]'),  fontsize=10, color='black')

    # Setting y axis label for the plot
    plt.ylabel(_('Temperature [°C]'),  fontsize=10, color='black')

    # Showing grid
    plt.grid()

    # Highlighting axis at x=0 and y=0
    plt.axhline(y=temp_average, color='k')
    plt.axvline(x=0, color='k')

    plt.xticks(np.arange(0,49,6))
    plt.yticks(np.arange(min_temp-1,max_temp+2,1))

    plt.legend([_("Text"), _('Tsurf_int')])     



    
    return plt



def plot_component_layers(
        names:list,
        thickness:list,
        heat_flow_direction:str,
        language:str="en"
    ):
    """get a matplotlib pyplot object of component layers

    Args:
        names (list): list of layers names
        thickness (list): list of layers thicknesses
        heat_flow_direction (str): 
                "Ho": Horizontal (example: wall)
                "Up": Upwards (example Roof)
                "Do": Downwards (example floor)


    Returns:
        plt: matplotlib pyplot object
    """

    # Do not accept None
    for k,v in locals().items():
        if v is None:
            raise TypeError(f"{k} cannot be None") 
        
    if heat_flow_direction=="Do":
        names= list(reversed(names))
        thickness= list(reversed(thickness))

    
    dict_for_df={}
    for i in range(0,len(names)):
        dict_for_df[names[i]]=thickness[i]
    df = pd.DataFrame(dict_for_df, index=[""])
    
    width = np.sum(np.array(thickness))*10

    _=get_translator(language)

    interior_string= _("Interior")
    exterior_string=_("Exterior")
    thickness_string = _("thickness [m]")


    if heat_flow_direction=="Ho":

        ax = df.plot.barh(width=width,stacked=True)
        ax2 = ax.twinx()

        ax.set_title(_("Component layers horizontal heat flow"), fontsize=12, color='black' )

        ax.set_ylabel(interior_string, fontsize=10, color='black' )
        ax2.set_ylabel(exterior_string, fontsize=10, color='black' )

        ax2.set_yticklabels([])
        ax2.set_yticks([])
        ax.set_yticks([])
        ax.set_xlabel(thickness_string, fontsize=10)


    elif heat_flow_direction=="Up":

        ax = df.plot.bar(width=width,stacked=True)
        ax2 = ax.twiny()

        ax.set_title(_("Component layers upwards heat flow"), fontsize=12, color='black' )

        ax.set_xlabel(interior_string, fontsize=10, color='black' )
        ax2.set_xlabel(exterior_string, fontsize=10, color='black' )

        ax2.set_xticklabels([])
        ax2.set_xticks([])
        ax.set_xticks([])

        ax.set_ylabel(thickness_string, fontsize=10)
    
    elif heat_flow_direction=="Do":

        ax = df.plot.bar(width=width,stacked=True)
        ax2 = ax.twiny()

        ax.set_title(_("Component layers downward heat flow"), fontsize=12, color='black' )

        ax.set_xlabel(exterior_string, fontsize=10, color='black' )
        ax2.set_xlabel(interior_string, fontsize=10, color='black' )

        ax2.set_xticklabels([])
        ax2.set_xticks([])
        ax.set_xticks([])

        ax.set_ylabel(thickness_string, fontsize=10)
    
    else:
        raise ValueError(f"""invalid string heat_flow_direction: {heat_flow_direction}
        available choices: Ho, Up ,Do
        """)

    return plt

