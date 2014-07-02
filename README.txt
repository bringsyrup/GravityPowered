READ gravGen.pdf FOR THE MATH BEHIND THE CODE. IT'S A BUNCH OF PHYSICS STUFF,
LOOK UP GEAR SYSTEMS IF IT'S DIFFICULT TO FOLLOW.

-- gravity_opt.py is for findinf the optimal power load for a gravity-powered gear system connected to an electrical generator/alternator. The system is optimized with given characterization data from the desired generator/alternator. Fake data (fake_data.txt) is provided in the repo as an example and for running the code without real data. See REQUIREMENTS to learn more about the required data.

-- gravity_n.py (in directory old_stuff) doesn't optimize for energy efficiency, is pretty straight forward, and doesn't really do anything interesting.

-- gravity_5.py (also in directory old_stuff) is a less-robust version of the above, and should probably just be deleted from the repo, but I kept it for records sake. 

--data.py converts the characterization data in a text file to individual numpy arrays and names them appropriately. gravity_opt.py imports the arrayed data and uses it to generate best-fit polynomials, which are used to optimize the system.

--constants.py contains global variables for the system. These constants are taken from universal constants and resources that will likely be used in Uganda (such as the radius of a bike wheel).

REQUIREMENTS:	
The data file required for gravity_opt.py is pretty straightforward. You need characterization data for an electrical generator/alternator for a range of power loads. Input power, rectified output power, and rotational velocity must be recorded for every load. The greater the range of loads the better. Copy the data into a text file with input power data on the first line, output power data on the second line, and rotational velocity data on the third line. Each data point must be separated by a comma. No spaces. See fake_data.txt for an example.


'Nuff said?
'nuff said.
