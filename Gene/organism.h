/* Organism
Class for the organism. 
Each instance of the organism represents a single trial solution
Methods: 
Fitness - return fitness of solution
Mate - Mates this organism with another to produce a new organism

Single helix.
*/

#ifndef organism_h
#define organism_h
#include "gene.h"
 
 class organism {
	int nGenes = 3;                  //overload in solution
	std::vector<gene> genes(nGenes); //overload
	bool mutateOneOnly = False; //mutation affects one randomly chosen or all genes     
    	double crossoverRate = 0.5; //proportion of genes to split out to first child
 public:
        organism();
        organism(std::vector<gene> initGenes);
	organism mate(organism *partner);
	gene getGene(int n);
	double fitness();
	int mutate();
}
 
#endif
