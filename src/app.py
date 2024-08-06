import streamlit as st
from crewai import Crew
from tasks import (
    intent_mapping_task,
    finding_recommendations_task,
    creating_itinerary_task
)
from agents import (
    intent_mapper_agent,
    finder_agent,
    itinerary_maker_agent,
)

# Initialize Streamlit app
st.title('Travel Planner with Crew AI')


if 'first_result' not in st.session_state:
    st.session_state.first_result = ""

if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

if 'user_selected_stay' not in st.session_state:
    st.session_state.user_selected_stay = ""

if 'second_result' not in st.session_state:
    st.session_state.second_result = ""

if 'days' not in st.session_state:
    st.session_state.days = ""


# User input
st.session_state.user_query = st.text_input('Enter your travel query:',key='travel_query_input')

if st.button('Submit', key='submit_query'):
    if st.session_state.user_query:
        st.write("Running first crew to map intent and find recommendations...")
        first_crew = Crew(
             agents=[intent_mapper_agent, finder_agent],
             tasks=[intent_mapping_task, finding_recommendations_task],
             verbose=True
             )
        user_search_query = {'user_query': st.session_state.user_query}
        first_result = first_crew.kickoff(inputs=user_search_query)
        st.session_state.first_result = first_result
    else:
        st.write("Please enter a travel query.")

# Display the first result if available
if st.session_state.first_result:
    st.markdown(st.session_state.first_result)
    st.write("---")
    
if st.session_state.first_result:
    st.session_state.user_selected_stay = st.text_input('Enter the name of your preferred stay from the recommendations to plan the itinerary:', key='stay_input')
    st.session_state.days = st.number_input('Enter the number of days', min_value=1, max_value=4, value=2, key='stay_days')
    if st.button('Get Itinerary', key='get_itinerary'):
        if st.session_state.user_selected_stay and st.session_state.days:
        # Execute second crew
            st.session_state.user_selected_stay_input = {'user_selected_stay': st.session_state.user_selected_stay,'days':st.session_state.days}
            second_crew = Crew(
                    agents=[itinerary_maker_agent],
                    tasks=[creating_itinerary_task],
                    verbose=True
                    )
            
            st.session_state.second_result = second_crew.kickoff(inputs=st.session_state.user_selected_stay_input)
            
        else:
            st.write("Please enter the name of your preferred stay from the recommendations.")

# Display the first result if available
if st.session_state.second_result:
    st.markdown(st.session_state.second_result)
    st.write("---")        
    