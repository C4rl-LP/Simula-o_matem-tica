import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


#phi latitude 
#teta longitude
def esfe_cart(phi,teta,r):
    x = -r * np.cos(phi) * np.cos(teta)
    y = -r * np.cos(phi) * np.sin(teta)
    z = r * np.sin(phi)
    return x,y,z

def ler_coordenadas(file_name):
    with open(file_name, 'r') as f:
        lat =[]
        long =[]
        for line in f:
            
            b,a = line.split()
            lat.append(float(a))
            long.append(float(b))
    return lat, long 

def projeção_mercator(phi,teta):
    return teta, np.log(np.tan(phi/2+np.pi/4))



#----------------------------------------------------------------------
#----------- Coordenadas ----------------------------------------------
#----------------------------------------------------------------------
lat, long = ler_coordenadas("border_main.txt")
lat = np.array(lat)
long = np.array(long)

phi_bra = lat*np.pi/180 
teta_bra = long*np.pi/180


teta_esf = np.linspace(-np.pi, np.pi, 100)
phi_esf = np.linspace(-np.pi/2, np.pi/2, 50)
teta_esf, phi_esf = np.meshgrid(teta_esf,phi_esf)
r=1

x_esf, y_esf, z_esf = esfe_cart( phi_esf,teta_esf, r)
x_bra_f, y_bra_f, z_bra_f = esfe_cart( phi_bra, teta_bra, r)

lat_rj = -22.90
lon_rj = -43.20
phi_rj = lat_rj * np.pi/ 180
teta_rj = lon_rj * np.pi/ 180

lat_bb = -27.47
lon_bb = 153.02
phi_bb = lat_bb * np.pi/ 180
teta_bb = lon_bb * np.pi/ 180

x_rj_bb, y_rj_bb, z_rj_bb = esfe_cart(np.array([phi_rj, phi_bb]), np.array([teta_rj, teta_bb]), r)

#----------------------------------------------------------------------
#----------- Laxodromia brisbane ao rio -------------------------------
#----------------------------------------------------------------------

x_merc_rj, y_merc_rj = projeção_mercator(phi_rj, teta_rj)
x_merc_bb, y_merc_bb = projeção_mercator(phi_bb, teta_bb)

x_laxo = np.linspace(x_merc_rj, x_merc_bb,100 )
y_laxo = np.linspace(y_merc_rj, y_merc_bb,100 )

phi_laxo = np.arcsin(np.tanh(y_laxo/r))
teta_laxo = x_laxo/r

x_laxo_esf, y_laxo_esf, z_laxo_esf = esfe_cart(phi_laxo, teta_laxo, r)

#----------------------------------------------------------------------
#----------- Geodésica brisbane ao rio --------------------------------
#----------------------------------------------------------------------

r_rj = np.array([x_rj_bb[0], y_rj_bb[0], z_rj_bb[0]])
r_bb = np.array([x_rj_bb[1], y_rj_bb[1], z_rj_bb[1]])



""" Aqui vou parametrizar a geodésica da segunite forma:
        * Determinar apartir do produto interno o angulo entre vetores p1 e p2 tal que p1, p2 são os 
        vetores posição da localidade em relação ao centro da esfera.
        * Em seguida vamos escolher um vetor unitário u tal que u.p1 =1, u = p1/|p1| = p1/r. agora vamos usar
        p2 para constuir v tal que v.u = 0. Vamos tomar v = p2 - (p2.u)u/ | p2 - (p2.u)u |
        * Agora resta parmetrizar a curva usando a base u e v:
            curva(t) = R(u cos(t) + v sin(t)) t vai de 0 até o angulo entre os dois pontos Thet
        cos (Thet) = u.v

"""
u = r_rj / np.linalg.norm(r_rj)
proj = np.dot(r_bb, u) * u
v = r_bb - proj
v = v / np.linalg.norm(v)

Theta = np.arccos(np.dot(u, r_bb))/np.linalg.norm(r_bb)

def geodesica(t):
    return u*np.cos(t) + v*np.sin(t)

t_vals = np.linspace(0, Theta, 200)
curve = np.array([geodesica(t) for t in t_vals])

x_geo, y_geo, z_geo = curve[:,0], curve[:,1], curve[:,2]


#----------------------------------------------------------------------
#----------- Plot em 3D -----------------------------------------------
#----------------------------------------------------------------------

fig = go.Figure(data=[
    
    go.Surface(x=x_esf, y=y_esf, z=z_esf, opacity=0.7, colorscale='Blues', showscale=False),
    go.Scatter3d(x= x_bra_f, y= y_bra_f, z= z_bra_f,mode='markers',
                 marker=dict(size=1, color='red')),
    go.Scatter3d(x= x_rj_bb, y= y_rj_bb, z= z_rj_bb,mode='markers',
                 marker=dict(size=5, color='green')),
    go.Scatter3d(x= x_laxo_esf, y= y_laxo_esf, z= z_laxo_esf,mode='lines',
                  line=dict(color='blue', width=6),
        name='Laxodromia'),
    go.Scatter3d(
        x=x_geo, y=y_geo, z=z_geo,
        mode='lines',
        line=dict(color='black', width=6),
        name='Geodésica'
    )
    
])

fig.update_layout(title='Esfera com Plotly', autosize=True,
                  scene=dict(aspectmode='data')) # Mantém a proporção correta

                  # Salvar como HTML interativo
fig.write_html("esfera_plotly.html")
# Para mostrar diretamente no notebook ou em uma nova janela
fig.show()



#----------------------------------------------------------------------
#----------- Plot projeção --------------------------------------------
#----------------------------------------------------------------------
#Plotar projeção


#Brasil!!
'Plotar retas delimitando o mapa'
plt.figure(figsize=(8,6))

plt.plot(x_laxo, y_laxo)

plt.scatter(
    projeção_mercator(phi_bra, teta_bra)[0],
    projeção_mercator(phi_bra, teta_bra)[1],
    s=1
)

plt.gca().set_aspect('equal', adjustable='box')  # <<< ESSENCIAL
plt.grid()
plt.show()
        