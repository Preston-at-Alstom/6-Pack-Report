import consist_list
import crew_lineup
import job_descriptions
import equipment_lineup
import date_tools
import pandas as pd


def main(dispatch_sheet, crew_lineup_sheet, consist_size):
    # Convert sheets to Dataframes (Consist, Crews, Jobs, Trips)
    equip_lineup_pdf = '(FINAL) Equipment Lineup - October 2025 Board eff. Oct 27, 2025.pdf'
    month, day, year = date_tools.get_date()    
    consist_df = consist_list.to_df(dispatch_sheet)
    crew_lineup_df = crew_lineup.to_df(crew_lineup_sheet)
    job_df, trips_df =  job_descriptions.to_df()
    
    # filter consist list by consist size
    filtered_consist_df = consist_df.loc[consist_df['Consist Size'] == consist_size]
        
    ## Equipment info ##
    # get list of starting trains
    AM_consist_list = list(set(filtered_consist_df['AM Train Number'].tolist()))
   
    
    ## Train info ##    
    # get all trains connected to starting trains
    consist_cycles_lists, connected_trains_list = equipment_lineup.get_connected_trains(equip_lineup_pdf, AM_consist_list)
    service_types = ['Revenue' , 'Non-Revenue']
    filtered_trips_df = trips_df[trips_df['train_number'].isin(connected_trains_list) & trips_df['service_type'].isin(service_types)]
    
    ## Job info ##
    # Get Job numbers that work above filtered trips
    Job_numbers_list = list(set(filtered_trips_df['job_number'].tolist()))
    Job_numbers_list = [ int(x) for x in Job_numbers_list ]
    job_df['job_number'] = job_df['job_number'].astype(int)
    job_df = job_df[job_df['job_number'].isin(Job_numbers_list)]
    job_df= job_df.drop_duplicates(subset=['job_number'])
    job_df = job_df.rename(columns={'job_number': 'Tour #'})
    job_df = job_df.reset_index(drop=True)

    ## Crew info ##
    # change 6 digit tour numbers to 5 digits
    crew_lineup_df['Tour #'] = crew_lineup_df['Tour #'].apply(lambda x: x // 10)
    crew_lineup_df = crew_lineup_df[crew_lineup_df['Tour #'].isin(Job_numbers_list)]
    crew_lineup_df = crew_lineup_df.reset_index(drop=True)

    final_df = pd.merge(job_df, crew_lineup_df, on='Tour #', how='inner')
    final_df = final_df.sort_values(by='on_duty')
    final_df = final_df[['Tour #',	'on_duty', 'on_duty_location', 'QCTO Daily', 'CTO Daily', 'CSA Daily', 'Extra CTO Daily']]

    
    filename = f'{consist_size} Report {month} {day}.xlsx'


    # export to excel file
    final_df.to_excel(filename, index=False)
    
    return filename






