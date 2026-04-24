#include <mpi.h>
#include <iostream>
#include <vector>

using namespace std;

int main(int argc, char* argv[]) {

    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    vector<int> orders = {101,102,103,104,105};
    int stock = 3;

    MPI_Bcast(&stock, 1, MPI_INT, 0, MPI_COMM_WORLD);

    for (int i = rank; i < orders.size(); i += size) {

        if (orders[i] <= 103) {
            cout << "Process " << rank
                 << " processed Order "
                 << orders[i]
                 << " SUCCESS" << endl;
        }
        else {
            cout << "Process " << rank
                 << " processed Order "
                 << orders[i]
                 << " FAILED - Out of Stock" << endl;
        }
    }

    MPI_Finalize();
    return 0;
}

