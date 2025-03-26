import os
os.environ["API_HOST"]=""
os.environ["CONSUMER_KEY"] = ""
os.environ["CONSUMER_SECRET"]=""

from an_common.resource import get_resource_doc, get_readings_df, get_building_metadata, \
get_readings_df_interpolation, get_sensor_metadata
import pandas as pd
pd.set_option('display.max_colwidth', None) 
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None) 
from an_common.api import get_app_data

def get_nantum_data(company, building, resource, start_date, end_date, gran='60min', floor=None, total=None, rename=False):
    """
    Retrieves interpolated data for a specified resource within a given time range and granularity.

    Args:
        company (str): Identifier for the company.
        building (str): Identifier for the building.
        resource (str): Type of resource data to retrieve.
        start_date (str): Start date of the data retrieval period.
        end_date (str): End date of the data retrieval period.
        gran (str, optional): Granularity of the data. Defaults to '60min'.
        floor (str, optional): Specific floor to filter data. Defaults to None.
        total (str, optional): If set to 'only', only total aggregated data is retrieved. Defaults to None.
        rename (bool, optional): If True, renames columns to more descriptive names. Defaults to False.

    Returns:
        DataFrame: A DataFrame containing the requested data.
    """
    tz = get_building_metadata(company, building, 'timezone')
    df = get_readings_df_interpolation(company, building, resource, start_date, end_date, gran,
         imputation=True, tz=tz, max_gap_td=None, use_beta=None, floor=floor, cache=False, total=total, query=None)
    
    if rename:
        sensor_doc = get_resource_doc(company, building, resource='sensors',
                     query=None, extract_all=True, use_beta=None, domain='buildings')
        sensor_doc = pd.DataFrame(sensor_doc)
        for col in df:
            row = int(sensor_doc[sensor_doc["_id"]==col].index.values)
            name = sensor_doc.at[row,"dis"]
            df = df.rename(columns={col: name})
    return df

def _resource_name_check(resource):
    if "consumption" in resource:
        resource = resource.replace("consumption", "demand")
    return resource

def get_one_day_hourly_energy_consumption(company, building, resource, start_date, end_date):
    """
    Retrieves hourly energy consumption data for a specified resource within a given time range.

    Returns:
        DataFrame or None: A DataFrame containing hourly energy demand data for the specified resource and time range.
                           Returns None if no data is available or if an error occurs during retrieval.

    Raises:
        Exception: Catches and prints any exception that occurs during data retrieval.
    """
    resource = _resource_name_check(resource)
    try:
        df = get_nantum_data(company, building, resource, start_date, end_date, gran='60min', total='only')
        if df.empty:
            print(f"No data available for {resource} from {start_date} to {end_date}")
            return None
        return df
    except Exception as e:
        print(f"No data available for {resource} from {start_date} to {end_date}")
        return None

def get_daily_energy_consumption(company, building, resource, start_date, end_date):
    """
    Retrieves and aggregates daily energy consumption data for a specified resource within a given time range.

    Args:
        company (str): Identifier for the company.
        building (str): Identifier for the building.
        resource (str): Type of resource data to retrieve, typically energy-related.
        start_date (str): Start date of the data retrieval period in 'YYYY-MM-DD' format.
        end_date (str): End date of the data retrieval period in 'YYYY-MM-DD' format.

    Returns:
        DataFrame: A DataFrame containing the daily sum of the requested energy consumption data. Rows are dates, and the column is resource consumption for that date.
    """
    df = get_one_day_hourly_energy_consumption(company, building, resource, start_date, end_date)
    if df is not None:
        return df.resample('D').sum()
    else:
        return None

def get_daily_water_consumption(company, building, start_date, end_date):
    """
    Retrieves and aggregates daily water consumption data for a specified resource within a given time range.
    """
    df = get_nantum_data(company, building, 'water_consumption', start_date, end_date, total='only')
    if df is not None:
        # Resample to daily frequency and keep the last value of each day
        daily_df = df.resample('D').last()
        return daily_df
    else:
        return None

