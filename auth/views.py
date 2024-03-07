from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import connection
from django.contrib.auth import authenticate
from pprint import pprint
from inspect import getmembers
from siprogress.globals import Globals
from siprogress.DictX import DictX

def loggedIn(request):
	if None != request.session and request.session.get('userauth') == True:
		return redirect('/')


def login(request):

	response = render(request, 'login.html', 
                       {'invalid': False })
	
	# Check Session
	if loggedIn(request) != None:
		return loggedIn(request)
	if request.POST:
		# print('coba')
		if "DOKTER" in request.POST['username']:
			dataUserDokter=request.POST['username'].split("_")
			userDokter=dataUserDokter[1]
			passDokter=request.POST['password']
			query="select FMDDOKTER_ID,FMDDOKTERN,PW,'USER_PRIV' as USER_PRIV from DOKTER where FMDDOKTER_ID ='{}' AND PW='{}' UNION Select USER_ID as FMDDOKTER_ID,USER_NAME as FMDDOKTERN ,USER_PASSWORD as PW,USER_PRIV from USERSPRIV where USER_ID='{}'".format(userDokter,passDokter,userDokter)			
			# print(query)
			cursor = connection.cursor()
			cursor.execute(query)
			rows = cursor.fetchall()
			# print(rows)
			jum=int(len(rows))
			if jum>0:
				# print("{} - {}".format(rows[0][0],rows[0][1]))
				

				request.session.set_expiry(0)
				request.session['userauth'] = True
				request.session['user_priv'] = "DOKTER"
				request.session['FMDDOKTER_ID'] = rows[0][0]
				request.session['FMDDOKTERN'] = rows[0][1]
				request.session['FMPPERAWAT_ID'] = rows[0][0]
				request.session['FMPPERAWATN'] = rows[0][1]
				request.session.modified = True
				query3="SELECT A.FMPKLINIK_ID,A.FMPKLINIKN,A.KODEASSESMENT FROM POLIKLINIK A,JADWAL_POLI B WHERE  A.FMPKLINIK_ID=B.FMJKD_KLINIK AND B.FMJKD_DOKTER='{}'".format(rows[0][0])			
				cursor3 = connection.cursor()
				cursor3.execute(query3)
				rows3 = cursor3.fetchall()
				jum3=int(len(rows3))
				if jum3>0:
					request.session['FMPKLINIK_ID'] = rows3[0][0]
					request.session['FMPKLINIKN'] = rows3[0][1]
				# print(rows[0][0])
				return redirect('/')				
				# response = render(request, 'emrdokter/home.html')

			else:
				response = render(request, 'login.html', 
                       {'invalid': True })

		else:
			user = checkLogin(str(request.POST['username']), str(
                request.POST['password']))
			# pprint(getmembers(user))
			if user is not None:
				# cek gudang
				q = "select a.USER_ID, a.USER_PRIV, b.GUDANG, c.NAME_WH, c.BRANCH from USERSPRIV as a left join PRIVILEGE as b on a.USER_PRIV = b.USER_PRIV left join WAREHOUSE as c on b.GUDANG = c.WH_ID where a.USER_ID = %s"
				cursor = connection.cursor()
				cursor.execute(q, [user.USER_ID])
				rows = cursor.fetchall()
				request.session.set_expiry(0)
				request.session['userauth'] = True
				request.session['user_priv'] = user.USER_PRIV
				request.session['user_name'] = user.USER_NAME
				request.session['user_id'] = user.USER_ID

				# DELETE STATIC FILES
				Globals().deleteFiles()
				# Globals().deleteFiles("/DEBUG/")

				user_privelege = request.session['user_priv']
				# print ('asss')
				# print (user_privelege)

				if rows[0][2] is None or rows[0][3] is None:
					qgudang = "select top 1 * from WAREHOUSE"
					cursor2 = connection.cursor()
					cursor2.execute(qgudang)
					data = cursor2.fetchall()
					request.session['kode_gudang_asli'] = 0
					request.session['kode_gudang'] = data[0][0].strip()
					request.session['nama_gudang'] = data[0][1].strip()
					request.session['branch'] = data[0][2].strip()
				
				else:
					request.session['kode_gudang_asli'] = rows[0][2].strip()
					request.session['kode_gudang'] = rows[0][2].strip()
					request.session['nama_gudang'] = rows[0][3].strip()
					request.session['branch'] = rows[0][4].strip()

				qprivilege = 'SELECT TOP 1 * FROM PRIVILEGE WHERE USER_PRIV = %s'
				dataprivilege = Globals().getDataQuery(qprivilege, [request.session['user_priv']])
				request.session['shift_cek'] = dataprivilege[0]['AKTIF']
				request.session['shift_isset'] = '0'
				
				if dataprivilege[0]['SHIFT_AKTIF'] == None:
					request.session['shift_aktif'] = '1'
				else:
					request.session['shift_aktif'] = dataprivilege[0]['SHIFT_AKTIF'].strip()

				qshift = 'SELECT * FROM SHIFT WHERE SHFUSER_PRIV = %s'
				datashift = Globals().getDataQuery(qshift, [request.session['user_priv']])
				request.session['shift_jumlah'] = len(datashift)

				for x in datashift:
					if x['KD_SHIFT'].strip() == dataprivilege[0]['SHIFT_AKTIF'].strip():
						request.session['shift_kode'] = x['KD_SHIFT'].strip()
						request.session['shift_nama'] = x['NAMA_SHIFT'].strip()
						shift_tanggal = str(x['TGL_SHIFT'])
						request.session['shift_tanggal'] = shift_tanggal[0:10].strip()
						request.session['shift_counter'] = x['COUNTER']
						request.session['shift_next'] = x['SHIFT_NEW'].strip()

				qcabang = 'SELECT TOP 1 * FROM CABANG'
				datares = Globals().getData(qcabang);
				request.session['id_cabang'] = datares[0]['CABANG_ID']
				request.session['kota_cabang'] = datares[0]['KOTA']
				request.session['nama_cabang'] = datares[0]['PERUSAHAAN']
				request.session['alamat_cabang'] = datares[0]['ALAMAT1']
				request.session['TARIPEMBALAGE'] = float(datares[0]['TARIPEMBALAGE'])
				# parameter
				qparameter= 'SELECT TOP 1 * FROM PARAMETER'
				datares = Globals().getData(qparameter);
				
				request.session['par_ppn'] = float(datares[0]['PPN'])


				q6 = "select case when MTH =1 then 'Januari'  "
				q6 +="when MTH =2 then 'Pebruari' "
				q6 +="when MTH =3 then 'Maret' "
				q6 +="when MTH =4 then 'April' "
				q6 +="when MTH =5 then 'Mei' "
				q6 +="when MTH =6 then 'Juni' "
				q6 +="when MTH =7 then 'Juli' "
				q6 +="when MTH =8 then 'Agustus' "
				q6 +="when MTH =9 then 'September' "
				q6 +="when MTH =10 then 'Oktober' "
				q6 +="when MTH =11 then 'Nopember' "
				q6 +="else 'Desember' end as MTH,YR  from parameter "
				datares = Globals().getData(q6);
				request.session['par_MTH'] = datares[0]['MTH']
				request.session['par_TAHUNYR'] = datares[0]['YR']



				request.session.modified = True

				# response = render(request, 'layout/base.html', {'user_id':user_privelege})

				return redirect('/')
			else:
				response = render(request, 'login.html', 
                       {'invalid': True })
				messages.add_message(request, messages.INFO, 'Username atau password Anda salah')
	response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
	return response

def logout(request):
	request.session['userauth'] = False
	request.session.clear()
	return redirect('/login')

def checkLogin(username, password):
    cursor = connection.cursor()
    q = "select * from USERSPRIV where USER_ID=%s and USER_PASSWORD=%s"
    cursor.execute(q, [username, password])
    result = Globals().dictfetchall(cursor)

    if len(result) == 0:
        return None
    else:
        return DictX(result[0])




