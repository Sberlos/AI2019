#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

struct City {
    unsigned id;
    double x;
    double y;
};

struct Instance {
    // distance matrix
    // represented with a single block of memory that I can access using
    // i * cols + j
    unsigned * distMatrix;
    // number of cities
    unsigned nCities;

    unsigned bestKnown;
};

struct Population {
    unsigned size;
    struct Tour ** tours; // array of tours
};

struct Tour {
    /* se lo tengo come int (usando la differenza di lunghezza tra il migliore
     * e questo) dovrei guadagnare in performance
     */
    double fitness; //could change to unsigned with some tricks maybe
    unsigned * solution;
};

unsigned evaluateSol(unsigned * solution, struct Instance * instance) {
    unsigned length = 0;
    // I would love to avoid it but I'm not sure how
    unsigned * temp_sol = malloc(sizeof(unsigned) * instance->nCities + 1);
    if (!temp_sol) {
        return 0;
    }
    memcpy(temp_sol, solution, sizeof(unsigned) * instance->nCities);
    temp_sol[instance->nCities] = temp_sol[0];

    unsigned from_node = temp_sol[0];

    for (unsigned i = 1; i <= instance->nCities; ++i) {
        // not sure about the index of the distMatrix
        length = length + instance->distMatrix[from_node * instance->nCities + i];
        // not sure about this either
        from_node = i;
    }
    free(temp_sol);
    return length;
}

// TODO implement
void TwoOpt(struct Tour * tour, unsigned iterations) {
}

// TODO implement
unsigned * nearestNeighbour(struct Instance * instance) {
    unsigned * solution = malloc(sizeof(unsigned) * instance->nCities);
    if (!solution) {
        return 0;
    }
    return solution;
}

// TODO implement
int generatePopulation(struct Population * pop, struct Instance * instance) {
    return 0;
}

struct Tour * crossover(struct Tour * p1, struct Tour * p2, unsigned nCities) {
    // I need to create a new children because the parent could be the one
    // saved for elitism, therefore modifying it would be bad. And in addition
    // it could be selected in next rounds of tournament for breeding.
    struct Tour * child = malloc(sizeof(struct Tour));
    if (!child) {
        return 0;
    }

    unsigned * permutation = malloc(sizeof(unsigned) * nCities);
    if (!permutation) {
        return 0;
    }
    unsigned * inversion = malloc(sizeof(unsigned) * nCities);
    if (!inversion) {
        return 0;
    }

    //int crossoverP1 = rand() % nCities;
    /* The use of the modulo operator ruin some numbers but I think in the end
     * it's ok, we will see */
    int crossoverP1 = rand() % nCities;
    int crossoverP2 = rand() % nCities;

    // copy all the cities of p1 to the new one
    memcpy(permutation, p1->solution, sizeof(unsigned) * nCities);

    for (unsigned i = 0; i < nCities; ++i) {
        inversion[permutation[i]] = i;
    }

    if (crossoverP1 > crossoverP2) {
        unsigned temp = crossoverP1;
        crossoverP1 = crossoverP2;
        crossoverP2 = temp;
    }

    for (unsigned i = crossoverP1; i <= crossoverP2; ++i) {
        unsigned value = p2->solution[i];
        unsigned invValue = inversion[value];
        unsigned t = permutation[invValue];
        permutation[invValue] = permutation[i];
        permutation[i] = t;
        t = inversion[permutation[invValue]];
        inversion[permutation[invValue]] = inversion[permutation[i]];
        permutation[inversion[i]] = t;
    }

    child->solution = permutation;

    // don't calculate the fitness here as I have to mutate and do local
    // search afterwards and I would have to recalculate it
    child->fitness = 0;
    return child;
}

void mutate(struct Tour * tour, double mutationRate, unsigned nCities) {
    unsigned city2;
    for (unsigned city1 = 0; city1 < nCities; ++city1) {
        double random = (double)rand() / (double)RAND_MAX;
        if (random < mutationRate) {
            city2 = rand() % nCities;
            while (city2 == city1) {
                city2 = rand() % nCities;
            }
            unsigned temp = tour->solution[city1];
            tour->solution[city1] = tour->solution[city2];
            tour->solution[city2] = temp;
        }
    }
}

// TODO implement
struct Tour * getBest(struct Population * pop) {
    return pop->tours[0];
}

// TODO check if it's right
struct Tour * TSelection(struct Population * pop) {
    struct Population * newPop = malloc(sizeof(struct Population));
    if (!newPop) {
        return 0;
    }
    newPop->size = 5;
    struct Tour ** tours = malloc(sizeof(struct Tour *) * 5);
    if (!tours) {
        return 0;
    }
    for (unsigned i = 0; i < newPop->size; ++i) {
        tours[i] = pop->tours[rand() % pop->size];
    }
    free(tours);
    struct Tour * best = getBest(newPop);
    free(newPop);
    return best;
}

