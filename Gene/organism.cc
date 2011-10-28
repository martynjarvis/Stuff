
#include <cstdlib> 
#include <iostream>
#include "organism.h" 

using namespace std;

organism::organism(){

}

organism::organism(std::vector<gene> initGenes){
	copy(initGenes.begin(),initGenes.end(),genes.begin());
}	

organism organism::mate(organism* partner){
	std::vector<gene> childGenes(nGenes);//Template
	copy(genes.begin(),genes.end(),childGenes.begin())

	for (int it=0;it<genes.size();++it){
		double rand = (1.0)*rand()/(float(RAND_MAX)+1);
		if (rand > crossoverRate){
			childGenes.at(it) = partner->getGene(it)			
		}
	}
	organism child(childGenes);
	return child;
}

gene organsim::getGene(int n){//TODO TEMPLATE
	return genes.at(n);
}


double organism::fitness(){//Method to be overloaded
	return 0.0;
}


int organism::mutate(){
	int nMutations = 0;
	for (it=genes.begin();it!=genes.end();++it){
		bool mutated = it.maybeMutate();
		if (mutated){
			nMutations++;
			if (mutateOneOnly){return nMutations;}
		}
	}
	return nMutations;
}

