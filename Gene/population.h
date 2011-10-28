/* Population

*/

#ifndef population_h
#define population_h
#include "organism.h"
 
 class population{
        // cull to this many children after each generation
	int childCull = 20;
    
        // number of children to create after each generation
	int childCount = 100;
    
        // max number of best parents to include in next generation
	int incest = 10;
    
        // parameters governing addition of random new organisms
	int numNewOrganisms = 0; // number of new orgs to add each generation
    
        // set to initial population size
	int initPopulation = 10;
    
        // set to species of organism
	// species = Organism
	//TODO - Use class templates such that we can use a different organism classes
	// Learn about class templates.    
        
	// mutate this proportion of organisms
	double mutants = 0.1;
    
        // set this to true to mutate all progeny
	bool mutateAfterMating = true;

        // keeps track of sorting
	bool sorted = false;

	// Vector containing all organisms in population
	std::vector<Organism> pop(initPopulation)
 public:
        population();
	void gen();
	double fitness();
	organism best();//TODO TEMPLATE
	void sort();
}
 
#endif
