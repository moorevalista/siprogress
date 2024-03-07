from django.shortcuts import redirect, render
from siprogress.globals import Globals

# edit juan start
from django.http import HttpResponse
from django.db import connection
from django.core.serializers.json import DjangoJSONEncoder
import json
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# edit juan end

# Create your views here.
def dashboard(request):
	# Check Session
	# print('masuk')
	is_login = checkLogin(request)

	# Code
	# print(user_priv)
	if(is_login[0]):
		# print(user_priv)
		#select name,icon,url from PRIVILEGE_MODUL, PROPERTIES_MENU where PRIVILEGE_MODUL.MENU_PRIV = PROPERTIES_MENU.id;
		qnavbar = "SELECT * FROM PRIVILEGE_NAVBAR A\
					RIGHT JOIN PROPERTIES_NAVBAR B ON A.NAVBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' ORDER BY B.parent ASC, B.nav_order ASC;"
		
		qmenubar = "SELECT * FROM PRIVILEGE_MENUBAR AS A\
					RIGHT JOIN PROPERTIES_MENUBAR AS B ON A.MENUBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' AND B.submodul is null order by id asc;"
		
		navbars = Globals().getData(qnavbar)
		menubars = Globals().getData(qmenubar)
		# print(navbars)
		#query = "select CAST(Privilege as varchar) as priv from TbPrivilege where PrivilegeId = '"+user_priv+"'"
		#cursor = connection.cursor()
		#cursor.execute(query)
		#results = dictfetchall(cursor)  
		#response = render(request, 'dashboard/home.html', {'results':results})
		response = render(request, 'dashboard/home.html', {'navbars':navbars, 'menubars':menubars})
		response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
		return response
	else:
		return redirect('/login')
	
# edit juan start
	
def dictfetchall(cursor):
    # "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
	
def checkLogin(request):
	if 'userauth' in request.session:
		is_login = request.session['userauth']
		user_priv = request.session['user_priv']
	else:
		is_login = False
		user_priv = None
	
	return [is_login, user_priv]
	
def divisi(request):
	is_login = checkLogin(request)

	if(is_login[0]):
		qnavbar = "SELECT * FROM PRIVILEGE_NAVBAR A\
					RIGHT JOIN PROPERTIES_NAVBAR B ON A.NAVBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' ORDER BY B.parent ASC, B.nav_order ASC;"
		
		qmenubar = "SELECT * FROM PRIVILEGE_MENUBAR AS A\
					RIGHT JOIN PROPERTIES_MENUBAR AS B ON A.MENUBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' AND B.submodul = 'divisi' order by id asc;"
		
		navbars = Globals().getData(qnavbar)
		menubars = Globals().getData(qmenubar)

		response = render(request, 'divisi/home/home.html', {'navbars':navbars, 'menubars':menubars})
		response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
		return response
	else:
		return redirect('/login')
	
def getIdDivisi(request):
	cursor = connection.cursor()
	sql = "EXEC getLastIdDivisi"
	cursor.execute(sql)
	result = []
	result = dictfetchall(cursor)
	json_data = json.dumps(result, cls=DjangoJSONEncoder)
	cursor.close()

	return HttpResponse(json_data, content_type="application/json")

def getDivisi(request):
	cursor = connection.cursor()
	sql = "SELECT mddivisi_id as kode_divisi, mddivisi_name as nama_divisi, (CASE WHEN status = 1 THEN 'Aktif' ELSE 'Tidak Aktif' END) AS status FROM MDDIVISI"
	cursor.execute(sql)
	result = []
	result = dictfetchall(cursor)
	json_data = json.dumps(result, cls=DjangoJSONEncoder)
	cursor.close()

	return HttpResponse(json_data, content_type="application/json")

