import numpy as np


def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Event','Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df

    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]

    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]

    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby(['Year']).sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year', ascending=True).reset_index()
    else:
        x = temp_df.groupby(['region']).sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
        x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

        x['Gold'] = x['Gold'].astype('int')
        x['Silver'] = x['Silver'].astype('int')
        x['Bronze'] = x['Bronze'].astype('int')

    return x


# def medal_tally(df):
#     medal_tally = df.drop_duplicates(
#         subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
#     medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
#                                                                                                 ascending=False).reset_index()
#     medal_tally["Total"] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
#
#     medal_tally['Gold'] = medal_tally['Gold'].astype('int')
#     medal_tally['Silver'] = medal_tally['Silver'].astype('int')
#     medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
#     medal_tally['Total'] = medal_tally['Total'].astype('int')
#     return medal_tally



def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, "Overall")

    return years,country


def data_over_time(df, col):
    counts = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    counts.columns = ['Year', col]
    sorted_counts = counts.sort_values('Year')
    return sorted_counts


def most_successful(df, sports):
    temp_df = df.dropna(subset=['Medal'])
    if sports != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sports]

    name_counts = temp_df['Name'].value_counts().reset_index()
    name_counts.columns = ['Name', 'Medals']

    top_names = name_counts.head(15)

    if not top_names.empty:
        merged_data = top_names.merge( df, left_on='Name', right_on='Name', how='left')
        result = merged_data[['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')
        result.rename(columns={'Name': 'Athlete'}, inplace=True)
        return result


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],
                            inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],
                            inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt



def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    name_counts = temp_df['Name'].value_counts().reset_index()
    name_counts.columns = ['Name', 'Medals']

    top_names = name_counts.head(10)

    if not top_names.empty:
        merged_data = top_names.merge( df, left_on='Name', right_on='Name', how='left')
        result = merged_data[['Name', 'Medals', 'Sport']].drop_duplicates('Name')
        result.rename(columns={'Name': 'Athlete'}, inplace=True)
        return result


def weight_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
         temp_df = athlete_df[athlete_df['Sport'] == sport]
         return temp_df
    else:
        return athlete_df


