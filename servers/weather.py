import requests

from mcp.server.fastmcp import FastMCP

mcp = FastMCP('Weather Alerts')

import typing as t


# this is just a set of state codes randomly selected for the tool below
RegionCode = t.TypeAlias = t.Literal['AZ', 'CA', 'NY', 'TX', 'FL', 'IL', 'WA', 'AK', 'CO']

@mcp.tool()
def get_california_alerts(region_code) -> list[dict[str, str]]:
    '''
    Call this to get the active weather alerts in a specified region
    '''

    url = f'https://api.weather.gov/alerts/active/area/{region_code}'

    data = requests.get(url).json()['features']

    # allows us to traverse through every element within the list of dictionaries
    alerts = list(
        map(
            lambda x: {'area': x['properties']['areaDesc'], 'description': x['properties']['headline']},
            data
        )
    )

    # have to first get features and then within that headline and areaDesc
    return alerts


# through using mcp inspector you can spawn a dev environment
