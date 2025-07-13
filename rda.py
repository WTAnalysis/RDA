import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from urllib.request import urlopen
from mplsoccer import PyPizza, add_image, FontManager
from scipy.stats import rankdata
import os

st.set_page_config(layout="wide")
st.title("RDA Insights - Pizza Chart Generator")

# File uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
if uploaded_file:
    data2 = pd.read_excel(uploaded_file)
    unique_players = sorted(data2['Player'].dropna().unique())
    playerrequest = st.selectbox("Select Player", options=unique_players)
    position = st.selectbox("Position", options=['', 'LW', 'RW', 'CM', 'LB', 'RB', 'DM', 'AM', 'CB', 'CF', 'LWB', 'RWB'])
    league = st.text_input("League", options = ['', 'Bundesliga', 'Bundesliga Two', 'Championship', 'English 7th Tier', 'La Liga', 'League One', 'League Two', 'Liga Portugal', 'Ligue 1', 'MLS', 'National League', 'National League N/S', 'PGA League', 'Premier League', 'Premier League 2', 'Pro League', 'Professional Development League', 'Scottish Premiership', 'Serie A', 'U18 Premier League', 'USL Super League', 'WSL', 'WSL2', "Women's A-League", "Women's National League"])
    season = st.text_input("Season", value='Enter Season Name')
    minutethreshold = st.number_input("Minimum Minutes Played", value=0)
else:
    playerrequest = None
    position = None
    league = None
    season = None
    minutethreshold = None

