
import numpy as np
import pickle

def getI_vector(N,F,T,SigmaInv,t_dim):
    
    I = np.eye(t_dim)
    TSinv = (T.T)*SigmaInv
    cov_i = I + ((TSinv*N).dot(T))
    V = np.dot(TSinv,F)
    ivector = np.dot(np.linalg.pinv(cov_i) ,V)
    
    return ivector

def cosineSimilarity(w_enroll,w_test):
    
    return np.dot(w_enroll,w_test)/(np.linalg.norm(w_enroll)*np.linalg.norm(w_test))
    
def trainTotalVariability(N,F,ubm,num_speakers,num_Components,n_iter=3):
    
    I = np.eye(num_speakers)
    sigma = np.linalg.pinv(ubm.covariances_)
    T =  np.random.rand(sigma.shape[0],sigma.shape[1],num_speakers)
    print("T",T.shape)
    print("sinv",T.shape)
    
    for i in range(n_iter):
        
        TinvS = np.dot((T.T),sigma)
        print("TinvS",TinvS.shape)
        
        Ey = np.zeros((num_speakers,1))
        Eyy = np.zeros((num_speakers,1))
        Linv = np.zeros((num_speakers,1))
        
        for s in range(num_speakers):
            print("N[s]",N[s].shape)
            
            L = (I + np.dot(np.dot(TinvS,N[s]),T))
            Linv[s] = np.linalg.pinv(L)
            Ey[s] = np.dot(np.dot(Linv[s],TinvS[s]),(F[s]))
            Eyy[s] = Linv[s] + Ey[s]*Ey[s].T
             
        C = np.sum(F*Ey.T)
        print(C.shape)

        newT = np.zeros((num_Components,1))
        for c in range(num_Components):
            Ac = np.zeros(num_speakers)
            for s in range(num_speakers):
                Ac = Ac + N[s][c]*Eyy[s]

            newT[c] = (np.linalg.pinv(Ac)*C[c]).T

        T = newT
    return T


def __map_adaptation(self, gmm, data, max_iterations = 10, likelihood_threshold = 1e-20, relevance_factor = 16):
        N = data.shape[0]
        D = data.shape[1]
        K = gmm.n_components
        
        mu_new = np.zeros((K,D))
        n_k = np.zeros((K,1))
        
        mu_k = gmm.means_
        cov_k = gmm.covariances_
        pi_k = gmm.weights_

        old_likelihood = gmm.score(data)
        new_likelihood = 0
        iterations = 0
        while(abs(old_likelihood - new_likelihood) > likelihood_threshold and iterations < max_iterations):
            iterations += 1
            old_likelihood = new_likelihood
            z_n_k = gmm.predict_proba(data)
            n_k = np.sum(z_n_k,axis = 0)

            for i in range(K):
                temp = np.zeros((1,D))
                for n in range(N):
                    temp += z_n_k[n][i]*data[n,:]
                mu_new[i] = (1/n_k[i])*temp

            adaptation_coefficient = n_k/(n_k + relevance_factor)
            for k in range(K):
                mu_k[k] = (adaptation_coefficient[k] * mu_new[k]) + ((1 - adaptation_coefficient[k]) * mu_k[k])
            gmm.means_ = mu_k

            log_likelihood = gmm.score(data)
            new_likelihood = log_likelihood
            
        return gmm

def save_model(model,file):        
    pickle.dump(model,open(file,"wb"))

def logLiklihoodRatio(self,logModelA, logModelB):
    return logModelA - logModelB