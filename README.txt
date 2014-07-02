READ gravGen.pdf FOR THE MATH BEHIND THE CODE. IT'S A BUNCH OF PHYSICS STUFF,
LOOK UP GEAR SYSTEMS IF IT'S DIFFICULT TO FOLLOW.

-- gravity_opt.py is for optimizing efficiency of a gravity-powered gear system connected to a generator. The system can only be optimized with given characterization data from a specific generator. Fake data is provided in the repo for use if no real data is available, or you can generate your own fake/simulated data. Keep reading to learn more about the required data types.

-- gravity_n.py (in directory old_stuff) doesn't optimize for energy efficiency, is pretty straight forward, and doesn't really do anything interesting.

-- gravity_5.py (also in directory old_stuff) is a less-robust version of the above, and should probably just be deleted from the repo, but I kept it for records sake. 

REQUIREMENTS:	
The data file required for gravity_opt.py is pretty straightforward. You need characterization data for an electrical generator/alternator for a range of power loads. Input power, rectified output power, and rotational velocity must be recorded for every load. The greater the range of loads the better. Copy the data into a text file with input power data on the first line, output power data on the second line, and rotational velocity data on the third line. Each data point must be separated by a comma. No spaces. See fake_data.txt for an example.

The data.py script takes care of converting the raw data in the text file to individual numpy arrays and names them appropriately. gravity_opt.py imports the arrayed data and uses it to generate best-fit polynomials, which are used to optimize the system.

The values defined in constants.py are taken from universal constants and resources that will likely be used in Uganda. 

'Nuff said?
'nuff said.