def saveDivisi(request):
	if request.method == 'POST':
		cursor = connection.cursor()
		
		params = (
			request.POST['kode_divisi'],
			request.POST['nama_divisi'],
			request.POST['status'],
			'NULL'
		)
		sql = "EXEC saveDivisi '%s', '%s', %s, '%s'"
		cursor.execute(sql % params)

		res = {
			'status': 'success',
			'message': 'Saved successfully.'
		}
	else:
		res = {
			'status': 'error',
			'message': 'Method tidak diijinkan!'
		}

	json_data = json.dumps(res, cls=DjangoJSONEncoder)
	return HttpResponse(json_data, content_type="application/json")

def deleteDivisi(request):
	if request.method == 'POST':
		cursor = connection.cursor()

		params = (
			request.POST['kode_divisi'],
			'NULL',
			0,
			'D'
		)
		sql = "EXEC saveDivisi '%s', '%s', '%s', '%s'"
		cursor.execute(sql % params)

		res = {
			'status': 'success',
			'message': 'Deleted successfully.'
		}
	else:
		res = {
			'status': 'error',
			'message': 'Method tidak diijinkan!'
		}

	json_data = json.dumps(res, cls=DjangoJSONEncoder)
	return HttpResponse(json_data, content_type="application/json")

def komplain(request):
	is_login = checkLogin(request)

	if(is_login[0]):
		qnavbar = "SELECT * FROM PRIVILEGE_NAVBAR A\
					RIGHT JOIN PROPERTIES_NAVBAR B ON A.NAVBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' ORDER BY B.parent ASC, B.nav_order ASC;"
		
		qmenubar = "SELECT * FROM PRIVILEGE_MENUBAR AS A\
					RIGHT JOIN PROPERTIES_MENUBAR AS B ON A.MENUBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' AND B.submodul = 'komplain' order by id asc;"
		
		navbars = Globals().getData(qnavbar)
		menubars = Globals().getData(qmenubar)

		response = render(request, 'komplain/home/home.html', {'navbars':navbars, 'menubars':menubars})
		response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
		return response
	else:
		return redirect('/login')
	
def getKomplain(request):
	cursor = connection.cursor()
	sql = "SELECT ROW_NUMBER() OVER(ORDER BY MDKOMPLAIN_ID ASC) AS no, *,\
			(\
				CASE\
					WHEN MDSTATUS = '0' THEN 'Belum diproses'\
					WHEN MDSTATUS = '1' THEN 'Diproses'\
					WHEN MDSTATUS = '2' THEN 'Selesai'\
				END\
			) AS status_komplain FROM MDKOMPLAIN"
	cursor.execute(sql)
	result = []
	result = dictfetchall(cursor)
	json_data = json.dumps(result, cls=DjangoJSONEncoder)
	cursor.close()

	return HttpResponse(json_data, content_type="application/json")

def getIdKomplain(request):
	cursor = connection.cursor()
	sql = "EXEC getLastIdKomplain"
	cursor.execute(sql)
	result = []
	result = dictfetchall(cursor)
	json_data = json.dumps(result, cls=DjangoJSONEncoder)
	cursor.close()

	return HttpResponse(json_data, content_type=DjangoJSONEncoder)

def saveKomplain(request):
	if request.method == 'POST':
		cursor = connection.cursor()

		files = request.FILES.getlist('gambarKomplain')
		image_types = ['image/png', 'image/jpg', 'image/jpeg', 'imagepjpeg', 'image/gif']
		img_url = ''

		for file in files:
			if file.content_type not in image_types:
				json_data = json.dumps({'status': 'failed', 'message': _('Bad image format.')})
				return HttpResponse(json_data, content_type=DjangoJSONEncoder)
			
			tmp_file = os.path.join('static/images/uploads/', file.name)
			if os.path.isfile(tmp_file):
				os.remove(tmp_file)
			path = default_storage.save(tmp_file, ContentFile(file.read()))
			img_url = path

		params = (
			request.POST['idKomplain'],
			request.POST['judulKomplain'],
			request.POST['ketKomplain'],
			request.POST['pelaporKomplain'],
			request.POST['pjKomplain'],
			img_url,
			'NULL'
		)
		sql = "EXEC saveKomplain '%s', '%s', '%s', '%s', '%s', '%s', '%s'"
		cursor.execute(sql % params)

		res = {
			'status': 'success',
			'message': 'Saved successfully.'
		}
	else:
		res = {
			'status': 'error',
			'message': 'Method tidak diijinkan!'
		}

	json_data = json.dumps(res, cls=DjangoJSONEncoder)
	return HttpResponse(json_data, content_type="application/json")

