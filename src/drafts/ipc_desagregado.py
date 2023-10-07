import pandas as pd
from io import StringIO
import plotly.graph_objects as go

data = """
3	Alimentos	22.8353%
4	Pan y cereales	5.2910%
4	Carne	7.3125%
4	Pescado	0.5494%
4	Leche, queso y huevos	3.0382%
4	Aceites y grasas	0.7059%
4	Frutas	1.6553%
4	Legumbres y Hortalizas	2.6011%
4	Azúcar, mermelada, miel, chocolate y dulces de azúcar	1.1462%
4	Productos alimenticios n.e.p.	0.5357%
3	Bebidas no alcohólicas	3.2213%
4	Café, te y cacao	1.0231%
4	Aguas minerales, refrescos, jugos de frutas y de legumbres	2.1982%
2	Bebidas Alcohólicas, Tabaco y Estupefacientes	4.2936%
3	Bebidas alcohólicas	1.4583%
4	Bebidas destiladas	0.2892%
4	Vino	0.7917%
4	Cerveza	0.3774%
3	Tabaco	2.8353%
4	Tabaco	2.8353%
2	Prendas de Vestir y Calzados	5.3748%
3	Prendas de vestir	3.8592%
4	Prendas de vestir	3.4975%
4	Limpieza, reparación y alquiler de prendas de vestir	0.3617%
3	Calzado	1.5156%
4	Zapatos y otros calzados	1.3158%
4	Reparación y alquiler de calzado	0.1998%
2	Vivienda	13.6778%
3	Alquileres efectivos del alojamiento	3.6580%
4	Alquileres efectivos pagados por los inquilinos	3.6580%
3	Conservación y reparación de la vivienda	0.7306%
4	Materiales para la conservación y la reparación de la vivienda	0.4087%
4	Servicios para la conservación y la reparación de la vivienda	0.3219%
3	Suministro de agua y servicios diversos relacionados con la vivienda	3.2742%
4	Suministro de agua	1.2624%
4	Recogida de basuras	0.6567%
4	Alcantarillado	0.2946%
4	Otros servicios relacionados con la vivienda n.e.p.	1.0605%
3	Electricidad, gas y otros combustibles	6.0150%
4	Electricidad	4.5993%
4	Gas	0.8709%
4	Combustibles sólidos	0.5448%
2	Muebles, Artículos Para el Hogar y Para la Conservación Ordinaria del Hogar	5.7320%
3	Muebles y accesorios, alfombras y otros materiales para pisos	1.0487%
4	Muebles y accesorios	1.0487%
3	Productos textiles para el hogar	0.3832%
4	Productos textiles para el hogar	0.3832%
3	Artefactos para el hogar	0.7338%
4	Artefactos para el hogar grandes, eléctricos o no	0.4912%
4	Reparación de artefactos para el hogar	0.2426%
3	Artículos de vidrio y cristal, vajilla y utensilios para el hogar	0.1311%
4	Artículos de vidrio y cristal, vajilla y utensilios para el hogar	0.1311%
3	Herramientas y equipo para el hogar y el jardín	0.1692%
4	Herramientas y equipo grandes	0.0620%
4	Herramientas pequeñas y accesorios diversos	0.1072%
3	Bienes y servicios para conservación ordinaria del hogar	3.2660%
4	Bienes para el hogar no duraderos	1.2666%
4	Servicios domésticos y para el hogar	1.9994%
2	Salud	7.7090%
3	Productos, artefactos y equipo médicos	1.5376%
4	Productos farmacéuticos	1.0840%
4	Artefactos y equipo terapéuticos	0.4536%
3	Servicios para pacientes externos	0.9963%
4	Servicios médicos	0.1061%
4	Servicios dentales	0.6155%
4	Servicios paramédicos	0.2747%
3	Servicios de hospital	0.1492%
4	Servicios de hospital	0.1492%
3	Servicios médicos mutuales y colectivos	5.0259%
4	Servicios médicos mutuales y colectivos	5.0259%
2	Transporte	10.1316%
3	Adquisición de vehículos	1.5504%
4	Vehículos a motor	1.2492%
4	Motocicletas	0.2675%
4	Bicicletas	0.0337%
3	Funcionamiento de equipo de transporte personal	5.6888%
4	Piezas de repuesto y accesorios para equipo de transporte personal	0.3847%
4	Combustibles y lubricantes para equipo de transporte personal	2.3103%
4	Conservación y reparación de equipo de transporte personal	1.6661%
4	Otros servicios relativos al equipo de transporte personal	1.3277%
3	Servicios de transporte	2.8924%
4	Transporte de pasajeros por carretera	2.3772%
4	Transporte de pasajeros por aire	0.3735%
4	Transporte de pasajeros por mar y cursos de agua interiores	0.0176%
4	Transporte combinado de pasajeros	0.0154%
4	Otros servicios de transporte adquiridos	0.1087%
2	Comunicaciones	3.3580%
3	Servicios postales	0.0526%
4	Servicios postales	0.0526%
3	Equipo telefónico y de facsímile	0.2829%
4	Equipo telefónico y de facsímile	0.2829%
3	Servicios telefónicos y de facsímile	3.0225%
4	Servicios telefónicos y de facsímile	3.0225%
2	Recreación y Cultura	6.4918%
3	Equipo audiovisual, fotográfico y de procesamiento de información	0.5697%
4	Equipo para la recepción, grabación y reproducción de sonidos e imágenes	0.2446%
4	Equipo fotográfico, cinematográfico e instrumentos ópticos	0.0492%
4	Equipo de procesamiento e información	0.1713%
4	Medios para grabación	0.1046%
3	Otros artículos y equipo para recreación, jardines y animales domésticos	1.1045%
4	Juegos, juguetes y aficiones	0.2196%
4	Jardines, plantas y flores	0.1579%
4	Animales domésticos y productos conexos	0.5749%
4	Servicios de veterinaria y de otro tipo para animales domésticos	0.1521%
3	Servicios de recreación y culturales	3.6749%
4	Servicios de recreación y deportivos	0.8463%
4	Servicios culturales	1.3939%
4	Juegos de azar	1.4347%
3	Periódicos, libros y papeles y útiles de oficina	0.7211%
4	Libros	0.3639%
4	Diarios y periódicos	0.1898%
4	Papel y útiles de oficina y materiales de dibujo	0.1674%
3	Paquetes turísticos	0.4216%
4	Paquetes turísticos	0.4216%
2	Educación	3.1421%
3	Enseñanza preescolar y enseñanza primaria	1.0064%
4	Enseñanza preescolar o enseñanza primaria	1.0064%
3	Enseñanza secundaria	0.8887%
4	Enseñanza secundaria	0.8887%
3	Enseñanza terciaria	0.3745%
4	Enseñanza terciaria	0.3745%
3	Enseñanza no atribuible a ningún nivel	0.8725%
4	Enseñanza no atribuible a ningún nivel	0.8725%
2	Restaurantes y Hoteles	7.7021%
3	Servicios de suministro de comidas por contrato	7.3492%
4	Restaurantes, cafés y establecimientos similares	7.2706%
4	Comedores	0.0786%
3	Servicios de alojamiento	0.3529%
4	Servicios de alojamiento	0.3529%
2	Bienes y Servicios Diversos	6.3306%
3	Cuidado personal	3.1917%
4	Salones de peluquería y establecimientos de cuidados personales	0.8993%
4	Otros aparatos, artículos y productos para la atención personal	2.2924%
3	Efectos personales n.e.p.	0.1909%
4	Otros efectos personales	0.1909%
3	Seguros	1.5956%
4	Seguro relacionado con la vivienda	0.1095%
4	Seguro relacionado con el transporte	1.4861%
3	Otros servicios n.e.p.	1.3524%
4	Otros servicios n.e.p.	1.3524%
"""

# Use StringIO to convert the string data into a file-like object so it can be read into a pandas dataframe
data_io = StringIO(data)

# Read the data into a pandas dataframe
df = pd.read_csv(data_io, sep='\t', header=None)

# Assign headers
df.columns = ['Level', 'Category', 'Percentage']
df['Percentage'] = df['Percentage'].str.rstrip('%').astype('float') / 100.0

# Create the treemap
fig = go.Figure(go.Treemap(
    labels=df['Level'],
    parents=df['Category'],
    values=df['Percentage'],
))

fig.show()





