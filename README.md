# ParentsEvening
A functional programming schedule system for parents evenings.

# Process

Takes in a CSV file like the one below

Student,	Teachers,	EveningArrival,	EveningDeparture

Will,	"Mr.Jeff (1), Mr.Walter (3), Ms.Gary (1), Ms.Onion (2)",	7.5,	8	

Bob,	"Mr.Jeff (3), Mr.Walter (3), Ms.Gary (2), Ms.Onion (2)",	7,	8.5	

Gee,	"Mr.Jeff (1), Mr.Walter (2), Ms.Gary (1), Ms.Onion (3)",	6,	8.5	

Jack,	"Mr.Jeff (3), Mr.Walter (1), Ms.Gary (1), Ms.Onion (1)",	6,	8.5	

## Student
 Name of student

## Teachers
A string of teachers the student would like to see followed by a priority rating of each teacher (1->3), this will prioritise the meeting of the respective student and teacher when the algorithm matches appointments.

## EveningArrival
A decimal time format of when the student will arrive

## EveningDeparture

A decimal time format of when the student will leave
