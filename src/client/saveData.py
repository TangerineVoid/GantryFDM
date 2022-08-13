from tensorflow.keras import layers
import datetime
import time as t
import numpy as np
import zlib
import base64
import tensorflow as tf
from ast import literal_eval


class SaveData:
    # instance attributes
    def __init__(self):
        self.file = None
        self.classifier = None

    def save_sql(self, val_type, storage_stype ,sqlConnection, val=None):
        if storage_stype == "sql":
            if val_type == "XDK":
                # fname = 'D:/Users/sergio.salinas/Documents/Imager Data/data/' + 'data_' + '.txt'
                print("Saving XDK data")
                for e, x in enumerate(val):
                    if e == len(val) - 1:
                        break
                    else:
                        val[e] = float(x)
                # XDKval[0:14] = np.array(readXDK(0:14)).astype(np.float)
                query = """
                    INSERT INTO tbXDK (
                    ftAccx, ftAccy, ftAccz,
                    ftHum, ftPress, ftTemp,
                    ftMagx, ftMagy, ftMagz, ftR,
                    ftGyx, ftGyy, ftGyz,
                    ftLight, ftNoise,
                    dtDate)
                    VALUES ( 
                    {} , {}, {},
                    {} , {}, {},
                    {} , {}, {},
                    {} , {}, {},
                    {} , {}, {},
                    '{}');
                       """.format(val[0], val[1], val[2], val[3], val[4], val[5], val[6], val[7],
                                  val[8], val[9], val[10], val[11], val[12], val[13], val[14], val[15])
                sqlConnection.add_value(str(query))
            elif val_type == "thermal_camera":
                    print("Saving thermal data")
                    query = """
                        SELECT max(XDKid) FROM tbXDK;
                    """
                    XDKid, = sqlConnection.select_from(str(query)) or ['NULL', ]
                    XDKid = XDKid if XDKid[0] is not None else 'NULL'
                    query = """
                        SELECT max(machinekitid) FROM tbmachinekit;
                    """
                    machinekitid, = sqlConnection.select_from(str(query))
                    machinekitid = machinekitid if machinekitid[0] is not None else ['NULL', ]
                    # print(query, XDKid[0])
                    query = """
                       INSERT INTO tbtest (strtempsnap, machinekitid, XDKid, dtDate)
                       VALUES ("{}", {}, {}, '{}');
                       """.format(self.compressData(self.convFile(self.file)), machinekitid[0], XDKid[0], str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[:-2]))
                    #print(query)
                    sqlConnection.add_value(str(query))
                    # print(query)
                    # convFile(file)
                    # f.write(sarr + '\n')
                    # f.write(sarr)
            elif val_type == "machinekit":
                try:
                    print("Saving machinekit data")
                    #print(val)
                    val[2] = val[2].replace('(', '')
                    val[2] = val[2].replace(')', '')
                    positions = val[2].split(',')
                    query = """
                   INSERT INTO tbmachinekit (intMotion_line,strGcode_command, ftPosition_x, ftPosition_y, ftPosition_z, ftPosition_a, ftCurrent_vel, strFile_name, dtDate)
                   VALUES ({}, "{}", {}, {}, {}, {}, {}, "{}", '{}');
                   """.format(val[0], val[1], positions[0], positions[1], positions[2], positions[3], val[3], val[4],
                              str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[
                                  :-2]))
                    print(query)
                    sqlConnection.add_value(str(query))
                except Exception as e:
                    print(f"Error saving machinekit data. The error '{e}' occurred")
        if storage_stype == "googleDrive":
            if val_type == "XDK":
                pass
            elif val_type == "thermal_camera":
                pass

    def save_txtFile(self, data, fname, data2 = None):
        fname = fname + str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")) + '.txt'
        datas = ('@'.join([str(item) for item in data])) + '@'
        data2 = [item.decode("ISO-8859-1") for item in data2] if data2 else None
        data2s = ('@'.join([item + '@' for item in data2 ])) if data2 else None
        datas2s = data2s + '@'
        with open(fname, 'a') as f:
            f.write(datas + data2s + self.convFile(self.file) + '@' + str(datetime.datetime.now()) + '\n')

    def process_server(self, data, fname):
        fname = fname + str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")) + '.txt'
        conv = self.convFile(self.file)
        r_img = self.reshape_image(conv)
        t_img = tf.convert_to_tensor(r_img)
        c_img = self.crop_image(t_img)
        max = 223.6 #np.max(c_img)
        min = 29 #np.min(c_img)
        norm_img = (c_img - min) / (max - min)
        return norm_img

    def convFile(self, file):
        t.sleep(0.2)
        #print(file)
        with open(file) as file_name:
            array = np.genfromtxt(file_name, delimiter=',')[:, :-1]
            sarr = ' '.join(str(c) for r in array for c in r)
            return sarr

    def compressData(self, data):
        #print(len(data))
        data = base64.b64encode(zlib.compress(bytes(data, "ISO-8859-1")))
        #data = base64.b64encode(data)
        #data = data.decode("ISO-8859-1")
        #print(len(data))
        return data

    def reshape_image(self, img):
        image = np.array(img.split(' '), dtype=np.float64)
        image_r = image.reshape((288, 382))
        return image_r

    def crop_image( self, tensor_image, a1 = 0, a2 = 25, a3 = 25, a4 = 25 ):
        a1 = 0
        a2 = 25
        a3 = 25
        a4 = 25
        filter = tf.where(tensor_image >= 195)
        if filter.shape == (0,2):
            filter = tf.where(tensor_image >= 25)
        indeces = list(np.array(tf.where(filter[:,0] == tf.reduce_max(filter[:,0]))).flatten())
        maxs =  tf.gather(filter, indeces)
        y = int( tf.reduce_mean(maxs[:,0]) )
        x = int( tf.round( tf.reduce_mean(maxs[:,1]) ) )
        #print( f"a1 = {a1}, a2 = {a2}, a3 = {a3}, a4 = {a4}")
        #print( f"Coordenas Hot End (x,y): ( {x}, {y} ) "  )
        #print( f"Coordenadas crop: ( {x - a3}, {x + a4}, {y - a1}, {y + a2} )")
        if x - a3 < 0:
          if x - a3 < 0 and y + a2 > 288:
            #print( f"Error en la coordenada x1 = { x - a3 }, x2 = {x + a4}\nCorregido: x1 = 0, x2 = {( abs(x - a3) + x + a4 )}" )
            #print( f"Error en la coordenada y2 = {y + a2}, y1 = {y - a1 }\nCorregido: y2 = 288, y1 = { ( ( y - a1 ) - ( (y + a2) - 288  ) ) }" )
            return np.array( tensor_image ).reshape( ( 288, 382 ) )[ ( ( y - a1 ) - ( (y + a2) - 288  ) ) : 288, 0 : ( abs(x - a3) + x + a4 ) ]
          else:
            #print( f"Error en la coordenada x1 = { x - a3 }, x2 = {x + a4}\nCorregido: x1 = {0}, x2 = {( abs(x - a3) + x + a4 )}" )
            return np.array( tensor_image ).reshape( ( 288, 382 ) )[ ( y - a1 ) : ( y + a2 ), 0 : ( abs(x - a3) + x + a4 ) ]
        elif x + a4 > 382:
          if x + a4 > 382 and y + a2 > 288:
            #print( f"Error en la coordenada x2 = {x + a4}, x1 = {x-a3}\nCorregido: x1 = {( x - a3) -  ( x + a4 - 382 )}" )
            #print( f"Error en la coordenada y2 = {y + a2}, y1 = {y - a1 }\nCorregido: y2 = 288, y1 = { ( ( y - a1 ) - ( (y + a2) - 288  ) ) }" )
            return np.array( tensor_image ).reshape( ( 288, 382 ) )[ ( ( y - a1 ) - ( (y + a2) - 288  ) ) : 288, ( x - a3) -  ( x + a4 - 382 ) : 382 ]
          else:
            #print( f"Error en la coordenada x2 = {x + 4}, x1 = {x-a3}\nCorregido: x1 = {( x - a3) -  ( x + a4 - 382 )}" )
            return np.array( tensor_image ).reshape( ( 288, 382 ) )[ ( y - a1 ) : ( y + a2 ), ( x - a3) -  ( x + a4 - 382 ) : 382 ]
        elif y + a2 > 288:
          #print( f"Error en la coordenada y2 = {y + a2}, y1 = {y - a1 }\nCorregido: y2 = 288, y1 = { ( ( y - a1 ) - ( (y + a2) - 288  ) ) }" )
          return np.array( tensor_image ).reshape( ( 288, 382 ) )[ ( ( y - a1 ) - ( (y + a2) - 288  ) ) : 288, x - a3 : x + a4  ]
        else:
          return np.array( tensor_image ).reshape( ( 288, 382 ) )[ y - a1 : y + a2, x - a3 : x + a4 ]

    def discriminator_model(self):
        input_layer = layers.Input(shape = ( 25, 50, 1 ) )

        cnn1_1 = layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same')(input_layer)
        relu_1 = layers.LeakyReLU()(cnn1_1)
        drop_1 = layers.Dropout(0.3)(relu_1)

        cnn1_2 = layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same')(drop_1)
        relu_2 = layers.LeakyReLU()(cnn1_2)
        drop_2 = layers.Dropout(0.3)(relu_2)

        cnn1_3 = layers.Conv2D(256, (5, 5), strides=(2, 2), padding='same')(drop_2)
        relu_3 = layers.LeakyReLU()(cnn1_3)
        drop_3 = layers.Dropout(0.3)(relu_3)

        flat = layers.Flatten()(drop_3)
        dense_2 = layers.Dense(1, activation='sigmoid')(flat)

        model = tf.keras.Model(inputs=[input_layer], outputs=[dense_2])

        loss = tf.keras.losses.BinaryCrossentropy(from_logits=True)
        optimizer = tf.keras.optimizers.Adam(1e-3)

        model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

        return model

    def run_model(self, image):
        image = image.reshape( ( -1, 25, 50, 1 ) )
        result = self.classifier.predict(image)

        if result > 0.99:
            sresult = "La boquilla no está calibrada, " + str(result)
        else:
            sresult = "La boquilla está calibrada, " + str(result)
        return sresult