def get_total_energy_consumption(company, building, resource, start_date, end_date):
    """
    Calculates the total energy consumption for a specified resource within a given time range.

    Args:
        company (str): Identifier for the company.
        building (str): Identifier for the building.
        resource (str): Type of resource data to retrieve, typically energy-related.
        start_date (str): Start date of the data retrieval period in 'YYYY-MM-DD' format.
        end_date (str): End date of the data retrieval period in 'YYYY-MM-DD' format.

    Returns:
        float: The total sum of the energy consumption data for the specified period.
    """
    df = get_daily_energy_consumption(company, building, resource, start_date, end_date)
    if df is not None:
        return df.sum().sum()
    else:
        return None


def calc_peak_demand_helper(df_elec_demand):
    """This function calculates daily peak demand from electricity data

    Args:
        df_elec (DataFrame): a dataframe with single column with datetime index

    Returns:
        DataFrame: peak demand for each day
    """

    # check df_elec has one column
    assert df_elec_demand.shape[1] == 1, "df_elec must have one column"
    # check df_elec index is datetime index
    assert isinstance(df_elec_demand.index[0], pd.Timestamp), "df_elec index must be datetime index"
    # sample electricity data to 15min frequency 
    df_elec_demand = df_elec_demand.resample('15T').mean()
    # fill missing data
    df_elec_demand = df_elec_demand.interpolate('linear').bfill().ffill()
    # take rolling average for every 2 15min interval data
    data_el_rl = df_elec_demand.rolling(window=2).mean()
    # calculate the peaks daily
    peak = data_el_rl.dropna().resample('D').max()
    # change output dataframe column name
    peak.columns = ['peak_demand']
    return peak

def calc_daily_peak_demand(company, building, start_date, end_date):
    """
    Calculate the peak electricity demand for a specified building over a given period.

    Args:
        company (str): Identifier for the company.
        building (str): Identifier for the building.
        start_date (str): Start date of the data retrieval period.
        end_date (str): End date of the data retrieval period.
        gran (str, optional): Granularity of the data. Defaults to '60min'.

    Returns:
        DataFrame: A DataFrame containing the peak demand for each day.
    """
    df_elec_demand = get_nantum_data(company, building, 'electric_demand', start_date, end_date, gran='60min', total='only')
    df_peak_demand = calc_peak_demand_helper(df_elec_demand)
    return df_peak_demand


