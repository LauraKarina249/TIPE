#TIPE: FIGURES DE CHLADNI
 
import numpy as np
import matplotlib.pyplot as plt
import math
 
 
#Nouvelle valeur de la position
#Oscillations correspond au signal sinusoidal impose
def nouvelle_position(W,oscillations,i,j,n,D,rho,h,dl,dt):
    #print(i,j,n,Nlongueur)
    if i==Nlongueur//2 and j==Nlongueur//2:
         
        return W[n,i,j]
         
    else:
         
        #Conditions pour les bords:
         
        #Pour le temps:
        if n==0 or n==Ntemps-1:
            return W[n,i,j]
         
        #Pour les largeurs:
        if i == 0 or i == 1:
            i = i+2
             
             
        if i == Nlongueur-1 or i == Nlongueur-0:
            i = i-2  
         
 
        #Pour les longueurs:
        if j == 0 or j == 1:
            j = j+2
         
             
        if j == Nlongueur-1 or j == Nlongueur-0:
            j = j-2   
         
         
        return (1/(2*rho*h*(dl**4)-16*D*(dt**2)))*((rho*h*(dl**4))*(W[n+1,i,j]+W[n-1,i,j])+(D*dt)*(W[n,i+2,j]+W[n,i-2,j]+W[n,i,j+2]+W[n,i,j-2]-6*(W[n,i+1,j]+W[n,i-1,j]+W[n,i,j+1]+W[n,i,j-1])+W[n,i+1,j+1]+W[n,i+1,j-1]+W[n,i-1,j+1]+W[n,i-1,j-1]))
         
     
     
#On modifie la totalite du tableau lors d'une oscillation
def iterations(W,oscillations,D,rho,h,dl,dt,Ntemps):
     
    N = len(W[0]) - 1
      
    Wk = np.copy(W) 
     
    for n in range (N):
        #print(n)
     
        for i in range (Nlongueur+1):
         
            for j in range (Nlongueur+1):
                 
                W[n,i,j] = nouvelle_position(Wk,oscillations,i,j,n,D,rho,h,dl,dt)
             
    erreur = np.sqrt(np.sum((W-Wk) ** 2) / (N**2*Ntemps))
                 
    return erreur
     
     
#Fonction d'oscillations
def Germain (iterations,W,oscillations,D,rho,h,dl,dt,Ntemps,eps):
     
    erreur=eps*2
    iter = 0
    while erreur>eps:
        print('iteration',iter)
        erreur=iterations(W,oscillations,D,rho,h,dl,dt,Ntemps)
        iter += 1
         
         
# #On realise des approximations lorsqu'on arrive aux bords (pas besoin) 
# def limite(W):
#     
#     N = len(W) -1
#     
#     #Pour les longueurs
#     for j in range (N+1):
#         
#         if j == 0:
#             j-1 = j+1
#             j-2 = j
#             
#         if j == 1:
#             j-2 = j
#             
#         if j == N-1:
#             j+2 = j    
#         
#         if j == N:
#             j+1 = j-1
#             j+2 = j
#             
#     #Pour les largeurs
#     for i in range (N+1):
#         
#         if i == 0:
#             i-1 = i+1
#             i-2 = i
#             
#         if i == 1:
#             i-2 = i
#             
#         if i == N-1:
#             i+2 = i    
#         
#         if i == N:
#             i+1 = i-1
#             i+2 = i
             
             
#Tableau avec espace: longueur et largeur; temps: hauteur 
def tableau(Nlongueur,Ntemps):
     
    return np.zeros((Ntemps,Nlongueur+1,Nlongueur+1))
     
 
#Definition de la fonction imposee au centre de la plaque
def oscillations(freq,t):
     
    w = 2*np.pi*freq
     
    return 2e-2*np.sin(w*t)
     
     
#Variables a imposer
 
#Longueur, largeur et epaisseur (en m)
dl = 2*3.6*1e-3
L = 18*1e-2
Nlongueur = int(L//dl)+1
h = 0.95*1e-3
 
 
#Temps (en s)
Tobs = 1/120
dt = Tobs/100 #faire attention par rapport a la frequence
Ntemps = int(Tobs//dt)
 
 
#Constante
E = 58*1e9
v = 0.346 #Pour l'aluminium
D = (E*(h**3))/(12*(1-(v**2)))
 
 
#Masse volumique
m = 204.31*1e-3 #kg
V = L*L*h # 3.07*1e-5 #m^3
rho = m/V
 
 
#Condition pour arret de la fonction
eps = 1e-4
 
 
#Creation du tableau:
W = tableau(Nlongueur,Ntemps)
 
 
#Frequence choisie
freq = 120 #(Hz)
t = np.linspace(0,Tobs,Ntemps)
 
 
#Condition au centre du tableau:
W[:,Nlongueur//2,Nlongueur//2] = oscillations(freq,t)
 
#Modification du reste du tableau
Germain(iterations,W,oscillations,D,rho,h,dl,dt,Ntemps,eps)
 
 
#Fonction qui renvoie un tableau ayant des 1 aux endroits ou il y a du sable
def alexandre(Tfin,eps):
     
    k = len(Tfin)
    Image = np.zeros((k,k))
 
    for i in range(k):
        for j in range(k):
            if abs(Tfin[i][j]) < eps:
                Image[i][j] = 1
                 
    return Image
             
             
#Recherche des zeros:
Tfin = W[-3]
 
Image = alexandre(Tfin,eps)
print(Tfin)
import matplotlib.pyplot as plt
 
 
for i in range(Ntemps):
    plt.imshow(W[i])
    plt.savefig('{:03d}.png'.format(i))
    plt.clf()
 
plt.imshow(Image)
plt.show()