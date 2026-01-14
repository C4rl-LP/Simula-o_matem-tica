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


fig = go.Figure(data=[
    
    go.Surface(x=x_esf, y=y_esf, z=z_esf, opacity=0.7, colorscale='Blues', showscale=False),
    go.Scatter3d(x= x_bra_f, y= y_bra_f, z= z_bra_f,mode='markers',
                 marker=dict(size=5, color='red'))
])

fig.update_layout(title='Esfera com Plotly', autosize=True,
                  scene=dict(aspectmode='data')) # Mantém a proporção correta

                  # Salvar como HTML interativo
fig.write_html("esfera_plotly.html")
# Para mostrar diretamente no notebook ou em uma nova janela
fig.show()

#Plotar projeção

def projeção_mercator(phi,teta):
    return teta, np.log(np.tan(phi/2+np.pi/4))

teta_esq = -np.pi
Collecting package metadata (repodata.json): / 
teta_dir =  np.pi

phi_min = -np.deg2rad(85)
phi_max =  np.deg2rad(85)



x_esq, y_sup = projeção_mercator(phi_max, teta_esq)
x_dir, y_inf = projeção_mercator(phi_min, teta_dir)

#Brasil!!
plt.figure(figsize=(8,6))
plt.scatter(x_esq, y_sup)
plt.scatter(x_dir, y_inf)
plt.scatter(x_esq, y_inf)
plt.scatter(x_dir, y_sup)



plt.scatter(projeção_mercator(phi_bra, teta_bra)[0], projeção_mercator(phi_bra, teta_bra)[1])
plt.show()

        