def calc_ghg_emission_helper(df_elec_demand, df_steam_demand=None, df_gas_demand=None,
                      elec_ghg_factor=None, steam_ghg_factor=None, gas_ghg_factor=None):
    """This function calculates ghg emission from electricity, steam and gas data if available

    Args:
        df_elec_demand (_type_): unit should be in kW
        df_steam_demand (_type_, optional): unit should be in Mlbs/h. Defaults to None.
        df_gas_demand (_type_, optional): unit should be in therms/h. Defaults to None.
        elec_ghg_factor (_type_, optional): _description_. Defaults to 3.412 * 0.08469.
        steam_ghg_factor (_type_, optional): _description_. Defaults to None.
        gas_ghg_factor (_type_, optional): _description_. Defaults to None.

    Returns:
        DataFrame: _description_
    """

    # check if available data have one columns only
    assert df_elec_demand.shape[1] == 1, "df_elec_demand must have one column"
    if df_steam_demand is not None:
        assert df_steam_demand.shape[1] == 1, "df_steam_demand must have one column"
    if df_gas_demand is not None:
        assert df_gas_demand.shape[1] == 1, "df_gas_demand must have one column"
    # check if avaialble data are in timestamp index
    assert isinstance(df_elec_demand.index, pd.DatetimeIndex), "df_elec_demand index must be a DatetimeIndex"
    if df_steam_demand is not None:
        assert isinstance(df_steam_demand.index, pd.DatetimeIndex), "df_steam_demand index must be a DatetimeIndex"
    if df_gas_demand is not None:
        assert isinstance(df_gas_demand.index, pd.DatetimeIndex), "df_gas_demand index must be a DatetimeIndex"

    # check if user specify ghg factor
    if elec_ghg_factor is None:
        elec_ghg_factor = 3.412 * 0.08469
    if steam_ghg_factor is None:
        steam_ghg_factor = 1194 * 0.04493
    if gas_ghg_factor is None:
        gas_ghg_factor = 5.3

    # Helper function to convert demand to correct units
    def convert_to_energy(demand_df, time_column='time'):
        demand_df = demand_df.copy()
        demand_df.columns = ['demand']
        demand_df[time_column] = demand_df.index.to_series()
        time_diff = demand_df[time_column].diff().dt.total_seconds() / 3600
        demand_df['energy'] = demand_df['demand'] * time_diff.fillna(1)
        return demand_df

    # Convert electricity demand to kWh
    df_elec_demand = convert_to_energy(df_elec_demand)
    df_elec_demand['elec_ghg_kgCO2'] = df_elec_demand['energy'] * elec_ghg_factor

    # Initialize the result DataFrame with electricity emissions
    df_ghg = df_elec_demand[['elec_ghg_kgCO2']].copy()

    # Calculate GHG emissions for steam if provided
    if df_steam_demand is not None:
        df_steam_demand = convert_to_energy(df_steam_demand)
        df_steam_demand['steam_ghg_kgCO2'] = df_steam_demand['energy'] * steam_ghg_factor
        df_ghg = df_ghg.join(df_steam_demand[['steam_ghg_kgCO2']], how='outer')

    # Calculate GHG emissions for gas if provided
    if df_gas_demand is not None:
        df_gas_demand = convert_to_energy(df_gas_demand)
        df_gas_demand['gas_ghg_kgCO2'] = df_gas_demand['energy'] * gas_ghg_factor
        df_ghg = df_ghg.join(df_gas_demand[['gas_ghg_kgCO2']], how='outer')

    # Fill NaN values with 0 for aggregation
    df_ghg = df_ghg.fillna(0)

    # Calculate total GHG emissions
    df_ghg['total_ghg_kgCO2'] = df_ghg.sum(axis=1)
    return df_ghg


def calc_ghg_emission(company, building, start_date, end_date, gran='60min',
                      elec_ghg_factor=None, steam_ghg_factor=None, gas_ghg_factor=None):
    """
    Calculate the greenhouse gas (GHG) emissions for electricity, steam, and gas demands.

    Args:
        company (str): Identifier for the company.
        building (str): Identifier for the building.
        start_date (str): Start date of the data retrieval period.
        end_date (str): End date of the data retrieval period.
        gran (str, optional): Granularity of the data. Defaults to '60min'.
        elec_ghg_factor (float, optional): GHG emission factor for electricity. Defaults to None.
        steam_ghg_factor (float, optional): GHG emission factor for steam. Defaults to None.
        gas_ghg_factor (float, optional): GHG emission factor for gas. Defaults to None.

    Returns:
        DataFrame: A DataFrame containing the calculated GHG emissions for each energy type and the total emissions.
    """
    try:
        df_elec_demand = get_nantum_data(company, building, 'electric_demand', start_date, end_date, gran=gran, total='only')
    except:
        df_elec_demand = None
    try:
        df_steam_demand = get_nantum_data(company, building, 'steam_demand', start_date, end_date, gran=gran, total='only')
    except:
        df_steam_demand = None
    try:
        df_gas_demand = get_nantum_data(company, building, 'gas_demand', start_date, end_date, gran=gran, total='only')
    except:
        df_gas_demand = None
    
    df_ghg = calc_ghg_emission_helper(df_elec_demand, df_steam_demand, df_gas_demand, elec_ghg_factor, steam_ghg_factor, gas_ghg_factor)
    return df_ghg