struct Population * evolve(struct Population * pop, double mutationRate,
        unsigned elitism, struct Instance * instance) {
    // initialize population
    struct Population * newPopulation = malloc(sizeof(struct Population));
    if (!newPopulation) {
        return 0;
    }
    struct Tour ** newTours = malloc(sizeof(struct Tour *) * pop->size);
    if (!newTours) {
        return 0;
    }
    newPopulation->tours = newTours;
    newPopulation->size = pop->size;

    unsigned elitismN = 0;
    if (elitism) {
        struct Tour * best = getBest(pop);

        // not so sure about this line
        // it's the first one, so maybe it's like this
        newPopulation->tours[0] = best;
        elitismN = 1;
    }

    for (unsigned i = elitismN; i < newPopulation->size; ++i) {
        struct Tour * parent1 = TSelection(pop);
        struct Tour * parent2 = TSelection(pop);
        // nCities is going to be moved to instance
        struct Tour * child = crossover(parent1, parent2, instance->nCities);
        mutate(child, mutationRate, instance->nCities);

        TwoOpt(child, 15);
        newPopulation->tours[i] = child;
    }

    // TODO check if it's right
    for (unsigned i = 0; i < newPopulation->size; ++i) {
        if (pop->tours[i] != newPopulation->tours[0]) {
            free((pop->tours[i])->solution);
            free(pop->tours[i]);
        }
    }
    free(pop);

    return newPopulation;
}

unsigned * gen(unsigned * solution, unsigned populationSize, double mutationRate,
        unsigned tournamentSize, unsigned elitism, unsigned generations,
        struct Instance * instance) {
    // command to set the seed of the random function
    // srand(seed);
    // srandom(seed); // It should be Linux specific
    struct Population * pop = malloc(sizeof(struct Population));
    if (!pop) {
        return 0;
    }
    generatePopulation(pop, instance);
    for (unsigned i = 0; i < generations; ++i) {
        printf("Migliore: %f", getBest(pop)->fitness);
        pop = evolve(pop, mutationRate, elitism, instance);
    }

    struct Tour * t = getBest(pop);
    // TODO free everything here
    return t->solution;
    //return getBest(pop)->solution;
}

unsigned * createDistMaxtrix(struct Instance * instance, struct City ** cities) {
    unsigned nCities = instance->nCities;
    unsigned * distMatrix =
        malloc(sizeof(unsigned) * nCities * nCities);
    if (!distMatrix) {
        return 0;
    }
    for (unsigned i = 0; i < nCities; ++i) {
        for (unsigned j = 0; j < nCities; ++j) {
            if (i == j) {
                distMatrix[i * nCities + j] = 0;
            } else {
                distMatrix[i * nCities + j] = 
                    round(sqrt(pow(cities[i]->x - cities[j]->x, 2.0) + 
                                pow(cities[i]->y - cities[j]->y, 2.0)));
                distMatrix[j * nCities + i] = distMatrix[i * nCities + j];
            }
        }
    }
    return distMatrix;
}

struct Instance * readProblem(char ** argv) {
    struct Instance * instance = malloc(sizeof(struct Instance));
    if (!instance) {
        return 0;
    }
    char line[50];
    unsigned i = 0;
    char[20] path;
    // TODO check if it's the right path
    strcpy(path, "../problems/");
    strcpy(path, argv[1]);
    FILE* file = fopen(path, "r");
    struct City * city = 0;
    struct City ** cities = 0;
    while (fgets(line, 50, file)) {
        if (!strcmp(line, "EOF")) {
            break;
        }
        if (i == 3) {
            scanf("DIMENSION : %d", &(instance->nCities));
            cities = malloc(sizeof(struct City *) * instance->nCities);
            if (!cities) {
                return 0;
            }
        }
        if (i == 5) {
            scanf("BEST_KNOWN : %d", &(instance->bestKnown));
        }
        if (i > 6) {
            city = malloc(sizeof(struct City));
            if (!city) {
                for (unsigned j = 7; j < i; ++j) {
                    free(cities[j]);
                }
                return 0;
            }
            scanf("%u %lf %lf", &(city->id), &(city->x), &(city->y));
            cities[i-7] = city;
        }
        ++i;
    }
    createDistMaxtrix(instance, cities);
    for (unsigned i = 0; i < instance->nCities; ++i) {
        free(cities[i]);
    }
    free(cities);
    fclose(file);
    return instance;
}

void checksolution(unsigned * sol) {
}

int main(int argc, char **argv) {
    printf("%f", pow(2, 3));
    if (argc < 2) {
        return 1;
    }
    struct Instance * instance = readProblem(argv);
    unsigned * solution = nearestNeighbour(instance);
    solution = gen(solution, 30, 0.015, 5, 1, 10, instance);
    checksolution(solution);
    free(instance->distMatrix);
    free(instance);
    free(solution);
}
