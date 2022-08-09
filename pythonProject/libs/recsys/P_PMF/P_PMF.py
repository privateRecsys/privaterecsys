def extern from "cP_PMF.h":
    void P_PMF(double *removedData, double *predData, int numUser,
		int numService, int dim, double lmda, int maxIter, double etaInit,
    	double *Udata, double *Sdata, double *bs, bool debugMode)


#=====================================================#
# Function to perform the prediction algorithm
# Wrap up the C++ implementation
#======================================================#
def predict(removedMatrix, para):
    cdef int numService = removedMatrix.shape[1]
    cdef int numUser = removedMatrix.shape[0]
    cdef int dim = para['dimension']
    cdef double lmda = para['lambda']
    cdef int maxIter = para['maxIter']
    cdef double etaInit = para['etaInit']
    cdef bool debugMode = para['debugMode']

    # initialization
    cdef np.ndarray[double, ndim=2, mode='c'] U = np.random.rand(numUser, dim)
    cdef np.ndarray[double, ndim=2, mode='c'] S = np.random.rand(numService, dim)
    cdef np.ndarray[double, ndim=1, mode='c'] bs = np.random.rand(numService)
    cdef np.ndarray[double, ndim=2, mode='c'] predMatrix = np.zeros((numUser, numService))

    # Wrap up cP_PMF.cpp
    P_PMF(
    	  <double *> (<np.ndarray[double, ndim=2, mode='c']> removedMatrix).data,
          <double *> predMatrix.data,
          numUser,
          numService,
          dim,
          lmda,
          maxIter,
          etaInit,
          <double *> U.data,
          <double *> S.data,
          <double *> bs.data,
          debugMode
         )

    return predMatrix