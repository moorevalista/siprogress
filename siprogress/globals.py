from urllib import request
from django.db import connection, connections, ProgrammingError, DatabaseError
from .settings import DATABASES
from pyreportjasper import JasperPy
from .environment import env
import datetime
import json
import os
import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from pprint import pprint
import requests
from datetime import datetime as DTime

# bpjs
import requests
import hashlib
import base64
import urllib
import hmac

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import lzstring


class Globals:
    kd_kamar_vk = '015'
    kd_kamar_ok = '010'

    def generateReport(self, request):
        ts = datetime.datetime.now()
        date = ts.strftime("%d_%m_%Y_%I_%M_%S_%f")
        user = "_" + request.GET['user'] + "_"

        jsonNameFile = str(datetime.datetime.now().timestamp()) + ".json"
        jrxmlNameFile = request.GET['jrxmlNameFile']
        reportNameFile = request.GET['reportNameFile'] + user + date
        json_query = request.GET['json_query']
        json_string = request.GET['json_string']
        arrKey = json.loads(input(request.GET, 'arrKey'))
        arrValue = json.loads(input(request.GET, 'arrValue'))
        dictionary = dict(zip(arrKey, arrValue)) if (input(
            request.GET, 'arrKey') is not None and input(request.GET, 'arrValue') is not None) else {}

        f = open(os.path.abspath(os.path.dirname(__name__)) +
                 "/jrxml/json/" + jsonNameFile, "w")
        f.write(json_string)
        f.close()

        input_file = os.path.abspath(os.path.dirname(
            __name__)) + '/jrxml/' + jrxmlNameFile
        output = os.path.abspath(os.path.dirname(
            __name__)) + '/static/report/' + reportNameFile
        data_file = os.path.abspath(os.path.dirname(
            __name__)) + '/jrxml/json/' + jsonNameFile

        jasper = JasperPy()
        jasper.process(
            input_file,
            output_file=output,
            format_list=["pdf"],
            parameters=dictionary,
            # parameters={
            # 	# parameter
            # 	# "gambar":url_img,
            # 	"gambar":"C:/Users/Administrator/Pictures/walls/TC_Build (4).jpg",
            # 	"tulisan":"ini tulisan dari parameter"
            # },
            db_connection={
                'data_file': data_file,
                'driver': 'json',
                'json_query': json_query,
            },
            locale='id_ID'
        )

        os.remove(os.path.abspath(os.path.dirname(__name__)) +
                  "/jrxml/json/" + jsonNameFile)

        url_file = '/static/report/' + reportNameFile + ".pdf"
        result = {"file": url_file}
        json_data = json.dumps(result, cls=DjangoJSONEncoder)
        return HttpResponse(json_data, content_type="application/json")

    # def generateReportDB(self,input_filename,output_filename,user,param={},db='',list_format=["pdf","html"] ):

    def generateReportDB(self, input_filename, output_filename, user, param={}, db='', list_format=["pdf"]):
        ts = datetime.datetime.now()
        date = ts.strftime("%d_%m_%Y_%I_%M_%S_%f")
        user = "_" + user + "_"

        reportNameFile = output_filename + user + date
        in_file = os.path.abspath(os.path.dirname(
            __name__)) + '/jrxml/'+input_filename
        out_file = os.path.abspath(os.path.dirname(
            __name__)) + '/static/report/'+reportNameFile

        if db == '':
            db_profile = 'default'
        else:
            db_profile = db

        username = DATABASES[db_profile]['USER']
        password = DATABASES[db_profile]['PASSWORD']
        host = DATABASES[db_profile]['HOST']
        database = DATABASES[db_profile]['NAME']
        port = DATABASES[db_profile]['PORT']

        if getattr(env, 'JDBC_MODE', 'WINDOWS') == 'WINDOWS':
            jdbc_driver = getattr(
                env, 'JDBC_DRIVER', 'com.microsoft.sqlserver.jdbc.SQLServerDriver')
            jdbc_url = getattr(
                env, 'JDBC_URL', 'jdbc:sqlserver://'+host+':'+port+';databaseName='+database)
            # jdbc_dir = getattr(env, 'JDBC_DIR', "\"C:/Program Files/Microsoft JDBC Driver 6.0 for SQL Server/sqljdbc_6.0/enu/jre8\"")
            jdbc_dir = getattr(env, 'JDBC_DIR', os.path.abspath(
                os.path.dirname(__name__)) + '/jdbc')

            con = {
                'driver': 'generic',
                'jdbc_driver': jdbc_driver,
                'jdbc_url': jdbc_url,
                'jdbc_dir': jdbc_dir,
                'username': username,
                'password': password,
                'host': host,
                'database': database,
                'port': port
            }
        else:
            jdbc_driver = getattr(env, 'JDBC_DRIVER',
                                  'net.sourceforge.jtds.jdbc.Driver')
            jdbc_url = getattr(env, 'JDBC_URL', 'jdbc:jtds:sqlserver://'+host +
                               ':'+port+'/'+database+';user='+username+';password='+password)
            jdbc_dir = getattr(env, 'JDBC_DIR', os.path.abspath(
                os.path.dirname(__name__)) + '/jdbc')

            con = {
                'driver': 'generic',
                'jdbc_driver': jdbc_driver,
                'jdbc_url': jdbc_url,
                # 'jdbc_dir': jdbc_dir,
                'username': username,
                'password': password,
                'host': host,
                'database': database,
                'port': port
            }

        jasper = JasperPy()
        if (not os.path.exists(in_file[0:-5]+'jasper')):
            jasper.compile(in_file)

        jasper.process(
            in_file[0:-5]+'jasper',
            output_file=out_file,
            format_list=list_format,
            parameters=param,
            db_connection=con,
            locale='en_US'
        )

        response = {}
        for file_format in list_format:
            response[file_format] = '/static/report/' + \
                reportNameFile + "." + file_format

        return response

    def generateReportJSON(self, input_filename, output_filename, user, param={}, db='', list_format=["pdf"]):
        ts = datetime.datetime.now()
        date = ts.strftime("%d_%m_%Y_%I_%M_%S_%f")
        user = "_" + user + "_"

        data_file = os.path.abspath(os.path.dirname(
            __name__)) + '/LOG/HISTORYDELETE/HistoryDelete.json'

        reportNameFile = output_filename + user + date
        in_file = os.path.abspath(os.path.dirname(
            __name__)) + '/jrxml/'+input_filename
        out_file = os.path.abspath(os.path.dirname(
            __name__)) + '/static/report/'+reportNameFile

        con = {
            'data_file': data_file,
            'driver': 'json',
            'json_query': "data",
        }

        jasper = JasperPy()
        if (not os.path.exists(in_file[0:-5]+'jasper')):
            jasper.compile(in_file)

        jasper.process(
            in_file[0:-5]+'jasper',
            output_file=out_file,
            format_list=list_format,
            parameters=param,
            db_connection=con,
            locale='en_US'
        )

        response = {}
        for file_format in list_format:
            response[file_format] = '/static/report/' + \
                reportNameFile + "." + file_format

        return response

    def dictfetchall(self, cursor):
        # "Return all rows from a cursor as a dict"
        fetchdata = cursor.fetchall()
        if (cursor.description):
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in fetchdata
            ]
        else:
            return fetchdata

    def printService(self, pdf, ip_client, nama_printer, paper_config={}):
        print(os.path.abspath(pdf['pdf'][1:]))
        files = {'file': open(pdf['pdf'][1:], 'rb')}
        values = {"ID": nama_printer,
                  "printer_config": json.dumps(paper_config)}

        r = requests.post(ip_client, files=files, data=values)

    def getData(self, query, param=None, setIndex=1):
        cursor = connection.cursor()
        if (param is not None):
            cursor.execute(query, param)
        else:
            cursor.execute(query)
        results = None
        i = 0
        while results is None:
            try:
                results = self.dictfetchall(cursor)

                i += 1
                if (i == setIndex):
                    break
                else:
                    results = None
                    cursor.nextset()

            except ProgrammingError as e:
                cursor.nextset()
        # pprint(results)
        cursor.close()
        return results

    def getDataQuery(self, query, params=[], db='main'):
        if db == 'main':
            cursor = connection.cursor()
        elif db == 'antrian':
            cursor = connections['antrian'].cursor()
        else:
            cursor = connections['epublic'].cursor()

        cursor.execute(query, params)
        result = self.dictfetchall(cursor)
        cursor.close()

        return result

    def executeQuery(self, query, params=[], db='main'):
        if db == 'main':
            cursor = connection.cursor()
        elif db == 'antrian':
            cursor = connections['antrian'].cursor()
        else:
            cursor = connections['epublic'].cursor()

        cursor.execute(query, params)
        cursor.close()

    def isLogin(self, request):
        # Privilege = getData("select distinct USER_PRIV from USERSPRIV;")
        Privilege = self.getData("select distinct USER_PRIV from USERSPRIV;")

        if 'userauth' in request.session:
            is_login = request.session['userauth']
            # if(request.session['user_priv'] not in PRIV['USER_PRIV']):
            if (not any(user['USER_PRIV'] == request.session['user_priv'] for user in Privilege)):
                is_login = False
        else:
            is_login = False
        return is_login

    def input(self, method, key, default=None):
        if key not in method:
            return default
        else:
            return method[key]

    def fetchResult(self, cursor, setIndex=1):
        i = 0
        results = self.dictfetchall(cursor)
        # pprint(results)
        if results is None:
            return None
        else:
            i += 1
            # print(i)
            # print(setIndex)
            if (i >= setIndex):
                return results
            else:

                while i < setIndex:
                    try:
                        cursor.nextset()
                        results = self.dictfetchall(cursor)
                        i += 1
                    except ProgrammingError as e:
                        i += 1
                    except DatabaseError as e:
                        i += 1

                return results

    def getDataCabang(self, column):
        cursor = connection.cursor()
        q = "SELECT * FROM CABANG"
        cursor.execute(q)
        cabang = self.dictfetchall(cursor)
        return cabang[0][column]

    def getNavbars(self, user_priv, modul, submodul=None):
        cursor = connection.cursor()

        if submodul == None:
            qnavbar = "SELECT * FROM PROPERTIES_NAVBAR WHERE modul = '" + \
                modul+"' AND submodul IS NULL AND id IN "
            qnavbar += "(SELECT NAVBAR_PRIV FROM PRIVILEGE_NAVBAR WHERE USER_PRIV = '" + \
                user_priv+"' AND modul = '"+modul+"' AND submodul IS NULL) "
        else:
            qnavbar = "SELECT * FROM PROPERTIES_NAVBAR WHERE modul = '" + \
                modul+"' AND submodul = '"+submodul+"' AND id IN "
            qnavbar += "(SELECT NAVBAR_PRIV FROM PRIVILEGE_NAVBAR WHERE USER_PRIV = '" + \
                user_priv+"' AND modul = '"+modul+"' AND submodul = '"+submodul+"') "

        qnavbar += "ORDER BY nav_order"
        cursor.execute(qnavbar)
        return self.dictfetchall(cursor)

    def getMenubars(self, user_priv, modul, submodul=None, level='default'):
        cursor = connection.cursor()

        if submodul == None:
            qmenubar = "SELECT * FROM PROPERTIES_MENUBAR WHERE modul = '" + \
                modul+"' AND submodul IS NULL "

            if level != 'default':
                qmenubar += "AND level = " + level

            qmenubar += "AND id IN (SELECT MENUBAR_PRIV FROM PRIVILEGE_MENUBAR WHERE USER_PRIV = '" + \
                user_priv+"' AND modul = '"+modul+"' AND submodul IS NULL) "
        else:
            qmenubar = "SELECT * FROM PROPERTIES_MENUBAR WHERE modul = '" + \
                modul+"' AND submodul = '"+submodul+"' "

            if level != 'default':
                qmenubar += "AND level = " + level

            qmenubar += "AND id IN (SELECT MENUBAR_PRIV FROM PRIVILEGE_MENUBAR WHERE USER_PRIV = '" + \
                user_priv+"' AND modul = '"+modul+"' AND submodul = '"+submodul+"') "

        qmenubar += "ORDER BY B.MENU_ORDER"
        cursor.execute(qmenubar)
        return self.dictfetchall(cursor)

    def getSeparator(self, n):
        separator = []
        n += 1
        counter = 7

        for x in range(n):
            if x+1 == counter:
                separator.append(counter)
                counter += 6

        return separator

    def dateIndo(self, date):
        tgl = date.split("-")

        tanggal = tgl[2]
        bulan = tgl[1]
        tahun = tgl[0]

        if (bulan == '01'):
            bulan = ' Januari '
        elif (bulan == '02'):
            bulan = ' Februari '
        elif (bulan == '03'):
            bulan = ' Maret '
        elif (bulan == '04'):
            bulan = ' April '
        elif (bulan == '05'):
            bulan = ' Mei '
        elif (bulan == '06'):
            bulan = ' Juni '
        elif (bulan == '07'):
            bulan = ' Juli '
        elif (bulan == '08'):
            bulan = ' Agustus '
        elif (bulan == '09'):
            bulan = ' September '
        elif (bulan == '10'):
            bulan = ' Oktober '
        elif (bulan == '11'):
            bulan = ' November '
        else:
            bulan = ' Desember '

        return tanggal + bulan + tahun

    def create_log(self, file_name, folder, data, user):
        if not os.path.exists(os.path.abspath(os.path.dirname(__name__)) + '/LOG/'+folder):
            os.makedirs(os.path.abspath(
                os.path.dirname(__name__)) + '/LOG/'+folder)

        files = os.path.abspath(os.path.dirname(
            __name__)) + '/LOG/'+folder+'/'+file_name

        if os.path.exists(files) == False:
            f = open(files, "w+")
        else:
            f = open(files, "a+")

        tanggal = self.tanggalIndo(
            datetime.datetime.now().strftime('%Y-%m-%d'))
        jam = str(datetime.datetime.now().strftime('%H:%M:%S'))

        jsonData = json.dumps(self.generateData(data), cls=DjangoJSONEncoder)

        f.write('==============================================' + "\n")
        f.write("USER ID : " + user['user_id'] + ", NAMA : " +
                user['user_name'] + ", USER PRIV : " + user['user_priv'] + "\n")
        f.write("TANGGAL : " + tanggal + ", JAM : " + jam + "\n")
        f.write('==============================================' + "\n")
        f.write(simplejson.dumps(simplejson.loads(jsonData), indent=2))
        f.write('\n==============================================' + "\r")
        f.write('==============================================' + "\r\n")

        f.close()

    def create_log_json(self, file_name, folder, data, user):
        if not os.path.exists(os.path.abspath(os.path.dirname(__name__)) + '/LOG/'+folder):
            os.makedirs(os.path.abspath(
                os.path.dirname(__name__)) + '/LOG/'+folder)

        files = os.path.abspath(os.path.dirname(
            __name__)) + '/LOG/'+folder+'/'+file_name

        if os.path.exists(files) == False:
            f = open(files, "w+")
        else:
            f = open(files, "a+")

        tanggal = self.tanggalIndo(
            datetime.datetime.now().strftime('%Y-%m-%d'))
        jam = str(datetime.datetime.now().strftime('%H:%M:%S'))
        jsonData = json.dumps(self.generateDataJson(
            data), cls=DjangoJSONEncoder, indent=4)
        jsonDumps = simplejson.loads(jsonData)
        dataDump = {
            'delete_info': {
                'user': user,
                'jam': jam,
                'tanggal': tanggal
            },
            'data_info': jsonDumps
        }

        if os.stat(files).st_size == 0:
            f.write('[')
            json.dump(dataDump, f)
            f.write('\n,')
        else:
            json.dump(dataDump, f)
            f.write('\n,')
        f.close()

    def read_log_json(self):

        lines = []
        output_data = []
        files = os.path.abspath(os.path.dirname(
            __name__)) + '/LOG/HISTORYDELETE/HistoryDelete.txt'
        read_files = open(files, "r")

        if os.stat(files).st_size > 0:
            lines = read_files.readlines()
            for number, line in enumerate(lines):
                if number not in [(len(lines)-1)]:
                    output_data.append(line)
            output_data.append("]")
        else:
            output_data.append({
                "delete_info": "No data."
            })

        read_files.close()

        return output_data

    def generateData(self, data):
        result = []
        jsonData = []

        for x in data:
            cursor = connection.cursor()
            cursor.execute(x['query'])
            result.append(self.dictfetchall(cursor))

        i = 0
        for y in data:
            jsonData.append({
                "query": y['query'],
                "data": result[i]
            })

            i += 1

        return jsonData

    def generateDataJson(self, data):
        result = []
        for x in data:
            cursor = connection.cursor()
            cursor.execute(x['query'])
            result.append(self.dictfetchall(cursor))

        if (len(result) > 1):
            jsonData = {
                "HEADER": result[0][0],
                "DETAIL": result[1]
            }
        else:
            jsonData = {
                "HEADER": result[0][0]
            }

        return jsonData

    def create_json_file(self, file_name, folder, data):
        files = os.path.abspath(os.path.dirname(
            __name__)) + '/LOG/'+folder+'/'+file_name

        if os.path.exists(files) == True:
            if os.stat(files).st_size > 0:
                os.unlink(files)

        f = open(files, "w+")
        for line in data:
            f.write(line)
        f.close()

    def update_json_file(self, tanggal):
        file = os.path.abspath(os.path.dirname(
            __name__)) + '/LOG/HISTORYDELETE/HistoryDelete.json'

        result = []
        result_detail = []
        filter_data = []
        nomor_bukti = []
        with open(file, "r") as json_file:
            data = json.load(json_file)

        print(tanggal)
        for item_data in data:
            if item_data["delete_info"]["tanggal"] == tanggal:
                filter_data.append(item_data)

        for item in filter_data:

            # HEADER
            for header_key in item['data_info']['HEADER']:
                if header_key.find("BUKTI_ID") != -1 and header_key != 'FHPCLMBUKTI_IDRI' or header_key.find("FHMTS_ID") != -1:
                    nomor_bukti.append(item['data_info']['HEADER'][header_key])
                elif header_key.find("DATE") != -1:
                    tanggal_header = item['data_info']['HEADER'][header_key]
                elif header_key.find("BARANGC") != -1:
                    nomor_bukti.append(item['data_info']['HEADER'][header_key])

            for item_info in item['data_info']:
                if item_info.find('DETAIL') != -1:

                    for number_detail, item_detail in enumerate(item['data_info'][item_info]):
                        for item_detail_key in item_detail:

                            if item_detail_key.find("BRG_ID") != -1:
                                kode_obat = item['data_info']['DETAIL'][number_detail][item_detail_key]
                            elif item_detail_key.find("BRGN") != -1 or header_key.find("FDMTSBRGN") != -1:
                                nama_obat = item['data_info']['DETAIL'][number_detail][item_detail_key]
                            elif item_detail_key.find("BUKTI_ID") != -1 or item_detail_key.find("FDMTS_ID") != -1:
                                nomor_bukti_detail = item['data_info']['DETAIL'][number_detail][item_detail_key]
                            elif item_detail_key.find("QTY") != -1:
                                qty = item['data_info']['DETAIL'][number_detail][item_detail_key]
                            elif item_detail_key.find("JUAL") != -1 or item_detail_key.find("POKOK") != -1:
                                hpp = item['data_info']['DETAIL'][number_detail][item_detail_key]

                        result_detail.append({
                            "nomor_bukti": str(nomor_bukti_detail),
                            "kode_obat": kode_obat,
                            "nama_obat": nama_obat,
                            "qty": qty,
                            "hpp": hpp
                        })
                else:
                    for header_key in item['data_info']['HEADER']:
                        if header_key.find("BARANGC") != -1:
                            kode_obat = item['data_info']['HEADER'][header_key]
                        elif header_key.find("NAME_BRG") != -1:
                            nama_obat = item['data_info']['HEADER'][header_key]
                        elif header_key.find("SATKECIL") != -1:
                            qty = item['data_info']['HEADER'][header_key]
                        elif header_key.find("HPOKOK") != -1:
                            hpp = item['data_info']['HEADER'][header_key]

                            result_detail.append({
                                "nomor_bukti": kode_obat,
                                "kode_obat": kode_obat,
                                "nama_obat": nama_obat,
                                "qty": qty,
                                "hpp": hpp
                            })

        for item_nomor_bukti in nomor_bukti:
            if item_nomor_bukti != None:
                result.append({
                    "data": {
                        "delete_info": item["delete_info"],
                        "data_info": {
                            "HEADER": {
                                "nomor_bukti": item_nomor_bukti,
                                "tanggal": str(tanggal_header)
                            },
                            "DETAIL": [i for i in result_detail if i["nomor_bukti"] == item_nomor_bukti]
                        }
                    }
                })

        os.unlink(file)
        with open(file, 'w', encoding='utf-8') as json_file:
            json.dump(result, json_file)
        return result

    def tanggalIndo(self, date):
        tgl = date.split("-")
        tanggal = tgl[2]
        bulan = tgl[1]
        tahun = tgl[0]

        if (bulan == '01'):
            bulan = ' Januari '
        elif (bulan == '02'):
            bulan = ' Februari '
        elif (bulan == '03'):
            bulan = ' Maret '
        elif (bulan == '04'):
            bulan = ' April '
        elif (bulan == '05'):
            bulan = ' Mei '
        elif (bulan == '06'):
            bulan = ' Juni '
        elif (bulan == '07'):
            bulan = ' Juli '
        elif (bulan == '08'):
            bulan = ' Agustus '
        elif (bulan == '09'):
            bulan = ' September '
        elif (bulan == '10'):
            bulan = ' Oktober '
        elif (bulan == '11'):
            bulan = ' November '
        else:
            bulan = ' Desember '

        return tanggal + bulan + tahun

    def RekamKegiatan(self, Kegiatan, user):

        ts = datetime.datetime.now()
        date = ts.strftime("%d_%m_%Y_%I_%M_%S")
        user = "," + user + ","
        input_filename = "LogDelete.txt"
        Aktivitas = Kegiatan + user + date
        in_file = os.path.abspath(os.path.dirname(
            __name__)) + '/log/'+input_filename
        # pprint (in_file)
        # pprint (input_filename)
        # Open the file in append & read mode ('a+')
        with open(in_file, "a+") as file_object:
            # Move read cursor to the start of file.
            file_object.seek(0)
            # If file is not empty then append '\n'
            data = file_object.read(100)
            if len(data) > 0:
                file_object.write("\n")
            # Append text at the end of file
            file_object.write(Aktivitas)
            # Close the file
            file_object.close()
        return

    def deleteFiles(self, folder="/static/report/"):
        root_path = os.path.abspath(os.path.dirname(__name__))
        path = root_path + folder
        today = datetime.datetime.today()

        hari = (int(getattr(env, 'HAPUS_FILE_HARI', 30)) + 1)

        if (hari == 0):
            hari = -1

        elif (hari > 0):
            hari = hari * -1

        os.chdir(path)

        for root, directories, files in os.walk(path, topdown=False):
            for directory in directories:
                t = os.stat(os.path.join(root, directory))[8]
                foldertime = datetime.datetime.fromtimestamp(t) - today

                if foldertime.days <= hari:
                    os.rmdir(os.path.join(root, directory))

            for name in files:
                t = os.stat(os.path.join(root, name))[8]
                filetime = datetime.datetime.fromtimestamp(t) - today

                if filetime.days <= hari:
                    split_tup = os.path.splitext(os.path.join(root, name))

                    data_extension = ['.pdf', '.xls',
                                      '.xlsx', '.html', '.txt', '.log']
                    if split_tup[1] in data_extension:
                        os.remove(os.path.join(root, name))

        os.chdir(root_path)

    def decrypt(self, key, txt_enc):
        decompress = None
        x = lzstring.LZString()
        # print(key)
        # print(txt_enc)
        key_hash = hashlib.sha256(key.encode("utf-8")).digest()

        mode = AES.MODE_CBC

        # decrypt
        decryptor = AES.new(key_hash[0:32], mode, IV=key_hash[0:16])
        plain = decryptor.decrypt(base64.b64decode(txt_enc))
        decompress = x.decompressFromEncodedURIComponent(plain.decode("utf-8"))

        return decompress

    def bridgeBPJS(self, url, method,  payload={}):

        # q = "select * from CABANG  WHERE CABANG_ID=%s "
        # cabang = Globals().getDataQuery(q, [kdCabang])
        # consid = cabang[0]["consid"]
        # secret = cabang[0]["secret"]

        # BPJS_USERKEY = cabang[0]["bpjs_userkey_apotek"]

        consid = getattr(env, 'consid_apotek', '')
        secret = getattr(env, 'secret_apotek', '')
        BPJS_URL = getattr(env, 'BPJS_URL_apotek', '')
        BPJS_USERKEY = getattr(env, 'BPJS_USERKEY_apotek', '')
        # vCLAIm
        # consid = "9374"
        # secret = "8kAE28A7DE"
        # BPJS_URL = "https://apijkn-dev.bpjs-kesehatan.go.id/apotek-rest-dev"
        # BPJS_USERKEY = "0571b6e9fd2e4d7bdb153bd62a09dc02"

        # consid = "9374"
        # secret = "8kAE28A7DE"
        # BPJS_URL = "https://apijkn-dev.bpjs-kesehatan.go.id/apotek-rest-dev"
        # BPJS_USERKEY = "0571b6e9fd2e4d7bdb153bd62a09dc02"

        # rsi kudus
        # consid = "32485"
        # secret = "3uABF095E7"
        # BPJS_USERKEY = "4beb8330a9590a0ee18f3a12c088fb8c"
        # BPJS_URL = "https://apijkn-dev.bpjs-kesehatan.go.id/apotek-rest-dev"

        # print(consid)
        tStamp = int(DTime.today().timestamp())
        tStamp = str(tStamp)
        message = consid + "&" + tStamp
        signature = hmac.new(
            bytes(secret, "UTF-8"), bytes(message, "UTF-8"), hashlib.sha256
        ).digest()
        encodeSignature = base64.b64encode(signature)

        headers = {
            "X-cons-id": consid,
            "X-timestamp": tStamp,
            "X-signature": encodeSignature.decode("UTF-8"),
            "Content-Type": "Application/JSON",
            "Accept": "*/*",
            "user_key": "" + BPJS_USERKEY,
        }
        # print(headers)
        # print(url)
        if not payload:
            payload = 0
        else:
            payload = json.dumps(payload, cls=DjangoJSONEncoder)

        if method == "post":
            if payload == 0:
                res = requests.post(url, headers=headers).json()
            else:
                headers = {
                    "X-cons-id": consid,
                    "X-timestamp": tStamp,
                    "X-signature": encodeSignature.decode("UTF-8"),
                    "Accept": "*/*",
                    "user_key": "" + BPJS_USERKEY,
                }
                # headers = {'X-cons-id': consid, 'X-timestamp': tStamp, 'X-signature': encodeSignature.decode('UTF-8'),'X-authorization': 'Basic '+authorization.decode('UTF-8'),'Accept': '*/*','user_key':''+BPJS_USERKEY,'Format' : 'Json','Content-Type':'text/plain'}
                # print(url)
                # print(headers)
                # print(payload)
                # print(requests.post(url   , data=payload, headers=headers).text)
                res = requests.post(url, data=payload, headers=headers).json()
                # print(res)
        elif method == "DELETE":
            headers = {
                "X-cons-id": consid,
                "X-timestamp": tStamp,
                "X-signature": encodeSignature.decode("UTF-8"),
                "user_key": "" + BPJS_USERKEY,
            }
            res = requests.delete(url, data=payload, headers=headers).json()
            # if requests.delete(url, headers=headers).status_code == 400:
            #     # res = {
            #     #     "response": {},
            #     #     "metaData": {"message": "URL SALAH", "code": 400},
            #     # }
            #     res = requests.delete(url, headers=headers).json()
            # else:
            #     res = requests.delete(url, headers=headers).json()
        elif method == "put":
            if payload == 0:
                res = requests.put(url, headers=headers).json()
            else:
                headers = {
                    "X-cons-id": consid,
                    "X-timestamp": tStamp,
                    "X-signature": encodeSignature.decode("UTF-8"),
                    "Accept": "*/*",
                    "user_key": "" + BPJS_USERKEY,
                }
                res = requests.put(url, data=payload, headers=headers).json()
        else:
            if payload == 0:
                res = requests.get(url, headers=headers).json()
            else:
                res = requests.get(url, data=payload, headers=headers).json()

        # print(url)
        # print(payload)
        # print(headers)
        # print(res)
        # print(json.loads(decrypt('{}{}{}'.format(consid,secret,"1660633017"),"fRTnNFDHL6h4Vs3knegkFByc6BoS+WRTcMtuaZRG73xMbAbFQQ6042\/pmLfHqe9LYyq8R46AYLrtvUt5eS\/0knnHnmjslJ\/UMevi6jXycRMROUtLpF7KcKyqq82q5r7i0NlTa7reKV2SqOEskoMW2PrK4vXZMFFyusbeCX7ILNJl7p7VF4bM6w\/+CH9eqAs1ZxFINbOhctbmVehZgWyxT4yJwlshtVVlc2jED10QSa9ZXcnxtSrphq5tchWPBK88cuCcsOoCmUXaYMufNqGx+7JKNh7Stkz4LakqsQ3nj1UO1edaXV8+bKLBc0XsIlhgiqQk7ONpBbMxBZdGU9ew38RJSjx3gb12jIndK\/+xrwLbNKI3dIUFg0abIofK8xzNCZR7zpAfl4HF4aMPyGuaDs\/c6FyhQjcOg7ptv9aW21Bm0IAUTop5Zk9ti2dAwHbQvIk57IY9sESZJeDrMNxZwGzXxQ82PevnN8aZFYP+MuuLBdzO+gme8nm1gBS1RXPEUcypioMwlO2sb\/1WJ84dN4bAWdTw8AiY01xVchimsNnaBBjQd+5aTk7Q3o6Y8Cx\/F9Ji1gLKkDgiG0IMdlPf\/8\/HdzI+h8uZBjIzxWmQ8ih0XBLQqhPdv7S5mFstfizOAnGd9HePdt4ZHLMx12p7S7vvSAfI8Av4w8gcpWVDJpo2MwS70qed1LiYzMim8kiu6v6Oy5+WDM1Cxf1RR1jVQFyKV7jgoIFLDHkuJwDt6xg=")))
        # print(res["response"]["message"])

        # try:
        keys = consid + secret + tStamp
        # print(self.decrypt(keys, res['response']))
        try:
            # print(res['response'])
            if method == "DELETE":
                resnew = {"response": [], "metaData": res["metaData"]}
            else:
                resnew = {
                    "response": json.loads(self.decrypt(keys, res["response"])),
                    "metaData": res["metaData"],
                }
        except:
            if res["response"] is None:
                resnew = {"response": [], "metaData": res["metaData"]}
            else:
                resnew = {"response": res["response"],
                          "metaData": res["metaData"]}
        return resnew
        # except:
        # print(res)
        # 	return res

    def input(self, method, key, default=None):
        if key not in method:
            return default
        else:
            return method[key]
