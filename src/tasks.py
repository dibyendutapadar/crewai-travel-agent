from crewai import Task
from agents import intent_mapper_agent, finder_agent, itinerary_maker_agent

# Define Tasks
intent_mapping_task = Task(
    description='Extract travel intent from user query {user_query}',
    agent=intent_mapper_agent,
    expected_output=""" map the details in the following example format, whatever is not available from the user query leave it blank
        'current_location': '<users current location, show only if available>',
        'destination_location': '<users destination locatio, show only if availablen>',
        'travel_distance_range': '<the distance from the current location user is willing to travel, show only if available>',
        'location_description': '<type of location user wants to visit, show only if available>',
        'check_in_date': '<check in date, show only if available>',
        'check_out_date': '<check out date, show only if available>',
        'amenities': <amaenities user wants in array['amenity1','ammenity2'], show only if available>,
        'stay_type': '<type of stay user is looking for, show only if available>'
        'stay_budget': '<max budget user is looking for in INR, show only if available>'
    """
)

finding_recommendations_task = Task(
    description='show user intent and the top 5 stay recommendations based on user intents',
    agent=finder_agent,
    expected_output="""
    the user intent received and the Top 5 travel recommendations with details of stay like stay, location, location surrounding description, address, user rating, nearby tourist places and distance from nearby tourist places in the below format in markdown
    * **Current Location:** <users current location>
    * **Destination Location**: <users destination location>
    * **Location Description**: <type of location user wants to visit>
    * **Stay Type**: <type of stay user is looking for>
    * **Dates**: <users desired checkin to checkout dates>
    * **travel_distance_range**: <the distance from the current location user is willing to travel>,
    * **amenities**: <amaenities user wants comma separated>
    * **stay_type**: <type of stay user is looking for>
    * **travel_distance_range**: <the distance from the current location user is willing to travel>,
    * **stay_budget**: <max budget user is lokking for in INR>
    
    Based on these criteria, below are suitable stay recommendations that match the user's intent. Here are my top 5 findings:

   **1.**

    | **Stay** | **Stay Description** | **Location**| **Address** | **User Rating** |
    |---|---|---|---|---|
    | Stay name, Location| Stay Description | Location Description | stay address | average user rating |

   **Nearby Tourist Places:**

   * tourist place 1 (distance from stay in kms)
   * tourist place 2 (distance from stay in kms)
   * tourist place 3 (distance from stay in kms)
   and more tourists places accordingly

   And so on for the next 4 recommendations as well
    """,
    context=[intent_mapping_task]
)

creating_itinerary_task = Task(
    description="""Create an itinerary for {days} days around the user selected stay {user_selected_stay}
    itinerary should include spots and/or activities based on user interests.
    it should include eateries (cafes, restaurants) based on user interest.
    """,
    agent=itinerary_maker_agent,
    expected_output="""itinerary for the days around the selected stay, 
    distance from one place to the next, suggested mode of transport, time taken for the travel in a markdown format
    """,
    context=[finding_recommendations_task]
)