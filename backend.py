import consist_list
import crew_lineup
import job_descriptions.py
import equipment_lineup
import date_tools

def main(dispatch_sheet, crew_lineup_sheet, size):
    # ingest excel sheets / pdfs 
    consist_sheet = dispatch_sheet
    consist_size = size
    crew_sheet = crew_lineup_sheet
    equip_lineup_pdf = '(FINAL) Equipment Lineup - September 2025 Board eff. Sept 2, 2025 (1).pdf'
    month, day, year = date_tools.get_date()    

    # Convert sheets to Dataframes (Consist, Crews, Jobs, Trips)
    consist_df = consist_list.to_df(consist_sheet)
    crew_lineup_df = crew_lineup.to_df(crew_sheet)
    job_df, trips_df =  job_descriptions.to_df()


    # filter consist list by consist size
    filtered_consist_df = consist_df.loc[consist_df['Consist Size'] == consist_size]
    
    # Sort consist list by departure time
    sorted_consist_df = filtered_consist_df.sort_values(by='AM Departure Time')


    # get AM, PM departure trains
    selected_consists = consist_list.get_consists(sorted_consist_df)

    # get all trains connected to above selected consists
    connected_trains = equipment_lineup.get_connected_trains(equip_lineup_pdf, selected_consists)

    # filter all trips, and pick out those that match above connected trips
    filtered_trips = trips_df.query('(train_number in @connected_trains) & (service_type == "Revenue")')

    # Get Job numbers that work above filtered trips
    Job_numbers_list = list(set(filtered_trips['job_number'].tolist()))


    # filter above selected jobs from all jobs
    filtered_jobs_df = job_df.query('job_number in @Job_numbers_list')
    # sort by On job number
    onduty_list = filtered_jobs_df.sort_values(by='job_number')
    # keep Job number and On duty columns
    filtered_jobs_df = filtered_jobs_df[['job_number', 'on_duty', 'on_duty_location']]

    # change 6 digit job numbers to 5 digits to match job descriptions
    crew_lineup_df['Tour #'] = crew_lineup_df['Tour #'].apply(lambda x: str(x // 10))
    crew_lineup_df = crew_lineup_df.sort_values(by ='Tour #' )


    selected_crew_lineup_df = crew_lineup_df.loc[crew_lineup_df["Tour #"].isin(onduty_list["job_number"])]

    # reindex both dataframes
    filtered_jobs_df = filtered_jobs_df.reset_index(drop=True)
    selected_crew_lineup_df = selected_crew_lineup_df.reset_index(drop=True)

    
    # add on duty time and on duty location column
    selected_crew_lineup_df.insert(0 , 'on duty', filtered_jobs_df['on_duty'])
    selected_crew_lineup_df.insert(2 , '', filtered_jobs_df['on_duty_location'])
    # sort by on duty time
    selected_crew_lineup_df = selected_crew_lineup_df.sort_values(by='on duty')




    filename = f'6 pack Report {month} {day}.xlsx'

    # export to excel file
    selected_crew_lineup_df.to_excel(filename, index=False)

    return filename

    # Dataframe to JSON if required #
    #  consist_df.to_json('consist_sheet.json', orient='records', indent=4)
    #  crew_lineup_df.to_json('crew_lineup.json', orient='records', indent=4)
    #  job_df.to_json('jobs.json', orient='records', indent=4)
    #  trips_df.to_json('trips.json', orient='records', indent=4)

    # Dataframes to excel if required #
    #  sorted_consist_df.to_excel('Sorted_consist.xlsx', index=False) 
    #  sorted_trips.to_excel('trips.xlsx', index=False) 
    #  onduty_list.to_excel('onduty.xlsx', index=False) 
    #  crew_lineup_df.to_excel('line_up.xlsx', index=False)




