# Práctica 3: Filtro de Kalman Extendido en ROS 2

En esta práctica se ha implementado un filtro de Kalman Extendido para la estimación de la pose de un robot móvil. Se han implementado 3 modelos de este filtro:

**1. Modelo 3D:** Se estima la posición y orientación, $(x,y,θ)$, del robot.

**2. Modelo 7D:** Estima la posición, la orientación, la velocidad linear, la velocidad angular y la aceleración en x y en y del robot, $(x,y,θ,v,ω,a_x,a_y)$.

**3. Modelo 8D:** Igual que el modelo 7D, pero separando la velocidad lineal en los ejes x e y, $(x,y,θ,v_x,v_y,ω,a_x,a_y)$.


## Modelo 3D
### Caso base
En este caso, se han mantenido los ruidos base siguientes:
- Incertidumbre en la observación: [1.02, 1.02, 100.01].
- Incertidumbre en el modelo: [0.002, 0.002, 0.001].
  
En este caso, puede observarse que el modelo no es lo suficientemente bueno por lo que la salida del filtro tiene un error muy elevado, especialmente al principio, aunque luego se aproxima al valor real.

Al ser las incertidumbres relativamente bajas, el valor de Σ es muy pequeño, casi imperceptible incluso, a pesar del enorme error existente entre la realidad y la salida del filtro.

