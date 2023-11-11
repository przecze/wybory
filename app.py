import pandas as pd
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

mandates_per_district = {
    1: 12,
    2: 8,
    3: 14,
    4: 12,
    5: 13,
    6: 15,
    7: 12,
    8: 12,
    9: 10,
    10: 9,
    11: 12,
    12: 8,
    13: 14,
    14: 10,
    15: 9,
    16: 10,
    17: 9,
    18: 12,
    19: 20,
    20: 12,
    21: 12,
    22: 11,
    23: 15,
    24: 14,
    25: 12,
    26: 14,
    27: 9,
    28: 7,
    29: 9,
    30: 9,
    31: 12,
    32: 9,
    33: 16,
    34: 8,
    35: 10,
    36: 12,
    37: 9,
    38: 9,
    39: 10,
    40: 8,
    41: 12
}
list_num_to_color = {1: '#FF0000', 
                     2: '#008000',
                     3: '#FF00FF',
                     4: '#0000FF',
                     5: '#000000',
                     6: '#FFD700',
                     7: '#ADD8E6'}

@st.cache_data
def process_sheet(sheet_name, file_path):
    # Load the specific sheet
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    # Melt the dataframe
    df_melted = df.melt(id_vars=['Nr okręgu'], value_vars=df.columns[3:], 
                        var_name='Candidate and Party', value_name='votes')
    
    # Extract candidate name, list (party), and position on list
    df_melted['candidate name'] = df_melted['Candidate and Party'].str.extract(r'^(.*) -')
    df_melted['list'] = df_melted['Candidate and Party'].str.extract(r'- (.*)$')
    
    # The position on the list is represented by the order in which candidates appear
    df_melted['position on list'] = df_melted.groupby('list').cumcount() + 1
    
    # Add district information
    df_melted['district'] = sheet_name
    
    # Select only relevant columns and return
    return df_melted[['district', 'list', 'position on list', 'candidate name', 'votes']]


@st.cache_data()
def get_dhondt_seats(input_df, mandates_per_district):
    # Calculate the total number of votes and determine the threshold
    total_votes = input_df['votes'].sum()
    threshold = total_votes * 0.05

    # Determine which lists are above the threshold
    votes_per_list = input_df.groupby('list')['votes'].sum()
    lists_above_threshold = votes_per_list[votes_per_list > threshold].index
    
    # Initialize the 'seat_won' column to False for all rows
    input_df['seat_won'] = False
    
    # Filter the DataFrame to include only lists above the threshold
    df_above_threshold = input_df[input_df['list'].isin(lists_above_threshold)].copy()

    for district, mandates in mandates_per_district.items():
        # Filter the DataFrame for the current district and sort by votes
        district_candidates = df_above_threshold[(df_above_threshold['district'] == district)].copy()

        # Calculate seats for each list using the d'Hondt method
        seats = {list_: 0 for list_ in district_candidates['list'].unique()}
        for _ in range(mandates):
            # Calculate the quotient for each list
            quotients = district_candidates.groupby('list')['votes'].transform('sum') / (district_candidates['list'].map(seats) + 1)
            district_candidates['Quotient'] = quotients

            # Find the list with the highest quotient that hasn't won a seat yet
            highest_quotient_index = district_candidates[~district_candidates['seat_won']].sort_values(by=['Quotient', 'votes'], ascending=False).index[0]
            district_candidates.loc[highest_quotient_index, 'seat_won'] = True
            winner = district_candidates.loc[highest_quotient_index]

            # Increment the seat count for the winning list
            seats[winner['list']] += 1

            # Set 'seat_won' to True for the correct row in the original DataFrame
            input_df.loc[(input_df['list'] == winner['list']) &
                         (input_df['district'] == district) &
                         (input_df['candidate name'] == winner['candidate name']) &
                         (input_df['position on list'] == winner['position on list']), 'seat_won'] = True

    # Return the updated DataFrame with the 'seat_won' column
    return input_df['seat_won']



def load_results():
    # File path to the Excel file
    file_path = './wyniki_gl_na_kandydatow_po_okregach_sejm_utf8.xlsx'

    # Get all sheet names
    all_sheet_names = pd.ExcelFile(file_path).sheet_names

    # Process each sheet and concatenate
    dfs_processed = [process_sheet(sheet_name, file_path) for sheet_name in all_sheet_names]
    final_df_processed = pd.concat(dfs_processed, ignore_index=True)
    df = final_df_processed
    lists = {name: i+1 for i, name in df['list'].drop_duplicates().reset_index(drop=True).items()}
    df['list_num'] = df['list'].map(lists)
    df['district'] = df['district'].str.split().str[-1].astype(int)
    return lists, df

