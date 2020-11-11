
import numpy as np
import pickle
import copy

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


def map_adaptation(model, data, max_iterations = 10, likelihood_threshold = 1e-20, relevance_factor = 16):
        gmm = copy.deepcopy(model)
        N = data.shape[0] #number of frames
        D = data.shape[1] #number of features (vector length)
        K = gmm.n_components #number of Gaussians
        
        E = np.zeros((K,D)) 
        n_k = np.zeros((K,1))
        
        mu_k = gmm.means_

        old_likelihood = gmm.score(data)
        new_likelihood = 0
        iterations = 0
        while(abs(old_likelihood - new_likelihood) > likelihood_threshold and iterations < max_iterations):
            iterations += 1
            old_likelihood = new_likelihood
            pr = gmm.predict_proba(data) #posterior probability
            n_k = np.sum(pr,axis = 0) 

            for i in range(K):
                temp = np.zeros((1,D))
                for n in range(N):
                    temp = temp + pr[n][i]*data[n,:]
                E[i] = (1/n_k[i])*temp

            adaptation_coefficient = n_k/(n_k + relevance_factor)
            for k in range(K):
                mu_k[k] = (adaptation_coefficient[k] * E[k]) + ((1 - adaptation_coefficient[k]) * mu_k[k])
            gmm.means_ = mu_k

            log_likelihood = gmm.score(data)
            new_likelihood = log_likelihood


        return gmm

def hmmMapAdapt(model, data, max_iterations = 10, likelihood_threshold = 1e-20, relevance_factor = 16):
    hmm = copy.deepcopy(model)
    N = data.shape[0]
    D = data.shape[1]
    C = hmm.n_mix
    S = hmm.n_components


    old_likelihood = hmm.score(data)
    new_likelihood = 0
    iterations = 0
    while(abs(old_likelihood - new_likelihood) > likelihood_threshold and iterations < max_iterations):
        iterations += 1
        old_likelihood = new_likelihood

        probability = hmm.predict_proba(data) #
        
        # n_k = np.sum(probability, axis=0)
        # np.seterr(divide='ignore', invalid='ignore')
        # E = np.zeros((D, K), dtype=np.float32)
        # for ii in range(0, K):
        #     probability_gauss = np.tile(probability[:, ii],(D, 1)).T * data
        #     E[:, ii] = np.sum(probability_gauss, axis=0) / n_k[ii]
        
        # alpha = n_k / (n_k + relevance_factor)

        # mu_k = gmm.means_
        # E = np.zeros((K,D), dtype=np.float32)

        # for ii in range(0, K):
        #     E[ii,:] = (alpha[ii] * E[:,ii]) + ((1 - alpha[ii]) * mu_k[ii, :])

        # gmm.means_ = E

        log_likelihood = hmm.score(data)
        new_likelihood = log_likelihood

    return hmm

def save_model(model,file):        
    pickle.dump(model,open(file,"wb"))

def save_model(model, file, model_use, modelType ='gmm'):
    dict_to_save = {}
    dict_to_save['purpose'] = model_use

    if (modelType=='gmm'):      

        dict_to_save['means'] = model.means_.tolist()
        dict_to_save['covars'] = model.covariances_.tolist()
        dict_to_save['weights'] = model.weights_.tolist()


def logLiklihoodRatio(self,logModelA, logModelB):
    return logModelA - logModelB