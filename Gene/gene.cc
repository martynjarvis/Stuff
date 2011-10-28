
#include <cstdlib> 
#include <iostream>
#include "gene.h" 
using namespace std;


gene::gene(){
	value = minValue+(maxValue-minValue)*rand()/(float(RAND_MAX)+1);
}

gene::gene(double initVal){
	value = initVal;
}

double gene::getValue(){
	return value;
}

double gene::combine(gene *other){
//Simple average determains phenotype
	return (value+other->getValue())/2.;
}

bool gene::maybeMutate(){
	double rand = (1.0)*rand()/(float(RAND_MAX)+1);
	if rand <mutProb {
		return mutate();
	}
	return false;
}

bool gene::mutate(){
//Increment value by a random double between -mutAmt and +mut Amt
	value+= -mutAmt+(2*mutAmt)*rand()/(float(RAND_MAX)+1);
	return true;
}