if uploaded_file:
    file_path = uploaded_file
    data = pd.read_excel(uploaded_file)
    
    ### USER INPUT
    
    #playerrequest = 'C. Hudson-Odoi'
    #position = 'LW'
    #league = 'Premier League'
    #season = '2024/25'
    #minutethreshold = 900
    
    ### FONT
    font_normal = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                              'src/hinted/Roboto-Regular.ttf')
    font_italic = FontManager('https://raw.githubusercontent.com/googlefonts/roboto/main/'
                              'src/hinted/Roboto-Italic.ttf')
    font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                            'RobotoSlab[wght].ttf')
    ### IMAGES
    
    rdaimage = Image.open("RDA.png")
    # Define a dictionary mapping leagues to their image URLs
    league_image_map = {
        "Premier League": "https://cdn5.wyscout.com/photos/competition/public/5_140x140.png",
        "League One": "https://cdn5.wyscout.com/photos/competition/public/64_140x140.png",
        "Championship": "https://cdn5.wyscout.com/photos/competition/public/18_140x140.png",
        "Serie A": "https://cdn5.wyscout.com/photos/competition/public/1_140x140.png",
        "League Two": "https://cdn5.wyscout.com/photos/competition/public/67_140x140.png",
        "Scottish Premiership": "https://cdn5.wyscout.com/photos/competition/public/17_140x140.png",
        "MLS": "https://cdn5.wyscout.com/photos/competition/public/324_140x140.png",
        "WSL": "https://cdn5.wyscout.com/photos/competition/public/g886_140x140.png",
        "WSL2": "https://cdn5.wyscout.com/photos/competition/public/g1330_140x140.png",
        "Women's National League": "https://cdn5.wyscout.com/photos/competition/public/g327_140x140.png",
        "PGA League":"https://cdn5.wyscout.com/photos/competition/public/g-557_140x140.png",
        "Women's A-League": "https://cdn5.wyscout.com/photos/competition/public/g370_140x140.png",
        "USL Super League": "https://cdn5.wyscout.com/photos/competition/public/g-985_140x140.png",
        "La Liga": "https://cdn5.wyscout.com/photos/competition/public/4_140x140.png",
        "Bundesliga": "https://cdn5.wyscout.com/photos/competition/public/2_140x140.png",
        "Bundesliga Two": "https://cdn5.wyscout.com/photos/competition/public/19_140x140.png",
        "Ligue 1": "https://cdn5.wyscout.com/photos/competition/public/3_140x140.png",
        "Pro League": "https://cdn5.wyscout.com/photos/competition/public/28_140x140.png",
        "Liga Portugal": "https://cdn5.wyscout.com/photos/competition/public/9_140x140.png",
        "National League": "https://cdn5.wyscout.com/photos/competition/public/135_140x140.png",
        "National League N/S": "https://cdn5.wyscout.com/photos/competition/public/135_140x140.png",
        "English 7th Tier": "https://cdn5.wyscout.com/photos/competition/public/555_140x140.png",
        "U18 Premier League": "https://cdn5.wyscout.com/photos/competition/public/g950_140x140.png",
        "Premier League 2": "https://cdn5.wyscout.com/photos/competition/public/g1592_140x140.png",
        "Professional Development League": "https://cdn5.wyscout.com/photos/competition/public/g1191_140x140.png",
        
        "INT-FIFACWC": "https://cdn5.wyscout.com/photos/competition/public/g72_140x140.png"
    
    }
    
    
    leagueimage2 = league_image_map.get(league, "URL not found")
    leagueimage = Image.open(urlopen(f'{leagueimage2}'))    
    ## COLUMN MOVE
    cols_to_move = ['Birth country', 'Passport country', 'Foot', 'Height', 'Weight', 'On loan']
    all_cols = list(data.columns)
    before = all_cols[:7]
    moving = [col for col in cols_to_move if col in all_cols]
    after = [col for col in all_cols if col not in before + moving]
    new_order = before + moving + after
    data = data[new_order]
    
    ## POSITION SPLIT
    position_split = data['Position'].str.split(',', expand=True)
    while position_split.shape[1] < 4:
        position_split[position_split.shape[1]] = None
    position_split.columns = ['position1', 'position2', 'position3', 'position4']
    position_split = position_split.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)
    data = pd.concat([data.drop(columns=['Position']), position_split], axis=1)
    position_cols = ['position1', 'position2', 'position3', 'position4']
    position_cols = [col for col in position_cols if col in data.columns]
    all_cols = list(data.columns)
    before = all_cols[:5]
    middle = position_cols
    after = [col for col in all_cols if col not in before + middle]
    new_order = before + middle + after
    data = data[new_order]
    replacements = {'LWF': 'LW', 'RWF': 'RW', 'LCMF':'CM','RCMF':'CM','DMF':'DM','RDMF':'DM','LDMF':'DM','AMF':'AM','RAMF':'RW',
                   'LAMF':'LW','RCB':'CB','LCB':'CB'}
    for col in ['position1', 'position2', 'position3', 'position4']:
        if col in data.columns:
            data[col] = data[col].replace(replacements)
    position_data = data[
        (data['position1'] == position) |
        (data['position2'] == position) |
        (data['position3'] == position) |
        (data['position4'] == position)
    ]
    position_data = position_data.loc[position_data['Minutes played']>= minutethreshold]
    # DEBUG: Show filtered dataset
    st.subheader("Filtered Data Preview")
    st.dataframe(position_data)

    if position_data.empty:
        st.warning("No players found for that position or below the minute threshold.")
        st.stop()

    if playerrequest not in position_data['Player'].values:
        st.warning(f"Player '{playerrequest}' not found in the filtered dataset.")
        st.stop()

    
    ### PERCENTILES
    cols_to_percentile = position_data.columns[18:]
    for col in cols_to_percentile:
        if pd.api.types.is_numeric_dtype(position_data[col]):
            position_data[col] = rankdata(position_data[col], method='average') / len(position_data[col]) * 100
    position_data.head()
    if position == 'CM':
        cols = [
            "Non-penalty goals per 90", "xG per 90", "xA per 90",
            "Shot assists per 90", "Touches in box per 90",
            "Accurate passes, %", "Accurate progressive passes, %", "Progressive runs per 90",
            "Accurate passes to final third, %", "Accurate crosses, %",
            "Successful defensive actions per 90", "Defensive duels won, %",
            "PAdj Sliding tackles", "Shots blocked per 90", "PAdj Interceptions"
        ]
    elif position == 'LB':
        cols = [
            "Shot assists per 90", "xA per 90", "Assists per 90",
            "xG per 90", "Successful attacking actions per 90",
            "Accurate passes, %", "Accurate progressive passes, %", "Crosses per 90", 
            "Accurate crosses, %", "Progressive runs per 90",
            "Successful defensive actions per 90", "Defensive duels won, %",
            "PAdj Sliding tackles", "Shots blocked per 90", "PAdj Interceptions"
        ]
    elif position == 'RB':
        cols = [
            "Shot assists per 90", "xA per 90", "Assists per 90",
            "xG per 90", "Successful attacking actions per 90",
            "Accurate passes, %", "Accurate progressive passes, %", "Crosses per 90", 
            "Accurate crosses, %", "Progressive runs per 90",
            "Successful defensive actions per 90", "Defensive duels won, %",
            "PAdj Sliding tackles", "Shots blocked per 90", "PAdj Interceptions"
        ]
    elif position == 'RWB':
        cols = [
            "Shot assists per 90", "xA per 90", "Assists per 90",
            "xG per 90", "Successful attacking actions per 90",
            "Accurate passes, %", "Accurate progressive passes, %", "Crosses per 90", 
            "Accurate crosses, %", "Progressive runs per 90",
            "Successful defensive actions per 90", "Defensive duels won, %",
            "PAdj Sliding tackles", "Shots blocked per 90", "PAdj Interceptions"
        ]
    elif position == 'LWB':
        cols = [
            "Shot assists per 90", "xA per 90", "Assists per 90",
            "xG per 90", "Successful attacking actions per 90",
            "Accurate passes, %", "Accurate progressive passes, %", "Crosses per 90", 
            "Accurate crosses, %", "Progressive runs per 90",
            "Successful defensive actions per 90", "Defensive duels won, %",
            "PAdj Sliding tackles", "Shots blocked per 90", "PAdj Interceptions"
        ]
    elif position == 'CB':
        cols = [
            "Offensive duels won, %", "Shot assists per 90", "xA per 90",
            "xG per 90", "Non-penalty goals per 90",
            "Accurate passes, %", "Accurate lateral passes, %", "Accurate short / medium passes, %", 
            "Progressive passes per 90", "Accurate progressive passes, %",
            "Defensive duels won, %", "Successful defensive actions per 90",
            "Aerial duels won, %", "PAdj Interceptions", "Shots blocked per 90"
        ]
    
    elif position == 'CF':
        cols = [
            "Touches in box per 90", "Shots per 90", "Shots on target, %",
            "xG per 90", "Non-penalty goals per 90",
            "Accurate passes, %", "Accurate smart passes, %", "Shot assists per 90", 
            "xA per 90", "Assists per 90",
            "Offensive duels per 90", "Offensive duels won, %",
            "Aerial duels won, %", "Successful dribbles, %", "Successful attacking actions per 90"
        ]   
    elif position == 'LW':
        cols = [
            "Touches in box per 90", "Shots per 90", "Shots on target, %",
            "xG per 90", "Non-penalty goals per 90",
            "Progressive runs per 90", "Accurate crosses, %", "Shot assists per 90", 
            "xA per 90", "Assists per 90",
            "Offensive duels per 90", "Offensive duels won, %",
            "Dribbles per 90", "Successful dribbles, %", "Successful attacking actions per 90"
        ]
    elif position == 'RW':
        cols = [
            "Touches in box per 90", "Shots per 90", "Shots on target, %",
            "xG per 90", "Non-penalty goals per 90",
            "Progressive runs per 90", "Accurate crosses, %", "Shot assists per 90", 
            "xA per 90", "Assists per 90",
            "Offensive duels per 90", "Offensive duels won, %",
            "Dribbles per 90", "Successful dribbles, %", "Successful attacking actions per 90"
        ] 
    elif position == 'DM':
        cols = [
            "Successful attacking actions per 90", "Shot assists per 90", "xA per 90",
            "Shots per 90", "xG per 90",
            "Accurate passes, %", "Accurate short / medium passes, %", "Accurate through passes, %", 
            "Progressive passes per 90", "Accurate progressive passes, %",
            "Successful defensive actions per 90", "Defensive duels per 90",
            "Defensive duels won, %", "PAdj Sliding tackles", "PAdj Interceptions"
        ]
    elif position == 'AM':
        cols = [
            "Touches in box per 90", "Shots per 90", "Goal conversion, %",
            "Non-penalty goals per 90", "xG per 90",
            "Accurate passes to penalty area, %", "Accurate crosses, %", "Shot assists per 90", 
            "xA per 90", "Assists per 90",
            "Offensive duels per 90", "Offensive duels won, %", "Successful attacking actions per 90",
            "Dribbles per 90", "Successful dribbles, %"
        ]
    else:
        cols = []  # Handle other cases if needed
    playerdata = position_data.loc[position_data['Player']==playerrequest]
    selected_columns = ['Player', 'Team', 'Age'] + cols
    new_df = playerdata[selected_columns].copy()
    new_df[cols] = new_df[cols].round(0)
    new_df[cols] = new_df[cols].astype(int)
    
    
    if position == 'CM':
        params = [
        "Non-penalty goals", "xG", "xA",
        "Shot assists", "Touches in box",
        "Accurate passes %", "\nAccurate progressive \npasses %", "Progressive runs",
        "\nAccurate passes \nto final third %", "Accurate crosses %",
        "\nSuccessful \ndefensive actions", "\nDefensive \nduels won %",
        "\nPAdj Sliding n\tackles", "Shots blocked", "\nPAdj \nInterceptions"
    ]
    elif position == 'LB':
        params = [
            "Shot assists", "xA", "Assists",
            "xG", "\nSuccessful \nattacking actions",
            "Accurate passes %", "\nAccurate progressive \npasses %", "Crosses", 
            "Accurate crosses %", "Progressive runs",
            "\nSuccessful \ndefensive actions per 90", "\nDefensive \nduels won %",
            "\nPAdj Sliding \ntackles", "Shots blocked", "\nPAdj \nInterceptions"
        ]
    elif position == 'RB':
        params = [
            "Shot assists", "xA", "Assists",
            "xG", "\nSuccessful \nattacking actions",
            "Accurate passes %", "\nAccurate progressive \npasses %", "Crosses", 
            "Accurate crosses %", "Progressive runs",
            "\nSuccessful \ndefensive actions per 90", "\nDefensive \nduels won %",
            "\nPAdj Sliding \ntackles", "Shots blocked", "\nPAdj \nInterceptions"
        ]
    elif position == ':WB':
        params = [
            "Shot assists", "xA", "Assists",
            "xG", "\nSuccessful \nattacking actions",
            "Accurate passes %", "\nAccurate progressive \npasses %", "Crosses", 
            "Accurate crosses %", "Progressive runs",
            "\nSuccessful \ndefensive actions per 90", "\nDefensive \nduels won %",
            "\nPAdj Sliding \ntackles", "Shots blocked", "\nPAdj \nInterceptions"
        ]
    elif position == 'RWB':
        params = [
            "Shot assists", "xA", "Assists",
            "xG", "\nSuccessful \nattacking actions",
            "Accurate passes %", "\nAccurate progressive \npasses %", "Crosses", 
            "Accurate crosses %", "Progressive runs",
            "\nSuccessful \ndefensive actions per 90", "\nDefensive \nduels won %",
            "\nPAdj Sliding \ntackles", "Shots blocked", "\nPAdj \nInterceptions"
        ]
    elif position == 'CB':
        params = [    
            "\nOffensive \nduels won %", "Shot assists", "xA",
            "xG", "\nNon-penalty \ngoals",
            "Accurate passes %", "\nAccurate lateral \npasses %", "\nAccurate short \n& medium passes %", 
            "\nProgressive \npasses", "\nAccurate progressive \npasses %",
            "\nDefensive \nduels won %", "\nSuccessful \ndefensive actions",
            "\nAerial \nduels won %", "\nPAdj \nInterceptions", "Shots blocked"
        ]
        
    elif position == 'CF':
        params = [
            "Touches in box", "Shots", "\nShots on \ntarget %",
            "xG", "Non-penalty goals",
            "Accurate passes %", "\nAccurate smart \npasses %", "Shot assists", 
            "xA", "Assists",
            "Offensive duels", "\nOffensive \nduels won %",
            "\nAerial \nduels won %", "\nSuccessful \ndribbles %", "\nSuccessful \nattacking actions"
        ]  
    elif position == 'LW':
        params = [
            "Touches in box", "Shots", "\nShots on \ntarget %",
            "xG", "Non-penalty goals",
            "Progressive runs", "Accurate crosses %", "Shot assists", 
            "xA", "Assists",
            "Offensive duels", "\nOffensive \nduels won %",
            "Dribbles", "\nSuccessful \ndribbles %", "\nSuccessful \nattacking actions"
        ]  
    elif position == 'RW':
        params = [
            "Touches in box", "Shots", "\nShots on \ntarget %",
            "xG", "Non-penalty goals",
            "Progressive runs", "Accurate crosses %", "Shot assists", 
            "xA", "Assists",
            "Offensive duels", "\nOffensive \nduels won %",
            "Dribbles", "\nSuccessful \ndribbles %", "\nSuccessful \nattacking actions"
        ]  
    elif position == 'DM':
        params = [
            "\nSuccessful \nattacking actions", "Shot assists", "xA",
            "Shots", "xG",
            "Accurate passes %", "\nAccurate \nshort/medium passes %", "\nAccurate \nthrough passes %", 
            "\nProgressive \npasses", "\nAccurate \nprogressive passes %",
            "\nSuccessful \ndefensive actions", "Defensive duels",
            "\nDefensive \nduels won %", "\nPAdj \nSliding tackles", "\nPAdj \nInterceptions"
        ]
    
    elif position == 'AM':
        params = [
            "Touches in box", "Shots", "Goal conversion %",
            "Non-penalty goals", "xG",
            "\nAccurate passes \nto penalty area %", "\nAccurate \ncrosses %", "Shot assists", 
            "xA", "Assists",
            "Offensive duels", "\nOffensive \nduels won %", "\nSuccessful \nattacking actions",
            "Dribbles", "\nSuccessful \ndribbles %"
        ] 
        params = []  # Handle other cases if needed
    
    # parameter list
    
    
    
    # Assuming `new_df` is your DataFrame containing the values
    # Extracting values from the DataFrame based on the columns specified in `params`
    teamname = new_df['Team'].iloc[0]
    
    values = new_df[cols].values[0]
    # color for the slices and text
    slice_colors = ["#A7192B"] * 5 + ["#C79A53"] * 5 + ["#B3B3B3"] * 5
    text_colors = ["#000000"] * 10 + ["#F2F2F2"] * 5
    
    # instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#F2F2F2",     # background color
        straight_line_color="#F2F2F2",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_lw=0,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )
    
    # plot pizza
    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(8, 8.5),                # adjust figsize according to your need
        color_blank_space="same",        # use same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.4,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#F2F2F2", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, va="center"
        ),                               # values to be used when adding parameter
        kwargs_values=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values
    )
    
    # add title
    fig.text(
        0.515, 0.975, f'{playerrequest} - {teamname} - Percentile Rank (0-100)', size=16,
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )
    
    # add subtitle
    fig.text(
        0.515, 0.953,
        f'Compared against other {position} in {league} | Season {season}',
        size=13,
        ha="center", fontproperties=font_bold.prop, color="#000000"
    )
    
    # add credits
    CREDIT_1 = f"Data from Wyscout | Metrics are per 90 unless stated | Minimum {minutethreshold} mins played"
    #CREDIT_2 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"
    
    fig.text(
        0.99, 0.02, f"{CREDIT_1}", size=9,
        fontproperties=font_italic.prop, color="#000000",
        ha="right"
    )
    
    # add text
    #fig.text(
    #    0.34, 0.925, " Scoring           Creativity         Duels", size=14,
    #    fontproperties=font_bold.prop, color="#000000"
    #)
    
    fig.text(
        0.34, 0.925, "Attacking        Possession       Defending", size=14,
        fontproperties=font_bold.prop, color="#000000"
    )
    
    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.31, 0.9225), 0.025, 0.021, fill=True, color="#A7192B",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.462, 0.9225), 0.025, 0.021, fill=True, color="#C79A53",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.632, 0.9225), 0.025, 0.021, fill=True, color="#b3b3b3",
            transform=fig.transFigure, figure=fig
        ),
    ])
    # add image
    #ax_image = add_image(
    #    fdj_cropped, fig, left=0.4618, bottom=0.4475, width=0.095, height=0.1075
    #)   # these values might differ when you are plotting
    
    
    ax_image = add_image(
        rdaimage, fig, left=0.87, bottom=0.85, width=0.15 ,height=0.15
    )   # these values might differ when you are plotting
    ax_image = add_image(
        leagueimage, fig, left=0.05, bottom=0.01, width=0.125 ,height=0.125
    )   # these values might differ when you are plotting
    
    
    st.pyplot(fig)

else:
    st.warning("Please upload an Excel file.")