def updateStatus(request):
	if request.method == 'POST':
		cursor = connection.cursor()

		sql = "UPDATE MDKOMPLAIN SET MDSTATUS = '%s' WHERE MDKOMPLAIN_ID = '%s'" % (request.POST['status'], request.POST['idKomplain'])
		print(sql)
		cursor.execute(sql)

		res = {
			'status': 'success',
			'message': 'Saved successfully.'
		}
	else:
		res = {
			'status': 'error',
			'message': 'Method tidak diijinkan!'
		}

	json_data = json.dumps(res, cls=DjangoJSONEncoder)
	return HttpResponse(json_data, content_type="application/json")

def deleteKomplain(request):
	if request.method == 'POST':
		cursor = connection.cursor()

		params = (
			request.POST['idKomplain'],
			'NULL',
			'NULL',
			'NULL',
			'NULL',
			'NULL',
			'D'
		)
		sql = "EXEC saveKomplain '%s', '%s', '%s', '%s', '%s', '%s', '%s'"
		cursor.execute(sql % params)

		res = {
			'status': 'success',
			'message': 'Deleted successfully.'
		}
	else:
		res = {
			'status': 'error',
			'message': 'Method tidak diijinkan!'
		}

	json_data = json.dumps(res, cls=DjangoJSONEncoder)
	return HttpResponse(json_data, content_type="application/json")

def listAllKomplain(request):
	is_login = checkLogin(request)

	if(is_login[0]):
		qnavbar = "SELECT * FROM PRIVILEGE_NAVBAR A\
					RIGHT JOIN PROPERTIES_NAVBAR B ON A.NAVBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' ORDER BY B.parent ASC, B.nav_order ASC;"
		
		qmenubar = "SELECT * FROM PRIVILEGE_MENUBAR AS A\
					RIGHT JOIN PROPERTIES_MENUBAR AS B ON A.MENUBAR_PRIV = B.id\
					WHERE A.USER_PRIV = '" + is_login[1] + "'\
					AND B.modul = 'e-komplain' AND B.submodul = 'komplain' order by id asc;"
		
		navbars = Globals().getData(qnavbar)
		menubars = Globals().getData(qmenubar)

		response = render(request, 'dxgridExample/home/home.html', {'navbars':navbars, 'menubars':menubars})
		response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'
		return response
	else:
		return redirect('/login')

def get_list_aduan(request):
    cursor = connection.cursor()
    q = "SELECT ROW_NUMBER() OVER(ORDER BY EKANO_TRANSAKSI ASC) AS no, * FROM EKOMPLEN_ADUAN where EKA_DELETED IS NULL"
    cursor.execute(q)
    result_set = Globals().dictfetchall(cursor)
    json_data = json.dumps(result_set, cls=DjangoJSONEncoder)
    cursor.close()

    return HttpResponse(json_data, content_type="application/json")

def deleteAduan(request):
	if request.method == 'POST':
		cursor = connection.cursor()

		sql = "DELETE FROM EKOMPLEN_ADUAN WHERE EKANO_TRANSAKSI = '%s'" % (request.POST['idAduan'])
		cursor.execute(sql)

		res = {
			'status': 'success',
			'message': 'Deleted successfully.'
		}
	else:
		res = {
			'status': 'error',
			'message': 'Method tidak diijinkan!'
		}

	json_data = json.dumps(res, cls=DjangoJSONEncoder)
	return HttpResponse(json_data, content_type="application/json")

# edit juan end