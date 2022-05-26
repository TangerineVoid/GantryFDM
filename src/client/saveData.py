import datetime
import time as t
import numpy as np

class SaveData:
    # instance attributes
    def __init__(self):
        self.file = None

    def save_sql(self, val_type, storage_stype ,sqlConnection, val=None):
        if storage_stype == "sql":
            if val_type == "XDK":
                    # fname = 'D:/Users/sergio.salinas/Documents/Imager Data/data/' + 'data_' + '.txt'

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
                   """.format(self.convFile(self.file), machinekitid[0], XDKid[0], str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[:-2]))
                #print(query)
                sqlConnection.add_value(str(query))
                # print(query)
                # convFile(file)
                # f.write(sarr + '\n')
                # f.write(sarr)
            elif val_type == "machinekit":
                try:
                    query = """
                   INSERT INTO tbmachinekit (motion_line,gcode_command, position_x, position_y, position_z, position_a, current_vel, dtDate)
                   VALUES ({}, "{}", {}, {}, {}, {}, {}, '{}');
                   """.format(val[0], val[1], val[2], val[3], val[4], val[5], val[6],
                              str(datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S.%f")[
                                  :-2]))
                    sqlConnection.add_value(str(query))
                except Exception as e:
                    print(f"Error saving machinekit data. The error '{e}' occurred")
        if storage_stype == "googleDrive":
            if val_type == "XDK":
                pass
            elif val_type == "thermal_camera":
                pass

    def convFile(self, file):
        t.sleep(0.2)
        print(file)
        with open(file) as file_name:
            array = np.genfromtxt(file_name, delimiter=',')[:, :-1]
            sarr = ' '.join(str(c) for r in array for c in r)
            return sarr