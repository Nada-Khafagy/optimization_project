# optimization_project
Optimization of the merging of vehicles on ramps into highways
We assume one lane on the highway
The intial scenario to optimize is generated stochasticly
The following optimization algorithims are tested:
- simulated annealing (linear - geometric)
- genetic algorithim 

## Installation instructions
- go to optimization_project\code
- run main.py

we have implemented platooning and substituted in the objective function
enjoy looking at the vehicles of the main line on the map :) 

## Team members
| Name              | ID       | GUC-mail               | personal E-mail        |
|-------------------|----------|------------------------|------------------------|
| Dina Mohamed      | 49-18602 | dina.mohamed           |dina67724@gmail.com     |
| Marwa Lotfy       | 49-18054 | marwa.hassan          |lotfymarwa410@gmail.com  |
| Ahmed Mohamed Sleem |49-18230| ahmed.sleem            |ahmedsleem.mail@gmail.com|
| Nada Tamer        | 49-13614 | nada.abdelhay         |nadatameer@outlook.com   |

## to get a solution
- randomize a sequence of letters or binary
- get car objects for this list
- check feasability in which we cruise control 
- return to initial conditions

## To do list
- change how ramp looks in visualtion
- change intial positin ramp to the first car on ramp (rest of the cars are already randomized based on value of first cars)
- make ditance to lead dynamic
- check for collision
- make visualzation start from zero and sraet platooning from decsision point 
- choose what to do if no main line cars in solution (reject?)
- remove r merged and make it calculated in objective function

## problems with GA
- checking feasability in cross over and mutation
- you shoud swap the binary list and not the letters list

## code of conduct 
- please don't use 'i' or 'j' or one letter as names for variables
- function names should be verbs and as descriptive as possible
- write the code in an abstract way, from the bigger picture to the smaller picture
- write polite code as uncle bob said
- add comments plz
- break the code into smaller reusable moduls
- avoid hard codded magic numbers
- use try-except blocks in error handling
- try to write in the documentation a lil bit just so people understand plz
- DON'T REPEAT CODE
- be as descriptive as possible! i swear if i see one more 'i' i will kill someone


