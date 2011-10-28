/* Gene Classes
*/
#ifndef gene_h
#define gene_h

class gene {
	double value; //Value held by gene
	double minValue = 0.00; // min value held by gene
	double maxValue = 1.00; // max value held by gene
	double mutProb = 0.01; // Probability of mutating
	double mutAmt = 0.1
public:
	gene();
	gene(double initVal);
	double getValue();
	double combine(gene *other);
	bool mutate();
} 

#endif
