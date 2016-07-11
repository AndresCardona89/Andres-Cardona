# Andres-Cardona
Coding challenge_Insight_Andres Cardona

DESCRIPTION

This code reads Venmo payments from one .txt file in JSON format.
It calculates the median degree of connections or payments for each end of the payment within a window of 60 seconds since the latest payment

REQUIREMENTS

This program assumes you have installed Python 3.5 and that you have these libraries available (described below)  


STRUCTURE (Libraries)

-Json: offers functions to help encode and decode data in JSON (JavaScript Object Notation) format

-datetime: Offers objects and variables to handle dates and times

-statistics: Offers functions and objects for different statistical opperations

-os: Provides tools for using operating system functionalities.

USAGE

Download the full folder and execute run.sh in the shell console. Make sure a proper 'venmo-trans.txt' file with JSON entries exists in the 'venmo_input' folder.

When the codes ends execution, a new 'output.txt' file will be created in the 'venmo_output' folder with the proper solution to the median degree calculation