@st.cache_resource
def get_names_word_cloud(df):
    names = df['candidate name'].str.split().str[-1].value_counts().to_dict()
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(names)
    # Create a figure
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    return fig

def entropy(df):
    _, center, _ = st.columns(3)
    with center:
        st.image('entropy_formula.svg')
    st.markdown("**Entropia - matematyczna miara niepewności** - w przypadku wyborów możemy użyć tej miary aby odnaleźć listy na których większość głosów skupiona jest na jednym lub kilku kandydatach (niska entropia) oraz takie na których głosy są bardziej równomiernie rozłożone (wysoka entropia)""")
    df = df[df['list_num'].isin(list_num_to_color.keys())].copy()
    list_to_color = df.set_index('list').list_num.map(list_num_to_color).drop_duplicates().to_dict()
    df['p'] = df['votes'] / df.groupby(['district', 'list']).votes.transform('sum')
    df['plogp'] = df['p'] * np.log(df['p'])
    entropy = (-df.groupby(['district', 'list', 'list_num']).plogp.sum()).sort_values().rename('entropy').reset_index()
    votes = df.groupby(['district', 'list_num']).votes.sum()
    entropy = entropy.join(votes, on=['district', 'list_num'])
    leader = df[df['position on list'].eq(1)].set_index(['district', 'list_num'])['candidate name'].rename('leader')
    entropy = entropy.join(leader, on=['district', 'list_num'])

    def plot_list(district, list_name):
        df_list = df[df.district.eq(district) & df['list'].eq(list_name)]
        df_list = df_list[['candidate name', 'votes']].set_axis(['Nazwisko, Imię', 'Otrzymane głosy'], axis=1)
        fig = px.bar(df_list, x='Nazwisko, Imię', y='Otrzymane głosy')
        fig.update_traces(marker_color=list_to_color[list_name])
        st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    for text, idx, col in (
        ('Niska', 0, col1),
        ('Wysoka', -1, col2)):
        row = entropy.iloc[idx]
        with col:
            st.subheader(f"{text} entropia:\n {row['list']}, okręg {row['district']}")
            plot_list(row['district'], row['list'])

    entropy = entropy[['list', 'district', 'list_num', 'votes', 'entropy', 'leader']].set_axis(
                      ['Lista', 'Okręg', 'Num. listy', 'Głosy', 'Entropia', 'Lider/Liderka'], axis=1)
    fig2 = px.scatter(
        entropy,
        x='Entropia',
        color='Lista',
        size='Głosy',
        y='Num. listy',
        hover_data=entropy.columns,
        color_discrete_map=list_to_color)
    st.subheader('A tak rozkłada się entropia dla wszystkich list')
    st.plotly_chart(fig2, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        district = st.selectbox('Wybierz okręg', sorted(entropy['Okręg'].unique()))
    with col2:
        lists = df.groupby('list').votes.sum().sort_values(ascending=False).index
        list_name = st.selectbox('Wybierz listę', lists)
    plot_list(district, list_name)

def rejected_leaders(df):
    st.header('Około 38% głosujących polaków głosuje na "jedynki"')
    x = (df.groupby('position on list').votes.sum()/df.votes.sum()).to_frame('votes share').reset_index().set_axis(['Pozycja na liście', '% głosów'], axis=1)
    fig = px.line(x[x['Pozycja na liście'].le(20)], x='Pozycja na liście', y='% głosów')
    fig.layout.yaxis.tickformat = ',.0%'
    st.plotly_chart(fig, use_container_width=True)
    st.subheader('Ale czy pierwsza pozycja na liście jest gwarancją zwycięstwa?')

    df['any_seats'] = df.groupby(['district', 'list']).seat_won.transform(any)
    leads = df[df['position on list'].eq(1) & df.any_seats & ~df.seat_won]

    st.write(f"Odpowiedź brzmi **nie** - w {len(leads)} przypadkach lider(ka) listy nie uzykał(a) mandatu, chociaż mandat przypadł komu innemu na liście. Szczegóły poniżej")
    for _, row in leads.iterrows():
        is_female = row['candidate name'][-1] == 'a'
        text = "największa zwyciężczyni" if is_female else "największy zwycięzca"
        st.markdown(f"#### **{row['candidate name']}**, pomimo pierwszego miejsca na liście, nie otrzymał{'a' if is_female else ''} mandatu w okręgu {row['district']}")
        st.markdown(f"Kandydat{'ka' if is_female else ''} komitetu {row['list']} otrzymał{'a' if is_female else ''} {row['votes']} głosów")
        winner = df[df.district.eq(row.district) & df['list'].eq(row['list']) & df.seat_won].iloc[0]
        is_female2 = winner['candidate name'][-1] == 'a'
        st.markdown(f"Mandat z tej listy zdobył{'a' if is_female2 else ''} za to **{winner['candidate name']}** startując{'a' if is_female2 else 'y'} z pozycji {winner['position on list']}")
        st.markdown(f"**{winner['candidate name']}** otrzymał{'a' if is_female2 else ''} {winner['votes']} głosów, o {winner['votes']-row['votes']} więcej niż {row['candidate name']}")
        with st.expander(f"Wszystkie głosy na listę {row['list_num']} w okręgu {row['district']}"):
            list_df = df[df.district.eq(row.district) & df['list'].eq(row['list'])][['candidate name', 'position on list', 'votes']]
            list_df = list_df.set_axis(['Nazwisko, Imię', 'Pozycja', 'Otrzymane głosy'], axis=1)
            fig = px.bar(list_df, x='Nazwisko, Imię', y='Otrzymane głosy', hover_data=list_df.columns)
            fig.update_traces(marker_color=list_num_to_color[row['list_num']])
            st.plotly_chart(fig, use_container_width=True)


def biggest_winners(df):
    biggest_winner = df[df.seat_won].sort_values('votes').iloc[0]
    is_female = biggest_winner['candidate name'][-1] == 'a'
    text = "największa zwyciężczyni" if is_female else "największy zwycięzca"
    medal_emoji = b"\xf0\x9f\x8f\x85".decode('utf8') 
    st.subheader(f"{medal_emoji} {text} wyborów {medal_emoji}")
    st.markdown(f"**{biggest_winner['candidate name']}** zdobył{'a' if is_female else ''} mandat przy zaledwie **{biggest_winner['votes']}** głosach")
    st.caption('gratulujemy')
    avg_votes = int(df[df.seat_won]['votes'].mean())
    st.subheader(f"Przeciętna liczba głosów skutkująca otrzymaniem mandatu to {avg_votes},")
    st.write("jednakże, w wyniku działania metody d'Hondta do sejmu wchodzą czasem kandydaci i kandydatki ze znacznie mniejszą liczbą głosów")
    winners = df[df.seat_won].sort_values('votes').head(10)[['candidate name', 'votes', 'list', 'district']]
    st.write(winners.set_axis(['Nazwisko, Imię', 'liczba głosów', 'lista', 'okręg wyborczy'], axis=1))
    st.subheader('A tak wygląda przeciętna liczba głosów potrzebna do uzyskania mandatu dla każdego ugrupowania:')
    st.write(df[df.seat_won].groupby('list').votes.mean().astype(int))
    
    list_to_color = df.set_index('list').list_num.map(list_num_to_color).drop_duplicates().to_dict()
    plot_df = df[df.seat_won][['votes','list','list_num','candidate name', 'district','position on list']].set_axis(['Głosy', 'Lista','Num. listy','Nazwisko, Imię', 'Okręg', 'Poz. na liście'], axis=1)
    st.subheader(f"Wszystkie zdobyte mandaty vs. liczba otrzymanych głosów")
    fig2 = px.scatter(
        plot_df,
        x='Głosy',
        color='Lista',
        size='Głosy',
        y='Num. listy',
        log_x=True,
        hover_data=plot_df.columns,
        color_discrete_map=list_to_color)
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("A najwięksi przegrani?")
    biggest_winner = df[~df.seat_won].sort_values('votes').iloc[-1]
    is_female = biggest_winner['candidate name'][-1] == 'a'
    text = "największa przegrana" if is_female else "największy przegrany"
    medal_emoji = b"\xf0\x9f\x8f\x85".decode('utf8') 
    st.subheader(f"{medal_emoji} {text} wyborów {medal_emoji}")
    st.markdown(f"**{biggest_winner['candidate name']}** nie zdobył{'a' if is_female else ''} mandatu pomimo otrzymania **{biggest_winner['votes']}** głosów")
    st.caption('nie gratulujemy')
    st.write("Inne porażki")
    winners = df[~df.seat_won].sort_values('votes', ascending=False).head(10)[['candidate name', 'votes', 'list', 'district']]
    st.write(winners)

def simulator(df):
    st.subheader("Wyniki wyborów przedstawiają się następująco")
    sorting = [3, 6, 2, 99, 4, 5]
    sorting = {l: i for i, l in enumerate(sorting)}
    list_to_color = df.set_index('list').list_num.map(list_num_to_color).drop_duplicates().to_dict()
    list_to_color['Zjedonoczona opozycja'] = '#808000'

    seats = df[df.seat_won].groupby(['list', 'list_num']).size().to_frame('seats').reset_index()
    seats_base = seats.copy().set_index('list_num').seats.rename('seats_base')
    seats_base.loc[99] = seats_base.loc[[2,3,6]].sum()

    def show_seats(seats):
        col1, col2 = st.columns(2)

        with col2:
            cols = ['list', 'seats']
            if 'diff' in seats.columns:
                cols.append('diff')
            st.write(seats[cols])

        with col1:
            seats['dummy'] = 0
            seats['sorting'] = seats.list_num.map(sorting)
            seats = seats.sort_values('sorting')
            seats.pop('sorting')
            fig = px.bar(seats, y='dummy', orientation='h', hover_data=['list', 'list_num', 'seats'], x='seats', color='list', color_discrete_map=list_to_color)
            fig.update_yaxes(visible=False, showticklabels=False)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    show_seats(seats)
    st.subheader("Ale co gdyby coś potoczyło się inaczej? Wybież scenariusz poniżej")

    def sim_below_threshold(df, list_n):
        df_sim = df.copy()
        df_sim.loc[df_sim['list_num'].eq(list_n), 'votes'] = 0
        df_sim['seat_won'] = get_dhondt_seats(df_sim, mandates_per_district)
        seats = df_sim[df_sim.seat_won].groupby(['list', 'list_num']).size().to_frame('seats').reset_index()
        seats['diff'] = (seats.seats - seats.join(seats_base, on='list_num').seats_base).apply(lambda x: '+'+str(x) if x > 0 else ('=' if x==0 else str(x)))
        show_seats(seats)

    def unified_sim(df):

        st.subheader('A gdyby poszli razem?')
        df_sim = df.copy()
        df_sim.loc[df_sim['list_num'].isin((6, 2, 3)), 'list'] = 'Zjedonoczona opozycja'
        df_sim.loc[df_sim['list_num'].isin((6, 2, 3)), 'list_num'] = 99
        df_sim['seat_won'] = get_dhondt_seats(df_sim, mandates_per_district)
        seats = df_sim[df_sim.seat_won].groupby(['list', 'list_num']).size().to_frame('seats').reset_index()
        seats['diff'] = (seats.seats - seats.join(seats_base, on='list_num').seats_base).apply(lambda x: '+'+str(x) if x > 0 else ('=' if x==0 else str(x)))
        show_seats(seats)
        st.markdown("""**UWAGA** symulacja jest bardzo uproszczona, zakłada po prostu,
                    że wszyscy kandydaci z list 2, 3 i 6 należą do tego samego
                    komitetu przy podziale mandatów metodą d'Hondta. Liczba głosów
                    na każdego kandydata nie jest zmieniona. Oczywiście w
                    rzeczywistości rozkład głosów wyglądałby inaczej, zjednoczona
                    opozycja mogłaby też umieścić znacznie mniej kandydatów i
                    kandydatek na jednej wspólnej liście.""")

    list_to_name = df[['list', 'list_num']].drop_duplicates().set_index('list_num')['list'].to_dict()
    sims = {f'{list_to_name[n]} poniżej progu wyborczego': n for n in (3, 2, 5)}
    sims['Wspólna lista opozycji'] = None
    selected = st.selectbox('Wybierz symulację', sims.keys())
    if selected == 'Wspólna lista opozycji':
        unified_sim(df)
    else:
        sim_below_threshold(df, sims[selected])

if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title='Wszystko czego NIE musisz wiedzieć o wyborach 2023')
    lists, df = load_results()
    st.header('Wszystko czego nie musisz wiedzieć o wyborach 2023')
    df['seat_won'] = get_dhondt_seats(df, mandates_per_district)
    views = {
        'Wybierz artykuł': lambda *args:None,
        'Jedynki odrzucone przez głosujących': rejected_leaders,
        'Najwięksi zwycięzcy, największe porażki': biggest_winners,
        'A co by było gdyby...': simulator,
        'Entropia partyjna': entropy
    }
    views[st.selectbox('', views.keys())](df)
    st.image('./wybory_name_cloud.png', caption=f'Najpopularniejsze imiona wśród {len(df)} kandydatów i kandydatek do sejmu')
    #st.write(lists)
    #st.write(df)
    
