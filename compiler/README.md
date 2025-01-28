## Goal
The primary objective of this project is to extract functions from [BILD API](https://bildexternalapi.portledocs.com/#/docs/apireference) and automatically generate corresponding functions in our codebase. This automation aims to streamline the process of integrating new functionalities and ensure that our codebase remains up-to-date with the latest features available for the BILD API.

Ideally after data is extracted, between some mix of parsing and AI, create a function to access that end point. That would also allow it to make the function in whatever language we want. After all the functions have been created, write it to a file and and run tests to make sure everything works as expected.

It can extract the name of the endpoint, url and descrpition, but cannot quite get the response or requred fields in an easy to read format. 