![EKF3D_base](https://github.com/user-attachments/assets/4a5e4543-d49a-4dff-be6e-7ae13d65da45)


### Alta incertidumbre en la observación
En este caso, se ha mantenido el ruido base en el modelo, pero se ha establecido el siguiente ruido en la observación: [100, 100, 100]. Estos valores tan grandes garantizan una incertidumbre en la medida mucho mayor que en el modelo.

Puede verse que al no ser tan bueno el modelo, y sin embargo atribuirle un ruido mucho menor que a la observación, mantiene un error elevado. Se aprecia además que el modelo tiene tendencia a moverse en el eje x más que el robot real, por lo que el error en el eje x que hay al principio se mantiene aproximadamente al final por la forma de la trayectoria. 

Por otro lado, al aumentar la incertidumbre, el valor de Σ es mayor que en el caso anterior.

![EKF3D_RAObs](https://github.com/user-attachments/assets/a99ee426-dbc5-4142-84cf-1fc12a0ac881)


### Alta incertidumbre en el modelo
En este último caso, se ha mantenido el ruido en la observación como en el primer caso, mientras que se ha aumentado la incertidumbre en el proceso: [0.1, 0.1, 0.1]. Pese a seguir teniendo valores menores que el ruido en la medida, es lo suficientemente grande como para que la observación eclipse al modelo en la estimación de la pose del robot.

Dado que la observación se acerca a la realidad mucho más que el proceso, el error de la salida del filtro es también mucho menor. Sin embargo, este error nunca es menor que el de la propia observación, llegando incluso a, finalmente, solaparse completamente la observación y la salida del filtro.

El valor de Σ también es mayor que en el primer caso, pero converge mucho más rápidamente que en el segundo.

![EKF3D_RAProc](https://github.com/user-attachments/assets/0e73c3d6-521e-49c2-a03e-d33ff666a1b7)


## Modelo 7D
### Caso base
En el primer caso de este modelo, se han mantenido los siguientes ruidos base:
- Incertidumbre en la observación: [100.0, 100.0, 1000.0, 6.853891945200942e-06, 1.0966227112321507e-06, 0.0015387262937311438, 0.0015387262937311438].
- Incertidumbre en el modelo: [0.1, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1].
  
En este primer caso, de igual forma que con el modelo 3D, el modelo no es lo muy bueno por lo que la salida del filtro tiene un error alto. Sin embargo, tiene un comportamiento mejor que el modelo 3D.

Al contrario que el modelo 3D, en el modelo base las incertidumbres son lo suficientemente altas como para apreciar claramente el valor de Σ.

![EKF7D_base](https://github.com/user-attachments/assets/cb11a1aa-1d54-4e28-9cd3-7a4b448a1d57)



### Alta incertidumbre en la observación
Se ha mantenido el ruido del modelo igual al caso base, pero aumentando el ruido en la observación de forma que el filtro de más importancia a la predicción: [200.0, 200.0, 2000.0, 1.0, 1.0, 1.0, 1.0].

Dado que el modelo del caso 7D es mejor que el del 3D, la salida del filtro da mejores resultados en la versión 7D que en la 3D, habiendo tramos que incluso solapa con el Ground-Truth. Sin embargo, también existen otros tramos en los que la observación tiene un error menor que la salida del filtro. 

A pesar de haber aumentado el valor de la incertidumbre de la observacion, el filtro ha convergido más rápidamente que en el experimento anterior, por lo que el valor de Σ no tiene una diferencia apreciable respecto del experimento anterior.

![EKF7D_RAObs](https://github.com/user-attachments/assets/0a836daa-583c-4052-8598-236ee06d6df4)



### Alta incertidumbre en el modelo
En este caso, de igual forma que con el modelo 3D, se ha mantenido la incertidumbre en la observación base a la vez que se ha aumentado la del proceso: [5, 5, 5, 5, 5, 5, 5]. En este experimento, la salida del filtro dependerá más de la actualización que de la predicción.

De forma similar a como ocurría con la versión 3D, en esta versión del modelo 7D la salida del filtro es casi idéntica a la medida, por lo que su error es aproximadamnte igual al error de la propia medida.

Dado que en esta versión el filtro converge mucho más rápidamente que ambas versiones anteriores del modelo 7D, el valor de Σ es también mucho menor.

![EKF7D_RAProc](https://github.com/user-attachments/assets/d8d00adf-5a80-4422-aa7a-fe67205d2da5)



## Modelo 8D
### Caso base
En el caso base del modelo 8D, se han definido las siguientes incertidumbres base:
- Incertidumbre en la observación: [100.0, 100.0, 1000.0, 6.853891945200942e-06, 1.0966227112321507e-06, 0.0015387262937311438, 0.0015387262937311438].
- Incertidumbre en el modelo: [0.1, 0.1, 0.05, 0.1, 0.1, 0.1, 0.1, 0.1].
  
En la experimentación, puede verse que el modelo es relativamente parecido al modelo 7D en cuanto al error a la salida del filtro, y por consiguiente arroja mejores resultados que el modelo 3D. Sin embargo, la observación sigue dando valores más parecidos a los reales que la predicción.

No obstante, el valor de Σ es mayor que en el caso base del modelo 3D y menor que en el del 7D, pues las incertidumbres son mayores que en el 3D y este filtro converge más rápido que el 7D en circunstancias parecidas.

![EKF8D_base](https://github.com/user-attachments/assets/ca148bd2-dc87-4e70-8aa7-1e9d0a8e3249)



### Alta incertidumbre en la observación
En el segundo caso, la incertidumbre del modelo se ha mantenido igual, pero se ha modificado el ruido en la observación: [200.0, 200.0, 2000.0, 1.0, 1.0, 1.0, 1.0], dando mayor importancia a la predicción que a la actualización.

A partir de la gráfica resultante de la experimentación, puede verse que el modelo del sistema mejora a la versión 3D, aunque sus resultados no mejoran a los del modelo 7D. Sin embargo, el valor de Σ, aunque mayor que la versión 3D (al ser las incertidumbres mayores) y aproximadamente igual al caso con incertidumbres base, es bastante menor que en el modelo 7D.

![EKF8D_RAObs](https://github.com/user-attachments/assets/e4a6c00b-7577-4ae7-aa6c-7a9dd70775b6)



### Alta incertidumbre en el modelo
Finalmente, se ha restaurado el ruido en la observación a los valores base y se ha aumentado la incertidumbre en el proceso: [5, 5, 5, 5, 5, 5, 5, 5]. De forma análoga a los modelos 3D y 7D, en este caso el filtro dará mayor importancia a los resultados de la actualización que a los de la predicción.

En este último caso, el comportamiento del filtror es similar a los otros dos modelos, pues la salida del filtro se asemeja enormemente a los valores medidos, teniendo aproximadamente el mismo error que estos. Ya que se ha comprobado en los casos anteriores que los valores de la observación se asemejan más a la realidad que los resultados del modelo, al aumentar la incertidumbre del proceso disminuye el error a la salida del filtro.

Además, dado que los resultados convergen mucho más rápido que en los casos anteriores, y aunque la incertidumbre sea mayor que en el caso base, el valor de Σ es el menor de todos los experimentos del modelo 8D.

![EKF8D_RAProc](https://github.com/user-attachments/assets/6528a279-37b0-4975-b4c1-3a51a43c8bfc)
