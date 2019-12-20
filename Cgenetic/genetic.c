#include <stdlib.h>

struct Population {
    int size;
    struct Tour ** tours; // array of tours
};

struct Tour {
    /* se lo tengo come int (usando la differenza di lunghezza tra il migliore 
     * e questo) dovrei guadagnare in performance
     */
    unsigned fitness;
    unsigned * solution;
};

unsigned * gen(unsigned * solution, unsigned populationSize, double mutationRate, unsigned tournamentSize, unsigned elitism, unsigned generations) {
    struct Population * pop = malloc(sizeof(struct Population));
    generatePopulation(pop);
    for (unsigned i = 0; i < generations; ++i) {
        printf("Migliore: %d", findBest(pop));
        evolve(pop, mutationRate, elitism);
    }

    return getBest(pop)->solution;
}

unsigned * evolve(struct Population * pop, double mutationRate, 
        unsigned elitism) {
    // initialize population
    struct Population * newPopulation = malloc(sizeof(struct Population));
    struct Tour ** newTours = malloc(sizeof(struct Tour *) * pop->size);
    newPopulation->tours = newTours;
    newPopulation->size = pop->size;

    unsigned elitismN = 0;
    if (elitism) {
        struct Tour * best = findBest(pop);

        // not so sure about this line
        // it's the first one, so maybe it's like this
        newPopulation->tours = best;
        elitismN = 1;
    }

    for (unsigned i = elitismN; i < newPopulation->size; ++i) {
        struct Tour * parent1 = TSelection(pop);
        struct Tour * parent2 = TSelection(pop);
        struct Tour * child = crossover(parent1, parent2);
        mutate(child, mutationRate);

        TwoOpt(child, 15);
        /* this is the first option
        struct Tour * position = newPopulation->tours + i;
        position = childM;
        */
        // second option, is it fully correct?
        newPopulation->tours[i] = childM;
    }

    return newPopulation;
}
